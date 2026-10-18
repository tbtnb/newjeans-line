# How Sweet — level design (worker 4)

**Concept: "A summer afternoon across a railway town, from the record shop and back."** The line leaves a street of small shops and climbs a teal footbridge to a rail plaza with a white commuter train and yellow level-crossing gantries. It crosses rooftop terraces and a long narrow laundry bridge, winds a helix up a water tower, and drops into a rooftop-garden finale before ending at the record shop. Palette (from the codex blueprint): cream `#F2EFE4`, charcoal `#292D32`, signal orange `#FF5B24`, sage `#A9C9B6`, teal `#507F83`, mustard `#E9BC48`, mint `#75E1D0`. Diamonds are mint, crowns mustard.

**Codex alignment** (`/workspace/nj-refs/how-sweet/concept.png` + design.md), used as a loose reference only:
- Kept: the teal footbridge rising L0→L1→L2, the white train on a lower track, the yellow gantries, the five B/W panels + orange panel, cat-balcony egg E1 and the rooftop garden.
- Changed: the route itself is our own and far denser. The blueprint's single plaza loop became a three-sided plaza loop, a water-tower helix, an expanding spiral and a rooftop loop with an overpass.
- Changed: crowns sit at 106 s / 146 s (49% / 67%), close to the blueprint's 38% / 68%.

## Route choreography (distinct texture per section)

| section | time | route texture | height | camera | scene / performance |
|---|---|---|---|---|---|
| Intro | 0.3–8.0 | **wide staircase** | 0 | close | flat charcoal frame decal under the start (cover border) sinks away at 8.0 s; NJ letters |
| Verse 1 | 8.0–23.4 | **serpentine corridor** (turns only after rests): long sweeps between shopfronts with 8th-pair wiggles | 0 | iso | shops and apartments rise in on the beat; **cat-balcony EGG E1** at 16.5 s; fake-out fork 20.0 s |
| Verse 1b | 23.4–38.7 | **lightning bolt** (alternating 1- and 2-bar legs) | 0 | iso | apple EGG (19.96 s) on a shop shelf just before this leg |
| Pre-chorus 1 | 38.7–46.4 | **staircase climbing +3** up the teal footbridge, with low railings both sides | 0 → 3 | low | |
| Chorus 1 | 46.4–61.8 | **three-sided plaza loop** (3 same-side turns, 2–3-bar legs) around the rail plaza | 3 | **high** | white train on the lower track pulses with the beat; six yellow gantries unfold; green rooftop court under the loop |
| Chorus 1b | 61.8–77.1 | **tight zigzag** (2 + 2 turns) | 3 | iso | barcode digits decal; five B/W panels + orange panel stand in the plaza |
| Verse 2 | 77.1–92.5 | **switchbacks** along the terrace wall, then the route **turns back west and climbs over the Verse-1 street** (loop-back over an earlier section) | 3 → 4 | iso | fork 84.8 s; floating **"How Sweet" sticker** (art) over the roofs |
| Verse 2b | 92.5–107.9 | **serpentine with every-2nd-tap turns**, climbing to L2 (+7) right above the Verse-1 roads | 4 → 7 | iso | |
| Chorus 2 | 107.9–123.2 | **plaza loop II** (3-turn orbit) high above the old street | 7 | side | the six panels rise one per half-bar on the music clock |
| Chorus 2b | 123.2–138.6 | **lightning bolt** | 7 | iso | panels poster (art) on a courtyard wall; fork 127.8 s |
| Bridge | 138.6–153.9 | **narrow laundry bridge**: switchbacks gliding down −4 between laundry poles on both sides, passing over the start street | 7 → 3 | low | crown 2 at 146.1 |
| Build | 153.9–169.3 | **square helix climbing +6 around the water tower** (4–5 same-side turns, laps pass over each other) | 3 → 9 | iso | water tower anchored in the clear centre of the helix |
| Final chorus | 169.3–184.7 | **fall −6** at 169.35 s onto the plaza, then an **expanding spiral** | 3 | iso | densest section (Chorus-1 tap pattern) |
| Final chorus b | 184.7–200.0 | **rooftop-garden loop** climbing +3 and **passing over the spiral** | 3 → 6 | **high** | cat silhouette returns on a far rooftop (EGG E1); fork 189.9 s |
| Outro | 200.0–219.1 | long **turn-out** glide to the record shop | 6 | wide | the shop sign flips CLOSED→OPEN on the last chord; outfit-rail EGG |

**Multi-level structure:** 73 over/under crossings (validator count: ≥ 3 height difference, ≥ 1.5 s apart). Verse 2 turns back and climbs over Verse 1. Chorus 2 runs at +7 above the old street. The bridge, build helix and final-chorus loops all stack over the intro/verse-1 district at different heights. There are no same-level overlaps, and the fall lands 0.67 s before the next tap.

## Landmarks and eggs
- **Landmarks**: rail plaza (train + gantries), the six panels, water tower (inside the build helix), "How Sweet" sticker, record shop (finish).
- **Eggs**: E1 orange cat on a balcony (returns as a rooftop silhouette); an apple with one bite on a shop shelf; five small outfits on a clothes rail; barcode decal digits.
- No real people are shown. The "members" appear only as five outfits on hangers and five abstract panels.

## Fake-out forks
Visual-only dead-end stubs at 20.0, 84.8, 127.8 and 189.9 s. They are revealed together with the road, so they carry no timing information.

## Art (under `art/`)
| file | use | generated-art prompt (GenerateImage asset) |
|---|---|---|
| `art/sky-summer.jpg` | `art.backdrop` | sage-to-cream summer sky with soft clouds (asset `c69229d1…jpg`) |
| `art/plaza-ground.jpg` | `art.ground` (scale 40) | cream plaza paving tiles with teal/orange flecks (asset `af1fd7d3…jpg`) |
| `art/panels-poster.jpg` | billboard image, chorus 2b | five black/white geometric panels + one orange (asset `dd5f29ad…jpg`) |
| `art/sticker.png` | floating billboard sticker, verse 2 | orange cut-corner "HOW SWEET" label (asset `8d0f3ef7…jpg`) |

The GenerateImage outputs were stored outside this box. The committed files are procedural stand-ins from `_w4_tools/art.py`, with the same names and motifs. Swap them in 1:1.

## No tap hints
All events follow the music clock: beats, half-bars and section downbeats. Nothing marks a corner.

## Chart summary
**307 taps** (legacy v1 count in chart-report.md). This is the rhythmic-logic audit of the curated 295-tap chart: drum layer (kick + clap) in every non-intro/outro section, and chorus/verse instances share one pattern bar for bar where it is audible. There are **four 16th fills (5 taps, 0.12 s gaps)**, each at a phrase end where the full mix has a prominent 16th hat/snare figure: 38.26 (into pre-chorus), 45.94 (into Chorus 1), 153.46 (into the build) and 161.14 (build phrase end). Peak 500 CPM with a ±54 ms window. See chart-report.md.

## Generated facts (from layout.json / chart.json)

- Road width {'width': [{'t': 0, 'w': 2.6}, {'t': 8.02, 'w': 2.2}, {'t': 46.42, 'w': 2.4}, {'t': 77.14, 'w': 2.1}, {'t': 107.86, 'w': 2.2}, {'t': 138.58, 'w': 2.0}, {'t': 169.3, 'w': 1.9}, {'t': 200.0, 'w': 2.6}], 'height': 0.6, 'reveal': [{'t': 0, 'mode': 'static', 'lead': 3.0}, {'t': 8.02, 'mode': 'rise', 'lead': 2.0}, {'t': 46.42, 'mode': 'unfold', 'lead': 1.6}, {'t': 77.14, 'mode': 'rise', 'lead': 1.8}, {'t': 138.58, 'mode': 'drop', 'lead': 1.8}, {'t': 153.94, 'mode': 'rise', 'lead': 1.4}, {'t': 169.3, 'mode': 'rise', 'lead': 1.4}, {'t': 200.0, 'mode': 'static', 'lead': 3.0}]}; start heading N; speed [{'t': 0, 'v': 9.0}]
- Elevation: ramp +3 @ 38.74–46.120000000000005 (pre-chorus: the teal footbridge staircase climbs from street level L0 to the rail plaza L1); ramp +4 @ 84.82–99.88000000000001 (verse 2 second half: rooftop terraces climb to L2 (+7)); ramp -4 @ 138.58–153.64 (bridge: long narrow laundry bridge glides back down to L1); ramp +6 @ 153.94–169.0 (build: climb around the water tower); fall -6 @ 169.345 (final-chorus downbeat: drop off the tower onto the plaza); ramp +3 @ 184.66–192.04 (final chorus 2nd half: rooftop-garden loop climbs and passes over the earlier roads)
- Camera: 0s close; 8.02s iso; 38.74s low; 46.42s high; 61.78s iso; 77.14s iso; 92.5s iso; 107.86s side; 123.2s iso; 138.58s low; 153.94s iso; 169.3s iso; 169.9s iso; 184.66s high; 200.0s wide
- Diamonds (t): 4.899, 24.339, 41.978, 58.298, 83.977, 101.497, 119.737, 146.136, 162.936, 195.215; crowns (checkpoints): 106.297, 146.136
- Landmarks: `court` (green rooftop sports court under the chorus route (big colour field, white lines)); `sticker` (giant cut-corner orange "How Sweet" sticker floating over the rooftops (cover sticker, generated art)); `record_shop` (finish: the record shop; its flip sign turns from CLOSED to OPEN as the line arrives (EGG: new beginning)); `train` (white commuter train on the lower track beside the rail plaza (MV level crossing)); `panel5` (five black/white standing panels + the orange sleeve panel (abstracted group cover); they rise one by one in chorus 2 and line up again in the final chorus); `water_tower` (water tower: the build-section helix winds around it)
- Easter eggs: `apple_egg` (EGG: an apple with one small bite on a shop shelf); `barcode_digits` (5 220722 221029); `members5` (EGG: five small denim/green/black outfits on a clothes rail outside the shop (cover outfits)); `cat_egg` (EGG E1: orange cat on an apartment balcony; it turns its head with the syncopated claps; the same cat silhouette reappears in the final chorus skyline); `cat_egg2` (EGG E1 return: cat silhouette on a far rooftop)
- Fake-out forks (visual only, road-coloured dead-end stubs that rise 2 s early and sink after the corner; they are revealed together with the road (same lead), so they add no timing information and only fake a straight continuation): fork0, fork1, fork3
- Objects: 80 total; events: 17
- Art wired into layout: backdrop `art/sky-summer.jpg`, ground `art/plaza-ground.jpg`, images/textures `art/panels-poster.jpg`, `art/sticker.png`
