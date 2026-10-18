"""H15 Bunny-Sail Paper Boat; size 3 x 1.1 x 3 m; budget 1500.
Pivots root, bob0. SIMPLIFICATIONS: lantern glow is lamp colour; hull paper is solid folded panels; reference side sail height differs from front/hero; shared cream #FFF3DE, pink #FF6FAE and darkest plum #2A1640 supplement the cool sail palette for the requested face and ear inserts."""
BUDGET=1500

import math
import bpy, bmesh
from mathutils import Vector, Matrix

def mesh(P,name,verts,faces,color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob); P.paint(ob,color); return ob

def bevel(P,name,size,loc,color,amount=.06):
    ob=P.box(name,size,loc=loc,color=color)
    m=ob.modifiers.new('paper chamfers','BEVEL');m.width=amount;m.segments=1
    bpy.context.view_layer.objects.active=ob;ob.select_set(True);bpy.ops.object.modifier_apply(modifier=m.name);P.paint(ob,color);ob.select_set(False);return ob

def rod(P,name,a,b,r,color,n=8):
    d=Vector(b)-Vector(a);o=P.cyl(name,r,d.length,n,loc=a,color=color);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return o

def ear(P,name,x,y,z,w,h,color,inner,lean=0):
    outline=[(-.30*w,0),(-.58*w,.48*h),(-.48*w,.92*h),(-.12*w,h),(.46*w,.77*h),(.50*w,.48*h),(.28*w,0)]
    def point(u,v,k=1):return (x+u+lean*v/h,y+.28*v/h-.18*w,z+v)
    outer=[point(u,v) for u,v in outline]
    inset=[(a+.0,b-.055*w,c) for a,b,c in [point(u*.62,.13*h+v*.72) for u,v in outline]]
    center=(x+lean*.49,y+.28*.49-.42*w,z+.49*h)
    back=[(a,b+.7*w,c) for a,b,c in outer]
    vs=outer+inset+[center]+back;fs=[]
    for i in range(7):fs.append((i,(i+1)%7,(i+1)%7+7,i+7))
    for i in range(7):fs.append((14,7+i,7+(i+1)%7))
    for i in range(7):fs.append((i,15+i,15+(i+1)%7,(i+1)%7))
    fs.append(tuple(range(15,22)))
    ob=mesh(P,name,vs,fs,color);P.paint(ob,inner,faces=set(range(7,14)));return [ob]

def arch(P,name,x,y,z,w,h,depth,color,rot=0):
    out=[(-w/2,0),(w/2,0),(w/2,h*.72),(w*.31,h*.88),(0,h),(-w*.31,h*.88),(-w/2,h*.72)]
    return P.prism(name,out,depth,loc=(x,y,z),color=color,rot=(0,0,rot))

def finish(P,spec,roots):
    bpy.context.view_layer.update(); obs=list(bpy.context.scene.objects); ms=[o for o in obs if o.type=='MESH']
    worlds={o:o.matrix_world.copy() for o in obs}; parents={o:o.parent for o in obs}
    pts=[worlds[o]@v.co for o in ms for v in o.data.vertices]
    lo=Vector(tuple(min(p[i] for p in pts) for i in range(3))); hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
    sz=spec['size_m'];sc=Vector((sz['w']/(hi.x-lo.x),sz['d']/(hi.y-lo.y),sz['h']/(hi.z-lo.z)))
    S=Matrix.Diagonal((sc.x,sc.y,sc.z,1));T=Matrix.Translation((-(hi.x+lo.x)/2,-(hi.y+lo.y)/2,-lo.z));M=S@T
    for o in obs:o.parent=None;o.matrix_world=Matrix.Identity(4)
    for o in obs:
        if o.type=='MESH':
            o.data.transform(M@worlds[o]);o.data.update()
            bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
            # Open paper surfaces need an explicit visible side; closed shells use outward normals.
            if bm.faces and not all(e.is_manifold for e in bm.edges):
                avg=sum((f.normal*f.calc_area() for f in bm.faces),Vector((0,0,0)))
                cen=sum((v.co for v in bm.verts),Vector((0,0,0)))/len(bm.verts)
                name=o.name.lower();flip=False
                if any(k in name for k in ('canopy folded','floor paper')):flip=avg.z<0
                elif any(k in name for k in ('faceted heart','creased cream sail','folded peach flower')):flip=avg.y>0
                elif any(k in name for k in ('folded hull facet','scalloped gold trim','scalloped lilac valance')):flip=avg.x*cen.x+avg.y*cen.y<0
                elif 'hull interior' in name:flip=avg.z<0
                if flip:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
            bm.to_mesh(o.data);bm.free();o.data.update()
        else:o.location=M@worlds[o].translation
    bpy.context.view_layer.update()
    for o in obs:
        if parents[o]:
            mw=o.matrix_world.copy();o.parent=parents[o];o.matrix_parent_inverse=parents[o].matrix_world.inverted();o.matrix_world=mw
    P.pivot('root',(0,0,0),roots)

def face_patch(P, head, name, outline, color, offset=.012, forward=(0,-1,0)):
    """Printed low-triangle mark, clipped to the head planes and lifted along their normals."""
    import bpy
    from mathutils import Vector
    import bmesh
    bm=bmesh.new();bm.from_mesh(head.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(head.data);bm.free();head.data.update()
    bpy.context.view_layer.update()
    front=Vector(forward);right=Vector((-front.y,front.x,0));up=Vector((0,0,1))
    def uv(p):return (p.dot(right),p.z)
    def clip(poly,a,b):
        result=[]
        for p,q in zip(poly,poly[1:]+poly[:1]):
            u,v=uv(p),uv(q)
            dp=(b[0]-a[0])*(u[1]-a[1])-(b[1]-a[1])*(u[0]-a[0])
            dq=(b[0]-a[0])*(v[1]-a[1])-(b[1]-a[1])*(v[0]-a[0])
            if dp>=-1e-9:result.append(p)
            if (dp>=0)!=(dq>=0):result.append(p+(q-p)*(dp/(dp-dq)))
        return result
    if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(outline,outline[1:]+outline[:1]))<0:outline=outline[::-1]
    mw=head.matrix_world;nm=mw.to_3x3().inverted().transposed();vs=[];fs=[]
    head.data.calc_loop_triangles()
    for tri in head.data.loop_triangles:
        normal=(nm@tri.normal).normalized()
        if normal.dot(front)<.05:continue
        poly=[mw@head.data.vertices[i].co for i in tri.vertices]
        for a,b in zip(outline,outline[1:]+outline[:1]):
            poly=clip(poly,a,b)
            if len(poly)<3:break
        if len(poly)<3:continue
        for j in range(1,len(poly)-1):
            if (poly[j]-poly[0]).cross(poly[j+1]-poly[0]).length<1e-10:continue
            k=len(vs);vs.extend([tuple(p+normal*offset) for p in (poly[0],poly[j],poly[j+1])]);fs.append((k,k+1,k+2))
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);P.paint(ob,color)
    return ob

def face_oval(x,z,rx,rz):
    # Six corners keep the little eyes flat and faceted.
    return [(x+rx*math.cos(i*math.tau/6),z+rz*math.sin(i*math.tau/6)) for i in range(6)]

def build(P,spec):
 c=spec['colors'];W,L,M,G,A=[c[k] for k in ('pearl','lilac','moon','gold','lamp')];a=[]
 # Front vertices follow the actual cut-paper pattern, not a rounded bunny icon.
 def xyz(px,py,y=0):return ((px-311)/207.33,y,(603-py)/201)
 def paper(name,outline,frontpoints,faces,depths,colours):
  n=len(outline);vs=[xyz(x,z,0) for x,z in outline]
  vs += [xyz(x,z,y) for x,z,y in frontpoints]
  # A shallow rear ridge gives the edge-on folded-paper profile.
  back=len(vs);vs += [xyz(x,z,depths) for x,z in outline]
  center=len(vs);vs.append(xyz(sum(x for x,z in outline)/n,sum(z for x,z in outline)/n,depths+.045))
  fs=list(faces)+[(center,back+i,back+(i+1)%n) for i in range(n)]+[(i,(i+1)%n,back+(i+1)%n,back+i) for i in range(n)]
  ob=mesh(P,name,vs,fs,W)
  for col,inds in colours:P.paint(ob,col,faces=set(inds))
  a.append(ob)
  return ob
 # Irregular broad head with a sharply projecting central crease.
 out=[(190,225),(280,198),(316,187),(406,226),(453,305),(427,382),(361,415),(267,418),(184,386),(153,305)]
 pts=[(245,239,-.12),(350,300,-.24),(422,331,-.075),(222,339,-.09)]
 fs=[(0,1,10),(1,2,11),(1,11,10),(2,3,11),(3,4,12),(3,12,11),(4,5,12),(5,6,11),(5,11,12),(6,7,11),(7,13,11),(7,8,13),(8,9,13),(9,0,10),(9,10,13),(10,11,13)]
 head=paper('creased cream sail head',out,pts,fs,.12,[(M,[1,4,6,9,13]),(L,[11])])
 # Preserve the folded sail silhouette; tiny printed marks follow its broad front planes.
 P.paint(head,'#FFF3DE',faces=set(range(len(fs)))-{1,4,6,9,11,13})
 for sign in (-1,1):
  a.append(face_patch(P,head,'printed_sail_eye',face_oval(sign*.31,1.59,.026,.041),'#2A1640'))
 a.append(face_patch(P,head,'printed_sail_nose',[(-.055,1.43),(0,1.38),(.055,1.43)],'#FF6FAE'))
 # Large asymmetrical ears with angular edges, broad inner panels, and a real ridge.
 for name,out,pts,fs,blue in [
 ('left',[(245,239),(190,225),(116,124),(142,15),(237,70),(282,198)],[(165,118,-.12),(219,96,-.12),(206,190,-.10)],[(0,1,8),(1,2,6),(1,6,8),(2,3,6),(3,7,6),(3,4,7),(4,5,7),(5,0,7),(0,8,6),(0,6,7)],8),
 ('right',[(330,193),(371,73),(456,16),(487,123),(405,228)],[(394,107,-.12),(437,72,-.12),(449,118,-.10)],[(0,1,5),(1,2,6),(1,6,5),(2,3,6),(3,7,6),(3,4,7),(4,0,5),(4,5,7),(5,6,7)],2)]:
  paper('creased cream sail '+name+' ear',out,pts,fs,.14,[('#FF6FAE',[4,8,9] if name=='left' else [7,8]),(M,[blue])])
 # Eight planar hull sides converge to a genuine keel, with the cockpit left open.
 top=[xyz(x,z,y) for x,z,y in [(0,432,0),(145,479,-.35),(295,485,-.55),(422,484,-.35),(621,462,0),(466,455,.35),(311,450,.55),(155,449,.35)]]
 low=[xyz(x,603,y) for x,y in [(106,0),(116,-.045),(298,-.080),(496,-.045),(496,0),(492,.045),(298,.080),(110,.045)]]
 for i in range(8):
  j=(i+1)%8;v=[top[i],top[j],low[j],low[i]];center=tuple(sum(p[k] for p in v)/4 for k in range(3));v.append((center[0],center[1]*1.07,center[2]))
  ob=mesh(P,'folded hull facet',v,[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],W);P.paint(ob,M,faces={2 if i%2 else 3});P.paint(ob,L,faces={1} if i in (0,3,4,7) else set());a.append(ob)
 inner=[(x*.97,y*.92,z-.04) for x,y,z in top];floor=[(x*.65,y*.28,.19) for x,y,z in top]
 for i in range(8):
  j=(i+1)%8;q=[inner[i],inner[j],floor[j],floor[i]];mid=tuple(sum(p[k] for p in q)/4 for k in range(3));q.append((mid[0],mid[1],mid[2]-.04))
  ob=mesh(P,'lilac hull interior',q,[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],L);a.append(ob)
  a.append(rod(P,'gold folded rim',top[i],top[j],.015,G,12))
 a.append(mesh(P,'cockpit floor',floor,[tuple(range(8))],L))
 a.append(P.lathe('gold mast',[(.033,.25),(.033,2.72),(.048,2.72),(.048,2.78),(.03,2.78),(.03,2.9)],12,color=G))
 for z in (.68,2.08,2.73):a.append(P.cyl('mast folded collar',.075,.045,8,loc=(0,0,z),color=G))
 a.append(P.lathe('mast diamond',[(0,2.77),(.10,2.90),(0,3.0)],4,color=G))
 x=1.34;y=0
 for z,r,h,col,r2 in [(.71,.07,.06,G,.07),(.77,.045,.08,G,.045),(.85,.10,.035,G,.10),(.885,.10,.26,A,.15),(1.145,.18,.035,G,.18),(1.18,.18,.12,G,.025)]:
  a.append(P.cyl('bow lantern',r,h,8,loc=(x,y,z),color=col,r2=r2))
 for i in range(4):
  t=math.pi/4+i*math.pi/2;a.append(rod(P,'lantern frame',(x+.10*math.cos(t),.10*math.sin(t),.89),(x+.15*math.cos(t),.15*math.sin(t),1.145),.01,G,6))
 a.append(P.lathe('lantern diamond',[(0,1.29),(.055,1.36),(0,1.43)],4,loc=(x,0,0),color=G))
 b=P.pivot('bob0',(0,0,.4),a);finish(P,spec,[b])
