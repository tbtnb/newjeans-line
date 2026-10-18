# OMG — 借来的自己（病房 → 身份幻想 → 钢琴尾音）· level design (worker w2, v3)

Files: `chart.json` (412 taps) · `layout.json` (schema v2.5, plus computed `path.nodes` [t,x,z,y,heading]) · `route.png` (whole map) · `route-sections.png` (one zoomed panel per section) · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (5 images).
The codex-ref art (`/workspace/nj-refs/omg/`) is a loose mood reference. **The route choreography below is ours** and is much denser than the blueprint (rev v3 after "routes too simple" feedback).
Palette from codex-ref: cream road `#F3F0E8`, charcoal sides `#25282B`, ward grey-green `#B8C8BC`, fog `#DCE4DA`, pink line `#EFA6B1`, gems `#88C7D5`, crowns `#E3BD60`. The actual OMG single cover is the black/white halftone black bunny. It appears as a low-poly bunny on a halftone plinth and on two halftone posters.

## Concept
- **Song:** bouncy R&B / UK garage with halftime and trap turns. The stem maps show garage-kick verses, a halftime chorus where the synth hook answers the drums, a trap-kick bridge, and a four-on-the-floor dance break.
- **MV motifs:** hospital ward, Hanni's phone/Siri identity, Haerin's cat, fairy-tale princess and glass slipper, group performance. "Borrowed self" is our creative reading, not an official one.
- **Player fantasy:** the line leaves an orderly ward and rides through borrowed identities: stage, slipper tower, phone bridge, book-page library with a cat. In the second half it dances on decks above the places it already passed: the dance break runs over the bridge/library knot, and the final-chorus skybridge runs over the hairpins. It quiets down at the piano tail.

## Core numbers
- **Speed and width:** 10.0 u/s, constant. Road width 2.2 → 2.0 (Chorus 2) → 1.8 (Bridge) → 2.0 → 1.8 (Final chorus b).
- **Taps: old 213 → new 412 (×1.93)**, averaging 1.94 taps/s. The re-audit made the choruses follow the kick/snare groove only (the synth hook is no longer charted in between) and removed 5 faint taps (15.0, 119.9, 120.1, 120.6, 158.5 s).
- **Difficulty (hard tier, title track):** avg CPM 116 (taps ÷ length) / 157 wiki-style. **Peak CPM 360** (validator style, most taps in any 1 s) and 508 instantaneous (min gap 118 ms). Only 2 bursts pass the full-mix and on-beat test: the 3-tap snare 16ths at 63.08 s (Verse 2 entry) and the bridge snare roll at 144.79 s. The final-chorus triplet-hat bursts were removed because they are not clearly audible in the full mix. The honest peak is below 400 CPM. Charting rules (user override): one audible layer per section, the same pattern on every repeat of a phrase, bursts only where the 16th figure is audible in the full mix and starts or ends on a beat, breaks stay sparse, no taps on faint or ghost onsets. CPM numbers are references, not quotas. See the per-section 'What the taps follow' table in `chart-report.md`.
- **Fastest run:** 11 consecutive 8ths (236 ms apart) at 162.1–164.4 s. Minimum 8th gap 226 ms; bursts go down to 118 ms.
- **Judgment:** the engine rule (v2.5, per tap) gives min ±53 ms (inside bursts) and median ±110 ms, always ≤ half the local gap.
- **Levels:** 0 → **fall −4** (Chorus 1 stage) → **spiral ramp +8** (Verse 2, glass-slipper tower, −4 → +4) → **ramp +6** (phone bridge, +10) → **fall −6** (Chorus 2, +4) → **ramp +4** (library, +8) → dance break on the +8 deck → **fall −8** (Final chorus, 0) → **ramp +5** (skybridge B2) → **fall −5** (outro, 0).
- **Checks:** the validator reports 180 segment pairs that cross on different levels and 0 same-level overlaps. The longest same-direction run is 5 (the spiral).

## Route choreography (each section has its own texture)
Planner: every tap's R/L comes from a beam search (width 160) over per-section motifs plus a drift bearing, using the exact v2.4 overlap rule. Motifs:
- **staircase:** alternating turns;
- **zigzag corridor:** R R L L;
- **switchbacks:** U-turn after short legs, reverse after long ones;
- **spiral:** the same hand repeated; laps stack on a steep ramp;
- **long sweeping legs.**

The table is computed from the built path.
