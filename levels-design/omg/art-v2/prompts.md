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

