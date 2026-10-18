"""List rhythm problems of a chart by bar: offbeat-only bars, untapped strong beat accents, weak taps,
16th syncopations without a strong onset, repeated-section pattern drift. Usage: problems.py <slug> <chart.json>"""
import sys, json, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
from barmap import ENV, B0, P, chart, LAG
T = np.array([x['t'] for x in chart['taps']]); secs = sorted(chart['sections'], key=lambda s: s['t'])
def val(L, t, w=0.03):
    f = int(round((t + LAG) * O.SR / O.HOP)); ww = int(w * O.SR / O.HOP)
    if f + ww >= len(ENV[L]): return 0.0
    return float(ENV[L][max(0, f - ww):f + ww + 1].max())
def acc(t): return max(val('full', t), 0.8 * max(val('kick', t), val('snare', t)), 0.8 * val('vocals', t) if val('rel_vocals', t, 0.01) > -14 else 0)
def sec(t): return [s for s in secs if s['t'] <= t + 0.05][-1]['label']
nb = int((T[-1] - B0) / (4 * P)) + 2; rows = []
pat = {}
for bar in range(nb):
    t0 = B0 + bar * 4 * P; tt = T[(T >= t0 - 0.06) & (T < t0 + 4 * P - 0.06)]
    steps = sorted({int(round((t - B0) / (P / 4))) % 16 for t in tt}); pat[bar] = tuple(steps)
    probs = []
    beats = [(b, acc(t0 + b * P)) for b in range(4)]
    strong_unt = [f'beat {b+1} ({a:.1f})' for b, a in beats if a >= 0.8 and not (len(tt) and np.min(np.abs(tt - (t0 + b * P))) < 0.06)]
    if len(tt) >= 2 and not any(s % 4 == 0 for s in steps) and max(a for _, a in beats) >= 0.6: probs.append(f'offbeat-only bar (taps on steps {steps}) while the beat has accents')
    if len(strong_unt) >= 2: probs.append('strong beat accents not tapped: ' + ', '.join(strong_unt))
    for t in tt:
        s = int(round((t - B0) / (P / 4))) % 16
        if s % 2 and acc(t) < 0.7: probs.append(f'16th syncopation at {t:.2f}s (step {s}) on a weak onset ({acc(t):.2f})')
        if acc(t) < 0.4: probs.append(f'weak tap {t:.2f}s ({acc(t):.2f})')
    if probs: rows.append((bar, t0, sec(t0), steps, probs))
for bar, t0, s, steps, probs in rows:
    print(f'| {t0:6.2f} | {bar} | {s} | {" ".join(map(str, steps))} | {"; ".join(probs)} |')
# repeated-section drift (choruses)
grp = {}
for s in secs:
    if 'chorus' in s['kind']:
        b0 = int(round((s['t'] - B0) / (4 * P))); grp[s['label']] = [pat.get(b) for b in range(b0, b0 + 8)]
names = list(grp); print('\nchorus 8-bar patterns:')
for n in names: print(' ', n, [' '.join(map(str, p)) for p in grp[n]])
