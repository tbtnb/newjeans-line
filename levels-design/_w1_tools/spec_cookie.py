from speclib import *
title='Cookie'; start='N'
P=dict(cobalt='#244BD8',denim='#496EC4',peri='#8098DC',ivory='#F2EEE5',bench='#20222C',violet='#8376CF',apricot='#FFAE70',gem='#BDEEFF',crown='#E8C76A')
palette=dict(skyTop='#7F95DA',skyBottom='#C9D3F2',fog='#AFBDE8',fogStart=35,fogEnd=110,ground=P['peri'],groundY=-12,
  road=P['ivory'],roadSide=P['denim'],line=P['apricot'],light='#F4F0FF',lightIntensity=1.05,ambient='#9FAFE0',particles=None)
width=[{'t':0,'w':2.4},{'t':12.33,'w':2.2},{'t':134.63,'w':2.0},{'t':159.09,'w':2.2},{'t':208.01,'w':2.4}]
reveal=[{'t':0,'mode':'rise','lead':1.8},{'t':49.02,'mode':'unfold','lead':1.5},{'t':110.17,'mode':'unfold','lead':1.4},
        {'t':134.63,'mode':'rise','lead':1.25},{'t':159.09,'mode':'drop','lead':1.4},{'t':183.55,'mode':'unfold','lead':1.5},{'t':208.01,'mode':'fade','lead':2.0}]
sections=[
 {'t':0,'label':'Intro','note':'01 L0 closed studio entrance: narrow black flats; sparse taps on kick/bass hits, two offset bends.'},
 {'t':12.33,'label':'Verse 1','note':'02 L0 narrow asymmetric S along the five-seat black bench; long-short-short phrasing on the half-time groove.','palette':{'fogEnd':90}},
 {'t':36.79,'label':'Pre-chorus 1','note':'03 three offset steps + continuous ramp L0->L1 (+3); E2 five-step folding stair unfolds on the rising phrase.','palette':{'fogEnd':120}},
 {'t':49.02,'label':'Chorus 1','note':'04 L1 open stage: square horseshoe (NE, SE, SW) around the 12-sided CD set piece; E3 side wings open, background grey-blue -> cobalt. CP1 at exit.','palette':{'skyTop':'#5B78DE','skyBottom':'#C4CEF4'}},
 {'t':73.48,'label':'Verse 2','note':'05 reprise: compressed offset corridor SE, bench motif repeats one tier higher.','palette':{'fogEnd':95}},
 {'t':97.94,'label':'Pre-chorus 2','note':'05 offset steps up L1->L2 (+3) heading NE.'},
 {'t':110.17,'label':'Chorus 2','note':'05 chorus 2 on L2 rectangular terrace heading SE; camera further out than chorus 1.','palette':{'skyTop':'#4E6CD8'}},
 {'t':134.63,'label':'Jersey-club bridge','note':'06 density peak: L2->L1 descending compressed 2+1+2 short zigzags (road 2.0); E5 paired risers alternate with the Jersey-club kicks; ends on CP2 release straight and B2 ramp back up to L2.','palette':{'skyTop':P['violet'],'skyBottom':'#D3CCF3','fogEnd':85}},
 {'t':159.09,'label':'Final chorus','note':'07 L2 wide L stage heading NW, bunny relief wall assembles block by block (E6); EE five-seat bunny shadow on the safe straight.','palette':{'skyTop':'#3E5FD6','skyBottom':'#D8DEF7'}},
 {'t':183.55,'label':'Dance break','note':'07/08 instrumental break: square meander (LLRR) through rows of studio flats like a choreography grid; fewer, heavier taps.','palette':{'skyTop':'#6F86D9'}},
 {'t':208.01,'label':'Outro','note':'08 continuous descending ramp L2->L0 (-6), long straights, last bend; E7 flats fold down, finish in the quiet studio.','palette':{'skyTop':'#93A6E0','fogEnd':140}},
]
camera=[{'t':0,'preset':'iso','dist':15,'blend':0},{'t':12.33,'preset':'close','dist':14,'blend':2.0},
 {'t':36.79,'preset':'iso','dist':18,'pitch':46,'blend':3.0},{'t':49.02,'preset':'wide','dist':22,'blend':1.0},
 {'t':61.25,'preset':'iso','dist':19,'blend':2.0},{'t':73.48,'preset':'iso','dist':16,'blend':2.0},
 {'t':97.94,'preset':'iso','dist':18,'blend':2.5},{'t':110.17,'preset':'wide','dist':24,'blend':1.0},
 {'t':134.63,'preset':'close','dist':14,'blend':1.0},{'t':152.97,'preset':'iso','dist':18,'blend':2.0},
 {'t':159.09,'preset':'wide','dist':23,'blend':1.2},{'t':183.55,'preset':'high','dist':20,'blend':2.0},
 {'t':208.01,'preset':'iso','dist':18,'blend':3.0},{'t':222.0,'preset':'wide','dist':27,'blend':5.0}]
bench={'id':'five-seat-bench','t':22.0,'side':6,'kind':'group','radius':6,'landmark':True,'name':'Five-seat black bench (MV)',
  'parts':[part('box',[0,0.6,0],[11,0.5,2],P['bench']),part('box',[0,1.6,0.9],[11,1.6,0.3],P['bench'])]+
         [part('box',[-4.4+2.2*i,0.9,0],[1.6,0.12,1.4],P['ivory']) for i in range(5)],'appear':appear(12.33,'rise',1.0)}
stairs={'id':'folding-stairs','t':42.0,'side':-7,'kind':'stairs','size':[6,5,8],'color':P['ivory'],'color2':P['denim'],'landmark':True,'name':'Five-step folding stair (E2)',
  'appear':appear(36.79,'unfold',2.4)}
cd={'id':'cd-set-piece','t':58.5,'side':16,'kind':'group','radius':10,'landmark':True,'name':'12-sided graffiti CD set piece',
  'parts':[part('cylinder',[0,3,0],[14,0.6,14],'#CFE6FA',[75,0,0]),part('cylinder',[0,3,-0.4],[3,0.7,3],P['cobalt'],[75,0,0]),
           part('box',[-3,4,-0.5],[2.5,0.3,0.2],'#FF8FB1',[0,0,30]),part('box',[2.5,1.8,-0.5],[2,0.3,0.2],P['apricot'],[0,0,-20]),
           part('box',[0,-3,0],[12,4,8],P['denim'])],'appear':appear(49.02,'rise',1.0)}
wings=[{'id':f'side-wing-{i}','t':52.0+12*i,'side':(-1)**i*7,'kind':'box','size':[0.5,6,7],'color':P['ivory'],'color2':P['violet'],'appear':appear(49.02+0.382*i,'unfold',0.8)} for i in range(2)]
risers=[{'id':f'riser-{i}','t':137.0+2.6*i,'side':(-1)**i*5,'kind':'box','size':[2.5,3,2.5],'color':P['ivory'],'color2':P['violet'],'react':'kick','name':'paired riser (E5)'} for i in range(8)]
bunny=bunny_relief('bunny-relief-wall',168.0,-24,P['cobalt'],P['ivory'],scale=1.25,landmark=True,name='2022 EP bunny relief wall (E6)',appear=appear(159.09,'rise',3.0))
egg={'id':'egg-bunny-shadow','t':176.0,'side':7,'kind':'group','radius':6,'egg':True,'name':'EE five seats cast a bunny shadow + cookie-shaped CD stamper',
  'parts':[part('box',[-3+1.5*i,1.0,0],[1.0,2.0,1.0],P['bench']) for i in range(5)]+
         [part('plane',[0,0.02,-3],[8,1,5],'#1B2A6B'),part('cylinder',[4.5,0.5,1.5],[1.6,0.4,1.6],'#D9A066')]}
objects=[
 {'id':'black-flats','kind':'row','t0':0.3,'t1':12.0,'side':4,'spacing':5,'bothSides':True,'item':{'kind':'box','size':[0.6,5,3],'color':P['bench']}},
 bench,
 {'id':'seat-inlays','kind':'row','t0':24,'t1':36.5,'side':4.5,'spacing':4,'bothSides':True,'item':{'kind':'box','size':[1.4,0.6,1.4],'color':P['ivory'],'react':'tap'}},
 stairs,cd]+wings+[
 {'id':'reprise-benches','kind':'row','t0':74,'t1':97.5,'side':5,'spacing':6,'bothSides':True,'item':{'kind':'bench','size':[3,1,1],'color':P['bench'],'react':'tap'}},
 {'id':'terrace-flats','kind':'row','t0':110.5,'t1':134,'side':6,'spacing':6,'bothSides':True,'item':{'kind':'box','size':[0.5,4,4],'color':P['denim']}},
 ]+risers+[bunny,egg,
 {'id':'break-flats','kind':'row','t0':184,'t1':207.5,'side':4,'spacing':3.5,'bothSides':True,'item':{'kind':'box','size':[0.5,3.5,2.5],'color':P['violet'],'react':'kick'}},
 {'id':'outro-flats','kind':'row','t0':208.5,'t1':229,'side':5,'spacing':6,'bothSides':True,'item':{'kind':'box','size':[0.5,4,3.5],'color':P['denim']},'exit':exitm(222.0,'fall',1.5)},
 {'id':'studio-lamps','kind':'row','t0':0,'t1':231,'side':26,'spacing':35,'bothSides':True,'item':{'kind':'lamp','size':[1,9,1],'color':'#F4F0FF','y':0}}]
BEAT=0.38217
events=[
 {'t':12.33,'type':'raise','target':'black-flats','dur':0.8,'note':'E1 flats rise as the bass enters'},
 {'t':49.02,'type':'color','palette':{'skyTop':'#5B78DE'},'dur':1.0},
 {'t':49.02,'type':'spin','target':'cd-set-piece','every':BEAT*4,'until':73.4},
 {'t':49.02,'type':'burst','at':'player','particles':'confetti'},
 {'t':110.17,'type':'burst','at':'player','particles':'confetti'},
 {'t':134.63,'type':'color','palette':{'skyTop':P['violet']},'dur':0.8},
 {'t':134.63,'type':'pulse','target':'riser-0','every':BEAT,'until':158.9},
 {'t':159.09,'type':'raise','target':'bunny-relief-wall','dur':3.0},
 {'t':159.09,'type':'burst','at':'player','particles':'stars'},
 {'t':183.55,'type':'particles','particles':'dust','until':208},
 {'t':222.0,'type':'lower','target':'outro-flats','dur':3.0}]
diamond_windows=[(0,12.33,1),(12.33,36.79,1),(36.79,49.02,1),(49.02,73.48,2),(73.48,134.63,2),(134.63,159.09,1),(159.09,183.55,1),(183.55,231,1)]
crown_near=[73.4,158.6]
finish={'kind':'pyramid','color':P['cobalt']}
chart_notes='Cookie 157 BPM grid (half-time feel 78.5; beat 0.382 s, downbeat 0.104 s). 478 taps (old 357, 1.34x as schema asks ~1.2-1.4x). Taps on 8th grid (0.191 s) only where kick/snare/vocal really double; runs capped at 6 (chorus) / 10 (Jersey-club bridge, which follows the 3-3-2 club kick-snare syncopation) taps. Min gap 0.173 s. Recommended judgment window +-80 ms.'
