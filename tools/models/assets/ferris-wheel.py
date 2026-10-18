"""H04 Heart Ferris Wheel; size 10.7 x 4.9 x 13 m, budget 6000.
Pivots: root; wheel at horizontal Y axle; swing0..7 at cabin suspension joints,
all nested under wheel so an engine can counter-rotate cabins to retain verticality.
SIMPLIFICATIONS: eighth cabin is behind the lowest cabin (sheet front shows seven);
bulbs use lamp palette without emission; thin cabin glazing is opaque cyan paper.
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
            static.extend([P.box('base_corner_post',(.67,.66,1.26),loc=(x,y,.12),color=K),P.box('post_gold_foot',(.77,.76,.15),loc=(x,y,.10),color=G),P.box('post_gold_cap',(.74,.73,.14),loc=(x,y,1.30),color=G),P.cyl('pyramid_finial',.42,.55,4,loc=(x,y,1.44),r2=0,rot=(0,0,45),color=G)])
            static.append(P.box('post_magenta_panel',(.43,.045,.88),loc=(x,y-.35,.33),color=M))
    hubz=8.05
    # Two A frames, with the front frame's plum paper inset visible between gold edges.
    for y in (-.73,.73):
        for side in (-1,1):
            poly=[(side*.20,hubz+.06),(side*1.08,hubz-.02),(side*3.38,1.13),(side*2.35,1.13)]
            static.append(P.prism('A_frame_paper_leg',poly[::side],.34,loc=(0,y,0),color=K))
            inner=[(side*.42,hubz-.57),(side*.83,hubz-.65),(side*3.05,1.35),(side*2.55,1.35)]
            static.append(P.prism('plum_leg_inset',inner[::side],.04,loc=(0,y-.20,0),color=D))
            for u,v in [(poly[0],poly[3]),(poly[1],poly[2])]:static.append(beam(P,'gold_leg_edge',(u[0],y-.20,u[1]),(v[0],y-.20,v[1]),.045,G))
            static.append(P.box('frame_gold_shoe',(.90,.69,.20),loc=(side*2.85,y,1.06),color=G))
        static.append(beam(P,'crossbar',(-2.75,y,1.56),(2.75,y,1.56),.09,G))
    # Front/back spreaders make the true depth and structural A shape readable from the side.
    for side in (-1,1):
        for sy in (-1,1):static.append(beam(P,'depth_brace',(side*.28,0,hubz-.35),(side*2.82,sy*1.93,1.11),.115,K,8))
    for side in (-1,1):
        poly=[(side*.12,hubz-.15),(side*.57,hubz-.15),(side*2.08,1.13),(side*1.42,1.13)]
        static.append(P.prism('side_A_frame',poly[::side],.40,loc=(.15,0,0),rot=(0,0,90),color=K))
        inner=[(side*.31,hubz-.65),(side*.45,hubz-.65),(side*1.91,1.35),(side*1.68,1.35)]
        static.append(P.prism('side_plum_inset',inner[::side],.04,loc=(.38,0,0),rot=(0,0,90),color=D))
    static.append(beam(P,'horizontal_axle',(0,-1.18,hubz),(0,1.18,hubz),.22,G,12))
    # Polygonal heart rim has a real open centre and two parallel gold rims.
    left=[(0,11.03),(-1.27,12.22),(-2.35,12.83),(-3.75,12.42),(-4.80,11.23),(-5.18,9.88),(-5.03,8.55),(-4.44,7.15),(-3.28,5.90),(-1.62,4.54),(0,3.75)]
    outline=left+[(-x,z) for x,z in left[-2:0:-1]];n=len(outline)
    inner=[(x*.865,8.5+(z-8.5)*.865) for x,z in outline]
    for y in (-.25,.25):
        vs=[(x,y,z) for x,z in outline]+[(x,y,z) for x,z in inner]
        wheel.append(mesh(P,'heart_rim_face',vs,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)],M))
    vs=[(x,-.25,z) for x,z in outline]+[(x,.25,z) for x,z in outline]+[(x,-.25,z) for x,z in inner]+[(x,.25,z) for x,z in inner]
    wheel.append(mesh(P,'rim_thickness',vs,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]+[(2*n+i,3*n+i,3*n+(i+1)%n,2*n+(i+1)%n) for i in range(n)],M))
    for pts in (outline,inner):
        for i,(x,z) in enumerate(pts):
            nx,nz=pts[(i+1)%n];wheel.append(beam(P,'gold_heart_outline',(x,-.29,z),(nx,-.29,nz),.040,G))
    for i,(x,z) in enumerate(outline):
        ix,iz=inner[i];wheel.append(P.ico('chasing_bulb',.15,loc=((x+ix)*.5,-.36,(z+iz)*.5),subdiv=1,color=Y if i%2==0 else M))
        if i%2==0:wheel.append(P.ico('rear_rim_bulb',.14,loc=((x+ix)*.5,.36,(z+iz)*.5),subdiv=1,color=Y))
    anchors=[(-2.43,11.93),(2.43,11.93),(-4.08,9.55),(4.08,9.55),(-3.33,6.78),(3.33,6.78),(0,4.13),(0,4.13)]
    # Eight flat cream/gold spokes stop inside the rim.
    for x,z in anchors:
        wheel.append(beam(P,'cream_spoke',(0,0,hubz),(x,0,z),.21,K,4))
        wheel.append(beam(P,'gold_spoke_trim',(0,-.23,hubz),(x,-.23,z),.035,G,4))
    wheel.append(P.cyl('gold_hub',.94,.30,12,loc=(0,-1.05,hubz),rot=(-90,0,0),color=G))
    wheel.append(P.cyl('cream_hub_medallion',.65,.08,12,loc=(0,-1.13,hubz),rot=(-90,0,0),color=K))
    wheel.append(P.prism('hub_heart',P.heart(.34,20),.13,loc=(0,-1.21,hubz-.12),color=M))
    for k,(x,z) in enumerate(anchors):
        # Capsule gondolas have faceted magenta bowls, cyan windows and cream pitched roofs.
        yy=-.05 if k<6 else (-.90 if k==6 else .90)
        cabin=[]
        cabin.append(P.cyl('suspension_ring',.15,.10,6,loc=(x,yy-.05,z),rot=(90,0,0),color=G))
        cabin.append(beam(P,'suspension_stem',(x,yy,z-.06),(x,yy,z-.42),.065,G))
        profile=[(0,-1.96),(.47,-1.93),(.73,-1.72),(.83,-1.47),(.83,-1.34)]
        cabin.append(P.lathe('gondola_bowl',[(r,zz+z) for r,zz in profile],10,loc=(x,yy,0),color=M))
        cabin.append(P.lathe('cream_roof',[(.83,z-.81),(.73,z-.62),(.40,z-.43),(.13,z-.37)],10,loc=(x,yy,0),color=K))
        for jj in range(4):
            aa=math.tau*jj/4;eps=.022
            vv=[(x+rr*math.cos(aa+da),yy+rr*math.sin(aa+da),z+zz) for rr,zz,da in [(.832,-.81,-eps),(.832,-.81,eps),(.14,-.37,eps),(.14,-.37,-eps)]]
            cabin.append(mesh(P,'roof_gold_fold',vv,[(0,1,2,3)],G))
        for j in range(8):
            a=math.tau*j/8;b=math.tau*(j+1)/8
            vs=[(x+.808*math.cos(a),yy+.808*math.sin(a),z-1.32),(x+.808*math.cos(b),yy+.808*math.sin(b),z-1.32),(x+.785*math.cos(b),yy+.785*math.sin(b),z-.83),(x+.785*math.cos(a),yy+.785*math.sin(a),z-.83)]
            cabin.append(mesh(P,'cyan_window_pane',vs,[(0,1,2,3)],C))
            cabin.append(beam(P,'window_mullion',vs[0],vs[3],.028,G,4))
        for zz,r in [(-1.35,.85),(-.82,.85),(-.43,.38)]:cabin.append(P.cyl('gondola_gold_band',r,.055,4 if r<.5 else 8,loc=(x,yy,z+zz),color=G))
        bpy.context.view_layer.update()
        for ob in cabin:
            for v in ob.data.vertices:
                p=ob.matrix_world@v.co;p=Vector((x,yy,z))+(p-Vector((x,yy,z)))*1.15;v.co=ob.matrix_world.inverted()@p
        joint=P.pivot('swing'+str(k),(x,yy,z),cabin)
        joint['counter_rotation_axis']='Y';joint['counter_rotation_factor']=-1.0;joint['counter_rotation_parent']='pivot_wheel';joint['pendulum_axis']='X'
        cabins.append(joint)
    wp=P.pivot('wheel',(0,0,hubz),wheel+cabins);root=P.pivot('root',(0,0,0),static+[wp])
    bpy.context.view_layer.update();v=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices];ext=[max(p[i] for p in v)-min(p[i] for p in v) for i in range(3)];s=spec['size_m'];root.scale=(s['w']/ext[0],s['d']/ext[1],s['h']/ext[2]);bpy.context.view_layer.update()
