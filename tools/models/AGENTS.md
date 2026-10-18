# OMG concept C – low-poly model builder (Blender bpy scripts)

You build game-ready low-poly papercraft models for a Dancing-Line-style rhythm game level ("Bunny Pop-up Storybook").
Each model is ONE Python script `tools/models/assets/<id>.py` defining `build(P, spec)`; the pipeline builds it headless in Blender,
exports a glb, renders ortho front/side/top/iso and composes a compare sheet against the design sheet with metrics.

## Loop (per asset)
1. Read the design: `design/assets/<design>/` — `front.jpg side.jpg top.jpg` (orthographic three-view, same scale), `hero.jpg`
   (3/4 view), `views.jpg`, `spec.json` (size_m w/d/h in metres, tris_budget, parts, pivots+motions, colors = exact palette hexes).
   Kit items (G1–G4): `front.jpg` / `top.jpg` are 4x2 grids (order left->right, top->bottom = item index), `kit.jpg` is the 3/4 view,
   spec.json `items[i]` has en/cn, size_m (largest extent, m) and tris. `design/assets/ASSETS.md` has the shared palette.
   `tools/models/catalog.json` maps every engine id to its design dir (+ kit item index) and budget.
2. Write/modify `tools/models/assets/<id>.py`, run `tools/models/build.sh <id>` (from the workspace root).
3. LOOK at `deliverables/omg-c-models/<id>-compare.jpg` with your image viewer (rows: design views, model renders, overlay with the
   design silhouette outline in magenta) and read `build/<id>.metrics.json` (per-view silhouette IoU, aspect delta, mean colours,
   size delta, tris/budget). Fix what differs; repeat. Up to ~8 iterations per asset.

## Design notes (sheets final @ae37a1d)
- `size_m` is measured from the final three-views: build to it. `size_target_m` is the original game target (informational; the engine
  rescales by height). `views_check.note` holds the manual review notes – obey them:
  H12 flip phone: top view is slightly angled → take dimensions from front/side only (ignore top IoU, state it).
  P08 curtain screen / P21 flag string: thin objects (depth a few px) → side/top IoU is unreliable; match front + the top's fold line.
  P24 cloud: top view drawn slightly flat → follow front/side; top IoU only advisory.

## Acceptance (every asset)
- Silhouette matches in all three views: front & side IoU >= 0.85, top >= 0.80 (where the design's own views disagree with each other,
  follow front+hero and say so). Proportions/size within ±5% of spec size_m (kit: largest extent ≈ size_m).
- Tri use: heroes (H..) 60–90% of tris_budget; props (P..) 50–90%; kit items 50–100%. Never over budget.
  Spend the tris where they show: silhouette, faceting of organic shapes (bunnies, hearts, clouds: icospheres subdiv 2–3, lathes with
  10–16 segments, chamfered edges), ears with real thickness and folds (not flat cards), recognisable details from `parts`.
- Colour: use the spec `colors` hexes EXACTLY (and ASSETS.md palette names). Bright clean paper: cream/white parts stay cream/white,
  pinks stay pink. Flat per-face colours; facet variety only by alternating between two palette tones of the same part (e.g. cream
  #FFF3DE / paper #FFF8EC). Do not darken, tint or "age" colours yourself – the pipeline bakes a soft light (lit faces = exact hex,
  faces turned away ≥ 0.88x). Glowing parts (windows, bulbs, lamps) use the lamp/gold hexes.
- Pivots: every animated part listed in spec `pivots` gets an empty named `pivot_<kind><index>` at its joint, created with
  `P.pivot('<kind><index>', joint_location, [children])` (index optional). Kinds the engine animates:
  root (whole object; pops up from the page – always the top-level pivot, at (0,0,0)), heart / pulse (scale 1→1.12 on beats),
  ears (tilt back on beats), gate / lid (hinge open about local X after the pop), flag (wave about Z), tower (staggered scale-z pop),
  bob (up-down on beats), spin (rotate about Z: carousel, sun rays, top star), wheel (rotate about Y = front-back axis: ferris wheel,
  windmill sails, clock), swing (pendulum about X: lanterns, chimes, IV bag), hand (clock hand: step about Y each beat).
  Nest pivots when parts ride on others (a flag on a tower). Keep ≤ 12 pivot groups per hero (each group = one draw call),
  ≤ 3 for props, none (root only) for kit items. Static parts go directly under root.

## Conventions
- Blender Z-up, metres. FRONT faces -Y (front view looks along +Y), side view = seen from +X (right side), top = from +Z with the
  front at the bottom of the image. The object stands on z = 0, footprint centred on x = y = 0. Exactly match spec size_m:
  w = X extent, d = Y extent, h = Z extent.
- Kit API is in `tools/models/paper.py` (read it): box, cyl (cone if r2=0), ico, prism (XZ outline extruded along Y), card, lathe,
  blade, outlines ellipse/heart/star/ear, pivot, join, mirror_x, mix, paint; colours may be hex strings or callables (center, normal)->hex.
  You may define helper functions inside your own script. `spec` is passed into build(); read sizes from it rather than hard-coding.
- Each script starts with a docstring: design id + name, size, budget, pivots, and a `SIMPLIFICATIONS:` line listing anything
  deliberately simplified vs the sheet (e.g. glow, text, tiny details below 2 cm, thin strings as single quads).

## Boundaries
- Write ONLY `tools/models/assets/<your ids>.py`, `build/`, `public/models/omg-c/<your ids>.glb`,
  `deliverables/omg-c-models/<your ids>-compare.jpg`, and your summary file. Never edit paper.py, run.py, compare.py, build.sh,
  catalog.json, the design folder, or another worker's assets. Never touch anything outside this workspace folder, never kill
  processes, never install software, no network (gltfpack is already cached for npx).
- When done write `build/summary-<worker>.md`: one line per id: tris/budget (%), IoU front/side/top, size delta, simplifications.
