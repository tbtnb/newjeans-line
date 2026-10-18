"""Curated chart generator: per-section rules (hand-chosen density, sources, grid, min gap, manual add/remove)
select tap slots on the measured beat grid by audio salience; tap times refined to the actual onset peak."""
import json,sys,numpy as np
fps=22050/256
def load(s):
    a=json.load(open(f'{s}.analysis.json')); st=np.load(f'{s}.stems.npz'); env=np.load(f'{s}.env.npz')
    E={k:st[k] for k in ['vocal_on','kick_on','snare_on','mel_on','bass_on']}
    vr=st['vocal_rms']; lv=np.log(vr+1e-3); lv=np.convolve(lv,np.ones(3)/3,'same')
    d=np.maximum(0,lv[2:]-lv[:-2]); d=np.concatenate([[0],d,[0]])*(vr>np.percentile(vr,30))
    E['vocal_on']=d
    for k in E: E[k]=E[k]/(np.percentile(E[k],99.5)+1e-9)
    # htdemucs stems are 25.03 ms late vs ffmpeg/librosa/browser decode: shift stem envelopes earlier
    n=len(E['kick_on']); tt=np.arange(n)/fps
    for k in ['vocal_on','kick_on','snare_on','mel_on','bass_on']:
        E[k]=np.interp(tt+0.02503,tt,E[k])
    E['mix']=env['oenv'][:n]
    return a,E
def win(x,t,w=0.03):
    i0=max(0,int((t-w)*fps)); i1=min(len(x)-1,int((t+w)*fps)+1); seg=x[i0:i1+1]
    j=int(np.argmax(seg)); return float(seg[j]),(i0+j)/fps
def gen(s,cfg):
    a,E=load(s); P=a['beat_period']; ph=a['grid_phase']; dur=a['duration']
    secs=cfg['sections']; taps=[]; stats=[]
    for k,sec in enumerate(secs):
        t0=sec['t']; t1=secs[k+1]['t'] if k+1<len(secs) else cfg.get('end',dur-1.0)
        res=sec.get('res',2); w=sec['w']; mg=sec.get('mingap',0.27); maxgap=sec.get('maxgap',3.0)
        n0=int(np.ceil((t0-ph)/P*res-1e-6)); n1=int(np.floor((t1-ph)/P*res-1e-6))
        cands=[]
        for n in range(n0,n1+1):
            t=ph+n*P/res
            if t<t0-1e-6 or t>=t1-0.05 or t<1.0 or t>dur-1.0: continue
            pos=(n-cfg.get('bar_off',0)*res)%(4*res)
            met=0.18 if pos==0 else 0.12 if pos%res==0 and (pos//res)%2==0 else 0.08 if pos%res==0 else 0.03 if res>=2 and pos%(res//2 if res>=4 else 1)==0 else 0.0
            sal=0; best=(0,t); src='beat'
            for key,wt in w.items():
                v,tt=win(E[key],t)
                if v*wt>best[0]: best=(v*wt,tt); src=key
                sal+=v*wt
            cands.append(dict(n=n,t=t,sal=sal+met*sec.get('met',1.0),src=src,tpk=best[1],pos=pos))
        target=int(round(sec['dens']*(t1-t0)))
        for c in cands:
            if any(abs(c['t']-x)<0.02 for x in sec.get('remove',[])): c['sal']=-9
            if any(abs(c['t']-x)<0.03 for x in sec.get('add',[])): c['sal']+=9
        chosen=[]
        for c in sorted(cands,key=lambda c:-c['sal']):
            if len(chosen)>=target: break
            if c['sal']<0: continue
            if all(abs(c['t']-x['t'])>=mg-1e-6 for x in chosen+taps[-1:]):
                mr=sec.get('maxrun',99); fg=sec.get('fastgap',0.25)
                ts=sorted([x['t'] for x in chosen]+[c['t']]); i=ts.index(c['t'])
                l=i
                while l>0 and ts[l]-ts[l-1]<fg: l-=1
                r=i
                while r<len(ts)-1 and ts[r+1]-ts[r]<fg: r+=1
                if r-l+1<=mr: chosen.append(c)
        chosen.sort(key=lambda c:c['t'])
        # fill excessive gaps
        changed=True
        while changed:
            changed=False
            seq=[dict(t=t0)]+chosen+[dict(t=t1)]
            for x,y in zip(seq,seq[1:]):
                if y['t']-x['t']>maxgap:
                    inner=[c for c in cands if x['t']+mg<=c['t']<=y['t']-mg and c not in chosen and c['sal']>=0]
                    if inner:
                        chosen.append(max(inner,key=lambda c:c['sal'])); chosen.sort(key=lambda c:c['t']); changed=True; break
        for c in chosen:
            # refine: use actual onset peak if within 25 ms of grid, else grid
            tt=c['tpk'] if abs(c['tpk']-c['t'])<=0.018 else c['t']
            taps.append(dict(t=round(tt,3),grid=round(c['t'],3),tag=c['src'],sec=sec['label'],pos=c['pos'],res=res))
        stats.append((sec['label'],t0,t1,len(chosen)))
    # global min-gap safety
    out=[]
    for tp in taps:
        if out and tp['t']-out[-1]['t']<0.15: continue
        out.append(tp)
    return a,out,stats
