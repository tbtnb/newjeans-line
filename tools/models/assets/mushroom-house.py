"""P02 Paper Mushroom House. spec size 2.5 x 2.5 x 3 m; budget 1000; pivots root,pulse.
SIMPLIFICATIONS: door grain and sub-centimetre seams omitted; spots follow cap facets."""

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
    c=spec['colors']
    P.lathe('tapered cream stem',[(.87,0),(.87,.12),(.84,.40),(.57,1.00),(.56,1.47),(.65,1.63)],12,color=c['cream'])
    cap=P.lathe('faceted coral cap',[(0,1.48),(.81,1.48),(1.20,1.54),(1.25,1.64),(1.18,1.98),(.99,2.34),(.72,2.66),(.38,2.90),(0,3)],12,color=c['coral'])
    for v in cap.data.vertices:
        if v.co.z<2:v.co.z-=.16*(2-v.co.z)/.52
    rim=P.lathe('cream folded underside',[(0,1.49),(.8,1.48),(1.21,1.54),(1.25,1.60),(1.24,1.64)],12,color=c['cream'])
    for v in rim.data.vertices:v.co.z-=.16
    spots=[]
    cap.data.update();cap.data.calc_loop_triangles()
    def cross(a,b,p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
    for j,(x,y,r) in enumerate([(0,-.72,.28),(.69,-.63,.29),(-.74,-.51,.29),(.55,.55,.29),(-.55,.55,.26),(0,.20,.26),(1.04,.08,.14),(-.91,.10,.14),(.12,-1.09,.13)]):
        clip=[]
        dist=math.hypot(x,y);ux,uy=(x/dist,y/dist) if dist else (0,1)
        for k in range(6):
            rr=r*(1+.06*math.sin(k*9+j));dx=rr*math.cos(2*math.pi*k/6);dy=rr*math.sin(2*math.pi*k/6)
            radial=dx*ux+dy*uy;compress=.45 if dist>.60 else .85
            clip.append((x+dx-(1-compress)*radial*ux,y+dy-(1-compress)*radial*uy))
        vv=[];ff=[]
        for tri in cap.data.loop_triangles:
            xyz=[cap.data.vertices[i].co.copy() for i in tri.vertices]
            if tri.normal.z<.08:continue
            poly=[(p.x,p.y) for p in xyz]
            for k in range(6):
                aa,bb=clip[k],clip[(k+1)%6];out=[]
                if not poly:break
                for aa2,bb2 in zip(poly,poly[1:]+poly[:1]):
                    ca,cb=cross(aa,bb,aa2),cross(aa,bb,bb2)
                    if ca>=-1e-9:out.append(aa2)
                    if (ca>=0)!=(cb>=0):
                        t=ca/(ca-cb);out.append((aa2[0]+(bb2[0]-aa2[0])*t,aa2[1]+(bb2[1]-aa2[1])*t))
                poly=out
            if len(poly)<3:continue
            a3,b3,c3=xyz;den=cross((a3.x,a3.y),(b3.x,b3.y),(c3.x,c3.y))
            if abs(den)<1e-9:continue
            face=[]
            for xx,yy in poly:
                wb=((xx-a3.x)*(c3.y-a3.y)-(yy-a3.y)*(c3.x-a3.x))/den
                wc=((b3.x-a3.x)*(yy-a3.y)-(b3.y-a3.y)*(xx-a3.x))/den
                zz=a3.z+wb*(b3.z-a3.z)+wc*(c3.z-a3.z)+.006
                face.append(len(vv));vv.append((xx,yy,zz))
            ff.append(tuple(face))
        if ff:spots.append(mesh(P,'conforming cream paper spot',vv,ff,c['cream']))
    P.pivot('pulse',(0,0,1.53),[cap,rim]+spots)
    outline=[(-.32,0),(-.32,.78),(-.26,.94),(0,1.10),(.26,.94),(.32,.78),(.32,0)]
    P.prism('gold arched door trim',outline,.07,loc=(0,-.89,0),color=c['sun'])
    P.prism('round topped door',[(x*.81,z*.94) for x,z in outline],.08,loc=(0,-.93,0),color=c['sun'])
    for x in [-.15,0,.15]: P.box('door board crease',(.012,.006,.76),loc=(x,-.977,.02),color=c['cream'])
    P.ico('door knob',.045,loc=(.19,-1.005,.43),subdiv=2,color=c['sun'])
    # Window on the right side, face +X.
    win=P.prism('sunlit round side window',P.ellipse(.245,.29,12),.06,loc=(.84,0,.81),rot=(0,0,90),color=c['sun'])
    for a,b in [((.879,-.23,.81),(.879,.23,.81)),((.879,0,.55),(.879,0,1.07))]: rod(P,'window cross',a,b,.022,c['cream'])
    P.box('green window sill',(.16,.53,.065),loc=(.84,0,.48),color=c['green'])

    finish(P,spec)
