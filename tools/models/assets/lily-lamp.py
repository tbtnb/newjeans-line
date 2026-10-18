"""P13 Lily lantern. 1.1 x 1.1 x .8 m; 500 tris; root, pulse flower.
SIMPLIFICATIONS: glow encoded in lamp palette; petal veins omitted."""

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
    c=s['colors']; st=[]; petals=[]
    # Three separate notched pads with folded triangulated top surfaces.
    for i,(x,y,r,a) in enumerate([(0,-.12,.46,-90),(-.34,.16,.22,-145),(.34,.2,.22,-40)]):
        ol=[]
        for j in range(14):
            ang=math.radians(a)+2*math.pi*j/14;rr=.70*r if j==0 else r;ol.append((x+rr*math.cos(ang),y+rr*math.sin(ang)))
        vv=[(x,y,.29)]+[(a,b,.13+(.025 if b>y else 0)) for a,b in ol]+[(x+(a-x)*.92,y+(b-y)*.92,.015+.07*((a-x)/r)**2) for a,b in ol];n=len(ol)
        ff=[(0,j+1,(j+1)%n+1) for j in range(n)]+[(j+1,n+j+1,n+(j+1)%n+1,(j+1)%n+1) for j in range(n)]
        st.append(mesh(P,'notched mint lily pad',vv,ff,c['mint']))
    for layer,(count,radius,height,col) in enumerate([(12,.34,.60,c['blush']),(6,.24,.49,c['pearl'])]):
        for i in range(count):
            a=2*math.pi*i/count+layer*.38; hh=height*(.92+.08*math.cos(4*a)); u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0));base=Vector((0,0,.16))
            # Cup petal: pointed tip, broad shoulders, convex paper crease.
            local=[(0,.17,0),(-.17,radius*.87,height*.25),(-.12,radius*1.06,height*.66),(0,radius*1.02,height),(.12,radius*1.06,height*.66),(.17,radius*.87,height*.25),(0,radius*1.06,height*.40)]
            vv=[tuple(base+v*x+u*y+Vector((0,0,z*hh/height))) for x,y,z in local]
            ff=[(6,j,(j+1)%6) for j in range(6)]
            petals.append(mesh(P,'folded lotus petal',vv,ff,col))
    # Low outer whorl supplies the rounded bowl seen below the tall back petals.
    for i in range(8):
        a=2*math.pi*(i+.5)/8;u=Vector((math.cos(a),math.sin(a),0));v=Vector((-math.sin(a),math.cos(a),0))
        local=[(0,.17,.17),(-.14,.30,.20),(-.13,.37,.36),(0,.39,.46),(.13,.37,.36),(.14,.30,.20),(0,.38,.27)]
        vv=[tuple(v*x+u*y+Vector((0,0,z))) for x,y,z in local]
        petals.append(mesh(P,'lower cupped blush petal',vv,[(6,j,(j+1)%6) for j in range(6)],c['blush']))
    petals.append(P.lathe('warm faceted lamp',[(0,.11),(.12,.12),(.17,.27),(.09,.46),(.045,.48),(0,.48)],12,color=c['lamp']))
    petals.append(P.cyl('lamp collar',.055,.025,10,loc=(0,0,.55),color=c['lamp']))
    finish(P,s,st,[('pulse',(0,0,.23),petals)])
