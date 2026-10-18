#!/usr/bin/env python3
"""Compose <id>-compare.jpg and <id>.metrics.json: design views (sheet front/side/top, or the item's cell of a 4x2 kit sheet)
above the built model's ortho renders, an overlay row (model render + design silhouette outline in magenta), and per-view
metrics: silhouette IoU (both silhouettes scale-normalised to the same height and bottom-centre aligned; top views centred),
aspect ratio delta and mean-colour delta. usage: compare.py <id> <render_dir> <out.jpg> [<design_asset_dir>] [<ref_image>] [--item N]"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
args = [a for a in sys.argv[1:]]
item = None
if '--item' in args: i = args.index('--item'); item = int(args[i + 1]); del args[i:i + 2]
aid, rdir, out = args[0:3]; ddir = args[3] if len(args) > 3 else ''; ref = args[4] if len(args) > 4 else ''
rep = json.load(open(f'{rdir}/{aid}.report.json'))
def F(s, b=False):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), '/System/Library/Fonts/Supplemental/Arial%s.ttf' % (' Bold' if b else ''), '/Library/Fonts/Arial.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p, s)
    return ImageFont.load_default()
C = 360; pad = 12
spec = json.load(open(f'{ddir}/spec.json')) if ddir and os.path.exists(f'{ddir}/spec.json') else {}
kit = item is not None and 'items' in spec

def fg_design(im):
    """foreground mask of a design view: pixels that differ from the flat grey studio background"""
    im = im.convert('RGB'); w, h = im.size
    bg = [im.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3), (w // 2, 2))]; bg = tuple(sorted(c[k] for c in bg)[2] for k in range(3))
    diff = ImageChops.difference(im, Image.new('RGB', im.size, bg)).convert('L')
    m = diff.point(lambda v: 255 if v > 14 else 0).filter(ImageFilter.MedianFilter(5))
    # fill holes (cream paper close to the grey studio): background = what a flood fill from the border reaches
    pm = Image.new('L', (w + 4, h + 4), 0); pm.paste(m, (2, 2)); ImageDraw.floodfill(pm, (0, 0), 128)
    return pm.crop((2, 2, w + 2, h + 2)).point(lambda v: 0 if v == 128 else 255)
def fg_model(im): return im.convert('RGBA').split()[3].point(lambda v: 255 if v > 20 else 0)

design = {}   # view -> RGB image (cropped to the item)
for v in ('front', 'side', 'top'):
    for p in (f'{ddir}/{v}.jpg', f'{ddir}/{v}.png') if ddir else ():
        if os.path.exists(p):
            im = Image.open(p).convert('RGB')
            if kit:   # 4 x 2 grid, item order left->right, top->bottom
                cw, ch = im.width // 4, im.height // 2; im = im.crop(((item % 4) * cw, (item // 4) * ch, (item % 4 + 1) * cw, (item // 4 + 1) * ch))
            bb = fg_design(im).getbbox()
            if bb: im = im.crop((max(0, bb[0] - 8), max(0, bb[1] - 8), min(im.width, bb[2] + 8), min(im.height, bb[3] + 8)))
            design[v] = im; break
if kit and 'side' not in design and 'front' in design: pass
model = {v: Image.open(f'{rdir}/{aid}-{v}.png').convert('RGBA') for v in ('front', 'side', 'top', 'iso')}

def norm(mask, top, H=240, W=420):
    bb = mask.getbbox()
    if not bb: return Image.new('L', (W, H + 20)), 1.0
    m = mask.crop(bb); asp = m.width / max(1, m.height)
    if top: s = min((W - 20) / m.width, H / m.height)
    else: s = H / m.height
    m = m.resize((max(1, int(m.width * s)), max(1, int(m.height * s))))
    c = Image.new('L', (W, H + 20)); x = (W - m.width) // 2; y = (H + 20 - m.height) // 2 if top else H + 10 - m.height
    c.paste(m, (x, y)); return c, asp
import numpy as np
def iou(a, b):
    A = np.asarray(a) > 0; B = np.asarray(b) > 0
    return float((A & B).sum()) / max(1, float((A | B).sum()))
def mean_col(im, mask):
    M = np.asarray(mask) > 0; px = np.asarray(im.convert('RGB'))[M]
    return tuple(int(x) for x in px.mean(0)) if len(px) else (0, 0, 0)

metrics = {}
overlay = {}
for v in ('front', 'side', 'top'):
    if v not in design: continue
    dm = fg_design(design[v]); mm = fg_model(model[v])
    dn, da = norm(dm, v == 'top'); mn, ma = norm(mm, v == 'top')
    metrics[v] = dict(iou=round(iou(dn, mn), 3), aspect_design=round(da, 3), aspect_model=round(ma, 3), aspect_delta=round(ma / da - 1, 3),
                      col_design=mean_col(design[v], dm), col_model=mean_col(model[v], mm))
    # overlay: model silhouette (grey) + model render, design outline in magenta, on the normalised frame
    bb = mm.getbbox(); mr = model[v].crop(bb) if bb else model[v]
    s = (240 / mr.height) if v != 'top' else min(400 / mr.width, 240 / mr.height)
    mr = mr.resize((max(1, int(mr.width * s)), max(1, int(mr.height * s))))
    ov = Image.new('RGB', dn.size, 'white'); x = (dn.width - mr.width) // 2; y = (dn.height - mr.height) // 2 if v == 'top' else 250 - mr.height
    ov.paste(mr, (x, y), mr)
    edge = dn.filter(ImageFilter.FIND_EDGES).point(lambda q: 255 if q > 40 else 0).filter(ImageFilter.MaxFilter(3))
    ov.paste(Image.new('RGB', ov.size, (230, 0, 160)), (0, 0), edge); overlay[v] = ov
if not design and ref and os.path.exists(ref): design = {'ref': Image.open(ref).convert('RGB')}

def on_white(im, size):
    im = im.copy(); im.thumbnail(size); bg = Image.new('RGB', size, 'white')
    if im.mode == 'RGBA': bg.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2), im)
    else: bg.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return bg
W = pad + 4 * (C + pad); rows = 3 if overlay else 2
img = Image.new('RGB', (W, 78 + rows * (C + 30)), 'white'); d = ImageDraw.Draw(img)
title = ' '.join(x for x in (spec.get('id', ''), (spec['items'][item]['en'] if kit else spec.get('en', spec.get('name', '')))) if x)
d.text((pad, 8), f"{aid} - {title}", fill='black', font=F(22, True))
ok = 'OK' if rep.get('ok') else 'OVER BUDGET'; b = rep.get('budget') or 0
use = f" ({rep['tris'] / b:.0%} of budget)" if b else ''
d.text((pad, 38), f"{rep['tris']} tris / budget {b}{use} {ok} - size {rep['size'][0]} x {rep['size'][1]} x {rep['size'][2]} m - pivots: {', '.join(p[6:] for p in rep['pivots']) or '-'}", fill='#444', font=F(15))
sz = spec.get('size_m') if not kit else None
line = '  '.join(f"{v} IoU {m['iou']:.2f}" for v, m in metrics.items())
if sz:
    dm_ = [rep['size'][0] / sz['w'] - 1, rep['size'][1] / sz['d'] - 1, rep['size'][2] / sz['h'] - 1]
    line += f"   size vs design {sz['w']}x{sz['d']}x{sz['h']}: {' '.join(f'{x:+.0%}' for x in dm_)}"; metrics['size_delta'] = [round(x, 3) for x in dm_]
d.text((pad, 58), line, fill='#a33' if any(m['iou'] < 0.8 for k, m in metrics.items() if isinstance(m, dict)) else '#263', font=F(15, True))
y = 80
labels = list(design.keys())
for i, k in enumerate(labels[:3]): d.text((pad + i * (C + pad), y), f'design {k}', fill='#666', font=F(14)); img.paste(on_white(design[k], (C, C - 20)), (pad + i * (C + pad), y + 18))
y += C + 30
for i, k in enumerate(('front', 'side', 'top', 'iso')): d.text((pad + i * (C + pad), y), f'model {k}', fill='#666', font=F(14)); img.paste(on_white(model[k], (C, C - 20)), (pad + i * (C + pad), y + 18))
if overlay:
    y += C + 30
    for i, k in enumerate(('front', 'side', 'top')):
        if k in overlay:
            m = metrics[k]; d.text((pad + i * (C + pad), y), f"overlay {k}: IoU {m['iou']:.2f}, aspect {m['aspect_delta']:+.0%}", fill='#666', font=F(14)); img.paste(on_white(overlay[k], (C, C - 20)), (pad + i * (C + pad), y + 18))
    d.text((pad + 3 * (C + pad), y), 'magenta = design silhouette outline', fill='#c0a', font=F(14))
os.makedirs(os.path.dirname(out) or '.', exist_ok=True); img.save(out, quality=88)
metrics.update(tris=rep['tris'], budget=b, ok=rep.get('ok'), size=rep['size'])
json.dump(metrics, open(f'{rdir}/{aid}.metrics.json', 'w'), indent=1)
print('METRICS', aid, json.dumps({k: (v['iou'] if isinstance(v, dict) else v) for k, v in metrics.items()}))
