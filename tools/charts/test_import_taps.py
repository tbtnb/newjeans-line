#!/usr/bin/env python3
"""Synthetic test for import_taps.py (scripted simulation, not human taps).
Ground truth = the OMG chart reduced to the grid rule (1/8, 1/16 only in fast runs, min gap, drop rule).
A fake tapper export is made from it with: 52 ms real lateness but only 45 ms measured calibration, Gaussian jitter
(sd 18 ms), 3 % double taps, 1 % outliers (70-100 ms late), 2 % missed taps. The converter runs into /tmp and must
recover the grid. Writes deliverables/tapper/converter-test.json."""
import json, random, subprocess, sys, statistics as st
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; OUT = Path('/tmp/nj-import-test'); random.seed(7)
ch = json.loads((ROOT / 'levels-src/omg/chart.json').read_text()); lay = json.loads((ROOT / 'levels-src/omg/layout.json').read_text())
dur = json.loads((ROOT / 'analysis/omg.json').read_text())['duration']
bpm, B0 = 127.003, 0.011; P = 60 / bpm; E8, E16 = P / 2, P / 4
sn = lambda t, s: B0 + round((t - B0) / s) * s
T = sorted({round(sn(t['t'], E16), 4) for t in ch['taps']})
fast = [False] * len(T); i = 0
while i < len(T):
    j = i
    while j + 1 < len(T) and T[j + 1] - T[j] <= 0.75 * E8 + 1e-6: j += 1
    if j - i + 1 >= 3: fast[i:j + 1] = [True] * (j - i + 1)
    i = j + 1
truth = sorted({round(t if f else sn(t, E8), 4) for t, f in zip(T, fast)})
falls = [e['t'] for e in lay['elevation'] if e['type'] in ('fall', 'jump')]
tt = []
for t in truth:
    if t < 1 or t > dur - 1 or (tt and t - tt[-1] < 0.105) or any(0 < t - f < 0.35 for f in falls): continue
    tt.append(t)
truth = tt
LATE, CAL, JIT = 0.052, 45, 0.018
taps, kind = [], {'dup': 0, 'out': 0, 'miss': 0}
for t in truth:
    r = random.random()
    if r < 0.02: kind['miss'] += 1; continue
    j = random.gauss(0, JIT); j = max(-0.045, min(0.045, j))
    if r < 0.03: kind['out'] += 1; j = random.uniform(0.070, 0.100) * random.choice((-1, 1))
    taps.append({'t_raw': round(t + LATE + j, 4), 'type': 'tap'})
    if 0.03 <= r < 0.06: kind['dup'] += 1; taps.append({'t_raw': round(t + LATE + j + random.uniform(0.02, 0.045), 4), 'type': 'tap'})
for tp in taps: tp['t'] = round(tp['t_raw'] - CAL / 1000, 4)
exp = {'format': 'nj-tapper', 'version': 1, 'song': 'omg', 'title': 'OMG', 'audio_duration': dur, 'bpm': bpm, 'beat_period': P, 'beat0': B0,
       'bar_beat': 0, 'grid_source': 'chart', 'calibration_ms': CAL, 'exported': 'synthetic', 'tool': 'test_import_taps.py', 'taps': sorted(taps, key=lambda x: x['t_raw'])}
OUT.mkdir(exist_ok=True); (OUT / 'export.json').write_text(json.dumps(exp))
r = subprocess.run([sys.executable, str(ROOT / 'tools/charts/import_taps.py'), str(OUT / 'export.json'), '--song', 'omg', '--out', str(OUT / 'levels'),
                    '--fit-offset', '--report', str(OUT / 'report.json')], capture_output=True, text=True)
print(r.stdout[-6000:], r.stderr[-2000:])
got = [t['t'] for t in json.loads((OUT / 'levels/omg/chart.json').read_text())['taps']]
import bisect
def nearest(arr, t):
    k = bisect.bisect_left(arr, t); return min((abs(arr[c] - t) for c in (k - 1, k) if 0 <= c < len(arr)), default=9)
hit = sum(1 for t in truth if nearest(got, t) < 0.0025); present = len(truth) - kind['miss']
wrong = [round(t, 3) for t in got if nearest(truth, t) >= 0.0025]
nfast_truth = sum(1 for k in range(len(truth)) if (k + 1 < len(truth) and truth[k + 1] - truth[k] < E8 - 1e-3) or (k and truth[k] - truth[k - 1] < E8 - 1e-3))
res = {'label': 'scripted simulation (synthetic jittered export), not human taps', 'truth_taps': len(truth), 'export_taps': len(taps), 'injected': kind,
       'jitter_sd_ms': JIT * 1000, 'true_lateness_ms': LATE * 1000, 'calibration_ms_in_export': CAL,
       'output_taps': len(got), 'exact_grid_hits': hit, 'recovery_of_tapped_truth': round(hit / present, 4),
       'wrong_slot': len(wrong), 'wrong_slot_examples': wrong[:10], 'truth_16th_taps': nfast_truth, 'outliers_expected_wrong': kind['out'], 'validate_exit': r.returncode,
       'report': {k: (v if not isinstance(v, list) else len(v)) for k, v in json.loads((OUT / 'report.json').read_text()).items()}}
(ROOT / 'deliverables/tapper/converter-test.json').write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
ok = res['recovery_of_tapped_truth'] >= 0.97 and r.returncode == 0
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
