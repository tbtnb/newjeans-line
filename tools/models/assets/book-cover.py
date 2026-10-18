"""H09 Giant Storybook Cover; size spec 14×10×1.5 m; budget 3000.
Pivots: root, lid at left spine, gate at page spine.
SIMPLIFICATIONS: no text; page edges represented by layered leaves; creased gem bunny relief follows top view; side/front drawing thickness disagrees with spec.
"""
import math
BUDGET=3000

def build(P,spec):
 import bpy,bmesh
 C=spec['colors'];base=[];cover=[];pages=[]
 def bevel(n,s,l,c,bev=.10,target=None):
  ob=P.box(n,s,l,C[c]);bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.bevel(bm,geom=list(bm.edges),offset=bev,segments=1,affect='EDGES');bm.to_mesh(ob.data);bm.free();P.paint(ob,C[c]);(base if target is None else target).append(ob);return ob
 bevel('bottom_mint_board',(14,10,.16),(0,0,0),'mint',.12)
 # A dense visible stack of actual thin paper leaves and tiny irregular fore-edge offsets.
 for i in range(35):
  w=13.12+.035*math.sin(i*2);d=9.64+.025*math.cos(i*1.7)
  bevel('paper_leaf',(w,d,.0164),(.22,0,.17+i*.0146),'cream' if i%3 else 'pearl',.015,pages)
 page=P.pivot('gate',(-6.45,0,.18),pages);base.append(page)
 bevel('top_mint_board',(13.0,10,.16),(.50,0,.77),'mint',.13,cover)
 # The rolled spine is a beveled rounded block and four gilded transverse bands.
 bevel('rounded_spine',(1.04,9.93,.90),(-6.47,0,.07),'mint',.23)
 for y in [-3.9,-1.35,1.30,3.85]:bevel('gold_spine_band',(1.10,.25,.95),(-6.46,y,.05),'gold',.025)
 # Thin raised inset border with clipped corners.
 pts=[(-5.65,-4.38), (5.78,-4.38),(6.38,-3.78),(6.38,3.78),(5.78,4.38),(-5.65,4.38),(-5.77,3.97),(-5.77,-3.97)]
 for a,b in zip(pts,pts[1:]+pts[:1]):
  dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
  ob=P.box('embossed_border',(L,.06,.028),((a[0]+b[0])/2,(a[1]+b[1])/2,.935),C['mint'],rot=(0,0,math.degrees(math.atan2(dy,dx))));cover.append(ob)
 # Gold protectors are folded triangular solids, with a raised diagonal crease.
 def relief(name,outline,z,peak,col,target,center=None):
  center=center or (sum(p[0] for p in outline)/len(outline),sum(p[1] for p in outline)/len(outline))
  vs=[(x,y,z) for x,y in outline]+[(center[0],center[1],peak)]+[(x,y,z-.055) for x,y in outline];n=len(outline)
  fs=[(i,(i+1)%n,n) for i in range(n)]+[(i,n+1+i,n+1+(i+1)%n,(i+1)%n) for i in range(n)]+[tuple(range(n+1,2*n+1))]
  me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,C[col]);target.append(ob);return ob
 for x in [-1,1]:
  for y in [-1,1]:
   for z,tgt in [(.94,cover),(.165,base)]:
    shift=1.10 if x<0 and tgt is cover else 0
    relief('creased_gold_corner',[(x*6.95+shift,y*4.95),(x*5.50+shift,y*4.95),(x*6.95+shift,y*3.50)],z,z+.04,'gold',tgt)
 # Twelve broad cut planes surround a domed, triangulated bunny-head relief.
 outline=[(.38+1.95*math.cos(t*math.tau/12),-.36+1.24*math.sin(t*math.tau/12)) for t in range(12)]
 vs=[(x,y,.945) for x,y in outline]+[(.38+(x-.38)*.69,-.36+(y+.36)*.69,1.065) for x,y in outline]+[(.38,-.36,1.105)]
 fs=[]
 for j in range(12):
  k=(j+1)%12;fs.extend([(j,k,12+j),(k,12+k,12+j),(12+j,12+k,24)])
 fs.append(tuple(reversed(range(12))))
 me=bpy.data.meshes.new('faceted_bunny_medallion');me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new('faceted_bunny_medallion',me);bpy.context.collection.objects.link(ob);P.paint(ob,C['cream']);P.paint(ob,C['pearl'],faces={2,8,14,20,26,32});cover.append(ob)
 for side in [-1,1]:
  # Polygonal ear with a knife crease, broad at the middle and pointed at the tip.
  ear=[(-.30,0),(-.62,1.35),(-.30,2.73),(.05,3.25),(.50,2.44),(.48,.71),(.19,0)]
  angle=math.radians(-side*20)
  outline=[(.38+side*.68+u*math.cos(angle)-v*math.sin(angle),.40+u*math.sin(angle)+v*math.cos(angle)) for u,v in ear]
  relief('creased_pearl_ear',outline,.945,1.105,'cream',cover)
 # The heart is a ten-sided gem, including the notch and pointed lower tip.
 out=[(-.76,.18),(-.76,.62),(-.42,.83),(0,.56),(.42,.83),(.76,.62),(.76,.18),(0,-.58)]
 relief('faceted_gold_heart',[(.38+x,-2.12+y) for x,y in out],.96,1.11,'gold',cover,center=(.38,-1.96))
 base.append(P.pivot('lid',(-6.48,0,.78),cover));_fit(P,spec,base)
 # Both spine joints use local X along the physical Y-axis spine.
 for name in ['pivot_lid','pivot_gate']:
  pivot=bpy.data.objects[name];saved={o:o.matrix_world.copy() for o in pivot.children};pivot.rotation_euler.z=math.pi/2;bpy.context.view_layer.update()
  for o,mw in saved.items():o.matrix_parent_inverse=pivot.matrix_world.inverted();o.matrix_world=mw

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
