"""P05 Folded Paper Pine. size 2.1 x 2.1 x 4 m from spec; budget 400; pivot root.
SIMPLIFICATIONS: gold rim replaced by spec mint; planar fold tessellation."""

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




def build(P, spec):
    c=spec['colors']
    P.cyl('octagonal trunk',.23,.77,8,color=c['wood'])
    for i,(r,z,hh) in enumerate([(1.05,.66,1.78),(.90,1.80,1.49),(.64,2.88,1.12)]):
        # Creased cone has a midpoint ring to expose the folded triangular planes.
        o=P.lathe('folded tier '+str(i),[(0,z), (r,z),(.58*r,z+hh*.48),(0,z+hh)],10,color=lambda p,n: c['mint'] if n.x>.12 else c['teal'])
        P.lathe('paper rim '+str(i),[(r*.985,z-.014),(r,z),(r*.985,z+.025)],10,color=c['mint'])

    finish(P,spec)
