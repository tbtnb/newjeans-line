#!/usr/bin/env python3
"""integ-a: ship a worker design (levels-design/<slug>/) into levels-src/<slug>/ keeping the designer's route.
1. follows: section layers from the worker chart-report (follows_from_reports.py) + integrate.py's kick/snare -> drums rule.
2. trim (user rule): taps chartlogic flags as FAINT or OFF-LAYER are removed (same thresholds as chartlogic.py /
   integrate.py: faint = layer < 0.35 & full < 0.35 & no other band >= 0.5; off-layer = layer < 0.35 while another band >= 0.6).
3. local route repair: dropping one turn necessarily rotates the rest of the route by 90 deg about the edit (turn parity), so the
   tail keeps its own shape (spirals, crossings) as a rigid piece. Around each edit up to 2 (then 3) turn directions within
   +-2..4 taps are flipped, choosing the fewest flips that keep the whole route legal (route.py overlap rule: no overlap closer
   than 3 u in height unless < 1.5 s apart). If no local fix is legal, the tap is kept and reported.
4. scenery: worldPos objects (and camera worldYaw) are carried with the route: nearest point on the designer's centreline ->
   same time and same local offset on the repaired centreline (rigid for the tail); absolute yaw rotated with it.
5. cutaway patch (W1 songs): tall worldPos groups lose `onroad` so the occluder cutaway may fade them (integ-a-issues.md #1).
6. art: levels-design/<slug>/art (art-codex 8b6ef1c overlaid) copied as-is.
Usage: integ_a.py <slug> [...] [--no-trim]"""
import json, math, shutil, subprocess, sys, itertools
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from route import Router, HEAD, elev_at
ROOT = Path(__file__).resolve().parents[2]
import os; FLIPW = float(os.environ.get("FLIPW", 3))

def cutaway(layout):
    for o in layout.get('objects', []):
        if not o.get('onroad') or o.get('kind') != 'group' or not o.get('worldPos'): continue
        h = max([p.get('pos', [0, 0, 0])[1] + p.get('size', [0, 0, 0])[1] for p in o.get('parts', [])] or [0])
        if h > 5: o.pop('onroad'); o['integNote'] = 'onroad dropped by integ-a so the occluder cutaway can fade it'
CUTAWAY = {'attention', 'hype-boy', 'cookie', 'hurt'}

def run(slug, trim=True):
    src = ROOT / f'levels-design/{slug}'; dst = ROOT / f'levels-src/{slug}'; dst.mkdir(parents=True, exist_ok=True)
    chart = json.loads((src / 'chart.json').read_text()); layout = json.loads((src / 'layout.json').read_text())
    dur = json.loads((ROOT / f'analysis/{slug}.json').read_text())['duration']
    V = chart.get('speed', [{'t': 0, 'v': 9.0}])[0]['v']; assert len(chart.get('speed', [1])) <= 1, 'variable speed not supported'
    H0 = 'NESW'.index(chart.get('startHeading', 'N'))
    elev = layout.get('elevation', []); W = layout['road']['width']
    def width_at(t):
        w = W[0]['w']
        for e in W:
            if e['t'] <= t + 1e-9: w = e['w']
        return w
    # ---- 1. follows
    (dst / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
    subprocess.run([sys.executable, str(ROOT / 'tools/charts/follows_from_reports.py'), slug], check=True, stdout=subprocess.DEVNULL)
    chart = json.loads((dst / 'chart.json').read_text())
    E = np.load(ROOT / f'analysis/{slug}.env.npz'); HOP = float(E['hop_s'])
    ENV = {k: E[k] / 100 for k in ['kick', 'snare', 'hat', 'mid', 'full']}; ENV['drums'] = np.maximum(ENV['kick'], ENV['snare'])
    ENV['vocal'] = E['vocal'] / 100 if 'vocal' in E.files else ENV['mid']
    def st(t, L):
        f = int(round(t / HOP)); w = int(round(0.03 / HOP)); return float(ENV[L][max(0, f - w):f + w + 1].max())
    secs = sorted(chart['sections'], key=lambda s: s['t'])
    def sec(t): return [s for s in secs if s['t'] <= t + 1e-6][-1] if secs and secs[0]['t'] <= t + 1e-6 else (secs[0] if secs else {})
    def others(t, L):
        excl = {L} | ({'kick', 'snare'} if L == 'drums' else set())
        return max(st(t, k) for k in ['kick', 'snare', 'hat', 'mid'] if k not in excl)
    for k, s in enumerate(secs):
        if s.get('follows') in ('kick', 'snare'):
            e = secs[k + 1]['t'] if k + 1 < len(secs) else 1e9
            tt = [x['t'] for x in chart['taps'] if s['t'] <= x['t'] < e]
            a = sum(st(t, s['follows']) < 0.35 and others(t, s['follows']) >= 0.6 for t in tt)
            b = sum(st(t, 'drums') < 0.35 and others(t, 'drums') >= 0.6 for t in tt)
            if a and b <= a / 2: s['follows_note'] = f"declared {s['follows']} -> drums (taps on kick and snare of one groove). " + s.get('follows_note', ''); s['follows'] = 'drums'
    # ---- 2. flagged taps
    taps = sorted(chart['taps'], key=lambda x: x['t'])
    flagged = []
    for x in taps:
        L = sec(x['t']).get('follows', 'full'); sl = st(x['t'], L); sf = st(x['t'], 'full'); oth = others(x['t'], L)
        why = 'faint' if (sl < 0.35 and sf < 0.35 and oth < 0.5) else 'off-layer' if (sl < 0.35 and oth >= 0.6) else None
        if why: flagged.append({'t': x['t'], 'why': why, 'follows': L, 'layer': round(sl, 2), 'full': round(sf, 2), 'other': round(oth, 2), 'vocal': round(st(x['t'], 'vocal'), 2)})
    # ---- 3. local route repair
    R = Router([x['t'] for x in taps], dur, elev, width_at, speed=V, start_heading=H0, margin=0.3)
    def segs(tt, dd):
        raw, (x, z, h, t0) = R.segs_for(0.0, 0.0, H0, 0.0, tt, dd)
        dx, dz = HEAD[h]; raw.append((t0, dur, x, z, x + dx * (dur - t0) * V, z + dz * (dur - t0) * V)); return raw
    def lc(tt, dd):
        """(bad, crossings): bad = overlapping segment pairs >= 1.5 s apart with < 3 u height difference (route.py rule)"""
        a = R.arr(segs(tt, dd)); bad = cross = 0
        for k in range(1, len(a)):
            r = a[k]; o = a[:k]
            m = (r[0] - o[:, 1] >= R.min_dt) & (r[2] < o[:, 3]) & (o[:, 2] < r[3]) & (r[4] < o[:, 5]) & (o[:, 4] < r[5])
            if not m.any(): continue
            dy = np.min(np.abs(r[6:11][None, :, None] - o[m][:, None, 6:11]).reshape(int(m.sum()), -1), axis=1)
            bad += int((dy < R.min_dy).sum()); cross += int((dy >= R.min_dy).sum())
        return bad, cross
    def span(tt, dd):
        s = segs(tt, dd); xs = [p for q in s for p in (q[2], q[4])]; zs = [p for q in s for p in (q[3], q[5])]
        return max(max(xs) - min(xs), max(zs) - min(zs))
    T = [x['t'] for x in taps]; D = [x.get('dir', 'L') for x in taps]
    BAD0, CR0 = lc(T, D)   # the designer route's own count (validate.py passes it; route.py margins are stricter)
    removed, kept_flagged, flips = [], [], []
    for f in (flagged if trim else []):
        i = T.index(f['t']); T2 = T[:i] + T[i + 1:]; D2 = D[:i] + D[i + 1:]
        best = None
        for win, kmax in ((4, 3), (6, 3)):
            cand = [j for j in range(max(0, i - win), min(len(T2), i + win + 1))]
            for k in range(kmax + 1):
                for sub in itertools.combinations(cand, k):
                    Dc = list(D2)
                    for j in sub: Dc[j] = 'L' if Dc[j] == 'R' else 'R'
                    bad, cr = lc(T2, Dc)
                    if bad <= BAD0:
                        sc = (abs(cr - CR0) + FLIPW * k, span(T2, Dc))    # stay close to the designer's crossing count with few flips
                        if best is None or sc < best[0]: best = (sc, Dc, sub)
            if best: break
        if best is None: kept_flagged.append(f); continue
        T, D = T2, best[1]; removed.append(f); flips += [round(T2[j], 3) for j in best[2]]
    newtaps = []
    byt = {x['t']: x for x in taps}
    for t, d in zip(T, D): y = dict(byt[t]); y['dir'] = d; newtaps.append(y)
    chart['taps'] = newtaps; chart['sections'] = secs
    chart.setdefault('meta', {})['source'] = f'levels-design/{slug} (worker design, integrated by integ-a)'
    chart['meta']['integration'] = {'tool': 'tools/charts/integ_a.py', 'source_taps': len(taps), 'trimmed': removed, 'kept_flagged': kept_flagged,
                                    'flipped_dirs_at': flips, 'route': 'designer route kept; local repair around each trimmed tap'}
    (dst / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
    # ---- 4. carry worldPos scenery with the route
    old = segs([x['t'] for x in taps], [x.get('dir', 'L') for x in taps]); new = segs(T, D)
    def hd(s): return (int(np.sign(s[4] - s[2])), int(np.sign(s[5] - s[3])))
    def at(sg, t):
        for s in sg:
            if s[0] <= t <= s[1] + 1e-9:
                L = (t - s[0]) / max(1e-9, s[1] - s[0]); return s[2] + (s[4] - s[2]) * L, s[3] + (s[5] - s[3]) * L, s
        return sg[-1][4], sg[-1][5], sg[-1]
    def hidx(s, fallback):
        v = hd(s); return HEAD.index(v) if v in HEAD else fallback
    def rot_k(t):
        _, _, so = at(old, t); _, _, sn = at(new, t); return (hidx(sn, 0) - hidx(so, 0)) % 4
    def segarr(sg):
        A = np.array([(s[0], s[1], s[2], s[3], s[4], s[5]) for s in sg if s[1] - s[0] > 1e-6], dtype=float)
        ym = np.array([elev_at(elev, (r[0] + r[1]) / 2) for r in A]); return A, ym
    OA, OY = segarr(old); NA, NY = segarr(new)
    def clearance(A, Y, px, pz, py):
        """distance from (px,pz) to the nearest road segment within 6 u of height py"""
        x0, z0, x1, z1 = A[:, 2], A[:, 3], A[:, 4], A[:, 5]
        vx, vz = x1 - x0, z1 - z0; L2 = np.maximum(vx * vx + vz * vz, 1e-9)
        u = np.clip(((px - x0) * vx + (pz - z0) * vz) / L2, 0, 1)
        d = np.hypot(px - x0 - u * vx, pz - z0 - u * vz); d[np.abs(Y - py) > 6] = 1e9; return float(d.min())
    moved = 0
    for o in layout.get('objects', []):
        wp = o.get('worldPos')
        if not wp: continue
        ox, oy, oz = wp[0], (wp[1] if len(wp) > 2 else 0), (wp[2] if len(wp) > 2 else wp[1])
        c_old = clearance(OA, OY, ox, oz, oy)
        cands = []
        for s in old:
            if s[1] - s[0] < 1e-6: continue
            dx, dz = hd(s); L = (s[1] - s[0]) * V; u = max(0.0, min(L, (ox - s[2]) * dx + (oz - s[3]) * dz))
            px, pz = s[2] + dx * u, s[3] + dz * u; ty = s[0] + u / V
            dist = math.hypot(ox - px, oz - pz) + 2.0 * abs(oy - elev_at(elev, ty))
            cands.append((dist, ty, px, pz))
        cands.sort(); base = cands[0][0]
        best = None
        for dist, ty, px, pz in [c for c in cands if c[0] <= base + 25][:40]:
            k = rot_k(ty); nx, nz, _ = at(new, ty); rx, rz = ox - px, oz - pz
            for _ in range(k): rx, rz = rz, -rx            # rotate the offset clockwise (N->E) k times
            qx, qz = nx + rx, nz + rz
            c_new = clearance(NA, NY, qx, qz, oy)
            # keep the object's clearance from the road (never closer than in the design) and prefer its nearest anchor
            sc = abs(c_new - c_old) + (5.0 if c_new < min(c_old, 2.5) - 0.3 else 0) + 0.05 * (dist - base)
            if best is None or sc < best[0]: best = (sc, qx, qz, k)
        _, qx, qz, k = best
        if abs(qx - ox) < 1e-6 and abs(qz - oz) < 1e-6 and k == 0: continue
        o['worldPos'] = [round(qx, 2), oy, round(qz, 2)] if len(wp) > 2 else [round(qx, 2), round(qz, 2)]
        if k:
            r = o.get('rot', 0)
            if isinstance(r, list): r = [r[0], (r[1] + 90 * k) % 360, r[2]]
            else: r = (r + 90 * k) % 360
            o['rot'] = r
        moved += 1
    for c in layout.get('camera', []):
        if 'worldYaw' in c: c['worldYaw'] = (c['worldYaw'] + 90 * rot_k(c['t'])) % 360
    layout.pop('path', None)
    if slug in CUTAWAY: cutaway(layout)
    (dst / 'layout.json').write_text(json.dumps(layout, indent=1, ensure_ascii=False))
    if (dst / 'art').exists(): shutil.rmtree(dst / 'art')
    if (src / 'art').exists(): shutil.copytree(src / 'art', dst / 'art')
    print(f'{slug}: {len(taps)} -> {len(T)} taps; trimmed {len(removed)} ({sum(f["why"]=="faint" for f in removed)} faint, {sum(f["why"]=="off-layer" for f in removed)} off-layer); '
          f'kept flagged {len(kept_flagged)}; dir flips {len(flips)}; worldPos moved {moved}')
    return removed, kept_flagged

if __name__ == '__main__':
    for slug in [a for a in sys.argv[1:] if not a.startswith('--')]: run(slug, trim='--no-trim' not in sys.argv)
