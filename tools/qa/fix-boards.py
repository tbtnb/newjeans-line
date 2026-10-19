"""v8 boards: broken-fix-board.jpg (model + in-scene before/after) and repetition-board.jpg (key views before/after with repcount numbers).
usage: python3 tools/qa/fix-boards.py <audit_before_dir> <audit_after_dir> <audit_codex_dir> <shots_before> <shots_after> <rep_before.json> <rep_after.json> <out_dir>"""
import sys, json
from PIL import Image, ImageDraw, ImageFont
ab, aa, ac, sb, sa, rb, ra, out = sys.argv[1:9]
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22); f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
except Exception: F = f = ImageFont.load_default()
RB, RA = json.load(open(ab + '/report.json')), json.load(open(aa + '/report.json'))
def model(path, crop=True):
    im = Image.open(path).convert('RGB'); return im.crop((0, 96, 1024, 416)) if crop else im
rows = [('tree-lo', ab, aa, 'decimated LOD: shattered crown, detached roots -> new bpy model (148 tris, 1 crown, clean)'),
        ('pine-lo', ab, aa, 'decimated LOD: half mint / half teal split -> new bpy pine (70 tris, teal tiers)'),
        ('paper-hill-lo', ab, aa, 'decimated LOD: torn star crater on top -> new bpy hill (78 tris)'),
        ('book-cover', ab, aa, '37 paper leaves inward-facing (dark folds) -> flipped in paper.finalize'),
        ('castle', ab, aa, 'z-fighting faces 260 -> 11 (coplanar trims nudged out), shimmer at distance gone'),
        ('ferris-wheel', ab, aa, 'z-fight 275 -> 0; Codex fidelity: thick heart rim, front IoU 0.75 -> 0.81'),
        ('pavilion', ab, aa, '30 duplicate faces + 12 z-fight -> 0; side IoU 0.58 -> 0.76 (stairs side, faceted plinth)'),
        ('spiral-tower', ab, aa, '156 duplicate faces + 73 z-fight -> 0')]
W = 2048 + 40; H = 320 + 44
bd = Image.new('RGB', (W, 70 + H * len(rows) + 560), (246, 242, 236)); d = ImageDraw.Draw(bd)
d.text((20, 18), 'OMG-C v8 broken-model audit: BEFORE (left) / AFTER (right)   -   all 83 GLBs audited (tools/qa/model-audit.mjs)', fill=(60, 40, 70), font=F)
y = 70
for k, b, a, note in rows:
    try: bd.paste(model(f'{b}/{k}.png'), (10, y + 40)); bd.paste(model(f'{a}/{k}.png'), (W // 2 + 10, y + 40))
    except Exception as e: print('skip', k, e)
    rb_, ra_ = RB.get(k, {}), RA.get(k, {})
    met = lambda r: f"zfight {r.get('zfight','?')}  dupes {r.get('dupes','?')}  inverted {r.get('inverted','?')}  floating {r.get('floating','?')}  tris {r.get('tris','?')}"
    d.text((20, y + 6), f'{k}: {note}', fill=(40, 30, 50), font=F); d.text((20, y + 30), met(rb_), fill=(150, 60, 60), font=f); d.text((W // 2 + 20, y + 30), met(ra_), fill=(40, 120, 70), font=f)
    y += H
# in-scene: z05 page-stack read as a road branch; z09 page curl + decor through it
d.text((20, y + 8), 'In-scene: page-stack cliff / page sheet in road cream+gold beside the road (z05) -> lilac/blush paper; decor no longer clips decor / set pieces / page curls', fill=(40, 30, 50), font=F)
bz = Image.open(f'{sb}/z05.png').convert('RGB').resize((270, 480)); az = Image.open(f'{sa}/z05.png').convert('RGB').resize((270, 480))
b2 = Image.open(f'{sb}/z08.png').convert('RGB').resize((270, 480)); a2 = Image.open(f'{sa}/z08.png').convert('RGB').resize((270, 480))
for i, im in enumerate([bz, b2]): bd.paste(im, (10 + i * 280, y + 44))
for i, im in enumerate([az, a2]): bd.paste(im, (W // 2 + 10 + i * 280, y + 44))
bd.save(out + '/broken-fix-board.jpg', quality=86); print('broken-fix-board', bd.size)
# repetition board
B, A = json.load(open(rb)), json.load(open(ra)); zs = list(A)
cw, ch = 270, 480; rb_ = Image.new('RGB', (40 + 5 * (2 * cw + 30), 80 + 2 * (ch + 110)), (246, 242, 236)); d = ImageDraw.Draw(rb_)
d.text((20, 18), 'OMG-C v8 repetition pass: key camera BEFORE | AFTER  (counts = what is built in frame, tools/qa/repcount.mjs)', fill=(60, 40, 70), font=F)
d.text((20, 46), 'looks = distinct asset x palette variant;  clones = tall pieces whose nearest neighbour (<7 m) is the identical model + palette', fill=(90, 70, 100), font=f)
for i, z in enumerate(zs):
    x = 20 + (i % 5) * (2 * cw + 30); y = 80 + (i // 5) * (ch + 110)
    rb_.paste(Image.open(f'{sb}/{z}.png').convert('RGB').resize((cw, ch)), (x, y + 70)); rb_.paste(Image.open(f'{sa}/{z}.png').convert('RGB').resize((cw, ch)), (x + cw + 4, y + 70))
    b, a = B[z], A[z]
    d.text((x, y), f"{z}", fill=(40, 30, 50), font=F)
    d.text((x, y + 26), f"kinds {b['distinctMid']}  looks {b['distinctLooks']}  clones {b['clonePairs']}/{b['tall']}", fill=(150, 60, 60), font=f)
    d.text((x + cw + 4, y + 26), f"kinds {a['distinctMid']}  looks {a['distinctLooks']}  clones {a['clonePairs']}/{a['tall']}", fill=(40, 120, 70), font=f)
    d.text((x, y + 48), f"top {b['mid'][0][0]} {int(b['topShare']*100)}%", fill=(150, 60, 60), font=f); d.text((x + cw + 4, y + 48), f"top {a['mid'][0][0]} {int(a['topShare']*100)}%", fill=(40, 120, 70), font=f)
rb_.save(out + '/repetition-board.jpg', quality=86); print('repetition-board', rb_.size)
