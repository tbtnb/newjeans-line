# Assemble the v3 design sheets: per-zone contact sheets + overview board (images under renders/, made by Codex on the Mac mini).
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
H = Path(__file__).parent; R = H.parents[3]; sys.path.insert(0, str(H))
from zones_c import ZONES, TEXT, LAYERS, LAYER_CN, stats
RD = H / 'renders'; OUT = R / 'deliverables/omg-redesign/C'; OUT.mkdir(parents=True, exist_ok=True)
FB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; FR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f = lambda s, b=False: ImageFont.truetype(FB if b else FR, s)
BG, FG, MUT = '#191b26', '#f2f2f8', '#aeb2c8'
def fit(p, w, h):
    im = Image.open(p).convert('RGB'); s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x, y, x + w, y + h))
def wrap(d, s, font, w):
    out, cur = [], ''
    for ch in s:
        if d.textlength(cur + ch, font=font) > w: out.append(cur); cur = ch
        else: cur += ch
    return out + [cur] if cur else out
def para(d, x, y, w, title, body, fs=23, accent='#ffd27a'):
    d.text((x, y), title, font=f(fs + 1, True), fill=accent); y += fs + 12
    for ln in wrap(d, body, f(fs), w): d.text((x, y), ln, font=f(fs), fill=FG); y += fs + 9
    return y + 14
def det(z): return sorted(RD.glob(f"{z}-d*.jpg"))
for Z in ZONES:
    z, T = Z['id'], TEXT[Z['id']]; W, Hh = 2000, 1560
    img = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(img); acc = Z['pal'][1] if z in ('z04', 'z07', 'z08') else Z['pal'][0]
    d.rectangle([0, 0, W, 104], fill='#11121a'); d.rectangle([0, 100, W, 106], fill=acc)
    d.text((30, 18), f"ZONE {z[1:]} · {Z['cn']}", font=f(46, True), fill=FG)
    d.text((30 + d.textlength(f"ZONE {z[1:]} · {Z['cn']}", font=f(46, True)) + 24, 36), f"{Z['en']}  ·  {Z['key']}  ·  {Z['t0']:.1f}–{Z['t1']:.1f} s", font=f(28), fill=MUT)
    d.text((W - 30, 40), 'OMG 重设计 v3 · 方案 C「兔子立体童话书」', font=f(22), fill=MUT, anchor='ra')
    k = RD / f'{z}-key.jpg'
    if k.exists(): img.paste(fit(k, 800, 1200), (40, 136))
    X, RW = 880, 1090; y = 136
    for i, c in enumerate(Z['pal']):
        x = X + i * 218; d.rounded_rectangle([x, y, x + 204, y + 64], 10, fill=c, outline='#ffffff30')
        d.text((x + 102, y + 80), c.upper(), font=f(18), fill=MUT, anchor='mt')
    y = 250; D = det(z)
    if len(D) <= 3:
        cw, ch = 352, 235
        for i, p in enumerate(D):
            x = X + i * (cw + 17); img.paste(fit(p, cw, ch), (x, y)); d.text((x + 4, y + ch + 8), f"{i + 1}. {T['assets'][i]}", font=f(21, True), fill=FG)
        y += ch + 52
    else:
        cw, ch = 536, 300
        for i, p in enumerate(D):
            x = X + (i % 2) * (cw + 18); yy = y + (i // 2) * (ch + 44); img.paste(fit(p, cw, ch), (x, yy)); d.text((x + 4, yy + ch + 6), f"{i + 1}. {T['assets'][i]}", font=f(21, True), fill=FG)
        y += 2 * (ch + 44) + 6
    fs = 23 if len(D) <= 3 else 21
    y = para(d, X, y, RW, '路面', T['road'], fs); y = para(d, X, y, RW, '灯光 / 氛围', T['light'], fs)
    y = para(d, X, y, RW, '音乐同步', T['sync'], fs, '#ff8fc0'); y = para(d, X, y, RW, '区域过渡', T['trans'], fs, '#9fd8ff')
    pcs = '  ·  '.join(f'{t:.1f}s {n}' for t, _, n in Z['pieces']); y = para(d, X, y, RW, '蓝图布景点', pcs, fs - 2, '#c9b8f0')
    st = stats(z); d.text((X, y), f"分层元素与实例估算（全区 ≈{st['inst']} 实例 / {st['kinds']} 种网格；同屏 ≈{st['vis_inst']} 实例 · {st['vis_tris'] // 1000}k 三角面）", font=f(fs, True), fill='#9ed8c8'); y += fs + 12
    for lk, items in LAYERS[z].items():
        ln = LAYER_CN[lk] + '：' + '、'.join(f'{n}×{c}' for n, c, _ in items)
        for row in wrap(d, ln, f(fs - 2), RW): d.text((X, y), row, font=f(fs - 2), fill=FG); y += fs + 6
    # left column under the key render: road/head readability note
    d.text((40, 1420), '游戏内视角关键渲染 (Codex) · 路宽≈2.3×线宽，路两侧留 1–2 路宽净空', font=f(20), fill=MUT)
    p = OUT / f"zones-{z}-{Z['key']}.jpg"; img.save(p, quality=86); print(p.name, p.stat().st_size // 1024, 'KB', len(D), 'details')
# ---- overview board (10 zone key renders + labels)
W, Hh = 2000, 2230; img = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(img)
d.text((40, 26), 'OMG 地图重设计 v3 · 方案 C「兔子立体童话书」', font=f(52, True), fill=FG)
d.text((40, 96), '一本会弹出的童话书：每个区域是一章，翻页换景；两次 DROP（45.4s / 105.8s）巨页翻开、城堡与游乐园弹起。高密度分层布景（地被/中景/地标/天空/小动画）。', font=f(24), fill=MUT)
tw, th = 368, 552
for i, Z in enumerate(ZONES):
    x = 40 + (i % 5) * (tw + 20); y = 160 + (i // 5) * (th + 460)
    p = RD / f"{Z['id']}-key.jpg"
    if p.exists(): img.paste(fit(p, tw, th), (x, y))
    acc = Z['pal'][1] if Z['id'] in ('z04', 'z07', 'z08') else Z['pal'][0]
    d.rectangle([x, y + th, x + tw, y + th + 8], fill=acc)
    d.text((x, y + th + 18), f"{Z['id'][1:]} {Z['cn']}", font=f(28, True), fill='#ffd27a' if Z['id'] in ('z04', 'z08') else FG)
    d.text((x, y + th + 58), f"{Z['key']} · {Z['t0']:.1f}–{Z['t1']:.1f}s", font=f(20), fill=MUT)
    yy = y + th + 92
    for ln in wrap(d, TEXT[Z['id']]['sync'], f(19), tw)[:6]: d.text((x, yy), ln, font=f(19), fill=FG); yy += 27
    for c_i, c in enumerate(Z['pal']): d.rectangle([x + c_i * 40, yy + 10, x + c_i * 40 + 34, yy + 34], fill=c)
p = OUT / 'board.jpg'; img.save(p, quality=86); print(p.name, p.stat().st_size // 1024, 'KB')
