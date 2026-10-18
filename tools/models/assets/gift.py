"""P12 Gift box. .7 x .6 x .8 m; 300 tris; root, lid at rear hinge.
SIMPLIFICATIONS: ribbon woven texture omitted; open six-sided bow loops."""

import math
import bpy
from mathutils import Vector, Matrix

def mesh(P,name,verts,faces,col):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    import bmesh
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free(); me.update()
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob); P.paint(ob,col); return ob

def beam(P,name,a,b,r,col,n=6):
    a,b=Vector(a),Vector(b); ob=P.cyl(name,r,(b-a).length,n,loc=a,color=col)
    ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return ob

def heart(P,name,w,h,d,loc,col):
    # Angular lobes, a central valley, and individually triangulated convex facets.
    outline=[(0,.79),(.16,.98),(.34,1),(.5,.83),(.49,.54),(.33,.27),(0,0),(-.33,.27),(-.49,.54),(-.5,.83),(-.34,1),(-.16,.98)]
    outline=[(x*w,z*h) for x,z in outline]; n=len(outline)
    vv=[]
    for y,k in [(0,1),(-d*.42,.77),(d*.42,.77)]:
        vv += [(loc[0]+x*k,loc[1]+y,loc[2]+h*.53+(z-h*.53)*k) for x,z in outline]
    vv += [(loc[0],loc[1]-d*.5,loc[2]+h*.55),(loc[0],loc[1]+d*.5,loc[2]+h*.55)]
    ff=[]
    for i in range(n):
        j=(i+1)%n
        ff += [(i,j,n+j),(i,n+j,n+i),(i,2*n+i,2*n+j),(i,2*n+j,j),(n+i,n+j,3*n),(2*n+j,2*n+i,3*n+1)]
    return mesh(P,name,vv,ff,col)

def puffstar(P,name,r,d,loc,col):
    ol=P.star(r,r*.46); n=len(ol); vv=[(loc[0]+x,loc[1],loc[2]+z) for x,z in ol]
    vv += [(loc[0],loc[1]-d/2,loc[2]),(loc[0],loc[1]+d/2,loc[2])]
    return mesh(P,name,vv,[(i,(i+1)%n,n) for i in range(n)]+[((i+1)%n,i,n+1) for i in range(n)],col)

def ring(P,name,points,r,col,sides=6,closed=False):
    pts=[Vector(p) for p in points]; vv=[]
    for i,p in enumerate(pts):
        tangent=(pts[(i+1)%len(pts)]-pts[(i-1)%len(pts)]) if closed else (pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)])
        tangent.normalize(); u=tangent.cross(Vector((0,1,0)))
        if u.length<.01:u=tangent.cross(Vector((0,0,1)))
        u.normalize(); v=tangent.cross(u).normalized()
        vv += [tuple(p+r*(u*math.cos(j*2*math.pi/sides)+v*math.sin(j*2*math.pi/sides))) for j in range(sides)]
    ff=[]
    for i in range(len(pts) if closed else len(pts)-1):
        for j in range(sides):ff.append((i*sides+j,i*sides+(j+1)%sides,((i+1)%len(pts))*sides+(j+1)%sides,((i+1)%len(pts))*sides+j))
    if not closed:ff += [tuple(reversed(range(sides))),tuple((len(pts)-1)*sides+j for j in range(sides))]
    return mesh(P,name,vv,ff,col)

def finish(P,s,static,groups=()):
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH']; bpy.context.view_layer.update()
    pts=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
    lo=Vector(tuple(min(p[k] for p in pts) for k in range(3))); hi=Vector(tuple(max(p[k] for p in pts) for k in range(3)))
    size=s['size_m']; scale=Vector((size['w']/(hi.x-lo.x),size['d']/(hi.y-lo.y),size['h']/(hi.z-lo.z)))
    offset=Vector((-(hi.x+lo.x)/2,-(hi.y+lo.y)/2,-lo.z))
    def tf(v):return Vector(tuple((v[k]+offset[k])*scale[k] for k in range(3)))
    for ob in obs:
        mw=ob.matrix_world.copy()
        for v in ob.data.vertices:v.co=tf(mw@v.co)
        ob.matrix_world=Matrix.Identity(4)
    piv=[]
    for name,joint,children in groups:piv.append(P.pivot(name,tf(Vector(joint)),children))
    P.pivot('root',(0,0,0),static+piv)

def build(P,s):
    c=s['colors']; L,K,G=c['lavender'],c['pink'],c['gold']; st=[]; lid=[]
    # Open box cavity, four separate walls, rim visible below floating lid.
    st.append(P.box('bottom',(.68,.58,.025),(0,0,0),L))
    for x in [-.328,.328]:st.append(P.box('box side',(.024,.58,.42),(x,0,.02),L))
    for y in [-.278,.278]:st.append(P.box('box wall',(.636,.024,.42),(0,y,.02),L))
    for y in [-.292,.292]:
        st += [P.card('body gold ribbon',[(-.095,0),(.095,0),(.095,.44),(-.095,.44)],(0,y,0),G),P.card('body pink ribbon',[(-.0775,0),(.0775,0),(.0775,.44),(-.0775,.44)],(0,y+(.002 if y>0 else -.002),0),K)]
    for x in [-.342,.342]:
        st += [P.card('side gold ribbon',[(-.085,0),(.085,0),(.085,.44),(-.085,.44)],(x,0,0),G,rot=(0,0,90)),P.card('side pink ribbon',[(-.0675,0),(.0675,0),(.0675,.44),(-.0675,.44)],(x+(.002 if x>0 else -.002),0,0),K,rot=(0,0,90))]
    lid.append(P.box('lid',(.7,.6,.105),(0,0,.465),L))
    lid += [P.box('lid gold band x',(.19,.607,.113),(0,0,.477),G),P.box('lid pink band x',(.155,.612,.117),(0,0,.475),K),P.box('lid gold band y',(.707,.17,.113),(0,0,.477),G),P.box('lid pink band y',(.712,.135,.117),(0,0,.475),K)]
    # A hollow paper ribbon loop: two open polygonal annuli, genuine interior.
    for sign in [-1,1]:
        points=[(.035,.61),(.13,.75),(.27,.77),(.32,.69),(.26,.60),(.10,.6)]
        vv=[]
        for y in [-.12,.07]:vv += [(sign*x*.80-y*.50,sign*x*.44+y*.86,z+(y+.12)*.65) for x,z in points]
        ff=[(i,(i+1)%6,(i+1)%6+6,i+6) for i in range(6)]
        lid.append(mesh(P,'open pink bow loop',vv,ff,K))
        for y in [-.121,.071]:
            vv=[]
            for scale in [1,.92]:vv += [(sign*(.16+(x-.16)*scale)*.80-y*.50,sign*(.16+(x-.16)*scale)*.44+y*.86,.69+(z-.69)*scale+(y+.12)*.65) for x,z in points]
            lid.append(mesh(P,'flat gold bow edging',vv,[(i,(i+1)%6,(i+1)%6+6,i+6) for i in range(6)],G))
        lid.append(P.prism('notched ribbon tail',[(0,.61),(sign*.25,.59),(sign*.21,.565),(sign*.24,.55),(sign*.07,.58)],.09,color=K))
    lid.append(P.box('bow knot',(.105,.12,.075),(0,-.005,.585),K))
    finish(P,s,st,[('lid',(0,.3,.465),lid)])
