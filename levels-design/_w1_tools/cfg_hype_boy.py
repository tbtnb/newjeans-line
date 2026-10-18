D={'kick_on':1.0,'snare_on':0.8,'vocal_on':1.0,'bass_on':0.5}
V={'vocal_on':1.6,'kick_on':0.5,'snare_on':0.3,'mel_on':0.3}
I={'snare_on':0.8,'mel_on':0.8,'kick_on':0.6}
cfg=dict(bar_off=0,end=172.9,sections=[
 dict(t=0.0,label='Intro riff',kind='intro',dens=0.8,w=I,mingap=0.55,maxgap=2.5,res=2,met=2.0),
 dict(t=19.452,label='Verse 1',kind='verse',dens=1.55,w=D,mingap=0.29,res=4,add=[19.452]),
 dict(t=38.652,label='Pre-chorus 1',kind='pre',dens=1.0,w=V,mingap=0.29,res=4,maxgap=2.0,add=[38.652]),
 dict(t=48.252,label='Build 1',kind='pre',dens=1.6,w=D,mingap=0.29,res=2),
 dict(t=53.052,label='Chorus 1',kind='chorus',dens=2.1,w=D,mingap=0.29,res=4,add=[53.052]),
 dict(t=72.252,label='Post-chorus 1',kind='post',dens=1.8,w=D,mingap=0.29,res=4),
 dict(t=91.452,label='Verse 2',kind='verse',dens=1.55,w=D,mingap=0.29,res=4,add=[91.452]),
 dict(t=115.452,label='Pre-chorus 2',kind='pre',dens=1.0,w=V,mingap=0.29,res=4,maxgap=2.0,add=[115.452]),
 dict(t=125.052,label='Build 2',kind='pre',dens=1.7,w=D,mingap=0.29,res=2),
 dict(t=129.852,label='Chorus 2',kind='chorus',dens=2.1,w=D,mingap=0.29,res=4,add=[129.852]),
 dict(t=149.052,label='Final chorus',kind='chorus',dens=2.45,w=D,mingap=0.29,res=4),
 dict(t=170.652,label='Outro',kind='outro',dens=0.6,w=V,mingap=0.4,res=2),
])
route=dict(speed=[{'t':0,'v':9.0}],W=2.2,
 elev=[{'t0':38.8,'t1':52.9,'type':'ramp','dy':3},{'t0':125.1,'t1':135.0,'type':'ramp','dy':3}],
 macro=[dict(t=1.0,diag='NE'),dict(t=53.05,diag='SE'),dict(t=55.4,diag='SW'),dict(t=60.2,diag='SE'),dict(t=66.0,diag='NE'),dict(t=70.0,diag='SE'),
        dict(t=93.8,diag='NE'),dict(t=99.0,diag='SE'),dict(t=105.0,diag='SW'),
        dict(t=149.05,diag='NW'),dict(t=155.0,diag='SW'),dict(t=157.3,diag='NW'),dict(t=162.0,diag='SW'),dict(t=164.3,diag='NW')])
