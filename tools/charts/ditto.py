"""Ditto (NewJeans, 133.98 BPM). Hand-authored chart on the fitted grid (bar = 1.791 s, beat0 = 0.293 s).
Section map derived from tools/audio/grid.py ditto (kick/snare/mid/full 16th rows) + loudness.
Every pattern below names the musical event it follows."""
from common import Grid, Chart
g = Grid('ditto'); c = Chart('ditto', g)

# --- Intro: choir 'woo-ooh', sporadic low kick. Long straights, one tap per bar on the bar's kick.
c.section(0, 'Intro · 雪原', 'intro')
for b in [2, 3, 4, 5, 6]: c.bar(b, [0], 'kick')
c.bar(4, [8], 'melody'); c.bar(6, [8], 'melody')
c.bar(7, [0, 8, 12], 'kick')                      # 7: 'O....   O..' + hat pickup at 12

# --- Hook A: Baltimore-club beat enters (bar 8). Kick accents at steps 3/6/12/15 (dotted-8th feel).
c.section(8, 'Hook · 雪林', 'verse')
for b in [8, 9, 10, 11]: c.bar(b, [0, 6, 12], 'kick')          # 1, a-of-2, 4
for b in [12, 13, 14]: c.bar(b, [0, 3, 6, 12], 'kick')        # add the 'e-and' syncopation
c.bar(15, [0, 2, 4, 6, 8], 'snare'); c.bar(15, [10, 11, 12, 13, 14], 'burst')  # bar 15: full-band fill; snare/full rows are solid 16ths at 10-14 -> 5-tap 16th burst (0.112 s)

# --- Verse: kick on beats, snare/vocal on 8ths.
c.section(16, 'Verse · 校舍', 'verse')
for b in [16, 17, 18, 20, 22]: c.bar(b, [0, 4, 11], 'kick')   # '#...#......#' (11 = 'a' of 3)
for b in [19, 21]: c.bar(b, [0, 4, 8, 11, 14], 'kick')
c.bar(23, [4, 8, 11, 14], 'kick')
c.section(24, 'Verse b · 走廊', 'verse')
for b in [24, 26]: c.bar(b, [0, 3, 6, 8, 12], 'snare')
for b in [25, 27]: c.bar(b, [0, 3, 6, 9, 12], 'kick')        # dotted-8th chain (3-step spacing) on the kick
c.bar(28, [0, 3, 6, 12, 14], 'kick'); c.bar(29, [0, 4, 8, 10, 12], 'snare'); c.bar(30, [0, 3, 6], 'kick'); c.bar(30, [8, 9, 10, 11, 12], 'burst')  # kick row o#o## at 8-12

# --- Pre-chorus: band drops out, kick on beats only -> breathing room, long lines.
c.section(31, 'Pre · 体育馆', 'pre')
c.bar(31, [0, 12], 'kick'); c.bar(32, [0, 8], 'kick'); c.bar(33, [0, 8, 11], 'kick'); c.bar(34, [4, 8], 'kick')
c.bar(35, [0, 4, 8], 'kick'); c.bar(36, [0, 8, 11], 'kick'); c.bar(37, [4, 8, 11, 14], 'kick'); c.bar(38, [0, 4, 8], 'kick')
c.bar(39, [0, 4, 8, 10, 12, 14], 'snare')                   # build: 8th run into the drop

# --- Chorus 1: 'I got no time to lose' — vocal 8ths + kick.
c.section(40, 'Chorus · 雪桥', 'chorus')
for b in range(40, 48):
    if b % 2 == 0: c.bar(b, [0, 4, 6, 10, 12, 14], 'vocal')
    elif b == 47: c.bar(b, [0, 3], 'kick'); c.bar(b, [6, 7, 8, 9, 10], 'burst'); c.bar(b, [12], 'kick')   # hat row #oOOO at 6-10
    else: c.bar(b, [0, 3, 6, 8, 12], 'kick')

# --- Post-chorus: 'Stay in the middle' groove, kick 0/11/15 snare 6/11. Four 4-bar phrases with variation.
c.section(48, 'Post · Stay in the middle', 'post')
P = [[0, 6, 11], [0, 6, 11, 14], [0, 6, 11], [0, 4, 6, 8, 11, 14],
     [0, 3, 6, 11], [0, 6, 11, 14], [0, 3, 6, 11], [0, 6, 8, 10, 12, 14],
     [0, 6, 11, 14], [0, 6, 11, 14], [0, 6, 11, 14], [0, 2, 4, 6, 11, 14],
     [0, 3, 6, 9, 12], [0, 6, 11, 14], [0, 3, 6, 9, 12], [0, 4, 6, 8, 10, 12]]
P[15] = [0, 4, 6, 8, 9, 10, 11, 12, 14]   # bar 63: hat row OOOO at 9-12 + full-band ### -> 16th burst 8-12
for i, steps in enumerate(P): c.bar(48 + i, steps, 'kick' if i % 4 != 3 else 'fill')

# --- Verse 2 / bridge: thinner groove, snare 8ths soft.
c.section(64, 'Bridge · 冰湖', 'bridge')
for b in [64, 66, 68]: c.bar(b, [0, 6, 12], 'kick')
for b in [65, 67, 69]: c.bar(b, [0, 8], 'snare')
c.bar(70, [0, 6, 12], 'kick')
c.section(71, 'Break · 夜', 'break')
c.bar(71, [0], 'kick'); c.bar(72, [0, 12], 'snare'); c.bar(73, [0], 'kick'); c.bar(74, [4, 12], 'snare')
c.bar(75, [4, 15], 'melody'); c.bar(76, [3, 8], 'fx'); c.bar(77, [3, 12], 'melody')
c.bar(78, [0, 4, 8, 10, 12], 'snare')                    # 'o   o .ooooo#' build into the last chorus

# --- Final chorus: heaviest kick section; density peak with two 8-tap 8th runs.
c.section(79, 'Final · 黎明', 'chorus')
F = [[0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 8, 12, 14], [0, 4, 8, 11, 14],
     [0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 8, 12, 14], [0, 2, 4, 6, 8, 10, 12, 14],
     [0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 8, 12, 14], [0, 2, 4, 6, 8, 10, 12, 14],
     [0, 4, 6, 8, 11, 14], [0, 4, 8, 11, 14], [0, 3, 6, 9, 12], [0, 4, 8, 12], [0, 2, 4, 5, 6, 7, 8, 10, 12, 14]]  # bar 95: kick row ooooo at 4-8
for i, steps in enumerate(F): c.bar(79 + i, steps, 'kick' if len(steps) < 8 else 'run')

# --- Outro: choir chords on half-bars, thinning out.
c.section(96, 'Outro · 光', 'outro')
for b in [96, 97, 98, 99]: c.bar(b, [0, 8], 'melody')
c.bar(100, [0], 'melody'); c.bar(101, [0], 'melody')
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
c.save(notes='Hand-authored rhythm on the fitted grid; route directions chosen by tools/charts/route.py (phrase patterns per section, legal multi-level crossings). See docs/design/levels/ditto.md')
