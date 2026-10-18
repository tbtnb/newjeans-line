"""P15 Phone cord arch. 3.6 x .6 x 3.5 m; 1200 tris; root, swing vine, pulse flowers.
SIMPLIFICATIONS: flowers pulse as a group; helical cord has triangular paper cross-section; five flowers pulse together on the swinging vine."""

import math
import bpy
from mathutils import Vector, Matrix

def mesh(P,name,verts,faces,col):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    import bmesh
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free(); me.update()
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob); P.paint(ob,col); return ob

def beam(P,name,a,b,r,col,n=6):
    a,b=Vector(a),Vector(b); ob=P.cyl(name,r,(b-a).length,n,loc=a,color=col)
    ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return ob

def heart(P,name,w,h,d,loc,col):
    # Angular lobes, a central valley, and individually triangulated convex facets.
    ol=[(0,.79),(.16,.98),(.34,1),(.5,.83),(.49,.54),(.33,.27),(0,0),(-.33,.27),(-.49,.54),(-.5,.83),(-.34,1),(-.16,.98)]
    vv=[(loc[0]+x*w,loc[1],loc[2]+z*h) for x,z in ol]+[(loc[0],loc[1]-d/2,loc[2]+h*.57),(loc[0],loc[1]+d/2,loc[2]+h*.57)]
    return mesh(P,name,vv,[(j,(j+1)%12,12) for j in range(12)]+[((j+1)%12,j,13) for j in range(12)],col)

def puffstar(P,name,r,d,loc,col):
    ol=P.star(r,r*.46); n=len(ol); vv=[(loc[0]+x,loc[1],loc[2]+z) for x,z in ol]
    vv += [(loc[0],loc[1]-d/2,loc[2]),(loc[0],loc[1]+d/2,loc[2])]
    return mesh(P,name,vv,[(i,(i+1)%n,n) for i in range(n)]+[((i+1)%n,i,n+1) for i in range(n)],col)

def ring(P,name,points,r,col,sides=6,closed=False):
    pts=[Vector(p) for p in points]; vv=[]
    for i,p in enumerate(pts):
        tangent=(pts[(i+1)%len(pts)]-pts[(i-1)%len(pts)]) if closed else (pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)])
        tangent.normalize(); u=tangent.cross(Vector((0,1,0)))
        if u.length<.01:u=tangent.cross(Vector((0,0,1)))
        u.normalize(); v=tangent.cross(u).normalized()
        vv += [tuple(p+r*(u*math.cos(j*2*math.pi/sides)+v*math.sin(j*2*math.pi/sides))) for j in range(sides)]
    ff=[]
    for i in range(len(pts) if closed else len(pts)-1):
        for j in range(sides):ff.append((i*sides+j,i*sides+(j+1)%sides,((i+1)%len(pts))*sides+(j+1)%sides,((i+1)%len(pts))*sides+j))
    if not closed:ff += [tuple(reversed(range(sides))),tuple((len(pts)-1)*sides+j for j in range(sides))]
    return mesh(P,name,vv,ff,col)

def finish(P,s,static,groups=()):
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH']; bpy.context.view_layer.update()
    pts=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
    lo=Vector(tuple(min(p[k] for p in pts) for k in range(3))); hi=Vector(tuple(max(p[k] for p in pts) for k in range(3)))
    size=s['size_m']; scale=Vector((size['w']/(hi.x-lo.x),size['d']/(hi.y-lo.y),size['h']/(hi.z-lo.z)))
    offset=Vector((-(hi.x+lo.x)/2,-(hi.y+lo.y)/2,-lo.z))
    def tf(v):return Vector(tuple((v[k]+offset[k])*scale[k] for k in range(3)))
    for ob in obs:
        mw=ob.matrix_world.copy()
        for v in ob.data.vertices:v.co=tf(mw@v.co)
        ob.matrix_world=Matrix.Identity(4)
    piv=[]
    for name,joint,children in groups:piv.append(P.pivot(name,tf(Vector(joint)),children))
    P.pivot('root',(0,0,0),static+piv)

def build(P,s):
    c=s['colors']; st=[];vine=[];flowers=[]
    for x in [-1.42,1.42]:
        st += [P.lathe('pink tapered foot',[(.27,0),(.29,.06),(.25,.24),(.21,.29)],8,loc=(x,0,0),color=c['pink']),P.cyl('cream collar',.215,.07,8,loc=(x,0,.26),color=c['cream'])]
    # Single continuous helix wraps a U-shaped arch, with genuinely open coils.
    points=[]
    for k in range(121):
        t=k/120
        if t<.25:x=-1.42;z=.36+t*6.4;tangent=Vector((0,0,1))
        elif t>.75:x=1.42;z=.36+(1-t)*6.4;tangent=Vector((0,0,-1))
        else:
            a=math.pi-(t-.25)*2*math.pi;x=1.42*math.cos(a);z=1.96+1.04*math.sin(a);tangent=Vector((1.42*math.sin(a),0,-1.04*math.cos(a))).normalized()
        u=Vector((tangent.z,0,-tangent.x));v=Vector((0,1,0));a=t*2*math.pi*17
        points.append(tuple(Vector((x,0,z))+.18*(u*math.cos(a)+v*math.sin(a))))
    vine.append(ring(P,'continuous coiled telephone cord',points,.205,c['pink'],3))
    for i,(x,z,a) in enumerate([(-1.42,1.05,-20),(-1.18,2.30,-25),(0,3.05,0),(1.18,2.30,25),(1.42,1.05,20)]):
        flowers.append(heart(P,'coral heart flower',.42,.40,.10,(x,-.29,z-.16),c['coral']))
        flowers.append(P.blade('cream petal',.10,.20,loc=(x,-.35,z-.08),color=c['cream'],bend=.10))
        for sign in [-1,1]:
            ob=P.blade('mint folded leaf',.22,.40,loc=(x+sign*.13,-.25,z-.08),color=c['mint'],rot=(0,sign*48,0),bend=.18);vine.append(ob)
    finish(P,s,st,[('swing',(-1.42,0,.3),vine),('pulse',(0,0,1.6),flowers)])

    pulse=bpy.data.objects['pivot_pulse'];swing=bpy.data.objects['pivot_swing'];mw=pulse.matrix_world.copy();pulse.parent=swing;pulse.matrix_world=mw
