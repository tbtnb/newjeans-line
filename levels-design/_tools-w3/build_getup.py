from route_getup import *
L=make(); T=L.taps; o=L.obj
assert not L.hits, L.hits
s=[x['t'] for x in L.secs]+[L.dur]
I,WL,HG,FL,LS,END=s
ROAD='#F5F1E8'; SH='#544D70'; LAV='#B8B4D5'; PINK='#EC679D'
COV=['#4B9EDF','#93CF9B','#F1A9C9','#E9BC83','#B39AD7']
# After the rain: shallow water + callbacks to Cool With You
o('puddle_frame',2.2,6,'group',radius=2.2,name='Empty gallery frame lying in the water (callback to Cool With You)',
  parts=[dict(kind='box',pos=[0,0.1,0],size=[3.4,0.15,4.4],color='#D8B86A'),dict(kind='box',pos=[0,0.12,0],size=[2.8,0.16,3.8],color='#9fbac4')])
o('egg_feather',4.5,-4.5,'box',[0.2,0.05,0.9],y=0.05,radius=0.4,egg=True,color='#ffffff',name='Easter egg: the feather from Cool With You floats in the water')
row(L,'stepping_stones',0.5,WL,3.2,2.6,dict(kind='disc',size=[1.2,0.2,1.2],color=LAV,react='tap'))
# One warm light: shadow alley (slabs slide apart on the beat)
row(L,'shadow_slabs',WL,HG,2.0,2.5,dict(kind='box',size=[0.8,3.2,2.2],color=SH,react='beat'),appear=dict(mode='rise',dur=0.5))
lt=slot_near(T,WL+3.5,0.8)
o('warm_lamp',lt,-4,'lamp',[0.4,4,0.4],landmark=True,color=ROAD,color2='#ffd79a',name='The one warm light')
L.events.append(dict(t=WL,type='light',target='warm_lamp',level=1.0,color='#ffd79a',note='lights on the section downbeat'))
fake_fork(L,'fork_alley',WL+5.0,1,length=6,color='#8d86a8',name='shadow alley side stub (visual fake-out, lower, dead end)')
# Horizon gathers: switchback knot climbing past door panels
for i in range(5):
    o(f'wing_{i}',HG+0.8+i*1.4,(-1)**i*5,'group',radius=1.8,name='folded white wing' if i!=2 else 'Five folded white wings',landmark=(i==2),
      parts=[dict(kind='box',pos=[0,2,0],size=[0.2,3.5,2.4],rot=[0,0,12],color=ROAD),dict(kind='box',pos=[0.5,2.4,0],size=[0.2,2.6,1.8],rot=[0,0,-18],color='#e8e3f2')],
      appear=dict(t=HG+i*2.0-0.6,mode='unfold',dur=0.7))
row(L,'door_panels',HG,FL,3.0,3.5,dict(kind='box',size=[0.3,2.6,1.6],color=LAV,react='tap'),appear=dict(mode='rise',dur=0.6))
# Five lights · moon-green grass: loop that passes under the knot
cx,cz,cy=centre(L,FL,LS)
for i in range(5):
    L.world(f'light_beam_{i}',cx-6+3*i,cz+9,cy,'cylinder',size=[0.9,14,0.9],color=COV[i],name='five light beams' if i==2 else 'light beam',landmark=(i==2),
            appear=dict(t=FL+i*0.5,mode='grow',dur=0.8))
L.events.append(dict(t=FL,type='light',target=[f'light_beam_{i}' for i in range(5)],every=2.0,level=0.9,note='one beam per vocal phrase (2 s)'))
image(L,'five_lights_mural',FL+2.5,-9,'art/five-lights.jpg',[8,0,4.5],mode='billboard',y=1.5,name='Five-lights mural (album motif)')
o('egg_bunny_ears',FL+5.5,6,'group',radius=1,egg=True,name='Easter egg: two bunny ears poke out of the grass',
  parts=[dict(kind='box',pos=[-0.25,0.5,0],size=[0.25,1.0,0.25],color='#ffffff'),dict(kind='box',pos=[0.25,0.5,0],size=[0.25,1.0,0.25],color='#ffffff')])
# Last step
L.events+=[dict(t=HG,type='color',palette=dict(skyTop='#b9d3db',skyBottom='#f2dfe8'),dur=2.0),
 dict(t=FL,type='color',palette=dict(skyTop='#cfe3e0',skyBottom='#fbeee2',ground='#a8c59a'),dur=2.0),
 dict(t=FL,type='particles',particles='dust',until=END),dict(t=LS,type='color',palette=dict(light='#fff1dc'),dur=3.0)]
L.camera=[dict(t=0,preset='iso',blend=0),dict(t=WL,preset='close',blend=1.5,note='narrow alley'),dict(t=HG,preset='high',blend=1.5,note='switchback knot climbs; high so laps stay visible'),
 dict(t=FL,preset='iso',yaw=-20,blend=1.5),dict(t=LS,preset='wide',blend=3.0)]
place_collectibles(L,[2.8,6.3,10.3,14.3,18.4,21.3,26.3,28.8,30.8,34.0],[12.3,FL+0.5])
L.art=dict(backdrop='art/dawn.jpg',ground=dict(src='art/grass.jpg',scale=30),
  catalog=[dict(file='art/dawn.jpg',use='backdrop: dawn after rain over shallow water'),dict(file='art/grass.jpg',use='ground: moon-green grass'),
           dict(file='art/five-lights.jpg',use='album-motif mural (five ribbons + folded wings)')])
layout=dict(id='get-up',title='Get Up',
 palette=dict(skyTop='#A8C8D1',skyBottom='#ece3ee',fog='#d8dbe6',fogStart=25,fogEnd=90,ground='#b9c9d6',groundY=-1.5,road=ROAD,roadSide=LAV,line=PINK,light='#fff6ee',lightIntensity=1.0,ambient='#c6c4dc',particles=None),
 road=dict(width=L.widths,height=0.6,reveal=[dict(t=0,mode='rise',lead=2.5),dict(t=WL,mode='unfold',lead=2.0),dict(t=HG,mode='rise',lead=2.0),dict(t=FL,mode='rise',lead=2.0)]),
 elevation=L.elev,
 sections=[dict(t=x['t'],label=x['label'],camera=[c for c in L.camera if c['t']<=x['t']+0.01][-1].get('preset')) for x in L.secs],
 camera=L.camera,events=L.events,diamonds=L.layout_diamonds,crowns=L.layout_crowns,finish=dict(kind='gate',color='#E7B44C'),collectibleColors=dict(diamond='#56D7E8',crown='#E7B44C'))
for sec,p in zip(layout['sections'],[dict(ground='#b9c9d6'),dict(ground='#8f89ab'),dict(skyTop='#b9d3db'),dict(ground='#a8c59a',groundY=-6),None]):
    if p: sec['palette']=p
L.write(dict(bpm=120.022,grid=dict(t0=0.335,sixteenth=0.124977,note='bar n starts at t0+1.99963*n (low-confidence grid, ambient track)'),
  judgment=dict(perfect=0.050,good=0.100,miss_beyond=0.125,note='recommended; see chart-report.md'),
  notes='39 taps (old 16, x2.44) on half-bar vocal swells; no runs longer than 2 taps; whole 36 s file.'),layout)
L.plot()
print('ok hits',len(L.hits),'passes',len(L.passes),'objects',len(L.objects))
