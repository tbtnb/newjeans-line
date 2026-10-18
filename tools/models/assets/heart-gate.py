"""H06 Heart Finish Gate; spec 12×3×11 m; budget 5000.
Pivots: root, gate0/1 at page feet, bob0/1 at bunny feet.
SIMPLIFICATIONS: layered folded pages replace individual curled sheets; warm bulbs are baked; no lettering. Real heart opening remains open. Top sheet has a lower width/depth ratio than the exact size_m; front/hero govern.
"""
import math
BUDGET=5000

def build(P,spec):
 import bpy
 C=spec['colors'];stat=[];gates=[]
 def strip(n,path,width,depth,y,col,reference=None):
  # A closed ribbon surface with bevel-like front/back ridges.
  verts=[];ybase=y
  for i,(x,z) in enumerate(path):
   a=path[max(0,i-1)];b=path[min(len(path)-1,i+1)];dx=b[0]-a[0];dz=b[1]-a[1];l=math.hypot(dx,dz);nx=-dz/l;nz=dx/l
   if i==len(path)-1:nx=0;nz=1
   section_depth=depth*(.92+.08*math.sin(math.pi*min(1,z/9)))
   curve_x=reference[i][0] if reference else x
   y=ybase+.06*math.sin(z*.65)-.60*(min(1,abs(curve_x)/5.1))**6
   for w,dy in [(-width/2,section_depth/2),(-width/2,-section_depth*.20),(-width*.37,-section_depth/2),(width*.37,-section_depth/2),(width/2,-section_depth*.20),(width/2,section_depth/2)]:verts.append((x+nx*w,y+dy,z+nz*w))
  faces=[]
  for i in range(len(path)-1):
   for k in range(6):faces.append((i*6+k,i*6+(k+1)%6,(i+1)*6+(k+1)%6,(i+1)*6+k))
  faces.extend([tuple(range(5,-1,-1)),tuple((len(path)-1)*6+k for k in range(6))]);me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(ob);P.paint(ob,C[col]);
  if col=='gold' and n=='curled_page':
   P.paint(ob,C['cream'],faces={f.index for f in me.polygons if f.normal.z>.25 and f.index%6 in (1,3)})
  return ob
 path=[(-3.52,.52),(-3.50,1.35),(-3.62,2.36),(-3.93,3.42),(-4.42,4.50),(-4.92,5.52),(-5.10,6.55),(-4.97,7.48),(-4.50,8.25),(-3.80,8.76),(-2.90,8.99),(-2.07,8.91),(-1.27,8.48),(-.58,7.87),(0,7.65)]
 for side in [-1,1]:
  p=[(-side*x,z) for x,z in path];parts=[]
  for w,depth,y,col in [(2.55,.80,.55,'gold'),(2.35,.80,.49,'cream'),(1.90,.78,.40,'cream'),(.17,.12,-.22,'pink')]:
   q=p
   if col=='pink':q=[(x+side*.84,z) for x,z in p]
   parts.append(strip('curled_page',q,w,depth,y,col,reference=p))
  # lamp rail follows the inner folded edge of each page.
  rail=[(x-side*.88,z) for x,z in p]
  parts.append(strip('gold_bulb_rail',rail,.19,.12,-.25,'gold',reference=p))
  for j,(x,z) in enumerate(rail[1:-1],1):parts.append(P.ico('warm_bulb',.145,loc=(x,-.37+.06*math.sin(z*.65)-.60*(min(1,abs(p[j][0])/5.1))**6,z),subdiv=1,color=C['lamp']))
  gates.append(P.pivot('gate'+str(len(gates)),(side*3.52,.25,.47),parts))
  for z,h,col in [(0,.13,'gold'),(.13,.51,'cream')]:
   foot=P.prism('foot_plinth',[(-2.02,0),(2.02,0),(1.78,h),(-1.78,h)],2.60,loc=(side*3.62,-.10,z),color=C[col])
   for v in foot.data.vertices:
    if v.co.y<0:v.co.x*=.72
   foot.data.update();stat.append(foot)
  bunny=[];x=side*3.65;y=-.63
  for k in [-1,1]:
   stat.append(P.prism('folded_page_fan',[(-.48,0),(.45,0),(.83,1.60),(-.24,1.20)],.15,loc=(x+k*.60,-.04,.63),rot=(0,k*20,0),color=C['gold']))
   stat.append(P.prism('pink_page_fan',[(-.35,0),(.30,0),(.64,1.35),(-.17,1.03)],.17,loc=(x+k*.60,-.14,.66),rot=(0,k*20,0),color=C['pink']))
  for name,r,l,scale,sub,col in [('body',.55,(x,y,1.18),(1,.72,1.2),2,'white'),('head',.47,(x,y,2.15),(1,.78,.85),2,'cream'),('paw',.19,(x-.4,y-.22,1.52),(1,.7,1),1,'white'),('paw',.19,(x+.4,y-.22,1.52),(1,.7,1),1,'white')]:bunny.append(P.ico(name,r,loc=l,scale=scale,subdiv=sub,color=C[col]))
  for sign in [-1,1]:
   bunny.append(P.prism('thick_ear',[(-.16,0),(-.23,.67),(-.17,1.10),(.06,1.16),(.22,.65),(.14,0)],.20,loc=(x+sign*.23,y,2.44),rot=(0,sign*24,0),color=C['cream']))
   bunny.append(P.prism('inner_ear',[(-.07,.15),(-.10,.68),(-.06,.94),(.05,.99),(.11,.65),(.06,.18)],.024,loc=(x+sign*.23,y-.114,2.44),rot=(0,sign*24,0),color=C['blush']))
   bunny.append(P.ico('toe',.22,loc=(x+sign*.26,y-.12,.76),scale=(1,1.2,.7),color=C['cream'],subdiv=1))
  bunny.append(P.prism('held_heart',P.heart(.43,18),.27,loc=(x,y-.47,1.49),color=C['pink']))
  for ob in bunny:
   ob.location.x=x+(ob.location.x-x)*1.25
   ob.scale.x*=1.25
  stat.append(P.pivot('bob'+str(0 if side<0 else 1),(x,y,.64),bunny))
 # Large paper bow and two tails at the heart crown.
 for side in [-1,1]:
  stat.append(P.prism('bow_gold',[ (side*.15,9.00),(side*1.80,10.68),(side*2.15,10.42),(side*2.32,8.67),(side*1.72,8.38)],1.30,loc=(0,.18,0),color=C['gold']))
  stat.append(P.prism('bow_cream',[(side*.2,9.02),(side*1.79,10.50),(side*1.97,10.22),(side*2.10,8.81),(side*1.72,8.61)],1.34,loc=(0,.12,0),color=C['cream']))
  stat.append(P.prism('bow_tail',[(side*.25,8.80),(side*.72,8.88),(side*1.36,7.62),(side*.88,7.82),(side*.56,7.55)],.14,loc=(0,-.65,0),color=C['blush']))
 stat.append(P.box('bow_knot',(.72,1.48,.96),loc=(0,.10,8.49),color=C['gold']))
 for ob in stat:
  if ob.type=='MESH' and ob.name.startswith('bow_gold'):
   P.paint(ob,C['cream'],faces={f.index for f in ob.data.polygons if f.normal.z>.25})
  if ob.type=='MESH' and ob.name.startswith(('bow_gold','bow_cream')):
   for v in ob.data.vertices:
    v.co.y*=.56+.44*max(0,min(1,(10.7-v.co.z)/1.3))
 # Fold the ribbon fronts into raised facets rather than flat cards.
 import bmesh
 for ob in stat:
  if ob.type=='MESH' and ob.name.startswith('bow_cream'):
   bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update();faces=[f for f in bm.faces if f.normal.y<-.7]
   bmesh.ops.poke(bm,faces=faces,offset=.20);bm.to_mesh(ob.data);bm.free();P.paint(ob,C['cream'])
 _fit(P,spec,stat+gates)

def _fit(P,spec,children):
 import bpy
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
  else:o.matrix_world=Matrix.Translation(M@world[o].translation)
 bpy.context.view_layer.update()
 for o in obs:
  if parents[o] is not None:
   mw=o.matrix_world.copy();o.parent=parents[o];o.matrix_parent_inverse=parents[o].matrix_world.inverted();o.matrix_world=mw
 bpy.context.view_layer.update();P.pivot('root',(0,0,0),children)
