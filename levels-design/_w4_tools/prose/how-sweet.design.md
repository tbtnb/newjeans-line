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
