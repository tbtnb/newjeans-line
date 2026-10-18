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
| Section | Route texture (planner motifs) | taps | max same-dir run | U-turns | height | over/under-passes |
|---|---|---|---|---|---|---|
| Intro · 病房走廊 (0.0s) | long sweeping legs → 0°, long sweeping legs → 90° | 12 | 3 | 3 | +0..+0 | 0 |
| Verse 1 · 治疗桌与五椅 (15.1s) | switchbacks → 90° | 29 | 2 | 4 | +0..+0 | 0 |
| Verse 1b · 墙板外折 (30.3s) | zigzag corridor (RRLL) → 0° | 30 | 2 | 15 | +0..+0 | 8 |
| Chorus 1 · 黑兔舞台 (45.4s) | staircase → 135°, staircase → 225°, staircase → 135°, staircase → 45° | 42 | 2 | 3 | -4..-4 | 5 |
| Verse 2 · 玻璃鞋 (60.5s) | switchbacks → 270°, spiral / wrap R, staircase → 300°, zigzag corridor (RRLL) → 270° | 32 | 5 | 12 | -4..+4 | 9 |
| Verse 2b · 双折长短路 (75.6s) | zigzag corridor (RRLL) → 270°, staircase → 0°, switchbacks → 60° | 29 | 5 | 8 | +4..+4 | 10 |
| Pre · 手机桥 (90.7s) | long sweeping legs → 150° | 28 | 2 | 1 | +4..+10 | 0 |
| Chorus 2 · 屏幕块 (105.9s) | staircase → 90°, staircase → 180°, staircase → 270°, staircase → 0° | 43 | 2 | 2 | +4..+4 | 0 |
| Post · 错列直角 (121.0s) | switchbacks → 270°, zigzag corridor (RRLL) → 180° | 23 | 3 | 7 | +4..+4 | 11 |
| Bridge · 书页墙与猫 (134.2s) | switchbacks → 200° | 40 | 5 | 20 | +4..+8 | 14 |
| Break · 书页合拢 (149.3s) | long sweeping legs | 3 | 2 | 1 | +8..+8 | 0 |
| Dance break · 舞台五墙 (151.2s) | staircase → 330°, staircase → 60°, staircase → 330°, staircase → 60° | 47 | 3 | 7 | +8..+8 | 26 |
| Final chorus · 兔耳发夹 (166.3s) | spiral / wrap L, staircase → 90°, spiral / wrap L, staircase → 90°, zigzag corridor (RRLL) → 180° | 43 | 3 | 15 | +0..+0 | 20 |
| Final chorus b · 天桥 (181.4s) | staircase → 270°, staircase → 180°, staircase → 90°, staircase → 0° | 44 | 2 | 8 | +0..+5 | 31 |
| Outro · 尾奏琴键 (196.6s) | long sweeping legs → 180° | 14 | 2 | 3 | +0..+0 | 0 |

How each section reads (see `route-sections.png`):
- **Intro (0–15 s):** long sweeping corridor legs of 2–4 s on the a-cappella "OMG" phrases. Ward door frames mark the scale.
- **Verse 1 (15–30 s):** serpentine switchbacks heading east along the ward wall. The clap rhythm (long–short–long–short) gives the long/short legs.
- **Verse 1b (30–45 s):** a tight R R L L zigzag corridor that runs **through a cut-away ward block**. Wall blocks have openings exactly where the road passes. Wall panels fold outward one by one.
- **Chorus 1 (45–60 s):** **drop −4** onto the stage floor. A zigzag of staircases changes diagonal every 2 bars (SE, SW, SE, NE), with the black bunny in its pocket.
- **Verse 2 (60–75 s):** one bar of switchbacks, then a **square spiral that climbs 8 units in 3.8 s** around the glass-slipper tower. Each lap passes ≥ 3 above the previous one (5 same-hand turns), and it exits as a NW staircase.
- **Verse 2b (75–90 s):** a zigzag corridor, then a north staircase, then switchbacks that curl back over the Chorus 1 area on the upper level.
- **Pre (91–106 s):** drums out. The **phone bridge B1** is a long sweeping ramp (+6, to +10) heading SE over the Chorus 1 stage.
- **Chorus 2 (106–121 s):** **drop −6**. A **ring of staircases** turns E → S → W → N, one quarter every 2 bars, and encloses an open plaza with five phone-screen blocks.
- **Post (121–134 s):** switchbacks and a zigzag corridor heading west and south, with a fake-out fork at 124.7 s.
- **Bridge (134–149 s):** narrow (1.8) **climbing switchbacks inside the book-page library** (cut-away walls, 20 U-turns, +4 ramp). The trap kick starts every bar off the beat. The black cat sits on a shelf.
- **Break (149–151 s):** three taps and a top-down camera.
- **Dance break (151–166 s):** long 8th-note staircases (6, 8, 11 taps) on the +8 deck that alternate NW and NE every 2 bars. They pass **over** the library and Post (26 over/under-pass segments).
- **Final chorus (166–181 s):** **drop −8** to the ward level. Two same-hand hairpins (bunny ears), then a south zigzag, crossed later by the skybridge.
- **Final chorus b (181–197 s):** **skybridge B2 ramps +5** while a ring of staircases (W, S, E, N) loops back over the hairpins (31 over/under-pass segments).
- **Outro (197–212 s):** **drop −5**, then long sweeping legs on the piano stabs. Three piano keys are pressed by the player's own taps.

## Map performance, camera, scenery
- **Camera:**
  - iso intro;
  - `high` (dist 21) at the Chorus 1 drop;
  - `side` swing in Verse 2 (the spiral reads from the side);
  - `low` chase up the phone bridge;
  - `wide` punch at Chorus 2;
  - `high` pitch 62 in the narrow library;
  - `top` for the 1-bar break;
  - iso + light shake in the dance break;
  - `wide` for the final-chorus ears;
  - slow `high` pull-back in the outro.

  Camera turns only on section downbeats.
- **Road reveal:** rise (lead 1.8 s) → unfold at Chorus 1 (1.6) → drop in the bridge (1.4) → rise at the dance break (1.4) → fade in the outro (2.0). Every lead is ≥ 1.4 s.
- **Cut-away buildings** (generated from the path):
  - `ward_block_*`, 43 wall blocks around the Verse 1b zigzag;
  - `library_*`, 36 blocks around the bridge switchbacks.

  They rise 2.5 s before the line enters and leave openings where any road at that level passes.
- **Fake-out forks** (`fakefork*`, visual only): at 124.7 s and 202.9 s the slab also seems to run straight on past a real corner, then crumbles (exit: fall). This is the classic DL fake branch. It sits on a corner that is already visible and never marks timing.
- **Landmarks** are placed by the builder into the most open pocket near their time (`worldPos`), e.g. the bunny inside the Chorus 1 staircase zigzag and the glass slipper next to the spiral:
  - ward doors and ceiling light row;
  - treatment table with five chairs;
  - black halftone bunny on its plinth, plus five stage walls;
  - glass slipper;
  - phone bridge body, phone face and signal bars;
  - book pages and the black cat shelf;
  - bunny-ear sculptures;
  - three piano keys (react `tap`);
  - halftone end plinth.

## Art assets (`art/`, listed in `layout.art.files`)
| file | use in layout |
|---|---|
| `art/sky.jpg` | `art.backdrop`: soft sage → cream sky, halftone clouds, blush horizon |
| `art/ground-halftone.jpg` | `art.ground` (scale 36): tileable halftone dots (cover print) |
| `art/bunny-poster.jpg` | `image` objects `poster_bunny_a` (Chorus 1) and `poster_bunny_b` (dance break, react kick): halftone black bunny with a blank mask, no features |
| `art/phone-screen.jpg` | `image` `phone_face` beside the phone bridge: black screen, chat bubbles, typing dots, no text |
| `art/slipper-cat-decal.png` | billboards `slipper_sticker` (spiral) and `cat_sticker` (library): transparent sticker |

The art was drawn procedurally with PIL (`_w2_tools/artgen.py`, flat/halftone style in the level palette). The GenerateImage tool returned paths that did not exist on the box, so its output could not be saved; the prompts are in the tool README. There are no faces, no text, and no arrows.

## Eggs, collectibles, fairness
- **Eggs:**
  - **E1** (Bridge, 145 s): during the long vocal the pages' shadows form cat ears and the cat turns its head (`egg_cat_ears`).
  - **E2** (outro, 204 s): three "calling…" dots become three gold stars (`egg_three_dots`).

  Both are off-road and need no branch or extra input.
- **Diamonds (10):** 8.2, 26.8, 59.2, 83.9, 99.9, 121.5, 143.0, 150.7, 197.6, 200.2 s. Each is centred on a straight, ≥ 0.2 s from any tap, and away from fall/ramp starts.
- **Crowns:** 95.1 s (on the phone bridge) and 132.9 s (before the library). The 3rd crown is the finish.
- **No tap hints of any kind:** no corner markers, no road pulses, no countdowns, no guide line. Scenery `react` is `beat`/`kick` (music) or `tap` (the player's own taps).
- **Air-time rule:** every fall/jump has ≥ 0.40 s to the next tap (the builder auto-shifts the event into the nearest gap).
- **Objects:** the builder pushes them out until clear by ≥ W/2 + 0.8 + radius at their height band, or drops them (2 dropped: ward_door2, wallpanel3).

## Chart rationale (why the taps are where they are)
- **Intro (0–15.2 s)**: a-cappella "OMG" vocal phrases only (no drums in the stem map): 12 taps on the sung syllable entries, 1–4 s gaps = the "waiting for the call" calm.
- **Verse 1 (15.2–30.3 s)**: finger-snap/clap layer enters with strong hits on step 6 and 14 (the "and" of 2 and 4) — taps on the clap downbeat + those syncopated snaps (s.....s.s.....s.): the first syncopation the player meets.
- **Verse 1b (30.3–45.4 s)**: full UK-garage kick enters (K...|k...|..k.|..kk / ..K.|k.kk|.kk.|K...): taps on the kicks, odd bars use the off-beat kick pair at steps 2/4 and 10/12 = call (even bar) / response (odd bar).
- **Chorus 1 / 2 / Final (45.4, 105.9, 166.4 s)**: halftime groove: kick 1, snare 3, kick on 4; the synth hook (other stem, "O" hits on steps 4/8/14 then 6/10/14) answers between drum hits, so even bars are drum-led and odd bars become a 6-tap 8th-note run (2,6,8,10,12,14) following the hook. Final chorus b adds the extra hook 8th (step 6) for the climax.
- **Verse 2 / 2b / Post**: same garage kick but thinned to 4–5 taps per bar so the vocals breathe; Verse 2b inserts the vocal "V V v v" accent at step 8.
- **Pre (90.8–105.9 s)**: drums drop out, only bass (..B.|..B.|..B.|..B.) + vocal: taps follow the bass pulses at a relaxed 1.9/s while the phone bridge ramps up 6 units; bar 55 is a 7-tap 8th-note build into Chorus 2.
- **Bridge (134.2–149.3 s)**: new trap-style kick pattern (...k|..k.|k.k.|.k.k): taps on steps 3,6,8,13,15 / 3,6,8,10,13 — every bar starts on an off-beat, the hardest syncopation in the level, on a narrow 1.8-wide road inside the library.
- **Break (149.3 s)**: one bar of near silence (2 snare hits + 1 kick): 3 taps, camera to top view.
- **Dance break (151.2–166.4 s)**: four-on-the-floor kick with 8th-note kick fills: long 8th runs (6, 8 and an 11-tap run on bars 86–87) — the densest passage (3.1 taps/s, 4.2/s peak).
- **Outro (196.6–212.3 s)**: drums stop, only the synth stabs remain: 2 taps per bar on the stabs, last tap > 1 s before the end.

## Per-section density (from chart-report.md)

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 病房走廊 | intro | 12 | 0.79 | 1.5/s |
| 15.15 | Verse 1 · 治疗桌与五椅 | verse | 29 | 1.92 | 2.5/s |
| 30.26 | Verse 1b · 墙板外折 | verse | 30 | 1.98 | 3.5/s |
| 45.38 | Chorus 1 · 黑兔舞台 | chorus | 42 | 2.78 | 3.5/s |
| 60.50 | Verse 2 · 玻璃鞋 | verse | 32 | 2.12 | 2.5/s |
| 75.62 | Verse 2b · 双折长短路 | pre | 29 | 1.92 | 3.0/s |
| 90.73 | Pre · 手机桥 | break | 28 | 1.85 | 4.0/s |
| 105.85 | Chorus 2 · 屏幕块 | chorus | 43 | 2.84 | 3.5/s |
| 120.97 | Post · 错列直角 | post | 23 | 1.74 | 2.5/s |
| 134.20 | Bridge · 书页墙与猫 | bridge | 40 | 2.65 | 3.5/s |
| 149.32 | Break · 书页合拢 | break | 3 | 1.59 | 1.5/s |
| 151.21 | Dance break · 舞台五墙 | drop | 47 | 3.11 | 4.5/s |
| 166.32 | Final chorus · 兔耳发夹 | chorus | 43 | 2.84 | 3.5/s |
| 181.44 | Final chorus b · 天桥 | chorus | 44 | 2.91 | 4.0/s |
| 196.56 | Outro · 尾奏琴键 | outro | 14 | 0.89 | 1.5/s |


Sync: every tap is snapped to a real onset of its tagged demucs stem (shifted −25.03 ms) within ±45 ms; spot checks at start / middle / section changes / end are in `chart-report.md` (stem and independent full-mix detector).
