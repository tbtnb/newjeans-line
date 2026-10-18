"""P16 Heart flower bed. 1.8 x 1 x .9 m; 800 tris; root, pulse0/1 staggered flowers.
SIMPLIFICATIONS: nine flower heads use two staggered pulse groups; planter uses specified lavender instead of off-palette illustrated cream."""

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
    c=s['colors']; st=[]; g=[[],[]]
    st.append(P.prism('lavender planter',[(-.84,0),(.84,0),(.90,.04),(.90,.14),(.84,.18),(-.84,.18),(-.90,.14),(-.90,.04)],1,loc=(0,0,0),color=c['lavender']))
    st.append(P.box('mint growing bed',(1.72,.92,.035),(0,0,.16),c['mint']))
    for x in [-.88,.88]:st.append(P.box('raised rim side',(.04,1,.055),(x,0,.15),c['lavender']))
    for y in [-.48,.48]:st.append(P.box('raised rim front',(1.8,.04,.055),(0,y,.15),c['lavender']))
    for row in range(3):
        for col in range(3):
            i=row*3+col;x=(col-1)*.56+(row-1)*.12;y=(row-1)*.21;z=[.40,.60,.47,.56,.47,.67,.49,.61,.54][i]
            st.append(P.cyl('mint stem',.022,z-.18,6,loc=(x,y,.18),color=c['mint']))
            for sign in [-1,1]:st.append(P.blade('creased mint leaf',.24,.46,loc=(x+sign*.035,y,.22),color=c['mint'],rot=(sign*25,sign*43,(row-1)*32),bend=.20))
            for sign in [-1,1]:st.append(P.blade('upper folded leaf',.29,.44,loc=(x,y,z-.20),color=c['mint'],rot=(sign*62,sign*35,75),bend=.3))
            # Twelve-point faceted outline; low triangulation concentrated in nine heads.
            ol=[(-.16,.18),(-.16,.28),(-.08,.32),(0,.26),(.08,.32),(.16,.28),(.16,.18),(0,0)]
            vv=[(x+a,y,z+b) for a,b in ol]+[(x,y-.17,z+.17),(x,y+.17,z+.17)];n=len(ol)
            ff=[(j,(j+1)%n,n) for j in range(n)]+[((j+1)%n,j,n+1) for j in range(n)]
            ob=mesh(P,'faceted heart flower',vv,ff,[c['coral'],c['pink'],c['lavender']][(row+col)%3]);g[i%2].append(ob)
            # Turn alternating flowers towards the side while maintaining the heart profile.
            if i%3==1:
                angle=math.radians(40)
                for v in ob.data.vertices:
                    xx,yy=v.co.x-x,v.co.y-y;v.co.x=x+xx*math.cos(angle)-yy*math.sin(angle);v.co.y=y+xx*math.sin(angle)+yy*math.cos(angle)
    # Keep foliage inside the planter; spreading leaves must not shrink the entire bed during sizing.
    bpy.context.view_layer.update()
    for ob in st:
        if 'leaf' in ob.name:
            mw=ob.matrix_world.copy();inv=mw.inverted()
            for v in ob.data.vertices:
                w=mw@v.co;w.x=max(-.86,min(.86,w.x));w.y=max(-.45,min(.45,w.y));v.co=inv@w
    finish(P,s,st,[('pulse0',(-.1,0,.6),g[0]),('pulse1',(.1,0,.6),g[1])])
