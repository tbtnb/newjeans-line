"""P19 Balloon Bunch — spec.size_m 2 × 1.2 × 3.5 m, budget 500 tris.
Pivots: root at page origin; swing at the gold weight's string attachment.
SIMPLIFICATIONS: thin gold threads are triangular rods; all balloons share one swing;
no printed paper texture; fine gold ear borders omitted; foil creases use six straight ribbons.
Ear lining uses the approved shared paper palette #FFF8EC.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

BUDGET = 500

def mesh(P, name, verts, faces, color):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces); me.update()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    P.paint(ob, color)
    return ob

def rod(P, name, a, b, r, color, n=3):
    a, b = Vector(a), Vector(b)
    ob = P.cyl(name, r, (b-a).length, n, loc=a, color=color)
    ob.rotation_euler = (b-a).to_track_quat('Z', 'Y').to_euler()
    return ob

def folded(P, name, loc, scale, color):
    # Geodesic eighty-face paper sphere: genuine triangular facets in every view.
    phi=(1+math.sqrt(5))/2
    base=[(0,a,b*phi) for a in (-1,1) for b in (-1,1)]
    base += [(a,b*phi,0) for a in (-1,1) for b in (-1,1)]
    base += [(a*phi,0,b) for a in (-1,1) for b in (-1,1)]
    def unit(v):
        r=math.sqrt(sum(x*x for x in v));return tuple(x/r for x in v)
    base=[unit(v) for v in base]
    edge=min(sum((a[k]-b[k])**2 for k in range(3)) for i,a in enumerate(base) for b in base[i+1:])
    def near(i,j): return abs(sum((base[i][k]-base[j][k])**2 for k in range(3))-edge)<1e-5
    faces=[(i,j,k) for i in range(12) for j in range(i+1,12) for k in range(j+1,12) if near(i,j) and near(i,k) and near(j,k)]
    vv=[];ff=[]
    for i,j,k in faces:
        a,b,d=base[i],base[j],base[k]
        ab=unit(tuple(a[q]+b[q] for q in range(3)));bd=unit(tuple(b[q]+d[q] for q in range(3)));da=unit(tuple(d[q]+a[q] for q in range(3)))
        start=len(vv);vv.extend([a,b,d,ab,bd,da])
        ff.extend([tuple(start+q for q in f) for f in [(0,3,5),(3,1,4),(5,4,2),(3,4,5)]])
    turn=.17
    rotated=[(x*math.cos(turn)+z*math.sin(turn),y,-x*math.sin(turn)+z*math.cos(turn)) for x,y,z in vv]
    # Normalize each axis so the design's measured radii remain exact.
    ext=[max(abs(v[q]) for v in rotated) for q in range(3)]
    verts=[tuple(loc[q]+scale[q]*v[q]/ext[q] for q in range(3)) for v in rotated]
    return mesh(P,name,verts,ff,color)

def finish(P,spec,moving,joint):
    bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
    pts=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
    lo=Vector(tuple(min(p[i] for p in pts) for i in range(3)))
    hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
    s=spec['size_m']; target=(s['w'],s['d'],s['h'])
    scale=[target[i]/(hi[i]-lo[i]) for i in range(3)]
    ctr=((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z)
    def point(v): return tuple((v[i]-ctr[i])*scale[i] for i in range(3))
    for ob in obs:
        mw=ob.matrix_world.copy()
        for v in ob.data.vertices: v.co=point(mw@v.co)
        ob.matrix_world=Matrix.Identity(4); ob.data.update()
    # Depth fitting retains the traced XZ silhouettes and clean triangular shells.
    for ob in obs:
        for v in ob.data.vertices:
            y=v.co.y; z=v.co.z
            if ob.name=='magenta gem heart' or ob.name.startswith('gold heart fold seam'):
                v.co.y=(y+.10)*.975-.10-.02625-.01875*(z-2.6)
            elif ob.name=='cyan bunny balloon':
                v.co.y=(y+.075)*.8475-.075-.09
            elif ob.name=='pink spherical balloon':
                v.co.y=(y-.29)*1.0375+.29-.0025
            elif ob.name.startswith(('cyan folded ear', 'paper ear lining')):
                v.co.y=y*1.2-.0375-.0375*(z-2.8)
        ob.data.update()
    # Weight and string anchor sit just behind the depth centre in the side drawing.
    weight=next(o for o in obs if o.name=='gold folded weight')
    for v in weight.data.vertices:v.co.y+=.04
    weight.data.update()
    for i in range(3):
        thread=next(o for o in obs if o.name=='gold tied string '+str(i))
        zs=[v.co.z for v in thread.data.vertices]; low=min(zs); high=max(zs)
        for v in thread.data.vertices:v.co.y+=.04*(1-max(0,min(1,(v.co.z-low)/(high-low))))
        thread.data.update()
    ys=[v.co.y for ob in obs for v in ob.data.vertices]
    depth_scale=s['d']/(max(ys)-min(ys)); depth_mid=(max(ys)+min(ys))/2
    for ob in obs:
        for v in ob.data.vertices: v.co.y=(v.co.y-depth_mid)*depth_scale
        ob.data.update()
    j=list(point(joint)); j[1]=(j[1]+.04-depth_mid)*depth_scale
    swing=P.pivot('swing',j,moving)
    P.pivot('root',(0,0,0),[o for o in obs if o not in moving]+[swing])

def build(P,spec):
    c=spec['colors']; gold=c['gold']; moving=[]
    # Front contour traced from the approved sheet, in sheet-relative metres.
    def front(px,py): return ((px-271)/259,(907-py)/259)
    outline=[front(x,z) for x,z in [(10,209),(42,150),(104,128),(157,158),(203,128),(234,119),(271,130),(302,182),(290,236),(263,284),(214,330),(169,362),(101,335),(55,303)]]
    cx,cz=front(157,242); n=len(outline)
    # Equator and inset face belts create the rounded heart lobes and a sharp gem ridge.
    vv=[(x,-.07+.45*(z-cz)+.25*(x-cx),z) for x,z in outline]
    vv += [(cx+(x-cx)*.79,-.49+.12*(z-cz)+.15*(x-cx)+1.4*((x-cx)*.79)**2,cz+(z-cz)*.79) for x,z in outline]
    vv += [(cx+(x-cx)*.78,.28+.04*(z-cz)+.15*(x-cx),cz+(z-cz)*.78) for x,z in outline]
    vv += [(cx,-.62,cz),(cx,.43,cz)]
    ff=[]
    for i in range(n):
        j=(i+1)%n
        ff.extend([(i,j,n+j,n+i),(n+i,n+j,3*n),(j,i,2*n+i,2*n+j),(2*n+j,2*n+i,3*n+1)])
    heart=mesh(P,'magenta gem heart',vv,ff,c['magenta']); moving.append(heart)
    heart_verts=vv; heart_faces=ff
    moving.append(folded(P,'pink spherical balloon',(*front(270,392)[:1],.29,front(270,392)[1]),(.37,.36,.385),c['pink']))
    moving.append(folded(P,'cyan bunny balloon',(*front(397,269)[:1],-.075,front(397,269)[1]),(.41,.50,.385),c['cyan']))
    # Solid folded ears with broad paper insets, swept slightly back like the hero.
    for idx,pixels in enumerate([[(339,188),(300,70),(338,0),(393,43),(405,141),(398,176)],[(433,183),(451,67),(516,25),(533,91),(511,135),(459,198)]]):
        poly=[front(*p) for p in pixels]; n=len(poly)
        mx=sum(p[0] for p in poly)/n; mz=sum(p[1] for p in poly)/n
        def ey(z): return .08+(.12 if idx==0 else .02)*(z-2.8)/.70
        v=[(x,ey(z),z) for x,z in poly]
        v += [(mx+(x-mx)*.68,ey(z)+.20*max(0,math.sin(math.pi*min(1,max(0,(z-2.77)/.73)))),z) for x,z in poly]
        v += [(mx,ey(mz)-.11,mz),(mx,ey(mz)+.17,mz)]
        f=[]
        for k in range(n):
            j=(k+1)%n
            f.extend([(k,j,2*n),(n+j,n+k,2*n+1),(k,n+k,n+j,j)])
        ear=mesh(P,'cyan folded ear '+str(idx),v,f,c['cyan']); moving.append(ear)
        # The cream lining is fitted to the shell's actual front triangles.
        inner=[front(*p) for p in ([(371,181),(356,140),(371,86),(381,62),(394,158)] if idx==0 else [(444,182),(457,124),(477,83),(515,46),(511,91),(464,174)])]
        # Subdivide each outline edge at its ridge intersection for a flush paper patch.
        def clip(poly,a,b):
            out=[]
            for u,w in zip(poly,poly[1:]+poly[:1]):
                du=(b[0]-a[0])*(u.z-a[1])-(b[1]-a[1])*(u.x-a[0])
                dw=(b[0]-a[0])*(w.z-a[1])-(b[1]-a[1])*(w.x-a[0])
                if du>=-1e-8:out.append(u)
                if (du>=0)!=(dw>=0):out.append(u+(w-u)*(du/(du-dw)))
            return out
        if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(inner,inner[1:]+inner[:1]))<0:inner.reverse()
        pv=[];pf=[]
        for k in range(n):
            piece=[Vector(v[k]),Vector(v[(k+1)%n]),Vector(v[2*n])]
            for a,b in zip(inner,inner[1:]+inner[:1]):
                piece=clip(piece,a,b)
                if not piece: break
            if len(piece)>2:
                s=len(pv);pv.extend([(q.x,q.y-.006,q.z) for q in piece]);pf.append(tuple(range(s,len(pv))))
        moving.append(mesh(P,'paper ear lining '+str(idx),pv,pf,'#FFF8EC'))
    joint=(0,.05,.44)
    for i,(x,y,z,col) in enumerate([(-.43,-.19,2.13,c['magenta']),(0,.29,1.605,c['pink']),(.43,.055,2.132,c['cyan'])]):
        moving.append(P.cyl('balloon knot '+str(i),.087,.10,4,loc=(x,y,z-.10),r2=.048,color=col,cap=False))
        moving.append(P.cyl('gold neck band '+str(i),.051,.016,3,loc=(x,y,z-.009),color=gold,cap=False))
        moving.append(rod(P,'gold tied string '+str(i),joint,(x,y,z-.10),.014,gold))
    # Thin gold crease ribbons conform to the real heart facets (twelve triangles).
    def surface_y(x,z):
        hits=[]
        for face in heart_faces:
            for j in range(1,len(face)-1):
                a,b,d=[heart_verts[i] for i in (face[0],face[j],face[j+1])]
                den=(b[2]-d[2])*(a[0]-d[0])+(d[0]-b[0])*(a[2]-d[2])
                if abs(den)<1e-10: continue
                u=((b[2]-d[2])*(x-d[0])+(d[0]-b[0])*(z-d[2]))/den
                v=((d[2]-a[2])*(x-d[0])+(a[0]-d[0])*(z-d[2]))/den
                w=1-u-v
                if min(u,v,w)>=-1e-6: hits.append(u*a[1]+v*b[1]+w*d[1])
        return min(hits)-.012 if hits else -.075
    for k,path in enumerate([[(100,156),(54,180),(54,239),(78,303),(166,352)],
                             [(203,143),(266,184),(267,234)]]):
        coords=[front(*p) for p in path]; verts=[]; faces=[]
        for a,b in zip(coords,coords[1:]):
            dx=b[0]-a[0]; dz=b[1]-a[1]; length=math.hypot(dx,dz)
            ox=-dz/length*.0045; oz=dx/length*.0045
            start=len(verts)
            for x,z in [(a[0]+ox,a[1]+oz),(a[0]-ox,a[1]-oz),
                        (b[0]-ox,b[1]-oz),(b[0]+ox,b[1]+oz)]:
                verts.append((x,surface_y(x,z),z))
            faces.append(tuple(range(start,start+4)))
        moving.append(mesh(P,'gold heart fold seam '+str(k),verts,faces,gold))
    # The weight follows the broad octagonal bottle silhouette in front and side.
    weight=P.lathe('gold folded weight',[(.18,0),(.225,.06),(.225,.20),(.075,.34),(.09,.43),(0,.44)],6,color=gold)
    finish(P,spec,moving,joint)
