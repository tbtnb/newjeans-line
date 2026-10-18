"""P01 Bunny-Ear Cottage. spec size 3 x 3 x 4 m; budget 1500; pivots root,ears,bob.
SIMPLIFICATIONS: heart glazing uses coral and sun from spec; tiny mortar and smoke wisps omitted."""

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

def ear(P,name,x,y,z,w,h,outer,inner,lean=0):
    outline=[(-.26,0),(-.49,.28),(-.43,.68),(-.13,1),(.28,.78),(.48,.40),(.25,.04)]
    verts=[]
    thick=w*.56
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
    arch=[(-1.32,0),(-1.32,1.45),(-1.13,1.94),(-.73,2.27),(0,2.45),(.73,2.27),(1.13,1.94),(1.32,1.45),(1.32,0)]
    P.prism('cream cottage walls',arch,2.45,color=c['cream'])
    # Faceted barrel roof, with full-volume hip folds at the two ends.
    profile=[(-1.5,1.45),(-1.43,1.81),(-1.20,2.19),(-.77,2.56),(0,2.72),(.77,2.56),(1.20,2.19),(1.43,1.81),(1.5,1.45)]
    verts=[]
    for y,scale in [(-1.39,.94),(-1.12,.96),(-.55,1),(.15,1),(.85,.96),(1.30,.94)]:
        verts.extend([(x*scale,y,1.45+(z-1.45)*scale) for x,z in profile])
    faces=[]
    for j in range(5):
        for i in range(8):
            a=j*9+i;faces.extend([(a,a+1,a+10),(a,a+10,a+9)])
    mesh(P,'creased coral barrel roof',verts,faces,c['coral'])
    inner=[(-1.32,1.45),(-1.25,1.72),(-1.05,2.06),(-.70,2.33),(0,2.49),(.70,2.33),(1.05,2.06),(1.25,1.72),(1.32,1.45)]
    for yy in [-1.40,1.30]:
        vv=[(x*.94,yy,1.45+(z-1.45)*.94) for x,z in profile]+[(x,yy,z) for x,z in inner]
        mesh(P,'coral roof fascia',vv,[(i,i+1,i+10,i+9) for i in range(8)],c['coral'])
        for i in range(8):
            a,b=inner[i:i+2]
            rod(P,'gold roof hem',(a[0],yy-.008,a[1]),(b[0],yy-.008,b[1]),.055,c['sun'])
    ears=[]
    for sign in [-1,1]: ears+=ear(P,'coral roof ear',sign*.64,-.55,2.45,.78,1.55,c['coral'],c['cream'],sign*.20)
    P.pivot('ears',(0,-.55,2.45),ears)
    for x in [-1.2,1.2]:
        P.box('corner foundation',(.32,2.45,.31),loc=(x,0,0),color=c['cream'])
        P.box('corner raised post',(.15,.17,1.38),loc=(x,-1.26,.27),color=c['cream'])
    door=[(-.49,0),(-.49,.74),(-.39,.99),(-.18,1.15),(0,1.18),(.28,1.08),(.49,.79),(.49,0)]
    P.prism('door arch surround',door,.08,loc=(0,-1.27,.08),color=c['sun'])
    P.prism('recessed round door',[(x*.83,z*.92) for x,z in door],.04,loc=(0,-1.33,.08),color=c['sun'])
    for x in [-.21,0,.21]:P.box('vertical door board',(.012,.01,.80),loc=(x,-1.359,.13),color=c['cream'])
    P.ico('gold round knob',.06,loc=(.27,-1.40,.57),subdiv=2,color=c['sun'])
    P.prism('heart shaped sun frame',P.heart(.43,20),.06,loc=(0,-1.25,1.72),color=c['sun'])
    P.prism('coral heart glass',P.heart(.33,20),.08,loc=(0,-1.30,1.76),color=c['coral'])
    for i in range(2):P.box('entry stair',(1.0,.30,.10),loc=(0,-1.48-i*.15,.10-i*.05),color=c['cream'])
    for x in [-.80,.80]:P.ico('folded shrub',1,loc=(x,-1.27,.29),scale=(.23,.24,.35),subdiv=1,color=c['green'])
    P.box('cream chimney',(.40,.44,.72),loc=(1.03,.80,2.19),color=c['cream'])
    P.box('coral chimney cap',(.48,.48,.12),loc=(1.03,.80,2.91),color=c['coral'])
    # Hidden at rest, the paper puff can pop above the chimney without altering the reference silhouette.
    puff=P.ico('folded chimney puff',.09,loc=(1.03,.73,2.78),subdiv=1,color=c['cream'])
    P.pivot('bob',(1.03,.73,2.81),[puff])

    finish(P,spec)
