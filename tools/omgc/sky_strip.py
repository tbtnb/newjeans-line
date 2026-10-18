"""v7 night sky strip: navy gradient (opaque at the top, clear at the bottom), stars, crescent moon, castle / house / tower
silhouette skyline with warm lit windows -> public/models/omg-c/paint/sky-night.webp (screen-top overlay band, night zones)"""
import random, math
from PIL import Image, ImageDraw, ImageFilter
W, H = 1024, 384; random.seed(7)
im = Image.new('RGBA', (W, H)); px = im.load()
for y in range(H):
    k = y / H; a = 255 if k < 0.55 else int(255 * max(0, 1 - (k - 0.55) / 0.45) ** 1.6)
    c = (int(28 + 40 * k), int(26 + 30 * k), int(78 + 50 * k))
    for x in range(W): px[x, y] = (*c, a)
d = ImageDraw.Draw(im)
for _ in range(170):   # stars
    x, y, r = random.uniform(0, W), random.uniform(0, H * 0.5), random.choice([1, 1, 1, 1.5, 2, 2.5])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 246, 214, random.randint(160, 255)))
for _ in range(9):     # four-point sparkles
    x, y = random.uniform(30, W - 30), random.uniform(10, H * 0.42); s = random.uniform(5, 9)
    d.polygon([(x, y - s), (x + s * 0.25, y), (x, y + s), (x - s * 0.25, y)], fill=(255, 236, 170, 255)); d.polygon([(x - s, y), (x, y + s * 0.25), (x + s, y), (x, y - s * 0.25)], fill=(255, 236, 170, 255))
glow = Image.new('RGBA', (W, H)); g = ImageDraw.Draw(glow); mx, my, mr = 790, 70, 38
g.ellipse([mx - mr * 2.2, my - mr * 2.2, mx + mr * 2.2, my + mr * 2.2], fill=(255, 230, 160, 70)); glow = glow.filter(ImageFilter.GaussianBlur(22)); im.alpha_composite(glow)
m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m); md.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=255); md.ellipse([mx - mr + 18, my - mr - 8, mx + mr + 18, my + mr - 8], fill=0)   # crescent mask
im.paste(Image.new('RGBA', (W, H), (255, 240, 190, 255)), (0, 0), m); d = ImageDraw.Draw(im)
base = int(H * 0.74); sil = (52, 38, 96, 255); win = (255, 205, 120, 255)
x = 0
while x < W:   # skyline: houses / towers / castle
    kind = random.random(); w = random.randint(26, 60); h = random.randint(26, 70)
    if 380 < x < 560: kind = 2
    if kind < 0.55:   # house with pointed roof
        d.rectangle([x, base - h, x + w, base + 40], fill=sil); d.polygon([(x - 4, base - h), (x + w / 2, base - h - w * 0.6), (x + w + 4, base - h)], fill=sil)
        for j in range(random.randint(1, 3)): wx = x + 6 + j * 14; (wx + 7 < x + w) and d.rectangle([wx, base - h + 12, wx + 6, base - h + 20], fill=win)
    elif kind < 0.85:   # tower with cone
        tw = max(14, w // 2); th = h + random.randint(30, 60); d.rectangle([x, base - th, x + tw, base + 40], fill=sil); d.polygon([(x - 5, base - th), (x + tw / 2, base - th - 34), (x + tw + 5, base - th)], fill=sil)
        d.rectangle([x + tw / 2 - 3, base - th + 14, x + tw / 2 + 3, base - th + 24], fill=win); w = tw
    else:   # castle block: towers + keep
        cw = 150; d.rectangle([x, base - 60, x + cw, base + 40], fill=sil)
        for tx, th in ((x - 6, 110), (x + 40, 140), (x + 95, 125), (x + cw - 16, 100)):
            d.rectangle([tx, base - th, tx + 24, base], fill=sil); d.polygon([(tx - 6, base - th), (tx + 12, base - th - 40), (tx + 30, base - th)], fill=sil); d.rectangle([tx + 9, base - th + 18, tx + 15, base - th + 30], fill=win)
        for j in range(5): d.rectangle([x + 18 + j * 26, base - 40, x + 26 + j * 26, base - 28], fill=win)
        w = cw
    x += w + random.randint(4, 22)
d.rectangle([0, base + 6, W, H], fill=(0, 0, 0, 0))   # skyline ends in the soft fade below
fade = Image.new('L', (W, H), 0); fd = fade.load()
for y in range(H):
    v = 255 if y < base - 4 else max(0, int(255 * (1 - (y - base + 4) / 10)))
    for x in range(W): fd[x, y] = v
r, g2, b, a = im.split(); a = Image.composite(a, Image.new('L', (W, H), 0), fade); im = Image.merge('RGBA', (r, g2, b, a))
im.save('public/models/omg-c/paint/sky-night.webp', 'WEBP', quality=82, method=6); im.convert('RGB').save('/tmp/sky-night-preview.jpg')
print('ok')
