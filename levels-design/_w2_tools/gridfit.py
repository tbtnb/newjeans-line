import json,sys,numpy as np,librosa
SR=22050;HOP=128
s=sys.argv[1]; lo,hi=float(sys.argv[2]),float(sys.argv[3])
d=json.load(open(f'/workspace/w2-work/{s}.json'))
y,_=librosa.load(f'/workspace/w2-stems/htdemucs/{s}/drums.wav',sr=SR)
env=librosa.onset.onset_strength(y=y,sr=SR,hop_length=HOP); env/=env.max(); dur=d['duration']
fps=SR/HOP
best=None
for bpm in np.arange(lo,hi,0.01):
    T=60/bpm
    for ph in np.arange(0,T,0.004):
        g=np.arange(ph,dur,T/2); fr=(g*fps).astype(int); fr=fr[fr<len(env)]
        sc=env[fr].mean()
        if best is None or sc>best[0]: best=(sc,bpm,ph)
print(s,best)
sc,bpm,ph=best; T=60/bpm
# local residuals per 20 s window: best phase offset
for w0 in range(0,int(dur),20):
    bo=None
    for off in np.arange(-0.04,0.0401,0.002):
        g=np.arange(ph+off,dur,T/2); g=g[(g>=w0)&(g<w0+20)]; fr=(g*fps).astype(int); fr=fr[fr<len(env)]
        if len(fr)==0: continue
        v=env[fr].mean()
        if bo is None or v>bo[0]: bo=(v,off)
    print(w0, bo and round(bo[1]*1000), bo and round(bo[0],3))
