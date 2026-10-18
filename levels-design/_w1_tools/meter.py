import sys,json,numpy as np
from chartgen import load,win
s=sys.argv[1]; t0=float(sys.argv[2]); t1=float(sys.argv[3]); res=4
a,E=load(s); P=a['beat_period']; ph=a['grid_phase']
acc={k:np.zeros(4*res) for k in ['kick_on','snare_on','vocal_on','bass_on','mel_on']}; cnt=np.zeros(4*res)
n=int(np.ceil((t0-ph)/P*res))
while ph+n*P/res<t1:
    t=ph+n*P/res; p=n%(4*res); cnt[p]+=1
    for k in acc: acc[k][p]+=win(E[k],t,0.02)[0]
    n+=1
for k in acc: print('%-9s'%k,' '.join('%4.2f'%x for x in acc[k]/cnt))
