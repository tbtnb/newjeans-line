"""Forward-only route for OMG (user 2026-10-18: '地图还是往前走的' = the map keeps moving forward in ONE overall direction).
Headings are only N (forward), E or W (lateral): from N a tap turns to E (R) or W (L); from E/W the next tap must turn back to N.
So progress along N never decreases and nothing ever doubles back (no self-crossings are even possible except side-by-side strips).
Lateral side policy (deterministic, so the same music gets the same shape): each 2-bar phrase is a staircase to one side and the
side alternates phrase by phrase (a forward zig-zag of staircases); the side flips early if the line would leave the +-XMAX m
corridor, and a side is refused if its next forward strip would touch an earlier strip (road overlap). Usage: route_forward.py [--xmax 12] [--song omg] [--dir levels-src]"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
opt = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
SONG = opt('--song', 'omg'); D = Path(opt('--dir', str(ROOT / 'levels-src'))) / SONG
XMAX = opt('--xmax', 12.0)
ch = json.loads((D / 'chart.json').read_text()); lay = json.loads((D / 'layout.json').read_text())
V = ch['speed'][0]['v']; P = ch['meta']['beat_period']; B0 = ch['meta']['beat0']; PH = 8 * P
W = max(w['w'] for w in lay['road']['width']); dur = json.loads((ROOT / f'analysis/{SONG}.json').read_text())['duration']
T = [x['t'] for x in ch['taps']] + [dur]
x, z, t0, head = 0.0, 0.0, 0.0, 'N'; strips = []; dirs = []
def touches(xn, z0, z1, tnow):
    for (sx, sz0, sz1, st) in strips:
        if tnow - st < 1.5: continue
        if abs(sx - xn) < W + 0.3 and z0 < sz1 + W and sz0 - W < z1: return True
    return False
for i, t in enumerate(T[:-1]):
    L = V * (t - t0)
    if head == 'N':
        strips.append((x, z, z + L, t)); z += L
        nxt = T[i + 1] - t; lat = V * nxt                 # length of the coming lateral leg
        phrase = int((t - B0) // PH); side = 1 if phrase % 2 == 0 else -1
        if abs(x + side * lat) > XMAX and abs(x - side * lat) < abs(x + side * lat): side = -side
        # the forward strip after this lateral leg starts at z and must not touch an earlier strip
        nz1 = z + V * ((T[i + 2] if i + 2 < len(T) else dur) - T[i + 1])
        if touches(x + side * lat, z, nz1, T[i + 1]) and not touches(x - side * lat, z, nz1, T[i + 1]): side = -side
        dirs.append('R' if side > 0 else 'L'); head = 'E' if side > 0 else 'W'
    else:
        x += (L if head == 'E' else -L); dirs.append('L' if head == 'E' else 'R'); head = 'N'
    t0 = t
for tp, d in zip(ch['taps'], dirs): tp['dir'] = d
ch['startHeading'] = 'N'
ch['meta']['route'] = {'tool': 'tools/research/route_forward.py', 'rule': 'forward-only: headings N/E/W, lateral staircase per 2-bar phrase alternating sides, corridor +-%g m' % XMAX}
(D / 'chart.json').write_text(json.dumps(ch, indent=1, ensure_ascii=False))
print(len(dirs), 'dirs; final x %.1f z %.1f' % (x, z))
