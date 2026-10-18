"""P20 Carnival candy stall. Size 2.6 x 1.5 x 3.2 m from spec; 1500 tris; root, heart.
SIMPLIFICATIONS: jar glass represented by cyan paper with raised printed candy facets; valance uses thin folded paper; six lights use fixed palette colours; text and transparent glazing omitted; front/side design masks fill the open counter void."""
BUDGET = 1500

import math
import bpy
import bmesh
from mathutils import Vector, Matrix

def mesh(P, name, verts, faces, color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.normal_update()
    if ('awning stripe' in name or 'hip stripe' in name) and sum(f.normal.z for f in bm.faces)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
    if 'scallop' in name:
        bm.normal_update();cen=sum((v.co for v in bm.verts),Vector((0,0,0)))/len(bm.verts)
        outward=Vector((1 if cen.x>0 else -1,0,0)) if name.startswith('side') else Vector((0,1 if cen.y>0 else -1,0))
        if sum(f.normal.dot(outward) for f in bm.faces)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
    bm.to_mesh(me); bm.free(); me.update()
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob); P.paint(ob,color)
    return ob

def rod(P,name,a,b,r,color,n=6):
    a,b=Vector(a),Vector(b); ob=P.cyl(name,r,(b-a).length,n,loc=a,color=color)
    ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return ob

def finish(P,spec,animated=()):
    bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
    pts=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
    lo=Vector(tuple(min(p[i] for p in pts) for i in range(3))); hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
    size=spec['size_m']; target=Vector((size['w'],size['d'],size['h'])) if isinstance(size,dict) else (hi-lo)*(size/max(hi-lo))
    factors=Vector(tuple(target[i]/(hi[i]-lo[i]) for i in range(3)))
    center=Vector(((hi.x+lo.x)/2,(hi.y+lo.y)/2,lo.z))
    def point(v): return Vector(tuple((v[i]-center[i])*factors[i] for i in range(3)))
    for ob in obs:
        mw=ob.matrix_world.copy()
        for v in ob.data.vertices: v.co=point(mw@v.co)
        ob.matrix_world=Matrix.Identity(4)
    moving=set(); roots=[]
    for name,joint,children in animated:
        roots.append(P.pivot(name,point(Vector(joint)),children)); moving.update(children)
    P.pivot('root',(0,0,0),[o for o in obs if o not in moving]+roots)

def gem(P,name,out,depth,loc,col):
    # Shallow bevel and a raised asymmetric crease make the paper heart read as a gem.
    n=len(out);cz=sum(z for x,z in out)/n
    if name!='creased magenta heart':
        ob=mesh(P,name,[(x,0,z) for x,z in out]+[(0,-depth,cz)],[(i,(i+1)%n,n) for i in range(n)],col);ob.location=loc;return ob
    v=[(x,-depth*.15,z) for x,z in out]+[(x*.79,-depth*.35,cz+(z-cz)*.79) for x,z in out]+[(0,-depth,cz+.06)]+[(x,depth*.20,z) for x,z in out]
    f=[]
    for i in range(n):
        j=(i+1)%n;f.extend([(i,j,n+j,n+i),(n+i,n+j,2*n),(i,2*n+1+i,2*n+1+j,j)])
    f.append(tuple(range(2*n+1,3*n+1)))
    o=mesh(P,name,v,f,col);o.location=loc;return o

def build(P, spec):
    c=spec['colors'];G=c['gold'];K=c['cream'];M=c['magenta'];C=c['cyan'];sign=[]
    P.box('gold bottom binding',(2.46,1.12,.075),color=G)
    P.box('cream cabinet',(2.33,1.05,.61),loc=(0,0,.075),color=K)
    P.box('gold countertop',(2.52,1.30,.065),loc=(0,0,.69),color=G)
    # Recessed bordered cartouches on both faces and both side panels.
    panel=[(-.40,0),(.40,0),(.40,.28),(.35,.35),(-.35,.35),(-.40,.28)]
    for x,y,rot,sc in [(-.59,-.572,0,1),(.59,-.572,0,1),(1.175,0,90,.88),(-1.175,0,-90,.88)]:
        P.card('gold panel frame',[(a*sc,b) for a,b in panel],loc=(x,y,.18),rot=(0,0,rot),color=G)
        P.card('pink inset panel',[(a*sc*.88,b*.80) for a,b in panel],loc=(x+(.012 if rot==90 else -.012 if rot==-90 else 0),y-.012 if rot==0 else y,.215),rot=(0,0,rot),color=M)
        ob=gem(P,'raised diamond',[(0,0),(.08,.09),(0,.18),(-.08,.09)],.05,(0,0,0),G);ob.location=(x,y-.035 if rot==0 else y,.29);ob.rotation_euler.z=math.radians(rot)
    for x in [-1.08,1.08]:
        P.card('cyan foot panel',[(-.042,0),(.042,0),(.053,.34),(0,.38),(-.053,.34)],loc=(x,-.54,.22),color=C)
    # Four heavy paper feet and very slim cream shafts, topped by diamond finials.
    for x in [-1.08,1.08]:
        for y in [-.43,.43]:
            P.box('cream pillar',(.125,.125,2.02),loc=(x,y,.07),color=K)
            for z,sz,col in [(.02,(.26,.23,.09),G),(.10,(.20,.18,.57),K)]:
                P.box('post moulding',sz,loc=(x,y,z),color=col)
            for z in [.82,2.02]:P.box('pink post band',(.14,.14,.065),loc=(x,y,z),color=M)
    for x in [-.99,.99]:
        P.box('ridge cream cap',(.14,.15,.17),loc=(x,0,2.51),color=K)
        P.lathe('gold ridge diamond',[(0,2.68),(.10,2.77),(0,2.89)],4,loc=(x,0,0),color=G)
    # Hipped canopy: long striped slopes plus folded three-stripe end slopes.
    ridge=.99;outer=1.30;zz=2.52;ee=2.13;depth=.72
    for j in range(7):
        x0=-outer+j*2*outer/7;x1=x0+2*outer/7;col=M if j%2==0 else K
        for side in [-1,1]:
            mesh(P,'broad awning stripe',[(x0/outer*ridge,0,zz),(x1/outer*ridge,0,zz),(x1,side*depth,ee),(x0,side*depth,ee)],[(0,1,2,3)],col)
            w=x1-x0;out=[(-w/2,0),(w/2,0)]+[(w/2*math.cos(math.pi*k/6),-.23*math.sin(math.pi*k/6)) for k in range(1,7)]
            # A single folded hem with a narrow gold paper border, no stacked solid cutouts.
            front=side*depth
            o=mesh(P,'scalloped valance',[(xx+(x0+x1)/2,front,ee+.012+z) for xx,z in out], [tuple(range(len(out)))],col)
            arc=out[1:];vs=[]
            for xx,z in arc:vs.extend([(xx+(x0+x1)/2,front-.002,ee+.012+z),(xx*.94+(x0+x1)/2,front-.003,ee+.012+z*.90)])
            mesh(P,'gold scallop piping',vs,[(2*k,2*k+1,2*k+3,2*k+2) for k in range(len(arc)-1)],G)
    for side in [-1,1]:
        # Side faces have their own pink/cream/pink folds, not cyan gable walls.
        for j in range(3):
            y0=-depth+j*2*depth/3;y1=y0+2*depth/3
            mesh(P,'side hip stripe',[(side*ridge,0,zz),(side*outer,y0,ee),(side*outer,y1,ee)],[(0,1,2)],K if j==1 else M)
            ww=2*depth/3;out=[(-ww/2,0),(ww/2,0)]+[(ww/2*math.cos(math.pi*k/5),-.23*math.sin(math.pi*k/5)) for k in range(1,6)]
            vs=[(side*outer,(y0+y1)/2+a,ee+.01+b) for a,b in out]
            mesh(P,'side scalloped valance',vs,[tuple(range(len(vs)))],K if j==1 else M)
            vs=[]
            for a,b in out[1:]:vs.extend([(side*(outer+.002),(y0+y1)/2+a,ee+.01+b),(side*(outer+.003),(y0+y1)/2+a*.94,ee+.01+b*.90)])
            mesh(P,'side gold scallop piping',vs,[(2*k,2*k+1,2*k+3,2*k+2) for k in range(len(out)-2)],G)
        for yy in [-depth,depth]:
            mesh(P,'gold hip binding',[(side*ridge-.014,0,zz+.005),(side*ridge+.014,0,zz+.005),(side*outer+.014,yy,ee+.005),(side*outer-.014,yy,ee+.005)],[(0,1,2,3)],G)
    # The triangular cream/cyan crest spans the front ridge behind the sign.
    P.prism('gold crest triangle',[(-1.07,2.52),(1.07,2.52),(0,2.98)],.045,loc=(0,-.04,0),color=G)
    for side in [-1,1]:
        P.prism('cyan crest inset',[(side*.35,2.57),(side*.94,2.57),(side*.49,2.80)],.05,loc=(0,-.055,0),color=C)
    heart=[(0,0),(-.48,.35),(-.53,.67),(-.28,.84),(-.10,.78),(0,.66),(.10,.78),(.28,.84),(.53,.67),(.48,.35)]
    sign.append(P.prism('gold sign frame',heart,.105,loc=(0,-.10,2.39),color=G))
    sign.append(gem(P,'creased magenta heart',[(x*.88,.05+z*.88) for x,z in heart],.30,(0,-.17,2.39),M))
    # Six diamond lanterns hang from a shallow draped string.
    last=None
    for i in range(7):
        x=-1.02+i*.34;z=1.94-.07*math.sin(i*math.pi/6)
        if last:mesh(P,'sagging light cord',[last,(last[0],last[1],last[2]-.010),(x,-.59,z-.010),(x,-.59,z)],[(0,1,2,3)],G)
        last=(x,-.59,z)
        if i<6:
            xx=x+.15;P.lathe('faceted hanging lamp',[(0,z-.25),(.085,z-.14),(.067,z-.06),(0,z-.02)],4,loc=(xx,-.59,0),color=G if i%2==0 else M)
    # Five generous eight-plane candy jars. Printed candy gems sit on their visible faces.
    for i,(x,r,h) in enumerate([(-.82,.18,.32),(-.43,.14,.26),(-.02,.19,.36),(.43,.16,.29),(.81,.14,.23)]):
        P.lathe('folded cyan jar',[(r,0),(r,h)],6,loc=(x,-.22,.76),color=C)
        P.cyl('gold jar lid',r*1.03,.040,6,loc=(x,-.22,.76+h),color=G)
        P.lathe('diamond jar knob',[(0,0),(.042,.04),(0,.10)],4,loc=(x,-.22,.80+h),color=G)
        for j in range(3):
            xx=x+(j-1)*r*.50;z=.84+(j%2)*h*.35
            ob=gem(P,'paper candy gem',P.star(.075,.038) if i%2 else [(0,-.06),(-.06,0),(-.04,.07),(.04,.07),(.06,0)],.034,(xx,-.22-r-.01,z),M if i%2==0 or j==1 else K)
    P.prism('gold counter pennant',[(-.32,.76),(.32,.76),(0,.40)],.027,loc=(0,-.68,0),color=G)
    P.prism('pink counter pennant',[(-.26,.74),(.26,.74),(0,.46)],.030,loc=(0,-.70,0),color=M)
    finish(P,spec,[('heart',(0,-.10,2.80),sign)])
