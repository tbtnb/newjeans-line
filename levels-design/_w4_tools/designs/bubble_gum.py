import sys; sys.path.insert(0,'/workspace/w4/designs'); from common import *
TITLE='Bubble Gum'; BPM=105.0; START='N'
GRID={'bar0':2.055,'beat':0.57139,'note':'bar n starts at 2.055 + 2.28556*n; grid shifted -24 ms to measured clap/hat transients'}
JUDGMENT={'perfect':0.05,'good':0.09,'miss_beyond':0.12,'note':'relaxed tempo; min gap 0.285 s (8th at 105 BPM)'}
SPEED=[{'t':0,'v':8.5}]
CHART_NOTES='Chorus taps follow the "bubble bubble" vocal hook syllables (vocal stem weighted 1.6) over the kick/clap on 1 and 3; pickup 8th runs at the end of each pre-chorus; breakdown nearly empty (breathing). See chart-report.md.'
SEA='#5fc4d6'; SAND='#f4e6c6'; PINK='#ff9ec4'; MINT='#bfe8d2'; CORAL='#ff8a73'
# Route: seawall north -> boardwalk NE -> greenhouse SE -> beach chorus NE with rising steps -> breakdown floats UP on bubbles ->
# hill picnic NW -> greenhouse callback NE -> balloon field SE -> sunset beach NE (drop) -> picnic table.
ROT=[(36.34,'R'),(56.91,'L'),(91.19,'L'),(118.62,'R'),(136.9,'R'),(164.33,'L')]
ELEV=[{'t0':60.0,'t1':78.0,'type':'ramp','dy':2,'note':'chorus 1: steps of the beach stairs rise gently'},
      {'t':79.78,'type':'jump','dy':3,'note':'drums drop out -> the line is lifted onto road pieces floating on bubbles'},
      {'t':91.20,'type':'fall','dy':-5,'note':'drums return, the giant bubble pops -> drop to the grass'},
      {'t':163.78,'type':'fall','dy':-2,'note':'land on the sunset beach right before the final-chorus downbeat'}]
WIDTH=[{'t':0,'w':2.8},{'t':18.05,'w':2.4},{'t':56.91,'w':2.3},{'t':79.76,'w':2.6},{'t':91.19,'w':2.2},{'t':136.9,'w':2.1},{'t':164.33,'w':2.0}]
REVEAL=[{'t':0,'mode':'static','lead':3.0},{'t':18.05,'mode':'rise','lead':2.0},{'t':79.76,'mode':'drop','lead':2.0},{'t':91.19,'mode':'rise','lead':1.8},{'t':164.33,'mode':'rise','lead':1.6}]
PALETTE={'skyTop':'#8fd3ec','skyBottom':'#f4fbff','fog':'#e7f6fb','fogStart':45,'fogEnd':130,'ground':SEA,'groundY':-1.2,
         'road':'#fffaf0','roadSide':MINT,'line':PINK,'light':'#fff7e8','lightIntensity':1.15,'ambient':'#c4dce4','particles':'bubbles'}
SECTIONS_L=[
 {'t':0,'label':'Intro','camera':'side','note':'low seawall, big sky, three slow bubbles; guitar only'},
 {'t':18.05,'label':'Verse 1','palette':{'roadSide':'#d8b98a'},'camera':'iso','note':'wooden boardwalk over the shallows (planks dip on taps)'},
 {'t':36.34,'label':'Pre-chorus 1','palette':{'ground':'#a9dcb4','roadSide':'#ffffff'},'camera':'low','note':'glass greenhouse corridor, white frames give scale'},
 {'t':56.91,'label':'Chorus 1','palette':{'ground':SAND,'roadSide':CORAL},'camera':'high','note':'open beach, balloons rise, stair steps climb'},
 {'t':79.76,'label':'Breakdown','palette':{'groundY':-12,'skyTop':'#a7c9f2','particles':'bubbles'},'camera':'top','note':'drums out: lifted on bubbles above the sea; giant pink bubble ahead'},
 {'t':91.19,'label':'Verse 2','palette':{'groundY':-1.2,'ground':'#9fd49a','roadSide':MINT},'camera':'iso','note':'grass hill, picnic blankets'},
 {'t':118.62,'label':'Pre-chorus 2','palette':{'ground':'#a9dcb4','roadSide':'#ffffff'},'camera':'low','note':'greenhouse again (callback)'},
 {'t':136.9,'label':'Chorus 2','palette':{'ground':SAND,'roadSide':CORAL},'camera':'side','note':'balloon field'},
 {'t':164.33,'label':'Final chorus','palette':{'skyTop':'#f6a37c','skyBottom':'#ffe2b8','ground':'#f0c38e','roadSide':'#ff7a6b','fog':'#ffe2c4'},'camera':'iso','note':'sunset beach'},
 {'t':191.76,'label':'Outro','palette':{'skyTop':'#7d6aa8','skyBottom':'#ffc9a0','particles':None},'camera':'wide','note':'picnic table, two chairs, one lamp; last bubble leaves'}]
CAMERA=[{'t':0,'preset':'side','blend':0},{'t':18.05,'preset':'iso','blend':2.5},{'t':36.34,'preset':'low','blend':2.0},{'t':54.6,'preset':'wide','blend':1.5},
 {'t':56.91,'preset':'high','blend':1.0},{'t':68.3,'preset':'iso','yaw':30,'blend':2.0},{'t':79.76,'preset':'top','blend':2.5},{'t':89.2,'preset':'iso','blend':1.6},
 {'t':104.9,'preset':'iso','yaw':-30,'blend':2.0},{'t':118.62,'preset':'low','blend':2.0},{'t':136.9,'preset':'side','blend':1.5},{'t':150.6,'preset':'iso','blend':2.0},
 {'t':164.33,'preset':'iso','dist':17,'blend':0.8},{'t':178.0,'preset':'high','blend':2.0},{'t':191.76,'preset':'wide','blend':3.0}]
OBJECTS=[
 {'id':'seawall','kind':'row','t0':0.5,'t1':17.8,'side':-3.2,'spacing':2.0,'bothSides':False,'item':{'kind':'box','size':[1.2,1.6,2.0],'color':'#e3ddd0'},'name':'seawall blocks on the sea side'},
 {'id':'planks','kind':'row','t0':18.2,'t1':36.0,'side':1.9,'spacing':1.1,'bothSides':True,'item':{'kind':'box','size':[0.9,0.15,1.0],'color':'#c99e6e','react':'tap'},'name':'boardwalk planks (dip on actual taps)'},
 {'id':'gh_arches','kind':'row','t0':36.5,'t1':56.5,'side':0,'spacing':4.0,'bothSides':False,'item':{'kind':'arch','size':[7,6,0.4],'color':'#ffffff'},'name':'greenhouse frames arching over the road (7 wide, 6 high, clear of the road)'},
 {'id':'gh_arches2','kind':'row','t0':118.8,'t1':136.5,'side':0,'spacing':4.0,'bothSides':False,'item':{'kind':'arch','size':[7,6,0.4],'color':'#ffffff'}},
 {'id':'giant_bubble','t':86.0,'off':(0,22),'y':6,'kind':'sphere','size':[12,12,12],'color':'#ffb8d6','landmark':True,'clear':7,'react':'beat',
  'name':'giant bubble-gum bubble hanging ahead during the breakdown; pops at 91.19 when the drums return','appear':{'t':80.0,'mode':'grow','dur':3.0},'exit':{'t':91.19,'mode':'shrink','dur':0.15}},
 {'id':'lighthouse','t':10.0,'off':(-18,25),'kind':'group','landmark':True,'clear':4,'name':'striped lighthouse on the breakwater (visible again at the end)',
  'parts':[{'kind':'cylinder','pos':[0,4,0],'size':[2.6,8,2.6],'color':'#ffffff'},{'kind':'cylinder','pos':[0,5,0],'size':[2.7,1.4,2.7],'color':CORAL},{'kind':'cylinder','pos':[0,8.6,0],'size':[1.8,1.2,1.8],'color':'#ffe08a'},{'kind':'cone','pos':[0,9.8,0],'size':[2.4,1.2,2.4],'color':CORAL}]},
 {'id':'marbles_egg','t':100.0,'off':(5,0),'kind':'group','egg':True,'clear':1.5,'name':'EGG: five glass marbles in the grass; one reflects a tiny bunny-ear cloud',
  'parts':[{'kind':'sphere','pos':[-1.2+0.6*i,0.25,0],'size':[0.45,0.45,0.45],'color':c} for i,c in enumerate(['#ff9ec4','#8fd3ec','#ffe08a','#bfe8d2','#c9b6f2'])]+[
           {'kind':'sphere','pos':[1.2,0.55,0],'size':[0.12,0.2,0.05],'color':'#ffffff'}]},
 {'id':'paper_boat','t':45.0,'off':(4.5,0),'y':1.0,'kind':'group','egg':True,'clear':1.0,'name':'EGG: paper boat on a greenhouse sill; the same boat floats on the water in the outro',
  'parts':[{'kind':'box','pos':[0,0,0],'size':[1.2,0.3,0.5],'color':'#ffffff'},{'kind':'pyramid','pos':[0,0.4,0],'size':[0.6,0.6,0.4],'color':'#ffffff'}]},
 {'id':'paper_boat2','t':196.0,'off':(-8,6),'y':-1.0,'kind':'group','clear':1.0,'parts':[{'kind':'box','pos':[0,0,0],'size':[1.2,0.3,0.5],'color':'#ffffff'},{'kind':'pyramid','pos':[0,0.4,0],'size':[0.6,0.6,0.4],'color':'#ffffff'}]},
 {'id':'picnic','t':198.0,'off':(5,8),'kind':'group','landmark':True,'clear':3,'name':'finish: picnic table, two empty chairs and a lamp that switches on',
  'parts':[{'kind':'box','pos':[0,1,0],'size':[3,0.2,1.6],'color':'#ffffff'},{'kind':'box','pos':[-1.2,0.5,0],'size':[0.2,1,1.4],'color':'#ffffff'},{'kind':'box','pos':[1.2,0.5,0],'size':[0.2,1,1.4],'color':'#ffffff'},
           {'kind':'box','pos':[-2.4,0.5,0],'size':[0.9,1,0.9],'color':PINK},{'kind':'box','pos':[2.4,0.5,0],'size':[0.9,1,0.9],'color':SEA},
           {'kind':'cylinder','pos':[3.6,1.5,0],'size':[0.12,3,0.12],'color':'#555555'},{'kind':'sphere','pos':[3.6,3.1,0],'size':[0.6,0.6,0.6],'color':'#ffe9a8','id':'lamp_bulb'}]},
]+[
 {'id':f'balloon{i}','t':t,'off':(s,2),'kind':'group','parts':balloon([PINK,SEA,'#ffe08a',MINT,CORAL,'#c9b6f2'][i%6],6+(i%3)),'clear':1.2,'react':'beat',
  'appear':{'t':t-2.2,'mode':'rise','dur':1.2}} for i,(t,s) in enumerate([(59,-6),(62,6),(65,-6),(68,6),(71,-6),(74,6),(77,-6),(139,-6),(142,6),(145,-6),(148,6),(151,-6),(154,6),(157,-6),(160,6)])
]+[
 {'id':f'step{i}','t':t,'off':(s,0),'kind':'box','size':[2.5,1+i*0.5,2.5],'color':[MINT,'#ffe08a',PINK][i%3],'clear':1.6,'appear':{'t':t-1.6,'mode':'rise','dur':0.5},'react':'kick',
  'name':'beach stair blocks rising beside the road (decor; road ramps gently)'} for i,(t,s) in enumerate([(60.5,5),(63,-5),(65.5,5),(68,-5),(70.5,5),(73,-5),(75.5,5)])
]+[
 {'id':f'tree{i}','t':t,'off':(s,0),'kind':'group','parts':palm_free_tree(['#7cc47f','#9fd49a','#6db873'][i%3]),'clear':1.6} for i,(t,s) in enumerate([(93,6),(96,-6),(99,-7),(103,6),(107,-6),(111,6),(115,-6)])
]+[
 {'id':f'blanket{i}','t':t,'off':(s,0),'kind':'box','size':[3,0.05,2.4],'color':c,'clear':1.8} for i,(t,s,c) in enumerate([(97,7,PINK),(105,-7,SEA),(113,7,'#ffe08a')])
]+[
 {'id':f'sun_bubble{i}','t':t,'off':(s,4),'y':3+i%3,'kind':'bubble','size':[1.4,1.4,1.4],'color':'#ffd6e8','clear':1.0,'appear':{'t':t-2,'mode':'grow','dur':1.0},'exit':{'t':t+3,'mode':'fade','dur':1.0}}
 for i,(t,s) in enumerate([(4,-7),(9,-8),(14,-7),(166,-7),(172,7),(178,-7),(184,7),(190,-7),(195,-6)])
]
EVENTS=[
 {'t':0.5,'type':'particles','particles':'bubbles','until':18.0,'note':'only three slow bubbles, off road'},
 {'t':56.91,'type':'burst','at':'player','particles':'confetti'},
 {'t':79.76,'type':'color','palette':{'skyTop':'#a7c9f2'},'dur':2.0},
 {'t':91.19,'type':'burst','at':'giant_bubble','particles':'confetti','note':'bubble pops on the drum re-entry'},
 {'t':136.9,'type':'flash','dur':0.2},
 {'t':164.33,'type':'color','palette':{'skyTop':'#f6a37c','skyBottom':'#ffe2b8'},'dur':4.0},
 {'t':191.76,'type':'light','target':'picnic','note':'lamp bulb switches on'},
 {'t':193.0,'type':'raise','target':'sun_bubble8','dy':8,'dur':5.0,'note':'last bubble drifts away'}]
FINISH={'kind':'gate','note':'two-post picnic arch with string lights'}
DIAMOND_TARGETS=[12,30,46,66,85,100,125,150,175,188]; CROWN_TARGETS=[85.0,132.0]
MARGIN=1.5
