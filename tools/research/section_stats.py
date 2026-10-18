"""Section-level rhythm stats for a chart (beat-position mix, coverage of strong beat accents, offbeat-only runs).
Usage: section_stats.py <slug> [chart.json] [--json out]"""
import sys, json, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
from barmap import ENV, B0, P, chart, LAG
secs = sorted(chart['sections'], key=lambda s: s['t']); T = np.array([x['t'] for x in chart['taps']])
dur = len(ENV['full']) * O.HOP / O.SR
def val(L, t, w=0.03):
    f = int(round((t + LAG) * O.SR / O.HOP)); ww = int(w * O.SR / O.HOP); return float(ENV[L][max(0, f - ww):f + ww + 1].max())
def accent(t):  # salience of a grid cell: drums backbone + full mix
    return max(val('full', t), 0.8 * max(val('kick', t), val('snare', t)), 0.8 * val('vocals', t) if val('rel_vocals', t, 0.01) > -14 else 0)
rows = []; out = {}
print(f"| section | taps | /s | on beat (q) | 8th off | 16th | strong beat accents tapped | strongest unt. beats (t) | taps w/o onset |")
print('|---|---|---|---|---|---|---|---|---|')
for k, s in enumerate(secs):
    e = secs[k + 1]['t'] if k + 1 < len(secs) else dur
    tt = T[(T >= s['t']) & (T < e)]
    steps = [int(round((t - B0) / (P / 4))) % 16 for t in tt]
    q = sum(1 for x in steps if x % 4 == 0); h = sum(1 for x in steps if x % 4 == 2); s16 = len(steps) - q - h
    # strong accents on quarter beats
    b0 = int(np.ceil((s['t'] - B0) / P - 1e-6)); b1 = int(np.floor((e - B0) / P - 1e-6))
    strong = []; tapped = 0
    for b in range(b0, b1 + 1):
        t = B0 + b * P
        a = accent(t)
        if a >= 0.75:
            hit = len(tt) and np.min(np.abs(tt - t)) < 0.06
            strong.append((t, a, hit)); tapped += bool(hit)
    unt = sorted([x for x in strong if not x[2]], key=lambda x: -x[1])[:4]
    weak = sum(1 for t in tt if max(val(L, t) for L in ['full', 'kick', 'snare', 'hat', 'vocals', 'other', 'bass']) < 0.4)
    n = max(1, len(tt))
    out[s['label']] = dict(taps=len(tt), on_beat=q, off8=h, s16=s16, strong=len(strong), strong_tapped=tapped, weak=weak)
    print(f"| {s['label']} | {len(tt)} | {len(tt)/(e-s['t']):.2f} | {q} ({100*q/n:.0f}%) | {h} ({100*h/n:.0f}%) | {s16} ({100*s16/n:.0f}%) | {tapped}/{len(strong)} | {', '.join(f'{x[0]:.2f}' for x in unt)} | {weak} |")
tot = {k: sum(v[k] for v in out.values()) for k in ['taps', 'on_beat', 'off8', 's16', 'strong', 'strong_tapped', 'weak']}
print(f"\nTotal: {tot['taps']} taps; on quarter beats {tot['on_beat']} ({100*tot['on_beat']/tot['taps']:.0f}%), 8th offbeats {tot['off8']} ({100*tot['off8']/tot['taps']:.0f}%), 16ths {tot['s16']} ({100*tot['s16']/tot['taps']:.0f}%); strong quarter-beat accents tapped {tot['strong_tapped']}/{tot['strong']}; taps with no onset >=0.4 in any layer: {tot['weak']}")
if '--json' in sys.argv: json.dump({'sections': out, 'total': tot}, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
