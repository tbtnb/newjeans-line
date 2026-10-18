# Supernatural Chrome

Slug: `supernatural`

A small liquid-chrome cube leads a solid brushed-silver ribbon through sharp right-angle turns. Broad aqua, peach and lavender reflections give the mirror finish a soft holographic shimmer, while electric-blue and neon-violet bevels keep the silhouette readable against the level. Each turn releases a compact flash of four-point Y2K stars and silver droplets; death breaks the cube into reflective fragments with a wider sparkling scatter. The finish is clean, cute and original, with no logos, lettering or human imagery.

## Exact palette

Hex values are sRGB authoring colors. Apply the renderer's normal color-space conversion before lighting; emissive multipliers below apply in linear space.

| Role | Hex | Use |
| --- | --- | --- |
| Head base | #DCE5F0 | Cool liquid-chrome silver |
| Head shadow/reflection | #677B96 | Broad reflected bands that preserve the cube shape |
| Head accent/emissive, primary | #3A9FFF | Electric-blue bevels |
| Head accent/emissive, secondary | #9165FF | Neon-violet opposing bevels |
| Trail base | #B9C9DD | Brushed chrome beneath the texture |
| Trail edge/stitch, primary | #3A9FFF | Continuous blue edge line |
| Trail edge/stitch, secondary | #9165FF | Continuous violet edge line; no literal stitching |
| Burst particle color 1 | #BDEFFF | Ice-blue star tint |
| Burst particle color 2 | #D9C7FF | Lavender star tint |
| Death particle color 1 | #EDF5FF | Silver-white fragments and droplets |
| Death particle color 2 | #9165FF | Violet sparkle tint |
| Picker UI accent | #3A9FFF | Selection outline and focus accent |
| Holographic sheen, aqua | #BDF8EE | Broad pastel reflection |
| Holographic sheen, peach | #FFD5BE | Broad warm reflection |
| Holographic sheen, lavender | #E6DEFF | Broad cool reflection |
| Specular highlight | #F5FAFF | Small white highlights |

## Babylon.js material recommendations

These are starting art settings, to be tuned under the game's actual lighting. Use a soft studio/environment reflection with large bright and dark regions so the chrome stays legible. A subtle bevel on the cube catches its rim; retain flat major faces and a solid opaque trail.

### PBR option

| Surface | Metallic | Roughness | Emission | Alpha |
| --- | --- | --- | --- | --- |
| Cube chrome | 1.00 | 0.14 | 0 on body | 1.00 |
| Brushed trail | 0.95 | 0.30 | 0 on body | 1.00 |
| Blue/violet rim strips | 0.35 | 0.20 | Palette rim color × 0.85 | 1.00 |
| Chrome droplets/fragments | 1.00 | 0.18 | 0 on body | 1.00 |

Keep environment intensity near 1.0 as a starting point. Use narrow dedicated rim geometry or a rim mask; do not make the entire chrome body emissive. A restrained glow pass may use intensity 0.30, with only rim meshes included. Keep the halo narrower than roughly 5% of a cube width. The rainbow colors belong in broad reflection/albedo accents; emission is reserved for blue/violet edges.

### StandardMaterial fallback

- Cube: diffuse color #DCE5F0 at approximately 0.70 strength, specular color #F5FAFF, specularPower 256, reflection texture level approximately 0.90, emissive black, alpha 1.00.
- Trail: diffuseTexture = trail.png with white diffuseColor to preserve its authored colors; specular color #EDF5FF, specularPower 96, reflection level approximately 0.55, emissive black, alpha 1.00.
- Separate rim strips: diffuse blue/violet, specularPower 128, emissiveColor equal to the chosen rim color × 0.65, alpha 1.00.
- This fallback approximates chrome through reflections and sharp highlights; it has no physical metallic parameter.

Use repeat wrapping in U and V for trail.png, with its horizontal brushed grain aligned to each straight trail segment's travel direction. Start with one tile per four cube widths. Rotate the segment UV basis at each 90-degree turn and use a clean miter at the elbow. Put the continuous neon boundary lines on separate narrow geometry so texture repetition does not create intermittent borders. The trail remains a solid bar, with no transparency.

## Particle behavior

All distances below use the head cube width as one world unit. Use particle.png for the single star sprite; use small pooled procedural mesh droplets and fragments for the chrome elements, with no additional image assets.

| Event/component | Count per event | Size | Lifetime | Initial velocity | Gravity | Shape |
| --- | --- | --- | --- | --- | --- | --- |
| Turn stars | 7 | 0.10–0.22 | 0.18–0.32 s | 0.6–1.4 units/s | 0 | Four-point sprite |
| Turn droplets | 3 | 0.05–0.09 | 0.22–0.36 s | 0.5–1.1 units/s, with slight lift | 0.8 units/s² downward | Silver sphere/short teardrop |
| Death stars | 12 | 0.12–0.28 | 0.35–0.65 s | 1.0–2.2 units/s | 0.4 units/s² downward | Four-point sprite |
| Death chrome fragments | 16 | 0.08–0.20 | 0.45–0.85 s | 1.2–2.8 units/s | 3.0 units/s² downward | Beveled cube shards |
| Death droplets | 8 | 0.05–0.12 | 0.40–0.75 s | 1.0–2.4 units/s | 2.0 units/s² downward | Silver spheres/teardrops |

Turn: emit once at the elbow, offset just above the trail. Spread along the horizontal plane around the turn, with modest upward lift on droplets; avoid obscuring the cube. Alternate the two burst tints. Stars grow from 70% to full size over the first 15% of life, then shrink to 20%; fade alpha from 1 to 0 over the final 70%. Rotate stars slowly, approximately ±1.5 radians/s. Use normal alpha blending to retain the star silhouette; optional low-strength additive glow can be applied separately.

Death: hide the intact head and emit one 36-element burst. Spread radially with upward velocity of 0.6–1.5 units/s. Fragments tumble at 3–7 radians/s; droplets stretch slightly along velocity. Assign silver-white to chrome meshes and alternate silver-white/violet star tints. Keep chrome mesh alpha at 1 through the first 65% of life, then fade; stars fade earlier. Disable collisions for these short cosmetic effects. Pool emitters and meshes; do not emit a sustained death fountain.

## Assets and validation

- concept.png: 1536 × 1024 RGB, 3:2 landscape concept sheet with cube, right-angle trail, turn burst, death shatter and five flat swatches.
- trail.png: 1254 × 1254 RGB, flat repeating brushed holographic chrome surface, generated with seamless repetition requested in both axes.
- particle.png: 1254 × 1254 RGBA, one four-point star.
- icon.png: 1254 × 1254 RGBA, cube with a short attached trail stub.
- The actual generator output dimensions above supersede the requested dimensions in the prompts.
- Python 3 + PIL verified both transparent PNGs are RGBA and all pixels in each 16 × 16 corner block have alpha 0. Native transparency succeeded; no magenta-background regeneration was needed.
- All four images were generated with the built-in image_gen tool, exactly one call per image, and copied without image edits from the generated_images directory into their exact final filenames.
- Review used the full-size images and numeric image checks; no Babylon.js runtime render is included.

## Exact image_gen prompts

### concept.png

transparent_background: false

```text
Use case: stylized-concept.
Asset type: original casual rhythm-game skin concept sheet, landscape 3:2, 1536x1024.
Design: Supernatural Chrome, a cute clean Y2K liquid-mirror chrome cube and trail, holographic pastel rainbow reflections with electric-blue and neon-violet luminous fine rims. Crisp geometric silhouettes, soft gradients, tasteful polished toy-like 3D rendering.
Scene: clean very pale cool ivory studio background, generous space between the groups. Composition: large chrome head cube in three-quarter isometric view on the left; a separate solid rectangular chrome ribbon trail with exactly one crisp 90-degree elbow in isometric view across the upper right, same bar width throughout, subtly brushed top with iridescent sheen and thin blue/violet edge lines. Lower middle: one compact tap/turn burst of four-point Y2K star sparkles and a few chrome droplets. Lower right: separate larger death shatter scattering chrome cube fragments, chrome droplets and four-point neon stars. Bottom left: one neat horizontal row of exactly five flat circular color swatches, silver, electric blue, neon violet, pastel aqua, pastel peach. No surrounding boxes or labels.
Head: recognizable small-game-player cube, planar faces with gently rounded bevels, liquid silver reflective surface, abstract pastel reflections only, thin electric-blue and violet neon rim; no face. Palette chrome #DCE5F0, electric blue #3A9FFF, violet #9165FF, pastel aqua #BDF8EE, pastel peach #FFD5BE; bright white highlights.
Constraints: entirely original design; no official logos, brand marks, people, faces or likenesses; absolutely no text, letters, numbers, typography, watermark, UI, captions or arrows. Swatches are plain solid colors. Keep all objects comfortably inside canvas.
```

### trail.png

transparent_background: false

```text
Use case: stylized-concept.
Asset type: square 1024x1024 seamless repeating game material texture, for the top surface of a chrome ribbon trail.
Primary request: a flat orthographic top-down brushed liquid-chrome silver texture, with an extremely fine horizontal brushed grain and gentle iridescent holographic pastel rainbow interference. Predominantly light chrome silver #DCE5F0 and cool #B9C9DD, subtle washed aqua #BDF8EE, pale lavender and pastel peach #FFD5BE across broad soft low-contrast bands. A few delicate electric-blue #3A9FFF and violet #9165FF parallel hairline accents running continuously from the left edge to the right edge, integrated into the brushed material. Even lighting across the entire image; clean cute Y2K casual-game style; soft gradients, crisp fine grain.
Critical: mathematically seamless tile appearance in BOTH x and y: all patterns smoothly continue on the opposite borders; uniform fine grain and periodic broad color changes. No border, no edge frame, no top/bottom edge trim, no isolated details, no focal point. Fill the entire square with material.
This is a FLAT TEXTURE, no object, no rendered ribbon, no cube, no scene, no perspective, no depth bevels, no shadows, no vignette, no bright light hotspot. No stars or droplets. Original material only; no logos, people, faces, text, letters, numbers, watermark.
```

### particle.png

transparent_background: true

```text
Use case: stylized-concept.
Asset type: square 1024x1024 transparent particle sprite for a casual Y2K rhythm game.
Primary request: exactly ONE single bold four-point Y2K sparkle star, centered, spanning 80 percent of the canvas width and height, the four points aligned up, down, left and right. One connected solid silhouette with graceful concave curves between the points and a generous thick center so it reads cleanly at 32 pixels. Pearly white/chrome-silver center #F5FAFF, very subtle ice-blue shading #DAEFFF and pale lavender shading #E6DEFF, a restrained slim electric-blue/violet reflective rim. Soft crisp beveled shading only, cute polished game art. Primarily near-white so runtime color tint remains effective. Symmetric shape; no interior cutouts, no decorative lines, no tiny details.
Background must be truly TRANSPARENT with alpha zero in all empty regions and corners. No backdrop color, no checkerboard painted into image, no floor, no cast shadow, no glow haze outside silhouette. Antialiased clean edge. Entire particle fits with 10 percent margin on every side.
Exactly one star only: no additional sparkles, droplets, dots, particles, orbit, objects or inset panels. Entirely original; no logos, people, faces, letters, words, numbers or watermark.
```

### icon.png

transparent_background: true

```text
Use case: stylized-concept.
Asset type: square 1024x1024 transparent UI skin-picker thumbnail, designed to read clearly at 64 pixels.
Subject: one original liquid-chrome cube head with a SHORT attached solid chrome rectangular trail stub emerging behind it toward the upper right, like a cute casual rhythm-game player. Large bold centered compact silhouette, cube dominates, entire assembly uses 82 percent of canvas with generous transparent margin on every side. View: three-quarter isometric, visible top and two side faces. Cube is a clear recognizable cube with subtly softened bevels, no facial features. Liquid mirror-silver faces with broad simple holographic reflections in pastel aqua #BDF8EE, pastel peach #FFD5BE and pale lavender. Brilliant chrome #DCE5F0 highlights, darker cool-silver reflections to define its faces. Thin yet readable electric-blue #3A9FFF and neon-violet #9165FF bevel rims; glow confined near edges. Trail stub has brushed-silver top, pastel sheen, blue/violet edge lines, width aligned to cube footprint, length about half a cube width behind cube. Clean cute polished Y2K 3D game-art finish; simplified broad gradients suitable for tiny thumbnail.
Background: actual transparent alpha; all four corners fully transparent. No floor plane, no shadow beneath, no circular badge or background panel, no painted checkerboard, no extra sparkle shapes or floating objects, no halo reaching canvas edges.
Constraints: original design; no official logos or copied brand marks, no people, no human likenesses, no faces; absolutely no text, letters, numbers, typography or watermark.
```

