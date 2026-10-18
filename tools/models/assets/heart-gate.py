"""H06 Heart Finish Gate; spec 12 x 3 x 11 m; budget 5000 triangles.
Pivots: root, gate0/1 at the page feet, bob0/1 at rabbit feet.
SIMPLIFICATIONS: warm bulbs use baked lamp colours; curled pages use broad folded
planes; no lettering or fine paper grain. Front/hero govern the inconsistent top aspect.
"""
import math
BUDGET=5000

def build(P,spec):
 import bpy,bmesh
 from mathutils import Vector
 C=spec['colors'];static=[];gates=[]
 def mesh(name,vs,fs,col):
  me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
  ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,C[col]);return ob
 def gem(name,outline,loc,depth,col,accent=None):
  n=len(outline);ring=.84 if name=='folded_bow_loop' else .73;cx=sum(x for x,z in outline)/n;cz=sum(z for x,z in outline)/n
  vs=[(x,-.035,z) for x,z in outline]+[(x,.035,z) for x,z in outline]
  vs += [(cx+(x-cx)*ring,-depth*.72,cz+(z-cz)*ring) for x,z in outline]
  vs += [(cx+(x-cx)*ring,depth*.72,cz+(z-cz)*ring) for x,z in outline]
  vs += [(cx,-depth,cz),(cx,depth,cz)];fs=[]
  for i in range(n):
   j=(i+1)%n;fs += [(i,j,2*n+j,2*n+i),(n+j,n+i,3*n+i,3*n+j),(2*n+i,2*n+j,4*n),(3*n+j,3*n+i,4*n+1),(i,n+i,n+j,j)]
  ob=mesh(name,vs,fs,col);ob.location=loc
  if accent:P.paint(ob,C[accent],faces={5*i+2 for i in range(n) if i%3==0})
  return ob
 # Front contours follow the broad folded shoulder and the deep heart notch.
 outer=[(-3.45,.63),(-3.48,1.95),(-3.66,3.35),(-4.22,4.55),(-5.28,5.65),(-5.91,6.85),(-5.96,7.55),(-5.55,8.60),(-4.73,9.40),(-3.40,9.96),(-2.05,9.78),(-.93,9.18),(0,8.63)]
 inner=[(-1.58,.63),(-1.66,1.95),(-1.93,3.12),(-2.51,4.45),(-3.24,5.60),(-3.51,6.54),(-3.37,7.04),(-2.97,7.50),(-2.45,7.69),(-1.73,7.64),(-1.14,7.33),(-.51,6.90),(0,6.57)]
 def page_shell(side,amount,yoffset,name):
  # Eight vertices across each section: binding edge, bevel, two broad creased planes, back.
  vs=[];n=len(outer)
  for i,((ox,oz),(ix,iz)) in enumerate(zip(outer,inner)):
   dx=ox-ix;dz=oz-iz;cx=(ox+ix)/2;cz=(oz+iz)/2
   for t,y in [(0,.43),(.04,-.22),(.17,-.44),(.50,-.66),(.83,-.44),(.96,-.22),(1,.43),(.50,.59)]:
    x=cx+(t-.5)*dx*amount;z=cz+(t-.5)*dz*amount
    # Flat rear spine with a shallow angular fold on the front; no round tube.
    vs.append((-side*x,y+yoffset,z))
  fs=[]
  for i in range(n-1):
   for k in range(8):fs.append((8*i+k,8*i+(k+1)%8,8*(i+1)+(k+1)%8,8*(i+1)+k))
  fs += [tuple(range(7,-1,-1)),tuple((n-1)*8+k for k in range(8))]
  ob=mesh(name,vs,fs,'cream')
  # A narrow, clean gold binding around the paper, cream remains cream.
  P.paint(ob,C['gold'],faces={i for i in range((n-1)*8) if i%8 in (0,5)})
  if name=='front_folded_page':P.paint(ob,C['white'],faces={i for i in range((n-1)*8) if i%8==3})
  return ob
 for side in [-1,1]:
  parts=[page_shell(side,1,.33,'outer_bound_page'),page_shell(side,.91,.18,'middle_folded_page'),page_shell(side,.82,0,'front_folded_page')]
  # Pink paper is visible at the outer cut edge, behind the cream face.
  vs=[]
  for (ox,oz),(ix,iz) in zip(outer,inner):
   for t in [.89,.98]:vs.append((-side*(ix+(ox-ix)*t),.05,iz+(oz-iz)*t))
  parts.append(mesh('pink_page_edge',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(outer)-1)],'pink'))
  # A real narrow folded lamp channel follows the inner heart contour.
  vs=[];lamp_points=[]
  for (ox,oz),(ix,iz) in zip(outer,inner):
   x=-side*(ix+(ox-ix)*.13);z=iz+(oz-iz)*.13;lamp_points.append((x,-.56,z))
   for t in [.085,.18]:vs.append((-side*(ix+(ox-ix)*t),-.49,iz+(oz-iz)*t))
  edge=[]
  for (ox,oz),(ix,iz) in zip(outer,inner):
   for t in [.015,.055]:edge.append((-side*(ix+(ox-ix)*t),-.22,iz+(oz-iz)*t))
  parts.append(mesh('gold_inner_binding',edge,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(outer)-1)],'gold'))
  patch=[]
  for i in [4,5,6,7]:
   ox,oz=outer[i]
   patch.append((-side*ox,.05 if i in (5,6) else .40,oz))
  patch += [(-side*outer[i][0],.77,outer[i][1]) for i in [7,6,5,4]]
  parts.append(mesh('pink_outer_fold',patch,[tuple(range(8))],'pink'))
  parts.append(mesh('gold_lamp_channel',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(outer)-1)],'gold'))
  for x,y,z in lamp_points[1:-1]:
   parts.append(P.cyl('folded_bulb_socket',.19,.055,8,loc=(x,y,z),rot=(90,0,0),color=C['gold']))
   parts.append(P.ico('warm_bulb',.17,loc=(x,y-.095,z),subdiv=1,color=C['lamp']))
  gates.append(P.pivot('gate'+str(len(gates)),(side*2.55,.15,.62),parts))
  x=side*3.62
  # Chamfered folded foot with a gold binding and a broad cream bevel.
  for z,h,wide,dep,col in [(0,.15,4.70,2.80,'gold'),(.15,.60,4.58,2.70,'cream'),(.73,.10,4.20,2.52,'gold')]:
   vs=[]
   for zz,w,d in [(0,wide,dep),(h,wide-.38,dep-.27)]:
    vs += [(x-w/2,-d/2,zz+z),(x+w/2,-d/2,zz+z),(x+w/2,d/2,zz+z),(x-w/2,d/2,zz+z)]
   plinth=mesh('bevelled_plinth',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],col)
   if z>.6:P.paint(plinth,C['cream'],faces={1})
   static.append(plinth)
  static.append(P.prism('diagonal_plinth_fold',[(x-1.45,.15),(x+.48,.65),(x+1.02,.65),(x-.92,.15)],.06,loc=(0,-1.405,0),color=C['gold']))
  # Folded paper fans splay out behind the rabbit at each foot.
  for sign in [-1,1]:
   poly=[(-.48,0),(.48,0),(.89,1.80),(-.33,1.38)]
   fan=P.prism('gold_folded_fan',poly,.16,loc=(x+sign*.64,-.23,.70),rot=(0,sign*18,0),color=C['gold']);static.append(fan)
   static.append(P.prism('pink_fan_inset',[(a*.78,b*.80+.06) for a,b in poly],.18,loc=(x+sign*.64,-.32,.70),rot=(0,sign*18,0),color=C['pink']))
  rabbit=[];yy=-.91
  rabbit.append(P.lathe('faceted_rabbit_body',[(.42,0),(.65,.20),(.62,.89),(.38,1.26)],8,loc=(x,yy,.78),color=C['white']))
  rabbit.append(P.ico('carved_rabbit_head',.78,loc=(x,yy,2.80),scale=(1,.70,.82),subdiv=1,color=C['cream']))
  for sign in [-1,1]:
   rabbit.append(P.ico('faceted_foot',.48,loc=(x+sign*.43,yy-.13,1.02),scale=(1,.85,1),subdiv=1,color=C['white']))
   rabbit.append(P.ico('front_paw',.26,loc=(x+sign*.62,yy-.43,1.95),scale=(1,.70,1),subdiv=1,color=C['cream']))
   ear=[(-.18,0),(-.29,.80),(-.20,1.48),(.12,1.56),(.29,.90),(.18,.10)]
   ear_ob=gem('creased_ear',ear,(x+sign*.37,yy,3.25),.15,'cream');ear_ob.rotation_euler.y=math.radians(sign*22);rabbit.append(ear_ob)
   inset=[(-.09,.23),(-.16,.82),(-.11,1.28),(.07,1.32),(.16,.86),(.09,.26)]
   ob=P.prism('pink_inner_ear',inset,.026,loc=(x+sign*.37,yy-.18,3.25),rot=(0,sign*22,0),color=C['pink']);rabbit.append(ob)
  heart=P.heart(.75,12);lo=min(z for _,z in heart);hi=max(z for _,z in heart);heart=[(xx,(z-lo)*1.12/(hi-lo)) for xx,z in heart]
  rabbit.append(gem('held_gem_heart',heart,(x,yy-.59,1.35),.29,'pink'))
  static.append(P.pivot('bob'+str(0 if side<0 else 1),(x,yy,.73),rabbit))
 # The crown is a thick folded loop with an exposed pink paper underside.
 for sign in [-1,1]:
  outline=[(sign*.38,9.02),(sign*2.05,8.98),(sign*2.31,9.32),(sign*2.15,10.68),(sign*1.78,10.98),(sign*.98,10.38),(sign*.38,9.74)]
  bow=gem('folded_bow_loop',outline,(0,-.20,0),.51,'cream');static.append(bow)
  n=len(outline)
  # Gold edge facets and pink folded underside of the loop.
  P.paint(bow,C['gold'],faces={5*i for i in range(n) if i in range(n)})
  static.append(P.prism('bow_pink_underside',[(sign*.44,9.05),(sign*2.00,9.03),(sign*2.18,9.31),(sign*.93,9.38)],.045,loc=(0,-.82,0),color=C['blush']))
  tail=[(sign*.31,9.14),(sign*.82,9.09),(sign*1.71,7.81),(sign*1.16,8.00),(sign*.88,7.63)]
  static.append(P.prism('gold_bow_tail',tail,.13,loc=(0,-.78,0),color=C['gold']))
  static.append(P.prism('pink_tail_inset',[(a*.94,b+.08) for a,b in tail],.04,loc=(0,-.88,0),color=C['pink']))
 knot=P.box('chamfered_bow_knot',(.82,1.20,1.40),loc=(0,-.16,8.91),color=C['gold'])
 bm=bmesh.new();bm.from_mesh(knot.data);bmesh.ops.bevel(bm,geom=list(bm.edges),offset=.12,segments=1,affect='EDGES');bm.to_mesh(knot.data);bm.free();P.paint(knot,C['gold']);static.append(knot)
 static.append(P.box('cream_knot_face',(.59,.03,1.05),loc=(0,-.775,9.08),color=C['cream']))
 _fit(P,spec,static+gates)

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
