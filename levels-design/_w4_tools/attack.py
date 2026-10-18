import json,numpy as np,librosa,scipy.signal as ss,sys
for s in ['supernatural','how-sweet','bubble-gum','right-now']:
    y,sr=librosa.load(f'/workspace/nj-design-w4/public/audio/{s}.mp3',sr=22050)
    g=json.load(open(f'{s}.grid.json')); P=g['period']; t0=g['t0']
    res={}
    for name,(lo,hi) in {'low':(30,150),'high':(2000,8000)}.items():
        b,a=ss.butter(4,[lo/(sr/2),hi/(sr/2)],'band'); e=np.abs(ss.hilbert(ss.filtfilt(b,a,y)))
        e=ss.filtfilt(*ss.butter(2,200/(sr/2)),e)
        d=[]
        for k in range(int((len(y)/sr-t0)/P)):
            t=t0+k*P; i0=int((t-0.08)*sr); i1=int((t+0.08)*sr)
            if i0<0 or i1>=len(e): continue
            seg=e[i0:i1]; base=seg[:int(0.03*sr)].mean(); pk=seg.max()
            if pk<3*base or pk<0.05: continue
            j=np.argmax(seg>base+0.5*(pk-base)); d.append((i0+j)/sr-t)
        res[name]=(len(d),round(np.median(d)*1000,1) if d else None)
    print(s,'mix attack(50% rise) - grid ms:',res)
