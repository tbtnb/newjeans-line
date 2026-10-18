"""G3_sky_small_anim / hanging paper star. Largest extent 0.8 m; budget 40 tris.
Pivots: root at (0,0,0), kit static group only.
SIMPLIFICATIONS: Gold/cream double-sided folded star, open hexagonal attachment eye, triangular string; circular loop approximated.
"""
BUDGET = 40
SIZE = 0.8

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

    outline=P.star(.34,.195);low=min(z for x,z in outline)
    outline=[(x,z-low) for x,z in outline]
    relief('gold_folded_star',outline,.11,['#F7D98B','#FFF3DE'])
    z=max(z for x,z in outline)
    stem('gold_string',(0,0,z+.07),(0,0,z+.36),.005,'#F7D98B',3)
    vv=[]
    for r in [.034,.020]:
        for i in range(6):
            a=2*math.pi*i/6;vv.append((r*math.cos(a),0,z+.035+r*math.sin(a)))
    mesh('hexagonal_attachment_eye',vv,[(i,(i+1)%6,6+(i+1)%6,6+i) for i in range(6)],'#F7D98B')

    finish()
