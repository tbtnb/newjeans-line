"""H03 Bunny Carousel; 7.5 x 7.4 x 9 m; budget 6000 triangles.
Pivots: root; spin carries canopy/platform and bob0..5 at each rabbit seat.
SIMPLIFICATIONS: bulbs are lamp-coloured facets; striped poles use short spiral ribbons;
rabbit faces use tiny palette gold marks, saddles omit stitch lines; canopy gores
are flat folded panels and seat ears are thick paper prisms.
"""
import math,bpy
from mathutils import Vector,Matrix
BUDGET=6000

def mesh(P,name,v,f,c):
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,c);return ob

def beam(P,name,a,b,r,c,n=3):
    a=Vector(a);b=Vector(b);ob=P.cyl(name,r,(b-a).length,n,loc=a,color=c);ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return ob

def build(P,spec):
    c=spec['colors'];M=c['magenta'];G=c['gold'];K=c['cream'];R=c['pink'];C=c['cyan'];Y=c['lamp'];parts=[];bobs=[]
    # Twelve-sided laminated rotating platform.
    parts.append(P.lathe('platform',[(3.65,0),(3.75,.12),(3.75,.23),(3.70,1.02),(3.75,1.10),(3.75,1.28),(3.50,1.34)],12,color=M))
    for z,h,r in [(0,.12,3.75),(.95,.10,3.75),(1.22,.12,3.75)]:parts.append(P.cyl('gold_platform_ring',r,h,12,loc=(0,0,z),color=G))
    parts.append(P.cyl('cream_deck',3.58,.09,12,loc=(0,0,1.30),color=K))
    for k in range(24):
        a=math.tau*k/24;x=3.73*math.cos(a);y=3.73*math.sin(a)
        parts.append(P.ico('deck_bulb',.095,loc=(x,y,1.16),subdiv=1,color=Y))
    for k in range(12):
        a=math.tau*k/12;x=3.72*math.cos(a);y=3.72*math.sin(a)
        parts.append(P.prism('platform_diamond',[(0,0),(.10,.17),(0,.34),(-.10,.17)],.05,loc=(x,y,.37),rot=(0,0,math.degrees(a)+90),color=G))
    parts.append(P.lathe('central_column',[(.78,1.35),(.78,1.50),(.53,1.65),(.53,4.9),(.80,5.10),(.98,5.64),(.51,5.75)],12,color=M))
    for k in range(8):
        a=math.tau*k/8;parts.append(beam(P,'column_gold_rib',(.55*math.cos(a),.55*math.sin(a),1.58),(.55*math.cos(a),.55*math.sin(a),5.11),.04,G))
    for z,r in [(1.50,.77),(4.96,.66),(5.22,.85)]:parts.append(P.cyl('column_collar',r,.11,12,loc=(0,0,z),color=G))
    # Alternating twelve canopy gores, each with a subtle intermediate paper fold.
    N=12
    for k in range(N):
        a=math.tau*k/N;b=math.tau*(k+1)/N;mid=(a+b)/2
        vs=[(.29*math.cos(a),.29*math.sin(a),7.75),(.29*math.cos(b),.29*math.sin(b),7.75),(1.65*math.cos(a),1.65*math.sin(a),6.99),(1.65*math.cos(b),1.65*math.sin(b),6.99),(3.73*math.cos(a),3.73*math.sin(a),6.20),(3.73*math.cos(b),3.73*math.sin(b),6.20)]
        parts.append(mesh(P,'striped_paper_canopy',vs,[(0,1,3,2),(2,3,5,4)],M if k%2==0 else K))
        parts.append(beam(P,'canopy_gold_seam',vs[0],vs[2],.025,G));parts.append(beam(P,'canopy_gold_seam',vs[2],vs[4],.025,G))
        # Scalloped panels are solid shallow extrusions of the downward curved valance.
        steps=6;outer=[];inner=[]
        for j in range(steps+1):
            t=j/steps;ang=a+(b-a)*t;zz=6.05-.56*math.sin(math.pi*t)
            outer.append((3.67*math.cos(ang),3.67*math.sin(ang),zz));inner.append((3.62*math.cos(ang),3.62*math.sin(ang),zz+.12))
        top=[(3.67*math.cos(a),3.67*math.sin(a),6.20),(3.67*math.cos(b),3.67*math.sin(b),6.20)]
        parts.append(mesh(P,'scallop_pink_panel',top+outer,[(0,1)+tuple(range(steps+2,1,-1))],M))
        parts.append(mesh(P,'scallop_gold_hem',outer+inner,[(j,j+1,steps+2+j,steps+1+j) for j in range(steps)],G))
        parts.append(P.ico('eave_bulb',.16,loc=(3.69*math.cos(a),3.69*math.sin(a),6.15),subdiv=1,color=Y))
        # Tiny gold paper diamond at the centre of each pink valance.
        x=3.68*math.cos(mid);y=3.68*math.sin(mid)
        parts.append(P.prism('scallop_diamond',[(0,0),(.10,.16),(0,.32),(-.10,.16)],.04,loc=(x,y,5.66),rot=(0,0,math.degrees(mid)+90),color=G))
    parts.append(P.lathe('finial_plinth',[(.55,7.69),(.55,7.84),(.25,8.04),(.19,8.10)],8,color=G))
    # Faceted thick heart finial.
    outline=P.heart(.81,20);lo=min(z for x,z in outline);hi=max(z for x,z in outline);outline=[(x*.93,(z-lo)*.95/(hi-lo)) for x,z in outline]
    n=len(outline);v=[(x,0,8.05+z) for x,z in outline]+[(x*.69,-.26,8.14+z*.76) for x,z in outline]+[(0,-.34,8.48)]
    finial=mesh(P,'heart_finial',v,[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]+[(n+i,n+(i+1)%n,2*n) for i in range(n)]+[tuple(range(n-1,-1,-1))],R);finial.rotation_euler.z=math.pi/4;finial.scale.y=2.3;parts.append(finial)
    for k in range(6):
        a=math.tau*k/6+math.pi/24;x=2.90*math.cos(a);y=2.90*math.sin(a)
        parts.append(P.lathe('seat_pole_foot',[(.23,1.39),(.23,1.50),(.075,1.75)],6,loc=(x,y,0),color=G))
        parts.append(P.cyl('seat_pole',.09,4.21,4,loc=(x,y,1.70),color=K))
        # A continuous thin gold spiral ribbon winds around the cream pole.
        verts=[]
        for j in range(13):
            t=j/12;ang=t*math.tau*4.0
            for dz in (-.14,.14):verts.append((x+.094*math.cos(ang),y+.094*math.sin(ang),1.72+t*4.10+dz))
        parts.append(mesh(P,'spiral_gold_ribbon',verts,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(12)],G))
        parts.append(P.cyl('pole_top_cap',.23,.25,6,loc=(x,y,5.57),r2=.09,color=G))
        # Local riding rabbit: horizontal body, raised forepaws, pointed folded ears.
        rabbit=[]
        def ico(name,loc,scale,sub=2,color=K):
            ob=P.ico(name,1,loc=loc,scale=scale,subdiv=sub,color=color);rabbit.append(ob);return ob
        ico('rabbit_body',(0,0,2.48),(.64,.36,.39));ico('rabbit_haunch',(-.37,0,2.40),(.38,.36,.37),1);ico('rabbit_head',(.57,0,2.96),(.38,.32,.38));ico('rabbit_muzzle',(.82,-.01,2.88),(.22,.24,.17),1)
        ico('rabbit_tail',(-.75,.03,2.62),(.18,.16,.19),1)
        for side in (-1,1):
            ico('rabbit_rear_leg',(-.39,side*.27,2.10),(.24,.13,.30),1)
            ico('rabbit_fore_leg',(.46,side*.25,2.19),(.27,.12,.16),1)
            er=P.prism('solid_rabbit_ear',[(0,0),(-.11,.34),(-.09,.95),(.13,.75),(.17,.18)],.16,loc=(.43,side*.19,3.21),color=K,rot=(0,-19,0));rabbit.append(er)
            rabbit.append(P.prism('pink_inner_ear',[(0,.15),(-.055,.39),(-.04,.78),(.075,.64),(.10,.20)],.018,loc=(.43,side*.19-.089,3.21),color=R,rot=(0,-19,0)))
        saddle=[(-.32,.06),(.32,.06),(.29,-.30),(.21,-.43),(-.21,-.43),(-.29,-.30)]
        rabbit.append(P.prism('saddle_gold_border',saddle,.78,loc=(-.07,0,2.83),color=G))
        rabbit.append(P.prism('cyan_saddle',[(x*.76,z*.78) for x,z in saddle],.81,loc=(-.07,0,2.83),color=C))
        for side in (-1,1):
            centre=Vector((.70,side*.294,3.02));vs=[tuple(centre+Vector(v)*.04) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
            rabbit.append(mesh(P,'tiny_eye',vs,[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)],G))
        bpy.context.view_layer.update();mat=Matrix.Translation((x,y,0))@Matrix.Rotation(a+math.pi/2,4,'Z')
        for ob in rabbit:ob.matrix_world=mat@Matrix.Translation((0,0,2.48))@Matrix.Scale(1.30,4)@Matrix.Translation((0,0,-2.48))@ob.matrix_world
        bobs.append(P.pivot('bob'+str(k),(x,y,2.48),rabbit))
    spin=P.pivot('spin',(0,0,0),parts+bobs);root=P.pivot('root',(0,0,0),[spin])
    bpy.context.view_layer.update();v=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices];ext=[max(p[i] for p in v)-min(p[i] for p in v) for i in range(3)];s=spec['size_m'];root.scale=(s['w']/ext[0],s['d']/ext[1],s['h']/ext[2]);bpy.context.view_layer.update()
