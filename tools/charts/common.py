"""Helpers for hand-authored charts on a fitted bar grid (see tools/audio/grid.py)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

class Grid:
    def __init__(self, sid):
        g = json.load(open(ROOT / f'analysis/{sid}.grid.json'))
        self.p = g['period']; self.b0 = g['beat0']; self.bars = g['bars']
    def t(self, bar, step=0):
        """time of 16th `step` (0..15, may be fractional/negative) in `bar`"""
        return self.b0 + (bar * 16 + step) * self.p / 4
    def strength(self, bar, step):
        if bar >= len(self.bars) or step != int(step): return None
        r = self.bars[bar]; s = int(step) % 16
        return max(r['kick'][s], r['snare'][s], r['mid'][s], r['full'][s])

class Chart:
    def __init__(self, sid, grid):
        self.sid = sid; self.g = grid; self.taps = []; self.sections = []; self.weak = []; self.rots = []
    def section(self, bar, label, kind, step=0):
        self.sections.append({'t': round(self.g.t(bar, step), 3), 'label': label, 'kind': kind})
    def bar(self, bar, steps, tag='beat', dirs=None):
        for i, s in enumerate(steps):
            d = None if dirs is None else dirs[i]
            self.add(bar, s, tag, d)
    def add(self, bar, step, tag='beat', d=None):
        t = round(self.g.t(bar, step), 3)
        st = self.g.strength(bar, step)
        if st is not None and st < 0.3: self.weak.append((bar, step, st))
        e = {'t': t, 'tag': tag}
        if d: e['dir'] = d
        self.taps.append(e)
    def rotate(self, bar, way, step=0):
        """Rotate the zig-zag's flow axis by 90 deg ('cw' or 'ccw') at the first suitable tap at/after bar:step.
        Implemented by repeating the previous turn direction (R,R = cw; L,L = ccw)."""
        self.rots.append((self.g.t(bar, step) - 1e-4, way))
    def _apply_dirs(self):
        prev = 'L'; pending = sorted(self.rots)
        for tap in self.taps:
            want = None
            if pending and tap['t'] >= pending[0][0]:
                need = 'R' if pending[0][1] == 'cw' else 'L'
                if prev == need: want = need; pending.pop(0)
            if 'dir' in tap and want is None: d = tap['dir']
            else: d = want or ('R' if prev == 'L' else 'L')
            tap['dir'] = d; prev = d
    def save(self, startHeading='N', speed=None, notes=''):
        self.taps.sort(key=lambda x: x['t'])
        self._apply_dirs()
        for a, b in zip(self.taps, self.taps[1:]):
            assert b['t'] - a['t'] >= 0.149, (a, b)
        out = {'id': self.sid, 'startHeading': startHeading, 'speed': speed or [{'t': 0, 'v': 9.0}], 'taps': self.taps, 'sections': self.sections, 'notes': notes}
        p = ROOT / f'levels-src/{self.sid}/chart.json'; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=1))
        print(f'{self.sid}: {len(self.taps)} taps; weak-onset taps: {len(self.weak)}')
        for w in self.weak[:40]: print('   weak', w)
