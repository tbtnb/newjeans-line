"""P03 Tulip Bed with Fence. spec size 2.1 x .9 x .8 m; budget 800; pivots root,bob0,bob1.
SIMPLIFICATIONS: two staggered animation groups; four-point open paper cups; rear pickets are paper cards; tray stays spec white/green (no unlisted soil colour)."""

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
    import bmesh
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color);return ob


def build(P, spec):
    c=spec['colors'];groups=[[],[]]
    P.box('white planting tray',(2.1,.9,.13),color=lambda p,n:c['green'] if n.z>.5 else c['white'])
    # Full-height pointed pickets: corner posts replace the four duplicate end pickets.
    for y in [-.425,.425]:
        for x in [-.66,-.33,0,.33,.66]:
            outline=[(-.055,0),(-.055,.27),(0,.35),(.055,.27),(.055,0)]
            if y<0:P.prism('pointed white picket',outline,.035,loc=(x,y,.13),color=c['white'])
            else:P.card('rear paper picket',outline,loc=(x,y,.13),color=c['white'])
        for z in [.24,.35]:
            P.box('white fence rail',(2.02,.025,.035),loc=(0,y+.015,z),color=c['white'])
    for x in [-1.005,1.005]:
        # The side-view central picket remains a real solid board.
        P.prism('side pointed picket',[(-.055,0),(-.055,.27),(0,.35),(.055,.27),(.055,0)],.035,loc=(x,0,.13),rot=(0,0,90),color=c['white'])
        for y in [-.405,.405]:
            P.box('corner post',(.09,.09,.35),loc=(x,y,.13),color=c['white'])
            P.cyl('sun pyramid post cap',.064,.07,4,loc=(x,y,.48),r2=0,color=c['sun'],rot=(0,0,45))
    for row in range(2):
        for i in range(6):
            x=-.825+i*.33+row*.075;y=-.22+row*.44
            bottom=.44+row*.06; tip=.74+row*.06
            g=groups[i%2];co=[c['sun'],c['coral'],c['white']][(i+row*2)%3]
            g.append(P.cyl('taller green tulip stem',.012,bottom-.13,3,loc=(x,y,.13),color=c['green'],cap=False))
            # Bulbous eight-facet cup; four petal tips surround a real open centre.
            vv=[(x,y,bottom)]
            for k in range(8):
                a=math.pi*2*k/8;vv.append((x+.16*math.cos(a),y+.16*math.sin(a),bottom+.12))
            for k in range(8):
                a=math.pi*2*k/8;vv.append((x+.143*math.cos(a),y+.143*math.sin(a),tip-(.07 if k%2 else 0)))
            ff=[(0,1+k,1+(k+1)%8) for k in range(8)]
            ff += [(1+k,1+(k+1)%8,9+(k+1)%8,9+k) for k in range(8)]
            g.append(mesh(P,'large cupped four petal tulip',vv,ff,co))
            for sign in [-1,1]:
                dx=sign*.19;dy=sign*.17
                vv=[(x,y,.15),(x+dx*.12,y+dy*.12,.38),(x+dx*.70,y+dy*.32,.39),(x+dx,y+dy,.59),(x+dx*.82,y+dy*.82,.31)]
                g.append(mesh(P,'broad three dimensional creased leaf',vv,[(0,1,2),(1,3,2),(3,4,2),(4,0,2)],c['green']))
    for i,g in enumerate(groups):P.pivot('bob'+str(i),(0,0,.13),g)
    finish(P,spec)
