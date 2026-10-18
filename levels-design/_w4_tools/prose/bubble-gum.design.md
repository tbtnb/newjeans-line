# Bubble Gum — level design (worker 4)

**Concept: "An island-hopping beach day."** Boardwalks and wooden piers link small islands across a turquoise sea. The line passes a greenhouse, spirals up around a giant shell, hops across floating bubble pads during the breakdown, climbs a pier over its own earlier road and ends at a picnic table at sunset. Palette: sea `#5fd8d2`, bubble pink `#ffb8d6`, coral, mint `#bfe8d2`, sand, navy silhouettes `#1d3260`, accent orange `#f07a2a`. Diamonds aqua `#4fd0e8`, crowns gold.

**Codex alignment** (`/workspace/nj-refs/bubble-gum/concept.png`), used as a loose reference:
- Kept: turquoise sea islands, boardwalk bridges, dark rocks, the folding screen with five featureless paper cut-out silhouettes plus an orange panel, the camper van, the giant shell, the bubble wand and floating bubbles.
- The route is our own. Tier: **moderate**, so it has the calmest chart of the four, but the route still has distinct textures per section.
- No faces are shown. The silhouettes are blank cut-outs.

## Route choreography

| section | time | route texture | height | camera | scene / performance |
|---|---|---|---|---|---|
| Intro | 2.1–18.1 | **wide staircase** along the beach | 0 | side | three slow bubbles; lighthouse on the breakwater; rocks in the shallows |
| Verse 1 | 18.1–36.3 | **serpentine boardwalk** (turns after rests), then a **zigzag** | 0 | iso | planks beside the road dip on the player's own taps (feedback only); silhouette screen (art) at 28 s; fork 30.1 s |
| Pre-chorus 1 | 36.3–56.9 | **staircase** between white greenhouse posts; paper-boat EGG on a sill | 0 | low → wide | fork 48.3 s |
| Chorus 1 | 56.9–79.8 | **square helix climbing +5 around the giant shell island** (4–5 same-side turns, laps cross over each other) | 0 → 5 | **high** | confetti burst on the downbeat; bubble-wand EGG; balloons rise beside the road; beach stair blocks |
| Breakdown | 79.8–91.2 | **jump +3** (80.4 s) onto floating bubble pads, then a slow **spiral**; vocal-only taps, sparse | 8 | **top** | giant bubble-gum bubble hangs ahead and **pops at 91.19 s** when the drums return |
| Verse 2 | 91.2–118.6 | **fall −6** (91.8 s) to the grass island, then **switchbacks** and a **serpentine** | 2 | iso | camper van; trees and picnic blankets; marbles EGG; fork 111.8 s |
| Pre-chorus 2 | 118.6–136.9 | **zigzag → staircase** | 2 | low | crown 2 at 131.2 |
| Chorus 2 | 136.9–150.6 | **pier loop climbing +3 over the Verse-2 road** (3-turn orbit) | 2 → 5 | side | second silhouette screen on the pier |
| Chorus 2b | 150.6–164.3 | **lightning bolt** | 5 | iso | fork 150.0 s |
| Final chorus | 164.3–178.0 | **fall −5** (165.0 s) onto the sunset beach, then an **expanding spiral** | 0 | iso | sky turns sunset orange |
| Final chorus b | 178.0–191.8 | **sunset-pier loop climbing +3 and passing over the spiral** | 0 → 3 | **high** | |
| Outro | 191.8–200.3 | long glide to the picnic table | 3 | wide | the lamp switches on; the last bubble drifts away; the paper boat floats on the water |

There are no same-level overlaps. Every jump or fall lands ≥ 1.09 s before the next tap.

## Landmarks and eggs
- **Landmarks**: lighthouse (start, seen again at the end), giant shell (inside the Chorus-1 helix), giant bubble, camper van, silhouette screens, picnic finish.
- **Eggs**: five glass marbles, one reflecting a bunny-ear cloud; the paper boat (a sill in pre-chorus 1, on the water in the outro); the bubble wand.

## Fake-out forks
Visual-only dead-end stubs at 30.1, 48.3, 111.8 and 150.0 s, revealed together with the road.

## Art (under `art/`)
| file | use | generated-art prompt (GenerateImage asset) |
|---|---|---|
| `art/sky-beach.jpg` | `art.backdrop` | aqua summer sky with soft clouds and floating bubbles (asset `12037e65…jpg`) |
| `art/sea-ground.jpg` | `art.ground` (scale 30) | low-poly turquoise sea with white foam lines (asset `56e3c6a1…jpg`) |
| `art/silhouette-screen.png` | upright image, verse 1 + chorus 2 | five navy featureless paper silhouettes + an orange panel (asset `1d6a6d29…jpg`) |

The GenerateImage outputs were stored outside this box. The committed files are procedural stand-ins from `_w4_tools/art.py`. Swap them in 1:1.

## No tap hints
Events follow section downbeats and the beat. Plank dips react only to the player's own taps (schema `react: tap`, which is feedback and never fires ahead of a tap).

## Chart summary
**257 taps** (moderate tier). This is the rhythmic-logic audit of the curated 269-tap chart:
- The drum layer runs through the song, with melodic plucks in the intro and vocal phrases in the breakdown.
- Choruses and verses share one pattern bar for bar.
- The full mix has no prominent 16th figure at phrase ends, so there are no bursts.
- Honest peak: 8th runs, 211 CPM.
