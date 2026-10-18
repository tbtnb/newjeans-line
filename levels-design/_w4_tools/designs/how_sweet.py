import sys; sys.path.insert(0,'/workspace/w4/designs'); from common import *
TITLE='How Sweet'; BPM=125.0; START='N'
GRID={'bar0':0.339,'beat':0.47999,'note':'bar n starts at 0.339 + 1.91996*n; grid fitted to beat tracker then shifted -23 ms to the measured transient (max-slope) of claps/hats'}
JUDGMENT={'perfect':0.045,'good':0.085,'miss_beyond':0.11,'note':'min gap 0.239 s (8th at 125 BPM); good window +/-85 ms keeps neighbouring taps unambiguous'}
SPEED=[{'t':0,'v':9.0}]
CHART_NOTES='Miami-bass tresillo (16th slots 0/6/12) is the backbone in verses and choruses; phrase-end 8th runs (4-6 taps) every 4 bars in choruses; final bar of last chorus = 8-tap run. See chart-report.md.'
CC='#e8735a'; CREAM='#f6e7b8'; DENIM='#4c6a96'; GREEN='#4f9a62'; BLACK='#141414'
# Route: start INSIDE the black album frame -> shop street NE -> rooftop (ramp) -> sports-court rooftops NW -> drop to street NE past the sticker
# -> blue-wall plaza SE -> laundry-flag lane NE -> build NW -> floating sky platforms NE -> long open straight to the record shop.
ROT=[(46.42,'L'),(77.14,'R'),(107.86,'R'),(138.58,'L'),(153.94,'L'),(169.30,'R')]
ELEV=[{'t0':38.9,'t1':45.9,'type':'ramp','dy':3,'note':'pre-chorus: street climbs a fire-escape ramp to the rooftops'},
      {'t':77.22,'type':'fall','dy':-3,'note':'chorus ends -> line hops off the roof back to street level (verse 2)'},
      {'t0':154.2,'t1':168.0,'type':'ramp','dy':6,'note':'build: long climb above the city'},
      {'t':169.38,'type':'fall','dy':-2,'note':'final-chorus downbeat drop onto the floating platforms'}]
WIDTH=[{'t':0,'w':2.6},{'t':8.02,'w':2.2},{'t':46.42,'w':2.4},{'t':77.14,'w':2.1},{'t':107.86,'w':2.2},{'t':138.58,'w':2.0},{'t':169.3,'w':1.8},{'t':200.0,'w':2.6}]
REVEAL=[{'t':0,'mode':'static','lead':3.0},{'t':8.02,'mode':'rise','lead':2.0},{'t':46.42,'mode':'unfold','lead':1.6},{'t':77.14,'mode':'rise','lead':1.8},
        {'t':138.58,'mode':'drop','lead':1.8},{'t':153.94,'mode':'rise','lead':1.4},{'t':169.3,'mode':'rise','lead':1.4},{'t':200.0,'mode':'static','lead':3.0}]
PALETTE={'skyTop':'#9fc6ea','skyBottom':'#fff4dc','fog':'#f6eedc','fogStart':40,'fogEnd':120,'ground':'#e9dcc2','groundY':-0.6,
         'road':'#fff7e6','roadSide':CC,'line':CC,'light':'#fff4e0','lightIntensity':1.15,'ambient':'#c9c2b4','particles':None}
SECTIONS_L=[
 {'t':0,'label':'Intro','palette':{'skyTop':'#20201f','skyBottom':'#3a3a38','ground':BLACK,'fogEnd':60},'camera':'close','note':'inside the black frame of the cover; coral letter blocks as walls'},
 {'t':8.02,'label':'Verse 1','palette':{'skyTop':'#b9d4ee','skyBottom':'#fff4dc','ground':'#e9dcc2'},'camera':'iso','note':'frame tips open -> narrow shop street, awnings unfold'},
 {'t':38.74,'label':'Pre-chorus 1','palette':{'roadSide':'#d9644c'},'camera':'low','note':'fire-escape ramp up'},
 {'t':46.42,'label':'Chorus 1','palette':{'ground':GREEN,'roadSide':DENIM,'skyTop':'#8cc0ec'},'camera':'high','note':'rooftop sports courts: green court, denim walls, barcode crossing'},
 {'t':77.14,'label':'Verse 2','palette':{'ground':'#e9dcc2','roadSide':CC},'camera':'iso','note':'back on the street, the giant How Sweet sticker'},
 {'t':107.86,'label':'Chorus 2','palette':{'ground':'#d7e3f2','roadSide':DENIM},'camera':'side','note':'denim-blue wall plaza, wide space'},
 {'t':138.58,'label':'Bridge','palette':{'skyTop':'#f2b38f','skyBottom':'#ffe7c4','roadSide':'#c75a46'},'camera':'low','note':'late afternoon, laundry flags overhead'},
 {'t':153.94,'label':'Build','palette':{'skyTop':'#9fc6ea'},'camera':'iso','note':'road rises late, climbing above roofs'},
 {'t':169.3,'label':'Final chorus','palette':{'groundY':-30,'ground':'#cfe3f5','roadSide':CC,'particles':'confetti'},'camera':'iso','note':'floating platforms in open sky'},
 {'t':200.0,'label':'Outro','palette':{'groundY':-0.6,'ground':'#e9dcc2','particles':None},'camera':'wide','note':'long calm straight to the record shop; sign flips CLOSED->OPEN'}]
CAMERA=[{'t':0,'preset':'close','blend':0},{'t':8.02,'preset':'iso','blend':2.5},{'t':38.74,'preset':'low','blend':1.8},
 {'t':46.42,'preset':'high','blend':1.2},{'t':61.78,'preset':'iso','yaw':-30,'blend':2.0},{'t':77.14,'preset':'iso','blend':1.0},
 {'t':92.5,'preset':'iso','yaw':35,'dist':20,'blend':2.5,'note':'frame the sticker'},{'t':107.86,'preset':'side','blend':1.5},
 {'t':123.2,'preset':'iso','yaw':-20,'blend':2.0},{'t':138.58,'preset':'low','blend':2.0},{'t':153.94,'preset':'iso','blend':2.0},
 {'t':169.3,'preset':'iso','dist':17,'shake':0.12,'blend':0.6},{'t':169.9,'preset':'iso','dist':17,'blend':0.5},{'t':184.66,'preset':'high','blend':2.0},
 {'t':200.0,'preset':'wide','blend':3.0}]
def letter_block(c=CC,h=4): return [{'kind':'box','pos':[0,h/2,0],'size':[2.2,h,1.0],'color':c}]
OBJECTS=[
 {'id':'cover_frame','t':1.0,'off':(0,6),'kind':'group','landmark':True,'clear':0,'onroad':True,'name':'Black album-cover frame the level starts inside (a hollow square border lying around the start)',
  'parts':[{'kind':'box','pos':[-9,0.3,6],'size':[1.2,0.6,26],'color':BLACK},{'kind':'box','pos':[9,0.3,6],'size':[1.2,0.6,26],'color':BLACK},
           {'kind':'box','pos':[0,0.3,-7],'size':[19,0.6,1.2],'color':BLACK}],
  'exit':{'t':8.02,'mode':'fall','dur':1.2}},
]+[
 {'id':f'nj_letter{i}','t':1.5+i*0.9,'off':(-7 if i%2==0 else 7,0),'kind':'group','parts':letter_block(CC,3+(i%3)),'clear':1.4,'react':'beat',
  'name':'coral NewJeans letter blocks (cover title)', 'appear':{'t':0.4+i*0.25,'mode':'rise','dur':0.5}} for i in range(8)
]+[
 {'id':f'shop{i}','t':t,'off':(s,0),'kind':'group','parts':shop(6,5+(i%3),4,['#f3e6cf','#e8d6f0','#d9ecd9','#f9d9c9'][i%4],[CC,DENIM,GREEN,'#f2c14e'][i%4]),'clear':3.5,
  'appear':{'t':t-2.0,'mode':'unfold','dur':0.6},'react':'beat'} for i,(t,s) in enumerate([(9.5,-7),(11.5,7),(13.5,-7),(15.5,7),(17.5,-7),(19.5,7),(21.5,-7),(23.5,7),(25.5,-7),(27.5,7),(29.5,-7),(31.5,7),(33.5,-7),(35.5,7)])
]+[
 {'id':'apple_egg','t':20.0,'off':(5.2,0),'kind':'group','egg':True,'clear':1.0,'name':'EGG: an apple with one small bite on a shop shelf',
  'parts':[{'kind':'box','pos':[0,0.6,0],'size':[1.6,1.2,0.8],'color':'#8a6a4a'},{'kind':'sphere','pos':[0,1.55,0],'size':[0.7,0.7,0.7],'color':'#d8312a'},
           {'kind':'sphere','pos':[0.28,1.65,-0.2],'size':[0.3,0.3,0.3],'color':'#fff7e6'},{'kind':'cylinder','pos':[0,2.0,0],'size':[0.06,0.25,0.06],'color':'#5a3b22'}]},
 {'id':'court','t':55.0,'off':(0,0),'onroad':True,'y':-0.55,'kind':'group','landmark':True,'clear':0,'name':'green rooftop sports court under the chorus route (big colour field, white lines)',
  'parts':[{'kind':'box','pos':[0,0,0],'size':[60,0.1,40],'color':GREEN},{'kind':'box','pos':[0,0.06,0],'size':[56,0.02,0.4],'color':'#ffffff'},
           {'kind':'torus','pos':[0,0.06,0],'size':[10,0.2,10],'color':'#ffffff'}],'appear':{'t':46.42,'mode':'unfold','dur':1.0}},
 {'id':'hoop1','t':52.0,'off':(-12,4),'kind':'group','clear':2,'parts':[{'kind':'cylinder','pos':[0,3,0],'size':[0.3,6,0.3],'color':'#e0e0e0'},{'kind':'box','pos':[0,6,0.5],'size':[3,2,0.2],'color':'#ffffff'},{'kind':'torus','pos':[0,5.2,1.2],'size':[1.2,0.1,1.2],'color':CC}]},
 {'id':'hoop2','t':70.0,'off':(12,4),'kind':'group','clear':2,'parts':[{'kind':'cylinder','pos':[0,3,0],'size':[0.3,6,0.3],'color':'#e0e0e0'},{'kind':'box','pos':[0,6,0.5],'size':[3,2,0.2],'color':'#ffffff'},{'kind':'torus','pos':[0,5.2,1.2],'size':[1.2,0.1,1.2],'color':CC}]},
 {'id':'barcode','kind':'row','t0':62.0,'t1':69.5,'side':2.4,'spacing':0.7,'bothSides':True,'item':{'kind':'box','size':[0.35,0.08,3.0],'color':BLACK,'react':'tap'},'name':'barcode crossing (cover barcode) - stripes dip on the player\'s actual taps'},
 {'id':'barcode_digits','t':69.8,'off':(5,2),'kind':'text','name':'5 220722 221029','size':[6,0,1.2],'color':BLACK,'egg':True,'clear':3},
 {'id':'denim_wall1','t':58.0,'off':(16,0),'kind':'box','size':[2,8,24],'color':DENIM,'clear':12},
 {'id':'denim_wall2','t':66.0,'off':(-16,0),'kind':'box','size':[2,8,24],'color':DENIM,'clear':12},
 {'id':'sticker','t':92.5,'off':(-14,14),'kind':'group','landmark':True,'clear':6,'react':'beat','name':'giant round "How Sweet" sticker from the cover, standing like a sun, slowly turning',
  'parts':[{'kind':'cylinder','pos':[0,7,0],'size':[11,0.6,11],'rot':[90,0,0],'color':CC},{'kind':'torus','pos':[0,7,-0.35],'size':[8,0.25,8],'rot':[90,0,0],'color':CREAM},
           {'kind':'cylinder','pos':[0,1,0],'size':[0.6,2,0.6],'color':'#999999'}]},
]+[
 {'id':f'vshop{i}','t':t,'off':(s,0),'kind':'group','parts':shop(6,6,4,['#f3e6cf','#d9ecd9','#f9d9c9'][i%3],[CC,GREEN,DENIM][i%3]),'clear':3.5,'appear':{'t':t-2,'mode':'rise','dur':0.6}}
 for i,(t,s) in enumerate([(80,7),(84,-7),(88,7),(97,7),(101,-7),(105,7)])
]+[
 {'id':f'bluewall{i}','t':t,'off':(s,0),'kind':'box','size':[2,10,14],'color':DENIM,'clear':8,'appear':{'t':t-2,'mode':'rise','dur':0.8}} for i,(t,s) in enumerate([(110,14),(116,-14),(122,14),(128,-14),(134,14)])
]+[
 {'id':'laundry','kind':'row','t0':139.0,'t1':153.5,'side':0,'spacing':3.0,'bothSides':False,'item':{'kind':'group','react':'beat','parts':[
   {'kind':'cylinder','pos':[0,6.5,0],'size':[0.05,0.05,9],'rot':[0,0,90],'color':'#ffffff'},
   {'kind':'box','pos':[-2,5.8,0],'size':[1.0,1.2,0.05],'color':CC},{'kind':'box','pos':[0,5.8,0],'size':[1.0,1.2,0.05],'color':CREAM},{'kind':'box','pos':[2,5.8,0],'size':[1.0,1.2,0.05],'color':GREEN}]},
  'name':'laundry-flag lines high overhead (y>=5.2, never on the road plane)'},
]+[
 {'id':f'cloud{i}','t':t,'off':(s,6),'y':-6,'kind':'cloud','size':[6,2.5,4],'color':'#ffffff','clear':4,'react':'none'} for i,(t,s) in enumerate([(171,-9),(176,9),(181,-10),(186,10),(191,-9),(196,9)])
]+[
 {'id':'record_shop','t':212.0,'off':(0,14),'onroad':False,'kind':'group','landmark':True,'clear':5,'name':'finish: the record shop; its flip sign turns from CLOSED to OPEN as the line arrives (EGG: new beginning)',
  'parts':shop(10,7,6,'#f3e6cf',CC,BLACK)+[{'kind':'box','pos':[0,3.2,-3.2],'size':[2.2,0.8,0.1],'color':'#ffffff','id':'open_sign'}]},
 {'id':'members5','t':205.0,'off':(-6,4),'kind':'group','egg':True,'clear':3,'name':'EGG: five small denim/green/black outfits on a clothes rail outside the shop (cover outfits)',
  'parts':[{'kind':'cylinder','pos':[0,2.2,0],'size':[0.06,0.06,5],'rot':[0,0,90],'color':'#888888'}]+[{'kind':'box','pos':[-2+i,1.5,0],'size':[0.7,1.2,0.15],'color':c} for i,c in enumerate([DENIM,BLACK,'#1d2a55',DENIM,GREEN])]},
]
EVENTS=[
 {'t':8.02,'type':'lower','target':'cover_frame','note':'frame edges fall away like the cover being lifted -> street appears'},
 {'t':46.42,'type':'color','palette':{'ground':GREEN},'dur':1.0},{'t':46.42,'type':'burst','at':'player','particles':'confetti'},
 {'t':77.14,'type':'spin','target':'sticker','until':107.86,'note':'one turn per 8 bars'},
 {'t':107.86,'type':'flash','dur':0.2},
 {'t':138.58,'type':'color','palette':{'skyTop':'#f2b38f','skyBottom':'#ffe7c4'},'dur':3.0},
 {'t':153.94,'type':'color','palette':{'skyTop':'#9fc6ea','skyBottom':'#fff4dc'},'dur':6.0},
 {'t':169.3,'type':'burst','at':'player','particles':'confetti'},{'t':169.3,'type':'shake','dur':0.35,'amount':0.15},
 {'t':200.0,'type':'particles','particles':None},
 {'t':212.5,'type':'spin','target':'open_sign','until':213.5,'note':'CLOSED -> OPEN flip'}]
FINISH={'kind':'gate','note':'record-shop door: the line enters the open door; OPEN sign flips'}
DIAMOND_TARGETS=[5,24,42,58,84,102,120,146,163,195]; CROWN_TARGETS=[104.5,146.0]
MARGIN=1.5
