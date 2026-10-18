"""H09 Giant Storybook Cover; size spec 14×10×1.5 m; budget 3000.
Pivots: root, lid at left spine, gate at page spine.
SIMPLIFICATIONS: no text; page edges represented by layered leaves; shallow bunny relief follows top view; side/front drawing thickness disagrees with spec.
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
  bevel('paper_leaf',(w,d,.0164),(.22,0,.17+i*.0167),'cream' if i%3 else 'pearl',.015,pages)
 page=P.pivot('gate',(-6.45,0,.18),pages);base.append(page)
 bevel('top_mint_board',(14,10,.16),(0,0,.77),'mint',.13,cover)
 # The rolled spine is a beveled rounded block and four gilded transverse bands.
 bevel('rounded_spine',(1.04,9.93,.81),(-6.47,0,.07),'mint',.23)
 for y in [-3.9,-1.35,1.30,3.85]:bevel('gold_spine_band',(1.10,.25,.85),(-6.46,y,.05),'gold',.13)
 # Thin raised inset border with clipped corners.
 pts=[(-5.65,-4.38), (5.78,-4.38),(6.38,-3.78),(6.38,3.78),(5.78,4.38),(-5.65,4.38),(-6.06,3.97),(-6.06,-3.97)]
 for a,b in zip(pts,pts[1:]+pts[:1]):
  dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy)
  ob=P.box('embossed_border',(L,.06,.028),((a[0]+b[0])/2,(a[1]+b[1])/2,.935),C['mint'],rot=(0,0,math.degrees(math.atan2(dy,dx))));cover.append(ob)
 # Corner protectors, folded gold triangles on both boards.
 for x in [-1,1]:
  for y in [-1,1]:
   for z,tgt in [(.94,cover),(.165,base)]:
    ob=P.prism('folded_gold_corner',[(0,0),(1.24,0),(0,1.24)],.045,loc=(x*6.98,y*4.98,z),rot=(90,0,0),color=C['gold']);ob.scale=( -x,1,y);tgt.append(ob)
 # Bunny relief laid in XY. Front remains at -Y.
 cover.append(P.ico('bunny_head_medallion',1,loc=(.38,-.36,1.04),scale=(1.95,1.24,.14),subdiv=2,color=C['cream']))
 for side in [-1,1]:
  outline=[(-.34,0),(-.53,1.20),(-.31,2.72),(.12,3.27),(.40,2.56),(.40,.63),(.19,0)]
  ob=P.prism('folded_bunny_relief_ear',outline,.18,loc=(.38+side*.68,.40,1.02),color=C['pearl'],rot=(-90,0,-side*20));cover.append(ob)
  ridge=P.prism('ear_relief_ridge',[(-.08,.15),(.04,2.97),(.22,1.7),(.18,.4)],.24,loc=(.38+side*.68,.40,1.04),color=C['cream'],rot=(-90,0,-side*20));cover.append(ridge)
 h=P.prism('gold_heart_emblem',P.heart(.75,24),.18,loc=(.38,-2.12,1.11),color=C['gold'],rot=(-90,0,0));cover.append(h)
 cover.append(P.ico('heart_facet',.34,loc=(.38,-2.09,1.15),scale=(1,1,.18),subdiv=1,color=C['foil']))
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
