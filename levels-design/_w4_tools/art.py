"""Procedural stand-ins for the GenerateImage art (the generated files are stored outside this box).
Same file names, palette and motif as the generated versions listed in design.md; swap in the generated images 1:1."""
import sys, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
OUT = '/workspace/newjeans-line-designs'
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def grad(w, h, top, bot, stars=0, seed=1, clouds=0, bubbles=0, streaks=0, hills=None):
    a = np.linspace(0, 1, h)[:, None, None]; t = np.array(hexc(top))[None, None]; b = np.array(hexc(bot))[None, None]
    im = (t * (1 - a) + b * a).repeat(w, 1).astype(np.uint8); img = Image.fromarray(im); d = ImageDraw.Draw(img, 'RGBA'); r = random.Random(seed)
    for _ in range(stars):
        x, y = r.random() * w, r.random() * h * 0.7; s = r.choice([1, 1, 1, 2]); d.ellipse([x, y, x + s, y + s], fill=(255, 255, 240, r.randint(90, 200)))
    for _ in range(streaks):
        y = r.random() * h * 0.8; x = r.random() * w * 0.8; d.line([x, y, x + r.uniform(120, 360), y - r.uniform(10, 40)], fill=(255, 220, 230, 60), width=r.randint(3, 8))
    for _ in range(clouds):
        x, y = r.random() * w, r.uniform(0.15, 0.75) * h; s = r.uniform(40, 110)
        for k in range(4): d.ellipse([x + k * s * 0.5 - s * 0.5, y - s * 0.3 * (k % 2), x + k * s * 0.5 + s * 0.5, y + s * 0.45], fill=(255, 255, 255, 120))
    for _ in range(bubbles):
        x, y = r.random() * w, r.random() * h * 0.7; s = r.uniform(12, 40); d.ellipse([x, y, x + s, y + s], outline=(255, 255, 255, 150), width=2, fill=(200, 230, 255, 40))
    if hills:
        for k, c in enumerate(hills):
            pts = [(0, h)] + [(x, h * (0.86 + 0.05 * k) - 25 * math.sin(x / 70 + k * 2) - 18 * math.sin(x / 23 + k)) for x in range(0, w + 20, 20)] + [(w, h)]
            d.polygon(pts, fill=hexc(c) + (255,))
    return img.filter(ImageFilter.GaussianBlur(1.2))
def tile(n, base, jitter, grid=None, dots=None, seed=2, lowpoly=False, foam=None):
    r = random.Random(seed); img = Image.new('RGB', (n, n), hexc(base)); d = ImageDraw.Draw(img)
    b = np.array(hexc(base))
    if lowpoly:
        step = n // 8
        for i in range(8):
            for j in range(8):
                for tri in ([(i, j), (i + 1, j), (i, j + 1)], [(i + 1, j), (i + 1, j + 1), (i, j + 1)]):
                    c = tuple(int(v) for v in np.clip(b + r.uniform(-jitter, jitter), 0, 255)); d.polygon([(x * step, y * step) for x, y in tri], fill=c)
    if grid:
        step = n // grid[0]
        for i in range(grid[0]):
            for j in range(grid[0]):
                c = tuple(int(v) for v in np.clip(b + r.uniform(-jitter, jitter), 0, 255)); d.rectangle([i * step + 1, j * step + 1, (i + 1) * step - 2, (j + 1) * step - 2], fill=c)
        for i in range(grid[0] + 1): d.line([i * step, 0, i * step, n], fill=hexc(grid[1]), width=2); d.line([0, i * step, n, i * step], fill=hexc(grid[1]), width=2)
    if foam:
        for k in range(3):
            y0 = n * (k + 0.5) / 3; d.line([(x, y0 + 8 * math.sin(x * 2 * math.pi / n * 3)) for x in range(0, n + 1, 4)], fill=hexc(foam), width=3)
    if dots:
        for _ in range(dots[0]):
            x, y = r.random() * n, r.random() * n; s = r.uniform(*dots[2]); d.ellipse([x, y, x + s, y + s], fill=hexc(r.choice(dots[1])))
    return img
def save(img, slug, name, q=88):
    import os; os.makedirs(f'{OUT}/{slug}/art', exist_ok=True); p = f'{OUT}/{slug}/art/{name}'
    img.convert('RGB').save(p, quality=q) if name.endswith('.jpg') else img.save(p); print('wrote', p)
def font(sz):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf'):
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()
def flower(n=768, bg='#000000'):
    img = Image.new('RGB', (n, n), hexc(bg)); d = ImageDraw.Draw(img); c = n / 2
    cols = ['#e8272b', '#ff8a1d', '#ffd400', '#5bbf3a', '#1fb5c8', '#2f7fe0', '#6a4fd8', '#c04fd0', '#ff5fa8', '#ff7ab8', '#9b5de5', '#29b6f6']
    for i, col in enumerate(cols):
        a = math.radians(90 - i * 30); px, py = c + math.cos(a) * n * 0.27, c - math.sin(a) * n * 0.27; r = n * 0.13
        d.ellipse([px - r, py - r, px + r, py + r], fill=hexc(col))
    r = n * 0.17; d.ellipse([c - r, c - r, c + r, c + r], fill=(255, 255, 255))
    e = n * 0.022; d.ellipse([c - n * 0.07 - e, c - n * 0.05 - e, c - n * 0.07 + e, c - n * 0.05 + e], fill=(0, 0, 0)); d.ellipse([c + n * 0.07 - e, c - n * 0.05 - e, c + n * 0.07 + e, c - n * 0.05 + e], fill=(0, 0, 0))
    d.chord([c - n * 0.07, c - n * 0.02, c + n * 0.07, c + n * 0.1], 0, 180, fill=(0, 0, 0))
    return img
slug = sys.argv[1]
if slug == 'supernatural':
    save(grad(1600, 900, '#0b0f35', '#6a5bb8', stars=260, seed=3, hills=['#3b3f8e', '#2a2d6e']), slug, 'sky-night.jpg')
    save(tile(512, '#1a1d4a', 10, grid=(8, '#14163a'), dots=(9, ['#ffb347', '#ffd98a'], (3, 5))), slug, 'roof-ground.jpg')
    save(flower(), slug, 'flower-billboard.jpg')
    im = grad(1200, 675, '#2b2366', '#c76aa8', stars=160, seed=5, hills=['#3a2f75', '#2b2558']); d = ImageDraw.Draw(im, 'RGBA')
    for k, col in enumerate(['#ff7ab8', '#9b7be0', '#63d2c6', '#ffd166', '#ff7ab8']):
        r = 300 - k * 50; d.ellipse([600 - r, 300 - r * 0.8, 600 + r, 300 + r * 0.8], outline=hexc(col) + (200,), width=18)
    d.polygon([(560, 560), (640, 560), (612, 250), (588, 250)], fill=(240, 232, 220, 255)); d.line([(600, 250), (560, 190)], fill=(240, 232, 220), width=8); d.line([(600, 250), (640, 190)], fill=(240, 232, 220), width=8)
    save(im, slug, 'signal-poster.jpg')
if slug == 'how-sweet':
    save(grad(1600, 900, '#a9d3c0', '#fbf3df', clouds=7, seed=4), slug, 'sky-summer.jpg')
    save(tile(512, '#f2ece0', 6, grid=(6, '#e2d9c8'), dots=(14, ['#507f83', '#ff5b24', '#c9b9a0'], (2, 4))), slug, 'plaza-ground.jpg')
    im = Image.new('RGB', (1200, 675), hexc('#cfe6da')); d = ImageDraw.Draw(im); r = random.Random(7)
    for k in range(5):
        x = 110 + k * 200; col = ['#292d32', '#f2efe4', '#292d32', '#f2efe4', '#ff5b24'][k]; d.rectangle([x, 120, x + 150, 470], fill=hexc(col))
        for _ in range(3):
            cx, cy = x + r.uniform(10, 140), r.uniform(140, 450); s = r.uniform(20, 60); d.polygon([(cx, cy), (cx + s, cy), (cx, cy + s)], fill=hexc(r.choice(['#8a8f96', '#c8c8c8', '#5a5f66'] if k < 4 else ['#ff8a5c', '#ffb08f'])))
    save(im, slug, 'panels-poster.jpg')
    im = Image.new('RGBA', (900, 450), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(60, 60), (780, 60), (860, 140), (860, 390), (840, 410), (60, 410), (20, 370), (20, 100)], fill=hexc('#ff5b24') + (255,))
    d.polygon([(780, 60), (860, 140), (780, 140)], fill=hexc('#ffa27e') + (255,))
    d.text((450, 235), 'HOW SWEET', fill=hexc('#f2efe4'), font=font(120), anchor='mm')
    save(im, slug, 'sticker.png')
if slug == 'bubble-gum':
    save(grad(1600, 900, '#4fd0dc', '#eafcfc', clouds=8, bubbles=14, seed=6), slug, 'sky-beach.jpg')
    save(tile(512, '#5fd8d2', 22, lowpoly=True, foam='#ffffff'), slug, 'sea-ground.jpg')
    im = Image.new('RGBA', (1200, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(6):
        x = 40 + k * 190; d.rectangle([x, 40, x + 180, 520], fill=hexc('#f6efe2' if k < 5 else '#f07a2a') + (255,))
        if k < 5:   # featureless cut-out figure: head + body + legs, no face
            cx = x + 90; d.ellipse([cx - 32, 110, cx + 32, 180], fill=hexc('#1d3260')); hair = [(cx - 45, 120), (cx + 45, 120), (cx + 40 + 8 * (k % 3), 230), (cx - 40 - 6 * (k % 2), 230)]
            d.polygon(hair, fill=hexc('#1d3260')) if k % 2 == 0 else None
            d.polygon([(cx - 40, 190), (cx + 40, 190), (cx + 30, 360), (cx - 30, 360)], fill=hexc('#1d3260')); d.rectangle([cx - 28, 360, cx - 6, 500], fill=hexc('#1d3260')); d.rectangle([cx + 6, 360, cx + 28, 500], fill=hexc('#1d3260'))
    save(im, slug, 'silhouette-screen.png')
if slug == 'right-now':
    save(grad(1600, 900, '#a99ad0', '#ffd2c2', streaks=14, seed=8), slug, 'sky-dawn.jpg')
    save(tile(512, '#86b85c', 14, grid=None, dots=(700, ['#ff9ec4', '#ffffff', '#ffb347', '#fff07a', '#6fa447'], (3, 7))), slug, 'flower-ground.jpg')
    im = Image.new('RGB', (800, 800), hexc('#ffdbe3')); d = ImageDraw.Draw(im); r = random.Random(9)
    for _ in range(40):
        x, y = r.random() * 800, r.random() * 800; s = r.uniform(10, 26); d.ellipse([x, y, x + s, y + s], fill=hexc(r.choice(['#ff9ec4', '#ffd166', '#a3c4f3', '#c3a6e8'])))
    d.rounded_rectangle([140, 230, 660, 520], radius=140, fill=(255, 255, 255), outline=hexc('#b9d0f0'), width=6); d.polygon([(250, 500), (330, 510), (200, 600)], fill=(255, 255, 255))
    for k in range(3): d.ellipse([310 + k * 70, 345, 350 + k * 70, 385], fill=hexc('#c4c4c8'))
    save(im, slug, 'chat-sign.jpg')
