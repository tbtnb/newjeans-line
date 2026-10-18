# Ditto Film
Slug: `film`

A frosted milky blue-grey cube carries a tiny amber light leak like a warm memory caught on an old winter camcorder. Its solid trail becomes a faded 35mm film band, with blank blue-grey frames, slate rails and snow-white sprocket insets along both edges. Taps release a brief snowfall of rounded flakes and grain motes; death breaks the head into frosted fragments that settle into dust. Soft gradients and restrained grain keep the silhouette clear during play. All artwork is original, without logos, lettering, people or likenesses.

## Exact runtime palette

These are material/tint targets; the generated illustrations contain shaded variations.

| Role | Hex | Use |
|---|---|---|
| Head base | #B7C9D3 | Milky mist-blue body |
| Head accent / emissive | #E7B477 | Small localized warm light-leak corner |
| Head frost highlight | #DCE8EB | Pale ice bevels |
| Trail base | #B7C9D3 | Faded blank film frames |
| Trail edge / stitch | #657C8B | Slate film rails and frame dividers |
| Trail sprocket inset | #F4F7F6 | Snow-white perforation markings |
| Burst particle 1 | #F4F7F6 | Main snowflakes |
| Burst particle 2 | #E7B477 | Sparse warm dust |
| Death particle 1 | #DCE8EB | Frosted flakes and shards |
| Death particle 2 | #657C8B | Fading slate grain motes |
| Picker UI accent | #E7B477 | Selected ring or highlight |

Concept swatches, left to right: #B7C9D3, #F4F7F6, #657C8B, #DCE8EB, #E7B477.

## Recommended Babylon.js materials

Starting values for a cube with side length 1 world unit; these are art recommendations, not a tested engine integration. Use either material approach below.

| Surface | StandardMaterial | PBRMaterial | Alpha / emission |
|---|---|---|---|
| Head | diffuseColor #B7C9D3; neutral specularColor (0.16, 0.16, 0.16); specularPower 32 | albedoColor #B7C9D3; metallic 0; roughness 0.66; clearCoat disabled | alpha 1; base emissiveColor = #DCE8EB × 0.025 |
| Corner light leak | Same diffuse body with a localized amber color blend; specularPower 24 | metallic 0; roughness 0.60 | alpha 1; localized emissiveColor = #E7B477 × 0.18 |
| Trail | diffuseTexture trail.png; diffuseColor white; specularColor (0.06, 0.06, 0.06); specularPower 12 | albedoTexture trail.png; albedoColor white; metallic 0; roughness 0.84 | alpha 1; emissiveColor = #B7C9D3 × 0.01 |
| Cube shards | Head settings; specularPower 24 | metallic 0; roughness 0.72 | alpha 1 initially, fade near end of life |
| Snowflake / dust | Unlit particle tint; no specular | Unlit equivalent if using mesh particles | alpha 0.80–0.95 initially, fade to 0; normal alpha blending |

PBR roughness corresponds to an approximate artistic glossiness of 0.34 for the head and 0.16 for the trail. StandardMaterial specularPower is a separate control. Keep frosting opaque; avoid refraction, metallic reflections and a transparent head, which weaken gameplay readability. A very small geometric bevel (about 0.025 cube widths) catches the frost highlight. Use a localized corner mask or vertex colors for the amber patch; do not illuminate the entire cube amber. Film grain should be static, subtle and approximately 2–3% luminance variation, with no animated flicker.

Map trail.png with U along travel and V across the bar, one whole V interval across its width. The image contains two frame panels per square tile. Repeat U according to segment length; use Repeat wrapping in both axes. Rotate the UV direction at each 90-degree turn and miter or join the bar geometry so both sprocket rows continue around the corner. The white sprockets are opaque printed insets in this asset, not actual alpha holes; preserve a solid trail silhouette. Apply the top texture to the top surface and use slate for the bar's shallow side walls. Use mipmaps and anisotropic filtering to reduce distant shimmer.

## Particle behavior

Sizes below are full billboard width relative to the 1-unit cube; Y is up. Effects are cosmetic and must not change collision geometry.

| Event | Count and shape | Size | Lifetime | Velocity and gravity |
|---|---|---|---|---|
| Tap / turn | 6 snowflake sprites from particle.png, plus 8 small round grain motes; mostly white, with about 15% amber motes | Flakes 0.08–0.16; motes 0.015–0.035 | Flakes 0.30–0.50 s; motes 0.20–0.38 s | Radial horizontal speed 0.35–0.80 units/s; initial upward speed 0.35–0.65; gravity (0, -0.8, 0) units/s² |
| Death | 14 small frosted cube mesh shards, 10 snowflake sprites, 20 dust motes; roughly 80% pale ice and 20% slate | Shards 0.06–0.16; flakes 0.09–0.20; dust 0.015–0.045 | Shards 0.55–0.95 s; flakes 0.65–1.10 s; dust 0.40–0.90 s | Shards horizontal speed 0.8–1.8, upward 0.8–1.6, gravity (0, -2.2, 0); flakes/dust horizontal speed 0.2–0.7, upward 0.2–0.6, gravity (0, -0.35, 0) |

Emit once per event. Tap burst originates at the inside of the turn, slightly above the trail. On death hide the intact head as shards emit from its volume. Use normal alpha blending for a soft film look, random flake rotation and slow angular drift of ±0.8 radians/s. Fade in over the first 8% of life and fade out over the last 45%; shrink to 65% size at expiry. Shards can tumble at 1–3 radians/s. Use built-in point particles or procedural round quads for grain motes and ordinary cube geometry for shards; no additional image files are required. The one supplied sprite contains a single bold snowflake. At very small screen sizes use motes instead of shrinking the flake below approximately 6 pixels. Keep effects brief and out of the upcoming path.

## Delivered assets and verification

- concept.png — 1536 × 1024 RGB, landscape 3:2 concept sheet with head, cornered film trail, turn/death particle studies and five swatches.
- trail.png — 1254 × 1254 RGB, full-bleed orthographic repeating film texture. Opposing edges retain the same rail/divider structure; mean absolute edge differences are approximately 3.6–4.3 out of 255 per channel, consistent with the fine grain.
- particle.png — 1254 × 1254 RGBA, single white snowflake.
- icon.png — 1254 × 1254 RGBA, cube with short film-strip stub.

Both transparent PNGs were checked using python3 + PIL: RGBA mode and alpha 0 at all four corner pixels. No magenta-background regeneration was needed. The generated alpha has some very low-opacity edge speckling; an optional runtime alpha cutoff of 0.02 can suppress stray faint pixels when rendering thumbnails. Preserve antialiasing on the main silhouette.

All four images were generated with the built-in image_gen tool, exactly one call per image, then copied unchanged from $CODEX_HOME/generated_images into this directory. No image postprocessing was applied. This delivery includes art and runtime recommendations; no Babylon.js scene was added or executed.

## Exact image_gen prompts

### concept.png

Transparent background: false.

```text
Use case: stylized-concept. Create one landscape 3:2 game skin concept sheet, 1536 by 1024, on a clean pale snow-white background. Original skin "Ditto Film": soft nostalgic winter camcorder / VHS film mood, clean cute Y2K pastel casual-game 3D art, crisp silhouettes and soft gradients. Absolutely NO text, letters, numbers, labels, logos, brand marks, watermarks, people or faces.
Composition: generously spaced polished object studies. Left: one large frosted milky blue-grey CUBE head in three-quarter isometric view, precise cubic form with subtly softened edges, translucent-looking cloudy surface but solid readable silhouette, fine subtle film grain, tiny warm amber light-leak glow in one upper corner. Right upper: a solid flat rectangular trail bar band forming exactly ONE 90-degree L corner in isometric view, like a thick 35mm film strip, faded blue-grey blank rectangular frames, slate rails with snow-white rounded rectangular sprocket holes along BOTH edges, continuous band, no writing or pictures inside frames. Right lower: two visibly separate particle studies: a compact tap burst of a few simple white six-arm snowflakes and tiny grain motes; beside it a larger death shatter of small frosted cube shards mixed with soft snowflakes and dust, tiny amber accents. Bottom: a neat row of exactly FIVE flat square color swatches without outlines or writing. Palette: mist blue-grey #B7C9D3, snow white #F4F7F6, faded slate #657C8B, pale ice #DCE8EB, warm amber #E7B477. Head and film strip are primary; particle clusters smaller. Gentle studio shadows only under objects. No scenery, no decorative page borders.
```

### trail.png

Transparent background: false.

```text
Use case: stylized-concept. Asset: square 1024x1024 seamless repeatable game texture for the TOP surface of a solid trail bar. Full-bleed orthographic flat 2D scan of an original faded 35mm film strip, oriented horizontally left-to-right. NO perspective, NO 3D thickness, NO environment, NO focal object, NO vignette, NO lighting gradient across the image. Clean cute Y2K pastel casual-game asset, crisp simple geometry and extremely subtle uniform faded film grain.
The ENTIRE square is the film surface: faded slate #657C8B outer edge rails at the very top and very bottom, a row of evenly spaced rounded rectangular snow-white #F4F7F6 sprocket-hole markings along each horizontal edge, inset from the image boundary; milky mist-blue #B7C9D3 blank rectangular film frames across the central broad area, separated by narrow slate vertical frame dividers. Two equal frame repeats across the square, eight evenly spaced sprocket repeats across each row. All frames blank with pale ice #DCE8EB subtly cloudy fill, no pictures. Flat opaque texture; white holes are printed pale insets, not transparency.
CRITICAL: seamless periodic pattern in BOTH axes, edges designed to wrap: left and right edges are identical phase at the center of a repeating narrow vertical divider; top and bottom terminate in the same flat uniform slate rail color, without shadows or grain discontinuities. No external border, no margin, no round-corner tile presentation. No directional light leak in this repeat texture. NO text, letters, numbers, logos, watermarks, people, faces.
```

### particle.png

Transparent background: true.

```text
Use case: stylized-concept. Asset: ONE square game particle sprite, 1024x1024, on a genuinely TRANSPARENT background with empty transparent corners. Create exactly ONE single centered connected six-arm snowflake silhouette, occupying approximately 80 percent of the canvas width and height. Simple bold cute casual-game shape readable at 32 pixels: six thick rounded spokes, each with just ONE pair of short thick diagonal branchlets, small solid central hexagonal hub. All branches connected, no holes in the hub. Snow-white #F4F7F6 main fill with a very subtle pale ice #DCE8EB edge shade, almost flat shading and crisp antialiased edges. Symmetrical, friendly, softly rounded ends. No outline, no surrounding glow or shadow, no halo, no dust, no specks, no other snowflakes, no other objects, no decorative background. Alpha must be zero around the shape and at all four corners; no checkerboard drawn into image. Original design, NO text, letters, numbers, logos, watermarks, people or faces.
```

### icon.png

Transparent background: true.

```text
Use case: stylized-concept. Asset: square transparent UI skin-picker thumbnail, original "Ditto Film" casual rhythm-game skin. ONE frosted milky blue-grey cube head with ONE short solid 35mm film-strip trail stub attached behind its base, isolated and centered as a compact group on genuinely TRANSPARENT background. All four corners fully transparent, no backdrop, no drawn checkerboard, no ground plane, no cast shadow outside silhouette. Three-quarter isometric view. Cube dominates, occupies about 65 percent of canvas; whole object group fits within 82 percent with generous clear padding. Short trail emerges toward lower left, about half a cube long, with pale blank blue-grey film frame and just a few large snow-white rounded rectangular sprocket insets on BOTH slate edges, no curl and no other objects. Cube has exact readable cubic proportions, subtly softened edges, broad crisp faces: snow-white #F4F7F6 top, misty blue-grey #B7C9D3 front, faded slate #657C8B shaded side, pale ice #DCE8EB frosted rim. Restrained soft fine film grain within the cube faces only, a warm amber #E7B477 light-leak patch on ONE upper corner. Clean cute Y2K pastel casual-game 3D illustration, bold simple silhouette readable at 64px, soft gradients, minimal tiny details. Opaque solid cube with frosting, not glass transparency. NO floating particles, no sparkle ornaments, no extra cubes. Absolutely NO text, letters, numbers, logos, brand marks, watermarks, people or faces.
```

