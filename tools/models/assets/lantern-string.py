"""P10 Lantern string. 4.1 x .4 x 2 m; 900 tris; root, swing left/right lantern groups.
SIMPLIFICATIONS: seven lanterns grouped into two swing pivots to respect prop draw-call limit; light represented by lamp color."""

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
    for y,k in [(0,1),(-d*.42,.90),(d*.42,.90)]:
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
    c=s['colors']; st=[]; left=[];right=[]
    for x in [-1.88,1.88]:
        st.append(P.box('square foot',(.36,.37,.04),(x,0,0),c['gold']))
        base=P.cyl('tapered foot',.19,.12,4,loc=(x,0,.04),color=c['lavender'],r2=.075,rot=(0,0,45));st.append(base)
        st.append(P.cyl('post',.055,1.68,6,loc=(x,0,.15),color=c['lavender']))
        st += [P.cyl('post collar',.065,.06,8,loc=(x,0,1.81),color=c['gold']),P.cyl('pointed cap',.085,.12,4,loc=(x,0,1.87),color=c['gold'],r2=0)]
    points=[(-1.88+3.76*i/8,0,1.64+.21*((-1.88+3.76*i/8)/1.88)**2) for i in range(9)]
    st.append(ring(P,'sagging gold cord',points,.012,c['gold'],4))
    for i,x in enumerate([-1.5,-1,-.5,0,.5,1,1.5]):
        g=left if i<3 else right;top=1.64+.21*(x/1.88)**2;z=top-.40
        g.append(beam(P,'gold hanger',(x,0,z+.12),(x,0,top),.01,c['gold'],4))
        if i in [0,3,6]:
            ob=P.lathe('ribbed round lavender lantern',[(0,-.24),(.13,-.22),(.22,-.13),(.245,.0),(.22,.15),(.10,.23),(0,.24)],8,loc=(x,0,z),color=c['lavender']); P.paint(ob,lambda p,n:c['lamp'] if p.z<-.18 else (c['pink'] if abs(n.x)>.85 else c['lavender']));g.append(ob)
            g.append(P.cyl('warm lower tassel',.045,.04,6,loc=(x,0,z-.26),color=c['lamp']))
        elif i in [1,5]:g.append(heart(P,'pink heart lantern',.51,.52,.36,(x,0,z-.32),c['pink']))
        else:g.append(puffstar(P,'gold star lantern',.31,.44,(x,0,z-.14),c['gold']))
    finish(P,s,st,[('swing0',(-.95,0,1.75),left),('swing1',(.75,0,1.75),right)])
