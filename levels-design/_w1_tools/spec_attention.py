from speclib import *
title='Attention'; start='N'
P=dict(deep='#243A8A',denim='#4F75CB',ice='#C7E3EF',ivory='#F4F0DB',grass='#64AA71',coral='#EF6555',gold='#E9BE61')
palette=dict(skyTop='#9FC6E6',skyBottom='#EAF4F8',fog='#DCEAF2',fogStart=40,fogEnd=120,ground='#C7E3EF',groundY=-14,
  road=P['ivory'],roadSide=P['denim'],line=P['coral'],light='#FFF4E2',lightIntensity=1.15,ambient='#B9CDE3',particles=None)
width=[{'t':0,'w':2.2},{'t':117.03,'w':2.0},{'t':137.6,'w':1.9},{'t':156.1,'w':2.2}]
reveal=[{'t':0,'mode':'rise','lead':1.8},{'t':62.18,'mode':'unfold','lead':1.6},{'t':101.6,'mode':'fade','lead':1.6},
        {'t':117.03,'mode':'rise','lead':1.4},{'t':137.6,'mode':'drop','lead':1.3},{'t':156.1,'mode':'rise','lead':1.8}]
sections=[
 {'t':0,'label':'Intro','note':'01 rooftop courtyard, L0. Long straights, calm; the line starts on a sunny roof beside the water tower.'},
 {'t':9.607,'label':'Hook A','note':'01 cont. bass enters (bar 4 beat 2): roof blocks rise row by row (P1 prelude); first staircase on the beat grid.','palette':{'skyTop':'#8DBCE4'}},
 {'t':27.893,'label':'Verse 1','note':'02 roof courts, L0, narrow: courtyard walls close in on both sides; vocal-syncopated turns.','palette':{'fogEnd':95}},
 {'t':46.75,'label':'Pre-chorus 1','note':'03 sky bridge B1: continuous ramp L0->L1 (+4) over the void; course swings from NE to SE.','palette':{'fogEnd':130}},
 {'t':62.18,'label':'Chorus 1','note':'04 open stadium (MV football pitch): space opens, stands unfold; route wraps the pitch in a U (SW dip, SE run, NE climb).','palette':{'skyTop':'#7FB6E8','ground':'#BFE0D0'}},
 {'t':83.32,'label':'Verse 2','note':'05 window strip on L1: closed, offset corridor of window panes; long SW run down the east side.','palette':{'fogEnd':100}},
 {'t':101.6,'label':'Pre-chorus 2','note':'06 quiet span B2 (L1->L2 ramp +4), five amber windows easter egg on the outer wall.','palette':{'skyTop':'#A9C8EC','fogEnd':140}},
 {'t':117.03,'label':'Chorus 2','note':'07 terraces fan open on L2; narrower road (2.0); SW then NW.','palette':{'skyTop':'#78ACE6'}},
 {'t':137.6,'label':'Final chorus','note':'08 double-ear gallery: two NE/SW notches = bunny ears; bunny relief resolves block by block (P5). Road 1.9.','palette':{'skyTop':'#5E8FD9','skyBottom':'#DCEBF7'}},
 {'t':156.1,'label':'Outro','note':'09 cover square: road widens, long release lines, warm late light; finish into the deep-blue cover plaza.','palette':{'skyTop':'#F2C9A8','skyBottom':'#FBEEDC','light':'#FFE3C4'}},
]
camera=[{'t':0,'preset':'iso','blend':0,'dist':16},
 {'t':9.607,'preset':'iso','blend':1.5},
 {'t':27.893,'preset':'iso','dist':15,'blend':2.0},
 {'t':46.75,'preset':'iso','dist':19,'pitch':45,'blend':2.5},
 {'t':62.18,'preset':'wide','dist':22,'blend':1.2},
 {'t':71.33,'preset':'iso','dist':19,'blend':2.0},
 {'t':83.32,'preset':'iso','dist':16,'blend':2.0},
 {'t':101.6,'preset':'side','dist':18,'blend':3.0},
 {'t':112.47,'preset':'iso','dist':18,'blend':3.0},
 {'t':117.03,'preset':'wide','dist':21,'blend':1.2},
 {'t':137.6,'preset':'high','dist':20,'blend':1.5},
 {'t':147.33,'preset':'iso','dist':18,'blend':2.0},
 {'t':156.1,'preset':'iso','dist':17,'blend':2.5},
 {'t':168.0,'preset':'wide','dist':26,'blend':5.0}]
water_tower={'id':'water-tower','t':3.0,'side':-7,'kind':'group','radius':3,'landmark':True,'name':'Rooftop water tower',
  'parts':[part('cylinder',[0,4.5,0],[3,2.6,3],'#5E86C9'),part('cone',[0,6.3,0],[3.2,1.0,3.2],'#4F75CB'),
           part('box',[-1,1.6,-1],[0.25,3.2,0.25],'#7A8FA8'),part('box',[1,1.6,-1],[0.25,3.2,0.25],'#7A8FA8'),
           part('box',[-1,1.6,1],[0.25,3.2,0.25],'#7A8FA8'),part('box',[1,1.6,1],[0.25,3.2,0.25],'#7A8FA8')]}
def stand(i,t):
    return {'id':f'stand-{i}','t':t,'side':16,'kind':'group','radius':7,'react':'kick','name':f'Stadium stand {i}',
      'parts':[part('stairs',[0,1.5,0],[10,3,4],'#F4F0DB'),part('box',[0,5.2,1.6],[10.5,0.4,4.5],'#F7F6EE'),
               part('box',[-4.6,3.4,2.4],[0.3,3.6,0.3],'#C9D4E4'),part('box',[4.6,3.4,2.4],[0.3,3.6,0.3],'#C9D4E4'),
               part('box',[0,0.9,-1.6],[10,0.5,0.6],'#4F75CB')],
      'appear':appear(62.18+0.5714*2*i,'unfold',0.9)}
pitch={'id':'stadium-pitch','t':70.5,'side':24,'kind':'group','radius':16,'landmark':True,'name':'MV football pitch (open stadium)',
  'parts':[part('box',[0,-0.5,0],[30,1.0,20],'#64AA71'),part('box',[0,0.05,0],[0.3,0.05,20],'#FFFFFF'),
           part('torus',[0,0.05,0],[5,0.2,5],'#FFFFFF'),part('box',[0,0.05,9.8],[30,0.05,0.3],'#FFFFFF'),part('box',[0,0.05,-9.8],[30,0.05,0.3],'#FFFFFF'),
           part('box',[-14.6,1.0,0],[0.3,2,5],'#FFFFFF'),part('box',[14.6,1.0,0],[0.3,2,5],'#FFFFFF'),
           part('box',[0,-4,0],[30,7,20],'#4F75CB')],
  'appear':appear(60.8,'rise',1.2)}
five_windows={'id':'egg-five-windows','t':109.0,'side':-6,'kind':'group','radius':6,'egg':True,'name':'E1 five window lights',
  'parts':[part('box',[0,2.5,0],[11,5,0.8],'#C7D6EA')]+[part('box',[-4+2*i,3,-0.5],[1.4,1.8,0.3],'#6A7A92') for i in range(5)],
  'appear':appear(104.0,'rise',1.0)}
terraces=[{'id':f'terrace-{i}','t':121.0+3.2*i,'side':9+2*i,'kind':'group','radius':6,'name':f'Terrace {i}',
  'parts':[part('box',[0,-1,0],[9,2,7],'#F4F0DB'),part('box',[0,-4,0],[8.6,4,6.6],'#4F75CB'),part('tree',[2.5,1.5,1.5],[1.6,3,1.6],'#64AA71')],
  'appear':appear(117.03+0.5714*i,'unfold',0.9)} for i in range(3)]
bunny=bunny_relief('cover-bunny-relief',141.0,30,P['deep'],'#F7F6EE',scale=1.2,landmark=True,name='M4 2022 EP cover bunny relief',
  appear=appear(137.6,'rise',2.0))
ears=[{'id':f'ear-gallery-{i}','t':t,'side':-5,'kind':'box','size':[2.4,9,8],'color':'#F7F6EE','color2':P['denim'],'name':'ear gallery pylon',
       'appear':appear(t-3.0,'rise',0.9)} for i,t in enumerate([141.6,150.2])]
cover_square={'id':'cover-square','t':171.5,'side':8,'kind':'group','radius':7,'landmark':True,'name':'M5 cover square',
  'parts':[part('box',[0,-0.8,0],[12,1.6,12],P['deep']),part('box',[0,0.2,0],[8,0.4,8],'#F4F0DB'),part('box',[3,1.4,3],[2,2.4,2],'#F4F0DB'),
           part('box',[-3,0.9,2.5],[1.6,1.4,1.6],P['gold'])],'appear':appear(165.0,'rise',1.5)}
objects=[water_tower,
 {'id':'roofs-a','kind':'row','t0':0.5,'t1':27.5,'side':6,'spacing':7,'bothSides':True,'item':{'kind':'building','size':[4,3,4],'color':'#F1ECDD','color2':'#E39A7F'}},
 {'id':'cloth-1','t':12.5,'side':5,'kind':'group','radius':2,'react':'beat','name':'coral cloth panels',
  'parts':[part('box',[0,2,0],[0.1,2.4,1.6],P['coral']),part('box',[0,2,2],[0.1,2.4,1.6],P['coral']),part('box',[0,3.3,1],[0.1,0.1,4],'#888888')],'appear':appear(9.607,'pop',0.4)},
 {'id':'courts','kind':'row','t0':28.2,'t1':46.5,'side':4.5,'spacing':4.5,'bothSides':True,'item':{'kind':'box','size':[2.5,4,3.5],'color':'#EDE6D6','react':'tap'}},
 {'id':'sky-bridge-arch','t':47.2,'side':0,'kind':'arch','size':[6,6,1.2],'color':'#F4F0DB','y':0,'name':'B1 sky bridge gate','landmark':True},
 {'id':'b1-pillars','kind':'row','t0':48,'t1':61.5,'side':0,'spacing':9,'bothSides':False,'item':{'kind':'pillar','size':[1.2,10,1.2],'color':P['denim'],'y':-10.5}},
]+[stand(i,66.0+3.0*i) for i in range(3)]+[pitch,
 {'id':'window-strip','kind':'row','t0':83.6,'t1':101.3,'side':4.2,'spacing':3.2,'bothSides':True,'item':{'kind':'box','size':[0.4,5,2.6],'color':'#DCE7F4','react':'tap'}},
 five_windows]+terraces+[bunny]+ears+[cover_square,
 {'id':'clouds','kind':'row','t0':100,'t1':175,'side':30,'spacing':40,'bothSides':True,'item':{'kind':'cloud','size':[8,3,5],'color':'#FFFFFF','y':10}}]
BEAT=0.5714
events=[
 {'t':9.607,'type':'raise','target':'roofs-a','dur':0.6},
 {'t':10.178,'type':'burst','at':'player','particles':'confetti'},
 {'t':62.18,'type':'color','palette':{'ground':'#BFE0D0'},'dur':1.0},
 {'t':62.18,'type':'pulse','target':'stadium-pitch','every':BEAT*2,'until':83.0},
 {'t':104.18,'type':'light','target':'egg-five-windows','every':BEAT,'until':107.0,'note':'five windows light one per beat on the sustained vocal, then all go dark together'},
 {'t':107.04,'type':'flash','target':'egg-five-windows'},
 {'t':117.03,'type':'burst','at':'player','particles':'confetti'},
 {'t':137.6,'type':'raise','target':'cover-bunny-relief','dur':2.0},
 {'t':137.6,'type':'pulse','target':'cover-bunny-relief','every':BEAT,'until':156.0},
 {'t':156.1,'type':'color','palette':{'skyTop':'#F2C9A8','skyBottom':'#FBEEDC'},'dur':4.0},
 {'t':156.1,'type':'particles','particles':'dust','until':175}]
diamond_windows=[(0,27.9,2),(27.9,46.75,1),(46.75,62.18,1),(62.18,83.32,1),(83.32,101.6,1),(101.6,117.03,1),(117.03,137.6,1),(137.6,156.1,1),(156.1,174,1)]
crown_near=[83.3,137.3]
finish={'kind':'pyramid','color':P['deep']}
chart_notes='Attention 105 BPM (beat 0.5714 s, downbeat grid 0.464 s). 277 taps (old 139, 2.0x). Taps on measured audio accents: vocal syllables (demucs stem, -25 ms corrected) in verses/pre, kick/snare/bass in hook & choruses; dotted vocal pickups (beat 2.5 / 4.5) are the motif. Min gap 0.267 s (8ths). Fastest run 12 consecutive 8ths in Chorus 2. Recommended judgment window +-90 ms (perfect +-35 ms).'
