"""P18 Curved paper stairs. 2 x 1.9 x 2 m; 400 tris; root only.
SIMPLIFICATIONS: six curved steps and four balusters replace very fine paper seams."""

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
    c=s['colors'];st=[];n=6;segments=2
    def bounds(t):return -.96+.63*t, .96-1.25*t*t
    def edge(i,j):
        t=i/n; l,r=bounds(t);q=j/segments
        return l+(r-l)*q,-.91+1.82*t-.09*(1-(2*q-1)**2)
    for i in range(n):
        z=(i+1)*.225;front=[edge(i,j) for j in range(segments+1)];back=[edge(i+1,j) for j in range(segments+1)];N=segments+1
        vv=[(x,y,z) for x,y in front+back]+[(x,y,0) for x,y in front+back]
        ff=[]
        for j in range(segments):ff += [(j,j+1,N+j+1,N+j),(2*N+j,2*N+j+1,j+1,j)]
        ff += [(0,N,3*N,2*N),(segments,2*N+segments,3*N+segments,N+segments)]
        st.append(mesh(P,'curved lilac stair',vv,ff,c['lilac']))
        st.append(mesh(P,'white tread',[(x,y,z+.004) for x,y in front+back],[(j,j+1,N+j+1,N+j) for j in range(segments)],c['white']))
        vv=[(x,y,z+.009) for x,y in front]+[(x,y+.022,z+.009) for x,y in front]
        st.append(mesh(P,'gold nosing',vv,[(j,j+1,N+j+1,N+j) for j in range(segments)],c['gold']))
    # Both folded stringer walls support the flight; left follows its tapered edge.
    for side in [0,1]:
        vv=[]
        for j in range(7):
            q=j/6;x=bounds(q)[side]+(-.055 if side==0 else .025);y=-.91+1.82*q;zz=.33+1.35*(.87*q+.13*q*q)
            vv += [(x,y,0),(x,y,zz),(x+(.12 if side==0 else .065),y,zz),(x+(.12 if side==0 else .065),y,0)]
        ff=[]
        for j in range(6):
            a=j*4;b=(j+1)*4;ff += [(a,a+1,b+1,b),(a+1,a+2,b+2,b+1),(a+2,a+3,b+3,b+2)]
        ff += [(0,3,2,1),(24,25,26,27)]
        st.append(mesh(P,'folded stair stringer',vv,ff,c['lilac']))
    rail=[]
    for j in range(7):
        q=j/6;x=bounds(q)[1]+.045;rail.append((x,-.91+1.82*q,.62+1.35*(.68*q+.32*q*q)))
    st.append(ring(P,'curved handrail',rail,.042,c['lilac'],4))
    vv=[(x-.025,y,z+.042) for x,y,z in rail]+[(x+.025,y,z+.042) for x,y,z in rail]
    st.append(mesh(P,'gold handrail stripe',vv,[(j,j+1,8+j,7+j) for j in range(6)],c['gold']))
    for j in range(4):
        q=j/3;x=bounds(q)[1]+.045;y=-.91+1.82*q;lo=.33+1.35*(.87*q+.13*q*q);hi=.62+1.35*(.68*q+.32*q*q)
        st.append(P.box('baluster',((.11 if j in [0,3] else .065),(.11 if j in [0,3] else .065),hi-lo),(x,y,lo),c['lilac']))
        if j in [0,3]:st.append(P.box('gold post cap',(.105,.105,.025),(x,y,hi+.025),c['gold']))
    finish(P,s,st)
