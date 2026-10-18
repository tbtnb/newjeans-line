# integ-a: New Jeans
Source: levels-design/new-jeans (designs-w2 d14bb6a); art from art-codex 8b6ef1c (overlaid in levels-design/new-jeans/art). Integrated by tools/charts/integ_a.py
(+ integ_a_tune.py): designer's chart, route and scenery kept; faint / off-layer taps trimmed with local route repair.

- Taps: 162 in the design -> **154 shipped** (trimmed 8: 6 faint, 2 off-layer; flagged but kept: 0).
- Route repair: 11 turn directions flipped next to the edits (flip weight 2); validate.py multi-level crossings designer 62 -> shipped 57. worldPos scenery and camera worldYaw carried with the repaired route.
- validate.py v2.5 on levels-src/new-jeans: 0 errors.
  == new-jeans  duration 109.04s  taps 154  dirs R/L 76/78  multi-level crossings 57
  peak density 300 CPM (taps in any 1 s window x60), average 85 CPM; gaps < 0.15 s: 0
- chartlogic after trim: Totals: off-layer (hop) 0, faint 0, weak bursts 0, off-grid 0 (docs/verification/integ-a-new-jeans-chartlogic.txt).
- Patches: themed dressing (paper voxels, paper houses, five-colour blocks, pixel plants; Break section sparse).
- **Scripted simulation playthrough** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader, --quality low, 540x960; not physical-device play, not proof of A/V sync):
  state complete, judged 154/154, perfect 154, good 0, diamonds 10/10, save crowns 3,
  timing error mean 1.5 ms sd 1.5 ms max |10| ms, fails 0, console errors 0, fps ~15.
- Screenshots taken during the scripted play (square-corner renderer, rebuild 8d29dd2): play-t010.png, play-t025.png, play-t043.png, play-t055.png, play-t075.png, play-t095.png, play-t107.png in deliverables/new-jeans/shots/; end-result.png; contact-sheet.png.

<details><summary>trimmed taps</summary>

   - 2.156 s faint (section follows mid: layer 0.2, full 0.3, strongest other band 0.39, vocal 0.0)
   - 7.063 s faint (section follows mid: layer 0.09, full 0.03, strongest other band 0.18, vocal 0.0)
   - 53.394 s faint (section follows snare: layer 0.26, full 0.28, strongest other band 0.49, vocal 0.13)
   - 55.185 s faint (section follows snare: layer 0.25, full 0.26, strongest other band 0.48, vocal 0.11)
   - 60.558 s off-layer (section follows drums: layer 0.33, full 0.43, strongest other band 0.81, vocal 0.09)
   - 85.422 s faint (section follows drums: layer 0.33, full 0.05, strongest other band 0.2, vocal 0.0)
   - 100.668 s faint (section follows mid: layer 0.24, full 0.29, strongest other band 0.43, vocal 0.05)
   - 101.357 s off-layer (section follows mid: layer 0.28, full 1.08, strongest other band 0.7, vocal 1.31)
</details>

