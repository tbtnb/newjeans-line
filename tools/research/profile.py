"""Per-section average 16-step onset profiles (full/kick/snare/hat/vocals/other/bass) vs tap template. Usage: profile.py <slug> [chart]"""
import sys, json, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
from barmap import ENV, B0, P, chart, LAG
secs = sorted(chart['sections'], key=lambda s: s['t']); T = np.array([x['t'] for x in chart['taps']])
dur = len(ENV['full']) * O.HOP / O.SR
def cellval(env, t, w=0.025):
    f = int(round((t + LAG) * O.SR / O.HOP)); ww = int(w * O.SR / O.HOP); return float(env[max(0, f - ww):f + ww + 1].max())
for k, s in enumerate(secs):
    e = secs[k + 1]['t'] if k + 1 < len(secs) else dur
    b0 = int(round((s['t'] - B0) / (4 * P))); b1 = int(round((e - B0) / (4 * P)))
    print(f"\n== {s['label']} bars {b0}-{b1-1} ({s['t']:.2f}-{e:.2f}s) taps {int(((T>=s['t'])&(T<e)).sum())}")
    for L in ['full', 'kick', 'snare', 'hat', 'vocals', 'other', 'bass']:
        prof = np.zeros(16)
        for bar in range(b0, b1):
            for st in range(16): prof[st] += cellval(ENV[L], B0 + (bar * 16 + st) * P / 4)
        prof /= max(1, b1 - b0)
        print(f"  {L:6s} " + ' '.join(f'{v*10:2.0f}' if v >= 0.05 else ' .' for v in prof))
    tp = np.zeros(16)
    for t in T[(T >= s['t']) & (T < e)]:
        q = int(round((t - B0) / (P / 4))); tp[q % 16] += 1
    print(f"  TAPS   " + ' '.join(f'{v/max(1,b1-b0)*10:2.0f}' if v else ' .' for v in tp) + "   (x10 = taps per bar at that step)")
