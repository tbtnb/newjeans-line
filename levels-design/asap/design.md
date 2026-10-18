# ASAP: Garden After Dark (天黑后的花园)

**Concept.** ASAP is a soft, swinging song about wanting to see someone right away. The level is a night walk through an emerald forest garden toward a small house with one lit window. It starts with eyes in the dark, passes a clock that seems to stand still and a pool that holds the moon, and ends with five lamps and a bunny made of pollen. It follows the Codex reference's mood (green forest, picnic stone, pendulum, small house), but the route is our own: a 13-texture walk that keeps crossing over and under itself.

- Palette: night teal #143D36 → morning #bcd6c0, emerald #315C4C, meadow #A8BE94, moon pool #76BBB9, ivory road #F4F1DF, rose line #E35D83, gold #E2BD65.
- Cover colours: #87D0E3 #A8D485 #F1B8CB #EAB88C #B5A0D5. They are used for the stars and the five stepped towers.
- Speed: 8.5 u/s. The song swings, so the road is relaxed.
- Road width: 2.8 → 2.6 → **2.0** (leaf-wall switchbacks) → 2.4 → 2.2 → **2.0** (dance break) → 2.4 → 2.1 → 2.8.
- Elevation range: 0 to +7. The road crosses itself 70 times as legal over/under passes (validator count), with 0 illegal crossings.

## Route choreography (each section has its own texture; see route.png)

| # | Section (t) | Route texture | Elevation | Scene / landmarks | Camera |
|---|---|---|---|---|---|
| 1 | Intro · snaps in the grass (0–4.0) | Short single staircase out of the undergrowth | 0 | **Egg 1**: two pairs of bunny eyes blink in the dark bushes (billboards, art/bunny-eyes.png) | close |
| 2 | Verse 1 · moon-green meadow (4.0–11.4) | **Hook**: 3 steps NE, 2 back NW, then onward (seq) | 0 | Folded picnic stone landmark, flowers bob on the beat | iso |
| 3 | Verse 1b · clock in the sky (11.4–26.2) | **Tight clockwise spiral** steps (pair rotates every 2 taps) winding past the clock tower | 0 | Pendulum clock tower; its face (art/pendulum-sign.jpg) turns slowly, as if time stands still | high |
| 4 | Pre · letters behind trees (26.2–41.0) | **Parallel switchback lanes** in a narrow 2.0 corridor between leaf walls that react to taps | **ramp +3.5** (37.3–41.0) | Letters hidden behind the trees. **Fake-out**: an overgrown side path, lower, ending at a hedge | iso yaw +20 |
| 5 | Chorus 1 · swing of pendulums (41.0–55.7) | **Wide anticlockwise sweep** (pair rotates L every 8 taps), forming a big U round the clearing | +3.5 | Five white wing slabs rise one per beat, four gold pendulums swing on the beat, sign-board | wide |
| 6 | Stop · held breath (55.7–57.6) | One step, then **fall −3.5** (56.69) into the silent bar | 0 | The meadow dims. Crown 1 sits just before the edge | top |
| 7 | Verse 2 · water garden (57.6–72.3) | **Serpentine** (flip every 3 taps) across the moon pool on stepping boards, crossing under Chorus 1 | 0 | Moon pool landmark, lily pads that react to taps | iso |
| 8 | Dance break · stars in groups (72.3–87.1) | **Zigzag (every 4), then a square spiral climb** (rotates R every 4) carrying the 16th snare fills | **ramp +7** (79.7–85.3) | Six stars pulse on the kick, star particles | high |
| 9 | Turnaround (87.1–92.6) | **Tight 2-tap curl** (rotates L every 2) | +7 | **Fake-out**: a garden path that ends at a gate | side (yaw −60) |
| 10 | Chorus 2 · the small house (92.6–114.8) | **Wrap round the small house** (pair rotates R every 12 taps) in one long loop, passing over the Pre and Verse 2 | **ramp −3.5** (92.6–96.3) | The small house; a window lights at the second phrase; a fence that reacts to taps | high |
| 11 | Hush · lamp flickers (114.8–120.3) | **fall −3.5** (114.84), then single-tap turns | 0 | The lamp that flickers, dimming on the hush | close |
| 12 | Final hook · lamp lights (120.3–129.6) | **Steps and V kinks** (4/3/5 seq) over the outro road | **ramp +7** (120.3–125.9) | The lamp lights fully; five stepped towers in the cover colours rise; petals | wide |
| 13 | Outro · pollen bunny (129.6–134.4) | Long straight stair to the gate | +7 | **Egg 2**: a bunny made of glowing pollen dots fades in beside the road | high |

The fake-out forks are scenery only. They sit 1.2 u lower than the road, have a different tint, end at a hedge or gate, and never react to music. Nothing marks a tap time.

## Map performances (music-synced, never previewing taps)
- Leaf walls, lily pads and the garden fence use `react:"tap"` (feedback on the player's actual taps).
- Stars use `react:"kick"`. Flowers, pendulums, letters and bunny eyes use `beat`.
- The white wings rise one per beat at the start of Chorus 1; the stepped towers rise one per bar in the final hook.
- Clock face spins slowly through Verse 1b.
- Palette changes:
  - moonlight at Verse 1;
  - green-gold clearing at Chorus 1;
  - dim on the held-breath stop;
  - pale dawn at Chorus 2;
  - dark on the hush;
  - morning glow in the final hook.
- Particles: stars through the dance break, petals from the final hook.

## Collectibles
- 10 diamonds, each on a straight away from taps: 6.46, 18.22, 30.34, 45.11, 61.72, 70.03, 81.91, 100.49, 109.72, 123.73 s.
- Crowns:
  - 55.84 s, at the start of the held-breath stop, before the fall (42 %);
  - 115.72 s, just after the hush fall, under the flickering lamp (86 %).
- The finish is a gold gate.

## Easter eggs
1. Bunny eyes blinking in the intro undergrowth (art/bunny-eyes.png billboards).
2. A bunny made of glowing pollen dots that fades in for the last bars.

## Art (levels-design/asap/art/, referenced in layout.json → `art`)

| file | use |
|---|---|
| art/forest.jpg | `art.backdrop`: emerald night forest with moon and fireflies |
| art/meadow.jpg | `art.ground`: meadow grass with flowers (scale 35) |
| art/pendulum-sign.jpg | clock-face part texture and the Chorus 1 sign-board |
| art/bunny-eyes.png | intro bunny-eyes billboards |

GenerateImage was tried first, but its output files never reached the box. These files are drawn procedurally by `_tools-w3/art_proc.py`: flat style, no people and no faces. They can be swapped 1:1 for generated versions.

## Chart summary (tier: hard, within a soft swing song)
- Taps: 201 (legacy 83, ×2.42).
- Density: average 90 CPM, peak 360 CPM (most taps in any 1 s).
- Runs: mostly 8ths on the kick and the hook's off-beats (16ths 6-10, 6-8-10-12-14), plus **12 short 16th bursts** (0.115 s). They sit only on real 16th events:
  - the hat/snare fill into Chorus 1 (bar 18);
  - the snare rolls of the dance break (bars 40–42);
  - the turnaround fill;
  - the hat pickups in Chorus 2 and the final hook.
- Densest run: 11 taps from 77.87 to 79.72 s (dance break).
- Judgment (schema v2.5): per-tap good window = half the local gap (validator minimum ±52 ms, ±100 ms max), perfect ±40 ms.
- ASAP is the gentlest of the "hard" songs: it is slow and swung, so its density sits below ETA's on purpose (see chart-report.md).
- No tap hints of any kind.


## Integration note (integ-b, 2026-10-18)
The rhythm-logic audit changed the tap count from 201 to 158 (only removals; see `chart-report.md` → *Rhythm-logic audit*). Tap counts quoted above are the pre-audit numbers; the original files are in `pre-audit/`. Because every removed tap is a removed turn, the route after the first removal is rotated relative to this description; the turn sequence of each phrase (spirals, switchbacks, wraps) was kept wherever legal, and worldPos landmarks were moved with the road (`tools/charts/integb_route.py`).
