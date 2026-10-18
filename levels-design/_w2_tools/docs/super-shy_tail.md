
How each section reads (see `route-sections.png`):
- **Intro (0–13.2 s):** a long straight past the red bike and bench (A, with a flat red-bike sticker), then short switchbacks on the synth stabs.
- **Verse 1 (13.2–38.8 s):** a tight RRLL zigzag corridor through **cut-away courtyard walls** (`courtyard_walls_*`, openings wherever the road passes), a staircase, switchbacks along the wall, then a same-hand **square spiral up round the green courtyard (B)** to +3.
- **Chorus 1 (38.8–64.4 s):** on +3, four staircases in different bearings (W, S, E, N) under ten parasols that open on the kick; a 4-tap hat burst lands on the fill into the break.
- **Break (64.4–70.8 s):** drums out; **fall −3** into the sunken fountain plaza and one sweeping S on the vocal syllables. The first crown waits here.
- **Build (70.8–77.2 s):** a left-hand **spiral up the Lisbon stairway** (+6 in 5.4 s, laps stacked ≥ 3 apart); a 3-tap hat burst on the build's last beat.
- **Verse 2 (77.2–102.8 s):** on the +6 market terrace: switchbacks under coral awnings, an RRLL corridor that **wraps through the market arcade** (`market_arcade_*`), a staircase, more switchbacks. Most over/under-passes of the song happen here, against the lower plaza and stairway. **E1** (white pixel bunny tile) lies under the market bench.
- **Break 2 (102.8–106 s):** step down to the viewpoint, a straight with the whole town spread out below.
- **Verse 3 (106–115.6 s):** a long downhill staircase back to L0, crossing under the earlier terrace.
- **Final chorus (115.6–128.4 s):** **jump onto Bridge B** (+3) over the five-dancer plaza (C: five abstract sculptures, no faces); two crossing staircases. The E1 tile flips once here to show five colour squares.
- **Final chorus b (128.4–141.2 s):** staircases and an RRLL corridor climbing +3 past the **teal stepped wall with the five-colour pixel relief (E)**; snare and hat bursts at 126.4 and 137.6 s.
- **Final chorus c (141.2–end):** **big fall −6** to the bus street, staircase, switchbacks on the 8th-note kick rolls (four 6-tap runs plus two bursts), then a calm straight to the gate.

## Map performance, camera, scenery
- **Camera:** low at the start; iso through the alleys; high on the courtyard spiral; wide at Chorus 1 and the break; side on the stairway; iso on the terrace; wide (dist 34) at the viewpoint; high with a small shake at the final chorus; wide, then close, then a slow high pull-back at the end. The camera turns only on downbeats or long straights.
- **Road reveal:** rise (1.6 s) → unfold at Chorus 1 (1.4 s) → fade into the plaza (2.0 s) → rise on the stairway (1.4 s) → drop at the final chorus (1.3 s).
- **Fake-out forks** (`fakefork*` at 10.9, 49.1, 124.3 s; the other planned forks were dropped because the slab would have hit road): the slab seems to continue straight past a visible corner and then falls away. Visual only; they never mark timing.
- **Landmarks** (placed into open pockets, `worldPos`): A bike + bench, B green courtyard, sunken fountain, D market arcade (columns, striped canopy, five flags), viewpoint town (far below), C five dancers, E stepped relief wall, colour-window bus.

## Art assets (`art/`, listed in `layout.art.files`)
| file | use |
|---|---|
| `art/sky.jpg` | `art.backdrop`: Lisbon afternoon sky with soft clouds |
| `art/ground-park.jpg` | `art.ground` (scale 34): park green with paving dots |
| `art/awning-stripes.jpg` | upright `image` awnings along Verse 2 and the market-arcade canopy texture |
| `art/pixel-relief.jpg` | `parts[].texture` on the relief wall (landmark E) |
| `art/red-bike-decal.png` | flat `image` sticker next to landmark A |
| `art/bunny-tile.jpg` | `parts[].texture` of egg E1 |

The art is procedural PIL (`_w2_tools/artgen.py`) in the codex palette; the image-generation tool's outputs were not saved on the box. No people or faces are depicted.

## Eggs, collectibles, fairness
- **Eggs:** **E1** white pixel bunny tile under the market bench (≈ 92 s), which spins/flips once at the final-chorus entry to show five colour squares. **E2** a bicycle bell near the bus that wobbles silently on the player's taps (≈ 149 s). Both are off-road.
- **Diamonds (10):** 5.0, 22.6, 47.8, 67.3, 74.6, 86.4, 104.3, 112.4, 124.6, 127.8 s.
- **Crowns:** 66.0 s (fountain plaza, Break) and 109.0 s (Verse 3 downhill). Codex asks for 3 crowns; the schema allows exactly 2, so the finish gate is the 3rd.
- **No tap hints:** no markers, no countdowns, no guide lines. The awning `light` events follow half-notes, not the next turn.
- **Air-time:** falls/jumps sit in gaps with ≥ 0.40 s before the next tap (103.0, 114.96, 139.96 s).
