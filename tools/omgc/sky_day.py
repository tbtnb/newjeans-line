"""v8 day / dusk / twilight sky strips (screen-top band like sky-night.webp): pastel gradient (opaque top, clear bottom), layered
paper-cut clouds, a paper sun (or moon for twilight) and a pastel silhouette skyline (houses, towers, windmill, castle) -> public/models/omg-c/paint/sky-<kind>.webp"""
import random, math, sys
from PIL import Image, ImageDraw, ImageFilter
W, H = 1024, 384
K = {
 'day':      dict(top=(150, 205, 245), bot=(255, 232, 214), cloud=[(255, 255, 255), (246, 238, 250), (255, 236, 240)], sun=(255, 214, 110), ray=(255, 232, 160), sil=[(196, 214, 236), (228, 206, 230), (214, 232, 214)], win=(255, 246, 220), body='sun'),
 'dusk':     dict(top=(186, 160, 226), bot=(255, 196, 170), cloud=[(255, 226, 214), (250, 206, 214), (255, 240, 226)], sun=(255, 186, 110), ray=(255, 214, 160), sil=[(214, 160, 196), (196, 150, 200), (232, 176, 186)], win=(255, 226, 160), body='sun'),
 'twilight': dict(top=(120, 136, 196), bot=(222, 206, 246), cloud=[(236, 226, 252), (214, 206, 246), (250, 230, 246)], sun=(255, 238, 190), ray=(255, 230, 170), sil=[(150, 150, 206), (170, 156, 214), (140, 160, 200)], win=(255, 222, 150), body='moon'),
}
def build(kind, seed=11):
    c = K[kind]; random.seed(seed)
    im = Image.new('RGBA', (W, H)); px = im.load()
    for y in range(H):
        k = y / H; a = 255 if k < 0.55 else int(255 * max(0, 1 - (k - 0.55) / 0.45) ** 1.6)
        col = tuple(int(c['top'][i] + (c['bot'][i] - c['top'][i]) * min(1, k / 0.72)) for i in range(3))
        for x in range(W): px[x, y] = (*col, a)
    d = ImageDraw.Draw(im)
    sx, sy, sr = 800, 74, 40
    glow = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(glow); g.ellipse([sx - sr * 2.6, sy - sr * 2.6, sx + sr * 2.6, sy + sr * 2.6], fill=(*c['ray'], 110)); glow = glow.filter(ImageFilter.GaussianBlur(26)); im.alpha_composite(glow); d = ImageDraw.Draw(im)
    if c['body'] == 'sun':   # paper sun: 16 folded rays (two tones) + faceted disc
        for i in range(16):
            a0 = i * math.pi / 8; L = sr * (1.75 if i % 2 else 1.5); w = 0.17
            pts = [(sx + math.cos(a0 - w) * sr * 0.9, sy + math.sin(a0 - w) * sr * 0.9), (sx + math.cos(a0) * L, sy + math.sin(a0) * L), (sx + math.cos(a0 + w) * sr * 0.9, sy + math.sin(a0 + w) * sr * 0.9)]
            d.polygon(pts, fill=(*(c['ray'] if i % 2 else c['sun']), 255))
        for i in range(12):   # faceted disc: alternating wedge tones
            a0, a1 = i * math.pi / 6, (i + 1) * math.pi / 6; t = 1.0 if i % 2 else 0.93
            d.polygon([(sx, sy), (sx + math.cos(a0) * sr, sy + math.sin(a0) * sr), (sx + math.cos(a1) * sr, sy + math.sin(a1) * sr)], fill=tuple(int(v * t) for v in c['sun']) + (255,))
    else:   # twilight: crescent moon + a few stars
        m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m); md.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=255); md.ellipse([sx - sr + 18, sy - sr - 8, sx + sr + 18, sy + sr - 8], fill=0)
        im.paste(Image.new('RGBA', (W, H), (*c['sun'], 255)), (0, 0), m); d = ImageDraw.Draw(im)
        for _ in range(60):
            x, y, r = random.uniform(0, W), random.uniform(0, H * 0.42), random.choice([1, 1, 1.5, 2])
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 248, 226, random.randint(150, 240)))
    def cloud(cx, cy, s, col):   # layered paper puffs: flat underside, 5-7 circles, darker under-layer offset
        under = tuple(int(v * 0.9) for v in col)
        n = random.randint(5, 7); pts = [(cx + (i - (n - 1) / 2) * s * 0.5 + random.uniform(-4, 4), cy - s * (0.15 + 0.75 * (1 - abs(i - (n - 1) / 2) / ((n - 1) / 2 + 0.5)) ** 1.2) + random.uniform(-4, 4)) for i in range(n)]
        for (x, y) in pts: r = s * random.uniform(0.42, 0.6); d.ellipse([x - r + 4, y - r + 6, x + r + 4, y + r + 6], fill=(*under, 255))
        d.rectangle([pts[0][0] + 4, cy - s * 0.1 + 6, pts[-1][0] + 4, cy + s * 0.32 + 6], fill=(*under, 255))
        for (x, y) in pts: r = s * random.uniform(0.42, 0.6); d.ellipse([x - r, y - r, x + r, y + r], fill=(*col, 255))
        d.rectangle([pts[0][0], cy - s * 0.1, pts[-1][0], cy + s * 0.3], fill=(*col, 255))
    for cx, cy, s in ((90, 70, 46), (300, 120, 38), (520, 60, 52), (640, 150, 30), (960, 140, 40), (180, 170, 28), (420, 190, 26)):
        cloud(cx + random.uniform(-20, 20), cy, s, random.choice(c['cloud']))
    base = int(H * 0.74); x = -10; castled = [False]
    for layer in (0, 1):   # two pastel skyline layers (far lighter, near deeper)
        x = -10 - layer * 20; sil = (*c['sil'][layer], 255) if layer == 0 else (*tuple(int(v * 0.86) for v in c['sil'][1]), 255); b = base - (14 if layer == 0 else 0)
        while x < W:
            kind2 = random.random(); w = random.randint(24, 52); h = random.randint(20, 56) + (16 if layer == 0 else 0)
            if 400 < x < 560 and layer == 1 and not castled[0]: kind2 = 0.95; castled[0] = True
            elif kind2 >= 0.9: kind2 = random.random() * 0.9
            if kind2 < 0.5:   # house + pointed roof, round window
                d.rectangle([x, b - h, x + w, b + 40], fill=sil); d.polygon([(x - 4, b - h), (x + w / 2, b - h - w * 0.62), (x + w + 4, b - h)], fill=sil)
                if layer: d.ellipse([x + w / 2 - 4, b - h + 10, x + w / 2 + 4, b - h + 18], fill=(*c['win'], 255))
            elif kind2 < 0.68:   # windmill
                tw = 16; d.polygon([(x, b + 40), (x + 4, b - h - 26), (x + tw - 4, b - h - 26), (x + tw, b + 40)], fill=sil); hx, hy = x + tw / 2, b - h - 26
                for i in range(4): a0 = i * math.pi / 2 + 0.4; d.polygon([(hx, hy), (hx + math.cos(a0) * 34 - math.sin(a0) * 5, hy + math.sin(a0) * 34 + math.cos(a0) * 5), (hx + math.cos(a0) * 34, hy + math.sin(a0) * 34)], fill=sil)
                w = tw + 8
            elif kind2 < 0.9:   # tower + cone + flag
                tw = max(14, w // 2); th = h + random.randint(24, 50); d.rectangle([x, b - th, x + tw, b + 40], fill=sil); d.polygon([(x - 5, b - th), (x + tw / 2, b - th - 32), (x + tw + 5, b - th)], fill=sil)
                d.polygon([(x + tw / 2, b - th - 32), (x + tw / 2 + 12, b - th - 28), (x + tw / 2, b - th - 24)], fill=sil); w = tw
            else:   # castle block
                cw = 140; d.rectangle([x, b - 56, x + cw, b + 40], fill=sil)
                for tx, th in ((x - 6, 100), (x + 38, 130), (x + 90, 115), (x + cw - 16, 92)):
                    d.rectangle([tx, b - th, tx + 22, b], fill=sil); d.polygon([(tx - 6, b - th), (tx + 11, b - th - 36), (tx + 28, b - th)], fill=sil)
                w = cw
            x += w + random.randint(4, 26)
    d.rectangle([0, base + 6, W, H], fill=(0, 0, 0, 0))
    fade = Image.new('L', (W, H), 0); fd = fade.load()
    for y in range(H):
        v = 255 if y < base - 4 else max(0, int(255 * (1 - (y - base + 4) / 10)))
        for x2 in range(W): fd[x2, y] = v
    r, g2, b2, a = im.split(); a = Image.composite(a, Image.new('L', (W, H), 0), fade); im = Image.merge('RGBA', (r, g2, b2, a))
    im.save(f'public/models/omg-c/paint/sky-{kind}.webp', 'WEBP', quality=82, method=6)
    bg = Image.new('RGB', (W, H), (90, 120, 90)); bg.paste(im, (0, 0), im); bg.save(f'/tmp/sky/sky-{kind}.jpg')
for k in (sys.argv[1:] or K): build(k)
print('ok')
