"""markdown table: route choreography per section, computed from the built layout. usage: route_doc.py slug"""
import json,sys,importlib,math
sys.path.insert(0,'/workspace/w2-work')
slug=sys.argv[1]; d=f'/workspace/newjeans-line-designs/{slug}'
spec=importlib.import_module('spec_'+slug.replace('-','_')); import build
c=json.load(open(f'{d}/chart.json')); L=json.load(open(f'{d}/layout.json'))
nodes=[(n[0],n[1],n[2],['N','E','S','W'].index(n[4])) for n in L['path']['nodes']]
dirs=[t['dir'] for t in c['taps']]; times=[t['t'] for t in c['taps']]
secs=c['sections']; dur=json.load(open(f'/workspace/w2-work/{slug}.json'))['duration']
segs=list(zip(nodes,nodes[1:]))
def W(t): return build.width_at(spec,t)
def E(t): return build.elev_at(spec,t)
boxes=[]
for a,b in segs:
    w=max(W(a[0]),W(b[0]))/2; boxes.append((min(a[1],b[1])-w,max(a[1],b[1])+w,min(a[2],b[2])-w,max(a[2],b[2])+w))
over=[0]*len(segs)
for i in range(len(segs)):
    for j in range(i+2,len(segs)):
        A,B=boxes[i],boxes[j]
        if A[0]<B[1] and B[0]<A[1] and A[2]<B[3] and B[2]<A[3] and segs[j][0][0]-segs[i][1][0]>=1.5: over[i]+=1; over[j]+=1
NAMES={'stair':'staircase','meander':'zigzag corridor (RRLL)','switch':'switchbacks','spiral':'spiral / wrap','free':'long sweeping legs'}
print('| Section | Route texture (planner motifs) | taps | max same-dir run | U-turns | height | over/under-passes |')
print('|---|---|---|---|---|---|---|')
for k,s in enumerate(secs):
    e=secs[k+1]['t'] if k+1<len(secs) else dur
    ids=[i for i,t in enumerate(times) if s['t']<=t<e]
    mot=[]
    for r in sorted(spec.ROUTE,key=lambda r:r[0]):
        nxt=[x[0] for x in spec.ROUTE if x[0]>r[0]]; rend=min(nxt) if nxt else 1e9
        if r[0]<e-0.3 and rend>s["t"]+0.3:
            m=NAMES.get(r[1],r[1])+('' if r[1]!='spiral' else f" {r[3].get('hand','R')}")+('' if r[2] is None else f" → {int(r[2])}°")
            if not mot or mot[-1]!=m: mot.append(m)
    run=mx=0; prev=None; ut=0
    for i in ids:
        run=run+1 if dirs[i]==prev else 1; mx=max(mx,run)
        if dirs[i]==prev: ut+=1
        prev=dirs[i]
    hs=[E(t) for t in [s['t']+(e-s['t'])*f for f in (0,0.25,0.5,0.75,0.999)]]
    xs=sum(1 for i,(a,b) in enumerate(segs) if s['t']<=a[0]<e and over[i])
    print(f"| {s['label']} ({s['t']:.1f}s) | {', '.join(mot)} | {len(ids)} | {mx} | {ut} | {min(hs):+.0f}..{max(hs):+.0f} | {xs} |")
