"""H16 Lake Paper Pavilion — spec size 4.8 x 5.1 x 6 m; 3000 tris.
Pivots: root at page origin; swing0..7 at eight eave lantern hooks.
SIMPLIFICATIONS: side-sheet entrance orientation (+Y) follows the explicit fidelity
brief; front/top/hero draw the same entrance at -Y. No simulated lamp glow or
paper texture. Shared exact lavender #B9A6F0 and blush #FFC7DA express the
purple plinth and pink canopy panels in the approved sheets.
"""
import math
import bpy
import bmesh
from mathutils import Vector
BUDGET = 3000


def mesh(P, name, v, f, color):
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f); me.update()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.normal_update()
    if 'canopy panel' in name and sum(f.normal.z*f.calc_area() for f in bm.faces)<0:
        bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
    if 'valance' in name:
        score=sum((f.calc_center_median().x*f.normal.x+(f.calc_center_median().y+.34)*f.normal.y)*f.calc_area() for f in bm.faces)
        if score<0: bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
    bm.to_mesh(me); bm.free(); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    P.paint(ob, color)
    return ob


def build(P, spec):
    c = spec['colors']
    pearl, blue, lilac, gold, lamp = [c[k] for k in ('pearl','moon','lilac','gold','lamp')]
    lavender, blush = '#B9A6F0', '#FFC7DA'
    static = []; animated = []
    cy = -.34
    def ring(r, z, n=16):
        return [(r*math.cos(math.tau*i/n), cy+r*math.sin(math.tau*i/n), z) for i in range(n)]
    def stone(name, levels, color, facets=False):
        n = 16; vv = []; ff = []
        for r,z in levels:
            vv.extend([(r*math.cos(math.tau*(i+.5)/n),cy+r*math.sin(math.tau*(i+.5)/n),z) for i in range(n)] if 'bottom paper rim' in name else ring(r,z))
        if 'bottom paper rim' in name: ff.append(tuple(reversed(range(n))))
        for j in range(len(levels)-1):
            for i in range(n):
                a=j*n+i; b=j*n+(i+1)%n; d=a+n; e=b+n
                if facets:
                    ff.extend([(a,b,d),(b,e,d)] if i%2 else [(a,b,e),(a,e,d)])
                else: ff.append((a,b,e,d))
        if 'pearl pavilion floor' in name: ff.append(tuple(range((len(levels)-1)*n,len(levels)*n)))
        ob = mesh(P,name,vv,ff,color)
        if facets:
            P.paint(ob,lilac,faces={k for k in range(1,len(ff)-1) if k%4 in (1,2)})
        static.append(ob); return ob
    # Tall folded island. The staggered middle ring is the source of the broad
    # alternating triangular planes, rather than painted flat zigzag decoration.
    n=16
    # Offset the bottom vertices half a facet: adjacent triangle planes really
    # fold in 3D rather than drawing a zigzag across a flat cylinder wall.
    bottom=[(2.38*math.cos(math.tau*(i+.5)/n),cy+2.38*math.sin(math.tau*(i+.5)/n),.06) for i in range(n)]
    vv=bottom+ring(2.40,.78)+ring(2.20,.98)
    ff=[tuple(reversed(range(n)))]
    for i in range(n):
        j=(i+1)%n
        ff.extend([(i,n+i,n+j),(i,n+j,j),(n+i,n+j,2*n+j,2*n+i)])
    ff.append(tuple(range(2*n,3*n)))
    ob=mesh(P,'lavender island triangular folds',vv,ff,lavender)
    P.paint(ob,lilac,faces={1+3*i for i in range(n)})
    static.append(ob)
    stone('island bottom paper rim',[(2.36,0),(2.38,.06)],lilac)
    stone('thin gold plinth seam',[(2.40,.78),(2.38,.825)],gold)
    stone('upper lilac floor bevel',[(2.22,.94),(2.22,1.035),(2.14,1.10)],lilac)
    stone('pearl pavilion floor',[(2.14,1.10),(2.14,1.125)],pearl)
    stone('gold floor edge',[(2.155,1.075),(2.155,1.10)],gold)
    # Flat star inlay, visible between the open columns.
    for i in range(16):
        t=math.tau*i/16; u=t+math.tau/16
        r=.94 if i%2==0 else .44; rr=.94 if (i+1)%2==0 else .44
        static.append(mesh(P,'floor star paper inlay',[(0,cy,1.128),(r*math.cos(t),cy+r*math.sin(t),1.128),(rr*math.cos(u),cy+rr*math.sin(u),1.128)],[(0,1,2)],lilac if i%2 else lavender))
    # The explicit side-view request puts the single entrance on the +Y side.
    # One continuous five-step shell avoids buried block bottoms.
    stair_profile=[(2.68,0),(2.68,.223),(2.45,.223),(2.45,.446),(2.22,.446),(2.22,.669),(1.99,.669),(1.99,.892),(1.76,.892),(1.76,1.115),(1.44,1.115),(1.44,0)]
    static.append(P.prism('five folded pearl treads',stair_profile,1.50,rot=(0,0,90),color=pearl))
    outline=[(2.68,0),(2.68,.29),(2.40,.29),(2.40,.60),(2.16,.60),(2.16,.89),(1.90,1.14),(1.48,1.14),(1.48,0)]
    for sign in (-1,1):
        # prism uses local XZ; rotate 90 degrees to make a YZ stair cheek.
        static.append(P.prism('folded pearl stair cheek',outline,.19,loc=(sign*.83,0,0),rot=(0,0,90),color=pearl))
        static.append(P.prism('gold stair cheek edge',outline,.045,loc=(sign*.735,0,0),rot=(0,0,90),color=gold))
    # Eight cream columns: broad faceted foot, slim shaft, gilt collars,
    # and a flared cream-and-gold capital under each canopy lobe.
    for i in range(8):
        t=math.tau*i/8+math.pi/8
        x=1.79*math.cos(t); y=cy+1.79*math.sin(t)*1.05
        profile=[(.29,1.125),(.29,1.30),(.23,1.40),(.185,1.43),(.185,3.18),(.22,3.23),(.29,3.38),(.29,3.46)]
        column=P.lathe('pearl faceted column',profile,8,loc=(x,y,0),color=pearl)
        P.paint(column,gold,faces={f.index for f in column.data.polygons if 1.39 < f.center.z < 1.44 or 3.18 < f.center.z < 3.24 or 3.38 < f.center.z < 3.46})
        # These caps are buried in the floor/eave; keep the budget on visible
        # octagonal shafts and capital folds.
        bm=bmesh.new();bm.from_mesh(column.data);bm.normal_update()
        bmesh.ops.delete(bm,geom=[f for f in bm.faces if abs(f.normal.z)>.999],context='FACES_ONLY')
        bm.to_mesh(column.data);bm.free();column.data.update()
        static.append(column)
    # Sixteen strips alternate blue and pink/lilac. Each strip has large
    # triangular folds; the wavy hem is sampled 4 times per scallop.
    N=32; rings=[]
    for band,(r,z) in enumerate([(.14,4.96),(.72,4.72),(1.37,4.33),(1.85,3.81),(2.15,3.48)]):
        pts=[]
        for i in range(N):
            t=math.tau*i/N
            wave=.34*(.5+.5*math.cos(8*t))*(r/2.15)**3
            # Stagger the main folds at successive rings, keeping a shared
            # watertight boundary between all neighbouring triangles.
            fold=(.045 if band in (1,2,3) else 0)*math.sin(math.pi*r/2.15)*math.cos(8*t+band*math.pi/2)
            radial=r+(.025 if i%2 and band in (1,2,3) else 0)
            crease=.025 if i%2 and band in (1,2,3) else 0
            pts.append((radial*math.cos(t),cy+radial*math.sin(t)*1.05,z+wave+fold+crease))
        rings.append(pts)
    # Continuous shared rings prevent cracks at the radial fold boundaries.
    # Every triangular facet contributes to the dome and scallop silhouette.
    for band in range(4):
        for i in range(N):
            j=(i+1)%N
            v=[rings[band][i],rings[band][j],rings[band+1][j],rings[band+1][i]]
            col=blue if (i//2)%2==0 else (blush if (i//4)%2 else lilac)
            fs=[(0,1,2),(0,2,3)]
            ob=mesh(P,'folded canopy panel',v,fs,col)
            static.append(ob)
    for i in range(N):
        j=(i+1)%N;p=rings[-1][i];q=rings[-1][j]
        # Gold hem follows the scalloped roof. The purple fabric-paper valance
        # dips farther at each lobe midpoint, giving it a rounded cut-paper edge.
        t=math.tau*i/N; u=math.tau*j/N
        dp=.13+.10*(.5-.5*math.cos(8*t));dq=.13+.10*(.5-.5*math.cos(8*u))
        static.append(mesh(P,'gold scalloped valance binding',[p,q,(q[0],q[1],q[2]-.09),(p[0],p[1],p[2]-.09)],[(0,3,2,1)],gold))
        static.append(mesh(P,'purple scalloped valance',[(p[0],p[1],p[2]-.09),(q[0],q[1],q[2]-.09),(q[0]*.99,cy+(q[1]-cy)*.99,q[2]-.09-dq),(p[0]*.99,cy+(p[1]-cy)*.99,p[2]-.09-dp)],[(0,3,2,1)],lavender))
    for i in range(8):
        t=math.tau*i/8;x=1.85*math.cos(t);y=cy+1.85*math.sin(t)*1.05;z=3.70
        parts=[P.cyl('gold lantern suspension',.025,.24,6,loc=(x,y,3.46),color=gold,cap=False)]
        parts.append(P.lathe('gold lantern hook',[(0,3.46),(.058,3.40),(0,3.32)],6,loc=(x,y,0),color=gold))
        parts.append(P.lathe('six facet warm lantern',[(0,2.65),(.115,2.71),(.21,2.94),(.21,3.01),(.115,3.21),(0,3.29)],6,loc=(x,y,0),color=lamp))
        P.paint(parts[-1],gold,faces={f.index for f in parts[-1].data.polygons if f.center.z<2.74 or f.center.z>3.14})
        parts.append(P.lathe('gold lantern tassel',[(0,2.49),(.06,2.56),(0,2.64)],6,loc=(x,y,0),color=gold))
        animated.append(P.pivot('swing'+str(i),(x,y,z),parts))
    # Pedestal and separate finial stem; crescent is a thick bevelled concave
    # shell with a continuous curved inset, not a flat cut-out moon.
    static.append(P.lathe('gold finial socket',[(.29,4.92),(.29,5.005),(.13,5.045),(.08,5.06)],8,loc=(0,cy,0),color=gold))
    static.append(P.cyl('gold crescent stem',.045,.09,8,loc=(0,cy,5.055),color=gold))
    # Two faceted crescent shells meet at sharp tips. The medial ridge is
    # real depth, so its triangular paper planes remain visible in iso/side.
    outer=[(.34,5.99),(.12,6.0),(-.10,5.91),(-.23,5.76),(-.28,5.54),(-.23,5.34),(-.09,5.20),(.13,5.16),(.37,5.23),(.51,5.39)]
    inner=[(.34,5.99),(.24,5.96),(.10,5.90),(-.01,5.77),(-.07,5.58),(-.03,5.42),(.08,5.31),(.25,5.29),(.42,5.34),(.51,5.39)]
    outer=[(.115+(x-.115)*1.12,6-(6-z)*1.06) for x,z in outer]
    inner=[(.115+(x-.115)*1.12,6-(6-z)*1.06) for x,z in inner]
    n=len(outer);v=[];f=[]
    for face_sign in (-1,1):
        for path,depth in ((outer,.025),(inner,.025),([(0.5*(a[0]+b[0]),0.5*(a[1]+b[1])) for a,b in zip(outer,inner)],.11)):
            v.extend([(x,cy+face_sign*(.008+depth*math.sqrt(max(0,1-((z-5.555)/.445)**2))),z) for x,z in path])
    for i in range(n-1):
        j=i+1
        for side in (0,3*n):
            f.extend([(side+i,side+j,side+2*n+j),(side+i,side+2*n+j,side+2*n+i),
                      (side+n+i,side+2*n+i,side+2*n+j),(side+n+i,side+2*n+j,side+n+j)])
        f.extend([(i,3*n+i,3*n+j,j),(n+j,4*n+j,4*n+i,n+i)])
    moon=mesh(P,'gold crescent folded silhouette',v,f,gold)
    bm=bmesh.new();bm.from_mesh(moon.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(moon.data);bm.free();moon.data.update();P.paint(moon,gold)
    static.append(moon)
    bpy.context.view_layer.update()
    pts=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices]
    lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)]
    size=spec['size_m'];sc=[size[k]/(hi[i]-lo[i]) for i,k in enumerate(('w','d','h'))]
    offset=Vector((.5*(hi[0]+lo[0]),.5*(hi[1]+lo[1]),lo[2]))
    for ob in static+animated: ob.location-=offset
    root=P.pivot('root',(0,0,0),static+animated)
    root.scale=sc
    bpy.context.view_layer.update()
