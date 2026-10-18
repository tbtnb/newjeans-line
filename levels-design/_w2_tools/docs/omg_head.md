# OMG — 借来的自己（病房 → 身份幻想 → 钢琴尾音）· level design (worker w2, v3)

Files: `chart.json` (459 taps) · `layout.json` (schema v2.4, plus computed `path.nodes` [t,x,z,y,heading]) · `route.png` (whole map) · `route-sections.png` (one zoomed panel per section) · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (5 images).
The codex-ref art (`/workspace/nj-refs/omg/`) is a loose mood reference. **The route choreography below is ours** and is much denser than the blueprint (rev v3 after "routes too simple" feedback).
Palette from codex-ref: cream road `#F3F0E8`, charcoal sides `#25282B`, ward grey-green `#B8C8BC`, fog `#DCE4DA`, pink line `#EFA6B1`, gems `#88C7D5`, crowns `#E3BD60`. The actual OMG single cover is the black/white halftone black bunny. It appears as a low-poly bunny on a halftone plinth and on two halftone posters.

## Concept
- **Song:** bouncy R&B / UK garage with halftime and trap turns. The stem maps show garage-kick verses, a halftime chorus where the synth hook answers the drums, a trap-kick bridge, and a four-on-the-floor dance break.
- **MV motifs:** hospital ward, Hanni's phone/Siri identity, Haerin's cat, fairy-tale princess and glass slipper, group performance. "Borrowed self" is our creative reading, not an official one.
- **Player fantasy:** the line leaves an orderly ward and rides through borrowed identities: stage, slipper tower, phone bridge, book-page library with a cat. In the second half it dances on decks above the places it already passed: the dance break runs over the bridge/library knot, and the final-chorus skybridge runs over the hairpins. It quiets down at the piano tail.

## Core numbers
- **Speed and width:** 10.0 u/s, constant. Road width 2.2 → 2.0 (Chorus 2) → 1.8 (Bridge) → 2.0 → 1.8 (Final chorus b).
- **Taps: old 213 → new 459 (×2.15)**, averaging 2.16 taps/s. The dance break is densest at 3.1/s.
- **Fastest run:** 11 consecutive 8ths (236 ms apart) at 162.1–164.4 s. Minimum gap 226 ms.
- **Judgment:** the engine rule (v2.4) gives min ±102 ms and median ±110 ms. My target is perfect ±60 / accept ±110 ms.
- **Levels:** 0 → **fall −4** (Chorus 1 stage) → **spiral ramp +8** (Verse 2, glass-slipper tower, −4 → +4) → **ramp +6** (phone bridge, +10) → **fall −6** (Chorus 2, +4) → **ramp +4** (library, +8) → dance break on the +8 deck → **fall −8** (Final chorus, 0) → **ramp +5** (skybridge B2) → **fall −5** (outro, 0).
- **Checks:** the validator reports 180 segment pairs that cross on different levels and 0 same-level overlaps. The longest same-direction run is 5 (the spiral).

## Route choreography (each section has its own texture)
Planner: every tap's R/L comes from a beam search (width 80) over per-section motifs plus a drift bearing, using the exact v2.4 overlap rule. Motifs:
- **staircase:** alternating turns;
- **zigzag corridor:** R R L L;
- **switchbacks:** U-turn after short legs, reverse after long ones;
- **spiral:** the same hand repeated; laps stack on a steep ramp;
- **long sweeping legs.**

The table is computed from the built path.
