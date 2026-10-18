import sys; sys.path.insert(0,'/workspace/w4/designs'); from common import *
TITLE='Right Now'; BPM=172.0; START='N'
GRID={'bar0':0.3345,'beat':0.34884,'note':'bar n starts at 0.3345 + 1.39536*n; grid = 8 eighths per bar (0.1744 s); shifted -31 ms to measured hat/snare transients'}
JUDGMENT={'perfect':0.04,'good':0.075,'miss_beyond':0.085,'note':'min gap 0.174 s (8th at 172): good window +/-75 ms so a tap is never ambiguous between neighbours (half-gap 87 ms). Must be checked with real touch latency.'}
SPEED=[{'t':0,'v':10.5},{'t':78.47,'v':9.5},{'t':100.79,'v':10.5},{'t':123.12,'v':11.0},{'t':145.45,'v':10.0}]
CHART_NOTES='Drum & bass: taps on kick (1, 3&) and snare (2, 4) with vocal pickups; 8th bursts of max 3 in verse/chorus, max 4 in the final chorus; half-time bridge follows the snare on 3 + vocal. Piano-only intro/outro tapped sparsely on chord hits. See chart-report.md.'
MINT='#bfead6'; CREAM='#fff8ec'; PETAL=PETALS
# Route: chat-bubble gate N -> mailbox lane NE -> greenhouse corridor (ramp) -> greenhouse opens NW (chorus) -> NE verse 2 ->
# half-time bridge climbs onto the roof girders SE (ramp +4, slower) -> drop into the flower field NE (chorus 2) -> break -> final NW narrow & fast -> NE plank to the lamp.
ROT=[(44.98,'L'),(67.31,'R'),(78.47,'R'),(100.79,'L'),(123.12,'L'),(145.45,'R')]
ELEV=[{'t0':34.2,'t1':44.5,'type':'ramp','dy':2,'note':'pre-chorus: gentle climb into the greenhouse'},
      {'t0':79.5,'t1':96.0,'type':'ramp','dy':4,'note':'half-time bridge: walk up the greenhouse roof girders'},
      {'t':100.12,'type':'fall','dy':-6,'note':'jump off the roof into the flower field, landing just before the chorus-2 downbeat'}]
WIDTH=[{'t':0,'w':2.8},{'t':11.5,'w':2.3},{'t':44.98,'w':2.2},{'t':78.47,'w':2.4},{'t':100.79,'w':2.1},{'t':123.12,'w':1.8},{'t':145.45,'w':2.6}]
REVEAL=[{'t':0,'mode':'static','lead':3.0},{'t':11.5,'mode':'rise','lead':1.8},{'t':44.98,'mode':'unfold','lead':1.5},{'t':78.47,'mode':'unfold','lead':2.0},
        {'t':100.79,'mode':'rise','lead':1.4},{'t':117.54,'mode':'drop','lead':1.8},{'t':123.12,'mode':'rise','lead':1.3},{'t':145.45,'mode':'static','lead':3.0}]
PALETTE={'skyTop':'#bfe3f2','skyBottom':'#fffaf0','fog':'#f3fbf7','fogStart':40,'fogEnd':120,'ground':'#e9f4ea','groundY':-0.6,
         'road':CREAM,'roadSide':MINT,'line':'#ff5fa8','light':'#fffaf0','lightIntensity':1.2,'ambient':'#cfe3dc','particles':None}
SECTIONS_L=[
 {'t':0,'label':'Intro','palette':{'skyTop':'#e9f1f5','ground':'#f4f6f6','roadSide':'#e2e6e8'},'camera':'close','note':'empty white chat-bubble gate, three typing dots breathe; piano only'},
 {'t':11.5,'label':'Verse 1','palette':{'roadSide':MINT},'camera':'iso','note':'mailbox lane; pots sprout as the beat comes in'},
 {'t':33.82,'label':'Pre-chorus 1','palette':{'roadSide':'#9fdcc0'},'camera':'low','note':'glass corridor climbs into the greenhouse'},
 {'t':44.98,'label':'Chorus 1','palette':{'ground':'#d8f0dc','roadSide':'#ff9ec4','particles':'petals'},'camera':'high','note':'greenhouse opens; flower crowd nods on the beat'},
 {'t':67.31,'label':'Verse 2','palette':{'roadSide':MINT,'particles':None},'camera':'iso','note':'potting benches, letters in transparent mailboxes'},
 {'t':78.47,'label':'Half-time bridge','palette':{'skyTop':'#ffd9c4','skyBottom':'#fff3e6','roadSide':'#f2c14e'},'camera':'side','note':'slower: up onto the roof girders, the line walks the glass roof ridge'},
 {'t':100.79,'label':'Chorus 2','palette':{'ground':'#cdeccf','roadSide':'#ff5a2c','particles':'petals'},'camera':'iso','note':'drop into the flower field'},
 {'t':117.54,'label':'Break','palette':{'particles':None},'camera':'high','note':'road tiles drop in from above, petals hang in the air'},
 {'t':123.12,'label':'Final chorus','palette':{'roadSide':'#c2449a','particles':'petals'},'camera':'iso','note':'narrow, fast, everything blooms'},
 {'t':145.45,'label':'Outro','palette':{'skyTop':'#ffd7b0','skyBottom':'#fff6e6','particles':None},'camera':'wide','note':'piano: plank road to a warm lamp (the typing dots became a light)'}]
CAMERA=[{'t':0,'preset':'close','blend':0},{'t':11.5,'preset':'iso','blend':2.0},{'t':33.82,'preset':'low','blend':1.8},{'t':44.98,'preset':'high','blend':1.0},
 {'t':56.14,'preset':'iso','yaw':30,'blend':2.0},{'t':67.31,'preset':'iso','blend':1.6},{'t':78.47,'preset':'side','blend':2.5},{'t':89.63,'preset':'side','yaw':70,'dist':20,'blend':3.0},
 {'t':99.4,'preset':'iso','blend':1.2},{'t':117.54,'preset':'high','blend':1.5},{'t':123.12,'preset':'iso','dist':16,'blend':0.8},{'t':134.28,'preset':'iso','yaw':-25,'dist':16,'blend':2.0},
 {'t':145.45,'preset':'wide','blend':3.0}]
def mailbox(c): return [{'kind':'cylinder','pos':[0,0.6,0],'size':[0.15,1.2,0.15],'color':'#9aa0a6'},{'kind':'box','pos':[0,1.45,0],'size':[0.9,0.7,1.2],'color':c},
                        {'kind':'box','pos':[0.5,1.7,0],'size':[0.05,0.5,0.15],'color':'#ff5a2c'}]
OBJECTS=[
 {'id':'chat_gate','t':1.0,'off':(0,6),'onroad':True,'kind':'group','landmark':True,'clear':0,'name':'start gate: an empty white chat bubble arch; three typing dots breathe on top (music clock)',
  'parts':[{'kind':'box','pos':[-3.2,2.5,0],'size':[1.0,5,1.0],'color':'#ffffff'},{'kind':'box','pos':[3.2,2.5,0],'size':[1.0,5,1.0],'color':'#ffffff'},{'kind':'box','pos':[0,5.6,0],'size':[7.4,1.6,1.0],'color':'#ffffff'},
           {'kind':'pyramid','pos':[-2.6,4.4,0],'size':[1.2,1.0,1.0],'color':'#ffffff'},
           {'kind':'sphere','pos':[-1.2,5.6,-0.55],'size':[0.6,0.6,0.2],'color':'#b0b8bf','id':'dot1'},{'kind':'sphere','pos':[0,5.6,-0.55],'size':[0.6,0.6,0.2],'color':'#b0b8bf','id':'dot2'},{'kind':'sphere','pos':[1.2,5.6,-0.55],'size':[0.6,0.6,0.2],'color':'#b0b8bf','id':'dot3'}]},
 {'id':'postmark','t':0.6,'off':(-3.5,1),'kind':'cylinder','size':[1.6,0.1,1.6],'color':'#ff9ec4','clear':0.5,'name':'petal-coloured postmark at the start'},
]+[
 {'id':f'mailbox{i}','t':t,'off':(s,0),'kind':'group','parts':mailbox(PETAL[(i*3)%12]),'clear':1.0,'appear':{'t':t-1.6,'mode':'pop','dur':0.3}} for i,(t,s) in enumerate([(13,-4.5),(16,4.5),(19,-4.5),(22,4.5),(25,-4.5),(28,4.5),(31,-4.5),(69,4.5),(72,-4.5),(75,4.5)])
]+[
 {'id':f'pot{i}','t':t,'off':(s,0),'kind':'group','parts':pot(PETAL[(i*5)%12],PETAL[(i*7+3)%12]),'clear':1.0,'react':'beat','appear':{'t':t-1.5,'mode':'grow','dur':0.5}}
 for i,(t,s) in enumerate([(14.5,4.5),(17.5,-4.5),(20.5,4.5),(23.5,-4.5),(26.5,4.5),(29.5,-4.5),(32.5,4.5)])
]+[
 {'id':'glass_corridor','kind':'row','t0':34.0,'t1':44.8,'side':0,'spacing':3.5,'bothSides':False,'item':{'kind':'arch','size':[7,6,0.3],'color':'#e8fbff'},'name':'glass greenhouse corridor frames'},
 {'id':'flower_crowd','kind':'row','t0':45.2,'t1':66.9,'side':4.5,'spacing':1.6,'bothSides':True,'item':{'kind':'flower','size':[0.9,1.2,0.9],'color':'#ff9ec4','color2':'#fff200','react':'beat'},'name':'flower crowd nodding on the beat'},
 {'id':'greenhouse','t':52.0,'off':(-20,10),'kind':'group','landmark':True,'clear':10,'name':'the message greenhouse (glass house with mint frame); its far wall opens at Chorus 1',
  'parts':[{'kind':'box','pos':[0,4,0],'size':[16,8,12],'color':'#dff6ff'},{'kind':'pyramid','pos':[0,10,0],'size':[17,4,13],'color':'#c9eef7'},{'kind':'box','pos':[0,4,-6.05],'size':[16.2,0.4,0.1],'color':MINT}]},
 {'id':'message_frame','t':60.0,'off':(18,18),'y':6,'kind':'group','clear':4,'name':'empty message box floating far off-road; a petal passes through it and turns into a star (never in front of the road)',
  'parts':[{'kind':'box','pos':[0,0,0],'size':[8,4,0.3],'color':'#ffffff'},{'kind':'pyramid','pos':[-2.5,-2.4,0],'size':[1.2,1,0.3],'color':'#ffffff'}]},
 {'id':'girders','kind':'row','t0':79.0,'t1':99.8,'side':2.6,'spacing':2.2,'bothSides':True,'item':{'kind':'box','size':[0.25,0.25,2.0],'color':'#6fbfa0'},'name':'greenhouse roof girders beside the ridge road'},
 {'id':'roof_panes','kind':'row','t0':79.0,'t1':99.8,'side':5.5,'spacing':4.0,'bothSides':True,'item':{'kind':'box','size':[3.5,0.1,3.5],'color':'#e8fbff'}},
 {'id':'cups_egg','t':88.0,'off':(5.5,0),'kind':'group','egg':True,'clear':1.5,'name':'EGG: two tiny paper cups on a roof ledge passing a flower back and forth (on the half-time snare)',
  'parts':[{'kind':'cone','pos':[-0.6,0.35,0],'size':[0.5,0.7,0.5],'color':'#ffffff'},{'kind':'cone','pos':[0.6,0.35,0],'size':[0.5,0.7,0.5],'color':'#ffffff'},{'kind':'flower','pos':[0,0.8,0],'size':[0.3,0.5,0.3],'color':'#ff5fa8'}]},
 {'id':'flower_field','kind':'row','t0':101.0,'t1':117.3,'side':4.0,'spacing':1.3,'bothSides':True,'item':{'kind':'flower','size':[1.0,1.4,1.0],'color':'#ff5a2c','color2':'#fff200','react':'kick'}},
 {'id':'big_flower','t':110.0,'off':(-16,12),'kind':'group','landmark':True,'clear':8,'react':'beat','name':'giant rainbow flower (Supernatural cover sister) standing in the field',
  'parts':[{'kind':'cylinder','pos':[0,3,0],'size':[0.8,6,0.8],'color':'#4c9a5b'}]+[dict(p,pos=[p['pos'][0],p['pos'][1]+2,p['pos'][2]]) for p in murakami_flower(r=4)]},
 {'id':'pots5_egg','t':140.0,'off':(-6,2),'kind':'group','egg':True,'clear':3,'name':'EGG: five pots with different-coloured tags; all five turn to face the direction the line leaves',
  'parts':sum([[dict(p,pos=[p['pos'][0]+(-3+1.5*i),p['pos'][1],p['pos'][2]]) for p in pot(PETAL[i*2],['#ff5fa8','#00aeef','#fff200','#00a651','#5b3f9e'][i])] for i in range(5)],[])},
 {'id':'final_petals','kind':'row','t0':123.3,'t1':145.2,'side':3.4,'spacing':1.8,'bothSides':True,'item':{'kind':'cylinder','size':[0.9,0.12,0.9],'color':'#ff9ec4','react':'tap'}},
 {'id':'lamp','t':155.0,'off':(4,6),'kind':'group','landmark':True,'clear':2,'name':'finish: the three typing dots became one warm lamp',
  'parts':[{'kind':'cylinder','pos':[0,2,0],'size':[0.2,4,0.2],'color':'#555555'},{'kind':'sphere','pos':[0,4.3,0],'size':[1.1,1.1,1.1],'color':'#ffe2a0'}],'appear':{'t':145.45,'mode':'fade','dur':3.0}},
 {'id':'planks_end','kind':'row','t0':145.6,'t1':156.0,'side':1.8,'spacing':1.0,'bothSides':True,'item':{'kind':'box','size':[0.8,0.12,0.9],'color':'#d8b98a','react':'tap'}},
]
EVENTS=[
 {'t':0.3,'type':'pulse','target':'chat_gate','every':0.69768,'until':11.5,'note':'typing dots breathe every half bar (music clock, not tap-related)'},
 {'t':11.5,'type':'burst','at':'player','particles':'petals'},
 {'t':44.98,'type':'unfold','target':'greenhouse','note':'far glass wall swings open'},{'t':44.98,'type':'particles','particles':'petals','until':67.3},
 {'t':60.0,'type':'burst','at':'message_frame','particles':'stars'},
 {'t':78.47,'type':'color','palette':{'skyTop':'#ffd9c4'},'dur':3.0},
 {'t':100.79,'type':'burst','at':'player','particles':'petals'},{'t':100.79,'type':'shake','dur':0.3,'amount':0.15},
 {'t':123.12,'type':'flash','dur':0.2},{'t':123.12,'type':'particles','particles':'petals','until':145.4},
 {'t':145.45,'type':'color','palette':{'skyTop':'#ffd7b0','skyBottom':'#fff6e6'},'dur':4.0},{'t':150.0,'type':'light','target':'lamp'}]
FINISH={'kind':'gate','note':'small wooden doorway with the lamp beside it'}
DIAMOND_TARGETS=[6,20,38,56,73,90,108,120,134,150]; CROWN_TARGETS=[70.0,120.0]
MARGIN=1.5
