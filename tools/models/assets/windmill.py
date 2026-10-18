"""H17 Bunny Village Windmill; size 5.3 x 2.8 x 9 m; budget 3000.
Pivots root, wheel0 (Y axle), ears0/1. SIMPLIFICATIONS: flower petals use cream/coral from the exact H17 palette; tiny foliage uses folded leaves; no glass emission."""
BUDGET=3000

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
    def point(u,v,k=1):return (x+u+lean*v/h,y+.90*v/h-.18*w,z+v)
    outer=[point(u,v) for u,v in outline]
    inset=[(a+.0,b-.055*w,c) for a,b,c in [point(u*.62,.13*h+v*.72) for u,v in outline]]
    center=(x+lean*.49,y+.72*.49-.42*w,z+.49*h)
    back=[(a,b+.35*w,c) for a,b,c in outer]
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
 c=spec['colors'];C,R,S,G,W=[c[k] for k in ('cream','coral','sun','green','wood')];a=[]
 a.append(P.cyl('octagonal tower',1.12,5.8,8,color=C,r2=.79,rot=(0,0,22.5)))
 for i in range(8):
  t=math.pi/8+i*math.tau/8;x=1.07*math.cos(t);y=1.07*math.sin(t)
  a.append(rod(P,'cream corner buttress',(x,y,.16),(x*.76,y*.76,5.75),.14,C,4))
  for z in (.0,2.05):
   a.append(P.cyl('buttress foot',.24,.32,4,loc=(x*(1-z*.025),y*(1-z*.025),z),color=C,rot=(0,0,45)))
 a.append(P.cyl('foundation collar',1.17,.12,8,color=S,rot=(0,0,22.5)))
 for z in (2.07,5.73):a.append(P.cyl('tower belt',1.08-z*.035,.1,8,loc=(0,0,z),color=S,rot=(0,0,22.5)))
 # Porch, arch door and folded miniature gable.
 a.append(bevel(P,'porch facade',(1.15,.38,1.75),(0,-1.02,.1),C,.045))
 a.append(arch(P,'door gold surround',0,-1.24,.14,.84,1.50,.06,S))
 a.append(arch(P,'wood arched door',0,-1.285,.14,.68,1.37,.04,S))
 for x in (-.21,-.07,.07,.21):a.append(P.box('door plank seam',(.018,.01,1.06),loc=(x,-1.315,.15),color=W))
 a.append(P.ico('diamond door handle',.045,loc=(.22,-1.34,.75),color=W,subdiv=1))
 for z,w,d in [(0,1.2,.46),(.11,1.02,.25)]:a.append(P.box('doorstep',(w,d,.12),loc=(0,-1.28-z,z),color=C))
 a.append(P.prism('porch gable',[(-.73,0),(0,.58),(.73,0),(.64,-.08),(0,.40),(-.64,-.08)],.6,loc=(0,-1.03,1.78),color=R))
 # Window boxes on front and right: little flowers and real leaves.
 for side in (False,True):
  for z in ([2.65] if not side else [1.0,2.9,4.47]):
   rad=1.08-z*.05;x,y=(rad,0) if side else (0,-rad);rot=90 if side else 0
   a.append(arch(P,'window frame',x,y,z,.53,.85,.06,C,rot))
   a.append(arch(P,'warm gold window',x+.05 if side else x,y if side else y-.05,z+.06,.34,.68,.04,S,rot))
   a.append(bevel(P,'flower window box',(.25,.72,.18) if side else (.72,.25,.18),(x+.13 if side else x,y if side else y-.13,z-.12),W,.03))
   for j in range(3):
    xx=x+.22 if side else (j-1)*.19;yy=(j-1)*.19 if side else y-.25
    a.append(P.ico('leaf cluster',.11,loc=(xx,yy,z+.02),color=G,subdiv=1,scale=(1,1,.6)))
    for k in range(5):
     t=math.tau*k/5;dx=0 if side else .055*math.cos(t);dy=.055*math.cos(t) if side else 0
     a.append(P.prism('five petal flower',P.ellipse(.043,.042,3),.018,loc=(xx+dx+( .04 if side else 0),yy+dy-(0 if side else .04),z+.08+.055*math.sin(t)),color=R if j%2 else C,rot=(0,0,90 if side else 0)))
    a.append(P.card('flower sun centre',P.ellipse(.028,.028,5),loc=(xx+.065 if side else xx,yy if side else yy-.065,z+.08),color=S,rot=(0,0,90 if side else 0)))
 a.append(P.lathe('creased red roof',[(1.25,0),(.97,.55),(.48,1.21),(0,1.65)],8,loc=(0,0,5.8),color=R,rot=(0,0,22.5)))
 a.append(P.cyl('roof gold edge',1.27,.13,8,loc=(0,0,5.73),color=S,rot=(0,0,22.5)))
 for i,sgn in enumerate((-1,1)):
  es=ear(P,'roof bunny ear',sgn*.45,-.05,6.93,1.05,2.07,C,R,sgn*1.12);a.append(P.pivot('ears'+str(i),(sgn*.45,-.05,6.93),es))
 # Four framed paper sails: exposed timber spar, cream folded cloth and sun edge pins.
 sail=[];hub=(0,-1.19,4.78)
 for i in range(4):
  t=math.radians([38,142,218,322][i]);v=Vector((math.cos(t),0,math.sin(t)));n=Vector((-math.sin(t),0,math.cos(t)))
  def at(r,w,y=-1.29):return tuple(Vector((0,y,4.78))+v*r+n*w)
  sail.append(rod(P,'timber spoke',at(.08,0,-1.2),at(3.30,0,-1.2),.065,W,6))
  vs=[at(1.00,-.43),at(3.31,-.43),at(3.31,.43),at(1.00,.43),at(1.96,0,-1.34)]
  sail.append(mesh(P,'creased cream sail',vs,[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],C))
  for r0,r1,w0,w1 in [(1.00,3.31,-.43,-.43),(1.00,3.31,.43,.43),(1.00,1.00,-.43,.43),(3.31,3.31,-.43,.43)]:
   sail.append(rod(P,'gold sail border',at(r0,w0),at(r1,w1),.040,W if w0==w1 else S,4))
  for j in range(1,3):sail.append(rod(P,'sail paper rib',at(1.00+j*.5775,-.42,-1.30),at(1.00+j*.5775,.42,-1.30),.009,W,4))
 for i in range(4):
  t=math.radians([38,142,218,322][i]);v=Vector((math.cos(t),0,math.sin(t)));n=Vector((-math.sin(t),0,math.cos(t)))
  for rr in (1.0,3.31):
   for ww in (-.43,.43):
    pt=Vector((0,-1.32,4.78))+v*rr+n*ww
    sail.append(P.cyl('gold sail corner pin',.055,.065,4,loc=pt,color=S,r2=0,rot=(90,0,0)))
 for r,h,y,col in [(.34,.15,-1.13,W),(.29,.20,-1.27,S),(.24,.09,-1.49,S)]:sail.append(P.cyl('faceted windmill hub',r,h,12,loc=(0,y,4.78),color=col,rot=(90,0,0)))
 sail.append(P.ico('creased golden hub jewel',1,loc=(0,-1.60,4.78),scale=(.25,.10,.25),subdiv=1,color=S))
 for sg in (-1,1):
  a.append(P.box('base flower planter',(.32,.4,.22),loc=(sg*1.04,0,.55),color=W))
  for j in range(2):
   a.append(P.ico('planter foliage',.11,loc=(sg*1.07,(j-1)*.12,.79),color=G,subdiv=1))
 a.append(P.prism('porch gold diamond',[(0,.13),(.1,0),(0,-.13),(-.1,0)],.04,loc=(0,-1.36,1.9),color=S))
 for sg in (-1,1):
  a.append(P.box('porch side upright',(.08,.12,.50),loc=(sg*.64,-1.22,1.20),color=W))
  a.append(P.prism('gable eave bracket',[(0,0),(.15,.20),(.15,0)],.10,loc=(sg*.47,-1.26,1.51),color=W))
 a.append(P.pivot('wheel0',hub,sail))
 bpy.context.view_layer.update()
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and ob.parent is None:
   mw=ob.matrix_world.copy();iv=mw.inverted()
   for v in ob.data.vertices:
    p=mw@v.co;factor=1.12 if p.z<5.9 else 1.0
    p.x*=factor*((1.12*(1+.10*max(0,1-p.z/5.75))) if p.z<5.75 else 1);p.y*=factor;v.co=iv@p
 finish(P,spec,a)
