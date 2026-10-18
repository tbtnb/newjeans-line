"""Route choreography planner (w2, v2.4 rules). Chooses R/L for every tap with a beam search.
spec.ROUTE = [(t_start, motif, aim, opts), ...]  motif: stair | meander | switch | spiral | free
  stair   : alternate R/L -> diagonal staircase (8th runs)
  meander : R R L L -> square-wave snake / zigzag corridor
  switch  : U-turn around short legs, reverse after long legs -> switchbacks along a wall
  spiral  : always opts['hand'] (R or L) -> square spiral / wrap around a landmark (needs a ramp to stack laps)
  free    : no turn preference, only aim/overlap
aim: compass bearing in degrees (0=N/+z, 90=E/+x) the section should drift to, or None.
opts: w_motif (default 1), w_aim (default .6), cross (bonus for passing over/under earlier road), hand
Overlap rule = levels-design/validate.py v2.4: boxes per segment inflated by own width/2, ignore pairs < 1.5 s apart,
height checked at 0.02/0.5/0.98 of both segments, need >= 3."""
import math, numpy as np
HEAD=[(0,1),(1,0),(0,-1),(-1,0)]; ORDER=['N','E','S','W']

def plan(spec, times, dur, speed_at_fn, width_at, elev_at, beam=80, fixed=None, verbose=True):
    fixed=fixed or {}
    N=len(times); T=[0.0]+list(times)+[dur]
    # cumulative distance
    bps=sorted(set([0.0]+[s[0] for s in spec.SPEED]))
    def D(t):
        d=0; a=0.0
        for b in [p for p in bps if 0<p<t]+[t]:
            d+=(b-a)*speed_at_fn(a); a=b
        return d
    Dk=[D(t) for t in T]; L=[Dk[k+1]-Dk[k] for k in range(N+1)]
    Wk=[max(width_at(T[k]),width_at(T[k+1])) for k in range(N+1)]
    Ek=np.array([[elev_at(T[k]+f*(T[k+1]-T[k])) for f in (0.02,0.5,0.98)] for k in range(N+1)])
    R=sorted(spec.ROUTE,key=lambda r:r[0])
    def rinfo(t):
        r=[x for x in R if x[0]<=t+1e-6]; r=r[-1] if r else R[0]
        return r
    gaps=np.diff(times)
    h0=ORDER.index(spec.START_HEADING)
    # seg 0
    dx,dz=HEAD[h0]
    b0=np.array([[min(0,dx*L[0])-Wk[0]/2,max(0,dx*L[0])+Wk[0]/2,min(0,dz*L[0])-Wk[0]/2,max(0,dz*L[0])+Wk[0]/2]])
    st=dict(sc=0.0,h=h0,x=dx*L[0],z=dz*L[0],dirs=[],boxes=b0,cross=0,brk=0)
    states=[st]
    for i in range(N):
        k=i+1  # new segment index
        r=rinfo(times[i]); motif=r[1]; aim=r[2]; o=r[3] if len(r)>3 else {}
        wm=o.get('w_motif',1.0); wa=o.get('w_aim',0.6); wc=o.get('cross',0.0); hand=o.get('hand','R')
        # section-local index (for meander phase)
        cand=[]
        # which earlier segments are checkable: j<=k-2 and T[k]-T[j+1]>=1.5
        jmax=k-2
        while jmax>=0 and T[k]-T[jmax+1]<1.5: jmax-=1
        aimv=None if aim is None else (math.sin(math.radians(aim)),math.cos(math.radians(aim)))
        gprev=times[i]-times[i-1] if i>0 else 9
        thr=o.get('thr',0.5)
        for s in states:
            p=s['dirs'][-1] if s['dirs'] else 'L'
            if motif=='stair': pref='R' if p=='L' else 'L'
            elif motif=='meander':
                ds=s['dirs']; pref=p if (len(ds)>=2 and ds[-1]!=ds[-2]) or len(ds)<2 else ('R' if p=='L' else 'L')
            elif motif=='switch': pref=p if gprev<thr else ('R' if p=='L' else 'L')
            elif motif=='spiral': pref=hand
            else: pref=None
            for d in ('R','L'):
                if i in fixed and fixed[i]!=d: continue
                h=(s['h']+(1 if d=='R' else -1))%4; dx,dz=HEAD[h]
                x1=s['x']+dx*L[k]; z1=s['z']+dz*L[k]; w=Wk[k]/2
                box=np.array([min(s['x'],x1)-w,max(s['x'],x1)+w,min(s['z'],z1)-w,max(s['z'],z1)+w])
                sc=s['sc']; cr=0
                if jmax>=0:
                    B=s['boxes'][:jmax+1]; m=0.3
                    hit=(B[:,0]<box[1]+m)&(box[0]-m<B[:,1])&(B[:,2]<box[3]+m)&(box[2]-m<B[:,3])
                    if hit.any():
                        idx=np.nonzero(hit)[0]
                        dy=np.abs(Ek[idx][:,:,None]-Ek[k][None,None,:]).min(axis=(1,2))
                        if (dy<3.05).any(): continue
                        cr=len(idx); sc+=wc*min(cr,2)
                    # readability: penalise same-level road passing close (within 2.5 u) and older than 3 s
                    m2=2.5
                    near=(B[:,0]<box[1]+m2)&(box[0]-m2<B[:,1])&(B[:,2]<box[3]+m2)&(box[2]-m2<B[:,3])
                    if near.any():
                        idx=np.nonzero(near)[0]
                        dy=np.abs(Ek[idx,1]-Ek[k,1])
                        sc-=0.35*int((dy<3).sum())
                if pref is not None and d==pref: sc+=wm
                elif pref is not None: pass
                if aimv: sc+=wa*(dx*aimv[0]+dz*aimv[1])*min(L[k],6)/4.0
                # soft world bound
                R2=math.hypot(x1,z1)
                if R2>getattr(spec,'RMAX',260): sc-=0.05*(R2-getattr(spec,'RMAX',260))
                cand.append(dict(sc=sc,h=h,x=x1,z=z1,dirs=s['dirs']+[d],boxes=None,_pb=s['boxes'],_box=box,cross=s['cross']+(1 if cr else 0)))
        if not cand:
            raise RuntimeError(f'route dead end at tap {i} t={times[i]:.2f} ({motif})')
        cand.sort(key=lambda c:-c['sc']); seen=set(); ns=[]
        for c in cand:
            key=(c['h'],round(c['x']/1.5),round(c['z']/1.5),tuple(c['dirs'][-3:]))
            if key in seen: continue
            seen.add(key); c['boxes']=np.vstack([c['_pb'],c['_box'][None,:]]); del c['_pb'],c['_box']; ns.append(c)
            if len(ns)>=beam: break
        states=ns
    best=states[0]
    if verbose: print(f'  route: score {best["sc"]:.1f}  crossings(seg) {best["cross"]}')
    return best['dirs']
