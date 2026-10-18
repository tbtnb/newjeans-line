import sys, json, numpy as np, librosa, scipy.signal as ss
from paths import *
slug=sys.argv[1]
path=f'{AUDIO}/{slug}.mp3'
sr=22050; hop=256
y,_=librosa.load(path,sr=sr,mono=True)
dur=len(y)/sr
H,P=librosa.effects.hpss(y,margin=2.0)
S=np.abs(librosa.stft(y,n_fft=2048,hop_length=hop))
SP=np.abs(librosa.stft(P,n_fft=2048,hop_length=hop))
SH=np.abs(librosa.stft(H,n_fft=2048,hop_length=hop))
freqs=librosa.fft_frequencies(sr=sr,n_fft=2048)
def band_flux(M,lo,hi):
    m=(freqs>=lo)&(freqs<hi)
    X=np.log1p(100*M[m])
    f=np.maximum(0,np.diff(X,axis=1)).sum(0)
    f=np.concatenate([[0],f]); f=f/ (np.percentile(f,99)+1e-9)
    return f
times=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=hop)
full_env=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
full_env=full_env/(np.percentile(full_env,99)+1e-9)
kick=band_flux(SP,30,150); snare=band_flux(SP,1500,6000); hat=band_flux(SP,7000,11000)
bass=band_flux(SH,40,250); vox=band_flux(SH,300,3000)
tempo,beats=librosa.beat.beat_track(onset_envelope=full_env*1.0,sr=sr,hop_length=hop,units='time',tightness=200)
tempo=float(np.atleast_1d(tempo)[0])
def peaks(env,thr,dist_s=0.07):
    p,_=ss.find_peaks(env,height=thr,distance=max(1,int(dist_s*sr/hop)))
    return [{'t':round(float(times[i]),3),'s':round(float(env[i]),3)} for i in p]
onsets=librosa.onset.onset_detect(onset_envelope=full_env,sr=sr,hop_length=hop,units='frames',backtrack=False)
ons=[{'t':round(float(times[i]),3),'s':round(float(full_env[i]),3)} for i in onsets]
chroma=librosa.feature.chroma_stft(y=H,sr=sr,hop_length=hop*2)
mfcc=librosa.feature.mfcc(y=y,sr=sr,hop_length=hop*2,n_mfcc=13)
rms=librosa.feature.rms(y=y,hop_length=hop*2)[0]
bf=librosa.time_to_frames(beats,sr=sr,hop_length=hop*2)
F=np.vstack([librosa.util.normalize(chroma,axis=0),mfcc/ (np.std(mfcc,axis=1,keepdims=True)+1e-9),rms[None]/rms.max()*4])
Fs=librosa.util.sync(F,bf,aggregate=np.median)
def novelty(Fs,k=8):
    D=1-np.corrcoef(Fs.T); n=D.shape[0]
    g=np.outer(np.r_[-np.ones(k),np.ones(k)],np.r_[-np.ones(k),np.ones(k)])
    nov=np.zeros(n); Dp=np.pad(D,k,mode='edge')
    for i in range(n): nov[i]=-(Dp[i:i+2*k,i:i+2*k]*g).sum()
    return nov
nov=novelty(Fs)
bt=np.r_[0,beats]
pk,_=ss.find_peaks(nov,distance=12,prominence=np.std(nov)*0.5)
bounds=sorted(set([round(float(bt[min(i,len(bt)-1)]),3) for i in pk]))
rb=librosa.util.sync(rms[None],bf,aggregate=np.mean)[0]
out=dict(slug=slug,duration=round(dur,3),tempo=round(tempo,3),beats=[round(float(b),3) for b in beats],
  onsets=ons,kick=peaks(kick,0.35),snare=peaks(snare,0.35),hat=peaks(hat,0.4,0.05),bass=peaks(bass,0.35),vocal=peaks(vox,0.35),
  novelty_bounds=bounds,beat_rms=[round(float(v),4) for v in rb])
json.dump(out,open(f'{WORK}/{slug}.raw.json','w'))
print(slug,dur,tempo,len(beats),'onsets',len(ons),'bounds',bounds)
