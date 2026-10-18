"""G1_ground_plants / 5-petal paper flower. Largest extent 0.3 m; budget 80 tris.
Pivots: root at (0,0,0), kit static group only.
SIMPLIFICATIONS: Five seven-facet blush petals, gold center, folded leaves; head tilted in depth; small calyx leaves and painted texture omitted.
"""
BUDGET = 80
SIZE = 0.3

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

    stem('mint_stem',(0,0,0),(0,0,.64),.018)
    leaf('left_paper_leaf',(0,0,0),(-.26,.04,.30),.19,'#BDEBD8',.05)
    leaf('right_paper_leaf',(0,0,0),(.31,.04,.35),.18,'#BDEBD8',.05)
    outlines=[[(608,377),(553,307),(556,262),(614,216),(672,262),(675,307),(640,378)],[(578,388),(481,311),(459,314),(433,359),(451,412),(495,433),(576,421)],[(573,420),(503,443),(476,491),(510,537),(558,540),(591,473),(597,432)],[(620,433),(623,470),(651,535),(698,541),(731,493),(710,448),(648,422)],[(642,381),(689,315),(740,312),(786,359),(768,412),(727,432),(643,417)]]
    for i,pts in enumerate(outlines):
        relief('folded_petal%d'%i,[((x-608)/500,(716-z)/500) for x,z in pts],.055,['#FFC7DA','#FFC7DA','#FFC7DA','#FF6FAE','#FFC7DA','#FFC7DA','#FFC7DA'],back=False)
    add(P.ico('gold_flower_center',.065,loc=(0,-.06,.634),color='#F7D98B',subdiv=1))

    def deform(v,name):
        if 'petal' in name or 'center' in name: v.y += (v.z-.634)*.95
        if 'leaf' in name: v.y += (.12 if 'left' in name else -.12)*(v.z/.35)
        return v

    finish()
