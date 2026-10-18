"""H10 Pop-up Paper Ward Bed; spec size 3.4×2.1×2.4 m; 2000 tris.
Pivots: root; gate0/1/2 (curtain folds), lid (bed pull-tab fold).
SIMPLIFICATIONS: lamp light baked; triangulated blanket is one folded paper volume; gold-looking outlines use prescribed cream/lamp.
"""
import math
BUDGET=2000

def build(P,spec):
 import bpy,bmesh
 C=spec['colors'];stat=[];bed=[]
 def box(n,s,l,c,tgt=bed):
  o=P.box(n,s,l,C[c]);tgt.append(o);return o
 def bevel(n,s,l,c,tgt=bed,amount=.06):
  o=P.box(n,s,l,C[c]);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.bevel(bm,geom=list(bm.edges),offset=amount,segments=1,affect='EDGES');bm.to_mesh(o.data);bm.free();P.paint(o,C[c]);tgt.append(o);return o
 # Three broad creased curtain panels with a zigzag footprint.
 points=[(-1.62,.95),(-.69,.59),(.18,.95),(.92,.59),(1.53,.95)];curtain_groups={0:[],1:[],2:[]}
 for i,(a,b) in enumerate(zip(points,points[1:])):
  dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy);ang=math.degrees(math.atan2(dy,dx));parts=[]
  # Faceted panel with central origami crease, coloured all in the specified wardgray.
  verts=[(a[0],a[1],.13),(b[0],b[1],.13),(b[0],b[1],2.40),(a[0],a[1],2.40),((a[0]+b[0])/2,(a[1]+b[1])/2-.10,1.28)]
  faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4)];me=bpy.data.meshes.new('creased_panel');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new('creased_curtain',me);bpy.context.collection.objects.link(ob);P.paint(ob,C['wardgray']);parts.append(ob)
  # Real shallow folded thickness in plan view.
  slab=P.box('curtain_paper_thickness',(L,.20,2.19),((a[0]+b[0])/2,(a[1]+b[1])/2+.14,.14),C['wardgray'],rot=(0,0,ang));parts.append(slab)
  for z,height,col in [(.15,.20,'coral'),(2.32,.08,'cream')]:
   o=P.box('curtain_edge',(L,.045,height),((a[0]+b[0])/2,(a[1]+b[1])/2,z),C[col],rot=(0,0,ang));parts.append(o)
  for p in [a,b]:parts.append(P.box('curtain_upright',(.055,.06,2.38),(p[0],p[1],.04),C['cream']))
  for z in [.28,1.91]:parts.append(P.cyl('fold_hinge',.035,.22,8,loc=(a[0],a[1]-.033,z),color=C['lamp']))
  for p in [a,b]:parts.append(P.cyl('folded_screen_foot',.13,.20,4,loc=(p[0],p[1],0),r2=.025,color=C['cream'],rot=(0,0,45)))
  curtain_groups[min(i,2)].extend(parts)
 for i,parts in curtain_groups.items():stat.append(P.pivot('gate'+str(i),(points[i][0],points[i][1],.06),parts))
 # Wide bed runs across X, pillow on the left.
 bevel('bed_frame',(2.72,1.34,.25),(.22,-.34,.22),'cream');box('coral_frame_edge',(2.73,1.36,.065),(.22,-.34,.22),'coral')
 bevel('mattress',(2.59,1.28,.23),(.22,-.34,.47),'white',amount=.05)
 bevel('blanket',(1.67,1.30,.25),(.66,-.34,.57),'wardgray',amount=.035)
 box('blanket_hem',(.18,1.33,.26),(-.11,-.34,.57),'wardgray')
 # A low poly quilt surface with real broad facets.
 for ix in range(5):
  for iy in range(3):
   x=.00+ix*.326;y=-.85+iy*.34
   verts=[(x,y,.823),(x+.326,y,.823),(x+.326,y+.34,.823),(x,y+.34,.823),(x+.163,y+.17,.84+(.015 if (ix+iy)%2 else 0))];faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
   me=bpy.data.meshes.new('blanket_facet');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('blanket_facet',me);bpy.context.collection.objects.link(o);P.paint(o,C['wardgray']);bed.append(o)
 bed.append(P.ico('pillow',1,loc=(-.70,-.34,.92),scale=(.38,.39,.18),rot=(0,25,0),subdiv=3,color=C['wardgray']))
 for x in [-1.17,1.61]:
  board=P.prism('bed_end',[(-.67,0),(.67,0),(.67,.86),(.56,1.01),(-.56,1.01),(-.67,.86)],.07,loc=(x,-.34,.04),rot=(0,0,90),color=C['cream']);bed.append(board)
  for y in [-.89,.21]:
   box('bed_post',(.065,.065,1.01),(x,y,0),'cream');bed.append(P.cyl('paper_foot',.115,.16,4,loc=(x,y,0),r2=.023,color=C['cream'],rot=(0,0,45)))
 # Coral end-board stripe and cream folded edge protectors.
 for x in [-1.215,1.655]:
  box('coral_endboard_stripe',(.017,1.19,.23),(x,-.34,.045),'coral')
  for y in [-.94,.26]:box('endboard_rim',(.026,.025,.80),(x,y,.12),'cream')
 # Nightstand and faceted warm lamp at left.
 bevel('nightstand',(.44,.59,.57),(-1.48,-.75,.02),'cream',stat,amount=.025);box('nightstand_coral',(.44,.59,.12),(-1.48,-.75,.02),'coral',stat)
 box('drawer',(.33,.012,.30),(-1.48,-1.056,.24),'white',stat)
 for n,r,h,z,r2,col in [('lamp_base',.17,.045,.60,.17,'cream'),('lamp_stem',.075,.53,.645,.045,'lamp'),('lamp_neck',.09,.10,1.165,.09,'lamp'),('lamp_shade',.27,.34,1.25,.16,'cream')]:stat.append(P.cyl(n,r,h,8,loc=(-1.48,-.75,z),r2=r2,color=C[col]))
 stat.append(P.lathe('folded_crystal_lamp',[(.09,0),(.12,.10),(.05,.20),(.12,.32),(.06,.43)],6,loc=(-1.48,-.75,.64),color=C['lamp']))
 stat.append(P.ico('warm_bulb',.12,loc=(-1.48,-.75,1.24),subdiv=2,color=C['lamp']))
 # Pull tab underneath the left foot of the bed.
 box('pull_tab',(.40,.25,.03),(-.8,-.91,.025),'cream')
 stat.append(P.pivot('lid',(-1.15,0,0),bed));_fit(P,spec,stat)
 # Curtain folds rotate about vertical joints; bed hinge follows the Y-axis end-board.
 for name in ['pivot_gate0','pivot_gate1','pivot_gate2','pivot_lid']:
  pivot=bpy.data.objects[name];saved={o:o.matrix_world.copy() for o in pivot.children}
  if name=='pivot_lid':pivot.rotation_euler.z=math.pi/2
  else:pivot.rotation_euler.y=-math.pi/2
  bpy.context.view_layer.update()
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
