from common import *
B=lambda n:round(1.6699+1.77780*n,3)
def sw(t,a,b,k,j,n=8):
    """parallel switchback lanes: k taps along a, j taps sideways (b), k taps back along -a ..."""
    opp={'NE':'SW','SW':'NE','NW':'SE','SE':'NW'}
    pairs=[];counts=[]
    for i in range(n):
        pairs+= [a if i%2==0 else opp[a], b]; counts+=[k,j]
    return dict(t=t,mode='seq',pairs=pairs,counts=counts)
def make():
    L=Level('eta','ETA',[{'t':0,'v':10.0},{'t':B(75),'v':9.0}]); T=L.taps
    el=[dict(t=gap_near(T,6.9),type='fall',dy=-3),
        dict(t0=B(13),t1=B(19),type='ramp',dy=5),
        dict(t=gap_near(T,B(29),0.6),type='jump',dy=2.5),dict(t=gap_near(T,B(32),0.6),type='jump',dy=2.5),
        dict(t0=B(35),t1=B(43),type='ramp',dy=-4),
        dict(t0=B(43),t1=B(51),type='ramp',dy=12),
        dict(t=gap_near(T,B(58),0.3),type='fall',dy=-6),
        dict(t0=B(59),t1=B(67),type='ramp',dy=-6),
        dict(t=gap_near(T,B(71),0.44),type='fall',dy=-3)]
    S=[dict(t=0,prog=[dict(t=0,mode='seq',pairs=['NE','SE','NE'],counts=[5,3,99])],fix=(0,0)),
       dict(t=B(3),prog=[sw(B(3),'NE','NW',8,3)]),
       dict(t=B(11),prog=[dict(t=B(11),mode='stair',pair='NE'),dict(t=B(18),mode='serp',pairs=['NE','NW'],every=2)]),
       dict(t=B(19),prog=[dict(t=B(19),mode='rot',pair='NE',every=14,rot='R')]),
       dict(t=B(26),prog=[dict(t=B(26),mode='seq',pairs=['NE','SE'],counts=[3,9])]),
       dict(t=B(27),prog=[dict(t=B(27),mode='serp',pairs=['NE','SE'],every=4)]),
       dict(t=B(35),prog=[sw(B(35),'NE','NW',7,3)],want='cross'),
       dict(t=B(43),prog=[dict(t=B(43),mode='rot',pair='NE',every=8,rot='L')]),
       dict(t=B(51),prog=[dict(t=B(51),mode='seq',pairs=['NE','SE','NE'],counts=[16,9,99])],want='cross'),
       dict(t=B(58),prog=[dict(t=B(58),mode='seq',pairs=['NE','NW'],counts=[3,9])]),
       dict(t=B(59),prog=[dict(t=B(59),mode='rot',pair='NE',every=12,rot='L')]),
       dict(t=B(67),prog=[dict(t=B(67),mode='serp',pairs=['NE','NW'],every=2),dict(t=B(71),mode='stair',pair='NE')]),
       dict(t=B(75),prog=[dict(t=B(75),mode='seq',pairs=['NE','SE','NE'],counts=[4,3,9])])]
    L.plan(S,el,W=2.8)
    L.widths=[dict(t=0,w=2.8),dict(t=B(3),w=2.0),dict(t=B(11),w=2.4),dict(t=B(19),w=2.4),dict(t=B(27),w=2.2),dict(t=B(43),w=2.4),dict(t=B(51),w=2.1),dict(t=B(67),w=1.8),dict(t=B(75),w=2.6)]
    from configs import CONFIGS
    L.secs=[dict(t=0 if i==0 else B(s['bars'][0]),label=s['label'],kind=s['kind']) for i,s in enumerate(CONFIGS['eta']['sections'])]
    return L
if __name__=='__main__':
    L=make(); print('hits',len(L.hits),L.hits[:12]); print('passes',len(L.passes)); L.plot('route_draft.png')
