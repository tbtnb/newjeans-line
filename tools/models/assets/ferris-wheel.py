"""H04 Heart Ferris Wheel; size 10.7 x 4.9 x 13 m, budget 6000.
Pivots: root; wheel at horizontal Y axle; swing0..7 at cabin suspension joints,
all nested under wheel so an engine can counter-rotate cabins to retain verticality.
SIMPLIFICATIONS: eighth cabin overlaps the lowest cabin in front (the sheet shows seven);
opaque cyan paper replaces glass; non-emissive rim studs have simpler rear facets;
the top sheet widens the base relative to the front, so front + hero govern its width.
"""
import math,bpy
from mathutils import Vector
BUDGET=6000

def mesh(P,name,v,f,c):
    import bmesh
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,c);return ob

def beam(P,name,a,b,r,c,n=4):
    a=Vector(a);b=Vector(b);ob=P.cyl(name,r,(b-a).length,n,loc=a,color=c);ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return ob

def build(P,spec):
    c=spec['colors'];M=c['magenta'];G=c['gold'];K=c['cream'];C=c['cyan'];D=c['plum'];Y=c['lamp'];static=[];wheel=[];cabins=[]
    static += [P.box('base_gold_foot',(8.48,4.9,.18),color=G),P.box('cream_base',(8.24,4.64,1.02),loc=(0,0,.18),color=K),P.box('upper_base_gold',(8.40,4.80,.14),loc=(0,0,1.20),color=G)]
    for y in (-2.30,2.30):static.append(P.box('base_gold_ribbon',(8.4,.06,.10),loc=(0,y,.47),color=G))
    for x in (-3.78,3.78):
        for y in (-1.94,1.94):
            static.extend([P.box('base_corner_post',(1.05,.90,1.42),loc=(x,y,.12),color=K),P.box('post_gold_foot',(1.28,1.02,.15),loc=(x,y,.10),color=G),P.box('post_gold_cap',(1.13,.99,.14),loc=(x,y,1.45),color=G),P.lathe('folded_diamond_finial',[(.58,0),(.64,.16),(0,.75)],4,loc=(x,y,1.59),rot=(0,0,45),color=G)])
            static.append(P.box('post_magenta_panel',(.70,.045,1.01),loc=(x,y-.47,.33),color=M))
            static.append(P.box('post_side_magenta_panel',(.045,.58,1.01),loc=(x+(.54 if x>0 else -.54),y,.33),color=M))
    static.append(P.box('cream_platform_inlay',(7.85,4.20,.025),loc=(0,0,1.34),color=K))
    hubz=8.05
    # Two A frames, with the front frame's plum paper inset visible between gold edges.
    for y in (-.73,.73):
        for side in (-1,1):
            poly=[(side*.20,hubz+.06),(side*1.08,hubz-.02),(side*3.38,1.13),(side*2.35,1.13)]
            static.append(P.prism('A_frame_paper_leg',poly[::side],.34,loc=(0,y,0),color=K))
            inner=[(side*1.42,4.70),(side*1.96,4.60),(side*3.05,1.35),(side*2.55,1.35)]
            static.append(P.prism('plum_leg_inset',inner[::side],.04,loc=(0,y-.20,0),color=D))
            for u,v in [(poly[0],poly[3]),(poly[1],poly[2])]:static.append(beam(P,'gold_leg_edge',(u[0],y-.20,u[1]),(v[0],y-.20,v[1]),.045,G))
            static.append(P.box('frame_gold_shoe',(.90,.69,.20),loc=(side*2.85,y,1.06),color=G))
        static.append(beam(P,'crossbar',(-2.75,y,1.56),(2.75,y,1.56),.09,G))
    # Four folded legs spread toward the actual base corners in plan view.
    bpy.context.view_layer.update()
    for ob in static:
        if ob.name.startswith(('A_frame_paper_leg','plum_leg_inset','gold_leg_edge','frame_gold_shoe','crossbar')):
            inv=ob.matrix_world.inverted()
            for vertex in ob.data.vertices:
                pt=ob.matrix_world@vertex.co
                pt.y *= .36+2.04*max(0,min(1,(hubz-pt.z)/(hubz-1.13)))
                vertex.co=inv@pt
            ob.data.update()
    for sx in [-1,1]:
        for sy in [-1,1]:
            points=[]
            for z,half in [(1.37,.26),(4.65,.13)]:
                t=(z-1.13)/(hubz-1.13);xx=sx*(3.38+(1.08-3.38)*t+.012)
                yy=sy*.73*(.36+2.04*(1-t))
                points.extend([(xx,yy-half,z),(xx,yy+half,z)])
            static.append(mesh(P,'side_plum_leg_panel',points,[(0,1,3,2)],D))
    static.append(beam(P,'horizontal_axle',(0,-1.18,hubz),(0,1.18,hubz),.22,G,12))
    # Independent outer and inner contours traced from the approved front sheet.
    # A radial scale would make the cleft too deep and pinch its ribbon to a point.
    def trace(points):
        return [((x-338)*spec['size_m']['w']/654,(794-z)*spec['size_m']['h']/784) for x,z in points]
    left_o=trace([(338,91),(269,29),(205,10),(94,49),(36,120),(12,199),
                  (17,265),(41,335),(95,406),(169,474),(253,536),(338,567)])
    left_i=trace([(338,143),(260,78),(205,60),(123,92),(76,144),(51,204),
                  (56,258),(79,316),(126,377),(192,435),(267,496),(338,526)])
    outline=left_o+[(-x,z) for x,z in left_o[-2:0:-1]]
    inner=left_i+[(-x,z) for x,z in left_i[-2:0:-1]]
    n=len(outline)
    middle=[((a[0]+b[0])/2,(a[1]+b[1])/2) for a,b in zip(outline,inner)]
    for sign in (-1,1):
        vs=[(x,sign*.34,z) for x,z in outline]+[(x,sign*.49,z) for x,z in middle]+[(x,sign*.34,z) for x,z in inner]
        fs=[]
        for i in range(n):
            j=(i+1)%n
            fs.extend([(i,j,n+j),(i,n+j,n+i),(n+i,n+j,2*n+j),(n+i,2*n+j,2*n+i)])
        wheel.append(mesh(P,'folded_magenta_heart_ribbon',vs,fs,M))
    vs=[(x,-.34,z) for x,z in outline]+[(x,.34,z) for x,z in outline]+[(x,-.34,z) for x,z in inner]+[(x,.34,z) for x,z in inner]
    wheel.append(mesh(P,'rim_thickness',vs,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]+[(2*n+i,3*n+i,3*n+(i+1)%n,2*n+(i+1)%n) for i in range(n)],M))
    for pts in (outline,inner):
        for i,(x,z) in enumerate(pts):
            nx,nz=pts[(i+1)%n];wheel.append(beam(P,'gold_heart_outline',(x,-.36,z),(nx,-.36,nz),.034,G,3))
    # Gold studs project from the ribbon rather than sitting edge-on like diamonds.
    for i,(x,z) in enumerate(middle):
        for yy in (-.53,.53):
            color=Y if i%2==0 else M
            if yy<0:
                wheel.append(P.ico('rim_gold_stud',.19,loc=(x,yy,z),color=color,subdiv=1,scale=(1,.70,1)))
            else:
                # Eight rear facets retain the stud silhouette at a smaller tri cost.
                vv=[(x-.17,yy,z),(x+.17,yy,z),(x,yy-.12,z),(x,yy+.12,z),
                    (x,yy,z-.17),(x,yy,z+.17)]
                ff=[(a,b,c) for a in (0,1) for b in (2,3) for c in (4,5)]
                wheel.append(mesh(P,'rear_folded_rim_stud',vv,ff,color))
    anchors=[(-2.43,12.08),(2.43,12.08),(-4.02,9.78),(4.02,9.78),(-3.42,6.60),(3.42,6.60),(0,3.67),(0,3.67)]
    # Eight flat cream/gold spokes stop inside the rim.
    for x,z in [(0,11.61),(-4.55,10.18),(4.55,10.18),(-3.67,6.44),(3.67,6.44),(-1.20,4.45),(1.20,4.45),(-2.30,11.76),(2.30,11.76)]:
        length=math.hypot(x,z-hubz);nx=-(z-hubz)/length;nz=x/length
        for width,depth,yy,color in [(.63,.17,0,G),(.51,.035,-.105,K)]:
            poly=[(nx*width/2,hubz+nz*width/2),(x+nx*width/2,z+nz*width/2),(x-nx*width/2,z-nz*width/2),(-nx*width/2,hubz-nz*width/2)]
            wheel.append(P.prism('laminated_paper_spoke',poly,depth,loc=(0,yy,0),color=color))
    wheel.append(P.lathe('bevelled_gold_hub',[(.72,0),(.96,.10),(1.03,.23),(.94,.37),(.75,.44)],12,loc=(0,-1.00,hubz),rot=(-90,0,0),color=G))
    wheel.append(P.cyl('cream_hub_medallion',.73,.08,12,loc=(0,-1.13,hubz),rot=(-90,0,0),color=K))
    heart=P.prism('hub_heart',P.heart(.39,12),.13,loc=(0,-1.22,hubz-.12),color=M)
    import bmesh
    bm=bmesh.new();bm.from_mesh(heart.data);bm.normal_update();bmesh.ops.poke(bm,faces=[f for f in bm.faces if f.normal.y<-.7],offset=.15);bm.to_mesh(heart.data);bm.free();P.paint(heart,M);wheel.append(heart)
    for k,(x,z) in enumerate(anchors):
        # Twelve-sided spherical cabins: faceted bowls, broad cyan windows,
        # cream folded shoulders and gold suspension caps, all with real depth.
        yy=0 if k<6 else (-.07 if k==6 else .07)
        cabin=[]
        cabin.append(P.cyl('suspension_gold_joint',.19,.10,10,loc=(x,yy-.13,z),rot=(90,0,0),color=G))
        cabin.append(P.ico('suspension_pink_button',.125,loc=(x,yy-.25,z),color=M,subdiv=1,scale=(1,.45,1)))
        cabin.append(beam(P,'suspension_stem',(x,yy,z-.06),(x,yy,z-.48),.075,G,6))
        # A single continuous shell avoids invisible cap triangles between bands.
        profile=[(0,-2.24),(.48,-2.20),(.76,-2.02),(.91,-1.75),(.94,-1.52),
                 (.96,-1.38),(.94,-1.05),(.86,-.81),(.68,-.57),(.43,-.42),
                 (.23,-.24),(0,-.22)]
        def cabin_color(center,normal):
            zz=center.z-z
            if zz < -1.52:return M
            if zz < -1.38:return K
            if zz < -.81:return C
            if zz < -.50:return K
            return G
        cabin.append(P.lathe('continuous_faceted_gondola',[(r,z+zz) for r,zz in profile],12,loc=(x,yy,0),color=cabin_color))
        for j in range(12):
            a=math.tau*j/12
            dx,dy=.034*math.sin(a),-.034*math.cos(a)
            lo=(x+.962*math.cos(a),yy+.962*math.sin(a),z-1.40)
            hi=(x+.883*math.cos(a),yy+.883*math.sin(a),z-.80)
            mid=(x+.991*math.cos(a),yy+.991*math.sin(a),z-1.10)
            vv=[(lo[0]+dx,lo[1]+dy,lo[2]),(hi[0]+dx,hi[1]+dy,hi[2]),
                (hi[0]-dx,hi[1]-dy,hi[2]),(lo[0]-dx,lo[1]-dy,lo[2]),mid]
            mullion=mesh(P,'creased_cream_gold_window_mullion',vv,[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],K)
            P.paint(mullion,G,faces={1,2});cabin.append(mullion)
        joint=P.pivot('swing'+str(k),(x,yy,z),cabin)
        joint['counter_rotation_axis']='Y';joint['counter_rotation_factor']=-1.0;joint['counter_rotation_parent']='pivot_wheel';joint['pendulum_axis']='X'
        cabins.append(joint)
    # Small single-crease chamfers on the four plinth corner blocks.
    import bmesh
    for ob in static:
        if ob.name.startswith('base_corner_post'):
            bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.bevel(bm,geom=list(bm.edges),offset=.065,segments=1,affect='EDGES');bm.to_mesh(ob.data);bm.free();P.paint(ob,K)
    wp=P.pivot('wheel',(0,0,hubz),wheel+cabins);root=P.pivot('root',(0,0,0),static+[wp])
    bpy.context.view_layer.update();v=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices];ext=[max(p[i] for p in v)-min(p[i] for p in v) for i in range(3)];s=spec['size_m'];root.scale=(s['w']/ext[0],s['d']/ext[1],s['h']/ext[2]);bpy.context.view_layer.update()
