import sys, json, numpy as np, librosa, scipy.signal as ss
slug=sys.argv[1]; prior=float(sys.argv[2])
path=f'/workspace/nj-design-w1/public/audio/{slug}.mp3'
sr=22050; HOP=256
y,_=librosa.load(path,sr=sr,mono=True)
dur=len(y)/sr
yh,yp=librosa.effects.hpss(y,margin=2.0)
def env(sig,fmin,fmax):
    S=np.abs(librosa.stft(sig,n_fft=2048,hop_length=HOP))
    f=librosa.fft_frequencies(sr=sr,n_fft=2048); m=(f>=fmin)&(f<fmax)
    M=librosa.amplitude_to_db(S[m]+1e-9)
    o=np.maximum(0,np.diff(M,axis=1)).mean(0); o=np.concatenate([[0],o])
    return o/(np.percentile(o,99)+1e-9)
oenv=librosa.onset.onset_strength(y=y,sr=sr,hop_length=HOP)
kick=env(yp,30,150); snare=env(yp,1500,8000); hat=env(yp,8000,11000)
bass=env(yh,40,250); vocal=env(yh,300,3400)
times=librosa.frames_to_time(np.arange(len(oenv)),sr=sr,hop_length=HOP)
tempo=prior; bt=np.array([])
fps=sr/HOP; best=None
for bpm in np.arange(prior-4,prior+4,0.01):
  p=60/bpm; ns=np.arange(0,dur-0.5,p)
  for off in np.arange(0,p,0.004):
    fr=np.clip(((ns+off)*fps).round().astype(int),0,len(oenv)-1)
    sc=oenv[fr].mean()
    if best is None or sc>best[0]: best=(sc,p,off)
_,per,ph=best
ph=ph%per
grid=np.arange(ph,dur,per)
def peaks(e,thr,dist=0.07):
    pk,pr=ss.find_peaks(e,height=thr,distance=max(1,int(dist*sr/HOP)))
    return [[round(float(times[i]),3),round(float(e[i]),3)] for i in pk]
on=librosa.onset.onset_detect(onset_envelope=oenv,sr=sr,hop_length=HOP,backtrack=False,units='time')
# rms & structure
rms=librosa.feature.rms(y=y,hop_length=HOP)[0]
bf=librosa.time_to_frames(grid,sr=sr,hop_length=HOP)
chroma=librosa.feature.chroma_cqt(y=yh,sr=sr,hop_length=HOP)
mfcc=librosa.feature.mfcc(y=y,sr=sr,hop_length=HOP,n_mfcc=13)
F=np.vstack([librosa.util.normalize(chroma),librosa.util.normalize(mfcc)])
Fs=librosa.util.sync(F,bf)
R=librosa.segment.recurrence_matrix(Fs,mode='affinity',sym=True,width=3)
# novelty via checkerboard
def novelty(S,k=16):
    n=S.shape[0]; g=np.outer(np.r_[np.ones(k),-np.ones(k)],np.r_[np.ones(k),-np.ones(k)])
    g=g*np.outer(ss.windows.gaussian(2*k,k/2),ss.windows.gaussian(2*k,k/2))
    Sp=np.pad(S,k); return np.array([np.sum(Sp[i:i+2*k,i:i+2*k]*g) for i in range(n)])
nov=novelty(R)
npk,_=ss.find_peaks(nov,distance=12,prominence=np.std(nov)*0.5)
bounds=[round(float(grid[min(i,len(grid)-1)]),3) for i in npk]
# per-beat energy
rms_b=librosa.util.sync(rms[None],bf)[0]
def bandbeat(e): return [round(float(x),3) for x in librosa.util.sync(e[None],bf)[0]]
out=dict(slug=slug,duration=round(dur,3),sr=sr,hop=HOP,
 tempo_librosa=float(np.atleast_1d(tempo)[0]),beat_period=round(float(per),5),bpm=round(60/per,3),grid_phase=round(float(ph),4),
 beats_librosa=[round(float(t),3) for t in bt],
 onsets_all=[round(float(t),3) for t in on],
 kick_peaks=peaks(kick,0.35),snare_clap_peaks=peaks(snare,0.35),hat_peaks=peaks(hat,0.4,0.05),
 bass_peaks=peaks(bass,0.35),vocal_band_peaks=peaks(vocal,0.3),
 structure_boundaries_auto=bounds,
 rms_per_beat=[round(float(x),4) for x in rms_b],
 kick_per_beat=bandbeat(kick),snare_per_beat=bandbeat(snare),vocal_per_beat=bandbeat(vocal))
json.dump(out,open(f'/workspace/nj-w1-work/{slug}.analysis.json','w'))
np.savez_compressed(f'/workspace/nj-w1-work/{slug}.env.npz',times=times,oenv=oenv/np.percentile(oenv,99),kick=kick,snare=snare,hat=hat,bass=bass,vocal=vocal,rms=rms)
print(slug,round(dur,2),'bpm',round(60/per,3),'phase',round(ph,3),'bounds',bounds)
