# integ-a: Hurt
Source: levels-design/hurt (designs-w1 00702bf); art from art-codex 8b6ef1c (overlaid in levels-design/hurt/art). Integrated by tools/charts/integ_a.py
(+ integ_a_tune.py): designer's chart, route and scenery kept; faint / off-layer taps trimmed with local route repair.

- Taps: 118 in the design -> **80 shipped** (trimmed 38: 6 faint, 32 off-layer; flagged but kept: 0).
- Route repair: 14 turn directions flipped next to the edits (flip weight 5); validate.py multi-level crossings designer 11 -> shipped 10. worldPos scenery and camera worldYaw carried with the repaired route.
- validate.py v2.5 on levels-src/hurt: 0 errors.
  == hurt  duration 175.05s  taps 80  dirs R/L 41/39  multi-level crossings 10
  peak density 180 CPM (taps in any 1 s window x60), average 27 CPM; gaps < 0.15 s: 0
- chartlogic after trim: Totals: off-layer (hop) 0, faint 0, weak bursts 0, off-grid 0 (docs/verification/integ-a-hurt-chartlogic.txt).
- Patches: cutaway; calm themed dressing (reeds, stones, empty frames, paper boxes; density 1.6-3.6, small bounce). 38 of 118 taps trimmed (32 off-layer vs the vocal layer) - see integ-a-issues.md #1b.
- **Scripted simulation playthrough** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader, --quality low, 540x960; not physical-device play, not proof of A/V sync):
  state complete, judged 80/80, perfect 79, good 1, diamonds 10/10, save crowns 3,
  timing error mean 1.3 ms sd 6.9 ms max |56| ms, fails 0, console errors 0, fps ~11.
- Screenshots taken during the scripted play (square-corner renderer, rebuild 8d29dd2): play-t020.png, play-t050.png, play-t090.png, play-t110.png, play-t135.png, play-t172.png in deliverables/hurt/shots/; end-result.png; contact-sheet.png.

<details><summary>trimmed taps</summary>

   - 11.262 s off-layer (section follows vocal: layer 0.17, full 0.45, strongest other band 0.68, vocal 0.17)
   - 24.927 s off-layer (section follows vocal: layer 0.27, full 1.46, strongest other band 0.68, vocal 0.27)
   - 27.260 s off-layer (section follows vocal: layer 0.14, full 0.49, strongest other band 0.64, vocal 0.14)
   - 30.260 s off-layer (section follows vocal: layer 0.12, full 1.38, strongest other band 0.7, vocal 0.12)
   - 33.599 s off-layer (section follows vocal: layer 0.21, full 0.74, strongest other band 0.71, vocal 0.21)
   - 34.260 s off-layer (section follows vocal: layer 0.07, full 1.5, strongest other band 0.66, vocal 0.07)
   - 38.260 s off-layer (section follows vocal: layer 0.0, full 1.5, strongest other band 0.72, vocal 0.0)
   - 42.260 s off-layer (section follows vocal: layer 0.12, full 1.1, strongest other band 0.66, vocal 0.12)
   - 43.259 s off-layer (section follows vocal: layer 0.15, full 1.13, strongest other band 1.31, vocal 0.15)
   - 46.916 s off-layer (section follows vocal: layer 0.09, full 0.92, strongest other band 0.82, vocal 0.09)
   - 50.933 s off-layer (section follows vocal: layer 0.12, full 0.4, strongest other band 0.6, vocal 0.12)
   - 51.594 s off-layer (section follows vocal: layer 0.15, full 1.5, strongest other band 0.7, vocal 0.15)
   - 59.594 s faint (section follows vocal: layer 0.32, full 0.26, strongest other band 0.42, vocal 0.32)
   - 79.594 s off-layer (section follows vocal: layer 0.0, full 0.63, strongest other band 0.66, vocal 0.0)
   - 91.928 s faint (section follows vocal: layer 0.21, full 0.27, strongest other band 0.49, vocal 0.21)
   - 96.270 s faint (section follows vocal: layer 0.34, full 0.26, strongest other band 0.4, vocal 0.34)
   - 97.245 s off-layer (section follows vocal: layer 0.1, full 0.64, strongest other band 0.86, vocal 0.1)
   - 101.251 s off-layer (section follows vocal: layer 0.22, full 0.52, strongest other band 0.66, vocal 0.22)
   - 101.924 s off-layer (section follows vocal: layer 0.12, full 0.75, strongest other band 0.69, vocal 0.12)
   - 104.261 s off-layer (section follows vocal: layer 0.32, full 0.42, strongest other band 0.65, vocal 0.32)
   - 104.927 s off-layer (section follows vocal: layer 0.1, full 0.95, strongest other band 0.73, vocal 0.1)
   - 108.261 s off-layer (section follows vocal: layer 0.09, full 0.77, strongest other band 0.66, vocal 0.09)
   - 108.927 s off-layer (section follows vocal: layer 0.03, full 1.5, strongest other band 0.7, vocal 0.03)
   - 109.594 s off-layer (section follows vocal: layer 0.16, full 0.87, strongest other band 1.3, vocal 0.16)
   - 118.927 s off-layer (section follows vocal: layer 0.12, full 1.05, strongest other band 0.94, vocal 0.12)
   - 121.594 s off-layer (section follows vocal: layer 0.04, full 1.11, strongest other band 0.62, vocal 0.04)
   - 122.915 s off-layer (section follows vocal: layer 0.13, full 0.93, strongest other band 0.85, vocal 0.13)
   - 124.261 s off-layer (section follows vocal: layer 0.06, full 1.24, strongest other band 0.72, vocal 0.06)
   - 127.594 s off-layer (section follows vocal: layer 0.16, full 0.57, strongest other band 0.66, vocal 0.16)
   - 130.926 s faint (section follows vocal: layer 0.31, full 0.3, strongest other band 0.46, vocal 0.31)
   - 136.916 s off-layer (section follows vocal: layer 0.27, full 0.72, strongest other band 0.75, vocal 0.27)
   - 140.910 s off-layer (section follows vocal: layer 0.26, full 1.0, strongest other band 1.01, vocal 0.26)
   - 141.247 s off-layer (section follows vocal: layer 0.15, full 0.36, strongest other band 0.61, vocal 0.15)
   - 143.594 s off-layer (section follows vocal: layer 0.0, full 1.5, strongest other band 0.73, vocal 0.0)
   - 155.910 s off-layer (section follows vocal: layer 0.24, full 1.5, strongest other band 1.21, vocal 0.24)
   - 162.911 s off-layer (section follows vocal: layer 0.31, full 1.25, strongest other band 1.1, vocal 0.31)
   - 163.594 s faint (section follows vocal: layer 0.26, full 0.3, strongest other band 0.45, vocal 0.26)
   - 167.602 s faint (section follows vocal: layer 0.11, full 0.34, strongest other band 0.42, vocal 0.11)
</details>

