
How each section reads (see `route-sections.png`):
- **Intro (0–14.6 s):** long legs (one per choir chord) out of the **cassette start box** (the start platform). The first leg heads north, then the line turns west.
- **Verse 1 (14.6–29 s):** switchbacks that wind **through a cut-away classroom block** (45 wall blocks with doorways where the road passes), then an RRLL corridor heading south. The locker rows react to the player's taps.
- **Chorus 1 (29–43 s):** a Baltimore-club zigzag of staircases that switches diagonal (NE, NW, NE, NW) every 2 bars, ending in the 7-tap kick roll. The giant camcorder sits in the pocket.
- **Post 1 (43–56 s):** staggered short folds (switchbacks) that climb the roof ramp (+3), heading west.
- **Break (56–65 s):** drums cut. The line **falls 7** into the fog onto the snow island: long quiet legs, the deer, crown 1.
- **Verse 2a / Verse 2 (65–86 s):** a corridor meander, then **long switchbacks along the window wall** while the road climbs 6. The window walls unfold in canon.
- **Chorus 2 (86–101 s):** a **ring of staircases** (E, S, W, N) around the rooftop courtyard with the five empty chairs, plus a small cut-away rooftop hut.
- **Post 2 (101–115 s):** **bridge B1** sweeps SW over Chorus 1 and Verse 1 (+6) as one long leg, then a staircase.
- **Bridge (115–129 s):** drumless. A **fall −4**, short switchbacks, then a **square spiral that winds DOWN 8 units around the deer island** (6 same-hand turns; each lap passes ≥ 3 under the previous one). The deer turns its head at the phrase end.
- **Pre (129–142 s):** long viewfinder legs climbing back. The off-road camcorder screen shows **a sixth chair** (E1).
- **Final chorus (142–158 s):** **jump +4** on the pickup, then two unequal return folds and a NW staircase that runs over the snow-break area.
- **Final post (158–172 s):** **jump +3** onto the rim (1.8 wide, the hardest stretch), a zigzag corridor, then a SE staircase crossing over earlier road.
- **Fade / Outro (172–185 s):** **fall −5**, long west legs into the **cassette end box**, which closes after the finish.

## Map performance, camera, scenery
- **Camera:**
  - `low` intro;
  - iso;
  - `high` at Chorus 1;
  - `side` up the roof ramp;
  - `wide` at the snow drop;
  - `low`, then iso;
  - `high` dist 21 round the rooftop ring;
  - `side` along the bridge;
  - `low` → `wide` round the spiral;
  - iso + light shake in the final chorus;
  - `high` on the rim;
  - `close` in the fade;
  - `top` at the end box.
- **Road reveal:** rise / static / unfold / drop / fade, every lead ≥ 1.4 s; fade 2.0 s in the drumless parts.
- **Cut-away buildings** (`classrooms_*`, `rooftop_hut_*`) and **fake-out forks** (`fakefork*` at 18.9, 47.3, 76.6, 134.2, 174.9 s) are visual only. A fork is a slab that seems to continue straight past a real, already-visible corner, then falls away. It never marks timing.
- **Landmarks** are placed into open pockets (`worldPos`):
  - cassette start/end boxes;
  - silver camcorder with flip screen;
  - classroom block with lockers;
  - rooftop empty chairs;
  - deer snow island and the turning deer;
  - bridge B1 truss;
  - halftone bunny relief;
  - warm windows.

## Art assets (`art/`, listed in `layout.art.files`)
| file | use |
|---|---|
| `art/sky.jpg` | `art.backdrop`: misty winter sky, snow specks, far pines, warm glow |
| `art/ground-snow.jpg` | `art.ground` (scale 30): chalk-white snow grain |
| `art/cassette-label.jpg` | flat `image` `cassette_label_start` on the start box (stripes and reels, no text) |
| `art/camcorder-screen.jpg` | upright `image` `cam_screen_e1` (egg E1): the rooftop with **six** chairs, scanlines, REC dot |
| `art/deer-decal.png` | billboard `deer_sticker` on the snow island (transparent silhouette) |
| `art/halftone-bunny-relief.jpg` | upright `image` `bunny_relief` in the final chorus (cover motif, wall relief) |

The art is procedural PIL (`_w2_tools/artgen.py`), in the level palette, with no faces, text or arrows. GenerateImage output could not be saved on the box.

## Eggs, collectibles, fairness
- **Eggs:**
  - **E1** (≈ 133–136 s): an off-road camcorder screen shows a *sixth* chair that is not on the real rooftop.
  - **E2**: a white wristband on the camcorder strap (a nod to the cast arm), around 34 s.

  Both are off-road and need no branch or extra input.
- **Diamonds (10):** 8.8, 23.9, 45.5, 58.2, 81.3, 110.0, 120.4, 136.6, 160.9, 175.4 s.
- **Crowns:** 59.8 s (snow break) and 126.6 s (end of the drumless bridge). The finish is the 3rd.
- **No hints:** no markers, no pulses, no countdowns, no guide lines. The locker rows react only to the player's real taps; everything else reacts to beat/kick.
- **Air-time rule:** every fall/jump has ≥ 0.40 s before the next tap. The builder shifted the bridge fall to 114.78 s, the final-chorus jump to the pickup at 140.94 s and the rim jump to 159.76 s.
