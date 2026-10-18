"""P24 Layered paper cloud. Size 3.5 x 1.2 x 2 m from spec; 300 tris; root, bob.
SIMPLIFICATIONS: top drawing is flatter than front/side, so top IoU is advisory per spec; eight overlapping puffs (one subdivision-2, seven subdivision-1) fit the 300-triangle budget; thin polygonal back plate; no paper texture."""
BUDGET = 300

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
    c=spec['colors']; pieces=[]
    # A thin paper back plate joins eight overlapping faceted puffs.
    outline=[(-1.75,.15),(-1.75,.65),(-1.30,.85),(-1.05,1.40),
             (-.70,1.35),(-.40,1.94),(.10,2),(.50,1.84),
             (.70,1.40),(1.20,1.35),(1.72,.62),(1.70,.15)]
    pieces.append(P.prism('thin scalloped paper back plate',outline,.12,
                          loc=(0,.25,0),color=c['pearl'],side_color=c['fog']))
    puffs=[
        (-1.43,-.07,.53,.36,.29,.38,'white'),
        (-.94,-.10,.98,.41,.33,.46,'pearl'),
        (-1.01,-.11,.29,.35,.29,.27,'pearl'),
        (-.10,-.09,1.30,.60,.40,.66,'white'),
        (-.38,-.18,.50,.56,.43,.50,'white'),
        (.77,-.11,.84,.61,.36,.57,'pearl'),
        (1.36,-.05,.43,.34,.28,.35,'white'),
        (.66,-.05,.30,.45,.29,.29,'pearl'),
    ]
    for k,(x,y,z,rx,ry,rz,col) in enumerate(puffs):
        ob=P.ico('overlapping geodesic puff'+str(k),1,loc=(x,y,z),
                 scale=(rx,ry,rz),subdiv=2 if k==3 else 1,
                 rot=(0,0,0),color=c[col])
        for v in ob.data.vertices:
            if v.co.z+z < .12: v.co.z=.12-z
        pieces.append(ob)
    finish(P,spec,[('bob',(0,0,1),pieces)])
