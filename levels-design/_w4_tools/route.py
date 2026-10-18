import json, math
HEAD={'N':(0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}; ORDER=['N','E','S','W']
def speed_at(speeds,t):
    v=speeds[0]['v']
    for s in speeds:
        if s['t']<=t: v=s['v']
    return v
def dist_between(speeds,a,b):
    bps=sorted(set([s['t'] for s in speeds if a<s['t']<b]))
    d=0;x=a
    for p in bps+[b]: d+=(p-x)*speed_at(speeds,x); x=p
    return d
def assign_dirs(taps,rotations,start='R'):
    """rotations: list of (t, 'L'|'R'): at first tap >= t whose previous dir equals the wanted dir, repeat it
    (rotates the zig-zag drift 90 deg that way). Returns dirs list and the tap indices used."""
    dirs=[];used=[];rot=sorted(rotations);ri=0;last=None
    for i,t in enumerate(taps):
        d=start if last is None else ('R' if last=='L' else 'L')
        if ri<len(rot) and t>=rot[ri][0] and last==rot[ri][1]:
            d=last; used.append((i,t,rot[ri][1])); ri+=1
        dirs.append(d); last=d
    return dirs,used
def build(taps,dirs,speeds,dur,start='N'):
    h=ORDER.index(start); x=z=0.0; t0=0.0; nodes=[(0.0,0.0,0.0,h)]
    for i,t in enumerate(list(taps)+[dur]):
        d=dist_between(speeds,t0,t); dx,dz=HEAD[ORDER[h]]; x+=dx*d; z+=dz*d
        if i<len(taps): h=(h+(1 if dirs[i]=='R' else -1))%4
        nodes.append((t,x,z,h)); t0=t
    return nodes
def elev_at(elev,t):
    y=0.0
    for e in elev:
        if e['type'] in ('fall','jump') and e['t']<=t: y+=e['dy']
        if e['type']=='ramp':
            if t>=e['t1']: y+=e['dy']
            elif t>e['t0']: y+=e['dy']*(t-e['t0'])/(e['t1']-e['t0'])
    return y
def overlaps(nodes,elev,W,margin=0.0,mingap=1.5):
    segs=[(nodes[i],nodes[i+1]) for i in range(len(nodes)-1)]
    def bb(s):
        (ta,xa,za,_),(tb,xb,zb,_)=s; m=W/2+margin
        return min(xa,xb)-m,max(xa,xb)+m,min(za,zb)-m,max(za,zb)+m
    B=[bb(s) for s in segs]; hits=[]
    # grid hash
    cell=12.0; grid={}
    for i,b in enumerate(B):
        for gx in range(int(math.floor(b[0]/cell)),int(math.floor(b[1]/cell))+1):
            for gz in range(int(math.floor(b[2]/cell)),int(math.floor(b[3]/cell))+1):
                grid.setdefault((gx,gz),[]).append(i)
    seen=set()
    for lst in grid.values():
        for a in range(len(lst)):
            for b in range(a+1,len(lst)):
                i,j=sorted((lst[a],lst[b]))
                if j<i+2 or (i,j) in seen: continue
                seen.add((i,j))
                if segs[j][0][0]-segs[i][1][0]<mingap: continue
                p,q=B[i],B[j]
                if p[0]<q[1] and q[0]<p[1] and p[2]<q[3] and q[2]<p[3]:
                    ti=(segs[i][0][0]+segs[i][1][0])/2; tj=(segs[j][0][0]+segs[j][1][0])/2
                    if abs(elev_at(elev,ti)-elev_at(elev,tj))<3: hits.append((segs[i][0][0],segs[j][0][0]))
    return sorted(hits)
def pos_at(nodes,t,elev=None):
    for a,b in zip(nodes,nodes[1:]):
        if a[0]<=t<=b[0]:
            f=(t-a[0])/max(b[0]-a[0],1e-9); x=a[1]+(b[1]-a[1])*f; z=a[2]+(b[2]-a[2])*f
            return x,z,a[3]
    a=nodes[-1]; return a[1],a[2],a[3]
def world_of(nodes,t,side=0,along=0):
    x,z,h=pos_at(nodes,t); hx,hz=HEAD[ORDER[h]]; rx,rz=hz,-hx
    return x+rx*side+hx*along, z+rz*side+hz*along
def snap_elev(elev, taps, minnext=0.6):
    """fall/jump entries with 'snap':True move to 0.05 s after the tap whose following gap is >= minnext, nearest to t."""
    out = []
    for e in elev:
        e = dict(e)
        if e.get('snap') and e['type'] in ('fall', 'jump'):
            c = [(abs(a + 0.05 - e['t']), a + 0.05) for a, b in zip(taps, taps[1:]) if b - a >= minnext and abs(a - e['t']) < 3]
            if c: e['t'] = round(min(c)[1], 3)
            e.pop('snap')
        out.append(e)
    return out
