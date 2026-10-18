"""P08 Paper Curtain Screen. spec size 2.3 x .6 x 2 m; budget 400; pivots root,gate0,gate1.
SIMPLIFICATIONS: spec thin-view exception: side/top IoU advisory; hinges use cream instead of unspec gold."""

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


def build(P, spec):
    c=spec['colors']; groups=[[],[],[]]
    xs=[-1.15,-.39,.39,1.15]; ys=[.10,-.18,.18,-.10]
    for j in range(3):
        a=Vector((xs[j],ys[j],0)); b=Vector((xs[j+1],ys[j+1],0)); dx=b-a
        # Four subtle accordion creases inside each structural panel.
        vv=[]
        for i in range(7):
            q=a+dx*(i/6);q.y+=.012*(i%2)
            vv.extend([(q.x,q.y,.24),(q.x,q.y,1.94)])
        faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(6)]
        groups[j].append(mesh(P,'pleated ward curtain',vv,faces,c['wardgray']))
        for z in [.23,1.96]: groups[j].append(rod(P,'cream panel rail',(a.x,a.y,z),(b.x,b.y,z),.025,c['cream'],4))
    for i,(x,y) in enumerate(zip(xs,ys)):
        g=groups[min(i,2)]
        g.append(P.cyl('ivory upright',.024,1.93,4,loc=(x,y,.07),color=c['cream']))
        g.append(P.cyl('post finial',.036,.055,4,loc=(x,y,1.98),r2=0,color=c['white']))
        g.append(P.box('caster cross foot',(.14,.24,.045),loc=(x,y,.064),color=c['cream']))
        for yy in [y-.10,y+.10]:g.append(P.cyl('small wheel',.04,.035,4,loc=(x-.017,yy,.04),rot=(0,90,0),color=c['white']))
    P.pivot('gate0',(-.39,-.14,1),groups[0]);P.pivot('gate1',(.39,.14,1),groups[2])

    finish(P,spec)
