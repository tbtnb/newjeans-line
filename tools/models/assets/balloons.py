"""P19 Balloon bunch. Size spec.size_m 2 x 1.2 x 3.5 m; 500 tris; root, swing.
SIMPLIFICATIONS: three balloons share one swing pivot; strings are four-sided rods; inflation uses bevelled facets; the official mask fills string-enclosed air."""
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
    c=spec['colors']; gold=c['gold']; moving=[]
    # Inflated heart: a bevelled silhouette, raised central facets, no flat card.
    outline=[(-.92,2.67),(-.98,2.91),(-.88,3.12),(-.66,3.24),(-.43,3.20),(-.30,3.04),(-.12,3.20),(.08,3.18),(.20,3.00),(.15,2.79),(-.33,2.36)]
    n=len(outline); verts=[(x,-.32,z) for x,z in outline]+[(x,.05,z) for x,z in outline]
    verts += [(-.36+(x+.36)*.72,-.56,2.87+(z-2.87)*.72) for x,z in outline]
    verts += [(-.36,-.64,2.87),(-.36,.28,2.87)]
    faces=[]
    for i in range(n):
        j=(i+1)%n
        faces.extend([(i,j,2*n+j,2*n+i),(2*n+i,2*n+j,3*n),(n+j,n+i,3*n+1),(i,n+i,n+j,j)])
    moving.append(mesh(P,'inflated heart',verts,faces,c['magenta']))
    moving.append(P.lathe('round pink balloon',[(0,0),(.27,.10),(.37,.36),(.31,.63),(0,.82)],10,loc=(.03,.29,1.85),color=c['pink']))
    moving.append(P.ico('bunny head',.42,loc=(.58,-.01,2.79),scale=(1,.94,.95),subdiv=2,color=c['cyan']))
    for i,(x,ang) in enumerate([(.39,-12),(.81,18)]):
        ear=P.lathe('thick bunny ear'+str(i),[(0,0),(.09,.08),(.13,.34),(.08,.56),(0,.69)],4,loc=(x,.04,3.03),rot=(0,ang,0),color=c['cyan']);moving.append(ear)
        moving.append(P.prism('inner ear fold'+str(i),[(-.035,.09),(.035,.12),(.035,.45),(0,.56),(-.025,.40)],.018,loc=(x,-.075,3.03),rot=(0,ang,0),color=gold))
    for i,p in enumerate([(-.33,0,2.36),(.03,.27,1.87),(.58,0,2.42)]):
        moving.append(P.cyl('balloon knot'+str(i),.055,.10,5,loc=(p[0],p[1],p[2]-.08),r2=.025,color=[c['magenta'],c['pink'],c['cyan']][i]))
        moving.append(rod(P,'taut golden string'+str(i),(0,0,.35),p,.009,gold,4))
    P.lathe('gold paper weight',[(.18,0),(.22,.08),(.21,.24),(.09,.32),(.045,.36),(0,.38)],6,color=gold)
    finish(P,spec,[('swing',(0,0,.35),moving)])
