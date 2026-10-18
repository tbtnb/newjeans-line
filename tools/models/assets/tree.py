"""P04 Round Paper Tree. size spec.size_m 2.3 x 2.3 x 3.5 m; budget 600; pivots root.
SIMPLIFICATIONS: hairline gold seam marks omitted; only exact spec palette used."""

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


def mesh(P,name,verts,faces,color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color);return ob


def build(P, spec):
    c=spec['colors']; w,d,h=[spec['size_m'][k] for k in ('w','d','h')]
    crown=P.ico('round triangulated crown',1,loc=(0,0,2.43),subdiv=3,color=c['mint'],scale=(1.15,1.15,1.07))
    for v in crown.data.vertices:
        if v.co.z<0:
            v.co.x*=1.09;v.co.y*=1.09
    # Selectively dissolve triangles into larger paper facets, retaining a rich geodesic silhouette.
    import bmesh
    bm=bmesh.new();bm.from_mesh(crown.data)
    edges=[e for i,e in enumerate(bm.edges) if i%3==0]
    bmesh.ops.dissolve_edges(bm,edges=edges,use_verts=False,use_face_split=False)
    bm.to_mesh(crown.data);bm.free();P.paint(crown,c['mint'])
    P.lathe('angular trunk',[(.20,0),(.17,.30),(.13,.65),(.15,1.30),(.22,1.53)],8,color=c['wood'])
    for i in range(5):
        a=2*math.pi*i/5
        verts=[(.12,0,.52),(.70,0,.025),(.25,-.18,0),(.06,-.10,.08),(.25,.18,0)]
        o=mesh(P,'folded spreading root',verts,[(0,1,2),(0,2,3),(0,4,1),(0,3,4),(1,4,3,2)],c['wood']);o.rotation_euler.z=a

    finish(P,spec)
