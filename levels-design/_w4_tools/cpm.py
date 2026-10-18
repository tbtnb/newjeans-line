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
# windows (schema v2.5): min(0.5 g, clamp(0.45 g, 0.045, 0.11))
win = []
for i, t in enumerate(taps):
    nb = [g for g in ((gaps[i - 1] if i else None), (gaps[i] if i < len(gaps) else None)) if g]
    lg = min(nb); win.append((t, min(0.5 * lg, max(0.045, min(0.11, 0.45 * lg))), lg))
worst = min(win, key=lambda w: w[1]); viol = [w for w in win if w[1] > w[2] / 2 + 1e-9]
# 4-tap peak: fastest 3-gap window
p4 = min((taps[i + 3] - taps[i], taps[i]) for i in range(len(taps) - 3)); cpm4 = 3 * 60 / p4[0]
au = json.load(open(f'{slug}.audit.json')); nb = len(au.get('bursts_16th', []))
FOLLOW = json.load(open('follow.json')).get(slug, {})
ol = len(orig['taps'])
L = []
L.append('\n## Rhythmic-logic audit (user override 11:55) and difficulty\n\n')
L.append(f"Rules applied by `_w4_tools/audit.py` to the curated chart ({ol} taps): one audible layer per section; repeated phrases get one shared pattern; 16th bursts only where the 16th figure is prominent in the **full mix** (not just a stem), starting and ending on beats; breathing room kept; no taps on faint onsets. The stem-only triplet/syncopation taps from the previous pass were dropped. Result: **{len(taps)} taps**.\n\n")
L.append(f"- removed as off-layer (no audible hit of the section's layer within ±35 ms): {len(au.get('off_layer_removed', []))} — {', '.join(f'{x[0]:.2f}' for x in au.get('off_layer_removed', [])[:20])}\n")
L.append(f"- removed as faint (full-mix onset < 0.7× median strength in both the tag band and broadband): {len(au.get('faint_removed', []))} — {', '.join(f'{x[0]:.2f}' for x in au.get('faint_removed', []))}\n")
L.append(f"- re-tagged to the section layer (they coincide with an audible hit of that layer): {len(au.get('retag', []))}\n")
L.append(f"- bars unified to a shared pattern (same phrase in another instance or 4 bars earlier, every added slot verified audible): {len(au.get('unified', []))}\n")
L.append(f"- 16th bursts: {nb} " + (('at ' + '; '.join(f'{b:.2f} s ({sec}, full-mix strength {sc}× median)' for b, sc, sec in au['bursts_16th'])) if nb else '(none: no prominent 16th figure in the full mix at a phrase end)') + '\n\n')
L.append('### What the taps follow, per section\n\n| section | layer the taps follow |\n|---|---|\n')
for sec in ch['sections']:
    L.append(f"| {sec['label']} | {FOLLOW.get(sec['label'], au['layers'].get(sec['label'], ''))} |\n")
L.append('\n')
L.append('### Difficulty (soft references, not quotas)\n\n| metric | this chart |\n|---|---|\n')
L.append(f'| avg CPM = taps / full audio length x 60 | **{avg:.0f}** ({len(taps)} taps / {dur:.1f} s) |\n')
L.append(f'| avg CPM over the playable span (first->last tap) | {active:.0f} |\n')
L.append(f'| wiki-style avg CPM (mean of instantaneous 60/gap) | **{inst:.0f}** (median {med:.0f}) |\n')
L.append(f'| peak CPM = 60 / min gap | **{peak:.0f}** (min gap {min(gaps)*1000:.0f} ms at {taps[gaps.index(min(gaps))]:.2f} s) |\n')
L.append(f'| sustained 4-tap peak (3 gaps) | {cpm4:.0f} CPM from {p4[1]:.2f} s |\n')
L.append(f'| tightest engine judgment window | ±{worst[1]*1000:.0f} ms at {worst[0]:.2f} s (local gap {worst[2]*1000:.0f} ms); half-gap rule violations: {len(viol)} |\n\n')
L.append('Originals (dlfm-wiki): The Racing avg 220 / peak 440 · The Chaos 136 / 408 · Chinese Garden 148 / 296 (window ±45.8 ms) · Amusement Park peak 512 · Storm peak 460 · Winter 140 / 280 · Piano 125 / 250 · Autumn avg 96.\n\n')
open(f'{OUT}/chart-report.cpm.md', 'w').write(''.join(L))
print(slug, len(taps), f'avg {avg:.0f} wiki {inst:.0f} peak {peak:.0f} 4tap {cpm4:.0f} win {worst[1]*1000:.0f}ms viol {len(viol)} bursts {nb} mingap {min(gaps):.3f}')
