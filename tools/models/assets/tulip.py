"""G1_ground_plants / single tulip. Largest extent 0.4 m; budget 90 tris.
Pivots: root at (0,0,0), kit static group only.
SIMPLIFICATIONS: Five open cupped petals have actual closed rims and inner pink faces; tiny calyx folds omitted; top drawing is oblique.
"""
BUDGET = 90
SIZE = 0.4

import math
import bpy
from mathutils import Vector

def build(P, spec):
    S = float(spec.get('size_m', SIZE))
    objects=[]
    deform=None
    def mesh(name, vertices, faces, colors):
        me=bpy.data.meshes.new(name)
        me.from_pydata(vertices, [], faces); me.update()
        ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob)
        P.paint(ob, colors[0] if isinstance(colors,list) else colors)
        if isinstance(colors,list):
            for i in range(len(faces)): P.paint(ob,colors[i%len(colors)],faces={i})
        objects.append(ob); return ob
    def add(ob): objects.append(ob); return ob
    def relief(name, outline, depth, colors, center=None, back=True):
        # Raised fold apex, actual triangular paper facets; outline in XZ.
        n=len(outline); center=center or (sum(x for x,z in outline)/n,sum(z for x,z in outline)/n)
        vv=[(x,0,z) for x,z in outline]+[(center[0],-depth,center[1])]
        ff=[(i,(i+1)%n,n) for i in range(n)]
        if back:
            vv.append((center[0],depth*.35,center[1])); ff += [(i,n+1,(i+1)%n) for i in range(n)]
        return mesh(name,vv,ff,colors)
    def leaf(name,a,b,width,colors,fold=.035):
        a,b=Vector(a),Vector(b); axis=b-a
        lateral=Vector((axis.z,0,-axis.x)).normalized()*width/2
        mid=a+axis*.55; ridge=mid+Vector((0,-fold,0))
        return mesh(name,[a,mid-lateral,b,mid+lateral,ridge],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],colors)
    def stem(name,a,b,r=.014,color='#BDEBD8',segs=4):
        a,b=Vector(a),Vector(b); ob=add(P.cyl(name,r,(b-a).length,segs,loc=a,color=color))
        ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return ob
    def rooted_leaf(name,x,y,tx,ty,h,w,colors):
        # Broad grounded base, pointed blade, continuous fold ridge.
        a=Vector((x-w*.5,y,0)); b=Vector((x+w*.5,y,0)); tip=Vector((tx,ty,h))
        m=Vector(((x+tx)/2,(y+ty)/2-.045,h*.57))
        l=Vector(((x+tx)/2-w*.65,(y+ty)/2,h*.57))
        r=Vector(((x+tx)/2+w*.65,(y+ty)/2,h*.57))
        return mesh(name,[a,b,l,r,tip,m],[(0,1,5),(0,5,2),(2,5,4),(4,5,3),(3,5,1) ],colors)
    def finish():
        bpy.context.view_layer.update()
        if deform:
            for ob in objects:
                mw=ob.matrix_world.copy()
                for v in ob.data.vertices: v.co=deform(mw@v.co,ob.name)
                ob.matrix_world.identity()
            bpy.context.view_layer.update()
        pts=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
        lo=Vector(tuple(min(v[k] for v in pts) for k in range(3)))
        hi=Vector(tuple(max(v[k] for v in pts) for k in range(3)))
        k=S/max(hi-lo); offset=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
        for ob in objects:
            mw=ob.matrix_world.copy()
            for v in ob.data.vertices: v.co=(mw@v.co-offset)*k
            ob.matrix_world.identity()
        P.pivot('root',(0,0,0),objects)

    stem('stem',(0,0,0),(0,0,.56),.025)
    leaf('left_leaf',(0,0,0),(-.31,.16,.41),.20,'#BDEBD8',.06)
    leaf('right_leaf',(0,0,0),(.34,-.16,.42),.20,'#BDEBD8',.06)
    n=5; vv=[]
    for r,z,phase in [(.0,.46,0),(.24,.67,0),(.22,.84,0)]:
        if r==0: vv.append((0,0,z));continue
        for i in range(n):
            a=-math.pi/2+i*2*math.pi/n; vv.append((r*math.cos(a),r*math.sin(a),z))
    for i in range(n):
        a=-math.pi/2+(i+.5)*2*math.pi/n; vv.append((.25*math.cos(a),.25*math.sin(a),1))
    ff=[]
    for i in range(n):
        j=(i+1)%n
        ff += [(0,1+i,1+j),(1+i,6+i,6+j),(1+i,6+j,1+j),(6+i,11+i,6+j)]
    mesh('open_five_lobed_cup',vv,ff,['#FF6FAE','#FFC7DA'])
    # Petal interior, folded bottom and pointed lips.
    inner=[(x*.88,y*.88,z-.015) for x,y,z in vv]
    mesh('petal_inner',inner,[tuple(reversed(f)) for f in ff], '#FFC7DA')
    m=len(vv);rim=[]
    for i in range(n):
        j=(i+1)%n
        rim.extend([(6+i,11+i,m+11+i,m+6+i),(11+i,6+j,m+6+j,m+11+i)])
    mesh('folded_petal_rim',vv+inner,rim,'#FFC7DA')

    finish()
