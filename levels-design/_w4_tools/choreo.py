"""Route choreography: turn the tap list into a rich route by choosing each tap's R/L.
A song is split into blocks; each block has a texture (rotation schedule). A beam search tries
variants of each texture (side, phase, period) and keeps routes without same-level overlaps
(validator rule: pieces >= 1.5 s apart and height difference < 3) and with clearance margin.
Textures (flip = alternate R/L, 'rotation' = repeat the previous direction once):
  stair            : pure alternation -> long diagonal staircase
  bolt   k         : rotation every k taps, sides alternating -> lightning-bolt zigzag of diagonals
  orbit  k,n       : n rotations to the same side every k taps -> square orbit of staircases (around a landmark)
  serp             : rotation every 2nd tap, sides alternating -> tight serpentine / switchback corridor
  spiral m         : m consecutive same-side turns (R,R,R,R..) -> square corkscrew (needs a ramp to stack laps)
  switch k         : two same-side rotations k taps apart -> U-turn: staircase out, staircase back alongside
  turn             : one rotation at the start -> the flow changes direction
"""
import math, itertools
from route import build, elev_at, HEAD, ORDER

def schedule(tex, bt, t0, t1, side, phase, P, m):
    """bt = tap times inside the block. phase/P in seconds except serp/spiral (taps). Returns [(time, side)]."""
    other = lambda x: 'L' if x == 'R' else 'R'; ev = []
    if tex == 'stair': pass
    elif tex == 'turn': ev = [(t0 + phase, side)]
    elif tex == 'bolt':
        s, t = side, t0 + phase
        while t < t1 - 0.5: ev.append((t, s)); s = other(s); t += P
    elif tex == 'orbit':
        t = t0 + phase
        for _ in range(m):
            if t >= t1 - 0.3: break
            ev.append((t, side)); t += P
    elif tex == 'serp':
        s = side; i = int(phase)
        while i < len(bt) - 1 and len(ev) < m: ev.append((bt[i], s)); s = other(s); i += 2
    elif tex == 'serpL':   # U-turn lanes on the long notes: rotate at taps followed by a gap >= P (s), sides alternating
        s = side; nxt = bt[1:] + [t1]
        for a, b in zip(bt, nxt):
            if b - a >= P - 1e-6 and a >= t0 + phase and len(ev) < m: ev.append((a, s)); s = other(s)
    elif tex == 'spiral':
        i = min(int(phase), max(0, len(bt) - 1)); ev = [(bt[i], side)] * m if bt else []
    elif tex == 'xspiral':  # expanding square spiral: same-side rotations with growing legs (never closes)
        t = t0 + phase; L = P
        for _ in range(m):
            if t >= t1 - 0.3: break
            ev.append((t, side)); t += L; L *= 1.5
    elif tex == 'switch':
        ev = [(t0 + phase, side), (t0 + phase + P, side)]
    elif tex == 'zig':      # switchback pair then back: U-turn right, later U-turn left -> S-bend
        ev = [(t0 + phase, side), (t0 + phase + P, side), (t0 + phase + 2 * P, other(side)), (t0 + phase + 3 * P, other(side))]
    return ev

def apply(taps, blocks_ev, start='R'):
    """blocks_ev: list of [(time, side), ...] per block. Returns dirs."""
    req = [(next((i for i, t in enumerate(taps) if t >= tt - 1e-6), len(taps)), s) for evs in blocks_ev for tt, s in evs]
    req.sort(key=lambda r: r[0])
    dirs = []; last = None; q = 0
    for i in range(len(taps)):
        d = start if last is None else ('R' if last == 'L' else 'L')
        if q < len(req) and i >= req[q][0] and last == req[q][1]:
            d = last; q += 1
        dirs.append(d); last = d
    return dirs

def overlap_count(nodes, elev, W, margin, upto=None, mingap=1.5):
    segs = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
    if upto is not None: segs = [s for s in segs if s[0][0] < upto]
    m = W / 2 + margin
    B = [(min(a[1], b[1]) - m, max(a[1], b[1]) + m, min(a[2], b[2]) - m, max(a[2], b[2]) + m) for a, b in segs]
    cell = 10.0; grid = {}
    for i, b in enumerate(B):
        for gx in range(int(math.floor(b[0] / cell)), int(math.floor(b[1] / cell)) + 1):
            for gz in range(int(math.floor(b[2] / cell)), int(math.floor(b[3] / cell)) + 1):
                grid.setdefault((gx, gz), []).append(i)
    seen = set(); hits = 0; cross = 0
    for lst in grid.values():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                i, j = lst[a], lst[b]
                if i > j: i, j = j, i
                if j < i + 2 or (i, j) in seen: continue
                seen.add((i, j))
                if segs[j][0][0] - segs[i][1][0] < mingap: continue
                p, q = B[i], B[j]
                if p[0] < q[1] and q[0] < p[1] and p[2] < q[3] and q[2] < p[3]:
                    ti = (segs[i][0][0] + segs[i][1][0]) / 2; tj = (segs[j][0][0] + segs[j][1][0]) / 2
                    if abs(elev_at(elev, ti) - elev_at(elev, tj)) < 3: hits += 1
                    else: cross += 1
    return hits, cross

def search(taps, speeds, dur, blocks, elev, W, margin=0.6, beam=8, start='N', verbose=True):
    """blocks: [{'t0':..,'tex':..,'sides':['R','L'],'phases':[..],'P':[..],'m':[..],'cross':n,'bias':{}}]"""
    states = [([], 0.0)]
    for bi, b in enumerate(blocks):
        t0 = b['t0']; t1 = blocks[bi + 1]['t0'] if bi + 1 < len(blocks) else dur
        bt = [t for t in taps if t0 <= t < t1]; cand = []
        variants = list(itertools.product(b.get('sides', ['R', 'L']), b.get('phases', [0.0]), b.get('P', [4.0]), b.get('m', [3])))
        for evs, sc in states:
            for side, ph, P, m in variants:
                ev = schedule(b['tex'], bt, t0, t1, side, ph, P, m)
                e2 = evs + [ev]
                dirs = apply(taps, e2)
                nodes = build(taps, dirs, speeds, dur, start)
                hits, cross = overlap_count(nodes, elev, W, margin, upto=t1 + b.get('look', 2.0))
                end = [nd for nd in nodes if nd[0] <= t1][-1]
                old = [nd for nd in nodes if nd[0] < t1 - 8]
                clear = min([math.hypot(end[1] - o[1], end[2] - o[2]) for o in old] or [60])
                want = b.get('cross', 0)
                bonus = min(clear, 40) * b.get('cw', 0.15) + (25 if want and cross >= want else 0) + b.get('bias', {}).get(side, 0)
                cand.append((sc + bonus - 1000 * hits, sc + bonus, e2, hits, cross, side, ph, P, m))
        cand.sort(key=lambda c: -c[0])
        uniq = []; seen = set()
        for c in cand:
            key = tuple(apply(taps, c[2]))
            if key in seen: continue
            seen.add(key); uniq.append(c)
            if len(uniq) >= beam: break
        states = [(c[2], c[1]) for c in uniq]
        if verbose:
            c = uniq[0]; print(f"  block {bi} t0={t0:.2f} {b['tex']:6s} n={len(bt):3d} hits {c[3]} cross {c[4]} side {c[5]} ph {c[6]} P {c[7]} m {c[8]}")
    best = states[0][0]
    return apply(taps, best), best
