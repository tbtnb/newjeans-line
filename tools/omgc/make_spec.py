#!/usr/bin/env python3
"""Generate levels-src/omg/scene-c.json (concept C placement spec) from the design data zones_c.py (branch omg-design-v3).
Everything is relative to the route by time t and side, so it survives re-charts. usage: make_spec.py [path/to/zones_c.py]"""
import json, sys, importlib.util, os, glob
src = sys.argv[1] if len(sys.argv) > 1 else '/workspace/nj-design-v3/levels-design/omg/redesign-v3/C/zones_c.py'
sp = importlib.util.spec_from_file_location('zones_c', src); Z = importlib.util.module_from_spec(sp); sp.loader.exec_module(Z)

# element name (design) -> asset id, placeholder shape, height m. model = glb id when public/models/omg-c/<glb>.glb exists (GLB aliases below).
A = {
 '纸草丛': ('grass', 'tuft', 0.45), '纸草丛(夜)': ('grass', 'tuft', 0.45), '小纸花': ('flower', 'flower', 0.2), '小纸花(夜光)': ('flower', 'flower', 0.2), '小纸花(夜)': ('flower', 'flower', 0.2),
 '爱心小花': ('flower-heart', 'flower', 0.22), '卵石': ('pebble', 'ico', 0.17), '石板': ('slab', 'box', 0.08), '苔石': ('moss-rock', 'ico', 0.2), '岸边纸石': ('rock', 'ico', 0.6),
 '纸蘑菇(小)': ('mushroom', 'mushroom', 0.3), '小纸蘑菇': ('mushroom', 'mushroom', 0.3), '纸格地砖贴片': ('tile-decal', 'card', 0.02), '纸屑': ('confetti-decal', 'card', 0.02),
 '星点纸地贴': ('star-decal', 'card', 0.02), '金箔碎片': ('gold-decal', 'card', 0.02), '纸波纹片': ('ripple-decal', 'card', 0.02), '纸睡莲叶': ('lily-pad', 'card', 0.03),
 '芦苇纸丛': ('reed', 'tuft', 0.9), '纸礼盒': ('gift', 'box', 0.5), '纸礼盒/糖果': ('gift', 'box', 0.5),
 '纸树丛': ('tree-bush', 'tree', 3.2), '纸树': ('tree', 'tree', 4.0), '纸树(夜)': ('tree', 'tree', 4.0), '折纸松树': ('pine', 'tree', 5.0),
 '兔子雕像': ('bunny-statue', 'bunny', 2.2), '纸山片': ('paper-hill', 'card', 4.0), '兔耳小屋': ('bunny-house', 'house', 4.5), '纸蘑菇屋': ('mushroom-house', 'mushroom', 4.0),
 '栅栏段': ('fence', 'box', 0.8), '郁金香花圃': ('tulip-bed', 'bed', 0.8), '立体纸病床': ('ward-bed', 'box', 1.4), '纸帘屏风': ('screen', 'card', 2.2), '心形点滴架': ('iv-heart', 'pole', 2.4),
 '拉片机关': ('pull-tab', 'card', 1.0), '纸灯笼串段': ('lantern-string', 'pole', 3.5), '音符/爱心纸雕': ('heart-sculpt', 'card', 2.2), '礼炮': ('cannon', 'cyl', 1.6),
 '兔子帆纸船': ('paper-boat', 'boat', 2.4), '睡莲灯': ('lily-lamp', 'flower', 0.6), '纸艺翻盖手机': ('flip-phone', 'box', 2.6), '电话线藤蔓拱': ('cord-arch', 'arch', 4.0),
 '爱心花圃': ('heart-bed', 'bed', 0.8), '螺旋纸塔(中)': ('spiral-tower', 'tower', 9.0), '星星风铃': ('star-chime', 'pole', 3.0), '纸楼梯段': ('stairs', 'box', 1.5),
 '纸灯笼塔': ('lantern-tower', 'tower', 6.0), '小摊位': ('stall', 'house', 3.2), '气球束': ('balloons', 'balloons', 4.0), '旗串段': ('bunting', 'pole', 3.0),
 '萤火纸灯': ('firefly-lamp', 'pole', 1.6), '树桩/书堆': ('book-stack', 'box', 1.2), '各章回归道具(实例复用)': ('bunny-house', 'house', 4.5),
 '巨书封面': ('book-cover', 'book', 6.0), '村口风车/钟塔': ('windmill', 'tower', 12.0), '纸时钟塔': ('clock-tower', 'tower', 12.0), '巨型立体城堡': ('castle', 'castle', 16.0),
 '弹出巨兔+爱心': ('bunny-heart', 'bunny', 12.0), '吊线弯月': ('moon', 'moon', 6.0), '湖心纸亭': ('pavilion', 'house', 8.0), '巨型翻盖手机塔': ('phone-tower', 'tower', 14.0),
 '最高纸塔': ('tall-tower', 'tower', 18.0), '兔子旋转木马': ('carousel', 'carousel', 10.0), '爱心摩天轮': ('ferris-wheel', 'wheel', 18.0), '蘑菇下读书兔': ('reading-bunny', 'bunny', 6.0),
 '合拢书页墙': ('page-wall', 'card', 10.0), '书页爱心终点门': ('heart-gate', 'arch', 12.0), '五只兔子一家': ('bunny-family', 'bunny', 3.0), '纸太阳': ('sun', 'moon', 8.0),
 '吊线星星': ('hanging-star', 'star', 1.0), '远山剪影(billboard)': ('far-hills', 'far', 12.0), '远岸剪影(billboard)': ('far-shore', 'far', 8.0), '远林剪影(billboard)': ('far-forest', 'far', 12.0),
 '纸云': ('cloud', 'cloud', 3.0), '纸月亮': ('moon', 'moon', 4.0), '纸星星': ('star', 'star', 1.2), '纸烟花爆点': ('firework', 'star', 4.0), '夕阳纸片': ('sun', 'moon', 8.0),
 '飘落花瓣': ('petal', 'card', 0.1), '花瓣': ('petal', 'card', 0.1), '小鸟': ('bird', 'bird', 0.5), '烟囱纸云': ('puff', 'cloud', 0.8), '蝴蝶': ('butterfly', 'bird', 0.3),
 '拉片翘起': ('pull-tab', 'card', 1.0), '漂浮纸心': ('float-heart', 'card', 0.5), '纸彩带': ('streamer', 'card', 0.3), '飘浮灯笼': ('lantern', 'cyl', 0.6),
 '萤光点': ('glow-dot', 'card', 0.08), '纸鱼跳跃': ('fish', 'bird', 0.5), '书页飞鸟': ('page-bird', 'bird', 0.6), '流星': ('meteor', 'card', 1.0),
 '上升气球': ('balloon', 'ico', 0.8), '萤火虫': ('glow-dot', 'card', 0.08), '飘落叶片': ('leaf', 'card', 0.12), '金色光斑': ('glow-dot', 'card', 0.1),
}
ALIAS = {'巨型弹出兔子+爱心': '弹出巨兔+爱心', '无数字纸时钟': '纸时钟塔', '纸艺翻盖手机雕塑': '纸艺翻盖手机', '翻盖手机②': '纸艺翻盖手机', '兔耳小屋②': '兔耳小屋',
 '兔耳屋顶小屋': '兔耳小屋', '电话线藤蔓拱门': '电话线藤蔓拱', '吊线星星风铃': '星星风铃', '纸睡莲灯': '睡莲灯', '郁金香花圃+栅栏': '郁金香花圃', '立体纸病床+纸帘': '立体纸病床',
 '心形点滴纸艺': '心形点滴架', '纸彩带礼炮': '礼炮', '折纸松林': '折纸松树', '折纸松林②': '折纸松树', '蘑菇下读书的兔子': '蘑菇下读书兔', '纸太阳+光芒': '纸太阳',
 '螺旋纸塔': '螺旋纸塔(中)', '坐着的兔子雕像': '兔子雕像', '纸山+星星挂饰': '纸山片', '巨书封面翻开(开场)': '巨书封面', 'DROP 巨页翻开·城堡弹起': '巨型立体城堡',
 '书页爱心终点门': '书页爱心终点门', '五只兔子一家': '五只兔子一家'}
# per layer: lateral distance from the road EDGE [near, far] m, height offset range, and pop-up anim default
LAYER = {   # dressing pass (in-game vs key renders): decor hugs the road and reads at the gameplay camera's scale
 'ground': dict(near=[0.3, 9.0], y=[0, 0], scale=[1.4, 2.2]),
 'mid':    dict(near=[1.5, 7.0], y=[0, 0], scale=[1.5, 2.2]),   # v3: mid pieces read as shapes, not specks
 'land':   dict(near=[8.0, 18.0], y=[0, 0], scale=[1.0, 1.0]),
 'sky':    dict(near=[12.0, 45.0], y=[7, 22], scale=[0.8, 1.25]),
 'anim':   dict(near=[1.0, 9.0], y=[1.0, 5.0], scale=[1.2, 1.8]),
}
PAL = {   # zone environment (sky/fog/page) from DESIGN.md light notes
 'z01': dict(skyTop='#CFE3E6', skyBottom='#FFE2C8', fog='#F3F1EA', ground='#EEF3E6', light='#FFF4E0', ambient='#DDEFE6', fogStart=45, fogEnd=150),
 'z02': dict(skyTop='#5FB8F0', skyBottom='#CDEBFF', fog='#E2F2FF', ground='#B7E3A2', light='#FFF8E6', ambient='#E6F3FF', fogStart=60, fogEnd=180),
 'z03': dict(skyTop='#3A2F6B', skyBottom='#FF8A65', fog='#F2A27A', ground='#F3D6BC', light='#FFC968', ambient='#E8C2B0', fogStart=45, fogEnd=150),
 'z04': dict(skyTop='#141A40', skyBottom='#3B2F6E', fog='#2A2A5A', ground='#2D2F66', light='#F7D98B', ambient='#8E86C8', fogStart=40, fogEnd=140),
 'z05': dict(skyTop='#7F93C4', skyBottom='#D8CCF5', fog='#CFC6EE', ground='#BFD4F5', light='#F4F1FA', ambient='#C9D3F0', fogStart=45, fogEnd=150),
 'z06': dict(skyTop='#C7B4EE', skyBottom='#FFC2A8', fog='#FFD3C0', ground='#F6D4C2', light='#FFE2C8', ambient='#E9CDE4', fogStart=50, fogEnd=160),
 'z07': dict(skyTop='#1E1A4A', skyBottom='#7B6CC8', fog='#4A3F8C', ground='#3A3478', light='#FFE08A', ambient='#9C90E0', fogStart=40, fogEnd=140),
 'z08': dict(skyTop='#1C0E30', skyBottom='#5A2A6A', fog='#3A1E55', ground='#3A1F52', light='#FFD27A', ambient='#C08AD8', fogStart=40, fogEnd=140),
 'z09': dict(skyTop='#0F2834', skyBottom='#2C3E6B', fog='#1F3A50', ground='#24495A', light='#F7D98B', ambient='#7FA8B8', fogStart=35, fogEnd=120),
 'z10': dict(skyTop='#A9DCFF', skyBottom='#FFD27A', fog='#FFE6C0', ground='#FFF3DE', light='#FFF1D6', ambient='#FFE8F0', fogStart=60, fogEnd=180),
}
here = os.path.dirname(os.path.abspath(__file__)); glbdir = os.path.join(here, '..', '..', 'public', 'models', 'omg-c')
# engine asset ids that reuse another asset's model (no sheet of their own)
GLB = {'tree-lo': 'tree-lo', 'tree-bush-lo': 'tree-lo', 'pine-lo': 'pine-lo', 'paper-hill-lo': 'paper-hill-lo', 'tree-bush': 'tree', 'tall-tower': 'spiral-tower', 'bird': 'page-bird', 'firework': 'star', 'lantern': 'firefly-lamp', 'leaf': 'petal', 'float-heart': 'flower-heart'}
def model_of(aid):
    g = GLB.get(aid, aid)
    return (True if g == aid else g) if os.path.exists(os.path.join(glbdir, g + '.glb')) else False
assets = {}; zones = []
for z in Z.ZONES:
    zid = z['id']; layers = []
    for layer, items in Z.LAYERS[zid].items():
        for name, count, tris in items:
            aid, shape, h = A[name]
            a = assets.setdefault(aid, dict(layer=layer, shape=shape, h=h, tris=tris, model=model_of(aid), names=[]))
            if name not in a['names']: a['names'].append(name)
            a['tris'] = max(a['tris'], tris)
            if layer == 'land': continue   # landmarks are placed as set pieces below
            L = LAYER[layer]; near = list(L['near'])
            if shape == 'far': near = [55.0, 90.0]
            layers.append(dict(asset=aid, layer=layer, count=count, near=near, y=L['y'], scale=L['scale'], colors=[0, 1, 2, 3, 4]))
    # set pieces: blueprint pieces matched to assets by label; landmarks the blueprint doesn't place are spaced through the zone
    sets = []
    land = [A[n][0] for n, c, _ in Z.LAYERS[zid].get('land', []) for _ in range(c)]
    used = []
    for t, side, label in z['pieces']:
        name = ALIAS.get(label) or next((n for n in sorted(A, key=len, reverse=True) if n in label), None)
        if side == 0:
            if name and A[name][0] in land and A[name][0] not in used: aid = A[name][0]; side = 1 if len(sets) % 2 == 0 else -1
            else: continue
        else:
            if not name: continue
            aid = A[name][0]
        is_land = aid in land; used.append(aid)
        sets.append(dict(t=t, side=side, asset=aid, dist=8.0 if is_land else 3.0, scale=1.0, pop='spring', label=label))
    rest = list(land)
    for u in used:
        if u in rest: rest.remove(u)
    for k, aid in enumerate(rest):
        t = z['t0'] + (k + 0.6) / (len(rest) + 0.4) * (z['t1'] - z['t0'])
        sets.append(dict(t=round(t, 2), side=1 if (len(sets) + k) % 2 == 0 else -1, asset=aid, dist=9.0, scale=1.0, pop='spring', label='landmark'))
    sets.sort(key=lambda d: d['t'])
    for i in range(len(sets) - 1):   # two big pieces within 3 s never share a side
        if sets[i + 1]['t'] - sets[i]['t'] < 3 and sets[i + 1]['side'] == sets[i]['side']: sets[i]['side'] *= -1
    moments = [dict(t=t, label=label) for t, side, label in z['pieces'] if side == 0]
    zones.append(dict(id=zid, key=z['key'], t0=z['t0'], t1=z['t1'], name=z['cn'], colors=z['pal'], palette=PAL[zid], layers=layers, setpieces=sets, moments=moments))
# ---- density pass (high tier): 3D kit instead of most flat decals, continuous mid clusters, a far ring, secondary hero copies.
# Everything added here carries hi=True so the low tier keeps its old counts.
KIT = {'clover': ('clover', 'tuft', 0.14), 'fern': ('fern', 'tuft', 0.55), 'tulip': ('tulip', 'flower', 0.4), 'mushroom-group': ('mushroom-group', 'mushroom', 0.5)}
DECAL_KEEP = {'z03': 0.35, 'z04': 0.3, 'z05': 0.35, 'z07': 0.3, 'z08': 0.3, 'z10': 0.4}
G, M = 'ground', 'mid'
EXTRA = {   # zone: [(asset, layer, count)]  -- counts before spec.density
 'z01': [('clover', G, 160), ('fern', G, 90), ('tulip', G, 90), ('mushroom', G, 50), ('tree', M, 24), ('fence', M, 24), ('tulip-bed', M, 10)],
 'z02': [('clover', G, 140), ('tulip', G, 120), ('fern', G, 70), ('mushroom-group', G, 30), ('bunny-statue', M, 6), ('tree-bush', M, 24)],
 'z03': [('flower-heart', G, 200), ('tulip', G, 120), ('gift', G, 60), ('mushroom', G, 80), ('clover', G, 100), ('tulip-bed', M, 14), ('bunny-statue', M, 6), ('iv-heart', M, 8)],
 'z04': [('flower-heart', G, 160), ('gift', G, 90), ('lily-lamp', G, 50), ('tulip', G, 90), ('star-chime', M, 16), ('firefly-lamp', M, 24), ('bunny-statue', M, 6), ('heart-sculpt', M, 12)],
 'z05': [('reed', G, 260), ('lily-lamp', G, 90), ('fern', G, 120), ('mushroom', G, 60), ('clover', G, 120), ('rock', M, 30), ('tulip-bed', M, 8), ('firefly-lamp', M, 24), ('tree', M, 18), ('pine', M, 16), ('bunny-statue', M, 4)],
 'z06': [('tulip', G, 150), ('clover', G, 150), ('mushroom-group', G, 30), ('tulip-bed', M, 14), ('fence', M, 24), ('bunny-house', M, 6)],
 'z07': [('mushroom', G, 90), ('gift', G, 60), ('lily-lamp', G, 60), ('flower-heart', G, 120), ('star-chime', M, 16), ('book-stack', M, 14), ('pine', M, 20)],
 'z08': [('gift', G, 120), ('flower-heart', G, 200), ('lily-lamp', G, 60), ('tulip', G, 100), ('balloons', M, 20), ('bunting', M, 20), ('stall', M, 8), ('tulip-bed', M, 10)],
 'z09': [('fern', G, 220), ('mushroom-group', G, 50), ('reed', G, 60), ('clover', G, 100), ('mushroom', G, 60), ('tree', M, 24), ('firefly-lamp', M, 24), ('bunny-statue', M, 4)],
 'z10': [('tulip', G, 150), ('flower-heart', G, 200), ('gift', G, 70), ('clover', G, 100), ('tulip-bed', M, 8), ('fence', M, 24), ('bunny-statue', M, 6), ('heart-bed', M, 5)],
}
KIT_BIG = {'clover', 'fern', 'tulip', 'flower-heart', 'mushroom', 'reed', 'flower'}
MASS = {'z01': [('tree-bush', 40)], 'z02': [('tree-bush', 40)], 'z03': [('tree-bush', 30)], 'z04': [('pine', 30)], 'z05': [('pine', 30), ('tree-bush', 20)],
        'z06': [('tree-bush', 40)], 'z07': [('pine', 40)], 'z08': [('tree-bush', 30)], 'z09': [('pine', 60)], 'z10': [('tree-bush', 40)]}
# pass 2 (merged mid layer): mid filler <= 650 tris x2.2, heavy mid unchanged; base ground specks halved (they read as dots at this camera)
MT = {}
for f in glob.glob(os.path.join(here, '..', '..', 'deliverables', 'omg-c-models', 'metrics', '*.metrics.json')):
    try: MT[os.path.basename(f).split('.')[0]] = json.load(open(f)).get('tris') or 0
    except Exception: pass
SPECKS = {'flower', 'grass', 'flower-heart', 'pebble', 'moss-rock', 'slab'}
NIGHT_LAMPS = {'z04': [('firefly-lamp', 'mid', 30), ('lily-lamp', 'mid', 20)], 'z07': [('firefly-lamp', 'mid', 36), ('lily-lamp', 'mid', 20), ('star-chime', 'mid', 12)],
               'z08': [('firefly-lamp', 'mid', 30), ('lily-lamp', 'mid', 16)], 'z09': [('firefly-lamp', 'mid', 50), ('lily-lamp', 'mid', 30), ('mushroom-house', 'mid', 8)]}
Z10 = [('bunny-statue', 'mid', 12), ('balloons', 'mid', 16), ('bunting', 'mid', 24), ('heart-bed', 'mid', 10), ('tulip-bed', 'mid', 10), ('tree-bush', 'mid', 14)]
RING = {   # far ring 22-55 m out: paper hills + zone silhouette pieces, big scale
 'z01': ['paper-hill', 'tree'], 'z02': ['paper-hill', 'tree'], 'z03': ['paper-hill', 'tree'], 'z04': ['paper-hill', 'lantern-tower'],
 'z05': ['paper-hill', 'pine'], 'z06': ['paper-hill', 'tree'], 'z07': ['paper-hill', 'pine', 'spiral-tower'], 'z08': ['paper-hill', 'lantern-tower'],
 'z09': ['paper-hill', 'pine'], 'z10': ['paper-hill', 'tree-bush'],
}
for lo, base in (('tree-lo', 'tree'), ('tree-bush-lo', 'tree-bush'), ('pine-lo', 'pine'), ('paper-hill-lo', 'paper-hill')):
    if base in assets: assets[lo] = dict(assets[base], model=model_of(lo), names=[], tris=150)
for a in KIT.values(): assets.setdefault(a[0], dict(layer='ground', shape=a[1], h=a[2], tris=200, model=model_of(a[0]), names=[]))
for z in zones:
    zid = z['id']
    for L in z['layers']:
        if L['asset'].endswith('-decal') and zid in DECAL_KEEP: L['count'] = round(L['count'] * DECAL_KEEP[zid])
    lum = lambda h: (0.299 * int(h[1:3], 16) + 0.587 * int(h[3:5], 16) + 0.114 * int(h[5:7], 16)) / 255
    bright = [i for i, h in enumerate(z['colors']) if lum(h) > 0.35] or [0, 1, 2, 3, 4]   # decor never takes the zone's night navy
    for L in z['layers']: L['colors'] = bright
    zk = (z['t1'] - z['t0']) / 15.12   # z09 is twice as long: keep density per second
    for aid, layer, n in EXTRA.get(zid, []):
        n = round(n * zk * (0.5 if aid in ('gift', 'lily-lamp') else 1))
        Ld = LAYER[layer]; sc = [2.2, 3.4] if layer == G and aid in KIT_BIG else Ld['scale']   # kit reads at the gameplay camera
        z['layers'].append(dict(asset=aid, layer=layer, count=n, near=list(Ld['near']), y=Ld['y'], scale=sc, colors=bright, hi=True))
    for aid, n in MASS.get(zid, []):   # cheap tree masses hugging the road (~300 tris each) so no stretch is bare
        z['layers'].append(dict(asset=aid, layer='mid', count=round(n * zk), near=[2.0, 12.0], y=[0, 0], scale=[1.0, 1.5], colors=bright, hi=True, mass=True))
    for L in z['layers']:
        if zid == 'z10' and L['asset'] == 'bunny-house' and not L.get('hi'): L['count'] = 20   # 1k-tri houses: z10 peak
    for aid, layer, n in NIGHT_LAMPS.get(zid, []) + (Z10 if zid == 'z10' else []):
        Ld = LAYER[layer]; z['layers'].append(dict(asset=aid, layer=layer, count=n, near=list(Ld['near']), y=Ld['y'], scale=Ld['scale'], colors=bright, hi=True))
    LO = {'tree': 'tree-lo', 'tree-bush': 'tree-bush-lo', 'pine': 'pine-lo', 'paper-hill': 'paper-hill-lo'}   # ~110-145 tri decimated fillers
    for L in list(z['layers']):
        g = GLB.get(L['asset'], L['asset']); t = MT.get(g, 9999)
        if L.get('mass') and L['asset'] in LO: L['asset'] = LO[L['asset']]
        elif L['layer'] == 'mid' and t <= 650 and L['near'][0] < 20:
            if L['asset'] in LO: z['layers'].append(dict(L, asset=LO[L['asset']], count=round(L['count'] * 1.2), hi=True))   # the extra copies are low-poly
            else: L['count'] = round(L['count'] * 2.2)
        elif L['layer'] == 'mid' and L['asset'] in LO and (L['near'][0] >= 20 or L.get('mass')): L['asset'] = LO[L['asset']]   # far ring / masses
        if L['layer'] == 'ground' and not L.get('hi') and L['asset'] in SPECKS: L['count'] = round(L['count'] * 0.5)
        if zid == 'z10' and L['layer'] == 'anim' and L['asset'] == 'streamer': L['count'] = 150   # 'scattered leaves'
        if zid == 'z10' and L['asset'] == 'gold-decal': L['count'] = 30
        if L['asset'] == 'lily-lamp': L['count'] = round(L['count'] * 0.5)   # 414 tris
        if L['asset'] == 'gift': L['count'] = round(L['count'] * 0.5)   # 252 tris
    for k, aid in enumerate(RING[zid]):
        z['layers'].append(dict(asset=LO.get(aid, aid), layer='mid', count=round((16 if k == 0 else 12 if aid in ('tree', 'pine', 'tree-bush') else 5) * zk), near=[40.0, 85.0], y=[0, 0], scale=[1.8, 3.0] if k == 0 else [1.8, 2.8], colors=bright, hi=True))
    # secondary hero copies: each hero/landmark set piece gets a smaller twin on the other side 2.5 s later and a far-ring copy
    extra = []
    for sp in z['setpieces']:
        if sp['asset'] in ('bunny-family',) or MT.get(GLB.get(sp['asset'], sp['asset']), 0) > 3000: continue   # heavy heroes: no twin (draws + tris)
        t2 = sp['t'] + 2.5
        if t2 < z['t1'] - 0.5: extra.append(dict(sp, t=round(t2, 2), side=-sp['side'], dist=max(4.0, sp['dist'] - 2), scale=0.6, label='twin', hi=True))
    z['setpieces'] = sorted(z['setpieces'] + extra, key=lambda d: d['t'])
# placement now retries spots over other road segments (place.ts), so ~95% of ground / ~70% of mid land instead of ~55% / ~30%:
# rescale the counts to the high-tier budget (~150k tris)
for z in zones:
    for L in z['layers']:
        if L['layer'] == 'ground': L['count'] = round(L['count'] * (0.33 if L['asset'] == 'reed' else 0.55))
        elif L['layer'] == 'mid' and not L['asset'].endswith('-lo') and L['near'][0] < 20:
            L['count'] = round(L['count'] * (0.45 if L['asset'] in ('firefly-lamp', 'lily-lamp', 'star-chime', 'heart-sculpt') else 0.72))
    zf = {'z07': (1, 0.85), 'z08': (0.9, 0.78), 'z09': (1.15, 1.25), 'z10': (0.8, 0.65)}.get(z['id'])   # (ground, mid) peak zones
    if zf:
        for L in z['layers']:
            if L['layer'] == 'ground': L['count'] = round(L['count'] * zf[0])
            elif L['layer'] == 'mid' and L['near'][0] < 20: L['count'] = round(L['count'] * zf[1])
# ---- v3 'big continuous masses' pass (keys read as solid forest / hedge / hill / house masses, not confetti):
# specks cut hard, single-tree masses thinned, clustered kit added (place.ts cluster: blob or row). All high tier only.
CL = {   # zone: [(asset, centres per 15 s, cluster)]
 'forest': ('forest-clump', dict(n=[2, 3], r=6.0), [4.0, 16.0]), 'pines': ('pine-lo', dict(n=[5, 8], r=3.2), [3.0, 16.0]),
 'hedge': ('hedge', dict(n=[3, 5], r=6.2, row=True), [2.0, 5.0]), 'hills': ('paper-hill-lo', dict(n=[3, 5], r=5.0), [14.0, 32.0]),
 'houses': ('bunny-house', dict(n=[3, 4], r=4.2, row=True), [6.0, 10.0]), 'mhouses': ('mushroom-house', dict(n=[3, 4], r=3.8, row=True), [6.0, 10.0]),
}
CLUMPS = {'z01': dict(forest=8, hedge=6, hills=4), 'z02': dict(forest=8, hedge=6, hills=4), 'z03': dict(forest=6, hedge=7, hills=3),
          'z04': dict(pines=6, hedge=4, hills=3, forest=3), 'z05': dict(pines=8, forest=4, hills=5), 'z06': dict(forest=6, hedge=6, hills=3, houses=3),
          'z07': dict(pines=14, forest=6, hills=5, mhouses=3, hedge=3), 'z08': dict(forest=5, hedge=6, hills=3, mhouses=2), 'z09': dict(pines=12, forest=6, hills=5, mhouses=3),
          'z10': dict(forest=7, hedge=7, hills=4, houses=2)}
for aid in ('hedge', 'forest-clump'): assets.setdefault(aid, dict(layer='mid', shape='tree', h={'hedge': 1.3, 'forest-clump': 5.7}[aid], w={'hedge': 6.1, 'forest-clump': 8.6}[aid], tris=300, model=model_of(aid), names=[]))
for z in zones:
    zid = z['id']; zk = (z['t1'] - z['t0']) / 15.12
    for L in z['layers']:
        if L['layer'] == 'ground': L['count'] = round(L['count'] * (0.3 if L['asset'] in SPECKS or L['asset'].endswith('-decal') else 0.45))
        if L.get('mass'): L['count'] = round(L['count'] * 0.4)
    bright = z['layers'][0]['colors'] if z['layers'] else [0, 1, 2, 3, 4]
    for kind, n in CLUMPS[zid].items():
        aid, cl, near = CL[kind]
        z['layers'].append(dict(asset=aid, layer='mid', count=max(1, round(n * zk)), near=near, y=[0, 0], scale=[0.75, 1.0] if aid == 'forest-clump' else [1.0, 1.3] if aid == 'hedge' else [1.1, 1.6] if aid != 'paper-hill-lo' else [1.0, 1.5], colors=bright, hi=True, cluster=cl))
# ---- v4 painted layer: impostor carpet (sprite cards from tools/impostors), painted ground tiles + horizon backdrops (Codex)
IMP = {
 'z01': [('tree', 3), ('tree-lo', 2), ('forest-clump', 2), ('hedge', 1), ('tulip-bed', 1), ('bunny-house', 0.4), ('fence', 0.5), ('paper-hill', 0.8), ('fern', 1)],
 'z02': [('tree', 2.5), ('forest-clump', 2), ('bunny-house', 1.2), ('mushroom-house', 1.2), ('tulip-bed', 1.5), ('windmill', 0.12), ('hedge', 1), ('fence', 0.6)],
 'z03': [('tree', 2), ('forest-clump', 1.5), ('heart-bed', 1.2), ('tulip-bed', 1.2), ('clock-tower', 0.1), ('bunny-house', 0.6), ('gift', 0.6), ('hedge', 1)],
 'z04': [('pine', 3), ('lantern-tower', 0.25), ('mushroom-house', 0.6), ('lily-lamp', 0.8), ('firefly-lamp', 1.2), ('heart-bed', 0.6), ('castle', 0.03)],
 'z05': [('pine', 3), ('tree', 1), ('reed', 1.5), ('lily-lamp', 1), ('rock', 1), ('paper-hill', 0.8), ('firefly-lamp', 0.6)],
 'z06': [('tulip-bed', 2), ('heart-bed', 1.5), ('tree', 1.5), ('forest-clump', 1), ('bunny-house', 0.8), ('fence', 0.5), ('hedge', 1)],
 'z07': [('pine', 3), ('spiral-tower', 0.15), ('star-chime', 0.6), ('mushroom-house', 0.8), ('firefly-lamp', 1.2), ('lantern-tower', 0.2), ('book-stack', 0.4)],
 'z08': [('tree', 1.5), ('forest-clump', 1), ('balloons', 1), ('stall', 0.5), ('carousel', 0.06), ('ferris-wheel', 0.04), ('bunting', 0.5), ('heart-bed', 1), ('lantern-string', 0.4)],
 'z09': [('pine', 4), ('forest-clump', 1), ('mushroom-house', 0.8), ('mushroom-group', 1), ('firefly-lamp', 1.2), ('lily-lamp', 0.5)],
 'z10': [('tree', 1.5), ('forest-clump', 1), ('tulip-bed', 1.5), ('heart-bed', 1.5), ('bunny-house', 0.8), ('balloons', 1), ('bunny-statue', 0.5)],
}
# ---- v5 heroes: each zone's key hero(es) beside the road ahead (in the key camera's view for several seconds), scaled up, with a
# lit / dressed entourage around them; duplicates of the same hero in the zone are dropped
HERO = {   # zone: [(asset, t, side, scale, entourage [(asset, n)])]
 'z01': [('book-cover', 4.5, 1, 1.6, [('bunny-statue', 5), ('tulip-bed', 4), ('fence', 6), ('hedge', 2)]), ('bunny-statue', 9.5, -1, 2.2, [('tulip-bed', 3), ('heart-bed', 3), ('fence', 4)])],
 'z03': [('clock-tower', 38.5, 1, 1.55, [('tulip-bed', 4), ('firefly-lamp', 6), ('gift', 5), ('heart-bed', 3)])],
 'z04': [('castle', 52.0, -1, 1.6, [('firefly-lamp', 10), ('lily-lamp', 6), ('star-chime', 4), ('heart-bed', 4)]), ('bunny-heart', 55.5, 1, 1.0, [('firefly-lamp', 6), ('lily-lamp', 4)])],
 'z08': [('carousel', 110.0, 1, 1.45, [('balloons', 6), ('firefly-lamp', 8), ('bunting', 6), ('stall', 2)]), ('ferris-wheel', 113.5, 1, 1.45, [('balloons', 5), ('firefly-lamp', 8), ('lantern-string', 3), ('heart-bed', 3)])],
 'z10': [('bunny-family', 155.5, -1, 1.9, [('balloons', 6), ('heart-bed', 4), ('bunny-statue', 6), ('tulip-bed', 4)]), ('heart-gate', 160.4, 1, 1.3, [('balloons', 6), ('bunny-statue', 4), ('heart-bed', 3)])],
}
for z in zones:   # v5: tree-bush / paper-hill set pieces read as big mint blobs near the camera: dropped (masses come from clusters)
    z['setpieces'] = [sp for sp in z['setpieces'] if sp['asset'] not in ('tree-bush', 'paper-hill')]
for z in zones:
    for aid, t, side, sc, ent in HERO.get(z['id'], []):
        base = next((sp for sp in z['setpieces'] if sp['asset'] == aid and not sp.get('hi')), None)
        z['setpieces'] = [sp for sp in z['setpieces'] if sp['asset'] != aid]   # drop duplicates and twins of the hero
        d = dict(base or dict(asset=aid, pop='spring', label='hero'), t=t, side=side, scale=sc, dist=1.5, hero=True, entourage=[list(e) for e in ent if e[0] in assets])
        z['setpieces'] = sorted(z['setpieces'] + [d], key=lambda x: x['t'])
paint = os.path.join(glbdir, 'paint')
for z in zones:
    zk = (z['t1'] - z['t0']) / 15.12
    z['impostors'] = dict(count=round(2600 * zk), near=[13.0, 95.0], scale=[1.5, 2.6], sprites=[list(x) for x in IMP[z['id']]])
    for kind in ('ground', 'backdrop'):
        f = next((f'{z["id"]}-{kind}.{e}' for e in ('webp', 'jpg') if os.path.exists(os.path.join(paint, f'{z["id"]}-{kind}.{e}'))), None)
        if f: z[kind] = 'models/omg-c/paint/' + f
    z['tile'] = 25
spec = dict(version=1, pagePad=60, source='levels-design/omg/redesign-v3/C/zones_c.py (omg-design-v3)', chunk=20, window=dict(behind=3, ahead=8),
            clear=dict(ground=0.3, groundMaxH=1.6, near=1.0), density=dict(ground=2.0, mid=1.6, anim=0.55), assets=assets, zones=zones)
# design asset sheets (levels-design/omg/redesign-v3/C/assets/<design id>/spec.json): their size / tri budget win over the table
CAT = json.load(open(os.path.join(here, '..', 'models', 'catalog.json')))
DESIGN_IDS = {c['id']: c['design'] for c in CAT if 'item' not in c}
DESIGN = os.environ.get('DESIGN', '/workspace/nj-design-v3/levels-design/omg/redesign-v3/C')
for aid, did in DESIGN_IDS.items():
    f = os.path.join(DESIGN, 'assets', did, 'spec.json')
    if aid in spec['assets'] and os.path.exists(f):
        d = json.load(open(f)); a = spec['assets'][aid]
        sz = d.get('size_m', {}); a['design'] = did; a['h'] = sz.get('h', a['h']); a['w'] = sz.get('w'); a['d'] = sz.get('d'); a['tris'] = d.get('tris_budget', a['tris'])
# the five-bunny family is one grouped asset (H07): keep a single set piece
for z in spec['zones']:
    seen = False; keep = []
    for sp in z['setpieces']:
        if sp['asset'] == 'bunny-family':
            if seen: continue
            seen = True; sp['t'] = sp['t'] if sp.get('hero') else 153.5
        keep.append(sp)
    z['setpieces'] = keep
# ---- v5 near band: tree / hill masses keep out of the near band (they read as oversized mint blobs at the frame edges);
# near-road decor is mid-sized and colourful. Trees within 14 m of the road are capped at ~4 m and thinned; hills / forest clumps
# start at 16 m. z01 / z10 get a colourful richness pass (beds, bunnies, balloons, houses, gifts) in their place.
TREEY = ('tree', 'tree-bush', 'tree-lo', 'tree-bush-lo', 'pine', 'pine-lo')
for z in zones:
    for ly in z['layers']:
        if ly.get('layer') != 'mid': continue
        a, nr = ly['asset'], ly.get('near', [0, 0])
        if a in TREEY and nr[0] < 14:
            h = assets.get(a, {}).get('h', 4.0); ly['scale'] = [round(min(ly['scale'][0], 3.0 / h), 2), round(min(ly['scale'][1], 4.2 / h), 2)]
            ly['count'] = max(1, round(ly['count'] * 0.55)); ly['near'] = [max(nr[0], 5.0), max(nr[1], 12.0)]
        elif a in ('paper-hill', 'paper-hill-lo', 'forest-clump') and nr[0] < 16:
            ly['near'] = [16.0, max(nr[1], 34.0)]
for z in zones:   # and no tree / hill mass anywhere taller than ~6 m (colourful sets and heroes own the vertical)
    for ly in z['layers']:
        a = ly['asset']
        if ly.get('layer') == 'mid' and (a in TREEY or a in ('paper-hill', 'paper-hill-lo', 'forest-clump')):
            h = assets.get(a, {}).get('h', 4.0); ly['scale'] = [round(min(ly['scale'][0], 4.5 / h), 2), round(min(ly['scale'][1], 6.0 / h), 2)]
for z in zones:   # v6: day zones z01-z03 read too mint at the hero zoom-out: forest masses / tree sprites halved
    if z['id'] in ('z01', 'z02', 'z03'):
        for ly in z['layers']:
            if ly['asset'] in ('forest-clump', 'paper-hill-lo', 'tree-lo', 'tree-bush-lo') and ly.get('layer') == 'mid': ly['count'] = max(1, round(ly['count'] * 0.5))
        z['impostors']['sprites'] = [[k, round(w * 0.5, 2) if k in ('tree', 'tree-lo', 'forest-clump', 'paper-hill') else w] for k, w in z['impostors']['sprites']]
RICH = {'z01': [('tulip-bed', 12), ('heart-bed', 8), ('bunny-statue', 8), ('balloons', 6), ('mushroom-house', 4), ('bunny-house', 4), ('gift', 6), ('flower-heart', 8)],
        'z10': [('balloons', 14), ('bunting', 10), ('heart-bed', 10), ('bunny-statue', 14), ('gift', 10), ('flower-heart', 10), ('tulip-bed', 8), ('lantern-string', 4)]}
for z in zones:
    for aid, n in RICH.get(z['id'], []):
        if z['id'] == 'z10': n = max(1, round(n * 0.7))   # v6 budget
        if aid in assets: z['layers'].append(dict(asset=aid, layer='mid', count=n, near=[3.0, 13.0], y=[0, 0], scale=[1.25, 1.7], colors=(z['layers'][0]['colors'] if z['layers'] else [0, 1, 2, 3, 4]), hi=True))   # richness is high tier only (low stays ~50k)
# ---- v6 night villages (z04 / z07 / z08 / z09): rows of small lit houses + towers along the road, lamp lines, glowing flowers
# (halos in the merged glow mesh), lit-window impostors in the distance; dark near-road trees thinned to pay for it
NIGHTZ = ('z04', 'z07', 'z08', 'z09')
for z in zones:
    if z['id'] not in NIGHTZ: continue
    zk = (z['t1'] - z['t0']) / 15.12; cols = z['layers'][0]['colors'] if z['layers'] else [0, 1, 2, 3, 4]
    for ly in z['layers']:
        if ly.get('layer') == 'mid' and ly['asset'] in TREEY + ('forest-clump', 'paper-hill-lo') and ly['near'][0] < 40: ly['count'] = max(1, round(ly['count'] * 0.4))
        if ly['asset'] in ('lantern-string', 'heart-sculpt', 'cannon') and ly.get('layer') == 'mid': ly['count'] = max(1, round(ly['count'] * 0.5))
    V = [('mushroom-house', 'mid', round(3 * zk), [5.0, 12.0], [0.9, 1.2], dict(n=[3, 4], r=3.8, row=True), True),
         ('bunny-house', 'mid', round(1 * zk), [6.0, 13.0], [0.85, 1.1], dict(n=[2, 3], r=4.2, row=True), True),
         ('mushroom-house', 'mid', round(1.5 * zk), [5.0, 12.0], [0.9, 1.2], dict(n=[2, 3], r=3.8, row=True), False),
         ('firefly-lamp', 'mid', round(14 * zk), [1.5, 4.0], [1.1, 1.4], None, False),
         ('firefly-lamp', 'mid', round(14 * zk), [1.5, 5.0], [1.1, 1.4], None, True),
         ('flower-heart', 'ground', round(70 * zk), [0.3, 9.0], [2.0, 3.0], None, True),
         ('flower-heart', 'ground', round(30 * zk), [0.3, 7.0], [2.0, 3.0], None, False)]
    if z['id'] == 'z04': V = [(v[0], v[1], round(v[2] * 0.6) if v[0] == 'flower-heart' else v[2], *v[3:]) for v in V]   # z04 fill rate (Mac 8.3 ms)
    if z['id'] == 'z09': V = [(v[0], v[1], round(v[2] * (1.8 if 'house' in v[0] else 1.5)), *v[3:]) for v in V]   # z09: no hero, darkest carpet -> densest village
    for aid, layer, n, near, sc, cl, hi in V:
        if aid not in assets or n < 1: continue
        d = dict(asset=aid, layer=layer, count=n, near=near, y=[0, 0], scale=sc, colors=cols, hi=hi)
        if cl: d['cluster'] = cl
        z['layers'].append(d)
    IM = z['impostors']['sprites']; W = {k: w for k, w in IM}
    for k in ('pine', 'tree', 'tree-lo', 'forest-clump'):
        if k in W: W[k] = round(W[k] * 0.5, 2)
    for k, w in (('mushroom-house', 1.6), ('bunny-house', 1.2), ('lantern-tower', 0.6), ('firefly-lamp', 1.4), ('lily-lamp', 0.8)): W[k] = max(W.get(k, 0), w)
    z['impostors']['sprites'] = [[k, w] for k, w in W.items()]
    z['nightLevel'] = 1.45   # night carpet texture brightened
for z in zones:   # v6 budget: z08 (carousel + wheel + village) over 150k -> lantern towers x0.4, high-tier balloons / bunting / hedges x0.5
    if z['id'] != 'z08': continue
    for ly in z['layers']:
        if ly['asset'] == 'lantern-tower': ly['count'] = max(1, round(ly['count'] * 0.4))
        elif ly['asset'] in ('balloons', 'bunting', 'hedge') and ly.get('hi'): ly['count'] = max(1, round(ly['count'] * 0.5))
# ---- v7 ----
def addl(z, aid, layer, n, near, sc, hi, cl=None, hug=False):
    if aid not in assets or n < 1: return
    d = dict(asset=aid, layer=layer, count=n, near=near, y=[0, 0], scale=sc, colors=(z['layers'][0]['colors'] if z['layers'] else [0, 1, 2, 3, 4]), hi=hi)
    if cl: d['cluster'] = cl
    if hug: d['hug'] = True
    z['layers'].append(d)
for z in zones:
    zid = z['id']; zk = (z['t1'] - z['t0']) / 15.12
    if zid == 'z06':   # v4 richness back, colourful and mid-sized (houses in rows, beds, fences, bunnies)
        addl(z, 'bunny-house', 'mid', round(2 * zk), [6.0, 12.0], [0.9, 1.2], True, dict(n=[2, 3], r=4.2, row=True))
        addl(z, 'mushroom-house', 'mid', round(2 * zk), [6.0, 12.0], [0.9, 1.2], True, dict(n=[2, 3], r=3.8, row=True))
        for aid, n in (('tulip-bed', 10), ('heart-bed', 8), ('fence', 10), ('bunny-statue', 5), ('flower-heart', 30)): addl(z, aid, 'mid' if aid != 'flower-heart' else 'ground', round(n * zk), [3.0, 12.0], [1.2, 1.6], True)
        z['impostors']['sprites'] = [[k, w * (1.6 if k in ('bunny-house', 'tulip-bed', 'heart-bed') else 1)] for k, w in z['impostors']['sprites']] + [['mushroom-house', 1.0]]
    if zid == 'z05':   # lake: lit lily lamps, reeds, rocks, pine masses beyond the near band (depth), a few beds / mushrooms
        addl(z, 'pine-lo', 'mid', round(4 * zk), [16.0, 34.0], [0.9, 1.1], True, dict(n=[5, 8], r=3.2))
        for aid, n in (('lily-lamp', 10), ('reed', 30), ('rock', 8), ('tulip-bed', 6), ('mushroom-group', 10), ('bunny-statue', 3)): addl(z, aid, 'mid' if aid not in ('reed',) else 'ground', round(n * zk), [2.5, 12.0], [1.2, 1.6], True)
        z['impostors']['sprites'] = [[k, w * (2.0 if k == 'pine' else 1)] for k, w in z['impostors']['sprites']]
    if zid == 'z04':   # glare: fewer, smaller glows (flowers x0.35, lamp lines x0.5)
        for ly in z['layers']:
            if ly['asset'] == 'flower-heart' and ly.get('layer') == 'ground': ly['count'] = max(1, round(ly['count'] * 0.35))
            if ly['asset'] == 'firefly-lamp': ly['count'] = max(1, round(ly['count'] * 0.5))
    if zid == 'z09':   # v7: with houses allowed near the road the v6 village rows over-fill z09 (126 houses): x0.35
        for ly in z['layers']:
            if ly['asset'] in ('pine', 'pine-lo') and ly.get('layer') == 'mid': ly['count'] = max(1, round(ly['count'] * 0.7))   # budget for the house rows
    if zid in ('z07', 'z09'):   # bigger lit house rows hugging the road (merged into the chunk mid mesh); towers cut to pay
        for ly in z['layers']:
            if ly['asset'] == 'lantern-tower': ly['count'] = max(1, round(ly['count'] * 0.4))
        addl(z, 'mushroom-house', 'mid', round(3 * zk), [3.5, 8.0], [1.35, 1.7], True, dict(n=[3, 4], r=4.6, row=True), hug=True)
        addl(z, 'mushroom-house', 'mid', round(1 * zk), [3.5, 8.0], [1.35, 1.7], False, dict(n=[2, 3], r=4.6, row=True), hug=True)
    if zid == 'z01':   # top-right mint mass: tree / hill / forest masses beyond the near band mostly gone, colourful houses instead
        for ly in z['layers']:
            if ly.get('layer') == 'mid' and ly['asset'] in TREEY + ('forest-clump', 'paper-hill-lo', 'paper-hill', 'hedge'): ly['count'] = max(1, round(ly['count'] * 0.3))
        z['impostors']['sprites'] = [[k, round(w * 0.3, 2) if k in ('tree', 'tree-lo', 'forest-clump', 'paper-hill', 'hedge') else w] for k, w in z['impostors']['sprites']] + [['bunny-house', 1.0], ['tulip-bed', 1.0]]
        addl(z, 'bunny-house', 'mid', round(1.5 * zk), [8.0, 16.0], [0.9, 1.2], True, dict(n=[2, 3], r=4.2, row=True))
# ---- v8: 'view' layers -- rows / masses at a lateral offset from the FLOW line (what the key camera's frame actually covers:
# ~8 m each side at the head, ~18 m at mid-frame), pushed out of the zig-zag until clear (place.ts). Paid for by thinning ground
# glow / scattered props that sit outside the frame or read as specks.
def addv(z, aid, n, lat, sc, hi=True, cl=None):
    if aid not in assets or n < 1: return
    d = dict(asset=aid, layer='mid', count=n, near=[0.0, 0.0], view=lat, y=[0, 0], scale=sc, colors=(z['layers'][0]['colors'] if z['layers'] else [0, 1, 2, 3, 4]), hi=hi)
    if cl: d['cluster'] = cl
    z['layers'].append(d)
def mul(z, k, aids, layer=None, cond=None):
    for ly in z['layers']:
        if ly['asset'] in aids and (layer is None or ly.get('layer') == layer) and (cond is None or cond(ly)): ly['count'] = max(1, round(ly['count'] * k))
ROW = lambda n0, n1, r: dict(n=[n0, n1], r=r, row=True)
BLOB = lambda n0, n1, r: dict(n=[n0, n1], r=r)
for z in zones:
    zid = z['id']; zk = (z['t1'] - z['t0']) / 15.12
    if zid == 'z09':   # lit village where the key camera looks (the lower carpet was bare): house rows both sides, pine masses behind, lamp lines
        mul(z, 0.5, ('flower-heart', 'fern', 'mushroom-group'), 'ground'); mul(z, 0.35, ('book-stack',)); mul(z, 0.55, ('firefly-lamp', 'lily-lamp'), 'mid')
        mul(z, 0.5, ('paper-hill-lo', 'forest-clump'), 'mid'); mul(z, 0.4, ('mushroom-house',), 'mid', lambda l: 'view' not in l)
        addv(z, 'mushroom-house', round(4 * zk), [6.0, 12.0], [1.25, 1.6], True, ROW(3, 4, 4.4))
        addv(z, 'bunny-house', round(2 * zk), [7.0, 13.0], [1.0, 1.25], True, ROW(2, 3, 4.6))
        addv(z, 'pine-lo', round(5 * zk), [11.0, 19.0], [0.8, 1.05], True, BLOB(4, 6, 3.4))
        addv(z, 'firefly-lamp', round(10 * zk), [4.0, 7.5], [1.2, 1.5], True, ROW(2, 3, 3.0))
        addv(z, 'mushroom-house', round(1.5 * zk), [6.0, 12.0], [1.25, 1.6], False, ROW(2, 3, 4.4))   # low tier: a lighter row
        mul(z, 0.4, ('paper-hill-lo',), 'mid')   # pale green slabs at this camera -> pine masses / far house rows instead
        addv(z, 'pine-lo', round(6 * zk), [14.0, 26.0], [0.85, 1.1], True, BLOB(5, 7, 3.6))
        addv(z, 'bunny-house', round(1.5 * zk), [12.0, 18.0], [1.0, 1.2], True, ROW(2, 3, 4.6))
    if zid == 'z08':   # carnival rows framing the carousel / wheel
        mul(z, 0.55, ('flower-heart',), 'ground'); mul(z, 0.5, ('bunting', 'lantern-tower'), 'mid'); mul(z, 0.6, ('gift',), 'ground')
        addv(z, 'stall', round(2 * zk), [6.0, 12.0], [1.1, 1.35], True, ROW(2, 3, 3.6))
        addv(z, 'mushroom-house', round(2 * zk), [7.0, 13.0], [1.1, 1.4], True, ROW(2, 3, 4.2))
        addv(z, 'balloons', round(5 * zk), [4.5, 9.0], [1.2, 1.5], True)
        addv(z, 'pine-lo', round(3 * zk), [12.0, 19.0], [0.8, 1.0], True, BLOB(3, 5, 3.2))
    if zid == 'z07':   # same lag fill as z09: pine masses / house rows where the camera looks across the bends
        mul(z, 0.5, ('paper-hill-lo',), 'mid'); addv(z, 'pine-lo', round(4 * zk), [13.0, 24.0], [0.85, 1.1], True, BLOB(4, 6, 3.4))
        addv(z, 'bunny-house', round(1.5 * zk), [9.0, 16.0], [1.0, 1.2], True, ROW(2, 3, 4.6))
    if zid == 'z05':   # lake: bunny statues, paper boats and lotus lamps lining the water (key), rocks / reeds thinned (specks)
        mul(z, 0.3, ('rock',)); mul(z, 0.5, ('reed',), 'ground'); mul(z, 0.5, ('lily-lamp', 'tulip-bed'), 'mid', lambda l: 'view' not in l)
        addv(z, 'bunny-statue', round(3 * zk), [5.0, 11.0], [1.2, 1.6], True, ROW(2, 3, 4.0))
        addv(z, 'paper-boat', round(2 * zk), [6.0, 12.0], [0.9, 1.15], True, ROW(2, 2, 5.0))
        addv(z, 'lily-lamp', round(8 * zk), [3.5, 8.0], [1.3, 1.7], True, ROW(2, 3, 3.0))
        addv(z, 'pine-lo', round(3 * zk), [11.0, 19.0], [0.8, 1.0], True, BLOB(4, 6, 3.2))
        addv(z, 'mushroom-house', round(1.5 * zk), [8.0, 14.0], [1.0, 1.3], True, ROW(2, 3, 4.2))
        addv(z, 'bunny-statue', round(1 * zk), [5.0, 11.0], [1.2, 1.6], False, ROW(2, 2, 4.0))
    if zid == 'z06':   # flip phones, bunnies, heart beds, house rows hugging the road (key); bed carpets thinned (they were 50k tris)
        mul(z, 0.35, ('heart-bed',)); mul(z, 0.5, ('tulip-bed', 'fence'), 'mid', lambda l: 'view' not in l)
        mul(z, 0.3, ('bunny-house', 'mushroom-house'), 'mid', lambda l: 'view' not in l)
        addv(z, 'bunny-house', round(2.5 * zk), [6.5, 12.0], [1.0, 1.25], True, ROW(2, 3, 4.6))
        addv(z, 'mushroom-house', round(2.5 * zk), [6.0, 12.0], [1.15, 1.45], True, ROW(2, 3, 4.2))
        addv(z, 'bunny-statue', round(3 * zk), [4.5, 9.0], [1.2, 1.5], True)
        addv(z, 'flip-phone', round(1.2 * zk), [6.0, 11.0], [0.9, 1.1], True)
        addv(z, 'tree-lo', round(3 * zk), [11.0, 19.0], [0.7, 0.9], True, BLOB(3, 5, 3.2))
        addv(z, 'bunny-house', round(1 * zk), [6.5, 12.0], [1.0, 1.25], False, ROW(2, 2, 4.6))
# v8 z08: the wheel faces the key camera on the far side of the road from the carousel, so it reads as a wheel next to it
for z in zones:
    if z['id'] != 'z08': continue
    for sp in z['setpieces']:
        if sp['asset'] == 'ferris-wheel' and sp.get('hero'): sp.update(t=113.0, side=-1, dist=1.0, scale=1.35, face='cam')
        if sp['asset'] == 'carousel' and sp.get('hero'): sp.update(t=110.5)
    z['setpieces'].sort(key=lambda d: d['t'])
# v8b repetition pass (user: repeated models everywhere): row / blob members alternate kinds (palette variants step per member at runtime),
# lamp / pine / bed carpets thinned, a few under-used sheet pieces added near the road so each key view holds more distinct things
ALT = {'mushroom-house': ['bunny-house'], 'bunny-house': ['mushroom-house'], 'pine-lo': ['pine-lo', 'tree-lo'], 'firefly-lamp': ['firefly-lamp', 'lily-lamp'],
       'stall': ['balloons'], 'tree-lo': ['forest-clump', 'tree-lo'], 'heart-bed': ['tulip-bed']}
CUT = {'z01': [(0.7, ('tulip-bed',), 'mid')], 'z03': [(0.65, ('firefly-lamp',), 'mid')], 'z04': [(0.65, ('firefly-lamp',), 'mid'), (0.6, ('paper-hill-lo',), 'mid')],
       'z05': [(0.7, ('lily-lamp',), 'mid')], 'z06': [(0.7, ('heart-bed',), 'mid')], 'z07': [(0.65, ('firefly-lamp',), 'mid')],
       'z08': [(0.45, ('firefly-lamp',), 'mid'), (0.6, ('pine-lo',), 'mid')], 'z09': [(0.6, ('firefly-lamp', 'heart-bed'), 'mid'), (0.7, ('pine-lo',), 'mid'), (0.5, ('bunting',), 'mid')],
       'z10': [(0.7, ('heart-bed',), 'mid')]}
ADD2 = {   # v8b: more distinct pieces where one kind owned the key view (counts from tools/qa/repcount.mjs)
    'z01': [('bunny-statue', 1, [5.0, 9.0], [1.0, 1.2], None), ('tree-lo', 1.5, [9.0, 16.0], [0.9, 1.2], BLOB(2, 3, 3.0))],
    'z02': [('mushroom-house', 2, [7.0, 13.0], [1.0, 1.25], ROW(2, 3, 4.6)), ('tree-lo', 2, [10.0, 18.0], [0.9, 1.2], BLOB(2, 3, 3.0)), ('gift', 1.5, [3.5, 7.0], [1.3, 1.6], BLOB(2, 2, 2.0)), ('bunny-statue', 1, [5.0, 9.0], [1.0, 1.2], None)],
    'z04': [('mushroom-house', 1.5, [7.0, 13.0], [1.0, 1.3], ROW(2, 3, 4.4)), ('heart-sculpt', 1.5, [5.0, 10.0], [1.0, 1.2], None), ('star-chime', 1.5, [6.0, 11.0], [0.8, 1.0], None), ('bunny-statue', 1, [5.0, 9.0], [1.0, 1.3], None)],
    'z05': [('mushroom-group', 2, [3.5, 7.0], [1.3, 1.7], BLOB(2, 3, 2.0)), ('heart-sculpt', 1, [5.0, 9.0], [1.0, 1.2], None)],
    'z07': [('heart-sculpt', 1, [5.0, 9.0], [1.0, 1.2], None), ('mushroom-group', 1.5, [3.5, 7.0], [1.3, 1.7], BLOB(2, 3, 2.0))],
    'z09': [('mushroom-group', 2.5, [3.5, 7.0], [1.3, 1.7], BLOB(2, 3, 2.0)), ('bunny-statue', 1.5, [5.0, 9.0], [1.0, 1.3], ROW(2, 2, 4.0)), ('tree-lo', 2, [9.0, 16.0], [0.9, 1.2], BLOB(2, 3, 3.0)), ('book-stack', 1.5, [3.5, 7.0], [1.2, 1.5], BLOB(2, 3, 1.8))],
    'z10': [('bunny-statue', 1, [5.0, 9.0], [1.0, 1.3], None), ('tree-lo', 1.5, [9.0, 16.0], [0.9, 1.2], BLOB(2, 3, 3.0)), ('gift', 1.5, [3.5, 7.0], [1.3, 1.6], BLOB(2, 2, 2.0))]}
CUT2 = {'z01': [(0.6, ('fence',), 'mid')], 'z02': [(0.45, ('fence',), 'mid')], 'z05': [(0.4, ('rock',), 'mid'), (0.4, ('paper-hill-lo',), 'mid'), (0.5, ('bunny-statue',), 'mid')], 'z06': [(0.7, ('fence',), 'mid')], 'z10': [(0.7, ('fence',), 'mid')]}
for z in zones:
    zk = (z['t1'] - z['t0']) / 15.12
    for k, aids, layer in CUT2.get(z['id'], []): mul(z, k, aids, layer)
    for aid, n, lat, sc, cl in ADD2.get(z['id'], []): addv(z, aid, max(1, round(n * zk)), lat, sc, True, cl)
ADD = {'z03': [('heart-sculpt', 1.5, [5.0, 10.0], [0.9, 1.1], ROW(2, 2, 4.0))], 'z06': [('gift', 2, [3.5, 7.0], [1.3, 1.6], BLOB(2, 3, 2.0)), ('heart-sculpt', 1, [5.0, 9.0], [0.9, 1.1], None)],
       'z07': [('star-chime', 1.5, [5.0, 10.0], [0.8, 1.0], ROW(2, 2, 4.5))], 'z10': [('heart-sculpt', 1.5, [5.0, 10.0], [1.0, 1.2], None), ('balloons', 1.5, [6.0, 11.0], [0.9, 1.1], ROW(2, 2, 4.0))],
       'z01': [('gift', 1.5, [3.5, 7.0], [1.3, 1.6], BLOB(2, 3, 2.0))]}
for z in zones:
    zid = z['id']; zk = (z['t1'] - z['t0']) / 15.12
    for k, aids, layer in CUT.get(zid, []): mul(z, k, aids, layer)
    for aid, n, lat, sc, cl in ADD.get(zid, []): addv(z, aid, round(n * zk), lat, sc, True, cl)
    for ly in z['layers']:
        if ly.get('cluster') and ly['asset'] in ALT and ly['layer'] == 'mid': ly['alt'] = ALT[ly['asset']]
# v8c: the keys mass varied set dressing right along the road on both sides; mixed 'hug' rows (each member a different kind, palette stepped)
HUG = {'z01': ['tulip-bed', 'gift', 'heart-bed', 'tree-lo'], 'z02': ['tulip-bed', 'mushroom-group', 'gift', 'tree-lo'], 'z03': ['pull-tab', 'heart-sculpt', 'tulip-bed', 'gift'],
       'z04': ['lily-lamp', 'heart-sculpt', 'mushroom-group', 'star-chime'], 'z05': ['lily-lamp', 'mushroom-group', 'heart-sculpt', 'tree-lo'], 'z06': ['heart-bed', 'gift', 'tulip-bed', 'heart-sculpt'],
       'z07': ['book-stack', 'lily-lamp', 'mushroom-group', 'star-chime'], 'z08': ['balloons', 'gift', 'lily-lamp', 'tulip-bed'], 'z09': ['book-stack', 'mushroom-group', 'lily-lamp', 'tree-lo'],
       'z10': ['heart-bed', 'balloons', 'gift', 'tulip-bed']}
for z in zones:
    L = [a for a in HUG.get(z['id'], []) if a in assets]
    if len(L) < 2: continue
    zk = (z['t1'] - z['t0']) / 15.12
    addv(z, L[0], max(2, round(5 * zk)), [3.0, 7.5], [1.1, 1.4], True, ROW(3, 5, 2.8)); z['layers'][-1]['alt'] = L[1:]
    addv(z, L[1], max(1, round(1.5 * zk)), [3.0, 7.0], [1.1, 1.3], False, ROW(2, 3, 2.8)); z['layers'][-1]['alt'] = L[2:] + L[:1]   # low tier keeps a little
# v9 density without clones: big mixed masses along the road like the keys - each blob mixes kinds (alt) and steps the palette per member;
# groves mix tree kinds, book piles mix with chimes / gifts, house clusters carry lamps. High tier only (low tier keeps v8c).
MASS = {
 'z03': [(['ward-bed', 'screen', 'iv-heart', 'tulip-bed', 'gift'], 6, [3.5, 9.0], [1.05, 1.25], BLOB(4, 6, 2.6)),
         (['tree-lo', 'forest-clump', 'tree-bush', 'pine-lo'], 5, [8.0, 16.0], [1.0, 1.35], BLOB(5, 8, 3.2)),
         (['book-stack', 'gift', 'heart-sculpt', 'book-stack'], 4, [3.5, 8.5], [1.4, 1.9], BLOB(3, 5, 2.0)),
         (['bunny-house', 'mushroom-house'], 2, [8.0, 14.0], [1.0, 1.25], ROW(2, 3, 4.6))],
 'z04': [(['mushroom-house', 'bunny-house', 'lily-lamp', 'pine-lo', 'firefly-lamp'], 4, [6.0, 13.0], [1.1, 1.4], BLOB(4, 6, 3.4)),
         (['pine-lo', 'tree-lo', 'forest-clump', 'pine'], 5, [9.0, 18.0], [0.95, 1.3], BLOB(5, 8, 3.4)),
         (['book-stack', 'star-chime', 'book-stack', 'gift'], 4, [3.5, 8.0], [1.4, 1.9], BLOB(3, 5, 2.0)),
         (['tulip-bed', 'heart-bed', 'mushroom-group', 'heart-sculpt'], 5, [3.0, 7.0], [1.1, 1.4], BLOB(3, 5, 2.2))],
 'z05': [(['lily-lamp', 'mushroom-group', 'tulip-bed', 'rock'], 5, [3.0, 7.0], [1.2, 1.5], BLOB(3, 5, 2.2)),
         (['tree-lo', 'pine-lo', 'forest-clump', 'tree'], 5, [9.0, 17.0], [0.95, 1.3], BLOB(5, 8, 3.4)),
         (['mushroom-house', 'bunny-house', 'firefly-lamp'], 2.5, [7.0, 13.0], [1.05, 1.35], BLOB(3, 4, 3.6)),
         (['book-stack', 'gift', 'heart-sculpt'], 3, [4.0, 9.0], [1.4, 1.8], BLOB(3, 4, 2.0))],
 'z07': [(['book-stack', 'star-chime', 'book-stack', 'lily-lamp'], 5, [3.5, 8.0], [1.4, 2.0], BLOB(4, 6, 2.2)),
         (['bunny-house', 'mushroom-house', 'pine-lo', 'firefly-lamp'], 3, [6.0, 12.0], [1.05, 1.35], BLOB(4, 5, 3.4)),
         (['pine-lo', 'tree-lo', 'forest-clump', 'pine'], 5, [10.0, 18.0], [0.95, 1.3], BLOB(5, 8, 3.4))],
}
for z in zones:
    zk = (z['t1'] - z['t0']) / 15.12
    if z['id'] in ('z03', 'z04', 'z07'): mul(z, 0.5, ('firefly-lamp', 'gift'), None)   # v9: confetti carpets -> masses
    if z['id'] == 'z05': mul(z, 0.35, ('bunny-statue',), 'mid'); mul(z, 0.55, ('lily-lamp', 'rock', 'mushroom-group'), 'mid')   # lamp / rock carpets were the clone pairs   # user: fewer bunny statues in the lake
    for kinds, n, lat, sc, cl in MASS.get(z['id'], []):
        kinds = [k for k in kinds if k in assets]
        if not kinds: continue
        addv(z, kinds[0], max(1, round(n * zk)), lat, sc, True, cl); z['layers'][-1]['alt'] = kinds[1:] or [kinds[0]]
    if z['id'] == 'z09':   # v9: the lit village sits where the key camera looks at the shot time (tw = placement time window)
        for aid, n, lat, sc, cl in (('mushroom-house', 3, [5.5, 10.0], [1.2, 1.5], ROW(3, 4, 4.4)), ('firefly-lamp', 4, [3.5, 6.0], [1.2, 1.5], ROW(2, 3, 3.0)),
                                    ('pine-lo', 3, [10.0, 16.0], [0.9, 1.1], BLOB(4, 6, 3.2))):
            addv(z, aid, n, lat, sc, True, cl); z['layers'][-1]['tw'] = [135.4, 141.0]
            z['layers'][-1]['alt'] = {'mushroom-house': ['bunny-house'], 'firefly-lamp': ['lily-lamp'], 'pine-lo': ['tree-lo', 'forest-clump']}[aid]
# v9b: the key frames are full edge to edge; cheap mixed groves (150-300 tris a tree) and small piles fill the frame between the hero pieces
GROVE = {'z03': ['tree-lo', 'forest-clump', 'tree-bush-lo', 'pine-lo'], 'z04': ['pine-lo', 'tree-lo', 'forest-clump', 'pine-lo', 'tree-bush-lo'],
         'z05': ['tree-lo', 'pine-lo', 'tree-bush-lo', 'forest-clump'], 'z07': ['pine-lo', 'forest-clump', 'tree-lo', 'pine-lo'],
         'z09': ['pine-lo', 'tree-lo', 'forest-clump', 'pine-lo'], 'z06': ['tree-lo', 'tree-bush-lo', 'pine-lo'], 'z02': ['tree-lo', 'tree-bush-lo', 'pine-lo'],
         'z10': ['tree-lo', 'tree-bush-lo', 'forest-clump'], 'z01': ['tree-lo', 'tree-bush-lo']}
PILE = {'z03': ['book-stack', 'mushroom-group', 'gift', 'pull-tab', 'rock'], 'z04': ['book-stack', 'mushroom-group', 'heart-sculpt', 'rock'],
        'z05': ['mushroom-group', 'rock', 'lily-lamp', 'book-stack'], 'z07': ['book-stack', 'mushroom-group', 'rock', 'star-chime'],
        'z09': ['mushroom-group', 'firefly-lamp', 'book-stack', 'rock'], 'z06': ['gift', 'mushroom-group', 'rock']}
GK = {'z03': 22, 'z04': 22, 'z05': 20, 'z07': 22, 'z09': 14, 'z06': 14, 'z02': 12, 'z10': 10, 'z01': 8}
for z in zones:
    zk = (z['t1'] - z['t0']) / 15.12; zid = z['id']
    g = [k for k in GROVE.get(zid, []) if k in assets]
    if g:
        addv(z, g[0], max(1, round(GK[zid] * zk)), [6.0, 26.0], [1.0, 1.5], True, BLOB(6, 9, 4.2)); z['layers'][-1]['alt'] = g[1:]
    p = [k for k in PILE.get(zid, []) if k in assets]
    if p:
        addv(z, p[0], max(1, round(GK[zid] * zk * 0.6)), [3.0, 14.0], [1.2, 1.6], True, BLOB(3, 5, 2.4)); z['layers'][-1]['alt'] = p[1:]   # v9: piles trimmed for the tri budget
# v9c frame fill (place.ts z.fill): empty grid cells get a little mixed blob - keys read full edge to edge
FILL = {'z01': ['tree-lo', 'tulip-bed', 'tree-bush-lo', 'gift'], 'z02': ['tree-lo', 'mushroom-group', 'tree-bush-lo', 'gift', 'pine-lo'],
        'z03': ['tree-lo', 'pine-lo', 'mushroom-group', 'tree-bush-lo', 'forest-clump', 'book-stack'], 'z04': ['pine-lo', 'tree-lo', 'mushroom-group', 'forest-clump', 'pine-lo', 'tree-bush-lo'],
        'z05': ['tree-lo', 'rock', 'pine-lo', 'mushroom-group', 'tree-bush-lo', 'lily-lamp'], 'z06': ['tree-lo', 'gift', 'tree-bush-lo', 'mushroom-group'],
        'z07': ['pine-lo', 'book-stack', 'forest-clump', 'tree-lo', 'pine-lo', 'mushroom-group'], 'z08': ['pine-lo', 'gift', 'tree-lo', 'balloons'],
        'z09': ['pine-lo', 'mushroom-group', 'tree-lo', 'firefly-lamp', 'forest-clump'], 'z10': ['tree-lo', 'gift', 'tree-bush-lo', 'tulip-bed']}
FCELL = {'z03': 7.5, 'z04': 7.5, 'z05': 7.5, 'z07': 7.5, 'z09': 8.5, 'z02': 9.0, 'z06': 9.0, 'z08': 10.0, 'z01': 10.0, 'z10': 10.0}
for z in zones:
    k = [a for a in FILL.get(z['id'], []) if a in assets]
    if k: z['fill'] = dict(kinds=k, cell=FCELL[z['id']], lat=32.0, n=[2, 4], r=2.6, scale=[1.0, 1.4], free=3.8)
# v9: a kind listed twice in a mixed blob lands on the same palette variant (variants step per member mod n) -> clone pairs; dedupe
for z in zones:
    for ly in z['layers']:
        if ly.get('alt'): ly['alt'] = [a for i, a in enumerate(ly['alt']) if a != ly['asset'] and a not in ly['alt'][:i]] or ly['alt'][:1]
    if z.get('fill'): z['fill']['kinds'] = list(dict.fromkeys(z['fill']['kinds']))
for z in zones:
    if z['id'] == 'z08':   # v9: low-tier z08 <= 50k tris (road ~25k + carousel + wheel ~11k): thinner scatter, side tower high tier only
        z['lowMul'] = 0.35
        for sp in z['setpieces']:
            if not sp.get('hero'): sp['hi'] = True
SKY = {'z01': 'day', 'z02': 'day', 'z03': 'dusk', 'z04': 'night', 'z05': 'twilight', 'z06': 'dusk', 'z07': 'night', 'z08': 'night', 'z09': 'night', 'z10': 'day'}   # v8 sky strip per zone
for z in zones: z['sky'] = SKY[z['id']]
out = os.path.join(here, '..', '..', 'levels-src', 'omg', 'scene-c.json')
json.dump(spec, open(out, 'w'), ensure_ascii=False, indent=1)
n = sum(l['count'] for z in zones for l in z['layers']); print(out, 'zones', len(zones), 'assets', len(assets), 'modelled', sum(bool(a['model']) for a in assets.values()), 'scatter instances', n, 'set pieces', sum(len(z['setpieces']) for z in zones))
