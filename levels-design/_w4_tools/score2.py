import numpy as np, json, sys
slug=sys.argv[1]; sub=4; b0=int(sys.argv[2]) if len(sys.argv)>2 else 0; b1=int(sys.argv[3]) if len(sys.argv)>3 else 999
z=np.load(f'{slug}.env.npz'); fps=float(z['sr'])/float(z['hop'])
g=json.load(open(f'{slug}.grid.json')); P=g['period']; t0=g['t0']; ph=g['phase']
rms=z['rms']; dur=len(rms)/fps
start=t0+ph*P
while start-4*P>-0.01: start-=4*P
g['bar0']=start; json.dump(g,open(f'{slug}.grid.json','w'))
def val(e,t,w=0.025):
    a=max(0,int((t-w)*fps)); b=min(len(e),int((t+w)*fps)+1)
    return float(e[a:b].max()) if b>a else 0
nbars=int((dur-start)/(4*P))+1
rows={}
for k in ['kick','snare','vocal','bass']:
    e=z[k]; M=np.array([[val(e,start+(bi*16+j)*P/4) for j in range(16)] for bi in range(nbars)])
    # local normalisation over 4-bar window
    out=np.zeros_like(M)
    for bi in range(nbars):
        w=M[max(0,bi-2):bi+2]; lo=np.median(w); hi=np.percentile(w,97)
        out[bi]=np.clip((M[bi]-lo)/(hi-lo+1e-9),0,0.999)
    rows[k]=out
print(slug,'bar0',round(start,3),'beat',round(P,4))
for bi in range(max(0,b0),min(nbars,b1)):
    t=start+bi*16*P/4
    r=rms[int(max(0,t)*fps):int((t+4*P)*fps)]; r=r.mean() if len(r) else 0
    line=f'{bi:3d} {t:7.2f} {int(r*100):2d} '
    for k,c in [('kick','K'),('snare','S'),('vocal','V'),('bass','B')]:
        q=''.join(('|' if j%4==0 else '')+(str(int(rows[k][bi,j]*10)) if rows[k][bi,j]>=0.3 else '.') for j in range(16))
        line+=f'{c}{q} '
    print(line)
