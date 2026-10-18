"""H05 Paper Lantern Tower; spec size 3.3×3.2×9 m; 2500 tris.
Pivots: root and swing0..5, one paired swing per tier per side.
SIMPLIFICATIONS: baked warm light; sharply bevelled stars/hearts and octagonal round lanterns; top-view star depth follows front/hero; no dynamic colour cycling; paired lanterns swing together; open frame is retained (design mask fills its openings).
"""
import math
BUDGET=2500

def build(P,spec):
 C=spec['colors']; static=[]; swings=[]
 def box(n,s,l,c):
  o=P.box(n,s,l,C[c]);static.append(o);return o
 def lantern(n,x,y,z,kind):
  children=[P.cyl(n+'string',.022,.25,3,loc=(x,y,z+.6),color=C['gold'])]
  if kind==0:
   children += [P.lathe(n,[(.10,-.51),(.43,-.35),(.55,0),(.43,.35),(.10,.51)],8,loc=(x,y,z),color=C['lamp'])]
   # Four narrow gilded ribs follow the faceted round lantern surface.
   import bpy
   profile=[(.10,-.51),(.43,-.35),(.55,0),(.43,.35),(.10,.51)]
   for k in range(4):
    theta=2*math.pi*k/4;vs=[]
    for r,zz in profile:
     for da in [-.013,.013]:vs.append((x+(r+.006)*math.cos(theta+da),y+(r+.006)*math.sin(theta+da),z+zz))
    fs=[(j*2,j*2+1,j*2+3,j*2+2) for j in range(len(profile)-1)];me=bpy.data.meshes.new('gilded_rib');me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new('gilded_rib',me);bpy.context.collection.objects.link(ob);P.paint(ob,C['gold']);children.append(ob)
  else:
   outline=P.heart(.65,14) if kind==1 else P.star(.64,.29)
   children.append(_fold(P,n,outline,(x,y,z),.30 if kind==1 else .31,C['pink' if kind==1 else 'gold'],C['magenta' if kind==1 else 'lamp']))
  children.extend([P.cyl(n+'cap',.105,.07,4,loc=(x,y,z+.52),color=C['gold']),P.cyl(n+'foot',.085,.06,3,loc=(x,y,z-.57),color=C['gold'])])
  return children
 box('plinth',(3.3,3.2,.55),(0,0,0),'gold');box('front_cream_inlay',(2.94,.018,.27),(0,-1.607,.10),'cream')
 box('back_cream_inlay',(2.94,.018,.27),(0,1.607,.10),'cream')
 for sign in [-1,1]:box('side_cream_inlay',(.018,2.84,.27),(sign*1.657,0,.10),'cream')
 for x in [-1.32,1.32]:
  for y in [-1.27,1.27]:
   col=box('column',(.25,.25,6.80),(x*.91,y*.91,.44),'cream')
   col.location.x=x;col.location.y=y;col.rotation_euler.x=math.radians(y*.46);col.rotation_euler.y=math.radians(-x*.46)
   for z in [.44,2.83,5.03,7.14]:
    f=1-.06*z/7.14
    xx=x*f;yy=y*f
    box('gold_collar',(.27,.27,.15),(xx,yy,z),'gold')
    static.append(P.cyl('finial',.19,.23,4,loc=(xx,yy,z+.15),r2=0,color=C['gold'],rot=(0,0,45)))
 for tier,z in enumerate([2.63,4.83,6.99]):
  f=1-.06*z/7.14
  for y in [-1.27,1.27]:box('tier_beam',(2.74*f,.18,.25),(0,y*f,z),'lavender')
  for x in [-1.32,1.32]:box('tier_side',(.18,2.62*f,.25),(x*f,0,z),'lavender')
  for y in [-.60,.60]:
   pair=[]
   for x in [-.61,.61]:pair.extend(lantern('lantern',x,y,z-.85,tier))
   swings.append(P.pivot('swing'+str(len(swings)),(0,y,z),pair))
 for x in [-1.39,1.39]:
  for y in [-1.34,1.34]:
   static.append(P.cyl('plinth_corner_fold',.34,.24,4,loc=(x,y,.32),r2=0,rot=(0,0,45),color=C['gold']))
 box('central_standard',(.17,.17,7.8),(0,0,.44),'cream')
 static.append(_fold(P,'top_star',P.star(.81,.38),(0,0,8.19),.33,C['gold'],C['lamp']))
 _fit(P,spec,static+swings)

def _fold(P,name,outline,loc,depth,color,accent=None):
 import bpy
 n=len(outline)
 vs=[(x,-.035,z) for x,z in outline]+[(x,.035,z) for x,z in outline]
 vs += [(x*.76,-depth*.72*(1-.8*min(1,abs(z-.08)/.65)),z*.76+.03) for x,z in outline]+[(x*.76,depth*.72*(1-.8*min(1,abs(z-.08)/.65)),z*.76+.03) for x,z in outline]
 vs += [(0,-depth,.08),(0,depth,.08)];fs=[]
 for i in range(n):
  j=(i+1)%n
  fs.extend([(i,j,2*n+j,2*n+i),(n+j,n+i,3*n+i,3*n+j),(2*n+i,2*n+j,4*n),(3*n+j,3*n+i,4*n+1),(i,n+i,n+j,j)])
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.location=loc;P.paint(ob,color)
 if accent:P.paint(ob,accent,faces={i*5+2 for i in range(n) if i%3==0})
 return ob

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
