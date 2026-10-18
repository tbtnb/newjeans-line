import sys,json,numpy as np,librosa,scipy.signal as ss
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=sys.argv[1]; sr=22050; HOP=256; fps=sr/HOP
a=json.load(open(f'{s}.analysis.json'))
v,_=librosa.load(f'sep/htdemucs/{s}/vocals.mp3',sr=sr)
nv,_=librosa.load(f'sep/htdemucs/{s}/no_vocals.mp3',sr=sr)
nh,npc=librosa.effects.hpss(nv,margin=2.0)
def band(sig,lo,hi):
    S=np.abs(librosa.stft(sig,n_fft=2048,hop_length=HOP)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    M=librosa.amplitude_to_db(S[(f>=lo)&(f<hi)]+1e-9); o=np.maximum(0,np.diff(M,axis=1)).mean(0)
    o=np.concatenate([[0],o]); return o/(np.percentile(o,99.5)+1e-9), S[(f>=lo)&(f<hi)].sum(0)
vo,ve=band(v,150,5000)
vrms=librosa.feature.rms(y=v,hop_length=HOP)[0]
ko,ke=band(npc,30,140); so,se=band(npc,1200,8000); mo,me=band(nh,200,4000); bo,be=band(nh,30,200)
L=min(map(len,[vo,ko,so,mo,bo,vrms]))
np.savez_compressed(f'{s}.stems.npz',vocal_on=vo[:L],vocal_rms=vrms[:L],kick_on=ko[:L],snare_on=so[:L],mel_on=mo[:L],bass_on=bo[:L],kick_e=ke[:L],bass_e=be[:L])
t=np.arange(L)/fps
def sm(x,w=1.0): k=int(w*fps); return np.convolve(x,np.ones(k)/k,'same')
fig,ax=plt.subplots(5,1,figsize=(26,12),sharex=True)
for axx,(nm,x) in zip(ax,[('vocal rms',vrms[:L]),('vocal onset',vo[:L]),('kick',ko[:L]),('snare/clap',so[:L]),('bass e',be[:L])]):
    axx.plot(t,sm(x,0.5),lw=0.8); axx.set_ylabel(nm)
    p=a['beat_period']; ph=a['grid_phase']
    for b in np.arange(ph,a['duration'],p*16): axx.axvline(b,color='r',lw=0.5)
    for b in np.arange(ph,a['duration'],p*4): axx.axvline(b,color='0.85',lw=0.3)
    for b in a['structure_boundaries_auto']: axx.axvline(b,color='g',ls='--',lw=0.8)
ax[-1].set_xticks(np.arange(0,a['duration'],5))
fig.tight_layout(); fig.savefig(f'{s}.overview.png',dpi=60)
print('ok',s)
