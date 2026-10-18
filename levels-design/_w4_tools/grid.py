import numpy as np, json, sys
slug=sys.argv[1]
z=np.load(f'{slug}.env.npz'); fps=float(z['sr'])/float(z['hop'])
bt=z['beats']
# robust linear fit of beat grid
idx=np.arange(len(bt)); A=np.vstack([idx,np.ones_like(idx)]).T
m=np.ones(len(bt),bool)
for _ in range(4):
    p,*_=np.linalg.lstsq(A[m],bt[m],rcond=None); r=bt-A@p; m=np.abs(r)<0.03
print(slug,'period',p[0],'bpm',60/p[0],'t0',p[1],'inliers',m.mean(),'resid ms(med abs)',np.median(np.abs(r[m]))*1000)
json.dump(dict(period=p[0],t0=p[1]),open(f'{slug}.grid.json','w'))
