# Builds the hand-composed tap list from per-section 16th-position motifs (configs.py).
# A motif position is kept only if a real event (aligned onset/kick/snare/vocal/bass/hat) lies within +-35 ms.
import json,sys,numpy as np
from configs import CONFIGS
from paths import *
LAYERS=['kick','snare','hat','bass','vocal','onsets']
def run(slug):
    C=CONFIGS[slug]; d=json.load(open(f'{WORK}/{slug}.al.json')); G=d['grid']; PER=G['per16']; T0=G['phase']+C['db']*PER
    idx={L:(np.array([x['t'] for x in d[L]]),np.array([x['s'] for x in d[L]])) for L in LAYERS}
    def S(L,t,w=0.035):
        ts,ss=idx[L]; m=np.abs(ts-t)<w
        return float(ss[m].max()) if m.any() else 0.0
    taps=[]
    for sec in C['sections']:
        a,z=sec['bars']
        for bar in range(a,z):
            t0=T0+bar*16*PER; j=bar-a; plen=sec.get('phrase',4)
            pats=sec['motif']; pat=pats[j%len(pats)]
            if sec.get('fillpat') and j%plen==plen-1: pat=sec['fillpat']
            if sec.get('lastpat') and bar==z-1: pat=sec['lastpat']
            if bar in sec.get('override',{}): pat=sec['override'][bar]
            for k in pat:
                t=t0+k*PER
                real=max(S(L,t) for L in ['onsets','kick','snare','vocal','bass','hat'])
                if real<sec.get('minS',0.2): continue
                tag=max(['kick','snare','vocal','bass','hat'],key=lambda L:S(L,t,0.03)*(1.15 if L in('kick','snare') else 1))
                taps.append(dict(t=round(t,3),grid=round(float(t),3),pos=f'{bar}:{k}',tag=tag,sec=sec['label']))
    taps.sort(key=lambda x:x['t'])
    mg=C.get('mingap',0.2); out=[]
    for tp in taps:
        if out and tp['t']-out[-1]['t']<mg: continue
        out.append(tp)
    # 16th-note bursts (v2 steering 11:48): extra taps only where a real 16th event exists (+-25 ms, strength >= burstS)
    for sec in C['sections']:
        for bar,ks in sec.get('burst',{}).items():
            for k in ks:
                t=T0+(bar*16+k)*PER
                st={L:S(L,t,0.025) for L in ['snare','hat','onsets','vocal','kick']}
                L_=max(st,key=st.get)
                if st[L_]<sec.get('burstS',0.5): print('  burst dropped (no event)',bar,k); continue
                if any(abs(tp['t']-t)<0.1 for tp in out): continue
                out.append(dict(t=round(t,3),grid=round(float(t),3),pos=f'{bar}:{k}',tag=L_ if L_!='onsets' else 'fx',sec=sec['label'],burst=True))
    out.sort(key=lambda x:x['t'])
    out=[tp for tp in out if 1.0<=tp['t']<=d['duration']-1.0]
    return out,d
if __name__=='__main__':
    for slug in sys.argv[1:]:
        taps,d=run(slug)
        json.dump(taps,open(f'{WORK}/{slug}.taps.json','w'),indent=0)
        C=CONFIGS[slug]; g=np.diff([t['t'] for t in taps])
        print(slug,'taps',len(taps),'old',C['old'],'ratio',round(len(taps)/C['old'],2),'min gap',g.min().round(3))
