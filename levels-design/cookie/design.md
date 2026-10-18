# Cookie - level design (designs-w1, v3)

Codex concept/blueprint (codex-ref/) is used as a loose mood/palette reference only; the route choreography is our own. 500 taps, speed 10.0 u/s, start heading N.

## Route textures per section

- **Intro** (0.00 s): Studio entrance: sparse taps on the kick/bass hits, two long sweeps between black flats.
- **Verse 1** (12.33 s): Bench switchbacks: the long gaps become lanes along the five-seat bench wall, the short 8th pairs are the hairpins; passes under the bench-gallery arch.
- **Pre-chorus 1** (36.79 s): Square spiral climbing around the folding stair tower (laps pass over each other) on the rising vocal phrase.
- **Chorus 1** (49.02 s): Fall onto the open stage, then a three-leg staircase horseshoe (NE, SE, SW) around the 12-sided CD set piece; one fake fork.
- **Verse 2** (73.48 s): Narrow sawtooth corridor (legs of 2-4 taps) - the bench motif compressed, road 1.8.
- **Pre-chorus 2** (97.94 s): Second, steeper spiral climb (same vocal phrase as pre 1, same spiral texture).
- **Chorus 2** (110.17 s): Four-leg staircase loop round the terrace (ramp +5), closing over its own start.
- **Jersey-club bridge** (134.63 s): Fall -4, then a tight NE/NW zigzag corridor (legs 4-7) on the 3-3-2 club kicks; paired risers pulse on the kick.
- **Final chorus** (159.09 s): One long sweeping staircase across the whole map (ramp +3) with the bunny relief tower on the skyline; one fake fork.
- **Dance break** (183.55 s): Choreography grid: sawtooth steps through rows of studio flats, then switchbacks through the studio-flat hall.
- **Outro** (208.01 s): Descending ramp (-6) to the quiet studio, long straights.

## Structure

- Multi-level crossings: 63 (over/under passes, piers added automatically under raised road; camera goes "high" over underpasses).
- Fake-out forks (visual only, a stub of road continuing straight that ends in a broken edge; no hint): 19.786, 59.914, 119.914, 169.979 s.
- Arcades / wraps through buildings: Bench gallery (the verse-1 switchbacks pass under a black studio arch) (12.3-36.7 s); Studio-flat hall of the dance break (196.5-207.9 s).
- Elevation: ramp +24.3 at 36.79-48.923; fall -4 at 48.683; ramp +26.7 at 97.94-110.072; ramp +5 at 110.6-133.8; fall -4 at 134.295; ramp +3 at 159.5-182.5; ramp -6 at 209.0-229.0.
- Landmarks: Five-seat black bench (MV); Five-step folding stair tower (the pre-chorus spiral climbs around it); Five-step folding stair tower (the pre-chorus spiral climbs around it); 12-sided graffiti CD set piece (chorus-1 horseshoe wraps it); Terrace with the five-seat bench repeated (chorus-2 loop circles it); 2022 EP bunny relief tower (assembles at the final chorus); Bench gallery (the verse-1 switchbacks pass under a black studio arch); Studio-flat hall of the dance break.
- Eggs: EE five seats cast a bunny shadow + cookie-shaped CD stamper.
- Diamonds (10): 5.46, 25.42, 42.99, 56.57, 65.17, 96.32, 112.36, 144.09, 173.52, 203.42 s. Crowns (2): 75.49, 159.08 s.
- Camera: 0.0s iso, 12.3s high, 13.0s high, 15.7s high, 36.8s side, 49.0s wide, 61.2s iso, 73.5s high, 97.9s side, 110.2s wide, 134.6s high, 153.0s iso, 159.1s wide, 183.6s high, 203.3s high, 206.0s high, 208.0s iso, 222.0s wide.
- No tap hints anywhere (the engine adds the % markers itself).

## Art (engine files under art/)

All art is procedural (PIL, `_w1_tools/v3/artgen.py`): the image-generation tool's outputs could not be reached from the box shell in this session, so they could not be copied into the level folder. No real people's faces - only cartoon bunnies, shapes and album motifs.

- `art/sky.jpg` - grey-blue studio sky with halftone dots
- `art/sky-violet.jpg` - violet backdrop for the Jersey-club bridge (section backdrop)
- `art/ground-studio.jpg` - periwinkle studio-floor stripes
- `art/poster-cd.jpg` - CD poster with bunny (billboards around the chorus-1 horseshoe)
- `art/bunny-wall.jpg` - cartoon bunny mural (arcade walls, bunny relief tower face)
- `art/sticker-*.png` - cookie / CD / star / bunny / heart decals beside the road

layout.json `art`: backdrop `art/sky.jpg`, ground `art/ground-studio.jpg`; section backdrops: Jersey-club bridge -> art/sky-violet.jpg; image objects (posters/stickers): 20.
