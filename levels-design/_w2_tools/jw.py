def windows(taps):
    w=[]
    for i,t in enumerate(taps):
        p=t-taps[i-1] if i>0 else 9; n=taps[i+1]-t if i+1<len(taps) else 9
        g=min(p,n); w.append(min(0.5*g,max(0.045,min(0.11,0.45*g))))   # v2.5 per-tap rule
    return w
def summary(taps):
    w=sorted(windows(taps)); n=len(w)
    return f'min ±{w[0]*1000:.0f} ms, median ±{w[n//2]*1000:.0f} ms, {sum(1 for x in w if x<0.11)} of {n} taps below the ±110 ms cap'
