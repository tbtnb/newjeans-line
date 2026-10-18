import json,sys
s=sys.argv[1]; p=f'/workspace/newjeans-line-designs/{s}/chart.json'; c=json.load(open(p))
t=[x['t'] for x in c['taps']]; g=[b-a for a,b in zip(t,t[1:])]
w=[min(0.5*m,max(0.045,min(0.11,0.45*m))) for m in [min(([g[i-1]] if i else [])+([g[i]] if i<len(g) else [])) for i in range(len(t))]]
c['judgment']={'perfect':0.04,'good':round(max(w),3),'minWindow':round(min(w),3),'rule':'schema v2.5 per-tap: min(0.5*g, clamp(0.45*g, 0.045, 0.11)), g = smaller neighbouring gap',
 'note':f'min tap gap {min(g):.3f} s -> tightest window ±{min(w)*1000:.0f} ms (always <= half the local gap); sparse taps ±110 ms.'}
c['notes']='Curated per section (one audible layer each), audited by _w4_tools/audit.py: repeated phrases share patterns, faint/off-layer taps removed, 16th bursts only where prominent in the full mix. See chart-report.md.'
json.dump(c,open(p,'w'),indent=1)
