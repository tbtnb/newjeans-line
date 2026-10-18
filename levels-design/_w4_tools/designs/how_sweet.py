import sys; sys.path.insert(0,'/workspace/w4/designs'); from common import *
TITLE='How Sweet'; BPM=125.0; START='N'
GRID={'bar0':0.339,'beat':0.47999,'note':'bar n starts at 0.339 + 1.91996*n; grid fitted to beat tracker then shifted -23 ms to the measured transient (max-slope) of claps/hats'}
JUDGMENT={'perfect':0.045,'good':0.085,'miss_beyond':0.11,'note':'min gap 0.239 s (8th at 125 BPM); good window +/-85 ms keeps neighbouring taps unambiguous'}
SPEED=[{'t':0,'v':9.0}]
CHART_NOTES='Miami-bass tresillo (16th slots 0/6/12) is the backbone in verses and choruses; phrase-end 8th runs (4-6 taps) every 4 bars in choruses; final bar of last chorus = 8-tap run. See chart-report.md.'
CC='#e8735a'; CREAM='#f6e7b8'; DENIM='#4c6a96'; GREEN='#4f9a62'; BLACK='#141414'
# Route: start INSIDE the black album frame -> shop street NE -> rooftop (ramp) -> sports-court rooftops NW -> drop to street NE past the sticker
# -> blue-wall plaza SE -> laundry-flag lane NE -> build NW -> floating sky platforms NE -> long open straight to the record shop.
WIDTH=[{'t':0,'w':2.6},{'t':8.02,'w':2.2},{'t':46.42,'w':2.4},{'t':77.14,'w':2.1},{'t':107.86,'w':2.2},{'t':138.58,'w':2.0},{'t':169.3,'w':1.9},{'t':200.0,'w':2.6}]
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
 {'id':'start_frame','t':1.0,'off':(0,5),'kind':'group','clear':0,'onroad':True,'y':-0.34,'name':'flat charcoal frame decal under the start (cover border motif; below road top, never blocks)',
  'parts':[{'kind':'box','pos':[-6,0,5],'size':[1.0,0.05,18],'color':'#292d32'},{'kind':'box','pos':[6,0,5],'size':[1.0,0.05,18],'color':'#292d32'},
           {'kind':'box','pos':[0,0,-4],'size':[13,0.05,1.0],'color':'#292d32'},{'kind':'box','pos':[0,0,14],'size':[13,0.05,1.0],'color':'#292d32'}],
  'exit':{'t':8.02,'mode':'sink','dur':1.2}},
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
 {'id':'sticker','t':92.5,'off':(-14,14),'kind':'image','src':'art/sticker.png','size':[14,0,7],'mode':'billboard','y':4,'landmark':True,'clear':7,'name':'giant cut-corner orange "How Sweet" sticker floating over the rooftops (cover sticker, generated art)'},
 {'id':'sticker_post','t':92.5,'off':(-14,14),'kind':'cylinder','size':[0.5,4,0.5],'color':'#999999','clear':7},
]+[
 {'id':f'vshop{i}','t':t,'off':(s,0),'kind':'group','parts':shop(6,6,4,['#f3e6cf','#d9ecd9','#f9d9c9'][i%3],[CC,GREEN,DENIM][i%3]),'clear':3.5,'appear':{'t':t-2,'mode':'rise','dur':0.6}}
 for i,(t,s) in enumerate([(80,7),(84,-7),(88,7),(97,7),(101,-7),(105,7)])
]+[
 {'id':f'bluewall{i}','t':t,'off':(s,0),'kind':'box','size':[2,10,14],'color':DENIM,'clear':8,'appear':{'t':t-2,'mode':'rise','dur':0.8}} for i,(t,s) in enumerate([(110,14),(116,-14),(122,14),(128,-14),(134,14)])
]+[
 {'id':'laundry','kind':'row','t0':139.0,'t1':153.5,'side':3.5,'spacing':3.0,'bothSides':True,'item':{'kind':'group','react':'beat','parts':[
   {'kind':'cylinder','pos':[0,3.2,0],'size':[0.15,6.4,0.15],'color':'#ffffff'},
   {'kind':'box','pos':[-2,5.8,0],'size':[1.0,1.2,0.05],'color':CC},{'kind':'box','pos':[0,5.8,0],'size':[1.0,1.2,0.05],'color':CREAM},{'kind':'box','pos':[2,5.8,0],'size':[1.0,1.2,0.05],'color':GREEN}]},
  'name':'laundry poles with flags on both sides of the narrow bridge (posts 3.5 off the centre line)'},
]+[
 {'id':f'cloud{i}','t':t,'off':(s,6),'y':-6,'kind':'cloud','size':[6,2.5,4],'color':'#ffffff','clear':4,'react':'none'} for i,(t,s) in enumerate([(171,-9),(176,9),(181,-10),(186,10),(191,-9),(196,9)])
]+[
 {'id':'record_shop','t':212.0,'off':(0,14),'onroad':False,'kind':'group','landmark':True,'clear':5,'name':'finish: the record shop; its flip sign turns from CLOSED to OPEN as the line arrives (EGG: new beginning)',
  'parts':shop(10,7,6,'#f3e6cf',CC,BLACK)+[{'kind':'box','pos':[0,3.2,-3.2],'size':[2.2,0.8,0.1],'color':'#ffffff','id':'open_sign'}]},
 {'id':'members5','t':205.0,'off':(-6,4),'kind':'group','egg':True,'clear':3,'name':'EGG: five small denim/green/black outfits on a clothes rail outside the shop (cover outfits)',
  'parts':[{'kind':'cylinder','pos':[0,2.2,0],'size':[0.06,0.06,5],'rot':[0,0,90],'color':'#888888'}]+[{'kind':'box','pos':[-2+i,1.5,0],'size':[0.7,1.2,0.15],'color':c} for i,c in enumerate([DENIM,BLACK,'#1d2a55',DENIM,GREEN])]},
]
EVENTS=[
 
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

B=1.91996; S0=0.339
def hb(bar): return round(S0+B*bar,2)
ELEV=[{'t0':hb(20),'t1':hb(24)-0.3,'type':'ramp','dy':3,'note':'pre-chorus: the teal footbridge staircase climbs from street level L0 to the rail plaza L1'},
      {'t0':hb(44),'t1':hb(52)-0.3,'type':'ramp','dy':4,'note':'verse 2 second half: rooftop terraces climb to L2 (+7)'},
      {'t0':hb(72),'t1':hb(80)-0.3,'type':'ramp','dy':-4,'note':'bridge: long narrow laundry bridge glides back down to L1'},
      {'t0':hb(80),'t1':hb(88)-0.3,'type':'ramp','dy':6,'note':'build: climb around the water tower'},
      {'t':hb(88),'type':'fall','dy':-6,'snap':True,'note':'final-chorus downbeat: drop off the tower onto the plaza'},
      {'t0':hb(96),'t1':hb(100)-0.3,'type':'ramp','dy':3,'note':'final chorus 2nd half: rooftop-garden loop climbs and passes over the earlier roads'}]
BLOCKS=[
 {'t0':0,'tex':'stair'},
 {'t0':hb(4),'tex':'serpL','P':[1.4,1.9],'m':[4,6],'phases':[0]},
 {'t0':hb(12),'tex':'bolt','P':[2*B,B],'phases':[0,B]},
 {'t0':hb(20),'tex':'stair'},
 {'t0':hb(24),'tex':'orbit','P':[2*B,2.5*B,3*B],'m':[3],'phases':[0,B/2,B],'xw':3,'look':4},
 {'t0':hb(32),'tex':'zig','P':[B,1.5*B,2*B],'phases':[0,B/2,B,1.5*B,2*B,3*B],'sides':['R','L'],'xw':3},
 {'t0':hb(40),'tex':'switch','P':[2*B,3*B],'phases':[0,B],'xw':3},
 {'t0':hb(48),'tex':'serp','m':[6,8],'phases':[0,2,4],'xw':3,'look':4},
 {'t0':hb(56),'tex':'orbit','P':[1.5*B,2*B,2.5*B,3*B],'m':[3,4],'phases':[0,B/2,B],'xw':4,'look':6},
 {'t0':hb(64),'tex':'bolt','P':[B,2*B],'phases':[0,B/2],'xw':4,'look':4},
 {'t0':hb(72),'tex':'switch','P':[B,1.5*B,2*B],'phases':[0,B/2,B],'xw':4,'look':4},
 {'t0':hb(80),'tex':'orbit','P':[2*B,1.75*B,1.5*B],'m':[4,5],'phases':[0,B/2,B],'xw':4,'look':6},
 {'t0':hb(88),'tex':'xspiral','P':[B,1.5*B,2*B],'m':[5,6],'phases':[0,B/2,B,1.5*B,2*B,3*B],'sides':['R','L'],'xw':4,'look':4},
 {'t0':hb(96),'tex':'orbit','P':[2*B,1.5*B,2.5*B],'m':[3,4],'phases':[0,B/2,B],'xw':4,'look':4},
 {'t0':hb(104),'tex':'turn','phases':[0,B],'xw':4},
]
MARGIN=0.3
FORKS=[20.0,85.0,128.0,190.0]
BEAM=20
# --- codex-ref alignment (nj-refs/how-sweet): cat balcony egg, teal footbridge, white train + yellow gantries, five B/W panels + orange
TEAL='#507f83'; SUN='#e9bc48'
OBJECTS+=[
 {'id':f'apt{i}','t':t,'off':(s_,0),'kind':'group','clear':4.5,'appear':{'t':t-2,'mode':'rise','dur':0.7},
  'parts':[{'kind':'box','pos':[0,4,0],'size':[7,8,6],'color':'#f2efe4'},{'kind':'box','pos':[0,8.2,0],'size':[7.4,0.4,6.4],'color':TEAL}]+
          [{'kind':'box','pos':[-2+2*(k%3),2+2.6*(k//3),-3.05],'size':[1.2,1.4,0.1],'color':'#292d32'} for k in range(6)]+
          [{'kind':'box','pos':[0,2.6+2.6*k,-3.6],'size':[6,0.15,1.2],'color':TEAL} for k in range(2)]}
 for i,(t,s_) in enumerate([(10.5,9),(14.5,-9),(18.5,9),(26.5,-9),(30.5,9),(34.5,-9)])]+[
 {'id':'cat_egg','t':16.5,'off':(-8.5,0),'y':5.4,'kind':'group','egg':True,'clear':4,'react':'beat','name':'EGG E1: orange cat on an apartment balcony; it turns its head with the syncopated claps; the same cat silhouette reappears in the final chorus skyline',
  'parts':[{'kind':'box','pos':[0,0,0],'size':[3,0.2,1.6],'color':TEAL},{'kind':'sphere','pos':[0,0.6,0],'size':[0.9,0.8,0.7],'color':'#ff5b24'},{'kind':'sphere','pos':[0.45,1.15,0],'size':[0.55,0.5,0.5],'color':'#ff5b24'},
           {'kind':'cone','pos':[0.33,1.45,0],'size':[0.18,0.25,0.18],'color':'#ff5b24'},{'kind':'cone','pos':[0.6,1.45,0],'size':[0.18,0.25,0.18],'color':'#ff5b24'}]},
 {'id':'cat_egg2','t':186.0,'off':(16,12),'y':6,'kind':'group','egg':True,'clear':6,'name':'EGG E1 return: cat silhouette on a far rooftop',
  'parts':[{'kind':'box','pos':[0,-3,0],'size':[5,6,5],'color':'#e6e1d4'},{'kind':'sphere','pos':[0,0.6,0],'size':[1.4,1.2,1.0],'color':'#292d32'},{'kind':'sphere','pos':[0.7,1.4,0],'size':[0.8,0.7,0.7],'color':'#292d32'}]},
 {'id':'rail_l','kind':'row','t0':38.9,'t1':46.2,'side':2.4,'spacing':1.2,'bothSides':True,'item':{'kind':'box','size':[0.18,0.9,1.0],'color':TEAL},'name':'teal footbridge railings (low, 2.4 off centre)'},
 {'id':'train','t':54.0,'off':(13,0),'y':-3,'kind':'group','landmark':True,'clear':6,'react':'beat','name':'white commuter train on the lower track beside the rail plaza (MV level crossing)',
  'parts':[{'kind':'box','pos':[0,1.6,k*7.4],'size':[3,3,7],'color':'#f2efe4'} for k in range(-2,3)]+[{'kind':'box','pos':[-1.52,2.1,k*7.4],'size':[0.05,0.9,5.5],'color':'#292d32'} for k in range(-2,3)]+
          [{'kind':'box','pos':[0,0,0],'size':[5,0.3,40],'color':'#8f8a80'}]},
]+[
 {'id':f'gantry{i}','t':t,'off':(s_,0),'kind':'group','clear':3.5,'appear':{'t':t-1.5,'mode':'unfold','dur':0.6},'name':'yellow level-crossing gantry (opens outward on the chorus downbeat)',
  'parts':[{'kind':'box','pos':[0,3,0],'size':[0.6,6,0.6],'color':SUN},{'kind':'box','pos':[s_/abs(s_)*-1.6,6,0],'size':[3.8,0.5,0.5],'color':SUN}]} for i,(t,s_) in enumerate([(48,5.5),(52,-5.5),(56,5.5),(60,-5.5),(64,5.5),(68,-5.5)])
]+[
 {'id':f'panel{i}','t':58.0,'off':(-17,-6+3.2*i),'y':-3,'kind':'box','size':[2.6,9,0.6],'color':['#292d32','#f2efe4','#292d32','#f2efe4','#292d32','#ff5b24'][i],'clear':10,'landmark':i==5,
  'name':'five black/white standing panels + the orange sleeve panel (abstracted group cover); they rise one by one in chorus 2 and line up again in the final chorus'} for i in range(6)
]+[
 {'id':'panels_poster','t':120.0,'off':(15,8),'kind':'image','src':'art/panels-poster.jpg','size':[12,0,6.75],'mode':'billboard','y':5,'clear':8,'name':'poster of the five panels on the rooftop courtyard wall'},
 {'id':'water_tower','t':160.0,'world':('hole',154.5,168.5),'kind':'group','landmark':True,'clear':1,'name':'water tower: the build-section helix winds around it',
  'parts':[{'kind':'cylinder','pos':[0,6,0],'size':[0.8,12,0.8],'color':TEAL},{'kind':'cylinder','pos':[0,13.5,0],'size':[3.4,3,3.4],'color':'#f2efe4'},{'kind':'cone','pos':[0,15.6,0],'size':[3.8,1.2,3.8],'color':'#ff5b24'}]},
]
EVENTS+=[{'t':107.86+i*0.96,'type':'raise','target':f'panel{i}','dy':6,'dur':0.5,'note':'panels rise one per half-bar at the chorus-2 downbeat (music clock)'} for i in range(6)]
EVENTS+=[{'t':46.42,'type':'pulse','target':'train','every':0.47999,'until':77.14}]
ART={'backdrop':'art/sky-summer.jpg','ground':{'src':'art/plaza-ground.jpg','scale':40}}
COLLECT={'diamond':'#75e1d0','crown':'#e9bc48'}
