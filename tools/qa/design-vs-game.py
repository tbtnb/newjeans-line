#!/usr/bin/env python3
"""Side-by-side sheet: design key render vs in-game shot per zone.
usage: design-vs-game.py <renders dir (zNN-key.jpg)> <shots dir (zNN.png)> <out.jpg> [title]"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
R, S, OUT = sys.argv[1:4]; title = sys.argv[4] if len(sys.argv) > 4 else ''
H = 640; pairs = []
def font(s):
    for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf']:
        if os.path.exists(f): return ImageFont.truetype(f, s)
    return ImageFont.load_default()
F, FB = font(20), font(30)
for i in range(1, 11):
    z = f'z{i:02d}'; k, g = os.path.join(R, z + '-key.jpg'), os.path.join(S, z + '.png')
    if not (os.path.exists(k) and os.path.exists(g)): continue
    a, b = Image.open(k).convert('RGB'), Image.open(g).convert('RGB')
    a = a.resize((round(a.width * H / a.height), H)); b = b.resize((round(b.width * H / b.height), H))
    p = Image.new('RGB', (a.width + b.width + 8, H + 34), (250, 248, 244)); p.paste(a, (0, 34)); p.paste(b, (a.width + 8, 34))
    d = ImageDraw.Draw(p); d.text((6, 6), f'{z} design key', fill=(40, 40, 40), font=F); d.text((a.width + 14, 6), f'{z} in-game', fill=(40, 40, 40), font=F)
    pairs.append(p)
cols = 5; rows = (len(pairs) + cols - 1) // cols; pw = max(p.width for p in pairs); ph = pairs[0].height
out = Image.new('RGB', (pw * cols + 16 * (cols + 1), ph * rows + 16 * (rows + 1) + 50), (230, 228, 222)); d = ImageDraw.Draw(out)
d.text((16, 12), title, fill=(20, 20, 20), font=FB)
for n, p in enumerate(pairs): out.paste(p, (16 + (n % cols) * (pw + 16), 66 + (n // cols) * (ph + 16)))
out.save(OUT, quality=88); print(OUT, len(pairs), out.size)
