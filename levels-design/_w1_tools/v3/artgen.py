"""Procedural flat-illustration art (fallback/complement to GenerateImage): sky backdrops, halftone ground tiles,
bunny murals (2022 EP motif, cartoon bunny only - no human faces), sticker decals, posters. All PIL, deterministic."""
from PIL import Image, ImageDraw, ImageFilter
import math, random, os
def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
def mix(a, b, f): return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))
def save(im, dst, q=86):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if dst.endswith('.png'): im.save(dst, optimize=True)
    else: im.convert('RGB').save(dst, quality=q, optimize=True)
    return os.path.getsize(dst)
def sky(dst, top, bottom, dots=None, clouds=6, seed=1, W=1600, H=900, sun=None):
    top, bottom = hx(top), hx(bottom); im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=mix(top, bottom, (y / H) ** 0.9))
    if sun:
        g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); sx, sy, r, col = sun
        for k in range(30, 0, -1): gd.ellipse([sx - r * k / 10, sy - r * k / 10, sx + r * k / 10, sy + r * k / 10], fill=hx(col) + (int(7 + 2 * (30 - k) / 3),))
        im = Image.alpha_composite(im.convert('RGBA'), g.filter(ImageFilter.GaussianBlur(20))).convert('RGB'); d = ImageDraw.Draw(im)
    if dots:
        col = hx(dots)
        for y in range(0, int(H * 0.45), 18):
            for x in range(0, W, 18):
                f = (1 - y / (H * 0.45)) * (0.35 + 0.65 * abs(x - W / 2) / (W / 2))
                r = 3.2 * f
                if r > 0.5: d.ellipse([x - r, y - r, x + r, y + r], fill=mix(mix(top, bottom, y / H), col, 0.35))
    rnd = random.Random(seed); cl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(cl)
    for _ in range(clouds):
        cx, cy, s = rnd.uniform(0, W), rnd.uniform(H * 0.35, H * 0.85), rnd.uniform(60, 150)
        for k in range(5):
            ox, oy, rr = rnd.uniform(-1.3, 1.3) * s, rnd.uniform(-0.3, 0.2) * s, rnd.uniform(0.45, 0.8) * s
            cd.ellipse([cx + ox - rr, cy + oy - rr * 0.6, cx + ox + rr, cy + oy + rr * 0.6], fill=(255, 255, 255, 150))
    im = Image.alpha_composite(im.convert('RGBA'), cl.filter(ImageFilter.GaussianBlur(6))).convert('RGB')
    return save(im, dst)
def dots_tile(dst, base, dot, n=8, S=512, r=6, stagger=True):
    im = Image.new('RGB', (S, S), hx(base)); d = ImageDraw.Draw(im); step = S / n
    for j in range(n):
        for i in range(n):
            x = (i + (0.5 if stagger and j % 2 else 0)) * step + step / 4; y = j * step + step / 4
            for ox in (-S, 0, S):
                d.ellipse([x + ox - r, y - r, x + ox + r, y + r], fill=hx(dot))
    return save(im, dst)
def stripes_tile(dst, a, b, S=512, n=8, diag=True):
    im = Image.new('RGB', (S, S), hx(a)); d = ImageDraw.Draw(im); w = S / n
    for k in range(-n, 2 * n):
        if k % 2: continue
        x = k * w
        d.polygon([(x, 0), (x + w, 0), (x + w + (S if diag else 0), S), (x + (S if diag else 0), S)], fill=hx(b))
    return save(im, dst)
def bunny(d, cx, cy, s, white, ink, cheek='#F2A7B5', arms=True, smile=True):
    W_, I = hx(white), hx(ink)
    for sx in (-1, 1):  # ears
        d.rounded_rectangle([cx + sx * 0.32 * s - 0.15 * s, cy - 1.25 * s, cx + sx * 0.32 * s + 0.15 * s, cy - 0.35 * s], radius=0.15 * s, fill=W_, outline=I, width=max(2, int(s * 0.04)))
        d.rounded_rectangle([cx + sx * 0.32 * s - 0.07 * s, cy - 1.12 * s, cx + sx * 0.32 * s + 0.07 * s, cy - 0.5 * s], radius=0.07 * s, fill=hx('#BFD3F5'))
    if arms:
        for sx in (-1, 1):
            d.rounded_rectangle([min(cx + sx * 0.4 * s, cx + sx * 1.15 * s), cy + 0.25 * s, max(cx + sx * 0.4 * s, cx + sx * 1.15 * s), cy + 0.5 * s], radius=0.12 * s, fill=W_, outline=I, width=max(2, int(s * 0.04)))
    d.ellipse([cx - 0.62 * s, cy - 0.5 * s, cx + 0.62 * s, cy + 0.55 * s], fill=W_, outline=I, width=max(2, int(s * 0.05)))
    for sx in (-1, 1):
        d.ellipse([cx + sx * 0.24 * s - 0.11 * s, cy - 0.12 * s, cx + sx * 0.24 * s + 0.11 * s, cy + 0.12 * s], fill=I)
        d.ellipse([cx + sx * 0.24 * s - 0.04 * s, cy - 0.08 * s, cx + sx * 0.24 * s + 0.03 * s, cy - 0.01 * s], fill=W_)
        d.ellipse([cx + sx * 0.42 * s - 0.09 * s, cy + 0.12 * s, cx + sx * 0.42 * s + 0.09 * s, cy + 0.24 * s], fill=hx(cheek))
    d.polygon([(cx - 0.06 * s, cy + 0.1 * s), (cx + 0.06 * s, cy + 0.1 * s), (cx, cy + 0.17 * s)], fill=I)
    if smile: d.chord([cx - 0.16 * s, cy + 0.1 * s, cx + 0.16 * s, cy + 0.4 * s], 0, 180, fill=I)
def mural(dst, bg, white, ink, dots=True, W=1024, H=1024, s=300):
    im = Image.new('RGB', (W, H), hx(bg)); d = ImageDraw.Draw(im)
    if dots:
        for y in range(0, H, 22):
            for x in range(0, W, 22):
                r = 2 + 3.5 * (math.hypot(x - W / 2, y - H / 2) / (W * 0.7))
                d.ellipse([x - r, y - r, x + r, y + r], fill=mix(hx(bg), hx(white), 0.55))
    bunny(d, W / 2, H * 0.56, s, white, ink)
    return save(im, dst)
def shape_heart(d, cx, cy, s, fill):
    pts = [(cx + s * 16 * math.sin(t) ** 3 / 17, cy - s * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17) for t in [k * 2 * math.pi / 120 for k in range(120)]]
    d.polygon(pts, fill=fill)
def shape_star(d, cx, cy, s, fill, n=5):
    pts = [(cx + (s if k % 2 == 0 else s * 0.45) * math.sin(k * math.pi / n), cy - (s if k % 2 == 0 else s * 0.45) * math.cos(k * math.pi / n)) for k in range(2 * n)]
    d.polygon(pts, fill=fill)
def sticker(dst, kind, col, col2='#FFFFFF', S=256):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); m = Image.new('L', (S, S), 0); md = ImageDraw.Draw(m)
    def draw(dd, scale, fill, fill2):
        c = S / 2; s = S * 0.36 * scale
        if kind == 'heart': shape_heart(dd, c, c, s * 1.15, fill)
        elif kind == 'star': shape_star(dd, c, c, s * 1.15, fill)
        elif kind == 'circle': dd.ellipse([c - s, c - s, c + s, c + s], fill=fill)
        elif kind == 'bunny':
            dd.ellipse([c - s * 0.8, c - s * 0.25, c + s * 0.8, c + s * 0.95], fill=fill)
            for sx in (-1, 1): dd.rounded_rectangle([c + sx * s * 0.38 - s * 0.2, c - s * 1.15, c + sx * s * 0.38 + s * 0.2, c + s * 0.1], radius=s * 0.2, fill=fill)
        elif kind == 'cookie':
            dd.ellipse([c - s, c - s, c + s, c + s], fill=fill)
        elif kind == 'cd':
            dd.ellipse([c - s, c - s, c + s, c + s], fill=fill)
        elif kind == 'window':
            dd.rounded_rectangle([c - s * 0.7, c - s, c + s * 0.7, c + s], radius=s * 0.5, fill=fill)
        elif kind == 'phone':
            dd.rounded_rectangle([c - s * 0.5, c - s, c + s * 0.5, c + s], radius=s * 0.2, fill=fill)
        elif kind == 'drop':
            dd.ellipse([c - s * 0.7, c - s * 0.1, c + s * 0.7, c + s * 1.0], fill=fill); dd.polygon([(c - s * 0.62, c + s * 0.3), (c + s * 0.62, c + s * 0.3), (c, c - s)], fill=fill)
    draw(md, 1.18, 255, 255)
    outline = Image.new('RGBA', (S, S), (255, 255, 255, 255)); im.paste(outline, (0, 0), m.filter(ImageFilter.GaussianBlur(1)))
    d = ImageDraw.Draw(im); draw(d, 1.0, hx(col) + (255,), hx(col2) + (255,))
    c = S / 2; s = S * 0.36
    if kind == 'bunny':
        for sx in (-1, 1): d.ellipse([c + sx * s * 0.3 - s * 0.09, c + s * 0.28, c + sx * s * 0.3 + s * 0.09, c + s * 0.46], fill=hx(col2))
    if kind == 'cookie':
        for (ox, oy) in [(-0.4, -0.3), (0.35, -0.4), (0.1, 0.2), (-0.35, 0.45), (0.5, 0.35)]: d.ellipse([c + ox * s - s * 0.1, c + oy * s - s * 0.1, c + ox * s + s * 0.1, c + oy * s + s * 0.1], fill=hx(col2))
    if kind == 'cd':
        d.ellipse([c - s * 0.25, c - s * 0.25, c + s * 0.25, c + s * 0.25], fill=hx(col2)); d.ellipse([c - s * 0.08, c - s * 0.08, c + s * 0.08, c + s * 0.08], fill=(0, 0, 0, 0))
        d.arc([c - s * 0.75, c - s * 0.75, c + s * 0.75, c + s * 0.75], 200, 260, fill=(255, 255, 255, 200), width=int(s * 0.08))
    if kind == 'window':
        d.rectangle([c - s * 0.5, c - s * 0.55, c + s * 0.5, c + s * 0.8], fill=hx(col2)); d.line([(c, c - s * 0.55), (c, c + s * 0.8)], fill=hx(col), width=int(s * 0.1)); d.line([(c - s * 0.5, c + s * 0.12), (c + s * 0.5, c + s * 0.12)], fill=hx(col), width=int(s * 0.1))
    if kind == 'phone':
        d.rectangle([c - s * 0.38, c - s * 0.8, c + s * 0.38, c + s * 0.1], fill=hx(col2))
        for k, cc in enumerate(['#FF7185', '#F8CB56', '#57CDD1', '#8FA2F0', '#FFFFFF']): d.rectangle([c - s * 0.3 + k * s * 0.13, c - s * 0.3, c - s * 0.2 + k * s * 0.13, c - s * 0.2], fill=hx(cc))
    if kind == 'circle':
        shape_star(d, c, c, s * 0.5, hx(col2) + (255,))
    return save(im, dst)
def poster(dst, bg, fg, motif='bunny', W=768, H=1024, accent='#FFFFFF'):
    im = Image.new('RGB', (W, H), hx(bg)); d = ImageDraw.Draw(im)
    for k in range(9): d.rectangle([0, k * H / 9, W, k * H / 9 + 6], fill=mix(hx(bg), hx(fg), 0.18))
    if motif == 'bunny': bunny(d, W / 2, H * 0.55, 230, '#FFFFFF', fg)
    elif motif == 'frames':
        for k in range(5):
            x0 = 70 + k * 130; d.rectangle([x0, 300 + (k % 2) * 80, x0 + 100, 520 + (k % 2) * 80], outline=hx(fg), width=10)
    elif motif == 'pool':
        for k in range(6): d.arc([W / 2 - 60 * k - 60, H * 0.6 - 30 * k - 30, W / 2 + 60 * k + 60, H * 0.6 + 30 * k + 30], 0, 360, fill=hx(accent), width=6)
        bunny(d, W / 2, H * 0.32, 120, '#FFFFFF', fg, arms=False)
    elif motif == 'cd':
        for r, cc in [(300, fg), (210, accent), (70, bg)]: d.ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=hx(cc))
        bunny(d, W / 2, H / 2 + 30, 60, '#FFFFFF', fg, arms=False)
    return save(im, dst)
