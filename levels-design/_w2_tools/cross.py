import json,sys
for s in sys.argv[1:]:
    n=json.load(open(f'/workspace/newjeans-line-designs/{s}/layout.json'))['path']['nodes']
    segs=list(zip(n,n[1:])); out=[]
    def inter(a,b,c,d):
        # axis-aligned segments
        ax0,ax1=sorted([a[1],b[1]]);az0,az1=sorted([a[2],b[2]]);cx0,cx1=sorted([c[1],d[1]]);cz0,cz1=sorted([c[2],d[2]])
        return ax0<=cx1+1 and cx0<=ax1+1 and az0<=cz1+1 and cz0<=az1+1
    for i,(a,b) in enumerate(segs):
        for j in range(i+2,len(segs)):
            c,d=segs[j]
            if inter(a,b,c,d): out.append((a[0],c[0],a[3],c[3]))
    # compress
    res=[];last=None
    for x in out:
        if last and abs(x[0]-last[0])<3 and abs(x[1]-last[1])<3: continue
        res.append(x); last=x
    print(s,[(round(a,1),round(b,1),ya,yb) for a,b,ya,yb in res])
