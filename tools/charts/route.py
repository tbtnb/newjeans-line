"""Route choreography search: given a fixed (musically authored) tap rhythm and an elevation plan, choose the
turn directions phrase by phrase so the road forms Dancing Line figures (staircases, switchbacks, U-turns,
spirals, multi-level crossings) without ever overlapping itself on the same level.
The centreline model is identical to the engine (src/core/path.ts): constant speed, 90-degree turns.
"""
import math, random
import numpy as np
HEAD = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # N E S W

def elev_at(elev, t):
    y = 0.0
    for e in elev:
        if e['type'] in ('fall', 'jump') and e['t'] <= t: y += e['dy']
        elif e['type'] == 'ramp':
            if t >= e['t1']: y += e['dy']
            elif t > e['t0']: y += e['dy'] * (t - e['t0']) / (e['t1'] - e['t0'])
    return y

PATTERNS = {
    'zig': [], 'cw': [(0, 'R')], 'ccw': [(0, 'L')], 'uR': [(0, 'R'), (0, 'R')], 'uL': [(0, 'L'), (0, 'L')],
    'cwM': [(0.5, 'R')], 'ccwM': [(0.5, 'L')], 'sw R': [(0, 'R'), (0.5, 'R')], 'swL': [(0, 'L'), (0.5, 'L')],
    'S': [(0, 'R'), (0.5, 'L')], 'Z': [(0, 'L'), (0.5, 'R')], 'sR': 'all R', 'sL': 'all L',
}
PATTERNS['swR'] = PATTERNS.pop('sw R')

def gen_dirs(pattern, prev, n):
    p = PATTERNS[pattern]
    if p == 'all R': return ['R'] * n
    if p == 'all L': return ['L'] * n
    pend = list(p); out = []
    for i in range(n):
        alt = 'R' if prev == 'L' else 'L'
        d = alt
        if pend and i / max(n, 1) >= pend[0][0] - 1e-9 and pend[0][1] == prev:
            d = prev; pend.pop(0)
        out.append(d); prev = d
    return out

class Router:
    def __init__(self, taps, dur, elev, width_at, speed=9.0, start_heading=0, margin=0.9, min_dt=1.5, min_dy=3.0):
        self.taps = taps; self.dur = dur; self.elev = elev; self.width_at = width_at; self.v = speed
        self.h0 = start_heading; self.margin = margin; self.min_dt = min_dt; self.min_dy = min_dy

    def segs_for(self, x, z, h, t0, times, dirs):
        """segments from (x,z,h) at t0 through tap times (turning with dirs); returns segs, end state"""
        segs = []
        for t, d in zip(times, dirs):
            dx, dz = HEAD[h]; L = (t - t0) * self.v
            segs.append((t0, t, x, z, x + dx * L, z + dz * L)); x += dx * L; z += dz * L; t0 = t
            h = (h + (1 if d == 'R' else -1)) % 4
        return segs, (x, z, h, t0)

    def arr(self, segs):
        """numpy rows: [t0, t1, xmin, xmax, zmin, zmax, y@5%, y@50%, y@95%]"""
        rows = []
        for (t0, t1, x0, z0, x1, z1) in segs:
            w = max(self.width_at(t0), self.width_at(t1)) / 2 + self.margin / 2
            ys = [elev_at(self.elev, t0 + f * (t1 - t0)) for f in (0.05, 0.5, 0.95)]
            rows.append([t0, t1, min(x0, x1) - w, max(x0, x1) + w, min(z0, z1) - w, max(z0, z1) + w, *ys])
        return np.array(rows, dtype=float).reshape(-1, 9)

    def check(self, new, old):
        """new, old: arrays from arr(). returns (ok, crossings)"""
        cross = 0
        for k, r in enumerate(new):
            old_k = np.vstack([old, new[:k]]) if k else old   # also against earlier segments of the same phrase
            if len(old_k) == 0: continue
            m = (r[0] - old_k[:, 1] >= self.min_dt) & (r[2] < old_k[:, 3]) & (old_k[:, 2] < r[3]) & (r[4] < old_k[:, 5]) & (old_k[:, 4] < r[5])
            if not m.any(): continue
            o = old_k[m]
            dy = np.min(np.abs(r[6:9][None, :, None] - o[:, None, 6:9]).reshape(len(o), -1), axis=1)
            if (dy < self.min_dy).any(): return False, 0
            cross += int(m.sum())
        return True, cross

    def search(self, phrases, beam=40, seed=1, bbox_soft=260.0, w_cross=6.0, w_turnfig=1.0):
        """phrases: list of (i0, i1, [pattern names]) covering tap indices [i0, i1). Returns dirs, stats."""
        rng = random.Random(seed)
        states = [dict(dirs=[], segs=np.zeros((0, 9)), end=(0.0, 0.0, self.h0, 0.0), prev='L', score=0.0, cross=0, figs=0, ext=(0, 0, 0, 0))]
        for (i0, i1, pats) in phrases:
            times = self.taps[i0:i1]; n = len(times)
            gaps = [b - a for a, b in zip(self.taps[max(0, i0 - 1):i1], self.taps[max(0, i0 - 1) + 1:i1])]
            nxt = []
            for st in states:
                for p in pats:
                    if PATTERNS[p] in ('all R', 'all L') and gaps and min(gaps) < 0.38: continue  # spirals only where legs are long enough to read
                    dirs = gen_dirs(p, st['prev'], n)
                    x, z, h, t0 = st['end']
                    raw, end = self.segs_for(x, z, h, t0, times, dirs)
                    segs = self.arr(raw)
                    ok, cr = self.check(segs, st['segs'])
                    if not ok: continue
                    allx = [s[2] for s in raw] + [s[4] for s in raw]; allz = [s[3] for s in raw] + [s[5] for s in raw]
                    e = st['ext']; ext = (min(e[0], *allx), max(e[1], *allx), min(e[2], *allz), max(e[3], *allz))
                    span = max(ext[1] - ext[0], ext[3] - ext[2])
                    figs = 0 if p == 'zig' else (2 if p in ('uR', 'uL', 'swR', 'swL', 'sR', 'sL') else 1)
                    score = st['score'] + w_cross * min(cr, 4) + w_turnfig * figs - max(0.0, span - bbox_soft) * 0.05 + rng.random() * 0.8
                    nxt.append(dict(dirs=st['dirs'] + dirs, segs=np.vstack([st['segs'], segs]), end=end, prev=dirs[-1] if dirs else st['prev'], score=score, cross=st['cross'] + cr, figs=st['figs'] + figs, ext=ext, pats=st.get('pats', []) + [p]))
            if not nxt: raise RuntimeError(f'no legal continuation for phrase starting at tap {i0} (t={self.taps[i0]:.2f})')
            nxt.sort(key=lambda s: -s['score'])
            # keep diversity: unique last-pattern signature
            seen, states = set(), []
            for s in nxt:
                k = (round(s['end'][0]), round(s['end'][1]), s['end'][2], s['prev'])
                if k in seen: continue
                seen.add(k); states.append(s)
                if len(states) >= beam: break
        best = states[0]
        # final leg to the end must also be legal
        x, z, h, t0 = best['end']; dx, dz = HEAD[h]; L = (self.dur - t0) * self.v
        last = (t0, self.dur, x, z, x + dx * L, z + dz * L)
        ok, _ = self.check(self.arr([last]), best['segs'])
        return best['dirs'], dict(crossings=best['cross'], figures=best['figs'], patterns=best['pats'], extent=best['ext'], final_ok=ok)
