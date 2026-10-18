# integ-a: Attention
Source: levels-design/attention (designs-w1 00702bf) with art-codex 8b6ef1c art overlay where present. Taps, dirs, elevation and scenery shipped unchanged
by tools/charts/integ_a.py (patches, if any, listed below).

- validate.py v2.5 on levels-src/attention: 0 errors, 0 warnings.
  == attention  duration 178.05s  taps 285  dirs R/L 146/139  multi-level crossings 43
  peak density 300 CPM (taps in any 1 s window x60), average 96 CPM; gaps < 0.15 s: 5
- chartlogic (Totals: off-layer (hop) 4, faint 47, weak bursts 8, off-grid 4); full table: docs/verification/integ-a-attention-chartlogic.txt. Reported only; taps not changed.
- Patch: `cutaway` (4 tall onroad landmarks may fade when occluding; integ-a-issues.md #1). Snapshots: head and next road readable in all 7 frames.
- **Scripted simulation playthrough** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader, --quality low, 540x960;
  not physical-device play, not proof of A/V sync): state complete, judged 285/285, perfect 285, good 0,
  diamonds 10/10, save crowns 3, timing error mean 1.4 ms sd 1.3 ms max |8| ms,
  fails 0, console errors 0, fps ~14.
- Screenshots: deliverables/attention/snap/*.png (static debug-preview frames), deliverables/attention/end-result.png, deliverables/attention/contact-sheet.png.

