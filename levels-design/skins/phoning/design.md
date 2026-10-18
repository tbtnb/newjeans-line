# Phoning (flip phone LCD)

Slug: `phoning`

A tiny silver-framed LCD cube carries a pink pixel heart and an abstract signal glyph, as if a favourite pocket gadget had become a dancing companion. Mint-cyan backlight shines through a chunky navy pixel matrix; its solid trail continues that screen texture around sharp right-angle turns. Taps release little squares and blinking pixel stars, while collisions scatter the screen into cyan and navy chips. Rounded shell bevels and restrained soft shading keep the original Y2K design cute and readable without reproducing any official logo, device branding, person, or face.

## Exact runtime palette

These hex codes are the implementation colour targets; generated image shading varies around them. Convert sRGB colour inputs using the project's existing colour-management convention.

| Role | Hex | Use |
| --- | --- | --- |
| Head base | #A9F5DF | Mint-cyan LCD inset faces |
| Head accent / emissive | #6DE8E8 | Backlight, inset luminous rim |
| Head pixel / glyph outline | #173D4D | Navy matrix, heart outline, abstract signal |
| Head shell | #E5EBEF | Pale silver chamfered housing |
| Head heart | #F6ACC8 | Soft pink pixel heart |
| Trail base | #A9F5DF | Illuminated square cells |
| Trail edge / stitch | #173D4D | Grid gaps and solid side walls; no fabric stitching |
| Trail rim | #E5EBEF | Narrow optional shell lip |
| Burst particle colour 1 | #6DE8E8 | Cyan chunky squares and stars |
| Burst particle colour 2 | #F6ACC8 | Pink accent squares and stars |
| Death particle colour 1 | #6DE8E8 | Bright LCD fragments |
| Death particle colour 2 | #173D4D | Dark pixel fragments |
| Picker UI accent | #F6ACC8 | Selection outline or selected-state accent |

Optional physical shell chips use the shell colour. Keep the specified two death colours dominant.

## Real-time materials

Recommended starting values, to tune under the game's actual lighting. H denotes the head cube's side length. Use separate LCD and shell materials to retain dark glyph contrast. Treat the concept and icon as visual references; neither is a head UV atlas.

| Surface | StandardMaterial | PBR alternative | Alpha |
| --- | --- | --- | --- |
| LCD head panels | specularPower 64; neutral specular strength 0.25; emissiveColor = cyan × 0.30 on illuminated cells, pink × 0.18 on heart | metallic 0.0; roughness 0.40 (glossiness 0.60); emissiveIntensity 0.30 with lit-cell mask | 1.0, opaque |
| Pale silver shell | specularPower 96; neutral specular strength 0.45; emission 0 | metallic 0.25; roughness 0.32 (glossiness 0.68); emissiveIntensity 0 | 1.0, opaque |
| Trail LCD top | specularPower 32; specular strength 0.15; emissiveColor = cyan × 0.18, modulated by lit cells | metallic 0.0; roughness 0.55 (glossiness 0.45); emissiveIntensity 0.18 with lit-cell mask | 1.0, opaque |
| Navy pixels / trail walls | specularPower 24; specular strength 0.10; emission 0 | metallic 0.0; roughness 0.65 (glossiness 0.35); emission 0 | 1.0, opaque |
| Particle sprites | unlit or disableLighting; emission equal to tint colour; use straight-alpha source texture | unlit sprite material preferred | texture alpha × lifetime opacity, 1 → 0 |

Use either the StandardMaterial or PBR column, not both. StandardMaterial specular strengths mean uniform RGB components. PBR glossiness here is the artist-facing complement of roughness, not a second property to set in the metallic/roughness workflow. Keep emission masked away from navy pixels; avoid globally lifting black levels. Any bloom should be subtle enough to preserve the heart and grid.

For `trail.png`, use white diffuse/albedo tint to preserve its baked colours, repeat wrapping in both axes, and nearest sampling when viewed close enough to resolve pixels. Use mipmapped filtering at distance if grid shimmer becomes visible. Keep UV density equal on each straight segment and join the corner with aligned square cells. One full tile contains approximately 16 × 16 cells; a useful starting density is eight cells per H, so one tile spans 2H × 2H. Use solid navy side materials and an optional thin silver lip rather than stretching this top texture down the walls. Keep the trail a continuous solid bar.

For transparent sprite edges use normal alpha blending; reserve additive blending for a few bright cyan stars because additive navy fragments would disappear. The picker icon uses ordinary UI alpha blending at opacity 1.

## Particle behaviour

- **Turn / tap:** emit 10 particles once at each 90-degree turn: 8 square quads and 2 stars using `particle.png`. Use a 70:30 cyan-to-pink distribution. Sizes 0.06–0.12H for squares and 0.12–0.20H for stars; lifetime 0.22–0.42 s. Spawn within 0.10H of the corner, spread in a compact outward fan at 0.7–1.5H/s with 0.3–0.7H/s upward velocity. Gravity is (0, −1.5H/s², 0), assuming Y-up. Snap square/star rotation to 90-degree increments. Blink stars twice with 0.05 s opacity dips, then fade during the final 35% of life.
- **Death:** emit 36 pieces once: 28 chunky square pixel chips, 4 stars using `particle.png`, and 4 pale silver shell cube fragments. Split pixel chips evenly between the two death colours. Sizes 0.07–0.18H for chips, 0.10–0.16H for stars, 0.12–0.24H for shell fragments; lifetime 0.45–0.85 s. Scatter radially at 1.4–3.0H/s with 0.8–1.8H/s upward velocity; gravity (0, −4.0H/s², 0). Shell fragments may tumble, while flat LCD chips retain coarse stepped orientations. One brief blink at 0.10 s, then fade after 60% of lifetime. Remove the head at impact so no intact duplicate remains.
- Keep the strong star silhouette of the supplied sprite; use engine-generated square quads or small cube meshes for square chips. No extra sprite sheet is required. Tint the light sprite by the desired runtime colour; compensate slightly if its pale cyan shading cools the pink tint.
- Reduce-motion option: no blinking, half the particle count, and emission changes without bloom pulses.

## Delivered assets and checks

| File | Actual dimensions | Purpose |
| --- | --- | --- |
| concept.png | 1536 × 1024, RGB | 3:2 concept sheet: cube, one-corner trail, turn burst, death shatter, five unlabelled swatches |
| trail.png | 1254 × 1254, RGB | Opaque repeating LCD pixel surface |
| particle.png | 1254 × 1254, RGBA | One connected pale pixel-star sprite, approximately 81% frame coverage |
| icon.png | 1254 × 1254, RGBA | Cube with short trail stub; transparent picker artwork |
| design.md | Markdown | Palette, material targets, particle guidance, exact prompts |

All four images were generated independently with the built-in image_gen tool, one call per image, and copied unchanged from `/Users/bit_1/.codex/generated_images/01a14d7c-0f78-7de2-a937-f09eab9b1d11/`. No raster post-processing was applied. Requested 1024-square sizes in prompts were returned by the tool as 1254-square files; retain these supplied dimensions or resize through the game's asset pipeline.

Python 3 + Pillow verified both transparent PNGs are RGBA: every corner has alpha 0, and each entire 32 × 32 corner block is transparent. No magenta-background regeneration was needed. A 2 × 2 in-memory repeat preview of the trail was visually checked in both directions: the grid continues without a conspicuous seam. Generated texture edges have small colour variations rather than byte-identical edge pixels (mean absolute channel difference below 4.6/255); the dark grid keeps the joins visually continuous. The icon's heart and the single star remain bold thumbnail silhouettes. These are art-asset checks; no game integration or Babylon runtime test was performed.

## Exact image_gen prompts

All calls were new generations, with no image references.

### concept.png

`transparent_background: false`

```text
Use case: stylized-concept.
Create a landscape 3:2 (1536x1024) original casual-game skin concept sheet, on clean warm near-white background, with generous breathing room and absolutely NO text, letters, numbers, captions, logos, watermarks or human faces.
Theme: Phoning, a cute Y2K flip-phone LCD-inspired moving cube skin. Consistent palette: mint-cyan backlight #A9F5DF, cyan emission #6DE8E8, deep LCD navy pixels #173D4D, pale silver shell #E5EBEF, soft pink accent #F6ACC8.
Composition: upper left a large three-quarter isometric CUBE head, not a literal telephone, with thin pale silver chamfered shell, mint-cyan LCD inset faces, obvious chunky square dark pixel matrix, a tiny soft pink pixel HEART on the front face and a tiny abstract antenna SIGNAL pictogram on the side (pure geometric symbol, no lettering). Subtle cyan internal glow, crisp readable silhouette, soft shaded dimensional edges.
Upper right an independent long solid rectangular trail bar with exactly ONE right-angle 90-degree corner, shown in matching isometric perspective; mint-cyan LCD top with visible regular square dark grid and faint scanlines, navy side walls, thin pale-silver edge. It is a continuous solid L-shaped bar, no dotted disconnected path.
Lower left a small isolated tap/turn particle burst group of chunky mint and pink square pixels plus a few blocky four-point pixel stars.
Lower right a larger death-shatter group: many chunky square cyan/navy LCD pixel chips and a few pale silver cube fragments spreading out, distinct from tap burst.
Along the bottom one neat row of exactly FIVE flat unlabelled square colour swatches, matching the five palette colours above. No extra panels or decorations. Clean cute polished Y2K-pastel casual-game art, crisp stepped pixel motifs, controlled soft gradients on cube surfaces only, gentle contact shadows. Original design only, no official brand marks, no real people or likenesses.
```

### trail.png

`transparent_background: false`

```text
Use case: stylized-concept.
Asset: square 1024x1024 seamless tileable game texture for the solid trail bar surface of an original Y2K flip-phone LCD cube skin.
Create a perfectly flat top-down orthographic LCD pixel matrix texture covering the entire image edge to edge. Absolutely no perspective or objects. Mint-cyan backlight #A9F5DF with fine deep LCD navy #173D4D grid gaps around chunky square LCD pixels, subtle cyan #6DE8E8 alternate cell shading, and very faint horizontal scanlines. A precise even 16 by 16 matrix of identical square cells. All cells illuminated; dark navy is used only for fine regular grid gaps. Soft colour variation ONLY repeated identically inside EACH cell, never a global lighting gradient. Grid pitch exactly divides the image in both axes; place grid-line centres on each outer image boundary so opposite edges join to form the same thickness gap as internal gaps. Every row and column follows the identical repeating structure. No large motifs, no diagonal pattern, no border, no edge trim, no heart, no symbols, no focal point. Texture must wrap seamlessly left-right AND up-down with uniform brightness, no vignette, no shadow, no highlight spot, no frame. Crisp square pixel geometry with understated LCD screen feel, cute clean pastel palette, matte backlit surface, not reflective glass. Opaque background. No text, letters, words, numbers, logos, watermarks, real people or faces.
```

### particle.png

`transparent_background: true`

```text
Use case: stylized-concept.
Asset: square 1024x1024 transparent game particle sprite, readable downscaled to 32px.
Draw exactly ONE single solid chunky four-point PIXEL STAR, centred in the frame, occupying about 80 percent of the width and height, with 10 percent clear transparent padding on every side. Symmetrical bold connected stepped silhouette built from a coarse 9 by 9 logical pixel grid, long vertical and horizontal points and a broad solid central square. Filled solid shape, not hollow, no detached squares, no extra twinkles, no companion particles. Flat front view, no perspective. Very pale icy white mint #EFFFFB body with a restrained pale cyan #C4F7F1 one-logical-pixel inset shade along bottom/right only; keep values light so a game engine can tint it cyan, navy or pink. Crisp hard square stair-step corners, simple cute Y2K LCD 8-bit appearance. No outline thinner than a logical pixel, no fine detail, no sparkly noise, no blurry halo, no drop shadow, no floor, no background colour, no checkerboard pattern. Background must be genuinely transparent RGBA, including all four corners. Original shape only; absolutely no letters, text, numbers, logos, watermark, people or faces.
```

### icon.png

`transparent_background: true`

```text
Use case: stylized-concept.
Asset: square 1024x1024 skin-picker UI thumbnail with genuine transparent RGBA background, designed to read boldly at 64px.
One cute original Y2K flip-phone LCD-inspired CUBE game head in three-quarter isometric view, with a very short continuous solid trail stub attached behind and extending toward the lower right. The head is the dominant 75 percent of the subject, the stub only 25 percent. Whole subject centred with generous fully transparent padding, fills about 80 percent of frame, entirely inside image. No other objects, no particles, no pedestal, no floor, no cast shadow outside the object.
Head design: chunky almost cubic proportions with lightly chamfered pale silver #E5EBEF shell edges; large mint-cyan #A9F5DF backlit LCD inset face; deep LCD navy #173D4D coarse square pixel matrix; one tiny bold soft pink #F6ACC8 pixel heart on the main front face outlined in chunky navy pixels, no facial features; simplified abstract antenna signal glyph on side face as geometric stepped bars only. Restrained cyan #6DE8E8 inset emission, never a halo on the transparent background. Trail stub: short solid rectangular navy-sided bar, mint-cyan top surface with sparse bold square grid, thin silver rim. Consistent large pixel shapes and simplified broad bevels for readability.
Clean polished cute pastel casual-game 3D icon with soft surface gradients and crisp contours. Not a literal phone, no buttons or keypad. No busy microdetails, no extra objects, no circular badge or background plate. Background entirely transparent, all corners fully transparent; no checkerboard drawn in image. Original design only. NO letters, words, numbers, logos, brand marks, watermark, real people, faces or likenesses.
```

