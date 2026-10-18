"""P25 Faceted paper hill. Size 5.2 x 2.8 x 2.5 m from spec; 400 tris; root.
SIMPLIFICATIONS: tiny flower centers use green, preserving the three specified palette colours; no texture."""
BUDGET = 400

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
    c=spec['colors'];n=16;verts=[]
    def height(x,y):
        left=max(0,1-((x+.30)**2/.96**2+(y-.04)**2/1.05**2)**.72)
        right=max(0,1-((x-.55)**2/.58**2+(y+.02)**2/.98**2)**.72)*.78
        return max(left,right)
    for k,r in enumerate([1,.72,.44,.18]):
        for i in range(n):
            a=2*math.pi*i/n;rr=r*(1+.06*math.sin(5*a));x=rr*math.cos(a);y=rr*math.sin(a)
            z=.10+.035*math.sin(3*a) if k==0 else .10+height(x,y)+.025*math.sin(i*2.7+k*1.1)
            verts.append((x*2.6,y*1.4,z*2.8))
    verts.append((-.72,0,2.6));faces=[]
    for k in range(3):
        for i in range(n):
            j=(i+1)%n;faces.extend([(k*n+i,k*n+j,(k+1)*n+i),(k*n+j,(k+1)*n+j,(k+1)*n+i)])
    for i in range(n):faces.append((3*n+i,3*n+(i+1)%n,4*n))
    mesh(P,'triangulated folded hillside',verts,faces,lambda p,no:c['green'] if no.x>.56 and no.y<-.15 and int(abs(p.x*5+p.y*3+p.z*2))%3==0 else c['mint'])
    rim=[(verts[i][0],verts[i][1],0) for i in range(n)]+[verts[i] for i in range(n)]
    mesh(P,'pearl paper cut edge',rim,[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]+[tuple(reversed(range(n)))],c['pearl'])
    hill=bpy.context.scene.objects.get('triangulated folded hillside')
    bpy.context.view_layer.update();hill.data.calc_loop_triangles()
    from mathutils.geometry import intersect_ray_tri
    # Sparse little paper daisies follow the folded slopes.
    for k,(x,y) in enumerate([(-.32,.02),(-.70,-.05),(-.55,-.52),(.45,-.45),(.60,.15),(.85,-.2)]):
        z=.10+height(x,y);cx=x*2.6;cy=y*1.4;hits=[]
        for tri in hill.data.loop_triangles:
            va,vb,vc=[hill.matrix_world@hill.data.vertices[t].co for t in tri.vertices]
            hit=intersect_ray_tri(va,vb,vc,Vector((0,0,-1)),Vector((cx,cy,8)),True)
            if hit is not None:hits.append(hit.z)
        cz=(max(hits) if hits else z*2.8)+.025
        for j in range(5):
            a=2*math.pi*j/5;dx=.095*math.cos(a);dy=.095*math.sin(a)
            mesh(P,'paper flower petal',[(cx,cy,cz),(cx+dx-dy*.35,cy+dy+dx*.35,cz+.025),(cx+dx*1.6,cy+dy*1.6,cz+.005),(cx+dx+dy*.35,cy+dy-dx*.35,cz+.025)],[(0,1,2,3)],c['pearl'])
        P.cyl('green flower center',.035,.02,5,loc=(cx,cy,cz+.025),color=c['green'])
    finish(P,spec)
