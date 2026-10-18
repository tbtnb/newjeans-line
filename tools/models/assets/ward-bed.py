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
 # Three broad panels: the middle panel has its own paper crease, not an extra upright.
 from mathutils import Vector
 points=[(-1.62,1.05),(-.69,.75),(.18,1.05),(.92,.75),(1.53,1.05)];curtain_groups={0:[],1:[],2:[]}
 def beam(name,a,b,w,c,parts):
  d=Vector(b)-Vector(a);o=P.box(name,(w,w,d.length),a,C[c]);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();parts.append(o)
 for i,(a,b) in enumerate(zip(points,points[1:])):
  parts=[];za=2.40 if i%2==0 else 2.31;zb=2.31 if i%2==0 else 2.40
  vs=[(a[0],a[1],.13),(b[0],b[1],.13),(b[0],b[1]-.20,zb),(a[0],a[1]-.20,za),((a[0]+b[0])/2,(a[1]+b[1])/2-.085,1.28)]
  vs+= [(x,y+.10,z) for x,y,z in vs[:4]]
  fs=[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(5,8,7,6),(0,5,6,1),(1,6,7,2),(2,7,8,3),(3,8,5,0)]
  me=bpy.data.meshes.new('creased_panel');me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new('creased_curtain',me);bpy.context.collection.objects.link(ob);P.paint(ob,C['wardgray']);parts.append(ob)
  dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy);ang=math.degrees(math.atan2(dy,dx))
  o=P.box('coral_screen_hem',(L,.065,.20),((a[0]+b[0])/2,(a[1]+b[1])/2,.15),C['coral'],rot=(0,0,ang));parts.append(o)
  beam('cream_screen_top',(a[0],a[1]-.20,za-.065),(b[0],b[1]-.20,zb-.065),.065,'cream',parts)
  if i in [0,1,3]:
   beam('screen_post',(a[0],a[1],.04),(a[0],a[1]-.20,za),.065,'cream',parts)
  if i==3:beam('screen_end_post',(b[0],b[1],.04),(b[0],b[1]-.20,zb),.065,'cream',parts)
  if i in [1,3]:
   for z in [.28,2.08]:parts.append(P.cyl('fold_hinge',.035,.22,8,loc=(a[0],a[1]-.045,z),color=C['lamp']))
  if i in [0,3]:
   p=a if i==0 else b;parts.append(P.cyl('screen_paper_foot',.145,.26,4,loc=(p[0],p[1],0),r2=0,color=C['cream'],rot=(0,0,45)))
  curtain_groups[0 if i==0 else 2 if i==3 else 1].extend(parts)
 for i,parts in curtain_groups.items():
  j=[0,1,3][i];stat.append(P.pivot('gate'+str(i),(points[j][0],points[j][1],.06),parts))
 # Wide bed runs across X, pillow on the left.
 bevel('bed_frame',(2.72,1.54,.29),(.22,-.34,.22),'cream');box('coral_frame_edge',(2.73,1.56,.08),(.22,-.34,.22),'coral')
 bevel('mattress',(2.59,1.48,.23),(.22,-.34,.47),'white',amount=.05)
 bevel('blanket',(1.67,1.50,.48),(.66,-.34,.45),'wardgray',amount=.035)
 box('blanket_hem',(.18,1.53,.48),(-.11,-.34,.45),'wardgray')
 # A low poly quilt surface with real broad facets.
 for ix in range(5):
  for iy in range(3):
   x=.00+ix*.326;y=-1.09+iy*.50
   verts=[(x,y,.923),(x+.326,y,.923),(x+.326,y+.50,.923),(x,y+.50,.923),(x+.163,y+.25,.94+(.04 if (ix+iy)%2 else 0))];faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
   me=bpy.data.meshes.new('blanket_facet');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('blanket_facet',me);bpy.context.collection.objects.link(o);P.paint(o,C['wardgray']);bed.append(o)
 # Rectangular, clipped-corner paper cushion with broad triangular crown facets.
 ring=[(-.30,-.52),(.20,-.52),(.31,-.38),(.31,.38),(.20,.52),(-.20,.52),(-.31,.38),(-.31,-.38)]
 vs=[(-.72+x,-.34+y,.73) for x,y in ring]+[(-.72+x*.77,-.34+y*.77,.94) for x,y in ring]+[(-.72,-.34,1.06)]
 fs=[]
 for j in range(8):
  k=(j+1)%8;fs.extend([(j,k,8+j),(k,8+k,8+j),(8+j,8+k,16)])
 fs.append(tuple(reversed(range(8))));me=bpy.data.meshes.new('creased_pillow');me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new('creased_pillow',me);bpy.context.collection.objects.link(ob);P.paint(ob,C['wardgray']);bed.append(ob)
 for x in [-1.17,1.61]:
  board=P.prism('bed_end',[(-.77,0),(.77,0),(.77,.86),(.65,1.01),(-.65,1.01),(-.77,.86)],.07,loc=(x,-.34,.04),rot=(0,0,90),color=C['cream']);bed.append(board)
  for y in [-1.00,.32]:
   box('bed_post',(.065,.065,1.01),(x,y,0),'cream');bed.append(P.cyl('paper_foot',.145,.24,4,loc=(x,y,0),r2=.023,color=C['cream'],rot=(0,0,45)))
 # Coral end-board stripe and cream folded edge protectors.
 for x in [-1.215,1.655]:
  box('coral_endboard_stripe',(.017,1.40,.23),(x,-.34,.045),'coral')
  for y in [-1.08,.40]:box('endboard_rim',(.026,.025,.80),(x,y,.12),'cream')
 # Nightstand and faceted warm lamp at left.
 bevel('nightstand',(.44,.59,.57),(-1.48,-.75,.02),'cream',stat,amount=.025);box('nightstand_coral',(.44,.59,.12),(-1.48,-.75,.02),'coral',stat)
 box('drawer',(.33,.012,.30),(-1.48,-1.056,.24),'white',stat)
 for n,r,h,z,r2,col in [('lamp_base',.17,.045,.60,.17,'cream'),('lamp_stem',.075,.53,.645,.045,'lamp'),('lamp_neck',.09,.10,1.165,.09,'lamp'),('lamp_shade',.27,.34,1.25,.16,'cream')]:stat.append(P.cyl(n,r,h,8,loc=(-1.48,-.75,z),r2=r2,color=C[col]))
 stat.append(P.lathe('folded_crystal_lamp',[(.09,0),(.12,.10),(.05,.20),(.12,.32),(.06,.43)],6,loc=(-1.48,-.75,.64),color=C['lamp']))
 stat.append(P.ico('warm_bulb',.12,loc=(-1.48,-.75,1.24),subdiv=2,color=C['lamp']))
 # Fine cabinet edging and the mattress piping are broad, clean paper strips.
 for x in [-1.68,-1.28]:box('cabinet_vertical_trim',(.024,.025,.43),(x,-1.06,.14),'cream',stat)
 for z in [.19,.55]:box('cabinet_horizontal_trim',(.40,.025,.024),(-1.48,-1.06,z),'cream',stat)
 stat.append(P.ico('drawer_pull',.045,loc=(-1.48,-1.085,.40),subdiv=1,color=C['lamp']))
 for y in [-1.08,.40]:box('mattress_piping',(2.67,.028,.026),(.22,y,.49),'cream')
 box('front_frame_top_trim',(2.67,.027,.025),(.22,-1.10,.45),'cream')
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
