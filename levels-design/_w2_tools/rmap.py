# print per-bar 16th-step onset maps: usage rmap.py slug [bar_offset_beats] [from_bar] [to_bar]
import json,sys,numpy as np
s=sys.argv[1]; d=json.load(open(f'/workspace/w2-work/{s}.json'))
off=int(sys.argv[2]) if len(sys.argv)>2 else 0
T=d['beat_period']; b0=d['beat0']+off*T; dur=d['duration']
nb=int((dur-b0)/(4*T))+1
fb=int(sys.argv[3]) if len(sys.argv)>3 else 0; tb=int(sys.argv[4]) if len(sys.argv)>4 else nb
def grid(key,thr):
    g=np.zeros((nb,16))
    for t,st in d.get(key,[]):
        if st<thr: continue
        x=(t-b0)/(T/4); i=int(round(x))
        if abs(x-i)<0.3 and 0<=i<nb*16: g[i//16,i%16]=max(g[i//16,i%16],st)
    return g
keys=[('kick','K',0.25),('snare','S',0.25),('bass','B',0.2),('vocals','V',0.15),('other','O',0.2)]
G={k:grid(k,th) for k,_,th in keys}
mix=d['beat_rms']['mix']
print('bar  time   | K:kick S:snare B:bass V:vocal O:other  (16 steps, | = beat)  rms')
for b in range(fb,min(tb,nb)):
    line=[]
    for k,c,_ in keys:
        if k not in d: continue
        row=''.join((c if G[k][b,i]>0.5 else c.lower() if G[k][b,i]>0 else '.')+('|' if i%4==3 and i<15 else '') for i in range(16))
        line.append(row)
    bi=off+b*4; r=np.mean(mix[bi:bi+4]) if bi<len(mix) else 0
    print(f'{b:3d} {b0+b*4*T:7.2f} '+'  '.join(line)+f'  {r:.3f}')
