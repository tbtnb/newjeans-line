import json,sys,numpy as np
s=sys.argv[1]; bpm=float(sys.argv[2]); ph=float(sys.argv[3])
d=json.load(open(f'/workspace/w2-work/{s}.json')); T=60/bpm
best=None
for cand in [ph%(T/2)+k*T/2 for k in range(2)]:
    sc=0
    for t,st in d['kick']:
        x=(t-cand)/T; sc+=st*(abs(x-round(x))<0.06)
    print('phase',round(cand,4),'kick-on-quarter score',round(sc,1))
    if best is None or sc>best[0]: best=(sc,cand)
b0=best[1]
d['bpm']=bpm; d['beat_period']=round(T,6); d['beat0']=round(b0,4)
d['beats']=[round(b0+i*T,4) for i in range(int((d['duration']-b0)/T)+1)]
d['grid_note']=f'grid refit: brute-force bpm/phase maximizing drum-stem onset strength on 8th grid; bpm {bpm}'
# recompute beat_rms not needed for grid shift small; keep
json.dump(d,open(f'/workspace/w2-work/{s}.json','w'))
print(s,'beat0',b0)
