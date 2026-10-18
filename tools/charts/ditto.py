"""Ditto (NewJeans, 133.98 BPM). Hand-authored chart on the fitted grid (bar = 1.791 s, beat0 = 0.293 s).
Section map derived from tools/audio/grid.py ditto (kick/snare/mid/full 16th rows) + loudness.
Every pattern below names the musical event it follows."""
from common import Grid, Chart
g = Grid('ditto'); c = Chart('ditto', g)

# --- Rhythm: the shipped chart is worker W2's audited chart (designs-w2 d14bb6a, levels-design/ditto/chart.json, 412 taps):
# one audible layer per section, 7 full-mix-audible 16th fills, faint taps removed (see levels-design/ditto/chart-report.md).
# Only its tap TIMES, tags and sections are used; the geometry (turn directions, elevation, widths) is regenerated below by
# route.py on this repo's elevation/scenery plan. (My earlier rhythm v3 generator stays in ditto_rhythm.py for reference.)
import json as _json
from common import ROOT as _ROOT
_w2 = _json.loads((_ROOT / 'levels-design/ditto/chart.json').read_text())
_FOLLOWS = {'synth / melody hook': 'mid', 'kick + snare drum groove': 'full', 'snare / clap backbeat': 'snare', 'vocal syllables': 'mid', 'kick drum': 'kick'}
_W2_LAYER = ['synth / melody hook', 'kick + snare drum groove', 'kick + snare drum groove', 'snare / clap backbeat', 'vocal syllables',
             'snare / clap backbeat', 'kick drum', 'kick drum', 'kick drum', 'vocal syllables', 'snare / clap backbeat', 'kick + snare drum groove',
             'kick drum', 'kick + snare drum groove', 'snare / clap backbeat']
assert len(_W2_LAYER) == len(_w2['sections'])
for sx, lay in zip(_w2['sections'], _W2_LAYER):
    c.sections.append({'t': sx['t'], 'label': sx['label'], 'kind': sx['kind'], 'follows': _FOLLOWS[lay], 'note': f'W2: {lay}'})
c.taps = [{'t': x['t'], 'tag': x.get('tag', 'beat')} for x in _w2['taps']]
# ---------------- route choreography (v2: replaces the old per-section rotations) ----------------
# Elevation plan (shared with ditto_layout.py via levels-src/ditto/elevation.json):
#   intro spirals UP around the camcorder (+5) so its 4th leg passes over the 1st; fall into the gym at the pre-chorus;
#   post-chorus climbs onto the school-roof level; the night break drops below everything (passes under earlier roads);
#   the final chorus climbs a staircase spiral towards dawn, crossing over earlier laps.
import json
from common import ROOT
from route import Router
c.taps.sort(key=lambda x: x['t'])
T = g.t
taps = [x['t'] for x in c.taps]
def first_gap_after(t, min_gap):
    for a, b in zip(taps, taps[1:]):
        if a >= t and b - a >= min_gap: return a
    raise ValueError(t)
elev = [
    {'type': 'ramp', 't0': round(T(2), 3), 't1': round(T(7, 8), 3), 'dy': 5},
    {'type': 'fall', 't': round(first_gap_after(T(31), 1.0) + 0.12, 3), 'dy': -5},
    {'type': 'ramp', 't0': round(T(48), 3), 't1': round(T(53), 3), 'dy': 5},
    {'type': 'fall', 't': round(first_gap_after(T(71), 1.2) + 0.15, 3), 'dy': -7},
    {'type': 'ramp', 't0': round(T(79), 3), 't1': round(T(95), 3), 'dy': 10},
    {'type': 'ramp', 't0': round(T(97), 3), 't1': round(T(102), 3), 'dy': 3},
]
WID = [(0, 2.6), (8, 2.3), (16, 2.1), (31, 2.3), (40, 1.9), (64, 2.1), (79, 1.9), (96, 2.4)]
def width_at(t):
    w = 2.6
    for b, x in WID:
        if T(b) <= t + 1e-9: w = x
    return w
DENSE = ['zig', 'cw', 'ccw', 'swR', 'swL', 'cwM', 'ccwM', 'S', 'Z']
SPARSE = ['uR', 'uL', 'swR', 'swL', 'sR', 'sL', 'cw', 'ccw', 'S', 'Z']
plan = [  # (bar0, bar1, bars per phrase, patterns)
    (0, 8, 2, ['sR', 'uR', 'swR', 'cw', 'cwM']),  # intro: clockwise spiral up around the camcorder
    (8, 16, 2, DENSE),                       # hook: staircase clusters that swing around
    (16, 24, 2, DENSE),                      # verse: school blocks
    (24, 31, 7, ['zig']),                    # verse b: one long zigzag corridor (walls both sides)
    (31, 40, 3, SPARSE),                     # pre: gym switchbacks
    (40, 48, 2, DENSE),                      # chorus 1
    (48, 64, 2, DENSE + ['uR', 'uL']),       # post
    (64, 71, 2, ['sL', 'sR', 'uL', 'uR', 'swL', 'swR', 'S', 'Z']),   # bridge: skating loops on the ice
    (71, 79, 4, SPARSE),                     # night break, lowest level (passes under)
    (79, 96, 2, ['cw', 'cw', 'cwM', 'swR', 'zig']),  # final: clockwise staircase spiral climbing to dawn
    (96, 104, 8, ['sL', 'sR', 'uL', 'uR', 'zig']),   # outro
]
phrases = []
for b0, b1, step, pats in plan:
    for b in range(b0, b1, step):
        lo, hi = T(b) - 0.01, T(min(b + step, b1)) - 0.01
        idx = [i for i, t in enumerate(taps) if lo <= t < hi]
        if idx: phrases.append((idx[0], idx[-1] + 1, pats))
assert sum(i1 - i0 for i0, i1, _ in phrases) == len(taps), 'phrases must cover all taps'
dur = 185.548
best = None
for seed in range(1, 7):
    try:
        dirs, st = Router(taps, dur, elev, width_at).search(phrases, beam=60, seed=seed)
    except RuntimeError as e:
        print('seed', seed, e); continue
    if not st['final_ok']: continue
    sc = st['crossings'] * 3 + st['figures']
    print('seed', seed, 'crossings', st['crossings'], 'figures', st['figures'], 'extent', [round(v) for v in st['extent']])
    if best is None or sc > best[0]: best = (sc, dirs, st, seed)
_, dirs, st, seed = best
print('chosen seed', seed, st['patterns'])
for tap, d in zip(c.taps, dirs): tap['dir'] = d
(ROOT / 'levels-src/ditto').mkdir(parents=True, exist_ok=True)
(ROOT / 'levels-src/ditto/elevation.json').write_text(json.dumps({'elevation': elev, 'width': [[round(T(b), 3) if b else 0, w] for b, w in WID]}, indent=1))
c.save(notes='Rhythm: W2 audited chart (designs-w2 d14bb6a); route directions chosen by tools/charts/route.py (phrase patterns per section, legal multi-level crossings). See docs/design/levels/ditto.md')
