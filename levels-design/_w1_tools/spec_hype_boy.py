from speclib import *
title='Hype Boy'; start='N'
P=dict(cobalt='#2447C6',indigo='#182857',ivory='#F4F1E8',aqua='#57CDD1',sky='#B8DCF0',lilac='#DCDDF5',pink='#FF7185',gold='#F8CB56')
palette=dict(skyTop='#9CCDEB',skyBottom='#EEF7FB',fog='#DDEEF7',fogStart=40,fogEnd=120,ground=P['sky'],groundY=-12,
  road=P['ivory'],roadSide=P['cobalt'],line=P['pink'],light='#FFF6E6',lightIntensity=1.15,ambient='#BBD3EA',particles=None)
width=[{'t':0,'w':2.2},{'t':53.05,'w':2.1},{'t':129.85,'w':2.0},{'t':149.05,'w':1.9},{'t':170.65,'w':2.2}]
reveal=[{'t':0,'mode':'rise','lead':1.8},{'t':19.45,'mode':'rise','lead':1.6},{'t':53.05,'mode':'unfold','lead':1.5},
        {'t':91.45,'mode':'rise','lead':1.5},{'t':125.05,'mode':'unfold','lead':1.6},{'t':149.05,'mode':'drop','lead':1.3},{'t':170.65,'mode':'fade','lead':2.0}]
sections=[
 {'t':0,'label':'Intro riff','note':'01 L0 sparse start deck; taps sit on the synth-riff beats (about one per beat), long breathing straights. P1: four roof slabs rise on the four-count.'},
 {'t':19.452,'label':'Verse 1','note':'02 locker canyon, L0, closed: staggered lockers on both sides; the moombah/dembow kick-snare (3+3+2) drives syncopated 16th-offset turns.','palette':{'fogEnd':90}},
 {'t':38.652,'label':'Pre-chorus 1','note':'03 R1 ramp L0->L1 (+3), walls fold outward (P2); sparse call-and-response vocal taps.','palette':{'fogEnd':130}},
 {'t':48.252,'label':'Build 1','note':'03 end: kick build, pool fully revealed before the chorus.'},
 {'t':53.052,'label':'Chorus 1','note':'04 pool, L1, open U around the pool (SW dip / SE run / NE climb). P3 back panels unfold, five colour dance pillars answer the vocal.','palette':{'skyTop':'#86C3EA','ground':'#BFE6EE'}},
 {'t':72.252,'label':'Post-chorus 1','note':'04 exit CP1, B1 flat bridge heading SE towards the sports court.'},
 {'t':91.452,'label':'Verse 2','note':'05 sports court U (NE up, SE across, SW down) around the court with red-white goal; P4 goal and low walls rise.','palette':{'fogEnd':110}},
 {'t':115.452,'label':'Pre-chorus 2','note':'06 phone patio: closed single corridor of phone-shaped screens; E1 flip phone silently flips open on the outer shelf.','palette':{'fogEnd':85,'skyTop':'#A9CBE8'}},
 {'t':125.052,'label':'Build 2','note':'07 bridge B2/R2: deck unfolds early (P6), ramp L1->L2 (+3).'},
 {'t':129.852,'label':'Chorus 2','note':'07 long SW bridge run up to L2, CP2 at the end; road narrows to 2.0.','palette':{'skyTop':'#B9B8EE','ground':P['lilac']}},
 {'t':149.052,'label':'Final chorus','note':'08 L2 sky dance: NW run with two syncopated SW offsets (asymmetric horseshoe steps); panels open in canon (P7), pillars return. Road 1.9.','palette':{'skyTop':'#C8C3F0','skyBottom':'#F5F2FB'}},
 {'t':170.652,'label':'Outro','note':'09 calm straight to the finish deck, little white bunny echo; P8 cover freeze.','palette':{'skyTop':'#AFC9EE'}},
]
camera=[{'t':0,'preset':'iso','dist':16,'blend':0},{'t':19.452,'preset':'close','dist':14,'blend':1.5},
 {'t':38.652,'preset':'iso','dist':18,'pitch':45,'blend':3.0},{'t':53.052,'preset':'wide','dist':22,'blend':1.0},
 {'t':62.652,'preset':'iso','dist':19,'blend':2.0},{'t':72.252,'preset':'iso','dist':17,'blend':2.0},
 {'t':91.452,'preset':'iso','dist':18,'blend':2.0},{'t':115.452,'preset':'close','dist':14,'blend':2.0},
 {'t':125.052,'preset':'low','dist':16,'blend':2.0},{'t':129.852,'preset':'wide','dist':22,'blend':1.2},
 {'t':149.052,'preset':'high','dist':21,'blend':1.5},{'t':158.652,'preset':'iso','dist':19,'blend':2.0},
 {'t':170.652,'preset':'wide','dist':26,'blend':4.0}]
pool={'id':'pool','t':62.0,'side':-14,'kind':'group','radius':12,'landmark':True,'name':'Summer pool + low diving board',
  'parts':[part('box',[0,-0.6,0],[20,1.2,13],'#F4F1E8'),part('water',[0,-0.1,0],[17,0.2,10],P['aqua']),
           part('box',[8,0.6,0],[3,0.3,1.2],'#F4F1E8'),part('box',[0,-4,0],[20,6,13],P['cobalt'])],'appear':appear(51.5,'unfold',1.5)}
pillar_cols=['#FF7185','#F8CB56','#57CDD1','#8FA2F0','#F4F1E8']
pillars=[{'id':f'dance-pillar-{i}','t':58.0+1.2*i,'side':9,'kind':'box','size':[1.6,3.5,1.6],'color':c,'react':'beat','name':'five-colour dance pillar',
          'appear':appear(53.052+0.6*i,'pop',0.3)} for i,c in enumerate(pillar_cols)]
bunny=bunny_relief('cover-bunny-tower',60.0,-28,P['cobalt'],P['ivory'],scale=1.0,landmark=True,name='2022 EP cover bunny relief tower',appear=appear(48.252,'rise',2.0))
court={'id':'sports-court','t':101.0,'side':14,'kind':'group','radius':11,'landmark':True,'name':'MV sports court, red-white goal, yellow basketball',
  'parts':[part('box',[0,-0.5,0],[18,1,12],'#6F8FE0'),part('box',[4.5,-0.45,0],[9,1,12],'#F2A6A6'),part('box',[0,0.05,0],[0.2,0.05,12],'#FFFFFF'),
           part('box',[8.5,1.2,0],[0.3,2.4,4],'#E04848'),part('box',[8.5,2.4,0],[0.3,0.3,4],'#FFFFFF'),part('sphere',[-3,0.6,2],[1.0,1.0,1.0],P['gold']),
           part('box',[0,-4,0],[18,6,12],P['cobalt'])],'appear':appear(91.452,'rise',1.2)}
phone={'id':'egg-flip-phone','t':120.0,'side':-7,'kind':'group','radius':3,'egg':True,'name':'E1 secret flip phone (five colour screen dots, then a white bunny)',
  'parts':[part('box',[0,0.3,0],[2.2,0.6,1.4],'#D9DDF0'),part('box',[0,1.3,-0.6],[2.2,2.0,0.2],'#D9DDF0',[ -20,0,0])]+
          [part('box',[-0.8+0.4*i,1.5,-0.72],[0.25,0.25,0.05],c) for i,c in enumerate(pillar_cols)]}
panels=[{'id':f'sky-panel-{i}','t':151.0+3.6*i,'side':(-1)**i*8,'kind':'box','size':[6,4,0.4],'color':P['lilac'],'color2':P['cobalt'],
         'appear':appear(149.052+1.2*i,'unfold',0.8),'react':'beat'} for i,_ in enumerate(range(5))]
objects=[
 {'id':'roof-slabs','kind':'row','t0':0.5,'t1':18.5,'side':6,'spacing':8,'bothSides':True,'item':{'kind':'box','size':[5,1.2,5],'color':'#DCE9F5'}},
 {'id':'lockers','kind':'row','t0':19.6,'t1':38.4,'side':3.8,'spacing':2.4,'bothSides':True,'item':{'kind':'box','size':[1.6,4.5,1.2],'color':P['aqua'],'color2':P['cobalt'],'react':'tap'}},
 {'id':'basketball-1','t':30.0,'side':5,'kind':'sphere','size':[1,1,1],'color':P['gold'],'name':'yellow basketball (MV still)'},
 {'id':'fold-walls','kind':'row','t0':39,'t1':52.5,'side':4.5,'spacing':5,'bothSides':True,'item':{'kind':'box','size':[0.4,3,4],'color':'#E8EEF8'},
  'exit':exitm(50.0,'fall',1.0)},
 pool,bunny]+pillars+[
 {'id':'b1-bridge-piers','kind':'row','t0':73,'t1':90,'side':0,'spacing':8,'bothSides':False,'item':{'kind':'pillar','size':[1.2,10,1.2],'color':P['cobalt'],'y':-10.5}},
 court,
 {'id':'phone-screens','kind':'row','t0':115.6,'t1':124.8,'side':3.8,'spacing':3,'bothSides':True,'item':{'kind':'box','size':[0.4,3.6,2.2],'color':'#2E3F7A','react':'tap'}},
 phone,
 {'id':'b2-deck-piers','kind':'row','t0':125.2,'t1':148.5,'side':0,'spacing':9,'bothSides':False,'item':{'kind':'pillar','size':[1.2,14,1.2],'color':P['indigo'],'y':-14.5}},
 ]+panels+[
 {'id':'finale-pillars','kind':'row','t0':160,'t1':170,'side':7,'spacing':3,'bothSides':False,'item':{'kind':'box','size':[1.4,3,1.4],'color':P['pink'],'react':'beat'}},
 {'id':'outro-bunny','t':172.0,'side':6,'kind':'group','radius':2,'landmark':True,'name':'little white bunny echo',
  'parts':[part('sphere',[0,0.8,0],[1.6,1.6,1.6],'#FFFFFF'),part('box',[-0.3,2.0,0],[0.3,1.2,0.3],'#FFFFFF'),part('box',[0.3,2.0,0],[0.3,1.2,0.3],'#FFFFFF')]},
 {'id':'clouds','kind':'row','t0':0,'t1':175,'side':32,'spacing':45,'bothSides':True,'item':{'kind':'cloud','size':[9,3,6],'color':'#FFFFFF','y':8}}]
BEAT=0.6
events=[
 {'t':0.252,'type':'raise','target':'roof-slabs','every':BEAT,'until':2.7,'note':'P1 four slabs on the four-count'},
 {'t':19.452,'type':'raise','target':'lockers','dur':0.6},
 {'t':38.652,'type':'lower','target':'fold-walls','dur':4.0,'note':'P2 walls fold out'},
 {'t':53.052,'type':'burst','at':'player','particles':'bubbles'},
 {'t':53.052,'type':'pulse','target':'dance-pillar-0','every':BEAT*2,'until':72.0},
 {'t':91.452,'type':'raise','target':'sports-court','dur':1.0},
 {'t':120.25,'type':'light','target':'egg-flip-phone','every':0.3,'until':121.8,'note':'five colour dots light one by one'},
 {'t':125.052,'type':'raise','target':'b2-deck-piers','dur':3.0},
 {'t':129.852,'type':'color','palette':{'skyTop':'#B9B8EE','ground':P['lilac']},'dur':1.5},
 {'t':129.852,'type':'burst','at':'player','particles':'confetti'},
 {'t':149.052,'type':'burst','at':'player','particles':'stars'},
 {'t':149.052,'type':'particles','particles':'bubbles','until':170.6},
 {'t':170.652,'type':'color','palette':{'skyTop':'#AFC9EE'},'dur':3.0}]
diamond_windows=[(0,19.45,1),(19.45,38.65,1),(38.65,53.05,1),(53.05,72.25,1),(72.25,91.45,1),(91.45,115.45,2),(115.45,129.85,1),(129.85,149.05,1),(149.05,173,1)]
crown_near=[72.3,148.9]
finish={'kind':'pyramid','color':P['cobalt']}
chart_notes='Hype Boy 100 BPM (beat 0.600 s, downbeat 0.252 s). 295 taps (old 140, 2.11x). 16th grid used for syncopation (moombah/dembow kick 1, a-of-2, 3, a-of-4; snare 3+3+2) but never two adjacent 16ths: min gap 0.267 s. Intro on riff beats, pre-choruses are vocal call-and-response, choruses mix kick/snare with vocal hook syllables. Recommended judgment window +-90 ms.'
