"""P27 Paper mushroom cluster. Size 0.7 x 0.7 x 0.8 m from spec; 300 tris; root, bob.
SIMPLIFICATIONS: three caps share a bounce pivot; gold rim omitted because gold is absent from the specified palette; nine filled raised paper spots."""
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
    from mathutils.geometry import intersect_ray_tri
    c=spec['colors'];caps=[]
    for k,(x,y,h,r,col) in enumerate([(.10,.10,.80,.29,c['coral']),(-.20,-.11,.48,.23,c['teal']),(.245,-.18,.33,.15,c['coral'])]):
        stem=P.lathe('faceted tapered stem'+str(k),[(.110,0),(.125,.04),(.070,h*.68)],5,loc=(x,y,.025 if k==0 else 0),color=c['cream'])
        base=h*.63
        cap=P.lathe('mushroom cap'+str(k),[(0,base),(r,base+.025),(r*.88,h*.82),(r*.46,h*.97),(0,h)],8,loc=(x,y,0),color=col);caps.append(cap)
        bpy.context.view_layer.update();cap.data.calc_loop_triangles()
        for j,(a,rr) in enumerate([(0,.67),(2.1,.60),(4.2,.64)]):
            px=x+r*rr*math.cos(a);py=y+r*rr*math.sin(a);pz=h-(h-base)*rr*.65+.002
            # Raised irregular paper spots, tangent to the cap's roof.
            vv=[]
            for t in range(5):
                aa=2*math.pi*t/5;xx=px+r*.18*math.cos(aa);yy=py+r*.18*math.sin(aa)
                rr=((xx-x)**2+(yy-y)**2)**.5/r
                hits=[]
                for tri in cap.data.loop_triangles:
                    va,vb,vc=[cap.matrix_world@cap.data.vertices[t].co for t in tri.vertices]
                    hit=intersect_ray_tri(va,vb,vc,Vector((0,0,-1)),Vector((xx,yy,h+1)),True)
                    if hit is not None:hits.append(hit.z)
                zz=max(hits)+.004 if hits else pz
                vv.append((xx,yy,zz))
            center=Vector((px,py,0));hits=[]
            for tri in cap.data.loop_triangles:
                va,vb,vc=[cap.matrix_world@cap.data.vertices[t].co for t in tri.vertices]
                hit=intersect_ray_tri(va,vb,vc,Vector((0,0,-1)),Vector((px,py,h+1)),True)
                if hit is not None:hits.append(hit.z)
            center.z=max(hits)+.012 if hits else pz+.012
            vv=[(xx,yy,zz+.008) for xx,yy,zz in vv]+[tuple(center)]
            caps.append(mesh(P,'cream paper spot',vv,[(i,(i+1)%5,5) for i in range(5)],c['cream']))
    finish(P,spec,[('bob',(.10,.10,.51),caps)])
