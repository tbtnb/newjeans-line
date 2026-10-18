
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
