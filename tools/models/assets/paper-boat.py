"""H15 Bunny-Sail Paper Boat; size 3 x 1.1 x 3 m; budget 1500.
Pivots root, bob0. SIMPLIFICATIONS: lantern glow is lamp colour; hull paper is solid folded panels; reference side sail height differs from front/hero."""
BUDGET=1500

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
    outline=[(-.30*w,0),(-.58*w,.48*h),(-.48*w,.92*h),(-.12*w,h),(.46*w,.77*h),(.50*w,.48*h),(.28*w,0)]
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
 c=spec['colors'];W,L,M,G,A=[c[k] for k in ('pearl','lilac','moon','gold','lamp')];a=[]
 top=[(-1.5,0,.79),(-.83,-.33,.68),(0,-.55,.66),(.83,-.33,.68),(1.5,0,.79),(.83,.33,.68),(0,.55,.66),(-.83,.33,.68)]
 low=[(-.94,0,0),(-.79,-.20,.0),(0,-.27,0),(.79,-.20,0),(.94,0,0),(.79,.20,0),(0,.27,0),(-.79,.20,0)]
 low=[(x,y*.035,z) for x,y,z in low]
 # Creased outer shell, with distinct triangular paper facets.
 for i in range(8):
  j=(i+1)%8;v=[top[i],top[j],low[j],low[i]];center=tuple(sum(p[k] for p in v)/4 for k in range(3));v.append((center[0],center[1]*1.04,center[2]))
  ob=mesh(P,'folded hull facet',v,[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],W);P.paint(ob,L if i%2 else M,faces={1})
 # Interior is visible from above and contains an actual lower cockpit.
 inner=[(x*.93,y*.89,z-.045) for x,y,z in top];floor=[(x*.55,y*.30,.23) for x,y,z in top]
 for i in range(8):
  j=(i+1)%8;a.append(mesh(P,'lilac hull interior',[inner[i],inner[j],floor[j],floor[i]],[(0,1,2),(0,2,3)],L))
  a.append(rod(P,'gold folded rim',top[i],top[j],.016,G,12))
 a.append(mesh(P,'cockpit floor',floor,[tuple(range(8))],L))
 # Collect shell panels that were generated directly above.
 a=list(bpy.context.scene.objects)
 a.append(P.lathe('gold mast',[(.033,.25),(.033,2.76),(.045,2.77),(.045,2.81),(.03,2.81),(.03,2.9)],12,color=G))
 a.append(P.cyl('mast foot',.065,.055,12,loc=(0,0,.30),color=G))
 a.append(P.lathe('mast diamond',[(0,2.81),(.10,2.96),(0,3.11)],4,color=G))
 outline=[(-.70,1.45),(-.55,1.81),(-.18,2.00),(.28,1.96),(.59,1.70),(.71,1.44),(.57,1.13),(.19,.99),(-.28,1.01),(-.59,1.16)]
 vs=[(x,-.035,z) for x,z in outline]+[(-.12,-.24,1.48),(.12,-.16,1.82),(.46,-.14,1.42),(.10,-.12,1.12)]
 front=[(0,1,10),(1,2,11),(1,11,10),(2,3,11),(3,4,11),(4,12,11),(4,5,12),(5,6,12),(6,7,13),(6,13,12),(7,8,13),(8,9,10),(8,10,13),(9,0,10),(10,11,12),(10,12,13)]
 vs += [(x,.06,z) for x,z in outline]+[(0,.18,1.5)]
 fs=front+[(24,14+(i+1)%10,14+i) for i in range(10)]+[(i,14+i,14+(i+1)%10,(i+1)%10) for i in range(10)]
 head=mesh(P,'large irregular origami sail facets',vs,fs,W);P.paint(head,M,faces={0,6,10,13});P.paint(head,L,faces={1,8,17,22});a.append(head)

 for i,sgn in enumerate((-1,1)):
  es=ear(P,'bunny sail folded ear',sgn*.38,0,1.85,.49,1.12,W,L,sgn*.39)
  # Thin but genuinely folded fabric/paper sail, rather than a flat card.
  for ob in es:
   for v in ob.data.vertices:v.co.y=v.co.y*.40-.10
  a+=es
 # Bow lantern: gold frame, warm faceted core, pagoda cap and diamond finial.
 x=1.32;y=0
 for z,r,h,col,r2 in [(.73,.07,.06,G,.07),(.79,.045,.1,G,.045),(.89,.09,.035,G,.09),(.925,.09,.24,A,.13),(1.165,.16,.035,G,.16),(1.2,.16,.11,G,.025)]:
  a.append(P.cyl('bow lantern',r,h,8,loc=(x,y,z),color=col,r2=r2))
 for i in range(4):
  t=math.pi/4+i*math.pi/2;a.append(rod(P,'lantern frame',(x+.09*math.cos(t),.09*math.sin(t),.93),(x+.13*math.cos(t),.13*math.sin(t),1.17),.008,G,5))
 a.append(P.ico('lantern finial',.04,loc=(x,0,1.35),color=G,subdiv=1,scale=(1,1,1.4)))
 b=P.pivot('bob0',(0,0,.4),a);finish(P,spec,[b])
