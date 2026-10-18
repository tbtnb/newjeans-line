import json,sys
s=sys.argv[1]; a=json.load(open(f'{s}.json'))
print(s, list(a.keys())[:20])
for k in ('hat','snare','vocals','other','kick'):
    ev=sorted(t for t,st in a.get(k,[]) if st>=0.2)
    runs=[];cur=[ev[0]] if ev else []
    for x in ev[1:]:
        g=x-cur[-1]
        if 0.15<=g<=0.20: cur.append(x)
        else:
            if len(cur)>=3: runs.append(cur)
            cur=[x]
    if len(cur)>=3: runs.append(cur)
    r16=[];cur=[ev[0]] if ev else []
    for x in ev[1:]:
        g=x-cur[-1]
        if 0.085<=g<0.15: cur.append(x)
        else:
            if len(cur)>=3: r16.append(cur)
            cur=[x]
    print(f'  {k:7s} runs(0.15-0.20s)>=3: {len(runs):3d}  e.g. {[round(r[0],2) for r in runs[:8]]}   true-16th runs(<0.15)>=3: {len(r16)} e.g. {[round(r[0],2) for r in r16[:6]]}')
