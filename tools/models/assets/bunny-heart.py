"""H02 Giant Pop-up Bunny with Heart — 6.5 × 6 × 10 m; 4000 tris.
Pivots: root (0,0,0), ears0/ears1 at folded ear roots, heart at gem centre.
SIMPLIFICATIONS: printed paper texture omitted; page edges are stacked folded leaves;
face uses shared navy #1F2350 eyes and the spec pink nose; gem microfacets follow the principal diamond creases;
shared paper #FFF8EC supplements the exact spec palette; top-view ear placement
is interpreted through front + hero (the drawn top ears extend farther back).
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix
BUDGET = 4000

def mesh(P, name, vertices, faces, color, refine=0):
    me = bpy.data.meshes.new(name)
    me.from_pydata(vertices, [], faces); me.update()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    for _ in range(refine):
        bmesh.ops.subdivide_edges(bm, edges=list(bm.edges), cuts=1, use_grid_fill=True)
        bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    P.paint(ob, color)
    return ob

def folded(P, name, center, radii, color, segs=12, refine=0):
    # Staggered angular sections create large, intentionally flat paper triangles.
    v = [(0, 0, -1)]
    levels = [-.86, -.52, -.05, .43, .79]
    for j, z in enumerate(levels):
        r = math.sqrt(1-z*z)
        for i in range(segs):
            a = 2*math.pi*i/segs + (j%2)*math.pi/segs
            v.append((r*math.cos(a), r*math.sin(a), z))
    v.append((0,0,1)); f=[]
    for i in range(segs): f.append((0,1+(i+1)%segs,1+i))
    for j in range(len(levels)-1):
        a=1+j*segs; b=a+segs
        for i in range(segs):
            k=(i+1)%segs
            f.extend([(a+i,a+k,b+i),(a+k,b+k,b+i)])
    for i in range(segs): f.append((1+(len(levels)-1)*segs+i,1+(len(levels)-1)*segs+(i+1)%segs,len(v)-1))
    vv=[(center[0]+x*radii[0],center[1]+y*radii[1],center[2]+z*radii[2]) for x,y,z in v]
    def paint(c,n):
        return '#FFF8EC' if n.z>.25 and n.x<-.12 else color
    return mesh(P,name,vv,f,paint,refine)

def surface_patch(P,ob,name,outline,color):
    def clip(poly,a,b):
        out=[]
        for u,w in zip(poly,poly[1:]+poly[:1]):
            du=(b[0]-a[0])*(u.z-a[1])-(b[1]-a[1])*(u.x-a[0])
            dw=(b[0]-a[0])*(w.z-a[1])-(b[1]-a[1])*(w.x-a[0])
            if du>=-1e-8:out.append(u)
            if (du>=0)!=(dw>=0):out.append(u+(w-u)*(du/(du-dw)))
        return out
    area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(outline,outline[1:]+outline[:1]))
    if area<0:outline=outline[::-1]
    vv=[];ff=[]
    for f in ob.data.polygons:
        if f.normal.y>=-.05:continue
        poly=[ob.data.vertices[i].co.copy() for i in f.vertices]
        for a,b in zip(outline,outline[1:]+outline[:1]):
            poly=clip(poly,a,b)
            if not poly:break
        if len(poly)>2:
            start=len(vv);vv.extend([(v.x,v.y-.012,v.z) for v in poly]);ff.append(tuple(range(start,len(vv))))
    return mesh(P,name,vv,ff,color)

def head_hull(P,c):
    outline=[(0,7.15),(.70,7.10),(1.18,6.85),(1.50,6.45),(1.62,5.91),(1.55,5.39),(.95,5.01),(0,4.70),(-.95,5.01),(-1.50,5.43),(-1.57,5.90),(-1.48,6.45),(-1.10,6.85),(-.60,7.10)]
    vv=[(x,-1.02 if z<4.8 else .12,z) for x,z in outline]
    vv.extend([(0,-.78,6.91),(-.85,-1.30,6.37),(.85,-1.30,6.37),(0,-1.45,6.18),(-1.25,-.95,6.18),(1.25,-.95,6.18),(-.62,-1.57,5.83),(.62,-1.57,5.83),(-.52,-1.26,5.22),(.52,-1.26,5.22),(0,-1.73,5.65),(-1.05,-1.30,5.65),(1.05,-1.30,5.65),(0,-1.05,5.02),(-.70,-.72,4.99),(.70,-.72,4.99),(0,1.19,5.75),(-.8,1.03,6.1),(.8,1.03,6.1),(0,.85,6.79),(0,.96,7.02),(0,-.84,7.01),(-.65,.86,5.12),(.65,.86,5.12)])
    bm=bmesh.new()
    for co in vv:bm.verts.new(co)
    bmesh.ops.convex_hull(bm,input=list(bm.verts),use_existing_faces=False)
    bm.verts.ensure_lookup_table();bm.verts.index_update()
    vertices=[tuple(v.co) for v in bm.verts];faces=[tuple(v.index for v in f.verts) for f in bm.faces];bm.free()
    return mesh(P,'folded_cheek_head',vertices,faces,lambda p,n:'#FFF8EC' if n.z>.5 and n.x<.1 else c,1)

def sections(P,name,profile,c,refine=0):
    v=[];n=12
    for j,(z,rx,ry,cy) in enumerate(profile):
        for i in range(n):
            a=2*math.pi*i/n+(j%2)*math.pi/n
            v.append((rx*math.cos(a),cy+ry*math.sin(a),z+(.11*math.sin(i*2.4+j) if 0<j<len(profile)-1 else 0)))
    f=[tuple(reversed(range(n)))]
    for j in range(len(profile)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;d=(j+1)*n+i;e=(j+1)*n+(i+1)%n
            f.extend([(a,b,d),(b,e,d)])
    f.append(tuple(range((len(profile)-1)*n,len(profile)*n)))
    return mesh(P,name,v,f,lambda p,n:'#FFF8EC' if n.z>.45 and n.x<-.1 else c,refine)

def ear(P,name,sign,c):
    # Front contour measured from H02 front; each shell is a solid wedge in plan.
    if sign<0:
        outline=[(-.69,6.80),(-1.13,7.15),(-1.55,7.85),(-1.67,8.74),(-1.17,9.98),(-.36,9.30),(.05,8.55),(.10,7.02)]
        inner=[(-.65,6.97),(-1.40,7.88),(-1.54,8.59),(-1.12,9.30),(-.65,8.98),(-.20,7.04)]
        mid=(-.50,8.20)
    else:
        outline=[(.43,6.87),(.57,8.50),(1.18,9.29),(2.34,10.0),(2.55,8.48),(2.12,7.41),(1.12,6.77)]
        inner=[(.85,6.95),(1.09,8.23),(2.08,9.44),(2.09,8.37),(1.58,7.42),(1.02,6.91)]
        mid=(1.43,8.20)
    # Solid triangular cross-sections, gently swept back; cream rims surround the inset.
    def pos(x,z,back=0):
        t=(z-6.8)/3.2
        front = .02+.65*t + (.20*(x+.8) if sign<0 else .20*(x-1.4))
        x=mid[0]+(x-mid[0])*(1+.06*math.sin(math.pi*max(0,min(1,t))))
        return (x, front+back, z)
    n=len(outline)
    v=[pos(x,z) for x,z in outline]
    for x,z in outline:
        back=pos(x,z,.85*max(0,math.sin(math.pi*min(1,max(0,(z-6.8)/3.2))))**.8+.06)
        v.append((mid[0]+(x-mid[0])*(.35 if z<9.5 else 1),back[1],z))
    v.extend([pos(*mid,.05 if sign<0 else -.60),pos(*mid,.95)])
    f=[]
    for i in range(n):
        j=(i+1)%n
        f.extend([(i,j,2*n),(n+j,n+i,2*n+1),(i,n+i,n+j,j)])
    shell=mesh(P,name+'_solid_paper',v,f,c['cream'],1)
    # Clip each front triangle against the pink outline in XZ, preserving its plane.
    def clip(poly, a, b):
        out=[]
        for u,w in zip(poly,poly[1:]+poly[:1]):
            du=(b[0]-a[0])*(u.z-a[1])-(b[1]-a[1])*(u.x-a[0])
            dw=(b[0]-a[0])*(w.z-a[1])-(b[1]-a[1])*(w.x-a[0])
            if du>=-1e-8: out.append(u)
            if (du>=0)!=(dw>=0): out.append(u+(w-u)*(du/(du-dw)))
        return out
    area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(inner,inner[1:]+inner[:1]))
    if area<0:inner.reverse()
    iv=[];inf=[]
    for i in range(n):
        poly=[Vector(v[i]),Vector(v[(i+1)%n]),Vector(v[2*n])]
        for a,b in zip(inner,inner[1:]+inner[:1]):
            poly=clip(poly,a,b)
            if not poly:break
        if len(poly)>=3:
            start=len(iv);iv.extend([(q.x,q.y-.012,q.z) for q in poly]);inf.append(tuple(range(start,len(iv))))
    ins=mesh(P,name+'_pink_inset',iv,inf,c['pink'],1)
    return P.pivot(name,(-.54 if sign<0 else .81,.28,6.88),[shell,ins])

def gem_heart(P,c):
    outline=[(0,4.59),(.62,5.05),(1.12,5.18),(1.55,5.03),(1.85,4.61),(1.94,4.29),(1.76,3.65),(1.18,2.92),(0,1.75),(-1.18,2.92),(-1.76,3.65),(-1.94,4.29),(-1.85,4.61),(-1.55,5.03),(-1.12,5.18),(-.62,5.05)]
    # The design's central diamond is an actual ridge, joined to lobe apices.
    v=[(x,-1.18 if i!=8 else -2.14,z) for i,(x,z) in enumerate(outline)]
    v.extend([(-1.12,-2.00,4.25),(1.12,-2.00,4.25),(0,-2.24,3.28),(0,-2.14,2.22),(-1.05,-1.68,5.01),(1.05,-1.68,5.01)])
    A,B,C,D,E,F=range(16,22)
    faces=[(0,1,F),(1,2,F),(2,3,F),(3,4,B),(3,B,F),(4,5,B),(5,6,B),(6,7,B),(7,C,B),(7,8,D),(7,D,C),(0,F,B),(0,B,C),
           (0,E,15),(15,E,14),(14,E,13),(13,A,12),(13,E,A),(12,A,11),(11,A,10),(10,A,9),(9,A,C),(9,D,8),(9,C,D),(0,A,E),(0,C,A)]
    fv=list(v); folded_faces=[]
    for k,f in enumerate(faces):
        if k in (0,2,4,6,8,10,11,13,15,17,19,21,23,24):
            q=sum((Vector(v[i]) for i in f),Vector())/3
            q.y-=.075
            mid=len(fv);fv.append(tuple(q))
            for i in range(3):folded_faces.append((f[(i+1)%3],f[i],mid))
        else:folded_faces.append(tuple(reversed(f)))
    front=mesh(P,'heart_front_diamond_facets',fv,folded_faces,c['pink'],2)
    backv=[(x,-.68,z) for x,z in outline]+[(-1.12,-.42,4.25),(1.12,-.42,4.25),(0,-.30,3.28),(0,-.49,2.22),(-1.05,-.75,5.01),(1.05,-.75,5.01)]
    back=mesh(P,'heart_back_facets',backv,faces,c['pink'],2)
    rv=v[:16]+backv[:16]
    rim=mesh(P,'heart_bevel',rv,[(i,(i+1)%16,16+(i+1)%16,16+i) for i in range(16)],c['pink'],1)
    for ob in (front,back,rim):
        for v in ob.data.vertices:
            v.co.x=v.co.x*1.09-.13
            v.co.y=-.60+(v.co.y+.60)*1.04-.04
    return P.pivot('heart',(-.13,-1.27,3.465),[front,back,rim])

def face_patch(P, head, name, outline, color):
    """Clip a flat mark to actual front facets; lift 12 mm along each face normal.

    Dissolving coplanar subdivision edges keeps the entire face below 40 tris.
    Coordinates are in world XZ before the asset's final size normalization.
    """
    import bmesh
    bpy.context.view_layer.update()
    bm = bmesh.new(); bm.from_mesh(head.data); bm.transform(head.matrix_world)
    bm.normal_update()
    bmesh.ops.dissolve_limit(bm, angle_limit=1e-5, verts=list(bm.verts), edges=list(bm.edges))
    bm.normal_update()
    def clip(poly, a, b):
        out = []
        for u, v in zip(poly, poly[1:] + poly[:1]):
            du = (b[0]-a[0])*(u.z-a[1]) - (b[1]-a[1])*(u.x-a[0])
            dv = (b[0]-a[0])*(v.z-a[1]) - (b[1]-a[1])*(v.x-a[0])
            if du >= -1e-8: out.append(u)
            if (du >= 0) != (dv >= 0): out.append(u + (v-u)*(du/(du-dv)))
        return out
    if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(outline,outline[1:]+outline[:1])) < 0:
        outline = outline[::-1]
    verts = []; faces = []
    for f in bm.faces:
        if f.normal.y >= -.05: continue
        poly = [v.co.copy() for v in f.verts]
        for a,b in zip(outline,outline[1:]+outline[:1]):
            poly = clip(poly,a,b)
            if not poly: break
        if len(poly) >= 3:
            start = len(verts)
            verts.extend([tuple(v + f.normal*.012) for v in poly])
            faces.append(tuple(range(start,len(verts))))
    bm.free()
    return mesh(P,name,verts,faces,color)

def build(P,spec):
    c=spec['colors']; parts=[]
    # Full-height open page block, articulated centre hinge and crisp gold covers.
    parts.append(P.box('gold_lower_cover',(6.5,6,.12),color=c['gold']))
    for s in (-1,1):
        for k in range(8):
            z=.14+k*.143
            poly=[(s*.30,z),(s*3.16,z+.04),(s*3.16,z+.155),(s*.22,z+.11)]
            parts.append(P.prism('folded_book_leaf',poly[::s],5.82,color=c['cream'] if k%2 else c['white']))
        poly=[(s*.015,1.20),(s*3.25,1.41),(s*3.25,1.50),(s*.015,1.31)]
        parts.append(P.prism('gold_upper_rim',poly[::s],6,color=c['gold']))
        poly=[(s*.025,1.31),(s*3.08,1.51),(s*3.08,1.54),(s*.025,1.37)]
        parts.append(P.prism('open_cream_page',poly[::s],5.67,color=c['cream']))
        for yy in (-2.94,2.94):
            poly=[(0,1.31),(s*.39,.13),(s*.29,.13),(0,1.09)]
            parts.append(P.prism('gold_hinge_fold',poly[::s],.05,loc=(0,yy,0),color=c['gold']))
    parts.append(sections(P,'folded_pear_body',[(1.41,1.50,1.37,.65),(1.75,1.97,1.60,.65),(2.15,2.05,1.68,.63),(2.60,2.04,1.63,.57),(3.45,1.99,1.50,.42),(4.25,1.66,1.18,.23),(4.95,.72,.65,.15)],c['cream']))
    parts.append(folded(P,'folded_chest',(0,.05,4.40),(1.72,1.32,1.22),c['cream']))
    head=head_hull(P,c['cream'])
    for v in head.data.vertices:
        v.co.x=v.co.x*1.02+.12
        if v.co.z>6.1:v.co.x=.12+(v.co.x-.12)*(1-.18*(v.co.z-6.1))
        v.co.z=5.95+(v.co.z-5.95)*1.035
        if v.co.y<0:v.co.y*=1.02
    head.data.update();parts.append(head)
    for s in (-1,1):
        foot=folded(P,'blocky_foot',(s*1.37,-1.09,2.13),(1.13,1.07,1.00),c['cream'])
        turn=Matrix.Rotation(math.radians(s*12),3,'Y');ctr=Vector((s*1.37,-1.09,2.13))
        for vertex in foot.data.vertices:vertex.co=ctr+turn@(vertex.co-ctr)
        foot.data.update();parts.append(foot)
        pad=[(s*1.37+x,2.02+z) for x,z in [(-.49,-.56),(.41,-.56),(.54,.12),(.25,.60),(-.38,.58),(-.54,.12)]]
        pad=[(s*1.37+(x-s*1.37)*math.cos(math.radians(s*12))+(z-2.13)*math.sin(math.radians(s*12)),2.13-(x-s*1.37)*math.sin(math.radians(s*12))+(z-2.13)*math.cos(math.radians(s*12))) for x,z in pad]
        parts.append(surface_patch(P,foot,'blush_sole',pad,c['blush']))
        parts.append(folded(P,'folded_forearm',(s*1.63,-.55,3.87),(.65,.85,.95),c['cream']))
        parts.append(folded(P,'hugging_paw',(s*1.76-.10,-1.77,3.44),(.58,.64,.60),c['cream']))
    parts.append(folded(P,'small_paper_tail',(.44,1.87,1.98),(.37,.39,.39),c['cream'],segs=8))
    # FA: simple readable eyes and the approved pink nose, on the head planes.
    for sign in (-1,1):
        parts.append(face_patch(P,head,'face_eye_'+str(sign),
            P.ellipse(.063,.090,6,cx=.12+sign*.62,cz=6.10), '#1F2350'))
    parts.append(face_patch(P,head,'face_nose',
        [(-.27+.12,5.65),(.12,5.43),(.27+.12,5.65)], c['pink']))
    # Folded bow tangent to the bunny's right neck: wings spread fore/aft,
    # readable as a bow in side view and as a pink ribbon in plan.
    for sign in (-1,1):
        v=[(1.76,-.10,4.91),(1.72,-.10+sign*.60,5.22),
           (1.72,-.10+sign*.60,4.62),(2.00,-.10+sign*.38,4.91),
           (1.65,-.10+sign*.38,4.91)]
        parts.append(mesh(P,'pink_bow_wing',v,[(0,1,3),(1,2,3),(2,0,3),
                          (0,4,1),(1,4,2),(2,4,0)],c['pink']))
    parts.append(P.box('blush_bow_knot',(.25,.24,.26),loc=(1.80,-.22,4.78),color=c['blush'],rot=(0,12,0)))
    animated=[ear(P,'ears0',-1,c),ear(P,'ears1',1,c),gem_heart(P,c)]
    root=P.pivot('root',(0,0,0),parts+animated)
    bpy.context.view_layer.update()
    verts=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
    e=[max(v[i] for v in verts)-min(v[i] for v in verts) for i in range(3)]
    size=spec['size_m'];root.scale=(size['w']/e[0],size['d']/e[1],size['h']/e[2])
    bpy.context.view_layer.update()
