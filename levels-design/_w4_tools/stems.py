import numpy as np, librosa, json, sys, scipy.signal as ss
slug=sys.argv[1]; d=f'/workspace/w4/stems/htdemucs/{slug}'
sr=22050; hop=256; fps=sr/hop
out={}
def load(n): return librosa.load(f'{d}/{n}.wav',sr=sr,mono=True)[0]
def env_band(y,lo,hi):
    S=np.abs(librosa.stft(y,n_fft=1024,hop_length=hop)); f=librosa.fft_frequencies(sr=sr,n_fft=1024)
    m=(f>=lo)&(f<hi)
    return librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[m],ref=np.max),sr=sr,hop_length=hop,lag=1,max_size=3)
dr=load('drums'); vo=load('vocals'); ba=load('bass'); ot=load('other')
E=dict(kick=env_band(dr,30,140), snare=env_band(dr,1200,5000), hat=env_band(dr,7000,11000),
       vocal=librosa.onset.onset_strength(y=vo,sr=sr,hop_length=hop), bass=librosa.onset.onset_strength(y=ba,sr=sr,hop_length=hop),
       other=librosa.onset.onset_strength(y=ot,sr=sr,hop_length=hop))
R=dict(vocal_rms=librosa.feature.rms(y=vo,hop_length=hop)[0], drums_rms=librosa.feature.rms(y=dr,hop_length=hop)[0],
       bass_rms=librosa.feature.rms(y=ba,hop_length=hop)[0], other_rms=librosa.feature.rms(y=ot,hop_length=hop)[0])
np.savez_compressed(f'{slug}.stems.npz',**E,**R)
pk={}
for k,e in E.items():
    n=e/(np.percentile(e,99.5)+1e-9)
    fr,pr=ss.find_peaks(n,prominence=0.15,distance=5)
    pk[k]=[[round(fr_/fps,3),round(float(min(n[fr_],1.5)),3)] for fr_ in fr]
json.dump(pk,open(f'{slug}.stem_onsets.json','w'))
print(slug,{k:len(v) for k,v in pk.items()})
