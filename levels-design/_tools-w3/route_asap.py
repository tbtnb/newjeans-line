from common import *
B=lambda n:round(0.341+1.84598*n,3)
def make():
    L=Level('asap','ASAP',[{'t':0,'v':8.5}]); T=L.taps
    el=[dict(t0=B(20),t1=B(22),type='ramp',dy=3.5),
        dict(t=gap_near(T,56.70,0.45),type='fall',dy=-3.5),
        dict(t0=B(43),t1=B(46),type='ramp',dy=7),
        dict(t0=B(50),t1=B(52),type='ramp',dy=-3.5),
        dict(t=gap_near(T,B(62.3),0.9),type='fall',dy=-3.5),
        dict(t0=B(65),t1=B(68),type='ramp',dy=7)]
    S=[dict(t=0,prog=[dict(t=0,mode='stair',pair='NE')],fix=(0,0)),
       dict(t=B(2),prog=[dict(t=B(2),mode='seq',pairs=['NE','NW','NE'],counts=[3,2,99])]),
       dict(t=B(6),prog=[dict(t=B(6),mode='rot',pair='NE',every=2,rot='R')],alts=[[dict(t=B(6),mode='rot',pair='NE',every=3,rot='R')],[dict(t=B(6),mode='rot',pair='NE',every=2,rot='L')],[dict(t=B(6),mode='serp',pairs=['NE','SE'],every=3)]]),
       dict(t=B(14),prog=[sw(B(14),'NE','NW',2,1)],alts=[[sw(B(14),'NE','NW',3,1)],[sw(B(14),'NE','NW',2,2)],[dict(t=B(14),mode='serp',pairs=['NE','NW'],every=4)],[dict(t=B(14),mode='serp',pairs=['NE','NW'],every=2)],[dict(t=B(14),mode='stair',pair='NE')]]),
       dict(t=B(22),prog=[dict(t=B(22),mode='rot',pair='NE',every=8,rot='L')],alts=[[dict(t=B(22),mode='rot',pair='NE',every=9,rot='R')]]),
       dict(t=B(30),prog=[dict(t=B(30),mode='stair',pair='NE')]),
       dict(t=B(31),prog=[dict(t=B(31),mode='serp',pairs=['NE','NW'],every=3)],alts=[[dict(t=B(31),mode='serp',pairs=['NE','SE'],every=4)]],want='cross'),
       dict(t=B(39),prog=[dict(t=B(39),mode='serp',pairs=['NE','NW'],every=4),dict(t=B(43),mode='rot',pair='NE',every=4,rot='R')],alts=[[dict(t=B(39),mode='rot',pair='NE',every=6,rot='R')]]),
       dict(t=B(47),prog=[dict(t=B(47),mode='rot',pair='NE',every=2,rot='L')],alts=[[dict(t=B(47),mode='stair',pair='NE')]]),
       dict(t=B(50),prog=[dict(t=B(50),mode='rot',pair='NE',every=12,rot='R')],alts=[[dict(t=B(50),mode='rot',pair='NE',every=10,rot='L')]],want='cross'),
       dict(t=B(62),prog=[dict(t=B(62),mode='rot',pair='NE',every=1,rot='R')],alts=[[dict(t=B(62),mode='stair',pair='NE')]]),
       dict(t=B(65),prog=[dict(t=B(65),mode='seq',pairs=['NE','SE','NE','NW'],counts=[4,3,5,99])],alts=[[dict(t=B(65),mode='rot',pair='NE',every=5,rot='R')]],want='cross'),
       dict(t=B(70),prog=[dict(t=B(70),mode='stair',pair='NE')])]
    L.plan(S,el,W=2.8)
    L.widths=[dict(t=0,w=2.8),dict(t=B(6),w=2.6),dict(t=B(14),w=2.0),dict(t=B(22),w=2.4),dict(t=B(31),w=2.2),dict(t=B(39),w=2.0),dict(t=B(50),w=2.4),dict(t=B(65),w=2.1),dict(t=B(70),w=2.8)]
    L.secs=secs_from('asap',B)
    return L
if __name__=='__main__':
    L=make(); print('hits',len(L.hits),L.hits[:12]); print('passes',len(L.passes)); L.plot('route_draft.png')
