# Hype Boy - level design (designs-w1, v3)

Codex concept/blueprint (codex-ref/) is used as a loose mood/palette reference only; the route choreography is our own. 327 taps, speed 9.0 u/s, start heading N.

## Route textures per section

- **Intro riff** (0.00 s): Beat-stepped NE staircase on the synth riff (one tap per beat), then two long sweeps over the start deck.
- **Verse 1** (19.45 s): Locker canyon: tight sawtooth zigzag (legs of 2-4 taps) on the dembow syncopation, narrow road 1.8, the road passes through a locker passage.
- **Pre-chorus 1** (38.65 s): Square spiral (L) climbing +12 around the diving tower; the laps pass over each other.
- **Build 1** (48.25 s): Short SE staircase run off the tower top; fall -4 onto the pool deck right before the chorus.
- **Chorus 1** (53.05 s): Open U of staircases around the summer pool (three diagonal legs); five-colour pillars answer the vocal; one fake fork.
- **Post-chorus 1** (72.25 s): Switchbacks down the bridge (lanes on the longer gaps), climbing +4; the sports-hall gate wraps one lane.
- **Verse 2** (91.45 s): Diamond staircase loop around the sports court (four legs); the road closes the loop at a different height.
- **Pre-chorus 2** (115.45 s): Fall -5 into the phone patio: a tight 2-tap zigzag corridor between phone screens (road 1.7); E1 flip phone.
- **Build 2** (125.05 s): Jump +3 onto the bridge deck B2, sparse build taps.
- **Chorus 2** (129.85 s): One long sweeping NE staircase over the whole map (ramp +3) - the longest diagonal of the level.
- **Final chorus** (149.05 s): Spiral staircase: five diagonal legs rotating around the five-colour pillar ring while climbing +6, crossing over its own start.
- **Outro** (170.65 s): Calm straight to the finish deck, little white bunny echo.

## Structure

- Multi-level crossings: 44 (over/under passes, piers added automatically under raised road; camera goes "high" over underpasses).
- Fake-out forks (visual only, a stub of road continuing straight that ends in a broken edge; no hint): 31.15, 64.319, 101.355, 159.863 s.
- Arcades / wraps through buildings: Locker canyon passage (road runs between the locker walls) (19.4-38.6 s); Sports-hall gate (72.3-91.4 s).
- Elevation: ramp +11.1 at 38.652-47.205; fall -4 at 52.515; ramp +4 at 73.0-90.5; fall -5 at 115.37; jump +3 at 125.72; ramp +3 at 130.2-148.6; ramp +6 at 149.4-169.8.
- Landmarks: little white bunny echo; Diving tower (the pre-chorus spiral climbs around it); Summer pool + low diving board (chorus 1 U wraps it); MV sports court, red-white goal, yellow basketball (verse-2 loop circles it); Five-colour dance pillar ring (final spiral staircase rotates around it); 2022 EP cover bunny relief tower (skyline, seen from chorus 1, verse 2 and the final chorus); Locker canyon passage (road runs between the locker walls); Sports-hall gate.
- Eggs: E1 secret flip phone (five colour screen dots, then a white bunny).
- Diamonds (10): 10.75, 29.96, 46.38, 58.46, 82.46, 99.25, 107.35, 122.96, 135.26, 160.16 s. Crowns (2): 72.41, 147.95 s.
- Camera: 0.0s iso, 19.5s high, 23.8s high, 25.9s high, 38.7s side, 48.3s iso, 53.1s wide, 62.7s iso, 72.3s iso, 79.9s high, 82.1s iso, 91.5s high, 115.5s high, 119.6s high, 121.5s high, 122.0s high, 123.9s high, 125.1s low, 129.9s wide, 149.1s high, 158.7s iso, 170.7s wide.
- No tap hints anywhere (the engine adds the % markers itself).

## Art (engine files under art/)

All art is procedural (PIL, `_w1_tools/v3/artgen.py`): the image-generation tool's outputs could not be reached from the box shell in this session, so they could not be copied into the level folder. No real people's faces - only cartoon bunnies, shapes and album motifs.

- `art/sky.jpg` - summer pool sky
- `art/sky-lilac.jpg` - lilac sky for chorus 2 / final (section backdrop)
- `art/ground-pooltile.jpg` - aqua pool-tile ground
- `art/lockers.jpg` - locker-door texture for the canyon arcade
- `art/poster-pool.jpg` - pool poster with bunny
- `art/sticker-*.png` - sticker decals beside the road

layout.json `art`: backdrop `art/sky.jpg`, ground `art/ground-pooltile.jpg`; section backdrops: Chorus 2 -> art/sky-lilac.jpg; image objects (posters/stickers): 18.
