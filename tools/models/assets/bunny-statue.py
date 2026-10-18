"""P06 Sitting Bunny Statue. spec size 1.4 x 1.4 x 2.4 m; budget 1200; pivots root,ears0,ears1.
SIMPLIFICATIONS: mint rim uses the spec light accent instead of non-spec gold; faceless sculptural head follows the hero; creased low-segment volumes and one-segment chamfered feet; no paper texture."""

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
        for u,v in outline:verts.append((x+w*u+lean*v,y+(thick/2 if back else -thick/2)*(.20+.80*math.sin(math.pi*v))+.25*v*v+.20*(w*u+lean*v),z+h*v))
    inset=[]
    for u,v in outline:
        v=.48+(v-.48)*.67
        inset.append((x+w*u*.62+lean*v,y-thick/2*(.20+.80*math.sin(math.pi*v))-.015+.25*v*v+.20*(w*u*.62+lean*v),z+h*v))
    verts+=inset
    faces=[tuple(range(7,14))]+[(i,(i+1)%7,(i+1)%7+7,i+7) for i in range(7)]+[(i,14+i,14+(i+1)%7,(i+1)%7) for i in range(7)]
    a=mesh(P,name,verts,faces,outer)
    inset.append((x+lean*.48,y-thick/2-.075+.25*.48*.48+.20*lean*.48,z+h*.48))
    b=mesh(P,name+' inset',inset,[(7,i,(i+1)%7) for i in range(7)],inner)
    return [a,b]

def folded_volume(P,name,profile,n,loc,scale,col):
    # Staggered low-segment rings: broad real triangular planes.
    vv=[];rings=[]
    for j,(r,z) in enumerate(profile):
        ring=[]
        for k in range(n if r else 1):
            a=math.tau*k/n+(j%2)*math.pi/n
            ring.append(len(vv));vv.append((loc[0]+scale[0]*r*math.cos(a),loc[1]+scale[1]*r*math.sin(a),loc[2]+scale[2]*z))
        rings.append(ring)
    ff=[]
    for a,b in zip(rings,rings[1:]):
        for i in range(n):
            j=(i+1)%n
            if len(a)==1:ff.append((a[0],b[j],b[i]))
            elif len(b)==1:ff.append((a[i],a[j],b[0]))
            else:ff += [(a[i],a[j],b[i]),(a[j],b[j],b[i])]
    return mesh(P,name,vv,ff,col)

def build(P, spec):
    c=spec['colors']; cream=c['pearl']
    base=P.lathe('low chamfered green plinth',[(0,0),(.70,.015),(.67,.17),(.65,.20),(.43,.245),(0,.255)],20,color=c['green'])
    # Slight angular crown makes the paper top visible in the exact front view.
    import bmesh
    bm=bmesh.new();bm.from_mesh(base.data)
    bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='ALTERNATE')
    bm.to_mesh(base.data);bm.free();base.data.update();P.paint(base,c['green'])
    rim=[]
    for r in (.646,.659):
        rim += [(r*math.cos(math.tau*i/20),r*math.sin(math.tau*i/20),.205) for i in range(20)]
    mesh(P,'thin spec mint plinth rim',rim,[(i,(i+1)%20,20+(i+1)%20,20+i) for i in range(20)],c['mint'])
    torso=folded_volume(P,'faceted seated pear torso',[(0,0),(.82,.02),(1,.24),(.89,.53),(.64,.84),(.50,1),(0,1.08)],10,(0,.115,.24),(.445,.42,.86),cream)
    for v in torso.data.vertices:
        t=max(0,min(1,(v.co.z-.24)/.93));v.co.y-=.25*t*t
    torso.data.update();P.paint(torso,cream)
    P.ico('angular broad cheek rabbit head',1,loc=(0,-.16,1.39),scale=(.37,.37,.35),subdiv=2,color=cream)
    P.ico('small folded cotton tail',.13,loc=(0,.52,.41),subdiv=1,color=cream)
    for sign in (-1,1):
        # Chamfered, flat-soled seated feet; pads share the same visible planar face.
        shape=[(-.19,0),(.16,0),(.24,.30),(.17,.48),(-.06,.53),(-.24,.40)]
        x=sign*.37
        foot=P.prism('chamfered seated foot',[(sign*u,v) for u,v in shape],.36,loc=(x,-.305,.245),rot=(0,sign*12,0),color=cream)
        # Cut three-dimensional corner facets without rounding the papercraft.
        bm=bmesh.new();bm.from_mesh(foot.data)
        bmesh.ops.bevel(bm,geom=list(bm.edges),offset=.045,segments=1,affect='EDGES')
        bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(foot.data);bm.free();foot.data.update();P.paint(foot,cream)
        pad=[(-.12,.015),(.10,.015),(.175,.28),(.105,.37),(-.07,.39),(-.16,.28)]
        P.prism('flat blush foot sole',[(sign*u,v) for u,v in pad],.008,loc=(x,-.491,.25),rot=(0,sign*12,0),color=c['blush'])
        folded_volume(P,'small faceted front paw',[(0,-1),(.77,-.66),(1,.15),(.61,.80),(0,1)],8,(sign*.155,-.405,.735),(.135,.135,.15),cream)
        folded_volume(P,'sloping folded shoulder',[(0,-1),(.75,-.55),(1,.10),(.63,.72),(0,1)],8,(sign*.265,-.11,.91),(.11,.15,.23),cream)
        e=ear(P,'thick folded ear',sign*.18,.025,1.60,.46,.83,cream,c['blush'],sign*.25)
        P.pivot('ears'+str((sign+1)//2),(sign*.18,.025,1.60),e)
        outline=[(0,-.035),(sign*.23,-.09),(sign*.26,.07),(sign*.04,.045)]
        verts=[(u,-.455,1.105+v) for u,v in outline]+[(sign*.14,-.53,1.105)]
        mesh(P,'creased mint bow loop',verts,[(4,(i+1)%4,i) for i in range(4)],c['mint'])
        P.prism('fork cut bow ribbon',[(0,0),(sign*.11,-.04),(sign*.24,-.30),(sign*.12,-.25),(sign*.06,-.31)],.025,loc=(0,-.44,1.14),color=c['mint'])
    P.lathe('mint neck ribbon',[(.235,0),(.245,.045),(.235,.055)],10,loc=(0,-.14,1.12),color=c['mint'])
    P.box('bow knot',(.09,.105,.105),loc=(0,-.47,1.065),color=c['mint'])
    finish(P,spec)
