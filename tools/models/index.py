#!/usr/bin/env python3
"""Contact sheet of every built model: iso render + id + tris/budget + IoU f/s/t.
usage: index.py <build dir> <out.jpg>   (reads <id>-iso.png, <id>.report.json, <id>.metrics.json; order = catalog.json)"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
B, OUT = sys.argv[1], sys.argv[2]
cat = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalog.json')))
ids = [c for c in cat if os.path.exists(os.path.join(B, c['id'] + '-iso.png'))]
CW, CH, N = 300, 330, 10
rows = (len(ids) + N - 1) // N
im = Image.new('RGB', (CW * N, CH * rows + 60), (238, 236, 230)); d = ImageDraw.Draw(im)
def font(s):
    for f in ['/System/Library/Fonts/Supplemental/Arial.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(f): return ImageFont.truetype(f, s)
    return ImageFont.load_default()
F, FB = font(15), font(26)
tot = 0
for k, c in enumerate(ids):
    x, y = (k % N) * CW, (k // N) * CH + 60
    iso = Image.open(os.path.join(B, c['id'] + '-iso.png')).convert('RGBA'); iso.thumbnail((CW - 16, CH - 70))
    im.paste(iso, (x + (CW - iso.width) // 2, y + 8 + (CH - 70 - iso.height) // 2), iso)
    r = json.load(open(os.path.join(B, c['id'] + '.report.json'))); tot += r['tris']
    m = {}
    try: m = json.load(open(os.path.join(B, c['id'] + '.metrics.json')))
    except Exception: pass
    io = '/'.join(f"{m.get(v, {}).get('iou', 0):.2f}" for v in ('front', 'side', 'top')) if m else '-'
    tag = (c['design'].split('_')[0] + (f"#{c['item']}" if 'item' in c else ''))
    d.text((x + 8, y + CH - 58), f"{tag} {c['id']}", fill=(30, 30, 30), font=F)
    d.text((x + 8, y + CH - 38), f"{r['tris']} / {c['budget']} tris ({100 * r['tris'] / max(1, c['budget']):.0f}%)", fill=(60, 60, 60), font=F)
    d.text((x + 8, y + CH - 20), f"IoU f/s/t {io}", fill=(90, 90, 90), font=F)
d.text((12, 14), f"OMG concept C models — {len(ids)} assets, {tot} tris total (iso renders, Blender Workbench; code: Grok Bot, art: Codex GPT-6.1-Sol high)", fill=(20, 20, 20), font=FB)
im.save(OUT, quality=90); print(OUT, len(ids), tot)
