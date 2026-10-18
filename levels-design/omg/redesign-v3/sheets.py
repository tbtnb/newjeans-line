# Assemble the v3 design sheets: per-zone contact sheets + overview board (images under renders/, made by Codex on the Mac mini).
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
H = Path(__file__).parent; R = H.parents[2]; sys.path.insert(0, str(H))
from zones_v3 import ZONES, TEXT
RD = H / 'renders'; OUT = R / 'deliverables/omg-redesign'; OUT.mkdir(parents=True, exist_ok=True)
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
    z, T = Z['id'], TEXT[Z['id']]; W, Hh = 2000, 1400
    img = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(img); acc = Z['pal'][1] if z in ('z04', 'z08') else Z['pal'][0]
    d.rectangle([0, 0, W, 104], fill='#11121a'); d.rectangle([0, 100, W, 106], fill=acc)
    d.text((30, 18), f"ZONE {z[1:]} · {Z['cn']}", font=f(46, True), fill=FG)
    d.text((30 + d.textlength(f"ZONE {z[1:]} · {Z['cn']}", font=f(46, True)) + 24, 36), f"{Z['en']}  ·  {Z['key']}  ·  {Z['t0']:.1f}–{Z['t1']:.1f} s", font=f(28), fill=MUT)
    d.text((W - 30, 40), 'OMG 重设计 v3 · 方案 A「粉彩病院·五个白日梦」', font=f(22), fill=MUT, anchor='ra')
    k = RD / f'{z}-key.jpg'
    if k.exists(): img.paste(fit(k, 800, 1200), (40, 136))
    d.text((40, 1380), '游戏内视角关键渲染 (Codex)', font=f(18), fill=MUT, anchor='ls')
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
    pcs = '  ·  '.join(f'{t:.1f}s {n}' for t, _, n in Z['pieces']); para(d, X, y, RW, '蓝图布景点', pcs, fs - 2, '#c9b8f0')
    p = OUT / f"zones-{z}-{Z['key']}.jpg"; img.save(p, quality=86); print(p.name, p.stat().st_size // 1024, 'KB', len(D), 'details')
# ---- overview board
W, Hh = 2000, 1720; img = Image.new('RGB', (W, Hh), BG); d = ImageDraw.Draw(img)
d.text((40, 26), 'OMG 地图重设计 v3 · 总览', font=f(52, True), fill=FG)
d.text((40, 96), '三个整体概念（Codex 关键渲染，游戏内视角）→ 推荐方案 A；下排为方案 A 的十个区域', font=f(26), fill=MUT)
C = [('concept-a', 'A 粉彩病院·五个白日梦', '病院为底色，墙板翻开即进入五位病人的幻想（黑兔舞台/玻璃鞋/手机/屏幕/书页）。最贴合 MV 叙事，区域变化最丰富。', True),
     ('concept-b', 'B 翻盖手机宇宙', '整关在一部 Y2K 翻盖手机内部：电路板地形、按键广场、屏幕天空。风格统一、科技感强，但叙事单一。', False),
     ('concept-c', 'C 兔子立体童话书', '从巨大书页中弹出的纸艺低多边形花园。温柔漂亮，但和 MV 的病院喜剧关联较弱。', False)]
for i, (n, title, desc, rec) in enumerate(C):
    x = 40 + i * 650; y = 160; p = RD / f'{n}.jpg'
    if p.exists(): img.paste(fit(p, 610, 915), (x, y))
    if rec:
        d.rectangle([x - 6, y - 6, x + 616, y + 921], outline='#ffd27a', width=6)
        d.rounded_rectangle([x + 14, y + 14, x + 190, y + 62], 12, fill='#ffd27a'); d.text((x + 102, y + 38), '★ 推荐', font=f(28, True), fill='#191b26', anchor='mm')
    d.text((x, y + 935), title, font=f(32, True), fill='#ffd27a' if rec else FG)
    yy = y + 985
    for ln in wrap(d, desc, f(21), 610): d.text((x, yy), ln, font=f(21), fill=MUT); yy += 30
y = 1250; d.text((40, y), '方案 A · 十个区域（点开 zones-*.jpg 看细节）', font=f(28, True), fill=FG); y += 50
tw, th = 184, 276
for i, Z in enumerate(ZONES):
    x = 40 + i * (tw + 7.6); p = RD / f"{Z['id']}-key.jpg"
    if p.exists(): img.paste(fit(p, tw, th), (int(x), y))
    d.text((int(x) + 4, y + th + 8), f"{Z['id'][1:]} {Z['cn']}", font=f(19, True), fill=FG)
    d.text((int(x) + 4, y + th + 36), f"{Z['t0']:.0f}–{Z['t1']:.0f}s", font=f(17), fill=MUT)
p = OUT / 'board.jpg'; img.save(p, quality=86); print(p.name, p.stat().st_size // 1024, 'KB')
