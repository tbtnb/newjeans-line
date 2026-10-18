"""G4 item 5 Page strip road. Largest extent 2.2 m from spec; budget 40; root only.
SIMPLIFICATIONS: layered edge uses three page slabs; pink center stripe is geometry; paper curl reduced to one thin fold; three solid laminations replace fine page lines; front shows the long edge."""
BUDGET = 40

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
    L=spec['size_m'];W=L*.25
    for k in range(3):P.box('paper leaf layer'+str(k),(W,L,L*.012),loc=(0,0,k*L*.012),color='#FFF3DE')
    P.card('pink stripe',[(-W*.18,0),(W*.18,0),(W*.18,L),(-W*.18,L)],loc=(0,-L/2,L*.036),rot=(-90,0,0),color='#FF6FAE')
    # Folded end tab is one thin card, spanning the width.
    mesh(P,'folded page end',[(-W/2,-L/2,L*.036),(W/2,-L/2,L*.036),(W/2,-L/2-.045,L*.060),(-W/2,-L/2-.045,L*.060)],[(0,1,2,3)],'#F7D98B')
    finish(P,spec)
