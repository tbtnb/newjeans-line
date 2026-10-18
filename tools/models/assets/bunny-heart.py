"""H02 Giant Pop-up Bunny with Heart; size 6.5 x 6 x 10 m, budget 4000.
Pivots: root at page hinge, ears0/ears1 at ear roots, heart at heart centre.
SIMPLIFICATIONS: page lines are layered geometry; tiny face marks use palette pink/cream;
heart has broad folded facets rather than every illustrated crease; side/top drawings
are not fully consistent in depth; foot pads are painted mesh facets; no emissive shader.
"""
import math
import bpy
from mathutils import Vector
BUDGET=4000

def mesh(P,name,verts,faces,color):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color);return ob

def heart(P,name,w,h,d,loc,color):
    pts=P.heart(1,20);xmin=min(x for x,z in pts);xmax=max(x for x,z in pts);zmin=min(z for x,z in pts);zmax=max(z for x,z in pts)
    pts=[((x-(xmin+xmax)/2)*w/(xmax-xmin),(z-zmin)*h/(zmax-zmin)) for x,z in pts]
    pts=[(x,z+(.14*h*(1-abs(x)/(.25*w)) if abs(x)<.25*w and z>.6*h else 0)) for x,z in pts]
    vs=[]
    for f,y in [(1,0),(.72,-d*.48),(.72,d*.48)]:
        vs += [(loc[0]+x*f,loc[1]+y,loc[2]+h*.53+(z-h*.53)*f) for x,z in pts]
    vs += [(loc[0],loc[1]-d*.94,loc[2]+h*.5),(loc[0],loc[1]+d*.82,loc[2]+h*.5)]
    fs=[];n=len(pts)
    for i in range(n):
        j=(i+1)%n
        fs.extend([(i,j,n+j,n+i),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n),(2*n+j,2*n+i,3*n+1)])
    return mesh(P,name,vs,fs,color)

def ear(P,name,side,x,y,z,cream,pink,blush):
    # Two longitudinal ridges and a turned tip make a solid folded paper ear.
    if side<0:
        outline=[(-.22,0),(-.98,1.10),(-1.08,2.00),(-.57,3.30),(.18,2.65),(.67,1.87),(.62,.40)]
    else:
        outline=[(-.25,0),(-.10,1.75),(.57,2.65),(1.66,3.30),(1.90,1.80),(1.32,.57),(.25,-.08)]
    def pos(a,b,dep): return (x+a,y+dep+b*.07+.25*(b/3.3)**2,z+b)
    n=len(outline);v=[pos(a,b,0) for a,b in outline]+[pos(a*.93,b,1.0 if b<2.5 else .35) for a,b in outline]
    v.extend([pos(.03 if side<0 else .60,1.75,-.38),pos(.03 if side<0 else .60,1.8,1.12)])
    f=[]
    for i in range(n):j=(i+1)%n;f.extend([(i,j,2*n),(n+j,n+i,2*n+1),(i,n+i,n+j,j)])
    shell=mesh(P,name,v,f,cream)
    cx=.03 if side<0 else .60
    inner=[(-.58,.15),(-.90,1.10),(-.93,1.91),(-.30,1.45),(.24,.18),(.10,-.03)] if side<0 else [(.0,.10),(.30,1.30),(1.43,2.87),(1.40,1.77),(.78,.60),(.21,.02)]
    iv=[pos(a,b,-.04-.27*math.sin(math.pi*b/3.55)) for a,b in inner]+[pos(cx,1.65,-.52)]
    ins=mesh(P,name+'_pink_fold',iv,[(i,(i+1)%len(inner),len(inner)) for i in range(len(inner))],pink)
    details=[shell,ins]
    if side>0:
        # One continuous inset follows the two outer fold planes, with a cream rim.
        points=[Vector(v[k]) for k in (3,3+n,4+n,5+n,5,4)];cc=sum(points,Vector())/6
        points=[tuple(cc+Vector(((p.x-cc.x)*.67,(p.y-cc.y)*.67,(p.z-cc.z)*.82))+Vector((.025,0,0))) for p in points]
        details.append(mesh(P,name+'_side_inner_fold',points,[(0,1,2,3,4,5)],pink))
    return P.pivot(name,(x,y,z),details)

def build(P,spec):
    c=spec['colors'];cream=c['cream'];white=c['white'];pink=c['pink'];blush=c['blush'];gold=c['gold'];parts=[]
    # Open but almost flat, with a real centre V and separated leaves on both fore edges.
    parts.append(P.box('lower_cover',(6.5,6,.10),color=gold))
    for s in (-1,1):
        for k in range(8):
            z=.12+k*.085
            poly=[(s*(.32-.035*k),z),(s*3.15,z+.03),(s*3.15,z+.090),(s*(.29-.035*k),z+.070)]
            parts.append(P.prism('page_leaf',poly[::s],5.78,color=cream if k%2 else white))
        parts.append(P.prism('upper_cover',[(s*.02,.70),(s*3.25,.82),(s*3.25,.92),(s*.02,.80)][::s],6,color=gold))
        parts.append(P.prism('open_page',[(s*.02,.80),(s*3.13,.93),(s*3.13,.96),(s*.02,.85)][::s],5.78,color=cream))
    for yy in (-2.91,2.91):
        for ss in (-1,1):
            parts.append(P.prism('spine_fold_gold',[(0,.80),(ss*.34,.10),(ss*.28,.10),(0,.69)][::ss],.035,loc=(0,yy,0),color=gold))
    parts.append(P.ico('pear_body',1,loc=(0,.65,2.74),scale=(1.94,1.54,2.05),subdiv=3,color=cream))
    parts.append(P.ico('chest',1,loc=(0,-.05,4.32),scale=(1.48,1.42,1.40),subdiv=2,color=cream))
    parts.append(P.ico('faceted_head',1,loc=(0,-.01,5.94),scale=(1.53,1.21,1.28),subdiv=2,color=lambda c,n:white if n.z>.65 else cream))
    for s in (-1,1):
        foot=P.ico('foot',1,loc=(s*1.28,-.84,1.78),scale=(1.11,1.22,.96),subdiv=3,color=lambda c,n:blush if n.y<-.40 and (c.x/.52)**2+(c.z/.65)**2<1.12 else cream)
        parts.append(foot)
        parts.append(P.ico('hugging_arm',1,loc=(s*1.77,-.96,3.62),scale=(.61,.76,.69),subdiv=3,color=cream))
    parts.append(P.ico('tail',.42,loc=(.5,1.82,1.61),subdiv=2,color=white))
    parts.append(P.prism('small_nose',[(-.22,.06),(0,-.12),(.22,.06)],.035,loc=(0,-1.15,5.69),color=pink))
    parts.append(P.prism('small_mouth_fold',[(-.10,0),(0,-.055),(.10,0),(0,-.085)],.018,loc=(0,-1.19,5.52),color=blush))
    # Eyes are subtle cream folded slits on the source sheet, kept in its allowed palette.
    for s in (-1,1):parts.append(P.prism('eye_crease',[(0,0),(.11,.025),(.025,.055)],.012,loc=(s*.65,-1.10,6.06),color=pink))
    for s in (-1,1):parts.append(P.prism('bow_loop',[(0,0),(s*.52,.28),(s*.59,-.25)],.21,loc=(1.49,-.45,5.05),color=pink))
    parts.append(P.ico('bow_knot',.19,loc=(1.49,-.59,5.04),scale=(1,.7,.8),subdiv=2,color=blush))
    ears=[ear(P,'ears0',-1,-.60,-.01,6.70,cream,pink,blush),ear(P,'ears1',1,.70,.03,6.70,cream,pink,blush)]
    h=heart(P,'folded_heart',3.90,3.60,1.10,(0,-1.35,1.85),pink)
    hp=P.pivot('heart',(0,-1.35,3.25),[h])
    root=P.pivot('root',(0,0,0),parts+ears+[hp]);fit(root,spec)

def fit(root,spec):
    bpy.context.view_layer.update();v=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
    e=[max(p[i] for p in v)-min(p[i] for p in v) for i in range(3)];s=spec['size_m'];root.scale=(s['w']/e[0],s['d']*.96/e[1],s['h']/e[2]);bpy.context.view_layer.update()
