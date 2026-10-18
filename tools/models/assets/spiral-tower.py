"""H14 Spiral Paper Tower; size 4.3 x 4.2 x 14 m; budget 3500.
Pivots root, tower0 at base side (fall), spin0 star. SIMPLIFICATIONS: stair handrail is a continuous folded paper parapet; window light uses gold."""
BUDGET=3500

import math
import bpy, bmesh
from mathutils import Vector, Matrix

def mesh(P,name,verts,faces,color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob); P.paint(ob,color); return ob

def bevel(P,name,size,loc,color,amount=.06):
    ob=P.box(name,size,loc=loc,color=color)
    m=ob.modifiers.new('paper chamfers','BEVEL');m.width=amount;m.segments=1
    bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.modifier_apply(modifier=m.name);P.paint(ob,color);ob.select_set(False);return ob

def rod(P,name,a,b,r,color,n=8):
    d=Vector(b)-Vector(a);o=P.cyl(name,r,d.length,n,loc=a,color=color);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return o

def ear(P,name,x,y,z,w,h,color,inner,lean=0):
    outline=[(-.30*w,0),(-.58*w,.48*h),(-.43*w,.88*h),(0,h),(.43*w,.82*h),(.50*w,.48*h),(.28*w,0)]
    def point(u,v,k=1):return (x+u+lean*v/h,y+.28*v/h-.18*w,z+v)
    outer=[point(u,v) for u,v in outline]
    inset=[(a+.0,b-.055*w,c) for a,b,c in [point(u*.62,.13*h+v*.72) for u,v in outline]]
    center=(x+lean*.49,y+.28*.49-.42*w,z+.49*h)
    back=[(a,b+.7*w,c) for a,b,c in outer]
    vs=outer+inset+[center]+back;fs=[]
    for i in range(7):fs.append((i,(i+1)%7,(i+1)%7+7,i+7))
    for i in range(7):fs.append((14,7+i,7+(i+1)%7))
    for i in range(7):fs.append((i,15+i,15+(i+1)%7,(i+1)%7))
    fs.append(tuple(range(15,22)))
    ob=mesh(P,name,vs,fs,color);P.paint(ob,inner,faces=set(range(7,14)));return [ob]

def arch(P,name,x,y,z,w,h,depth,color,rot=0):
    out=[(-w/2,0),(w/2,0),(w/2,h*.72),(w*.31,h*.88),(0,h),(-w*.31,h*.88),(-w/2,h*.72)]
    return P.prism(name,out,depth,loc=(x,y,z),color=color,rot=(0,0,rot))

def finish(P,spec,roots):
    bpy.context.view_layer.update(); obs=list(bpy.context.scene.objects); ms=[o for o in obs if o.type=='MESH']
    worlds={o:o.matrix_world.copy() for o in obs}; parents={o:o.parent for o in obs}
    pts=[worlds[o]@v.co for o in ms for v in o.data.vertices]
    lo=Vector(tuple(min(p[i] for p in pts) for i in range(3))); hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
    sz=spec['size_m'];sc=Vector((sz['w']/(hi.x-lo.x),sz['d']/(hi.y-lo.y),sz['h']/(hi.z-lo.z)))
    S=Matrix.Diagonal((sc.x,sc.y,sc.z,1));T=Matrix.Translation((-(hi.x+lo.x)/2,-(hi.y+lo.y)/2,-lo.z));M=S@T
    for o in obs:o.parent=None;o.matrix_world=Matrix.Identity(4)
    for o in obs:
        if o.type=='MESH':
            o.data.transform(M@worlds[o]);o.data.update()
            bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
            # Open paper surfaces need an explicit visible side; closed shells use outward normals.
            if bm.faces and not all(e.is_manifold for e in bm.edges):
                avg=sum((f.normal*f.calc_area() for f in bm.faces),Vector((0,0,0)))
                cen=sum((v.co for v in bm.verts),Vector((0,0,0)))/len(bm.verts)
                name=o.name.lower();flip=False
                if any(k in name for k in ('canopy folded','floor paper')):flip=avg.z<0
                elif any(k in name for k in ('faceted heart','creased cream sail','folded peach flower')):flip=avg.y>0
                elif any(k in name for k in ('folded hull facet','scalloped gold trim','scalloped lilac valance')):flip=avg.x*cen.x+avg.y*cen.y<0
                elif 'hull interior' in name:flip=avg.z<0
                if flip:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
            bm.to_mesh(o.data);bm.free();o.data.update()
        else:o.location=M@worlds[o].translation
    bpy.context.view_layer.update()
    for o in obs:
        if parents[o]:
            mw=o.matrix_world.copy();o.parent=parents[o];o.matrix_parent_inverse=parents[o].matrix_world.inverted();o.matrix_world=mw
    P.pivot('root',(0,0,0),roots)

def build(P,spec):
 c=spec['colors'];L,W,V,G,I=[c[k] for k in ('lilac','white','lavender','gold','indigo')];a=[]
 for j,(r,h,z,col) in enumerate([(1.8,.25,0,V),(1.8,.08,.25,G),(1.7,.35,.33,L),(1.57,.08,.68,G),(1.52,.25,.76,W)]):
  a.append(P.cyl('octagonal foundation',r,h,8,loc=(0,0,z),color=col,rot=(0,0,22.5)))
 a.append(P.cyl('slender tower core',.96,10.95,8,loc=(0,0,1.0),color=lambda c,n: L if n.x<.3 else W,rot=(0,0,22.5)))
 for i in range(8):
  t=math.tau*i/8+math.pi/8;x=.97*math.cos(t);y=.97*math.sin(t)
  a.append(P.cyl('folded corner pilaster',.095,10.9,4,loc=(x,y,.82),color=W,rot=(0,0,45)))
 for z in (.9,3.2,5.8,8.35,10.95):a.append(P.cyl('tower stone belt',1.035,.16,8,loc=(0,0,z),color=V,rot=(0,0,22.5)))
 for side in (False,True):
  for z in (1.18,3.8,6.45,9.1):
   x,y=(.96,0) if side else (0,-.96);rot=90 if side else 0
   for off,w,h,col in [(0,.52,1.14,V),(.025,.40,1.02,I),(.05,.28,.86,G)]:a.append(arch(P,'pointed tower window',x+off if side else x,y if side else y-off,z,w,h,.025,col,rot))
 # Each step is a real closed wedge, not a painted helix.
 N=64;turns=1.6;t0=-math.pi*.60
 for i in range(N):
  t=t0+turns*math.tau*i/N;u=t0+turns*math.tau*(i+1)/N;z=1.5+9*i/N
  vs=[]
  for zz in (z-.12,z):
   for r,ang in [(.98,t),(1.69,t),(1.69,u),(.98,u)]:vs.append((r*math.cos(ang),r*math.sin(ang),zz))
  a.append(mesh(P,'spiral stair tread',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],V if i%2 else L))
 # Helical cream parapet and fine gold coping, sampled in shared rectangular panels.
 for i in range(48):
  t=t0+turns*math.tau*i/48;u=t0+turns*math.tau*(i+1)/48;z=1.5+9*i/48;zu=1.5+9*(i+1)/48
  for bottom,top,col in [(0,.68,W),(.68,.74,G)]:
   vs=[(r*math.cos(ang),r*math.sin(ang),zz+dz) for r in (1.64,1.73) for ang,zz in ((t,z),(u,zu)) for dz in (bottom,top)]
   a.append(mesh(P,'spiral paper railing',vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3)],col))
 for i in range(5):
  t=t0+turns*math.tau*i/4;z=1.5+9*i/4;x=1.69*math.cos(t);y=1.69*math.sin(t)
  a.append(bevel(P,'stair landing post',(.17,.17,.83),(x,y,z),W,.02));a.append(bevel(P,'post gold cap',(.26,.26,.08),(x,y,z+.83),G,.02))
 a.append(P.cyl('roof underside',1.3,.18,8,loc=(0,0,11.55),color=W,rot=(0,0,22.5)))
 a.append(P.cyl('roof gold eave',1.33,.08,8,loc=(0,0,11.73),color=G,rot=(0,0,22.5)))
 a.append(P.cyl('lavender folded spire',1.31,1.95,8,loc=(0,0,11.81),r2=.06,color=lambda c,n: V if n.x>-.1 else L,rot=(0,0,22.5)))
 a.append(P.cyl('gold roof finial',.13,.38,8,loc=(0,0,13.67),r2=.045,color=G))
 star=P.prism('five point star',P.star(.39,.17),.13,loc=(0,0,14.32),color=G)
 a.append(P.pivot('spin0',(0,0,14.32),[star]));tower=P.pivot('tower0',(-1.6,0,0),a)
 finish(P,spec,[tower])
