"""P20 Carnival candy stall. Size 2.6 x 1.5 x 3.2 m from spec; 1500 tris; root, heart.
SIMPLIFICATIONS: opaque cyan paper replaces glass; candy details use raised facets; six lights have fixed palette colours; text omitted. The open serving bay follows front/hero (the comparison mask fills this opening)."""
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
    n=len(out);cz=sum(z for x,z in out)/n
    if name!='creased magenta heart':
        if name=='side candy heart':
            # Raised shoulder and centre crease form an embossed solid paper candy.
            v=[(x,0,z) for x,z in out]+[(x*.70,-depth*.65,cz+(z-cz)*.70) for x,z in out]+[(0,-depth,cz)]
            f=[]
            for i in range(n):
                j=(i+1)%n;f.extend([(i,j,n+j,n+i),(n+i,n+j,2*n)])
        else:
            v=[(x,0,z) for x,z in out]+[(0,-depth,cz)]
            f=[(i,(i+1)%n,n) for i in range(n)]
        ob=mesh(P,name,v,f,col);ob.location=loc;return ob
    # Independent lobe apices and a descending centre crease, rather than one flat fan.
    v=[(x,-depth*.15,z) for x,z in out]+[(x*.79,-depth*.40,cz+(z-cz)*.79) for x,z in out]
    L,R,C,D=range(2*n,2*n+4)
    v.extend([(-.20,-depth*1.65,cz+.14),(.20,-depth*1.65,cz+.14),(0,-depth*1.80,cz-.10),(0,-depth,cz-.28)])
    back=len(v);v.extend([(x,depth*.20,z) for x,z in out]);f=[]
    for i in range(n):
        j=(i+1)%n;f.extend([(i,j,n+j,n+i),(i,back+i,back+j,j)])
    q=lambda k:n+k
    f.extend([(q(0),q(1),D),(q(1),L,D),(q(1),q(2),L),(q(2),q(3),L),(q(3),q(4),L),(q(4),q(5),L),(q(5),C,L),(C,D,L),(q(0),D,C),
              (q(5),q(6),R),(q(6),q(7),R),(q(7),q(8),R),(q(8),q(9),R),(q(9),D,R),(q(9),q(0),D),(q(5),R,C),(C,R,D)])
    f.append(tuple(range(back,back+n)))
    ob=mesh(P,name,v,f,col);ob.location=loc;return ob

def build(P, spec):
    c=spec['colors'];G=c['gold'];K=c['cream'];M=c['magenta'];C=c['cyan'];sign=[]
    P.box('gold bottom binding',(2.38,1.16,.075),color=G)
    P.box('cream cabinet',(2.10,1.02,.61),loc=(0,0,.075),color=K)
    P.box('gold countertop',(2.52,1.30,.075),loc=(0,0,.69),color=G)
    # Recessed bordered cartouches on both faces and both side panels.
    panel=[(-.40,0),(.40,0),(.40,.28),(.35,.35),(-.35,.35),(-.40,.28)]
    for x,y,rot,sc in [(-.56,-.523,0,1),(.56,-.523,0,1),(1.057,0,90,.78),(-1.057,0,-90,.78)]:
        P.card('gold panel frame',[(a*sc,b) for a,b in panel],loc=(x,y,.18),rot=(0,0,rot),color=G)
        P.card('pink inset panel',[(a*sc*.88,b*.80) for a,b in panel],loc=(x+(.012 if rot==90 else -.012 if rot==-90 else 0),y-.012 if rot==0 else y,.215),rot=(0,0,rot),color=M)
        ob=gem(P,'raised diamond',[(0,0),(.08,.09),(0,.18),(-.08,.09)],.05,(0,0,0),G);ob.location=(x,y-.035 if rot==0 else y,.29);ob.rotation_euler.z=math.radians(rot)
    for x in [-1.105,1.105]:
        P.card('cyan foot panel',[(-.042,0),(.042,0),(.053,.34),(0,.38),(-.053,.34)],loc=(x,-.602,.22),color=C)
    # Four heavy paper feet and very slim cream shafts, topped by diamond finials.
    for x in [-1.105,1.105]:
        for y in [-.475,.475]:
            P.box('cream pillar',(.125,.125,2.02),loc=(x,y,.07),color=K)
            for z,sz,col in [(.0,(.27,.25,.09),G),(.09,(.23,.23,.57),K)]:
                P.box('post moulding',sz,loc=(x,y,z),color=col)
            for z in [.82,1.79]:
                # The collars wrap all four sides; their hidden caps cost no triangles.
                v=[(x+a*.07,y+b*.07,z+h) for h in [0,.065] for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]]
                mesh(P,'pink post band',v,[(k,(k+1)%4,(k+1)%4+4,k+4) for k in range(4)],M)
            # Side-facing inset is on the projecting pier, outside the cabinet wall.
            side=1 if x>0 else -1
            P.card('cyan side pier panel',[(-.045,0),(.045,0),(.06,.30),(0,.35),(-.06,.30)],loc=(x+side*.118,y,.22),rot=(0,0,side*90),color=C)
    for x in [-1.025,1.025]:
        P.box('ridge cream cap',(.14,.15,.17),loc=(x,0,2.59),color=K)
        P.lathe('gold ridge diamond',[(0,2.76),(.10,2.85),(0,2.97)],4,loc=(x,0,0),color=G)
    # Hipped canopy: long striped slopes plus folded three-stripe end slopes.
    ridge=1.025;outer=1.30;zz=2.59;ee=2.055;depth=.75
    for j in range(7):
        x0=-outer+j*2*outer/7;x1=x0+2*outer/7;col=M if j%2==0 else K
        for side in [-1,1]:
            mesh(P,'broad awning stripe',[(x0/outer*ridge,0,zz),(x1/outer*ridge,0,zz),(x1,side*depth,ee),(x0,side*depth,ee)],[(0,1,2,3)],col)
            w=x1-x0;out=[(-w/2,0),(w/2,0)]+[(w/2*math.cos(math.pi*k/5),-.23*math.sin(math.pi*k/5)) for k in range(1,6)]
            # Plan drawing shows a straight back hem; keep the scallops on the serving edge.
            if side>0:out=[(-w/2,0),(w/2,0),(w/2,-.035),(-w/2,-.035)]
            # A single folded hem with a narrow gold paper border, no stacked solid cutouts.
            front=side*depth
            o=mesh(P,'scalloped valance',[(xx+(x0+x1)/2,front,ee+.012+z) for xx,z in out], [tuple(range(len(out)))],col)
            if side>0:continue
            arc=out[1:];vs=[]
            for xx,z in arc:vs.extend([(xx+(x0+x1)/2,front-.002,ee+.012+z),(xx*.94+(x0+x1)/2,front-.003,ee+.012+z*.90)])
            mesh(P,'gold scallop piping',vs,[(2*k,2*k+1,2*k+3,2*k+2) for k in range(len(arc)-1)],G)
    mesh(P,'gold straight back hem',[(-outer,depth,ee-.035),(outer,depth,ee-.035),(outer,depth,ee-.012),(-outer,depth,ee-.012)],[(0,1,2,3)],G)
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
    # Thick gold corner folds finish the eaves in side and plan views.
    for x in [-outer+.014,outer-.014]:
        for y in [-depth+.014,depth-.014]:
            P.box('gold eave corner',(.055,.055,.21),loc=(x,y,ee-.20),color=G)
    # The triangular cream/cyan crest spans the front ridge behind the sign.
    P.prism('cream crest triangle',[(-1.07,2.59),(1.07,2.59),(0,3.03)],.045,loc=(0,-.04,0),color=K)
    crest=[(-1.07,2.59),(1.07,2.59),(0,3.03)]
    inner=[(-.94,2.63),(.94,2.63),(0,2.98)]
    for i in range(3):
        j=(i+1)%3
        mesh(P,'gold crest border',[(crest[k][0],-.067,crest[k][1]) for k in [i,j]]+[(inner[k][0],-.067,inner[k][1]) for k in [j,i]],[(0,1,2,3)],G)
    for side in [-1,1]:
        P.card('cyan crest inset',[(side*.35,2.63),(side*.94,2.63),(side*.49,2.85)],loc=(0,-.069,0),color=C)
    heart=[(0,0),(-.48,.35),(-.53,.67),(-.28,.84),(-.10,.78),(0,.66),(.10,.78),(.28,.84),(.53,.67),(.48,.35)]
    sign.append(P.prism('gold sign frame',heart,.105,loc=(0,-.10,2.39),color=G))
    sign.append(gem(P,'creased magenta heart',[(x*.88,.05+z*.88) for x,z in heart],.085,(0,-.17,2.39),M))
    # Six diamond lanterns hang from a shallow draped string.
    last=None
    for i in range(7):
        x=-1.02+i*.34;z=1.82-.07*math.sin(i*math.pi/6)
        if last:mesh(P,'sagging light cord',[last,(last[0],last[1],last[2]-.010),(x,0,z-.010),(x,0,z)],[(0,1,2,3)],G)
        last=(x,0,z)
        if i<6:
            xx=x+.15;P.lathe('faceted hanging lamp',[(0,z-.25),(.085,z-.14),(.067,z-.06),(0,z-.02)],4,loc=(xx,0,0),color=G if i%2==0 else M)
    # Five shoulder-folded six-sided candy jars, with raised gems on visible faces.
    for i,(x,r,h) in enumerate([(-.82,.18,.32),(-.43,.14,.26),(-.02,.19,.36),(.43,.16,.29),(.81,.14,.23)]):
        yy=[.04,-.045,.035,-.10,-.25][i]
        P.lathe('folded cyan jar',[(r*.87,0),(r,h-.05),(r*.87,h)],6,loc=(x,yy,.76),color=C)
        # Folded lid: vertical lip and six roof facets; underside is inside the jar.
        lv=[(x+r*1.03*math.cos(j*math.pi/3),yy+r*1.03*math.sin(j*math.pi/3),.76+h+z) for z in [0,.028] for j in range(6)]+[(x,yy,.76+h+.067)]
        mesh(P,'gold jar lid',lv,[(j,(j+1)%6,(j+1)%6+6,j+6) for j in range(6)]+[(j+6,(j+1)%6+6,12) for j in range(6)],G)
        P.lathe('diamond jar knob',[(0,0),(.042,.04),(0,.10)],4,loc=(x,yy,.80+h),color=G)
        for j in range(2):
            xx=x+(j-.5)*r*.70;z=.84+(j%2)*h*.35
            ob=gem(P,'paper candy gem',P.star(.075,.038) if i%2 else [(0,-.07),(-.067,0),(-.064,.055),(-.03,.08),(0,.045),(.03,.08),(.064,.055),(.067,0)],.034,(xx,yy-r-.01,z),M if i%2==0 or j==1 else K)
        if i%2==0:
            gem(P,'extra folded candy heart',[(0,-.06),(-.05,0),(-.05,.045),(-.025,.065),(0,.035),(.025,.065),(.05,.045),(.05,0)],.032,(x+r*.35,yy-r-.016,.87+h*.28),M if i!=2 else K)
        if i==4:
            # Candy wraps around the right jar instead of disappearing from the side.
            for j in range(2):
                ob=gem(P,'side candy heart',[(0,-.055),(-.05,0),(-.05,.04),(-.025,.06),(0,.03),(.025,.06),(.05,.04),(.05,0)],.035,(x+r+.008,yy+(j-.5)*.075,.86+j*.055),M)
                ob.rotation_euler.z=math.pi/2
    for x in [-.145,.145]:P.card('front pink ribbon',[(-.027,0),(.027,0),(.027,.59),(-.027,.59)],loc=(x,-.53,.08),color=M)
    P.prism('gold counter pennant',[(-.32,.76),(.32,.76),(0,.40)],.027,loc=(0,-.68,0),color=G)
    gem(P,'folded pink counter pennant',[(-.26,.74),(.26,.74),(0,.46)],.044,(0,-.702,0),M)
    finish(P,spec,[('heart',(0,-.10,2.80),sign)])
