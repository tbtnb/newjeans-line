import json,sys,numpy as np
from configs import CONFIGS
from paths import WORK
slug=sys.argv[1]; C=CONFIGS[slug]; T=json.load(open(f'{WORK}/{slug}.taps.json')); G=json.load(open(f'{WORK}/grids.json'))[slug] if True else None
for sec in C['sections']:
    tt=[x['t'] for x in T if x['sec']==sec['label']]
    if not tt: print(sec['label'],'0'); continue
    g=np.diff(tt); print(f"{sec['label']:38s} bars{sec['bars']} n={len(tt):3d} t={tt[0]:.2f}-{tt[-1]:.2f} long(>=.6)={int((g>=.6).sum())} max={g.max() if len(g) else 0:.2f}")
