"""H01 Pop-up Castle; size 15 x 11 x 18 m, budget 6000 triangles.
Pivots: root at book fold; tower0..4 at bases; flag0..4 nested at pole tops.
SIMPLIFICATIONS: luminous windows use lamp-coloured inset meshes, page engraving is
layered geometry, tiny masonry joints omitted; pennants have fixed sculpted waves.
"""
import bpy,math
BUDGET=6000

def build(P,spec):
    c=spec['colors'];K=c['cream'];B=c['blush'];L=c['lavender'];G=c['gold'];Y=c['lamp'];R=c['pink'];static=[]
    static.append(P.prism('book_cover',[(-7.5,.18),(-.70,.18),(-.40,0),(.40,0),(.70,.18),(7.5,.18),(7.5,.36),(.70,.36),(.40,.18),(-.40,.18),(-.70,.36),(-7.5,.36)],11,color=R))
    # Layered paper edges with a folded centre and a shallow cambered page surface.
    for s in (-1,1):
        for k in range(7):
            z=.16+k*.11
            pts=[(s*.02,z-.04),(s*3.5,z+.30),(s*7.23,z+.05),(s*7.23,z+.125),(s*3.5,z+.375),(s*.02,z+.035)]
            static.append(P.prism('paper_leaf',pts[::s],10.25,color=K))
        for y in (-5.28,5.28):static.append(P.box('gold_book_corner',(.63,.42,.16),loc=(s*7.15,y,.03),color=G))
        static.append(P.prism('gold_foreedge',[(s*7.17,.18),(s*7.36,.18),(s*7.36,.75),(s*7.17,.75)][::s],10.20,color=G))
    for side in [-1,1]:
        for k in range(3):
            z=.24+k*.20
            line=[(side*.02,z),(side*3.5,z+.34),(side*7.23,z+.09),(side*7.23,z+.115),(side*3.5,z+.365),(side*.02,z+.025)]
            for y in [-5.14,5.14]:static.append(P.prism('bound_page_crease',line[::side],.018,loc=(0,y,0),color=G))
    page=1.10
    def arch(w,h):
        return [(-w/2,0),(w/2,0),(w/2,h*.64),(w*.43,h*.82),(w*.25,h*.95),(0,h),(-w*.25,h*.95),(-w*.43,h*.82),(-w/2,h*.64)]
    def window(x,y,z,w,h,rot=0):
        return [P.prism('window_gold_arch',arch(w,h),.065,loc=(x,y,z),rot=(0,0,rot),color=G),P.prism('warm_window',arch(w*.67,h*.83),.075,loc=(x,y-.032,z+.07),rot=(0,0,rot),color=Y)]
    def diamond(x,y,z,w=.22,h=.45):return P.prism('gold_lozenge',[(0,0),(w/2,h/2),(0,h),(-w/2,h/2)],.06,loc=(x,y,z),color=G)
    def waving_flag(i,x,y,z,sz):
        # The flag is a solid waving pennant fixed along the pole, its free edge is a heart point.
        outline=[(0,0),(0,.61),(.27,.78),(.63,.58),(.99,.84),(1.30,.78),(1.42,.60),(1.35,.37),(.71,-.04),(.30,.17)]
        verts=[]
        for dy in (-.025,.025):
            verts += [(x+a*sz,y+a*sz+math.sin(a*5.2)*.14*sz+dy,z+b*sz) for a,b in outline]
        n=len(outline);faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
        me=bpy.data.meshes.new('waving_pennant');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new('heart_pennant',me);bpy.context.collection.objects.link(ob);P.paint(ob,R)
        return P.pivot('flag'+str(i),(x,y,z+.61*sz),[ob])
    def tower(i,x,y,r,top,roof):
        parts=[];n=8
        profile=[(r*1.17,page),(r*1.17,page+.25),(r*1.02,page+1.0),(r,top-.24),(r*1.18,top-.10),(r*1.18,top+.25),(r*1.18,top+.29),(r*1.18,top+.40)]
        parts.append(P.lathe('tower_paper_shaft',profile,n,loc=(x,y,0),color=K))
        for z,h,rr in [(page,.16,r*1.19),(top+.08,.12,r*1.18),(top+.39,.11,r*1.18)]:parts.append(P.cyl('gold_tower_moulding',rr,h,8,loc=(x,y,z),color=G))
        # Broad blush vertical panels alternate with cream structural ribs.
        for a in range(8):
            ang=2*math.pi*a/8
            parts.append(P.box('pink_vertical_panel',(.40,.055,top-page-1.12),loc=(x+math.sin(ang)*r*.987,y-math.cos(ang)*r*.987,page+.9),rot=(0,0,math.degrees(ang)),color=B))
            parts.append(P.box('crenellation',(.30,.27,.30),loc=(x+math.sin(ang)*r*1.10,y-math.cos(ang)*r*1.10,top+.42),rot=(0,0,math.degrees(ang)),color=K))
            parts.append(P.prism('folded_buttress',[(0,0),(.37,0),(.12,.90)],.40,loc=(x+math.sin(ang)*r*.96,y-math.cos(ang)*r*.96,page),rot=(0,0,math.degrees(ang)+90),color=K))
        parts.append(P.cyl('lavender_roof',r*1.08,roof,8,loc=(x,y,top+.50),r2=.10,color=L))
        # Seam folds give the cone a deliberate papercraft construction.
        parts.append(P.cyl('roof_gold_cap',.23,.44,8,loc=(x,y,top+.50+roof-.04),r2=.07,color=G))
        apex=top+.50+roof+.35
        parts.append(P.cyl('flagpole',.055,1.03,8,loc=(x,y,apex),color=G));parts.append(P.ico('pole_ball',.12,loc=(x,y,apex+1.04),subdiv=1,color=G))
        for ang in [0,math.pi/2]:
            wx=x+math.sin(ang)*r*.99;wy=y-math.cos(ang)*r*.99
            for ob in window(wx,wy,top-(2.45 if top>8 else 2.80),.56,1.85 if top>8 else 1.60,math.degrees(ang)):parts.append(ob)
        if i in (0,3,4):
            z=top-3.65 if i==0 else page+(top-page)*.13
            parts.append(P.prism('heart_banner',[(-.37,0),(0,-.22),(.37,0),(.37,2.30),(-.37,2.30)],.06,loc=(x+r*.40,y-r*.97,z),color=R))
            parts.append(P.prism('banner_heart',P.heart(.26,12),.04,loc=(x+r*.40,y-r-.03,z+1.30),color=K))
        flag=waving_flag(i,x+.04,y,apex+.35,.93 if i==0 else .79)
        return P.pivot('tower'+str(i),(x,y,page),parts+[flag])
    # Connecting walls remain visible between the five distinct towers.
    for s in (-1,1):
        static.append(P.box('curtain_wall',(3.6,.70,8.7),loc=(s*2.75,1.1,page),color=B))
        static.append(P.box('side_wall',(.66,3.1,4.8),loc=(s*4.40,-.10,page),color=B))
        static.append(P.box('gate_pillar',(.64,1.24,5.50),loc=(s*1.72,-2.0,page+.78),color=K))
        static.append(P.box('gold_pillar_foot',(.78,1.37,.20),loc=(s*1.72,-2.0,page+.78),color=G))
        static.append(P.box('gate_cap',(.83,1.40,.20),loc=(s*1.72,-2.0,page+6.13),color=G))
        static.append(diamond(s*1.72,-2.64,page+5.20,.24,.58))
        for k in range(4):static.append(P.box('wall_merlon',(.34,.75,.49),loc=(s*(1.3+k*.85),1.1,page+8.7),color=K))
    for x in (-2.75,2.75):static.append(diamond(x,.70,page+6.65,.33,.65))
    for x in (-.85,0,.85):static.append(P.box('gate_merlon',(.38,1.15,.35),loc=(x,-1.90,page+5.88),color=K))
    static.append(P.box('inner_hall',(6.3,3.8,5.65),loc=(0,.25,page),color=B))
    static.append(P.box('cream_hall_deck',(6.20,3.70,.045),loc=(0,.25,page+5.65),color=K))
    # The arched entry is outlined by gold and cream paper laminations.
    static.append(P.prism('gable_wall',[(-1.58,0),(1.58,0),(1.58,4.1),(0,5.50),(-1.58,4.1)],1.1,loc=(0,-1.90,page+.78),color=K))
    static.append(P.prism('gable_gold',[(-1.96,4.06),(0,5.66),(1.96,4.06),(1.91,3.93),(0,5.48),(-1.91,3.93)],.10,loc=(0,-2.54,page+.78),color=G))
    static.append(P.prism('arched_door_frame',arch(2.50,3.66),.10,loc=(0,-2.49,page+1.08),color=G))
    static.append(P.prism('lamp_door',arch(2.12,3.37),.08,loc=(0,-2.57,page+1.11),color=Y))
    static.append(P.box('door_central_stile',(.07,.08,2.95),loc=(0,-2.64,page+1.11),color=G))
    for side in [-1,1]:
        static.append(P.prism('door_branch',[(0,0),(side*.77,.91),(side*.71,.97),(0,.15)],.035,loc=(0,-2.68,page+3.34),color=G))
    static.append(P.prism('gate_heart',P.heart(.27,12),.08,loc=(0,-2.65,page+5.30),color=R))
    for k in range(6):
        static.append(P.box('stair',(3.30,2.75-k*.39,.22*(k+1)),loc=(0,-3.45+k*.195,page-.04),color=K))
        static.append(P.box('stair_gold_nosing',(3.32,.045,.045),loc=(0,-4.84+k*.39,page+.22*(k+1)-.06),color=G))
    for s in (-1,1):
        for y in (-4.37,-2.47):
            static.extend([P.box('stair_post',(.46,.48,1.42),loc=(s*1.88,y,.75),color=K),P.box('stair_post_trim',(.53,.55,.13),loc=(s*1.88,y,2.10),color=G),P.cyl('post_gold_finial',.27,.38,4,loc=(s*1.88,y,2.23),r2=0,color=G)])
            static.append(P.prism('post_pink_panel',[(-.15,0),(.15,0),(.15,.53),(-.15,.53)],.04,loc=(s*1.88,y-.26,.93),color=R))
    for side in (-1,1):
        static.append(P.prism('outer_fold_tab',[(side*5.90,page),(side*7.10,.28),(side*5.90,3.25)][::side],1.3,loc=(0,.6,0),color=K))
        for y,sg in [(-3.25,-1),(3.30,1)]:
            static.append(P.prism('depth_fold_tab',[(0,page),(sg*1.45,page),(0,2.65)],.45,loc=(side*4.7,y,0),rot=(0,0,90),color=K))
    towers=[tower(0,0,1.80,1.47,12.45,3.02),tower(1,-4.16,1.72,1.35,10.12,2.52),tower(2,4.16,1.72,1.35,10.12,2.52),tower(3,-4.70,-2.05,1.27,6.32,2.12),tower(4,4.70,-2.05,1.27,6.32,2.12)]
    root=P.pivot('root',(0,0,0),static+towers)
    bpy.context.view_layer.update();v=[o.matrix_world@v.co for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices];ext=[max(p[i] for p in v)-min(p[i] for p in v) for i in range(3)];s=spec['size_m'];root.scale=(s['w']/ext[0],s['d']*.975/ext[1],s['h']/ext[2]);bpy.context.view_layer.update()
