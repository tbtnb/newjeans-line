"""Prepare levels-src/omg for the user's own taps (level ends where their taps end, ~158 s).
Sets layout.endTime (the first downbeat at least 1 bar after the last tap, i.e. 1-2 bars after it) + endFade 1.5 s, drops every
time-keyed layout/chart entry at or after the end (sections, camera cues, road reveals, objects, events), moves the falls to
the user's chorus/drop downbeat taps (>= 0.45 s to the next tap), and places the 2 crowns at ~1/3 and ~2/3 in calm gaps.
Run BEFORE tools/charts/import_taps.py (the import keeps chart sections and the layout). Usage: omg_user_level.py <snap.json>"""
import json, sys, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; D = ROOT / 'levels-src/omg'
snap = json.load(open(sys.argv[1])); T = [x['t'] for x in snap['taps']]
ch = json.loads((D / 'chart.json').read_text()); lay = json.loads((D / 'layout.json').read_text())
P = 0.4724304864737013; B0 = 0.011; BAR = 4 * P
k = math.ceil((T[-1] + BAR - B0) / BAR - 1e-6); END = round(B0 + k * BAR, 3)          # first downbeat >= 1 bar after the last tap
lay['endTime'] = END; lay['endFade'] = 1.5
cut = lambda lst, key='t': [x for x in lst if x.get(key, 0) < END - 1.0]
ch['sections'] = [s for s in ch['sections'] if s['t'] < END - 2.0]
lay['sections'] = [s for s in lay['sections'] if s['t'] < END - 2.0]
lay['camera'] = cut(lay.get('camera', [])); lay['road']['reveal'] = cut(lay['road']['reveal'])
lay['road']['width'] = [w for w in lay['road']['width'] if w['t'] < END - 1.0] or lay['road']['width'][:1]
lay['events'] = cut(lay.get('events', [])); lay['objects'] = [o for o in lay.get('objects', []) if o.get('t', 0) < END - 1.0]
def fall_at(target, dy):
    c = [t for i, t in enumerate(T[:-1]) if T[i + 1] - t >= 0.45 and abs(t - target) < 1.0]
    t = min(c, key=lambda x: abs(x - target)); t = B0 + round((t - B0) / (P / 4)) * (P / 4)
    return {'t': round(max(t, round(t, 3)), 6), 'type': 'fall', 'dy': dy}   # at (not before) that tap, both exact and as stored (3 dp): the fall starts on that turn
ramps = [e for e in lay['elevation'] if e['type'] == 'ramp' and e['t1'] < END - 1.0]
secs = {s.get('kind'): [] for s in ch['sections']}
for s in ch['sections']: secs[s.get('kind')].append(s['t'])
falls = [fall_at(t, dy) for t, dy in zip(secs.get('chorus', [])[:2] + secs.get('drop', [])[:1], (-4, -6, -8))]
lay['elevation'] = sorted(falls + ramps, key=lambda e: e.get('t', e.get('t0')))
def crown_near(target):
    best = None
    for a, b in zip(T, T[1:]):
        if b - a >= 0.45 and abs(a - target) < 4 and not any(abs(f['t'] - a) < 0.6 for f in falls):
            if best is None or abs(a - target) < abs(best - target): best = a
    return round(best + 0.1, 3)
lay['crowns'] = [{'t': crown_near(END / 3)}, {'t': crown_near(2 * END / 3)}]
(D / 'chart.json').write_text(json.dumps(ch, indent=1, ensure_ascii=False)); (D / 'layout.json').write_text(json.dumps(lay, indent=1, ensure_ascii=False))
print('endTime', END, 'last tap', T[-1], '| sections', [(round(s['t'], 1), s.get('kind')) for s in ch['sections']])
print('elevation', lay['elevation']); print('crowns', lay['crowns'])
