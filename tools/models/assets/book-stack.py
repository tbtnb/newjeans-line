"""P23 Stump with books. Size 1 x 1 x 1 m from spec; 500 tris; root, pulse.
SIMPLIFICATIONS: bark uses geometric creases in exact wood colour; printed book text and sub-2cm gilding omitted."""
BUDGET = 500

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
    c=spec['colors']; wood=c['wood']; cream=c['cream']; teal=c['teal']; lamp=c['lamp']
    # Lobed flared root perimeter, narrow waist and broad sawn top.
    n=16; verts=[]
    for z,r in [(0,.48),(.10,.45),(.30,.38),(.62,.39),(.67,.39)]:
        for i in range(n):
            a=2*math.pi*i/n+math.pi/16;rr=r*(1 if i%2==0 else .80) if z<.3 else r*(1 if i%2==0 else .955)
            verts.append((rr*math.cos(a),rr*math.sin(a),z+(.022 if i%2 else 0) if z==0 else z))
    faces=[]
    for k in range(4):
        for i in range(n):
            j=(i+1)%n;faces.extend([(k*n+i,k*n+j,(k+1)*n+j),(k*n+i,(k+1)*n+j,(k+1)*n+i)])
    faces.extend([tuple(reversed(range(n))),tuple(4*n+i for i in range(n))]);mesh(P,'creased root stump',verts,faces,wood)
    for r in [.29,.19]:
        vs=[]
        for i in range(16):
            a=2*math.pi*i/16
            for rad in [r,r-.009]:vs.append((rad*math.cos(a),rad*math.sin(a),.671))
        mesh(P,'sawn concentric ring',vs,[(2*i,2*((i+1)%16),2*((i+1)%16)+1,2*i+1) for i in range(16)],cream)
    for k,(x,y,ang) in enumerate([(-.04,-.025,-28),(-.05,.01,-18),(-.06,.02,-34)]):
        z=.68+k*.11; col=teal if k!=1 else cream
        P.box('book page block'+str(k),(.33,.25,.082),loc=(x,y,z+.009),rot=(0,0,ang),color=cream)
        for zz in [z,z+.088]:P.box('book cover'+str(k),(.36,.27,.012),loc=(x,y,zz),rot=(0,0,ang),color=col)
        P.box('rounded spine'+str(k),(.022,.27,.100),loc=(x-.175,y,z),rot=(0,0,ang),color=col)
    P.cyl('candle saucer',.066,.032,8,loc=(.20,-.025,.675),color=lamp)
    P.cyl('cream candle',.039,.17,6,loc=(.20,-.025,.707),color=cream)
    flame=P.lathe('folded flame',[(0,0),(.028,.025),(.018,.06),(0,.095)],5,loc=(.20,-.025,.89),color=lamp)
    finish(P,spec,[('pulse',(.20,-.025,.93),[flame])])
