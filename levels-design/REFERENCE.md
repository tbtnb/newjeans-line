# Original Dancing Line reference — baseline & observations (integrator research)

Baseline chosen: **Dancing Line classic mobile (Cheetah Games / 猎豹), 2017–2018 versions (~v1.1–2.1)**, levels *The Piano* (钢琴, 125 BPM) and *The Autumn* (秋天). Primary motion source: a real 3-crown 100% portrait phone recording of The Piano (2018, https://video.zhouii.com/game/dancing_line/The_Piano.mp4, linked from https://www.zhouii.com/2018/07/519.html), frames extracted at 1 fps and 10 fps (repo: docs/reference/piano-frames/). Text sources: fandom wiki The Piano / The Autumn / Crowns, dlfm-wiki 秋天, readonly.wiki 가을 (tap-run counts), touchportal walkthrough.
Static frames + wiki text can't prove motion fidelity; the 10 fps strips do show camera follow and tap glow timing.

## Look
- Camera: high oblique (pitch ≈ 50–60°), yaw on the diagonal between the two travel directions, so the zig-zag climbs *up the screen*. Line head sits in the lower ~35–40 % of the screen; ~60 % of the screen is road ahead (look-ahead ≈ 2–3 s). Narrow-ish FOV, soft fog to a pale sky, no horizon clutter.
- Camera follows smoothly (no per-turn jerk: it tracks the mean diagonal, not the zig-zag). In section changes it rotates dramatically (Piano 55–62 %: camera swings to a side view, line moves left/right across the screen; then back to the classic view when the level returns to the keys at 80 %).
- Line: chunky square prism, saturated single colour (Piano: orange) on a paler road of the same hue family. The full trail stays visible behind. Head = cube.
- Road: either flat floor bounded by tall scenery blocks (Piano part 1: corridor between giant piano keys, keys bob with each tap) or raised platform blocks with shaded sides (inside the piano, part 2) floating over a void with huge radiating string-like beams. Road width varies a lot: wide at starts (≈2–3 line widths), narrow late (≈1.3–1.5). Width trend narrows through the level (Autumn).
- Percentage markers ("10%", "20%"…) are printed on world surfaces near the path — part of the scenery language.
- Palette: 1 hue family per level, soft lighting, long soft shadows, low-poly flat shading, generous negative space.

## Motion / map performance
- Scenery reacts to the player's taps (Piano keys press down on each tap) — feedback for actual taps, never previewing future ones.
- Roads rise from below/water just ahead of the line in late sections (Autumn 80–100 %: paths "spawn from the water", sometimes a fake branch rises too). Fall(s): line runs off a platform edge and drops to a lower road (Piano has 2 falls).
- Tap feedback: a soft white light puff/sparkle at the head on each turn (visible in 10 fps strips). No corner markers in the classic version (guidance lines were added only in a later update, as an option).
- Gems: small yellow/gold rotating gems on or just off the path; collecting = sparkle burst. Crowns: gold crown on/next to path at checkpoints (Piano 18/39/84 %, Autumn 25/60/100 %); passed crown leaves an outline. Checkpoint gift box (glass cube with a red heart) shatters into red shards when passed.
- End: line enters a tall light beam / pyramid, screen fades to white, then results.

## Flow / UI
- Level select: the level's own 3D diorama full-screen, thin geometric title, progress % bar, gem count x/10, three crown slots; swipe/arrows between levels. Start: finger icon pulsing at the bottom = "tap to start" (start only, not a timing hint). First tap starts both music and the line.
- In-play HUD: almost nothing (pause + small progress). No text over the road.
- Fail: line crashes (stops at a wall / shatters) or falls off; music stops; panel shows % reached + gems, retry; if a crown checkpoint was passed, option to continue from it (costs that crown and the gems after it).
- Results: grey translucent overlay over the scene, title, gems x/10, 3 crowns (gold for earned), progress bar "100%", hexagon-shaped buttons: back < , big replay ▶|, share. Confetti on full clear.

## Charting (how DL places taps) — follow this
- Taps sit on audible accents: piano/melody note onsets, kick/snare on 1/2/3/4, vocal syllables in hooks. The road geometry *is* the rhythm: a long straight = a held note/rest, a staircase = a run of 8ths/16ths.
- Density follows song energy: calm intros with 1–2 s gaps, choruses dense (8ths ≈ 0.24 s at 125 BPM), climax sections contain long runs (Autumn: 10-tap and 20-tap runs of 8ths; 15-tap run right before the end; "6-tap run where the first tap is half a beat late" = syncopation).
- Classic Piano average ≈ 96 CPM (1.6 taps/s), Autumn similar with peaks ≥ 4 taps/s. Hard levels peak > 5 taps/s in bursts.
- Difficulty also from: narrowing road, roads appearing late (rise just ahead), camera turns, falls, fake branches (we do not use fake branches unless clearly readable).
- Leave breathing gaps at section changes and around checkpoints.

## Our mapping (engine v2)
speed default 9 u/s with line width 1 (an 8th at 125 BPM ≈ 2.2 line widths — matches the staircase look in the recording); default camera preset `iso`; tap → soft glow at head only; road reveal modes rise/drop/unfold for the "map unfolds with the music" feel; react:"tap" for Piano-key style scenery; falls/jumps/ramps for layers; percentage markers on surfaces (engine adds 10 %..90 % automatically).

## Route choreography (user feedback 2026-10-18: routes must not be simple shapes)
Codex blueprints are loose mood references; the route design is ours. A Dancing Line map reads as choreography, not as a single zigzag:
- **Staircase clusters**: 6–20 alternating taps on 8ths form a diagonal stair; the camera frames it along the diagonal.
- **Zigzag corridors** between walls or pillars (scenery tight on both sides; road narrow).
- **Spirals / U-turns**: repeated same-direction taps (R,R,R,R…) wind around a landmark (tower, fountain, clock). Spiral up with a ramp so each lap passes over the previous one (≥ 3 units higher).
- **Switchbacks**: long straight, U-turn, long straight back alongside (keep ≥ road width + 1 apart, or on another level).
- **Multi-level crossings**: overpasses and underpasses, with the road passing under a bridge built earlier, or over the start area later. Drops (falls) at section downbeats, jumps onto floating platforms.
- **Wrap-through-buildings**: the road enters a building (walls on both sides, roof overhead → camera `high`/`top` or `side`), turns inside, and exits.
- **Landmarks seen twice**: a skyline object (`worldPos`) visible from several sections ties the map together.
- Vary the flow direction per section (rotation via repeated directions), so the level travels across the world instead of one diagonal.
- Readability first: dense clusters need a wide enough road (≥ 1.9), a clear camera (iso/high), and no scenery occluding the next 2 s of road.
