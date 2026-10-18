from common import *
B=lambda n:round(0.3344+1.77784*n,3)
def make():
    L=Level('cool-with-you','Cool With You',[{'t':0,'v':8.5}]); T=L.taps
    el=[dict(t=gap_near(T,B(24),0.6),type='fall',dy=-3),
        dict(t0=B(32),t1=B(36),type='ramp',dy=6),
        dict(t=gap_near(T,B(48),0.8),type='fall',dy=-3),
        dict(t=gap_near(T,B(55.5),0.4),type='jump',dy=3),
        dict(t0=B(56),t1=B(64),type='ramp',dy=6),
        dict(t0=B(64),t1=B(72),type='ramp',dy=-6),
        dict(t0=B(72),t1=B(76),type='ramp',dy=-3)]
    S=[dict(t=0,prog=[dict(t=0,mode='seq',pairs=['NE','SE','SW','SE','NE'],counts=[2,1,1,1,99])],fix=(0,0)),
       dict(t=B(8),prog=[dict(t=B(8),mode='rot',pair='NE',every=8,rot='R')],alts=[[dict(t=B(8),mode='rot',pair='NE',every=7,rot='L')]]),
       dict(t=B(16),prog=[sw(B(16),'NE','NW',6,3)],alts=[[sw(B(16),'NE','NW',4,3)],[sw(B(16),'NE','NW',7,4)]]),
       dict(t=B(24),prog=[dict(t=B(24),mode='rot',pair='NE',every=4,rot='R')],alts=[[dict(t=B(24),mode='rot',pair='NE',every=5,rot='R')],[dict(t=B(24),mode='rot',pair='NE',every=3,rot='R')]],want='cross'),
       dict(t=B(32),prog=[dict(t=B(32),mode='rot',pair='NE',every=12,rot='L')]),
       dict(t=B(40),prog=[dict(t=B(40),mode='serp',pairs=['NE','NW'],every=6)]),
       dict(t=B(48),prog=[dict(t=B(48),mode='rot',pair='NE',every=2,rot='R')],alts=[[dict(t=B(48),mode='rot',pair='NE',every=2,rot='L')]]),
       dict(t=B(52),prog=[dict(t=B(52),mode='stair',pair='NE'),dict(t=B(55),mode='serp',pairs=['NE','NW'],every=2)]),
       dict(t=B(56),prog=[dict(t=B(56),mode='rot',pair='NE',every=5,rot='R')],alts=[[dict(t=B(56),mode='rot',pair='NE',every=4,rot='R')],[dict(t=B(56),mode='rot',pair='NE',every=7,rot='R')]],want='cross'),
       dict(t=B(64),prog=[dict(t=B(64),mode='rot',pair='NE',every=15,rot='L')],alts=[[dict(t=B(64),mode='seq',pairs=['NE','SE','NE','SE'],counts=[12,8,12,99])]]),
       dict(t=B(72),prog=[dict(t=B(72),mode='rot',pair='NE',every=2,rot='R')])]
    L.plan(S,el,W=2.8)
    L.widths=[dict(t=0,w=2.8),dict(t=B(8),w=2.4),dict(t=B(16),w=2.0),dict(t=B(24),w=2.6),dict(t=B(32),w=2.4),dict(t=B(40),w=2.2),dict(t=B(48),w=2.6),dict(t=B(52),w=2.0),dict(t=B(56),w=2.2),dict(t=B(64),w=1.9),dict(t=B(72),w=2.8)]
    L.secs=secs_from('cool-with-you',B)
    return L
if __name__=='__main__':
    L=make(); print('hits',len(L.hits),L.hits[:12]); print('passes',len(L.passes)); L.plot('route_draft.png')
