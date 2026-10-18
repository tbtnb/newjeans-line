from route_asap import *
L=make(); T=L.taps; o=L.obj
assert not L.hits, L.hits
s=[x['t'] for x in L.secs]+[L.dur]
I,V1,V1b,PR,C1,ST,V2,DB,TA,C2,HU,FH,OUT,END=s
NIGHT='#143D36'; EMER='#315C4C'; GRASS='#A8BE94'; POOL='#76BBB9'; ROAD='#F4F1DF'; LINE='#E35D83'; GOLD='#E2BD65'; WINGSH='#C5B5DD'
COV=['#87D0E3','#A8D485','#F1B8CB','#EAB88C','#B5A0D5']
# Intro · eyes in the dark forest
for i,sd in enumerate([-6,6]):
    image(L,f'bunny_eyes_{i}',1.0+i*1.4,sd,'art/bunny-eyes.png',[2.4,0,1.6],mode='billboard',y=0.8,react='beat',name='bunny eyes in the undergrowth')
row(L,'night_pines',0.3,V1b,5.5,4.0,dict(kind='pine',size=[2.2,5,2.2],color=EMER))
# Verse 1 · moon-green meadow
o('picnic_stone',V1+3,-5,'group',radius=2.2,landmark=True,name='Folded picnic stone',
  parts=[dict(kind='box',pos=[0,0.3,0],size=[3,0.6,2],rot=[0,10,0],color=ROAD),dict(kind='box',pos=[0.6,0.8,0],size=[1.6,0.5,1.4],rot=[0,-15,0],color='#e9e4cc')])
row(L,'meadow_flowers',V1,PR,3.0,2.5,dict(kind='flower',size=[0.8,0.8,0.8],color='#F1B8CB',react='beat'))
# Verse 1b · clock in the sky (route winds round the clock tower)
cx,cz,cy=centre(L,V1b,PR)
L.world('clock_tower',cx,cz,cy-2,'group',landmark=True,name='Pendulum clock in the sky (Verse 1b winds around it)',
  parts=[dict(kind='box',pos=[0,5,0],size=[2.2,10,2.2],color=ROAD),dict(kind='plane',pos=[0,9,1.15],size=[3.6,3.6,1],color='#ffffff',texture='art/pendulum-sign.jpg'),
         dict(kind='box',pos=[0,6,1.3],size=[0.2,3,0.2],color=GOLD)])
L.events.append(dict(t=V1b,type='spin',target='clock_tower',until=PR,note='the clock face turns slowly (time standing still)'))
L.world('moon',cx+25,cz+35,30,'moon',size=[7,7,7],color='#f2f0d8',name='moon')
# Pre · letters behind leaf walls (switchbacks)
row(L,'leaf_walls',PR,C1,2.2,2.6,dict(kind='box',size=[0.6,2.4,2.2],color='#3f7a5c',react='tap'),appear=dict(mode='unfold',dur=0.5))
for i in range(4):
    o(f'letter_{i}',PR+1.5+i*3.2,(-1)**i*4.5,'box',[0.9,0.05,0.6],y=1.2+0.3*i,color='#fffdf3',react='beat',name='letter hidden behind the trees')
fake_fork(L,'fork_leaf',PR+6.0,1,length=7,color='#8fae86',name='overgrown side path (visual fake-out, lower, ends at a hedge)')
# Chorus 1 · pendulum clearing (white wings)
ux,uz,uy=centre(L,C1,ST)
for i in range(5):
    L.world(f'white_wing_{i}',ux-8+4*i,uz,uy,'group',name='five white wing slabs' if i==2 else 'white wing slab',landmark=(i==2),
      parts=[dict(kind='box',pos=[0,2.5,0],size=[0.25,5,2.2],rot=[0,0,10*(i-2)],color=ROAD),dict(kind='box',pos=[0,2.0,0.2],size=[0.2,3.5,1.6],rot=[0,0,-8],color=WINGSH)],
      appear=dict(t=C1+i*0.923,mode='rise',dur=0.6))
for i in range(4):
    o(f'pendulum_{i}',C1+1+i*3,(-1)**i*6,'group',radius=1.2,react='beat',name='swinging pendulum',
      parts=[dict(kind='box',pos=[0,3.5,0],size=[0.1,3,0.1],color=GOLD),dict(kind='sphere',pos=[0,1.8,0],size=[0.8,0.8,0.8],color=GOLD)])
image(L,'pendulum_sign',C1+6,-8,'art/pendulum-sign.jpg',[4,0,4],mode='upright',y=1,name='pendulum sign-board')
# Verse 2 · water garden (moon pool + lily pads)
wx,wz,wy=centre(L,V2,DB)
L.world('moon_pool',wx,wz,wy-0.7,'disc',size=[12,0.3,12],color=POOL,landmark=True,name='Moon pool (water garden; the road crosses it on stepping boards)')
row(L,'lily_pads',V2,DB,2.6,3.0,dict(kind='disc',size=[1.2,0.1,1.2],color='#7fb38a',react='tap'))
# Dance break · stars in groups (climb)
for i in range(6):
    o(f'star_{i}',DB+1+i*2.4,(-1)**i*5,'star',[1.2,1.2,1.2],y=2+i*0.6,color=COV[i%5],react='kick',name='star group')
L.events.append(dict(t=DB,type='particles',particles='stars',until=TA))
# Turnaround
fake_fork(L,'fork_turn',TA+1.0,-1,length=6,color='#b7c9a8',name='garden path that ends at a gate (visual fake-out)')
# Chorus 2 · the small house (route wraps around it)
hx,hz,hy=centre(L,C2,HU)
L.world('small_house',hx,hz,hy-1,'group',landmark=True,name='The small house (Chorus 2 wraps around it)',
  parts=[dict(kind='box',pos=[0,2,0],size=[5,4,5],color=ROAD),dict(kind='pyramid',pos=[0,5.2,0],size=[6,2.4,6],color='#c97a6a'),
         dict(kind='box',pos=[0,1.2,2.55],size=[1.2,2.2,0.1],color='#8a5a44'),dict(kind='box',pos=[1.6,2.6,2.55],size=[1,1,0.1],color='#ffe7a8')])
L.events.append(dict(t=C2+7.4,type='light',target='small_house',level=0.9,color='#ffe1a0',note='a window lights at the second phrase'))
row(L,'garden_fence',C2,HU,2.3,2.2,dict(kind='box',size=[0.15,0.8,1.8],color='#f1ead0',react='tap'))
# Hush · lamp flickers
lt=slot_near(T,HU+1.5,1.0)
o('hush_lamp',lt,-4,'lamp',[0.4,4,0.4],landmark=True,color=ROAD,color2='#ffd79a',name='The lamp that flickers')
L.events+=[dict(t=HU,type='light',target='hush_lamp',level=0.3,dur=0.3),dict(t=FH,type='light',target='hush_lamp',level=1.0,color='#ffd79a')]
# Final hook · lamp lights, five-colour stepped towers
for i in range(5):
    o(f'cover_tower_{i}',FH+0.6+i*1.6,(-1)**i*7,'group',radius=2,name='five-colour stepped tower' if i==2 else 'stepped tower',landmark=(i==2),
      parts=[dict(kind='box',pos=[0,1+2*k,0],size=[3-0.6*k,2,3-0.6*k],color=COV[i]) for k in range(3)],appear=dict(t=FH+i*1.846,mode='rise',dur=0.8))
# Outro · pollen bunny egg
bt=slot_near(T,OUT+1.0,0.9)
o('egg_pollen_bunny',bt,6,'group',radius=1.5,egg=True,name='Easter egg: a bunny made of glowing pollen dots appears for the last bars',
  parts=[dict(kind='sphere',pos=[0,0.7,0],size=[1.2,1.0,1.2],color='#fff4b0'),dict(kind='sphere',pos=[0,1.5,0.3],size=[0.7,0.7,0.7],color='#fff4b0'),
         dict(kind='box',pos=[-0.15,2.1,0.3],size=[0.15,0.7,0.15],color='#fff4b0'),dict(kind='box',pos=[0.15,2.1,0.3],size=[0.15,0.7,0.15],color='#fff4b0')],
  appear=dict(t=OUT,mode='fade',dur=1.5))
L.events+=[dict(t=V1,type='color',palette=dict(skyTop='#2c5a4b',skyBottom='#6f8f78'),dur=2.0),
 dict(t=C1,type='color',palette=dict(skyTop='#7fa58c',skyBottom='#e6ecd2',ground=GRASS),dur=2.0),
 dict(t=ST,type='color',palette=dict(skyTop='#3b5d52'),dur=0.3,note='held breath: the meadow dims for the silent bar'),
 dict(t=V2,type='color',palette=dict(skyTop='#5f8f86'),dur=1.0),dict(t=C2,type='color',palette=dict(skyTop='#9cc0a5',skyBottom='#f4f1df'),dur=2.0),
 dict(t=HU,type='color',palette=dict(skyTop='#2f4f45'),dur=1.0),dict(t=FH,type='color',palette=dict(skyTop='#bcd6c0',skyBottom='#fff6e6',light='#fff0d0'),dur=2.0),
 dict(t=FH,type='particles',particles='petals',until=END)]
L.camera=[dict(t=0,preset='close',blend=0),dict(t=V1,preset='iso',blend=1.5),dict(t=V1b,preset='high',blend=1.5,note='winds round the clock'),
 dict(t=PR,preset='iso',yaw=20,blend=1.2),dict(t=C1,preset='wide',blend=1.5),dict(t=ST,preset='top',blend=0.4),dict(t=V2,preset='iso',blend=1.0),
 dict(t=DB,preset='high',blend=1.0),dict(t=TA,preset='side',yaw=-60,blend=1.0),dict(t=C2,preset='high',blend=1.5,note='house wrap'),
 dict(t=HU,preset='close',blend=1.0),dict(t=FH,preset='wide',blend=1.5),dict(t=OUT,preset='high',blend=2.0)]
place_collectibles(L,[6.5,18,30,45,62,70,82,100,110,124],[ST+0.6,HU+1.2])
L.art=dict(backdrop='art/forest.jpg',ground=dict(src='art/meadow.jpg',scale=35),
  catalog=[dict(file='art/forest.jpg',use='backdrop: emerald night forest with moon and fireflies'),dict(file='art/meadow.jpg',use='ground: meadow grass with flowers'),
           dict(file='art/pendulum-sign.jpg',use='clock face texture (part texture) and sign-board image'),dict(file='art/bunny-eyes.png',use='bunny-eyes billboards in the intro')])
layout=dict(id='asap',title='ASAP',
 palette=dict(skyTop=NIGHT,skyBottom='#3d6b5a',fog='#2c5045',fogStart=28,fogEnd=100,ground=EMER,groundY=-6,road=ROAD,roadSide='#cfd8b8',line=LINE,light='#f6f2dc',lightIntensity=0.95,ambient='#8fae9a',particles=None),
 road=dict(width=L.widths,height=0.6,reveal=[dict(t=0,mode='fade',lead=2.5),dict(t=V1,mode='rise',lead=2.0),dict(t=PR,mode='unfold',lead=1.6),dict(t=C1,mode='rise',lead=1.8),dict(t=V2,mode='rise',lead=1.6),dict(t=DB,mode='drop',lead=1.4),dict(t=C2,mode='rise',lead=1.6),dict(t=FH,mode='rise',lead=1.4),dict(t=OUT,mode='static',lead=3.0)]),
 elevation=L.elev,
 sections=[dict(t=x['t'],label=x['label'],camera=[c for c in L.camera if c['t']<=x['t']+0.01][-1].get('preset')) for x in L.secs],
 camera=L.camera,events=L.events,diamonds=L.layout_diamonds,crowns=L.layout_crowns,finish=dict(kind='gate',color=GOLD),collectibleColors=dict(diamond='#41D7E7',crown=GOLD))
for sec,p in zip(layout['sections'],[None,dict(ground='#4d7a5f'),None,dict(ground='#3f6b53'),dict(ground=GRASS),dict(skyTop='#3b5d52'),dict(ground='#5f8f86'),None,None,dict(ground=GRASS),dict(skyTop='#2f4f45'),dict(skyTop='#bcd6c0'),None]):
    if p: sec['palette']=p
L.write(dict(bpm=130.012,grid=dict(t0=0.341,sixteenth=0.115374,note='bar n starts at t0+1.84598*n'),
  judgment=dict(perfect=0.040,good='half the local gap, max 0.100 (0.057 in 16th bursts)',miss_beyond=0.095,note='schema v2.5 per-tap windows; see chart-report.md'),
  notes='Hand-composed chart, 201 taps (old 83, x2.42), tier hard. 12 16th-burst taps on real snare/hat rolls (dance break, turnaround, chorus fills). Min gap 0.115 s.'),layout)
L.plot()
print('ok hits',len(L.hits),'passes',len(L.passes),'objects',len(L.objects))
