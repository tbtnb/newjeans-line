"""G4 item 1 L-shaped paper road corner. Largest extent 2.2 m from spec; budget 20; root only.
SIMPLIFICATIONS: the front design is a second plan projection, so a level L-shaped tile cannot reproduce that front silhouette; hidden bottom and cut-end faces omitted for visible foil."""
BUDGET = 20

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
        ob.matrix_world=Matrix.Identity(4)
    moving=set(); roots=[]
    for name,joint,children in animated:
        roots.append(P.pivot(name,point(Vector(joint)),children)); moving.update(children)
    P.pivot('root',(0,0,0),[o for o in obs if o not in moving]+roots)

def build(P, spec):
    L=spec['size_m'];w=L*.47;h=L*.12;t=L*.055
    x0=-L/2;x1=L*.39;y0=-L/2;y1=L/2
    outline=[(x0+t,y0),(x0+t,y1-t),(x1,y1-t),(x1,y1-w+t),(x0+w-t,y1-w+t),(x0+w-t,y0)]
    vs=[(x,y,h) for x,y in outline]
    mesh(P,'cream L paper surface',vs,[tuple(range(6))],'#FFF3DE')
    strips=[[(x0,y0),(x0+t,y0),(x0+t,y1),(x0,y1)],[(x0,y1-t),(x1,y1-t),(x1,y1),(x0,y1)],[(x0+w-t,y0),(x0+w,y0),(x0+w,y1-w),(x0+w-t,y1-w+t)],[(x0+w-t,y1-w),(x1,y1-w),(x1,y1-w+t),(x0+w-t,y1-w+t)]]
    for i,points in enumerate(strips):mesh(P,'top gold foil fold'+str(i),[(x,y,h) for x,y in points],[(0,1,2,3)],'#F7D98B')
    edges=[((x0,y0),(x0,y1)),((x0,y1),(x1,y1)),((x0+w,y0),(x0+w,y1-w)),((x0+w,y1-w),(x1,y1-w))]
    for i,(a,b) in enumerate(edges):mesh(P,'paper edge'+str(i),[(a[0],a[1],0),(b[0],b[1],0),(b[0],b[1],h),(a[0],a[1],h)],[(0,1,2,3)],'#FFF3DE')
    finish(P,spec)
