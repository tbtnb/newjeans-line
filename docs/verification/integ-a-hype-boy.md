# integ-a: Hype Boy
Source: levels-design/hype-boy (designs-w1 00702bf) with art-codex 8b6ef1c art overlay where present. Taps, dirs, elevation and scenery shipped unchanged
by tools/charts/integ_a.py (patches, if any, listed below).

- validate.py v2.5 on levels-src/hype-boy: 0 errors, 0 warnings.
  == hype-boy  duration 176.64s  taps 327  dirs R/L 168/159  multi-level crossings 44
  peak density 300 CPM (taps in any 1 s window x60), average 111 CPM; gaps < 0.15 s: 2
- chartlogic (Totals: off-layer (hop) 0, faint 2, weak bursts 1, off-grid 195); full table: docs/verification/integ-a-hype-boy-chartlogic.txt. Reported only; taps not changed.
- Patch: `cutaway` (5 tall onroad landmarks may fade when occluding; integ-a-issues.md #1).
- Outro (170.65-176.64 s, 0 taps): last tap 168.263 s, then an 8.4 s straight (~75 u) under the authored `wide` camera (dist 28) into the blue pyramid finish with the bunny echo; snapshot t175 shows the finish straight and pyramid clearly, and the scripted run ended in state complete at 176.59 s with the results screen (end-result.png). No data change needed.
- chartlogic off-grid 195 is a grid-refit artifact (100.468 BPM refit, swung groove, no meta.beat_period in the chart); see integ-a-issues.md #2.
- **Scripted simulation playthrough** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader, --quality low, 540x960;
  not physical-device play, not proof of A/V sync): state complete, judged 327/327, perfect 327, good 0,
  diamonds 10/10, save crowns 3, timing error mean 1.4 ms sd 1.3 ms max |12| ms,
  fails 0, console errors 0, fps ~13.
- Screenshots: deliverables/hype-boy/snap/*.png (static debug-preview frames), deliverables/hype-boy/end-result.png, deliverables/hype-boy/contact-sheet.png.

