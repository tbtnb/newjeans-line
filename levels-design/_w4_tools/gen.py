import json, sys, math, importlib.util, subprocess, numpy as np
sys.path.insert(0,'/workspace/w4'); from route import *; from choreo import search, overlap_count; from plotroute import plot_route, plot_sections
slug=sys.argv[1]; OUT=f'/workspace/newjeans-line-designs/{slug}'; import os; os.makedirs(OUT,exist_ok=True)
PREFIX=sys.argv[2] if len(sys.argv)>2 else ''
sp=importlib.util.spec_from_file_location('d',f'/workspace/w4/designs/{slug.replace("-","_")}.py'); D=importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
raw=json.load(open(f'/workspace/w4/{slug}.chart.raw.json'))
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'/workspace/nj-design-w4/public/audio/{slug}.mp3'],capture_output=True,text=True).stdout)
taps=[r['t'] for r in raw['taps']]
speeds=D.SPEED
W=max(w['w'] for w in D.WIDTH)
D.ELEV=snap_elev(D.ELEV,taps)
if hasattr(D,'BLOCKS'):
    dirs,_=search(taps,speeds,dur,D.BLOCKS,D.ELEV,W,margin=getattr(D,'MARGIN',0.3),beam=getattr(D,'BEAM',8),start=D.START,verbose=False); used=[]
else:
    dirs,used=assign_dirs(taps,D.ROT)
nodes=build(taps,dirs,speeds,dur,D.START)
hits=overlaps(nodes,D.ELEV,W,margin=getattr(D,'MARGIN',0.3))
print(slug,'rotations used:',[(round(t,2),d) for i,t,d in used],'of',len(getattr(D,'ROT',[])))
print('overlaps (margin):',len(hits),hits[:10])
hard=overlaps(nodes,D.ELEV,W,margin=0)
print('overlaps (validator-equivalent):',len(hard))
for e in D.ELEV:
    if e['type'] in ('fall','jump'):
        nxt=min([x for x in taps if x>e['t']] or [dur])
        print('ELEV',e['type'],e['t'],'next tap in',round(nxt-e['t'],3),'OK' if nxt-e['t']>=0.35 else 'TOO SOON')
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
    if 'world' in o and isinstance(o['world'][0],str):
        _,ta,tb=o['world']; pts=[world_of(nodes,ta+(tb-ta)*i/200) for i in range(201)]
        cx,cz=sum(p[0] for p in pts)/len(pts),sum(p[1] for p in pts)/len(pts)
        if o['world'][0]=='hole':   # largest empty spot near the centroid (centre of a loop / helix)
            best=(-1,cx,cz); X0,X1=min(p[0] for p in pts),max(p[0] for p in pts); Z0,Z1=min(p[1] for p in pts),max(p[1] for p in pts)
            for i in range(int((X1-X0)/0.5)+1):
                for j in range(int((Z1-Z0)/0.5)+1):
                    qx,qz=X0+i*0.5,Z0+j*0.5
                    # inside the loop: road of the window exists on all four sides
                    sides=[any(p[0]<qx-1 and abs(p[1]-qz)<3 for p in pts),any(p[0]>qx+1 and abs(p[1]-qz)<3 for p in pts),
                           any(p[1]<qz-1 and abs(p[0]-qx)<3 for p in pts),any(p[1]>qz+1 and abs(p[0]-qx)<3 for p in pts)]
                    if not all(sides): continue
                    d=seg_dist(qx,qz)
                    if d>best[0]: best=(d,qx,qz)
            cx,cz=best[1],best[2]
        o['world']=(cx+o.get('wdx',0),cz+o.get('wdz',0))
    o.pop('wdx',None); o.pop('wdz',None)
    for k in range(60):
        if 'world' in o: wx,wz=o['world']; break
        wx=px0+rx*lat+fx*fwd; wz=pz0+rz*lat+fz*fwd
        if o.get('onroad') or seg_dist(wx,wz)>=need: break
        lat=lat*1.12+ (0.5 if lat>=0 else -0.5)
    yaw=math.degrees(math.atan2(fx,fz)); r=o.get('rot',0)
    if isinstance(r,list): o['rot']=[r[0],round(yaw+r[1],1),r[2]]
    else: o['rot']=round(yaw+r,1)
    wy=elev_at(D.ELEV,t)+o.pop('y',0)
    o['worldPos']=[round(wx,2),round(wy,2),round(wz,2)]
    o.pop('side',None); o.pop('along',None); o.pop('world',None); o['debugXZ']=[round(wx,2),round(wz,2)]
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
def straight_mid(target):
    best=None
    for a,b in zip([0.0]+taps,taps+[dur]):
        m=(a+b)/2
        if b-a>=0.45 and a>1.5 and not any(x0-0.25<=m<=x1+0.25 for x0,x1 in AIR):
            c=abs(m-target)
            if best is None or c<best[0]: best=(c,m)
    return round(best[1],3)
dia=[{'t':straight_mid(x),'side':0} for x in D.DIAMOND_TARGETS]
# fake-out forks: a dead-end stub continuing straight past a corner; rises with the road, sinks after the line has turned
forks=[]
for i,ft in enumerate(getattr(D,'FORKS',[])):
    k=min(range(len(taps)),key=lambda j:abs(taps[j]-ft)); tc=taps[k]
    x,z,h=pos_at(nodes,tc-0.01); hx,hz=HEAD[ORDER[h]]; L=getattr(D,'FORK_LEN',6.0)
    pts=[(x+hx*(W/2+L*f),z+hz*(W/2+L*f)) for f in (0.2,0.5,0.8,1.0)]
    def far(px,pz):
        for a,b in zip(nodes,nodes[1:]):
            if a[0]<=tc+2 and b[0]>=tc-2: continue
            ax_,az_,bx_,bz_=a[1],a[2],b[1],b[2]; vx,vz=bx_-ax_,bz_-az_; L2=vx*vx+vz*vz
            f=0 if L2==0 else max(0,min(1,((px-ax_)*vx+(pz-az_)*vz)/L2))
            if math.hypot(px-(ax_+f*vx),pz-(az_+f*vz))<W+0.6 and abs(elev_at(D.ELEV,a[0])-elev_at(D.ELEV,tc))<3: return False
        return True
    # the next corner's road also must not be hit: next segment heads 90 deg away, so only the stub tip matters
    if not all(far(*p) for p in pts): print('fork skipped (collides)',ft); continue
    cx,cz=x+hx*(W/2+L/2),z+hz*(W/2+L/2)
    forks.append({'id':f'fork{i}','t':round(tc,3),'kind':'box','onroad':True,'size':[W,0.6,L],'worldPos':[round(cx,2),round(elev_at(D.ELEV,tc)-0.6,2),round(cz,2)],
                  'rot':round(math.degrees(math.atan2(hx,hz)),1),'color':D.PALETTE['road'],'name':'fake-out fork: dead-end stub that rises with the road and sinks once the line has turned (scenery only)',
                  'appear':{'t':round(tc-2.0,3),'mode':'rise','dur':0.6},'exit':{'t':round(tc+0.35,3),'mode':'sink','dur':0.8},'debugXZ':[round(cx,2),round(cz,2)]})
objs+=forks
print('forks',[(f['id'],f['t']) for f in forks])
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
     'diamonds':dia,'crowns':crowns,'finish':D.FINISH,'collectibleColors':getattr(D,'COLLECT',{}),
     **({'art':D.ART} if hasattr(D,'ART') else {}),
     'route':{'note':'centerline nodes [t,x,z,headingIndex(0N,1E,2S,3W),y] computed from taps+dirs+speed (same math as validate.py)',
              'nodes':[[round(n[0],3),round(n[1],2),round(n[2],2),n[3],round(elev_at(D.ELEV,n[0]),2)] for n in nodes]}}
json.dump(ch,open(f'{OUT}/{PREFIX}chart.json','w'),indent=1)
json.dump(lay,open(f'{OUT}/{PREFIX}layout.json','w'),indent=1)
hard,cross=overlap_count(nodes,D.ELEV,W,0)
plot_route(f'{OUT}/{PREFIX}route.png',nodes,D.ELEV,W,secs,f'{slug}: {len(taps)} taps, same-level overlaps={hard}, multi-level crossings={cross} (top-down, +x=E right, +z=N up; colour = road height)',objs,dia,crowns,getattr(D,'BLOCKS',None))
plot_sections(f'{OUT}/{PREFIX}route-sections.png',nodes,D.ELEV,W,secs,slug,dur)
print('objects clearance (id,t,dist to centerline):',report)
xs=[n[1] for n in nodes]; zs=[n[2] for n in nodes]; print('extent x',round(min(xs)),round(max(xs)),'z',round(min(zs)),round(max(zs)))
