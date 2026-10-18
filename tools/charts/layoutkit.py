"""Helpers for authoring layout.json against an existing chart."""
import json, random
from common import ROOT, Grid

class Layout:
    def __init__(self, sid):
        self.sid = sid
        self.chart = json.load(open(ROOT / f'levels-src/{sid}/chart.json'))
        self.taps = [t['t'] for t in self.chart['taps']]
        self.g = Grid(sid)
        self.d = {'id': sid, 'palette': {}, 'road': {'width': [], 'height': 0.7, 'reveal': []}, 'elevation': [], 'sections': [],
                  'camera': [], 'objects': [], 'events': [], 'diamonds': [], 'crowns': [], 'finish': {'kind': 'pyramid'}}
        self.rng = random.Random(sid)
    def T(self, bar, step=0): return round(self.g.t(bar, step), 3)
    def gap_mid(self, t, min_gap=0.5):
        """midpoint of the first inter-tap gap (>= min_gap) at/after t"""
        for a, b in zip(self.taps, self.taps[1:]):
            if b > t and b - a >= min_gap and a >= t - 0.01: return round((a + b) / 2, 3)
        return round(t, 3)
    def gap_after(self, t, min_gap):
        for a, b in zip(self.taps, self.taps[1:]):
            if a >= t and b - a >= min_gap: return a, b
        return None
    def obj(self, **o): self.d['objects'].append(o); return o
    def cam(self, t, **c): self.d['camera'].append({'t': round(t, 3), **c})
    def ev(self, t, type, **e): self.d['events'].append({'t': round(t, 3), 'type': type, **e})
    def section(self, t, label, **kw): self.d['sections'].append({'t': round(t, 3), 'label': label, **kw})
    def width(self, t, w): self.d['road']['width'].append({'t': round(t, 3), 'w': w})
    def reveal(self, t, mode, lead=1.8): self.d['road']['reveal'].append({'t': round(t, 3), 'mode': mode, 'lead': lead})
    def scatter(self, t0, t1, n, kinds, side_rng=(5, 14), **common):
        for i in range(n):
            t = t0 + (t1 - t0) * (i + self.rng.random() * 0.8) / n
            side = self.rng.uniform(*side_rng) * self.rng.choice([-1, 1])
            k = self.rng.choice(kinds)
            o = dict(common); o.update(k if isinstance(k, dict) else {'kind': k})
            s = o.get('size')
            if s and o.get('jitter', True):
                f = self.rng.uniform(0.75, 1.3); o['size'] = [round(v * f, 2) for v in s]
            o.pop('jitter', None)
            self.obj(t=round(t, 3), side=round(side, 2), **o)
    def save(self):
        for k in ['camera', 'events', 'sections']: self.d[k].sort(key=lambda x: x['t'])
        assert len(self.d['diamonds']) == 10, len(self.d['diamonds'])
        assert len(self.d['crowns']) == 2
        p = ROOT / f'levels-src/{self.sid}/layout.json'
        p.write_text(json.dumps(self.d, indent=1, ensure_ascii=False))
        print(f'{self.sid}: layout {len(self.d["objects"])} objects, {len(self.d["events"])} events, {len(self.d["camera"])} camera cues')
