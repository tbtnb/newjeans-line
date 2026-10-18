"""P19 Balloon bunch. Size spec.size_m 2 x 1.2 x 3.5 m; 500 tris; root, swing.
SIMPLIFICATIONS: balloons share one swing pivot; triangular gold strings; pale gold ear insets use the spec light slot; no paper texture."""
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
        ob.matrix_world=Matrix.Identity(4);ob.data.update()
    moving=set(); roots=[]
    for name,joint,children in animated:
        roots.append(P.pivot(name,point(Vector(joint)),children)); moving.update(children)
    P.pivot('root',(0,0,0),[o for o in obs if o not in moving]+roots)

def angular_balloon(P,name,loc,scale,col):
    # Staggered polygon belts give actual triangular paper folds, not flat latitude bands.
    profile=[(0,-1),(.64,-.80),(.96,-.32),(.97,.27),(.70,.78),(0,1)]
    n=9; vv=[]; rings=[]
    for j,(r,z) in enumerate(profile):
        ids=[]
        for k in range(n if r else 1):
            a=math.tau*k/n+(j%2)*math.pi/n
            ids.append(len(vv));vv.append((loc[0]+scale[0]*r*math.cos(a),loc[1]+scale[1]*r*math.sin(a),loc[2]+scale[2]*z))
        rings.append(ids)
    ff=[]
    for a,b in zip(rings,rings[1:]):
        for i in range(n):
            j=(i+1)%n
            if len(a)==1:ff.append((a[0],b[j],b[i]))
            elif len(b)==1:ff.append((a[i],a[j],b[0]))
            else:ff.extend([(a[i],a[j],b[i]),(a[j],b[j],b[i])])
    return mesh(P,name,vv,ff,col)

def build(P,spec):
    c=spec['colors']; gold=c['gold']; moving=[]
    # Front drawing coordinates in metres. Broad gem faces converge at the heart ridge.
    outline=[(-1,2.69),(-.94,2.94),(-.67,3.06),(-.40,2.93),
       (-.14,3.10),(.06,3.04),(.14,2.86),(.10,2.64),(-.15,2.30),
       (-.43,2.12),(-.72,2.33),(-.91,2.51)]
    n=len(outline);cx=-.43;cz=2.64
    vv=[(x,-.04,z) for x,z in outline]
    vv += [(cx+(x-cx)*.83,-.50,cz+(z-cz)*.83) for x,z in outline]
    vv += [(cx+(x-cx)*.78,.24,cz+(z-cz)*.78) for x,z in outline]
    vv += [(cx,-.63,cz),(cx+.05,.37,cz)]
    ff=[]
    for i in range(n):
        j=(i+1)%n
        ff += [(i,j,n+j),(i,n+j,n+i),(n+i,n+j,3*n),
               (j,i,2*n+i),(j,2*n+i,2*n+j),(2*n+j,2*n+i,3*n+1)]
    heart=mesh(P,'faceted broad heart balloon',vv,ff,lambda p,n:c['pink'] if n.z>.45 else c['magenta']);moving.append(heart)
    moving.append(angular_balloon(P,'folded pink balloon',(-.01,.25,1.98),(.39,.38,.385),c['pink']))
    moving.append(angular_balloon(P,'faceted cyan bunny head',(.49,.015,2.48),(.42,.40,.39),c['cyan']))
    # Tall asymmetric pointed paper ears, with a folded inner gold panel.
    for i,(x,lean,h) in enumerate([(.34,-.17,.74),(.69,.25,.70)]):
        z=2.78;y=.065
        shape=[(-.075,0),(-.16,.39),(-.10,.70),(0,1),(.14,.77),(.15,.36),(.075,0)]
        vv=[]
        for back in (False,True):
            for u,v in shape:
                vv.append((x+u+lean*v,y+.035*v+(.17 if back else -.17)*math.sin(math.pi*v),z+h*v))
        vv += [(x+lean*.47,y-.27+.035*.47,z+h*.47)]
        ff=[tuple(range(7,14))]+[(k,(k+1)%7,(k+1)%7+7,k+7) for k in range(7)]
        ff += [(k,(k+1)%7,14) for k in range(7)]
        ear=mesh(P,'sharp folded cyan ear '+str(i),vv,ff,c['cyan']);moving.append(ear)
        # Reference inner ear is pale; gold is the light slot available in this spec.
        panel=[(x-.035+lean*.12,y-.066+.035*.12,z+h*.12),
               (x+.045+lean*.15,y-.07+.035*.15,z+h*.15),
               (x+.075+lean*.65,y-.075+.035*.65,z+h*.65),
               (x+lean*.87,y-.03+.035*.87,z+h*.87),
               (x-.05+lean*.57,y-.12+.035*.57,z+h*.57)]
        panel += [(x+lean*.45,y-.205+.035*.45,z+h*.45)]
        from mathutils.bvhtree import BVHTree
        tree=BVHTree.FromPolygons([v.co.copy() for v in ear.data.vertices],[list(f.vertices) for f in ear.data.polygons])
        for j,(px,py,pz) in enumerate(panel):
            hit,_,_,_=tree.ray_cast(Vector((px,y-1,pz)),Vector((0,1,0)))
            if hit is not None:panel[j]=(px,hit.y-.012,pz)
        moving.append(mesh(P,'creased pale gold ear inset '+str(i),panel,[(k,(k+1)%5,5) for k in range(5)],gold))
    for i,(x,y,z,col) in enumerate([(-.43,-.14,2.12,c['magenta']),(-.01,.25,1.595,c['pink']),(.49,.015,2.09,c['cyan'])]):
        moving.append(P.cyl('flared tied balloon neck '+str(i),.087,.105,4,loc=(x,y,z-.10),r2=.035,color=col))
        moving.append(P.cyl('gold neck band '+str(i),.037,.018,5,loc=(x,y,z-.012),color=gold,cap=False))
        moving.append(rod(P,'taut gold string '+str(i),(0,.06,.43),(x,y,z-.10),.013,gold,3))
    # Visible gold crease thread on the heart face, following its angular contour.
    seam=[(-.91,-.37,2.92),(-.84,-.52,2.70),(-.80,-.46,2.46),(-.43,-.20,2.13)]
    for i,(a,b) in enumerate(zip(seam,seam[1:])):
        moving.append(rod(P,'fine gold heart seam '+str(i),a,b,.004,gold,3))
    weight=P.lathe('faceted gold weight',[(.18,0),(.225,.045),(.225,.20),(.09,.34),(.075,.43),(0,.43)],6,color=gold)
    for v in weight.data.vertices:
        if abs(v.co.z-.20)<.001:
            a=math.atan2(v.co.y,v.co.x)+math.pi/6;r=math.hypot(v.co.x,v.co.y)
            v.co.x=r*math.cos(a);v.co.y=r*math.sin(a)
    weight.data.update()
    bm=bmesh.new();bm.from_mesh(weight.data)
    bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='ALTERNATE')
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    bm.to_mesh(weight.data);bm.free();weight.data.update();P.paint(weight,gold)
    finish(P,spec,[('swing',(0,0,.43),moving)])
