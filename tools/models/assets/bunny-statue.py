"""P06 Sitting Bunny Statue. spec size 1.4 x 1.4 x 2.4 m; budget 1200; pivots root,ears0,ears1.
SIMPLIFICATIONS: face left blank as in sheet; gold base rim uses spec mint."""

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
    P.lathe('round green plinth',[(0,0),(.70,0),(.70,.10),(.66,.18),(0,.18)],20,color=c['green'])
    P.lathe('mint plinth edge',[(.66,.165),(.668,.17),(.66,.182)],20,color=c['mint'])
    P.ico('pear seated body',1,loc=(0,.08,.65),scale=(.47,.41,.54),subdiv=2,color=c['pearl'])
    P.ico('round rabbit head',1,loc=(0,-.06,1.32),scale=(.39,.35,.35),subdiv=2,color=c['pearl'])
    P.ico('cotton tail',.15,loc=(0,.42,.40),subdiv=2,color=c['pearl'])
    for sign in [-1,1]:
        P.ico('large forward foot',1,loc=(sign*.36,-.31,.42),scale=(.26,.28,.29),subdiv=2,color=c['pearl'])
        P.ico('pink foot pad',1,loc=(sign*.36,-.57,.40),scale=(.17,.037,.20),subdiv=1,color=c['blush'])
        P.ico('small front paw',1,loc=(sign*.15,-.37,.58),scale=(.12,.13,.14),subdiv=2,color=c['pearl'])
        P.ico('sloping arm',1,loc=(sign*.29,-.13,.78),scale=(.13,.14,.29),rot=(0,sign*23,0),subdiv=1,color=c['pearl'])
        e=ear(P,'thick folded ear',sign*.17,.015,1.62,.40,.79,c['pearl'],c['blush'],sign*.23)
        P.pivot('ears'+str((sign+1)//2),(sign*.17,.015,1.62),e)
        P.ico('faceted bow loop',1,loc=(sign*.14,-.35,.99),scale=(.18,.10,.10),subdiv=1,color=c['mint'])
        P.prism('bow hanging ribbon',[(0,0),(sign*.11,-.04),(sign*.24,-.30),(sign*.12,-.25),(sign*.06,-.31)],.025,loc=(0,-.35,.99),color=c['mint'])
    P.box('bow knot',(.10,.105,.12),loc=(0,-.36,.93),color=c['mint'])

    finish(P,spec)
