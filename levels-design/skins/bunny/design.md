# Bunny (Tokki)

Slug: `bunny`

An original soft-white bunny cube glides along a plush ribbon path, with tall sky-blue ears, delicate navy ear-root seams and a single baby-pink nose dot. The glossy head contrasts with the softly textured continuous trail, whose blue trim, tiny paw dots and pink hearts stay playful without obscuring the path. Turns release a quick little heart-and-fluff hop; a collision breaks the cube into white chips and floating pastel pieces. The design uses a cute Y2K pastel game aesthetic and contains no copied official mascot, logo, brand mark or human likeness.

## Exact palette

Hex values are sRGB authoring targets; lighting and generated-image gradients introduce lighter and darker variants.

| Role | Hex | Use |
| --- | --- | --- |
| Head base | `#F8FCFF` | Glossy cube and outer ear trim |
| Head accent / emissive hue | `#A9D9F5` | Ear interiors, restrained blue fill |
| Nose | `#F6BED1` | Single small pink dot |
| Detail accent | `#344C70` | Thin ear-root seams only |
| Trail base | `#F8FCFF` | Soft white plush band |
| Trail edge / stitch | `#A9D9F5` | Continuous blue side stripe and stitches |
| Burst particle colour 1 | `#F6BED1` | Turn hearts |
| Burst particle colour 2 | `#F8FCFF` | Turn fluff |
| Death particle colour 1 | `#A9D9F5` | Floating hearts |
| Death particle colour 2 | `#F8FCFF` | Fluff and cube chips |
| Picker UI accent | `#A9D9F5` | Selection border / highlight |
| Secondary shading | `#E7F4FB` | Icy shading and sprite interior |

## Assets

| File | Dimensions | Purpose |
| --- | --- | --- |
| `concept.png` | 1536 × 1024, RGB | 3:2 concept sheet: head, one corner, turn burst, death shatter and five swatches |
| `trail.png` | 1254 × 1254, RGB | Flat repeating plush surface with paw/heart motifs and blue stitch rows |
| `particle.png` | 1254 × 1254, RGBA | One near-white heart for tintable billboard particles |
| `icon.png` | 1254 × 1254, RGBA | Bunny cube and short trail stub on transparency |

All four images were generated separately with the built-in image_gen tool and copied unchanged from `$CODEX_HOME/generated_images` into this directory. The particle uses a single bold heart silhouette; fluff puffs and cube shards in the concept are runtime geometry recommendations, not additional sprite files.

## Real-time material recommendations

Values below are starting points for Babylon.js. Let W be the cube width. Keep the gameplay collision shape cubic; ears are visual attachments. Use a bevel around 0.06W, ears about 1.0W tall, and a nose about 0.09W across. Trail geometry is a continuous solid bar with a square 90-degree turn, with the fluffy appearance supplied primarily by its texture rather than expensive fur geometry.

| Surface | StandardMaterial | PBR metallic/roughness | Alpha |
| --- | --- | --- | --- |
| Cube / white ear trim | Specular power 96, specular RGB (0.65, 0.70, 0.75) | Metallic 0, roughness 0.22; optional clear coat intensity 0.35, roughness 0.18 | 1.0, opaque |
| Blue ears / nose | Specular power 80, specular RGB (0.55, 0.60, 0.65) | Metallic 0, roughness 0.28 | 1.0, opaque |
| Plush trail | Specular power 12, specular RGB (0.12, 0.14, 0.16) | Metallic 0, roughness 0.82 | 1.0, opaque |
| Blue side stripe | Specular power 40, specular RGB (0.30, 0.35, 0.40) | Metallic 0, roughness 0.46 | 1.0, opaque |
| Navy seams | Specular power 24, subdued specular | Metallic 0, roughness 0.60 | 1.0, opaque |

Emissive strength here means a scalar multiplied into the chosen emissive RGB, not an assumed shared material property. Start the cube and trail at 0.02 × their base RGB; ear accent at 0.08 × sky blue; navy and nose at 0. Keep it subtle so white surfaces retain shape. For PBR implementations that expose `emissiveIntensity`, use the same scalar with the unscaled emissive colour. Convert palette colours appropriately for the engine's linear-light shading workflow. For StandardMaterial, set `emissiveColor` to the scaled linear RGB.

Use `trail.png` as the diffuse/albedo texture with neutral white material tint. Set wrap U and V to repeat and enable mipmaps; use anisotropic filtering around 4–8. Map a repeating section in world space rather than stretching one tile over the entire path. Keep the UV direction stable through corners. The stitch rows are decorative top-surface details; implement the continuous side-edge blue stripe as a narrow material band so it follows both sides around a turn. Avoid displacement that changes the trail silhouette or path readability.

Use conventional alpha blending for heart billboards, not additive blending, to preserve pastel colour and the heart notch. Disable particle depth writes, retain depth testing, and fade particle alpha to zero. For the picker icon, preserve straight alpha and render without a background plate baked into the image.

## Particle behaviour

All dimensions and speeds use W as the unit. A burst is instantaneous, not a continuous emitter.

| Event / shape | Count | Size | Lifetime | Motion and gravity |
| --- | --- | --- | --- | --- |
| Turn: pink hearts | 4 | 0.12–0.20W | 0.28–0.42 s | Outward/upward speed 0.5–1.0W/s; gravity (0, −0.35W/s², 0) |
| Turn: white fluff puffs | 4 | 0.10–0.18W | 0.22–0.36 s | Short upward hop 0.3–0.7W/s; gravity (0, −0.20W/s², 0) |
| Death: blue hearts | 8 | 0.14–0.27W | 0.65–1.05 s | Radial speed 0.7–1.4W/s, initial upward component 0.8W/s; gravity (0, −0.45W/s², 0) |
| Death: white fluff puffs | 10 | 0.16–0.30W | 0.55–0.90 s | Gentle expanding cloud 0.4–0.9W/s; gravity (0, +0.08W/s², 0), mild upward drift |
| Death: white cube shards | 8 | 0.08–0.17W | 0.45–0.80 s | Radial speed 1.0–2.0W/s plus upward kick; gravity (0, −2.0W/s², 0) |

Use Y-up coordinates, adapting the gravity axes if the game uses another convention. Spawn turns at the exact corner, just above the bar, with a small outward bias so the leading cube stays readable. Hearts use `particle.png`, multiplying its near-white RGB by the event tint. Keep billboard tilt within ±20 degrees and rotation below 1 rad/s. Grow from 75% to full size in the first 15% of life, then fade over the final 60%. Use two or three overlapping low-poly white spheres per fluff puff; no extra texture is required. Chips are tiny beveled cubes with randomized tumbling at 2–5 rad/s. On death, hide the intact head immediately and emit once; leave the trail solid.

For reduced effects, halve counts and omit shard spin. Do not use a flash, screen-covering smoke or lingering particles that hide the next turn.

## Verification

Python 3 + PIL confirmed both transparent files are RGBA with alpha range 0–255, and alpha 0 at all four corners. No solid-magenta regeneration was needed; therefore no separate `prompts.md` was created. The concept aspect ratio and all square dimensions were checked. Trail opposite-edge mean RGB differences measured about 2–5 levels out of 255, consistent with its fine plush grain; it is generated for two-axis repeat, though this is not proof of pixel-identical edge continuity. No live Babylon.js integration or in-game visual test is included in this art delivery.

## Exact image_gen prompts

Each section records one independent generation call. No reference images or edits were supplied. Actual output dimensions are recorded above; the built-in tool selected square outputs larger than the requested 1024.

### concept.png — transparent_background: false

```text
Use case: stylized-concept. Asset: concept.png, a polished landscape 3:2 game skin concept sheet, 1536x1024 composition. Design an ORIGINAL cute bunny-themed moving cube and solid trail for a rhythm path game, named Bunny (Tokki) only in this instruction; absolutely NO text in the artwork.
Clean very pale icy-white background, carefully spaced art-board composition. Large hero in upper left: small glossy soft-white beveled CUBE head, unmistakably cube-shaped, 3/4 isometric view, two tall rounded pastel sky-blue ears growing from its top, white-blue soft shading and one tiny baby-pink nose dot on its front. NO eyes, no mouth, no human features. Original proportions: upright parallel pill ears with slightly inward-curved tips and a subtle navy-blue seam near their roots. Upper right: separate continuous thick solid white fluffy-surfaced trail bar with exactly ONE crisp 90-degree corner in isometric view; smooth continuous center, very fine soft fluff edge, narrow pastel-blue edge stripe, sparse tiny pink hearts and pale-blue paw dots on top. It is a straight solid bar around the corner, never a chain of cubes. Bottom middle left: small compact tap burst of 6 pastel hearts and white fluff puffs. Bottom right: larger airy death shatter cluster of white cube chips, white fluff puffs and baby-pink/pastel-blue hearts, no character duplication. Bottom left margin: a neat row of exactly five FLAT solid circular colour swatches, white #F8FCFF, sky blue #A9D9F5, baby pink #F6BED1, soft navy #344C70, ice blue #E7F4FB; subtle neutral outline so white is visible.
Clean cute Y2K pastel casual-game 3D art, crisp silhouettes, soft studio light and restrained gradients, coordinated materials, ample negative space, no panels or labels. No logos, official mascot artwork, brand marks, real people, human likenesses, lettering, words, numbers, watermark, signature.
```

### trail.png — transparent_background: false

```text
Use case: stylized-concept. Asset: trail.png, square 1024x1024 seamless repeating game surface texture. Create an ORIGINAL flat top-down albedo texture for a cute bunny-themed solid trail bar. Entire image is an evenly lit soft white #F8FCFF plush/fluffy surface with extremely subtle small-scale fleece curls, crisp enough for a casual game. Sparse small flat baby-pink #F6BED1 hearts and pastel-sky-blue #A9D9F5 paw-print dot motifs in a restrained regularly repeating staggered pattern, each motif tiny relative to tile. Include very thin straight pastel sky-blue stitched stripes running horizontally across the tile at one quarter and three quarters height, continuous to both horizontal borders, as edge/stitch accents. Repeat the surface seamlessly in BOTH X and Y: opposite edges must have exactly continuous colour, texture, spacing and line alignment; motifs remain well inside tile edges, texture at borders should be near-uniform white. No border around the square. No perspective, no visible bar or cube, no floating objects, no cast shadows, no directional lighting, no vignette, no central focal object, no background scene. Flat texture, restrained pastel colours and very fine plush grain; do not depict 3D fur clumps. No text, letters, words, numbers, logos, official mascot, brand marks, real people, human faces or watermarks.
```

### particle.png — transparent_background: true

```text
Use case: stylized-concept. Asset: particle.png, square game particle sprite, 1024x1024 with TRUE TRANSPARENT alpha background.
ONE SINGLE simple bold softly rounded heart silhouette centered in the frame, filling approximately 80 percent of width and height, upright and symmetrical, with two plump lobes, a clear notch and softly pointed bottom. Near-white #F8FCFF main fill with very subtle ice-blue #E7F4FB shading and a narrow pastel sky-blue #A9D9F5 rim for readability. Clean cute Y2K pastel casual-game style, restrained soft gradient suggesting a tiny puffy heart, no internal lines, no tiny details, excellent silhouette at 32px, designed for colour tinting. Heart is one connected shape. Keep entire heart inside frame with transparent margin on all sides.
No other hearts or particles, no sparkles, no fluff cloud, no eyes, no face, no pedestal, no ground plane, no cast shadow, no opaque background, no checkerboard drawn into image, no glow outside the silhouette. No text, letters, words, numbers, logos, official marks, real people or watermarks. Actual transparent RGBA PNG, all four corners fully transparent.
```

### icon.png — transparent_background: true

```text
Use case: stylized-concept. Asset: icon.png, square 1024x1024 UI thumbnail, actual TRANSPARENT RGBA background.
ONE centered ORIGINAL bunny-themed cube game head with a short attached solid trail stub behind it, large and bold, all elements fit comfortably inside frame with 8 percent transparent safety margins. 3/4 isometric camera, readable at 64px. Head is an unmistakable glossy SOFT WHITE #F8FCFF beveled CUBE, not a sphere, with two tall thick rounded pastel sky-blue #A9D9F5 bunny ears, nearly parallel, gently inward-curved tips, white outer trim, tiny soft navy #344C70 root seams. Only facial detail is ONE tiny pink #F6BED1 nose dot on the front face; NO eyes, NO mouth, NO whiskers. Ears are about as tall as the cube itself. Short solid white plush trail bar attached at the rear, extending toward the right rear by roughly one cube width; continuous broad band with very subtle fluffy surface, one narrow sky-blue stripe along its side edge, and ONE tiny pink heart dot on top. Keep the stub secondary so the head dominates. No disconnected parts.
Clean cute Y2K pastel casual-game 3D render, crisp silhouette, soft gradients and glossy highlights, cool subtle edge shading for contrast on white or dark UI. No ground, no pedestal, no cast shadow on a backdrop, no scene, no extra floating hearts, no frame, no background colour, no baked checkerboard. Background and all corners fully transparent. No text, letters, words, numbers, logos, copied mascot artwork, brand marks, real people, human faces or watermarks.
```

