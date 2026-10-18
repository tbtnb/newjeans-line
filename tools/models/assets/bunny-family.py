"""H07 Bunny Family of Five; spec 4.6 x 1.6 x 3 m; budget 4000.
Pivots: root, bob0..4, ears0..4 (11 groups).
SIMPLIFICATIONS: waving arms share each bunny bob to respect the 12-group cap; eyes use the spec lavender/sky rather than an extra dark pigment.
"""
import math
BUDGET=4000

def build(P,spec):
 import bpy,bmesh
 C=spec['colors'];static=[];bobs=[]
 def mesh(n,vs,fs,c):
  me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);P.paint(o,C[c]);return o
 # Triangulated, chamfered oval plinth: broad creases rather than a smooth hill.
 n=16;vs=[]
 for rx,ry,z in [(2.3,.8,0),(2.30,.80,.08),(2.20,.73,.43),(2.10,.68,.46)]:
  vs.extend([(rx*math.cos(t*math.tau/n+(.07 if z==.08 else 0)),ry*math.sin(t*math.tau/n+(.07 if z==.08 else 0)),z) for t in range(n)])
 fs=[tuple(reversed(range(n)))]
 for ring in range(3):
  for j in range(n):
   a=ring*n+j;b=ring*n+(j+1)%n;c=(ring+1)*n+(j+1)%n;d=(ring+1)*n+j
   fs.extend([(a,b,d),(b,c,d)])
 fs.append(tuple(range(3*n,4*n)));static.append(mesh('creased_cream_hill',vs,fs,'cream'))
 o=P.cyl('mint_hill_top',1,.025,16,loc=(0,0,.46),color=C['mint']);o.scale=(2.10,.68,1);static.append(o)
 for i,(x,h,col) in enumerate([(-1.66,2.21,'mint'),(-.83,2.22,'blush'),(0,2.72,'lavender'),(.91,2.22,'sun'),(1.74,1.91,'sky')]):
  k=h/2.72;z=.485;parts=[];es=[];wave=-1 if i in (0,1) else 1
  def ico(n,l,scale,c=col,sub=2):
   o=P.ico(str(i)+n,1,loc=l,scale=tuple(v*k for v in scale),subdiv=sub,color=C[c]);parts.append(o);return o
  body=P.lathe('angular_bunny_body',[(0,0),(.30,.04),(.44,.19),(.48,.42),(.36,.71),(.30,1.05),(.23,1.21),(0,1.24)],10,loc=(x,.05,z),color=C[col]);body.scale=(k,k,k);parts.append(body)
  # Stagger ring edges to make genuine triangular origami facets instead of lathe strips.
  for v in body.data.vertices:
   if abs(v.co.z-.42)<.001 or abs(v.co.z-1.05)<.001:
    u,w=v.co.x,v.co.y;v.co.x=u*math.cos(.055)-w*math.sin(.055);v.co.y=u*math.sin(.055)+w*math.cos(.055)
  bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free();P.paint(body,C[col])
  # A broad creased cream chest follows the torso taper and meets the muzzle.
  outline=[(-.10,1.24),(.10,1.24),(.20,.98),(.29,.53),(.22,.22),(0,.10),(-.22,.22),(-.29,.53),(-.20,.98)]
  vs=[(x+a*k,-(.31 if b>.8 else .41)*k,z+b*k) for a,b in outline]+[(x,-.52*k,z+.51*k)]
  parts.append(mesh('folded_cream_belly',vs,[(j,(j+1)%9,9) for j in range(9)],'cream'))
  head=ico('angular_head',(x,-.005,z+1.51*k),(.51,.46,.46))
  # Colour the head's lower face itself cream; an attached faceted muzzle supplies the folded cheeks.
  P.paint(head,lambda center,normal:C['cream'] if center.z<-.08*k and center.y<-.09*k else C[col])
  ico('cream_muzzle',(x,-.395*k,z+1.36*k),(.40,.16,.205),'cream')
  for sx in [-1,1]:
   ico('paper_foot',(x+sx*.245*k,-.15*k,z+.05*k),(.20,.25,.12),'cream',1)
   ico('eye',(x+sx*.205*k,-.445*k,z+1.53*k),(.043,.025,.059),'sky' if col=='lavender' else 'lavender',1)
   arm=ico('waving_arm' if sx==wave else 'lowered_arm',(x+sx*.50*k,-.04,z+(1.02 if sx==wave else .68)*k),(.16,.18,.29),col,2)
   arm.rotation_euler.y=math.radians(sx*(-24 if sx==wave else 13))
   ico('cream_hand',(x+sx*.59*k,-.13*k,z+(1.23 if sx==wave else .46)*k),(.12,.13,.14),'cream',1)
   # Thick seven-plane ears, with a recessed blush insert and a true front crease.
   outline=[(-.10,0),(-.23,.31),(-.24,.61),(-.04,.81),(.18,.62),(.19,.25),(.08,0)]
   lean=sx*.16;ex=x+sx*.22*k;ez=z+1.83*k
   front=[(ex+(a+lean*b/.81)*k,-.09*k+.24*b*k,ez+b*k) for a,b in outline]
   back=[(a,b+.34*k*max(.18,max(0,math.sin(math.pi*(c-ez)/(.81*k)))**.5),c) for a,b,c in front]
   inner=[(ex+(a*.61+lean*(.08+b*.76)/.81)*k,-.11*k+.24*(.08+b*.76)*k,ez+(.08+b*.76)*k) for a,b in outline]
   vs=front+inner+[(ex+lean*.47*k,-.20*k,ez+.41*k)]+back;fs=[]
   for j in range(7):fs.append((j,(j+1)%7,(j+1)%7+7,j+7))
   for j in range(7):fs.append((14,j+7,(j+1)%7+7))
   for j in range(7):fs.append((j,15+j,15+(j+1)%7,(j+1)%7))
   fs.append(tuple(range(15,22)));o=mesh('creased_thick_ear',vs,fs,col);P.paint(o,C['cream'],faces=set(range(7)));P.paint(o,C['blush'],faces=set(range(7,14)));es.append(o)
  ico('gem_nose',(x,-.57*k,z+1.43*k),(.050,.027,.034),'blush',1)
  parts.append(P.pivot('ears'+str(i),(x,0,z+1.83*k),es));bobs.append(P.pivot('bob'+str(i),(x,0,z),parts))
 # The bunnies occupy a compact front-to-back row, with a generous oval page margin.
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH' and o not in static:
   o.location.y*=.84
   for v in o.data.vertices:v.co.y*=.84
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
