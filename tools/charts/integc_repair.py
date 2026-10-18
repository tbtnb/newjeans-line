#!/usr/bin/env python3
"""Remove chart taps and repair the route locally (integ-c, 2026-10-18).
Every tap turns 90 deg, so dropping one tap flips the heading parity of everything after it (a straight that ran N now
runs E), so the old route cannot simply continue. Removals are processed in groups (taps < 4 s apart). For each group a
short window after the first removed tap is re-planned (beam search over turn directions that tracks the original
centreline and obeys the validator's same-level overlap rule), and the designer's remaining route is then re-attached
VERBATIM as a rigid copy (rotation by k*90 deg + translation; k = 0 and zero translation whenever parity allows, i.e. an
exact re-join). The join is chosen to keep every validator rule and to maximise multi-level crossings while preferring
the identity transform and the shortest window. worldPos objects after the join get the same rigid transform (rot += 90k),
objects inside the window move with the local route displacement, and anything the edit pushed into the road is nudged out.
Usage: integc_repair.py <slug> <t1,t2,...> [--beam 400] [--why "t:reason;..."]"""
import json, sys, math, subprocess
import numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
HEAD = [(0, 1), (1, 0), (0, -1), (-1, 0)]; ORDER = ['N', 'E', 'S', 'W']

def opt(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
slug = sys.argv[1]; REM = [float(x) for x in sys.argv[2].split(',') if x]
BEAM = int(opt('--beam', 400)); GROUP_S = float(opt('--group', 4.0)); MINCROSS = int(opt('--mincross', 0))
D = ROOT / 'levels-src' / slug
chart = json.loads((D / 'chart.json').read_text()); layout = json.loads((D / 'layout.json').read_text())
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(ROOT / f'public/audio/{slug}.mp3')], capture_output=True, text=True).stdout)
speeds = sorted(chart.get('speed') or [{'t': 0, 'v': 9.0}], key=lambda s: s['t'])
def v_at(t):
    v = 9.0
    for s in speeds:
        if s['t'] <= t + 1e-9: v = s['v']
    return v
BPS = sorted(set([0.0] + [s['t'] for s in speeds]))
def dist(a, b):
    d, x = 0.0, a
    for p in [p for p in BPS if a < p < b] + [b]: d += (p - x) * v_at(x); x = p
    return d
def elev(t):
    y = 0.0
    for e in layout.get('elevation', []):
        if e['type'] in ('fall', 'jump') and e['t'] <= t: y += e['dy']
        if e['type'] == 'ramp':
            if t >= e['t1']: y += e['dy']
            elif t > e['t0']: y += e['dy'] * (t - e['t0']) / (e['t1'] - e['t0'])
    return y
WID = sorted(layout.get('road', {}).get('width', [{'t': 0, 'w': 2.2}]), key=lambda w: w['t'])
def w_at(t):
    w = 2.2
    for x in WID:
        if x['t'] <= t: w = x['w']
    return w

def nodes_of(times, dirs):
    h = ORDER.index(chart.get('startHeading', 'N')); x = z = t0 = 0.0; out = [(0.0, 0.0, 0.0, h)]
    for i, t in enumerate(list(times) + [dur]):
        L = dist(t0, t); x += HEAD[h][0] * L; z += HEAD[h][1] * L
        if i < len(times): h = (h + (1 if dirs[i] == 'R' else -1)) % 4
        out.append((t, x, z, h)); t0 = t
    return out
def pos_at(nodes, t):
    for a, b in zip(nodes, nodes[1:]):
        if a[0] <= t <= b[0]:
            L = dist(a[0], t); return a[1] + HEAD[a[3]][0] * L, a[2] + HEAD[a[3]][1] * L, a[3]
    a = nodes[-1]; return a[1], a[2], a[3]
def row(t0, x0, z0, t1, x1, z1):
    W = max(w_at(t0), w_at(t1)) / 2
    return [t0, t1, min(x0, x1) - W, max(x0, x1) + W, min(z0, z1) - W, max(z0, z1) + W] + [elev(t0 + f * (t1 - t0)) for f in (0.02, 0.5, 0.98)]
def conflicts(r, rows):
    """r: new row; rows: earlier rows EXCLUDING the immediately preceding segment. returns (illegal, crossings)"""
    if len(rows) == 0: return False, 0
    m = (r[0] - rows[:, 1] >= 1.5) & (r[2] < rows[:, 3]) & (rows[:, 2] < r[3]) & (r[4] < rows[:, 5]) & (rows[:, 4] < r[5])
    if not m.any(): return False, 0
    o = rows[m]; dy = np.abs(np.asarray(r[6:9])[None, :, None] - o[:, None, 6:9]).reshape(len(o), -1).min(axis=1)
    return bool((dy < 3).any()), int(m.sum())

def rows_of(nodes): return np.array([row(a[0], a[1], a[2], b[0], b[1], b[2]) for a, b in zip(nodes, nodes[1:])]).reshape(-1, 9)
def check_all(R):
    """validator-exact: same-level overlaps (hits) and multi-level crossings over all segment pairs j >= i+2"""
    n = len(R); I, J = np.triu_indices(n, 2)
    m = (R[J, 0] - R[I, 1] >= 1.5) & (R[I, 2] < R[J, 3]) & (R[J, 2] < R[I, 3]) & (R[I, 4] < R[J, 5]) & (R[J, 4] < R[I, 5])
    I, J = I[m], J[m]
    dy = np.abs(R[I][:, 6:9, None] - R[J][:, None, 6:9]).reshape(len(I), -1).min(axis=1)
    return int((dy < 3).sum()), int((dy >= 3).sum())
def rotk(x, z, k):
    for _ in range(k % 4): x, z = z, -x
    return x, z

def footprint(o):
    if o.get('radius'): r = float(o['radius'])
    else: r = None
    ext = 0.5; top = 1.0; st = [(o, 0.0)]
    while st:
        p, by = st.pop(); sz = p.get('size') or [1, 1, 1]; pp = p.get('pos') or [0, 0, 0]
        ext = max(ext, math.hypot(abs(pp[0]) + sz[0] / 2, abs(pp[2]) + (sz[2] if len(sz) > 2 else sz[0]) / 2))
        top = max(top, by + pp[1] + (sz[1] if len(sz) > 1 else 1) / 2); st += [(q, by + pp[1]) for q in (p.get('parts', []) or [])]
    return (r if r else min(ext, 12.0)), min(top, 30.0)
SKIPK = ('cloud', 'moon', 'sun', 'text', 'plane', 'disc', 'water')
def hits_of(o, R, wp):
    """road decks that pass through the object's volume (footprint radius x [y-1, y+height+1])"""
    if o.get('onroad') or o.get('kind') in SKIPK: return R[:0]
    rad, top = footprint(o); rr = rad * 0.6; y = wp[1] if len(wp) > 1 else 0.0
    m = (R[:, 2] - rr < wp[0]) & (wp[0] < R[:, 3] + rr) & (R[:, 4] - rr < wp[2]) & (wp[2] < R[:, 5] + rr)
    ys = R[:, 6:9]; m &= ((ys > y - 1.0) & (ys < y + top + 1.0)).any(axis=1)
    return R[m]
taps = [dict(x) for x in chart['taps']]
last = 'L'
for x in taps:
    if not x.get('dir'): x['dir'] = 'R' if last == 'L' else 'L'
    last = x['dir']
T_orig = [x['t'] for x in taps]
nodes_design = nodes_of(T_orig, [x['dir'] for x in taps])
_, cross_design = check_all(rows_of(nodes_design))
_DR = rows_of(nodes_design)
BASE_HITS = {id(o): len(hits_of(o, _DR, list(o['worldPos']) + [0] * (3 - len(o['worldPos'])))) for o in layout['objects'] if 'worldPos' in o}
for r in REM: assert min(abs(t - r) for t in T_orig) < 0.003, r
groups = [[float(x) for x in gg.split(',')] for gg in opt('--groups').split('|')] if opt('--groups') else []
for r in ([] if groups else sorted(REM)):
    if groups and r - groups[-1][-1] < GROUP_S: groups[-1].append(r)
    else: groups.append([r])
why = dict(kv.split(':', 1) for kv in (opt('--why', '') or '').split(';') if ':' in kv)
removed_meta = [{'t': x['t'], 'tag': x.get('tag'), 'why': why.get(f"{x['t']:.3f}", '')} for x in taps if any(abs(x['t'] - r) < 0.003 for r in REM)]
log = []
def disp_obj(o, f):
    wp = list(o['worldPos']) + [0] * (3 - len(o['worldPos'])); x, z = f(wp[0], wp[2]); o['worldPos'] = [round(x, 2), wp[1], round(z, 2)]
for g in groups:
    T0 = [x['t'] for x in taps]; D0 = [x['dir'] for x in taps]
    orig = nodes_of(T0, D0); orig_rows = rows_of(orig)
    rm = {min(range(len(T0)), key=lambda k: abs(T0[k] - r)) for r in g}
    keep = [i for i in range(len(T0)) if i not in rm]; T1 = [T0[i] for i in keep]; Dk = [D0[i] for i in keep]
    k0 = next(k for k, i in enumerate(keep) if i > min(rm)); last_rm = max(T0[i] for i in rm)
    pre_nodes = nodes_of(T1[:k0], Dk[:k0])[:-1]; prefix_rows = rows_of(pre_nodes); s0 = pre_nodes[-1]
    oh = {a[0]: a[3] for a in orig}
    # original remainder index in T0 for a kept tap time
    idx0 = {T0[i]: i for i in range(len(T0))}
    states = [(0.0, s0[1], s0[2], s0[3], s0[0], np.zeros((0, 9)), [])]
    cands = []
    horizon = [t for t in T1[k0:] if t <= last_rm + 8.0]
    for t in horizon:
        nxt = []
        for (c, x, z, h, ta, rws, dirs) in states:
            L = dist(ta, t); xb = x + HEAD[h][0] * L; zb = z + HEAD[h][1] * L
            r = row(ta, x, z, t, xb, zb)
            older = np.vstack([prefix_rows, rws[:-1]]) if len(rws) else prefix_rows[:-1]
            bad, _ = conflicts(r, older)
            if bad: continue
            ox, oz, _h = pos_at(orig, t); dev = (xb - ox) ** 2 + (zb - oz) ** 2
            for d in ('R', 'L'):
                nxt.append((c + dev, xb, zb, (h + (1 if d == 'R' else -1)) % 4, t, np.vstack([rws, [r]]), dirs + [d]))
        if not nxt: break
        nxt.sort(key=lambda s: s[0]); seen = set(); states = []
        for s in nxt:
            kk = (round(s[1], 2), round(s[2], 2), s[3])
            if kk in seen: continue
            seen.add(kk); states.append(s)
            if len(states) >= BEAM: break
        if t < last_rm: continue
        # join candidates at t: the segment starting at t follows the original remainder (rigidly transformed)
        jn = T1.index(t); i0 = idx0[t]
        for s in states[:24]:
            k = (s[3] - oh[t]) % 4
            ox, oz, _h = pos_at(orig, t)
            rx, rz = rotk(ox, oz, k); tx, tz = s[1] - rx, s[2] - rz
            full_dirs = Dk[:k0] + s[6] + Dk[jn + 1:]
            nodes = nodes_of(T1, full_dirs); R = rows_of(nodes)
            hits, cross = check_all(R)
            if hits: continue
            ntap = jn - k0 + 1
            bad_obj = 0
            for o in layout['objects']:
                if 'worldPos' not in o or 't' not in o: continue
                wp = list(o['worldPos']) + [0] * (3 - len(o['worldPos']))
                if o['t'] >= t:
                    rx2, rz2 = rotk(wp[0], wp[2], k); wp = [rx2 + tx, wp[1], rz2 + tz]
                elif o['t'] > (T1[k0 - 1] if k0 else 0.0):
                    a = pos_at(orig, o['t']); b = pos_at(nodes, o['t']); wp = [wp[0] + b[0] - a[0], wp[1], wp[2] + b[1] - a[1]]
                bad_obj += max(0, len(hits_of(o, R, wp)) - BASE_HITS.get(id(o), 0))
            score = min(cross, max(cross_design, MINCROSS)) - 2.0 * bad_obj - (2 if k else 0) - 0.01 * math.hypot(tx, tz) - 0.3 * ntap
            cands.append((score, cross, k, (tx, tz), t, full_dirs, nodes, ntap, bad_obj))
        if len(cands) and t - last_rm > 6.0: break
    if not cands: sys.exit(f'no legal join for group {g}')
    cands.sort(key=lambda c: -c[0]); score, cross, k, (tx, tz), tj, full_dirs, new, ntap, bad_obj = cands[0]
    # objects
    def M(x, z):
        rx, rz = rotk(x, z, k); return rx + tx, rz + tz
    t_start = T1[k0 - 1] if k0 else 0.0
    nobj = [0, 0]
    for o in layout['objects']:
        if 'worldPos' not in o or 't' not in o: continue
        if o['t'] >= tj:
            disp_obj(o, M); nobj[0] += 1
            if k:
                if isinstance(o.get('rot'), list): o['rot'][1] = (o['rot'][1] or 0) + 90 * k
                else: o['rot'] = (o.get('rot') or 0) + 90 * k
        elif o['t'] > t_start:
            a = pos_at(orig, o['t']); b = pos_at(new, o['t'])
            disp_obj(o, lambda x, z: (x + b[0] - a[0], z + b[1] - a[1])); nobj[1] += 1
            if o.get('onroad'): log.append(f"WARN onroad object {o.get('id')} sits in a re-planned window")
    for c in layout.get('camera', []):
        if 'worldYaw' in c and c['t'] >= tj and k: c['worldYaw'] = (c['worldYaw'] + 90 * k) % 360
    taps = [dict(taps[i], dir=d) for i, d in zip(keep, full_dirs)]
    log.append(f"group {g}: window {t_start:.3f}-{tj:.3f} s ({ntap} re-planned turns), remainder re-attached with rotation {90*k} deg, translation ({tx:.2f}, {tz:.2f}); crossings {cross}; objects transformed {nobj[0]}, window-moved {nobj[1]}, new object/road intersections before nudge {bad_obj}")
# nudge objects that now intersect the road (compared with the designer's original placement)
final = nodes_of([x['t'] for x in taps], [x['dir'] for x in taps]); FR = rows_of(final); DR = rows_of(nodes_design)
design_layout = json.loads((D / 'layout.json').read_text()); dpos = {o.get('id'): o for o in design_layout['objects']}
nudged, stuck = [], []
for o in layout['objects']:
    if 'worldPos' not in o: continue
    before = BASE_HITS.get(id(o), 0)
    wp = list(o['worldPos'])
    for it in range(40):
        hh = hits_of(o, FR, wp)
        if len(hh) <= before: break
        q = hh[-1]; cx, cz = (q[2] + q[3]) / 2, (q[4] + q[5]) / 2; vx, vz = wp[0] - cx, wp[2] - cz
        if (q[3] - q[2]) > (q[5] - q[4]): vx = 0
        else: vz = 0
        n = math.hypot(vx, vz) or 1.0; wp = [round(wp[0] + vx / n, 2), wp[1], round(wp[2] + vz / n, 2)]
        if it == 0: nudged.append(o.get('id'))
    if len(hits_of(o, FR, wp)) > before: stuck.append(o.get('id'))
    o['worldPos'] = wp
chart['taps'] = taps
chart.setdefault('meta', {})['integc_removed'] = removed_meta
chart['meta']['integc_repair'] = log
if 'route' in layout: layout['route'] = {'note': 'centerline nodes [t,x,z,headingIndex,y] recomputed after integ-c tap removals (tools/charts/integc_repair.py)', 'nodes': [[round(a[0], 3), round(a[1], 2), round(a[2], 2), a[3], round(elev(a[0]), 2)] for a in final]}
(D / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False)); (D / 'layout.json').write_text(json.dumps(layout, indent=1, ensure_ascii=False))
hits, cross = check_all(FR)
print(json.dumps({'slug': slug, 'taps': f'{len(T_orig)} -> {len(taps)}', 'crossings': f'{cross_design} -> {cross}', 'same_level_overlaps': hits, 'log': log, 'nudged': nudged, 'still_hitting_road': stuck}, indent=1, ensure_ascii=False))
