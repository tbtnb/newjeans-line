"""P14 Hanging crescent. 3 x .4 x 4 m; 600 tris; root, swing at suspension.
SIMPLIFICATIONS: tiny star beads represented by faceted diamonds; no glow."""

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
    outline=[(0,.79),(.16,.98),(.34,1),(.5,.83),(.49,.54),(.33,.27),(0,0),(-.33,.27),(-.49,.54),(-.5,.83),(-.34,1),(-.16,.98)]
    outline=[(x*w,z*h) for x,z in outline]; n=len(outline)
    vv=[]
    for y,k in [(0,1),(-d*.42,.77),(d*.42,.77)]:
        vv += [(loc[0]+x*k,loc[1]+y,loc[2]+h*.53+(z-h*.53)*k) for x,z in outline]
    vv += [(loc[0],loc[1]-d*.5,loc[2]+h*.55),(loc[0],loc[1]+d*.5,loc[2]+h*.55)]
    ff=[]
    for i in range(n):
        j=(i+1)%n
        ff += [(i,j,n+j),(i,n+j,n+i),(i,2*n+i,2*n+j),(i,2*n+j,j),(n+i,n+j,3*n),(2*n+j,2*n+i,3*n+1)]
    return mesh(P,name,vv,ff,col)

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
    c=s['colors']; parts=[]
    # Explicit outer and inner arcs reproduce the wide left crescent and slender tips.
    outer=[(.96,3.48),(.12,3.53),(-.50,3.34),(-.95,3.0),(-1.28,2.6),(-1.49,2.0),(-1.44,1.4),(-1.26,1.0),(-1.03,.6),(-.44,.2),(.05,.02),(.77,.2),(1.1,.4),(1.28,.6),(1.5,1.0)]
    inner=[(.96,3.48),(.54,3.2),(.22,3.0),(.02,2.8),(-.23,2.4),(-.36,2.0),(-.27,1.6),(-.11,1.2),(.08,1.0),(.48,.8),(.90,.73),(1.14,.8),(1.5,1.0)]
    # Annular ribbon with interpolated arc samples, ridge at centre depth.
    def samples(arr,n):
        lens=[0]
        for a,b in zip(arr,arr[1:]):lens.append(lens[-1]+math.dist(a,b))
        out=[]
        for i in range(n):
            t=lens[-1]*i/(n-1);k=next((j for j in range(len(lens)-1) if lens[j+1]>=t),len(lens)-2);f=(t-lens[k])/(lens[k+1]-lens[k]);out.append(tuple(arr[k][q]*(1-f)+arr[k+1][q]*f for q in [0,1]))
        return out
    n=20; out=samples(outer,n);inn=samples(inner,n);vv=[]
    for y in [-.065,.065]:vv += [(x,y*math.sin(math.pi*i/(n-1)),z) for i,(x,z) in enumerate(out)]+[(x,y*math.sin(math.pi*i/(n-1)),z) for i,(x,z) in enumerate(inn)]
    vv += [((out[i][0]+inn[i][0])/2,-.2*max(0,min(1,((out[i][0]+inn[i][0])/2+1.45)/.55,(1.48-(out[i][0]+inn[i][0])/2)/.60)),(out[i][1]+inn[i][1])/2) for i in range(n)]
    vv += [((out[i][0]+inn[i][0])/2,.2*max(0,min(1,((out[i][0]+inn[i][0])/2+1.45)/.55,(1.48-(out[i][0]+inn[i][0])/2)/.60)),(out[i][1]+inn[i][1])/2) for i in range(n)]
    ff=[]
    for i in range(n-1):
        j=i+1;ff += [(i,j,4*n+i),(j,4*n+j,4*n+i),(n+i,4*n+i,n+j),(n+j,4*n+i,4*n+j),(2*n+i,5*n+i,2*n+j),(2*n+j,5*n+i,5*n+j),(3*n+i,3*n+j,5*n+i),(3*n+j,5*n+j,5*n+i),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
    body=mesh(P,'layered faceted crescent',vv,ff,c['gold']);parts.append(body)
    # Blue inset on inner side, exact moon blue selected facets.
    P.paint(body,c['cream'],faces={i*10+j for i in range(n-1) for j in [2,3]})
    P.paint(body,c['moon'],faces={i*10+j for i in range(1,9) for j in [2,3]})
    parts.append(beam(P,'suspension',(0,0,3.53),(0,0,4),.012,c['gold'],4))
    for x,z,r,top in [(.37,1.52,.48,3.30),(.92,2.36,.34,3.45)]:
        parts.append(beam(P,'star thread',(x,-.01,z+r),(x,-.01,top),.009,c['gold'],4));parts.append(puffstar(P,'hanging gold star',r*.92,.14,(x,-.015,z),c['gold']))
        parts.append(P.ico('thread bead',.045,loc=(x,-.015,z+r+.055),color=c['gold']))
    finish(P,s,[],[('swing',(0,0,4),parts)])
