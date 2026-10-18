# integ-a: Attention
Source: levels-design/attention (designs-w1 00702bf); art from art-codex 8b6ef1c (overlaid in levels-design/attention/art). Integrated by tools/charts/integ_a.py
(+ integ_a_tune.py): designer's chart, route and scenery kept; faint / off-layer taps trimmed with local route repair.

- Taps: 285 in the design -> **222 shipped** (trimmed 63: 47 faint, 16 off-layer; flagged but kept: 0).
- Route repair: 31 turn directions flipped next to the edits (flip weight 20); validate.py multi-level crossings designer 43 -> shipped 50. worldPos scenery and camera worldYaw carried with the repaired route.
- validate.py v2.5 on levels-src/attention: 0 errors.
  == attention  duration 178.05s  taps 222  dirs R/L 113/109  multi-level crossings 50
  peak density 300 CPM (taps in any 1 s window x60), average 75 CPM; gaps < 0.15 s: 3
- chartlogic after trim: Totals: off-layer (hop) 0, faint 0, weak bursts 5, off-grid 4 (docs/verification/integ-a-attention-chartlogic.txt).
- Patches: cutaway (tall onroad landmarks may fade, integ-a-issues.md #1); themed roadside dressing v2.6 (rooftop blocks, water tanks, AC units, potted trees, railings). chartlogic weak bursts 5 remain (not in the trim rule).
- **Scripted simulation playthrough** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader, --quality low, 540x960; not physical-device play, not proof of A/V sync):
  state complete, judged 222/222, perfect 221, good 1, diamonds 10/10, save crowns 3,
  timing error mean 1.2 ms sd 4 ms max |56| ms, fails 0, console errors 0, fps ~14.
- Screenshots taken during the scripted play (square-corner renderer, rebuild 8d29dd2): play-t020.png, play-t055.png, play-t075.png, play-t092.png, play-t128.png, play-t150.png, play-t175.png in deliverables/attention/shots/; end-result.png; contact-sheet.png.

<details><summary>trimmed taps</summary>

   - 7.607 s off-layer (section follows vocal: layer 0.12, full 1.33, strongest other band 0.73, vocal 0.12)
   - 11.900 s faint (section follows drums: layer 0.22, full 0.21, strongest other band 0.22, vocal 0.15)
   - 17.612 s faint (section follows drums: layer 0.25, full 0.33, strongest other band 0.23, vocal 0.15)
   - 24.764 s faint (section follows drums: layer 0.34, full 0.32, strongest other band 0.15, vocal 0.33)
   - 29.327 s off-layer (section follows vocal: layer 0.26, full 0.77, strongest other band 0.62, vocal 0.26)
   - 31.602 s off-layer (section follows vocal: layer 0.29, full 0.73, strongest other band 0.89, vocal 0.29)
   - 44.745 s off-layer (section follows vocal: layer 0.34, full 0.4, strongest other band 0.6, vocal 0.34)
   - 46.452 s off-layer (section follows vocal: layer 0.25, full 0.51, strongest other band 0.73, vocal 0.25)
   - 47.624 s faint (section follows vocal: layer 0.15, full 0.33, strongest other band 0.38, vocal 0.15)
   - 49.897 s off-layer (section follows vocal: layer 0.06, full 0.82, strongest other band 0.78, vocal 0.06)
   - 56.183 s off-layer (section follows vocal: layer 0.17, full 0.84, strongest other band 0.65, vocal 0.17)
   - 58.909 s off-layer (section follows vocal: layer 0.16, full 0.44, strongest other band 0.74, vocal 0.16)
   - 65.341 s faint (section follows drums: layer 0.25, full 0.25, strongest other band 0.25, vocal 0.15)
   - 67.628 s faint (section follows drums: layer 0.34, full 0.32, strongest other band 0.34, vocal 0.23)
   - 68.184 s faint (section follows drums: layer 0.29, full 0.3, strongest other band 0.26, vocal 0.09)
   - 70.194 s faint (section follows drums: layer 0.24, full 0.26, strongest other band 0.22, vocal 0.09)
   - 71.332 s faint (section follows drums: layer 0.19, full 0.25, strongest other band 0.22, vocal 0.15)
   - 72.470 s faint (section follows drums: layer 0.22, full 0.27, strongest other band 0.27, vocal 0.13)
   - 73.909 s faint (section follows drums: layer 0.22, full 0.34, strongest other band 0.23, vocal 0.7)
   - 74.768 s faint (section follows drums: layer 0.19, full 0.31, strongest other band 0.26, vocal 0.21)
   - 79.328 s faint (section follows drums: layer 0.29, full 0.33, strongest other band 0.32, vocal 0.16)
   - 79.614 s faint (section follows drums: layer 0.34, full 0.28, strongest other band 0.22, vocal 0.17)
   - 81.614 s faint (section follows drums: layer 0.33, full 0.34, strongest other band 0.27, vocal 0.15)
   - 85.329 s off-layer (section follows vocal: layer 0.0, full 0.63, strongest other band 0.81, vocal 0.0)
   - 98.743 s off-layer (section follows vocal: layer 0.12, full 1.25, strongest other band 0.79, vocal 0.12)
   - 105.906 s faint (section follows vocal: layer 0.19, full 0.31, strongest other band 0.34, vocal 0.19)
   - 111.316 s off-layer (section follows vocal: layer 0.1, full 0.84, strongest other band 0.81, vocal 0.1)
   - 112.744 s off-layer (section follows vocal: layer 0.14, full 0.63, strongest other band 0.74, vocal 0.14)
   - 113.035 s off-layer (section follows vocal: layer 0.15, full 1.42, strongest other band 0.61, vocal 0.15)
   - 113.604 s off-layer (section follows vocal: layer 0.08, full 1.5, strongest other band 0.65, vocal 0.08)
   - 115.032 s off-layer (section follows vocal: layer 0.23, full 0.8, strongest other band 0.81, vocal 0.23)
   - 120.198 s faint (section follows drums: layer 0.24, full 0.24, strongest other band 0.24, vocal 0.11)
   - 120.761 s faint (section follows drums: layer 0.32, full 0.16, strongest other band 0.22, vocal 0.1)
   - 121.618 s faint (section follows drums: layer 0.31, full 0.19, strongest other band 0.23, vocal 0.13)
   - 122.485 s faint (section follows drums: layer 0.22, full 0.32, strongest other band 0.4, vocal 0.26)
   - 123.046 s faint (section follows drums: layer 0.31, full 0.28, strongest other band 0.24, vocal 0.14)
   - 124.761 s faint (section follows drums: layer 0.3, full 0.26, strongest other band 0.23, vocal 0.12)
   - 125.047 s faint (section follows drums: layer 0.24, full 0.26, strongest other band 0.26, vocal 0.11)
   - 126.189 s faint (section follows drums: layer 0.19, full 0.23, strongest other band 0.23, vocal 0.1)
   - 126.475 s faint (section follows drums: layer 0.34, full 0.27, strongest other band 0.27, vocal 0.12)
   - 128.761 s faint (section follows drums: layer 0.34, full 0.33, strongest other band 0.28, vocal 0.69)
   - 129.614 s faint (section follows drums: layer 0.28, full 0.32, strongest other band 0.32, vocal 0.15)
   - 131.904 s faint (section follows drums: layer 0.26, full 0.27, strongest other band 0.21, vocal 0.3)
   - 134.476 s faint (section follows drums: layer 0.27, full 0.27, strongest other band 0.24, vocal 0.11)
   - 136.476 s faint (section follows drums: layer 0.17, full 0.29, strongest other band 0.24, vocal 0.11)
   - 136.762 s faint (section follows drums: layer 0.34, full 0.34, strongest other band 0.24, vocal 0.12)
   - 138.762 s faint (section follows drums: layer 0.21, full 0.25, strongest other band 0.22, vocal 0.19)
   - 139.905 s faint (section follows drums: layer 0.32, full 0.23, strongest other band 0.24, vocal 0.1)
   - 142.191 s faint (section follows drums: layer 0.33, full 0.28, strongest other band 0.25, vocal 0.2)
   - 144.475 s faint (section follows drums: layer 0.22, full 0.26, strongest other band 0.21, vocal 0.09)
   - 144.763 s faint (section follows drums: layer 0.31, full 0.33, strongest other band 0.22, vocal 0.15)
   - 145.620 s faint (section follows drums: layer 0.2, full 0.25, strongest other band 0.28, vocal 0.16)
   - 148.190 s faint (section follows drums: layer 0.32, full 0.23, strongest other band 0.19, vocal 0.43)
   - 150.192 s faint (section follows drums: layer 0.2, full 0.28, strongest other band 0.19, vocal 0.14)
   - 151.057 s faint (section follows drums: layer 0.22, full 0.25, strongest other band 0.36, vocal 0.15)
   - 152.478 s faint (section follows drums: layer 0.2, full 0.31, strongest other band 0.2, vocal 0.14)
   - 152.764 s faint (section follows drums: layer 0.27, full 0.21, strongest other band 0.23, vocal 0.13)
   - 153.612 s faint (section follows drums: layer 0.24, full 0.3, strongest other band 0.3, vocal 0.19)
   - 154.764 s faint (section follows drums: layer 0.21, full 0.29, strongest other band 0.19, vocal 0.16)
   - 155.907 s faint (section follows drums: layer 0.21, full 0.19, strongest other band 0.24, vocal 0.49)
   - 156.201 s faint (section follows vocal: layer 0.22, full 0.26, strongest other band 0.25, vocal 0.22)
   - 163.907 s faint (section follows vocal: layer 0.2, full 0.33, strongest other band 0.26, vocal 0.2)
   - 171.607 s off-layer (section follows vocal: layer 0.32, full 0.62, strongest other band 0.77, vocal 0.32)
</details>

