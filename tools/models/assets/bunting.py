"""P21 Pennant string. Size 2.5 x 0.2 x 1 m from spec; 300 tris; root, flag.
SIMPLIFICATIONS: pennants share a rope pivot; side/top IoU unreliable per spec; front reference is cropped before the second post; side drawing contains another front projection; hero layout retained."""
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
    c=spec['colors']; gold=c['gold']; flags=[]
    for i,x in enumerate([-1.2,1.2]):
        P.box('square plinth'+str(i),(.16,.20,.045),loc=(x,0,0),color=gold)
        P.box('stepped foot'+str(i),(.11,.14,.04),loc=(x,0,.045),color=gold)
        P.cyl('post'+str(i),.025,.84,4,loc=(x,0,.08),color=gold)
        P.cyl('collar'+str(i),.04,.025,4,loc=(x,0,.91),color=gold)
        P.ico('faceted finial'+str(i),.06,loc=(x,0,.965),scale=(1,1,1.18),subdiv=1,color=gold)
    def sag(x):return .93-.15*(1-(x/1.2)**2)
    for i in range(7):
        x=-1.2+i*(2.4/7);rod(P,'sagging cord'+str(i),(x,0,sag(x)),(x+2.4/7,0,sag(x+2.4/7)),.006,gold,3)
    for i in range(8):
        x=-1.10+i*.285; z=sag(x)
        co=[c['magenta'],gold,c['cyan']][i%3]
        flags.append(mesh(P,'creased thick pennant'+str(i),[(x-.125,0,z),(x+.125,0,sag(x+.25)),(x-.01,-.018,z-.34),(x, -.018,z-.10),(x-.125,.008,z),(x+.125,.008,sag(x+.25)),(x-.01,-.010,z-.34)],[(0,3,2),(3,1,2),(4,6,5),(0,4,5,1),(0,2,6,4),(1,5,6,2)],co))
    finish(P,spec,[('flag',(0,0,.81),flags)])
