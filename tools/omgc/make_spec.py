#!/usr/bin/env python3
"""Generate levels-src/omg/scene-c.json (concept C placement spec) from the design data zones_c.py (branch omg-design-v3).
Everything is relative to the route by time t and side, so it survives re-charts. usage: make_spec.py [path/to/zones_c.py]"""
import json, sys, importlib.util, os
src = sys.argv[1] if len(sys.argv) > 1 else '/workspace/nj-design-v3/levels-design/omg/redesign-v3/C/zones_c.py'
sp = importlib.util.spec_from_file_location('zones_c', src); Z = importlib.util.module_from_spec(sp); sp.loader.exec_module(Z)

# element name (design) -> asset id, placeholder shape, height m. model=True when tools/models/assets/<id>.py exists.
A = {
 '纸草丛': ('grass', 'tuft', 0.45), '纸草丛(夜)': ('grass', 'tuft', 0.45), '小纸花': ('flower', 'flower', 0.2), '小纸花(夜光)': ('flower', 'flower', 0.2), '小纸花(夜)': ('flower', 'flower', 0.2),
 '爱心小花': ('flower-heart', 'flower', 0.22), '卵石': ('pebble', 'ico', 0.17), '石板': ('slab', 'box', 0.08), '苔石': ('pebble', 'ico', 0.2), '岸边纸石': ('rock', 'ico', 0.6),
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
LAYER = {
 'ground': dict(near=[0.4, 16.0], y=[0, 0]),
 'mid':    dict(near=[3.0, 10.0], y=[0, 0]),
 'land':   dict(near=[10.0, 25.0], y=[0, 0]),
 'sky':    dict(near=[12.0, 45.0], y=[7, 22]),
 'anim':   dict(near=[1.5, 14.0], y=[1.0, 6.0]),
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
here = os.path.dirname(os.path.abspath(__file__)); models = os.path.join(here, '..', 'models', 'assets')
assets = {}; zones = []
for z in Z.ZONES:
    zid = z['id']; layers = []
    for layer, items in Z.LAYERS[zid].items():
        for name, count, tris in items:
            aid, shape, h = A[name]
            a = assets.setdefault(aid, dict(layer=layer, shape=shape, h=h, tris=tris, model=os.path.exists(os.path.join(models, aid + '.py')), names=[]))
            if name not in a['names']: a['names'].append(name)
            a['tris'] = max(a['tris'], tris)
            if layer == 'land': continue   # landmarks are placed as set pieces below
            L = LAYER[layer]; near = list(L['near'])
            if shape == 'far': near = [55.0, 90.0]
            layers.append(dict(asset=aid, layer=layer, count=count, near=near, y=L['y'], scale=[0.8, 1.25], colors=[0, 1, 2, 3, 4]))
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
        sets.append(dict(t=t, side=side, asset=aid, dist=12.0 if is_land else 5.0, scale=1.0, pop='spring', label=label))
    rest = list(land)
    for u in used:
        if u in rest: rest.remove(u)
    for k, aid in enumerate(rest):
        t = z['t0'] + (k + 0.6) / (len(rest) + 0.4) * (z['t1'] - z['t0'])
        sets.append(dict(t=round(t, 2), side=1 if (len(sets) + k) % 2 == 0 else -1, asset=aid, dist=14.0, scale=1.0, pop='spring', label='landmark'))
    sets.sort(key=lambda d: d['t'])
    for i in range(len(sets) - 1):   # two big pieces within 3 s never share a side
        if sets[i + 1]['t'] - sets[i]['t'] < 3 and sets[i + 1]['side'] == sets[i]['side']: sets[i]['side'] *= -1
    moments = [dict(t=t, label=label) for t, side, label in z['pieces'] if side == 0]
    zones.append(dict(id=zid, key=z['key'], t0=z['t0'], t1=z['t1'], name=z['cn'], colors=z['pal'], palette=PAL[zid], layers=layers, setpieces=sets, moments=moments))
spec = dict(version=1, source='levels-design/omg/redesign-v3/C/zones_c.py (omg-design-v3)', chunk=20, window=dict(behind=3, ahead=8),
            clear=dict(ground=0.3, groundMaxH=0.3, near=1.0), assets=assets, zones=zones)
# design asset sheets (levels-design/omg/redesign-v3/C/assets/<design id>/spec.json): their size / tri budget win over the table
DESIGN_IDS = {'castle': 'H01_popup_castle', 'bunny-heart': 'H02_giant_bunny_heart', 'carousel': 'H03_bunny_carousel', 'ferris-wheel': 'H04_heart_ferris_wheel',
 'lantern-tower': 'H05_lantern_tower', 'heart-gate': 'H06_heart_finish_gate', 'bunny-family': 'H07_bunny_family', 'cannon': 'H08_confetti_cannon',
 'book-cover': 'H09_book_cover', 'ward-bed': 'H10_ward_bed_set', 'clock-tower': 'H11_clock_tower', 'flip-phone': 'H12_flip_phone_sculpture',
 'phone-tower': 'H13_phone_tower', 'spiral-tower': 'H14_spiral_paper_tower', 'paper-boat': 'H15_bunny_sail_boat', 'pavilion': 'H16_lake_pavilion',
 'windmill': 'H17_bunny_windmill', 'reading-bunny': 'H18_reading_bunny', 'sun': 'H19_paper_sun', 'bunny-house': 'P01_bunny_cottage',
 'mushroom-house': 'P02_mushroom_house', 'tulip-bed': 'P03_tulip_bed', 'tree': 'P04_paper_tree_round', 'pine': 'P05_paper_pine', 'bunny-statue': 'P06_sitting_bunny',
 'iv-heart': 'P07_heart_iv_stand', 'screen': 'P08_curtain_screen', 'pull-tab': 'P09_pull_tab', 'lantern-string': 'P10_lantern_string', 'heart-sculpt': 'P11_heart_sculpture', 'gift': 'P12_gift_box'}
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
            seen = True; sp['t'] = 153.5
        keep.append(sp)
    z['setpieces'] = keep
out = os.path.join(here, '..', '..', 'levels-src', 'omg', 'scene-c.json')
json.dump(spec, open(out, 'w'), ensure_ascii=False, indent=1)
n = sum(l['count'] for z in zones for l in z['layers']); print(out, 'zones', len(zones), 'assets', len(assets), 'modelled', sum(a['model'] for a in assets.values()), 'scatter instances', n, 'set pieces', sum(len(z['setpieces']) for z in zones))
