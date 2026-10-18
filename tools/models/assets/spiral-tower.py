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
 for j,(r,h,z,col) in enumerate([(1.95,.28,0,V),(1.95,.075,.28,G),(1.84,.43,.355,V),(1.69,.075,.785,G),(1.64,.28,.86,L),(1.54,.075,1.14,G),(1.50,.12,1.215,W)]):
  a.append(P.cyl('octagonal foundation',r,h,8,loc=(0,0,z),color=col,rot=(0,0,22.5)))
 a.append(P.cyl('slender tower core',.96,10.22,8,loc=(0,0,1.33),color=lambda c,n: L if n.x<.3 else W,rot=(0,0,22.5)))
 for i in range(8):
  t=math.tau*i/8+math.pi/8;x=.97*math.cos(t);y=.97*math.sin(t)
  a.append(P.cyl('folded corner pilaster',.105,10.18,4,loc=(x,y,1.31),color=V,rot=(0,0,45)))
 for z in (1.35,4.10,7.10,9.98,11.39):a.append(P.cyl('tower stone belt',1.035,.16,8,loc=(0,0,z),color=V,rot=(0,0,22.5)))
 for side in (False,True):
  for z in (1.45,3.55,6.95,9.64):
   x,y=(.96,0) if side else (0,-.96);rot=90 if side else 0
   for off,w,h,col in [(0,.54,1.13,V),(.025,.41,1.00,I),(.05,.29,.85,G)]:a.append(arch(P,'pointed tower window',x+off if side else x,y if side else y-off,z,w,h,.025,col,rot))
 # The middle window sits on the oblique front-right face in the design.
 for off,w,h,col in [(0,.51,1.10,V),(.025,.40,.99,I),(.05,.28,.85,G)]:
  a.append(arch(P,'oblique glowing window',.70+off*.707,-.70-off*.707,5.25,w,h,.025,col,45))
 for i in range(4):
  t=math.tau*i/4+math.pi/4
  a.append(P.box('paper pilaster foot',(.20,.20,.37),loc=(.94*math.cos(t),.94*math.sin(t),1.32),color=V))
 # Each step is a real closed wedge, not a painted helix.
 N=56;turns=-1.28;t0=math.pi*.60
 for i in range(N):
  t=t0+turns*math.tau*i/N;u=t0+turns*math.tau*(i+1)/N;z=2.4+6.9*i/N
  vs=[]
  for zz in (z-.12,z):
   for r,ang in [(.98,t),(1.64,t),(1.64,u),(.98,u)]:vs.append((r*math.cos(ang),r*math.sin(ang),zz))
  a.append(mesh(P,'spiral stair tread',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],V if i%2 else L))
 # Helical cream parapet and fine gold coping, sampled in shared rectangular panels.
 for i in range(40):
  t=t0+turns*math.tau*i/40;u=t0+turns*math.tau*(i+1)/40;z=2.4+6.9*i/40;zu=2.4+6.9*(i+1)/40
  for bottom,top,col in [(0,.68,W),(.68,.74,G)]:
   vs=[(r*math.cos(ang),r*math.sin(ang),zz+dz) for r in (1.59,1.68) for ang,zz in ((t,z),(u,zu)) for dz in (bottom,top)]
   a.append(mesh(P,'spiral paper railing',vs,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3)],col))
 for i in range(5):
  t=t0+turns*math.tau*i/4;z=2.4+6.9*i/4;x=1.64*math.cos(t);y=1.64*math.sin(t)
  a.append(bevel(P,'stair landing post',(.17,.17,.83),(x,y,z),W,.02));a.append(bevel(P,'post gold cap',(.26,.26,.08),(x,y,z+.83),G,.02))
 for i in range(8):
  t=math.tau*i/8+math.pi/8;co=math.cos(t);si=math.sin(t)
  out=[(.94*co,.94*si,10.95),(1.24*co,1.24*si,11.55),(.94*co,.94*si,11.55)]
  tangent=Vector((-si,co,0))*.055;vs=[tuple(Vector(v)+tangent) for v in out]+[tuple(Vector(v)-tangent) for v in out]
  a.append(mesh(P,'creased eave bracket',vs,[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],V))
 a.append(P.cyl('roof underside',1.3,.18,8,loc=(0,0,11.55),color=W,rot=(0,0,22.5)))
 a.append(P.cyl('roof gold eave',1.33,.08,8,loc=(0,0,11.73),color=G,rot=(0,0,22.5)))
 a.append(P.cyl('lavender folded spire',1.31,1.65,8,loc=(0,0,11.81),r2=.025,color=lambda c,n: V if n.x>-.1 else L,rot=(0,0,22.5)))
 a.append(P.cyl('gold roof finial',.13,.70,8,loc=(0,0,13.40),r2=.045,color=G))
 outline=P.star(.39,.17);vs=[(x,0,14.32+z) for x,z in outline]+[(0,-.16,14.32),(0,.16,14.32)];star=mesh(P,'five point folded star',vs,[(10,i,(i+1)%10) for i in range(10)]+[(11,(i+1)%10,i) for i in range(10)],G)
 cross=[];center=Vector((0,0,14.32))
 for plane in ('side','top'):
  out=P.star(0.39,0.17);vs=[]
  for u,v in out:vs.append(tuple(center+Vector((0,u,v) if plane=='side' else (u,v,0))))
  axis=Vector((.075,0,0) if plane=='side' else (0,0,.075));vs += [tuple(center+axis),tuple(center-axis)]
  cross.append(mesh(P,'creased star '+plane,vs,[(10,i,(i+1)%10) for i in range(10)]+[(11,(i+1)%10,i) for i in range(10)],G))
 a.append(P.pivot('spin0',(0,0,14.32),[star]+cross));tower=P.pivot('tower0',(-1.6,0,0),a)
 bpy.context.view_layer.update()
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':
   mw=ob.matrix_world.copy();iv=mw.inverted()
   for v in ob.data.vertices:
    q=mw@v.co;z=q.z
    if z<11.55:q.z=z*1.35 if z<=1.335 else 1.80225+(z-1.335)*(11.55-1.80225)/(11.55-1.335)
    v.co=iv@q
 finish(P,spec,[tower])
