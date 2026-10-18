"""P17 Star mobile. 1.7 x 1.4 x 2.5 m; 600 tris; root, spin0/1 pendant groups.
SIMPLIFICATIONS: five pendants share two rotation banks; open hoop and suspension triangle remain open despite filled design masks; crescent uses diamond folds; tiny beads simplified to octahedra."""

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
        ob.matrix_world=Matrix.Identity(4);ob.data.update()
    piv=[]
    for name,joint,children in groups:piv.append(P.pivot(name,tf(Vector(joint)),children))
    P.pivot('root',(0,0,0),static+piv)

def build(P,s):
    c=s['colors']; st=[];g=[[],[]];R=.72;z=1.54
    # Flat polygonal annulus, open in its centre.
    n=12;vv=[]
    for h,r in [(z-.115,R-.01),(z+.055,R),(z-.115,R-.085),(z+.055,R-.075)]:vv += [(r*math.cos(2*math.pi*i/n),r*math.sin(2*math.pi*i/n),h) for i in range(n)]
    # Each outside panel folds out to a middle ridge, giving the lilac band sharp triangular planes.
    for i in range(n):
        a=2*math.pi*(i+.5)/n;vv.append(((R+.012)*math.cos(a),(R+.012)*math.sin(a),z-.03))
    ff=[]
    for i in range(n):
        j=(i+1)%n;mid=4*n+i
        ff += [(i,j,mid),(j,n+j,mid),(n+j,n+i,mid),(n+i,i,mid),
               (2*n+i,3*n+i,3*n+j,2*n+j),(n+i,n+j,3*n+j,3*n+i),(i,2*n+i,2*n+j,j)]
    st.append(mesh(P,'open lilac hoop',vv,ff,c['lilac']))
    rim=[(R*math.cos(2*math.pi*i/n),R*math.sin(2*math.pi*i/n),z+.057) for i in range(n)]+[((R-.022)*math.cos(2*math.pi*i/n),(R-.022)*math.sin(2*math.pi*i/n),z+.057) for i in range(n)]
    st.append(mesh(P,'gold rim line',rim,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],c['gold']))
    for a in [math.pi/6,5*math.pi/6,3*math.pi/2]:
        st.append(beam(P,'suspension cord',(R*math.cos(a),R*math.sin(a),z+.04),(0,0,2.32),.012,c['gold'],3))
    st.append(beam(P,'ceiling thread',(0,0,2.32),(0,0,2.55),.012,c['gold'],3));st.append(P.ico('gold hanger bead',.065,loc=(0,0,2.32),color=c['gold']))
    for sign in [-1,1]:
        ol=[(-.08,0),(-.17,.20),(-.17,.46),(-.09,.72),(.075,.60),(.16,.33),(.10,.10)]
        # Real bevelled cream border and a recessed lilac face, bounded by gold foil.
        vv=[]
        for k,yy in [(1,0),(.70,-.085),(.66,-.082),(1,.09)]:
            vv += [(x*k,yy,.34+(zz-.34)*k) for x,zz in ol]
        ff=[]
        for i in range(7):
            j=(i+1)%7;ff.append((i,j,7+j,7+i))
        for i in range(7):
            j=(i+1)%7;ff.append((7+i,7+j,14+j,14+i))
        ff.append(tuple(range(14,21)))
        for i in range(7):
            j=(i+1)%7;ff.append((j,i,21+i,21+j))
        ff.append(tuple(reversed(range(21,28))))
        ear=mesh(P,'bevelled cream bunny ear',vv,ff,c['cream'])
        P.paint(ear,c['gold'],faces=set(range(7,14)));P.paint(ear,c['lilac'],faces={14})
        ear.location=(sign*.50,.38,z+.04);ear.rotation_euler=tuple(math.radians(v) for v in (-14,sign*24,sign*-10));st.append(ear)
    for i,(a,h,r) in enumerate([(-math.pi/2,.48,.38),(-math.pi,.75,.25),(0,.75,.25),(-2.16,.13,.18),(-.98,.11,.23)]):
        x,y=R*math.cos(a),R*math.sin(a)
        q=.042;zz=h+r+.07;vv=[(x+q,y,zz),(x,y+q,zz),(x-q,y,zz),(x,y-q,zz),(x,y,zz+.065),(x,y,zz-.065)]
        g[i%2].append(mesh(P,'pendant diamond bead',vv,[(j,(j+1)%4,4) for j in range(4)]+[((j+1)%4,j,5) for j in range(4)],c['gold']))
        g[i%2].append(beam(P,'pendant thread',(x,y,z-.04),(x,y,h+r),.011,c['gold'],3))
        if i==4:
            # Diamond sections along a curved crescent create large folded gold planes.
            outer=[(-.07,.30),(.08,.21),(.18,.07),(.18,-.09),(.10,-.23),(-.05,-.29),(-.22,-.24)]
            inner=[(-.07,.30),(-.015,.17),(.02,.04),(-.015,-.09),(-.09,-.16),(-.16,-.20),(-.22,-.24)]
            vv=[(x+outer[0][0],y,h+outer[0][1])]
            for j in range(1,6):
                a,b=outer[j],inner[j];mx=(a[0]+b[0])/2;mz=(a[1]+b[1])/2
                vv += [(x+a[0],y,h+a[1]),(x+mx,y-.105,h+mz),(x+b[0],y,h+b[1]),(x+mx,y+.105,h+mz)]
            vv.append((x+outer[-1][0],y,h+outer[-1][1]));ff=[]
            for j in range(4):ff.append((0,1+j,1+(j+1)%4))
            for k in range(4):
                for j in range(4):ff.append((1+4*k+j,1+4*k+(j+1)%4,5+4*k+(j+1)%4,5+4*k+j))
            for j in range(4):ff.append((17+j,21,17+(j+1)%4))
            g[i%2].append(mesh(P,'folded crescent with convex gold facets',vv,ff,c['gold']))
        else:g[i%2].append(puffstar(P,'dimensional paper star',r,.30 if i==0 else .21,(x,y,h),c['gold']))
    for i,a in enumerate([-math.pi/2,-math.pi,0,-2.16,-.98]):
        x,y=R*math.cos(a),R*math.sin(a)
        q=.035;h=z-.04;vv=[(x+q,y,h),(x,y+q,h),(x-q,y,h),(x,y-q,h),(x,y,h+.07),(x,y,h-.07)];st.append(mesh(P,'diamond hoop fitting',vv,[(j,(j+1)%4,4) for j in range(4)]+[((j+1)%4,j,5) for j in range(4)],c['gold']))
    finish(P,s,st,[('spin0',(0,0,z),g[0]),('spin1',(0,0,z),g[1])])
