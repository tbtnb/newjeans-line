"""H12 flip-phone; size 2.7 x 2.2 x 5 m; budget 2000. Pivots root, lid0, tower0.
SIMPLIFICATIONS: no key glyphs; screen glow uses flat palette; tiny flower stamens omitted; cream substitutes for sheet gold hardware and peach for pale screen pink to preserve the specified palette. H12 top view angled: front/side govern."""
BUDGET=2000
LARGE=False

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

def phone_panel(P,name,w,d,h,loc,col,cut):
    k=min(cut,w*.23,h*.23)
    out=[(-w/2+k,0),(w/2-k,0),(w/2,k),(w/2,h-k),(w/2-k,h),(-w/2+k,h),(-w/2,h-k),(-w/2,k)]
    if 'coral shell' not in name:return P.prism(name,out,d,loc=loc,color=col)
    # Broad bevels catch the light as sharp folded-paper edge planes.
    b=.075;inner=[(x*(w-2*b)/w,b+z*(h-2*b)/h) for x,z in out]
    vs=[(x,-d/2,z) for x,z in inner]+[(x,-d/2+b,z) for x,z in out]+[(x,d/2-b,z) for x,z in out]+[(x,d/2,z) for x,z in inner]
    fs=[tuple(range(7,-1,-1)),tuple(range(24,32))]
    for r in range(3):
     for i in range(8):fs.append((r*8+i,r*8+(i+1)%8,(r+1)*8+(i+1)%8,(r+1)*8+i))
    ob=mesh(P,name,vs,fs,col);ob.location=loc;return ob

def build(P,spec):
 c=spec['colors'];C,R,K=[c[k] for k in ('cream','coral','pink')];large=LARGE
 L=c.get('lavender',c.get('peach'));G=c.get('gold',C);a=[]
 # A unified sculpted clamshell, with separate hinge and extendable antenna.
 def panel(name,w,h,z,y,angle,upper=False):
  before=set(bpy.context.scene.objects)
  phone_panel(P,name+' coral shell',w,.38,h,(0,0,0),R,.19)
  phone_panel(P,name+' cream bezel',w-.23,.055,h-.25,(0,-.19,.125),C,.17)
  if upper:
   phone_panel(P,name+' inset screen',w-.48,.035,h-.72,(0,-.23,.29),G if large else C,.09)
   phone_panel(P,name+' screen inner',w-.56,.025,h-.8,(0,-.255,.33),L if large else c['peach'],.075)
   if not large:P.paint(bpy.context.scene.objects[name+' screen inner'],c['peach'])
   hw=(w-.64)*.42
   # Ten-cut gemstone outline and four distinct, planar creases.
   outline=[(-1,.32),(-1,.69),(-.66,.91),(-.30,.91),(0,.64),(.30,.91),(.66,.91),(1,.69),(1,.32),(0,-.55)]
   outline=[(x*hw,z*hw+h*.42) for x,z in outline]
   verts=[(x,-.28,z) for x,z in outline]+[(-hw*.42,-.33,h*.53),(hw*.42,-.33,h*.53),(0,-.36,h*.39)]
   fs=[(0,1,10),(1,2,10),(2,3,10),(3,4,10),(4,11,10),(4,5,11),(5,6,11),(6,7,11),(7,8,11),(8,9,12),(8,12,11),(9,0,12),(0,10,12),(10,11,12)]
   heart=mesh(P,name+' faceted heart',verts,fs,K)
   if large:
    rim=P.prism(name+' heart gold rim',[(x*1.055,(z-h*.42)*1.055+h*.42) for x,z in outline],.025,loc=(0,-.27,0),color=G)
   bevel(P,name+' speaker',(.4,.04,.055),(0,-.25,h-.32),G,.018)
   bevel(P,name+' side button',(.055,.13,.39),(w/2+.015,0,.65),G,.025)
  else:
   for row in range(4):
    for col in range(3):
     xx=(col-1)*(w-.45)/3;zz=.28+row*(h-.48)/4
     key=bevel(P,'key '+str(row)+str(col),((w-.56)/3,.085,(h-.76)/4),(xx,-.255,zz),K if large else C,.045)
     if not large:P.paint(key,lambda q,n:C if n.y<-.9 else c['peach'])
  bpy.context.view_layer.update();obs=list(set(bpy.context.scene.objects)-before)
  for ob in obs:
   if 'coral shell' not in ob.name and 'side button' not in ob.name:
    ob.location.y+=0
  bpy.context.view_layer.update();T=Matrix.Translation((0,y,z))@Matrix.Rotation(math.radians(angle),4,'X')
  for ob in obs:ob.data.transform(T@ob.matrix_world);ob.matrix_world=Matrix.Identity(4)
  return obs
 # coordinates use compact phone units, final spec scaling preserves the architecture.
 if large:
  # chunky wound telephone cord, a clear open oval in plan.
  cord=[];n=26
  for i in range(n):
   t=math.tau*i/n;x=1.19*math.cos(t);y=.79*math.sin(t);z=.19+.20*(math.sin(t)+1)
   ob=P.lathe('coiled cord segment',[(.11,0),(.18,.04),(.18,.24),(.11,.28)],8,color=L)
   tangent=Vector((-1.19*math.sin(t),.79*math.cos(t),.04));ob.rotation_euler=tangent.to_track_quat('Z','Y').to_euler();ob.location=(x,y,z)
   cord.append(ob)
  a.append(P.pivot('swing0',(1.02,.33,.7),cord))
  lower=panel('keypad',1.55,2.05,.42,-.28,-18);a+=lower
  hinge_z=2.4;hy=.31
  upper=panel('lid',1.6,1.95,hinge_z,hy,10,True)
 else:
  # Eight lobes, layered coral / cream / peach flower pedestal.
  outline=[]
  for i in range(40):
   t=math.tau*i/40;r=1.27*(1+.055*math.cos(8*t+math.pi));outline.append((r*math.cos(t),r*.70*math.sin(t)))
  for j,(z,th,col,k) in enumerate([(0,.16,R,1),(.16,.13,C,.99),(.29,.1,c['peach'],.98)]):
   vs=[(x*k,y*k,z) for x,y in outline]+[(x*k,y*k,z+th) for x,y in outline]
   fs=[tuple(range(39,-1,-1)),tuple(range(40,80))]+[(i,(i+1)%40,(i+1)%40+40,i+40) for i in range(40)]
   a.append(mesh(P,'scalloped flower plinth',vs,fs,col))
  a.append(P.cyl('cream phone pedestal',.60,.22,16,loc=(0,-.34,.38),color=C))
  lower=panel('keypad',1.55,2.06,.65,-.43,-22);a+=lower
  hinge_z=2.67;hy=.27
  upper=panel('lid',1.45,1.93,hinge_z,hy,0,True)
  # Genuine faceted flower blossoms and folded mint leaves.
  for f,(x,y,r) in enumerate([(-.91,-.37,.27),(.86,-.46,.29),(.94,.27,.24)]):
   for i in range(5):
    t=math.tau*i/5;a.append(mesh(P,'folded peach flower petal',[(x,y,.95),(x+r*math.cos(t-.45),y-.04,.95+r*math.sin(t-.45)),(x+r*1.12*math.cos(t),y-.13,.95+r*1.12*math.sin(t)),(x+r*math.cos(t+.45),y-.04,.95+r*math.sin(t+.45))],[(0,1,2),(0,2,3)],c['peach']))
   a.append(P.ico('flower centre',r*.32,loc=(x,y-.15,.95),color=C,subdiv=1))
  for i,(x,y,rx,rz) in enumerate([(-1,-.1,-35,-30),(-.8,.32,25,-35),(1,.0,35,35),(.8,.39,-20,40)]):
   a.append(P.blade('mint folded leaf',.48,.91,loc=(x,y,.40),color=c['mint'],rot=(rx,rz,0),bend=.26))
 # horizontal X-axis barrel hinge and its gold/cream end collars.
 for x,width,col in [(-(.87 if large else .76),.16,G),(-.60,.20,R if not large else L),(0,1.0,C if not large else L),(.60,.20,R if not large else L),((.87 if large else .76),.16,G)]:
  a.append(P.cyl('hinge barrel',.155,width,12,loc=(x-width/2,hy-.15,hinge_z),color=col,rot=(0,90,0)))
 # Antenna rides with the lid: extension is an engine scale-Z tower group.
 ant=[];x=-.62 if large else .61;top=4.28 if large else 4.60
 ant_y=hy+(-.34 if large else .03)
 ant.append(P.cyl('antenna socket',.11,.17,8,loc=(x,ant_y,top-.03),color=G))
 for i in range(3 if large else 1):
  ant.append(P.cyl('telescoping antenna',.065-i*.013,.31 if large else .24,8,loc=(x,ant_y,top+.12+i*.27),color=L if large and i<2 else C))
 if large:
  star=P.prism('antenna five-point star',P.star(.235,.105),.085,loc=(x,ant_y,5.33),color=G)
  ant.append(P.pivot('spin0',(x,ant_y,5.33),[star]))
 else:ant.append(P.ico('coral antenna tip',.115,loc=(x,ant_y,4.96),color=R,subdiv=1,scale=(1,1,1.3)))
 upper.append(P.pivot('tower0',(x,ant_y,top),ant))
 a.append(P.pivot('lid0',(0,hy-.15,hinge_z),upper))
 finish(P,spec,a)
