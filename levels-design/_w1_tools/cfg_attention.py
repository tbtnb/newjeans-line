V={'vocal_on':1.6,'snare_on':0.4,'kick_on':0.5,'mel_on':0.3,'bass_on':0.3}
C={'vocal_on':1.4,'kick_on':0.8,'snare_on':0.6,'bass_on':0.5,'mel_on':0.2}
cfg=dict(bar_off=0,end=174.2,sections=[
 dict(t=0.0,label='Intro',kind='intro',dens=0.5,w={'vocal_on':1.0,'mel_on':0.5},mingap=0.55,maxgap=3.0,res=2),
 dict(t=9.607,label='Hook A',kind='chorus',dens=1.7,w=C,mingap=0.27,res=2,add=[10.178]),
 dict(t=27.893,label='Verse 1',kind='verse',dens=1.0,w=V,mingap=0.27,res=2,maxgap=2.0,add=[27.893]),
 dict(t=46.75,label='Pre-chorus 1',kind='pre',dens=1.4,w=V,mingap=0.27,res=2),
 dict(t=62.18,label='Chorus 1',kind='chorus',dens=2.1,w=C,mingap=0.27,res=2,add=[62.18]),
 dict(t=83.32,label='Verse 2',kind='verse',dens=1.0,w=V,mingap=0.27,res=2,maxgap=2.0,add=[83.32]),
 dict(t=101.6,label='Pre-chorus 2',kind='pre',dens=1.45,w=V,mingap=0.27,res=2),
 dict(t=117.03,label='Chorus 2',kind='chorus',dens=2.15,w=C,mingap=0.27,res=2,add=[117.03]),
 dict(t=137.6,label='Final chorus',kind='chorus',dens=2.3,w=C,mingap=0.27,res=2),
 dict(t=156.1,label='Outro',kind='outro',dens=1.0,w=V,mingap=0.27,res=2,maxgap=2.5,add=[156.17]),
])
route=dict(speed=[{'t':0,'v':9.0}],W=2.2,
 elev=[{'t0':46.9,'t1':61.9,'type':'ramp','dy':4},{'t0':101.7,'t1':116.8,'type':'ramp','dy':4}],
 macro=[dict(t=1.0,diag='NE'),dict(t=46.75,diag='SE'),
        dict(t=64.4,diag='SW'),dict(t=69.0,diag='SE'),dict(t=76.4,diag='NE'),dict(t=81.0,diag='SE'),
        dict(t=83.32,diag='SW'),dict(t=127.3,diag='NW'),
        dict(t=140.4,diag='NE'),dict(t=142.6,diag='NW'),dict(t=144.0,diag='SW'),dict(t=146.4,diag='NW'),
        dict(t=148.6,diag='NE'),dict(t=150.8,diag='NW'),dict(t=152.2,diag='SW'),dict(t=154.4,diag='NW'),
        dict(t=156.1,diag='SW')])
