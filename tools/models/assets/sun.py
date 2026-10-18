"""H19 Layered Paper Sun. spec size 7.8 x 1.4 x 8 m; budget 2000; pivots root,spin,pulse.
SIMPLIFICATIONS: continuous gold crescent face strips; cloud border sheets replace tiny paper rim seams."""

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
    c=spec['colors'];center=(0,0,4.08)
    disc=[]
    for name,r,y,depth,col in [('cream outer paper rim',2.96,-.10,.19,c['cream']),('gold raised ring',2.74,-.24,.16,c['gold'])]:
        disc.append(P.lathe(name,[(0,0),(r*.96,0),(r,.06),(r*.99,depth),(r*.94,depth+.035),(0,depth+.04)],16,loc=(0,y,4.08),rot=(90,0,0),color=col))
    face=P.ico('triangulated folded sun face',1,loc=(0,-.44,4.08),scale=(2.60,.31,2.60),subdiv=2,color=c['sun'])
    # Only the front half is visible; broad triangles make the radial paper folds readable.
    face.data.update()
    P.paint(face,c['sun'])
    disc.append(face)
    rays=[]
    for i in range(16):
        a=math.pi/2+2*math.pi*i/16;R=3.90;r=2.55;wid=.70
        u=Vector((math.cos(a),0,math.sin(a)));v=Vector((-math.sin(a),0,math.cos(a)));cen=Vector(center)
        pts=[cen+u*r-v*wid,cen+u*R,cen+u*r+v*wid,cen+u*(r+.65)+Vector((0,-.42,0))]
        vv=[tuple(p+Vector((0,.12 if j==1 else .30,0))) for j,p in enumerate(pts[:3])]+[tuple(p+Vector((0,.02 if j==1 else -.12,0))) for j,p in enumerate(pts[:3])]+[tuple(pts[3])]
        rays.append(mesh(P,'folded alternating ray',vv,[(0,2,1),(0,1,4,3),(1,2,5,4),(2,0,3,5),(6,3,4),(6,4,5),(6,5,3)],c['pink'] if i%2==0 else c['gold']))
    P.pivot('spin',center,rays)
    # Raised crescent cut-paper strips are continuous, so the smile has no bead joints.
    for x in [-.95,.95]:
        outer=[(x+.39*math.cos(math.pi*j/8),4.24+.32*math.sin(math.pi*j/8)) for j in range(9)]
        inner=[(x+.28*math.cos(math.pi*j/8),4.24+.20*math.sin(math.pi*j/8)) for j in range(8,-1,-1)]
        disc.append(P.prism('creased crescent eye',outer+inner,.10,loc=(0,-.79,0),color=c['gold']))
        disc.append(P.ico('peach polygon cheek',1,loc=(x*1.17,-.78,3.85),scale=(.25,.055,.24),subdiv=1,color=c['peach']))
    outer=[(.43*math.cos(math.pi+math.pi*j/8),3.94+.29*math.sin(math.pi+math.pi*j/8)) for j in range(9)]
    inner=[(.32*math.cos(math.pi+math.pi*j/8),3.94+.18*math.sin(math.pi+math.pi*j/8)) for j in range(8,-1,-1)]
    disc.append(P.prism('continuous paper smile',outer+inner,.10,loc=(0,-.80,0),color=c['gold']))
    P.pivot('pulse',center,disc)
    for i,(x,z,rx,rz) in enumerate([(-2.28,.98,.94,.86),(-1.33,1.70,1.04,1.11),(-.22,1.25,1.16,1.20),(1.03,.66,.84,.65),(1.93,.89,.72,.70),(2.43,.49,.73,.45)]):
        depth_offset=[.10,.10,-.06,-.02,.08,.10][i]
        P.ico('peach cloud paper border',1,loc=(x,-.44+depth_offset,z),scale=(rx*1.10,.28,rz*1.10),subdiv=2,color=c['peach'])
        P.ico('cream faceted cloud',1,loc=(x,-.68+depth_offset,z+.02),scale=(rx,.38,rz),subdiv=2,color=c['cream'])

    finish(P,spec)
