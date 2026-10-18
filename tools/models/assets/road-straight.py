"""G4 item 0 Cream paper road. Largest extent spec.size_m=2.2 m; budget 12; root only.
SIMPLIFICATIONS: top foil is two narrow faces; hidden underside and back cut-end omitted to retain the 12-triangle budget; front drawing shows the long edge."""
BUDGET = 12

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
    L=spec['size_m'];W=L*.35;H=W/.315* .10
    # Eight boundary vertices on top allow three colour faces while keeping a 12-triangle shell: bottom omitted.
    xs=[-W/2,-W*.37,W*.37,W/2];vs=[(x,y,z) for z in [0,H] for y in [-L/2,L/2] for x in xs]
    fs=[(8+i,8+i+1,12+i+1,12+i) for i in range(3)]+[(0,8,11,3),(0,4,12,8),(3,11,15,7)]
    ob=mesh(P,'cream road gold top borders',vs,fs,'#FFF3DE')
    P.paint(ob,'#F7D98B',faces={0,2});finish(P,spec)
