"""G4 item 2 Folded gold foil edge trim. Largest extent 2.2 m from spec; budget 16; root only.
SIMPLIFICATIONS: open underside channel, crisp folded edges without microscopic foil texture; top cell contains neighboring corner pixels, so automatic top IoU is invalid."""
BUDGET = 16

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
    L=spec['size_m'];w=L*.088;h=w/5.35
    profile=[(-w/2,0),(-w/2,h*.86),(-w*.40,h),(w*.40,h),(w/2,h*.86),(w/2,0)]
    vs=[(x,y,z) for y in [-L/2,L/2] for x,z in profile];n=6
    # Open underside only; 8 cap tris + 8 side tris = 16.
    fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,i+1,i+1+n,i+n) for i in range(4)]
    mesh(P,'folded gold trim',vs,fs,'#F7D98B');finish(P,spec)
