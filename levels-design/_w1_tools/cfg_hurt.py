V={'vocal_on':1.8,'snare_on':0.6,'kick_on':0.5,'mel_on':0.4,'bass_on':0.4}
C={'vocal_on':1.5,'snare_on':0.8,'kick_on':0.6,'bass_on':0.5,'mel_on':0.3}
cfg=dict(bar_off=0,end=171.0,sections=[
 dict(t=0.0,label='Intro',kind='intro',dens=0.45,w={'vocal_on':1.0,'kick_on':0.8,'bass_on':0.8},mingap=0.9,maxgap=3.5,res=2,met=2.0),
 dict(t=10.927,label='Verse 1',kind='verse',dens=0.62,w=V,mingap=0.33,res=2,maxgap=2.7,add=[10.927]),
 dict(t=32.26,label='Pre-chorus 1',kind='pre',dens=0.8,w=V,mingap=0.33,res=2,add=[32.26]),
 dict(t=42.927,label='Chorus 1',kind='chorus',dens=1.0,w=C,mingap=0.33,res=2,add=[42.927]),
 dict(t=64.26,label='Verse 2',kind='verse',dens=0.62,w=V,mingap=0.33,res=2,maxgap=2.7,add=[64.26]),
 dict(t=80.26,label='Breath',kind='break',dens=0.4,w=V,mingap=0.66,res=2,maxgap=4.0),
 dict(t=85.594,label='Pre-chorus 2',kind='pre',dens=0.85,w=V,mingap=0.33,res=2,add=[85.594]),
 dict(t=96.26,label='Chorus 2',kind='chorus',dens=1.05,w=C,mingap=0.33,res=2,add=[96.26]),
 dict(t=117.594,label='Bridge',kind='bridge',dens=0.8,w=V,mingap=0.33,res=2,add=[117.594]),
 dict(t=128.26,label='Final chorus',kind='chorus',dens=1.2,w=C,mingap=0.16,res=4,maxrun=3,fastgap=0.2,add=[128.26]),
 dict(t=143.594,label='Outro',kind='outro',dens=0.55,w=V,mingap=0.33,res=2,maxgap=3.0,add=[143.594]),
])
route=dict(speed=[{'t':0,'v':7.5}],W=2.2,
 elev=[{'t0':32.4,'t1':42.8,'type':'ramp','dy':2.5},{'t0':96.4,'t1':104.0,'type':'ramp','dy':2.5},{'t0':118.0,'t1':127.8,'type':'ramp','dy':-2.5}],
 macro=[dict(t=1.0,diag='NE'),dict(t=42.927,diag='SE'),dict(t=64.26,diag='SW'),dict(t=104.0,diag='SE'),dict(t=110.5,diag='NE'),
        dict(t=131.0,diag='NW'),dict(t=134.0,diag='NE'),dict(t=137.5,diag='NW'),dict(t=140.0,diag='NE')])
