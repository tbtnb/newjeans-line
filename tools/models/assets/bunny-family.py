"""H07 Bunny Family of Five; size from spec 4.6×1.6×3 m; budget 4000.
Pivots: root, bob0..4, ears0..4 nested under each bob (11 groups).
SIMPLIFICATIONS: tiny facial marks use palette lavender; arms share their bunny bob rather than independent shoulder animation.
"""
import math
BUDGET=4000

def build(P,spec):
 C=spec['colors'];static=[];bobs=[];all_ears=[]
 base=P.lathe('faceted_paper_hill',[(0,0),(1,.0),(.99,.19),(.94,.36),(0,.36)],14,color=C['cream']);base.scale=(2.3,.8,1);static.append(base)
 o=P.cyl('mint_hill_top',1,.025,14,loc=(0,0,.36),color=C['mint']);o.scale=(2.16,.70,1);static.append(o)
 for i,(x,h,col) in enumerate([(-1.66,2.17,'mint'),(-.83,2.08,'blush'),(0,2.72,'lavender'),(.91,2.23,'sun'),(1.74,1.91,'sky')]):
  k=h/2.72; z=.38;parts=[];arms=[];earparts=[];wave=-1 if i in (0,1) else 1
  def ico(n,l,scale,c=col,sub=2):
   ob=P.ico(str(i)+n,1,loc=l,scale=tuple(v*k for v in scale),subdiv=sub,color=C[c]);parts.append(ob);return ob
  body=P.lathe('faceted_bunny_body',[(0,0),(.26,.05),(.43,.22),(.48,.40),(.33,.90),(.24,1.09),(0,1.19)],10,loc=(x,.03,z),color=C[col]);body.scale=(k,.92*k,k);parts.append(body)
  ico('belly',(x,-.46*k,z+.59*k),(.255,.10,.47),'cream')
  ico('head',(x,-.015,z+1.62*k),(.50,.46,.47));ico('muzzle',(x,-.45*k,z+1.50*k),(.34,.13,.20),'cream')
  for sx in [-1,1]:
   ico('foot',(x+sx*.245*k,-.14*k,z+.07*k),(.20,.26,.12),'cream',1)
   ico('eye',(x+sx*.18*k,-.47*k,z+1.65*k),(.041,.026,.052),('sky' if col=='lavender' else 'lavender'),1)
   ob=ico('arm',(x+sx*.50*k,-.04,z+(.99 if sx==wave else .68)*k),(.15,.16,.27),col,1);
   if sx==wave:parts.remove(ob);arms.append(ob)
   hand=P.ico('hand',1,loc=(x+sx*.59*k,-.105,z+(1.22 if sx==wave else .48)*k),scale=(.105*k,.115*k,.12*k),subdiv=1,color=C['cream']);(arms if sx==wave else parts).append(hand)
   # Thick ear with a front ridge and a folded tip.
   outline=[(-.14,0),(-.23,.40),(-.20,.65),(-.03,.80),(.19,.65),(.19,.26),(.08,0)]
   ob=P.prism('folded_ear',[(a*k,b*k) for a,b in outline],.30*k,loc=(x+sx*.23*k,.015,z+1.93*k),color=C[col],rot=(0,sx*16,0))
   for v in ob.data.vertices:
    t=v.co.z/(.80*k);v.co.y*=max(.12,max(0,math.sin(math.pi*t))**.7)
    v.co.y+=.12*k*t
   earparts.append(ob)
   inner=P.prism('inner_pink',[(a*.58*k,b*.79*k+.065*k) for a,b in outline],.025*k,loc=(x+sx*.23*k,-.163*k,z+1.93*k),color=C['blush'],rot=(0,sx*16,0));earparts.append(inner)
   fold=P.prism('ear_fold',[(0,.12*k),(.07*k,.55*k),(0,.73*k),(-.04*k,.49*k)],.035*k,loc=(x+sx*.23*k,-.185*k,z+1.93*k),color=C['cream'],rot=(0,sx*16,0));earparts.append(fold)
  ico('nose',(x,-.60*k,z+1.55*k),(.038,.025,.026),'blush',1)
  parts.append(P.pivot('ears'+str(i),(x,0,z+1.93*k),earparts))
  parts.extend(arms)
  bobs.append(P.pivot('bob'+str(i),(x,0,z),parts))
 _fit(P,spec,static+bobs)

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
