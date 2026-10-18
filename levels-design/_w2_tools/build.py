"""Level builder for worker w2. Usage: python build.py <slug>   (spec in spec_<slug>.py)
Chart: per-section 16-step patterns on the fitted beat grid, each tap snapped to the nearest real onset of the
tagged stem (demucs htdemucs) within SNAP window. Route: dirs planned per section motif, overlap-checked."""
import warnings; warnings.filterwarnings('ignore')
import json, sys, math, importlib, numpy as np, subprocess
from pathlib import Path
W2=Path('/workspace/w2-work'); OUT=Path('/workspace/newjeans-line-designs')
HEAD={'N':(0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}; ORDER=['N','E','S','W']
SRC={'k':['kick'],'s':['snare'],'v':['vocals'],'b':['bass'],'m':['other'],'h':['hat'],
     'x':['kick','snare','vocals','other','bass']}
TAGN={'k':'kick','s':'snare','v':'vocal','b':'bass','m':'melody','h':'hat','x':'phrase','c':'clap'}
SNAP=0.045

def load(slug):
    return json.loads((W2/f'{slug}.json').read_text())

def onsets(a,keys,thr=0.12):
    out=[]
    for k in keys:
        for t,s in a.get(k,[]):
            if s>=thr: out.append((t,s,k))
    return out

def make_chart(slug, spec, a):
    T=a['beat_period']; b0=a['beat0']+spec.BEAT_OFFSET*T
    bar=lambda n: b0+n*4*T
    taps=[]
    for sec in spec.SECTIONS:
        if 'auto' in sec:
            au=sec['auto']; cand=[]
            for t,st,_k in onsets(a,au['src'],au['thr']):
                q=round((t-b0)/(T/4))
                if sec['b0']*16<=q<sec['b1']*16 and (q*1.0) not in []: cand.append((q,st))
            cand.sort(key=lambda x:-x[1]); chosen=[]
            for q,st in cand:
                if all(abs(q-c)>=au.get('minsteps',2) for c in chosen) and (q%16) not in au.get('ban',[]): chosen.append(q)
            for q in sorted(chosen):
                taps.append(dict(grid=b0+q*T/4,c=au.get('c','v'),sec=sec['label']))
            if 'pats' not in sec: continue
        pats=sec['pats']; ov=sec.get('over',{})
        for i,n in enumerate(range(sec['b0'],sec['b1'])):
            p=ov.get(n, pats[i%len(pats)])
            p=p.replace('|','').replace(' ','')
            steps=len(p)  # 16 normally, 12 for triplet feel
            for j,c in enumerate(p):
                if c=='.' : continue
                tg=bar(n)+j*(4*T/steps)
                taps.append(dict(grid=tg,c=c,sec=sec['label']))
    for t,c in getattr(spec,'EXTRA',[]): taps.append(dict(grid=t,c=c,sec='extra'))
    taps.sort(key=lambda d:d['grid'])
    # snap
    res=[]
    for d in taps:
        c=d['c'].lower(); cand=onsets(a,SRC.get(c,SRC['x']))
        best=None
        for t,s,k in cand:
            dt=t-d['grid']
            if abs(dt)<=SNAP:
                score=abs(dt)-0.02*s
                if best is None or score<best[0]: best=(score,t,k,s)
        if best: t=best[1]; src=best[2]
        else: t=d['grid']; src='grid'
        res.append(dict(t=round(t,3),tag=TAGN.get(c,'phrase'),src=src,grid=round(d['grid'],3)))
    # enforce min gap: drop later tap if too close
    vmin=min(v for _,v in spec.SPEED); wmax=max(w for _,w in spec.WIDTH)
    mg=max(spec.MIN_GAP,(wmax+0.06)/vmin)
    out=[]
    for d in res:
        if out and d['t']-out[-1]['t']<mg-1e-6:
            # revert both to grid where it helps
            if d['grid']-out[-1]['t']>=mg: d['t']=d['grid']; d['src']='grid'
            elif d['t']-out[-1]['grid']>=mg and (len(out)<2 or out[-1]['grid']-out[-2]['t']>=mg): out[-1]['t']=out[-1]['grid']; out[-1]['src']='grid'
            elif d['grid']-out[-1]['grid']>=mg and (len(out)<2 or out[-1]['grid']-out[-2]['t']>=mg): out[-1]['t']=out[-1]['grid']; out[-1]['src']='grid'; d['t']=d['grid']; d['src']='grid'
            else: print('  drop close tap',d['t'],'after',out[-1]['t']); continue
        out.append(d)
    out=apply_bursts(spec,a,out)
    return out, b0, T

BTAG={'snare':'snare','hat':'hat','vocals':'vocal','other':'melody','kick':'kick'}
def burst_runs(a,t0,t1,lo,hi,stems):
    runs=[]
    for k in stems:
        ev=sorted((t,s) for t,s in a.get(k,[]) if s>=0.2 and t0<=t<=t1)
        cur=[]
        for x in ev:
            if cur and lo<=x[0]-cur[-1][0]<=hi: cur.append(x)
            else:
                if len(cur)>=3: runs.append((k,cur))
                cur=[x]
        if len(cur)>=3: runs.append((k,cur))
    out=[]
    for k,r in runs:
        for i in range(0,len(r)-2):          # all sub-runs of 3..4
            for n in (4,3):
                if i+n<=len(r): out.append((n,sum(x[1] for x in r[i:i+n])/n,k,[x[0] for x in r[i:i+n]]))
    # merged percussive+vocal stream (a fast roll often alternates snare/hat/vocal hits): greedy chains of real onsets
    ev={}
    for k in stems+['drums']:
        for t,s in a.get(k,[]):
            if s>=0.25 and t0<=t<=t1:
                key=round(t/0.03)
                if key not in ev or ev[key][1]<s: ev[key]=(t,s,k)
    ev=sorted(ev.values())
    dense=lambda x0:sum(1 for e in ev if x0-0.6<=e[0]<=x0+0.6)/1.2
    for i,e in enumerate(ev):
        if dense(e[0])<5.5: continue                 # only inside genuinely 16th-dense passages
        ch=[e]
        while len(ch)<4:
            nx=[f for f in ev if lo<=f[0]-ch[-1][0]<=hi]
            if not nx: break
            ch.append(max(nx,key=lambda f:f[1]))
        if len(ch)>=3:
            k=max(set(c[2] for c in ch),key=lambda k:sum(c[2]==k for c in ch))
            out.append((len(ch),sum(c[1] for c in ch)/len(ch)-0.15,k if k!='drums' else 'snare',[c[0] for c in ch]))
    out.sort(key=lambda x:(-x[0],-x[1])); return out

def apply_bursts(spec,a,taps):
    """short fast bursts (3-4 taps) placed ONLY on real fast onset runs of one stem (snare/hat rolls, triplet fills,
    rapid vocal syllables) inside designated fill / build-up / drop / final-chorus windows. Gap floor = schema 0.15 s
    (true 16ths at 127-150 BPM are 0.10-0.118 s and would violate it), ceiling 0.19 s (faster than any 8th here)."""
    lo=getattr(spec,'BURST_MIN',0.152); hi=getattr(spec,'BURST_MAX',0.19); stems=getattr(spec,'BURST_STEMS',['snare','hat','vocals','other','kick'])
    taps=list(taps); spec._bursts=[]
    for w in getattr(spec,'BURST_WINDOWS',[]):
        t0,t1,mx=w if len(w)==3 else (w[0],w[1],1)
        used=0
        for n,st,k,r in burst_runs(a,t0,t1,lo,hi,stems):
            if used>=mx: break
            if any(not(r[-1]+0.19<=b0 or r[0]-0.19>=b1) for b0,b1 in spec._bursts): continue
            keep=[d for d in taps if d['t']<=r[0]-0.20 or d['t']>=r[-1]+0.20]
            keep+= [dict(t=round(x,3),tag=BTAG.get(k,k),src=k,grid=round(x,3)) for x in r]
            taps=sorted(keep,key=lambda d:d['t']); spec._bursts.append((r[0],r[-1])); used+=1
            print(f'  burst {len(r)} x {k} at {r[0]:.3f}-{r[-1]:.3f} gaps {[round(y-x,3) for x,y in zip(r,r[1:])]}')
    return taps

def speed_of(spec,t):
    v=spec.SPEED[0][1]
    for tt,vv in spec.SPEED:
        if tt<=t: v=vv
    return v

def width_at(spec,t):
    w=spec.WIDTH[0][1]
    for tt,ww in spec.WIDTH:
        if tt<=t: w=ww
    return w

def elev_at(spec,t):
    y=0.0
    for e in spec.ELEV:
        if e['type'] in('fall','jump') and e['t']<=t: y+=e['dy']
        if e['type']=='ramp':
            if t>=e['t1']: y+=e['dy']
            elif t>e['t0']: y+=e['dy']*(t-e['t0'])/(e['t1']-e['t0'])
    return y

def build_path(spec, times, dirs, dur, h0):
    h=ORDER.index(h0); x=z=0.0; t0=0.0; nodes=[(0.0,0.0,0.0,h)]
    bps=sorted(set([0.0]+[s[0] for s in spec.SPEED]))
    for i,t in enumerate(list(times)+[dur]):
        dist=0; a_=t0
        for b in [p for p in bps if t0<p<t]+[t]:
            dist+=(b-a_)*speed_of(spec,a_); a_=b
        dx,dz=HEAD[ORDER[h]]; x+=dx*dist; z+=dz*dist
        if i<len(times): h=(h+(1 if dirs[i]=='R' else -1))%4
        nodes.append((t,x,z,h)); t0=t
    return nodes

def overlaps(spec,nodes,upto=None,W=None):
    """v2.4 validator rule (per-segment width, ignore < 1.5 s apart, height sampled at 0.02/0.5/0.98, need >= 3)."""
    segs=[(nodes[i],nodes[i+1]) for i in range(len(nodes)-1)]
    if upto: segs=segs[:upto]
    bx=[]
    for (ta,xa,za,_),(tb,xb,zb,_) in segs:
        Wd=max(width_at(spec,ta),width_at(spec,tb))
        bx.append((min(xa,xb)-Wd/2,max(xa,xb)+Wd/2,min(za,zb)-Wd/2,max(za,zb)+Wd/2,[elev_at(spec,ta+f*(tb-ta)) for f in (0.02,0.5,0.98)]))
    hits=[]; cross=0
    for i in range(len(bx)):
        a=bx[i]
        for j in range(i+2,len(bx)):
            b=bx[j]
            if not (a[0]<b[1] and b[0]<a[1] and a[2]<b[3] and b[2]<a[3]): continue
            if segs[j][0][0]-segs[i][1][0]<1.5: continue
            if min(abs(p-q) for p in a[4] for q in b[4])<3: hits.append((segs[i][0][0],segs[j][0][0]))
            else: cross+=1
    overlaps.cross=cross
    return hits

def plan_dirs(spec, taps, dur):
    """motif per section: 'stair' alternate; 'meander' RRLL; pivots: list of times where the tap repeats the previous
    dir (rotates staircase diagonal), sign chosen greedily to avoid overlaps. spec.DIRS_FIXED: {tap_time: 'R'/'L'}"""
    times=[d['t'] for d in taps]
    motif_at=lambda t: [m for (mt,m) in spec.MOTIFS if mt<=t+1e-6][-1]
    pivots=sorted(spec.PIVOTS)
    dirs=[]; last='L'
    # build sequentially; at pivot taps try both choices with lookahead until next pivot
    pivot_idx=set()
    for p in pivots:
        k=min(range(len(times)),key=lambda i:abs(times[i]-p)); pivot_idx.add(k)
    fixed={min(range(len(times)),key=lambda i:abs(times[i]-t)):d for t,d in getattr(spec,'DIRS_FIXED',{}).items()}
    def gen(prefix, start, end, choice):
        ds=list(prefix); last=ds[-1] if ds else 'L'; mcount=0
        for i in range(start,end):
            m=motif_at(times[i])
            if i in fixed: d=fixed[i]
            elif i==start and i in pivot_idx and choice: d=choice
            elif m=='meander':
                # pairs: same, same, other, other ...
                d= last if (len(ds)>=2 and ds[-1]!=ds[-2]) else ('R' if last=='L' else 'L')
            else: d='R' if last=='L' else 'L'
            ds.append(d); last=d
        return ds
    bounds=sorted(pivot_idx)+[len(times)]
    first=bounds[0]
    beam=[(0,gen([],0,first,None))]
    BW=getattr(spec,'BEAM',6)
    for bi,s_ in enumerate(bounds[:-1]):
        e=bounds[bi+1]; cand=[]
        for _,pref in beam:
            for ch in ['R','L']:
                ds=gen(pref,s_,e,ch)
                nodes=build_path(spec,times[:e],ds,times[e] if e<len(times) else dur,spec.START_HEADING)
                hits=len(overlaps(spec,nodes))
                xs=[n[1] for n in nodes]; zs=[n[2] for n in nodes]
                ext=(max(xs)-min(xs))+(max(zs)-min(zs))
                cand.append((hits*10000+ext*getattr(spec,'COMPACT',1.0),ds))
        cand.sort(key=lambda x:x[0]); seen=set(); beam=[]
        for sc,ds in cand:
            k=''.join(ds)
            if k in seen: continue
            seen.add(k); beam.append((sc,ds))
            if len(beam)>=BW: break
    dirs=beam[0][1]
    return dirs

def at_time(nodes,t):
    for a,b in zip(nodes,nodes[1:]):
        if a[0]<=t<=b[0]:
            f=(t-a[0])/max(b[0]-a[0],1e-9); hx,hz=HEAD[ORDER[a[3]]]
            return a[1]+(b[1]-a[1])*f, a[2]+(b[2]-a[2])*f, hx, hz
    a=nodes[-1]; hx,hz=HEAD[ORDER[a[3]]]; return a[1],a[2],hx,hz

def obj_world(nodes,o):
    x,z,hx,hz=at_time(nodes,o['t']); rx,rz=hz,-hx
    return x+rx*o.get('side',0)+hx*o.get('along',0), z+rz*o.get('side',0)+hz*o.get('along',0)

def seg_dist(px,pz,a,b):
    ax,az=a[1],a[2]; bx,bz=b[1],b[2]; dx,dz=bx-ax,bz-az; L=dx*dx+dz*dz
    f=0 if L==0 else max(0,min(1,((px-ax)*dx+(pz-az)*dz)/L))
    return math.hypot(px-(ax+f*dx),pz-(az+f*dz))

def road_segs(spec,nodes):
    return [(a[1],a[2],b[1],b[2],elev_at(spec,(a[0]+b[0])/2),max(width_at(spec,a[0]),width_at(spec,b[0])),a[0],b[0]) for a,b in zip(nodes,nodes[1:])]

def clearance(px,pz,y0,y1,RS,skip=()):
    best=99
    for k,(ax,az,bx,bz,ey,w,ta,tb) in enumerate(RS):
        if k in skip: continue
        if y0 < ey+4.5 and y1 > ey-1.0:
            dx,dz=bx-ax,bz-az; L=dx*dx+dz*dz
            f=0 if L==0 else max(0,min(1,((px-ax)*dx+(pz-az)*dz)/L))
            d=math.hypot(px-(ax+f*dx),pz-(az+f*dz))-w/2
            if d<best: best=d
    return best

def obj_height(o):
    if o.get('kind')=='group' and o.get('parts'):
        return max(p.get('pos',[0,0,0])[1]+p.get('size',[1,1,1])[1]/2 for p in o['parts'])
    return (o.get('size') or [2,2,2])[1]

def place_pockets(spec,nodes,objs):
    """landmarks -> worldPos in the most open pocket near their anchor time (centre of a spiral/ring/U if there is one)."""
    RS=road_segs(spec,nodes)
    for o in objs:
        if not (o.get('landmark') or o.get('pocket')) or o.get('onroad') or 'worldPos' in o or o.get('kind')=='row' or o.get('nopocket'): continue
        t=o['t']; r=o.get('radius',2.0); hgt=obj_height(o); need=0.9+r
        best=None
        for tt in np.linspace(max(0.5,t-3),t+3,9):
            x0,z0,hx,hz=at_time(nodes,tt); ey=elev_at(spec,tt)
            for rad in (3.5,5,6.5,8,10,12.5,15,18):
                for ang in range(0,360,30):
                    px=x0+rad*math.sin(math.radians(ang)); pz=z0+rad*math.cos(math.radians(ang))
                    oy=ey+o.get('y',0)
                    c=clearance(px,pz,oy,oy+hgt,RS)
                    if c<need: continue
                    sc=min(c,need+2.5)-0.12*rad-0.4*abs(tt-t)
                    if best is None or sc>best[0]: best=(sc,px,pz,oy,c)
        if best:
            o['worldPos']=[round(best[1],2),round(best[3],2),round(best[2],2)]; o.pop('side',None); o.pop('along',None)
            o['_clear']=round(best[4]-need,2)
        else: print('  !! no pocket for',o.get('id'))
    return objs

def make_forks(spec,nodes,times,road_color):
    """visual-only fake-out forks: at a few real corners the slab also continues straight for a few units and breaks off
    into the void (Dancing Line 'fake branch'). Not a hint: it sits on an already visible corner, it never marks timing."""
    RS=road_segs(spec,nodes); out=[]
    for n,tf in enumerate(getattr(spec,'FORKS',[])):
        i=min(range(len(times)),key=lambda k:abs(times[k]-tf))
        if i==0 or i>=len(times)-1 or times[i]-times[i-1]<0.35: continue
        a=nodes[i]; b=nodes[i+1]   # node i+1 = corner at times[i] (nodes[0] is the start)
        hin=a[3]; hx,hz=HEAD[ORDER[hin]]; W=width_at(spec,times[i]); ey=elev_at(spec,times[i])
        for Lf in (6.0,4.5,3.0):
            cx=b[1]+hx*(W/2+Lf/2); cz=b[2]+hz*(W/2+Lf/2)
            ok=all(clearance(b[1]+hx*(W/2+f*Lf),b[2]+hz*(W/2+f*Lf),ey-0.5,ey+0.5,RS,skip=(i,i+1))>W/2+0.6 for f in (0.1,0.5,1.0))
            if ok:
                yaw=[0,90,180,270][hin]
                out.append(dict(id=f'fakefork{n}',t=round(times[i],3),worldPos=[round(cx,2),round(ey-0.35,2),round(cz,2)],rot=yaw,kind='box',
                                size=[round(W,2),0.7,Lf],color=road_color,name='fake-out fork (visual only, crumbles away)',
                                appear=dict(t=round(times[i]-2.0,2),mode='rise',dur=0.6),exit=dict(t=round(times[i]+0.6,2),mode='fall',dur=0.8)))
                break
    return out

def make_buildings(spec,nodes,times):
    """cut-away buildings the road winds through: wall blocks on the bbox perimeter of the path in [t0,t1],
    with openings wherever the road (or any road on that level) passes."""
    RS=road_segs(spec,nodes); out=[]
    for n,bd in enumerate(getattr(spec,'BUILDINGS',[])):
        t0,t1=bd['t0'],bd['t1']; pts=[(x[1],x[2]) for x in nodes if t0<=x[0]<=t1]
        if len(pts)<2: continue
        ey=min(elev_at(spec,t) for t in np.linspace(t0,t1,20)); m=bd.get('margin',2.6)
        x0=min(p[0] for p in pts)-m; x1=max(p[0] for p in pts)+m; z0=min(p[1] for p in pts)-m; z1=max(p[1] for p in pts)+m
        hgt=bd.get('h',3.2); blk=1.6; k=0
        def edge(ax,az,bx,bz):
            nonlocal k
            L=math.hypot(bx-ax,bz-az); nb=max(1,int(L/blk))
            for j in range(nb):
                f=(j+0.5)/nb; px=ax+(bx-ax)*f; pz=az+(bz-az)*f
                if clearance(px,pz,ey,ey+hgt,RS)<0.9+0.6: continue
                yaw=0 if abs(bx-ax)<1e-6 else 90
                out.append(dict(id=f'{bd["id"]}_{k}',t=round((t0+t1)/2,2),worldPos=[round(px,2),round(ey,2),round(pz,2)],rot=yaw,kind='box',
                                size=[0.5,hgt,round(L/nb,2)],color=bd.get('color','#ffffff'),
                                appear=dict(t=round(t0-2.5+0.03*k,2),mode='rise',dur=0.5))); k+=1
        edge(x0,z0,x0,z1); edge(x1,z0,x1,z1); edge(x0,z0,x1,z0); edge(x0,z1,x1,z1)
    return out

def fix_objects(spec,nodes,objs):
    """push objects sideways until footprint clears the road (>= W/2+0.8+radius) everywhere at same level band."""
    W=max(w for _,w in spec.WIDTH); fixed=[]
    for o in objs:
        if o.get('kind')=='row' or o.get('onroad') or 'worldPos' in o: fixed.append(o); continue
        size=o.get('size',[2,2,2]); r=0.5*math.hypot(size[0],size[2]) if o.get('kind')!='group' else o.get('radius',2.5)
        if o.get('kind')=='group' and o.get('parts'):
            size=[2,max(p['pos'][1]+p['size'][1]/2 for p in o['parts']),2]
        for it in range(40):
            px,pz=obj_world(nodes,o)
            oy=elev_at(spec,o['t'])+o.get('y',0)
            dmin=min([seg_dist(px,pz,a,b) for a,b in zip(nodes,nodes[1:]) if (oy < elev_at(spec,(a[0]+b[0])/2)+4.5) and (oy+size[1] > elev_at(spec,(a[0]+b[0])/2)-1.0)] or [99])
            need=W/2+0.8+r
            if dmin>=need: break
            s=o.get('side',0) or 1
            o['side']=round(s+ (0.75 if s>0 else -0.75),2)
        else:
            print('  !! object could not be cleared (dropped):',o.get('id')); continue
        o['_clear']=round(dmin-need,2); fixed.append(o)
    return fixed

def fix_air(spec,times):
    """v2.3 air-time rule: a fall/jump needs >= 0.35 s (we use 0.40) before the next tap. Move the event into the
    nearest gap that allows it (earliest: 0.06 s after the previous tap)."""
    for e in spec.ELEV:
        if e['type'] not in ('fall','jump'): continue
        t=e['t']; nxt=next((x for x in times if x>t+1e-6),9e9)
        if nxt-t>=0.40: continue
        best=None
        for a_,b_ in zip(times,times[1:]):
            if b_-a_>=0.46:
                lo,hi=a_+0.06,b_-0.40
                c=min(max(t,lo),hi); 
                if best is None or abs(c-t)<abs(best-t): best=c
        print(f'  air-fix {e["type"]} {t:.3f} -> {best:.3f}'); e['t']=round(best,3)

def build(slug):
    spec=importlib.import_module(f'spec_{slug.replace("-","_")}')
    a=load(slug); dur=a['duration']
    taps,b0,T=make_chart(slug,spec,a)
    times=[d['t'] for d in taps]
    fix_air(spec,times)
    if hasattr(spec,'ROUTE'):
        import route
        fixed={min(range(len(times)),key=lambda i:abs(times[i]-t)):d for t,d in getattr(spec,'DIRS_FIXED',{}).items()}
        dirs=route.plan(spec,times,dur,lambda t:speed_of(spec,t),lambda t:width_at(spec,t),lambda t:elev_at(spec,t),beam=getattr(spec,'BEAM',80),fixed=fixed)
    else:
        dirs=plan_dirs(spec,taps,dur)
    nodes=build_path(spec,times,dirs,dur,spec.START_HEADING)
    hits=overlaps(spec,nodes)
    d=OUT/spec.FOLDER; d.mkdir(parents=True,exist_ok=True)
    chart=dict(id=slug,startHeading=spec.START_HEADING,speed=[dict(t=t,v=v) for t,v in spec.SPEED],
               taps=[dict(t=x['t'],dir=dirs[i],tag=x['tag']) for i,x in enumerate(taps)],
               sections=[dict(t=round(b0+s['b0']*4*T if s['b0']>0 else 0,3),label=s['label'],kind=s['kind']) for s in spec.SECTIONS],
               notes=spec.NOTES, meta=dict(author='level-design worker w2', bpm=a['bpm'], beat0=round(b0,4),
               beat_period=a['beat_period'], min_gap_design=spec.MIN_GAP, judgment_window_ms=spec.JUDGE,
               old_tap_count=spec.OLD, snap_sources=[x['src'] for x in taps]))
    sec_t=[c['t'] for c in chart['sections']]
    def secT(label): return chart['sections'][[s['label'] for s in spec.SECTIONS].index(label)]['t']
    used=set()
    elevt=[e.get('t',e.get('t0')) for e in spec.ELEV]+[e.get('t1') for e in spec.ELEV if 't1' in e]
    def gap_mid(t,mg=0.8):
        gs=[(times[i],times[i+1]) for i in range(len(times)-1) if times[i+1]-times[i]>=mg and i not in used
            and not any(times[i]-0.3<=et<=times[i+1]+0.3 for et in elevt)]
        a_,b_=min(gs,key=lambda g:abs((g[0]+g[1])/2-t)); used.add(times.index(a_)); return round((a_+b_)/2,3)
    ctx=dict(b0=b0,T=T,bar=lambda n:round(b0+n*4*T,3),dur=dur,taps=times,secT=secT,gap_mid=gap_mid)
    L=spec.layout(ctx)
    if hasattr(spec,'ART'): L['art']=spec.ART
    if hasattr(spec,'more_objects'): L['objects']+=spec.more_objects(ctx)
    if hasattr(spec,'patch_layout'): spec.patch_layout(ctx,L)
    objs=place_pockets(spec,nodes,L['objects'])
    objs=fix_objects(spec,nodes,objs)
    objs+=make_forks(spec,nodes,times,L['palette']['road'])+make_buildings(spec,nodes,times)
    L['objects']=[{k:v for k,v in o.items() if k!='_clear'} for o in objs]
    # diamonds: verify straight
    for dm in L['diamonds']:
        g=min(abs(dm['t']-t) for t in times)
        if g<0.2: print('  !! diamond near tap',dm['t'],g)
    L['path']=dict(note='computed centerline nodes [t,x,z,y,heading_after] (world units, y = road elevation offset)',
                   nodes=[[round(n[0],3),round(n[1],2),round(n[2],2),round(elev_at(spec,n[0]),2),ORDER[n[3]]] for n in nodes])
    L['diamonds']=sorted(L['diamonds'],key=lambda d:d['t'])
    L['elevation']=[{k:(round(v,3) if isinstance(v,float) else v) for k,v in e.items()} for e in spec.ELEV]
    L['road']['width']=[dict(t=t,w=w) for t,w in spec.WIDTH]
    (d/'chart.json').write_text(json.dumps(chart,indent=1,ensure_ascii=False))
    (d/'layout.json').write_text(json.dumps(L,indent=1,ensure_ascii=False))
    # report stats
    gaps=np.diff(times)
    print(f'{slug}: taps {len(times)} (old {spec.OLD}, x{len(times)/spec.OLD:.2f}) min gap {gaps.min():.3f} overlaps {len(hits)} {hits[:5]}')
    snapped=sum(1 for x in taps if x['src']!='grid'); print(f'  snapped {snapped}/{len(taps)}')
    plot(slug,spec,nodes,taps,chart,L,objs,d)
    return chart,L,nodes,taps,a

def plot(slug,spec,nodes,taps,chart,L,objs,d):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.patheffects as pe
    secs=chart['sections']; cols=list(plt.cm.tab20.colors)
    segs=[]
    for a_,b_ in zip(nodes,nodes[1:]):
        k=max([j for j,s in enumerate(secs) if s['t']<=a_[0]] or [0]); y=elev_at(spec,(a_[0]+b_[0])/2)
        segs.append((y,k,a_,b_))
    ys=[s[0] for s in segs]; ymin,ymax=min(ys),max(ys)
    def draw(ax,focus=None,lwk=1.0):
        for y,k,a_,b_ in sorted(segs,key=lambda s:s[0]):
            c=cols[k%20] if (focus is None or k==focus) else (0.82,0.82,0.82)
            lw=(1.6+2.2*(y-ymin)/max(ymax-ymin,1))*lwk
            ax.plot([a_[1],b_[1]],[a_[2],b_[2]],color=c,lw=lw,solid_capstyle='butt',
                    path_effects=[pe.Stroke(linewidth=lw+1.6,foreground='k' if (focus is None or k==focus) else (0.9,0.9,0.9)),pe.Normal()])
        for dm in L['diamonds']:
            x,z,_,_=at_time(nodes,dm['t']); ax.plot(x,z,'D',color='#00c0d0',ms=5,mec='k',zorder=5)
        for c in L['crowns']:
            x,z,_,_=at_time(nodes,c['t']); ax.plot(x,z,'^',color='gold',ms=10,mec='k',zorder=5)
        for e in spec.ELEV:
            t=e.get('t',e.get('t0')); x,z,_,_=at_time(nodes,t)
            ax.plot(x,z,'v' if e['dy']<0 else '^',color='purple',ms=7,zorder=6,mfc='none',mew=1.5)
        for o in objs:
            if o.get('landmark') or o.get('egg'):
                if 'worldPos' in o: x,z=o['worldPos'][0],o['worldPos'][2]
                elif 't' in o: x,z=obj_world(nodes,o)
                else: continue
                ax.plot(x,z,'*',color='r' if o.get('egg') else 'k',ms=11,zorder=7)
                ax.annotate(o['id'],(x,z),fontsize=6,zorder=8)
        ax.set_aspect('equal'); ax.grid(alpha=.25)
    fig,ax=plt.subplots(figsize=(15,13))
    draw(ax); ax.plot(0,0,'go',ms=8)
    from matplotlib.lines import Line2D
    hs=[Line2D([0],[0],color=cols[k%20],lw=3) for k in range(len(secs))]
    ax.legend(hs,[f"{s['t']:.0f}s {s['label'].split(' · ')[0]}" for s in secs],loc='center left',bbox_to_anchor=(1.01,0.5),fontsize=8)
    ax.set_title(f'{slug}: {len(taps)} taps, height {ymin:+.0f}..{ymax:+.0f} (line width = height, drawn low->high, black edge = overpass)\n'
                 f'cyan D diamonds, gold ^ crowns, purple v/^ fall/jump/ramp start, * landmarks (red = egg)',fontsize=9)
    fig.tight_layout(); fig.savefig(d/'route.png',dpi=72); plt.close(fig)
    n=len(secs); nc=4; nr=(n+nc-1)//nc
    fig,axs=plt.subplots(nr,nc,figsize=(4.2*nc,4.2*nr))
    for k in range(nr*nc):
        ax=axs.flat[k]
        if k>=n: ax.axis('off'); continue
        pts=[(a_[1],a_[2]) for y,kk,a_,b_ in segs if kk==k]+[(b_[1],b_[2]) for y,kk,a_,b_ in segs if kk==k]
        draw(ax,focus=k,lwk=0.8)
        if pts:
            xs=[p[0] for p in pts]; zs=[p[1] for p in pts]; m=6; c=max(max(xs)-min(xs),max(zs)-min(zs))/2+m
            cx=(max(xs)+min(xs))/2; cz=(max(zs)+min(zs))/2; ax.set_xlim(cx-c,cx+c); ax.set_ylim(cz-c,cz+c)
        ax.set_title(secs[k]['label'].split(' · ')[0]+f" ({secs[k]['t']:.1f}s)",fontsize=9); ax.tick_params(labelsize=6)
    fig.tight_layout(); fig.savefig(d/'route-sections.png',dpi=60); plt.close(fig)

if __name__=='__main__':
    sys.path.insert(0,str(W2)); build(sys.argv[1])
