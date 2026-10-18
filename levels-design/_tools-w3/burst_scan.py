"""list real 16th-note events next to existing taps (candidates for 16th bursts)"""
import json,sys,numpy as np
from configs import CONFIGS
from paths import WORK
slug=sys.argv[1]; kinds=sys.argv[2].split(',') if len(sys.argv)>2 else ['pre','chorus','drop','break','post']
C=CONFIGS[slug]; d=json.load(open(f'{WORK}/{slug}.al.json')); G=d['grid']; PER=G['per16']; T0=G['phase']+C['db']*PER
taps=json.load(open(f'{WORK}/{slug}.taps.json')); pos=set(x['pos'] for x in taps)
def S(L,t,w=0.025):
    ts=np.array([x['t'] for x in d[L]]); ss=np.array([x['s'] for x in d[L]]); m=np.abs(ts-t)<w
    return float(ss[m].max()) if m.any() else 0.0
for sec in C['sections']:
    if sec['kind'] not in kinds: continue
    a,z=sec['bars']; out=[]
    for bar in range(a,z):
        for k in range(16):
            if f'{bar}:{k}' in pos: continue
            nb=[f'{bar}:{k-1}' in pos, f'{bar}:{k+1}' in pos or (k==15 and f'{bar+1}:0' in pos)]
            if not any(nb): continue
            t=T0+(bar*16+k)*PER
            st={L:S(L,t) for L in ['hat','snare','onsets','vocal','kick']}
            best=max(st,key=st.get)
            if st[best]>=0.55: out.append(f"{bar}:{k}({best[:2]}{st[best]:.2f})")
    print(f"{sec['label'][:30]:30s} bars{sec['bars']}: "+' '.join(out))
