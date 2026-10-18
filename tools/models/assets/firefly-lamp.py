"""P22 Firefly paper lantern. Size 0.7 x 0.5 x 1.4 m from spec; 200 tris; root, pulse.
SIMPLIFICATIONS: warm light uses exact lamp vertex colour, without bloom; flattened geodesic shoulders; side drawing is wider than the spec depth/height ratio."""
BUDGET = 200

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
    c=spec['colors']; teal=c['teal']; gold=c['gold']
    joints=[(.025,0,0),(.025,0,.14),(.105,.065,.34),(.02,0,.51),(.02,0,.76)]
    vs=[(x+.022*math.cos(i*math.pi/2),y+.022*math.sin(i*math.pi/2),z) for x,y,z in joints for i in range(4)]
    fs=[(k*4+i,k*4+(i+1)%4,(k+1)*4+(i+1)%4,(k+1)*4+i) for k in range(4) for i in range(4)]+[(3,2,1,0),(16,17,18,19)]
    mesh(P,'continuous bent paper stem',vs,fs,teal)
    leaf=mesh(P,'folded leaf',[(-.34,-.07,.74),(-.18,-.19,.73),(.02,0,.51),(-.22,.13,.55),(-.20,-.02,.62)],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],teal)
    rod(P,'leaf vein',(-.335,-.065,.735),(.02,-.006,.51),.004,gold,3)
    body=P.ico('faceted round lantern',.285,loc=(.02,0,1.00),scale=(1,1,1),subdiv=2,color=c['lamp'])
    for v in body.data.vertices:
        zz=v.co.z/.285;v.co.z=math.copysign(abs(zz)**.80,zz)*.285
    ring=mesh(P,'equatorial paper seam',[(.02+.276*math.cos(i*math.pi/4),.276*math.sin(i*math.pi/4),zz) for zz in [.995,.999] for i in range(8)],[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)],gold)
    cap=P.cyl('top gold cap',.065,.035,6,loc=(.02,0,1.28),color=gold)
    finial=P.cyl('point finial',.032,.065,4,loc=(.02,0,1.315),r2=0,color=gold)
    bottom=P.cyl('lower socket',.041,.06,3,loc=(.02,0,.68),color=gold)
    finish(P,spec,[('pulse',(.02,0,.99),[body,ring,cap,finial,bottom])])
