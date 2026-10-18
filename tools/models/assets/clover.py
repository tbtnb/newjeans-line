"""G1_ground_plants / clover patch. Largest extent 0.4 m; budget 60 tris.
Pivots: root at (0,0,0), kit static group only.
SIMPLIFICATIONS: Sheet depicts four leaflets on each clover despite its three-leaf name; three stalks, paper folds, basal foliage; underside and tiny veins omitted.
"""
BUDGET = 60
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

    for j,(x,z,r,tilt) in enumerate([(0,.65,.32,0),(-.26,.34,.22,.15),(.30,.27,.23,-.45)]):
        mesh('stalk%d'%j,[(x*.65-.018,.015,0),(x*.65+.018,.015,0),(x+.018,.015,z),(x-.018,.015,z)],[(0,1,2),(0,2,3)],'#BDEBD8')
        for i in range(4):
            a=math.pi/2+i*2*math.pi/4+tilt+.65
            pts=[]
            for u,v in [(0,0),(.68,-.52),(1,-.21),(.94,.04),(1,.27),(.65,.53)]:
                pts.append((x+r*(u*math.cos(a)-v*math.sin(a)),z+r*(u*math.sin(a)+v*math.cos(a))))
            # Six-sided outline uses four triangles, one actual lifted fold.
            ob=add(P.card('clover_leaf_%d_%d'%(j,i),pts,color='#BDEBD8'))
            for v in ob.data.vertices: v.co.y=.02*abs(v.co.x-x)/max(.01,r)
    for i,(x,h,w) in enumerate([(-.30,.14,.18),(-.10,.24,.20),(.10,.20,.18)]):
        mesh('basal_leaf%d'%i,[(x-w/2,-.01,0),(x-w*.32,-.04,h*.6),(x,-.08,h),(x+w/2,0,0)],[(0,1,2),(0,2,3)],'#BDEBD8')

    def deform(v,name):
        if name.startswith('clover_leaf'):
            j=int(name.split('_')[2]); z=[.65,.34,.27][j]
            v.y += 1.05*(v.z-z)
        return v

    finish()
