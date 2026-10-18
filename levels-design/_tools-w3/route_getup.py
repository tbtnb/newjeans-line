from common import *
B=lambda n:round(0.335+1.99963*n,3)
def make():
    L=Level('get-up','Get Up',[{'t':0,'v':7.5}]); T=L.taps
    el=[dict(t0=B(8),t1=B(11.5),type='ramp',dy=3.5),
        dict(t=gap_near(T,B(13.9),0.8),type='fall',dy=-3.5)]
    S=[dict(t=0,prog=[dict(t=0,mode='seq',pairs=['NE','SE','NE'],counts=[3,2,99])],alts=[[dict(t=0,mode='seq',pairs=['NE','SE','SW'],counts=[2,1,99])],[dict(t=0,mode='stair',pair='NE')]]),
       dict(t=B(4),prog=[dict(t=B(4),mode='serp',pairs=['NE','NW'],every=3)],alts=[[dict(t=B(4),mode='serp',pairs=['NE','NW'],every=2)]]),
       dict(t=B(8),prog=[sw(B(8),'NE','NW',3,1)],alts=[[sw(B(8),'NE','NW',4,1)],[sw(B(8),'NE','NW',3,2)]],want='cross'),
       dict(t=B(12),prog=[dict(t=B(12),mode='rot',pair='NE',every=2,rot='R')],alts=[[dict(t=B(12),mode='rot',pair='NE',every=1,rot='R')],[dict(t=B(12),mode='rot',pair='NE',every=3,rot='L')]],want='cross'),
       dict(t=B(16),prog=[dict(t=B(16),mode='stair',pair='NE')])]
    L.plan(S,el,W=2.8)
    L.widths=[dict(t=0,w=2.8),dict(t=B(4),w=2.0),dict(t=B(8),w=2.4),dict(t=B(12),w=2.6),dict(t=B(16),w=2.8)]
    L.secs=secs_from('get-up',B)
    return L
if __name__=='__main__':
    L=make(); print('hits',len(L.hits),L.hits[:12]); print('passes',len(L.passes)); L.plot('route_draft.png')
