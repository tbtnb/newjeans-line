import sys,json,importlib
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from route import *
s=sys.argv[1]; C=importlib.import_module('cfg_'+s.replace('-','_'))
R=C.route; d=json.load(open(f'{s}.taps.json')); a=json.load(open(f'{s}.analysis.json'))
times=[t['t'] for t in d['taps']]
dirs=assign_dirs2(times,R['macro'],R['speed'],R['W'])
nodes=build(times,dirs,R['speed'],a['duration'],R['elev'])
ov=overlaps(nodes,R['W'],R['elev'])
print('overlaps',len(ov),ov[:15])
xs=[n['x'] for n in nodes]; zs=[n['z'] for n in nodes]; print('extent',min(xs),max(xs),min(zs),max(zs))
secs=C.cfg['sections']
fig,ax=plt.subplots(figsize=(12,12)); cols=plt.cm.tab10.colors
for p,q in zip(nodes,nodes[1:]):
    k=max(i for i,sc in enumerate(secs) if sc['t']<=p['t']+1e-6)
    ax.plot([p['x'],q['x']],[p['z'],q['z']],color=cols[k%10],lw=1.2+0.25*p['y'])
for k,sc in enumerate(secs):
    x,z,_=pos_at(nodes,sc['t']); ax.annotate(sc['label'],(x,z),fontsize=8,color=cols[k%10])
for e in R['elev']:
    tt=e.get('t',e.get('t0')); x,z,_=pos_at(nodes,tt); ax.plot(x,z,'v' if e['dy']<0 else '^',color='k')
for o in ov[:30]:
    x,z,_=pos_at(nodes,o[0]+0.01); ax.plot(x,z,'rx',ms=10)
ax.set_aspect('equal'); fig.savefig(f'{s}.explore.png',dpi=60)
