# Cool With You: The Observer in the Rain (雨中的旁观者)

**Concept.** The MV retells Eros and Psyche: a love that cannot be looked at directly. The surrounding characters are the observers, and the song's choice is to stay ("I'm cool with you"). The warm coral line moves through a cool, rainy gallery city that never reflects it. It loses one light, then chooses to come back.

The level follows the mood of the Codex reference: gallery frame, empty mirror, sunken rain courtyard, five-pillar balcony, white-topped black monument, pixel city, separated zebra crossing. The routes are our own: 11 distinct textures, with crossings over and under each other.

- Palette:

  | role | colour |
  |---|---|
  | rain void | #536C78 |
  | road | ivory #EEEADF |
  | stone | #AEBFC5 |
  | deep | #254647 |
  | line | coral #F08B78 |
  | city | cyan #9BD8E2 |
  | frame / crown | gold #D8B86A |

- Speed: 8.5 u/s.
- Road width: 2.8 → 2.4 → **2.0** (rain curtain, build) → 2.6 → 2.4 → 2.2 → **1.9** (final drop B) → 2.8.
- Elevation: −3 to +9. 141 multi-level crossings (validator), 0 illegal.

## Route choreography (see route.png)

| # | Section (t) | Route texture | Elevation | Scene | Camera |
|---|---|---|---|---|---|
| 1 | Intro · empty gallery (0–14.6) | Doorway, a long straight, then a **square hook and a staircase** with wide 7–20 u legs (sparse taps) | 0 | Gallery doorway, plinths, two floating frames (art/wings-painting.jpg) | iso |
| 2 | Verse 1 · reflections wake (14.6–28.8) | **Wrap around the mirror room**: the pair rotates every 8 taps, giving three sides of a box | 0 | Empty mirror landmark at the room centre; gallery walls rise and react to taps. **Egg 1**: wings in the mirror at 21 s | high → iso (yaw −40) |
| 3 | Verse 1b · rain curtain (28.8–43.0) | **Parallel switchbacks** (6 along / 3 across) in a narrow 2.0 lane between rain posts | 0 | Rain particles. Two flooded-side-path **fake-outs** (lower, end in water) | iso |
| 4 | Hook · moonlit pool (43.0–57.2) | **fall −3** into the sunken courtyard, then a **square spiral round the moon pool** (rotates every 4 taps). The pool lies under Verse 1b's lane: an underpass | −3 | Moon pool, moon | high |
| 5 | Drop 1 · courtyard (57.2–71.4) | **Big climbing U** (rotates every 12) | **ramp +6** | Five pale observer pillars; a warm lamp lights one per bar; lanterns pulse on kick | wide |
| 6 | Verse 2 · two lights (71.4–85.7) | **Serpentine descent** (diagonal flips every 6 taps) | +3 | Two lights drift together (raise/converge). Parallel-boardwalk **fake-out** | iso |
| 7 | Break · one light leaves (85.7–92.8) | **fall −3**, then a **wide double U-turn** (rotates every 2 taps, about 15 u legs) | 0 | Light B sinks away; white-topped black monument | side (yaw 70) |
| 8 | Build · wings unfold (92.8–99.9) | **Straight staircase**, then a 2-tap wiggle on the 8th bar | 0 → **jump +3** (99.94) | Four wing panels unfold on bar downbeats | low |
| 9 | Final drop A · feather storm (99.9–114.1) | **Helix up** round the feather spire (rotates every 4), each lap ≥ 3 u over the last | **ramp +6** | Feather particles, the spire spins, feather billboard | high |
| 10 | Final drop B · choosing to stay (114.1–128.3) | **Large horseshoe loop** through the pixel city, closing over the intro on the way down | **ramp −6** | Eight cover-colour buildings rise; windows light per half-bar; rails react to taps | iso |
| 11 | Outro · open exit (128.3–147.9) | **Wide rectangle** with 15–30 u legs, then a long straight to the gate | **ramp −3** | Separated zebra crossing. **Egg 2**: one white feather. Light B returns; the rain stops | wide |

The fake-out forks are scenery only. They sit 1.2 u lower, are tinted, end in water or a rock, and have no music reaction. Nothing previews tap times.

## Map performances
- Taps (react:"tap"): gallery walls, rain posts, city rails.
- Kick: lanterns and the feather spire.
- Beat: city buildings.
- Light cues: observer lamps one per bar (Drop 1), city windows per half-bar (Final B).
- The two lights converge through Verse 2, light B sinks in the break and returns in the outro.
- Particles: rain from Verse 1b to Drop 1, feathers in Final A, a pixel burst at Final B.
- Palette cues: darker at the hook and break, brighter at the drops, warm and clear in the outro.

## Collectibles
- 10 diamonds: 8.67, 19.56, 32.89, 47.00, 61.67, 76.45, 90.12, 103.78, 117.45, 132.56 s.
- Crowns:
  - 57.56 s, at the start of Drop 1 (39 %);
  - 92.45 s, at the start of the build (63 %).
- Finish: gold gate.

## Easter eggs
1. A tiny pair of wings flickers in the "empty mirror" during the camera swing at about 21 s. The mirror never shows the line.
2. A single white feather on the separated zebra crossing in the outro: the light that left came back.

## Art (cool-with-you/art/)

| file | use |
|---|---|
| art/rain-city.jpg | `art.backdrop`: rainy pixel city, cyan facades, warm windows |
| art/wet-stone.jpg | `art.ground`: wet slate paving (scale 40) |
| art/wings-painting.jpg | gallery frames: two abstract ivory forms, one winged (no figures) |
| art/feather-poster.jpg | posters and billboards (Verse 2, Final A) |

All four are procedural (`_tools-w3/art_proc.py`) because GenerateImage output did not reach the box. No faces.

## Chart summary (tier: moderate)
- Taps: 252 (legacy 107, ×2.36).
- Density: average 102 CPM, peak 300 CPM.
- Two-step logic: kick on 16ths 0 and 10, ghost on 6, dotted garage fills (0-3-6-…) at phrase ends. The hook and break stay sparse.
- 16th taps: only **four 16th pairs**, on the loud snare flams (16ths 3-4) at phrase ends in the drops: 70.11, 105.67, 112.78 and 118.12 s.
- Densest run: 15 taps from 124.8 to 127.9 s.
- Judgment (schema v2.5): good window = half the local gap (±55 ms at the flams, ±100 ms max), perfect ±40 ms.
- See chart-report.md.
