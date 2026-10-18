# Ditto — 冬日录像带（Winter Videotape）· level design (worker w2, v3)

Files: `chart.json` (412 taps) · `layout.json` (v2.5 + `path.nodes`) · `route.png` · `route-sections.png` · `chart-report.md` · `analysis.json` / `analysis-notes.md` · `art/` (6 images).
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
- **Taps: old 181 → new 412 (×2.28)**, averaging 2.22/s. The re-audit removed 6 faint taps; 2 taps were dropped inside jump flights (142.03, 158.24 s) so the jumps stay on the final-chorus downbeats.
- **Difficulty (hard tier, title track):** avg CPM 133 (taps ÷ length) / 186 wiki-style. **Peak CPM 360** (validator style) and 545 instantaneous (min gap 110 ms). 7 bursts of 3–4 real 16ths (hat/snare/kick fills, all audible in the full mix and starting or ending on a beat) at 28.0, 74.4, 114.0, 140.9, 142.7, 152.6 and 167.8 s, i.e. Chorus 1 fill, Verse 2 fill, bridge entry, final-chorus entry and fills, Final post. Charting rules (user override): one audible layer per section, the same pattern on every repeat of a phrase, bursts only where the 16th figure is audible in the full mix and starts or ends on a beat, breaks stay sparse, no taps on faint or ghost onsets. CPM numbers are references, not quotas. See the per-section 'What the taps follow' table in `chart-report.md`.
- **Fastest run:** 7 consecutive 8ths (224 ms) at 41.3–42.6 s, the Jersey kick roll. The validator counts 8 taps with gaps ≤ 0.30 s at 40.97–42.62 s. Minimum 8th gap 222 ms; bursts go down to 110 ms.
- **Judgment:** the engine rule (v2.5, per tap) gives min ±49 ms (inside bursts) and median ±106 ms, always ≤ half the local gap.
- **Levels:** 0 → ramp +3 (Post 1 roof) → **fall −7** (snow island, −4) → ramp +6 (Verse 2, +2) → ramp +4 (bridge B1, +6) → **fall −4** (+2) → **spiral ramp −8 round the deer** (−6) → ramp +4 (−2) → **jump +4** onto the memory courtyard (+2, on the pickup at 140.9 s) → **jump +3** onto the rim (+5, 159.8 s) → **fall −5** (fade, 0).
- **Checks:** the validator reports 0 same-level overlaps. The longest same-direction run is 6 (the descending spiral).

## Route choreography (each section has its own texture)
The planner is the same as OMG's: a beam search over per-section motifs and drift bearings with the exact v2.4 overlap rule. The table is computed from the built path.
| Section | Route texture (planner motifs) | taps | max same-dir run | U-turns | height | over/under-passes |
|---|---|---|---|---|---|---|
| Intro · 录像带入口 (0.0s) | long sweeping legs → 0°, long sweeping legs → 270° | 14 | 2 | 3 | +0..+0 | 5 |
| Verse 1 · 教室走廊 (14.6s) | switchbacks → 90°, zigzag corridor (RRLL) → 180° | 37 | 2 | 15 | +0..+0 | 18 |
| Chorus 1 · 摄像机取景框 (29.0s) | staircase → 45°, staircase → 315°, staircase → 45°, staircase → 315° | 41 | 2 | 3 | +0..+0 | 0 |
| Post 1 · 屋顶坡道 (43.3s) | switchbacks → 270° | 32 | 3 | 8 | +0..+3 | 3 |
| Break · 雪地鹿岛 (55.8s) | long sweeping legs → 180° | 8 | 2 | 3 | -4..+3 | 6 |
| Verse 2a · 雾隙 (64.8s) | zigzag corridor (RRLL) → 90° | 13 | 2 | 5 | -4..-4 | 13 |
| Verse 2 · 窗墙长 U (72.0s) | switchbacks → 0° | 32 | 5 | 17 | -4..+2 | 8 |
| Chorus 2 · 屋顶空椅 (86.3s) | staircase → 90°, staircase → 180°, staircase → 270°, staircase → 0° | 44 | 2 | 3 | +2..+2 | 14 |
| Post 2 · 跨空桥 (100.6s) | long sweeping legs → 225°, staircase → 225° | 35 | 3 | 12 | +2..+6 | 34 |
| Bridge · 鹿回头 (114.9s) | switchbacks → 135°, spiral / wrap L, staircase → 90° | 22 | 6 | 7 | -6..+2 | 5 |
| Pre · 取景屏 (129.3s) | long sweeping legs → 270° | 22 | 2 | 2 | -6..-2 | 17 |
| Final chorus · 记忆庭院 (141.8s) | switchbacks → 0°, staircase → 300° | 56 | 5 | 16 | -2..+2 | 44 |
| Final post · 网点兔 (157.9s) | zigzag corridor (RRLL) → 60°, staircase → 150° | 43 | 2 | 11 | +5..+5 | 40 |
| Fade · 暖窗熄灭 (172.3s) | long sweeping legs → 270° | 11 | 2 | 3 | +0..+5 | 1 |
| Outro · 录像带合上 (179.4s) | long sweeping legs → 270° | 2 | 1 | 0 | +0..+0 | 2 |

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

## Chart rationale (why the taps are where they are)
- **Intro (0–14.6 s)**: choir/pad only: 2 taps per bar on the chord changes (beats 1 and 3) — 1 s+ gaps, the camcorder room.
- **Verse 1 (14.6–29.0 s)**: busy Baltimore hat/snare layer (S at steps 0, 5-6, 11, 14): taps on those snare accents (0,6,11,14) → syncopated, with bar 15 an 8-tap 8th fill into the chorus.
- **Chorus 1 (29.0–43.3 s)**: the iconic jersey-club kick K...|K...|K..K|..K. charted exactly (0,4,8,11,14); bars 20 and 23 add the kick-roll 8ths (7-tap runs).
- **Post 1 (43.3–55.8 s)**: snare-led 16th groove: taps on the loud snares (0,4,6,9,12,14 / 0,4,8,12,14) — 3–3.4 taps/s while the road climbs the bleachers.
- **Break & Verse 2a (55.8–72.0 s)**: drums cut out: taps follow the sung syllables (vocal stem onsets, ≥ 1 beat apart), then the light claps on 2 and 4 return — the breathing room (≈1 tap/s).
- **Verse 2 / Chorus 2 / Post 2 (72.0–114.9 s)**: full Baltimore beat: 3+3+2+3+3+2 sixteenth pattern (steps 0,3,6,8,11,14) following kick+snare, alternating with lighter 3–4-tap bars every other bar so phrases breathe; 7-tap 8th roll at 98.8 s.
- **Bridge & Pre (114.9–141.8 s)**: drumless vocal bridge, then claps on 2/4 with the vocal line — low density before the finale.
- **Final chorus / post (141.8–172.3 s)**: tresillo pattern + 8th-note kick rolls every 4th bar on a 1.8-wide road — hardest part.
- **Fade & outro (172.3–185.5 s)**: beat thins and fades: 5→2 taps per bar, last taps on the final snare hits.

## Per-section density (from chart-report.md)

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 录像带入口 | intro | 14 | 0.96 | 1.5/s |
| 14.64 | Verse 1 · 教室走廊 | verse | 37 | 2.58 | 4.5/s |
| 28.97 | Chorus 1 · 摄像机取景框 | chorus | 41 | 2.86 | 4.0/s |
| 43.30 | Post 1 · 屋顶坡道 | post | 32 | 2.55 | 3.0/s |
| 55.83 | Break · 雪地鹿岛 | break | 8 | 0.89 | 1.5/s |
| 64.79 | Verse 2a · 雾隙 | verse | 13 | 1.81 | 2.5/s |
| 71.95 | Verse 2 · 窗墙长 U | verse | 32 | 2.23 | 3.5/s |
| 86.28 | Chorus 2 · 屋顶空椅 | chorus | 44 | 3.07 | 4.0/s |
| 100.61 | Post 2 · 跨空桥 | post | 35 | 2.44 | 3.5/s |
| 114.94 | Bridge · 鹿回头 | bridge | 22 | 1.54 | 2.5/s |
| 129.27 | Pre · 取景屏 | pre | 22 | 1.75 | 3.5/s |
| 141.80 | Final chorus · 记忆庭院 | chorus | 56 | 3.47 | 5.0/s |
| 157.92 | Final post · 网点兔 | chorus | 43 | 3.00 | 4.5/s |
| 172.25 | Fade · 暖窗熄灭 | outro | 11 | 1.54 | 2.0/s |
| 179.41 | Outro · 录像带合上 | outro | 2 | 0.33 | 1.0/s |


Sync: every tap is snapped to a real onset of its tagged demucs stem (shifted −25.03 ms) within ±45 ms; spot checks at start / middle / section changes / end are in `chart-report.md` (stem and independent full-mix detector).
