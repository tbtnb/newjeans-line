import json, sys, math, importlib.util, subprocess, numpy as np
sys.path.insert(0,'/workspace/w4'); from route import *
slug=sys.argv[1]; OUT=f'/workspace/newjeans-line-designs/{slug}'; import os; os.makedirs(OUT,exist_ok=True)
PREFIX=sys.argv[2] if len(sys.argv)>2 else ''
sp=importlib.util.spec_from_file_location('d',f'/workspace/w4/designs/{slug.replace("-","_")}.py'); D=importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
raw=json.load(open(f'/workspace/w4/{slug}.chart.raw.json'))
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'/workspace/nj-design-w4/public/audio/{slug}.mp3'],capture_output=True,text=True).stdout)
taps=[r['t'] for r in raw['taps']]
dirs,used=assign_dirs(taps,D.ROT)
speeds=D.SPEED
nodes=build(taps,dirs,speeds,dur,D.START)
W=max(w['w'] for w in D.WIDTH)
hits=overlaps(nodes,D.ELEV,W,margin=getattr(D,'MARGIN',1.0))
print(slug,'rotations used:',[(round(t,2),d) for i,t,d in used],'of',len(D.ROT))
print('overlaps (margin):',len(hits),hits[:10])
hard=overlaps(nodes,D.ELEV,W,margin=0)
print('overlaps (validator-equivalent):',len(hard))
for e in D.ELEV:
    if e['type'] in ('fall','jump'):
        bad=[x for x in taps if e['t']<=x<=e['t']+0.47]
        print('ELEV',e['type'],e['t'],'taps during air:',bad)
# drift frame: mean travel direction over window
def drift(t,win=2.5):
    a=world_of(nodes,max(0,t-win)); b=world_of(nodes,min(dur,t+win))
    dx,dz=b[0]-a[0],b[1]-a[1]; n=math.hypot(dx,dz) or 1; return dx/n,dz/n
def seg_dist(px,pz):
    best=1e9
    for a,b in zip(nodes,nodes[1:]):
        ax,az,bx,bz=a[1],a[2],b[1],b[2]; vx,vz=bx-ax,bz-az; L2=vx*vx+vz*vz
        f=0 if L2==0 else max(0,min(1,((px-ax)*vx+(pz-az)*vz)/L2))
        d=math.hypot(px-(ax+f*vx),pz-(az+f*vz)); best=min(best,d)
    return best
def nearest_free_t(t):
    # anchor time not within 0.05 s of a tap (heading ambiguous at the corner)
    for k in range(0,40):
        for s in (1,-1):
            tt=t+s*k*0.02
            if all(abs(tt-x)>0.05 for x in taps): return round(tt,3)
    return t
objs=[]; report=[]
for o in D.OBJECTS:
    o=dict(o)
    if o.get('kind')=='row': objs.append(o); continue
    t=nearest_free_t(o['t']); o['t']=t
    lat,fwd=o.pop('off',(o.get('side',0),o.get('along',0)))
    fx,fz=drift(t); rx,rz=fz,-fx                       # right of drift
    px0,pz0,h=pos_at(nodes,t)
    rad=o.pop('clear',max(o.get('size',[2,2,2])[0],o.get('size',[2,2,2])[2])/2 if 'size' in o else 3)
    need=W/2+0.8+rad
    for k in range(60):
        if 'world' in o: wx,wz=o['world']; break
        wx=px0+rx*lat+fx*fwd; wz=pz0+rz*lat+fz*fwd
        if o.get('onroad') or seg_dist(wx,wz)>=need: break
        lat=lat*1.12+ (0.5 if lat>=0 else -0.5)
    hx,hz=HEAD[ORDER[h]]; hrx,hrz=hz,-hx
    ox,oz=wx-px0,wz-pz0
    o['side']=round(ox*hrx+oz*hrz,2); o['along']=round(ox*hx+oz*hz,2)
    o.pop('world',None); o['debugXZ']=[round(wx,2),round(wz,2)]
    objs.append(o)
    report.append((o['id'],t,round(seg_dist(wx,wz),1)))
# diamonds: on straights (>=0.45 s between taps), spread by target times
def straight_mid(target):
    best=None
    for a,b in zip([0.0]+taps,taps+[dur]):
        if b-a>=0.45 and a>1.5:
            m=(a+b)/2; c=abs(m-target)
            if best is None or c<best[0]: best=(c,m,a,b)
    return round(best[1],3)
AIR=[(e['t'],e['t']+0.5) for e in D.ELEV if e['type'] in ('fall','jump')]
def best_gap(target,win=3.0):
    best=None
    for a,b in zip([0.0]+taps,taps+[dur]):
        m=(a+b)/2
        if abs(m-target)>win or b-a<0.6 or a<1.5: continue
        if any(x0-0.2<=m<=x1+0.2 for x0,x1 in AIR): continue
        if best is None or b-a>best[0]: best=(b-a,m)
    return round(best[1],3) if best else straight_mid(target)
dia=[{'t':straight_mid(x),'side':0} for x in D.DIAMOND_TARGETS]
crowns=[{'t':best_gap(x)} for x in D.CROWN_TARGETS]
for d_ in dia:
    if any(x0-0.2<=d_['t']<=x1+0.2 for x0,x1 in AIR): print('WARN diamond in air',d_)
print('crowns',crowns,'gaps',[ [round(b-a,2) for a,b in zip([0.0]+taps,taps+[dur]) if a<=c['t']<=b] for c in crowns])
# chart.json
secs=raw['sections']
ch={'id':slug,'startHeading':D.START,'speed':speeds,
    'taps':[{'t':r['t'],'dir':d,'tag':r['tag']} for r,d in zip(raw['taps'],dirs)],
    'sections':secs,'bpm':D.BPM,'grid':D.GRID,'judgment':D.JUDGMENT,
    'notes':D.CHART_NOTES}
lay={'id':slug,'title':D.TITLE,'palette':D.PALETTE,'road':{'width':D.WIDTH,'height':0.6,'reveal':D.REVEAL},
     'elevation':D.ELEV,'sections':D.SECTIONS_L,'camera':D.CAMERA,'objects':objs,'events':D.EVENTS,
     'diamonds':dia,'crowns':crowns,'finish':D.FINISH,
     'route':{'note':'centerline nodes [t,x,z,headingIndex(0N,1E,2S,3W),y] computed from taps+dirs+speed (same math as validate.py)',
              'nodes':[[round(n[0],3),round(n[1],2),round(n[2],2),n[3],round(elev_at(D.ELEV,n[0]),2)] for n in nodes]}}
json.dump(ch,open(f'{OUT}/{PREFIX}chart.json','w'),indent=1)
json.dump(lay,open(f'{OUT}/{PREFIX}layout.json','w'),indent=1)
# plot
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(12,12)); cols=plt.cm.tab10.colors
st=[s['t'] for s in secs]
for a,b in zip(nodes,nodes[1:]):
    k=max([i for i,x in enumerate(st) if x<=a[0]] or [0]); y=elev_at(D.ELEV,a[0])
    ax.plot([a[1],b[1]],[a[2],b[2]],color=cols[k%10],lw=1.2+0.25*max(0,y))
for i,s in enumerate(secs):
    x,z=world_of(nodes,s['t']); ax.annotate(f"{s['label']} {s['t']:.0f}s",(x,z),fontsize=8,color=cols[i%10],weight='bold')
for o in objs:
    if 'debugXZ' in o:
        x,z=o['debugXZ']; m='*' if o.get('landmark') else ('X' if o.get('egg') else 's')
        ax.plot(x,z,m,color='r' if o.get('egg') else 'k',ms=14 if o.get('landmark') else 6)
        if o.get('landmark') or o.get('egg'): ax.annotate(o['id'],(x,z),fontsize=7,xytext=(4,4),textcoords='offset points')
for d_ in dia: x,z=world_of(nodes,d_['t']); ax.plot(x,z,'D',color='deepskyblue',ms=6)
for c in crowns: x,z=world_of(nodes,c['t']); ax.plot(x,z,'^',color='gold',ms=11,mec='k')
for e in D.ELEV:
    t=e.get('t',e.get('t0')); x,z=world_of(nodes,t); ax.annotate(f"{e['type']} {e['dy']:+g}",(x,z),fontsize=7,color='purple')
ax.set_aspect('equal'); ax.set_title(f'{slug}: {len(taps)} taps, overlaps={len(hard)} (top-down, +x=E right, +z=N up)')
fig.savefig(f'{OUT}/{PREFIX}route.png',dpi=80,bbox_inches='tight'); plt.close(fig)
print('objects clearance (id,t,dist to centerline):',report)
xs=[n[1] for n in nodes]; zs=[n[2] for n in nodes]; print('extent x',round(min(xs)),round(max(xs)),'z',round(min(zs)),round(max(zs)))
