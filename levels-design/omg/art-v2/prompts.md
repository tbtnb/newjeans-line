## worker a
# Asset prompts

Generated with the built-in image_gen tool, one call per asset. Three landscape 3:2 images and one square image. No alpha assets are specified; no transparency fallback is required.

## sky-dream.png

Aspect: landscape 3:2. Target dimensions are recorded in spec.tsv.

```text
Use case: stylized-concept. Create exactly one final in-game panoramic sky illustration, landscape 3:2 composition, for a lavish music-driven casual game. Art direction: Y2K Starlight Stage, matching the reference's polished glossy stylized casual-game rendering, clean shapes, soft gradients and luminous glow. This asset is the dreamy dusk intro/verse sky: soft pastel lilac fading into baby-blue across a broad open sky, fluffy pastel pink and pearl-white cloud banks kept low along the horizon, a few tiny delicate gold twinkle stars. A subtle navy-violet undertone ties it to a sparkling nighttime stage. Dreamy, airy, refined and uncluttered. The sky fills the whole image edge to edge; prioritize generous clear sky across the upper two thirds, clouds only near the bottom. Opaque full-bleed sky background, no border. Palette strictly pastel pink, baby-blue, lilac, pearl white, navy-violet and tiny warm gold accents; no orange sunset. No foreground objects, no ground, no stage, no phones, no bunny, no buildings, no people, no human figures or faces, no likenesses, no logos, no letters, no numbers, no words, no watermarks, no UI, no photorealism.
```

## sky-stage.png

Aspect: landscape 3:2. Target dimensions are recorded in spec.tsv.

```text
Use case: stylized-concept. Create exactly one final in-game panoramic night concert sky illustration, landscape 3:2 composition, for a lavish music-driven casual game. Art direction: Y2K Starlight Stage, matching the reference's polished glossy stylized casual-game rendering, clean shapes, soft gradients and luminous glow. Deep navy at the top blends into rich violet below. Soft pastel pink and baby-blue light haze rises gently from the very bottom like distant stage illumination, diffused and atmospheric with no visible lamps or stage equipment. Scattered delicate sparkling stars and a few small warm-gold four-point star glints, tastefully spaced with plenty of quiet dark sky. Keep the upper half open and calm: no beams crossing the top. Wide panoramic sky only, opaque full-bleed edge to edge, no foreground objects or terrain, no border, no vignette. Palette strictly navy-violet, pastel pink, baby-blue, lilac, pearl-white starlight and tiny warm-gold accents. No people, no human figures or faces, no likenesses, no phones, no bunny, no buildings, no logos, no letters, no numbers, no words, no watermarks, no UI, no photorealism, no clutter.
```

## sky-moon.png

Aspect: landscape 3:2. Target dimensions are recorded in spec.tsv.

```text
Use case: stylized-concept. Create exactly one final in-game moonlit garden sky panorama, landscape 3:2 composition, for the bridge of a lavish music-driven casual game. Art direction: Y2K Starlight Stage, matching the reference's polished glossy stylized casual-game rendering, clean shapes, soft gradients and gentle luminous glow. A broad lilac twilight sky graduates into navy-violet near the upper edge and pale baby-blue near the horizon. A big soft pearly full moon sits slightly above center, beautifully round with a delicate luminous halo and restrained pearl-white surface shading. Tiny pastel-white and occasional warm-gold stars sparkle sparsely around it. Along only the very lowest horizon, faint distant fairy-tale palace silhouettes in hazy lilac-blue are tiny, quiet and atmospheric, blending into the sky. They are distant horizon silhouettes, never foreground objects. Dreamlike and uncluttered with generous empty sky. Sky fills the entire frame, opaque full-bleed, no border. Palette strictly navy-violet, lilac, baby-blue, pastel pink, pearl white and tiny warm-gold accents. No foreground objects, no garden plants, no ground plane, no people, no human figures or faces, no likenesses, no bunny, no phones, no logos, no letters, no numbers, no words, no watermarks, no UI, no photorealism.
```

## ground-ward.png

Aspect: square. Target dimensions are recorded in spec.tsv.

```text
Use case: stylized-concept. Create exactly one square seamless tileable top-down floor texture for a fantasy hospital ward in a lavish glossy casual music game, art direction Y2K Starlight Stage. Orthographic straight-down view of a perfectly regular checkerboard of alternating soft baby-blue and pearl-white square floor tiles with very thin warm-gold grout lines. Show a balanced 4 by 4 repeat of equally sized squares, with the outer edges aligned to the repeating grid so opposite edges match precisely and the checkerboard continues seamlessly on every side. A few small pastel-pink decorative plus-shaped cross inlays and cute two-tone pink/lilac candy-capsule inlays sit centered inside separate tiles, sparsely distributed. Crosses are purely geometric decorative shapes; capsule inlays have no markings. Smooth polished enamel surfaces, delicate uniform soft gradient highlights contained within each individual tile, restrained glossy sheen, clean crisp shapes, softly rounded inlay details. Use the reference's baby-blue, pearl-white, pastel-pink, lilac and warm-gold palette; navy-violet only as a very subtle cool reflective tint. Flat even lighting identical across all four edges, no directional cast shadows. Opaque full-bleed repeating texture. Absolutely no perspective, no horizon, no vignette, no overall center glow, no outer frame, no surrounding room, no furniture, no raised objects, no people, no human figures or faces, no likenesses, no logos, no letters, no numbers, no words, no watermarks, no UI, no photorealism, no clutter.
```

## worker b
# Asset generation prompts

Generated with the built-in image_gen tool, one call per asset. Palette and finish follow `ref-concept.png`. Square aspect for both tiles and bunny; portrait 2:3 for the flip phone, the closest allowed aspect to its target.

## ground-stage.png

```text
Use case: stylized-concept. Final in-game seamless ground texture for a lavish Y2K Starlight Stage music game. Output exactly ONE square 1:1 image. Primary request: seamless top-down dark concert stage floor, deep navy-violet glossy panels with a subtle regular grid of tiny glowing pastel pink and baby-blue star dots and faint lilac-silver chrome seams. Match the provided art direction in words: midnight navy-violet, pastel pink, baby blue and lilac, restrained chrome and tiny warm gold accents; polished glossy stylized casual-game illustration, clean shapes, soft gradients, delicate glow. Orthographic straight-down flat surface only, full bleed, equal detail and brightness across the entire tile, even density, very subtle reflections. Perfectly seamless on all four edges for infinite repetition; panel seams and tiny star-dot rhythm continue across opposite edges. No perspective, no horizon, no vignette, no directional lighting gradient, no border, no focal object. Keep the pattern understated and readable at 512x512. NO people, NO human figures or human faces, NO likenesses, NO logos, NO letters, NO numbers, NO words, NO watermark, NO UI, NO photorealism, NO clutter. Opaque background.
```

## ground-garden.png

```text
Use case: stylized-concept. Final in-game seamless ground texture for a lavish Y2K Starlight Stage music game. Output exactly ONE square 1:1 image. Primary request: seamless top-down moonlit garden lawn, a deep lilac-blue grass texture with scattered tiny glowing pale baby-blue and pastel pink flowers and little warm gold sparkles, even density. Match this exact art direction: navy-violet night, pastel pink, baby blue, lilac, restrained glints of chrome and gold; polished glossy stylized casual-game illustration, clean simplified shapes, soft gradients and gentle magical glow. Very fine soft grass tufts, small simple five-petal flower heads seen straight from above, delicate sparse gold star sparkles integrated into the surface. Orthographic straight-down flat surface only, full bleed, equal brightness and detail across the entire tile. Perfectly seamless on all four edges for infinite repetition, with the same even flower and grass density at the edges and center. No perspective, no horizon, no vignette, no directional lighting gradient, no border, no focal object, no large flowers or ornaments. Readable and understated at 512x512. NO people, NO human figures or human faces, NO likenesses, NO logos, NO letters, NO numbers, NO words, NO watermark, NO UI, NO photorealism, NO clutter. Opaque background.
```

## flip-phone.png

```text
Use case: stylized-concept. Final isolated transparent PNG sticker asset for a lavish Y2K Starlight Stage music game. Output exactly ONE portrait 2:3 image. Primary request: one giant chrome Y2K flip phone monument standing open, pastel lilac-silver chrome body with fine warm gold trim; screen glowing soft pastel pink with exactly one simple white heart silhouette; physical keypad buttons are completely blank softly glowing pastel squares with no numbers or markings. Upright open clamshell phone with gently rounded corners and substantial polished hinge, near-front view with slight three-quarter depth so the open lower keypad and upper screen are both readable. Entire phone fully visible and centered, with generous clear transparent margins; a few small baby-blue, lilac and pale gold star sparkles close around the silhouette. Match the Y2K Starlight Stage art direction: navy-violet reflected shading, pastel pink, baby blue and lilac, mirror chrome and gold accents, cute luxurious polished glossy stylized casual-game rendering, clean shapes, soft gradients, delicate rim glow. Genuinely TRANSPARENT background with alpha channel, fully transparent corners and empty space; no painted checkerboard, no colored background, no floor, no environment, no pedestal, no ground shadow. This is a decorative physical sculpture, not an interface screenshot. NO people, NO human figures or human faces, NO likenesses, NO logos, NO letters, NO numbers, NO words, NO watermark, NO UI, NO status bars or icons except the requested single white heart, NO photorealism, NO clutter.
```

## bunny-giant.png

```text
Use case: stylized-concept. Final isolated transparent PNG sticker asset for a lavish Y2K Starlight Stage music game. Output exactly ONE square 1:1 image. Primary request: one giant cute white bunny statue sitting upright on a round pastel pink pedestal with a polished warm gold rim and small white pearls evenly arranged around its edge. Bunny has a soft glossy white porcelain finish, long upright rounded ears with pastel pink inner ears, tiny warm gold bow at its neck, two simple dark navy dot eyes and a tiny subtle pink nose; simple rounded paws and feet, sweet compact collectible-sculpture proportions. Front view with enough gentle depth to show the pedestal top, entire statue including ear tips and pedestal fully visible, centered with clear transparent margins. Match Y2K Starlight Stage art direction: navy-violet reflected shading, pastel pink, baby-blue and lilac highlights, gold accents; polished glossy stylized casual-game illustration, clean shapes, soft gradients, beautiful soft studio-style lighting and restrained glints. Genuinely TRANSPARENT background with alpha channel, fully transparent corners and all empty space; no painted checkerboard, no colored background, no floor, no environment, no ground shadow. Only the bunny and its attached pedestal. NO people, NO human figures or human faces, NO likeness of any real person, NO logos, NO letters, NO numbers, NO words, NO watermark, NO UI, NO photorealism, NO clutter.
```


## Validation

All four PNGs were copied unchanged from `$CODEX_HOME/generated_images`. Both alpha assets passed python3 + PIL validation: RGBA with all four corner pixels fully transparent. No regeneration or magenta-background fallback was needed. Native generated dimensions: stage 1254×1254; garden 1254×1254; phone 1024×1536; bunny 1254×1254.
## worker c
# Asset generation prompts

Generated with the built-in image_gen tool, one call per asset. Each call used `ref-concept.png` as a style reference and `transparent_background: true`. No regeneration or magenta fallback was needed.

## star-arch.png

```text
Use case: stylized-concept.
Create exactly ONE final in-game illustration asset: a big glowing gold-and-chrome star arch gate. Use the supplied ref-concept.png ONLY as a style and palette reference, not as a scene to reproduce. Match its Y2K Starlight Stage look: polished glossy stylized casual-game 3D illustration, clean rounded shapes, soft gradients, pastel pink / baby-blue / lilac surfaces, chrome and warm gold accents, navy-violet reflected shading, luminous jewel-like highlights.
Subject: a large pastel pink faceted five-point star crowns an elegant symmetrical rounded arch made of chrome and gold, small glowing bulbs spaced along the arch, subtle pastel baby-blue edge glow. Open empty passage under the arch. Front view, perfectly symmetrical, entire gate visible, centered, strong readable silhouette, generous transparent margin around all sides. Landscape 3:2 composition.
Background: genuinely TRANSPARENT PNG RGBA alpha, including the arch opening and all four corners. Isolated sticker asset, no floor, no environment, no background color or gradient, no opaque glow rectangle. Keep restrained soft glow attached to the object only.
Hard constraints: NO people, human figures, faces, member likenesses, logos, letters, numbers, words, watermarks, UI, photorealism, clutter, extra props, contact sheet or multiple variants. Render only this one gate at final production polish.
```

## ward-bed.png

```text
Use case: stylized-concept.
Create exactly ONE final in-game illustration asset: a fantasy hospital bed turned dreamy. Use supplied ref-concept.png ONLY as a style and palette reference. Match its Y2K Starlight Stage look: polished glossy stylized casual-game 3D illustration, clean shapes, soft gradients, pastel pink / baby-blue / lilac, reflective chrome and warm gold trim, navy-violet reflected shading, glowing jewel-like highlights. No photorealism.
Subject: an inviting empty white hospital-style bed with a plush pastel baby-blue quilt and fluffy white pillows, ornate gold headboard with five-point star finials; pink sheer curtains hang from a gold canopy rail around the headboard, half-open to reveal the bedding. One small candy-capsule-shaped pillow, half pastel pink and half baby-blue, rests on the quilt. Dreamy and cute, clean readable forms, restrained soft glow and small star-like highlights. Front three-quarter view, entire bed and canopy rail visible, centered, ample transparent margin on every side, landscape 3:2 composition.
Background: genuinely TRANSPARENT PNG RGBA alpha with transparent corners and transparent space surrounding the isolated bed; translucent sheer curtains retain real alpha. No floor, room, backdrop, ground shadow plane or background gradient. Glow is attached to the object only.
Hard constraints: NO people, human figures, faces, likenesses, patients, medical crosses, logos, letters, numbers, words, watermarks, UI, clutter, extra furniture, contact sheet or multiple variants. Render only this one cohesive bed sticker at final production polish.
```

## heart-pill.png

```text
Use case: stylized-concept.
Create exactly ONE final in-game illustration asset: a cute glossy candy capsule pill sticker. Use supplied ref-concept.png ONLY as the visual style and palette reference. Match its Y2K Starlight Stage polished stylized casual-game 3D look: clean rounded forms, soft gradients, glossy pearlescent finish, pastel pink / baby-blue / lilac, warm gold accents, subtle navy-violet reflected shading, crisp luminous specular highlights. No photorealism.
Subject: one simple plump rounded capsule, half pastel pink and half pastel baby-blue, tilted diagonally with pink toward upper left and blue toward lower right, a tiny gold five-point star highlight on its shell, soft close-fitting glow, plus exactly TWO small detached four-point sparkles. Keep the design simple and iconic, with a clear division between the two capsule halves. Center the whole composition, show the entire capsule and sparkles, ample transparent margin on all sides. Square 1:1 composition.
Background: genuinely TRANSPARENT PNG RGBA alpha including all four corners; isolated sticker, no floor, no environment, no colored background, no background gradient, no opaque glow rectangle. All exterior space remains transparent, with only a restrained translucent halo close to the capsule.
Hard constraints: NO people, human figures, faces, member likenesses, logos, letters, numbers, words, watermarks, UI, clutter, pill bottle, packaging, extra capsules, contact sheet or multiple variants. Render this one final production-quality sticker.
```

## call-bubble.png

```text
Use case: stylized-concept.
Create exactly ONE final in-game illustration asset: a glowing phone-call speech bubble sticker. Use supplied ref-concept.png ONLY as the style and palette reference. Match its Y2K Starlight Stage polished glossy stylized casual-game 3D illustration: clean shapes, soft gradients, pastel pink / baby-blue / lilac, chrome and warm gold accents, navy-violet reflected shading, luminous highlights. No photorealism.
Subject: a rounded pastel pink-to-lilac speech bubble with a short curved speech tail and an elegant reflective gold outline. Within the bubble put one simple solid white classic telephone-handset pictogram and exactly three curved ringing wave arcs; these are purely pictorial symbols, with no text. Restrained baby-blue edge light, soft local glow, and a few small four-point star sparkles around the bubble. Front view, centered, easy-to-read silhouette, entire bubble and sparkles visible, generous transparent margin on every side. Landscape 3:2 composition. This is a collectible game illustration object, not an app interface or button.
Background: genuinely TRANSPARENT PNG RGBA alpha including all four corners. Isolated sticker, no floor, no environment, no backdrop color, no background gradient, no opaque glow rectangle. Only restrained translucent glow close to the object.
Hard constraints: NO people, human figures, faces, member likenesses, logos, letters, numbers, words, watermarks, UI panels, screens, buttons, extra devices, clutter, contact sheet or multiple variants. Only this one production-polished bubble asset.
```

## worker d
# Asset prompts

Generated with the built-in image_gen tool. All assets use a square aspect ratio. The reference image is used only for style and palette.

One image_gen call was made per asset. Outputs were copied from /Users/bit_1/.codex/generated_images/01a14e04-dd98-7f30-8b0b-1f22a70f931e/ and resized with sips to the exact target dimensions. Both alpha assets passed python3/Pillow validation as RGBA PNGs with fully transparent corners, before and after resizing. No regeneration or magenta-background fallback was needed.

## stage-facade.png

```text
Use case: stylized-concept. Create exactly one square 1:1 final in-game building facade texture, target 1024x1024. Reference image: /Users/bit_1/nj-level-art/omg-v2/assets/wd/ref-concept.png is STYLE AND PALETTE REFERENCE ONLY: Y2K Starlight Stage, glossy stylized casual-game finish, navy-violet night, pastel pink, baby-blue and lilac, reflective chrome and delicate warm gold accents, clean shapes, soft gradients and controlled luminous bloom. Primary request: the front wall of a lavish Y2K concert stage building filling the entire frame. A big dark navy LED screen panel displays one large pastel pink heart with a few five-point pastel stars, framed on both sides by chrome speaker stacks with round glowing pastel-blue woofers, fine gold trim, and a neat string of glowing lights along the top edge. Composition: perfectly straight-on orthographic FRONT elevation, symmetrical, square full-bleed architectural wall artwork edge to edge, no surrounding scene, no sky margins, no floor, no perspective, no mockup, strong readable shapes for a game texture. Refined glossy chrome reflecting pink and lilac, subtle navy panel depth. Keep details deliberate and uncluttered. Hard constraints: NO people, human figures, faces, portraits or likenesses; NO logos, letters, numbers, words, typography, watermarks or UI anywhere. Only abstract heart and star symbols on the screen. Output one opaque full-bleed image.
```

transparent_background: false

## ward-facade.png

```text
Use case: stylized-concept. Create exactly one square 1:1 final in-game building facade texture, target 1024x1024. Reference image: /Users/bit_1/nj-level-art/omg-v2/assets/wd/ref-concept.png is STYLE AND PALETTE REFERENCE ONLY: Y2K Starlight Stage, polished glossy stylized casual-game look with clean shapes, soft gradients, controlled glow, navy-violet shadows, pastel pink, baby-blue and lilac, pearl-white, chrome and warm gold accents. Primary request: the front facade of a dreamy pastel hospital-palace filling the entire frame. Pearl-white wall with tall arched windows glowing softly warm, pastel pink sheer curtains visible inside, elegant gold window frames, a small pastel-blue candy-like plus/cross emblem above the central window, and a pastel lilac roof edge along the top. The cross must be only a simple equal-armed rounded geometric symbol with no text. Composition: perfectly straight-on orthographic FRONT elevation, symmetrical central arched window and two flanking tall arched windows, square full-bleed facade artwork edge to edge, no surrounding landscape or sky margins, no floor, no perspective, no mockup. Rich but clean sculpted glossy surfaces, lilac shadow recesses, warm gentle window glow, restrained gold detail. Hard constraints: NO people, human figures, faces, portraits or likenesses; NO logos, letters, numbers, words, typography, signage, watermarks or UI anywhere. No medical labels. Output one opaque full-bleed image.
```

transparent_background: false

## mural-stars.png

```text
Use case: stylized-concept. Create exactly one square 1:1 final in-game floor mural decal asset, target 1024x1024, isolated on a genuinely TRANSPARENT background with real alpha. Reference image: /Users/bit_1/nj-level-art/omg-v2/assets/wd/ref-concept.png is STYLE AND PALETTE REFERENCE ONLY: Y2K Starlight Stage, clean polished stylized casual-game look, pastel pink, baby-blue, lilac and warm gold highlights. Primary request: a circular ring of gold and pastel-pink five-point stars and tiny four-point sparkles surrounding a glowing pastel-blue heart. Perfectly direct TOP-DOWN orthographic view, flat painted floor-decal look, balanced circular composition centered in the square. Soft gradients, tidy silhouettes, subtle luminous painted highlights; no raised physical object, no extruded thickness, no cast shadow. One central blue heart and a spacious ring of distinct stars, uncluttered and readable in game. Artwork fits within the central 80 percent of the canvas, leaving transparent padding on all sides. Every space between the separate shapes and all four corners must be fully transparent. Gentle glow must fade into transparency, never into an opaque background. Do NOT draw a floor, colored backdrop, checkerboard or dark rectangle. Hard constraints: NO people, human figures, faces, portraits or likenesses; NO logos, letters, numbers, words, typography, watermarks or UI anywhere. Output one transparent PNG decal.
```

transparent_background: true

## sparkle.png

```text
Use case: stylized-concept. Create exactly one square 1:1 final in-game sparkle sprite, target 512x512, isolated on a genuinely TRANSPARENT background with real alpha. Reference image: /Users/bit_1/nj-level-art/omg-v2/assets/wd/ref-concept.png is STYLE AND PALETTE REFERENCE ONLY: Y2K Starlight Stage, polished glossy stylized casual-game finish, clean shapes, soft luminous gradients. Primary request: one single soft glowing FOUR-POINT star sparkle. Exactly four elegant tapered points aligned vertically and horizontally, symmetric around the center, bright white core fading through pale gold to a restrained pastel pink glow. Smooth soft edges and controlled bloom. One centered sparkle only, no extra stars, dots, rings or surrounding particles. Its glow fades completely to transparent with generous transparent padding and fully transparent corners. Main shape occupies the middle two-thirds of the square. No physical background or checkerboard. No cast shadow, no floor, no scene, no frame. Hard constraints: NO people, human figures, faces, portraits or likenesses; NO logos, letters, numbers, words, typography, watermarks or UI anywhere. Output one transparent PNG sprite.
```

transparent_background: true


## v3 corridor assets (2026-10-18 18:3x)
# Final asset prompts

Generated with the built-in `image_gen` tool, one call per asset, using `ref-concept.png` as the style and palette reference. `transparent_background: true` for every call. No regeneration or magenta fallback was needed.

Output preparation: copied from `$CODEX_HOME/generated_images`, downsampled to the target dimensions with Lanczos while retaining RGBA transparency. Negligible alpha values of 1/255 were rounded to zero to keep empty pixels fully transparent. Verified PNG format, RGBA mode and zero-alpha corners with Python 3 + Pillow; also verified the empty center of the curtain opening.

## light-tower.png

Target: 768 × 1152. Reference: `./ref-concept.png`. Tool option: `transparent_background: true`.

Exact prompt:

```text
Use case: stylized-concept.
Asset type: final transparent PNG game prop sticker, portrait 2:3 canvas, intended target 768 x 1152.
Input image: ref-concept.png is a STYLE AND PALETTE REFERENCE ONLY. Generate a single new isolated prop; do not reproduce its scene.
Primary request: a tall slender concert light tower: one chrome-and-gold lattice truss column standing upright, stacked rows of round glowing bulbs in pastel pink, baby-blue and warm gold running up its height, a glowing faceted pastel pink five-point star on top, a few small sparkles.
Composition: straight-on front view, full tower visible from its small base to the star tip with generous transparent margins. Tall narrow silhouette, centered. Clean readable shapes and restrained detail.
Style: lavish polished glossy stylized casual-game illustration in the exact Y2K Starlight Stage art direction of the reference: soft gradients, luminous pastel lighting, crisp chrome reflections, delicate warm gold edging, navy-violet reflected shadows, pink, baby-blue and lilac accents. No photorealism.
Background: genuinely TRANSPARENT alpha, including all four corners and all holes in the lattice. No colored background, no checkerboard drawing, no stage, no floor, no cast shadow plane. Keep glow small and localized around bulbs.
Hard constraints: exactly one tower. NO people, human figures, human faces, or likenesses. NO logos, letters, numbers, words, watermarks or UI anywhere. No unrelated objects, no clutter.
```

## spot-rig.png

Target: 1152 × 768. Reference: `./ref-concept.png`. Tool option: `transparent_background: true`.

Exact prompt:

```text
Use case: stylized-concept.
Asset type: final transparent PNG game prop sticker, landscape 3:2 canvas, intended target 1152 x 768.
Input image: ref-concept.png is a STYLE AND PALETTE REFERENCE ONLY. Generate a single new isolated prop; do not reproduce its scene.
Primary request: one stage spotlight rig: a horizontal chrome-and-gold lattice truss bar supported on two short legs, carrying exactly four round theatre spotlights tilted upward. The four lenses glow pastel pink, baby-blue, lilac and warm gold respectively, each with a small soft localized light flare.
Composition: straight-on front view of the whole rig; spotlights may show their upward tilt while their round luminous lenses remain visible. Entire horizontal bar, four fixtures and both feet visible, centered, generous transparent margins. Simple clean silhouette.
Style: lavish polished glossy stylized casual-game illustration in the exact Y2K Starlight Stage art direction of the reference: clean shapes, soft gradients, luminous pastel lighting, reflective chrome, warm gold trims, navy-violet reflected shadows, pastel pink, baby-blue and lilac. No photorealism.
Background: genuinely TRANSPARENT alpha, including all four corners and the gaps between truss bars and legs. No colored background, no checkerboard drawing, no stage, floor or shadow plane. No long beams of light; only soft flares close to the four lenses.
Hard constraints: exactly one rig, exactly four spotlights. NO people, human figures, human faces, or likenesses. NO logos, letters, numbers, words, watermarks or UI anywhere. No unrelated objects, no clutter.
```

## curtain.png

Target: 1152 × 768. Reference: `./ref-concept.png`. Tool option: `transparent_background: true`.

Exact prompt:

```text
Use case: stylized-concept.
Asset type: final transparent PNG game prop sticker, landscape 3:2 canvas, intended target 1152 x 768.
Input image: ref-concept.png is a STYLE AND PALETTE REFERENCE ONLY. Generate a new isolated proscenium prop; do not reproduce its scene.
Primary request: a grand stage proscenium FRAME ONLY: tall drawn-back pastel pink velvet curtains with gold fringe and gold tassels on both sides; an arched gold top valance studded with small glowing bulbs, crowned by one small pastel pink faceted five-point star. The side curtains hang in graceful lustrous folds and are tied back to expose a large central opening.
Composition: exact straight-on front view, symmetrical wide frame, entire star, arched top, both side curtains and bottom hems visible with transparent margins. Curtain sides slender enough for a large broad opening. No lower crossbar.
CRITICAL ALPHA REQUIREMENT: the large central opening between the curtains must be completely EMPTY and fully TRANSPARENT, alpha zero. This is a cutout arch that the game scene will show through. No backdrop fabric, no sky, no stage, no floor, no wall, no dark fill, no gradient, no haze, no glow, no floating sparkles or decoration across this empty central opening. The exterior surrounding the frame and all four corners must also be genuinely transparent. Confine any bulb glows to the gold frame itself. Do not draw a checkerboard.
Style: lavish polished glossy stylized casual-game illustration matching the exact Y2K Starlight Stage reference: clean shapes, soft gradients, pastel pink velvet with baby-blue and lilac reflected highlights, lustrous warm gold, small chrome accents, restrained navy-violet shading. No photorealism, no clutter.
Hard constraints: exactly one curtain frame. NO people, human figures, human faces, or likenesses. NO logos, letters, numbers, words, watermarks or UI anywhere. No unrelated objects.
```

# Generation prompts

Generated with the built-in image_gen tool, one call per asset. All used transparent_background=true and portrait 2:3 composition. PNGs are copied unchanged at their native 1024 × 1536 resolution. All three passed Python/PIL RGBA and transparent-corner verification; no magenta regeneration was needed.

## bunny-balloon.png

```text
Use case: stylized-concept. Final in-game illustration asset for a lavish Y2K Starlight Stage rhythm game. Match this exact art direction: polished glossy stylized casual-game 3D illustration, clean rounded shapes, luxurious pearl/chrome materials with soft gradients, luminous soft highlights and restrained glow. Palette exclusively pearl white, pastel pink, baby blue, lilac, navy-violet reflections and warm pale gold accents. No photorealism, no clutter. Portrait 2:3 aspect ratio, intended target 768 x 1152. Front view, single centered isolated sticker, whole balloon and entire curly ribbon visible, comfortable transparent margins on all sides. Genuinely TRANSPARENT background with alpha, including completely transparent corners; no colored background, no checkerboard pattern, no floor, no cast shadow, no scenery, no stage, no frame. No people, no human figures or human faces, no celebrity likenesses. No logos, letters, numbers, words, watermarks or UI anywhere.
Subject: one giant floating foil balloon shaped like a cute white bunny HEAD with two long ears, glossy pearl-white mylar, pastel pink inner ears, soft lilac and baby-blue reflections, two tiny navy dot eyes as a simple animal expression, a tiny subtle pink nose, a small warm gold bow at the balloon neck. A single thin pale gold curly ribbon string hangs gracefully below. Bunny head only, no body. Subtle foil edge seam and sparse soft fold highlights, clean friendly silhouette. No additional objects.
```

## heart-balloon.png

```text
Use case: stylized-concept. Final in-game illustration asset for a lavish Y2K Starlight Stage rhythm game. Match this exact art direction: polished glossy stylized casual-game 3D illustration, clean rounded shapes, luxurious pearl/chrome materials with soft gradients, luminous soft highlights and restrained glow. Palette exclusively pearl white, pastel pink, baby blue, lilac, navy-violet reflections and warm pale gold accents. No photorealism, no clutter. Portrait 2:3 aspect ratio, intended target 768 x 1152. Front view, single centered isolated sticker, whole balloon and entire curly ribbon visible, comfortable transparent margins on all sides. Genuinely TRANSPARENT background with alpha, including completely transparent corners; no colored background, no checkerboard pattern, no floor, no cast shadow, no scenery, no stage, no frame. No people, no human figures or human faces, no celebrity likenesses. No logos, letters, numbers, words, watermarks or UI anywhere.
Subject: one giant floating glossy chrome heart-shaped foil balloon in pastel pink with baby-blue and lilac reflections, sculpted rounded lobes, a warm gold knot at its tapered lower tip. A single thin pale gold curly ribbon string hangs gracefully below, and a few tiny restrained four-point sparkles hover close to the balloon. Subtle foil edge seam and soft inflated folds, mirror-polished yet simplified stylized material. No face and no additional objects.
```

## star-balloon.png

```text
Use case: stylized-concept. Final in-game illustration asset for a lavish Y2K Starlight Stage rhythm game. Match this exact art direction: polished glossy stylized casual-game 3D illustration, clean rounded shapes, luxurious pearl/chrome materials with soft gradients, luminous soft highlights and restrained glow. Palette exclusively pearl white, pastel pink, baby blue, lilac, navy-violet reflections and warm pale gold accents. No photorealism, no clutter. Portrait 2:3 aspect ratio, intended target 768 x 1152. Front view, single centered isolated sticker, whole balloon and entire curly ribbon visible, comfortable transparent margins on all sides. Genuinely TRANSPARENT background with alpha, including completely transparent corners; no colored background, no checkerboard pattern, no floor, no cast shadow, no scenery, no stage, no frame. No people, no human figures or human faces, no celebrity likenesses. No logos, letters, numbers, words, watermarks or UI anywhere.
Subject: one giant floating glossy FIVE-POINT star-shaped foil balloon in pale warm gold and pearl white with pastel pink and baby-blue reflections, rounded inflated points and a tiny pale gold tied neck. A single thin pale gold curly ribbon string hangs gracefully below, and a few tiny restrained four-point sparkles hover close to the balloon. Subtle foil edge seam and soft inflated folds, polished stylized material. No face and no additional objects.
```

# Final asset prompts

Generated with the built-in image_gen tool, one call per asset, with `transparent_background: true`.

## moon-flower.png

```text
Use case: stylized-concept.
Asset type: final in-game illustration, isolated transparent PNG sticker for a lavish Dancing Line style music level.
Art direction: Y2K Starlight Stage. Match the supplied ref-concept.png visual language: polished glossy stylized casual-game 3D illustration, clean rounded shapes, soft gradients, pearly translucent materials, chrome and gold accents, delicate star sparkles and gentle luminous bloom. Restrict the palette to pastel pink, baby-blue, lilac, pearly white, pale gold and chrome with subtle navy-violet reflected shading. No photorealism, no clutter.
Background: genuinely transparent alpha, including all four corners; no painted checkerboard, no solid backdrop, no scenery, no ground plane or cast floor shadow. Preserve soft glow with translucent alpha.
Subject: one giant magical glowing garden flower: tall gracefully curved stem with exactly two leaves, a big open bloom of translucent lilac and baby-blue petals glowing softly from within, a pearly glowing center with tiny gold sparkles. Stylized lilac-blue stem and leaves, moonlit fairy-tale mood.
Composition: portrait 2:3 aspect ratio. Front view. Whole plant visible from stem base to highest petal, centered with comfortable transparent margins. Bloom large and legible, elegant single curved stem, two clearly separated leaves; a small restrained handful of tiny gold sparkles near the bloom.
Hard constraints: NO people, NO human figures or faces, NO likeness of any NewJeans member. NO logos, letters, numbers, words, watermark or UI anywhere. Exactly one complete isolated asset, no extra objects beyond the specified ornamentation, no mockup, no collage.
```

## lantern.png

```text
Use case: stylized-concept.
Asset type: final in-game illustration, isolated transparent PNG sticker for a lavish Dancing Line style music level.
Art direction: Y2K Starlight Stage. Match the supplied ref-concept.png visual language: polished glossy stylized casual-game 3D illustration, clean rounded shapes, soft gradients, pearly translucent materials, chrome and gold accents, delicate star sparkles and gentle luminous bloom. Restrict the palette to pastel pink, baby-blue, lilac, pearly white, pale gold and chrome with subtle navy-violet reflected shading. No photorealism, no clutter.
Background: genuinely transparent alpha, including all four corners; no painted checkerboard, no solid backdrop, no scenery, no ground plane or cast floor shadow. Preserve soft glow with translucent alpha.
Subject: one ornate garden lantern post: slender gently curved gold-and-chrome lamp post with a hanging round lantern of pastel pink glass glowing warmly, delicate tiny star filigree and a few floating sparkles. Rounded glossy decorative foot, slim elegant shaft, curved hook holding the round glass lantern, polished gold trim with cool chrome highlights. Soft pastel pink internal light.
Composition: portrait 2:3 aspect ratio. Front view. Whole post visible from its base to its highest curved tip, centered with comfortable transparent margins. Clear readable silhouette, restrained ornament, no surrounding environment.
Hard constraints: NO people, NO human figures or faces, NO likeness of any NewJeans member. NO logos, letters, numbers, words, watermark or UI anywhere. Exactly one complete isolated asset, no extra objects beyond the specified ornamentation, no mockup, no collage.
```

## crescent-moon.png

```text
Use case: stylized-concept.
Asset type: final in-game illustration, isolated transparent PNG sticker for a lavish Dancing Line style music level.
Art direction: Y2K Starlight Stage. Match the supplied ref-concept.png visual language: polished glossy stylized casual-game 3D illustration, clean rounded shapes, soft gradients, pearly translucent materials, chrome and gold accents, delicate star sparkles and gentle luminous bloom. Restrict the palette to pastel pink, baby-blue, lilac, pearly white, pale gold and chrome with subtle navy-violet reflected shading. No photorealism, no clutter.
Background: genuinely transparent alpha, including all four corners; no painted checkerboard, no solid backdrop, no scenery, no ground plane or cast floor shadow. Preserve soft glow with translucent alpha.
Subject: one big glowing crescent moon ornament: smooth thick pearly pale-gold crescent moon with soft luminous halo, exactly two small hanging gold five-pointed stars dangling from two thin delicate gold chains beneath it, a few tiny sparkles. Rounded polished crescent surface, cool lilac and baby-blue reflected highlights, luminous creamy pale-gold inner edge. Simple sumptuous polished ornament.
Composition: square 1:1 aspect ratio. Front view. Entire crescent, both chains and both hanging stars visible, centered with comfortable transparent margins. Crescent opens toward the right; two small stars hang at different lengths beneath the lower arc. Clean readable silhouette.
Hard constraints: NO people, NO human figures or faces, NO likeness of any NewJeans member. NO logos, letters, numbers, words, watermark or UI anywhere. Exactly one complete isolated asset, no extra objects beyond the specified ornamentation, no mockup, no collage.
```

Validation: all final PNGs are RGBA with transparent corners. No flat #FF00FF regeneration was needed. Outputs were copied from $CODEX_HOME/generated_images and resized to the spec.tsv target dimensions with alpha preserved.

# Asset prompts

Generated with the built-in image_gen tool. All four assets use square (1:1) composition and request genuine transparency.

## wreath-star.png

```text
Use case: stylized-concept. Create exactly ONE finished in-game floor-emblem sticker asset for a lavish music rhythm game in the Y2K Starlight Stage art direction. Square 1:1 canvas, target use 768 x 768. Polished glossy stylized casual-game illustration, crisp clean shapes, soft gradients, pearlescent shine, delicate chrome and pale-gold trim, restrained luminous highlights. Strict shared palette: pastel pink, baby-blue, lilac, pearl-white, pale gold, with only subtle navy-violet reflections. Camera perfectly straight overhead, flat orthographic, no perspective, no tilt, no visible side walls. Centered balanced symmetric circular composition occupying about 82 percent of the canvas; leave clear padding on all sides. Background genuinely transparent with real alpha, including the corners and the open spaces between separate motifs. No opaque background, no ground plane, no disk, no checkerboard pattern. Keep glow tight to each object so the sticker remains clean. NO people, no human figures or human faces, no member likenesses. NO logos, letters, numbers, words, watermark, UI, frame, or mockup. No photorealism, no clutter.
Subject: a circular wreath of small glowing pastel five-point stars and luminous round pearls in baby-blue and pale gold, evenly arranged with clear gaps. In the center floats one plump glossy pastel-pink heart with a fine pale-gold edge and soft pink glow. The stars alternate in size in a deliberate symmetrical rhythm, with only a few tiny four-point glints. All motifs lie in the same flat top-down plane; the central heart is clearly separated from the surrounding wreath by transparent negative space.
```

## wreath-flower.png

```text
Use case: stylized-concept. Create exactly ONE finished in-game floor-emblem sticker asset for a lavish music rhythm game in the Y2K Starlight Stage art direction. Square 1:1 canvas, target use 768 x 768. Polished glossy stylized casual-game illustration, crisp clean shapes, soft gradients, pearlescent shine, delicate chrome and pale-gold trim, restrained luminous highlights. Strict shared palette: pastel pink, baby-blue, lilac, pearl-white, pale gold, with only subtle navy-violet reflections. Camera perfectly straight overhead, flat orthographic, no perspective, no tilt, no visible side walls. Centered balanced symmetric circular composition occupying about 82 percent of the canvas; leave clear padding on all sides. Background genuinely transparent with real alpha, including the corners and the open spaces between separate motifs. No opaque background, no ground plane, no disk, no checkerboard pattern. Keep glow tight to each object so the sticker remains clean. NO people, no human figures or human faces, no member likenesses. NO logos, letters, numbers, words, watermark, UI, frame, or mockup. No photorealism, no clutter.
Subject: a circular wreath of small lilac and pastel-pink five-petal flowers and delicate stylized leaves in lilac and baby-blue, with a few tiny pale-gold sparkles, arranged evenly and symmetrically. Petals have smooth glossy enamel gradients and small pearl-white or pale-gold centers. In the center floats one glowing plump pastel baby-blue heart with a fine pale-gold edge. All motifs lie in the same flat top-down plane; the central heart is clearly separated from the floral wreath by transparent negative space. Keep the floral forms simple and readable, no dense bouquet.
```

## wreath-ribbon.png

```text
Use case: stylized-concept. Create exactly ONE finished in-game floor-emblem sticker asset for a lavish music rhythm game in the Y2K Starlight Stage art direction. Square 1:1 canvas, target use 768 x 768. Polished glossy stylized casual-game illustration, crisp clean shapes, soft gradients, pearlescent shine, delicate chrome and pale-gold trim, restrained luminous highlights. Strict shared palette: pastel pink, baby-blue, lilac, pearl-white, pale gold, with only subtle navy-violet reflections. Camera perfectly straight overhead, flat orthographic, no perspective, no tilt, no visible side walls. Centered balanced symmetric circular composition occupying about 82 percent of the canvas; leave clear padding on all sides. Background genuinely transparent with real alpha, including the corners and the open spaces between separate motifs. No opaque background, no ground plane, no disk, no checkerboard pattern. Keep glow tight to each object so the sticker remains clean. NO people, no human figures or human faces, no member likenesses. NO logos, letters, numbers, words, watermark, UI, frame, or mockup. No photorealism, no clutter.
Subject: a circular ring made of looping pastel-pink satin ribbon, with smooth repeated scalloped loops arranged symmetrically and four small pale-gold ribbon bows at the top, right, bottom, and left. Ribbon highlights are lilac and pearl-white. In the center floats one glowing pearl-white bunny-head silhouette, a simple round head joined to two long upright ears; a completely featureless silhouette with no eyes, nose, mouth or facial marks. The central silhouette is separated from the ribbon ring by generous transparent negative space. Everything lies in the same flat top-down plane. No other objects.
```

## wreath-moon.png

```text
Use case: stylized-concept. Create exactly ONE finished in-game floor-emblem sticker asset for a lavish music rhythm game in the Y2K Starlight Stage art direction. Square 1:1 canvas, target use 768 x 768. Polished glossy stylized casual-game illustration, crisp clean shapes, soft gradients, pearlescent shine, delicate chrome and pale-gold trim, restrained luminous highlights. Strict shared palette: pastel pink, baby-blue, lilac, pearl-white, pale gold, with only subtle navy-violet reflections. Camera perfectly straight overhead, flat orthographic, no perspective, no tilt, no visible side walls. Centered balanced symmetric circular composition occupying about 82 percent of the canvas; leave clear padding on all sides. Background genuinely transparent with real alpha, including the corners and the open spaces between separate motifs. No opaque background, no ground plane, no disk, no checkerboard pattern. Keep glow tight to each object so the sticker remains clean. NO people, no human figures or human faces, no member likenesses. NO logos, letters, numbers, words, watermark, UI, frame, or mockup. No photorealism, no clutter.
Subject: a circular ring of tiny glowing crescent moons and small pearl-like dots in alternating lilac and pale gold, spaced evenly in a precisely balanced symmetrical arrangement. Crescent tips have graceful clean curves and pearlescent glossy surfaces. In the center floats one large luminous four-point star, pearl-white with baby-blue and lilac gradient highlights and a fine pale-gold edge. The central four-point star is clearly separated from the moon ring by transparent negative space. Everything lies in the same flat top-down plane. Restrained small sparkle accents, no extra planets, no clouds.
```

## wreath-flower.png — transparency fallback regeneration

The first PNG was RGBA, but its bottom-left corner had alpha 1 rather than 0. Regenerated once using flat #FF00FF background preparation and requesting genuine transparent output. Tool parameter: transparent_background=true.

```text
Use case: stylized-concept. Create exactly ONE finished in-game floor-emblem sticker asset for a lavish music rhythm game in the Y2K Starlight Stage art direction. Square 1:1 canvas, target use 768 x 768. Polished glossy stylized casual-game illustration, crisp clean shapes, soft gradients, pearlescent shine, delicate chrome and pale-gold trim, restrained luminous highlights. Strict shared palette: pastel pink, baby-blue, lilac, pearl-white, pale gold, with only subtle navy-violet reflections. Camera perfectly straight overhead, flat orthographic, no perspective, no tilt, no visible side walls. Centered balanced symmetric circular composition occupying about 82 percent of the canvas; leave clear padding on all sides. Transparency fallback: render the isolated emblem against a perfectly uniform flat #FF00FF magenta chroma background for clean separation, with no magenta reflections or magenta details on the emblem. Remove that flat magenta background in the delivered image, including all open spaces between the motifs, and deliver genuine RGBA transparency with exactly zero alpha at all four corners. No ground plane, no disk, no checkerboard pattern. Keep glow tight to each object so the sticker remains clean. NO people, no human figures or human faces, no member likenesses. NO logos, letters, numbers, words, watermark, UI, frame, or mockup. No photorealism, no clutter.
Subject: a circular wreath of small lilac and pastel-pink five-petal flowers and delicate stylized leaves in lilac and baby-blue, with a few tiny pale-gold sparkles, arranged evenly and symmetrically. Petals have smooth glossy enamel gradients and small pearl-white or pale-gold centers. In the center floats one glowing plump pastel baby-blue heart with a fine pale-gold edge. All motifs lie in the same flat top-down plane; the central heart is clearly separated from the floral wreath by transparent negative space. Keep the floral forms simple and readable, no dense bouquet.
```
