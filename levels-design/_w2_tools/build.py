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
    return out, b0, T

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
    segs=[(nodes[i],nodes[i+1]) for i in range(len(nodes)-1)]
    if upto: segs=segs[:upto]
    W=W or max(w for _,w in spec.WIDTH)
    bx=[]
    for (ta,xa,za,_),(tb,xb,zb,_) in segs:
        bx.append((min(xa,xb)-W/2,max(xa,xb)+W/2,min(za,zb)-W/2,max(za,zb)+W/2,elev_at(spec,(ta+tb)/2)))
    hits=[]
    for i in range(len(bx)):
        a=bx[i]
        for j in range(i+2,len(bx)):
            b=bx[j]
            if a[0]<b[1] and b[0]<a[1] and a[2]<b[3] and b[2]<a[3] and abs(a[4]-b[4])<3:
                hits.append((segs[i][0][0],segs[j][0][0]))
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

def fix_objects(spec,nodes,objs):
    """push objects sideways until footprint clears the road (>= W/2+0.8+radius) everywhere at same level band."""
    W=max(w for _,w in spec.WIDTH); fixed=[]
    for o in objs:
        if o.get('kind')=='row' or o.get('onroad'): fixed.append(o); continue
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
            print('  !! object could not be cleared:',o['id'])
        o['_clear']=round(dmin-need,2); fixed.append(o)
    return fixed

def build(slug):
    spec=importlib.import_module(f'spec_{slug.replace("-","_")}')
    a=load(slug); dur=a['duration']
    taps,b0,T=make_chart(slug,spec,a)
    dirs=plan_dirs(spec,taps,dur)
    times=[d['t'] for d in taps]
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
    objs=fix_objects(spec,nodes,L['objects'])
    L['objects']=[{k:v for k,v in o.items() if k!='_clear'} for o in objs]
    # diamonds: verify straight
    for dm in L['diamonds']:
        g=min(abs(dm['t']-t) for t in times)
        if g<0.2: print('  !! diamond near tap',dm['t'],g)
    L['path']=dict(note='computed centerline nodes [t,x,z,y,heading_after] (world units, y = road elevation offset)',
                   nodes=[[round(n[0],3),round(n[1],2),round(n[2],2),round(elev_at(spec,n[0]),2),ORDER[n[3]]] for n in nodes])
    L['elevation']=spec.ELEV
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
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(12,12)); cols=plt.cm.tab20.colors
    secs=chart['sections']
    for a_,b_ in zip(nodes,nodes[1:]):
        k=max([j for j,s in enumerate(secs) if s['t']<=a_[0]] or [0])
        y=elev_at(spec,(a_[0]+b_[0])/2)
        ax.plot([a_[1],b_[1]],[a_[2],b_[2]],color=cols[k%20],lw=2.6 if y>-0.1 else 1.4, alpha=1 if y>-0.1 else 0.8,
                ls='-' if y>-4.5 else '--')
    for j,s in enumerate(secs):
        x,z,_,_=at_time(nodes,s['t']); ax.annotate(s['label'].split(' · ')[0],(x,z),fontsize=7,color=cols[j%20])
    for o in objs:
        if o.get('kind')=='row' or 't' not in o: continue
        x,z=obj_world(nodes,o)
        ax.plot(x,z,'*' if o.get('landmark') else 's',color='r' if o.get('egg') else 'k',ms=12 if o.get('landmark') else 4)
        if o.get('landmark') or o.get('egg'): ax.annotate(o['id'],(x,z),fontsize=7)
    for dm in L['diamonds']:
        x,z,_,_=at_time(nodes,dm['t']); ax.plot(x,z,'D',color='gold',ms=6)
    for c in L['crowns']:
        x,z,_,_=at_time(nodes,c['t']); ax.plot(x,z,'^',color='orange',ms=11)
    for e in spec.ELEV:
        x,z,_,_=at_time(nodes,e.get('t',e.get('t0'))); ax.plot(x,z,'v' if e['dy']<0 else 'P',color='purple',ms=9)
    ax.plot(0,0,'go'); ax.set_aspect('equal'); ax.grid(alpha=.3)
    ax.set_title(f'{slug}: {len(taps)} taps  (thin=lower level, dashed=-8 or below; D diamonds, ^ crowns, v falls)')
    fig.savefig(d/'route.png',dpi=80); plt.close(fig)

if __name__=='__main__':
    sys.path.insert(0,str(W2)); build(sys.argv[1])
