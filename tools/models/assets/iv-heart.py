"""P07 Heart IV Stand. spec size 1 x 1 x 2.2 m; budget 500; pivots root,swing.
SIMPLIFICATIONS: cream fittings replace unlisted gold; six-sided casters and paper yokes; tube is a continuous thin angular hose."""

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

def rod(P,name,a,b,r,color,segs=4):
    a,b=Vector(a),Vector(b); d=b-a
    o=P.cyl(name,r,d.length,segs,loc=a,color=color)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    return o

def mesh(P,name,verts,faces,color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces);me.update()
    import bmesh
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color);return ob


def build(P, spec):
    c=spec['colors'];x=.15
    P.lathe('pentagonal caster hub',[(.105,.12),(.105,.28),(.065,.30)],5,loc=(x,0,0),color=c['wardgray'])
    for i in range(5):
        a=math.pi/2+2*math.pi*i/5
        ex=x+.44*math.cos(a);ey=.44*math.sin(a)
        # Rectangular paper spokes sit horizontally above five recognisable casters.
        P.box('broad rectangular caster spoke',(.43,.12,.10),loc=(x+.215*math.cos(a),.215*math.sin(a),.26),rot=(0,0,math.degrees(a)),base=False,color=c['wardgray'])
        P.card('cream caster yoke',[(-.035,0),(.035,0),(.035,.14),(-.035,.14)],loc=(ex,ey,.075),color=c['cream'])
        P.cyl('six-sided caster wheel',.083,.092,6,loc=(ex-.046,ey,.083),rot=(0,90,math.degrees(a)+120),color=c['cream'])
    P.cyl('upright square IV pole',.040,1.85,4,loc=(x,0,.29),color=c['wardgray'],rot=(0,0,45))
    for z in [.32,1.94]:P.cyl('cream pole collar',.043,.035,4,loc=(x,0,z),color=c['cream'])
    P.cyl('cream pole finial',.049,.05,5,loc=(x,0,2.15),r2=.03,color=c['cream'])
    # The long squared hook reaches over the hanging loop, as on the sheet.
    pts=[(x,0,2.12),(-.18,0,2.12),(-.23,-.08,2.03),(-.18,-.08,2.02),(-.15,-.08,2.06)]
    for a,b in zip(pts,pts[1:]):rod(P,'squared hanging hook',a,b,.023,c['cream'],3)
    ol=[(0,.79),(.16,.98),(.34,1),(.5,.83),(.49,.54),(.33,.27),(0,0),(-.33,.27),(-.49,.54),(-.5,.83),(-.34,1),(-.16,.98)]
    w=.72;h=.64;cx=-.18;z0=1.38;yc=-.08;n=len(ol)
    vv=[(cx+u*w,yc,z0+v*h) for u,v in ol]
    vv += [(cx+u*w*.75,yc-.18-(.04 if v>.65 else 0),z0+h*.52+(v-.52)*h*.75) for u,v in ol]
    vv += [(cx+u*w*.75,yc+.075,z0+h*.52+(v-.52)*h*.75) for u,v in ol]
    vv += [(cx,yc-.27,z0+h*.49),(cx,yc+.12,z0+h*.55)]
    ff=[]
    for i in range(n):
        j=(i+1)%n;ff += [(i,j,n+j),(i,n+j,n+i),(n+i,n+j,3*n),(j,i,2*n+i),(j,2*n+i,2*n+j),(2*n+j,2*n+i,3*n+1)]
    bag=mesh(P,'creased gem coral heart drip bag',vv,ff,c['coral'])
    tabs=[bag,P.prism('folded blush hanging tab',[(-.037,0),(.037,0),(.026,.19),(-.025,.19)],.05,loc=(cx,yc,1.87),color=c['blush']),P.cyl('cream bag nozzle',.043,.085,4,loc=(cx,yc,1.32),r2=.060,color=c['cream']),P.box('blush drip connector',(.045,.043,.07),loc=(cx,yc,1.26),color=c['blush'])]
    P.pivot('swing',(cx,yc,2.06),tabs)
    # A continuous triangular-section hose preserves the clear soft loop.
    path=[(cx,yc,1.27),(cx+.015,yc,1.12),(cx+.07,yc,1.02),(cx+.17,yc,.95),(x-.022,-.025,.87),(x-.022,-.025,.34)]
    vv=[]
    for p in path:
        vv += [(p[0]+.009*math.cos(k*2*math.pi/3),p[1]+.009*math.sin(k*2*math.pi/3),p[2]) for k in range(3)]
    ff=[]
    for j in range(len(path)-1):
        for k in range(3):ff.append((j*3+k,j*3+(k+1)%3,(j+1)*3+(k+1)%3,(j+1)*3+k))
    mesh(P,'continuous folded blush hose',vv,ff,c['blush'])
    for z in [.87,1.43]:P.box('blush hose clip',(.060,.060,.065),loc=(x,-.025,z),color=c['blush'])
    finish(P,spec)
