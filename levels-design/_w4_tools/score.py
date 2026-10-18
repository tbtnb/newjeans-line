import numpy as np, json, sys
slug=sys.argv[1]; sub=int(sys.argv[2]) if len(sys.argv)>2 else 4
z=np.load(f'{slug}.env.npz'); fps=float(z['sr'])/float(z['hop'])
g=json.load(open(f'{slug}.grid.json')); P=g['period']; t0=g['t0']
def norm(e): return e/(np.percentile(e,99.5)+1e-9)
E={k:norm(z[k]) for k in ['kick','snare','hat','bass','vocal','all']}
rms=z['rms']
def val(k,t,w=0.03):
    a=max(0,int((t-w)*fps)); b=int((t+w)*fps)+1
    return float(E[k][a:b].max()) if b>a else 0
dur=len(rms)/fps
nb=int((dur-t0)/P)
# downbeat phase: snare on beats 2,4 -> phase where beats (phase+1, phase+3) have most snare
sn=np.array([val('snare',t0+i*P) for i in range(nb)]); kk=np.array([val('kick',t0+i*P) for i in range(nb)])
sc=[sn[(np.arange(nb)%4)==(ph+1)%4].mean()+sn[(np.arange(nb)%4)==(ph+3)%4].mean()+kk[(np.arange(nb)%4)==ph].mean() for ph in range(4)]
ph=int(np.argmax(sc)); print('phase scores',np.round(sc,2),'downbeat phase',ph)
g['phase']=ph; json.dump(g,open(f'{slug}.grid.json','w'))
start=t0+ph*P - 4*P*(1 if ph*P+t0>4*P else 0)
while start-4*P>-0.01: start-=4*P
bar=0;t=start
print('legend: K kick S snare/clap X both v vocal-onset b bass h hat . none ; uppercase strong')
while t<dur:
    s=''
    for j in range(4*sub):
        tt=t+j*P/sub
        k,sn_,v,b,h=val('kick',tt),val('snare',tt),val('vocal',tt),val('bass',tt),val('hat',tt)
        c='.'
        if k>0.45 and sn_>0.45: c='X'
        elif k>0.45: c='K'
        elif sn_>0.45: c='S'
        elif v>0.45: c='v'
        elif b>0.45: c='b'
        elif k>0.3: c='k'
        elif sn_>0.3: c='s'
        elif h>0.4: c='h'
        if j%sub==0: s+='|'
        s+=c
    r=rms[int(t*fps):int((t+4*P)*fps)].mean() if t>=0 else 0
    print(f'{bar:3d} {t:7.3f} {s} {"#"*int(r*40)}')
    bar+=1; t+=4*P
