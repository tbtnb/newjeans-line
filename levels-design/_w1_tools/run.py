import sys,json,importlib,numpy as np
from chartgen import gen
s=sys.argv[1]; cfg=importlib.import_module('cfg_'+s.replace('-','_')).cfg
a,taps,stats=gen(s,cfg)
T=np.array([t['t'] for t in taps]); g=np.diff(T)
print(s,'taps',len(T),'min gap',g.min().round(3))
for st in stats: print('  %-22s %7.2f-%7.2f %4d  %.2f/s'%(st[0],st[1],st[2],st[3],st[3]/(st[2]-st[1])))
# fastest run gaps<=0.31
best=(0,0);cur=0
for i,x in enumerate(g):
    cur=cur+1 if x<=0.31 else 0
    if cur>best[0]: best=(cur,i-cur+1)
print('  fastest run',best[0]+1,'taps from',T[best[1]])
print('  gap hist',np.histogram(g,[0,.2,.25,.31,.45,.6,1,2,4,10])[0])
json.dump(dict(taps=taps,stats=stats),open(f'{s}.taps.json','w'))
