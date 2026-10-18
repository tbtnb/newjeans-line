from route_eta import *
L=make(); T=L.taps; o=L.obj
assert not L.hits, L.hits
COV=['#77C9ED','#A5DFB5','#F3A8C8','#F8BB7D','#B1A1E3']
s=[x['t'] for x in L.secs]+[L.dur]
I,V1,P1,C1,S1,V2,P2,P3,C2,S2,FA,FB,OUT,END=s
# --- Intro · Call Court: the line starts inside a giant phone frame
gate_over(L,'phone_frame',0.45,color='#203750',color2='#203750',h=6.5,name='Giant phone door-frame (start: the line leaves through the screen)')
o('phone_body',0.3,-7,'phone',[5,11,1],color='#203750',color2='#CDEFF0',landmark=True,name='Standing phone (Call Court)',rot=15)
image(L,'egg_bunny_sticker',0.3,-7,'art/bunny-sticker.png',[1.6,0,1.6],mode='upright',y=6,egg=True,along=-0.6,
      name='Easter egg: pixel bunny sticker on the back of the phone (seen when the camera swings at 3 s)')
row(L,'court_benches',1.2,V1-0.3,4.5,5.0,dict(kind='bench',size=[2.4,0.9,0.9],color='#FFF2D7'))
o('palm_c1',3.0,6,'tree',[2,5,2],color='#4f9a5a',color2='#8a6a4a',react='beat')
# --- Verse 1 · terracotta alley switchbacks (narrow, walls tight both sides)
row(L,'alley_walls',V1+0.3,P1-0.2,2.1,2.3,dict(kind='box',size=[0.8,2.6,2.0],color='#CE785A',color2='#e8a07f',react='tap'),appear=dict(mode='rise',dur=0.4))
for i,tt in enumerate([V1+3.6,V1+8.9]):
    fake_fork(L,f'fork_alley_{i}',tt,(-1)**i,length=6,color='#d8b9a3',name='side alley stub (visual fake-out, lower & ends at a planter)')
o('red_car',V1+6.0,-5,'group',radius=2.2,landmark=True,name='Little red car parked in the switchback bend',
  parts=[dict(kind='box',pos=[0,0.6,0],size=[2.0,1.0,3.6],color='#F05A50'),dict(kind='box',pos=[0,1.4,-0.2],size=[1.7,0.8,2.0],color='#ffd9cf'),
         dict(kind='cylinder',pos=[-1,0.3,1.2],size=[0.6,0.3,0.6],rot=[0,0,90],color='#203750'),dict(kind='cylinder',pos=[1,0.3,1.2],size=[0.6,0.3,0.6],rot=[0,0,90],color='#203750'),
         dict(kind='cylinder',pos=[-1,0.3,-1.2],size=[0.6,0.3,0.6],rot=[0,0,90],color='#203750'),dict(kind='cylinder',pos=[1,0.3,-1.2],size=[0.6,0.3,0.6],rot=[0,0,90],color='#203750')])
for i in range(4): o(f'bougainvillea_{i}',V1+1.5+i*3.4,(-1)**i*4.2,'flower',[1.2,1.2,1.2],color='#F3A8C8',react='beat')
# --- Pre 1 · phone bridge: long climbing staircase of message cards
row(L,'msg_cards',P1,C1-0.2,3.4,2.8,dict(kind='box',size=[2.0,0.12,1.3],color='#ffffff',react='tap'),appear=dict(mode='unfold',dur=0.35))
o('relay_mast',P1+7,10,'tower',[2,16,2],color='#FFF2D7',color2='#F05A50',react='kick')
gate_over(L,'bridge_gate',P1+0.6,color='#FFF2D7',color2='#35C4C8',name='Phone-bridge gate')
# --- Chorus 1 · pool party: the road wraps three sides of the pool
cx,cz,cy=centre(L,C1,S1)
L.world('pool',cx,cz,cy-1.0,'group',landmark=True,name='Pool party (the hook wraps around it)',
  parts=[dict(kind='box',pos=[0,0,0],size=[14,0.4,14],color='#35C4C8'),dict(kind='box',pos=[0,-0.3,0],size=[15.5,0.4,15.5],color='#FFF2D7')]+
        [dict(kind='torus',pos=[(-4+2*i),0.35,(i%2)*3-1.5],size=[1.6,0.4,1.6],color=COV[i]) for i in range(5)])
for i in range(5): L.events.append(dict(t=round(C1+i*0.889,3),type='raise',target='pool',dy=0,dur=0.2,note='floats bob in on the first five beats of the hook'))
for i in range(6): o(f'palm_pool_{i}',C1+1+i*2.0,(-1)**i*5.5,'tree',[2,5.5,2],color='#4f9a5a',color2='#8a6a4a',react='beat')
image(L,'pool_poster',C1+5.5,9,'art/heart-poster.png',[6,0,4],mode='billboard',y=2,name='Pool-party pixel-heart poster')
# --- Stop 1 · E-T-A voice chops (pinwheel)
for i,ch in enumerate('ETA'):
    o(f'letter1_{ch}',S1+0.4*i,-4.5-1.5*i,'text',[2.2,0,2.2],name=ch,color=COV[i],react='tap')
# --- Verse 2 · rooftop hops (road on roofs; jumps between them)
for i,(tt,dur) in enumerate(long_pieces(L,V2,P2,0.4)[:8]):
    o(f'roof_{i}',tt+dur/2,0,'building',[4,6,4],y=-6.6,onroad=True,color='#e8b494',color2='#CE785A',name='rooftop under the road')
row(L,'chimneys',V2,P2,4.0,4.5,dict(kind='box',size=[0.7,1.6,0.7],color='#CE785A',react='kick'))
image(L,'roof_poster',V2+6,-7,'art/heart-poster.png',[5,0,3.4],mode='upright',y=2.5,name='Rooftop billboard')
fake_fork(L,'fork_roof',V2+9.5,1,length=7,color='#e0c2ad',name='roof plank to nowhere (visual fake-out)')
# --- Pre 2 · cliff switchbacks descending along a sea cliff
o('cliff_wall',P2+7,-9,'box',[6,14,30],y=-10,color='#d9b48f',color2='#c28c66',name='Sea cliff the switchbacks hug')
o('egg_cliff_bunny',P2+9.3,-6.4,'group',radius=1,y=0.5,egg=True,name='Easter egg: pixel bunny peeking from a crack in the cliff',
  parts=[dict(kind='box',pos=[0,0.5,0],size=[0.8,0.8,0.4],color='#ffffff'),dict(kind='box',pos=[-0.2,1.2,0],size=[0.2,0.6,0.2],color='#ffffff'),dict(kind='box',pos=[0.2,1.2,0],size=[0.2,0.6,0.2],color='#ffffff')])
fake_fork(L,'fork_cliff',P2+4.2,1,length=8,color='#e7d3bb',name='broken cliff ledge (visual fake-out, drops off into the sea)')
row(L,'cliff_rails',P2,P3,2.0,2.6,dict(kind='box',size=[0.25,0.8,0.25],color='#FFF2D7'),bothSides=False)
# --- Pre 3 · helix round the five-colour pixel tower (skyline landmark, seen again from Chorus 2 and Final A)
hx,hz,hy=centre(L,P3,C2)
L.world('pixel_tower',hx,hz,-3,'group',landmark=True,name='Five-colour pixel tower (helix centre, skyline landmark)',
  parts=[dict(kind='box',pos=[0,2+4*i,0],size=[5-0.5*i,4,5-0.5*i],color=COV[i]) for i in range(5)]+[dict(kind='star',pos=[0,23,0],size=[2.5,2.5,2.5],color='#F2C34E')],react='kick')
L.events+=[dict(t=P3,type='light',target='pixel_tower',every=1.7778,level=0.8,note='one colour band lights per bar while the line circles up'),
           dict(t=C2,type='spin',target='pixel_tower',until=S2)]
# --- Chorus 2 · sea-cliff sky bridge (passes over earlier sections)
row(L,'bridge_rails',C2,S2,1.9,2.2,dict(kind='box',size=[0.2,0.9,1.6],color='#FFF2D7'))
for i in range(5):
    o(f'scene_panel_{i}',C2+1.2+i*1.7778,(-1)**i*9,'box',[4,4,0.4],y=3,color=COV[i],appear=dict(t=C2+i*1.7778,mode='drop',dur=0.5),name='five assembled-scene panels')
gate_over(L,'skybridge_gate',C2+0.3,color='#ffffff',color2='#F2C34E',name='Sky-bridge gate')
# --- Stop 2: drop off the bridge
for i,ch in enumerate('ETA'):
    o(f'letter2_{ch}',S2+0.4*i,4.5+1.5*i,'text',[2.2,0,2.2],name=ch,color=COV[i+2],react='tap')
# --- Final A · pixel heart lobe (road loops round a giant flat pixel heart)
fx,fz,fy=centre(L,FA,FB)
L.world('pixel_heart',fx,fz,fy-2.5,'image',landmark=True,name='Giant flat pixel heart (Final A loops around it)',src='art/heart-poster.png',size=[16,0,11],mode='flat')
row(L,'heart_lamps',FA,FB,3.2,4.0,dict(kind='lamp',size=[0.4,3.5,0.4],color='#ffffff',color2='#F2C34E',react='tap'))
# --- Final B · arrival sprint (narrow wiggle corridor + five windows egg)
row(L,'sprint_posts',FB,OUT,1.6,1.8,dict(kind='box',size=[0.3,1.1,0.3],color='#F05A50',react='tap'))
for i in range(5):
    o(f'egg_window_{i}',FB+2+i*0.45,-7,'box',[1.4,1.8,0.3],y=3,color='#203750',color2=COV[i],egg=(i==2),name='Easter egg: five windows that light one per beat' if i==2 else 'window')
    L.events.append(dict(t=round(FB+3.5556+i*0.4445,3),type='light',target=f'egg_window_{i}',note='beats, not tap times'))
fake_fork(L,'fork_sprint',FB+9.6,-1,length=6,color='#f3c6b9',name='closed side street (visual fake-out)')
# --- Outro · bench between two lamps
tb=slot_near(T,OUT+7)
o('bench',tb,-5,'bench',[3,1,1],landmark=True,name='Bench between two lamps (arrival)',color='#FFF2D7')
o('lamp_a',tb,-4,'lamp',[0.4,4.5,0.4],along=-2.5,color='#ffffff',color2='#F2C34E')
o('lamp_b',tb,-4,'lamp',[0.4,4.5,0.4],along=2.5,color='#ffffff',color2='#F2C34E')
L.events+=[dict(t=OUT+1.8,type='light',target='lamp_a'),dict(t=OUT+3.6,type='light',target='lamp_b')]
# --- palette / music events
L.events+=[dict(t=V1,type='burst',at='player',particles='pixels'),
 dict(t=C1,type='color',palette=dict(skyTop='#7fd6e0',skyBottom='#fff2d7'),dur=1.5),
 dict(t=S1,type='color',palette=dict(skyTop='#a9c3c9'),dur=0.3,note='voice-only stop: colour drains'),
 dict(t=V2,type='color',palette=dict(skyTop='#9fdbe6'),dur=0.6),
 dict(t=C2,type='color',palette=dict(skyTop='#62c3e8',skyBottom='#fff6e6'),dur=2.0),
 dict(t=C2,type='particles',particles='confetti',until=S2),
 dict(t=S2,type='color',palette=dict(skyTop='#a9c3c9'),dur=0.3),
 dict(t=FA,type='color',palette=dict(skyTop='#ffb59a',skyBottom='#ffe9c9',fog='#ffe3cf'),dur=3.0,note='golden hour'),
 dict(t=OUT,type='color',palette=dict(skyTop='#f8c58f',skyBottom='#fff4df',light='#ffd9a0'),dur=3.0)]
L.camera=[dict(t=0,preset='close',blend=0),dict(t=3.0,preset='iso',yaw=-25,blend=2.0,note='swing reveals the sticker'),
 dict(t=V1,preset='iso',blend=1.0),dict(t=P1,preset='iso',yaw=15,blend=1.5),dict(t=C1,preset='high',blend=1.2),
 dict(t=S1,preset='close',blend=0.4),dict(t=V2,preset='iso',blend=0.8),dict(t=P2,preset='side',yaw=60,blend=1.5,note='cliff on screen edge'),
 dict(t=P3,preset='high',blend=1.5,note='helix: high camera so upper laps do not hide lower'),dict(t=C2,preset='wide',blend=1.5),
 dict(t=C2+7.1,preset='high',blend=2.0),dict(t=S2,preset='top',blend=0.4),dict(t=FA,preset='high',blend=1.0),
 dict(t=FB,preset='iso',blend=1.0,shake=0.08),dict(t=OUT,preset='high',blend=2.0),dict(t=OUT+5,preset='wide',blend=4.0)]
place_collectibles(L,[3.4,15,27,41,55,70,86,99,113,128],[S1,S2])
L.layout_crowns[1]=dict(t=slot_near(T,77.0,0.8),note='checkpoint at the foot of the tower helix (last calm straight of Pre 2)')
L.art=dict(backdrop='art/sky.jpg',ground=dict(src='art/sea.jpg',scale=60),
  catalog=[dict(file='art/sky.jpg',use='backdrop: summer sea sky with voxel clouds'),dict(file='art/sea.jpg',use='ground texture: turquoise sea'),
           dict(file='art/terracotta-tile.jpg',use='texture on the alley walls / roofs'),dict(file='art/heart-poster.png',use='posters, giant flat pixel heart'),
           dict(file='art/bunny-sticker.png',use='egg decal on the phone back')])
layout=dict(id='eta',title='ETA',
 palette=dict(skyTop='#9fdbe6',skyBottom='#f4fbf8',fog='#dff3f2',fogStart=40,fogEnd=130,ground='#35C4C8',groundY=-10,road='#FFF2D7',roadSide='#e2c9a6',line='#F05A50',light='#fff6e8',lightIntensity=1.15,ambient='#c9e8ea',particles=None),
 road=dict(width=L.widths,height=0.6,reveal=[dict(t=0,mode='static',lead=3.0),dict(t=V1,mode='rise',lead=1.6),dict(t=P1,mode='unfold',lead=1.5),dict(t=C1,mode='rise',lead=1.6),dict(t=V2,mode='drop',lead=1.5),dict(t=P3,mode='rise',lead=1.8),dict(t=FB,mode='rise',lead=1.3),dict(t=OUT,mode='static',lead=3.0)]),
 elevation=L.elev,
 sections=[dict(t=x['t'],label=x['label'],camera=[c for c in L.camera if c['t']<=x['t']+0.01][-1].get('preset')) for x in L.secs],
 camera=L.camera,events=L.events,diamonds=L.layout_diamonds,crowns=L.layout_crowns,
 finish=dict(kind='gate',color='#F2C34E'),collectibleColors=dict(diamond='#35D6E5',crown='#F2C34E'))
for sec,p in zip(layout['sections'],[None,dict(ground='#d9a07f',groundY=-8),None,dict(skyTop='#7fd6e0'),dict(skyTop='#a9c3c9'),dict(ground='#e8b494'),dict(ground='#35C4C8'),dict(fogEnd=160),dict(skyTop='#62c3e8',groundY=-14),None,dict(skyTop='#ffb59a'),dict(line='#e8443a'),dict(skyTop='#f8c58f')]):
    if p: sec['palette']=p
L.write(dict(bpm=134.998,grid=dict(t0=1.6699,sixteenth=0.111113,note='bar n starts at t0+1.7778*n'),
  judgment=dict(perfect=0.040,good='half the local gap, max 0.100 (0.055 in 16th bursts)',miss_beyond=0.090,note='schema v2.5 per-tap windows; see chart-report.md'),
  notes='Hand-composed motif chart, 422 taps (old 232, x1.82), tier hard. 8th runs plus 12 16th-burst taps on real fills/rolls/syllables (min gap 0.111 s). Avg 167 CPM, peak 420 CPM (1 s window). Fastest run 19 taps (131.0-134.7 s).'),layout)
L.plot()
print('ok hits',len(L.hits),'passes',len(L.passes),'objects',len(L.objects))
