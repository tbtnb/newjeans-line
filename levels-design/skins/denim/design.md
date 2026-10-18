# Y2K Denim
Slug: `denim`

A pocket-sized denim cube skates through the song, laying down a solid indigo ribbon with warm orange double stitching and little copper rivets. Washed blue faces and diagonal twill soften the geometric silhouette into a cute Y2K accessory. Each tap flicks off a small scatter of pale fabric chips, thread curls and copper glints; a crash unravels the cube into a wider tumbling denim shatter. The artwork is original and contains no logos, people, faces, lettering or watermarks.

## Exact implementation palette
Hex values below are the runtime color targets; generated raster shading naturally varies around them.

| Role | Hex | Use |
| --- | --- | --- |
| Head base | `#294572` | Indigo fabric body |
| Head accent | `#8FB9D7` | Washed top face and cloth highlights |
| Head emissive accent | `#F5A33B` | Very restrained stitch pulse on turns |
| Trail base | `#294572` | Continuous opaque denim bar |
| Trail edge / stitch | `#F5A33B` | Two parallel stitch rows on each edge |
| Copper hardware | `#BC754C` | Pocket rivet and edge rivets |
| Burst particle 1 | `#DCECF4` | Pale denim scraps |
| Burst particle 2 | `#F5A33B` | Thread loops and small warm glints |
| Death particle 1 | `#8FB9D7` | Tumbling denim fragments |
| Death particle 2 | `#BC754C` | Copper rivet sparks |
| Picker UI accent | `#F5A33B` | Selected outline / highlight |

## Babylon.js material recommendations
Use a head edge length of 1 world unit as the reference for the values below.

| Surface | StandardMaterial | PBRMaterial | Alpha / emission |
| --- | --- | --- | --- |
| Denim head / trail | specularColor `(0.08, 0.10, 0.13)`; specularPower `16` | metallic `0`; roughness `0.88` | alpha `1`; emission `0` |
| Orange stitches | specularColor `(0.12, 0.09, 0.05)`; specularPower `24` | metallic `0`; roughness `0.72` | alpha `1`; emission strength `0.03`, briefly `0.12` for 80 ms on a turn |
| Copper rivet mesh | specularColor `(0.60, 0.34, 0.18)`; specularPower `64` | metallic `0.85`; roughness `0.32` | alpha `1`; emission `0` |
| Particle billboard | disableLighting `true`; specularColor black | unlit `true` if using PBR | alpha `1 → 0` over final 35% of life |
| Picker icon plane | disableLighting `true`; specularColor black | unlit `true` | alpha `1` multiplied by texture alpha; emission `0` |

Emission strengths mean the linear RGB palette color multiplied by that scalar, assigned to emissiveColor; they are recommendations rather than a separate universal Babylon property. Prefer PBR roughness for fabric and reserve metallic response for separate rivet geometry. Do not make the entire textile metallic. With a StandardMaterial texture, use white diffuseColor to preserve its baked color; with PBR use white albedoColor. Do not multiply the colored texture by the indigo base again.

Use `trail.png` as the albedo/diffuse texture with `Texture.WRAP_ADDRESSMODE` on U and V. Map U across the bar and V along its length; keep U at one repeat so stitched seams remain near the sides. Rotate UVs with each segment and miter the corner geometry and seam placement. Use mipmaps and anisotropicFilteringLevel `8` to calm the fine weave. The supplied texture includes copper marks in its color, so separate hardware meshes are optional.

For sprites, enable texture alpha and use ordinary alpha blending rather than additive blending for fabric. Copper glints may use additive blending sparingly. Keep the solid head and trail fully opaque. The icon is a UI image, not a replacement for a cube mesh.

## Particle behavior
All sizes and gravity are relative to the 1-unit head; gravity assumes Y is up.

| Event / shape | Count per event | Size | Lifetime | Velocity / gravity |
| --- | --- | --- | --- | --- |
| Tap: denim chips | 6 | 0.07–0.13 | 0.20–0.34 s | speed 0.7–1.5 units/s; gravity `(0,-2.0,0)` |
| Tap: orange thread loops | 3 | 0.05–0.10 | 0.18–0.28 s | speed 0.5–1.1; gravity `(0,-1.2,0)` |
| Tap: copper glints | 2 | 0.025–0.05 | 0.12–0.20 s | speed 1.0–1.8; gravity `(0,-1.0,0)` |
| Death: denim fragments | 18 | 0.10–0.28 | 0.50–0.85 s | speed 1.2–3.0; gravity `(0,-4.0,0)` |
| Death: thread curls | 6 | 0.06–0.15 | 0.45–0.75 s | speed 0.8–1.8; gravity `(0,-2.0,0)` |
| Death: copper flecks | 8 | 0.035–0.08 | 0.30–0.55 s | speed 1.8–3.4; gravity `(0,-5.0,0)` |

Emit exactly once at each turn or death. Turn particles originate just behind the head near the outside corner and spread mostly sideways/upward without covering the next path. Death is a radial burst with a slight upward bias; hide the head immediately. Randomize rotation through 360 degrees and angular speed around ±6 radians/s for chips, ±9 for death fragments. Shrink to 30% and fade near the end; no persistent smoke or full-screen flash.

`particle.png` contains exactly one light denim scrap, suitable for color multiplication. Use it for cloth chips. Build thread loops from a tiny open curved mesh and copper sparks from small discs or short quads; these are runtime shapes, not extra image files. The supplied sprite remains the sole particle raster. Preserve thread thickness at a minimum of approximately one screen pixel.

## Delivered assets and checks
- `concept.png`: 1536 × 1024, RGB, landscape 3:2 concept sheet.
- `trail.png`: 1254 × 1254, RGB, full-bleed flat twill with paired stitched seams; generated for two-axis repetition.
- `particle.png`: 1254 × 1254, RGBA, single pale denim scrap.
- `icon.png`: 1254 × 1254, RGBA, cube head and short attached trail.
- Both transparent files were checked with Python 3 and Pillow: RGBA mode, alpha 0 at all four corners, and fully transparent 16 × 16 corner patches. Native generated alpha was retained; no magenta fallback was required.
- Each image was produced in one built-in image_gen call and copied unchanged from `$CODEX_HOME/generated_images`. No separately authored raster or vector substitute was used.

## Exact image_gen prompts
All four used the built-in tool; concept and trail used transparent_background=false, particle and icon used transparent_background=true.

### concept.png
Use case: stylized-concept. Create an original casual rhythm-game skin concept sheet for Y2K Denim. Landscape 3:2 canvas, 1536x1024. Clean warm off-white background, generous spacing, no panel borders. Show a large small-cube player head at left in three-quarter isometric view, dressed entirely in indigo jean fabric with fine diagonal twill, bright mustard-orange double stitches around edges, a simple stitched pentagonal pocket outline on the front face and a single round copper rivet near a pocket corner; no logos. At upper right show a solid continuous rectangular denim trail bar with exactly one crisp 90-degree turn, isometric, constant width and solid thickness, double orange stitching along both long edges continuing neatly around the corner and a few tiny copper rivets. At lower middle show a compact tap-turn burst of tiny pale denim scraps, orange thread loops and copper sparks. At lower right show a wider death shatter of angular denim fragments, broken thread curls and copper rivet flecks. Along bottom show a neat row of five flat unlabeled color swatches: deep indigo #294572, washed denim #8FB9D7, mustard orange #F5A33B, copper #BC754C, pale denim #DCECF4. Clean cute Y2K-pastel casual-game 3D art, crisp geometric silhouettes, soft gradients, subtle textile detail, soft studio lighting. Everything visible and separated, attractive balanced professional asset sheet. Absolutely NO text, letters, words, numbers, brand marks, official logos, watermark, people, faces or likenesses.

### trail.png
Use case: stylized-concept. Asset type: seamless square game material texture. Create a 1024x1024 perfectly flat top-down albedo texture for an indigo denim trail bar. The image is entirely fabric, edge to edge, with fine regular diagonal twill weave in indigo #294572 and slightly washed blue threads, subtle even variation, clean cute Y2K casual-game style. Two parallel orange #F5A33B dashed stitch lines form one double-stitched seam near the left edge and an identical double-stitched seam near the right edge, each seam inset about 6 percent from its side, running vertically through the full image and repeating continuously across the top and bottom boundaries. A very small copper #BC754C rivet is embedded midway along each stitched edge, flat circular and understated, no cast shadow. Periodic textile pattern must tile seamlessly horizontally AND vertically: matching opposite edge colors and twill phase, stitch dashes phase matched at top and bottom. Full bleed square with absolutely uniform illumination. NO perspective, no cube, no objects sitting on the fabric, no border outside fabric, no vignette, no central motif, no focal object, no folds, no directional lighting, no highlights or cast shadows, no text, letters, numbers, logo, watermark, people or faces. The textile is the entire image.

### particle.png
Use case: stylized-concept. Asset type: ONE transparent game particle sprite, square 1024x1024. Draw ONE single simple bold pale washed-denim scrap: a small chunky tilted diamond-shaped fabric chip with slightly clipped corners and just two short stitch dashes near one edge. One connected silhouette only. The scrap is pale icy denim #DCECF4 with subtle light-blue #8FB9D7 diagonal twill and restrained soft gradient. Center it, filling roughly 80 percent of canvas width and height, leaving clear transparent padding on every side. Cute crisp casual-game art, strong silhouette readable at 32 pixels, minimal detail, almost flat with tiny bevel. Genuine alpha-transparent empty background including all four corners. No other particles, no multiple pieces, no thread loops around it, no sparkles, no ground, no cast shadow, no glow outside shape, no backdrop, no checkerboard drawn in image. NO text, letters, words, numbers, logos, watermarks, people, faces or likenesses.

### icon.png
Use case: stylized-concept. Asset type: transparent square skin-picker game UI icon, 1024x1024. An original Y2K Denim small cube player head in three-quarter isometric view, joined to one short solid rectangular denim trail stub behind it. Center the complete compact silhouette with generous transparent padding on every side, filling about 80 percent of square. Cube head is the clear hero, indigo-blue #294572 diagonal jean twill, lighter washed denim #8FB9D7 top face, bright mustard-orange #F5A33B double stitching tracing edges. Front face has a simple orange stitched pentagonal pocket outline and ONE round copper #BC754C rivet on upper pocket corner. Trail stub is solid indigo with clean double orange stitched edges, same width as head. Clean cute Y2K pastel casual-game 3D render, bold crisp geometry, soft gradients, simplified details readable at 64 pixels, no fine clutter. Genuine alpha-transparent background and transparent corners, no floor, no cast shadow outside object, no backdrop, no drawn checkerboard. No extra objects or particles. Absolutely NO text, letters, numbers, words, official logos, brand marks, watermarks, people, faces or likenesses.

