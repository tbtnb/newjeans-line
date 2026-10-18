"""P24 Layered paper cloud. Size 3.5 x 1.2 x 2 m from spec; 300 tris; root, bob.
SIMPLIFICATIONS: top drawing is flatter than front/side, so top IoU is advisory per spec; seven folded 24-facet puff shells and a continuous scalloped back plate; no paper texture."""
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
        ob.matrix_world=Matrix.Identity(4);ob.data.update()
    moving=set(); roots=[]
    for name,joint,children in animated:
        roots.append(P.pivot(name,point(Vector(joint)),children)); moving.update(children)
    P.pivot('root',(0,0,0),[o for o in obs if o not in moving]+roots)

def folded_puff(P,name,x,z,rx,rz,depth,back,col):
    # Eight silhouette corners, eight offset creases and a forward apex: 24 flat facets; rear closes against the plate.
    vv=[(x+rx*math.cos(k*math.pi/4),back,z+rz*math.sin(k*math.pi/4)) for k in range(8)]
    vv += [(x+rx*.78*math.cos(k*math.pi/4+math.pi/8),back-depth*.74,z+rz*.78*math.sin(k*math.pi/4+math.pi/8)) for k in range(8)]
    vv += [(x,back-depth,z)]
    ff=[]
    for k in range(8):
        j=(k+1)%8
        ff += [(k,j,8+k),(j,8+j,8+k),(8+k,8+j,16)]
    return mesh(P,name,vv,ff,lambda p,n: '#F3F1EA' if col=='#FFFFFF' and (n.x>.25 or n.z<-.45) else col)

def build(P, spec):
    c=spec['colors']; pieces=[]
    # The continuous scalloped back is visible around each puff, not a rectangular side slab.
    outline=[(-1.75,.38),(-1.70,.69),(-1.49,.91),(-1.23,.93),
             (-1.13,1.24),(-.91,1.47),(-.67,1.49),(-.58,1.78),
             (-.24,1.97),(.11,2.0),(.43,1.84),(.64,1.49),
             (.93,1.50),(1.19,1.35),(1.29,.99),(1.50,1.02),
             (1.69,.86),(1.72,.62),(1.75,.51),(1.71,.24),
             (1.49,.15),(.72,.14),(.18,.12),(-.92,.20),(-1.53,.23)]
    plate=P.prism('scalloped thick layered paper backing',outline,.19,loc=(0,.42,0),color=c['pearl'])
    P.paint(plate,c['fog'],faces={f.index for f in plate.data.polygons if abs(f.normal.y)<.5})
    pieces.append(plate)
    # Arranged from rear to front; front masses and their overlaps follow the hero.
    puffs=[(-1.45,.64,.34,.35,.60,.38,'white'),
           (-.92,.99,.37,.45,.68,.38,'pearl'),
           (-.92,.35,.36,.25,.56,.38,'pearl'),
           (-.04,1.31,.61,.59,.86,.40,'white'),
           (.74,.86,.54,.51,.84,.40,'pearl'),
           (1.34,.49,.32,.34,.64,.40,'white'),
           (-.28,.49,.59,.49,1.02,.40,'white')]
    for k,(x,z,rx,rz,d,y,col) in enumerate(puffs):
        pieces.append(folded_puff(P,'creased paper puff '+str(k),x,z,rx,rz,d,y,c[col]))
    finish(P,spec,[('bob',(0,0,1),pieces)])
