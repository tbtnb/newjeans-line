import json, sys, statistics as st
slug = sys.argv[1]; OUT = f'/workspace/newjeans-line-designs/{slug}'
ch = json.load(open(f'{OUT}/chart.json')); an = json.load(open(f'{OUT}/analysis.json'))
orig = json.load(open(f'{slug}.chart.raw.orig.json'))
dur = an.get('duration') or an.get('dur') or json.load(open(f'{slug}.grid.json')).get('duration')
taps = [x['t'] for x in ch['taps']]; tags = [x.get('tag', '') for x in ch['taps']]
gaps = [b - a for a, b in zip(taps, taps[1:])]
avg = len(taps) / dur * 60; active = len(taps) / (taps[-1] - taps[0]) * 60
inst = st.mean(60 / g for g in gaps); med = st.median(60 / g for g in gaps)
peak = 60 / min(gaps)
# windows: engine = clamp(0.45*min(neighbouring gaps), 0.065, 0.11)
win = []
for i, t in enumerate(taps):
    nb = [g for g in ((gaps[i - 1] if i else None), (gaps[i] if i < len(gaps) else None)) if g]
    lg = min(nb); win.append((t, max(0.065, min(0.11, 0.45 * lg)), lg))
worst = min(win, key=lambda w: w[1]); viol = [w for w in win if w[1] > w[2] / 2 + 1e-9]
# 4-tap peak: fastest 3-gap window
p4 = min((taps[i + 3] - taps[i], taps[i]) for i in range(len(taps) - 3)); cpm4 = 3 * 60 / p4[0]
nt = sum(1 for x in tags if x == 'fill-triplet'); ns = sum(1 for x in tags if x == 'synco-16th')
ol = len(orig['taps']) if isinstance(orig, dict) else len(orig)
L = []
L.append('\n## Difficulty calibration vs. original Dancing Line (11:48 steering)\n\n')
L.append(f'Chart change in this pass: {ol} -> **{len(taps)} taps** (+{nt} taps from 8th-triplet fill bursts tagged `fill-triplet` replacing beat interiors, {ns} off-beat 16th syncopations tagged `synco-16th`).\n\n')
L.append('| metric | this chart |\n|---|---|\n')
L.append(f'| avg CPM = taps / full audio length x 60 | **{avg:.0f}** ({len(taps)} taps / {dur:.1f} s) |\n')
L.append(f'| avg CPM over the playable span (first->last tap) | {active:.0f} |\n')
L.append(f'| wiki-style avg CPM (mean of instantaneous 60/gap) | **{inst:.0f}** (median {med:.0f}) |\n')
L.append(f'| peak CPM = 60 / min gap | **{peak:.0f}** (min gap {min(gaps)*1000:.0f} ms at {taps[gaps.index(min(gaps))]:.2f} s) |\n')
L.append(f'| sustained 4-tap peak (3 gaps) | {cpm4:.0f} CPM from {p4[1]:.2f} s |\n')
L.append(f'| tightest engine judgment window | ±{worst[1]*1000:.0f} ms at {worst[0]:.2f} s (local gap {worst[2]*1000:.0f} ms); half-gap rule violations: {len(viol)} |\n\n')
L.append('Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.\n\n')
open(f'{OUT}/chart-report.cpm.md', 'w').write(''.join(L))
print(slug, len(taps), f'avg {avg:.0f} wiki {inst:.0f} peak {peak:.0f} 4tap {cpm4:.0f} win {worst[1]*1000:.0f}ms viol {len(viol)} trip {nt} syn {ns} mingap {min(gaps):.3f}')
