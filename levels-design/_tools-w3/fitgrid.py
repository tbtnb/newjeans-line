# constant-tempo 16th grid fit + attack calibration + layer bias alignment -> work/<slug>.al.json, work/grids.json
import json,numpy as np,librosa,scipy.signal as ss
from paths import *
res={}
for slug,bpm0 in [('eta',135.0),('cool-with-you',135.0),('asap',130.03),('get-up',120.0)]:
    d=json.load(open(f'{WORK}/{slug}.raw.json'))
    ts=np.array([x['t'] for x in d['onsets']]); ws=np.array([x['s'] for x in d['onsets']])
    best=None
    for bpm in np.arange(bpm0-0.3,bpm0+0.3,0.0005):
        per=60/bpm/4
        z=(ws*np.exp(2j*np.pi*ts/per)).sum()/ws.sum()
        if best is None or abs(z)>best[0]: best=(abs(z),bpm,np.angle(z))
    r,bpm,a=best; per16=60/bpm/4; ph=(a/(2*np.pi))*per16 % per16
    drift=[]
    for w0 in range(0,int(d['duration'])-20,20):
        m=(ts>=w0)&(ts<w0+20)
        if m.sum()<10: continue
        z=(ws[m]*np.exp(2j*np.pi*(ts[m]-ph)/per16)).sum()/ws[m].sum()
        drift.append((w0,round(float(np.angle(z)/(2*np.pi)*per16*1000),1),round(float(abs(z)),2)))
    y,sr=librosa.load(f'{AUDIO}/{slug}.mp3',sr=22050)
    e=np.sqrt(ss.lfilter(np.ones(44)/44,1,y**2)); le=20*np.log10(e+1e-6); le=ss.lfilter(np.ones(66)/66,1,le)
    der=np.diff(le); offs=[]
    for t,s in zip(ts,ws):
        if s<0.6: continue
        g=ph+round((t-ph)/per16)*per16
        a_=int((g-0.045)*sr); b_=int((g+0.045)*sr)
        if a_<0 or b_>=len(der): continue
        k=np.argmax(der[a_:b_])
        if der[a_+k]>0.05: offs.append((a_+k)/sr-0.0025-g)
    cal=float(np.median(offs))
    g=dict(bpm=round(float(bpm),4),per16=per16,phase_onset=round(float(ph),4),attack_cal_ms=round(cal*1000,1),phase=round(float(ph+cal),4),resultant=round(float(r),3),drift_ms_per20s=drift)
    g['layer_shift_ms']={}
    for L in ['onsets','kick','snare','hat','bass','vocal']:
        t2=np.array([x['t'] for x in d[L]]); w2=np.array([x['s'] for x in d[L]]); m=w2>0.5
        z=(w2[m]*np.exp(2j*np.pi*(t2[m]-g['phase'])/per16)).sum()/w2[m].sum(); sh=np.angle(z)/(2*np.pi)*per16
        g['layer_shift_ms'][L]=(round(float(sh*1000),1),round(float(abs(z)),2))
        if abs(z)>0.15:
            for x in d[L]: x['t']=round(x['t']-sh,4)
    d['grid']=g; json.dump(d,open(f'{WORK}/{slug}.al.json','w')); res[slug]=g
    print(slug,g['bpm'],'phase',g['phase'],'cal',g['attack_cal_ms'],'R',g['resultant'])
json.dump(res,open(f'{WORK}/grids.json','w'),indent=1)
