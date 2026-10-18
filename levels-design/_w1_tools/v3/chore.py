"""Route choreography planner (v3). Each tap turns 90 deg; we choose L/R per tap so every section gets its own
route texture (staircases, zigzag corridors, switchbacks, spirals over ramps, meanders, forced U-turns), with a
depth-first search over move variants that keeps the road free of same-level overlaps (exact mirror of
levels-design/validate.py: bbox overlap, >=1.5 s apart, dy<3 on a 3x3 sample)."""
import math, itertools
import numpy as np
ORDER = ['N', 'E', 'S', 'W']; HEAD = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
OPP = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
def turn(h, d): return ORDER[(ORDER.index(h) + (1 if d == 'R' else -1)) % 4]
def dir_to(h, h2):
    k = (ORDER.index(h2) - ORDER.index(h)) % 4
    return 'R' if k == 1 else 'L' if k == 3 else None
def flip(d): return 'L' if d == 'R' else 'R'

def elev_at(elev, t):
    y = 0.0
    for e in elev:
        if e['type'] in ('fall', 'jump') and e['t'] <= t: y += e['dy']
        if e['type'] == 'ramp':
            if t >= e['t1']: y += e['dy']
            elif t > e['t0']: y += e['dy'] * (t - e['t0']) / (e['t1'] - e['t0'])
    return y
def speed_at(sp, t):
    v = 9.0
    for s in sp:
        if s['t'] <= t + 1e-9: v = s['v']
    return v
def w_at(widths, t):
    w = 2.2
    for x in widths:
        if x['t'] <= t: w = x['w']
    return w

class Planner:
    def __init__(self, T, dur, speed, widths, elev, moves, start='N', max_tries=60000, patience=3):
        self.T = list(T); self.dur = dur; self.speed = sorted(speed, key=lambda s: s['t']); self.widths = sorted(widths, key=lambda w: w['t'])
        self.elev0 = list(elev); self.moves = sorted(moves, key=lambda m: m['t0']); self.start = start; self.max_tries = max_tries; self.patience = patience
        self.bps = sorted(set([0.0] + [s['t'] for s in self.speed]))
        # tap index ranges per move
        for k, m in enumerate(self.moves):
            t1 = self.moves[k + 1]['t0'] if k + 1 < len(self.moves) else 1e9
            m['_i0'] = next((i for i, t in enumerate(self.T) if t >= m['t0'] - 1e-6), len(self.T))
            m['_i1'] = next((i for i, t in enumerate(self.T) if t >= t1 - 1e-6), len(self.T))
        self.tries = 0
    def dist(self, t0, t):
        d, a = 0.0, t0
        for b in [p for p in self.bps if t0 < p < t] + [t]:
            d += (b - a) * speed_at(self.speed, a); a = b
        return d
    # ---- direction rules
    def move_dirs(self, m, var, h, last, lastA):
        i0, i1 = m['_i0'], m['_i1']; out = []; kind = m['kind']
        for k, i in enumerate(range(i0, i1)):
            if kind == 'alt':
                d = flip(last)
                if k == 0 and var.get('first'): d = var['first']
            elif kind in ('stair', 'zig'):
                diags = var['diags']; per = var.get('every') or m.get('every', 10 ** 6)
                D = diags[(k // per) % len(diags)] if m.get('cycle') else diags[min(k // per, len(diags) - 1)]
                if h in D: d = dir_to(h, D[1] if h == D[0] else D[0])
                else: d = 'R' if turn(h, 'R') in D else 'L'
            elif kind == 'serp':
                A, P = var['A'], var['P']
                if h in A: d = dir_to(h, P) or dir_to(h, OPP[P])
                else:
                    nxt = OPP[lastA] if (lastA and lastA in A) else A[0]
                    d = dir_to(h, nxt)
            elif kind == 'spiral':
                d = var['turn']
                ev = var.get('every')
                if ev and k % ev == ev - 1: d = flip(var['turn'])
            elif kind in ('lspiral', 'lserp'):
                g = (self.T[i + 1] - self.T[i]) if i + 1 < len(self.T) else 9
                thr = m.get('thr', 0.5)
                if k == 0:
                    if kind == 'lspiral': tgt = turn(h, var['turn'] if not var.get('alt0') else flip(var['turn']))
                    else: tgt = var['A0'] if dir_to(h, var['A0']) else OPP[var['A0']] if dir_to(h, OPP[var['A0']]) else var['A0']
                if g >= thr:
                    if dir_to(h, tgt):
                        d = dir_to(h, tgt)
                        tgt = turn(tgt, var['turn']) if kind == 'lspiral' else OPP[tgt]
                    else:
                        d = var['turn'] if kind == 'lspiral' else (dir_to(h, var['P']) or flip(last))
                else:
                    if h in (tgt, OPP[tgt]):
                        d = flip(last) if kind == 'lspiral' else (dir_to(h, var['P']) or flip(last))
                    else:
                        d = dir_to(h, tgt)
            elif kind == 'pattern':
                p = var['pat']; d = p[(k + var.get('off', 0)) % len(p)]
            else: raise ValueError(kind)
            out.append(d); last = d; h = turn(h, d)
            if h in ('E', 'W') and m.get('kind') == 'serp' and var['A'] == 'EW': lastA = h
            if h in ('N', 'S') and m.get('kind') == 'serp' and var['A'] == 'NS': lastA = h
        return out, h, last, lastA
    def variants(self, m):
        k = m['kind']
        if k == 'alt': return [{'first': None}, {'first': 'flip'}]
        if k == 'stair':
            pref = m.get('diag'); allD = ['NE', 'SE', 'SW', 'NW']
            lst = ([pref] if pref else []) + [x for x in m.get('alts', allD) if x != pref]
            return [{'diags': [d]} for d in lst]
        if k == 'zig':
            pairs = [m['diags']] + m.get('alts', [])
            if not m.get('strict'):
                rot = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
                base = m['diags']
                for r in range(1, 4):
                    pp = [''.join(sorted(rot_n(c, r) for c in dd)) for dd in base]
                    pairs.append(pp)
                pairs.append(list(reversed(base)))
            evs = m.get('everys', [m.get('every')])
            return [{'diags': [canon(d) for d in p], 'every': ev} for ev in evs for p in pairs]
        if k == 'serp':
            combos = [(m['A'], m['P'])] + [(a, p) for a in ('EW', 'NS') for p in (['N', 'S'] if a == 'EW' else ['E', 'W']) if (a, p) != (m['A'], m['P'])]
            return [{'A': a, 'P': p} for a, p in combos]
        if k == 'spiral':
            dys = m.get('dys', [None])
            evs = m.get('everys', [None])
            return [{'turn': tr, 'dy': dy, 'every': ev} for ev in evs for dy in dys for tr in ([m['turn'], flip(m['turn'])] if not m.get('strict') else [m['turn']])]
        if k == 'lspiral':
            dys = m.get('dys', [None])
            return [{'turn': tr, 'dy': dy, 'alt0': a0} for dy in dys for a0 in (False, True) for tr in ([m['turn'], flip(m['turn'])] if not m.get('strict') else [m['turn']])]
        if k == 'lserp':
            combos = [(m['A0'], m['P'])] + [(a, p) for a in 'NESW' for p in 'NESW' if dir_to(a, p) and (a, p) != (m['A0'], m['P'])]
            return [{'A0': a, 'P': p} for a, p in combos]
        if k == 'pattern':
            pats = [m['pat']] + ([''.join(flip(c) for c in m['pat'])] if not m.get('strict') else [])
            return [{'pat': p, 'off': o} for p in pats for o in range(len(m['pat']) if m.get('shift', True) else 1)]
        raise ValueError(k)
    # ---- geometry + overlap
    def extend(self, nodes, dirs_all, upto):
        """nodes: list of (t,x,z,heading) for completed segment starts; returns nodes extended through tap index upto-1
        (the segment that starts at tap upto-1 is complete because its end is T[upto] or dur)."""
        nodes = list(nodes)
        while len(nodes) - 1 < upto:
            k = len(nodes) - 1          # tap index whose segment end we add
            t0, x, z, h = nodes[-1]
            t = self.T[k] if k < len(self.T) else self.dur
            dx, dz = HEAD[h]; L = self.dist(t0, t); x += dx * L; z += dz * L
            h2 = turn(h, dirs_all[k]) if k < len(self.T) else h
            nodes.append((t, x, z, h2))
        return nodes
    def seg_box(self, a, b):
        W = max(w_at(self.widths, a[0]), w_at(self.widths, b[0]))
        return (min(a[1], b[1]) - W / 2, max(a[1], b[1]) + W / 2, min(a[2], b[2]) - W / 2, max(a[2], b[2]) + W / 2)
    def check(self, nodes, elev, from_seg):
        segs = list(zip(nodes, nodes[1:]))
        if len(segs) < 3: return []
        B = np.array([self.seg_box(a, b) for a, b in segs]); TS = np.array([a[0] for a, b in segs]); TE = np.array([b[0] for a, b in segs])
        for j in range(max(from_seg, 2), len(segs)):
            bj = B[j]; i = np.arange(0, j - 1)
            m = (TS[j] - TE[i] >= 1.5) & (B[i, 0] < bj[1]) & (bj[0] < B[i, 1]) & (B[i, 2] < bj[3]) & (bj[2] < B[i, 3])
            for ii in i[m]:
                si, sj = segs[ii], segs[j]
                dyv = min(abs(elev_at(elev, si[0][0] + f * (si[1][0] - si[0][0])) - elev_at(elev, sj[0][0] + g * (sj[1][0] - sj[0][0])))
                          for f in (0.02, 0.5, 0.98) for g in (0.02, 0.5, 0.98))
                if dyv < 3: return [(round(si[0][0], 2), round(sj[0][0], 2))]
        return []
    def solve(self):
        self.best_fail = None
        res = self._dfs(0, [(0.0, 0.0, 0.0, self.start)], [], self.start, 'L', None, list(self.elev0))
        if res is None: raise RuntimeError(f'no route found; deepest failure {self.best_fail}')
        return res
    def _dfs(self, mi, nodes, dirs, h, last, lastA, elev):
        """returns result tuple, or None. self.internal is set when the child failed purely inside itself
        with every variant (then the parent's choices cannot help except through the entry heading)."""
        if mi == len(self.moves):
            n2 = self.extend(nodes, dirs, len(self.T) + 1)
            if self.check(n2, elev, len(nodes) - 1): self.internal = False; return None
            return dirs, n2, elev, self.choice
        m = self.moves[mi]
        if mi == 0: self.choice = {}
        all_internal = True; tried_entry = set()
        vlist = []
        for var in self.variants(m):
            v = dict(var)
            if v.get('first') == 'flip': v['first'] = last
            d2, h2, l2, la2 = self.move_dirs(m, v, h, last, lastA)
            vlist.append((v, d2, h2, l2, la2))
        if m.get('toward'):
            tx, tz = m['toward']
            def endd(item):
                n2 = self.extend(nodes, dirs + item[1], m['_i1'])
                return math.hypot(n2[-1][1] - tx, n2[-1][2] - tz)
            vlist.sort(key=endd)
        for v, d2, h2, l2, la2 in vlist:
            self.tries += 1
            if self.tries > self.max_tries: self.internal = False; return None
            el = list(elev)
            if m['kind'] in ('spiral', 'lspiral') and v.get('dy') is not None:
                r0 = m.get('rt0', m['t0']); r1 = m.get('rt1', self.T[m['_i1'] - 1] + 0.3 if m['_i1'] > m['_i0'] else m['t0'] + 1)
                dy = v['dy'] if not m.get('rate') else round(v['dy'] * (r1 - r0), 1)
                el.append({'type': 'ramp', 't0': round(r0, 3), 't1': round(r1, 3), 'dy': dy, '_auto': m['name']})
            dd = dirs + d2
            n2 = self.extend(nodes, dd, m['_i1'])
            hit = self.check(n2, el, len(nodes) - 1)
            if hit:
                if self.best_fail is None or mi > self.best_fail[0]: self.best_fail = (mi, m['name'], hit); self.fail_nodes = (n2, el, v)
                if hit[0][0] < m['t0'] - 0.01: all_internal = False
                continue
            self.choice[m['name']] = v
            r = self._dfs(mi + 1, n2, dd, h2, l2, la2, el)
            if r is not None: return r
            if not self.internal: all_internal = False
            else:
                # child failed internally: only a different exit heading / position can help; skip variants giving same exit state
                key = (h2, l2, round(n2[-1][1], 1), round(n2[-1][2], 1))
                if key in tried_entry: continue
                tried_entry.add(key)
                if len(tried_entry) >= self.patience: break
        self.internal = all_internal and mi > 0
        return None

def rot_n(c, r):
    o = ORDER.index(c); return ORDER[(o + r) % 4]
def canon(d):
    s = set(d)
    for k in ('NE', 'SE', 'SW', 'NW'):
        if set(k) == s: return k
    raise ValueError(d)
