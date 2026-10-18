"""P06 Sitting Bunny Statue. spec size 1.4 x 1.4 x 2.4 m; budget 1200; pivots root,ears0,ears1.
SIMPLIFICATIONS: face left blank as in sheet; base rim uses spec mint because gold is absent from this asset palette; broad faceted head includes integrated cheeks."""

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
    outline=[(-.26,0),(-.49,.28),(-.43,.68),(0,1),(.43,.70),(.48,.30),(.25,.04)]
    verts=[]
    thick=w*.90
    for back in [False,True]:
        for u,v in outline:verts.append((x+w*u+lean*v,y+(thick/2 if back else -thick/2)*(.20+.80*math.sin(math.pi*v))+.40*v*v+.20*(w*u+lean*v),z+h*v))
    inset=[]
    for u,v in outline:
        v=.48+(v-.48)*.67
        inset.append((x+w*u*.62+lean*v,y-thick/2*(.20+.80*math.sin(math.pi*v))-.015+.35*v*v+.20*(w*u*.62+lean*v),z+h*v))
    verts+=inset
    faces=[tuple(range(7,14))]+[(i,(i+1)%7,(i+1)%7+7,i+7) for i in range(7)]+[(i,14+i,14+(i+1)%7,(i+1)%7) for i in range(7)]
    a=mesh(P,name,verts,faces,outer)
    inset.append((x+lean*.48,y-thick/2-.075+.35*.48*.48+.20*lean*.48,z+h*.48))
    b=mesh(P,name+' inset',inset,[(7,i,(i+1)%7) for i in range(7)],inner)
    return [a,b]

def build(P, spec):
    c=spec['colors']
    base=P.lathe('round green plinth',[(0,0),(.70,.015),(.69,.23),(.665,.32),(.39,.32),(0,.32)],16,color=c['green'])
    # Alternating paper creases on the broad side band.
    import bmesh
    bm=bmesh.new();bm.from_mesh(base.data)
    side=[f for f in bm.faces if abs(f.normal.z)<.6]
    bmesh.ops.triangulate(bm,faces=side,quad_method='ALTERNATE')
    bm.to_mesh(base.data);bm.free();base.data.update();P.paint(base,c['green'])
    rim=[]
    for r in (.660,.674):
        rim += [(r*math.cos(math.tau*i/16),r*math.sin(math.tau*i/16),.324) for i in range(16)]
    mesh(P,'thin mint paper base rim',rim,[(i,(i+1)%16,16+(i+1)%16,16+i) for i in range(16)],c['mint'])
    body=P.ico('pear seated body',1,loc=(0,.10,.76),scale=(.39,.39,.46),subdiv=2,color=c['pearl'])
    for v in body.data.vertices:
        if v.co.z>0:
            v.co.x*=1-.28*v.co.z
            v.co.y*=1-.16*v.co.z
    body.data.update()
    head=P.ico('round rabbit head with chunky cheeks',1,loc=(0,-.10,1.36),scale=(.35,.33,.32),subdiv=2,color=c['pearl'])
    for v in head.data.vertices:
        if -.70<v.co.z<.20:
            v.co.x*=1.08
            v.co.y-=.035*(1-abs(v.co.z))
    head.data.update()
    P.ico('cotton tail',.135,loc=(0,.49,.46),subdiv=1,color=c['pearl'])
    for sign in [-1,1]:
        P.ico('large forward foot',1,loc=(sign*.38,-.30,.54),scale=(.215,.26,.27),rot=(0,sign*18,0),subdiv=2,color=c['pearl'])
        P.ico('pink foot pad',1,loc=(sign*.38,-.558,.53),scale=(.15,.037,.20),rot=(0,sign*18,0),subdiv=1,color=c['blush'])
        P.ico('small front paw',1,loc=(sign*.16,-.385,.77),scale=(.14,.15,.17),subdiv=1,color=c['pearl'])
        P.ico('sloping arm',1,loc=(sign*.22,-.15,.91),scale=(.10,.12,.22),rot=(0,sign*23,0),subdiv=2,color=c['pearl'])
        e=ear(P,'thick folded ear',sign*.18,.025,1.60,.46,.83,c['pearl'],c['blush'],sign*.25)
        P.pivot('ears'+str((sign+1)//2),(sign*.18,.025,1.60),e)
        outline=[(0,-.035),(sign*.23,-.09),(sign*.26,.07),(sign*.04,.045)]
        verts=[(u,-.47,1.06+v) for u,v in outline]+[(sign*.14,-.55,1.06)]
        mesh(P,'creased mint bow loop',verts,[(4,(i+1)%4,i) for i in range(4)],c['mint'])
        P.prism('bow hanging ribbon',[(0,0),(sign*.11,-.04),(sign*.24,-.30),(sign*.12,-.25),(sign*.06,-.31)],.025,loc=(0,-.43,1.09),color=c['mint'])
    P.lathe('mint neck ribbon',[(.235,0),(.245,.045),(.235,.055)],10,loc=(0,-.07,1.075),color=c['mint'])
    P.box('bow knot',(.10,.105,.12),loc=(0,-.44,1.03),color=c['mint'])

    finish(P,spec)
