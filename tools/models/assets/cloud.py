"""P24 Layered paper cloud. Size 3.5 x 1.2 x 2 m from spec; 300 tris; root, bob.
SIMPLIFICATIONS: top drawing is flatter than front/side, so top IoU is advisory per spec; central puff is subdivision-2 ico, five peripheral puffs subdivision-1 to fit 300 tris; bright paper causes holes in the automatic design mask."""
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
    outline=[(-1.75,.18),(-1.73,.58),(-1.56,.82),(-1.31,.83),(-1.11,1.36),(-.78,1.39),(-.62,1.70),(-.34,1.93),(.07,2),(.44,1.88),(.69,1.54),(1.01,1.50),(1.26,1.26),(1.55,.87),(1.74,.56),(1.72,.18),(1.44,.26),(.80,.28),(.25,.20),(-.43,.20),(-1.05,.28),(-1.51,.25)]
    pieces.append(P.prism('scalloped pale backing',outline,.20,loc=(0,.16,0),color=c['fog']))
    puffs=[(-1.42,-.06,.55,.35,.46),(-.94,-.06,.95,.38,.49),(-.12,-.08,1.30,.64,.70),(-.32,-.08,.48,.57,.51),(.79,-.08,.81,.53,.58),(1.39,-.04,.39,.31,.38)]
    for k,(x,y,z,rx,rz) in enumerate(puffs):
        pieces.append(P.ico('layered geodesic puff'+str(k),1,loc=(x,y,z),scale=(rx,.33,rz),subdiv=2 if k==2 else 1,color=c['white'] if k in [0,2,4] else c['pearl']))
    finish(P,spec,[('bob',(0,0,1),pieces)])
