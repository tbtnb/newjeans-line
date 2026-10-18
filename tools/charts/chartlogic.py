#!/usr/bin/env python3
"""Chart-logic check (user rule 2026-10-18: rhythmic logic beats density).
Per section: which audible layer the taps follow, whether taps hop between layers, ghost/faint onsets,
bursts that are not prominent in the full mix, and whether repeated phrases reuse the same pattern.
Needs analysis/<slug>.grid.json (tools/audio/grid.py). Strengths are per-band onset strengths normalised to the
band's 99.5th percentile (~0.3 faint, >=0.6 clear).
Usage: chartlogic.py <slug> [--chart path/to/chart.json] [--md out.md]"""
import json, sys, statistics as st
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
sid = args[0]
chart = json.load(open(opt('--chart', ROOT / f'levels-src/{sid}/chart.json')))
g = json.load(open(ROOT / f'analysis/{sid}.grid.json'))
P, B0, BARS = g['period'], g['beat0'], g['bars']
# Align the 16th grid to the chart author's grid when the chart declares one (avoids false off-grid flags)
_m = chart.get('meta', {})
def _offgrid(P_, B0_):
    n = 0
    for x in chart['taps']:
        q = (x['t'] - B0_) / (P_ / 4); n += abs(q - round(q)) * P_ / 4 > 0.025
    return n
GRID_SRC = 'analysis grid'
if _m.get('beat_period') or _m.get('bpm'):
    P2 = _m.get('beat_period') or 60 / _m['bpm']; B02 = _m.get('beat0', B0)
    if _offgrid(P2, B02) < _offgrid(P, B0): P, B0, GRID_SRC = P2, B02, 'chart meta grid'
if _offgrid(P, B0) > 0.1 * len(chart['taps']):
    # neither grid fits the chart: refit the phase (and a small tempo correction) to the chart's own taps
    best = (_offgrid(P, B0), P, B0)
    for dp in (0, -0.0005, 0.0005, -0.001, 0.001):
        for k in range(40):
            b = B0 + k * (P / 4) / 40; n = _offgrid(P * (1 + dp), b)
            if n < best[0]: best = (n, P * (1 + dp), b)
    _, P, B0 = best; GRID_SRC = 'grid refit to the chart taps'
# Strengths are sampled at the tap's actual time from the per-band onset envelopes (analysis/<slug>.env.npz),
# so they do not depend on the grid at all.
import numpy as _np
_E = _np.load(ROOT / f'analysis/{sid}.env.npz'); _HOP = float(_E['hop_s'])
ENV = {k: _E[k].astype(float) / 100 for k in ['kick', 'snare', 'hat', 'mid', 'full']}
ENV['drums'] = _np.maximum(ENV['kick'], ENV['snare'])
if 'vocal' in _E.files: ENV['vocal'] = _E['vocal'].astype(float) / 100
else: ENV['vocal'] = ENV['mid']   # no stem: fall back to the mid band
NBARS = int((len(ENV['full']) * _HOP - B0) / (4 * P)) + 1
LAYERS = ['kick', 'snare', 'hat', 'mid', 'full']
TAGMAP = {'kick': 'kick', 'snare': 'snare', 'clap': 'snare', 'hat': 'hat', 'vocal': 'mid', 'melody': 'mid', 'bass': 'kick', 'burst': 'full', 'run': 'full', 'fill': 'full', 'accent': 'full', 'fx': 'full'}
FAINT, CLEAR = 0.35, 0.6

TAPT = {}
def cell(t):
    q = (t - B0) / (P / 4); k = round(q); off = (q - k) * P / 4
    bar, step = divmod(k, 16)
    if bar < 0 or bar >= NBARS: return None
    TAPT[(bar, step)] = t
    return bar, step, off

def strength(bar, step, layer):
    # onset strength within +-30 ms of the tap time (the tap's own time if known, else the grid cell)
    t = TAPT.get((bar, step), B0 + (bar * 16 + step) * P / 4)
    e = ENV[layer]; f = int(round(t / _HOP)); w = int(round(0.03 / _HOP))
    return float(e[max(0, f - w):f + w + 1].max()) if f < len(e) else 0.0

taps = chart['taps']; T = [x['t'] for x in taps]
secs = sorted(chart.get('sections', []), key=lambda s: s['t']) or [{'t': 0, 'label': 'all', 'kind': ''}]
end = T[-1] + 5 if T else 0
out = [f'## Chart logic: {sid} ({len(T)} taps; 16th grid from {GRID_SRC}: {60/P:.3f} BPM, beat0 {B0:.3f} s)', '', '| section | follows | taps | /s | layer strength (median) | off-layer taps | faint taps | weak bursts | off-grid >25ms | phrase patterns (unique/total) |', '|---|---|---|---|---|---|---|---|---|---|']
flags_total = {'hop': 0, 'faint': 0, 'burst': 0, 'offgrid': 0}
details = []
for k, s in enumerate(secs):
    e = secs[k + 1]['t'] if k + 1 < len(secs) else 1e9
    idx = [i for i, t in enumerate(T) if s['t'] <= t < e]
    if not idx:
        out.append(f"| {s.get('label','')} | (no taps) | 0 | 0 | | | | | | |"); continue
    cells = [cell(T[i]) for i in idx]
    follows = s.get('follows')
    if not follows:
        # infer: the layer with the best median strength over the section's taps (the 'full' mix is the fallback)
        med = {L: st.median(strength(c[0], c[1], L) for c in cells if c) for L in LAYERS}
        follows = max(LAYERS[:-1], key=lambda L: med[L]) if max(med[L] for L in LAYERS[:-1]) >= 0.5 else 'full'
    hop = faint = weakb = offg = 0
    for j, i in enumerate(idx):
        c = cells[j]
        if not c: continue
        bar, step, off = c
        sl = strength(bar, step, follows); sf = strength(bar, step, 'full')
        others = {L: strength(bar, step, L) for L in LAYERS[:-1] if L != follows and not (follows == 'drums' and L in ('kick', 'snare'))}
        best_o = max(others, key=others.get)
        gap = min([T[i] - T[i - 1]] if i else [9] + [T[i + 1] - T[i]] if i + 1 < len(T) else [9])
        gap = min(T[i] - T[i - 1] if i else 9, T[i + 1] - T[i] if i + 1 < len(T) else 9)
        if abs(off) > 0.025: offg += 1; details.append(f'   off-grid {T[i]:.3f}s ({off*1000:+.0f} ms from 16th grid)')
        if sl < FAINT and sf < FAINT and max(others.values()) < 0.5:
            faint += 1; details.append(f'   FAINT {T[i]:.3f}s bar {bar} step {step}: {follows} {sl:.2f}, full {sf:.2f}')
        elif sl < FAINT and others[best_o] >= CLEAR:
            hop += 1; details.append(f'   HOP {T[i]:.3f}s bar {bar} step {step}: {follows} {sl:.2f} but {best_o} {others[best_o]:.2f} (section follows {follows})')
        if gap < 0.15 and sf < CLEAR and strength(bar, step, follows) < CLEAR:
            weakb += 1; details.append(f'   WEAK-BURST {T[i]:.3f}s bar {bar} step {step}: full {sf:.2f}, {follows} {sl:.2f}')
    # phrase patterns: 2-bar step signatures
    sig = {}
    for c in cells:
        if c: sig.setdefault(c[0] // 2, []).append((c[0] % 2) * 16 + c[1])
    pats = [tuple(v) for v in sig.values()]
    medl = st.median(strength(c[0], c[1], follows) for c in cells if c)
    dur = (min(e, end) - s['t'])
    flags_total['hop'] += hop; flags_total['faint'] += faint; flags_total['burst'] += weakb; flags_total['offgrid'] += offg
    out.append(f"| {s.get('label','')} | {follows}{'' if s.get('follows') else ' (inferred)'} | {len(idx)} | {len(idx)/max(dur,1e-6):.2f} | {medl:.2f} | {hop}{' ⚠' if hop > max(1, 0.1 * len(idx)) else ''} | {faint}{' ⚠' if faint else ''} | {weakb}{' ⚠' if weakb else ''} | {offg} | {len(set(pats))}/{len(pats)} |")
out.append('')
out.append(f"Totals: off-layer (hop) {flags_total['hop']}, faint {flags_total['faint']}, weak bursts {flags_total['burst']}, off-grid {flags_total['offgrid']}")
out += ['', '<details><summary>flagged taps</summary>', '', '```'] + details[:200] + ['```', '</details>']
txt = '\n'.join(out); print(txt)
if opt('--md'): Path(opt('--md')).write_text(txt)
