"""Route repair for audited charts (integrator B). Removing a tap removes a 90-degree turn, which rotates everything after
it, so the worker's geometry cannot be kept verbatim. This beam search re-chooses the turn directions phrase by phrase:
it strongly prefers the worker's own turn sequence for the surviving taps ('keep') or its mirror ('flip'), and only falls
back to the Dancing Line figure patterns of route.py when neither is legal. Legality = the validator's rule (no overlap on
the same level unless >= 3 units apart in height or < 1.5 s apart). Speed changes are honoured (unlike route.Router).
Also maps `worldPos` objects rigidly from the old centreline frame to the new one at the same song time."""
import math, random
import numpy as np
from route import PATTERNS, gen_dirs, elev_at
HEAD = [(0, 1), (1, 0), (0, -1), (-1, 0)]
ORDER = ['N', 'E', 'S', 'W']

def speed_fn(chart):
    sp = sorted(chart.get('speed') or [{'t': 0, 'v': 9.0}], key=lambda s: s['t'])
    def dist(a, b):
        d = 0.0; bps = [s['t'] for s in sp if a < s['t'] < b] + [b]; x = a
        for p in bps:
            v = [s['v'] for s in sp if s['t'] <= x + 1e-9]; d += (p - x) * (v[-1] if v else 9.0); x = p
        return d
    return dist

def centreline(chart, dur):
    dist = speed_fn(chart); h = ORDER.index(chart.get('startHeading', 'N')); x = z = 0.0; t0 = 0.0
    nodes = [(0.0, 0.0, 0.0, h)]; last = 'L'
    for tp in chart['taps'] + [{'t': dur}]:
        L = dist(t0, tp['t']); dx, dz = HEAD[h]; x += dx * L; z += dz * L
        if 'dir' in tp or tp['t'] < dur:
            d = tp.get('dir') or ('R' if last == 'L' else 'L'); last = d
            if tp['t'] < dur: h = (h + (1 if d == 'R' else -1)) % 4
        nodes.append((tp['t'], x, z, h)); t0 = tp['t']
    return nodes

def pose(nodes, chart, t):
    """position (x,z) and heading index at song time t"""
    dist = speed_fn(chart)
    for (ta, xa, za, ha), (tb, xb, zb, hb) in zip(nodes, nodes[1:]):
        if ta <= t <= tb or (tb == nodes[-1][0] and t > tb):
            L = dist(ta, t); dx, dz = HEAD[ha]; return xa + dx * L, za + dz * L, ha
    return nodes[-1][1], nodes[-1][2], nodes[-1][3]

class Repair:
    def __init__(self, chart, layout, dur, margin=0.2, min_dt=1.5, min_dy=3.0):
        self.chart = chart; self.elev = layout.get('elevation', []); self.dur = dur
        self.dist = speed_fn(chart); self.h0 = ORDER.index(chart.get('startHeading', 'N'))
        W = sorted(layout.get('road', {}).get('width', [{'t': 0, 'w': 2.2}]), key=lambda w: w['t'])
        self.w_at = lambda t: [w['w'] for w in W if w['t'] <= t + 1e-9][-1] if any(w['t'] <= t + 1e-9 for w in W) else 2.2
        self.margin = margin; self.min_dt = min_dt; self.min_dy = min_dy

    def segs_for(self, x, z, h, t0, times, dirs):
        segs = []
        for t, d in zip(times, dirs):
            dx, dz = HEAD[h]; L = self.dist(t0, t)
            segs.append((t0, t, x, z, x + dx * L, z + dz * L)); x += dx * L; z += dz * L; t0 = t
            h = (h + (1 if d == 'R' else -1)) % 4
        return segs, (x, z, h, t0)

    def arr(self, segs):
        rows = []
        for (t0, t1, x0, z0, x1, z1) in segs:
            w = max(self.w_at(t0), self.w_at(t1)) / 2 + self.margin / 2
            ys = [elev_at(self.elev, t0 + f * (t1 - t0)) for f in (0.02, 0.5, 0.98)]
            rows.append([t0, t1, min(x0, x1) - w, max(x0, x1) + w, min(z0, z1) - w, max(z0, z1) + w, *ys])
        return np.array(rows, dtype=float).reshape(-1, 9)

    def check(self, new, old):
        cross = 0
        for k, r in enumerate(new):
            old_k = np.vstack([old, new[:k]]) if k else old
            if len(old_k) == 0: continue
            m = (r[0] - old_k[:, 1] >= self.min_dt) & (r[2] < old_k[:, 3]) & (old_k[:, 2] < r[3]) & (r[4] < old_k[:, 5]) & (old_k[:, 4] < r[5])
            if not m.any(): continue
            o = old_k[m]
            dy = np.min(np.abs(r[6:9][None, :, None] - o[:, None, 6:9]).reshape(len(o), -1), axis=1)
            if (dy < self.min_dy).any(): return False, 0
            cross += int(m.sum())
        return True, cross

    def search(self, taps, orig_dirs, phrases, beam=50, seed=1):
        """taps: kept times; orig_dirs: the worker's dir for each kept tap; phrases: list of (i0, i1)."""
        rng = random.Random(seed); flip = {'R': 'L', 'L': 'R'}
        states = [dict(dirs=[], segs=np.zeros((0, 9)), end=(0.0, 0.0, self.h0, 0.0), prev='L', score=0.0, cross=0, pats=[])]
        others = ['zig', 'cw', 'ccw', 'uR', 'uL', 'swR', 'swL', 'S', 'Z', 'cwM', 'ccwM']
        for (i0, i1) in phrases:
            times = taps[i0:i1]; n = len(times); nxt = []
            for stt in states:
                cands = [('keep', orig_dirs[i0:i1], 6.0), ('flip', [flip[d] for d in orig_dirs[i0:i1]], 3.0)]
                cands += [(p, gen_dirs(p, stt['prev'], n), 0.0 if p == 'zig' else 1.0) for p in others]
                for name, dirs, bonus in cands:
                    x, z, h, t0 = stt['end']
                    raw, end = self.segs_for(x, z, h, t0, times, dirs)
                    segs = self.arr(raw); ok, cr = self.check(segs, stt['segs'])
                    if not ok: continue
                    score = stt['score'] + bonus + 0.5 * min(cr, 4) + rng.random() * 0.3
                    nxt.append(dict(dirs=stt['dirs'] + list(dirs), segs=np.vstack([stt['segs'], segs]), end=end, prev=dirs[-1] if dirs else stt['prev'], score=score, cross=stt['cross'] + cr, pats=stt['pats'] + [name]))
            if not nxt: raise RuntimeError(f'no legal continuation at tap {i0} (t={taps[i0]:.2f})')
            nxt.sort(key=lambda s: -s['score']); seen, states = set(), []
            for s in nxt:
                k = (round(s['end'][0]), round(s['end'][1]), s['end'][2], s['prev'])
                if k in seen: continue
                seen.add(k); states.append(s)
                if len(states) >= beam: break
        for best in states:
            x, z, h, t0 = best['end']; dx, dz = HEAD[h]; L = self.dist(t0, self.dur)
            ok, _ = self.check(self.arr([(t0, self.dur, x, z, x + dx * L, z + dz * L)]), best['segs'])
            if ok: return best['dirs'], dict(crossings=best['cross'], patterns=best['pats'], keep=best['pats'].count('keep'), flip=best['pats'].count('flip'))
        raise RuntimeError('no legal final leg')

def phrases_for(taps, secs, max_len=8):
    out = []; i = 0; bounds = sorted(s['t'] for s in secs)[1:] + [1e9]
    while i < len(taps):
        b = next(x for x in bounds if x > taps[i] + 1e-6); j = i
        while j < len(taps) and taps[j] < b - 1e-6 and j - i < max_len: j += 1
        out.append((i, j)); i = j
    return out

def remap_worldpos(layout, old_chart, new_chart, dur, log):
    """move each worldPos object rigidly with the centreline frame at the song time where it was closest to the old road"""
    old = centreline(old_chart, dur); new = centreline(new_chart, dur)
    def nearest_t(px, pz):
        best = (1e18, 0.0)
        for (ta, xa, za, ha), (tb, xb, zb, hb) in zip(old, old[1:]):
            dx, dz = xb - xa, zb - za; L2 = dx * dx + dz * dz
            u = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - xa) * dx + (pz - za) * dz) / L2))
            d = (xa + u * dx - px) ** 2 + (za + u * dz - pz) ** 2
            if d < best[0]: best = (d, ta + u * (tb - ta))
        return best[1]
    # sample the old centreline every 0.1 s; anchor each object to the pass whose +-6 s neighbourhood stays closest to it
    # (the section that winds round it), falling back to the object's own t
    samples = []
    tt = 0.0
    while tt < dur:
        x, z, _ = pose(old, old_chart, tt); samples.append((tt, x, z)); tt += 0.1
    S = np.array(samples)
    def anchor_t(px, pz, t_own):
        d = np.hypot(S[:, 1] - px, S[:, 2] - pz)
        near = d < 20
        if not near.any(): return nearest_t(px, pz)
        best = None
        for i in np.where(near)[0][::5]:
            w = (S[:, 0] > S[i, 0] - 6) & (S[:, 0] < S[i, 0] + 6)
            sc = float((d[w] < 15).sum())
            if t_own is not None and abs(S[i, 0] - t_own) < 6: sc += 20   # the designer's own anchor wins unless another pass circles much more
            if best is None or sc > best[0]: best = (sc, S[i, 0])
        # snap to the closest point of that pass
        w = (S[:, 0] > best[1] - 6) & (S[:, 0] < best[1] + 6)
        return float(S[w][np.argmin(d[w]), 0])
    moved = 0
    def walk(o):
        nonlocal moved
        if 'worldPos' in o:
            px, py, pz = o['worldPos']; t = o.get('anchorT', None)
            if t is None: t = anchor_t(px, pz, o.get('t'))
            ox, oz, oh = pose(old, old_chart, t); nx, nz, nh = pose(new, new_chart, t)
            rot = (nh - oh) % 4; c, s = [(1, 0), (0, -1), (-1, 0), (0, 1)][rot]   # heading +1 = 90 deg clockwise seen from above
            rx, rz = px - ox, pz - oz
            # clockwise 90 (N->E): (x,z) -> (z,-x)
            for _ in range(rot): rx, rz = rz, -rx
            o['worldPos'] = [round(nx + rx, 3), py, round(nz + rz, 3)]
            if rot:
                r = o.get('rot', 0)
                if isinstance(r, list): o['rot'] = [r[0], r[1] + 90 * rot, r[2]]
                else: o['rot'] = (r or 0) + 90 * rot
            moved += 1
        for p in o.get('parts', []) or []: pass
    for o in layout.get('objects', []): walk(o)
    log.append(f'worldPos objects remapped: {moved}')
    return moved
