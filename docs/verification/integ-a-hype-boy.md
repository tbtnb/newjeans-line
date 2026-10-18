# integ-a: Hype Boy
Source: levels-design/hype-boy (designs-w1 00702bf); art from art-codex 8b6ef1c (overlaid in levels-design/hype-boy/art). Integrated by tools/charts/integ_a.py
(+ integ_a_tune.py): designer's chart, route and scenery kept; faint / off-layer taps trimmed with local route repair.

- Taps: 327 in the design -> **317 shipped** (trimmed 10: 0 faint, 10 off-layer; flagged but kept: 0).
- Route repair: 13 turn directions flipped next to the edits (flip weight 8); validate.py multi-level crossings designer 44 -> shipped 43. worldPos scenery and camera worldYaw carried with the repaired route.
- validate.py v2.5 on levels-src/hype-boy: 0 errors.
  == hype-boy  duration 176.64s  taps 317  dirs R/L 161/156  multi-level crossings 43
  peak density 300 CPM (taps in any 1 s window x60), average 108 CPM; gaps < 0.15 s: 2
- chartlogic after trim: Totals: off-layer (hop) 0, faint 0, weak bursts 1, off-grid 188 (docs/verification/integ-a-hype-boy-chartlogic.txt).
- Patches: cutaway; themed dressing (lockers, deck chairs, pool floats, palms, cones). Outro 0 taps: last tap 168.263 s then ~8.4 s straight under the wide camera into the pyramid finish (see shots play-t174 and end-result). chartlogic off-grid count is a grid-refit artifact (integ-a-issues.md #2).
- **Scripted simulation playthrough** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader, --quality low, 540x960; not physical-device play, not proof of A/V sync):
  state complete, judged 317/317, perfect 317, good 0, diamonds 10/10, save crowns 3,
  timing error mean 1.5 ms sd 1.6 ms max |20| ms, fails 0, console errors 0, fps ~12.
- Screenshots taken during the scripted play (square-corner renderer, rebuild 8d29dd2): play-t015.png, play-t045.png, play-t062.png, play-t100.png, play-t140.png, play-t160.png, play-t174.png in deliverables/hype-boy/shots/; end-result.png; contact-sheet.png.

<details><summary>trimmed taps</summary>

   - 38.656 s off-layer (section follows vocal: layer 0.26, full 0.49, strongest other band 0.76, vocal 0.26)
   - 40.755 s off-layer (section follows vocal: layer 0.08, full 0.44, strongest other band 0.98, vocal 0.08)
   - 42.411 s off-layer (section follows vocal: layer 0.25, full 1.0, strongest other band 0.79, vocal 0.25)
   - 43.155 s off-layer (section follows vocal: layer 0.1, full 0.43, strongest other band 1.27, vocal 0.1)
   - 43.455 s off-layer (section follows vocal: layer 0.3, full 0.24, strongest other band 1.0, vocal 0.3)
   - 117.560 s off-layer (section follows vocal: layer 0.11, full 0.65, strongest other band 0.98, vocal 0.11)
   - 119.200 s off-layer (section follows vocal: layer 0.33, full 0.57, strongest other band 0.77, vocal 0.33)
   - 119.960 s off-layer (section follows vocal: layer 0.13, full 0.42, strongest other band 1.27, vocal 0.13)
   - 120.260 s off-layer (section follows vocal: layer 0.33, full 0.27, strongest other band 1.02, vocal 0.33)
   - 123.260 s off-layer (section follows vocal: layer 0.32, full 0.42, strongest other band 1.31, vocal 0.32)
</details>

