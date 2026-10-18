#!/usr/bin/env python3
"""Runtime-size the OMG v2 Codex originals (levels-design/omg/art-v2/*.png) into levels-{design,src}/omg/art/v2/.
backdrops -> 1536x864 jpg, tiles -> 512 jpg, facades -> 768 jpg, alpha stickers -> <=640 png, sparkle -> 128 png."""
from pathlib import Path
from PIL import Image, ImageEnhance
SRC = Path('levels-design/omg/art-v2'); OUT = [Path('levels-design/omg/art/v2'), Path('levels-src/omg/art/v2')]
RULES = {'sky-': ('jpg', (1536, 864)), 'ground-': ('jpg', (512, 512)), '-facade': ('jpg', (768, 768)), 'sparkle': ('png', (128, 128))}
def cover(im, size):
    tw, th = size; s = max(tw / im.width, th / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2; return im.crop((l, t, l + tw, t + th))
for o in OUT: o.mkdir(parents=True, exist_ok=True)
for p in sorted(SRC.glob('*.png')):
    rule = next((v for k, v in RULES.items() if k in p.stem), ('png', None))
    im = Image.open(p)
    if rule[0] == 'jpg':
        im = cover(im.convert('RGB'), rule[1])
        # calm ground tiles so the road reads first: low contrast, darker stage/garden, softer ward checker
        CALM = {'ground-stage': (0.45, 0.55), 'ground-garden': (0.5, 0.65), 'ground-ward': (0.45, 0.97)}
        if p.stem in CALM: c, b = CALM[p.stem]; im = ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(c)).enhance(b)
        for o in OUT: im.save(o / (p.stem + '.jpg'), quality=86)
    else:
        im = im.convert('RGBA')
        if rule[1]: im = im.resize(rule[1], Image.LANCZOS)
        else: im.thumbnail((640, 640), Image.LANCZOS)
        for o in OUT: im.save(o / (p.stem + '.png'))
    print(p.name, '->', rule[0], im.size)
