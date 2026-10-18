#!/usr/bin/env python3
"""Author route-anchored Codex art props into a layout (schema v2.7, see docs/ART_PROPS.md).

usage: artkit.py <slug> <spec.json> [--dry]

spec.json = { "objects": [ {<SceneObject fields>, "window": [t0, t1], "count": n}, ... ],
              "dressing": {...}  (merged into layout.dressing),  "art": {...} (merged into layout.art) }
For every object spec the tool picks `count` times inside `window` on the longest straight runs
(so the prop sits beside a stretch the camera follows), chooses the side of the road with more free
space (away from other road segments), and writes {t, side, near, face, ...} objects with ids
"art-<n>" into levels-src/<slug>/layout.json (previous art-* objects are replaced; nothing else changes).
The engine resolves the final position at load (hug/near + RoadGrid push-out), so props never sit on the road.
"""
import json, math, sys
from pathlib import Path

HV = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # heading index -> (x, z); N=+z, E=+x

def spans(nodes):
    out = []
    for a, b in zip(nodes, nodes[1:]):
        out.append(dict(t0=a[0], t1=b[0], x0=a[1], z0=a[2], x1=b[1], z1=b[2], h=a[3] % 4, y=a[4] if len(a) > 4 else 0))
    return out

def pos(sp, t):
    k = 0 if sp['t1'] == sp['t0'] else (t - sp['t0']) / (sp['t1'] - sp['t0'])
    return sp['x0'] + (sp['x1'] - sp['x0']) * k, sp['z0'] + (sp['z1'] - sp['z0']) * k

def seg_dist(px, pz, s):
    ax, az, bx, bz = s['x0'], s['z0'], s['x1'], s['z1']
    dx, dz = bx - ax, bz - az; L2 = dx * dx + dz * dz
    k = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (pz - az) * dz) / L2))
    return math.hypot(ax + dx * k - px, az + dz * k - pz)

def clearance(S, t, x, z, y):
    d = 99.0
    for s in S:
        if s['t1'] > t - 1.2 and s['t0'] < t + 1.2: continue
        if abs(s['y'] - y) > 6: continue
        d = min(d, seg_dist(x, z, s))
    return d

def main():
    slug, spec_p = sys.argv[1], sys.argv[2]; dry = '--dry' in sys.argv
    lp = Path('levels-src') / slug / 'layout.json'
    L = json.loads(lp.read_text()); spec = json.loads(Path(spec_p).read_text())
    S = spans(L['route']['nodes']); used = []
    gy = (L.get('palette') or {}).get('groundY', -0.6)
    if gy is None: gy = -0.6
    objs = [o for o in L['objects'] if not str(o.get('id', '')).startswith('art-')]
    n = 0; report = []
    for o in spec.get('objects', []):
        o = dict(o); w = o.pop('window'); cnt = o.pop('count', 1); want_side = o.pop('prefer', 0)
        reach = o.pop('reach', 4.0)  # how far from the road edge the prop needs room
        cands = []
        for sp in S:
            a, b = max(sp['t0'], w[0]), min(sp['t1'], w[1])
            if b - a < 0.25: continue
            dur = sp['t1'] - sp['t0']
            for k in range(1, 6):
                t = a + (b - a) * k / 6
                x, z = pos(sp, t); hx, hz = HV[sp['h']]; rx, rz = hz, -hx
                for side in (1, -1):
                    if want_side and side != want_side: continue
                    c = clearance(S, t, x + rx * side * reach, z + rz * side * reach, sp['y'])
                    score = min(c, 8) + min(dur, 3) * 1.5 - (0 if sp['y'] < 1 else 6)
                    cands.append((score, t, side, sp))
        cands.sort(key=lambda c: -c[0]); picked = []
        for sc, t, side, sp in cands:
            if len(picked) >= cnt: break
            if any(abs(t - u) < max(2.0, (w[1] - w[0]) / (cnt * 2.5)) for u in used + [p[1] for p in picked]): continue
            picked.append((sc, t, side, sp))
        for sc, t, side, sp in sorted(picked, key=lambda p: p[1]):
            n += 1; ob = {'id': f'art-{n}', **o, 't': round(t, 3), 'side': side}
            ob.setdefault('near', 0.8); used.append(t)
            # base 0.6 below the road top, the level the roadside dressing stands on
            if 'y' not in ob and 'worldPos' not in ob: ob['y'] = -0.6
            objs.append(ob); report.append(f"art-{n:<3} {o.get('kind'):8s} t={t:7.2f} side={side:+d} clear={sc:5.1f} {o.get('src','')}")
    L['objects'] = objs
    if 'dressing' in spec: L['dressing'] = {**(L.get('dressing') or {}), **spec['dressing']}
    if 'art' in spec: L['art'] = {**(L.get('art') or {}), **spec['art']}
    if 'sections' in spec:
        for patch in spec['sections']:
            for s in L.get('sections', []):
                if abs(s['t'] - patch['t']) < 1e-6: s.update({k: v for k, v in patch.items() if k != 't'})
    print('\n'.join(report)); print(f'{n} art objects')
    if not dry: lp.write_text(json.dumps(L, indent=1, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
