import json, sys, numpy as np, librosa, scipy.signal as sg
from pathlib import Path
REPO=Path('/workspace/nj-design-w2'); STEMS=Path('/workspace/w2-stems/htdemucs')
SR=22050; HOP=128
def fr2t(f): return librosa.frames_to_time(f, sr=SR, hop_length=HOP)
def band_env(y, lo, hi):
    S=np.abs(librosa.stft(y,n_fft=1024,hop_length=HOP)); fq=librosa.fft_frequencies(sr=SR,n_fft=1024)
    m=(fq>=lo)&(fq<hi); e=librosa.amplitude_to_db(S[m]+1e-6,ref=np.max)
    env=np.maximum(0,np.diff(e,axis=1)).mean(0); env=np.concatenate([[0],env])
    return env/(env.max()+1e-9)
def picks(env, delta, wait=8):
    p=librosa.util.peak_pick(env,pre_max=3,post_max=3,pre_avg=12,post_avg=12,delta=delta,wait=wait)
    return [[round(float(fr2t(i)),4), round(float(env[i]),3)] for i in p]
def refine_attack(y, t, win=0.04):
    # find steepest energy rise within +-win of t on a 2ms rms envelope
    a=int(max(0,(t-win)*SR)); b=int(min(len(y),(t+win)*SR))
    seg=y[a:b]**2
    if len(seg)<100: return t
    k=int(0.002*SR); e=np.convolve(seg,np.ones(k)/k,'same'); d=np.diff(np.sqrt(e))
    return (a+int(np.argmax(d)))/SR
def main(slug):
    y,_=librosa.load(REPO/f'public/audio/{slug}.mp3',sr=SR,mono=True); dur=len(y)/SR
    stems={}
    for s in ['drums','bass','vocals','other']:
        p=STEMS/slug/f'{s}.wav'
        if p.exists(): stems[s],_=librosa.load(p,sr=SR,mono=True)
    if not stems:
        H,P=librosa.effects.hpss(y,margin=2.0); stems={'drums':P,'other':H}
    full=librosa.onset.onset_strength(y=y,sr=SR,hop_length=HOP); fulln=full/full.max()
    tempo,beats=librosa.beat.beat_track(onset_envelope=full,sr=SR,hop_length=HOP,tightness=300)
    bt=fr2t(beats)
    # linear grid fit with outlier rejection
    idx=np.arange(len(bt)); T=60/float(np.atleast_1d(tempo)[0])
    # unwrap indices by actual spacing
    idx=np.concatenate([[0],np.cumsum(np.round(np.diff(bt)/T))]).astype(int)
    for _ in range(4):
        A=np.vstack([idx,np.ones_like(idx)]).T; sol,_,_,_=np.linalg.lstsq(A,bt,rcond=None)
        res=bt-(A@sol); keep=np.abs(res)<max(0.03,2.5*np.std(res))
        idx,bt=idx[keep],bt[keep]
    T,t0=sol; bpm=60/T
    # phase refine against drums/full onset env (sub-frame search)
    ref = stems.get('drums', y); env = librosa.onset.onset_strength(y=ref,sr=SR,hop_length=HOP); env/=env.max()
    best=None
    for dt in np.arange(-0.03,0.0301,0.002):
        g=t0+dt+T*np.arange(-int(t0/T)-1, int(dur/T)+2); g=g[(g>0)&(g<dur)]
        sc=env[np.clip(librosa.time_to_frames(g,sr=SR,hop_length=HOP),0,len(env)-1)].sum()
        if best is None or sc>best[0]: best=(sc,dt)
    t0+=best[1]
    first=t0-T*int(t0/T)
    grid=first+T*np.arange(0,int((dur-first)/T)+1)
    out=dict(id=slug,duration=round(dur,4),bpm=round(bpm,3),beat_period=round(T,5),beat0=round(first,4),
             grid_fit_residual_ms=round(float(np.std(res[keep])*1000),1),beats=[round(float(b),4) for b in grid])
    out['onsets_full']=picks(fulln,0.06)
    if 'drums' in stems:
        d=stems['drums']
        out['kick']=picks(band_env(d,30,130),0.10); out['snare']=picks(band_env(d,1200,6000),0.10); out['hat']=picks(band_env(d,7000,11000),0.12)
        de=librosa.onset.onset_strength(y=d,sr=SR,hop_length=HOP); out['drums']=picks(de/de.max(),0.06)
    for s in ['bass','vocals','other']:
        if s in stems:
            e=librosa.onset.onset_strength(y=stems[s],sr=SR,hop_length=HOP); out[s]=picks(e/e.max(),0.07)
    # refine attack times of drum/vocal onsets on raw stem
    for key,src in [('kick','drums'),('snare','drums'),('drums','drums'),('vocals','vocals'),('bass','bass'),('other','other'),('onsets_full',None)]:
        if key in out:
            yy=stems[src] if src else y
            out[key]=[[round(refine_attack(yy,t,0.025),4),s] for t,s in out[key]]
    # per-beat activity / energy
    def rms_per(yy, edges):
        return [float(np.sqrt(np.mean(yy[int(a*SR):int(b*SR)]**2))) if b>a else 0 for a,b in zip(edges[:-1],edges[1:])]
    bars=grid[::1]
    out['beat_rms']={k:[round(v,4) for v in rms_per(stems.get(k,y),np.append(grid,dur))] for k in ['drums','bass','vocals','other'] if k in stems}
    out['beat_rms']['mix']=[round(v,4) for v in rms_per(y,np.append(grid,dur))]
    # structural novelty at beat level
    chroma=librosa.feature.chroma_cqt(y=y,sr=SR,hop_length=512); mf=librosa.feature.mfcc(y=y,sr=SR,hop_length=512,n_mfcc=13)
    F=np.vstack([librosa.util.normalize(chroma),librosa.util.normalize(mf)])
    bf=librosa.time_to_frames(grid,sr=SR,hop_length=512); F=librosa.util.sync(F,bf)
    R=librosa.segment.recurrence_matrix(F,mode='affinity',width=4,sym=True)
    k=16; nov=np.zeros(F.shape[1])
    from scipy.ndimage import gaussian_filter
    ker=np.outer(np.r_[-np.ones(k),np.ones(k)],np.r_[-np.ones(k),np.ones(k)])*-1
    Rf=np.pad(R.astype(float),k)
    for i in range(F.shape[1]): nov[i]=(Rf[i:i+2*k,i:i+2*k]*ker).sum()
    out['novelty_beat']=[round(float(v),3) for v in nov]
    Path(f'/workspace/w2-work/{slug}.json').write_text(json.dumps(out))
    print(slug,'dur',round(dur,2),'bpm',round(bpm,3),'beat0',round(first,4),'res_ms',out['grid_fit_residual_ms'],{k:len(out[k]) for k in ['kick','snare','vocals','bass','other'] if k in out})
for s in sys.argv[1:]: main(s)
