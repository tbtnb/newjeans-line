"""H19 Layered Paper Sun. spec size 7.8 x 1.4 x 8 m; budget 2000; pivots root,spin,pulse.
SIMPLIFICATIONS: smile and eyes are palette gold rods; cloud facets replace tiny paper rim seams."""

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
    c=spec['colors'];center=(0,0,4.35)
    disc=[]
    for name,r,y,depth,col in [('cream outer paper rim',2.96,-.10,.19,c['cream']),('gold raised ring',2.74,-.24,.16,c['gold']),('sun face',2.56,-.36,.20,c['sun'])]:
        disc.append(P.lathe(name,[(0,0),(r*.87,0),(r,.10),(r*.99,depth),(r*.75,depth+.035),(0,depth+.12)],24,loc=(0,y,4.35),rot=(90,0,0),color=col))
    rays=[]
    for i in range(16):
        a=math.pi/2+2*math.pi*i/16;R=3.90;r=2.55;wid=.70
        u=Vector((math.cos(a),0,math.sin(a)));v=Vector((-math.sin(a),0,math.cos(a)));cen=Vector(center)
        pts=[cen+u*r-v*wid,cen+u*R,cen+u*r+v*wid,cen+u*(r+.65)+Vector((0,-.42,0))]
        vv=[tuple(p+Vector((0,.30,0))) for p in pts[:3]]+[tuple(p+Vector((0,-.12,0))) for p in pts[:3]]+[tuple(pts[3])]
        rays.append(mesh(P,'folded alternating ray',vv,[(0,2,1),(0,1,4,3),(1,2,5,4),(2,0,3,5),(6,3,4),(6,4,5),(6,5,3)],c['pink'] if i%2==0 else c['gold']))
    P.pivot('spin',center,rays)
    # Raised smiling face, closed crescent eyes.
    for x in [-.95,.95]:
        for j in range(6):
            a=math.pi*j/6;b=math.pi*(j+1)/6
            disc.append(rod(P,'closed smiling eye',(x+.38*math.cos(a),-.66,4.51+.30*math.sin(a)),(x+.38*math.cos(b),-.66,4.51+.30*math.sin(b)),.045,c['gold'],4))
        disc.append(P.ico('peach cheek',1,loc=(x*1.17,-.66,4.12),scale=(.25,.05,.24),subdiv=2,color=c['peach']))
    for j in range(6):
        a=math.pi+math.pi*j/6;b=math.pi+math.pi*(j+1)/6
        disc.append(rod(P,'curved sun smile',(.40*math.cos(a),-.67,4.21+.27*math.sin(a)),(.40*math.cos(b),-.67,4.21+.27*math.sin(b)),.045,c['gold'],4))
    P.pivot('pulse',center,disc)
    for i,(x,z,rx,rz) in enumerate([(-2.28,.94,.94,.90),(-1.33,1.45,1.04,1.11),(-.22,1.05,1.16,1.05),(1.03,.65,.84,.65),(1.93,.86,.72,.70),(2.43,.44,.73,.45)]):
        P.ico('peach cloud paper border',1,loc=(x,-.44,z),scale=(rx*1.045,.36,rz*1.045),subdiv=1,color=c['peach'])
        P.ico('cream faceted cloud',1,loc=(x,-.68,z+.02),scale=(rx,.38,rz),subdiv=2,color=c['cream'])

    finish(P,spec)
