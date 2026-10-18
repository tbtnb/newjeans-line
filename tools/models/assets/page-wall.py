"""P26 Standing curved page wall. Size 8.5 x 1.2 x 5 m from spec; 800 tris; root, lid.
SIMPLIFICATIONS: six paper leaves share one bottom hinge; individual printed page marks omitted; spec depth/height is wider than side drawing."""
BUDGET = 800

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
    c=spec['colors'];pieces=[];n=8
    for leaf in range(6):
        vs=[]
        for i in range(n+1):
            x=-4.25+8.5*i/n; bend=.18*(x/4.25)**2
            for y,z in [(leaf*.11+bend,0.10*bend),(leaf*.11+bend,4.94+.30*bend),(leaf*.11+bend+.108,0.10*bend),(leaf*.11+bend+.108,4.94+.30*bend)]:vs.append((x,y,z))
        faces=[]
        for i in range(n):
            a=4*i;b=4*(i+1);faces.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a+1,b+1,b+3,a+3),(a,a+2,b+2,b)])
        faces.extend([(0,1,3,2),(4*n,4*n+2,4*n+3,4*n+1)])
        ob=mesh(P,'curved leaf'+str(leaf),vs,faces,c['navy'] if leaf==5 else c['cream']);pieces.append(ob)
        if leaf<5:
            # Gold borders are integral face strips on the two long edges.
            for upper in [False,True]:
                vv=[]
                for i in range(n+1):
                    x=-4.25+8.5*i/n;bend=.18*(x/4.25)**2;zz=4.94+.30*bend if upper else .10*bend
                    vv.extend([(x,leaf*.11+bend-.003,zz),(x,leaf*.11+bend-.003,zz+(-.055 if upper else .055))])
                pieces.append(mesh(P,'gold page border',vv,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(n)],c['gold']))
            for x in [-4.25,4.25]:pieces.append(P.box('gold vertical edge',(.045,.04,4.99),loc=(x,leaf*.11+.18-.004,0),color=c['gold']))
    finish(P,spec,[('lid',(0,0,0),pieces)])
