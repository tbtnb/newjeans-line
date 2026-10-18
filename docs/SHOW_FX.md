# Show visuals: `layout.fx` (schema v2.8)

`src/render/showfx.ts` is wired into `world.ts` through small hooks: construct at load, `update()` per frame, `dispose()` at unload. It also hooks `road.ts` (`onFlush`, `topBuffer`).

It is off unless a level sets `layout.fx`. It doesn't touch the camera rig or the head; it only reads `scene.activeCamera` through the scene, so it works with any camera choreography.

Quality `low` disables the glow layer and vignette, and cuts sparkles to 40 %. Quality changes take effect on the next level load.

```json
"fx": {
  "exposure": 1.0, "contrast": 1.05,
  "vignette": { "weight": 1.2, "color": "#1c1440" },
  "glow": { "intensity": 0.9, "kernel": 48 },
  "keys":     [ { "t": 45.36, "exposure": 1.08, "contrast": 1.2, "glow": 1.1, "blend": 1.2 } ],
  "pulse":    [ { "t": 45.36, "t1": 60.48, "amount": 0.18 } ],
  "flashes":  [ { "t": 45.36, "dur": 0.6, "amount": 0.5, "sparkle": true } ],
  "beams":    [ { "t0": 45.9, "t1": 60.0, "every": 1.1, "colors": ["#ff9ad5", "#9fd8ff"], "height": 45, "near": 3.5 } ],
  "sparkles": [ { "t0": 45.36, "t1": 60.48, "density": 4, "colors": ["#fff3c4"], "size": 0.9, "spread": 12, "height": 9 } ],
  "road": { "gloss": 0.5, "trim": "#ffd27a", "trimGlow": 0.9 },
  "sprite": "art/v2/sparkle.png"
}
```

- **Grading** (`exposure`, `contrast`, `vignette`): uses the scene `ImageProcessingConfiguration`, which is applied inside the material shaders. There is no post-process pass, so the transparent canvas over the CSS sky backdrop keeps working. `keys` re-grade from `t` on, blended over `blend` seconds.
- **`pulse`**: beat-reactive exposure pulse driven by `layout.beats` between `t` and `t1`.
- **`flashes`**: exposure flash on drops, plus a star burst at the head (`sparkle: false` disables the burst).
- **`glow`**: a `GlowLayer` (35 % resolution) that halos only the meshes that opt in: road trims, beams, and objects with `glowfx: true`.
- **`beams`**: stage searchlights.
  - Placement: one every `every` seconds of route, alternating sides, `near` units off the road edge, never on any road footprint.
  - Timing: they rise in 2.2 s ahead of the line, the same lead as the dressing, so they never reveal the route earlier than the road itself does. They are gone 15 s after.
  - Motion: they sweep with time and pulse width and alpha on the beat.
  - Rendering: one thin-instanced additive mesh per colour.
- **`sparkles`**: twinkling glow sprites beside and above the road. They are static particles in one additive `ParticleSystem`, appear with the road lead, and swell on the beat.
- **`road`**:
  - `gloss` is the specular sheen on the road top.
  - `trim` gives glowing edge lips that share the road-top instance buffer, so they reveal and animate exactly with the tiles and need no extra matrix work.
- **`sprite`**: texture for the sparkles (default: a soft radial dot).

Per-section lighting, fog, sky and particles still come from `sections[].palette`, blended over 1.6 s. Backdrop and ground switching use `sections[].backdrop` and `sections[].ground` (v2.7). Set pieces use objects plus events:

- `raise` / `lower` with `dy` (for example, the giant bunny rising behind the stage);
- `light` with `every` (phone screens lighting up one after another on "Oh my god");
- `spin`;
- `burst`;
- `react: "beat"` (props bouncing on the beat).

Performance:

- Scratch vectors and matrices; no per-frame allocation in showfx.
- Shared materials, one per colour or image.
- Instanced beams and trims; sparkles are one particle system.

## OMG v2 pipeline (route-relative)

```
python3 tools/art/omg_art.py          # Codex originals (levels-design/omg/art-v2) -> runtime sizes in art/v2
python3 tools/art/omg_scene.py        # themes/fx/dressing/set pieces from chart sections -> levels-design/omg/art-props.json
python3 tools/art/artkit.py omg levels-design/omg/art-props.json                       # levels-src layout
python3 tools/art/artkit.py omg levels-design/omg/art-props.json --root levels-design  # design copy
```

Re-run the last three after a re-chart.

- Themes are assigned by musical role: intro → dream, verse → ward, the section before a chorus → rise, chorus → stage, the last choruses → finale, bridge → garden, outro → calm.
- Every prop is placed by time window plus side plus `near` against the current route.
- `artkit` only replaces `art-*` objects (and keeps `fakefork*`), `dressing`, `fx`, `events`, `palette` and the section theme fields. The route, chart, camera, diamonds and finish are untouched.

## Corridor scenery (schema v2.9, `layout.corridor`, src/render/corridor.ts)

For long forward routes: big set pieces that line both sides of the road and repeat in time with the music, so there is always something lavish in frame.

- **`items`**: `{src, size:[w,h], glow, float, lights:'beat'|'chase'|'none', flat, tilt}`. Upright items are camera-facing quads that lean toward the camera (`tilt`, default 0.5). `flat` items are floor emblems. `chase` splits the instances into two groups lit on alternate beats.
- **`bands`**: `{t0, t1, every, phase, near:[min,max], items:[...], sides:2|1, mirror, y:[min,max], scale}`. One placement every `every` seconds (the OMG generator uses bar lines). The offset is measured across the corridor from the actual road at t (so pieces stand left/right of the line, never ahead of it), then pushed out until clear of every road segment (RoadGrid; radius ≥ 0.36 × height for tall pieces).
- **`floor`**: glowing dots in strips beside the road that chase forward with the beat (4 phase groups).
- **`fireworks`**: bursts high above the band at given times (one particle system).
- `lead` / `tail`: pieces rise in `lead` s before the line arrives and stay `tail` s after it. Only instances in that window are written each frame (compacted thin-instance buffers, no per-frame allocation); `maxActive` caps each layer; `quality: low` keeps every other placement.

OMG: `tools/art/omg_scene.py` builds the corridor per section theme (towers + phones in verses, towers + spotlight rigs in pre-choruses, towers/arches/rigs/balloons in choruses, curtains, giant bunnies and fireworks in the final choruses, moon flowers/lanterns/crescent moons in the bridge garden). `revealLead` in the spec raises every road reveal lead (2.8 s) so more road ahead is visible.
