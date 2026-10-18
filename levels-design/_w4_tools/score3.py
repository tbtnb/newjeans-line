import numpy as np, json, sys
slug=sys.argv[1]; b0=int(sys.argv[2]) if len(sys.argv)>2 else 0; b1=int(sys.argv[3]) if len(sys.argv)>3 else 999
z=np.load(f'{slug}.stems.npz'); fps=22050/256
g=json.load(open(f'{slug}.grid.json')); P=g['period']; start=g['bar0']
dur=len(z['vocal_rms'])/fps
def val(e,t,w=0.03):
    a=max(0,int((t-w)*fps)); b=min(len(e),int((t+w)*fps)+1)
    return float(e[a:b].max()) if b>a else 0
nbars=int((dur-start)/(4*P))+1
rows={}
for k in ['kick','snare','vocal','other','bass']:
    e=z[k]/(np.percentile(z[k],99.5)+1e-9)
    rows[k]=np.array([[val(e,start+(bi*16+j)*P/4) for j in range(16)] for bi in range(nbars)])
vr=z['vocal_rms']/np.percentile(z['vocal_rms'],99); drr=z['drums_rms']/np.percentile(z['drums_rms'],99); orr=z['other_rms']/np.percentile(z['other_rms'],99); br=z['bass_rms']/np.percentile(z['bass_rms'],99)
print(slug,'bar0',round(start,3),'beat',round(P,4),' cols: vox drm oth bas levels(0-9)')
for bi in range(max(0,b0),min(nbars,b1)):
    t=start+bi*4*P
    sl=slice(int(max(0,t)*fps),int((t+4*P)*fps))
    lv=''.join(str(min(9,int(np.mean(x[sl])*10))) if len(x[sl]) else '0' for x in (vr,drr,orr,br))
    line=f'{bi:3d} {t:7.2f} {lv} '
    for k,c in [('kick','K'),('snare','S'),('vocal','V'),('other','O')]:
        q=''.join(('|' if j%4==0 else '')+(str(min(9,int(rows[k][bi,j]*10))) if rows[k][bi,j]>=0.25 else '.') for j in range(16))
        line+=f'{c}{q} '
    print(line)
