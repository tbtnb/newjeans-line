import json,numpy as np,librosa,scipy.signal as ss,sys
s=sys.argv[1]
y,sr=librosa.load(f'/workspace/nj-design-w4/public/audio/{s}.mp3',sr=44100)
raw=json.load(open(f'{s}.chart.raw.json'))
env={}
for name,(lo,hi,lp) in {'hi':(1500,10000,300),'lo':(40,180,80),'mid':(300,3000,150)}.items():
    b,a=ss.butter(4,[lo/(sr/2),hi/(sr/2)],'band'); x=ss.filtfilt(b,a,y)
    e=np.sqrt(ss.filtfilt(*ss.butter(2,lp/(sr/2)),x*x).clip(0)); env[name]=np.diff(e)
res=[]
for r in raw['taps']:
    t=r['t']; band={'kick':'lo','bass':'lo','vocal':'mid','melody':'mid'}.get(r['tag'],'hi')
    de=env[band]; i0=int((t-0.06)*sr); i1=int((t+0.06)*sr); seg=de[i0:i1]
    j=int(np.argmax(seg)); sal=seg[j]/(np.median(np.abs(de[max(0,i0-sr):i1+sr]))+1e-12)
    off=round(((i0+j)/sr-t)*1000,1) if sal>8 else None
    res.append({'t':t,'tag':r['tag'],'band':band,'offset_ms':off,'salience':round(float(sal),1),'sec':r['sec']})
json.dump(res,open(f'{s}.offsets.json','w'))
o=np.array([x['offset_ms'] for x in res if x['offset_ms'] is not None])
print(s,'measured',len(o),'/',len(res),'median',np.median(o),'median|.|',np.median(np.abs(o)),'p90|.|',np.percentile(np.abs(o),90))
