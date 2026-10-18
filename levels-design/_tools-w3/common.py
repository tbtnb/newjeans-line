import json, math, os, numpy as np
from geom import *
from paths import WORK, OUT
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
def load_taps(slug): return json.load(open(f'{WORK}/{slug}.taps.json'))
def gap_near(taps,t,min_gap=0.45,pad=0.05):
    min_gap=max(min_gap,0.45)
    """time inside the gap (>=min_gap) closest to t, pad after the earlier tap"""
    best=None
    for a,b in zip(taps,taps[1:]):
        if b-a>=min_gap:
            c=a+pad
            if best is None or abs(c-t)<abs(best-t): best=c
    return round(best,3)
def slot_near(taps,t,min_gap=0.5):
    best=None
    for a,b in zip(taps,taps[1:]):
        if b-a>=min_gap:
            m=(a+b)/2
            if best is None or abs(m-t)<abs(best-t): best=m
    return round(best,3)
def tap_index(taps,t):
    """index of the first tap at/after t"""
    for i,x in enumerate(taps):
        if x>=t-1e-6: return i
    return len(taps)
class Level:
    def __init__(s,slug,title,speeds,start='N'):
        s.slug=slug; s.title=title; s.speeds=speeds; s.start=start
        s.raw=load_taps(slug); s.taps=[x['t'] for x in s.raw]; s.dur=duration(slug)
        s.objects=[]; s.events=[]; s.elev=[]; s.camera=[]; s.secs=[]; s.art={}
        s.layout_diamonds=[]; s.layout_crowns=[]
    def plan(s,sections,elev,W=2.6,forced=None):
        from planner import plan,plan_dfs
        prog,s.orient=plan_dfs(s.taps,s.speeds,s.dur,s.start,elev,sections,W,forced)
        if prog is None: prog,s.orient=plan(s.taps,s.speeds,s.dur,s.start,elev,sections,W,forced)
        return s.route(prog,elev,forced,W)
    def route(s,program,elev,forced=None,W=2.4):
        s.program=program; s.elev=elev; s.W=W; s.forced=forced or {}
        s.pairs=program_pairs(s.taps,program)
        s.dirs=plan_dirs(s.taps,s.pairs,s.start,s.forced)
        s.nodes=build(s.taps,s.dirs,s.speeds,s.dur,s.start,elev)
        s.hits=overlaps(s.nodes,W,elev)
        s.passes=crossings(s.nodes,W,elev)
        return s.hits
    def P(s,t,side=0,along=0):
        (x,z),h=pos_at(s.nodes,s.speeds,t,side,along); return x,z
    def obj(s,id,t,side,kind,size=None,radius=None,along=0,y=0,**kw):
        r=radius if radius is not None else (max(size[0],size[2])/2*1.2 if size else 1.5)
        sd,(px,pz)=clear_side(s.nodes,s.speeds,s.elev,t,side,r,s.W,along)
        o=dict(id=id,t=round(t,3),side=round(sd,2),along=along,y=y,kind=kind)
        if size: o['size']=size
        o.update(kw); o['_xy']=(round(px,2),round(pz,2)); s.objects.append(o); return o
    def world(s,id,x,z,y,kind,**kw):
        """object at an absolute world position (converted to the schema anchor on write)"""
        o=dict(id=id,kind=kind,worldPos=[round(x,2),round(y,2),round(z,2)]); o.update(kw); o['_xy']=(round(x,2),round(z,2)); s.objects.append(o); return o
    def write(s,chart_extra,layout):
        d=f'{OUT}/{s.slug}'; os.makedirs(d,exist_ok=True)
        chart=dict(id=s.slug,startHeading=s.start,speed=s.speeds,
            taps=[dict(t=x['t'],dir=dd,tag=x['tag']) for x,dd in zip(s.raw,s.dirs)],sections=s.secs)
        chart.update(chart_extra)
        json.dump(chart,open(f'{d}/chart.json','w'),indent=1,ensure_ascii=False)
        objs=[]
        for o in s.objects:
            if 'worldPos' in o:
                wx,wy,wz=o['worldPos']; best=None
                for a,b in zip(s.nodes,s.nodes[1:]):
                    hx,hz=HEAD[a['h']]; L_=math.hypot(b['x']-a['x'],b['z']-a['z'])
                    u=max(0,min(L_,(wx-a['x'])*hx+(wz-a['z'])*hz))
                    px,pz=a['x']+hx*u,a['z']+hz*u; dd=math.hypot(wx-px,wz-pz)
                    # prefer anchors at a similar height
                    dd+=0.5*abs(elev_at(s.elev,a['t'])-wy) if o.get('anchorByHeight') else 0
                    if best is None or dd<best[0]:
                        f=u/max(L_,1e-9); tt=a['t']+(b['t']-a['t'])*f; best=(dd,tt,a['h'],px,pz)
                _,tt,h,px,pz=best; hx,hz=HEAD[h]; rx,rz=hz,-hx
                o['t']=round(tt,3); o['side']=round((wx-px)*rx+(wz-pz)*rz,2); o['along']=round((wx-px)*hx+(wz-pz)*hz,2)
                o['y']=round(wy-elev_at(s.elev,tt),2); o['worldPosNote']='t/side/along/y = schema anchor; worldPos (x,y,z absolute) is the same point'
            o2={k:v for k,v in o.items() if not k.startswith('_') and k!='anchorByHeight'}
            if '_xy' in o: o2['debugXZ']=list(o['_xy'])
            objs.append(o2)
        layout['objects']=objs
        layout['art']=s.art
        layout['route']=dict(note='Centerline computed from chart taps+dir+speed (Babylon left-handed, y up, N=+z, E=+x). nodes = position at each tap (heading after the tap). y = road height from elevation events.',
            nodes=[[n['t'],n['x'],n['y'],n['z'],n['h']] for n in s.nodes],node_format='[t, x, y, z, headingAfter]',
            selfCrossingErrors=s.hits,overUnderPasses=[dict(lowerT=a,upperT=b,dy=c) for a,b,c in s.passes])
        json.dump(layout,open(f'{d}/layout.json','w'),indent=1,ensure_ascii=False)
    def plot(s,fn='route.png',labels=True):
        d=f'{OUT}/{s.slug}'; os.makedirs(d,exist_ok=True)
        fig,ax=plt.subplots(figsize=(13,13)); cols=[matplotlib.colors.to_rgb(c) for c in ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#17becf','#bcbd22','#7f7f7f','#ff1493','#00ced1','#ffd700','#4b0082','#228b22','#a0522d']]
        secs=s.secs; segs=list(zip(s.nodes,s.nodes[1:]))
        ys=[n['y'] for n in s.nodes]; ymin,ymax=min(ys),max(ys)
        polys=[]
        for a,b in segs:
            k=max([j for j,sc in enumerate(secs) if sc['t']<=a['t']] or [0])
            y=elev_at(s.elev,(a['t']+b['t'])/2); w=s.width_at(a['t'])/2
            x0,x1=sorted([a['x'],b['x']]); z0,z1=sorted([a['z'],b['z']])
            poly=[(x0-w,z0-w),(x1+w,z0-w),(x1+w,z1+w),(x0-w,z1+w)]
            polys.append((y,a['t'],poly,cols[k%20]))
        for y,t,poly,c in sorted(polys,key=lambda p:(p[0],p[1])):
            sh=0.35+0.65*(y-ymin)/max(ymax-ymin,1)
            ax.add_patch(Polygon(poly,closed=True,fc=tuple(np.array(c)*sh+(1-sh)*np.array([.2,.2,.25])),ec='k',lw=0.25))
        xs=[n['x'] for n in s.nodes]; zs=[n['z'] for n in s.nodes]
        ax.plot(xs,zs,color='w',lw=0.4,alpha=.7)
        for j,sc in enumerate(secs):
            px,pz=s.P(sc['t']+0.01)
            ax.annotate(f"{sc['t']:.1f}s {sc['label']}",(px,pz),fontsize=8,color='k',xytext=(8,-12),textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.15',fc=cols[j%20],alpha=.55,lw=0))
        for o in s.objects:
            if 'kind' not in o or o['kind']=='row' or '_xy' not in o: continue
            x,z=o['_xy']; m='*' if o.get('landmark') else ('P' if o.get('egg') else ('x' if o.get('fake') else 's'))
            ax.plot(x,z,m,color='r' if o.get('egg') else ('k' if o.get('landmark') else 'gray'),ms=13 if (o.get('landmark') or o.get('egg')) else 4)
            if labels and (o.get('landmark') or o.get('egg')): ax.annotate(o.get('name',o['id'])[:34],(x,z),fontsize=7,xytext=(5,5),textcoords='offset points')
        for dm in s.layout_diamonds:
            x,z=s.P(dm['t']); ax.plot(x,z,'D',color='deepskyblue',ms=7,mec='k')
        for c in s.layout_crowns:
            x,z=s.P(c['t']); ax.plot(x,z,'^',color='gold',ms=12,mec='k')
        for e in s.elev:
            tt=e.get('t',e.get('t0')); x,z=s.P(tt); ax.annotate(f"{e['type']} {e['dy']:+g}",(x,z),fontsize=8,color='purple',weight='bold')
        x,z=s.P(0); ax.plot(x,z,'o',color='lime',ms=10,mec='k')
        ax.set_aspect('equal'); ax.grid(alpha=.2); ax.autoscale_view()
        ax.set_title(f"{s.title}: {len(s.taps)} taps · top-down road (darker = lower layer, upper layers drawn on top) · ◆ diamonds ▲ crowns ★ landmarks + egg x fake fork\n"
                     f"self-crossing errors: {len(s.hits)} · legal over/under passes: {len(s.passes)} · height range {ymin:+.0f}..{ymax:+.0f}",fontsize=10)
        fig.savefig(f'{d}/{fn}',dpi=75,bbox_inches='tight'); plt.close(fig)
    def width_at(s,t):
        w=2.4
        for x in getattr(s,'widths',[{'t':0,'w':s.W}]):
            if x['t']<=t: w=x['w']
        return w

def sw(t,a,b,k,j,n=8):
    """parallel switchback lanes: k taps along a, j taps sideways (b), k taps back along -a ..."""
    opp={'NE':'SW','SW':'NE','NW':'SE','SE':'NW'}
    pairs=[];counts=[]
    for i in range(n):
        pairs+= [a if i%2==0 else opp[a], b]; counts+=[k,j]
    return dict(t=t,mode='seq',pairs=pairs,counts=counts)
def secs_from(slug,B):
    from configs import CONFIGS
    return [dict(t=0 if i==0 else B(s['bars'][0]),label=s['label'],kind=s['kind']) for i,s in enumerate(CONFIGS[slug]['sections'])]

# ---------- decoration helpers ----------
def centre(L,t0,t1):
    pts=[n for n in L.nodes if t0<=n['t']<=t1]
    return sum(n['x'] for n in pts)/len(pts), sum(n['z'] for n in pts)/len(pts), sum(n['y'] for n in pts)/len(pts)
def long_pieces(L,t0,t1,min_len=0.6):
    """straight pieces (start time, duration) inside [t0,t1] at least min_len s long"""
    out=[]
    for a,b in zip(L.nodes,L.nodes[1:]):
        if t0<=a['t'] and b['t']<=t1 and b['t']-a['t']>=min_len: out.append((a['t'],b['t']-a['t']))
    return out
def fake_fork(L,id,t,side,length=7,color='#d9cbb8',name='visual fake-out fork'):
    """a decorative stub road that branches off at time t on one side, sits 1.2 lower, is tinted and ends at a broken edge
       (scenery only: never on the true route, no reaction to music)"""
    w=L.width_at(t); sgn=1 if side>0 else -1
    return L.obj(id,t,sgn*(w/2+length/2+0.6),'group',radius=length/2,y=-1.2,fake=True,name=name,
        parts=[dict(kind='box',pos=[0,0,0],size=[length,0.6,w],color=color),
               dict(kind='box',pos=[sgn*(length/2+0.4),-0.2,0.3],size=[0.8,0.5,w*0.7],rot=[0,0,8*sgn],color=color),
               dict(kind='rock',pos=[sgn*(length/2+1.2),-0.4,-0.4],size=[0.9,0.7,0.9],color='#9a8f84')])
def gate_over(L,id,t,color='#ffffff',color2=None,h=5.0,name='gateway the road runs through'):
    w=L.width_at(t)
    o=dict(id=id,t=round(t,3),side=0,along=0,y=0,kind='group',onroad=True,name=name,
           parts=[dict(kind='box',pos=[-(w/2+0.7),h/2,0],size=[0.8,h,1.2],color=color),dict(kind='box',pos=[w/2+0.7,h/2,0],size=[0.8,h,1.2],color=color),
                  dict(kind='box',pos=[0,h+0.4,0],size=[w+2.6,0.8,1.4],color=color2 or color)])
    o['_xy']=tuple(round(v,2) for v in L.P(t)); L.objects.append(o); return o
def row(L,id,t0,t1,side,spacing,item,bothSides=True,**kw):
    o=dict(id=id,kind='row',t0=round(t0,3),t1=round(t1,3),side=side,spacing=spacing,bothSides=bothSides,item=item); o.update(kw); L.objects.append(o); return o
def image(L,id,t,side,src,size,mode='upright',y=0,**kw):
    return L.obj(id,t,side,'image',radius=max(size[0],size[2])/2,y=y,src=src,size=size,mode=mode,**kw)
def place_collectibles(L,diamond_targets,crown_targets):
    T=L.taps
    L.layout_diamonds=[dict(t=slot_near(T,x,0.42),side=0) for x in diamond_targets]
    L.layout_crowns=[dict(t=slot_near(T,x,0.6)) for x in crown_targets]
