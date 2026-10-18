"""P21 Pennant string. Size 2.5 x 0.2 x 1 m from spec; 300 tris; root, flag.
SIMPLIFICATIONS: nine pennants share one flag pivot; both end posts retained from hero; cropped front and composite side drawing cannot give complete-model IoU; side/top are thin per spec."""
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
        P.cyl('tapered plinth step'+str(i),.078,.045,4,loc=(x,0,.045),r2=.052,rot=(0,0,45),color=gold)
        P.box('square gold post'+str(i),(.049,.049,.83),loc=(x,0,.09),color=gold)
        P.box('finial collar'+str(i),(.075,.075,.025),loc=(x,0,.91),color=gold)
        mesh(P,'faceted gold finial'+str(i),[(x-.06,0,.965),(x,.06,.965),(x+.06,0,.965),(x,-.06,.965),(x,0,1.035),(x,0,.93)],[(j,(j+1)%4,4) for j in range(4)]+[((j+1)%4,j,5) for j in range(4)],gold)
    # Broad flags follow a shallow catenary; attachment points use each flag edge.
    def sag(x):return .92-.22*(1-(x/1.2)**2)
    for i in range(9):
        x=-1.2+i*(2.4/9);rod(P,'sagging golden cord'+str(i),(x,0,sag(x)),(x+2.4/9,0,sag(x+2.4/9)),.007,gold,3)
    for i in range(9):
        x=-1.07+i*.267; left=x-.119;right=x+.119
        zl=sag(left);zr=sag(right);bottom=(zl+zr)/2-.43
        co=[c['magenta'],gold,c['cyan']][i%3]
        flags.append(mesh(P,'creased solid pennant'+str(i),[(left,0,zl),(right,0,zr),(x-.015,-.018,bottom),(x,-.025,(zl+zr)/2-.105),(left,.009,zl),(right,.009,zr),(x-.015,-.009,bottom)],[(0,3,2),(3,1,2),(4,6,5),(0,4,5,1),(0,2,6,4),(1,5,6,2)],co))
    finish(P,spec,[('flag',(0,0,.92),flags)])
