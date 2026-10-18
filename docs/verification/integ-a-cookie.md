# integ-a: Cookie
Source: levels-design/cookie (designs-w1 00702bf) + art-codex 8b6ef1c art overlay. Taps, dirs, elevation and scenery shipped unchanged
(tools/charts/integ_a.py); one data patch: `cutaway` (see integ-a-issues.md #1).

- Taps: 500 (legacy 357, x1.40); validate.py v2.5 on levels-src: 0 errors, 0 warnings, 63 multi-level crossings, peak 360 CPM, avg 129 CPM.
- chartlogic: off-layer 8, faint 25, weak bursts 0, off-grid 0 (docs/verification/integ-a-cookie-chartlogic.txt). Reported only; taps not changed.
- Height: road climbs to about +52 u (two 24-27 u spiral ramps around the folding stair tower, then the terrace). Snapshot check
  (deliverables/cookie/snap/t043, t105, t125, t170): head and the next road stay readable from the authored `side`/`wide` cameras once the
  tower can fade (before the patch, t043 was blocked by the tower). Spirals NOT flattened.
- **Scripted simulation playthrough** (play.mjs, CDP touches at chart times, headless SwiftShader, --quality low, 540x960):
  state complete, judged 500/500, perfect 499, good 1, diamonds 10/10, crowns 3 in save,
  timing error mean 1.4 ms sd 2.8 ms max 54 ms, fails 0, page errors 0, fps ~12.
  The playthrough ran on the build before the `cutaway` patch (visual-only change; chart identical).
- Screenshots: deliverables/cookie/snap/*.png (debug preview frames, static), deliverables/cookie/end-result.png, deliverables/cookie/contact-sheet.png.

