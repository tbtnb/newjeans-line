import librosa, numpy as np, json, sys, scipy.signal as ss
slug=sys.argv[1]; bpm_hint=float(sys.argv[2])
path=f'/workspace/nj-design-w4/public/audio/{slug}.mp3'
y,sr=librosa.load(path,sr=22050,mono=True)
dur=len(y)/sr
hop=256
H,P=librosa.effects.hpss(y,margin=(1.0,2.0))
def band(sig,lo,hi):
    S=np.abs(librosa.stft(sig,n_fft=1024,hop_length=hop))
    f=librosa.fft_frequencies(sr=sr,n_fft=1024)
    m=(f>=lo)&(f<hi)
    return S[m]
def onset_env_band(sig,lo,hi):
    S=band(sig,lo,hi)
    return librosa.onset.onset_strength(S=librosa.amplitude_to_db(S,ref=np.max),sr=sr,hop_length=hop)
env_all=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
env_kick=onset_env_band(P,30,150)
env_snare=onset_env_band(P,1500,6000)
env_hat=onset_env_band(P,6000,11000)
env_bass=onset_env_band(H,30,200)
env_voc=onset_env_band(H,300,3000)
fps=sr/hop
oe=env_all/ (env_all.std()+1e-9)
# refine tempo near hint by autocorrelation
ac=np.correlate(oe-oe.mean(),oe-oe.mean(),'full')[len(oe)-1:]
cands=np.arange(bpm_hint*0.97,bpm_hint*1.03,0.01)
sc=[np.interp(60*fps/b,np.arange(len(ac)),ac)+0.5*np.interp(120*fps/b,np.arange(len(ac)),ac)+0.5*np.interp(240*fps/b,np.arange(len(ac)),ac) for b in cands]
tempo=float(cands[int(np.argmax(sc))])
period=60*fps/tempo
# Ellis DP
n=len(oe); score=oe.copy(); back=-np.ones(n,int)
lo,hi=int(round(period*0.8)),int(round(period*1.25))
for i in range(hi,n):
    prev=np.arange(i-hi,i-lo+1)
    pen=-400*(np.log((i-prev)/period))**2
    v=score[prev]+pen
    j=int(np.argmax(v)); score[i]=oe[i]+v[j]; back[i]=prev[j]
i=int(np.argmax(score[-int(period*2):]))+n-int(period*2)
bl=[]
while i>=0: bl.append(i); i=back[i]
beats=np.array(bl[::-1])
bt=librosa.frames_to_time(beats,sr=sr,hop_length=hop)
def peaks(env,delta=0.12,wait=6):
    e=env/ (np.percentile(env,99)+1e-9)
    fr,_=ss.find_peaks(e,prominence=delta,distance=wait)
    t=librosa.frames_to_time(fr,sr=sr,hop_length=hop)
    s=e[fr]
    return [[round(float(a),3),round(float(min(b,2.0)),3)] for a,b in zip(t,s)]
on={k:peaks(v) for k,v in dict(all=env_all,kick=env_kick,snare=env_snare,hat=env_hat,bass=env_bass,vocal=env_voc).items()}
# sections: beat-synced features, novelty
C=librosa.feature.chroma_cqt(y=H,sr=sr,hop_length=hop)
M=librosa.feature.mfcc(y=y,sr=sr,hop_length=hop,n_mfcc=13)
rms=librosa.feature.rms(y=y,hop_length=hop)[0]
F=np.vstack([librosa.util.normalize(C,axis=0),M/ (np.std(M,axis=1,keepdims=True)+1e-9)*0.5])
Fs=librosa.util.sync(F,beats)
# checkerboard novelty on self-similarity
S=np.corrcoef(Fs.T); S=np.nan_to_num(S)
L=16
g=np.outer(ss.windows.gaussian(2*L,L/2),ss.windows.gaussian(2*L,L/2))
k=np.block([[np.ones((L,L)),-np.ones((L,L))],[-np.ones((L,L)),np.ones((L,L))]])*g
n=len(S); nov=np.zeros(n)
Sp=np.pad(S,L,mode='edge')
for i in range(n): nov[i]=np.sum(Sp[i:i+2*L,i:i+2*L]*k)
nov=np.maximum(nov,0)
pk,_=ss.find_peaks(nov,distance=12,prominence=np.percentile(nov,70)*0.3)
bounds=[round(float(bt[min(p,len(bt)-1)]),3) for p in pk]
seg_k=librosa.segment.agglomerative(Fs,14)
agg=[round(float(bt[min(b,len(bt)-1)]),3) for b in seg_k]
# energy per beat
rms_b=librosa.util.sync(rms[None,:],beats)[0]
out=dict(slug=slug,duration=round(dur,3),tempo=float(np.atleast_1d(tempo)[0]),beats=[round(float(x),3) for x in bt],
  beat_rms=[round(float(x),4) for x in rms_b],onsets=on,novelty_bounds=bounds,agglomerative_bounds=agg,
  rms_1s=[round(float(np.mean(rms[int(i*sr/hop):int((i+1)*sr/hop)])),4) for i in range(int(dur))],
  method="librosa %s; HPSS(margin 1,2); band onset envs on percussive (kick 30-150Hz, snare/clap 1.5-6k, hat 6-11k) and harmonic (bass 30-200, vocal-band 300-3k proxy); beat_track tightness 400 with tempo hint; checkerboard novelty (L=16 beats) + agglomerative(14) for section candidates"%librosa.__version__)
np.savez_compressed(f'/workspace/w4/{slug}.env.npz',all=env_all,kick=env_kick,snare=env_snare,hat=env_hat,bass=env_bass,vocal=env_voc,rms=rms,beats=bt,sr=sr,hop=hop)
json.dump(out,open(f'/workspace/w4/{slug}.analysis.raw.json','w'))
print(slug,dur,out['tempo'],len(bt),'bounds',bounds)
print('agg',agg)
print('rms per 2s',[round(float(np.mean(out['rms_1s'][i:i+2])),2) for i in range(0,int(dur),2)])
