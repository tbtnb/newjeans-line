"""H11 Paper Clock Tower; spec size 3.5 x 3.4 x 9 m; budget 2500.
Pivots: root, hand0/1, ears0/1. SIMPLIFICATIONS: window glow is palette colour; no clock numerals."""
BUDGET=2500


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
    outline=[(-.30*w,0),(-.58*w,.48*h),(-.47*w,.92*h),(-.15*w,h),(.45*w,.72*h),(.50*w,.48*h),(.28*w,0)]
    def point(u,v,k=1):return (x+u+lean*v/h,y+.50*v/h-.18*w,z+v)
    outer=[point(u,v) for u,v in outline]
    inset=[(a+.0,b-.055*w,c) for a,b,c in [point(u*.62,.13*h+v*.72) for u,v in outline]]
    center=(x+lean*.49,y+.50*.49-.42*w,z+.49*h)
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
 c=spec['colors'];C,G,W,R,L=[c[k] for k in ('cream','gold','wardgray','coral','lamp')];a=[]
 for i,(w,d,h,z) in enumerate([(3.5,3.4,.35,0),(3.5,3.4,.11,.35),(2.95,2.9,.4,.46),(2.55,2.5,.14,.86)]):a.append(bevel(P,'base'+str(i),(w,d,h),(0,0,z),G if i%2 else C,.045))
 a.append(P.box('tower',(2.2,2.15,5.25),loc=(0,0,1),color=W))
 for x in (-1.03,1.03):
  for y in (-1,1):
   a.append(bevel(P,'corner column',(.28,.28,5.3),(x,y,1),C,.035))
   for z in (1,4.35,6.22):a.append(bevel(P,'column capital',(.4,.4,.25),(x,y,z),C,.045))
 for z in (1,4.35,6.27):
  a.append(bevel(P,'gold belt',(2.55,2.45,.1),(0,0,z),G,.035));a.append(P.box('cream cornice',(2.42,2.35,.12),loc=(0,0,z+.1),color=C))
 for x in (-1.2,1.2):
  for y in (-1.16,1.16):a.append(P.ico('roof corner gold button',.085,loc=(x,y,6.48),color=G,subdiv=1))
 for side in (False,True):
  rot=90 if side else 0;x,y=(1.12,0) if side else (0,-1.105)
  for off,w,h,col in [(0,.99,2.7,C),(.04,.85,2.55,G),(.07,.68,2.34,L)]:
   a.append(arch(P,'arched window',x+off if side else x,y if side else y-off,1.5,w,h,.06,col,rot))
  if side:
   a.append(P.box('window mullion',(.04,.055,2.05),loc=(1.21,0,1.55),color=G));a.append(P.box('window bar',(.04,.7,.055),loc=(1.21,0,2.48),color=G));a.append(P.box('upper window bar',(.04,.7,.055),loc=(1.21,0,3.37),color=G))
  else:
   a.append(P.box('window mullion',(.055,.04,2.05),loc=(0,-1.21,1.55),color=G));a.append(P.box('window bar',(.7,.04,.055),loc=(0,-1.21,2.48),color=G));a.append(P.box('upper window bar',(.7,.04,.055),loc=(0,-1.21,3.37),color=G))
 a.append(P.cyl('clock rim',.81,.09,32,loc=(0,-1.03,5.33),color=G,rot=(90,0,0)))
 a.append(P.cyl('clock face',.74,.03,32,loc=(0,-1.13,5.33),color=C,rot=(90,0,0)))
 for i in range(12):
  t=i*math.tau/12;a.append(P.ico('hour dot',.035,loc=(.64*math.sin(t),-1.18,5.33+.64*math.cos(t)),color=G,subdiv=1))
 for i,(dx,dz) in enumerate([(-.35,.26),(.44,.40)]):
  hand=rod(P,'clock hand',(0,-1.22,5.33),(dx,-1.22,5.33+dz),.032,G);a.append(P.pivot('hand'+str(i),(0,-1.22,5.33),[hand]))
 a.append(P.ico('clock spindle',.075,loc=(0,-1.23,5.33),color=G,subdiv=1))
 a.append(P.cyl('hip roof',1.7,.68,4,loc=(0,0,6.49),r2=0,color=W,rot=(0,0,45)))
 for x in (-1.2,1.2):
  for y in (-1.2,1.2):a.append(rod(P,'roof gold seam',(x,y,6.49),(0,0,7.17),.04,G))
 a.append(bevel(P,'roof cap',(.42,.42,.16),(0,0,7.1),G,.05))
 for i,s in enumerate((-1,1)):
  es=ear(P,'folded roof ear',s*.55,.05,6.98,.80,2.02,C,R,s*.62)
  if s>0:
   for ob in es:
    for v in ob.data.vertices:
     axis=s*.55+s*.62*(v.co.z-6.98)/2.02;v.co.x=2*axis-v.co.x
  a.append(P.pivot('ears'+str(i),(s*.55,.05,6.98),es))
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and not ob.name.startswith('base'):
   ob.location.x*=.94;ob.location.y*=.88
   for v in ob.data.vertices:v.co.x*=.94;v.co.y*=.88
 finish(P,spec,a)
