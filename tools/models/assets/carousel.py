"""H03 Bunny Carousel; 7.5 x 7.4 x 9 m; budget 6000 triangles.
Pivots: root; spin carries canopy/platform and bob0..5 at each rabbit seat.
SIMPLIFICATIONS: bulbs are lamp-coloured facets; striped poles use short spiral ribbons;
rabbit faces use shared darkest plum #2A1640 flat eyes and palette pink noses, saddles omit stitch lines; canopy gores
are flat creased panels and seat ears are thick paper prisms.
"""
import math,bpy
from mathutils import Vector,Matrix
BUDGET=6000

def mesh(P,name,v,f,c):
    me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,c);return ob

def beam(P,name,a,b,r,c,n=3):
    a=Vector(a);b=Vector(b);ob=P.cyl(name,r,(b-a).length,n,loc=a,color=c);ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return ob

def face_patch(P, head, name, outline, color, offset=.012, forward=(0,-1,0)):
    """Printed low-triangle mark, clipped to the head planes and lifted along their normals."""
    import bpy
    from mathutils import Vector
    import bmesh
    bm=bmesh.new();bm.from_mesh(head.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(head.data);bm.free();head.data.update()
    bpy.context.view_layer.update()
    front=Vector(forward);right=Vector((-front.y,front.x,0));up=Vector((0,0,1))
    def uv(p):return (p.dot(right),p.z)
    def clip(poly,a,b):
        result=[]
        for p,q in zip(poly,poly[1:]+poly[:1]):
            u,v=uv(p),uv(q)
            dp=(b[0]-a[0])*(u[1]-a[1])-(b[1]-a[1])*(u[0]-a[0])
            dq=(b[0]-a[0])*(v[1]-a[1])-(b[1]-a[1])*(v[0]-a[0])
            if dp>=-1e-9:result.append(p)
            if (dp>=0)!=(dq>=0):result.append(p+(q-p)*(dp/(dp-dq)))
        return result
    if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(outline,outline[1:]+outline[:1]))<0:outline=outline[::-1]
    mw=head.matrix_world;nm=mw.to_3x3().inverted().transposed();vs=[];fs=[]
    head.data.calc_loop_triangles()
    for tri in head.data.loop_triangles:
        normal=(nm@tri.normal).normalized()
        if normal.dot(front)<.05:continue
        poly=[mw@head.data.vertices[i].co for i in tri.vertices]
        for a,b in zip(outline,outline[1:]+outline[:1]):
            poly=clip(poly,a,b)
            if len(poly)<3:break
        if len(poly)<3:continue
        for j in range(1,len(poly)-1):
            if (poly[j]-poly[0]).cross(poly[j+1]-poly[0]).length<1e-10:continue
            k=len(vs);vs.extend([tuple(p+normal*offset) for p in (poly[0],poly[j],poly[j+1])]);fs.append((k,k+1,k+2))
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color)
    return ob

def face_oval(x,z,rx,rz):
    # Six corners keep the little eyes flat and faceted.
    return [(x+rx*math.cos(i*math.tau/6),z+rz*math.sin(i*math.tau/6)) for i in range(6)]

def build(P,spec):
    c=spec['colors'];M=c['magenta'];G=c['gold'];K=c['cream'];R=c['pink'];C=c['cyan'];Y=c['lamp'];parts=[];bobs=[]
    # Twelve-sided laminated rotating platform.
    parts.append(P.lathe('platform',[(3.65,0),(3.75,.12),(3.75,.23),(3.70,1.02),(3.75,1.10),(3.75,1.28),(3.50,1.34)],12,color=M))
    for z,h,r in [(0,.12,3.75),(.95,.10,3.75),(1.22,.12,3.75)]:parts.append(P.cyl('gold_platform_ring',r,h,12,loc=(0,0,z),color=G))
    parts.append(P.cyl('cream_deck',3.58,.09,12,loc=(0,0,1.30),color=K))
    for k in range(20):
        a=math.tau*k/20;x=3.73*math.cos(a);y=3.73*math.sin(a)
        parts.append(P.ico('deck_bulb',.095,loc=(x,y,1.16),subdiv=1,color=Y))
    for k in range(12):
        a=math.tau*k/12;x=3.72*math.cos(a);y=3.72*math.sin(a)
        if k%3==0:
            parts.append(P.prism('cream_platform_plaque',[(-.27,0),(.27,0),(.31,.10),(.31,.67),(.22,.77),(-.22,.77),(-.31,.67),(-.31,.10)],.065,loc=(x,y,.20),rot=(0,0,math.degrees(a)+90),color=K))
        parts.append(P.prism('platform_diamond',[(0,0),(.10,.17),(0,.34),(-.10,.17)],.05,loc=(x,y,.37),rot=(0,0,math.degrees(a)+90),color=G))
    parts.append(P.lathe('central_column',[(.78,1.35),(.78,1.50),(.53,1.65),(.53,4.9),(.80,5.10),(.98,5.64),(.51,5.75)],12,color=M))
    for k in range(8):
        a=math.tau*k/8;parts.append(beam(P,'column_gold_rib',(.55*math.cos(a),.55*math.sin(a),1.58),(.55*math.cos(a),.55*math.sin(a),5.11),.04,G))
    for z,r in [(1.50,.77),(4.96,.66),(5.22,.85)]:parts.append(P.cyl('column_collar',r,.11,12,loc=(0,0,z),color=G))
    # Alternating twelve canopy gores, each with a subtle intermediate paper fold.
    N=12
    for k in range(N):
        a=math.tau*k/N;b=math.tau*(k+1)/N;mid=(a+b)/2
        vs=[(.29*math.cos(a),.29*math.sin(a),7.75),(.29*math.cos(b),.29*math.sin(b),7.75),(1.65*math.cos(a),1.65*math.sin(a),7.12),(1.65*math.cos(b),1.65*math.sin(b),7.12),(3.73*math.cos(a),3.73*math.sin(a),6.20),(3.73*math.cos(b),3.73*math.sin(b),6.20)]
        vs.append((3.70*math.cos(mid),3.70*math.sin(mid),6.36))
        parts.append(mesh(P,'striped_paper_canopy',vs,[(0,1,3,2),(2,3,6),(2,6,4),(6,3,5)],R if k%2==0 else K))
        for u,v in [(vs[0],vs[2]),(vs[2],vs[4])]:
            off=Vector((-math.sin(a)*.025,math.cos(a)*.025,.009));uu=Vector(u);vv=Vector(v)
            parts.append(mesh(P,'flat_gold_canopy_seam',[tuple(uu-off),tuple(uu+off),tuple(vv+off),tuple(vv-off)],[(0,1,2,3)],G))
        # Scalloped panels are solid shallow extrusions of the downward curved valance.
        steps=6;outer=[];inner=[]
        for j in range(steps+1):
            t=j/steps;ang=a+(b-a)*t;zz=6.05-.56*math.sin(math.pi*t)
            outer.append((3.67*math.cos(ang),3.67*math.sin(ang),zz));inner.append((3.70*math.cos(ang),3.70*math.sin(ang),zz+.09))
        top=[(3.67*math.cos(a),3.67*math.sin(a),6.20),(3.70*math.cos(mid),3.70*math.sin(mid),6.36),(3.67*math.cos(b),3.67*math.sin(b),6.20)]
        parts.append(mesh(P,'scallop_pink_panel',top+outer,[(0,1,2)+tuple(range(steps+3,2,-1))],M))
        cream_outer=[(x*.998,y*.998,z-.10) for x,y,z in outer]
        parts.append(mesh(P,'cream_scallop_border',outer+cream_outer,[(j,j+1,steps+2+j,steps+1+j) for j in range(steps)],K))
        for u,v in zip(top,top[1:]):parts.append(beam(P,'scallop_gold_top',u,v,.035,G,3))
        parts.append(mesh(P,'scallop_gold_hem',outer+inner,[(j,j+1,steps+2+j,steps+1+j) for j in range(steps)],G))
        parts.append(P.ico('eave_bulb',.16,loc=(3.69*math.cos(a),3.69*math.sin(a),6.15),subdiv=1,color=Y))
        # Tiny gold paper diamond at the centre of each pink valance.
        x=3.68*math.cos(mid);y=3.68*math.sin(mid)
        parts.append(P.prism('scallop_diamond',[(0,0),(.10,.16),(0,.32),(-.10,.16)],.04,loc=(x,y,5.66),rot=(0,0,math.degrees(mid)+90),color=G))
    parts.append(P.lathe('finial_plinth',[(.55,7.69),(.55,7.84),(.25,8.04),(.19,8.10)],8,color=G))
    # Faceted thick heart finial.
    outline=P.heart(.84,12);lo=min(z for x,z in outline);hi=max(z for x,z in outline);outline=[(x,(z-lo)*1.04/(hi-lo)) for x,z in outline]
    n=len(outline);v=[(x,-.06,8.00+z) for x,z in outline]+[(x,.06,8.00+z) for x,z in outline]
    v += [(x*.76,-.34,8.12+z*.76) for x,z in outline]+[(x*.76,.34,8.12+z*.76) for x,z in outline]+[(0,-.43,8.45),(0,.43,8.45)]
    fs=[]
    for i in range(n):
        j=(i+1)%n;fs.extend([(i,j,2*n+j,2*n+i),(n+j,n+i,3*n+i,3*n+j),(2*n+i,2*n+j,4*n),(3*n+j,3*n+i,4*n+1),(i,n+i,n+j,j)])
    finial=mesh(P,'gem_heart_finial',v,fs,R);finial.rotation_euler.z=math.pi/4
    P.paint(finial,M,faces={i*5+2 for i in range(n) if i%3==0});parts.append(finial)
    for k in range(6):
        a=math.tau*k/6+math.pi/16;x=2.90*math.cos(a);y=2.90*math.sin(a)
        parts.append(P.lathe('seat_pole_foot',[(.23,1.39),(.23,1.50),(.075,1.75)],6,loc=(x,y,0),color=G))
        parts.append(P.cyl('seat_pole',.09,4.21,4,loc=(x,y,1.70),color=K))
        # A continuous thin gold spiral ribbon winds around the cream pole.
        verts=[]
        for j in range(25):
            t=j/24;ang=t*math.tau*4.0
            for dz in (-.14,.14):verts.append((x+.094*math.cos(ang),y+.094*math.sin(ang),1.72+t*4.10+dz))
        parts.append(mesh(P,'spiral_gold_ribbon',verts,[(j*2,j*2+1,j*2+3,j*2+2) for j in range(24)],G))
        parts.append(P.cyl('pole_top_cap',.23,.25,6,loc=(x,y,5.57),r2=.09,color=G))
        # Local riding rabbit: horizontal body, raised forepaws, pointed folded ears.
        rabbit=[]
        def ico(name,loc,scale,sub=2,color=K):
            if name in ('rabbit_body','rabbit_head'):
                profile=[(.48,-.92),(1,-.12),(.48,.92)]
                ob=P.lathe(name,profile,6 if name=='rabbit_body' else 8,loc=loc,color=color);ob.scale=scale
            else:ob=P.ico(name,1,loc=loc,scale=scale,subdiv=sub,color=color)
            rabbit.append(ob);return ob
        ico('rabbit_body',(0,0,2.48),(.70,.38,.43));ico('rabbit_haunch',(-.37,0,2.40),(.38,.36,.37),1);head=ico('rabbit_head',(.57,0,2.96),(.43,.35,.41));muzzle=ico('rabbit_muzzle',(.82,-.01,2.88),(.22,.24,.17),1)
        ico('rabbit_tail',(-.75,.03,2.62),(.18,.16,.19),1)
        for side in (-1,1):
            ico('rabbit_rear_leg',(-.39,side*.27,2.10),(.24,.13,.30),1)
            ico('rabbit_fore_leg',(.46,side*.25,2.19),(.27,.12,.16),1)
            er=P.prism('solid_rabbit_ear',[(0,0),(-.11,.34),(-.09,.95),(.13,.75),(.17,.18)],.16,loc=(.43,side*.19,3.21),color=K,rot=(0,-19,0));rabbit.append(er)
        saddle=[(-.32,.06),(.32,.06),(.29,-.30),(.21,-.43),(-.21,-.43),(-.29,-.30)]
        rabbit.append(P.prism('saddle_gold_border',saddle,.78,loc=(-.07,0,2.83),color=G))
        rabbit.append(P.prism('cyan_saddle',[(x*.76,z*.78) for x,z in saddle],.81,loc=(-.07,0,2.83),color=C))
        # Riding rabbits keep the sheet's tangential pose; +X is their local muzzle normal.
        for side in (-1,1):
            rabbit.append(face_patch(P,head,'printed_eye',face_oval(side*.16,3.055,.022,.029),'#2A1640',forward=(1,0,0)))
        rabbit.append(face_patch(P,muzzle,'printed_pink_nose',[(-.045,2.94),(0,2.895),(.045,2.94)],R,forward=(1,0,0)))
        for ob in list(rabbit):
            if ob.name.startswith('solid_rabbit_ear'):
                import bmesh
                bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update();bmesh.ops.poke(bm,faces=[f for f in bm.faces if f.normal.y<-.7],offset=.055);bm.to_mesh(ob.data);bm.free();P.paint(ob,K)
                bpy.context.view_layer.update()
                outline=[ob.matrix_world@Vector((u,0,z)) for u,z in [(0,.15),(-.055,.39),(-.04,.78),(.075,.64),(.10,.20)]]
                rabbit.append(face_patch(P,ob,'surface_pink_inner_ear',[(v.x,v.z) for v in outline],R))
        bpy.context.view_layer.update();rise=.16 if k%2 else -.06
        mat=Matrix.Translation((x,y,rise))@Matrix.Rotation(a+math.pi/2,4,'Z')
        for ob in rabbit:ob.matrix_world=mat@Matrix.Translation((0,0,2.48))@Matrix.Diagonal((1.40,1.40,1.25,1))@Matrix.Translation((0,0,-2.48))@ob.matrix_world
        bobs.append(P.pivot('bob'+str(k),(x,y,2.48),rabbit))
    spin=P.pivot('spin',(0,0,0),parts+bobs);root=P.pivot('root',(0,0,0),[spin])
    bpy.context.view_layer.update();v=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices];ext=[max(p[i] for p in v)-min(p[i] for p in v) for i in range(3)];s=spec['size_m'];root.scale=(s['w']/ext[0],s['d']/ext[1],s['h']/ext[2]);bpy.context.view_layer.update()
