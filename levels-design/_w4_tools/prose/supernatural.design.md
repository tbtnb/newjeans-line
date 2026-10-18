# Supernatural — level design (worker 4)

**Concept: "Two signals finding each other over a night city."** The line is a radio signal hopping across rooftops at night. Antennas, water tanks and receivers line the roofs. At the centre of the city a flower-shaped dish antenna (the album flower motif) is closed until Chorus 1, then blooms. The level climbs a helix around it, falls into a floating star layer, climbs back out over a gantry overpass, and lands on the final-chorus deck. Palette: midnight indigo `#1a1d4a`, broadcast pink `#c2449a`, cobalt `#0072bc`, sodium amber `#ffb347`. Diamonds are ice-cyan `#7fe3ff`, crowns gold `#ffd54a`.

Codex reference: none had arrived in `codex-ref/` when this was built, so the design is original. No real people are depicted; every figure is a prop or a motif.

## Route choreography (each section has its own texture; see route.png and route-sections.png)

| section | time | route texture | height | camera | scene / performance |
|---|---|---|---|---|---|
| Intro | 0.3–9.1 | **staircase** (2 taps per bar, short treads) | 0 | close | radio booth under the flower billboard; the billboard flickers on with the first sample hit |
| Groove | 9.1–26.8 | **lightning bolt**: alternating long/short legs one bar apart | 0 | iso | NJS drums enter; antennas and water tanks rise beside the road on the kick |
| Groove (2nd half) | 17.9– | **switchback** pair along the rooftop parapet | 0 | iso | fake-out fork at 20.7 s |
| Verse 1 | 26.8–44.4 | **serpentine corridor**: rotations only after rests ≥ 1 beat, so the long vocal lines become long sweeps and the 8th pairs become tight wiggles | 0 | iso | radio receiver EGG (dial cycles the 5 cover colours, one per bar); fork at 37.5 s |
| Pre-chorus 1 | 44.4–62.0 | **tight zigzag** then a **staircase** into the 8-tap snare-roll run | 0 | low → wide at 60.0 | six receivers light one per bar; signal poster on a rooftop hoarding |
| Chorus 1 | 62.0–79.6 | **double square helix** (orbit, 8 + 7 same-side turns) climbing **+8** around the flower antenna; laps cross over and under each other | 0 → 8 | **high** | antenna blooms on the downbeat; two orbiting light dots circle its mast |
| Verse 2 | 79.6–97.2 | **sweep out** of the helix (crosses back over the Chorus-1 roads), then a serpentine corridor | 8 | iso | fork at 86.2 s |
| Bridge | 97.2–114.8 | **fall −8** off the tower into the star layer when the drums drop (97.1 s), then a slow staircase and a **switchback** climb (+4) | 8 → 0 → 4 | **top** | floating petal pads drift around the road |
| Chorus 2 | 114.8–132.4 | **serpentine with overpasses** (rotate every 2nd tap): a figure-8 knot climbing +4 across the earlier roads | 4 → 8 | iso | gantry pylons carry the overpass |
| Interlude | 132.4–150.1 | **second helix** (+5) around the gantry pylon | 8 → 13 | **high** | crown checkpoint 2 at 132.6; fork at 141.3 |
| Final chorus | 150.1–167.7 | **big drop −8** (149.0 s) onto the deck, then **staircase → zigzag** at the highest density (2.84 taps/s) | 5 | iso | same signal poster seen again |
| Outro | 167.7–191.0 | long **turn-out** glide toward the moon | 5 | wide → orbit swing at 176.5 | bunny-face moon EGG framed by the camera swing |

Multi-level crossings: the validator counts 21 over/under passes (106 overlapping road cells in my own plot), from the helices and overpasses. There are no same-level overlaps. Every fall lands ≥ 0.35 s before the next tap: 0.64 s at 97.1 and 1.05 s at 149.0.

## Landmarks and easter eggs
- **Flower billboard** (start): textured with `art/flower-billboard.jpg`.
- **Flower antenna**: a slim mast with the flower dish at +18. It is anchored in the clear centre of the Chorus-1 helix, which wraps around it twice. You see it from the verse, again from inside the helix, and again from the Verse-2 sweep.
- **Gantry sign**: the pylons that hold up the Chorus-2 overpass, placed in the clear centre of the interlude helix.
- EGG **radio receiver**: its needle is a tiny bunny.
- EGG/landmark **bunny-face moon**: only framed by the outro camera swing.

## Fake-out forks (visual only, no hints)
Four road-coloured dead-end stubs continue straight past a real corner, at 20.7, 37.5, 86.2 and 141.3 s. They are revealed together with the road, so they add no timing information. They sink after the corner. They are part of the scenery, never a cue.

## Collectibles
- 10 diamonds sit on mid-straights, never inside air windows.
- 2 crowns (checkpoints) sit at 43.1 s (end of Verse 1) and 132.6 s (start of the interlude), on calm straights.

## Art (under `art/`, referenced by layout.json)
| file | use | generated-art prompt (GenerateImage asset) |
|---|---|---|
| `art/sky-night.jpg` | `art.backdrop` | night-city panorama, indigo to violet, stars, distant skyline (asset `6e9152caf1a606dc…jpg`) |
| `art/roof-ground.jpg` | `art.ground` (scale 40) | tiled rooftop membrane with amber lamp dots (asset `b2f4cf6c…jpg`) |
| `art/flower-billboard.jpg` | texture of the billboard face | smiling 12-petal rainbow flower on black (asset `899d6b18…jpg`) |
| `art/signal-poster.jpg` | billboard image, pre-chorus + final chorus | retro radio tower with rainbow rings (asset `1c7ac7b1…jpg`) |

The GenerateImage outputs were stored outside this box. The files committed here are procedural stand-ins drawn by `_w4_tools/art.py`, with the same names, palette and motif. To use the generated versions, swap them in 1:1.

## No tap hints
Nothing is placed at or flashes on an upcoming tap. Events follow the music clock only: beats, bars and section downbeats. The forks are scenery, revealed together with the road.

## Chart summary
348 taps, up from 162 in legacy v1 (2.15×). The hardest stretches are the 8–9-tap 8th runs into each chorus. Five off-beat 16th syncopations were added on real snare/vocal onsets. No triplet or 16th-roll events exist in the stems (checked), so no fake bursts were added. See chart-report.md.
