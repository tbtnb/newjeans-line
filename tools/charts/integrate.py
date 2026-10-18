#!/usr/bin/env python3
"""Integrate a worker design (levels-design/<slug>/{chart,layout}.json) into the engine format (levels-src/<slug>/).
Same pipeline as the Ditto representative level:
  1. rhythm: the worker's audited tap times; each section gets `follows` (from chart-report.md, else inferred by
     chartlogic); taps failing the rhythm-logic rule are trimmed with the chartlogic thresholds
     (faint: layer < 0.35 & full < 0.35 & no other band >= 0.5; off-layer: layer < 0.35 while another band >= 0.6;
     weak burst: gap < 0.15 s and neither the layer nor the full mix >= 0.6). --no-trim keeps every tap.
  2. route: turn directions re-chosen by route.py (phrase patterns per section, legal multi-level crossings) on the
     worker's elevation plan and road widths, at the chart's speed. --keep-route keeps the worker's directions.
  3. scenery: objects placed by absolute worldPos on the worker's route are re-anchored route-relatively (nearest
     point of the worker's centreline -> same time + signed side offset on the new route); the engine then pushes
     side-placed scenery off the road. The stale 'path' node list is dropped.
  4. art: levels-design/<slug>/art (art-codex illustrations already overlaid) is copied to levels-src/<slug>/art.
Usage: integrate.py <slug> [--no-trim] [--keep-route] [--reuse-route (same taps: keep the last searched directions)] [--seeds 6] [--beam 60]"""
import json, sys, math, shutil, subprocess
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from route import Router, HEAD, elev_at
ROOT = Path(__file__).resolve().parents[2]
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
sid = args[0]
D = ROOT / f'levels-design/{sid}'; OUT = ROOT / f'levels-src/{sid}'; OUT.mkdir(parents=True, exist_ok=True)
chart = json.loads((D / 'chart.json').read_text()); layout = json.loads((D / 'layout.json').read_text())
old_dirs = {round(x['t'], 3): x.get('dir') for x in chart['taps']}
dur = json.loads((ROOT / f'analysis/{sid}.json').read_text())['duration']
speed = chart.get('speed', [{'t': 0, 'v': 9.0}]); V = speed[0]['v']
if len(speed) > 1: print('WARNING: variable speed; route search uses the first speed', V)
# ---- 1. follows + trim
prev = json.loads((OUT / 'chart.json').read_text()) if (OUT / 'chart.json').exists() else None
(OUT / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
subprocess.run([sys.executable, str(ROOT / 'tools/charts/follows_from_reports.py'), sid], check=True)
chart = json.loads((OUT / 'chart.json').read_text())
E = np.load(ROOT / f'analysis/{sid}.env.npz'); H = float(E['hop_s'])
ENV = {k: E[k] / 100 for k in ['kick', 'snare', 'hat', 'mid', 'full']}; ENV['drums'] = np.maximum(ENV['kick'], ENV['snare'])
ENV['vocal'] = E['vocal'] / 100 if 'vocal' in E.files else ENV['mid']
def st(t, L):
    f = int(round(t / H)); w = int(round(0.03 / H)); return float(ENV[L][max(0, f - w):f + w + 1].max())
secs = sorted(chart['sections'], key=lambda s: s['t'])
def sec(t): return [s for s in secs if s['t'] <= t + 1e-6][-1] if secs else {}
def infer(s, taps):
    meds = {L: float(np.median([st(t, L) for t in taps])) for L in ['kick', 'snare', 'hat', 'mid', 'drums', 'vocal']}
    return max(meds, key=meds.get)
for k, s in enumerate(secs):
    if not s.get('follows'):
        e = secs[k + 1]['t'] if k + 1 < len(secs) else 1e9
        tt = [x['t'] for x in chart['taps'] if s['t'] <= x['t'] < e]
        if tt: s['follows'] = infer(s, tt); s['follows_note'] = 'inferred by integrate.py (strongest band at the taps)'
def offlayer(L, tt):
    excl = {L} | ({'kick', 'snare'} if L == 'drums' else set())
    return sum(1 for t in tt if st(t, L) < 0.35 and max(st(t, k) for k in ['kick', 'snare', 'hat', 'mid'] if k not in excl) >= 0.6)
# A section declared as 'kick' or 'snare' whose taps land on both drums of the same groove follows the kick+snare
# groove ('drums'): switch when that removes at least half of its off-layer flags.
for k, s in enumerate(secs):
    if s.get('follows') in ('kick', 'snare'):
        e = secs[k + 1]['t'] if k + 1 < len(secs) else 1e9
        tt = [x['t'] for x in chart['taps'] if s['t'] <= x['t'] < e]
        a, b = offlayer(s['follows'], tt), offlayer('drums', tt)
        if a and b <= a / 2:
            s['follows_note'] = f"declared {s['follows']}; taps sit on kick and snare of one groove ({a} off-layer as {s['follows']}, {b} as kick+snare) -> drums. " + s.get('follows_note', '')
            s['follows'] = 'drums'
trimmed = []
if '--no-trim' not in sys.argv:
    for _ in range(3):
        taps = sorted(chart['taps'], key=lambda x: x['t']); T = [x['t'] for x in taps]; keep = []
        for i, x in enumerate(taps):
            L = sec(x['t']).get('follows', 'full'); sl = st(x['t'], L); sf = st(x['t'], 'full')
            excl = {L} | ({'kick', 'snare'} if L == 'drums' else set())
            oth = max(st(x['t'], k) for k in ['kick', 'snare', 'hat', 'mid'] if k not in excl)
            gap = min(T[i] - T[i - 1] if i else 9, T[i + 1] - T[i] if i + 1 < len(T) else 9)
            why = 'faint' if (sl < 0.35 and sf < 0.35 and oth < 0.5) else 'off-layer' if (sl < 0.35 and oth >= 0.6) else 'weak-burst' if (gap < 0.15 and sf < 0.6 and sl < 0.6) else None
            if why: trimmed.append({'t': x['t'], 'why': why, 'follows': L, 'layer': round(sl, 2), 'full': round(sf, 2), 'other': round(oth, 2)})
            else: keep.append(x)
        if len(keep) == len(taps): break
        chart['taps'] = keep
chart['taps'].sort(key=lambda x: x['t'])
taps = [x['t'] for x in chart['taps']]
print(f'{sid}: {len(taps)} taps after trim ({len(trimmed)} trimmed)')
# ---- 2. route
elev = layout.get('elevation', [])
W = layout.get('road', {}).get('width', [{'t': 0, 'w': 2.2}]) if isinstance(layout.get('road'), dict) else [{'t': 0, 'w': 2.2}]
def width_at(t):
    w = W[0]['w'] if W else 2.2
    for e in W:
        if e['t'] <= t + 1e-9: w = e['w']
    return w
meta = chart.get('meta', {}); P = meta.get('beat_period') or (60 / meta['bpm'] if meta.get('bpm') else json.loads((ROOT / f'analysis/{sid}.grid.json').read_text())['period'])
BAR = 4 * P
DENSE = ['zig', 'cw', 'ccw', 'swR', 'swL', 'cwM', 'ccwM', 'S', 'Z']
SPARSE = ['uR', 'uL', 'swR', 'swL', 'sR', 'sL', 'cw', 'ccw', 'S', 'Z']
phrases = []
for k, s in enumerate(secs):
    e = secs[k + 1]['t'] if k + 1 < len(secs) else 1e9
    idx = [i for i, t in enumerate(taps) if s['t'] <= t < e]
    if not idx: continue
    sparse = s.get('kind') in ('intro', 'outro', 'break', 'bridge', 'pre') or len(idx) / max(1e-6, min(e, dur) - s['t']) < 1.4
    pats = SPARSE if sparse else DENSE
    t0 = s['t']; cur = []
    for i in idx:
        if cur and taps[i] >= t0 + 2 * BAR - 0.01:
            phrases.append((cur[0], cur[-1] + 1, pats)); cur = []; t0 = taps[i]
        cur.append(i)
    if cur: phrases.append((cur[0], cur[-1] + 1, pats))
assert sum(b - a for a, b, _ in phrases) == len(taps)
H0 = 'NESW'.index(chart.get('startHeading', 'N'))
if '--reuse-route' in sys.argv and prev and [round(x['t'], 3) for x in prev['taps']] == [round(t, 3) for t in taps]:
    dirs = [x['dir'] for x in prev['taps']]; stt = {'crossings': prev.get('meta', {}).get('integration', {}).get('crossings')}; print('reusing previous route')
elif '--keep-route' in sys.argv:
    dirs = [old_dirs.get(round(t, 3)) or 'L' for t in taps]; stt = {'crossings': None}
else:
    best = None
    for seed in range(1, int(opt('--seeds', 6)) + 1):
        try:
            d, stt = Router(taps, dur, elev, width_at, speed=V, start_heading=H0).search(phrases, beam=int(opt('--beam', 60)), seed=seed)
        except RuntimeError as ex:
            print('seed', seed, ex); continue
        if not stt['final_ok']: continue
        sc = stt['crossings'] * 3 + stt['figures']
        print('seed', seed, 'crossings', stt['crossings'], 'figures', stt['figures'])
        if best is None or sc > best[0]: best = (sc, d, stt)
    if best is None: raise SystemExit('route search failed for every seed; try --keep-route')
    _, dirs, stt = best
for x, d in zip(chart['taps'], dirs): x['dir'] = d
chart.setdefault('meta', {})['integration'] = {'tool': 'tools/charts/integrate.py', 'source_taps': len(old_dirs), 'trimmed': trimmed, 'route': 'kept from worker' if '--keep-route' in sys.argv else 'route.py search', 'crossings': stt.get('crossings')}
chart['sections'] = secs
(OUT / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
# ---- 3. scenery re-anchoring
def centreline(taps_dirs, h0):
    pts = []; x = z = 0.0; h = h0; t0 = 0.0
    for t, d in taps_dirs + [(dur, None)]:
        dx, dz = HEAD[h]; L = (t - t0) * V
        pts.append((t0, t, x, z, dx, dz)); x += dx * L; z += dz * L; t0 = t
        if d: h = (h + (1 if d == 'R' else -1)) % 4
    return pts
old_cl = centreline([(x['t'], x.get('dir', 'L')) for x in json.loads((D / 'chart.json').read_text())['taps']], H0)
moved = 0
for o in layout.get('objects', []):
    wp = o.get('worldPos')
    if not wp: continue
    ox, oy, oz = wp[0], (wp[1] if len(wp) > 2 else 0), (wp[2] if len(wp) > 2 else wp[1])
    best = None
    for (t0, t1, x0, z0, dx, dz) in old_cl:
        L = (t1 - t0) * V
        u = max(0.0, min(L, (ox - x0) * dx + (oz - z0) * dz))
        px, pz = x0 + dx * u, z0 + dz * u; dist = math.hypot(ox - px, oz - pz)
        ty = t0 + u / V; dy = abs(oy - elev_at(elev, ty))
        score = dist + 2.0 * dy
        if best is None or score < best[0]:
            side = (ox - px) * dz - (oz - pz) * dx      # + = right of travel (heading (dx,dz) -> right (dz,-dx))
            best = (score, ty, side, oy - elev_at(elev, ty))
    _, ty, side, rel_y = best
    o.pop('worldPos'); o['t'] = round(ty, 3); o['side'] = round(side if abs(side) > 0.5 else (2.5 if side >= 0 else -2.5), 2)
    if rel_y > 1.0: o['y'] = round(rel_y, 2)
    o['reanchored'] = 'worldPos -> t/side (integrate.py)'; moved += 1
# Wall/shelf clusters authored as many worldPos boxes along the worker's corridors cannot keep their shape on a new
# route; re-express each cluster (same id prefix, >= 6 members) as a road-hugging row over the same time span.
import re as _re, collections as _col
groups = _col.defaultdict(list)
for o in layout.get('objects', []):
    if o.get('reanchored') and o.get('kind') not in ('group',) and not o.get('landmark'):
        groups[_re.sub(r'[_\-]?\d+$', '', o.get('id', ''))].append(o)
rows_made = 0
for pref, mem in groups.items():
    if len(mem) < 6 or not pref: continue
    ts = sorted(m['t'] for m in mem); sides = [m['side'] for m in mem]
    first = mem[0]; size = first.get('size', [1, 2, 1])
    item = {k: first[k] for k in ('kind', 'size', 'color', 'texture', 'src', 'mode', 'react') if k in first}
    row = {'id': pref + '_row', 'kind': 'row', 't0': round(ts[0], 3), 't1': round(ts[-1] + 0.6, 3),
           'side': round(max(1.9, float(np.median([abs(x) for x in sides]))), 2), 'spacing': round(max(size[0], size[2] if len(size) > 2 else size[0]) + 0.15, 2),
           'bothSides': any(x > 0 for x in sides) and any(x < 0 for x in sides), 'hug': True, 'item': item,
           'note': f'{len(mem)} worldPos pieces of the worker corridor re-expressed as a road-hugging row (integrate.py)'}
    if not row['bothSides'] and sides[0] < 0: row['side'] = -row['side']
    ids = {id(m) for m in mem}
    layout['objects'] = [o for o in layout['objects'] if id(o) not in ids] + [row]; rows_made += 1
print(f'{sid}: {rows_made} wall clusters -> rows')
layout.pop('path', None)
(OUT / 'layout.json').write_text(json.dumps(layout, indent=1, ensure_ascii=False))
# ---- 4. art
if (D / 'art').exists():
    shutil.rmtree(OUT / 'art', ignore_errors=True); shutil.copytree(D / 'art', OUT / 'art')
    (OUT / 'art' / 'CREDITS.md').unlink(missing_ok=True)
print(f'{sid}: route {"kept" if "--keep-route" in sys.argv else "searched"}; crossings {stt.get("crossings")}; {moved} worldPos objects re-anchored; trimmed {len(trimmed)}')
for tr in trimmed: print('   trimmed', tr)
