import sys,json,math,importlib,numpy as np
from route import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT='/workspace/newjeans-line-designs'
TAG={'vocal_on':'vocal','kick_on':'kick','snare_on':'snare','mel_on':'melody','bass_on':'bass','beat':'phrase'}
s=sys.argv[1]; C=importlib.import_module('cfg_'+s.replace('-','_')); S=importlib.import_module('spec_'+s.replace('-','_'))
R=C.route; d=json.load(open(f'{s}.taps.json')); a=json.load(open(f'{s}.analysis.json')); dur=a['duration']
taps=d['taps']; T=[t['t'] for t in taps]
dirs=assign_dirs2(T,R['macro'],R['speed'],R['W'],start=S.start)
nodes=build(T,dirs,R['speed'],dur,R['elev'],start=S.start)
assert not overlaps(nodes,R['W'],R['elev']), 'overlap'
secs=[dict(t=round(x['t'],3),label=x['label'],kind=x['kind']) for x in C.cfg['sections']]
def secof(t): return max([x for x in secs if x['t']<=t+1e-6],key=lambda x:x['t'])['label']
# ---- chart.json
chart=dict(id=s,startHeading=S.start,speed=R['speed'],
  taps=[dict(t=tp['t'],dir=dd,tag=TAG.get(tp['tag'],'phrase')) for tp,dd in zip(taps,dirs)],
  sections=secs,notes=S.chart_notes)
json.dump(chart,open(f'{OUT}/{s}/chart.json','w'),indent=1)
# ---- object placement with clearance
W=max(w['w'] for w in S.width)
def place(o):
    if 't' not in o or o.get('kind')=='row': return o
    x,z,h=pos_at(nodes,o['t']); hx,hz=HEAD[h]; rx,rz=hz,-hx
    y0=elev_at(R['elev'],o['t'])
    sz=o.get('size',[2,2,2]); rad=math.hypot(sz[0],sz[2])/2 if o.get('kind')!='group' else o.get('radius',4)
    side=o.get('side',6); sgn=1 if side>=0 else -1; along=o.get('along',0)
    for k in range(80):
        px=x+rx*side+hx*along; pz=z+rz*side+hz*along
        dd=seg_dist(px,pz,nodes,R['elev'],y0+o.get('y',0))
        if dd>=rad+W/2+0.9: break
        side+=sgn*1.0
    o=dict(o); o['side']=round(side,2)
    o['_world']=[round(px,2),round(y0+o.get('y',0),2),round(pz,2)]
    return o
objs=[place(o) for o in S.objects]
# ---- diamonds: midpoints of long gaps, allocated per section list
cand=[]
for i in range(len(T)-1):
    g=T[i+1]-T[i]
    if g>=0.5: cand.append(round((T[i]+T[i+1])/2,3))
crowns=[]
for tt in S.crown_near:
    cc=[round((T[i]+T[i+1])/2,3) for i in range(len(T)-1) if T[i+1]-T[i]>=0.6]
    c=min(cc,key=lambda t:abs(t-tt)); crowns.append({'t':c})
dia=[]
for (t0,t1,n) in S.diamond_windows:
    c=[t for t in cand if t0<=t<t1 and all(abs(t-x)>3 for x in dia) and all(abs(t-x['t'])>3 for x in crowns)]
    if len(c)<n: raise SystemExit(f'not enough diamond candidates in {t0}-{t1}: {len(c)}')
    idx=np.linspace(0,len(c)-1,n+2)[1:-1].round().astype(int)
    dia+= [c[i] for i in idx]
assert len(dia)==10,len(dia)
layout=dict(id=s,title=S.title,palette=S.palette,
  road=dict(width=S.width,height=0.6,reveal=S.reveal),
  elevation=R['elev'],sections=S.sections,camera=S.camera,
  objects=[{k:v for k,v in o.items() if not k.startswith('_')} for o in objs],
  events=S.events,diamonds=[{'t':t,'side':0} for t in dia],crowns=crowns,finish=S.finish,
  path=dict(note='computed centerline nodes (t, x, y=road height, z, heading after node). Babylon left-handed, N=+z, E=+x.',
            nodes=[[n['t'],n['x'],n['y'],n['z'],n['heading']] for n in nodes]),
  landmarks=[dict(id=o['id'],name=o.get('name',o['id']),t=o['t'],world=o['_world'],egg=o.get('egg',False)) for o in objs if o.get('landmark') or o.get('egg')])
json.dump(layout,open(f'{OUT}/{s}/layout.json','w'),indent=1)
# ---- route.png
fig,ax=plt.subplots(figsize=(13,13)); cols=plt.cm.tab20.colors
for p,q in zip(nodes,nodes[1:]):
    k=[i for i,x in enumerate(secs) if x['t']<=p['t']+1e-6][-1]
    ax.plot([p['x'],q['x']],[p['z'],q['z']],color=cols[(2*k)%20],lw=1.0+0.35*max(p['y']+3,0),solid_capstyle='butt')
for k,x in enumerate(secs):
    px,pz,_=pos_at(nodes,x['t']); ax.annotate(f"{x['label']} {x['t']:.1f}s",(px,pz),fontsize=8,color=cols[(2*k)%20],xytext=(4,4),textcoords='offset points')
for o in objs:
    if '_world' in o:
        wx,_,wz=o['_world']; m='*' if o.get('landmark') else ('P' if o.get('egg') else 's')
        ax.plot(wx,wz,m,color='crimson' if o.get('egg') else ('k' if o.get('landmark') else '0.6'),ms=14 if o.get('landmark') else 9 if o.get('egg') else 4)
        if o.get('landmark') or o.get('egg'): ax.annotate(o.get('name',o['id']),(wx,wz),fontsize=7,xytext=(5,-9),textcoords='offset points')
for t in dia:
    px,pz,_=pos_at(nodes,t); ax.plot(px,pz,'D',color='deepskyblue',ms=6)
for c in crowns:
    px,pz,_=pos_at(nodes,c['t']); ax.plot(px,pz,'^',color='goldenrod',ms=12)
for e in R['elev']:
    tt=e.get('t',e.get('t0')); px,pz,_=pos_at(nodes,tt); ax.annotate(('ramp ' if e['type']=='ramp' else e['type']+' ')+f"{e['dy']:+g}",(px,pz),fontsize=7,color='purple')
ax.plot(0,0,'go',ms=10); ax.plot(nodes[-1]['x'],nodes[-1]['z'],'ro',ms=10)
ax.set_aspect('equal'); ax.set_title(f'{S.title}: {len(T)} taps, speed {R["speed"][0]["v"]}, road {S.width[0]["w"]}  (line width ~ height; star=landmark, P=egg, D=diamond, ^=crown)')
fig.savefig(f'{OUT}/{s}/route.png',dpi=70); plt.close(fig)
print(s,'ok taps',len(T),'diamonds',dia,'crowns',crowns)
