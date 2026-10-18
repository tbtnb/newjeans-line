import json,numpy as np,librosa,scipy.signal as ss
for s in ['supernatural','how-sweet','bubble-gum','right-now']:
    y,sr=librosa.load(f'/workspace/nj-design-w4/public/audio/{s}.mp3',sr=44100)
    g=json.load(open(f'{s}.grid.json')); P=g['period']; t0=g['t0']
    out=[]
    for lo,hi in [(1500,10000),(60,200)]:
        b,a=ss.butter(4,[lo/(sr/2),hi/(sr/2)],'band'); x=ss.filtfilt(b,a,y)
        e=np.sqrt(ss.filtfilt(*ss.butter(2,(300 if lo>500 else 60)/(sr/2)),x*x).clip(0))
        de=np.diff(e)
        dd=[];dp=[]
        for k in range(int((len(y)/sr-t0)/P)):
            t=t0+k*P; i0=int((t-0.06)*sr); i1=int((t+0.06)*sr)
            if i0<0 or i1>=len(de): continue
            seg=de[i0:i1]; j=np.argmax(seg)
            if seg[j]<5*np.median(np.abs(seg))+1e-9: continue
            dd.append((i0+j)/sr-t)
            dp.append((i0+np.argmax(e[i0:i1]))/sr-t)
        out.append((f'{lo}-{hi}Hz',len(dd),'maxslope ms',round(np.median(dd)*1000,1),'peak ms',round(np.median(dp)*1000,1)))
    print(s,out)
