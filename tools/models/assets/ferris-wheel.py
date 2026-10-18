"""H04 Heart Ferris Wheel; size 10.7 x 4.9 x 13 m, budget 6000.
Pivots: root; wheel at horizontal Y axle; swing0..7 at cabin suspension joints,
all nested under wheel so an engine can counter-rotate cabins to retain verticality.
SIMPLIFICATIONS: eighth cabin is behind the lowest cabin (sheet front shows seven);
bulbs are six-plane paper gems in the lamp palette without emission; thin cabin glazing is opaque cyan paper.
"""
import math,bpy
from mathutils import Vector
BUDGET=6000

def mesh(P,name,v,f,c):
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,c);return ob

def beam(P,name,a,b,r,c,n=4):
    a=Vector(a);b=Vector(b);ob=P.cyl(name,r,(b-a).length,n,loc=a,color=c);ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return ob

def build(P,spec):
    c=spec['colors'];M=c['magenta'];G=c['gold'];K=c['cream'];C=c['cyan'];D=c['plum'];Y=c['lamp'];static=[];wheel=[];cabins=[]
    static += [P.box('base_gold_foot',(8.48,4.9,.18),color=G),P.box('cream_base',(8.24,4.64,.92),loc=(0,0,.18),color=K),P.box('upper_base_gold',(8.40,4.80,.14),loc=(0,0,1.10),color=G)]
    for y in (-2.30,2.30):static.append(P.box('base_gold_ribbon',(8.4,.06,.10),loc=(0,y,.47),color=G))
    for x in (-3.90,3.90):
        for y in (-2.10,2.10):
            static.extend([P.box('base_corner_post',(.67,.66,1.26),loc=(x,y,.12),color=K),P.box('post_gold_foot',(.77,.76,.15),loc=(x,y,.10),color=G),P.box('post_gold_cap',(.74,.73,.14),loc=(x,y,1.30),color=G),P.lathe('folded_diamond_finial',[(0,0),(.60,.28),(0,.80)],4,loc=(x,y,1.44),rot=(0,0,45),color=G)])
            static.append(P.box('post_magenta_panel',(.43,.045,.88),loc=(x,y-.35,.33),color=M))
            static.append(P.box('post_side_magenta_panel',(.045,.43,.88),loc=(x+(.35 if x>0 else -.35),y,.33),color=M))
    static.append(P.box('cream_platform_inlay',(7.85,4.20,.025),loc=(0,0,1.24),color=K))
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
    # Polygonal heart rim has a real open centre and two parallel gold rims.
    left=[(0,11.03),(-1.27,12.22),(-2.35,12.83),(-3.75,12.42),(-4.80,11.23),(-5.18,9.88),(-5.03,8.55),(-4.44,7.15),(-3.28,5.90),(-1.62,4.54),(0,3.75)]
    outline=left+[(-x,z) for x,z in left[-2:0:-1]];n=len(outline)
    inner=[(x*.84,8.5+(z-8.5)*.84) for x,z in outline]
    for y in (-.34,.34):
        vs=[(x,y,z) for x,z in outline]+[(x,y,z) for x,z in inner]
        wheel.append(mesh(P,'heart_rim_face',vs,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)],M))
    vs=[(x,-.34,z) for x,z in outline]+[(x,.34,z) for x,z in outline]+[(x,-.34,z) for x,z in inner]+[(x,.34,z) for x,z in inner]
    wheel.append(mesh(P,'rim_thickness',vs,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]+[(2*n+i,3*n+i,3*n+(i+1)%n,2*n+(i+1)%n) for i in range(n)],M))
    for pts in (outline,inner):
        for i,(x,z) in enumerate(pts):
            nx,nz=pts[(i+1)%n];wheel.append(beam(P,'gold_heart_outline',(x,-.38,z),(nx,-.38,nz),.040,G,3))
    for i,(x,z) in enumerate(outline):
        ix,iz=inner[i];wheel.append(P.lathe('chasing_gem_bulb',[(0,-.16),(.17,0),(0,.16)],6,loc=((x+ix)*.5,-.45,(z+iz)*.5),color=Y if i%2==0 else M))
        wheel.append(P.lathe('rear_gem_bulb',[(0,-.16),(.17,0),(0,.16)],6,loc=((x+ix)*.5,.45,(z+iz)*.5),color=Y if i%2==0 else M))
    anchors=[(-2.43,12.08),(2.43,12.08),(-4.08,9.95),(4.08,9.95),(-3.33,6.55),(3.33,6.55),(0,3.75),(0,3.75)]
    # Eight flat cream/gold spokes stop inside the rim.
    for x,z in [(0,11.03),(-4.60,9.92),(4.60,9.92),(-3.67,6.44),(3.67,6.44),(-1.20,4.45),(1.20,4.45)]:
        length=math.hypot(x,z-hubz);nx=-(z-hubz)/length;nz=x/length
        for width,depth,yy,color in [(.55,.17,0,G),(.43,.035,-.105,K)]:
            poly=[(nx*width/2,hubz+nz*width/2),(x+nx*width/2,z+nz*width/2),(x-nx*width/2,z-nz*width/2),(-nx*width/2,hubz-nz*width/2)]
            wheel.append(P.prism('laminated_paper_spoke',poly,depth,loc=(0,yy,0),color=color))
    wheel.append(P.lathe('bevelled_gold_hub',[(.72,0),(.96,.10),(1.03,.23),(.94,.37),(.75,.44)],12,loc=(0,-1.00,hubz),rot=(-90,0,0),color=G))
    wheel.append(P.cyl('cream_hub_medallion',.73,.08,12,loc=(0,-1.13,hubz),rot=(-90,0,0),color=K))
    heart=P.prism('hub_heart',P.heart(.39,12),.13,loc=(0,-1.22,hubz-.12),color=M)
    import bmesh
    bm=bmesh.new();bm.from_mesh(heart.data);bm.normal_update();bmesh.ops.poke(bm,faces=[f for f in bm.faces if f.normal.y<-.7],offset=.15);bm.to_mesh(heart.data);bm.free();P.paint(heart,M);wheel.append(heart)
    for k,(x,z) in enumerate(anchors):
        # Capsule gondolas have faceted magenta bowls, cyan windows and cream pitched roofs.
        yy=0 if k<6 else (-.05 if k==6 else .05)
        cabin=[]
        cabin.append(P.cyl('suspension_ring',.15,.10,6,loc=(x,yy-.05,z),rot=(90,0,0),color=G))
        cabin.append(beam(P,'suspension_stem',(x,yy,z-.06),(x,yy,z-.42),.065,G))
        profile=[(0,-1.96),(.47,-1.93),(.67,-1.76),(.82,-1.48),(.83,-1.34)]
        cabin.append(P.lathe('gondola_bowl',[(r,zz+z) for r,zz in profile],10,loc=(x,yy,0),color=M))
        cabin.append(P.lathe('cream_roof',[(.83,z-.81),(.73,z-.62),(.40,z-.43),(.13,z-.37)],10,loc=(x,yy,0),color=K))
        for jj in range(4):
            aa=math.tau*jj/4;eps=.022
            vv=[(x+rr*math.cos(aa+da),yy+rr*math.sin(aa+da),z+zz) for rr,zz,da in [(.832,-.81,-eps),(.832,-.81,eps),(.14,-.37,eps),(.14,-.37,-eps)]]
            cabin.append(mesh(P,'roof_gold_fold',vv,[(0,1,2,3)],G))
        for j in range(10):
            a=math.tau*j/10;b=math.tau*(j+1)/10
            vs=[(x+.808*math.cos(a),yy+.808*math.sin(a),z-1.32),(x+.808*math.cos(b),yy+.808*math.sin(b),z-1.32),(x+.785*math.cos(b),yy+.785*math.sin(b),z-.83),(x+.785*math.cos(a),yy+.785*math.sin(a),z-.83)]
            cabin.append(mesh(P,'cyan_window_pane',vs,[(0,1,2,3)],C))
            cabin.append(beam(P,'window_mullion',vs[0],vs[3],.027,G,3))
        for zz,r in [(-1.35,.84),(-.82,.84),(-.43,.30)]:cabin.append(P.cyl('gondola_gold_band',r,.055,6 if r<.5 else 10,loc=(x,yy,z+zz),color=K if r>.5 else G))
        bpy.context.view_layer.update()
        for ob in cabin:
            for v in ob.data.vertices:
                p=ob.matrix_world@v.co;p=Vector((x,yy,z))+(p-Vector((x,yy,z)))*1.15;p.y=yy+(p.y-yy)*1.08;v.co=ob.matrix_world.inverted()@p
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
