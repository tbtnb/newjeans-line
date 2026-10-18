"""P24 Layered paper cloud. Size 3.5 x 1.2 x 2 m from spec; 300 tris; root, bob.
SIMPLIFICATIONS: top drawing is flatter than front/side, so top IoU is advisory per spec; seven folded 24-facet puff shells and a curved scalloped back plate, without paper texture."""
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
    # Broad triangular creases with a blunt front crown, never a conical spike.
    n=8
    vv=[(x+rx*math.cos(k*math.tau/n),back,z+rz*math.sin(k*math.tau/n)) for k in range(n)]
    vv += [(x+rx*.84*math.cos(k*math.tau/n+math.pi/n),back-depth*.90,z+rz*.84*math.sin(k*math.tau/n+math.pi/n)) for k in range(n)]
    vv += [(x-rx*.10,back-depth,z+rz*.08)]
    ff=[]
    for k in range(n):
        j=(k+1)%n
        ff += [(k,j,n+k),(j,n+j,n+k),(n+k,n+j,2*n)]
    return mesh(P,name,vv,ff,lambda p,n: '#F3F1EA' if col=='#FFFFFF' and (n.x>.25 or n.z<-.45) else col)

def build(P, spec):
    c=spec['colors']; pieces=[]
    # Trace the actual scalloped paper rim. Its back curves in plan, as on the hero.
    pixels=[(0,274),(23,214),(65,161),(97,161),(116,126),(173,100),
      (195,106),(228,51),(284,20),(349,16),(405,46),(445,121),
      (490,117),(525,135),(552,207),(576,206),(614,260),(638,300),
      (628,339),(606,358),(317,373),(267,378),(176,345),
      (137,348),(102,333),(18,322)]
    outline=[((u-319)*3.5/638,(378-v)*2/362) for u,v in pixels]
    vv=[]
    for layer in (0,1):
        for x,z in outline:
            y=.16+.48*(1-(abs(x)/1.76)**1.5)
            vv.append((x,y-.13 if layer==0 else y,z))
    n=len(outline)
    ff=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    ff += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    plate=mesh(P,'scalloped curved paper back plate',vv,ff,c['pearl'])
    P.paint(plate,c['fog'],faces={f.index for f in plate.data.polygons if abs(f.normal.y)<.45})
    pieces.append(plate)
    # Seven polygonal puff shells; dimensions taken from their front-view boundaries.
    puffs=[(67,251,54,57,.66,.28,'white'),
           (163,203,61,72,.70,.38,'pearl'),
           (143,311,51,34,.63,.34,'pearl'),
           (310,143,107,96,.81,.43,'white'),
           (445,239,88,87,.88,.36,'pearl'),
           (555,292,53,55,.65,.27,'white'),
           (272,288,103,88,1.02,.30,'white')]
    for k,(u,v,rx,rz,d,y,col) in enumerate(puffs):
        pieces.append(folded_puff(P,'folded paper puff '+str(k),(u-319)*3.5/638,(378-v)*2/362,rx*3.5/638*1.08,rz*2/362*(1.02 if k==6 else 1.08),d,y,c[col]))
    finish(P,spec,[('bob',(0,0,1),pieces)])
