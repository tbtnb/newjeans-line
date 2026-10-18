"""H08 Confetti Cannon; spec 2×2.6×2.5 m; 1800 tris.
Pivots: root, gate (barrel trunnion), pulse (mouth/confetti emitter).
SIMPLIFICATIONS: runtime confetti emitter represented by a named empty; no airborne confetti in orthographic rest pose.
"""
import math
BUDGET=1800

def build(P,spec):
 import bpy
 from mathutils import Vector
 C=spec['colors'];static=[];barrel=[]
 def box(n,s,l,c,rot=(0,0,0)):
  o=P.box(n,s,l,C[c],rot=rot);static.append(o);return o
 box('carriage',(1.50,1.60,.50),(0,-.18,.26),'lavender');box('lower_gold_rail',(1.55,1.65,.06),(0,-.18,.26),'gold');box('upper_gold_rail',(1.55,1.65,.055),(0,-.18,.73),'gold')
 for y in [-.95,.47]:
  for x in [-.88,.88]:
   sign=1 if x>0 else -1
   for r,h,offset,col in [(.30,.20,-.10,'lavender'),(.246,.025,.105,'gold'),(.205,.03,.132,'cream'),(.10,.045,.164,'gold')]:
    static.append(P.cyl('faceted_wheel',r,h,(6 if r<.15 else 10),loc=(x+sign*offset,y,.30),rot=(0,sign*90,0),color=C[col]))
 for x in [-.60,.60]:static.append(P.prism('trunnion_cheek',[(-.43,0),(.44,0),(.22,.63),(-.05,.72)],.14,loc=(x,.16,.76),rot=(0,0,90),color=C['lavender']))
 # Hollow tapered barrel, local z axis transformed into upward/front pointing barrel.
 origin=Vector((0,.50,1.14));axis=Vector((0,-.86,.51));q=Vector((0,0,1)).rotation_difference(axis);length=1.72
 def tube(n,profile,color):
  o=P.lathe(n,profile,12,color=C[color]);o.location=origin;o.rotation_euler=q.to_euler();barrel.append(o);return o
 tube('rolled_paper_hollow_barrel',[(0,-.30),(.34,-.28),(.44,-.13),(.47,0),(.51,.40),(.55,.85),(.59,1.20),(.61,length),(.54,length),(.52,1.30),(.47,.80),(.40,.28),(.32,.05),(0,.05)],'cream')
 tube('lavender_breech',[(0,-.32),(.34,-.31),(.45,-.16),(.47,.02),(.42,.04),(0,.04)],'lavender')
 for z,r in [(.12,.485),(1.54,.615)]:tube('gold_barrel_band',[(r,z),(r+.018,z+.025),(r+.018,z+.16),(r,z+.19),(r-.015,z+.16),(r-.015,z)],'gold')
 # Curl lips, modeled as closed hollow loops on either side of the rolled sheet seam.
 for side in [-1,1]:
  vs=[];fs=[];N=10;M=4;center=origin+axis*.88+Vector((side*.54,0,0))
  for i in range(N):
   a=i*2*math.pi/N
   for j in range(M):
    b=j*2*math.pi/M;r=.13+.025*math.cos(b);v=Vector((side*.025*math.sin(b),r*math.cos(a),r*math.sin(a)));vs.append(tuple(center+v))
  for i in range(N):
   for j in range(M):fs.append((i*M+j,i*M+(j+1)%M,((i+1)%N)*M+(j+1)%M,((i+1)%N)*M+j))
  me=bpy.data.meshes.new('scroll');me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new('paper_scroll',me);bpy.context.collection.objects.link(ob);P.paint(ob,C['cream']);barrel.append(ob)
 # Front bow: real folded wings, knot, and swallow tails.
 for side in [-1,1]:
  outline=[(side*.03,.60),(side*.47,.96),(side*.59,.80),(side*.55,.47),(side*.14,.48)]
  static.append(P.prism('bow_gold',outline,.13,loc=(0,-1.02,0),color=C['gold']))
  static.append(P.prism('bow_pink',[(x*.90,z*.96+.025) for x,z in outline],.15,loc=(0,-1.04,0),color=C['pink']))
  static.append(P.prism('ribbon_tail',[(side*.07,.55),(side*.30,.56),(side*.49,.12),(side*.32,.18),(side*.21,.09)],.06,loc=(0,-1.09,0),color=C['magenta']))
 static.append(P.ico('bow_knot',.15,loc=(0,-1.16,.55),scale=(.8,.6,1),subdiv=1,color=C['gold']))
 for side in [-1,1]:static.append(P.ico('trunnion_pin',.135,loc=(side*.71,.30,1.24),scale=(.5,1,1),subdiv=1,color=C['gold']))
 # Raised folds in the pink bow wings (four visible extra triangles).
 import bmesh
 for ob in static:
  if ob.type=='MESH' and ob.name.startswith('bow_pink'):
   bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update();bmesh.ops.poke(bm,faces=[f for f in bm.faces if f.normal.y<-.7],offset=.07);bm.to_mesh(ob.data);bm.free();P.paint(ob,C['pink'])
 mouth=origin+axis*length;emitter=P.pivot('pulse',mouth,[]);barrel.append(emitter)
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
