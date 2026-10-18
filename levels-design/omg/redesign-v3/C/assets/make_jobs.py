# Writes Codex job specs (one folder per asset) for the Mac mini; run: python3 make_jobs.py OUTDIR
import sys, json
from pathlib import Path
from assets_c import ASSETS, GROUND, ATLAS
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
order = []
for a in ASSETS:
    d = out / a['id']; d.mkdir(exist_ok=True); w, dp, h = a['size']; cols = ', '.join(f"{c} {ATLAS[c]}" for c in a['colors'])
    parts = '; '.join(f'({i + 1}) {p[0]}' for i, p in enumerate(a['parts']))
    base = f"ASSET {a['id']} '{a['en']}': {a['desc']}. Real size: width {w} m, depth {dp} m, height {h} m (keep these proportions exactly: W:D:H = {w}:{dp}:{h}). Colours (palette atlas): {cols}."
    rows = [('hero.png', 'hero', base), ('views.png', 'views', base + f' Same model as ./hero.png.'), ('parts.png', 'parts', base + f' Parts in order: {parts}.')]
    (d / 'spec.tsv').write_text(''.join(f'{a["id"]}\t{f}\t{t}\t{s}\n' for f, t, s in rows)); order.append(a['id'])
for g in GROUND:
    d = out / g['id']; d.mkdir(exist_ok=True)
    items = '; '.join(f'({i + 1}) {it[0]} (~{it[2]} m)' for i, it in enumerate(g['items']))
    base = f"GROUND/SMALL KIT {g['id']} — {len(g['items'])} small low-poly papercraft items for the Bunny Pop-up Storybook level, laid out in a grid of 4 columns x 2 rows, reading order left-to-right then top-to-bottom: {items}. Each item centred in its own equal cell, all at a consistent scale relative to their sizes, palette from mint, cream, coral, pink, lavender, gold, teal, sky blue."
    rows = [('kit.png', 'kit', base + ' Three-quarter view of each.'), ('front.png', 'kitfront', base + ' Same items as ./kit.png, each as an orthographic FRONT view.'), ('top.png', 'kittop', base + ' Same items as ./kit.png, each as an orthographic TOP view (looking straight down).')]
    (d / 'spec.tsv').write_text(''.join(f'{g["id"]}\t{f}\t{t}\t{s}\n' for f, t, s in rows)); order.append(g['id'])
(out / 'order.txt').write_text('\n'.join(order) + '\n'); print(len(order))
