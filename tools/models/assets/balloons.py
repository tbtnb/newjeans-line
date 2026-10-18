"""P19 Balloon bunch. Size spec.size_m 2 x 1.2 x 3.5 m; 500 tris; root, swing.
SIMPLIFICATIONS: three balloons share one swing pivot; strings are triangular rods; inflation uses five polygonal belts and large triangulated facets; one visible gold fold seam; shared blush #FFC7DA inner ears follow the faces-pass pink-ear direction; cyan bunny identity retained; shared navy #1F2350 flat eyes and spec pink nose; the official mask fills string-enclosed air."""
BUDGET = 500

import math
import bpy
import bmesh
from mathutils import Vector, Matrix

def mesh(P, name, verts, faces, color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free(); me.update()
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
        ob.matrix_world=Matrix.Identity(4);ob.data.update()
    moving=set(); roots=[]
    for name,joint,children in animated:
        roots.append(P.pivot(name,point(Vector(joint)),children)); moving.update(children)
    P.pivot('root',(0,0,0),[o for o in obs if o not in moving]+roots)

def face_patch(P, head, name, outline, color):
    """Clip a flat mark to actual front facets; lift 12 mm along each face normal.

    Dissolving coplanar subdivision edges keeps the entire face below 40 tris.
    Coordinates are in world XZ before the asset's final size normalization.
    """
    import bmesh
    bpy.context.view_layer.update()
    bm = bmesh.new(); bm.from_mesh(head.data); bm.transform(head.matrix_world)
    bm.normal_update()
    bmesh.ops.dissolve_limit(bm, angle_limit=1e-5, verts=list(bm.verts), edges=list(bm.edges))
    bm.normal_update()
    def clip(poly, a, b):
        out = []
        for u, v in zip(poly, poly[1:] + poly[:1]):
            du = (b[0]-a[0])*(u.z-a[1]) - (b[1]-a[1])*(u.x-a[0])
            dv = (b[0]-a[0])*(v.z-a[1]) - (b[1]-a[1])*(v.x-a[0])
            if du >= -1e-8: out.append(u)
            if (du >= 0) != (dv >= 0): out.append(u + (v-u)*(du/(du-dv)))
        return out
    if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(outline,outline[1:]+outline[:1])) < 0:
        outline = outline[::-1]
    # One tangent-normal offset per mark keeps shared crease vertices together.
    # Offsetting every clipped fragment by a different normal opens visible seams.
    from mathutils.bvhtree import BVHTree
    cx = sum(p[0] for p in outline)/len(outline)
    cz = sum(p[1] for p in outline)/len(outline)
    origin = Vector((cx,min(v.co.y for v in bm.verts)-1,cz))
    _, normal, _, _ = BVHTree.FromBMesh(bm).ray_cast(origin,Vector((0,1,0)))
    lift = (normal if normal is not None else Vector((0,-1,0)))*.012
    verts = []; faces = []
    for f in bm.faces:
        if f.normal.y >= -.05: continue
        poly = [v.co.copy() for v in f.verts]
        for a,b in zip(outline,outline[1:]+outline[:1]):
            poly = clip(poly,a,b)
            if not poly: break
        if len(poly) >= 3:
            start = len(verts)
            verts.extend([tuple(v + lift) for v in poly])
            faces.append(tuple(range(start,len(verts))))
    bm.free()
    return mesh(P,name,verts,faces,color)

def build(P, spec):
    c=spec['colors']; gold=c['gold']; moving=[]
    # An angular heart with a pronounced valley and a ridge running to its lower point.
    outline=[(-.99,2.68),(-.96,2.86),(-.79,3.00),(-.57,3.03),(-.39,2.94),(-.25,3.04),(-.05,3.07),(.12,2.94),(.17,2.75),(.09,2.51),(-.13,2.30),(-.40,2.10),(-.68,2.29),(-.88,2.48)]
    n=len(outline); cx=-.41;cz=2.65
    verts=[(x,-.02,z) for x,z in outline]
    verts += [(cx+(x-cx)*.77,-.43,cz+(z-cz)*.77) for x,z in outline]
    verts += [(cx,-.57,cz),(cx,.34,cz)]
    faces=[]
    for i in range(n):
        j=(i+1)%n
        faces.extend([(i,j,n+j),(i,n+j,n+i),(n+i,n+j,2*n),(j,i,2*n+1)])
    moving.append(mesh(P,'gem heart balloon with broad paper creases',verts,faces,lambda p,n:c['pink'] if n.z>.43 and n.x<.4 else c['magenta']))
    def angular_balloon(name,loc,scale,col):
        profile=[(0,-1),(.58,-.81),(.94,-.35),(1,.14),(.82,.66),(.42,.93),(0,1)]
        ob=P.lathe(name,profile,8,loc=loc,color=col,rot=(0,0,22.5))
        # Triangulate the coarse rings explicitly; no smoothing or subdivision.
        bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=bm.faces,quad_method='ALTERNATE');bm.to_mesh(ob.data);bm.free()
        for i,v in enumerate(ob.data.vertices):
            if abs(v.co.z)<.95:
                v.co.z+=.022*(1 if i%2 else -1)
            v.co.x*=scale[0];v.co.y*=scale[1];v.co.z*=scale[2]
        ob.data.update();P.paint(ob,col);return ob
    moving.append(angular_balloon('creased octagonal pink balloon',(.05,.27,2.01),(.39,.40,.43),c['pink']))
    head=angular_balloon('creased octagonal blue bunny head',(.59,-.025,2.48),(.43,.44,.41),c['cyan']); moving.append(head)
    for sign in (-1,1):
        moving.append(face_patch(P,head,'face_eye_'+str(sign),P.ellipse(.022,.030,6,cx=.59+sign*.155,cz=2.51),'#1F2350'))
    moving.append(face_patch(P,head,'face_nose',[(.545,2.43),(.59,2.39),(.635,2.43)],c['pink']))
    for i,(x,ang) in enumerate([(.36,-12),(.80,18)]):
        moving.append(P.lathe('inflated bunny ear'+str(i),[(0,0),(.09,.10),(.15,.38),(.105,.60),(0,.75)],4,loc=(x,.01,2.79),rot=(-25,ang,0),color=c['cyan']))
        vv=[(-.05,-.11,.14),(.05,-.11,.14),(.07,-.15,.43),(0,-.11,.64),(-.06,-.15,.44),(0,-.165,.40)]
        ob=mesh(P,'creased blush inner ear panel'+str(i),vv,[(k,(k+1)%5,5) for k in range(5)],'#FFC7DA')
        ob.location=(x,.01,2.79);ob.rotation_euler=tuple(math.radians(v) for v in (-25,ang,0));moving.append(ob)
    for i,p in enumerate([(-.40,-.06,2.10),(.05,.28,1.60),(.59,-.025,2.07)]):
        moving.append(P.cyl('inflation knot'+str(i),.060,.095,4,loc=(p[0],p[1],p[2]-.085),r2=.025,color=[c['magenta'],c['pink'],c['cyan']][i]))
        moving.append(rod(P,'converging golden string'+str(i),(0,0,.40),(p[0],p[1],p[2]-.075),.011,gold,3))
    seam=[(-.82,-.20,2.87),(-.76,-.40,2.69),(-.64,-.45,2.44),(-.40,-.33,2.14)]
    for i,(a,b) in enumerate(zip(seam,seam[1:])):
        ob=rod(P,'fine gold heart fold seam'+str(i),a,b,.0045,gold,3);moving.append(ob)
    P.lathe('gold faceted weight',[(.18,0),(.22,.08),(.21,.24),(.09,.34),(.055,.40),(0,.42)],6,color=gold)
    finish(P,spec,[('swing',(0,0,.40),moving)])
