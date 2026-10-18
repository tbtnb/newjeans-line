# Attention - level design (designs-w1, v3)

Codex concept/blueprint (codex-ref/) is used as a loose mood/palette reference only; the route choreography is our own. 285 taps, speed 9.0 u/s, start heading N.

## Route textures per section

- **Intro** (0.00 s): Sweep: two long straights and one big L on the sunny rooftop (L0).
- **Hook A** (9.61 s): Staircase cluster NE on the bass entry, then a sawtooth zigzag (NE/NW legs every 4-5 taps) between roof blocks.
- **Verse 1** (27.89 s): Switchbacks along the roof-court walls: lanes on the long vocal gaps, rungs on the short ones; narrow road 1.8; a roof-court passage wraps the road.
- **Pre-chorus 1** (46.75 s): Sky bridge B1: one long SE staircase climbing +4 over the void.
- **Chorus 1** (62.18 s): Rotating staircase that wraps the MV football pitch (SE -> SW -> NW legs); stands unfold; one fake fork ends in a broken edge.
- **Verse 2** (83.32 s): Drop -4 at the end of chorus 1, then a square spiral that climbs +18 around the window clock tower (laps pass over each other), then switchbacks down the tower wall and through the window arcade.
- **Pre-chorus 2** (101.60 s): Tight sawtooth corridor (legs of 3-4 taps), narrow road 1.7, ramping down -6; five amber windows easter egg.
- **Chorus 2** (117.03 s): Drop -4, then a wide zigzag that passes OVER the hook and verse-1 roofs (multi-level crossings), terraces fan open.
- **Final chorus** (137.60 s): Staircase loop around the bunny relief (four diagonal legs) while climbing +6, crossing above the verse-1 switchbacks; one 3-tap 16th figure on the audible snare fill.
- **Outro** (156.10 s): Drop -5 onto the cover square level, long release sweeps and a last pair of switchbacks into the deep-blue finish.

## Structure

- Multi-level crossings: 43 (over/under passes, piers added automatically under raised road; camera goes "high" over underpasses).
- Fake-out forks (visual only, a stub of road continuing straight that ends in a broken edge; no hint): 25.623, 70.473, 124.761, 146.763 s.
- Arcades / wraps through buildings: Window arcade: the road runs through the gallery building (93.9-101.6 s); Roof-court passage (27.9-46.7 s).
- Elevation: ramp +4 at 47.7-61.8; fall -4 at 82.816; ramp +18.3 at 83.32-93.5; ramp -6 at 103.2-116.6; fall -4 at 119.376; ramp +6 at 138.0-155.5; fall -5 at 156.261.
- Landmarks: Rooftop water tower; B1 sky bridge gate; M5 cover square; Window clock tower (the verse-2 spiral climbs around it); MV football pitch (chorus 1 staircase wraps it); M4 2022 EP cover bunny relief (final loop circles it); Window arcade: the road runs through the gallery building; Roof-court passage.
- Eggs: E1 five window lights.
- Diamonds (10): 13.04, 19.04, 38.47, 54.34, 68.75, 93.61, 110.76, 123.62, 147.05, 163.34 s. Crowns (2): 83.61, 137.91 s.
- Camera: 0.0s iso, 9.6s iso, 27.9s iso, 32.0s high, 38.7s iso, 46.8s iso, 62.2s wide, 83.6s side, 93.9s iso, 96.0s high, 99.2s iso, 101.6s high, 117.0s wide, 137.6s high, 147.3s iso, 156.1s iso, 168.0s wide.
- No tap hints anywhere (the engine adds the % markers itself).

## Art (engine files under art/)

All art is procedural (PIL, `_w1_tools/v3/artgen.py`): the image-generation tool's outputs could not be reached from the box shell in this session, so they could not be copied into the level folder. No real people's faces - only cartoon bunnies, shapes and album motifs.

- `art/sky.jpg` - soft summer sky backdrop with faint halftone dots
- `art/sky-dusk.jpg` - warm outro sky (section backdrop)
- `art/ground-dots.jpg` - ice-blue halftone ground tile
- `art/bunny-mural.jpg` - 2022 EP bunny mural (cartoon bunny, no faces of people)
- `art/stadium-banner.jpg` - coral/ivory stripe banner for the stadium stands
- `art/sticker-*.png` - sticker decals lying beside the road

layout.json `art`: backdrop `art/sky.jpg`, ground `art/ground-dots.jpg`; section backdrops: Outro -> art/sky-dusk.jpg; image objects (posters/stickers): 17.
