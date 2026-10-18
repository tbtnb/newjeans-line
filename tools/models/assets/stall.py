"""P20 Carnival candy stall. Size 2.6 x 1.5 x 3.2 m from spec; 1500 tris; root, heart.
SIMPLIFICATIONS: jar glass represented by cyan paper with candy facets; six lights use fixed palette colours; rear scalloped hem and text omitted; front/side design masks fill the open counter void."""
BUDGET = 1500

import math
import bpy
import bmesh
from mathutils import Vector, Matrix

def mesh(P, name, verts, faces, color):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free(); me.update()
    ob=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(ob); P.paint(ob,color)
    return ob

def rod(P,name,a,b,r,color,n=6):
    a,b=Vector(a),Vector(b); ob=P.cyl(name,r,(b-a).length,n,loc=a,color=color)
    ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return ob

def finish(P,spec,animated=()):
    bpy.context.view_layer.update()
    obs=[o for o in bpy.context.scene.objects if o.type=='MESH']
    pts=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
    lo=Vector(tuple(min(p[i] for p in pts) for i in range(3))); hi=Vector(tuple(max(p[i] for p in pts) for i in range(3)))
    size=spec['size_m']; target=Vector((size['w'],size['d'],size['h'])) if isinstance(size,dict) else (hi-lo)*(size/max(hi-lo))
    factors=Vector(tuple(target[i]/(hi[i]-lo[i]) for i in range(3)))
    center=Vector(((hi.x+lo.x)/2,(hi.y+lo.y)/2,lo.z))
    def point(v): return Vector(tuple((v[i]-center[i])*factors[i] for i in range(3)))
    for ob in obs:
        mw=ob.matrix_world.copy()
        for v in ob.data.vertices: v.co=point(mw@v.co)
        ob.matrix_world=Matrix.Identity(4)
    moving=set(); roots=[]
    for name,joint,children in animated:
        roots.append(P.pivot(name,point(Vector(joint)),children)); moving.update(children)
    P.pivot('root',(0,0,0),[o for o in obs if o not in moving]+roots)

def build(P, spec):
    c=spec['colors']; gold=c['gold']; cream=c['cream']; pink=c['magenta']; cyan=c['cyan']; sign=[]
    P.box('gold plinth',(2.44,1.30,.09),loc=(0,0,0),color=gold)
    P.box('cream cabinet',(2.33,1.20,.62),loc=(0,0,.09),color=cream)
    P.box('counter gold edge',(2.52,1.40,.055),loc=(0,0,.71),color=gold)
    P.box('counter cream slab',(2.55,1.43,.055),loc=(0,0,.765),color=cream)
    for x in [-.61,.61]:
        P.prism('gold raised cabinet frame',[(-.48,.10),(.48,.10),(.48,.56),(.40,.63),(-.40,.63),(-.48,.56)],.02,loc=(x,-.607,.09),color=gold)
        P.prism('magenta cabinet inset',[(-.41,.14),(.41,.14),(.41,.52),(.34,.56),(-.34,.56),(-.41,.52)],.025,loc=(x,-.625,.09),color=pink)
        P.prism('cabinet diamond',[(0,.27),(.07,.34),(0,.41),(-.07,.34)],.025,loc=(x,-.646,.09),color=gold)
    for x in [-1.11,1.11]:
        for y in [-.53,.53]:
            P.box('cream corner post',(.095,.095,2.37),loc=(x,y,.12),color=cream)
            for z in [.12,2.53]:P.box('gold post collar',(.135,.135,.045),loc=(x,y,z),color=gold)
            P.cyl('post spear',.083,.14,4,loc=(x,y,2.575),r2=0,color=gold)
    # Seven striped roof strips, pitched back and front; rounded scalloped valance.
    for j in range(7):
        x=-1.30+j*2.6/7;ww=2.6/7;co=pink if j%2==0 else cream
        for s in [-1,1]:
            roof=mesh(P,'striped pitched awning',[(x*.78,0,2.59),((x+ww)*.78,0,2.59),(x+ww,s*.75,2.14),(x,s*.75,2.14)],[(0,1,2,3)],co)
            contour=[(-ww/2,0),(ww/2,0),(ww*.40,-.14),(0,-.19),(-ww*.40,-.14)]
            if s==-1: P.prism('scalloped paper valance',contour,.025,loc=(x+ww/2,s*.75,2.15),color=co)
        rod(P,'gold roof seam',(x,0,2.60),(x,-.75,2.15),.012,gold,4)
    for y in [-.75,.75]:rod(P,'gold awning hem',(-1.3,y,2.14),(1.3,y,2.14),.013,gold,4)
    for xx in [-1,1]:
        mesh(P,'cyan gable end',[(xx*1.3,-.75,2.14),(xx*1.3,.75,2.14),(xx*1.014,0,2.59)],[(0,1,2)],cyan)
    for x in [-1.3,1.3]:
        rod(P,'gold roof rake',(x,-.75,2.14),(x,0,2.60),.018,gold,4);rod(P,'gold roof rake',(x,0,2.60),(x,.75,2.14),.018,gold,4)
    for i,x in enumerate([-.92,-.56,-.18,.22,.60,.95]):
        rod(P,'light string',(x,-.65,2.04),(x,-.65,1.93-(i%2)*.08),.008,gold,4)
        P.ico('carnival bulb',.065,loc=(x,-.65,1.88-(i%2)*.08),subdiv=1,scale=(.8,.8,1.15),color=pink if i%2 else gold)
    for i,(x,r,h) in enumerate([(-.87,.13,.32),(-.47,.11,.25),(-.04,.14,.34),(.43,.12,.29),(.83,.10,.21)]):
        P.lathe('cyan candy jar',[(r,0),(r,h*.80),(r*.8,h)],6,loc=(x,-.13,.82),color=cyan)
        P.cyl('gold jar lid',r*1.04,.025,6,loc=(x,-.13,.82+h),color=gold)
        P.cyl('jar knob',.025,.025,4,loc=(x,-.13,.85+h),r2=0,color=gold)
        for j in range(2):P.card('paper candy',P.ellipse(r*.28,r*.30,5),loc=(x+(j-1)*r*.50,-.13-r,.89+(j%2)*h*.30),color=pink if j%2 else cream)
    outline=P.heart(.50,14);sign.append(P.prism('gold heart sign frame',outline,.10,loc=(0,-.14,2.58),color=gold))
    sign.append(P.prism('magenta heart sign',P.heart(.44,14),.115,loc=(0,-.16,2.61),color=pink))

    P.prism('hanging counter pennant',[(-.28,.82),(.28,.82),(0,.53)],.025,loc=(0,-.77,0),color=gold)
    P.prism('counter pennant inset',[(-.22,.79),(.22,.79),(0,.57)],.028,loc=(0,-.785,0),color=pink)
    finish(P,spec,[('heart',(0,-.14,2.86),sign)])
