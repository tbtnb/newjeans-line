# Ditto — 冬日录像带（Winter Videotape）· level design (worker w2, v3)

Files: `chart.json` (422 taps) · `layout.json` (v2.4 + `path.nodes`) · `route.png` · `route-sections.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (6 images).
The codex-ref (`/workspace/nj-refs/ditto/`) is a mood reference only; the route choreography is ours (rev v3 after "routes too simple").
Palette from codex-ref:

| use | colour |
|---|---|
| fog | `#DCE3DF` |
| campus grey-green | `#788A80` |
| chalk-white road | `#F2F0E7` |
| charcoal | `#272D32` |
| coral line | `#C85F65` |
| gems | `#87CBCD` |
| crowns | `#D9B56B` |
| camcorder silver / warm window | `#AEB7BA` / `#D8BE93` |

The cover (OMG single, black/white halftone bunny) appears only as an off-road relief late in the level.

## Concept
- **Song:** warm vocals over a light, urgent Baltimore/Jersey-club kit; the lyric is about waiting for the other person to answer. The drums drop out completely twice (55.8–64.8 s and 114.9–129.3 s); those become the "stillness" spaces.
- **MV:** school, hand-held camcorder, watching tapes back, plaster-cast arm, winter deer. The level walks through a tape of the school in winter: crowded memories open into white silence and are kept, not owned.
- **Space:** campus blocks floating in fog on stacked levels:
  - 0 = campus;
  - +3 = roof;
  - +6 = bridge B1;
  - −4 to −6 = snow island.

  The second half keeps passing over and under the first.

## Core numbers
- **Speed and width:** 10.2 u/s (an 8th = 224 ms = 2.28 u). Width 2.2 → 2.0 (Verse 2) → 2.2 (bridge) → 2.0 → **1.8 (final post)** → 2.2 (outro).
- **Taps: old 181 → new 422 (×2.33)**, averaging 2.27/s. The final chorus is densest.
- **Difficulty (hard tier, title track):** avg CPM 136 (taps ÷ length) / 184 wiki-style; **peak CPM 390** (min gap 154 ms). 11 fast bursts of 3–4 taps on the swung synth/vocal 16ths at phrase fills, the chorus entries, the Post-2 pickup and the final chorus; 86 dotted-8th gaps (the tresillo 3-3-2 feel). Comparison with the original levels is in `chart-report.md`.
- **Fastest run:** 7 consecutive 8ths (224 ms) at 41.3–42.6 s, the Jersey kick roll. The validator counts 8 taps with gaps ≤ 0.30 s at 40.97–42.62 s. Minimum 8th gap 222 ms; bursts go down to 154 ms.
- **Judgment:** the engine rule (v2.4) gives min ±69 ms (inside bursts) and median ±105 ms, i.e. ≤ half the local minimum gap. My target is perfect ±60 / accept ±110 ms.
- **Levels:** 0 → ramp +3 (Post 1 roof) → **fall −7** (snow island, −4) → ramp +6 (Verse 2, +2) → ramp +4 (bridge B1, +6) → **fall −4** (+2) → **spiral ramp −8 round the deer** (−6) → ramp +4 (−2) → **jump +4** onto the memory courtyard (+2, on the pickup at 140.9 s) → **jump +3** onto the rim (+5, 159.8 s) → **fall −5** (fade, 0).
- **Checks:** the validator reports 0 same-level overlaps. The longest same-direction run is 6 (the descending spiral).

## Route choreography (each section has its own texture)
The planner is the same as OMG's: a beam search over per-section motifs and drift bearings with the exact v2.4 overlap rule. The table is computed from the built path.
