# Art props (layout schema v2.7)

This is how a level places its Codex art (`levels-design/<slug>/art/`, copied to `public/levels/<slug>/art/` by `tools/build-levels.mjs`) in the 3D world. It is all data-driven from `layout.json`. Charts and gameplay are not affected: art props never sit on any road footprint, and they fade out whenever they would hide the head (and, for non-landmarks, the road just ahead).

The reference implementation covers Supernatural, How Sweet, Bubble Gum and Right Now. For each of them, `levels-design/<slug>/art-props.json` is the spec and `levels-src/<slug>/layout.json` holds the generated `art-*` objects plus `dressing`.

## 1. Object kinds

All paths are `art/<file>` relative to the level. `.png` sources are alpha-blended by default; `.jpg` sources are opaque. In every kind, the front of the art faces the object's local −z (see `face`).

| kind | size | what it is | colours |
|---|---|---|---|
| `standee` | `[w, h, post]` (default `[3, 3, 0.6]`) | An art card w×h standing on two posts of height `post`. With `post: 0` the card stands on the ground (good for png cut-outs). An opaque card gets a frame plate behind it. | `color` = frame, `color2` = posts |
| `facade` | `[w, h, d]` (default `[4, 5, 3]`) | A building block whose front wall carries the art (88 % × 78 % of the wall), with a roof slab. | `color` = walls, `color2` = roof |
| `decal` | `[w, 0, d]` (default `[4, 0, 4]`) | A painted floor decal or mural lying flat beside the road. It never fades because it can't hide the line. | `color` (opaque art only) = border plate |
| `image` | `[w, 0, h]` | The existing v2.4 textured quad (`mode` upright, flat or billboard). It now also accepts `uv`. | none |

Extra fields for all of these kinds:

- **`uv: [u0, v0, u1, v1]`** selects a sub-rectangle of `src` in image coordinates (0..1, top-left origin), so one image can act as a texture atlas. Example: the six pattern panels of How Sweet's `panels-poster.jpg` are six standees and facades using one shared material. Keep `size` at the crop's aspect ratio.
- **`glow`** is the emissive amount of the art: 0.25 for decals, 0.3 for facades, 0.4 for standees. Raise it for night levels.

## 2. Placement and orientation fields (any object)

| field | meaning |
|---|---|
| `t`, `side` | Route-anchored as before. The sign of `side` picks the side (+ = right of travel). |
| `near` | Near-road placement: `\|side\|` becomes road half-width(t) + `near` + the object's radius. It implies `hug`. |
| `hug` | Anchor to the actual road at `t` rather than the smoothed corridor. When `near` or `hug` is set, the off-road push-out also walks along the actual road in 0.75-unit steps. |
| `face` | Points the front (local −z) at something. `road`: toward the road point at `t`. `oncoming`: toward the line approaching from behind (mostly against travel, turned 30° toward the road), which suits the follow camera. `travel`: along travel. `camera`: yaw-billboard toward the camera every frame, with no per-frame allocation. `rot` is added on top. |
| `y` | Base offset relative to the road top. Art props normally use `-0.6`, the level the roadside dressing stands on. |

Prefer `t` / `side` / `near` over `worldPos` for art. The engine resolves the position against the real road, so the prop sits beside the stretch the camera follows when the line passes `t`. To get a prop on screen at time T, use t ≈ T + 0.3…1.4 s. Objects with `worldPos` are not pushed off the road.

Occlusion: standees and facades are tested with their projected screen box, not a bounding sphere. A prop fades to 12 % while it covers the head or the road 0.5/1.0/1.6 s ahead. With `landmark: true` it only fades while it covers the head.

## 3. Roadside dressing with art (`layout.dressing`)

```json
"dressing": {
  "colors": ["#efebe1", "#d9d4c7", "#ff5a1f", "#2a2a2a", "#7fb069"],
  "art": [
    { "src": "art/panels-poster.jpg", "uv": [0.203, 0.144, 0.335, 0.824], "as": "facade", "size": [2.2, 4.2, 2.2], "weight": 0.6, "scale": [0.8, 1.2], "scaleY": [0.7, 1.5] },
    { "src": "art/sticker.png", "as": "card", "size": [2.6, 1.3, 0.12], "weight": 0.8, "scaleY": [1, 1] }
  ]
}
```

- **`colors`** are the theme colours for the five default untextured props, in the order [light block, mid block, accent cube, dark block, foliage]. Sample them from the level's art. Missing entries fall back to the palette.
- **`art`** lists textured props that are appended to the default palette. If you write your own `props`, put textured entries straight into `props` instead (any entry with `src` is an art prop).
- Art prop fields:
  - `src` and `uv`.
  - `as`:
    - `facade`: a box with the art on its four sides and the roof sampled from the art's centre colour.
    - `card`: a thin upright panel.
    - `crate`: art on every face.
    - `tile`: a flat floor decal.
  - `size` [w, h, d].
  - `alpha` (default: `.png`).
  - `glow`.
  - `face`: `road` (default for facades), `oncoming` (default for cards) or `random` (default for crates and tiles).
  - The usual `weight`, `scale` and `scaleY`. Use `scaleY: [1, 1]` for cards and tiles so the art is not stretched.
- Performance:
  - Every prop type is a single thin-instanced mesh.
  - Art props share the cached per-image material (`Materials.textured`), so one image means one material, no matter how many props or uv crops use it.
  - Matrices are written with `ComposeToRef` into scratch objects, so there is no per-frame allocation.
  - Keep art images ≤ 1200 px.

## 4. Ground

- `art.ground`: `{ "src": "art/ground.jpg", "scale": 40, "tint": "#ffffff" }`. `tint` is optional. Without it, the tile is multiplied by `palette.ground` as before, which can mute the art. With it, the tile keeps the tint colour throughout, ignoring section palettes.
- `sections[].ground`: `{ "src": "art/ground2.jpg", "scale": 30 }`. Switches the ground tile at a section start. Textures are preloaded at load, and switching is a pointer swap.

## 5. Authoring helper

```
python3 tools/art/artkit.py <slug> levels-design/<slug>/art-props.json [--dry]
cp levels-src/<slug>/layout.json levels-design/<slug>/layout.json
```

`art-props.json` = `{ "objects": [ {<object fields>, "window": [t0, t1], "count": n, "reach": 4}, … ], "dressing": {…}, "art": {…}, "sections": [{"t": …, "ground": …}] }`.

For each object spec, the tool:

1. Picks `count` times inside `window`, preferring long straight runs at ground level.
2. Chooses the side with more free space, away from other road segments within ±6 height.
3. Writes `{id: "art-N", t, side, near: 0.8, y: -0.6, …}`.

It replaces previous `art-*` objects and changes nothing else; the route and chart are untouched.

Then:

- Run `python3 levels-design/validate.py <slug>`.
- Run `npm run build` (under `flock /workspace/.nj-heavy.lock`).
- Check the frames with `node tools/qa/play.mjs … --shots T1,T2 --shotdir D`.
