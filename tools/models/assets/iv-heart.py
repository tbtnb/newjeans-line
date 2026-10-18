"""P07 Heart IV Stand. spec size 1 x 1 x 2.2 m; budget 500; pivots root,swing.
SIMPLIFICATIONS: cream fittings replace unspec gold; tube is an angular thin hose; five actual caster wheels."""

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
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color);return ob


def build(P, spec):
    c=spec['colors'];x=.08
    P.lathe('five wheel base hub',[(.10,.10),(.10,.26),(.055,.38)],6,loc=(x,0,0),color=c['wardgray'])
    for i in range(5):
        a=math.pi/2+2*math.pi*i/5
        ex=x+.44*math.cos(a);ey=.44*math.sin(a)
        rod(P,'splayed caster leg',(x,0,.31),(ex,ey,.23),.060,c['wardgray'],3)
        P.box('cream caster fork',(.085,.085,.16),loc=(ex,ey,.065),color=c['cream'])
        P.cyl('caster wheel',.083,.075,4,loc=(ex-.0375,ey,.075),rot=(0,90,0),color=c['cream'])
    P.cyl('upright IV pole',.042,1.86,4,loc=(x,0,.29),color=c['wardgray'])
    for z in [.25,1.94,2.13]:P.cyl('cream pole collar',.035,.04,3,loc=(x,0,z),color=c['cream'])
    rod(P,'top hook arm',(x,0,2.14),(-.27,0,2.14),.022,c['cream'],3)
    for a,b in [((-.27,0,2.14),(-.29,0,2.08)),((-.29,0,2.08),(-.24,0,2.04)),((-.24,0,2.04),(-.20,0,2.08))]:rod(P,'curled hook',a,b,.018,c['cream'],3)
    P.cyl('pole finial',.036,.04,4,loc=(x,0,2.17),r2=0,color=c['cream'])
    outline=P.heart(.39,14);vv=[]
    for y,scale in [(-.04,1),(-.13,.72),(.04,1),(.11,.72)]:vv += [(u*scale-.13,y-.12,1.62+v*scale) for u,v in outline]
    vv += [(-.13,-.23,1.75),(-.13,.10,1.75)]
    ff=[]
    for i in range(14):
        j=(i+1)%14;ff +=[(i,j,14+j,14+i),(14+i,14+j,56),(28+i,57,28+j),(i,28+i,28+j,j)]
    bag=mesh(P,'inflated faceted coral heart bag',vv,ff,c['coral'])
    tabs=[bag,P.box('bag hanging tab',(.07,.05,.13),loc=(-.13,-.12,1.94),color=c['blush']),P.cyl('cream bag nozzle',.033,.09,3,loc=(-.20,-.12,1.28),color=c['cream'])]
    P.pivot('swing',(-.13,-.12,2.10),tabs)
    pts=[(-.20,-.12,1.31),(-.24,-.12,1.18),(-.20,-.12,1.04),(-.11,-.10,.97),(.035,-.04,.92),(.07,-.02,.87),(.07,-.02,.33)]
    for a,b in zip(pts,pts[1:]):rod(P,'blush drip tube',a,b,.009,c['blush'],3)
    for z in [.87,1.36]:P.box('coral hose clip',(.055,.065,.055),loc=(x,-.02,z),color=c['coral'])

    finish(P,spec)
