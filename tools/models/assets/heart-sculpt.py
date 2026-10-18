"""P11 Heart sculpture. 1.2 x .52 x 1.58 m (+4% depth, -1.25% height to reconcile rounded sheet dimensions); 500 tris; root, heart.
SIMPLIFICATIONS: broad paper folds replace finer illustration facet network."""

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
    for y,k in [(0,1),(-d*.43,.91),(d*.43,.91)]:
        vv += [(loc[0]+x*k,loc[1]+y*min(1,.08+2.7*z/h,.35+3.0*(1-z/h)),loc[2]+h*.53+(z-h*.53)*k) for x,z in outline]
    vv += [(loc[0],loc[1]-d*.5,loc[2]+h*.55),(loc[0],loc[1]+d*.5,loc[2]+h*.55)]
    ff=[]
    for i in range(n):
        j=(i+1)%n
        ff += [(i,j,n+j),(i,n+j,n+i),(i,2*n+i,2*n+j),(i,2*n+j,j),(n+i,n+j,3*n),(2*n+j,2*n+i,3*n+1)]
    ob=mesh(P,name,vv,ff,col)
    import bmesh
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.subdivide_edges(bm,edges=[e for e in bm.edges if all(abs(v.co.y-loc[1])>.01 for v in e.verts)][:12],cuts=1,use_grid_fill=False);bm.to_mesh(ob.data);bm.free();P.paint(ob,col);return ob

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
    size=dict(s['size_m']);size['d']*=1.04;size['h']*=.9875; scale=Vector((size['w']/(hi.x-lo.x),size['d']/(hi.y-lo.y),size['h']/(hi.z-lo.z)))
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
    c=s['colors']; st=[]; parts=[]
    # Chamfered plinth built as stacked beveled rings, broad cream faces.
    for name,w0,d0,w1,d1,z0,z1,col in [('plinth',.83,.50,.70,.42,.02,.22,c['cream']),('lower gold rim',.84,.50,.83,.50,0,.022,c['gold']),('upper gold rim',.72,.43,.70,.42,.205,.221,c['gold'])]:
        vv=[(x*w/2,y*d/2,z) for w,d,z in [(w0,d0,z0),(w1,d1,z1)] for x,y in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        st.append(mesh(P,name,vv,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],col))
    st += [P.box('pedestal',(.20,.23,.22),(0,0,.21),c['cream']),P.box('capital',(.22,.22,.035),(0,0,.42),c['gold'])]
    parts.append(heart(P,'gold silhouette rim',1.2,1.15,.25,(0,0,.45),c['gold']))
    parts.append(heart(P,'faceted pink heart',1.155,1.11,.49,(0,-.005,.47),c['pink']))
    finish(P,s,st,[('heart',(0,0,1.02),parts)])
