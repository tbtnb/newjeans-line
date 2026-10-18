"""% of chart taps landing on a sung syllable (analysis/omg.lyrics.json), +-W ms. Usage: vocal_cov.py chart.json [W_ms=50]"""
import json, sys, numpy as np
c = json.load(open(sys.argv[1])); W = float(sys.argv[2]) / 1000 if len(sys.argv) > 2 else 0.05
d = json.load(open('analysis/omg.lyrics.json')); S = np.array(sorted(s['t'] for s in d['syllables']))
T = np.array([x['t'] for x in c['taps']]); near = np.array([np.min(np.abs(S - t)) <= W for t in T])
lines = d['lines']; starts = np.array([l['start'] for l in lines])
ls = sum(np.min(np.abs(T - t)) <= W for t in starts)
inside = np.array([any(l['t0'] - 0.1 <= t <= l['t1'] for l in lines) for t in T])
print(f'{sys.argv[1]}: {len(T)} taps; on a syllable (+-{W*1000:.0f} ms): {near.sum()} ({near.mean():.0%}); taps during sung lines: {inside.sum()}, of those on a syllable {near[inside].sum()} ({near[inside].mean():.0%}); line starts tapped {ls}/{len(starts)}; syllables tapped {sum(np.min(np.abs(T - s)) <= W for s in S)}/{len(S)}')
