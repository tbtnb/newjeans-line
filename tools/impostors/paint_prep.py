#!/usr/bin/env python3
"""Codex paint art -> game textures. Ground tiles: made seamless (cross-blend with a half-rolled copy at the edges), 1024 px WebP.
Backdrops: horizontally wrap-blended, 2048x512 WebP. usage: paint_prep.py <src dir> <out dir> [ground_px] [quality]"""
import sys, os, glob
import numpy as np
from PIL import Image
S, O = sys.argv[1:3]; GP = int(sys.argv[3]) if len(sys.argv) > 3 else 1024; Q = int(sys.argv[4]) if len(sys.argv) > 4 else 72
def ramp(n, f):   # 0 at the edges -> 1 inside, smooth over f of the size
    x = np.minimum(np.arange(n), np.arange(n)[::-1]) / (n * f); return np.clip(x, 0, 1) ** 2 * (3 - 2 * np.clip(x, 0, 1))
for f in sorted(glob.glob(os.path.join(S, '*.png'))):
    n = os.path.basename(f)[:-4]; im = Image.open(f).convert('RGB')
    if n.endswith('-ground'):
        im = im.resize((GP, GP), Image.LANCZOS); a = np.asarray(im).astype(np.float32); r = np.roll(np.roll(a, GP // 2, 0), GP // 2, 1)
        m = np.minimum.outer(ramp(GP, 0.12), ramp(GP, 0.12))[..., None]; out = a * m + r * (1 - m)
    else:
        im = im.resize((2048, 512), Image.LANCZOS); a = np.asarray(im).astype(np.float32); r = np.roll(a, 1024, 1)
        m = ramp(2048, 0.08)[None, :, None]; out = a * m + r * (1 - m)
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(os.path.join(O, n + '.webp'), 'WEBP', quality=Q, method=6)
    print(n, os.path.getsize(os.path.join(O, n + '.webp')))
