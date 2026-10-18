"""H18 Reading Bunny under Mushroom. spec size 2.8 x 2.9 x 3.5 m; budget 2500; pivots root,ears0,ears1,lid,pulse.
SIMPLIFICATIONS: book print and tiny star wires omitted; pink ears use warm lamp tone because pink is absent from spec palette."""

import math
import bpy
from mathutils import Vector, Matrix

def finish(P, spec):
    """Bake the measured world geometry before parenting; anisotropic object scales can introduce shear."""
    bpy.context.view_layer.update()
    obs=list(bpy.context.scene.objects)
    old_world={o:o.matrix_world.copy() for o in obs}
    parents={o:o.parent for o in obs}
    pts=[old_world[o]@v.co for o in obs if o.type=='MESH' for v in o.data.vertices]
    lo=Vector(tuple(min(p[k] for p in pts) for k in range(3)))
    hi=Vector(tuple(max(p[k] for p in pts) for k in range(3)))
    target=Vector(tuple(spec['size_m'][k] for k in ('w','d','h')))
    center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
    scale=Vector(tuple(target[k]/(hi[k]-lo[k]) for k in range(3)))
    transform=Matrix.Diagonal((*scale,1))@Matrix.Translation(-center)
    for o in obs:
        o.parent=None;o.matrix_parent_inverse=Matrix.Identity(4)
        if o.type=='MESH':
            world=transform@old_world[o]
            for v in o.data.vertices:v.co=world@v.co
            o.matrix_world=Matrix.Identity(4);o.data.update()
        else:o.matrix_world=Matrix.Translation(transform@old_world[o].translation)
    def depth(o):return 1+depth(parents[o]) if parents[o] else 0
    for o in sorted(obs,key=depth):
        if parents[o]:
            bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=parents[o]
            o.matrix_parent_inverse=o.parent.matrix_world.inverted();o.matrix_world=mw
    bpy.context.view_layer.update()
    P.pivot('root',(0,0,0),[o for o in obs if o.parent is None])

def rod(P,name,a,b,r,color,segs=6):
    a,b=Vector(a),Vector(b); d=b-a
    o=P.cyl(name,r,d.length,segs,loc=a,color=color)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    return o

def mesh(P,name,verts,faces,color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color);return ob

def ear(P,name,x,y,z,w,h,outer,inner,lean=0):
    outline=[(-.26,0),(-.49,.28),(-.43,.68),(-.13,1),(.28,.78),(.48,.40),(.25,.04)]
    verts=[]
    thick=w*.64
    for back in [False,True]:
        for u,v in outline:verts.append((x+w*u+lean*v,y+(thick/2 if back else -thick/2)*(.20+.80*math.sin(math.pi*v))+.18*v*v+.35*(w*u+lean*v),z+h*v))
    inset=[]
    for u,v in outline:
        v=.48+(v-.48)*.67
        inset.append((x+w*u*.62+lean*v,y-thick/2*(.20+.80*math.sin(math.pi*v))-.015+.14*v*v+.35*(w*u*.62+lean*v),z+h*v))
    verts+=inset
    faces=[tuple(range(7,14))]+[(i,(i+1)%7,(i+1)%7+7,i+7) for i in range(7)]+[(i,14+i,14+(i+1)%7,(i+1)%7) for i in range(7)]
    a=mesh(P,name,verts,faces,outer)
    inset.append((x+lean*.48,y-thick/2-.075+.35*lean*.48,z+h*.48))
    b=mesh(P,name+' inset',inset,[(7,i,(i+1)%7) for i in range(7)],inner)
    return [a,b]

def build(P, spec):
    c=spec['colors']
    # A shallow many-sided paper plinth with a triangulated top.
    base=P.lathe('mint polygon plinth',[(0,0),(1.34,0),(1.32,.23),(1.27,.30),(0,.30)],16,color=c['mint'])
    # Twelve broad canopy panels, explicitly triangulated along their creases.
    N=12; rings=[(1.42,2.32),(1.30,2.60),(.91,3.08),(.44,3.36)]
    vv=[]
    def canopy_z(x,y,z): return z-.17*x-.19*y
    for ring_index,(radius,z) in enumerate(rings):
        for i in range(N):
            ang=math.tau*i/N;x=radius*math.cos(ang);y=radius*math.sin(ang)
            vv.append((x,y+.22,canopy_z(x,y,z)))
    vv.append((0,.10,3.50));ff=[]
    for k in range(3):
        for i in range(N):
            j=(i+1)%N;a=k*N+i;b=k*N+j;d=(k+1)*N+i;e=(k+1)*N+j
            ff.extend([(a,b,e),(a,e,d)] if (i+k)%2 else [(a,b,d),(b,e,d)])
    ff += [(36+i,36+(i+1)%N,48) for i in range(N)]
    cap=mesh(P,'creased twelve-panel mushroom canopy',vv,ff,c['teal'])
    P.paint(cap,c['navy'],faces={4,5,6,7,28,29,30,31,52,53,54,55,74,75})
    # Folded cream underside: ridge and valley alternation remains visible under the brim.
    gv=[(.15,.24,2.40)]
    for radius,z in [(.68,2.29),(1.39,2.29)]:
        for i in range(24):
            t=math.tau*i/24;x=radius*math.cos(t);y=radius*math.sin(t)
            gv.append((x,y+.22,canopy_z(x,y,z)+(.065 if i%2 else 0)))
    gf=[]
    for i in range(24):
        j=(i+1)%24;gf.extend([(0,1+i,1+j),(1+i,25+i,25+j),(1+i,25+j,1+j)])
    mesh(P,'creased radial mushroom gills',gv,[tuple(reversed(f)) for f in gf],c['cream'])
    stem=P.lathe('angular tapered mushroom stem',[(.55,.28),(.47,.72),(.34,1.50),(.36,2.12),(.60,2.40)],8,loc=(.30,.36,0),color=c['cream'])
    for i in range(6):
        idx=i*2
        path=[vv[k*N+idx] for k in [3,2,1,0]]
        for q,r in zip(path,path[1:]): rod(P,'gold canopy panel seam',q,r,.009,c['lamp'],3)
    for i in range(N):rod(P,'gold polygon brim',vv[i],vv[(i+1)%N],.010,c['lamp'],3)
    P.ico('seated rabbit body',1,loc=(-.05,-.37,.76),scale=(.43,.33,.43),subdiv=2,color=c['cream'])
    P.ico('reading bunny head',1,loc=(-.05,-.58,1.35),scale=(.38,.32,.34),subdiv=2,color=c['cream'])
    for sign in [-1,1]:
        e=ear(P,'reading bunny thick folded ear',-.05+sign*.17,-.42,1.58,.29,.66,c['cream'],c['lamp'],sign*.20)
        P.pivot('ears'+str((sign+1)//2),(-.05+sign*.17,-.42,1.58),e)
        P.ico('navy bead eye',.042,loc=(-.05+sign*.145,-.88,1.37),subdiv=1,color=c['navy'])
        P.ico('bunny foot',1,loc=(-.05+sign*.27,-.78,.51),scale=(.17,.22,.22),subdiv=2,color=c['cream'])
        P.ico('warm sole',1,loc=(-.05+sign*.27,-.99,.50),scale=(.10,.025,.14),subdiv=1,color=c['lamp'])
        P.ico('book holding paw',1,loc=(-.05+sign*.39,-.72,1.15),scale=(.115,.12,.11),subdiv=1,color=c['cream'])
    P.prism('tiny bunny nose',[(-.04,0),(.04,0),(0,-.04)],.022,loc=(-.05,-.90,1.29),color=c['lamp'])
    # Open V book, cream page stacks riding on a spine hinge.
    pages=[]
    for sign in [-1,1]:
        outline=[(0,0),(sign*.63,.20),(sign*.63,.09),(0,-.11)]
        ob=P.prism('navy hard book cover',outline,.63,loc=(-.05,-.85,.86),color=c['navy']);ob.rotation_euler.x=math.radians(23)
        for layer in range(3):
            outline=[(0,.05+layer*.025),(sign*.25,.18+layer*.025),(sign*.58,.25+layer*.025),(sign*.59,.225+layer*.025),(sign*.25,.155+layer*.025),(0,.025+layer*.025)]
            p=P.prism('folded cream book leaf',outline,.63,loc=(-.05,-.85,.86),color=c['cream']);p.rotation_euler.x=math.radians(23)
            pages.append(p)
        rod(P,'gold book cover corner',(-.05+sign*.62,-1.12,.88),(-.05+sign*.62,-.58,1.08),.018,c['lamp'],4)
    P.prism('navy folded cover below pages',[(-.63,.16),(0,-.08),(.63,.16),(.47,-.33),(0,-.41),(-.47,-.33)],.08,loc=(-.05,-1.10,.86),color=c['navy'])
    P.cyl('navy book spine',.095,.48,8,loc=(-.05,-1.12,.84),rot=(-90,0,0),color=c['navy'])
    P.pivot('lid',(-.05,-.56,.97),pages)
    # Small bent desk lamp to the rabbit's left.
    P.cyl('lamp foot',.17,.055,10,loc=(-.89,-.32,.32),color=c['lamp'])
    for a,b in [((-.89,-.32,.36),(-.95,-.32,1.65)),((-.95,-.32,1.65),(-.69,-.32,1.96)),((-.69,-.32,1.96),(-.48,-.32,1.89))]:rod(P,'angular lamp arm',a,b,.035,c['lamp'])
    shade=P.cyl('glowing little shade',.23,.25,10,r2=.085,loc=(-.48,-.32,1.56),color=c['lamp'])
    P.pivot('pulse',(-.48,-.32,1.70),[shade])
    for i in range(8):
        a=2*math.pi*i/8;r=1.06;x=r*math.cos(a);y=r*math.sin(a)
        if y<-.80 and abs(x)<.6:continue
        P.ico('angular moss rock',1,loc=(x,y,.27+(.32+(i%3)*.15)*.9),scale=(.20,.20,.24+(i%3)*.10),subdiv=1,color=c['teal'] if i%3==0 else c['mint'])
    # Visible five-petal daisies frame the feet and lamp, instead of hiding inside moss.
    for x,y,z,r in [(-1.02,-.66,.61,.075),(-.78,-1.02,.45,.065),(1.00,-.71,.59,.09),(.77,-1.00,.44,.06),(-1.02,.20,.72,.065)]:
        for k in range(5):
            aa=math.tau*k/5
            P.prism('cream five petal daisy',P.ellipse(r*.65,r*.75,4),.01,loc=(x+r*math.cos(aa),y-.04,z+r*math.sin(aa)),color=c['cream'])
        P.ico('gold daisy heart',.038,loc=(x,y-.065,z),subdiv=1,color=c['lamp'])
    for x,y in [(-1.07,.12),(1.1,.2),(.92,-.55),(-.89,-.70)]:
        for k in range(2):P.blade('creased moss leaf',.29,.61,loc=(x,y,.27),rot=(0,(k-1)*25,k*100),color=c['teal'],bend=.3)
    for xx,zz in [(-1.10,1.90),(.88,1.65),(-.31,1.62)]:P.prism('floating paper glow star',P.star(.07,.028,n=4),.015,loc=(xx,-.82,zz),color=c['lamp'])
    bpy.context.view_layer.update()
    for x,z,r in [(-.75,2.79,.07),(.20,3.01,.12),(.91,2.47,.065),(-.23,2.98,.055)]:
        hit,loc,normal,ind=cap.ray_cast(Vector((x,-3,z)),Vector((0,1,0)))
        if hit:
            outline=P.star(r,r*.28,n=4)
            front=[(x+xx,loc.y-.02,z+zz) for xx,zz in outline]
            center=(x,loc.y-.11,z)
            mesh(P,'raised four point gold canopy star',front+[center],[(8,(i+1)%8,i) for i in range(8)],c['lamp'])

    finish(P,spec)
