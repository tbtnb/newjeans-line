"""Semi-automatic chart builder. Per-section rhythmic vocabulary + density are hand-set in specs/<slug>.py;
the audio (demucs stems: drums kick/snare, vocals, other, bass) scores every 8th-note slot; for each bar the best
template from the section's allowed vocabulary is chosen (with phrase-level repetition/variation rules); then the
hand edits in the spec (add/remove/override) are applied. Output: chart.json + stats."""
import numpy as np, json, sys, importlib.util
slug=sys.argv[1]
spec_p=f'/workspace/w4/specs/{slug.replace("-","_")}.py'
sp=importlib.util.spec_from_file_location('spec',spec_p); S=importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
z=np.load(f'/workspace/w4/{slug}.stems.npz'); fps=22050/256
g=json.load(open(f'/workspace/w4/{slug}.grid.json')); P=g['period']; bar0=g['bar0']
def win(e,t,w=0.035):
    a=max(0,int((t-w)*fps)); b=min(len(e),int((t+w)*fps)+1)
    return float(e[a:b].max()) if b>a else 0.0
N={k:z[k]/(np.percentile(z[k],99.0)+1e-9) for k in ['kick','snare','hat','vocal','bass','other']}
# local contrast: divide by running 2-bar 90th pct to see accents inside quiet parts
STEM_LAG=0.050  # demucs output latency 25 ms + onset_strength centring lag ~25 ms (measured)
def slot_feats(bar,slot):
    t=tslot(bar,slot)+STEM_LAG; return {k:min(1.5,win(N[k],t)) for k in N}
SUB=getattr(S,'SUB',16)          # grid subdivisions per bar
U=4*P/SUB
def tslot(bar,slot): return bar0+bar*4*P+slot*U
MINSL=int(np.ceil(getattr(S,'MIN_GAP',0.15)/U-1e-6))   # min slots between taps
M16=[0.30,-0.25,0.0,-0.2, 0.18,-0.25,0.0,-0.2, 0.25,-0.25,0.0,-0.2, 0.18,-0.25,0.0,-0.2]
METRIC=getattr(S,'METRIC',M16 if SUB==16 else [M16[i*2] for i in range(8)])
masks=[]
for m in range(1<<SUB):
    sl=[i for i in range(SUB) if m>>i&1]
    if all(b-a>=MINSL for a,b in zip(sl,sl[1:])):
        r=1;mr=1 if sl else 0
        for a,b in zip(sl,sl[1:]):
            r=r+1 if b-a==MINSL and U*MINSL<0.2 else 1; mr=max(mr,r)
        masks.append((m,np.array([(m>>i)&1 for i in range(SUB)]),mr))
print('masks',len(masks),'unit',round(U,4),'minslots',MINSL)
def score_bar(bar,w):
    sc=[]
    for s_ in range(SUB):
        f=slot_feats(bar,s_); sc.append(sum(w.get(k,0)*f[k] for k in f)+METRIC[s_])
    return np.array(sc)
def pat(s_): return np.array([int(c) for c in s_])
taps=[]; sections=[]; choice_log=[]; lastpat={}
carry=None  # last tap slot from previous bar (for cross-bar gap)
for sec in S.SECTIONS:
    b0,b1,label,kind=sec['bars'][0],sec['bars'][1],sec['label'],sec['kind']
    sections.append({'t':round(tslot(b0,0),3),'label':label,'kind':kind})
    w=sec.get('w',{'kick':1,'snare':1,'vocal':0.6,'other':0.4,'bass':0.3}); tgt=sec['tpb']
    lam=sec.get('lam',0.06); rep=sec.get('rep',0.25)
    plan=sec.get('plan',{})
    hist=[]
    allsc=np.concatenate([score_bar(b,w) for b in range(b0,b1)])
    srt=np.sort(allsc)
    def rank(x): return np.searchsorted(srt,x)/len(srt)
    tau=sec.get('tau',1-tgt/SUB*1.15)
    for bi,bar in enumerate(range(b0,b1)):
        if bi in plan or (bar-b0-len(plan)) in ():
            p=pat(plan[bi]); name='plan'
        else:
            sc=rank(score_bar(bar,w))
            best=None
            ref2=hist[-2] if len(hist)>=2 else None
            for m,p_,mr in masks:
                if mr>sec.get('maxrun',99): continue
                n=p_.sum()
                v=float(((sc-tau)*p_).sum())-lam*abs(n-tgt)
                if ref2 is not None and bi%4 in (1,2,3) and bi%2==0: v+=rep*(1-np.abs(p_-ref2).sum()/max(1,(p_+ref2).sum()))*n/max(1,tgt)
                if carry is not None and p_.argmax()+SUB-carry<MINSL and n>0: v-=99
                if best is None or v>best[0]: best=(v,p_)
            p=best[1]; name=''.join(map(str,p))
        hist.append(p)
        idx=np.nonzero(p)[0]
        carry=idx[-1] if len(idx) else -99
        choice_log.append((bar,label,''.join(map(str,p))))
        for s_ in idx: taps.append([round(tslot(bar,int(s_)),3),bar,int(s_),label])
# hand edits
rm=set(tuple(x) for x in getattr(S,'REMOVE',[]))
taps=[t for t in taps if (t[1],t[2]) not in rm]
for bar,s in getattr(S,'ADD',[]):
    lab=[sec['label'] for sec in S.SECTIONS if sec['bars'][0]<=bar<sec['bars'][1]]
    taps.append([round(tslot(bar,s),3),bar,s,lab[0] if lab else '?'])
taps.sort()
# dedupe
out=[];
for t in taps:
    if out and abs(t[0]-out[-1][0])<1e-3: continue
    out.append(t)
taps=out
# tag by dominant feature, measure nearest onset offset within 60ms on tagged stem
on=json.load(open(f'/workspace/w4/{slug}.stem_onsets.json'))
def tag_of(bar,s):
    f=slot_feats(bar,s); cand={'kick':f['kick'],'snare':f['snare']*1.0,'vocal':f['vocal']*0.9,'melody':f['other']*0.8,'bass':f['bass']*0.7}
    k=max(cand,key=cand.get)
    return (k if cand[k]>0.3 else 'phrase'), cand[k]
res=[]
dirs=getattr(S,'DIRS',{})
for t,bar,s,lab in taps:
    tg,st=tag_of(bar,s)
    stem={'kick':'kick','snare':'snare','vocal':'vocal','melody':'other','bass':'bass'}.get(tg,'kick')
    near=[o[0] for o in on[stem] if abs(o[0]-t)<0.06]
    off=round((min(near,key=lambda o:abs(o-t))-t)*1000) if near else None
    d={'t':t,'tag':'clap' if tg=='snare' else tg,'bar':bar,'slot8':s,'sec':lab,'onsetOffsetMs':off}
    res.append(d)
ts=[r['t'] for r in res]
gaps=np.diff(ts)
json.dump({'taps':res,'sections':sections,'choices':choice_log},open(f'/workspace/w4/{slug}.chart.raw.json','w'))
print(slug,'taps',len(ts),'min gap',round(gaps.min(),3))
for sec in S.SECTIONS:
    a,b=tslot(sec['bars'][0],0),tslot(sec['bars'][1],0)
    n=sum(1 for t in ts if a<=t<b); print(f"  {sec['label']:<14} bars {sec['bars'][0]:3d}-{sec['bars'][1]:3d} {a:7.2f}-{b:7.2f} taps {n:3d} dens {n/(b-a):.2f}/s  ",' '.join(c[2] for c in choice_log if c[1]==sec['label']))
