from speclib import *
title='Hurt'; start='N'
P=dict(mist='#DDE9EF',ivory='#F5F1E8',cobalt='#243C9F',navy='#182446',sage='#A8B9A5',blush='#E5BCB3',coral='#D76F72',gold='#E3BC65')
palette=dict(skyTop='#C9DAE6',skyBottom=P['mist'],fog=P['mist'],fogStart=35,fogEnd=105,ground='#D3E2EA',groundY=-10,
  road=P['ivory'],roadSide=P['navy'],line=P['coral'],light='#FFF3E6',lightIntensity=0.95,ambient='#B7C6D4',particles=None)
width=[{'t':0,'w':2.2},{'t':128.26,'w':2.0},{'t':143.594,'w':2.2}]
reveal=[{'t':0,'mode':'rise','lead':2.0},{'t':42.927,'mode':'unfold','lead':1.8},{'t':80.26,'mode':'fade','lead':2.2},
        {'t':96.26,'mode':'unfold','lead':1.8},{'t':117.594,'mode':'rise','lead':2.0},{'t':128.26,'mode':'rise','lead':1.6},{'t':143.594,'mode':'fade','lead':2.2}]
sections=[
 {'t':0,'label':'Intro','note':'01 L0 sparse long entrance at about one tap per bar; outer bases lift on the intro beats; road fully shown first.'},
 {'t':10.927,'label':'Verse 1','note':'02 L0 offset short corridor, five empty portrait frames close in (one rises per vocal phrase).','palette':{'fogEnd':85}},
 {'t':32.26,'label':'Pre-chorus 1','note':'03 R1 ramp L0->L1 (+2.5), the unsent blank folded paper opens outward away from the road.','palette':{'fogEnd':110}},
 {'t':42.927,'label':'Chorus 1','note':'04 L1 open balcony bending around the quiet square court with the halftone bunny wall; each title repeat lights a row of dots. CP1 at exit.','palette':{'skyTop':'#BCD0E2'}},
 {'t':64.26,'label':'Verse 2','note':'05 L1 long-short-long switchback heading SW, reed clumps and thin navy pillars (hair strands) on the outer edge.','palette':{'fogEnd':90}},
 {'t':80.26,'label':'Breath','note':'05 vocal-gap breath: almost no taps, long straight over still water, scenery holds still.','palette':{'skyTop':'#D4E1EA','fogEnd':130}},
 {'t':85.594,'label':'Pre-chorus 2','note':'05 pre 2: paper panels fold outward again, the corridor opens.'},
 {'t':96.26,'label':'Chorus 2','note':'06 R2 ramp L1->L2 (+2.5) onto the double-ear trestle: open U at the bottom of the map (SW down, SE across, NE up). E1 five pixel bunnies under the trestle. CP2 at exit.','palette':{'skyTop':'#B4C8E0','ground':'#C8D9E6'}},
 {'t':117.594,'label':'Bridge','note':'07 B2 long quiet span, R3 descends L2->L1 (-2.5), fewer bends; outer thin panels retract.','palette':{'fogEnd':140}},
 {'t':128.26,'label':'Final chorus','note':'08 L1 three fan terraces (short NW offsets), five frames open on alternating beats, bunny wall dots complete; short 16th vocal pairs; road 2.0.','palette':{'skyTop':'#E2D3D3','skyBottom':'#F1E7E2'}},
 {'t':143.594,'label':'Outro','note':'09 L1 last long straights to the square quiet platform; first light of dawn, frames stop moving.','palette':{'skyTop':'#F0DCCF','skyBottom':'#F7EEE6','light':'#FFE8D2'}},
]
camera=[{'t':0,'preset':'iso','dist':18,'pitch':50,'blend':0},{'t':10.927,'preset':'iso','dist':16,'blend':3.0},
 {'t':32.26,'preset':'iso','dist':18,'blend':3.0},{'t':42.927,'preset':'wide','dist':21,'blend':2.0},
 {'t':64.26,'preset':'iso','dist':17,'blend':3.0},{'t':80.26,'preset':'side','dist':20,'blend':3.0},
 {'t':85.594,'preset':'iso','dist':18,'blend':3.0},{'t':96.26,'preset':'wide','dist':22,'blend':2.0},
 {'t':117.594,'preset':'high','dist':22,'blend':3.0},{'t':128.26,'preset':'iso','dist':19,'blend':2.0},
 {'t':143.594,'preset':'iso','dist':19,'blend':3.0},{'t':160.0,'preset':'wide','dist':26,'blend':6.0}]
frames=[{'id':f'portrait-frame-{i}','t':13.0+3.9*i,'side':(-1)**i*5.5,'kind':'group','radius':2.5,'name':'empty portrait frame',
  'parts':[part('box',[0,2.5,-0.9],[2.6,0.3,0.2],P['ivory']),part('box',[0,2.5,0.9],[2.6,0.3,0.2],P['ivory']),
           part('box',[0,1.3,0],[2.6,0.3,2],P['ivory']),part('box',[0,3.7,0],[2.6,0.3,2],P['ivory']),part('plane',[0,2.5,0],[2.2,1,2.2],'#EEF3F6')],
  'appear':appear(10.927+2.667*i*1.5,'rise',1.0)} for i in range(5)]
frames[2]['landmark']=True; frames[2]['name']='M1 five empty portrait frames'
paper={'id':'unsent-paper','t':37.0,'side':-8,'kind':'group','radius':4,'landmark':True,'name':'M2 unsent blank folded letter',
  'parts':[part('box',[-1.6,1.5,0],[3,0.1,4],'#FBF8F2',[0,0,25]),part('box',[1.6,1.5,0],[3,0.1,4],'#FBF8F2',[0,0,-25]),part('box',[0,0.8,0],[0.2,1.5,4],P['blush'])],
  'appear':appear(32.26,'unfold',2.6)}
bunny=bunny_relief('halftone-bunny-wall',52.0,18,P['cobalt'],P['ivory'],scale=1.1,landmark=True,name='M3 halftone bunny wall (2022 EP cover)',appear=appear(40.3,'rise',2.5))
ears=[{'id':f'ear-pier-{i}','t':t,'side':-6,'kind':'box','size':[2.2,8,6],'color':P['ivory'],'color2':P['cobalt'],'name':'M4 ear pier','landmark':i==0,
       'appear':appear(t-4.0,'rise',1.2)} for i,t in enumerate([101.0,112.5])]
egg={'id':'egg-pixel-bunnies','t':99.0,'side':4,'y':-2.4,'kind':'group','radius':4,'egg':True,'name':'E1 five pixel bunnies under the trestle',
  'parts':sum([[part('box',[-3+1.5*i,0.4,0],[0.8,0.8,0.8],'#FFFFFF'),part('box',[-3.2+1.5*i,1.1,0],[0.2,0.6,0.2],'#FFFFFF'),part('box',[-2.8+1.5*i,1.1,0],[0.2,0.6,0.2],'#FFFFFF')] for i in range(5)],[]),
  'appear':appear(97.0,'pop',0.5),'exit':exitm(103.0,'fade',1.0)}
fan=[{'id':f'fan-terrace-{i}','t':130.0+4.5*i,'side':(-1)**(i+1)*9,'kind':'group','radius':6,'name':'M5 opening frame terrace',
  'parts':[part('box',[0,-0.6,0],[8,1.2,6],P['sage']),part('box',[0,2,0],[0.3,3,5],P['ivory']),part('box',[0,-3,0],[7.6,4,5.6],P['navy'])],
  'appear':appear(128.26+0.667*i,'unfold',1.0)} for i in range(3)]
platform={'id':'quiet-platform','t':168.0,'side':6,'kind':'group','radius':6,'landmark':True,'name':'square quiet platform at dawn',
  'parts':[part('box',[0,-0.6,0],[10,1.2,10],P['ivory']),part('box',[0,-3.5,0],[9.6,5,9.6],P['navy']),part('box',[0,0.8,0],[1.2,1.6,1.2],P['blush'])],'appear':appear(160.0,'rise',2.0)}
objects=[
 {'id':'outer-bases','kind':'row','t0':0.5,'t1':10.5,'side':7,'spacing':6,'bothSides':True,'item':{'kind':'box','size':[3,1,3],'color':P['sage']}},
 ]+frames+[paper,bunny,
 {'id':'hair-pillars','kind':'row','t0':64.5,'t1':96,'side':6,'spacing':3.5,'bothSides':False,'item':{'kind':'cylinder','size':[0.3,7,0.3],'color':P['navy'],'react':'beat'}},
 {'id':'reeds','kind':'row','t0':66,'t1':95,'side':-5,'spacing':5,'bothSides':False,'item':{'kind':'cone','size':[1,2.5,1],'color':P['sage']}},
 {'id':'still-water','t':83.0,'side':0,'y':-2.0,'kind':'water','size':[30,0.2,30],'color':'#C9DCE8','name':'still water under the breath straight'},
 ]+ears+[egg]+fan+[platform,
 {'id':'trees','kind':'row','t0':0,'t1':171,'side':18,'spacing':22,'bothSides':True,'item':{'kind':'tree','size':[3,5,3],'color':P['sage']}}]
BEAT=0.6667
events=[
 {'t':0.26,'type':'raise','target':'outer-bases','every':BEAT*4,'until':10.9},
 {'t':42.927,'type':'light','target':'halftone-bunny-wall','every':BEAT*4,'until':64.0,'note':'one row of dots per bar of the chorus'},
 {'t':80.26,'type':'color','palette':{'skyTop':'#D4E1EA'},'dur':2.0},
 {'t':96.26,'type':'raise','target':'ear-pier-0','dur':1.5},
 {'t':117.594,'type':'lower','target':'hair-pillars','dur':3.0},
 {'t':128.26,'type':'pulse','target':'fan-terrace-0','every':BEAT*2,'until':143.5},
 {'t':143.594,'type':'color','palette':{'skyTop':'#F0DCCF','skyBottom':'#F7EEE6'},'dur':6.0},
 {'t':143.594,'type':'particles','particles':'dust','until':175}]
diamond_windows=[(0,10.93,1),(10.93,32.26,2),(32.26,42.93,1),(42.93,64.26,1),(64.26,96.26,2),(96.26,117.6,1),(117.6,128.26,1),(128.26,171,1)]
crown_near=[64.0,117.4]
finish={'kind':'pyramid','color':P['cobalt']}
chart_notes='Hurt 90 BPM (beat 0.667 s, downbeat 0.260 s). 144 taps (old 64, 2.25x; still only 0.82 taps/s - the calmest level). Mostly vocal-phrase taps (demucs vocal stem, -25 ms corrected) with snare backbeat anchors; final chorus allows short 16th-note vocal pairs. Min gap 0.316 s. Recommended judgment window +-100 ms.'
