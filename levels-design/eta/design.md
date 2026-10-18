# ETA: Arrival Circuit (到场之前)

**Concept.** ETA is a message to a friend: "tell me your ETA, I'm on my way". The level is the trip from the moment the message is sent to arriving at the bench where the friend waits. It follows the loose mood of the Codex reference ("Arrival Circuit": phone frame, terracotta alley with a red car, pool party, rooftops, sea-cliff bridge, pixel heart, arrival). The route itself is ours: the Codex blueprint's single open loop has become a 13-texture circuit that winds back over itself.

- Palette: aqua sky #9fdbe6, ivory road #FFF2D7, coral line #F05A50, sea/pool #35C4C8, terracotta #CE785A, navy #203750, gold #F2C34E.
- Cover colours: #77C9ED #A5DFB5 #F3A8C8 #F8BB7D #B1A1E3. They are used for the pixel tower, the floats, the scene panels and the windows.
- Speed: 10 u/s, then 9 u/s in the outro.
- Road width: 2.8 → 2.0 (alley) → 2.4 → 2.2 → 2.4 → 2.1 → **1.8** (sprint) → 2.6.
- Elevation range: −3 to +15. The road crosses itself 160 times as legal over/under passes (validator count), with 0 illegal crossings.

## Route choreography (each section has its own texture; see route.png)

| # | Section (t) | Route texture | Elevation | Scene / landmarks | Camera |
|---|---|---|---|---|---|
| 1 | Intro · Call Court (0–7.0) | The line exits through a giant **phone door-frame**: a short stair, then a sidestep and a hook (seq NE/SE/NE) | 0 | Standing phone, benches, palm. **Egg 1**: bunny sticker on the phone back | close → iso swing (yaw −25) reveals the sticker |
| 2 | Verse 1 · terracotta alley (7.0–21.2) | **Parallel switchback lanes**: 8 taps along, 3 across, 8 back. Narrow 2.0 corridor between terracotta walls that react to taps | **fall −3** into the alley (8.83) | Little red car parked in a bend, bougainvillea. **Fake-out** side-alley stubs (lower, tinted, dead-end planter) | iso |
| 3 | Pre 1 · phone bridge (21.2–35.4) | **Long sweeping staircase** (one diagonal, about 60 u) ending in a 2-tap wiggle for the bar-18 8th run | **ramp +5** (24.8–35.4) | Message cards flip up on taps, relay mast, bridge gate | iso yaw +15 |
| 4 | Chorus 1 · pool party (35.4–47.9) | **Wrap three sides of the pool** (pair rotates every 14 taps: a U of stairs) | +2 | Pool with five cover-colour floats, palms, pixel-heart poster | high |
| 5 | Stop 1 · E-T-A (47.9–49.7) | Six voice-chop taps make a **V kink** (3 + 3) | +2 | Letters E, T, A react to the player's taps | close |
| 6 | Verse 2 · rooftops (49.7–63.9) | **Sawtooth hops**: the stair flips its diagonal every 4 taps, and the road runs over roofs | **jump +2.5 ×2** (52.39, 59.50) | Rooftops under the road, chimneys pulsing on kick, billboard. **Fake-out** roof plank | iso |
| 7 | Pre 2 · sea cliff (63.9–78.1) | **Cliff switchbacks** (7 along / 3 across) hugging the cliff wall | **ramp −4** (descending; passes under the helix laps later) | Cliff wall, rails, broken-ledge **fake-out**. **Egg 2**: pixel bunny in a cliff crack | side (yaw 60) |
| 8 | Pre 3 · tower helix (78.1–92.3) | **Helix spiral** around the five-colour pixel tower (pair rotates L every 8 taps). Each lap clears the lap below | **ramp +12** | Pixel tower (skyline landmark, seen again from Chorus 2 and Final A); one colour band lights per bar | high |
| 9 | Chorus 2 · sky bridge (92.3–104.8) | **Long bridge with a dog-leg** (16 + 9 + rest) high over Pre 2 / Pre 3 | +13 (top) | Bridge gate, rails, five scene panels drop in on bar downbeats, confetti | wide → high |
| 10 | Stop 2 · E-T-A (104.8–106.6) | **fall −6** off the bridge edge (104.61), then a mirrored V kink | +7 | Letters E, T, A | top |
| 11 | Final A · pixel heart (106.6–120.8) | **Closed lobe** (pair rotates every 12 taps) round a giant flat pixel heart. It closes because of the descent | **ramp −6** | Giant flat heart image (art/heart-poster.png), lamps that react to taps | high |
| 12 | Final B · arrival sprint (120.8–135.0) | **Tight 2-tap wiggle corridor** (posts at ±1.6), then a long straight stair carrying the 19-tap run | **fall −3** at the end (134.72) | Sprint posts. **Egg 3**: five windows light one per beat (124.3 s). **Fake-out** closed side street | iso (shake 0.08) |
| 13 | Outro · two lamps (135.0–151.4) | **Big sweeping steps** (16 u legs), then a long straight to the gate | −3 | Bench between two lamps; the lamps light on 136.8 / 138.6 | high → wide |

The fake-out forks are scenery only. They sit 1.2 u lower than the road, have a different tint, end in a broken edge, rock or planter, and never react to music. Nothing marks a tap time.

## Map performances (music-synced, never previewing taps)
- Alley walls, message cards, lamps, letters and sprint posts use `react:"tap"` (piano-key feedback on the player's actual taps).
- Chimneys and the relay mast use `react:"kick"`. Palms and bougainvillea use `beat`.
- Pool floats bob in on the first five beats of Chorus 1.
- Pixel tower: one band lights per bar through the helix, then it spins during Chorus 2.
- Scene panels drop on the Chorus 2 bar downbeats.
- Palette changes:
  - colour drains on both voice-chop stops;
  - the sky deepens at Chorus 2;
  - golden hour from Final A;
  - warm dusk in the outro.
- Particles: a pixel burst when landing in the alley, and confetti over the sky bridge.

## Collectibles
- 10 diamonds, each on a straight at least 0.21 s from any tap: 3.12, 14.78, 26.78, 40.12, 54.78, 69.45, 85.89, 100.56, 113.89, 128.56 s.
- Crowns:
  - 47.78 s, before the first E-T-A stop (32 %);
  - 75.01 s, at the foot of the tower helix (50 %).
- The finish is a gold gate past the bench.

## Easter eggs
1. Bunny sticker on the back of the start phone (art/bunny-sticker.png). It shows when the camera swings at 3 s.
2. A pixel bunny peeking from a crack in the sea cliff, Pre 2 at about 73 s (the Codex reference's E1).
3. Five windows next to the sprint light up one per beat, like five friends picking up the call.

## Art (levels-design/eta/art/, referenced in layout.json → `art`)

| file | use |
|---|---|
| art/sky.jpg | `art.backdrop`: summer sea sky with voxel clouds and distant islands |
| art/sea.jpg | `art.ground`: turquoise sea texture (scale 60) |
| art/terracotta-tile.jpg | catalogued for the alley walls and roofs |
| art/heart-poster.png | pool billboard, rooftop billboard, giant flat pixel heart (Final A) |
| art/bunny-sticker.png | egg decal on the phone |

GenerateImage was used first, but its files never reached the box after the 11:33 restore. These files are drawn procedurally by `_tools-w3/art_proc.py`: flat, pixel and low-poly style, no people and no faces. They can be swapped 1:1 for generated versions.

## Chart summary (tier: hard)
- Taps: 422 (legacy 232, ×1.82).
- Density: average 167 CPM, peak 420 CPM (most taps in any 1 s; The Racing peaks at 440).
- Runs: mostly 8ths (0.222 s), plus **12 short 16th bursts** (0.111 s). They sit only on real 16th events:
  - the hat/vocal fill into Chorus 1 (bar 18: four 16ths);
  - the snare fill into Chorus 2 (bar 50);
  - the rapid "E-T-A" syllables in Chorus 2;
  - the vocal pickups in Final A/B.
- The hook keeps its off-beat syncopation (16ths 2-4-6-8-12-15), like The Racing's dotted figures.
- Densest run: 19 taps from 131.0 to 134.7 s.
- Judgment (schema v2.5): per-tap good window = half the local gap (±55 ms inside bursts, ±100 ms max), perfect ±40 ms.
- See chart-report.md for per-section density, spot checks and the comparison with the originals.
- No tap hints of any kind.


## Integration note (integ-b, 2026-10-18)
The rhythm-logic audit changed the tap count from 422 to 413 (only removals; see `chart-report.md` → *Rhythm-logic audit*). Tap counts quoted above are the pre-audit numbers; the original files are in `pre-audit/`. Because every removed tap is a removed turn, the route after the first removal is rotated relative to this description; the turn sequence of each phrase (spirals, switchbacks, wraps) was kept wherever legal, and worldPos landmarks were moved with the road (`tools/charts/integb_route.py`).
