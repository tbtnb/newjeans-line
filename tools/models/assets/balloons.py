"""P19 Balloon bunch. Size spec.size_m 2 x 1.2 x 3.5 m; 500 tris; root, swing.
SIMPLIFICATIONS: three balloons share one swing pivot; strings are triangular rods; inflation uses triangulated facets; fine gold seams omitted; inner ears use spec gold rather than unlisted white; the official mask fills string-enclosed air."""
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
    # The inflated bodies now occupy the upper 55% of the entire bunch.
    outline=[(-.99,2.68),(-.96,2.86),(-.79,3.00),(-.57,3.03),(-.39,2.94),(-.25,3.04),(-.05,3.07),(.12,2.94),(.17,2.75),(.09,2.51),(-.13,2.30),(-.40,2.10),(-.68,2.29),(-.88,2.48)]
    n=len(outline); cx=-.41;cz=2.65
    verts=[(x,-.28,z) for x,z in outline]+[(x,.08,z) for x,z in outline]
    verts += [(cx+(x-cx)*.72,-.48,cz+(z-cz)*.72) for x,z in outline]
    verts += [(cx,-.57,cz),(cx,.28,cz)]
    faces=[]
    for i in range(n):
        j=(i+1)%n
        faces.extend([(i,j,2*n+j),(i,2*n+j,2*n+i),(2*n+i,2*n+j,3*n),(n+j,n+i,3*n+1),(i,n+i,n+j,j)])
    moving.append(mesh(P,'large faceted inflated heart',verts,faces,lambda p,n:c['pink'] if n.z>.23 and n.x<0 else c['magenta']))
    moving.append(P.ico('large round pink balloon',1,loc=(.05,.28,2.01),scale=(.39,.39,.43),subdiv=2,color=c['pink']))
    moving.append(P.ico('large blue bunny head',1,loc=(.59,-.025,2.48),scale=(.43,.44,.41),subdiv=2,color=c['cyan']))
    for i,(x,ang) in enumerate([(.36,-12),(.80,18)]):
        moving.append(P.lathe('inflated bunny ear'+str(i),[(0,0),(.09,.10),(.15,.38),(.105,.60),(0,.75)],4,loc=(x,.01,2.79),rot=(-25,ang,0),color=c['cyan']))
        moving.append(P.prism('gold inner ear crease'+str(i),[(-.045,.13),(.045,.14),(.052,.45),(0,.64),(-.040,.46)],.018,loc=(x,-.095,2.79),rot=(-25,ang,0),color=gold))
    for i,p in enumerate([(-.40,-.06,2.10),(.05,.28,1.60),(.59,-.025,2.07)]):
        moving.append(P.cyl('inflation knot'+str(i),.060,.095,4,loc=(p[0],p[1],p[2]-.085),r2=.025,color=[c['magenta'],c['pink'],c['cyan']][i]))
        moving.append(rod(P,'converging golden string'+str(i),(0,0,.40),(p[0],p[1],p[2]-.075),.011,gold,3))
    P.lathe('gold faceted weight',[(.18,0),(.22,.08),(.21,.24),(.09,.34),(.055,.40),(0,.42)],6,color=gold)
    finish(P,spec,[('swing',(0,0,.40),moving)])
