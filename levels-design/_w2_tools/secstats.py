import json,sys,numpy as np
s=sys.argv[1]; c=json.load(open(f'/workspace/newjeans-line-designs/{s}/chart.json'))
t=np.array([x['t'] for x in c['taps']]); secs=c['sections']
for k,se in enumerate(secs):
    e=secs[k+1]['t'] if k+1<len(secs) else 999
    tt=t[(t>=se['t'])&(t<e)]; g=np.diff(tt)
    if len(g)==0: print(f"{se['t']:7.2f} {se['label']:28s} n={len(tt)}"); continue
    h=np.histogram(g,[0,.3,.5,.8,1.2,99])[0]
    print(f"{se['t']:7.2f}-{min(e,999):6.1f} {se['label'][:26]:26s} n={len(tt):3d} gaps<.3:{h[0]:2d} <.5:{h[1]:2d} <.8:{h[2]:2d} <1.2:{h[3]:2d} >:{h[4]:2d}")
