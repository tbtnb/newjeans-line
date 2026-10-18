#!/usr/bin/env python3
"""Compose <id>-compare.jpg: design views (three-view sheet from spec, or the reference render) above the built model's
ortho front/side/top + iso renders, with tris/budget/size. usage: compare.py <id> <render_dir> <out.jpg> [<design_asset_dir>] [<ref_image>]"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
aid, rdir, out = sys.argv[1:4]; ddir = sys.argv[4] if len(sys.argv) > 4 else ''; ref = sys.argv[5] if len(sys.argv) > 5 else ''
rep = json.load(open(f'{rdir}/{aid}.report.json'))
F = lambda s, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
C = 380; pad = 14
def on_white(im, size):
    im = im.convert('RGBA'); im.thumbnail(size); bg = Image.new('RGB', size, 'white'); bg.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2), im); return bg
design = []   # (label, image)
spec = {}
if ddir and os.path.exists(f'{ddir}/spec.json'): spec = json.load(open(f'{ddir}/spec.json'))
views = spec.get('views') or {}
if ddir:
    for v in ('front', 'side', 'top'):
        cand = views.get(v) if isinstance(views.get(v), str) else None
        for p in [cand and f'{ddir}/{cand}', f'{ddir}/{v}.png', f'{ddir}/{v}.jpg']:
            if p and os.path.exists(p): design.append((f'design {v}', Image.open(p))); break
    sheet = next((f'{ddir}/{n}' for n in ('sheet.png', 'sheet.jpg', 'three-view.png', 'three-view.jpg') if os.path.exists(f'{ddir}/{n}')), None)
    if not design and sheet:
        im = Image.open(sheet); boxes = views if all(isinstance(views.get(v), list) for v in ('front', 'side', 'top')) else None
        if boxes: design = [(f'design {v}', im.crop(tuple(boxes[v]))) for v in ('front', 'side', 'top')]
        else: design = [('design sheet', im)]
if not design and ref and os.path.exists(ref): design = [('design reference (zone render; three-view sheet pending)', Image.open(ref))]
model = [(f'model {v}', Image.open(f'{rdir}/{aid}-{v}.png')) for v in ('front', 'side', 'top', 'iso')]
W = pad + 4 * (C + pad); H1 = C if len(design) > 1 else int(C * 1.15)
img = Image.new('RGB', (W, 70 + H1 + 40 + C + 40), 'white'); d = ImageDraw.Draw(img)
ok = 'OK' if rep.get('ok') else 'OVER BUDGET'
d.text((pad, 10), f"{aid} - {spec.get('name', '')}", fill='black', font=F(26, True))
d.text((pad, 42), f"{rep['tris']} tris / budget {rep.get('budget')} ({ok}) - size {rep['size'][0]} x {rep['size'][1]} x {rep['size'][2]} m (x,y,z) - pivots: {', '.join(p[6:] for p in rep['pivots']) or '-'}", fill='#444', font=F(17))
y = 70
if len(design) == 1:
    lab, im = design[0]; d.text((pad, y), lab, fill='#666', font=F(16)); img.paste(on_white(im, (W - 2 * pad, H1 - 22)), (pad, y + 22))
else:
    for i, (lab, im) in enumerate(design): d.text((pad + i * (C + pad), y), lab, fill='#666', font=F(16)); img.paste(on_white(im, (C, C - 22)), (pad + i * (C + pad), y + 22))
y += H1 + 30
for i, (lab, im) in enumerate(model): d.text((pad + i * (C + pad), y), lab, fill='#666', font=F(16)); img.paste(on_white(im, (C, C - 22)), (pad + i * (C + pad), y + 22))
os.makedirs(os.path.dirname(out), exist_ok=True); img.save(out, quality=88); print(out, img.size)
