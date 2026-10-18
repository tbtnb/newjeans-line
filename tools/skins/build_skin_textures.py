#!/usr/bin/env python3
"""Build runtime skin textures from the Codex art (Mac mini ~/nj-skins-art/<skin>/).

usage: python3 tools/skins/build_skin_textures.py <raw_dir>
  raw_dir/<skin>/{concept,trail,particle,icon}.png + design.md
writes
  levels-design/skins/<skin>/concept.jpg, design.md, src/{trail,particle,icon}.png (512px sources)
  public/skins/<skin>/trail.(jpg|png) 256px (u = across the line, v = along it), particle.png 128px (desaturated, tintable),
  icon.png 128px (cropped to content)
"""
import sys, os, shutil
import numpy as np
from PIL import Image, ImageDraw

RAW = sys.argv[1]
SKINS = {
    # rotate: make features that should run ALONG the line vertical in the image (v = along)
    'bunny': dict(rotate=True, edges=('#a9d9f5', '#a9d9f5')), 'denim': dict(rotate=False), 'bubble-gum': dict(rotate=False),
    'phoning': dict(rotate=False, pixel=True), 'film': dict(rotate=True),
    'supernatural': dict(rotate=True, edges=('#3a9fff', '#9165ff')),
}

def grid_period(gray):
    prof = gray.mean(axis=0) - gray.mean()
    ac = np.correlate(prof, prof, 'full')[len(prof) - 1:]
    lo = 20
    return lo + int(np.argmax(ac[lo:len(prof) // 4]))

for sk, opt in SKINS.items():
    src = os.path.join(RAW, sk)
    des = f'levels-design/skins/{sk}'; pub = f'public/skins/{sk}'
    os.makedirs(des + '/src', exist_ok=True); os.makedirs(pub, exist_ok=True)
    Image.open(f'{src}/concept.png').convert('RGB').save(f'{des}/concept.jpg', quality=86, optimize=True)
    shutil.copy(f'{src}/design.md', f'{des}/design.md')
    for f in ('trail', 'particle', 'icon'):
        im = Image.open(f'{src}/{f}.png'); im.thumbnail((512, 512), Image.LANCZOS); im.save(f'{des}/src/{f}.png', optimize=True)
    # trail
    tr = Image.open(f'{src}/trail.png').convert('RGB')
    if opt.get('rotate'): tr = tr.transpose(Image.ROTATE_90)
    if opt.get('pixel'):
        g = np.asarray(tr.convert('L'), dtype=np.float32); p = grid_period(g)
        # 8 cells across the line; start on a dark grid line so the crop stays periodic
        n = 8 * p; prof = g.mean(axis=0); off = int(np.argmin(prof[:p])); offy = int(np.argmin(g.mean(axis=1)[:p]))
        tr = tr.crop((off, offy, off + n, offy + n)).resize((128, 128), Image.LANCZOS)
        d = ImageDraw.Draw(tr); d.rectangle((0, 0, 7, 127), fill='#173d4d'); d.rectangle((120, 0, 127, 127), fill='#173d4d')
        tr.save(f'{pub}/trail.png', optimize=True)
        print(sk, 'grid period', p)
    else:
        tr = tr.resize((256, 256), Image.LANCZOS)
        if opt.get('edges'):
            d = ImageDraw.Draw(tr); a, b = opt['edges']; d.rectangle((0, 0, 9, 255), fill=a); d.rectangle((246, 0, 255, 255), fill=b)
            d.rectangle((10, 0, 12, 255), fill='#f5faff'); d.rectangle((243, 0, 245, 255), fill='#f5faff')
        tr.save(f'{pub}/trail.jpg', quality=86, optimize=True)
    # particle: desaturate to light luminance so the per-skin colours tint it
    pa = Image.open(f'{src}/particle.png').convert('RGBA')
    bb = pa.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox()
    if bb:
        w, h = bb[2] - bb[0], bb[3] - bb[1]; s = int(max(w, h) * 1.08); cx, cy = (bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2
        pa = pa.crop((cx - s // 2, cy - s // 2, cx - s // 2 + s, cy - s // 2 + s))
    pa = pa.resize((128, 128), Image.LANCZOS)
    a = np.asarray(pa, dtype=np.float32); lum = a[..., :3] @ np.array([0.299, 0.587, 0.114])
    lum = 255 * (0.55 + 0.45 * (lum / 255) ** 0.8)
    out = np.dstack([lum, lum, lum, a[..., 3]]).clip(0, 255).astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(f'{pub}/particle.png', optimize=True)
    # icon
    ic = Image.open(f'{src}/icon.png').convert('RGBA'); bb = ic.getchannel('A').point(lambda v: 255 if v > 16 else 0).getbbox()
    if bb:
        w, h = bb[2] - bb[0], bb[3] - bb[1]; s = int(max(w, h) * 1.06); cx, cy = (bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2
        canvas = Image.new('RGBA', (s, s), (0, 0, 0, 0)); canvas.paste(ic.crop(bb), ((s - w) // 2, (s - h) // 2)); ic = canvas
    ic.resize((128, 128), Image.LANCZOS).save(f'{pub}/icon.png', optimize=True)
print('ok')
