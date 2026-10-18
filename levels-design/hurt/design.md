# Hurt - level design (designs-w1, v3)

Codex concept/blueprint (codex-ref/) is used as a loose mood/palette reference only; the route choreography is our own. 118 taps, speed 8.0 u/s, start heading N.

## Route textures per section

- **Intro** (0.00 s): Sparse entrance, about one tap per bar on the intro chords; two long NE steps.
- **Verse 1** (10.93 s): Frame switchbacks: long lanes on the held vocal lines, hairpins on the short syllable pairs; one lane runs through the portrait-frame gallery.
- **Pre-chorus 1** (32.26 s): Paper staircase climbing NE (ramp +3.5); the unsent folded letter opens beside it.
- **Chorus 1** (42.93 s): Three-leg staircase horseshoe around the quiet court and its halftone bunny wall; one fake fork.
- **Verse 2** (64.26 s): Reed switchbacks heading back SW and passing OVER the verse-1 area (+3.5 above it).
- **Breath** (80.26 s): Vocal-gap breath: one tap, long straight over still water.
- **Pre-chorus 2** (85.59 s): Narrow paper corridor: short 2-3-tap zigzag (road 1.8).
- **Chorus 2** (96.26 s): Ramp +4 onto the ear trestle: three-leg staircase U that crosses over the earlier route; five pixel bunnies under the trestle.
- **Bridge** (117.59 s): Long quiet switchbacks through the colonnade, few bends.
- **Final chorus** (128.26 s): Fall -4, then fan terraces: 2-4-tap zigzag steps; the frames open on alternating beats.
- **Outro** (143.59 s): Long dawn staircase to the square quiet platform; frames stop moving.

## Structure

- Multi-level crossings: 11 (over/under passes, piers added automatically under raised road; camera goes "high" over underpasses).
- Fake-out forks (visual only, a stub of road continuing straight that ends in a broken edge; no hint): 51.594, 104.927, 150.268 s.
- Arcades / wraps through buildings: Portrait-frame gallery (one verse-1 lane runs through it) (10.9-32.2 s); Quiet colonnade on the bridge (117.6-128.2 s).
- Elevation: ramp +3.5 at 32.6-42.5; ramp +4 at 96.6-116.8; fall -4 at 128.989.
- Landmarks: M1 five empty portrait frames; M2 unsent blank folded letter; M3 halftone bunny wall (2022 EP cover); M4 ear pier; square quiet platform at dawn; Quiet square court with the halftone bunny wall (chorus-1 horseshoe wraps it); Portrait-frame gallery (one verse-1 lane runs through it); Quiet colonnade on the bridge.
- Eggs: E1 five pixel bunnies under the trestle.
- Diamonds (10): 8.26, 16.26, 25.59, 37.27, 50.60, 78.92, 89.60, 104.59, 123.59, 148.09 s. Crowns (2): 63.59, 116.93 s.
- Camera: 0.0s iso, 10.9s high, 17.8s high, 21.4s high, 32.3s side, 42.9s wide, 64.3s high, 80.3s low, 85.6s iso, 96.3s wide, 117.6s side, 122.4s high, 124.8s side, 128.3s iso, 143.6s wide.
- No tap hints anywhere (the engine adds the % markers itself).

## Art (engine files under art/)

All art is procedural (PIL, `_w1_tools/v3/artgen.py`): the image-generation tool's outputs could not be reached from the box shell in this session, so they could not be copied into the level folder. No real people's faces - only cartoon bunnies, shapes and album motifs.

- `art/sky.jpg` - misty blue-grey morning sky
- `art/sky-dawn.jpg` - dawn backdrop for the final chorus/outro (section backdrop)
- `art/ground-halftone.jpg` - pale halftone ground
- `art/bunny-halftone-wall.jpg` - halftone bunny wall (court landmark face)
- `art/poster-frames.jpg` - five empty frames poster (arcade walls, billboards)
- `art/sticker-*.png` - heart / star / bunny / drop / window decals

layout.json `art`: backdrop `art/sky.jpg`, ground `art/ground-halftone.jpg`; section backdrops: Final chorus -> art/sky-dawn.jpg; image objects (posters/stickers): 17.
