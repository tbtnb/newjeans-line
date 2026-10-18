"""Check worldPos scenery against the road (the engine does not push worldPos objects out). Compares the worker's
original geometry (levels-design/<slug>/pre-audit) with the integrated one (levels-src/<slug>).
Usage: integb_clearance.py <slug>"""
import json, sys, math
sys.path.insert(0, __import__('os').path.dirname(__file__))
from common import ROOT
from integb_route import centreline
from route import elev_at
from integb_song import duration
FLAT = {'water', 'plane', 'disc', 'text', 'cloud', 'moon', 'sun'}
def hits(chart, layout, dur):
    nodes = centreline(chart, dur); W = sorted(layout['road']['width'], key=lambda w: w['t'])
    w_at = lambda t: ([w['w'] for w in W if w['t'] <= t] or [2.2])[-1]
    out = []
    for o in layout['objects']:
        if 'worldPos' not in o or o.get('onroad') or o.get('kind') in FLAT: continue
        px, py, pz = o['worldPos']; sz = o.get('size') or [2, 2, 2]
        r = o.get('radius') or (1.5 if o.get('kind') == 'group' else max(sz[0], sz[2]) / 2)
        h = sz[1] if len(sz) > 1 else 2
        for (ta, xa, za, _), (tb, xb, zb, _) in zip(nodes, nodes[1:]):
            dx, dz = xb - xa, zb - za; L2 = dx * dx + dz * dz
            u = 0 if L2 == 0 else max(0, min(1, ((px - xa) * dx + (pz - za) * dz) / L2))
            d = math.hypot(xa + u * dx - px, za + u * dz - pz); t = ta + u * (tb - ta); y = elev_at(layout.get('elevation', []), t)
            if d < r + w_at(t) / 2 and py - 0.5 < y + 1 and y < py + h:
                out.append((o.get('id'), round(t, 2), round(d, 2))); break
    return out
if __name__ == '__main__':
    sid = sys.argv[1]; dur = duration(sid); d = ROOT / f'levels-design/{sid}'
    pre = d / 'pre-audit' if (d / 'pre-audit').exists() else d
    a = hits(json.load(open(pre / 'chart.json')), json.load(open(pre / 'layout.json')), dur)
    b = hits(json.load(open(ROOT / f'levels-src/{sid}/chart.json')), json.load(open(ROOT / f'levels-src/{sid}/layout.json')), dur)
    print(f'{sid}: worldPos objects touching the road: worker geometry {len(a)}, integrated {len(b)}')
    new = [x for x in b if x[0] not in {y[0] for y in a}]
    for x in new: print('   NEW', x)

def nudge(chart, layout, dur, allowed_ids, log):
    """move worldPos objects that newly touch the road to the nearest clear spot (rings of 1.5 u up to 15 u, 24 angles)"""
    bad = [x[0] for x in hits(chart, layout, dur) if x[0] not in allowed_ids]
    for oid in bad:
        for o in layout['objects']:
            if o.get('id') != oid or 'worldPos' not in o: continue
            px, py, pz = o['worldPos']; done = False
            for k in range(1, 11):
                r = 1.5 * k
                for a in range(24):
                    ang = a * math.pi / 12
                    o['worldPos'] = [round(px + r * math.cos(ang), 3), py, round(pz + r * math.sin(ang), 3)]
                    if not hits(chart, {**layout, 'objects': [o]}, dur): done = True; break
                if done: break
            if done: log.append(f"moved {oid} {r:.1f} u to a clear spot (route repair shifted the road onto it)")
            else: o['worldPos'] = [px, py, pz]; o['exit'] = {'t': 0.0, 'mode': 'fade', 'dur': 0.01}; log.append(f'hid {oid} (no clear spot within 15 u)')
    return [x for x in hits(chart, layout, dur) if x[0] not in allowed_ids]
