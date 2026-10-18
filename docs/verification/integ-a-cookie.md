# integ-a: Cookie
Source: levels-design/cookie (designs-w1 00702bf); art from art-codex 8b6ef1c (overlaid in levels-design/cookie/art). Integrated by tools/charts/integ_a.py
(+ integ_a_tune.py): designer's chart, route and scenery kept; faint / off-layer taps trimmed with local route repair.

- Taps: 500 in the design -> **458 shipped** (trimmed 42: 23 faint, 19 off-layer; flagged but kept: 0).
- Route repair: 14 turn directions flipped next to the edits (flip weight 12); validate.py multi-level crossings designer 63 -> shipped 63. worldPos scenery and camera worldYaw carried with the repaired route.
- validate.py v2.5 on levels-src/cookie: 0 errors.
  == cookie  duration 233.43s  taps 458  dirs R/L 233/225  multi-level crossings 63
  peak density 360 CPM (taps in any 1 s window x60), average 118 CPM; gaps < 0.15 s: 0
- chartlogic after trim: Totals: off-layer (hop) 0, faint 0, weak bursts 0, off-grid 0 (docs/verification/integ-a-cookie-chartlogic.txt).
- Patches: cutaway (the 19 u folding-stair tower had hidden the head at t 43 s); themed dressing (studio cubes, speakers, CD discs, cookie stools, light stands). Height up to ~+52 u kept (spirals not flattened); readability judged from shots play-t043/t105/t125/t170.
- **Scripted simulation playthrough** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader, --quality low, 540x960; not physical-device play, not proof of A/V sync):
  state complete, judged 458/458, perfect 458, good 0, diamonds 10/10, save crowns 3,
  timing error mean 1.4 ms sd 3.3 ms max |33| ms, fails 0, console errors 0, fps ~13.
- Screenshots taken during the scripted play (square-corner renderer, rebuild 8d29dd2): play-t025.png, play-t043.png, play-t060.png, play-t105.png, play-t125.png, play-t170.png, play-t220.png in deliverables/cookie/shots/; end-result.png; contact-sheet.png.

<details><summary>trimmed taps</summary>

   - 32.589 s faint (section follows drums: layer 0.32, full 0.33, strongest other band 0.28, vocal 0.21)
   - 38.512 s off-layer (section follows vocal: layer 0.25, full 0.79, strongest other band 0.82, vocal 0.25)
   - 40.600 s off-layer (section follows vocal: layer 0.13, full 1.37, strongest other band 0.81, vocal 0.13)
   - 41.761 s off-layer (section follows vocal: layer 0.16, full 0.86, strongest other band 0.64, vocal 0.16)
   - 42.701 s off-layer (section follows vocal: layer 0.17, full 0.65, strongest other band 0.81, vocal 0.17)
   - 45.582 s off-layer (section follows vocal: layer 0.27, full 0.6, strongest other band 0.61, vocal 0.27)
   - 48.623 s off-layer (section follows vocal: layer 0.24, full 0.76, strongest other band 0.94, vocal 0.24)
   - 50.359 s faint (section follows drums: layer 0.32, full 0.25, strongest other band 0.34, vocal 0.24)
   - 51.888 s faint (section follows drums: layer 0.32, full 0.31, strongest other band 0.39, vocal 0.11)
   - 58.194 s faint (section follows drums: layer 0.34, full 0.21, strongest other band 0.26, vocal 0.31)
   - 62.971 s off-layer (section follows drums: layer 0.32, full 0.34, strongest other band 0.6, vocal 0.08)
   - 63.936 s faint (section follows drums: layer 0.18, full 0.27, strongest other band 0.16, vocal 0.23)
   - 69.474 s faint (section follows drums: layer 0.26, full 0.2, strongest other band 0.32, vocal 0.16)
   - 76.347 s faint (section follows drums: layer 0.33, full 0.31, strongest other band 0.3, vocal 0.11)
   - 97.942 s faint (section follows vocal: layer 0.24, full 0.33, strongest other band 0.4, vocal 0.24)
   - 101.750 s off-layer (section follows vocal: layer 0.14, full 1.4, strongest other band 0.67, vocal 0.14)
   - 103.851 s off-layer (section follows vocal: layer 0.2, full 0.41, strongest other band 0.68, vocal 0.2)
   - 109.772 s off-layer (section follows vocal: layer 0.24, full 0.79, strongest other band 0.81, vocal 0.24)
   - 111.507 s faint (section follows drums: layer 0.3, full 0.24, strongest other band 0.32, vocal 0.2)
   - 119.341 s faint (section follows drums: layer 0.31, full 0.22, strongest other band 0.27, vocal 0.32)
   - 121.823 s faint (section follows drums: layer 0.3, full 0.29, strongest other band 0.24, vocal 0.16)
   - 125.074 s faint (section follows drums: layer 0.25, full 0.27, strongest other band 0.24, vocal 0.15)
   - 130.624 s faint (section follows drums: layer 0.31, full 0.21, strongest other band 0.25, vocal 0.15)
   - 131.007 s faint (section follows drums: layer 0.31, full 0.29, strongest other band 0.22, vocal 0.2)
   - 137.112 s faint (section follows drums: layer 0.24, full 0.22, strongest other band 0.2, vocal 0.25)
   - 149.341 s faint (section follows drums: layer 0.29, full 0.25, strongest other band 0.27, vocal 0.23)
   - 160.424 s faint (section follows drums: layer 0.32, full 0.3, strongest other band 0.33, vocal 0.19)
   - 161.953 s faint (section follows drums: layer 0.32, full 0.29, strongest other band 0.32, vocal 0.19)
   - 168.259 s faint (section follows drums: layer 0.34, full 0.22, strongest other band 0.27, vocal 0.3)
   - 173.991 s faint (section follows drums: layer 0.24, full 0.26, strongest other band 0.27, vocal 0.4)
   - 174.182 s faint (section follows drums: layer 0.32, full 0.27, strongest other band 0.28, vocal 0.19)
   - 197.495 s off-layer (section follows drums: layer 0.26, full 0.68, strongest other band 0.88, vocal 0.0)
   - 210.280 s off-layer (section follows vocal: layer 0.25, full 0.78, strongest other band 0.82, vocal 0.25)
   - 211.244 s off-layer (section follows vocal: layer 0.13, full 0.31, strongest other band 0.83, vocal 0.13)
   - 211.812 s off-layer (section follows vocal: layer 0.19, full 0.75, strongest other band 0.79, vocal 0.19)
   - 214.309 s off-layer (section follows vocal: layer 0.05, full 0.4, strongest other band 0.91, vocal 0.05)
   - 220.425 s off-layer (section follows vocal: layer 0.06, full 0.52, strongest other band 0.68, vocal 0.06)
   - 221.565 s off-layer (section follows vocal: layer 0.06, full 1.0, strongest other band 0.65, vocal 0.06)
   - 223.291 s faint (section follows vocal: layer 0.19, full 0.28, strongest other band 0.41, vocal 0.19)
   - 223.482 s off-layer (section follows vocal: layer 0.08, full 0.4, strongest other band 0.92, vocal 0.08)
   - 226.349 s off-layer (section follows vocal: layer 0.12, full 0.83, strongest other band 0.93, vocal 0.12)
   - 228.659 s faint (section follows vocal: layer 0.24, full 0.15, strongest other band 0.38, vocal 0.24)
</details>

