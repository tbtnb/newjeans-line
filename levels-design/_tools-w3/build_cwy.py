from route_cwy import *
L=make(); T=L.taps; o=L.obj
assert not L.hits, L.hits
s=[x['t'] for x in L.secs]+[L.dur]
I,V1,V1b,HK,D1,V2,BR,BU,FA,FB,OUT,END=s
IV='#EEEADF'; STONE='#AEBFC5'; DEEP='#254647'; CYAN='#9BD8E2'; GOLD='#D8B86A'; CORAL='#F08B78'
COV=['#77C9ED','#A5DFB5','#F3A8C8','#F8BB7D','#B1A1E3']
# Intro · empty gallery
gate_over(L,'gallery_door',0.5,color=IV,color2=GOLD,h=5.5,name='Gallery doorway (start)')
image(L,'painting_1',2.0,6,'art/wings-painting.jpg',[3.6,0,4.8],y=1.5,landmark=True,name='Floating gallery frame: two ivory forms, one winged')
image(L,'painting_2',9.0,-6,'art/wings-painting.jpg',[3.0,0,4.0],y=1.8,name='second frame')
row(L,'gallery_plinths',1.5,V1,4.5,6.0,dict(kind='box',size=[1.2,1.0,1.2],color=STONE))
# Verse 1 · reflections wake: the road wraps around a mirror room
mx,mz,my=centre(L,V1,V1b)
L.world('mirror',mx,mz,my,'group',landmark=True,name='The empty mirror (road wraps around it; it reflects the room but never the line)',
  parts=[dict(kind='box',pos=[0,3,0],size=[6,6,0.4],color=GOLD),dict(kind='plane',pos=[0,3,-0.25],size=[5.2,5.2,1],color='#cfe3e8')])
o('egg_mirror_wings',V1+6,0.1,'group',radius=1.2,y=5.5,egg=True,name='Easter egg: a tiny pair of wings appears in the mirror only during the camera swing at 21 s',
  parts=[dict(kind='box',pos=[-0.4,0,0],size=[0.6,0.3,0.1],rot=[0,0,20],color='#ffffff'),dict(kind='box',pos=[0.4,0,0],size=[0.6,0.3,0.1],rot=[0,0,-20],color='#ffffff')],
  appear=dict(t=V1+6.2,mode='fade',dur=0.4),exit=dict(t=V1+8.0,mode='fade',dur=0.4))
row(L,'gallery_walls',V1,V1b,3.2,3.0,dict(kind='box',size=[0.6,3.0,2.6],color=STONE,react='tap'),appear=dict(mode='rise',dur=0.5))
# Verse 1b · rain curtain switchbacks (narrow)
row(L,'rain_posts',V1b,HK,1.8,2.2,dict(kind='box',size=[0.2,2.2,0.2],color=CYAN,react='tap'))
fake_fork(L,'fork_rain_1',V1b+3.0,1,length=7,color='#c3cfd3',name='flooded side path (visual fake-out, lower, ends in water)')
fake_fork(L,'fork_rain_2',V1b+10.2,-1,length=6,color='#c3cfd3',name='flooded side path (visual fake-out)')
# Hook · sunken moonlit pool spiral
px_,pz_,py_=centre(L,HK,D1)
L.world('moon_pool',px_,pz_,py_-0.8,'group',landmark=True,name='Sunken rain courtyard with the moon pool (the hook spirals round it)',
  parts=[dict(kind='disc',pos=[0,0,0],size=[10,1,10],color='#3d6f78'),dict(kind='torus',pos=[0,0.1,0],size=[10.5,0.4,10.5],color=IV)])
L.world('moon',px_+20,pz_+30,26,'moon',size=[6,6,6],color='#f4f1e0',name='moon')
# Drop 1 · five-pillar balcony (observers)
cx,cz,cy=centre(L,D1,V2)
for i in range(5):
    L.world(f'observer_{i}',cx-8+4*i,cz,cy-4,'pillar',size=[1.4,7,1.4],color=CYAN,color2=COV[i],name='five pale observers (pillars)',landmark=(i==2))
L.events.append(dict(t=D1,type='light',target=[f'observer_{i}' for i in range(5)],every=1.77784,level=0.9,color='#ffe1a8',note='warm lamps on the observers, one per bar of the drop'))
row(L,'courtyard_lanterns',D1,V2,3.0,4.5,dict(kind='lamp',size=[0.3,3,0.3],color=IV,color2='#ffd79a',react='kick'))
# Verse 2 · two lights approach
o('light_a',V2+1,-8,'sphere',[1.2,1.2,1.2],y=3,color='#ffe1a8',name='light A')
o('light_b',V2+1,8,'sphere',[1.2,1.2,1.2],y=3,color='#ffd0c8',name='light B')
L.events.append(dict(t=V2+0.5,type='raise',target=['light_a','light_b'],dy=0,converge=0.8,dur=13.0,note='the two lights drift toward each other through Verse 2'))
fake_fork(L,'fork_parallel',V2+6.2,1,length=9,color='#d3dcdf',name='parallel boardwalk that stops short (visual fake-out)')
image(L,'feather_poster_v2',V2+9,-7,'art/feather-poster.jpg',[3,0,4],y=1.2,name='feather poster')
# Break · one light leaves
L.events.append(dict(t=BR,type='lower',target='light_b',dy=-8,dur=4.0,note='one light sinks away during the break'))
o('black_monument',BR+3,-9,'group',radius=2.5,landmark=True,name='White-topped black monument',
  parts=[dict(kind='box',pos=[0,3,0],size=[2.5,6,2.5],color='#1f2a2e'),dict(kind='box',pos=[0,6.6,0],size=[2.7,1.2,2.7],color='#f4f4f4')])
# Build · wings unfold
for i in range(4):
    o(f'wing_panel_{i}',BU+1+i*1.6,(-1)**i*5,'box',[0.3,3.5,5],y=1,color='#ffffff',color2=IV,rot=(-1)**i*25,appear=dict(t=BU+i*1.778,mode='unfold',dur=0.6),name='wing panel')
# Final A · feather storm helix
hx,hz,hy=centre(L,FA,FB)
L.world('feather_spire',hx,hz,-3,'group',landmark=True,name='Feather spire (Final A helix centre)',
  parts=[dict(kind='cylinder',pos=[0,6,0],size=[2,14,2],color=IV),dict(kind='cone',pos=[0,14,0],size=[3,3,3],color=GOLD)]+
        [dict(kind='box',pos=[1.5*((-1)**k),4+2*k,0],size=[2.2,0.15,0.8],rot=[0,30*k,15],color='#ffffff') for k in range(5)],react='kick')
L.events+=[dict(t=FA,type='particles',particles='petals',until=FB,note='feather storm (white petals)'),dict(t=FA,type='spin',target='feather_spire',until=FB)]
image(L,'feather_poster_fa',FA+4,8,'art/feather-poster.jpg',[4,0,5.4],mode='billboard',y=2,name='feather billboard')
# Final B · pixel city horseshoe
for i in range(8):
    o(f'city_{i}',FB+0.8+i*1.7,(-1)**i*7,'building',[4,7+2*(i%3),4],color='#c7e6ec',color2=COV[i%5],react='beat',appear=dict(t=FB+i*1.7-1.5,mode='rise',dur=0.6))
L.events.append(dict(t=FB,type='light',target=[f'city_{i}' for i in range(8)],every=0.889,level=0.8,note='windows assemble, one building per half-bar'))
row(L,'city_rails',FB,OUT,1.5,2.0,dict(kind='box',size=[0.2,0.9,0.2],color=CORAL,react='tap'))
# Outro · separated zebra crossing
zt=slot_near(T,OUT+4,1.0)
o('zebra',zt,-7,'group',radius=3,landmark=True,name='Separated zebra crossing (scenery platform)',
  parts=[dict(kind='box',pos=[0,0,-2+0.8*k],size=[4,0.1,0.45],color='#ffffff') for k in range(6)])
o('egg_feather',zt,-7,'box',[0.2,0.05,0.9],y=0.2,radius=0.4,along=0.8,egg=True,color='#ffffff',name='Easter egg: one white feather left on the crossing (the light that left came back)')
L.events+=[dict(t=OUT+1,type='raise',target='light_b',dy=8,dur=3.0,note='the second light returns'),dict(t=OUT,type='particles',particles=None,until=END)]
# palette / particles
L.events+=[dict(t=V1b,type='particles',particles='rain',until=D1),dict(t=HK,type='color',palette=dict(skyTop='#3f5966',fog='#5c7682'),dur=1.0),
 dict(t=D1,type='color',palette=dict(skyTop='#6d8a96',skyBottom='#d8e2e4'),dur=1.5),dict(t=BR,type='color',palette=dict(skyTop='#46606b'),dur=2.0),
 dict(t=FA,type='color',palette=dict(skyTop='#7fb0bf',skyBottom='#eef4f2'),dur=2.0),dict(t=FB,type='burst',at='player',particles='pixels'),
 dict(t=OUT,type='color',palette=dict(skyTop='#a9c9d3',skyBottom='#f5efe3',light='#ffe8cc'),dur=4.0,note='rain stops')]
L.camera=[dict(t=0,preset='iso',blend=0),dict(t=V1,preset='high',blend=1.5,note='road wraps the mirror room'),dict(t=V1+6,preset='iso',yaw=-40,blend=1.5),
 dict(t=V1b,preset='iso',blend=1.2),dict(t=HK,preset='high',blend=1.2,note='spiral over the sunken pool'),dict(t=D1,preset='wide',blend=1.5),
 dict(t=V2,preset='iso',blend=1.5),dict(t=BR,preset='side',yaw=70,blend=2.0),dict(t=BU,preset='low',blend=1.2),dict(t=FA,preset='high',blend=1.0),
 dict(t=FB,preset='iso',blend=1.2),dict(t=OUT,preset='wide',blend=3.0)]
place_collectibles(L,[9,20,33,47,62,77,90,104,118,133],[D1,BU])
L.art=dict(backdrop='art/rain-city.jpg',ground=dict(src='art/wet-stone.jpg',scale=40),
  catalog=[dict(file='art/rain-city.jpg',use='backdrop: rainy pixel city'),dict(file='art/wet-stone.jpg',use='ground texture'),
           dict(file='art/wings-painting.jpg',use='gallery frames (Eros & Psyche, abstract)'),dict(file='art/feather-poster.jpg',use='posters / billboards in Verse 2 and the feather storm')])
layout=dict(id='cool-with-you',title='Cool With You',
 palette=dict(skyTop='#536C78',skyBottom='#b8c8cc',fog='#8ea3aa',fogStart=30,fogEnd=110,ground='#3c5157',groundY=-8,road=IV,roadSide=STONE,line=CORAL,light='#f2f4f6',lightIntensity=1.0,ambient='#9fb3ba',particles=None),
 road=dict(width=L.widths,height=0.6,reveal=[dict(t=0,mode='fade',lead=2.5),dict(t=V1,mode='rise',lead=1.8),dict(t=V1b,mode='drop',lead=1.5),dict(t=HK,mode='rise',lead=1.8),dict(t=D1,mode='unfold',lead=1.5),dict(t=BR,mode='fade',lead=2.0),dict(t=BU,mode='rise',lead=1.5),dict(t=FB,mode='rise',lead=1.3),dict(t=OUT,mode='static',lead=3.0)]),
 elevation=L.elev,
 sections=[dict(t=x['t'],label=x['label'],camera=[c for c in L.camera if c['t']<=x['t']+0.01][-1].get('preset')) for x in L.secs],
 camera=L.camera,events=L.events,diamonds=L.layout_diamonds,crowns=L.layout_crowns,finish=dict(kind='gate',color=GOLD),collectibleColors=dict(diamond='#A4E4D1',crown=GOLD))
for sec,p in zip(layout['sections'],[None,None,dict(fogEnd=80),dict(skyTop='#3f5966'),dict(skyTop='#6d8a96'),None,dict(skyTop='#46606b'),None,dict(skyTop='#7fb0bf'),dict(ground='#5d7d86'),dict(skyTop='#a9c9d3')]):
    if p: sec['palette']=p
L.write(dict(bpm=134.995,grid=dict(t0=0.3344,sixteenth=0.111115,note='bar n starts at t0+1.77784*n'),
  judgment=dict(perfect=0.045,good=0.095,miss_beyond=0.120,note='recommended; see chart-report.md'),
  notes='Hand-composed two-step chart, 248 taps (old 107, x2.32). Min gap 0.222 s. Fastest run 15 taps (124.8-127.9 s).'),layout)
L.plot()
print('ok hits',len(L.hits),'passes',len(L.passes),'objects',len(L.objects))
