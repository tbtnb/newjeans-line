#!/usr/bin/env python3
"""'Best of' board: chosen zones, design key next to the in-game Mac shot, 3 pairs per row.
usage: progress-board.py <renders dir (zNN-key.jpg)> <shots dir (zNN.png)> <out.jpg> <title> zNN [zNN ...]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
R, S, OUT, TITLE = sys.argv[1:5]; zones = sys.argv[5:]
def font(s):
    for f in ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(f): return ImageFont.truetype(f, s)
    return ImageFont.load_default()
H = 900; pairs = []
for z in zones:
    k = Image.open(os.path.join(R, z + '-key.jpg')).convert('RGB'); g = Image.open(os.path.join(S, z + '.png')).convert('RGB')
    k = k.resize((round(k.width * H / k.height), H)); g = g.resize((round(g.width * H / g.height), H))
    p = Image.new('RGB', (k.width + g.width + 12, H + 44), (246, 242, 236)); p.paste(k, (0, 44)); p.paste(g, (k.width + 12, 44))
    d = ImageDraw.Draw(p); F = font(26); d.text((8, 8), f'{z} design key', fill=(60, 50, 60), font=F); d.text((k.width + 20, 8), f'{z} in-game (Mac M4, high tier)', fill=(60, 50, 60), font=F)
    pairs.append(p)
cols = 3; rows = (len(pairs) + cols - 1) // cols; pw = max(p.width for p in pairs); ph = pairs[0].height
W = Image.new('RGB', (cols * pw + (cols + 1) * 24, rows * ph + (rows + 1) * 24 + 70), (236, 230, 222))
ImageDraw.Draw(W).text((24, 18), TITLE, fill=(40, 30, 40), font=font(38))
for i, p in enumerate(pairs): W.paste(p, (24 + (i % cols) * (pw + 24), 94 + (i // cols) * (ph + 24)))
W.save(OUT, quality=90); print(OUT, W.size)
