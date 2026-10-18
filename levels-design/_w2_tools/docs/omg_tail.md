
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
