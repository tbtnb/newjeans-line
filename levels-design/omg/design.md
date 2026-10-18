# OMG — 借来的自己（病房 → 身份幻想 → 钢琴尾音）  · level design (worker w2)

Files: `chart.json` (459 taps, schema v2) · `layout.json` (schema v2 + computed `path.nodes`) · `route.png` (top-down check) · `chart-report.md` · `analysis.json` / `analysis-notes.md`.
Art direction follows `codex-ref/` (concept.png, blueprint.png, design.md): cream road `#F3F0E8` with charcoal sides `#25282B`, grey-green ward `#B8C8BC`, fog `#DCE4DA`, pink line `#EFA6B1`, gems `#88C7D5`, crowns `#E3BD60`. The **actual OMG single cover is the black/white halftone black bunny** (not the red bunny the old research claimed) — it appears as the low-poly black bunny on a halftone plinth.

## Concept / grounding
- Song: bouncy R&B / UK-garage with trap and halftime turns (stem maps confirm: garage kick verses, halftime chorus, trap-kick bridge, four-on-the-floor dance break).
- MV: hospital ward, Hanni's phone/Siri identity, Haerin's cat, fairy-tale princess + glass slipper, group performance. "Borrowed self" is a creative reading, not an official one.
- Player fantasy: the line leaves an orderly ward, rides through identities (stage, slipper, phone, book pages with a cat), later dances on bridges above the places it already passed (two real overpasses, computed from the path), and quiets down at the piano tail.

## Core numbers
- Speed 10.0 u/s constant (8th note = 236 ms = 2.36 units ≥ road width + margin, so 8th-note staircases are geometrically clean). Road width 2.2 → 2.0 (Chorus 2) → 1.8 (Bridge) → 2.0 → 1.8 (Final chorus b).
- **Taps: old 213 → new 459 (×2.15)**, 2.16 taps/s average; densest passage Dance break 3.1/s (4.5/s peak 2 s window); **fastest run 11 consecutive 8ths (236 ms) at 162.1–164.4 s**; 15 runs of ≥ 6 eighths. Min gap 226 ms.
- Judgment: perfect ±60 ms, accept ±110 ms (windows of neighbouring 8ths never overlap).
- Levels (y): L0 = 0, chorus stage −4, phone bridge climbs to +4, chorus 2 back to 0, bridge climbs to +6, final chorus 0, outro −2. All crossings of earlier road happen with ≥ 3 units height difference (validator: 0 overlaps).

## Section plan (times = mp3 seconds)
| t | section (chart kind) | route / space | camera | map performance (music-synced) |
|---|---|---|---|---|
| 0–15.2 | Intro · 病房走廊 | closed corridor: long straights + 12 wide turns on the a-cappella "OMG" phrases; door-frame pairs every 3.6 s give scale | `iso`, tight | ceiling light row reacts on beats; doors rise 1.8 s ahead of the line |
| 15.2–30.3 | Verse 1 · 治疗桌与五椅 | **meander** (square-wave R R L L) around the treatment table + five chairs; low walls narrow the space | iso, dist 16 | table & chairs rise on bar 9; snaps at steps 6/14 = first syncopation |
| 30.3–45.4 | Verse 1b · 墙板外折 | staircase widens; five ward wall panels fold outward one by one, then fall away at the chorus | iso | panels rise 1.5 s ahead; exit (fall) at 45 s |
| 45.4–60.5 | Chorus 1 · 黑兔舞台 | **fall −4** onto the open stage level; big diagonal staircase; halftone tiles on the right edge | `high`, dist 21 (≈ +15 %) | black bunny rises with the first hook and bobs on the kick; five stage walls rise on successive half-notes; road reveal = unfold |
| 60.5–75.6 | Verse 2 · 玻璃鞋 | meander again (identity shift), glass slipper plinth on the left | `side` swing on the phrase boundary | slipper rises bar 33; E-egg cat box nearby |
| 75.6–90.7 | Verse 2b · 双折长短路 | staircase, long-short pairs | iso | — |
| 90.7–105.9 | Pre · 手机桥 | **ramp +8** along the phone bridge B1 (cream body under the road, black screen off-road), drums out, bass pulses | `low` chase up the bridge | phone screen unfolds, signal-bar sculpture; 7-tap 8th build at 104 s |
| 105.9–121.0 | Chorus 2 · 屏幕块 | **fall −4** to staggered right-angle road, width 2.0 | `wide` punch then iso | phone-screen blocks lift on the kicks, off-road |
| 121.0–134.2 | Post · 错列直角 | meander | iso | — |
| 134.2–149.3 | Bridge · 书页墙与猫 | **ramp +6**; at 142.7 s it passes **over the Chorus 1 stage (y −4)** — the bunny stage is visible below; compressed angular S between book-page walls, width 1.8, trap kick (all bars start off-beat) | high pitch 62°, dist 15 (narrow road stays readable) | pages unfold in, darker grey-green palette; cat on shelf; E1 cat-ear shadow at 145 s |
| 149.3–151.2 | Break · 书页合拢 | 1 bar, 3 taps | `top` | pages close inward (outside clearance) |
| 151.2–166.4 | Dance break · 舞台五墙 | four-on-the-floor 8th runs at +6; at 153.6 s the route **crosses over the Verse 1b wall-panel staircase (y 0) on an overpass** — the player sees the ward area they left below (callback) | iso, light shake 0.12 | five stage walls flip open on the kick; flash at the downbeat |
| 166.4–181.5 | Final chorus · 兔耳发夹 | **fall −6**; two unequal hairpin-like staircases = bunny ears; ear sculptures rise | `wide` | ears rise bar 88 |
| 181.5–196.6 | Final chorus b · 天桥 | width 1.8, densest hook bars (7 taps) | iso | — |
| 196.6–212.3 | Outro · 尾奏琴键 | small fall −2, meander, three off-road piano keys pressed by the player's taps, halftone end plinth | `high`, dist 24, slow | far layers lower with the piano tail; E2 three dots → three stars |

## Landmarks & eggs
Landmarks: ward doors, treatment table + five chairs, black low-poly bunny on halftone plinth (cover), five stage walls, glass slipper, phone bridge B1 + signal bars, book-page walls + black cat shelf, bunny-ear sculptures, piano keys.
Eggs: **E1** cat-ear shadow formed by the pages during the bridge's long vocal (145 s), the cat turns its head; **E2** three "calling…" dots become three small gold stars at 204 s; **E3** a cardboard-box-with-cat-ears was in v1; replaced by E1 to stay with the codex art. All are off-road, no branch, no extra input.

## Collectibles
10 diamonds at 8.2, 26.8, 59.2, 83.9, 98.9, 121.5, 143.0, 150.7, 197.6, 200.2 s — each on a straight ≥ 0.25 s from any tap, never on a fall/ramp start. Crowns (checkpoints) at 95.1 s (on the phone bridge, breathing room after Verse 2b) and 132.9 s (before the bridge); 3rd crown = finish.

## Readability / fairness
- No tap hints of any kind: no corner markers, no pulses on the road, no countdowns, no guide line. Scenery `react` is only `beat`/`kick` (music, not the next tap) or `tap` (player's actual taps, piano keys).
- Road reveal lead ≥ 1.4 s everywhere (rise 1.8, unfold 1.6, drop 1.4 in the bridge); camera changes start on section downbeats.
- Every object is pushed by the builder until its footprint is ≥ W/2 + 0.8 units from all road at its height band; objects that span the road are under it (`onroad`, y < 0) or start ≥ 4.5 units above it.
- Density progression: intro 0.8/s → verses ~2/s → choruses 2.8/s → dance break 3.1/s; 1–4 s gaps at intro, break (149 s) and outro.
