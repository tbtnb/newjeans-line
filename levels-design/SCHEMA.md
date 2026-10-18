# NewJeans Line v2: level data schema (v2.5)

Owner: the integrator (the assistant that maintains the `rebuild` branch). This file is the contract between design workers and the engine.
Canonical copy: `levels-design/SCHEMA.md` on branch `rebuild` of tbtnb/newjeans-line. A mirror lives at `/workspace/newjeans-line-designs/SCHEMA.md`.
Recreated on 2026-10-18 after the box reset. The content matches v2.2 plus the additions marked v2.3 and v2.4 below.

## Where to put your work (after the reset)
- Branch from `origin/rebuild` and push to **`designs-wN`** (N = your worker number). Commit early and push after every song.
- Put files **only** under `levels-design/<slug>/`:
  - `chart.json`: required.
  - `layout.json`: required.
  - `design.md`: required (concept, sections, landmarks, eggs, chart rationale, per-section density, sync notes).
  - `analysis.json`: optional (your analysis output).
  - `art/`: optional images (see "Art assets").
  - `route.png` / `preview.png`: optional. Do not commit huge files; keep each image ≤ 1.5 MB, PNG or JPG, at most 2048 px.
- Do not touch `src/`, `tools/` or anything else. The integrator copies `levels-design/<slug>/{chart,layout}.json` into `levels-src/` and builds them.
- Validate before you push: `python3 levels-design/validate.py <slug> --dir levels-design`. Zero `ERROR` lines are required.
- Slugs: attention, hype-boy, cookie, hurt, omg, ditto, new-jeans, super-shy, eta, cool-with-you, get-up, asap, how-sweet, bubble-gum, supernatural, right-now.
- Audio: `public/audio/<slug>.mp3` in the repo. Never modify it. Shared analysis candidates are in `analysis/<slug>.json` (librosa, made with `levels-design/analyze.py`), with a constant-tempo grid where one exists in `analysis/<slug>.grid.json`.
- Timing reference: song time 0 = first decoded sample of the mp3 as the browser decodes it (gapless; the same as librosa `load` on this file). htdemucs stems come out **25.03 ms late** relative to that, so correct for it if you analyse stems.

## Coordinates and motion (what the engine does)
- Units: the line is 1 × 1 (width × height). Default speed is **9 u/s**. Babylon left-handed, y up, **N = +z, E = +x**. The start position is the origin; `startHeading` defaults to N.
- Every tap turns the line 90°. `dir: "R"` turns clockwise (seen from above), `"L"` counter-clockwise. Without `dir` the turns alternate R, L, R, … (starting with R).
  - Right vector for heading (hx, hz) = (hz, -hx).
- Geometry is fully determined by `taps[].t`, `taps[].dir`, `speed` and `elevation`. The road is built exactly on that centreline, so you cannot place the road anywhere else.
- Repeating a direction rotates the flow. R, R = U-turn; R, R, R, R = a square spiral. Use this for spirals, switchbacks and loops.
- **Self-crossing is allowed only on different levels.** Two road parts may overlap in plan only if their heights differ by ≥ 3 units (bridge/overpass) **or** they are < 1.5 s apart (adjacent stair steps merging into one band, as in Dancing Line). The validator enforces this.
- Multi-level: road tiles are drawn at their own heights, and scenery collision (push-out) is height-aware. Judging is time-based, so a crossing never kills the player by itself. The road you cross over stays visible below.
  - The camera follows the head's height smoothly. When it is about to pass under a higher deck, put a camera cue there (`high` or `top`, or a `side` yaw) so the deck does not block the view.

### Elevation (v2.3 air-time rule, engine-enforced)
```json
"elevation": [ {"type":"fall","t":55.945,"dy":-3}, {"type":"jump","t":80.0,"dy":3}, {"type":"ramp","t0":91,"t1":98,"dy":8} ]
```
- `fall` (dy < 0) and `jump` (dy > 0) start a ballistic flight at `t`.
  - Natural flight times: fall ≈ 0.45–0.65 s (vy 2, g 30); jump 0.6 s.
  - **The engine shortens the flight so the line lands 50 ms before the next tap** (steeper parabola, never shorter than 0.15 s). **No tap ever happens in mid-air.**
  - Design rule: leave ≥ 0.35 s between a fall/jump and the next tap. The validator reports a shorter gap as an ERROR because it looks wrong.
- `ramp`: a linear height change from `t0` to `t1`. Taps are allowed on ramps (staircases going up).
- The ground plane follows the lowest road height reached so far (falls go down into the world; climbs leave the ground below).

## chart.json
```json
{
  "id": "ditto",
  "startHeading": "N",
  "speed": [ {"t": 0, "v": 9.0}, {"t": 141.8, "v": 10.0} ],
  "taps": [ {"t": 3.876, "dir": "R", "tag": "kick"}, ... ],
  "sections": [ {"t": 0.293, "label": "Intro · 雪原", "kind": "intro"}, ... ],
  "notes": "free text"
}
```
- `taps[].t`: seconds of song time, 3 decimals, strictly increasing.
  - Minimum gap **0.105 s** (ERROR below that; v2.5). Dense runs at 8ths (≈ 0.22 s at 134 BPM) are normal. **Short 16th-note bursts (gaps ≈ 0.11–0.13 s, 3–8 taps, peak ≈ 400–460 CPM)** are wanted where the audio clearly has them: drum fills, hi-hat/snare rolls, rapid vocal syllables. They must never be used on silence or as filler.
  - Calibration from the original game (dlfm-wiki.top): The Racing has 357 taps in 2:24 (2.48 taps/s, average 220 CPM, peak 440). Chaos peaks at 408 CPM, Amusement Park at 512 CPM, and Chinese Garden's narrowest window is ±45.8 ms. Our overall densities already match; the peaks should reach about 400–460 CPM in the hardest sections.
  - First tap ≥ 1.0 s. Last tap ≤ duration − 1 s.
- `tag`: kick | snare | clap | hat | vocal | melody | bass | fx | accent (informational; used in reports).
- `kind` of a section: intro | verse | pre | chorus | post | drop | bridge | break | outro.
- Extra keys (`bpm`, `grid`, `meta`, `judgment`, ...) are allowed and ignored by the engine.
- **Judging (engine, v2.5 per-tap):** window = min(0.5·g, clamp(0.45·g, 0.045, 0.11)) s each side, where g = min(gap to previous tap, gap to next tap). A 0.11 s burst gets ±49.5 ms, 8ths at 0.22 s get ±99 ms, and sparse taps get ±110 ms. Neighbouring windows never touch, so one tap can never count twice. PERFECT is ±0.04 s. Duplicate events within 0.045 s are ignored.
  - An early tap outside the window, a tap with nothing to hit, or no tap by the deadline = fail.
  - A late failure is shown 0.15 s after the deadline. That is input-latency grace, not a bigger window.
  - Road width does **not** change the window. Road width is purely visual and difficulty-feel.
- Charting rules (user requirements): taps on audible accents (kick/snare/clap backbeats, vocal syllables in hooks, melody runs). Density follows energy. Breathing gaps at section changes and checkpoints. Aim for about 1.5–2× the legacy tap count without inventing taps on silence.

## layout.json
```jsonc
{
  "id": "ditto", "title": "Ditto",
  "palette": { "skyTop":"#b9cde0","skyBottom":"#eef1f4","fog":"#e9edf1","fogStart":35,"fogEnd":110,
               "ground":"#d5dee8","groundY":-5,"road":"#ffffff","roadSide":"#8ea2b9","line":"#2f4f7a",
               "light":"#fff8ee","lightIntensity":1.0,"ambient":"#c3cfdc","particles":"snow" },
  "road": {
    "width":  [ {"t":0,"w":2.6}, {"t":141.8,"w":1.75} ],          // step function; 1.6–3.0 sensible
    "height": 0.7,                                                 // slab thickness
    "reveal": [ {"t":0,"mode":"rise","lead":2.4} ]                 // rise | drop | unfold | fade | static; lead = s before the line arrives
  },
  "elevation": [ ... ],
  "sections": [ {"t":14.6,"label":"Hook 雪林","palette":{"skyTop":"#a9c2da"},"camera":"iso","note":"..."} ],   // partial palette, blended over ~1.5 s
  "camera": [ {"t":0,"preset":"wide","blend":0}, {"t":7.458,"preset":"iso","blend":4.5},
              {"t":40,"preset":"side","yaw":72,"blend":2}, {"t":60,"worldYaw":45,"pitch":60,"dist":35} ],
  "objects": [ ... ], "events": [ ... ],
  "diamonds": [ {"t":14.96,"side":0} ],     // exactly 10; side = lateral offset (keep |side| ≤ road half-width so it is collectable)
  "crowns":   [ {"t":55.875} ],             // exactly 2 checkpoints (the 3rd crown = finishing without using checkpoints)
  "finish":   { "kind":"pyramid" | "gate" | "custom", "color":"#hex", "parts":[ ...Part ] },
  "collectibleColors": { "diamond":"#hex", "crown":"#hex" },   // v2.3, optional
  "art": { ... }                                               // v2.4, optional, see below
}
```
- Extra keys (`path`, `route`, `debugXZ`, `node_format`, `note`, `worldPosNote`, ...) are allowed and ignored.

### Camera
- Presets (pitch°/distance/fov°): iso 52/31/36 (classic DL), high 64/38/36, low 32/24/42, side 42/31/38 with yaw +72, top 80/42/36, wide 46/50/40, close 46/21/40.
- `yaw` is degrees **relative to the auto flow direction**. Flow = displacement from t−1.2 s to t+2.8 s, so a dense staircase is framed along its diagonal, not per step.
- `worldYaw` is absolute (0 = looking toward +z).
- `pitch`, `dist`, `fov`, `roll`, `shake`, `lead` override the preset. `blend` = seconds to ease in.
- The camera always looks 0.45 s ahead of the head. Portrait screens get a slightly larger distance automatically.

### Objects
Anchored to the centreline at time `t`:
- `side` = lateral offset (+ = right of the mean travel direction);
- `along` = offset along travel;
- `y` = height above the road at t.

Objects with `side ≠ 0` are anchored to the **mean corridor** (flow frame), so a zigzag does not shake them. Objects that would intersect the road are pushed outward automatically (height-aware), except `onroad` / `worldPos` objects.
```jsonc
{ "id":"camcorder", "t":2.0, "side":-9, "along":0, "y":0, "kind":"group", "landmark":true, "egg":false, "name":"Banhee 的摄像机",
  "size":[w,h,d], "rot": 15 | [rx,ry,rz], "color":"#hex", "color2":"#hex",
  "parts":[ {"kind":"box","pos":[0,0,0],"size":[3,3,5],"rot":[0,0,0],"color":"#3b3f4a","texture":"art/tape.png"} ],
  "appear":{"t":1.0,"mode":"rise|drop|pop|grow|unfold|fade","dur":0.7}, "exit":{"t":30,"mode":"sink|fall|shrink|fade","dur":0.7},
  "react":"none|beat|tap|kick",
  "worldPos":[x,y,z],     // v2.3: absolute placement (then rot = absolute yaw); use for skyline landmarks and things seen from several sections
  "onroad":true,          // v2.3: bridge decks / slabs under or on the road: never pushed out
  "radius":1.6 }          // v2.3: collision radius for push-out (groups default 1.5)
```
- Kinds:
  - primitives: box, cylinder, cone, sphere, torus, plane, disc, pyramid;
  - `text`: a flat label lying on the ground (text = `name`; size [w,0,h]);
  - prefabs: tree, pine, cloud, building, tower, arch, pillar, lamp, flower, heart, star, note, bubble, rock, bridge, stairs, water, moon, sun, ring, crystal, cassette, phone, bench;
  - `group` (with `parts`);
  - `row`: `{kind:"row", t0, t1, spacing, side, bothSides, item:{...object}}`, repeated along the corridor and auto-skipping items that would hit the road;
  - `image`: v2.4, see "Art assets".
- `react` is feedback only. `tap` fires on the player's actual taps (like piano keys), never before a tap. `beat`/`kick` follow the music grid.
- Percentage markers 10–90 % are added by the engine. Do not add them.

### Events
```jsonc
{ "t": 71.948, "type": "flash", "amount": 0.4 }
```
| type | fields | effect |
|---|---|---|
| pulse | target, every, until | targets bounce on a period |
| raise / lower | target, dy, dur, converge (0–1, v2.3) | persistent move (stays moved); `converge` drifts targets toward their common centre (e.g. two lights meeting) |
| spin | target, speed (rad/s), until | rotate |
| shake | amount, until | camera shake |
| flash | amount | white screen flash |
| burst | at:"player" or target, color, amount | particle burst |
| light | target, every, level (0–1), color, dur, until | targeted objects glow (one after another with `every`); stays on unless `until`. Without a target it brightens the sun |
| color | palette (partial), dur | palette transition |
| particles | particles: snow, petals, leaves, bubbles, stars, dust, rain, confetti, pixels, or null; until | override the ambient particles for a time span |

**Forbidden (user requirement): any tap hint.** That means no corner markers, no next-tap flashes, pulses or countdowns synced to upcoming taps, no "tap now" text and no guide lines. Events may follow the music (beats, sections) but must never mark where or when the next turn is.

## Roadside dressing (v2.6, engine)

The engine fills both sides of every ground segment with small set-dressing props (DL-style buildings/trees/blocks 0.4–4 units off the road edge). It is **on by default** for every level; tune it in `layout.json`:

```json
"dressing": {
  "density": 3.6,              // props per 10 road units per side
  "near": [0.4, 4],            // gap from road edge (units)
  "lead": 2.6,                 // s ahead of the line when props pop in (rise with overshoot)
  "bounce": 0.12,              // beat bounce (uses layout.beats) for props within 2.5 s of the line
  "seed": 7,
  "props": [ { "kind": "box", "size": [1.8,2.6,1.8], "color": "#F3F0E8", "weight": 3, "scale": [0.7,1.3], "scaleY": [0.6,2.2] },
             { "kind": "group", "parts": [ ... ], "weight": 1 } ],
  "sections": [ { "t": 41.2, "density": 6, "props": [0, 2] }, { "t": 90, "off": true } ]
}
```
or `"dressing": false` to disable. Without `props`, a palette is derived from `palette.road / roadSide / ambient / ground / line`. Props use flat part colours (no textures). Placement is deterministic, never on any road footprint (incl. upper/lower decks), never overlapping each other or authored objects; anything that would cover the head or the road just ahead shrinks away.

## Art assets (v2.4)
Put images in `levels-design/<slug>/art/` and reference them by the relative path `art/<file>`. The build copies them to `public/levels/<slug>/art/`.
- `layout.art.backdrop`: `"art/sky.jpg"`. A full-screen image behind the 3D scene, replacing the CSS gradient. It should be soft and low-contrast so the road reads. A section can switch it: `sections[].backdrop`.
- `layout.art.ground`: `{"src":"art/ground.png","scale":40}`. A tiled texture on the ground plane.
- `layout.art.road`: `{"src":"art/tile.png"}`. Optional texture on the road top. Keep it subtle; the line must always contrast.
- Object kind `image`: `{ "kind":"image", "t":..., "side":..., "src":"art/poster.png", "size":[w,0,h], "mode":"upright|flat|billboard", "alpha":true }`. A textured quad: upright faces the road, flat lies on the ground, billboard faces the camera. Use it for posters, murals, cut-out silhouettes and decals.
- `parts[].texture`: `"art/x.png"`. Texture on a primitive part.
- Use GenerateImage for these (soft low-poly / flat-illustration style matching the palette). No text inside images unless the text is part of the scene (signs). Never draw arrows or anything that could read as a tap hint.

## Changelog

- v2.6: `layout.dressing` roadside dressing (engine-placed props, on by default).
- v2.0: base schema. v2.0a: shared analysis. v2.1: relative `yaw`/`worldYaw`, kinds `pyramid`/`text`, auto % markers, rows auto-skip.
- v2.2: overlap rule (error only if ≥ 1.5 s apart and height difference < 3).
- v2.3 (2026-10-18): `worldPos`, `onroad`, `radius`, `collectibleColors`, finish `gate`/`custom` + `color`, `particles` event, targeted `light` (every/level/color), persistent raise/lower + `converge`. **Air-time rule:** the engine shortens flights to land 0.05 s before the next tap, and the validator requires ≥ 0.35 s. Judging is grace-based on event timestamps.
- v2.5 (2026-10-18): minimum gap 0.105 s (16th bursts allowed), per-tap judgment windows ≤ half the local gap (floor 45 ms), and the validator prints peak and average CPM.
- v2.4 (2026-10-18): art assets (`art.backdrop`, `art.ground`, `art.road`, kind `image`, `parts[].texture`, `sections[].backdrop`). Workers commit to `designs-wN` under `levels-design/<slug>/`.
