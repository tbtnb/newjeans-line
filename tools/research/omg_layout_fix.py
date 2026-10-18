"""Keep OMG layout timing legal for a new chart: falls must have >= 0.35 s of air before the next tap, diamonds must sit >= 0.2 s
from any tap (validator). Moves each offending fall to the nearest tap (within 1.6 s after) with >= 0.42 s to the next tap, and each
offending diamond to the nearest point >= 0.25 s from every tap. Prints every change (for the art/layout log)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; D = ROOT / 'levels-src/omg'
ch = json.loads((D / 'chart.json').read_text()); lay = json.loads((D / 'layout.json').read_text()); T = [x['t'] for x in ch['taps']]
changes = []
for e in lay['elevation']:
    if e['type'] not in ('fall', 'jump'): continue
    nxt = next((t for t in T if t > e['t'] + 1e-6), 1e9)
    if nxt - e['t'] >= 0.35: continue
    cands = [t for i, t in enumerate(T) if e['t'] - 0.4 <= t <= e['t'] + 1.6 and i + 1 < len(T) and T[i + 1] - t >= 0.42]
    if not cands: changes.append(f"fall {e['t']}: NO legal tap nearby"); continue
    new = min(cands, key=lambda t: abs(t - e['t'])); changes.append(f"elevation fall {e['t']} -> {new} (dy {e['dy']}; next tap was {nxt - e['t']:.3f} s after)"); e['t'] = new
for dm in lay['diamonds']:
    if all(abs(dm['t'] - t) >= 0.2 for t in T): continue
    pts = [min(max(dm['t'], a + 0.25), b - 0.25) for a, b in zip(T, T[1:]) if b - a >= 0.5]
    new = round(min(pts, key=lambda q: abs(q - dm['t'])), 3); changes.append(f"diamond {dm['t']} -> {new}"); dm['t'] = new
    dm['moved'] = 'kept off taps after the OMG lyric re-chart (chart-research)'
for c in lay['crowns']:
    if any(0 < c['t'] - t < 0.05 or 0 < t - c['t'] < 0.3 for t in T):
        gaps = [(a + 0.06, b - a) for a, b in zip(T, T[1:]) if b - a >= 0.5 and abs(a - c['t']) <= 2.0]
        if gaps: new = round(min(gaps, key=lambda g: abs(g[0] - c['t']))[0], 3); changes.append(f"crown {c['t']} -> {new}"); c['t'] = new
(D / 'layout.json').write_text(json.dumps(lay, indent=1, ensure_ascii=False))
print('\n'.join(changes) or 'no layout changes')
