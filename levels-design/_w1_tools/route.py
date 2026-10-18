import json,math,numpy as np
HEAD={'N':(0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}; ORDER=['N','E','S','W']
def elev_at(elev,t):
    y=0.0
    for e in elev:
        if e['type'] in('fall','jump') and e['t']<=t: y+=e['dy']
        if e['type']=='ramp':
            if t>=e['t1']: y+=e['dy']
            elif t>e['t0']: y+=e['dy']*(t-e['t0'])/(e['t1']-e['t0'])
    return y
def speed_at(sp,t):
    v=9.0
    for s in sp:
        if s['t']<=t: v=s['v']
    return v
def assign_dirs(times,macro,speed,W,start_last='L'):
    """macro: list of {t, kind:'rot', turn:'R'|'L'} -> deviation at first eligible tap after t.
       or {t,kind:'force',dirs:'RRR'} force explicit dirs for consecutive taps starting at first tap>=t."""
    dirs=[]; last=start_last; pend=sorted(macro,key=lambda m:m['t']); forced={}
    for m in pend:
        if m.get('kind')=='force':
            k=next(i for i,t in enumerate(times) if t>=m['t']-1e-6)
            for j,ch in enumerate(m['dirs']): forced[k+j]=ch
    rots=[m for m in pend if m.get('kind','rot')=='rot']
    for i,t in enumerate(times):
        d='R' if last=='L' else 'L'
        if i in forced: d=forced[i]
        elif rots and t>=rots[0]['t']-1e-6 and i>0:
            need=(W+0.6)/speed_at(speed,t)
            gprev=t-times[i-1]
            gnext=(times[i+1]-t) if i+1<len(times) else 9
            if gprev>=need and gnext>=need*0.9:
                want=rots[0]['turn']
                if want==last:   # deviation = repeat previous direction
                    d=want; rots.pop(0)
                # else wait one tap so that the repeat matches 'want'
        dirs.append(d); last=d
    if rots: print('WARNING unplaced macro rotations',rots)
    return dirs
def build(times,dirs,speed,dur,elev,start='N'):
    h=ORDER.index(start); x=z=0.0; t0=0.0; nodes=[dict(t=0.0,x=0.0,z=0.0,y=0.0,heading=ORDER[h])]
    bps=sorted(set([0.0]+[s['t'] for s in speed]))
    for i,t in enumerate(list(times)+[dur]):
        dist=0; a=t0
        for b in [p for p in bps if t0<p<t]+[t]:
            dist+=(b-a)*speed_at(speed,a); a=b
        dx,dz=HEAD[ORDER[h]]; x+=dx*dist; z+=dz*dist
        if i<len(times): h=(h+(1 if dirs[i]=='R' else -1))%4
        nodes.append(dict(t=round(t,3),x=round(x,3),z=round(z,3),y=round(elev_at(elev,t),3),heading=ORDER[h])); t0=t
    return nodes
def overlaps(nodes,W,elev):
    segs=list(zip(nodes,nodes[1:]))
    def bb(s):
        a,b=s; return min(a['x'],b['x'])-W/2,max(a['x'],b['x'])+W/2,min(a['z'],b['z'])-W/2,max(a['z'],b['z'])+W/2
    B=np.array([bb(s) for s in segs]); out=[]
    for i in range(len(segs)):
        j=np.arange(i+2,len(segs))
        if not len(j): continue
        m=(B[i,0]<B[j,1])&(B[j,0]<B[i,1])&(B[i,2]<B[j,3])&(B[j,2]<B[i,3])
        for jj in j[m]:
            ti=(segs[i][0]['t']+segs[i][1]['t'])/2; tj=(segs[jj][0]['t']+segs[jj][1]['t'])/2
            if segs[jj][0]['t']-segs[i][1]['t']<1.5: continue
            if abs(elev_at(elev,ti)-elev_at(elev,tj))<3: out.append((round(segs[i][0]['t'],2),round(segs[jj][0]['t'],2)))
    return out
def pos_at(nodes,t):
    for a,b in zip(nodes,nodes[1:]):
        if a['t']<=t<=b['t']:
            f=(t-a['t'])/max(b['t']-a['t'],1e-9)
            return a['x']+(b['x']-a['x'])*f, a['z']+(b['z']-a['z'])*f, a['heading']
    b=nodes[-1]; return b['x'],b['z'],b['heading']
def seg_dist(px,pz,nodes,elev=None,py=None):
    d=1e9
    for a,b in zip(nodes,nodes[1:]):
        if elev is not None and py is not None:
            ym=elev_at(elev,(a['t']+b['t'])/2)
            if abs(ym-py)>=6: continue
        ax,az,bx,bz=a['x'],a['z'],b['x'],b['z']
        vx,vz=bx-ax,bz-az; L=vx*vx+vz*vz
        f=0 if L==0 else max(0,min(1,((px-ax)*vx+(pz-az)*vz)/L))
        d=min(d,math.hypot(px-(ax+f*vx),pz-(az+f*vz)))
    return d

DIAG={frozenset('NE'):'NE',frozenset('NW'):'NW',frozenset('SE'):'SE',frozenset('SW'):'SW'}
def assign_dirs2(times,macro,speed,W,start='N'):
    """macro: {t,diag:'NE'|'NW'|'SE'|'SW'} target staircase diagonal from time t;
              {t,kind:'force',dirs:'RRLL..'} explicit dirs; {t,kind:'straight'} unused."""
    forced={}
    for m in macro:
        if m.get('kind')=='force':
            k=next(i for i,t in enumerate(times) if t>=m['t']-1e-6)
            for j,ch in enumerate(m['dirs']): forced[k+j]=ch
    targets=sorted([m for m in macro if 'diag' in m],key=lambda m:m['t'])
    h=ORDER.index(start); last='L'; dirs=[]; tgt=None; ti=0
    for i,t in enumerate(times):
        while ti<len(targets) and targets[ti]['t']<=t+1e-6: tgt=targets[ti]['diag']; ti+=1
        d='R' if last=='L' else 'L'
        if i in forced: d=forced[i]
        elif tgt:
            opt={}
            for c in 'RL':
                h2=(h+(1 if c=='R' else -1))%4
                opt[c]=DIAG[frozenset(ORDER[h]+ORDER[h2])]
            if opt[d]!=tgt and opt[('R' if d=='L' else 'L')]==tgt:
                need=(W+0.6)/speed_at(speed,t)
                gprev=t-times[i-1] if i else 9; gnext=(times[i+1]-t) if i+1<len(times) else 9
                if gprev>=need and gnext>=need*0.9: d='R' if d=='L' else 'L'
        dirs.append(d); last=d; h=(h+(1 if d=='R' else -1))%4
    return dirs
