D={'kick_on':1.0,'snare_on':0.9,'vocal_on':1.2,'bass_on':0.5,'mel_on':0.2}
V={'vocal_on':1.6,'kick_on':0.6,'snare_on':0.5,'mel_on':0.3}
B=1.5287
cfg=dict(bar_off=0,end=231.0,sections=[
 dict(t=0.0,label='Intro',kind='intro',dens=0.7,w={'kick_on':1.0,'snare_on':0.6,'vocal_on':1.0,'bass_on':0.8},mingap=0.7,maxgap=2.5,res=1),
 dict(t=12.33,label='Verse 1',kind='verse',dens=1.9,w=D,mingap=0.19,res=2,maxrun=4,add=[12.33]),
 dict(t=36.79,label='Pre-chorus 1',kind='pre',dens=1.8,w=V,mingap=0.19,res=2,maxrun=4,add=[36.79]),
 dict(t=49.02,label='Chorus 1',kind='chorus',dens=2.6,w=D,mingap=0.19,res=2,maxrun=6,add=[49.02]),
 dict(t=73.48,label='Verse 2',kind='verse',dens=1.8,w=D,mingap=0.19,res=2,maxrun=4,add=[73.48]),
 dict(t=97.94,label='Pre-chorus 2',kind='pre',dens=1.8,w=V,mingap=0.19,res=2,maxrun=4,add=[97.94]),
 dict(t=110.17,label='Chorus 2',kind='chorus',dens=2.6,w=D,mingap=0.19,res=2,maxrun=6,add=[110.17]),
 dict(t=134.63,label='Jersey-club bridge',kind='bridge',dens=3.1,w={'snare_on':1.0,'kick_on':0.9,'mel_on':0.6,'vocal_on':0.8,'bass_on':0.5},mingap=0.19,res=2,maxrun=10,add=[134.63]),
 dict(t=159.09,label='Final chorus',kind='chorus',dens=2.6,w=D,mingap=0.19,res=2,maxrun=6,add=[159.09]),
 dict(t=183.55,label='Dance break',kind='break',dens=1.35,w={'kick_on':1.0,'snare_on':0.8,'vocal_on':1.4,'mel_on':0.4},mingap=0.38,res=2,maxgap=2.0,add=[183.55]),
 dict(t=208.01,label='Outro',kind='outro',dens=1.45,w=V,mingap=0.19,res=2,maxrun=4,add=[208.01]),
])
route=dict(speed=[{'t':0,'v':10.0}],W=2.4,
 elev=[{'t0':36.9,'t1':48.9,'type':'ramp','dy':3},{'t0':98.0,'t1':110.0,'type':'ramp','dy':3},
       {'t0':134.7,'t1':146.0,'type':'ramp','dy':-3},{'t0':153.0,'t1':159.0,'type':'ramp','dy':3},{'t0':208.1,'t1':228.0,'type':'ramp','dy':-6}],
 macro=[dict(t=1.0,diag='NE'),dict(t=49.02,diag='NE'),dict(t=54.5,diag='SE'),dict(t=62.5,diag='SW'),dict(t=68.0,diag='SE'),
        dict(t=73.48,diag='SE'),dict(t=97.94,diag='NE'),dict(t=110.17,diag='SE'),dict(t=134.63,diag='SW'),
        dict(t=159.09,diag='NW'),dict(t=188.32,kind='force',dirs='LLRR'*6),dict(t=196.0,diag='SW'),dict(t=208.01,diag='SW')])
