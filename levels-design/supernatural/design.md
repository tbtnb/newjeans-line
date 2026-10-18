# Supernatural — level design (worker 4)

**Concept: "Two signals finding each other over a night city."** The line is a radio signal hopping across rooftops at night. Antennas, water tanks and receivers line the roofs. At the centre of the city a flower-shaped dish antenna (the album flower motif) is closed until Chorus 1, then blooms. The level climbs a helix around it, falls into a floating star layer, climbs back out over a gantry overpass, and lands on the final-chorus deck. Palette: midnight indigo `#1a1d4a`, broadcast pink `#c2449a`, cobalt `#0072bc`, sodium amber `#ffb347`. Diamonds are ice-cyan `#7fe3ff`, crowns gold `#ffd54a`.

**Codex alignment** (`codex-ref/design.md` + concept/blueprint, which arrived late in the build), used as a loose reference:
- Kept from the blueprint: the night city opening up from closed streets to wide rooftops, and its landmarks:
  - L1 cloud weather tower (intro, far side);
  - L2 text-free CRT TV whose colour block switches on the snare backbeat (verse 1);
  - L3 rooftop broadcast stage with three square lamps and **five white square mic plinths standing in for the members, with no figures**, beside the Chorus-1 helix; the lamps switch on at the chorus downbeat;
  - L4 bunny-face rainbow flower (our billboard + flower antenna);
  - L6 five coloured flower terraces rising one per bar in the final chorus;
  - L7 white bunny-ear finish stone;
  - E1 red-beret boat sliding out of a cloud gap in the bridge.
- Kept from the palette: gold collectibles `#FFD34E`.
- Changed: the route is our own and much denser than the blueprint's U and C corridors (helices, overpasses, serpentine corridors). No real people are depicted.

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
| Final chorus | 150.1–167.7 | **big drop −8** (149.0 s) onto the deck, then **staircase → zigzag** at the highest density | 5 | iso | same signal poster seen again |
| Outro | 167.7–191.0 | long **turn-out** glide toward the moon | 5 | wide → orbit swing at 176.5 | bunny-face moon EGG framed by the camera swing |

Multi-level crossings come from the helices and overpasses (see the validator output in chart-report.md / route.png). There are no same-level overlaps. Every fall lands ≥ 0.35 s before the next tap: 0.64 s at 97.1 and 1.05 s at 149.0.

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
**320 taps** (legacy v1: 162). This is the rhythmic-logic audit of the curated 343-tap chart: one layer per section (the drum kit through most of the song, the sample hits in the intro), shared patterns for repeated phrases, and faint/off-layer taps removed. The full mix has no prominent 16th figure, so there are no 16th bursts. The honest peak stays at 8ths: 218 CPM, i.e. 8–9-tap runs into the choruses. See chart-report.md.

## Generated facts (from layout.json / chart.json)

- Road width {'width': [{'t': 0, 'w': 2.6}, {'t': 26.78, 'w': 2.3}, {'t': 62.01, 'w': 2.2}, {'t': 97.24, 'w': 2.4}, {'t': 114.85, 'w': 2.0}, {'t': 150.08, 'w': 1.8}, {'t': 167.7, 'w': 2.4}], 'height': 0.6, 'reveal': [{'t': 0, 'mode': 'static', 'lead': 3.0}, {'t': 9.17, 'mode': 'rise', 'lead': 2.0}, {'t': 62.01, 'mode': 'rise', 'lead': 1.6}, {'t': 97.24, 'mode': 'unfold', 'lead': 1.8}, {'t': 114.85, 'mode': 'drop', 'lead': 1.5}, {'t': 150.08, 'mode': 'rise', 'lead': 1.4}, {'t': 167.7, 'mode': 'fade', 'lead': 2.5}]}; start heading N; speed [{'t': 0, 'v': 9.0}]
- Elevation: ramp +8 @ 62.279999999999994–79.6 (Chorus 1: square helix of staircases around the flower antenna, +4 per lap); fall -8 @ 97.813 (drums drop out -> long fall off the antenna tower into the floating star layer); ramp +4 @ 106.02–114.83 (climb out of the star layer); ramp +4 @ 117.03–128.04 (Chorus 2 gantry climbs over earlier roads); ramp +5 @ 132.44–141.25 (interlude helix around the gantry pylon); fall -8 @ 150.657 (big drop onto the final-chorus deck)
- Camera: 0s close; 9.17s iso; 26.78s iso; 44.39s low; 60.0s wide; 62.01s high; 79.62s iso; 97.24s top; 112.65s iso; 123.66s iso; 132.47s high; 141.28s iso; 150.08s iso; 150.6s iso; 167.7s wide; 176.5s 
- Diamonds (t): 7.488, 20.424, 38.038, 57.305, 85.928, 103.681, 122.809, 142.625, 160.791, 178.68; crowns (checkpoints): 43.13, 132.58
- Landmarks: `flower_billboard` (Murakami flower billboard (album cover) above the radio booth); `flower_antenna` (Flower dish antenna at the centre of the loop: petals closed until Chorus 1, bloom on the downbeat; reachable only by eye (the loop orbits it)); `bunny_moon` (EGG/landmark: the moon is the bunny face from the cover (only framed when the outro camera swings at 176.5 s)); `gantry_sign` (gantry pylons holding the overpass (two-signals crossing)); `cloud_tower` (L1 cloud weather tower: faceted cloud blocks stacked on a mast (rain/wind motif, never over the road)); `crt_tv` (L2 retro CRT TV with colour-block screen only (no text)); `broadcast_stage` (L3 rooftop broadcast stage: metal deck, three square front lamps, five white square mic plinths (stand-ins for the five members, no figures)); `bunny_stone` (L7 white bunny-ear finish stone)
- Easter eggs: `radio_egg` (EGG: old receiver; its dial lights the 5 cover colours in turn and the needle is a tiny bunny); `bunny_moon` (EGG/landmark: the moon is the bunny face from the cover (only framed when the outro camera swings at 176.5 s)); `boat_egg` (E1 tiny boat with a red beret slides out of a cloud gap (far scenery, no collision))
- Fake-out forks (visual only, road-coloured dead-end stubs that rise 2 s early and sink after the corner; they are revealed together with the road (same lead), so they add no timing information and only fake a straight continuation): fork0, fork1, fork2, fork3
- Objects: 71 total; events: 26
- Art wired into layout: backdrop `art/sky-night.jpg`, ground `art/roof-ground.jpg`, images/textures `art/flower-billboard.jpg`, `art/signal-poster.jpg`
