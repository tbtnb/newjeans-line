"""Greedy section-by-section route planner.
Each section gives a route TEXTURE in canonical orientation (pairs written around 'NE'); the planner tries the
8 orientations (4 rotations x mirror) and keeps the first-best one that creates no illegal self-crossing with the
road built so far, preferring compact placements (so the level folds back over itself with real over/under passes)."""
import numpy as np, math
from geom import *
ROT={'N':'E','E':'S','S':'W','W':'N'}; MIR={'E':'W','W':'E','N':'N','S':'S'}
def tf_pair(P,r,m):
    out=''
    for c in P:
        if m: c=MIR[c]
        for _ in range(r): c=ROT[c]
        out+=c
    return norm(out)
def tf_seg(seg,r,m):
    s=dict(seg)
    if 'pair' in s: s['pair']=tf_pair(s['pair'],r,m)
    if 'pairs' in s: s['pairs']=[tf_pair(p,r,m) for p in s['pairs']]
    if m and 'rot' in s: s['rot']={'R':'L','L':'R'}[s['rot']]
    return s
def new_hits(nodes,W,elev,i0,min_dt=1.5,clear=3.0,widths=None):
    segs=list(zip(nodes,nodes[1:])); n=len(segs); hits=[]
    bx=np.array([(min(a['x'],b['x']),max(a['x'],b['x']),min(a['z'],b['z']),max(a['z'],b['z']),a['t'],b['t']) for a,b in segs])
    for j in range(i0,n):
        A=bx[j]; cand=np.where((bx[:,0]-W/2<A[1]+W/2)&(A[0]-W/2<bx[:,1]+W/2)&(bx[:,2]-W/2<A[3]+W/2)&(A[2]-W/2<bx[:,3]+W/2)&(bx[:,5]<=A[4]-min_dt))[0]
        for i in cand:
            yi=[elev_at(elev,x) for x in np.linspace(bx[i,4],bx[i,5],5)]
            yj=[elev_at(elev,x) for x in np.linspace(A[4],A[5],5)]
            if min(abs(a-b) for a in yi for b in yj)<clear: hits.append((round(bx[i,4],2),round(A[4],2)))
    return hits
def count_passes(nodes,W,i0,min_dt=1.5):
    segs=list(zip(nodes,nodes[1:])); n=len(segs); c=0
    bx=np.array([(min(a['x'],b['x']),max(a['x'],b['x']),min(a['z'],b['z']),max(a['z'],b['z']),a['t'],b['t']) for a,b in segs])
    for j in range(i0,n):
        A=bx[j]; c+=int(((bx[:,0]-W/2<A[1]+W/2)&(A[0]-W/2<bx[:,1]+W/2)&(bx[:,2]-W/2<A[3]+W/2)&(A[2]-W/2<bx[:,3]+W/2)&(bx[:,5]<=A[4]-min_dt)).sum())
    return c
def plan(taps,speeds,dur,start,elev,sections,W=2.6,forced=None,verbose=True):
    """sections: list of dict(t, prog=[seg,...] (canonical, seg['t'] absolute), want='compact'|'far'|'cross', fix=(r,m) optional)"""
    chosen=[]; prog_all=[]
    for si,S in enumerate(sections):
        t_end=sections[si+1]['t'] if si+1<len(sections) else dur
        opts=[S['fix']] if 'fix' in S else [(r,m) for m in (0,1) for r in range(4)]
        best=None
        for r,m in opts:
            prog=prog_all+[tf_seg(sg,r,m) for sg in S['prog']]
            tt=[x for x in taps if x<t_end]
            pairs=program_pairs(tt,prog); dirs=plan_dirs(tt,pairs,start,forced)
            nodes=build(tt,dirs,speeds,t_end,start,elev)
            i0=sum(1 for x in taps if x<S['t'])
            h=new_hits(nodes,W,elev,i0)
            xs=np.array([n['x'] for n in nodes]); zs=np.array([n['z'] for n in nodes])
            cx,cz=xs[:i0+1].mean(),zs[:i0+1].mean()
            spread=math.hypot(xs[i0:].mean()-cx,zs[i0:].mean()-cz)
            ext=(xs.max()-xs.min())+(zs.max()-zs.min())
            pas=count_passes(nodes,W,i0)
            want=S.get('want','compact')
            score=len(h)*1000+ (ext if want!='far' else -spread) - (40*min(pas,6) if want=='cross' else 0)
            if best is None or score<best[0]: best=(score,r,m,len(h),pas)
        sc,r,m,nh,pas=best; chosen.append((r,m)); prog_all+= [tf_seg(sg,r,m) for sg in S['prog']]
        if verbose: print(f"  sec@{S['t']:7.2f} orient r{r} m{m} hits {nh} passes {pas}")
    return prog_all,chosen

def plan_dfs(taps,speeds,dur,start,elev,sections,W=2.6,forced=None,max_evals=6000,verbose=True):
    """depth-first version: options of each section are tried in score order; backtracks when a section cannot be
    placed without an illegal crossing. sections may carry 'alts': list of alternative canonical progs."""
    evals=[0]; T=list(taps)
    def options(si,prog_all):
        S=sections[si]; t_end=sections[si+1]['t'] if si+1<len(sections) else dur
        tt=[x for x in T if x<t_end]; i0=sum(1 for x in T if x<S['t'])
        alts=[S['prog']]+S.get('alts',[])
        ors=[S['fix']] if 'fix' in S else [(r,m) for m in (0,1) for r in range(4)]
        res=[]
        for ai,alt in enumerate(alts):
            for r,m in ors:
                evals[0]+=1
                prog=prog_all+[tf_seg(sg,r,m) for sg in alt]
                pairs=program_pairs(tt,prog); dirs=plan_dirs(tt,pairs,start,forced)
                nodes=build(tt,dirs,speeds,t_end,start,elev)
                h=new_hits(nodes,W,elev,i0)
                if h: continue
                xs=np.array([n['x'] for n in nodes]); zs=np.array([n['z'] for n in nodes])
                ext=(xs.max()-xs.min())+(zs.max()-zs.min())
                pas=count_passes(nodes,W,i0); want=S.get('want','compact')
                score=ext+ai*15-(40*min(pas,6) if want=='cross' else 0)
                res.append((score,ai,r,m,pas,[tf_seg(sg,r,m) for sg in alt]))
        res.sort(key=lambda x:x[0]); return res
    path=[]; deep=[0]
    def rec(si,prog_all):
        deep[0]=max(deep[0],si)
        if si==len(sections): return True
        if evals[0]>max_evals: return False
        for sc,ai,r,m,pas,segs in options(si,prog_all):
            path.append((ai,r,m,pas))
            if rec(si+1,prog_all+segs): return True
            path.pop()
            if evals[0]>max_evals: return False
        return False
    ok=rec(0,[])
    if verbose: print('  dfs ok' if ok else f'  dfs FAILED (deepest section {deep[0]})', 'evals',evals[0],'choices',path)
    if not ok: return None,path
    prog=[]
    for S,(ai,r,m,_) in zip(sections,path):
        alt=([S['prog']]+S.get('alts',[]))[ai]; prog+=[tf_seg(sg,r,m) for sg in alt]
    return prog,path
