# Composite Codex renders into modeling design sheets: python3 build_sheets.py [ids...]  (inputs: <id>/hero.jpg views.jpg parts.jpg | kit.jpg front.jpg top.jpg)
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
H = Path(__file__).parent; sys.path.insert(0, str(H))
from assets_c import ASSETS, GROUND, ATLAS
FB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; FR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f = lambda s, b=False: ImageFont.truetype(FB if b else FR, s)
BG, FG, MUT, PAN = '#1c1e2a', '#f2f2f8', '#aeb2c8', (230, 230, 230)
# manual review after the automatic check (thin objects give tiny depth pixels, so the ratio test over-reacts)
REVIEW = {'P08_curtain_screen': (True, '人工复核通过：薄片物体，深度像素过小致误差偏大；俯视折线与正视一致'),
          'P21_flag_string': (True, '人工复核通过：细绳物体，深度仅数像素；俯视为直线，与正视一致'),
          'H12_flip_phone_sculpture': (True, '人工复核：俯视图带少许俯角(非纯俯视)，尺寸以正/侧视图为准'),
          'P24_paper_cloud': (True, '人工复核：俯视略扁，建模以正/侧视图为准')}
CLS = dict(hero='主件 HERO', prop='标准道具 PROP')
def mask_of(im):
    a = np.asarray(im.convert('RGB')).astype(int); b = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    bg = np.median(b, axis=0); m = np.abs(a - bg).sum(axis=2) > 36
    return m
def bbox(m):
    ys, xs = np.where(m)
    if len(xs) < 50: return None
    lo, hi = lambda v: int(np.percentile(v, 0.3)), lambda v: int(np.percentile(v, 99.7))
    return lo(xs), lo(ys), hi(xs) + 1, hi(ys) + 1
def fit(im, w, h):
    s = min(w / im.width, h / im.height); return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
def wrap(d, s, font, w):
    out, cur = [], ''
    for ch in s:
        if d.textlength(cur + ch, font=font) > w: out.append(cur); cur = ch
        else: cur += ch
    return out + [cur] if cur else out
def comps3(im):
    # three views = three biggest connected blobs (after dilation), small blobs join the nearest by x; fallback: equal thirds
    from scipy import ndimage
    m = mask_of(im); lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=5)); lab = lab * m
    areas = ndimage.sum(m, lab, range(1, n + 1)); idx = [i + 1 for i in np.argsort(-areas)[:3] if areas[i] > m.size * 0.004]
    if len(idx) < 3:
        return [(im, mask_of(im).copy() * 0) for _ in range(0)] or [(im.crop((x0, 0, x1, im.height)), mask_of(im.crop((x0, 0, x1, im.height)))) for x0, x1 in split3(im)]
    cx = {i: np.where(lab == i)[1].mean() for i in idx}; idx.sort(key=lambda i: cx[i]); groups = {i: [i] for i in idx}
    for j in range(1, n + 1):
        if j in idx or areas[j - 1] < 30: continue
        xs = np.where(lab == j)[1]
        if len(xs): groups[min(idx, key=lambda i: abs(cx[i] - xs.mean()))].append(j)
    return [(im, np.isin(lab, groups[i])) for i in idx]
def split3(im):
    # the three views are separated by empty background columns; fall back to equal thirds
    m = mask_of(im); occ = m.sum(axis=0) > 2; W = im.width; runs = []; x = 0
    while x < W:
        if occ[x]:
            s0 = x
            while x < W and (occ[x] or (x + 4 < W and occ[x:x + 4].any())): x += 1
            runs.append((s0, x))
        x += 1
    runs = [r for r in runs if r[1] - r[0] > W * 0.04]
    if len(runs) >= 3:
        runs = sorted(sorted(runs, key=lambda r: r[0] - r[1])[:3])
        cuts = [0, (runs[0][1] + runs[1][0]) // 2, (runs[1][1] + runs[2][0]) // 2, W]
        return [(cuts[i], cuts[i + 1]) for i in range(3)]
    t = W // 3; return [(0, t), (t, 2 * t), (2 * t, W)]
def nice(m):
    for v in (0.1, 0.2, 0.5, 1, 2, 5, 10):
        if m / v <= 6: return v
    return 10
def measure(path):
    vim = Image.open(path).convert('RGB'); bs = [bbox(m) for _, m in comps3(vim)]
    if None in bs or len(bs) < 3: return 9
    (fx0, fy0, fx1, fy1), (sx0, sy0, sx1, sy1), (tx0, ty0, tx1, ty1) = bs; hf, hs, wf, wt, ws, ht = fy1 - fy0, sy1 - sy0, fx1 - fx0, tx1 - tx0, sx1 - sx0, ty1 - ty0
    return max(abs(hf - hs) / max(hf, hs), abs(wf - wt) / max(wf, wt), abs(ws - ht) / max(ws, ht))
def views(a, d, img, X, Y, W, Hh, fs=20):
    cand = [p for p in (d / 'views.jpg', d / 'views2.jpg', d / 'views3.jpg') if p.exists()]; best = min(cand, key=measure)
    if best.name != 'views.jpg': Image.open(best).save(d / 'views-final.jpg', quality=90)
    vim = Image.open(best).convert('RGB'); tw = vim.width // 3
    crops, boxes = [], []
    for c, m in comps3(vim):
        b = bbox(m); crops.append((c, m)); boxes.append(b)
    if None in boxes: return None
    (fx0, fy0, fx1, fy1), (sx0, sy0, sx1, sy1), (tx0, ty0, tx1, ty1) = boxes
    wf, hf, ws, hs, wt, ht = fx1 - fx0, fy1 - fy0, sx1 - sx0, sy1 - sy0, tx1 - tx0, ty1 - ty0
    cons = dict(height=abs(hf - hs) / max(hf, hs), width=abs(wf - wt) / max(wf, wt), depth=abs(ws - ht) / max(ws, ht))
    Wt, Dt, Hm = a['size']; ratio = dict(front=(wf / hf) / (Wt / Hm), side=(ws / hs) / (Dt / Hm))
    Wm = round(Hm * wf / hf, 1); Dm = round(Hm * (ws / hs + ht / hf * (wf / wt)) / 2, 1)  # side width and top depth (top rescaled to front width) averaged
    if not 0.5 <= Wm / Wt <= 2: Wm = Wt  # thin/odd silhouettes: keep the design target
    if not 0.5 <= Dm / Dt <= 2: Dm = Dt
    # common scale: px per metre from the front view (height and width averaged), panels share it
    names = ['正视图 FRONT', '侧视图 SIDE', '俯视图 TOP']; dims = [(Wm, Hm), (Dm, Hm), (Wm, Dm)]; bx = boxes
    pw = (W - 40) // 3; ph = Hh - 50
    k = min(min((pw - 150) / (b[2] - b[0]), (ph - 100) / (b[3] - b[1])) for b in bx)
    ppm_src = (hf / Hm + wf / Wm) / 2; ppm = ppm_src * k
    for i, ((c, m), b) in enumerate(zip(crops, bx)):
        x0 = X + i * (pw + 20); y0 = Y + 40
        d_ = ImageDraw.Draw(img); d_.text((x0, Y), names[i], font=f(fs + 2, True), fill=FG)
        panel = Image.new('RGB', (pw, ph), PAN); pd = ImageDraw.Draw(panel)
        g = nice(max(Wm, Dm, Hm)) / 2 if max(Wm, Dm, Hm) > 4 else nice(max(Wm, Dm, Hm)) / 2
        step = max(6, g * ppm)
        ox = pw / 2 - (b[2] - b[0]) * k / 2 + 36; oy = ph / 2 - (b[3] - b[1]) * k / 2 - 10
        gx = ox % step; gy = (oy + (b[3] - b[1]) * k) % step
        for xx in np.arange(gx, pw, step): pd.line([(xx, 0), (xx, ph)], fill=(212, 212, 216))
        for yy in np.arange(gy, ph, step): pd.line([(0, yy), (pw, yy)], fill=(212, 212, 216))
        obj = c.crop(b).resize((max(1, round((b[2] - b[0]) * k)), max(1, round((b[3] - b[1]) * k))), Image.LANCZOS)
        mk = Image.fromarray((m[b[1]:b[3], b[0]:b[2]] * 255).astype('uint8')).resize(obj.size)
        panel.paste(obj, (round(ox), round(oy)), mk)
        # dimension lines
        L, T, R, B = ox, oy, ox + obj.width, oy + obj.height; dc = (200, 60, 110)
        pd.line([(L, B + 22), (R, B + 22)], fill=dc, width=2); pd.line([(L, B + 14), (L, B + 30)], fill=dc, width=2); pd.line([(R, B + 14), (R, B + 30)], fill=dc, width=2)
        pd.text(((L + R) / 2, B + 34), f'{dims[i][0]:g} m', font=f(fs, True), fill=dc, anchor='mt')
        pd.line([(L - 22, T), (L - 22, B)], fill=dc, width=2); pd.line([(L - 30, T), (L - 14, T)], fill=dc, width=2); pd.line([(L - 30, B), (L - 14, B)], fill=dc, width=2)
        pd.text((L - 28, (T + B) / 2), f'{dims[i][1]:g} m', font=f(fs, True), fill=dc, anchor='rm')
        img.paste(panel, (x0, y0))
    # scale bar
    sb = nice(Hm / 2); d_ = ImageDraw.Draw(img); yb = Y + 40 + ph + 14
    d_.rectangle([X, yb, X + sb * ppm, yb + 10], fill='#f2f2f8'); d_.text((X + sb * ppm + 12, yb - 6), f'比例尺 {sb:g} m · 网格 {nice(max(Wm, Dm, Hm)) / 2:g} m', font=f(fs - 2), fill=MUT)
    ok = max(cons.values()) <= 0.25; note = ''
    if a['id'] in REVIEW: ok, note = REVIEW[a['id']]
    elif not ok: note = '⚠ 俯视/侧视比例与正视不一致，建模以正视图 + 3/4 插图为准'
    d_.text((X + 520, yb - 6), f"三视图一致性：高度差 {cons['height']:.0%} · 宽度差 {cons['width']:.0%} · 深度差 {cons['depth']:.0%}  {'✓' if ok else '⚠'}", font=f(fs - 2, True), fill='#9ed8c8' if ok else '#ffb056')
    if note: d_.text((X + 520, yb + 22), note, font=f(fs - 3), fill='#ffb056' if not ok else '#9ed8c8')
    for i, (c, m) in enumerate(crops):
        b = bx[i]; c.crop((max(0, b[0] - 20), max(0, b[1] - 20), min(c.width, b[2] + 20), min(c.height, b[3] + 20))).save(d / ['front.jpg', 'side.jpg', 'top.jpg'][i], quality=88)
    return dict(consistency={k_: round(v, 3) for k_, v in cons.items()}, drawing_vs_target={k_: round(v, 2) for k_, v in ratio.items()}, ok=ok, note=note, views_file=best.name, size=[Wm, Dm, Hm])
def sheet(a):
    d = H / a['id']; W, Hh = 2400, 1600
    if not (d / 'hero.jpg').exists(): return None
    img = Image.new('RGB', (W, Hh), BG); dr = ImageDraw.Draw(img)
    acc = '#ffd27a' if a['cls'] == 'hero' else '#9fd8ff'
    dr.rectangle([0, 0, W, 104], fill='#11121a'); dr.rectangle([0, 100, W, 106], fill=acc)
    dr.text((30, 16), f"{a['id'].split('_')[0]} · {a['cn']}", font=f(48, True), fill=FG)
    dr.text((30 + dr.textlength(f"{a['id'].split('_')[0]} · {a['cn']}", font=f(48, True)) + 26, 34), f"{a['en']}  ·  {CLS[a['cls']]}  ·  区域 {', '.join(a['zones'])}", font=f(28), fill=MUT)
    dr.text((W - 30, 38), 'OMG 方案 C · 建模设计稿', font=f(24), fill=MUT, anchor='ra')
    hero = Image.open(d / 'hero.jpg').convert('RGB'); img.paste(fit(hero, 860, 860), (30, 130)); dr.text((30, 996), '3/4 主视插图 (Codex)', font=f(20), fill=MUT)
    X = 930; RW = W - X - 30
    cons = views(a, d, img, X, 128, RW, 640)
    w, dp, h = cons['size'] if cons else a['size']
    y = 1036; dr.text((30, y), f'尺寸 W×D×H：{w:g} × {dp:g} × {h:g} m（按三视图量取，高度为设定值）', font=f(26, True), fill=FG); y += 40
    dr.text((30, y), f"面数预算：≤ {a['tris']:,} 三角面（LOD1 ≈ {int(a['tris'] * 0.3):,}）", font=f(26, True), fill=FG); y += 48
    dr.text((30, y), '材质/色板槽（共享色板图集）', font=f(22, True), fill='#ffd27a'); y += 36
    for i, c in enumerate(a['colors']):
        x = 30 + (i % 6) * 142; yy = y + (i // 6) * 92; dr.rounded_rectangle([x, yy, x + 128, yy + 50], 8, fill=ATLAS[c], outline='#ffffff40')
        dr.text((x + 64, yy + 56), f'{c} {ATLAS[c]}', font=f(15), fill=MUT, anchor='mt')
    y += 92 * ((len(a['colors']) + 5) // 6) + 6
    dr.text((30, y), '枢轴 / 动画（随音乐）', font=f(22, True), fill='#ff8fc0'); y += 36
    for part, piv, mo in a['pivots']:
        for ln in wrap(dr, f'• {part}｜枢轴：{piv}｜{mo}', f(20), 860): dr.text((30, y), ln, font=f(20), fill=FG); y += 29
    # parts
    py = 850; dr.text((X, py), '细节部件 Callouts', font=f(24, True), fill=FG); py += 40
    if (d / 'parts.jpg').exists():
        pim = Image.open(d / 'parts.jpg').convert('RGB'); m = mask_of(pim); b = bbox(m)
        if b: pim = pim.crop((0, max(0, b[1] - 30), pim.width, min(pim.height, b[3] + 30)))
        pp = fit(pim, RW, 560); img.paste(pp, (X, py)); n = len(a['parts']); cw = pp.width / n
        for i, (_, cn) in enumerate(a['parts']):
            cx = X + cw * i; dr.ellipse([cx + 8, py + 8, cx + 44, py + 44], fill='#ff6fae'); dr.text((cx + 26, py + 26), str(i + 1), font=f(22, True), fill='#fff', anchor='mm')
            for j, ln in enumerate(wrap(dr, cn, f(22, True), cw - 12)): dr.text((cx + 6, py + pp.height + 10 + j * 30), ln, font=f(22, True), fill=FG)
    img.save(d / 'sheet.jpg', quality=86)
    spec = dict(id=a['id'], cn=a['cn'], en=a['en'], cls=a['cls'], zones=a['zones'], size_m=dict(w=w, d=dp, h=h), size_target_m=dict(zip('wdh', a['size'])), tris_budget=a['tris'], lod1_tris=int(a['tris'] * 0.3),
                parts=[dict(en=p[0], cn=p[1]) for p in a['parts']], pivots=[dict(part=p, pivot=q, motion=r) for p, q, r in a['pivots']],
                colors={c: ATLAS[c] for c in a['colors']}, views_check=cons, files=['sheet.jpg', 'hero.jpg', 'views.jpg', 'front.jpg', 'side.jpg', 'top.jpg', 'parts.jpg'])
    (d / 'spec.json').write_text(json.dumps(spec, ensure_ascii=False, indent=1)); return cons
def gsheet(g):
    d = H / g['id']; W, Hh = 2400, 1560
    if not (d / 'kit.jpg').exists(): return None
    img = Image.new('RGB', (W, Hh), BG); dr = ImageDraw.Draw(img)
    dr.rectangle([0, 0, W, 104], fill='#11121a'); dr.rectangle([0, 100, W, 106], fill='#9ed8c8')
    dr.text((30, 16), f"{g['id'].split('_')[0]} · {g['cn']}", font=f(48, True), fill=FG)
    dr.text((W - 30, 38), f"OMG 方案 C · 地被/小件共享设计稿 · 每件 {g['tris'][0]}–{g['tris'][1]} 面 · thin instance", font=f(24), fill=MUT, anchor='ra')
    img.paste(fit(Image.open(d / 'kit.jpg').convert('RGB'), 900, 900), (30, 130)); dr.text((30, 1040), '3/4 视图', font=f(22, True), fill=MUT)
    for i, (fn, t) in enumerate([('front.jpg', '正视图'), ('top.jpg', '俯视图')]):
        if (d / fn).exists(): img.paste(fit(Image.open(d / fn).convert('RGB'), 700, 700), (960 + i * 720, 130)); dr.text((960 + i * 720, 840), t, font=f(22, True), fill=MUT)
    y = 900; dr.text((960, y), '编号（网格顺序：左→右，上→下）', font=f(24, True), fill='#ffd27a'); y += 44
    for i, (en, cn, sz, tr) in enumerate(g['items']):
        x = 960 + (i % 2) * 720; yy = y + (i // 2) * 44
        dr.text((x, yy), f'{i + 1}. {cn}（{en}）  ≈{sz:g} m · {tr} 面', font=f(22), fill=FG)
    y = 1110; dr.text((30, y), '用法：每种一个网格 + thin instance（实例色取色板），不投影；按路线两侧条带随机撒点，RoadGrid 推开保证不压路；远处减量。', font=f(22), fill=MUT)
    img.save(d / 'sheet.jpg', quality=86)
    (d / 'spec.json').write_text(json.dumps(dict(id=g['id'], cn=g['cn'], tris_range=g['tris'], items=[dict(en=e, cn=c, size_m=s, tris=t) for e, c, s, t in g['items']],
        files=['sheet.jpg', 'kit.jpg', 'front.jpg', 'top.jpg']), ensure_ascii=False, indent=1)); return True
if __name__ == '__main__':
    want = set(sys.argv[1:]); res = {}
    for a in ASSETS:
        if not want or a['id'] in want: r = sheet(a); res[a['id']] = r; print(a['id'], r)
    for g in GROUND:
        if not want or g['id'] in want: print(g['id'], gsheet(g))
