# Super Shy — 把心事跳成一座城 · Lisbon afternoon · level design (worker w2, v3/v4)

Files: `chart.json` · `layout.json` (v2.4 + `path.nodes`) · `route.png` · `route-sections.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (6 images).
**Aligned with codex-ref** (`/workspace/nj-refs/super-shy/`): a blue line hops through a pastel Lisbon-style hill town on a sunny afternoon, the shy feeling turned into a whole city. The blueprint is mood only; the route choreography is ours.

## Concept
- **Song:** the Get Up title track, 2:35, a skippy jersey-club / drum-and-bass-lite beat at 150 BPM. Shy crush, light, bouncy, a little breathless.
- **Level:**
  - the line passes the red bike and bench (A);
  - it zigzags through cobbled alleys and cut-away courtyard walls;
  - it spirals up round the green courtyard (B) to +3 for Chorus 1 under parasols;
  - it drops into the sunken fountain plaza, then spirals up the Lisbon stairway to the +6 market terrace;
  - it wraps through the coral market arcade (D), where the E1 bunny tile sits under a bench;
  - it steps down to the viewpoint and runs downhill to L0;
  - it jumps onto Bridge B over the five-dancer plaza (C), climbs past the teal stepped wall with the five-colour pixel relief (E), then drops to the bus street for the finish.
- **Palette** (codex-ref):

  | use | colour |
  |---|---|
  | sky | `#CDEDF1` |
  | park / ground | `#BEE9C9` |
  | road | `#FFF8ED` |
  | road side wall | `#3B8A89` |
  | player line | `#295BE7` |
  | market roofs / sunlit walls | `#F4A39B` |
  | annotations | `#B1A6E8` |
  | diamonds | `#FF82D0` |
  | crown | `#F7CE63` |

## Core numbers
- **Speed and width:** 11.0 u/s. Width 2.0 → 1.9 (Chorus 1) → 1.8 (Verse 2) → 1.9 (final chorus) → 1.7 (final chorus b).
- **Taps: old 176 → new 396 (×2.25)**, 2.56 taps/s. Avg CPM 154 (taps ÷ length), 192 wiki-style; **peak CPM 395** (min gap 152 ms). 11 fast bursts at fills, build-up and final choruses; 96 dotted-8th gaps. Full comparison with the original levels is in `chart-report.md`.
- **Fastest 8th run:** 6 × 200 ms at 137.1 s; fastest burst 4 taps at 137.56 s (395 CPM).
- **Judgment:** the engine rule (v2.4) gives min ±68 ms (inside bursts) and median ±110 ms, i.e. ≤ half the local minimum gap everywhere.
- **Levels** (codex L0 / +3W / +6W = 0 / +3 / +6): spiral ramp +3 round courtyard B (32.7–38.1 s) → fall −3 into the fountain plaza (64.4 s) → stairway spiral +6 (71.1–76.5 s) → fall −3 to the viewpoint (103.0 s) → downhill ramp −3 (106.3–114.6 s) → jump +3 onto Bridge B (115.0 s) → ramp +3 past the relief wall (128.7–133.2 s) → big fall −6 to the bus street (140.0 s).
- **Checks:** the validator reports 0 same-level overlaps.

## Route choreography (each section has its own texture)
Planner: beam search over per-section motifs plus a drift bearing, using the exact v2.4 overlap rule. The table is computed from the built path.
| Section | Route texture (planner motifs) | taps | max same-dir run | U-turns | height | over/under-passes |
|---|---|---|---|---|---|---|
| Intro · 薄荷街角 (0.0s) | long sweeping legs → 0°, switchbacks → 90° | 13 | 2 | 3 | +0..+0 | 3 |
| Verse 1 · 石砖小巷 (13.2s) | zigzag corridor (RRLL) → 45°, staircase → 0°, switchbacks → 90°, spiral / wrap R | 61 | 5 | 25 | +0..+3 | 0 |
| Chorus 1 · 公园遮阳伞 (38.8s) | staircase → 270°, staircase → 180°, staircase → 90°, zigzag corridor (RRLL) → 0° | 79 | 2 | 12 | +3..+3 | 0 |
| Break · 下沉喷泉广场 (64.4s) | long sweeping legs | 8 | 3 | 3 | +0..+3 | 3 |
| Build · 里斯本阶梯 (70.8s) | spiral / wrap L | 16 | 5 | 7 | +0..+6 | 4 |
| Verse 2 · 市场拱廊 (77.2s) | switchbacks → 45°, zigzag corridor (RRLL) → 135°, staircase → 180°, switchbacks → 270° | 64 | 6 | 23 | +6..+6 | 23 |
| Break 2 · 观景台 (102.8s) | long sweeping legs | 5 | 2 | 2 | +3..+6 | 0 |
| Verse 3 · 下坡 (106.0s) | staircase → 225° | 22 | 3 | 5 | +1..+3 | 10 |
| Final chorus · 五人广场 (115.6s) | staircase → 90°, staircase → 0° | 37 | 2 | 1 | +3..+3 | 0 |
| Final chorus b · 像素浮雕墙 (128.4s) | staircase → 315°, staircase → 45°, zigzag corridor (RRLL) → 270° | 45 | 3 | 15 | +0..+6 | 32 |
| Final chorus c · 巴士街 (141.2s) | staircase → 180°, switchbacks → 90°, long sweeping legs | 46 | 6 | 23 | +0..+0 | 21 |

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

## Chart rationale (why the taps are where they are)
- **Intro (0–13.2 s)**: drums + synth before the vocals: taps on the kick on beat 2 and the "and" of 3 (steps 4,10), 1–2 per bar; bar 7 previews the verse groove.
- **Verse 1 / 2 / 3**: skippy broken-beat kick on steps 4,7,10,14 (3+3+4 sixteenths = 300/300/400 ms): the signature "shy" bounce, alternated with 2-tap bars so the vocal phrases breathe; phrase-end bars add a kick/snare 8th fill.
- **Chorus 1 / Final**: jersey-style kick 0,4,8,11,14 under "I'm super shy, super shy"; the 4th bar of each phrase is an 8th-note kick roll (6–7 taps at 200 ms). Final chorus c alternates 5-tap and 7-tap bars (hardest).
- **Break / Break 2**: drums cut: taps on vocal syllables ≥ 1 beat apart (0.4 s+), the breathing room before the stair climb.
- **Build (70.8–77.2 s)**: kick on 2 and 4 returning, densifying to an 8th run — synced with the road ramping up the Lisbon stairway.

## Per-section density (from chart-report.md)

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 薄荷街角 | intro | 13 | 0.99 | 2.5/s |
| 13.16 | Verse 1 · 石砖小巷 | verse | 61 | 2.38 | 3.5/s |
| 38.76 | Chorus 1 · 公园遮阳伞 | chorus | 79 | 3.09 | 4.0/s |
| 64.36 | Break · 下沉喷泉广场 | break | 8 | 1.25 | 2.0/s |
| 70.76 | Build · 里斯本阶梯 | pre | 16 | 2.50 | 3.5/s |
| 77.16 | Verse 2 · 市场拱廊 | verse | 64 | 2.50 | 4.0/s |
| 102.76 | Break 2 · 观景台 | break | 5 | 1.56 | 2.0/s |
| 105.96 | Verse 3 · 下坡 | verse | 22 | 2.29 | 3.5/s |
| 115.56 | Final chorus · 五人广场 | chorus | 37 | 2.89 | 4.0/s |
| 128.36 | Final chorus b · 像素浮雕墙 | chorus | 45 | 3.52 | 4.5/s |
| 141.16 | Final chorus c · 巴士街 | chorus | 46 | 3.40 | 5.0/s |


Sync: every tap is snapped to a real onset of its tagged demucs stem (shifted −25.03 ms) within ±45 ms; spot checks at start / middle / section changes / end are in `chart-report.md` (stem and independent full-mix detector).
