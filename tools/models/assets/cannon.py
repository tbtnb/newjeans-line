"""H08 Confetti Cannon; spec 2×2.6×2.5 m; 1800 tris.
Pivots: root, gate (barrel trunnion), pulse (mouth/confetti emitter).
SIMPLIFICATIONS: a compact heart/star burst sits within the muzzle silhouette; runtime may instance additional airborne confetti.
"""
import math
BUDGET=1800

def build(P,spec):
 import bpy
 from mathutils import Vector
 C=spec['colors'];static=[];barrel=[]
 import bmesh
 def box(n,s,l,c,rot=(0,0,0)):
  o=P.box(n,s,l,C[c],rot=rot);static.append(o);return o
 box('carriage',(1.72,1.65,.65),(0,-.18,.26),'lavender');box('lower_gold_rail',(1.77,1.70,.06),(0,-.18,.26),'gold');box('upper_gold_rail',(1.77,1.70,.055),(0,-.18,.90),'gold')
 for y in [-.95,.47]:
  for x in [-.88,.88]:
   sign=1 if x>0 else -1
   for r,h,offset,col in [(.30,.20,-.10,'lavender'),(.246,.025,.105,'gold'),(.205,.03,.132,'cream'),(.10,.045,.164,'gold')]:
    static.append(P.cyl('faceted_wheel',r,h,(6 if r<.15 else 10),loc=(x+sign*offset,y,.30),rot=(0,sign*90,0),color=C[col]))
 for x in [-.60,.60]:static.append(P.prism('trunnion_cheek',[(-.43,0),(.44,0),(.22,.63),(-.05,.72)],.14,loc=(x,.16,.90),rot=(0,0,90),color=C['lavender']))
 # Hollow tapered barrel, local z axis transformed into upward/front pointing barrel.
 origin=Vector((0,.50,1.40));axis=Vector((0,-.86,.51));q=Vector((0,0,1)).rotation_difference(axis);length=1.72
 def tube(n,profile,color):
  if profile[0][0]>0 and profile[-1][0]>0:
   # A real annular band: never use a lathe end cap across the bore.
   vs=[(r*math.cos(j*math.tau/12),r*math.sin(j*math.tau/12),z) for r,z in profile for j in range(12)]
   fs=[]
   for k in range(len(profile)):
    for j in range(12):fs.append((k*12+j,k*12+(j+1)%12,((k+1)%len(profile))*12+(j+1)%12,((k+1)%len(profile))*12+j))
   me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);P.paint(o,C[color])
  else:o=P.lathe(n,profile,12,color=C[color])
  o.location=origin;o.rotation_euler=q.to_euler();barrel.append(o);return o
 tube('rolled_paper_hollow_barrel',[(0,-.30),(.34,-.28),(.44,-.13),(.47,0),(.51,.40),(.55,.85),(.59,1.20),(.61,length),(.54,length),(.52,1.30),(.47,.80),(.40,.28),(.32,.05),(0,.05)],'cream')
 # The deep inner paper folds use the prescribed gold tone, making the open bore legible.
 barrel[-1].data.update()
 P.paint(barrel[-1],C['gold'],faces=set(range(96,156)))
 P.paint(barrel[-1],C['lavender'],faces=set(range(144,156)))
 tube('lavender_breech',[(0,-.32),(.34,-.31),(.45,-.16),(.47,.02),(.42,.04),(0,.04)],'lavender')
 for z,r in [(.12,.485),(1.54,.615)]:tube('gold_barrel_band',[(r+.018,z),(r+.018,z+.19),(r-.015,z+.19),(r-.015,z)],'gold')
 # Curl lips, modeled as closed hollow loops on either side of the rolled sheet seam.
 for side in [-1,1]:
  vs=[];fs=[];N=8;M=3;center=origin+axis*.88+Vector((side*.54,0,0))
  for i in range(N):
   a=i*2*math.pi/N
   for j in range(M):
    b=j*2*math.pi/M;r=.13+.025*math.cos(b);v=Vector((side*.025*math.sin(b),r*math.cos(a),r*math.sin(a)));vs.append(tuple(center+v))
  for i in range(N):
   for j in range(M):fs.append((i*M+j,i*M+(j+1)%M,((i+1)%N)*M+(j+1)%M,((i+1)%N)*M+j))
  me=bpy.data.meshes.new('scroll');me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new('paper_scroll',me);bpy.context.collection.objects.link(ob);P.paint(ob,C['cream']);barrel.append(ob)
 # Front bow: real folded wings, knot, and swallow tails.
 for side in [-1,1]:
  outline=[(side*.03,.72),(side*.52,1.15),(side*.65,.96),(side*.60,.56),(side*.14,.58)]
  static.append(P.prism('bow_gold',outline,.13,loc=(0,-1.02,0),color=C['gold']))
  static.append(P.prism('bow_pink',[(x*.90,z*.96+.025) for x,z in outline],.15,loc=(0,-1.04,0),color=C['pink']))
  tail=[(side*.07,.66),(side*.32,.67),(side*.52,.13),(side*.35,.20),(side*.23,.10)]
  static.append(P.prism('gold_tail_border',tail,.07,loc=(0,-1.09,0),color=C['gold']))
  static.append(P.prism('ribbon_tail',[(x*.87,.37+(z-.37)*.87) for x,z in tail],.025,loc=(0,-1.14,0),color=C['magenta']))
 static.append(P.ico('bow_knot',.15,loc=(0,-1.16,.66),scale=(.8,.6,1),subdiv=1,color=C['gold']))
 for side in [-1,1]:static.append(P.ico('trunnion_pin',.135,loc=(side*.71,.30,1.43),scale=(.5,1,1),subdiv=1,color=C['gold']))
 # Raised folds in the pink bow wings (four visible extra triangles).
 import bmesh
 for ob in static:
  if ob.type=='MESH' and ob.name.startswith('bow_pink'):
   bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update();bmesh.ops.poke(bm,faces=[f for f in bm.faces if f.normal.y<-.7],offset=.07);bm.to_mesh(ob.data);bm.free();ob.data.update();P.paint(ob,lambda center,normal:C['magenta'] if normal.z<-.35 else C['pink'])
 # Faceted heart/star confetti remains inside the rim's outer silhouette in the rest pose.
 for ob in static:
  if ob.name.startswith('carriage'):
   bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.bevel(bm,geom=list(bm.edges),offset=.065,segments=1,affect='EDGES');bm.to_mesh(ob.data);bm.free();P.paint(ob,C['lavender'])
 mouth=origin+axis*length;burst=[]
 for i,(x,y,kind,size,col) in enumerate([(-.24,.12,'heart',.13,'pink'),(.15,.23,'star',.13,'gold'),(.22,-.17,'heart',.11,'magenta'),(-.15,-.20,'star',.10,'lavender')]):
  out=P.heart(size,10) if kind=='heart' else P.star(size,size*.45)
  vs=[(u,-.025,v) for u,v in out]+[(0,-.10,.03)]+[(u,.025,v) for u,v in out];n=len(out)
  fs=[(j,(j+1)%n,n) for j in range(n)]+[(j,n+1+j,n+1+(j+1)%n,(j+1)%n) for j in range(n)]+[tuple(range(n+1,2*n+1))]
  me=bpy.data.meshes.new('gem_'+kind);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('confetti_'+kind,me);bpy.context.collection.objects.link(o);P.paint(o,C[col]);o.location=mouth+q@Vector((x,y,-.12));burst.append(o)
 emitter=P.pivot('pulse',mouth,burst);barrel.append(emitter)
 static.append(P.pivot('gate',origin,barrel));_fit(P,spec,static)

def _fit(P,spec,children):
 import bpy,bmesh
 from mathutils import Vector,Matrix
 bpy.context.view_layer.update();obs=list(bpy.context.scene.objects)
 world={o:o.matrix_world.copy() for o in obs};parents={o:o.parent for o in obs}
 pts=[world[o]@v.co for o in obs if o.type=='MESH' for v in o.data.vertices]
 lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)])
 s=spec['size_m'];sc=Vector([s[k]/(hi[i]-lo[i]) for i,k in enumerate(['w','d','h'])]);M=Matrix.Diagonal((*sc,1));M.translation=Vector([-(lo.x+hi.x)/2*sc.x,-(lo.y+hi.y)/2*sc.y,-lo.z*sc.z])
 for o in obs:o.parent=None
 for o in obs:
  if o.type=='MESH':
   for v in o.data.vertices:v.co=M@world[o]@v.co
   o.matrix_world=Matrix.Identity(4);o.data.update()
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
  else:o.matrix_world=Matrix.Translation(M@world[o].translation)
 bpy.context.view_layer.update()
 for o in obs:
  if parents[o] is not None:
   mw=o.matrix_world.copy();o.parent=parents[o];o.matrix_parent_inverse=parents[o].matrix_world.inverted();o.matrix_world=mw
 bpy.context.view_layer.update();P.pivot('root',(0,0,0),children)
