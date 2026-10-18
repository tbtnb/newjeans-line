# Top-down blueprint of the whole OMG route (current chart on origin/rebuild) with v3 zones and set-piece placements.
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R = Path(__file__).resolve().parents[4]; sys.path.insert(0, str(R / 'tools/art')); sys.path.insert(0, str(Path(__file__).parent))
import artkit
from zones_c import ZONES, stats
L = json.loads((R / 'levels-src/omg/layout.json').read_text()); END = L['endTime']
nodes = artkit.route_from_chart(R / 'levels-src/omg/chart.json', L)
def at(t):
    for a, b in zip(nodes, nodes[1:]):
        if a[0] <= t <= b[0]:
            k = (t - a[0]) / max(1e-9, b[0] - a[0]); return a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k
    return nodes[-1][1], nodes[-1][2]
FB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; FR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f = lambda s, b=False: ImageFont.truetype(FB if b else FR, s)
zmax = at(END)[1]; ROWS = 4; seg = zmax / ROWS; S = 9.0; W = int(seg * S) + 160; RH = 560; TOP = 150
img = Image.new('RGB', (W, TOP + ROWS * RH + 40), '#1b1d2a'); d = ImageDraw.Draw(img)
d.text((40, 24), 'OMG 重设计 v3 · 方案 C「兔子立体童话书」路线蓝图（俯视，前进方向 → ）', font=f(44, True), fill='#ffffff')
d.text((40, 84), f'当前谱面 origin/rebuild · 361 拍点 · {END:.1f}s · 路线长 {zmax:.0f} m（每行 {seg:.0f} m） · 白线=路面  ◆=钻石  皇冠=金冠图标  ●n=布景主件  ▲=音乐同步时刻', font=f(24), fill='#c8cbe0')
def tx(z, row): return 80 + (z - row * seg) * S
def ty(x, row): return TOP + row * RH + RH * 0.45 - x * S
legend = []
n = 0
for row in range(ROWS):
    z0, z1 = row * seg, (row + 1) * seg
    for Z in ZONES:  # zone bands (z-ranges, the route only moves forward)
        a, b = max(at(Z['t0'])[1], z0), min(at(Z['t1'])[1], z1)
        if b <= a: continue
        c = Z['pal'][1] if Z['id'] in ('z04', 'z07', 'z08', 'z09') else Z['pal'][0]
        d.rectangle([tx(a, row), TOP + row * RH + 10, tx(b, row), TOP + row * RH + RH - 120], fill=tuple(int(c[i:i + 2], 16) // 3 + 20 for i in (1, 3, 5)))
        d.rectangle([tx(a, row), TOP + row * RH + 10, tx(b, row), TOP + row * RH + 52], fill=c)
        d.text((tx(a, row) + 8, TOP + row * RH + 14), f"{Z['id'][1:]} {Z['cn']} · ≈{stats(Z['id'])['inst']} 实例", font=f(22, True), fill='#1b1d2a' if sum(int(c[i:i + 2], 16) for i in (1, 3, 5)) > 360 else '#ffffff')
    pts = []
    t = 0.0
    while t <= END:
        x, z = at(t)
        if z0 - 1 <= z <= z1 + 1: pts.append((tx(z, row), ty(x, row)))
        t += 0.02
    if len(pts) > 1:
        d.line(pts, fill='#555a70', width=int(2.6 * S) + 4); d.line(pts, fill='#ffffff', width=int(2.2 * S))
    for Z in ZONES:
        for (t, side, name) in Z['pieces']:
            x, z = at(t)
            if not (z0 <= z < z1): continue
            n += 1; legend.append((n, t, Z['cn'], name))
            if side == 0:
                px, py = tx(z, row), ty(x, row) - 4.5 * S
                d.polygon([(px, py - 16), (px - 14, py + 10), (px + 14, py + 10)], fill='#ffd27a', outline='#1b1d2a')
                d.text((px + 16, py - 18), str(n), font=f(22, True), fill='#ffd27a')
            else:
                px, py = tx(z, row), ty(x + side * 12, row)
                d.line([(tx(z, row), ty(x + side * 2, row)), (px, py)], fill='#ffffff88', width=2)
                d.ellipse([px - 17, py - 17, px + 17, py + 17], fill='#ff5fa8', outline='#ffffff', width=3)
                d.text((px, py), str(n), font=f(20, True), fill='#ffffff', anchor='mm')
    for dm in L['diamonds']:
        x, z = at(dm['t'])
        if z0 <= z < z1:
            px, py = tx(z, row), ty(x, row); d.polygon([(px, py - 9), (px + 7, py), (px, py + 9), (px - 7, py)], fill='#5fd8ff', outline='#1b1d2a')
    for cr in L['crowns']:
        x, z = at(cr['t'])
        if z0 <= z < z1:
            px, py = tx(z, row), ty(x, row); d.polygon([(px - 13, py + 9), (px - 15, py - 9), (px - 6, py - 1), (px, py - 13), (px + 6, py - 1), (px + 15, py - 9), (px + 13, py + 9)], fill='#ffd27a', outline='#1b1d2a')
    # time ticks every 10 s
    for tt in range(0, int(END) + 1, 10):
        x, z = at(tt)
        if z0 <= z < z1:
            d.line([(tx(z, row), TOP + row * RH + RH - 118), (tx(z, row), TOP + row * RH + RH - 104)], fill='#c8cbe0', width=2)
            d.text((tx(z, row), TOP + row * RH + RH - 100), f'{tt}s', font=f(18), fill='#c8cbe0', anchor='mt')
    # legend for this row
    items = [l for l in legend if z0 <= at(l[1])[1] < z1]
    lx, ly = 80, TOP + row * RH + RH - 72
    for (k, t, zc, name) in items:
        s = f'{k}. {t:.1f}s {name}'; w = d.textlength(s, font=f(19)) + 26
        if lx + w > W - 40: lx = 80; ly += 28
        d.text((lx, ly), s, font=f(19), fill='#e8e8f4'); lx += w
img.save(R / 'deliverables/omg-redesign/C/blueprint.png', optimize=False)
print(img.size, n)
