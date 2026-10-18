"""H16 Lake Paper Pavilion; size 4.8 x 5.1 x 6 m; budget 3000.
Pivots root, swing0..7 lanterns at eaves. SIMPLIFICATIONS: side sheet reverses the stairs relative to front/top; front/hero govern. Open column gaps remain open (design-mask extraction fills them). Warm light is flat palette; tiny lamp chains are slim rods; dome is faceted paper."""
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
 c=spec['colors'];W,M,L,G,A=[c[k] for k in ('pearl','moon','lilac','gold','lamp')];a=[]
 def island(name,r,r2,z,h,col,fold=False):
  def ring(rr,zz):
   pts=[]
   for i in range(8):
    t=math.tau*i/8
    if i==6:
     yy=-math.sqrt(rr*rr-.77*.77)
     pts += [(-.77,yy,zz),(-.77,-1.4,zz),(.77,-1.4,zz),(.77,yy,zz)]
    else:
     radius=rr
     pts.append((radius*math.cos(t),radius*math.sin(t),zz))
   return pts
  lo=ring(r,z);hi=ring(r2,z+h);n=len(lo);vv=lo+hi;ff=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
  for i in range(n):
   j=(i+1)%n
   if fold:
    q=[lo[i],lo[j],hi[j],hi[i]];cen=tuple(sum(x[k] for x in q)/4 for k in range(3));idx=len(vv);vv.append((cen[0]*1.02,cen[1]*1.02,cen[2]));ff += [(i,j,idx),(j,n+j,idx),(n+j,n+i,idx),(n+i,i,idx)]
   else:ff.append((i,j,n+j,n+i))
  ob=mesh(P,name,vv,ff,col)
  if fold:P.paint(ob,M,faces={i for i in range(2,len(ff)) if i%4 in (0,1)})
  return ob
 for r,h,z,col,r2 in [(2.40,.09,0,L,2.40),(2.40,.50,.09,L,2.38),(2.38,.055,.59,G,2.38),(2.38,.15,.645,L,2.25),(2.25,.055,.795,G,2.25),(2.25,.10,.85,W,2.19)]:
  a.append(island('notched island foundation',r,r2,z,h,col,col==L and h>.3))
 a.append(island('notched pearl floor',2.10,2.10,.95,.055,W))
 # Starburst floor inlays remain visible in the open pavilion.
 for i in range(8):
  t=math.tau*i/8;u=t+math.pi/8;v=t+math.pi/4
  a.append(mesh(P,'floor paper star',[(0,0,1.012),(.96*math.cos(t),.96*math.sin(t),1.012),(.45*math.cos(u),.45*math.sin(u),1.012),(.96*math.cos(v),.96*math.sin(v),1.012)],[(0,1,2),(0,2,3)],L))
 for i in range(5):
  z=i*.175;y=-2.68+i*.23
  a.append(P.box('pearl stair',(1.35,.55,z+.18),loc=(0,y,0),color=W));a.append(P.box('stair paper fold line',(1.32,.022,.012),loc=(0,y-.273,z+.165),color=L))
 for sgn in (-1,1):
  for i in range(5):
   a.append(P.box('gold stair cheek',(.15,.3,.19+i*.17),loc=(sgn*.76,-2.7+i*.24,0),color=G))
 # Eight columns and independent hanging lantern groups.
 lamps=[]
 for i in range(8):
  t=math.tau*i/8+math.pi/8;x=1.80*math.cos(t);y=1.80*math.sin(t)
  a.append(P.lathe('fluted pearl column',[(.25,.92),(.25,1.10),(.18,1.18),(.17,3.56),(.23,3.65),(.23,3.80)],6,loc=(x,y,0),color=W))
  for z in (1.17,3.59):a.append(P.cyl('column gilded collar',.185,.055,6,loc=(x,y,z),color=G))
  t+=math.pi/8;x=1.98*math.cos(t);y=1.98*math.sin(t);hang=3.74
  lamp=[rod(P,'lantern short chain',(x,y,hang),(x,y,3.43),.018,G,6)]
  lamp.append(P.lathe('warm faceted eave lantern',[(0,2.60),(.065,2.70),(.24,2.91),(.21,3.12),(.065,3.30),(0,3.43)],6,loc=(x,y,0),color=A))
  lamp.append(P.ico('gold lamp tassel',.032,loc=(x,y,2.61),color=G,subdiv=1,scale=(1,1,1.6)))
  lamps.append(P.pivot('swing'+str(i),(x,y,hang),lamp))
 # Scalloped canopy: eight lobes, two facets across each lobe, three radial bands.
 N=32;rings=[]
 for r,z in [(.10,5.12),(.78,4.99),(1.45,4.68),(1.95,4.12),(2.28,3.72)]:
  ring=[]
  for i in range(N):
   t=math.tau*i/N+(.032 if r==.78 else (-.028 if r==1.45 else (.026 if r==1.95 else 0)));wave=.44*(.5+.5*math.cos(8*t))*(r/2.28)**3
   ring.append((r*math.cos(t),r*math.sin(t),z+wave+(.085*(i%2) if r==1.45 else (-.035*(i%2) if r==1.95 else 0))))
  rings.append(ring)
 for k in range(4):
  for i in range(N):
   j=(i+1)%N;v=[rings[k][i],rings[k][j],rings[k+1][j],rings[k+1][i]]
   col=M if i%4<2 else L
   ob=mesh(P,'canopy folded facet',v,[(0,1,2),(0,2,3)],col)
   if i%4 in (1,3) and k==2:P.paint(ob,L if col==M else M,faces={1})
   a.append(ob)
 for i in range(N):
  j=(i+1)%N;p=rings[-1][i];q=rings[-1][j]
  a.append(mesh(P,'scalloped gold trim',[p,q,(q[0],q[1],q[2]-.085),(p[0],p[1],p[2]-.085)],[(0,1,2,3)],G))
  a.append(mesh(P,'scalloped lilac valance',[(p[0],p[1],p[2]-.085),(q[0],q[1],q[2]-.085),(q[0]*.98,q[1]*.98,q[2]-.23),(p[0]*.98,p[1]*.98,p[2]-.23)],[(0,1,2,3)],L))
 a.append(P.cyl('crescent gold pedestal',.28,.14,8,loc=(0,0,5.1),color=G,r2=.13))
 # Crescent silhouette is a real concave extruded mesh.
 out=[]
 for i in range(15):
  t=math.radians(65)+(math.radians(300)-math.radians(65))*i/14;out.append((.43*math.cos(t),.43*math.sin(t)))
 for i in range(11):
  t=math.radians(290)-(math.radians(290)-math.radians(78))*i/10;out.append((.13+.28*math.cos(t),.06+.31*math.sin(t)))
 n=len(out);vs=[(x+.16,-.09,z+5.67) for x,z in out]+[(x*.88+.16,-.14,z*.88+5.67) for x,z in out]+[(x+.16,.09,z+5.67) for x,z in out]
 fs=[tuple(range(n,2*n)),tuple(range(3*n-1,2*n-1,-1))]
 for i in range(n):
  j=(i+1)%n;fs += [(i,j,n+j,n+i),(i,2*n+i,2*n+j,j)]
 a.append(mesh(P,'creased crescent moon',vs,fs,G))
 bpy.context.view_layer.update()
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':
   mw=ob.matrix_world.copy();iv=mw.inverted()
   for v in ob.data.vertices:
    p=mw@v.co;z=p.z
    p.z=z*1.16 if z<=1.01 else (1.1716+(z-1.01)*.78 if z<3.8 else 3.3478+(z-3.8)*1.06)
    v.co=iv@p
 # Move each swing origin onto the warped hook without moving its children.
 for empty in lamps:
  worlds={child:child.matrix_world.copy() for child in empty.children}
  z=empty.location.z
  empty.location.z=z*1.16 if z<=1.01 else (1.1716+(z-1.01)*.78 if z<3.8 else 3.3478+(z-3.8)*1.06)
  bpy.context.view_layer.update()
  for child,mw in worlds.items():child.matrix_world=mw
 finish(P,spec,a+lamps)
