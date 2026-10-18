"""Choose turn directions for the re-charted OMG taps with the shared route search (tools/charts/route.py):
phrase patterns per section, legal multi-level crossings on the existing elevation plan and road widths.
All OMG scenery is route-relative (t/side), diamonds/crowns are time-based, so a new route keeps the level dressing.
Usage: route_omg.py [--seeds 8] [--beam 60]"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/charts'))
from route import Router
opt = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
D = ROOT / 'levels-src/omg'
chart = json.loads((D / 'chart.json').read_text()); layout = json.loads((D / 'layout.json').read_text())
dur = json.loads((ROOT / 'analysis/omg.json').read_text())['duration']
V = chart['speed'][0]['v']; taps = [x['t'] for x in chart['taps']]
elev = layout.get('elevation', []); W = layout['road']['width']
def width_at(t):
    w = W[0]['w']
    for e in W:
        if e['t'] <= t + 1e-9: w = e['w']
    return w
P = chart['meta']['beat_period']; BAR = 4 * P
DENSE = ['zig', 'cw', 'ccw', 'swR', 'swL', 'cwM', 'ccwM', 'S', 'Z']
SPARSE = ['uR', 'uL', 'swR', 'swL', 'sR', 'sL', 'cw', 'ccw', 'S', 'Z']
secs = sorted(chart['sections'], key=lambda s: s['t']); phrases = []
for k, s in enumerate(secs):
    e = secs[k + 1]['t'] if k + 1 < len(secs) else 1e9
    idx = [i for i, t in enumerate(taps) if s['t'] - 0.06 <= t < e - 0.06]
    if not idx: continue
    sparse = s.get('kind') in ('intro', 'outro', 'break') or len(idx) / max(1e-6, min(e, dur) - s['t']) < 1.4
    t0 = s['t']; cur = []
    for i in idx:
        if cur and taps[i] >= t0 + 2 * BAR - 0.06:
            phrases.append((cur[0], cur[-1] + 1, SPARSE if sparse else DENSE)); cur = []; t0 = taps[i]
        cur.append(i)
    if cur: phrases.append((cur[0], cur[-1] + 1, SPARSE if sparse else DENSE))
assert sum(b - a for a, b, _ in phrases) == len(taps), (sum(b - a for a, b, _ in phrases), len(taps))
H0 = 'NESW'.index(chart.get('startHeading', 'N')); best = None
for seed in range(int(opt('--seed0', 1)), int(opt('--seed0', 1)) + int(opt('--seeds', 8))):
    try: d, stt = Router(taps, dur, elev, width_at, speed=V, start_heading=H0).search(phrases, beam=int(opt('--beam', 60)), seed=seed)
    except RuntimeError as ex: print('seed', seed, ex); continue
    if not stt['final_ok']: print('seed', seed, 'final leg illegal'); continue
    sc = stt['crossings'] * 3 + stt['figures']; print('seed', seed, 'crossings', stt['crossings'], 'figures', stt['figures'])
    if best is None or sc > best[0]: best = (sc, d, stt)
if best is None: sys.exit('route search failed')
_, dirs, stt = best
for x, d in zip(chart['taps'], dirs): x['dir'] = d
chart['meta']['route'] = {'tool': 'tools/research/route_omg.py (route.py search)', 'crossings': stt['crossings'], 'figures': stt['figures']}
(D / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
print('written', len(taps), 'taps; crossings', stt['crossings'])
