"""P09 Pull tab. 1.9 x .3 x 1.2 m; 300 tris; root, bob slider.
SIMPLIFICATIONS: tiny engraved seams omitted; slider uses bob motion supported by engine."""

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
    c=s['colors']; C,G,R=c['cream'],c['gold'],c['coral']; st=[]; moving=[]
    st.append(P.box('cream rail',(1.42,.28,.145),(.22,0,0),C))
    st.append(P.box('rail gold edge',(1.44,.29,.018),(.22,0,.14),G))
    moving.append(P.box('coral slider',(1.5,.13,.105),(.02,-.005,.15),R))
    for x in [-.25,.3]:
        st.append(P.box('slider guide',(.14,.27,.16),(x,0,.14),C))
        st.append(P.box('guide edge',(.018,.275,.205),(x-.065,0,.11),G))
    for r,d,col in [(.19,.15,R),(.164,.155,G),(.145,.16,C)]:
        moving.append(P.cyl('round pull handle',r,d,8,loc=(-.87,d/2,.205),color=col,rot=(90,0,0)))
    # Folded linkage at rear right, seen as alternating diagonal bands.
    joints=[(.70,.01,.11),(.70,-.02,.35),(.89,.065,.51),(.78,.04,.67),(.73,-.07,.87)]
    for i,(a,b) in enumerate(zip(joints,joints[1:])):
        st.append(beam(P,'folded thick paper link',a,b,.075,C,4))
    ol=[(-.34,0),(.26,-.08),(.34,0),(.34,.53),(.27,.60),(-.33,.66),(-.4,.59),(-.4,.08)]
    for k,dep,col,y in [(1,.12,R,-.07),(.96,.003,G,-.134),(.90,.003,C,-.139)]:
        st.append(P.prism('raised display plate',[(x*k,z*k) for x,z in ol],dep,loc=(.43,y,.53),color=col) if k==1 else P.card('cream inset',[(x*k,z*k) for x,z in ol],loc=(.43,y-.004,.53),color=col))
    finish(P,s,st,[('bob',(0,0,.15),moving)])
