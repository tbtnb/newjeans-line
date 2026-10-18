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
LAYERS = ['kick', 'snare', 'hat', 'mid', 'full']
TAGMAP = {'kick': 'kick', 'snare': 'snare', 'clap': 'snare', 'hat': 'hat', 'vocal': 'mid', 'melody': 'mid', 'bass': 'kick', 'burst': 'full', 'run': 'full', 'fill': 'full', 'accent': 'full', 'fx': 'full'}
FAINT, CLEAR = 0.35, 0.6

def cell(t):
    q = (t - B0) / (P / 4); k = round(q); off = (q - k) * P / 4
    bar, step = divmod(k, 16)
    if bar < 0 or bar >= len(BARS): return None
    return bar, step, off

def strength(bar, step, layer):
    s = BARS[bar][layer][step]
    # allow +-1 16th of smear for onset detection, but only half weight
    nb = [BARS[b][layer][s2] for b, s2 in ((bar, step - 1), (bar, step + 1)) if 0 <= s2 < 16]
    return max(s, *(0.6 * x for x in nb)) if nb else s

taps = chart['taps']; T = [x['t'] for x in taps]
secs = sorted(chart.get('sections', []), key=lambda s: s['t']) or [{'t': 0, 'label': 'all', 'kind': ''}]
end = T[-1] + 5 if T else 0
out = [f'## Chart logic: {sid} ({len(T)} taps)', '', '| section | follows | taps | /s | layer strength (median) | off-layer taps | faint taps | weak bursts | off-grid >25ms | phrase patterns (unique/total) |', '|---|---|---|---|---|---|---|---|---|---|']
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
        others = {L: strength(bar, step, L) for L in LAYERS[:-1] if L != follows}
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
