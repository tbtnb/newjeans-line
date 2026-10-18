import json, sys, numpy as np
slug = sys.argv[1]; OUT = f'/workspace/newjeans-line-designs/{slug}'
a = json.load(open(f'{OUT}/analysis.json')); g = a['grid']; L = []
bar = a['beat_period'] * 4
L.append(f"# {slug} — audio analysis notes (worker 4)\n\n")
L.append(f"- Audio: full mp3 as shipped, {a['duration']:.2f} s, not trimmed or edited.\n")
L.append(f"- Tempo **{a['tempo_bpm']:.2f} BPM** constant (beat {a['beat_period']*1000:.2f} ms, bar {bar:.4f} s); first downbeat (bar 0) at **{g['bar0']:.3f} s**.\n")
L.append(f"- Grid: {g.get('note','')}\n- Transient correction applied to the grid: {g.get('transient_correction_s',0)*1000:+.0f} ms.\n")
L.append("- Demucs (htdemucs) stems are **25.03 ms late** against the mix (delay measured for htdemucs by the project lead and confirmed on our drum stems); all stem onsets stored here are already shifted earlier by 25 ms + ~25 ms envelope lag (−50 ms total), so stem-based tap choices sit on the real attack.\n\n")
L.append("## Sections (labels inferred, not from official metadata)\n\n| # | label | kind | start s | bars | vocal | drums | bass | other | evidence |\n|---|---|---|---|---|---|---|---|---|---|\n")
lv = a['per_bar_levels_0to1']; cand = a['section_candidates']
for i, s in enumerate(a['sections']):
    b0, b1 = s['bars']; m = {k: float(np.mean(v[b0:b1])) if b1 > b0 and len(v) > b0 else 0 for k, v in lv.items()}
    near = [c for k in cand for c in cand[k] if abs(c - s['t']) < 1.2]
    ev = f"novelty/agglom boundary within {min(abs(c-s['t']) for c in near):.2f} s" if near else 'set from stem levels / phrase count'
    L.append(f"| {i} | {s['label']} | {s['kind']} | {s['t']:.3f} | {b0}–{b1} | {m.get('vocal',0):.2f} | {m.get('drums',0):.2f} | {m.get('bass',0):.2f} | {m.get('other',0):.2f} | {ev} |\n")
L.append("\n(Stem columns = mean per-bar level 0–1 over the section; they back the labels: e.g. drums≈0 + vocals → break/bridge, all high → chorus.)\n\n")
L.append(f"## Method\n\n{a['method']}\n\nThe machine-readable data is in `analysis.json` (beats, sections, candidates, per-bar stem levels, mix and stem onset candidates with strengths, 1 s RMS).\n")
open(f'{OUT}/analysis.md', 'w').write(''.join(L)); print('ok')
