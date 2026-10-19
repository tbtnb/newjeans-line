"""P24 Paper Cloud — spec size 3.5 x 1.2 x 2 m; budget 300 tris.
Pivots: root at page origin, bob at the whole cloud centre.
SIMPLIFICATIONS: paper grain omitted; three frequency-two icosahedral domes and four smaller folded domes share a solid
scalloped pearl/fog backing. Top drawing is flatter than front/side, advisory.
"""
import math
import bpy
import bmesh
from mathutils import Vector
BUDGET = 300


def mesh(P, name, verts, faces, color):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces); me.update()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob); P.paint(ob, color)
    return ob


def paper_hemisphere():
    """Frequency-two icosahedron, cut on an existing ten-edge equator: 40 tris."""
    r=2/math.sqrt(5); h=1/math.sqrt(5)
    vv=[(0,-1,0)]
    for y,offset in ((-h,0),(h,math.pi/5)):
        for i in range(5):
            a=math.pi/2+i*math.tau/5+offset
            vv.append((r*math.cos(a),y,r*math.sin(a)))
    vv.append((0,1,0)); ff=[]
    for i in range(5):
        j=(i+1)%5
        ff += [(0,1+i,1+j),(1+i,6+i,1+j),(1+j,6+i,6+j),(11,6+j,6+i)]
    cache={}
    def middle(a,b):
        key=tuple(sorted((a,b)))
        if key not in cache:
            q=tuple((vv[a][j]+vv[b][j])/2 for j in range(3))
            length=math.sqrt(sum(c*c for c in q))
            cache[key]=len(vv); vv.append(tuple(c/length for c in q))
        return cache[key]
    refined=[]
    for a,b,c in ff:
        ab=middle(a,b);bc=middle(b,c);ca=middle(c,a)
        refined += [(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)]
    return vv,[f for f in refined if max(vv[i][1] for i in f)<1e-7 and min(vv[i][1] for i in f)<-1e-7]


def build(P, spec):
    c = spec['colors']; size = spec['size_m']
    # Coordinates traced in the approved front drawing, normalised below.
    def point(u, v, y):
        return ((u-319)/638, y-.40*(abs((u-319)/319)**1.5), (378-v)/362)
    outline = [(0,274),(23,214),(65,161),(97,161),(116,126),(173,100),
       (195,106),(228,51),(284,20),(349,16),(405,46),(445,121),
       (490,117),(525,135),(552,207),(576,206),(614,260),(638,300),
       (628,339),(267,378),
       (102,333),(18,322)]
    # Rear sheet is vertically straight, swept across X only as in the hero.
    n = len(outline)
    verts = [point(u,v,.60) for u,v in outline]
    verts += [point(319+(u-319)*.94, 210+(v-210)*.94,.38) for u,v in outline]
    # Triangulate the front sweep explicitly, keeping it behind the domes.
    verts.append(point(319,210,.38))
    faces = [tuple(range(n-1,-1,-1))]
    faces += [(n+i,n+(i+1)%n,2*n) for i in range(n)]
    faces += [(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
    plate = mesh(P,'solid scalloped pearl back and folded rim',verts,faces,c['pearl'])
    P.paint(plate,c['fog'],faces=set(range(1,n+1)))
    pieces = [plate]
    # Back outline -> staggered shoulder -> blunt forward crown: large paper
    # triangles form genuinely convex puffs with a tapered side silhouette.
    puffs = [(67,251,54,57,.48,.38,'white'),
             (163,203,61,72,.68,.38,'white'),
             (143,311,51,34,.47,.38,'pearl'),
             (310,143,107,96,.80,.38,'white'),
             (445,239,88,87,.80,.38,'white'),
             (555,292,53,55,.52,.38,'white'),
             (272,288,103,88,.98,.30,'white')]
    for k,(u,v,rx,rz,depth,back,col) in enumerate(puffs):
        # The measured outlines include the shallow paper shoulders that must
        # overlap their neighbours; the lower forward layer sits above the rim.
        rx *= 1.10; rz *= 1.08
        if k == 6: v = 280
        big = k in (3,4,6)
        n = 8
        m = n//2
        if k == 3: depth = .94
        if big:
            vertices,faces=paper_hemisphere()
            used=sorted({i for face in faces for i in face})
            remap={old:new for new,old in enumerate(used)}
            vertices=[point(u+rx*vertices[i][0],v-rz*vertices[i][2],back+depth*vertices[i][1]) for i in used]
            faces=[tuple(remap[i] for i in face) for face in faces]
            pieces.append(mesh(P,'geodesic folded puff %d'%k,vertices,faces,
                lambda p,n: c['pearl'] if n.x>.5 and n.z<.3 else c[col]))
            continue
        vs=[]
        for i in range(n):
            angle=i*math.tau/n
            vs.append(point(u+rx*math.cos(angle),v-rz*math.sin(angle),back))
        for i in range(m):
            angle=(2*i+1)*math.tau/n
            vs.append(point(u+rx*.74*math.cos(angle),v-rz*.74*math.sin(angle),back-depth*.70))
        fs=[]
        for i in range(m):
            a=2*i; b=(a+1)%n; d=(a+2)%n
            c0=n+i; c1=n+(i+1)%m
            fs += [(a,b,c0),(b,d,c0),(d,c1,c0)]
        crown=len(vs)
        vs.append(point(u-rx*.06,v-rz*.02,back-depth))
        fs += [(n+i,n+(i+1)%m,crown) for i in range(m)]
        pieces.append(mesh(P,'layered folded puff %d'%k,vs,fs,
            lambda p,n: c['pearl'] if n.x>.5 and n.z<.3 else c[col]))
    # Normalize the entire assembly once; plate stands on the page and its
    # footprint is centred, preserving exact spec dimensions and pivot joints.
    vv=[v.co for ob in pieces for v in ob.data.vertices]
    lo=Vector(tuple(min(v[i] for v in vv) for i in range(3)))
    hi=Vector(tuple(max(v[i] for v in vv) for i in range(3)))
    target=(size['w'],size['d'],size['h'])
    ctr=Vector(((hi.x+lo.x)/2,(hi.y+lo.y)/2,lo.z))
    for ob in pieces:
        for v in ob.data.vertices:
            v.co=Vector(tuple((v.co[i]-ctr[i])*target[i]/(hi[i]-lo[i]) for i in range(3)))
        ob.data.update()
    bob=P.pivot('bob',(0,0,size['h']/2),pieces)
    P.pivot('root',(0,0,0),[bob])
