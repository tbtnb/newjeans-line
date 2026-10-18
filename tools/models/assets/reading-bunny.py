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
    P.lathe('mint mossy polygon plinth',[(0,0),(1.25,0),(1.31,.17),(1.26,.29),(0,.32)],18,color=c['mint'])
    P.lathe('faceted mushroom stem',[(.43,.22),(.37,.75),(.30,1.5),(.45,2.40),(.61,2.57)],12,loc=(.25,.30,0),color=c['cream'])
    cap=P.lathe('deep teal umbrella cap',[(0,2.30),(.75,2.32),(1.34,2.45),(1.40,2.55),(1.23,2.93),(.87,3.25),(.40,3.46),(0,3.5)],20,loc=(0,.10,0),color=c['teal'])
    # The mushroom canopy visibly tilts down to the right in the design.
    for v in cap.data.vertices:v.co.z-=.20*v.co.x+.31*v.co.y
    P.paint(cap,lambda p,n:c['navy'] if int(abs(p.x*7+p.y*9+p.z*5))%7==0 else c['teal'])
    gills=P.lathe('cream folded gill underside',[(0,2.32),(.45,2.32),(.94,2.39),(1.34,2.45),(1.40,2.52)],20,loc=(0,.10,0),color=c['cream'])
    for v in gills.data.vertices:v.co.z-=.20*v.co.x+.31*v.co.y+.055
    for i in range(6):
        a=2*math.pi*i/6
        rod(P,'umbrella radial paper seam',(0,.10,2.34),(1.33*math.cos(a),.10+1.33*math.sin(a),2.46),.009,c['lamp'],4)
    P.ico('seated rabbit body',1,loc=(-.05,-.37,.78),scale=(.46,.36,.46),subdiv=2,color=c['cream'])
    P.ico('reading bunny head',1,loc=(-.05,-.53,1.42),scale=(.39,.33,.36),subdiv=2,color=c['cream'])
    for sign in [-1,1]:
        e=ear(P,'reading bunny thick folded ear',-.05+sign*.17,-.42,1.67,.25,.62,c['cream'],c['lamp'],sign*.20)
        P.pivot('ears'+str((sign+1)//2),(-.05+sign*.17,-.42,1.67),e)
        P.ico('navy bead eye',.042,loc=(-.05+sign*.145,-.768,1.43),subdiv=1,color=c['navy'])
        P.ico('bunny foot',1,loc=(-.05+sign*.27,-.69,.47),scale=(.17,.22,.20),subdiv=2,color=c['cream'])
        P.ico('warm sole',1,loc=(-.05+sign*.27,-.89,.46),scale=(.10,.025,.14),subdiv=1,color=c['lamp'])
        P.ico('book holding paw',1,loc=(-.05+sign*.33,-.61,1.03),scale=(.12,.14,.13),subdiv=2,color=c['cream'])
    P.prism('tiny bunny nose',[(-.04,0),(.04,0),(0,-.04)],.022,loc=(-.05,-.798,1.35),color=c['lamp'])
    # Open book is a substantial V, page stacks and a separate spine hinge.
    pages=[]
    for sign in [-1,1]:
        outline=[(0,.05),(sign*.55,.14),(sign*.57,.04),(0,-.06)]
        ob=P.prism('navy hard book cover',outline,.60,loc=(-.05,-.86,.85),color=c['navy']);ob.rotation_euler.x=math.radians(16)
        for layer in range(2):
            p=P.prism('cream book page layer',[(0,.10+layer*.025),(sign*.51,.20+layer*.025),(sign*.52,.17+layer*.025),(0,.07+layer*.025)],.63,loc=(-.05,-.86,.85),color=c['cream']);p.rotation_euler.x=math.radians(16)
            pages.append(p)
    P.pivot('lid',(-.05,-.56,.97),pages)
    # Small bent desk lamp to the rabbit's left.
    P.cyl('lamp foot',.17,.055,10,loc=(-.89,-.32,.32),color=c['lamp'])
    for a,b in [((-.89,-.32,.36),(-.95,-.32,1.65)),((-.95,-.32,1.65),(-.69,-.32,1.96)),((-.69,-.32,1.96),(-.48,-.32,1.89))]:rod(P,'angular lamp arm',a,b,.035,c['lamp'])
    shade=P.cyl('glowing little shade',.23,.25,10,r2=.085,loc=(-.48,-.32,1.56),color=c['lamp'])
    P.pivot('pulse',(-.48,-.32,1.70),[shade])
    for i in range(10):
        a=2*math.pi*i/10;r=1.06;x=r*math.cos(a);y=r*math.sin(a)
        if y<-.80 and abs(x)<.6:continue
        P.ico('angular moss rock',1,loc=(x,y,.27+(.32+(i%3)*.15)*.9),scale=(.20,.20,.32+(i%3)*.15),subdiv=1,color=c['teal'] if i%3==0 else c['mint'])
        if i%2==0:
            for k in range(3):
                aa=k*2*math.pi/3;P.ico('small cream flower petal',.055,loc=(x+.075*math.cos(aa),y+.075*math.sin(aa),.56),subdiv=1,color=c['cream'])
            P.ico('lamp flower center',.035,loc=(x,y,.58),subdiv=1,color=c['lamp'])
    for x,y in [(-1.07,.12),(1.1,.2),(.92,-.55),(-.89,-.70)]:
        for k in range(2):P.blade('creased moss leaf',.28,.70,loc=(x,y,.27),rot=(0,(k-1)*25,k*100),color=c['teal'],bend=.3)
    for xx,zz in [(-.77,1.86),(.80,1.66)]:P.prism('floating paper glow star',P.star(.07,.028),.015,loc=(xx,-.82,zz),color=c['lamp'])
    bpy.context.view_layer.update()
    for x,z in [(-.75,2.93),(.42,3.09),(.96,2.73)]:
        hit,loc,normal,ind=cap.ray_cast(Vector((x,-3,z)),Vector((0,1,0)))
        if hit:P.prism('cap golden star',P.star(.095,.04),.018,loc=(x,loc.y+.08,z),color=c['lamp'])

    finish(P,spec)
