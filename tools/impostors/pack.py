#!/usr/bin/env python3
"""Pack impostor sprites (render.py output: <id>.png + <id>.json) into one atlas: each sprite cropped to its alpha bbox,
shelf-packed into 2048x2048, written as WebP (alpha) + JSON {id: {uv:[u0,v0,u1,v1], w, h}} with w/h = card size in metres at scale 1.
usage: pack.py <sprite dir> <out.webp> <out.json>"""
import sys, os, json, glob
from PIL import Image
S, OUT, OJ = sys.argv[1:4]; N = 2048
items = []
for f in sorted(glob.glob(os.path.join(S, '*.json'))):
    m = json.load(open(f)); im = Image.open(f[:-5] + '.png').convert('RGBA'); bb = im.getchannel('A').point(lambda a: 255 if a > 24 else 0).getbbox()
    if not bb: continue
    mpp = m['ortho'] / m['px']; c = im.crop(bb)
    items.append((m['id'], c, (bb[2] - bb[0]) * mpp, (bb[3] - bb[1]) * mpp))
items.sort(key=lambda t: -t[1].height)
A = Image.new('RGBA', (N, N), (0, 0, 0, 0)); x = y = sh = 0; meta = {}; pad = 4
for aid, c, w, h in items:
    if x + c.width + pad > N: x = 0; y += sh + pad; sh = 0
    if y + c.height > N: raise SystemExit('atlas full')
    # bleed the edge colours into the padding so mip / bilinear sampling never pulls in black
    A.paste(c, (x, y), c); meta[aid] = dict(uv=[x / N, y / N, (x + c.width) / N, (y + c.height) / N], w=round(w, 3), h=round(h, 3))
    x += c.width + pad; sh = max(sh, c.height)
# premultiplied-style bleed: fill transparent texels with the nearest opaque colour (cheap: dilate a few times)
from PIL import ImageFilter
rgb = A.convert('RGB'); a = A.getchannel('A')
for _ in range(3):
    big = Image.composite(rgb, rgb.filter(ImageFilter.MaxFilter(3)), a.point(lambda v: 255 if v > 0 else 0)); rgb = big
    a = a.filter(ImageFilter.MaxFilter(3)).point(lambda v: 255 if v > 0 else 0) if False else a
Hh = 1 << (y + sh - 1).bit_length()   # crop to the used power-of-two height
for m in meta.values(): m['uv'] = [m['uv'][0], m['uv'][1] * N / Hh, m['uv'][2], m['uv'][3] * N / Hh]
out = rgb.copy(); out.putalpha(A.getchannel('A')); out = out.crop((0, 0, N, Hh)); out.save(OUT, 'WEBP', quality=86, method=6)
json.dump(dict(size=[N, Hh], sprites=meta), open(OJ, 'w'), indent=0)
print(OUT, os.path.getsize(OUT), 'sprites', len(meta), 'used rows to y', y + sh)
