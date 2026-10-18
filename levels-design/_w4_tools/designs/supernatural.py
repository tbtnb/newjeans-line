import sys; sys.path.insert(0,'/workspace/w4/designs'); from common import *
TITLE='Supernatural'; BPM=109.0; START='N'
GRID={'bar0':0.358,'beat':0.55046,'note':'bar n starts at 0.358 + 2.20184*n (4/4); constant tempo (beat-tracker fit, median residual 4.7 ms)'}
JUDGMENT={'perfect':0.05,'good':0.09,'miss_beyond':0.12,'note':'+/-90 ms good; min tap gap 0.275 s (eighth at 109 BPM) so windows never overlap. Validate on real touch: if late-tap bias > 30 ms, shift engine latency, not chart.'}
SPEED=[{'t':0,'v':9.0}]
CHART_NOTES='Semi-automatic: per-section density/weights set by hand, slot choice scored on demucs stems (kick/clap/vocal/synth), phrase fills hand-planned (bar 27 8-run, bar 51 7-run). See chart-report.md.'
# Route: W-shaped rooftop run (intro->verse1 ridge->pre), then a diamond LOOP around the flower antenna (chorus1->verse2->bridge->chorus2)
# that closes by crossing OVER the pre-chorus road on a raised gantry (+4) at ~134 s, then out east to the open sky.
ROT=[(26.78,'R'),(44.39,'L'),(62.01,'L'),(79.62,'R'),(97.24,'R'),(114.85,'R'),(137.0,'L'),(150.08,'L')]
WIDTH=[{'t':0,'w':2.6},{'t':26.78,'w':2.3},{'t':62.01,'w':2.2},{'t':97.24,'w':2.4},{'t':114.85,'w':2.0},{'t':150.08,'w':1.8},{'t':167.7,'w':2.4}]
REVEAL=[{'t':0,'mode':'static','lead':3.0},{'t':9.17,'mode':'rise','lead':2.0},{'t':62.01,'mode':'rise','lead':1.6},
        {'t':97.24,'mode':'unfold','lead':1.8},{'t':114.85,'mode':'drop','lead':1.5},{'t':150.08,'mode':'rise','lead':1.4},{'t':167.7,'mode':'fade','lead':2.5}]
PALETTE={'skyTop':'#070b24','skyBottom':'#1b2152','fog':'#141a40','fogStart':35,'fogEnd':110,'ground':'#0e1230','groundY':-14,
         'road':'#f6f0e4','roadSide':'#5b3f9e','line':'#ff5fa8','light':'#fff1dc','lightIntensity':0.9,'ambient':'#3a4374','particles':None}
SECTIONS_L=[
 {'t':0,'label':'Intro','palette':{'roadSide':'#5b3f9e'},'camera':'close','note':'radio booth under the flower billboard; sample ad-libs, no drums'},
 {'t':9.17,'label':'Groove','palette':{'roadSide':'#0072bc','particles':'dust'},'camera':'iso','note':'NJS groove enters: antennas & water tanks on rooftops'},
 {'t':26.78,'label':'Verse 1','palette':{'roadSide':'#00aeef'},'camera':'iso','note':'route bends right along a long roof ridge'},
 {'t':44.39,'label':'Pre-chorus 1','palette':{'roadSide':'#00a651'},'camera':'low','note':'climb toward the loop; receivers light up one by one'},
 {'t':62.01,'label':'Chorus 1','palette':{'roadSide':'#93d14b','skyBottom':'#2a2a66'},'camera':'high','note':'flower antenna blooms; loop begins'},
 {'t':79.62,'label':'Verse 2','palette':{'roadSide':'#fff200'},'camera':'iso','note':'north edge of the loop, city lights below'},
 {'t':97.24,'label':'Bridge','palette':{'roadSide':'#ffc928','skyTop':'#03040f','fogEnd':140,'particles':'stars'},'camera':'top','note':'drums out: fall into the floating star layer'},
 {'t':114.85,'label':'Chorus 2','palette':{'roadSide':'#ff8f2a','skyTop':'#0b0f30'},'camera':'iso','note':'back up; gantry climbs over the loop'},
 {'t':132.47,'label':'Interlude','palette':{'roadSide':'#ff5a2c'},'camera':'side','note':'crossing over our own pre-chorus road = the two signals meet'},
 {'t':150.08,'label':'Final chorus','palette':{'roadSide':'#ff5fa8','particles':'stars'},'camera':'iso','note':'drop + narrow road, everything pulses'},
 {'t':167.7,'label':'Outro','palette':{'roadSide':'#c2449a','fog':'#0a0d26'},'camera':'wide','note':'sample returns, road runs into empty sky toward the bunny moon'}]
CAMERA=[{'t':0,'preset':'close','blend':0},
 {'t':9.17,'preset':'iso','blend':2.2},
 {'t':26.78,'preset':'iso','yaw':30,'blend':2.0},
 {'t':44.39,'preset':'low','blend':2.0},
 {'t':60.0,'preset':'wide','blend':1.6,'note':'one-bar reveal of the flower antenna during the 8-run (road ahead still in frame)'},
 {'t':62.01,'preset':'high','blend':1.0},
 {'t':79.62,'preset':'iso','yaw':-25,'blend':2.0},
 {'t':97.24,'preset':'top','blend':2.5,'note':'falling into stars, top-down calm'},
 {'t':112.65,'preset':'iso','blend':1.6},
 {'t':123.66,'preset':'iso','yaw':40,'dist':20,'blend':2.0},
 {'t':132.47,'preset':'high','blend':2.2,'note':'high view: the helix around the gantry pylon passes over its own first lap'},
 {'t':141.28,'preset':'iso','blend':2.0},
 {'t':150.08,'preset':'iso','dist':16,'shake':0.15,'blend':0.6},
 {'t':150.6,'preset':'iso','dist':16,'shake':0,'blend':0.4},
 {'t':167.7,'preset':'wide','blend':3.0},
 {'t':176.5,'worldYaw':45,'pitch':28,'dist':26,'blend':4.0,'note':'swing to face the bunny moon'}]
def tank(): return [{'kind':'cylinder','pos':[0,1.6,0],'size':[2.2,2.4,2.2],'color':'#2d3566'},{'kind':'cone','pos':[0,3.1,0],'size':[2.4,0.8,2.4],'color':'#3c4680'},
                    {'kind':'box','pos':[0,0.3,0],'size':[2.6,0.6,2.6],'color':'#232a52'}]
def antenna(h=7,c='#ff5fa8'): return [{'kind':'cylinder','pos':[0,h/2,0],'size':[0.25,h,0.25],'color':'#9aa3d0'},{'kind':'box','pos':[0,h*0.7,0],'size':[2.4,0.15,0.15],'color':'#9aa3d0'},
                    {'kind':'box','pos':[0,h*0.85,0],'size':[1.6,0.15,0.15],'color':'#9aa3d0'},{'kind':'sphere','pos':[0,h+0.2,0],'size':[0.5,0.5,0.5],'color':c}]
def building(w,h,d,c='#1f2650',win='#ffd98a'):
    p=[{'kind':'box','pos':[0,-h/2,0],'size':[w,h,d],'color':c}]
    for k in range(int(h//3)):
        p.append({'kind':'box','pos':[w*0.18*((k%3)-1),-1.5-k*3,-d/2-0.05],'size':[0.8,1.0,0.1],'color':win})
    return p
OBJECTS=[
 # --- landmarks ---
 {'id':'flower_billboard','t':2.0,'off':(-12,18),'kind':'group','landmark':True,'name':'Murakami flower billboard (album cover) above the radio booth','clear':7,
  'parts':[{'kind':'box','pos':[0,7,0.6],'size':[13,13,0.4],'color':'#000000','texture':'art/flower-billboard.jpg'},{'kind':'cylinder','pos':[0,0.5,0.6],'size':[0.5,1,0.5],'color':'#444b78'}],
  'react':'beat'},
 {'id':'radio_booth','t':1.2,'off':(-5,4),'kind':'group','name':'tiny broadcast booth (start)','clear':2.5,
  'parts':[{'kind':'box','pos':[0,1.3,0],'size':[3,2.6,2.4],'color':'#f6f0e4'},{'kind':'box','pos':[0,2.75,0],'size':[3.4,0.3,2.8],'color':'#c2449a'},{'kind':'box','pos':[0.6,1.5,-1.21],'size':[1.2,0.8,0.05],'color':'#ffd98a'}]+[dict(p,pos=[p['pos'][0]-0.8,p['pos'][1]+2.8,p['pos'][2]]) for p in antenna(3,'#ff5a2c')]},
 {'id':'flower_antenna','t':62.5,'world':('hole',62.5,79.0),'kind':'group','landmark':True,'clear':9,
  'name':'Flower dish antenna at the centre of the loop: petals closed until Chorus 1, bloom on the downbeat; reachable only by eye (the loop orbits it)',
  'parts':[{'kind':'cylinder','pos':[0,10,0],'size':[0.9,20,0.9],'color':'#c7cbe8'},{'kind':'cylinder','pos':[0,20.2,0],'size':[3,0.6,3],'color':'#9aa3d0'}]+[dict(p,pos=[p['pos'][0],p['pos'][1]+18,p['pos'][2]]) for p in murakami_flower(r=6)],
  'appear':{'t':61.0,'mode':'grow','dur':1.0},'react':'beat'},
 {'id':'orbit_dot_a','t':62.5,'world':('hole',62.5,79.0),'wdx':-4,'kind':'sphere','size':[1.2,1.2,1.2],'y':30,'color':'#00aeef','name':'signal A (orbits the flower)','clear':1},
 {'id':'orbit_dot_b','t':62.5,'world':('hole',62.5,79.0),'wdx':4,'kind':'sphere','size':[1.2,1.2,1.2],'y':30,'color':'#ff5fa8','name':'signal B (orbits the flower)','clear':1},
 {'id':'radio_egg','t':36.0,'off':(9,4),'kind':'group','egg':True,'clear':2.5,
  'name':'EGG: old receiver; its dial lights the 5 cover colours in turn and the needle is a tiny bunny',
  'parts':[{'kind':'box','pos':[0,1,0],'size':[3.2,2,1.4],'color':'#7a4b2a'},{'kind':'box','pos':[0,1.3,-0.71],'size':[2.4,0.6,0.05],'color':'#f6f0e4'},
           {'kind':'sphere','pos':[-0.6,1.35,-0.75],'size':[0.25,0.35,0.1],'color':'#ffffff','id':'bunny_needle'},
           {'kind':'cylinder','pos':[-1.0,0.6,-0.72],'size':[0.5,0.1,0.5],'rot':[90,0,0],'color':'#c2449a'},{'kind':'cylinder','pos':[1.0,0.6,-0.72],'size':[0.5,0.1,0.5],'rot':[90,0,0],'color':'#00aeef'}]},
 {'id':'bunny_moon','t':178.0,'off':(-40,70),'y':38,'kind':'group','egg':True,'landmark':True,'clear':1,
  'name':'EGG/landmark: the moon is the bunny face from the cover (only framed when the outro camera swings at 176.5 s)',
  'parts':[{'kind':'sphere','pos':[0,0,0],'size':[12,12,2],'color':'#fff8e8'},{'kind':'box','pos':[0,6.5,0],'size':[2.6,5,1],'color':'#fff8e8'},
           {'kind':'sphere','pos':[-2,1,-1.1],'size':[1.0,1.4,0.2],'color':'#e8272b'},{'kind':'sphere','pos':[2,1,-1.1],'size':[1.0,1.4,0.2],'color':'#1fae6a'},
           {'kind':'sphere','pos':[0,-2,-1.1],'size':[4.5,2.6,0.2],'color':'#ff6fb5'}],
  'appear':{'t':167.7,'mode':'fade','dur':4.0}},
 {'id':'gantry_sign','t':133.0,'world':('hole',133.0,147.0),'kind':'group','landmark':True,'clear':3,'name':'gantry pylons holding the overpass (two-signals crossing)',
  'parts':[{'kind':'box','pos':[0,-3,0],'size':[1,10,1],'color':'#9aa3d0'},{'kind':'box','pos':[0,2,0],'size':[1.4,0.6,1.4],'color':'#ff5a2c'}]},
 {'id':'outro_bench','t':183.0,'off':(5,6),'kind':'bench','size':[3,1,1],'color':'#f6f0e4','name':'two-seat stargazing bench at the end','clear':2},
 # --- rooftop dressing (groove / verse 1) ---
]+[
 {'id':f'tank{i}','t':t,'off':(s,0),'kind':'group','parts':tank(),'clear':1.6,'appear':{'t':t-1.8,'mode':'rise','dur':0.6}} for i,(t,s) in enumerate([(11.5,7),(15.0,-7),(19.0,8),(23.0,-7),(30,7),(41,-8)])
]+[
 {'id':f'ant{i}','t':t,'off':(s,2),'kind':'group','parts':antenna(6+i%3,PETALS[(i*5)%12]),'clear':1.4,'react':'beat','appear':{'t':t-2,'mode':'rise','dur':0.5}} for i,(t,s) in enumerate([(13,-6),(17,6),(21,-6),(25,6),(28,-7),(33,7),(38,-6),(47,6),(51,-6),(55,6),(59,-6)])
]+[
 {'id':f'bld{i}','t':t,'off':(s,0),'y':-0.6,'kind':'group','parts':building(8,16+4*(i%3),8),'clear':5} for i,(t,s) in enumerate([(5,14),(14,-15),(24,15),(34,-15),(46,15),(56,-15),(70,16),(86,-16),(105,16),(122,-16),(142,16),(158,-16)])
]+[
 {'id':f'recv{i}','t':t,'off':(s,1),'kind':'group','clear':1.6,'name':'receiver dish (lights up one by one in Pre-chorus 1)',
  'parts':[{'kind':'cylinder','pos':[0,1,0],'size':[0.4,2,0.4],'color':'#9aa3d0'},{'kind':'disc','pos':[0,2.4,0],'size':[2.4,2.4,0.1],'rot':[60,0,0],'color':PETALS[(2+i*2)%12]}],
  'appear':{'t':t-1.5,'mode':'unfold','dur':0.6}} for i,(t,s) in enumerate([(45.5,-6),(48,6),(50.5,-6),(53,6),(55.5,-6),(58,6)])
]+[
 {'id':f'petal{i}','t':t,'off':(s,0),'kind':'cylinder','size':[2.4,0.3,2.4],'y':-2.5 if 97<t<115 else 0,'color':PETALS[i%12],'clear':1.4,'react':'tap',
  'appear':{'t':t-1.5,'mode':'pop','dur':0.3},'exit':{'t':t+4,'mode':'shrink','dur':0.6},'name':'floating petal pads'} for i,(t,s) in enumerate([(99,-5),(101,5),(103,-5),(105,5),(107,-5),(109,5),(111,-5),(113,5)])
]+[
 {'id':'stars_row','kind':'row','t0':97.4,'t1':114.4,'side':6,'spacing':4.0,'bothSides':True,'item':{'kind':'star','size':[0.8,0.8,0.8],'color':'#fff6c8','react':'beat'}},
 {'id':'city_lights','kind':'row','t0':62.0,'t1':97.0,'side':9,'spacing':5.0,'bothSides':True,'item':{'kind':'lamp','size':[0.6,3,0.6],'color':'#ffd98a','react':'kick'}},
 {'id':'final_lamps','kind':'row','t0':150.2,'t1':167.6,'side':4.0,'spacing':3.0,'bothSides':True,'item':{'kind':'box','size':[0.6,0.6,0.6],'color':'#ff5fa8','react':'tap'}},
]
EVENTS=[
 {'t':0.36,'type':'light','target':'flower_billboard','note':'billboard flickers on with the first sample hit'},
 {'t':9.17,'type':'particles','particles':'dust','until':26.78},
 {'t':36.0,'type':'color','target':'radio_egg','every':2.2018,'until':44.39,'note':'dial cycles the 5 cover colours, one per bar (music clock)'},
 {'t':44.39,'type':'light','target':'recv0'},{'t':46.6,'type':'light','target':'recv1'},{'t':48.8,'type':'light','target':'recv2'},
 {'t':51.0,'type':'light','target':'recv3'},{'t':53.2,'type':'light','target':'recv4'},{'t':55.4,'type':'light','target':'recv5'},
 {'t':62.01,'type':'burst','at':'flower_antenna','particles':'confetti'},
 {'t':62.01,'type':'spin','target':'orbit_dot_a','until':132.47,'note':'signals orbit the flower, one revolution per 4 bars'},
 {'t':62.01,'type':'spin','target':'orbit_dot_b','until':132.47},
 {'t':62.01,'type':'pulse','target':'flower_antenna','every':0.55046,'until':79.62},
 {'t':97.24,'type':'color','palette':{'skyTop':'#03040f','skyBottom':'#101436'},'dur':1.5},
 {'t':97.24,'type':'particles','particles':'stars','until':114.85},
 {'t':114.85,'type':'flash','dur':0.25,'note':'drum re-entry; screen-edge flash only, road surface untouched'},
 {'t':114.85,'type':'pulse','target':'flower_antenna','every':0.55046,'until':132.47},
 {'t':134.6,'type':'burst','at':'player','color':'#fff6c8','amount':40,'note':'interlude: the two orbit dots merge into one (music phrase start, not a turn)'},
 {'t':134.6,'type':'lower','target':'orbit_dot_a'},{'t':134.6,'type':'lower','target':'orbit_dot_b'},
 {'t':150.08,'type':'shake','dur':0.4,'amount':0.2},
 {'t':150.08,'type':'color','palette':{'skyBottom':'#3b1f5e'},'dur':2.0},
 {'t':167.7,'type':'color','palette':{'skyTop':'#05071a','skyBottom':'#141a40','particles':'stars'},'dur':3.0},
 {'t':176.5,'type':'raise','target':'bunny_moon','dy':4,'dur':4},
]
FINISH={'kind':'custom','note':'bunny-face gate: white arch shaped like the cover face, mouth opens as the line enters','parts':[
 {'kind':'box','pos':[-2.2,3,0],'size':[1.2,6,1.2],'color':'#ffffff'},{'kind':'box','pos':[2.2,3,0],'size':[1.2,6,1.2],'color':'#ffffff'},
 {'kind':'box','pos':[0,6.2,0],'size':[5.6,1.4,1.2],'color':'#ffffff'},{'kind':'box','pos':[0,8,0],'size':[1.2,2.4,1.2],'color':'#c2449a'}]}
DIAMOND_TARGETS=[7.5,20.5,38,57,86,104,123,143,160,178]; CROWN_TARGETS=[44.0,133.5]
MARGIN=1.5

B=2.20184; S0=0.333
def bt(bar): return round(S0+B*bar,2)
ELEV=[{'t0':bt(28)+0.3,'t1':bt(36),'type':'ramp','dy':8,'note':'Chorus 1: square helix of staircases around the flower antenna, +4 per lap'},
      {'t':bt(44),'type':'fall','dy':-8,'snap':True,'note':'drums drop out -> long fall off the antenna tower into the floating star layer'},
      {'t0':bt(48),'t1':bt(52),'type':'ramp','dy':4,'note':'climb out of the star layer'},
      {'t0':bt(53),'t1':bt(58),'type':'ramp','dy':4,'note':'Chorus 2 gantry climbs over earlier roads'},
      {'t0':bt(60),'t1':bt(64),'type':'ramp','dy':5,'note':'interlude helix around the gantry pylon'},
      {'t':bt(68),'type':'fall','dy':-8,'snap':True,'note':'big drop onto the final-chorus deck'}]
BLOCKS=[
 {'t0':0,'tex':'stair'},
 {'t0':bt(4),'tex':'bolt','P':[B],'phases':[0,B/2]},
 {'t0':bt(8),'tex':'switch','P':[2*B,1.5*B],'phases':[0,B/2]},
 {'t0':bt(12),'tex':'serpL','P':[0.8,1.0],'m':[4,6],'phases':[0]},
 {'t0':bt(16),'tex':'stair'},
 {'t0':bt(20),'tex':'zig','P':[B,1.5*B],'phases':[0,B/2,B]},
 {'t0':bt(24),'tex':'stair'},
 {'t0':bt(28),'tex':'orbit','P':[B,1.25*B],'m':[8,7],'phases':[0,B/2],'cross':1},
 {'t0':bt(36),'tex':'turn','phases':[0,B],'cross':1},
 {'t0':bt(40),'tex':'serpL','P':[0.8,1.0],'m':[4,6],'phases':[0]},
 {'t0':bt(44),'tex':'stair'},
 {'t0':bt(48),'tex':'switch','P':[B,1.5*B],'phases':[0,B/2]},
 {'t0':bt(52),'tex':'serp','m':[8,10],'phases':[0,2,4],'cross':1},
 {'t0':bt(60),'tex':'orbit','P':[B,1.25*B],'m':[4,5],'phases':[0,B/2],'cross':1},
 {'t0':bt(68),'tex':'stair'},
 {'t0':bt(72),'tex':'zig','P':[B,1.5*B],'phases':[0,B/2]},
 {'t0':bt(76),'tex':'turn','phases':[0,B]},
]
MARGIN=0.3
FORKS=[20.5,37.5,86.0,141.0]
COLLECT={'diamond':'#7fe3ff','crown':'#ffd54a'}
ART={'backdrop':'art/sky-night.jpg','ground':{'src':'art/roof-ground.jpg','scale':40}}
OBJECTS+=[
 {'id':'signal_poster','t':47.0,'off':(-13,6),'kind':'image','src':'art/signal-poster.jpg','size':[12,0,6.75],'mode':'billboard','y':3,'clear':7,'name':'retro broadcast poster on a rooftop hoarding (pre-chorus)'},
 {'id':'signal_poster2','t':156.0,'off':(13,6),'kind':'image','src':'art/signal-poster.jpg','size':[12,0,6.75],'mode':'billboard','y':3,'clear':7,'name':'same poster seen again in the final chorus'},
]
# --- codex-ref alignment (codex-ref/design.md + concept/blueprint, arrived late): L1 cloud weather tower, L2 text-free CRT TV, L3 rooftop broadcast stage
# (three square lamps, five square mic plinths instead of people), L6 five flower terraces, L7 white bunny-ear finish stone, E1 red-beret boat
OBJECTS+=[
 {'id':'cloud_tower','t':6.0,'off':(16,20),'kind':'group','landmark':True,'clear':8,'name':'L1 cloud weather tower: faceted cloud blocks stacked on a mast (rain/wind motif, never over the road)',
  'parts':[{'kind':'box','pos':[0,6,0],'size':[0.8,12,0.8],'color':'#7772b6'}]+[{'kind':'box','pos':[(k%2)*2-1,12+k*1.6,0],'size':[4-k*0.5,1.4,3],'color':'#dfe2f4'} for k in range(4)],
  'appear':{'t':0.4,'mode':'rise','dur':3.0}},
 {'id':'crt_tv','t':30.0,'off':(-8,4),'kind':'group','landmark':True,'clear':4,'name':'L2 retro CRT TV with colour-block screen only (no text)',
  'parts':[{'kind':'box','pos':[0,1.6,0],'size':[3.4,2.8,2.6],'color':'#34345c'},{'kind':'box','pos':[0,1.7,-1.31],'size':[2.6,2.0,0.05],'color':'#08aee0','id':'crt_screen'},
           {'kind':'cylinder','pos':[-0.6,3.6,0],'size':[0.06,1.4,0.06],'rot':[0,0,25],'color':'#cccccc'},{'kind':'cylinder','pos':[0.6,3.6,0],'size':[0.06,1.4,0.06],'rot':[0,0,-25],'color':'#cccccc'}]},
 {'id':'broadcast_stage','t':70.0,'off':(-13,0),'y':-3.6,'kind':'group','landmark':True,'clear':9,'name':'L3 rooftop broadcast stage: metal deck, three square front lamps, five white square mic plinths (stand-ins for the five members, no figures)',
  'parts':[{'kind':'box','pos':[0,0.3,0],'size':[10,0.6,6],'color':'#9aa0b8'}]+[{'kind':'box','pos':[-3+3*k,1.2,-3.2],'size':[1.0,1.0,0.6],'color':'#fff8f1'} for k in range(3)]+
          [{'kind':'box','pos':[-3.6+1.8*k,1.4,0.5],'size':[0.7,1.6,0.7],'color':'#ffffff'} for k in range(5)]},
 {'id':'boat_egg','t':104.0,'off':(-22,10),'y':2,'kind':'group','egg':True,'clear':10,'name':'E1 tiny boat with a red beret slides out of a cloud gap (far scenery, no collision)',
  'parts':[{'kind':'box','pos':[0,0,0],'size':[3,0.6,1.2],'color':'#fff8f1'},{'kind':'cylinder','pos':[0,0.7,0],'size':[0.5,0.15,0.5],'color':'#e8272b'}],
  'appear':{'t':101.0,'mode':'fade','dur':1.0},'exit':{'t':108.0,'mode':'fade','dur':1.0}},
]+[
 {'id':f'flower_terrace{k}','t':152.0+3.2*k,'off':(9 if k%2 else -9,0),'kind':'cylinder','size':[4.5,0.8,4.5],'y':-1.2,'color':['#fa428e','#ff8935','#f6e829','#93cd42','#08aee0'][k],'clear':4,
  'appear':{'t':150.06+2.2018*k,'mode':'rise','dur':0.6},'name':'L6 five coloured flower terraces rise one per bar in the final chorus'} for k in range(5)
]+[
 {'id':'bunny_stone','t':186.0,'off':(5,6),'kind':'group','landmark':True,'clear':4,'name':'L7 white bunny-ear finish stone',
  'parts':[{'kind':'box','pos':[0,1.5,0],'size':[2.4,3,1.2],'color':'#fff8f1'},{'kind':'box','pos':[-0.6,4.0,0],'size':[0.5,2.2,0.5],'color':'#fff8f1'},{'kind':'box','pos':[0.6,4.0,0],'size':[0.5,2.2,0.5],'color':'#fff8f1'}]},
]
EVENTS+=[{'t':26.754,'type':'color','target':'crt_tv','every':1.10092,'until':44.37,'note':'CRT colour block changes on the snare backbeat (music clock)'},
         {'t':61.983,'type':'light','target':'broadcast_stage','note':'stage lamps switch on at the chorus downbeat'}]
COLLECT={'diamond':'#ffd34e','crown':'#ffd34e'}
