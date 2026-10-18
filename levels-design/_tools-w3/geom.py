import json, math, numpy as np, subprocess
from paths import AUDIO
HEAD={'N':(0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}
ORDER=['N','E','S','W']
def norm(p): return ''.join(sorted(set(p),key=lambda c:'NSEW'.index(c)))
_RR={'NE':'SE','SE':'SW','SW':'NW','NW':'NE'}
def rotp(P,rot):
    P=norm(P)
    return _RR[P] if rot=='R' else {v:k for k,v in _RR.items()}[P]
def speed_at(speeds,t):
    v=speeds[0]['v']
    for s in speeds:
        if s['t']<=t: v=s['v']
    return v
def dist_between(speeds,a,b):
    bps=sorted(set([s['t'] for s in speeds if a<s['t']<b])); d=0; x=a
    for p in bps+[b]:
        d+=(p-x)*speed_at(speeds,x); x=p
    return d
def program_pairs(taps,program):
    """program: list of dicts sorted by t:
       {t, mode:'stair', pair}                     diagonal staircase
       {t, mode:'serp', pairs:[..], every:k}       pair changes every k taps (switchbacks / wiggle corridors)
       {t, mode:'rot', pair, every:k, rot:'R'|'L'} pair rotates 90deg every k taps (spiral / wrap round a block)
       {t, mode:'seq', pairs:[..], counts:[..]}    explicit pair sequence with tap counts (last one holds)"""
    out=[]
    for i,t in enumerate(taps):
        seg=[p for p in program if p['t']<=t+1e-9][-1]
        k=sum(1 for x in taps[:i] if x>=seg['t']-1e-9)
        m=seg['mode']
        if m=='stair': P=seg['pair']
        elif m=='serp': P=seg['pairs'][(k//seg['every'])%len(seg['pairs'])]
        elif m=='rot':
            P=seg['pair']
            for _ in range((k//seg['every'])%4): P=rotp(P,seg.get('rot','R'))
        elif m=='seq':
            acc=0; P=seg['pairs'][-1]
            for pp,c in zip(seg['pairs'],seg['counts']):
                if k<acc+c: P=pp; break
                acc+=c
        out.append(norm(P))
    return out
def plan_dirs(taps,pairs_per_tap,start='N',forced=None):
    h=ORDER.index(start); dirs=[]; forced=forced or {}
    for i,t in enumerate(taps):
        P=pairs_per_tap[i]
        if i in forced: d=forced[i]
        else:
            r=ORDER[(h+1)%4]; l=ORDER[(h-1)%4]; cur=ORDER[h]
            if r in P and l in P: d='R'
            elif r in P: d='R'
            elif l in P: d='L'
            else: d='R'
        dirs.append(d); h=(h+(1 if d=='R' else -1))%4
    return dirs
def elev_at(elev,t):
    y=0.0
    for e in elev:
        if e['type'] in('fall','jump') and e['t']<=t: y+=e['dy']
        if e['type']=='ramp':
            if t>=e['t1']: y+=e['dy']
            elif t>e['t0']: y+=e['dy']*(t-e['t0'])/(e['t1']-e['t0'])
    return y
def build(taps,dirs,speeds,dur,start='N',elev=()):
    h=ORDER.index(start); x=z=0.0; t0=0.0
    nodes=[dict(t=0.0,x=0.0,z=0.0,y=elev_at(elev,0),h=ORDER[h])]
    for i,t in enumerate(list(taps)+[dur]):
        d=dist_between(speeds,t0,t); dx,dz=HEAD[ORDER[h]]
        x+=dx*d; z+=dz*d
        if i<len(taps): h=(h+(1 if dirs[i]=='R' else -1))%4
        nodes.append(dict(t=round(t,3),x=round(x,3),z=round(z,3),y=round(elev_at(elev,t),3),h=ORDER[h])); t0=t
    return nodes
def pos_at(nodes,speeds,t,side=0,along=0):
    for a,b in zip(nodes,nodes[1:]):
        if a['t']<=t<=b['t']:
            hx,hz=HEAD[a['h']]; d=dist_between(speeds,a['t'],t); rx,rz=hz,-hx
            return (a['x']+hx*(d+along)+rx*side, a['z']+hz*(d+along)+rz*side), a['h']
    a=nodes[-1]; hx,hz=HEAD[a['h']]; return (a['x']+hx*along+hz*side,a['z']+hz*along-hx*side),a['h']
def seg_dist(px,pz,a,b):
    ax,az,bx,bz=a['x'],a['z'],b['x'],b['z']; vx,vz=bx-ax,bz-az; L2=vx*vx+vz*vz
    u=0 if L2==0 else max(0,min(1,((px-ax)*vx+(pz-az)*vz)/L2))
    return math.hypot(px-(ax+u*vx),pz-(az+u*vz))
def overlaps(nodes,W,elev,min_dt=1.5,clear=3.0):
    """strict version of validator v2.2: pieces >=min_dt apart whose boxes overlap need >=clear height difference
       everywhere along both pieces (ramps sampled)."""
    segs=list(zip(nodes,nodes[1:])); hits=[]
    box=[(min(a['x'],b['x'])-W/2,max(a['x'],b['x'])+W/2,min(a['z'],b['z'])-W/2,max(a['z'],b['z'])+W/2) for a,b in segs]
    for i in range(len(segs)):
        for j in range(i+2,len(segs)):
            if segs[j][0]['t']-segs[i][1]['t']<min_dt: continue
            A,B=box[i],box[j]
            if A[0]<B[1] and B[0]<A[1] and A[2]<B[3] and B[2]<A[3]:
                yi=[elev_at(elev,x) for x in np.linspace(segs[i][0]['t'],segs[i][1]['t'],6)]
                yj=[elev_at(elev,x) for x in np.linspace(segs[j][0]['t'],segs[j][1]['t'],6)]
                if min(abs(a-b) for a in yi for b in yj)<clear: hits.append((round(segs[i][0]['t'],2),round(segs[j][0]['t'],2)))
    return hits
def crossings(nodes,W,elev,min_dt=1.5):
    """legal over/under passes (for reporting)"""
    segs=list(zip(nodes,nodes[1:])); out=[]
    box=[(min(a['x'],b['x'])-W/2,max(a['x'],b['x'])+W/2,min(a['z'],b['z'])-W/2,max(a['z'],b['z'])+W/2) for a,b in segs]
    for i in range(len(segs)):
        for j in range(i+2,len(segs)):
            if segs[j][0]['t']-segs[i][1]['t']<min_dt: continue
            A,B=box[i],box[j]
            if A[0]<B[1] and B[0]<A[1] and A[2]<B[3] and B[2]<A[3]:
                out.append((round(segs[i][0]['t'],2),round(segs[j][0]['t'],2),round(elev_at(elev,segs[j][0]['t'])-elev_at(elev,segs[i][0]['t']),1)))
    return out
def clear_side(nodes,speeds,elev,t,side,radius,W=2.4,along=0,maxtry=60,ytol=6):
    sgn=1 if side>=0 else -1; s=side
    for _ in range(maxtry):
        (px,pz),h=pos_at(nodes,speeds,t,s,along); y0=elev_at(elev,t); ok=True
        for a,b in zip(nodes,nodes[1:]):
            ym=elev_at(elev,(a['t']+b['t'])/2)
            if ym-y0>ytol or y0-ym>ytol+4: continue
            if seg_dist(px,pz,a,b)<radius+W/2+0.8: ok=False; break
        if ok: return s,(px,pz)
        s+=sgn*1.5
    return s,(px,pz)
def duration(slug):
    p=f'{AUDIO}/{slug}.mp3'
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
