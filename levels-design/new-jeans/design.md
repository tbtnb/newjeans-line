# New Jeans — 城市换新 City Unfolded · level design (worker w2, v3)

Files: `chart.json` (167 taps) · `layout.json` (v2.4 + `path.nodes`) · `route.png` · `route-sections.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (5 images).
**Aligned with codex-ref** (`/workspace/nj-refs/new-jeans/`): a pink solid line through a light-blue city that keeps unfolding; streets → rooftops → the five flight trails become the skyline. Cover = **Get Up EP digital cover** (pale-blue pixel city, five Powerpuff-style members, five colour trails, small bunny icon top-left). The blueprint shapes are mood only; the route choreography is ours.

## Concept
- **Song:** a 1:49 opener with a Baltimore/UK-garage club beat at 134 BPM. The MV is the Powerpuff Girls collaboration. Theme: renewing yourself, showing a new style, inviting others along. The mood is light, confident and bouncy.
- **Level:**
  - the pink line starts on a blank city plan (graph-paper ground);
  - blocks unfold;
  - the line wraps round the **Bunny Gate**;
  - it climbs an alley ramp onto L1, where a horseshoe of staircases wraps the **sunken city courtyard** while five **flight fins** rise;
  - it drops under the chorus deck (E1 bunny shadow);
  - the city re-rises;
  - the line spirals up the courtyard tower;
  - it flies on L2 above everything;
  - the five trails freeze into the **cover tableau**.
- **Palette** (codex-ref):

  | use | colour |
  |---|---|
  | sky | `#DDF5FF` |
  | ivory road | `#FFF9ED` |
  | city | `#73D5EB` |
  | denim sides | `#397FC0` |
  | ink / road side | `#164A63` |
  | player line | `#F36BA5` |
  | crown | `#F5CA63` |
  | five trail colours | `#F36BA5 #397FC0 #8FDFB7 #F5CA63 #B7A0EA` (mint/peach/lavender from the fins) |

  Diamonds are pink and the crown is gold (`collectibleColors`).

## Core numbers
- **Speed and width:** 10.2 u/s. Width 2.2 → 2.0 (Chorus 1) → 1.8 (Chorus 2) → 2.2 (outro).
- **Taps: old 68 → new 167 (×2.46)**, averaging 1.53/s. This is above 2× because the old chart was anomalously sparse (0.62/s, first tap at 8 s). A trim to about 150 is possible: drop the snare on beat 2 in Verse 2 for every other bar.
- **Fastest run:** 6 × 8th (224 ms) at 63.3 s (Rebuild). Minimum gap 222 ms.
- **Judgment:** the engine rule (v2.4) gives min ±100 ms and median ±110 ms. My target is perfect ±60 / accept ±115 ms.
- **Levels** (codex L0/L1/L2 = 0/+4/+8): 0 → **alley ramp +4** (31.7–35.8 s, L1) → **fall −4** at the break (50.8 s, L0, under the chorus deck) → **spiral ramp +4** round the courtyard tower (79–83 s, L1) → **ramp +4** into Chorus 2 (86–92 s, L2), and it stays on top to the finish.
- **Checks:** the validator reports 0 same-level overlaps.

## Route choreography (each section has its own texture)
Planner: beam search over per-section motifs plus a drift bearing, using the exact v2.4 overlap rule. The table is computed from the built path.
| Section | Route texture (planner motifs) | taps | max same-dir run | U-turns | height | over/under-passes |
|---|---|---|---|---|---|---|
| Intro · 方格纸 (0.0s) | long sweeping legs → 0°, long sweeping legs → 90° | 8 | 2 | 2 | +0..+0 | 0 |
| Beat in · 蓝图线 (7.5s) | switchbacks → 90° | 13 | 6 | 5 | +0..+0 | 0 |
| Verse 1 · 纸片房屋 (14.7s) | spiral / wrap R, switchbacks → 0°, zigzag corridor (RRLL) → 0°, staircase → 45° | 26 | 2 | 9 | +0..+4 | 0 |
| Chorus 1 · 五色尾迹 (36.2s) | staircase → 90°, staircase → 180°, staircase → 270° | 26 | 2 | 2 | +4..+4 | 13 |
| Break · 像素平面 (50.5s) | long sweeping legs | 10 | 3 | 4 | +0..+4 | 6 |
| Rebuild · 重新立起 (57.7s) | staircase → 0°, staircase → 90°, staircase → 0°, staircase → 90° | 16 | 2 | 1 | +0..+0 | 13 |
| Verse 2 · 立体城市 (64.8s) | zigzag corridor (RRLL) → 270°, switchbacks → 0°, spiral / wrap L, staircase → 0° | 29 | 2 | 8 | +0..+4 | 15 |
| Chorus 2 · 飞行 (86.3s) | staircase → 90°, staircase → 0°, staircase → 90°, staircase → 180° | 33 | 3 | 10 | +4..+8 | 31 |
| Outro · 牛仔徽章 (100.6s) | long sweeping legs → 90° | 6 | 2 | 1 | +8..+8 | 2 |

How each section reads (see `route-sections.png`):
- **Intro (0–7.5 s):** one long straight and one big L on the synth stabs. Six side slabs flip up when the percussion enters (codex P1).
- **Beat in (7.5–14.7 s):** switchbacks on the syncopated 2-step snares, ending in an 8-tap fill.
- **Verse 1 (14.7–36 s):**
  - a same-hand **wrap round the Bunny Gate** (white voxel gate with square eyes; its face uses `art/bunny-gate-face.jpg`);
  - then an open U through the courtyard;
  - then a **four-fold offset alley through a cut-away block** (`alley_block_*`);
  - then a NE staircase up the alley ramp onto L1.

  Courtyard building rows rise between vocal phrases.
- **Chorus 1 (36–50.5 s):** on L1, a **horseshoe of staircases** (E → S → W), open on one side, beside the sunken city courtyard. The courtyard's blocks rise from below (y −4 relative to the deck). The five flight fins rise one per half-bar on the hook accents and glow in turn (targeted `light`, music-timed).
- **Break (50.5–57.7 s):** drums out, off-beat claps. The line **drops 4** and runs a short S **under the chorus deck** (cross bonus in the planner). Tall blocks lower. **E1:** for one beat the fins' shadows form a bunny on the ground (`egg_bunny_shadow`).
- **Rebuild (57.7–65 s):** a zigzag of staircases that switches N/E every bar while ten towers re-rise on the kicks. It contains the 6-tap 8th run.
- **Verse 2 (65–86 s):** a four-fold offset alley (RRLL corridor) heading west, short switchbacks, then a **square spiral up the courtyard tower** (+4 in 3.6 s, laps stacked ≥ 3 apart), then a north staircase.
- **Chorus 2 (86–100.6 s):** **ramp to L2 (+8)**. Big offset staircases (E, N, E, S) above the whole city; the fins slowly spin open like pages. The **pixel sky billboard** floats far off-road.
- **Outro (100.6–109 s):** one elbow and a long finish straight on L2 to the **cover tableau** (five pixel silhouettes and five colour bands). There are no sudden turns at the end.

## Map performance, camera, scenery
- **Camera:**
  - iso;
  - small yaw round the gate;
  - `wide` (codex: pull out about 15 %) at Chorus 1;
  - `high` under the deck in the break (keeps the deck from hiding the road);
  - `side` along the alley;
  - `high` on the spiral;
  - `wide` at Chorus 2;
  - slow `high` pull-back at the end.

  The camera turns only on downbeats or long straights.
- **Road reveal:** rise (2.0 s) → unfold (1.6 s) → static under the deck (2.0 s) → rise at the rebuild (1.5 s) → unfold at Chorus 2 (1.6 s).
- **Fake-out forks** (`fakefork*` at 55.2, 71.3, 102.5 s): the slab seems to continue straight past a visible corner and then falls away. Visual only; they never mark timing.
- **Landmarks** are placed into open pockets (`worldPos`):
  - Bunny Gate;
  - courtyard block rows;
  - sunken city courtyard;
  - five flight fins;
  - courtyard tower;
  - pixel sky billboard;
  - five-trails ground decal;
  - cover tableau (finish).

## Art assets (`art/`, listed in `layout.art.files`)
| file | use |
|---|---|
| `art/sky.jpg` | `art.backdrop`: pale sky blue with white pixel clouds |
| `art/ground-graph-paper.jpg` | `art.ground` (scale 32): the city plan |
| `art/pixel-billboard.jpg` | billboard `image` `pixel_billboard`: five abstract pixel flyers with trails and a small pixel bunny (no faces, no text) |
| `art/bunny-gate-face.jpg` | `parts[].texture` on the Bunny Gate lintel |
| `art/five-trails-decal.png` | flat `image` `trails_decal` on the ground below the L2 flight |

The art is procedural PIL (`_w2_tools/artgen.py`) in the codex palette. There are no real people's faces; the "members" are abstract pixel blobs.

## Eggs, collectibles, fairness
- **Eggs:**
  - **E1** (Break, ≈ 54 s): the bunny shadow formed by the fins, for one beat.
  - **E2**: a little potted plant that nods on the player's own taps (31 s, `react: tap`).

  Both are off-road and need no branch.
- **Diamonds (10):** 17.9, 26.9, 42.0, 47.0, 48.8, 54.7, 71.6, 93.6, 97.2, 99.0 s. Codex distribution 0/2/1/3/1/3/0 adapted to my sections: 2 in Verse 1, 3 in Chorus 1, 1 in the break, 1 in Verse 2, 3 in Chorus 2.
- **Crowns:** 34.9 s (top of the alley ramp, before Chorus 1) and 81.5 s (Verse 2 tower). The finish is the 3rd.
- **No tap hints:** no markers, no pulses, no countdowns, no guide lines. The fin `light` events follow the hook on half-notes, not the next turn.
- **Air-time:** the break fall was moved to 50.77 s so there is ≥ 0.40 s before the next tap.

## Chart rationale (why the taps are where they are)
- **Intro (0–7.5 s)**: synth stabs only (other stem "O" on steps 0 and 6): 2 taps per bar — the line is drawn on graph paper.
- **Beat in (7.5–14.7 s)**: drums without bass: taps on the snare accents at steps 2,4,12 (syncopated 2-step snares), 8-tap fill in bar 7.
- **Verse 1 / 2**: garage 2-step: kick on 1 and the "and" of 3 (steps 0,10) every bar, plus snare on beat 2 every other bar — 2–3 taps per bar so the rap-like vocal sits on a readable pulse.
- **Chorus 1 / 2**: jersey kick on 2, 3, 3a, 4+ (steps 4,8,11,14) under the "new hair, new tee" hook; the downbeat snare starts every other bar; bar 27/55 ends with an 8th kick roll (5 taps).
- **Break (50.5–57.7 s)**: kick drops, only off-beat claps on steps 2,6,10,14: the player taps off the beat for 4 bars (syncopation test).
- **Rebuild (57.7–64.9 s)**: kick returns on beats 2 and 4 with off-beat claps: "..s.k" call-response pairs, 7-tap run in bar 35.
- **Outro (100.7–109 s)**: drums stop, synth stabs: 1–2 taps per bar, camera pulls back.

## Per-section density (from chart-report.md)

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 方格纸 | intro | 8 | 1.07 | 1.5/s |
| 7.51 | Beat in · 蓝图线 | intro | 13 | 1.81 | 3.0/s |
| 14.68 | Verse 1 · 纸片房屋 | verse | 26 | 1.21 | 2.0/s |
| 36.17 | Chorus 1 · 五色尾迹 | chorus | 26 | 1.81 | 3.0/s |
| 50.50 | Break · 像素平面 | break | 10 | 1.40 | 2.0/s |
| 57.66 | Rebuild · 重新立起 | break | 16 | 2.23 | 3.5/s |
| 64.83 | Verse 2 · 立体城市 | verse | 29 | 1.35 | 2.5/s |
| 86.32 | Chorus 2 · 飞行 | chorus | 33 | 2.30 | 3.0/s |
| 100.64 | Outro · 牛仔徽章 | outro | 6 | 0.72 | 1.5/s |


Sync: every tap is snapped to a real onset of its tagged demucs stem (shifted −25.03 ms) within ±45 ms; spot checks at start / middle / section changes / end are in `chart-report.md` (stem and independent full-mix detector).
