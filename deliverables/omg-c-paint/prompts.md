# Image generation prompts

Generated with the built-in image_gen tool, one call per asset. Reference renders were opened and visually inspected before generation.

## z01-ground.png

```text
Use case: stylized-concept.
Asset type: final seamless square ground texture for a pop-up papercraft storybook rhythm game, z01-ground.png.
Create ONE square 1:1 texture, camera exactly vertically overhead, orthographic, flat ground surface filling the entire image. Soft mint-green paper grass carpet with small scattered cream and pale peach paper flowers, tiny warm yellow flower centers and mint clover leaves. Match the morning-light palette of the viewed z01-key.jpg: muted seafoam mint, sage, warm ivory, pale apricot-peach, softly golden diffuse light. Soft painted papercraft storybook look, layered hand-cut paper blades and petals, delicate fibrous matte paper grain and subtle shallow paper-layer shadows. Medium-small detail scale, evenly distributed edge to edge, quiet carpet suitable for gameplay. No single focal object. All plants lie flat as seen from directly above.
CRITICAL: truly seamless repeating texture in BOTH axes. Opposite left/right and top/bottom edges must have matching colors, density, texture and continuing motifs; any motif crossing an edge continues at the opposite edge. Uniform overall illumination, no center glow, no corner darkening, no vignette, no border, no empty edge margin. No horizon or perspective.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, typography, watermark, UI, roads or paths. No landscape scene, trees, hills, buildings, book, pedestal or foreground object. Rich but harmonious color, gentle soft lighting, no photorealism.
```

## z01-backdrop.png

```text
Use case: stylized-concept.
Asset type: final wide panoramic distant horizon backdrop for a pop-up papercraft storybook rhythm game, z01-backdrop.png.
Generate ONE image in the widest available landscape aspect, aiming for a very wide 4:1 panorama. Match the palette and gentle morning mood of the viewed z01-key.jpg: pale mint, misty seafoam sage, warm ivory, delicate apricot-peach and golden cream sunlight. The upper TWO THIRDS of the entire image is open pale mint-to-peach morning sky, a very soft painted gradient with faint wispy paper-cloud haze. The distant scenery is strictly confined to the BOTTOM THIRD: several low overlapping layers of softly rolling mint-green cut-paper hills, tiny distant round-canopy paper trees, pale mist between the layers. Everything remains far away, small and quiet. Hills touch the bottom edge, with no foreground objects. Low horizon, broad tranquil sky, very shallow distant relief.
Style: soft painted papercraft storybook illustration, gently folded and hand-cut matte paper layers, lightly fibrous texture, rich but harmonious pastel color, delicate ambient shadows and soft diffuse warm morning lighting. Scenic atmosphere, no photorealism. No prominent sun disk, no strong lighting hotspot. Keep the left and right edges at identical sky colors and matching low hill heights and tones so the panorama blends when wrapped.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, typography, watermark, UI, roads or paths. No foreground trees, flowers or objects, no book, no bridge, no elevated track, no border, no frame. Only distant low rolling hills and round trees along the bottom, open sky above.
```

## z02-ground.png

```text
Use case: stylized-concept.
Asset type: final seamless square ground texture for a pop-up papercraft storybook rhythm game, z02-ground.png.
Create ONE square 1:1 texture, camera exactly vertically overhead, orthographic, flat ground surface filling the entire image. Lush bright spring-green paper grass carpet densely scattered with small sunny yellow and coral-red paper tulips, white paper daisies with yellow centers, and green leaves. Match the bright spring daylight palette of the viewed z02-key.jpg: fresh apple and leaf greens, sunny butter yellow, warm coral red, soft ivory white. Soft painted papercraft storybook look, layered hand-cut and folded paper leaves and petals, gently faceted folded tulip petals, delicate matte paper grain and subtle shallow layer shadows. Medium-small detail scale, balanced dense distribution of small flowers and grass evenly edge to edge. Texture rather than a flower arrangement, no central motif. All flowers and leaves seen directly from above, with foreshortened tulip cups and no upright side-view stems. No single focal object.
CRITICAL: truly seamless repeating texture in BOTH axes. Opposite left/right and top/bottom edges must match in colors, density, texture and continuing motifs; any motif crossing an edge continues at the opposite edge. Uniform overall bright diffuse illumination, no center glow, no corner darkening, no vignette, no border, no empty edge margin. No horizon or perspective.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, typography, watermark, UI, roads or paths. No landscape scene, trees, hills, cottages, buildings, book, pedestal or foreground object. Rich but harmonious color, gentle soft lighting, no photorealism.
```

## z02-backdrop.png

```text
Use case: stylized-concept.
Asset type: final wide panoramic distant horizon backdrop for a pop-up papercraft storybook rhythm game, z02-backdrop.png.
Generate ONE image in the widest available landscape aspect, aiming for a very wide 4:1 panorama. Match the palette, lighting and paper craft mood of the viewed z02-key.jpg: bright clear spring-blue sky, white and cream folded-paper clouds, fresh apple-green and sage-green hills, warm ivory cottage walls, coral-red roofs and sunny buttery yellow details. The upper TWO THIRDS of the entire image is open bright blue sky with a few soft puffy layered paper clouds, plenty of spacious blue between them. The distant scenery is strictly confined to the BOTTOM THIRD: gently rolling green papercraft hills in several shallow overlapping layers, tiny faraway cottages with paired bunny-ear roof ornaments made of ivory and pale coral folded paper, and a few very small distant traditional four-sail windmill silhouettes. The bunny-ear details are abstract roof ornaments only, no eyes or faces. Buildings are tiny accents nestled into the faraway hills, all under the low horizon band. Everything stays distant and small; no close buildings, no foreground objects. Soft hazy depth, gentle bright spring daylight.
Style: soft painted papercraft storybook illustration, hand-cut matte paper layers and subtly folded geometric forms, delicate paper texture, soft ambient shadows, rich but harmonious colors, no photorealism. Keep the left and right edges at matching blue sky colors and low hill heights and tones so it can wrap. No strong sun hotspot.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, typography, watermark, UI, roads or paths. No foreground trees, flowers, fences or objects, no book, bridge or elevated track, no frame, no border. Only distant hills, tiny cottages and windmills along the bottom third, open blue sky and paper clouds above.
```

# Image generation prompts

Generated with the built-in image_gen tool. Each asset used a separate call. Both ground tiles received one seam-correction retry; the retry is the saved final image. Dimensions are left at generation size for later resizing.

## z03-ground.png

### Initial generation

```text
Use case: stylized-concept.
Create exactly one final in-game ground texture image, square 1:1, for z03-ground.png in a pop-up papercraft storybook rhythm game.
Reference direction: match the already viewed ../refs/z03-key.jpg: warm peach and blush cream paper surfaces, coral orange and soft rose pink flowers, golden sunset illumination, gentle lavender paper shadows, softly painted folded and layered cardstock. Preserve that warm harmonious storybook palette and tactile cut-paper finish, without copying its scene or road.
Subject: a warm peach paper ground carpet with scattered tiny orange and pink paper flowers and very subtle paper grid tile hints. Medium-small detail scale; numerous tiny simple paper blossoms distributed evenly, restrained low-relief layered petals and fine matte paper grain. The grid must be faint square sheet joins, never roads or paths.
Composition: perfectly straight-down orthographic flat texture, no perspective, no horizon, no vignette, no central focal object. Equal detail density and identical soft light across the whole square, including all edges. Seamless repeat in both axes: left and right boundary colors and motifs continue exactly, top and bottom boundary colors and motifs continue exactly; no border, no edge shading, no large interrupted flowers on boundaries. Use a consistent quiet peach paper base at all four edges with tiny paper grain and evenly dispersed tiny blossoms, making repeats invisible.
Style: soft painted papercraft storybook art, cut-paper layers, gentle soft ambient sunset lighting, rich but harmonious colors, no photorealism. This is a material texture swatch filling the entire canvas, not a photographed sheet or diorama.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, text, watermarks, UI, roads or paths. Opaque image.
```

### Seam-correction retry — saved final

```text
Use case: stylized-concept.
Generate exactly one SQUARE 1:1 seamless repeating ground texture, z03-ground.png, for a papercraft storybook game. This is the seam-correction retry.
Match the colors and soft cut-paper finish of the viewed ../refs/z03-key.jpg: peach cream and warm blush paper, coral orange and rose pink tiny paper flowers, delicate golden sunset ambient light and soft lavender shadows. Soft painted storybook, tactile matte cardstock layers, gentle light, rich harmonious color, no photorealism.
Straight-down orthographic material swatch. Cover the whole canvas with a warm peach paper ground carpet and many evenly scattered TINY orange and pink paper flowers. Very faint same-color square paper sheet grid hints. Medium-small detail scale, low relief, equal density and illumination everywhere. No perspective, horizon, vignette, spotlight, border or central subject.
CRITICAL SEAMLESSNESS: treat the canvas as a mathematical torus, wrapping all motifs and paper grain in both axes. Left/right edges and top/bottom edges must match in base color, grid alignment, shadows and every crossing petal. If a flower crosses an edge, its exact remainder must emerge at the corresponding coordinate on the opposite edge. Favor tiny sparse blossom fragments at boundaries and a consistent peach base without shading gradients, so joins disappear. No ragged sheet seams that terminate at unmatched locations. Tiny motifs distributed with equal density through the whole image; avoid oversized flowers. Do not make a visible frame or blank perimeter.
Hard exclusions: no people, human figures, faces, animals, logos, letters, numbers, words, watermarks, UI, road or path of any kind. Opaque full-bleed texture.
```

## z03-backdrop.png

```text
Use case: stylized-concept.
Create exactly one final wide panoramic BACKDROP image, z03-backdrop.png, for a pop-up papercraft storybook rhythm game. Use the widest available landscape generation aspect, ideally a 4:1 panoramic horizon band; the intended later output is 2048 by 512. Fill the canvas with the image, no letterbox borders.
Match the viewed ../refs/z03-key.jpg palette and mood: deep muted violet upper sunset sky melting through dusky mauve and coral into warm apricot orange and peach at the horizon; lavender and blush cream layered paper architecture, gently glowing amber windows, muted teal pine accents and soft golden light. Tactile folded cardstock, delicate painted paper grain and cut-paper layers; charming storybook finish, gentle soft lighting, rich harmonious color, no photorealism.
Composition: a broad quiet sunset sky occupies the UPPER TWO THIRDS of the frame. ONLY the LOWER THIRD contains very distant warm papercraft rooftops, a modest distant clock tower silhouette, and a few tiny muted teal pine silhouettes, in shallow layered bands. All buildings remain small and far away, the clock tower fully contained in the lower third. Its clock is a tiny simple blank circular paper inset, with NO numerals, tick marks, symbols or face-like features. No foreground objects, no close buildings, no floor or ground plane visible. The distant silhouettes sit along the bottom edge. Soft aerial perspective and subtle cut-paper layering, no dramatic focal scene. A few delicate painted cloud wisps are acceptable.
Horizontal wrapping: left and right edges must blend naturally with exactly the same horizon height, sky gradient colors, distant scenery scale and illumination. Avoid prominent structures at either side edge.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, watermark, UI, roads or paths anywhere. No giant moon, no floating foreground props. Opaque full-bleed panoramic artwork.
```

## z04-ground.png

### Initial generation

```text
Use case: stylized-concept.
Generate exactly one final SQUARE 1:1 seamless repeating ground texture, z04-ground.png, for a pop-up papercraft storybook rhythm game.
Reference palette and mood: match the viewed ../refs/z04-key.jpg, a magical pop-up castle at night with deep navy and indigo shadows, lavender violet paper folds, rosy pink blossoms, warm creamy gold highlights and gentle star glow. Use its soft painted cut-paper storybook finish and rich harmonious colors, no photorealism.
Subject: a DEEP INDIGO moss carpet made of tiny flat overlapping paper moss shapes, scattered with many TINY glowing pink and warm gold paper flowers and a restrained scattering of miniature four-point star sparkles. Indigo must remain the dominant ground color. Layered matte cardstock, fine paper grain, delicate low-relief petals, lavender blue subtle shadowing, very gentle local golden glow around tiny accents. Medium-small detail scale, equal density across the entire square. No oversized flowers, no large star, no focal object.
Camera and composition: straight down, perfectly orthographic flat material swatch, no perspective, no horizon, no vignette, no spotlight or central glow, no border, no hills or landscape. Even soft ambient night illumination from edge to edge.
CRITICAL: fully seamless tileable on ALL FOUR edges. Treat the texture as a mathematical torus. Opposite edges must continue exactly, including moss, petals, sparkles and shadow direction. A motif crossing the left boundary must resume exactly at the corresponding point on the right; similarly top and bottom. Consistent indigo base tone and fine paper texture at every boundary, no mismatched edge shading, no blank perimeter. Avoid large cut-off blossoms on edges; use tiny evenly dispersed motifs throughout.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, text, watermarks, UI, road or path. No buildings, moon or horizon. Opaque full-bleed texture.
```

### Seam-correction retry — saved final

```text
Use case: stylized-concept.
Generate exactly ONE SQUARE 1:1 final seamless repeating texture for z04-ground.png. This is a seam-correction retry: the previous version's opposite edge strips did not match, so prioritize true periodic borders.
Reference style: the viewed ../refs/z04-key.jpg, magical night pop-up papercraft storybook, rich deep indigo navy shadows, lavender violet paper layers, soft rose pink blossoms and creamy warm gold star glows. Tactile matte painted cut-paper layers and gentle soft light, no photorealism.
Subject: a deep indigo PAPER MOSS CARPET, tiny flattened indigo and muted violet moss flecks over a mostly even navy-indigo paper base. Evenly scatter miniature pink and pale gold cut-paper flowers, delicate four-point golden star sparkles and tiny gold pinpricks. Keep the details medium-small and restrained, with no big leaves or oversized flowers. The ground must remain mostly deep indigo with fine softly painted paper texture. Shallow paper relief only, subtle soft contact shadows, no dramatic shadows or light gradient. Dense enough for a game ground carpet, equal motif density edge to edge, no blank margin.
Perfectly top-down orthographic flat material texture, filling every pixel, no perspective, horizon, vignette, landscape, focal object, central glow or frame.
TRUE SEAMLESS REPEAT ON BOTH AXES: build a toroidal periodic texture. The first and last columns must have identical base tones and connected motifs at every y coordinate; the first and last rows must have identical base tones and connected motifs at every x coordinate. Any clipped flower, moss fleck or sparkle must have its exact matching other half at the opposite edge. Use small motifs and gentle uniform navy-indigo at the boundaries to hide joins. Avoid large features crossing the edge. Align the paper grain and colors across all four boundaries. Do not merely crop an arbitrary floral pattern. No visible border, no lighter edge strips.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, text, watermark, UI, road, path, buildings or moon. Opaque square texture.
```

## z04-backdrop.png

```text
Use case: stylized-concept.
Create exactly one final WIDE PANORAMIC BACKDROP, z04-backdrop.png, for a pop-up papercraft storybook rhythm game. Use the widest available landscape generation aspect, ideally a 4:1 horizon band; intended later output 2048 by 512. Full-bleed artwork without borders or letterboxing.
Match the viewed ../refs/z04-key.jpg: deep navy midnight sky, indigo and lavender violet paper layers, rosy pink accents, creamy ivory castle walls, warmly glowing golden windows, muted teal pine silhouettes, a luminous faceted golden paper crescent and delicate gold star points. Soft painted papercraft storybook look, matte cut-paper grain and folds, gentle magical soft lighting, rich harmonious colors, no photorealism.
Composition: the UPPER TWO THIRDS is open deep navy night sky with scattered tiny golden and pale pink star sparkles and ONE modest crescent moon made of softly folded golden paper, suspended high above the distant skyline. A few restrained lavender layered-paper cloud wisps. The entire LOWER THIRD is a small very distant glowing pop-up paper castle skyline with elegant lavender pointed rooftops and tiny warm windows, shallow lavender hill silhouettes and dark muted teal pine silhouettes. Keep the castle and every tree entirely within the bottom third, small and far away. All distant scenery is arranged in shallow cut-paper layers along the bottom edge, soft atmospheric separation. No foreground objects, no close-up architecture, no ground plane or water foreground. No large floating props, strings, frames or ornaments.
Horizontal wrap: left and right edges have matching navy sky colors, star density, horizon height and dark distant scenery color, so they blend naturally. Avoid a focal castle tower or moon touching either edge. Soft even illumination, no vignette.
Hard exclusions: NO people, human figures, faces, animals, logos, letters, numbers, words, text, watermarks, UI, roads or paths anywhere. No flags with symbols, no clock markings. Opaque panoramic artwork.
```

# Image generation prompts

Generated with the built-in image_gen tool. Each tile received one seam-check retry; the saved PNG uses the final prompt. Images remain at generated dimensions for later resizing.

## z05-ground.png

### Final prompt

```text
Use case: illustration-story. Asset type: final in-game seamless ground texture for a pop-up papercraft storybook rhythm game. Generate one square 1:1 image. Primary request: a seamless tileable carpet of periwinkle blue paper suggesting calm lake water, scattered small lily pads, short slender reed clusters and tiny lavender and pale pink flowers. Match the colours, gentle illumination and handcrafted cut-paper style of the viewed z05-key.jpg reference: cornflower and periwinkle blue, lavender, dusty lilac, muted sage and mint foliage, restrained warm creamy highlights. Soft painted paper fibres, delicate layered paper edges and very shallow soft contact shadows, rich harmonious colours, tender moonlit mood, no photorealism. Composition: strictly orthographic directly overhead, flat texture field, medium-small motifs with an even distribution and equal density from edge to edge, no central arrangement or single focal object. Absolutely seamless periodic repeat in both axes: every clipped leaf, pad, reed, flower, painted ripple and paper grain at the left edge must continue at the right edge at the same height; top and bottom must continue identically at the same horizontal position. Uniform periwinkle base across all four edges, no edge darkening or lighting gradient. No people, human figures, faces, animals, boats, buildings, logos, letters, numbers, words, watermarks, UI, roads or paths. No perspective, horizon, vignette, border, frame or foreground.
Seam correction requirement: make the outermost 3 percent on all sides quiet uninterrupted periwinkle painted paper water, with no lily pads, reeds, flowers or conspicuous ripples intersecting any boundary. Keep the same water colour and paper grain scale on every boundary, without a visible border or abrupt cleared band. Scatter all small motifs evenly through the rest of the surface. The opposing edges must join without any chopped botanical shapes or tonal jump.
```

### Initial prompt (replaced after seam check)

```text
Use case: illustration-story. Asset type: final in-game seamless ground texture for a pop-up papercraft storybook rhythm game. Generate one square 1:1 image. Primary request: a seamless tileable carpet of periwinkle blue paper suggesting calm lake water, scattered small lily pads, short slender reed clusters and tiny lavender and pale pink flowers. Match the colours, gentle illumination and handcrafted cut-paper style of the viewed z05-key.jpg reference: cornflower and periwinkle blue, lavender, dusty lilac, muted sage and mint foliage, restrained warm creamy highlights. Soft painted paper fibres, delicate layered paper edges and very shallow soft contact shadows, rich harmonious colours, tender moonlit mood, no photorealism. Composition: strictly orthographic directly overhead, flat texture field, medium-small motifs with an even distribution and equal density from edge to edge, no central arrangement or single focal object. Absolutely seamless periodic repeat in both axes: every clipped leaf, pad, reed, flower, painted ripple and paper grain at the left edge must continue at the right edge at the same height; top and bottom must continue identically at the same horizontal position. Uniform periwinkle base across all four edges, no edge darkening or lighting gradient. No people, human figures, faces, animals, boats, buildings, logos, letters, numbers, words, watermarks, UI, roads or paths. No perspective, horizon, vignette, border, frame or foreground.
```

## z05-backdrop.png

### Final prompt

```text
Use case: illustration-story. Asset type: final in-game panoramic background horizon band for a pop-up papercraft storybook rhythm game. Generate one image in the widest landscape format available, ideally 4:1. Primary request: lavender-blue moonlit sky above a distant lake shore, with delicate layered papercraft pines, softly rolling distant hills and a subtle glowing golden crescent moon reflection in the far lake. Match the colours, soft lighting and handcrafted cut-paper style of the viewed z05-key.jpg reference: periwinkle and cornflower blue, violet-lavender sky, dusty lilac clouds, muted sage-blue pines, pale pink hill highlights and small warm cream-gold light accents. Soft painted paper texture, stacked cut-paper silhouettes, gentle diffuse illumination, rich harmonious colour, magical calm storybook mood, no photorealism. Composition: a very wide panoramic horizon strip; the upper two-thirds is open softly painted sky with sparse lavender clouds, a modest pale warm crescent moon and very few tiny light points; all distant hills, pines, shoreline and the narrow lake reflection band stay entirely in the bottom third. Everything feels far away. No foreground objects. Left and right edges must blend for horizontal wrapping: same sky and lake colours and matching low shoreline heights at both edges, avoid prominent objects at the edges. No people, human figures, faces, animals, boats, large near trees, architecture, logos, letters, numbers, words, watermarks, UI, roads or paths. No frame, border or vignette.
```

## z06-ground.png

### Final prompt

```text
Use case: illustration-story. Asset type: final in-game seamless ground texture for a pop-up papercraft storybook rhythm game. Generate one square 1:1 image. Primary request: blush-pink paper flower field carpet, dense small pink, coral, cream-blush and lilac paper flowers with mint and muted sage leaves. Match the colours, soft lighting and handcrafted cut-paper style of the viewed z06-key.jpg reference: warm blush, rose pink, soft coral and peach, pastel lavender, creamy pale petal highlights, mint-sage foliage and tiny subdued golden flower centres. Soft painted paper fibres, overlapping cut-paper petals and folded leaves, very shallow soft contact shadows, rich harmonious pastel colour, gentle warm dusk storybook mood, no photorealism. Composition: strictly orthographic directly overhead, flat ground texture, medium-small flower scale with varied blossom shapes, dense but clearly readable even coverage all the way to every edge, no single focal flower or central bouquet. Absolutely seamless periodic repeat in both axes: every clipped petal, flower, leaf, shadow and paper grain at the left edge must continue at the right edge at the same height; top and bottom must continue identically at the same horizontal position. Uniform blush base and uniform lighting across all four edges, no edge darkening. No people, human figures, faces, animals, phones, buildings, logos, letters, numbers, words, watermarks, UI, roads or paths. No perspective, horizon, vignette, border or frame.
Seam correction requirement: use much smaller botanical motifs, around twenty-five blossoms across the square, with dense evenly scattered flowers and leaves. Treat the image as a single repeat cell of an infinite wallpaper. Opposite boundaries must have identical blush colour and matching tiny botanical silhouettes at corresponding positions. Keep the outermost one percent on every side softly mottled blush paper with tiny indistinct petal flecks instead of large clipped flowers or leaves; continue the same blush paper between the dense flowers everywhere so this does not form a frame, band or border. Absolutely no conspicuous cut blossoms or tonal jumps along the repeat boundaries. Prioritize seamless repeat and consistent edge-to-edge density.
```

### Initial prompt (replaced after seam check)

```text
Use case: illustration-story. Asset type: final in-game seamless ground texture for a pop-up papercraft storybook rhythm game. Generate one square 1:1 image. Primary request: blush-pink paper flower field carpet, dense small pink, coral, cream-blush and lilac paper flowers with mint and muted sage leaves. Match the colours, soft lighting and handcrafted cut-paper style of the viewed z06-key.jpg reference: warm blush, rose pink, soft coral and peach, pastel lavender, creamy pale petal highlights, mint-sage foliage and tiny subdued golden flower centres. Soft painted paper fibres, overlapping cut-paper petals and folded leaves, very shallow soft contact shadows, rich harmonious pastel colour, gentle warm dusk storybook mood, no photorealism. Composition: strictly orthographic directly overhead, flat ground texture, medium-small flower scale with varied blossom shapes, dense but clearly readable even coverage all the way to every edge, no single focal flower or central bouquet. Absolutely seamless periodic repeat in both axes: every clipped petal, flower, leaf, shadow and paper grain at the left edge must continue at the right edge at the same height; top and bottom must continue identically at the same horizontal position. Uniform blush base and uniform lighting across all four edges, no edge darkening. No people, human figures, faces, animals, phones, buildings, logos, letters, numbers, words, watermarks, UI, roads or paths. No perspective, horizon, vignette, border or frame.
```

## z06-backdrop.png

### Final prompt

```text
Use case: illustration-story. Asset type: final in-game panoramic background horizon band for a pop-up papercraft storybook rhythm game. Generate one image in the widest landscape format available, ideally 4:1. Primary request: pastel lilac-to-peach dusk sky above rolling distant papercraft flower hills with a few tiny distant houses. Match the colours, soft lighting and handcrafted cut-paper style of the viewed z06-key.jpg reference: lilac and rose-pink upper sky, warm peach and pale gold near the horizon, blush and coral flowers, dusty lavender hill layers, mint-sage foliage, tiny warm cream houses with muted rose roofs. Soft painted paper texture, gentle layered cut-paper silhouettes, warm diffuse dusk illumination and delicate soft shadows, rich harmonious pastel colour, romantic storybook mood, no photorealism. Composition: very wide panoramic horizon strip; the upper two-thirds is spacious open sky with sparse soft peach and lilac paper clouds; all rolling flower hills and very small faraway houses stay entirely in the lower third, small flowers read as colour flecks on distant hills. Everything feels distant. No foreground objects, no close flowers or close trees. Left and right edges must blend for horizontal wrapping: matching sky colours and gentle hill elevations at both edges, no prominent structures at the edges. No people, human figures, faces, animals, phones, logos, letters, numbers, words, watermarks, UI, roads or paths. No frame, border or vignette.
```

# Asset generation prompts

Generated with the built-in image_gen tool, one call per asset. Reference renders inspected: ../refs/z07-key.jpg and ../refs/z08-key.jpg. Images copied unchanged from $CODEX_HOME/generated_images; exact target resizing is deferred.

## z07-ground.png

```text
Use case: stylized-concept. Create exactly one final in-game ground texture, square 1:1 composition, a fully seamless repeating tile. Zone 7: starry paper towers at night. Match the viewed z07-key.jpg design reference in palette, gentle golden lighting and soft painted pop-up papercraft storybook material, without reproducing its scene layout. Ground only: a dense deep violet and dusky indigo moss carpet built from small overlapping cut-paper flecks, scattered tiny softly glowing butter-yellow star-shaped flowers and delicate dusty-lavender sprigs, with muted sage accents. Rich harmonious violet, lilac and warm pale-gold colors, subtle paper grain and shallow soft layer shadows. Medium-small details at an even density across the entire square. Strict orthographic view straight down, perfectly flat surface; no perspective, no horizon, no vignette, no central focal object, no large individual objects. True toroidal seamless pattern: opposite edges must continue exactly, including all paper shapes and flowers cut by an edge, with matching color, density and illumination on all four borders. No edge border or framing. No people, human figures or faces; no animals; no logos, letters, numbers, words, watermark or UI. No road, path, trail, track or clearing. No buildings, towers, sky or landscape in this ground texture. Soft painted papercraft, never photorealistic. Output only the finished square texture.
```

## z07-backdrop.png

```text
Use case: stylized-concept. Create exactly one final in-game panoramic background texture for Zone 7, starry paper towers at night. Use the widest available landscape generation aspect, aiming at a 4:1 horizon band (target later 2048 by 512). Match the viewed z07-key.jpg design reference: dusky indigo and deep violet night, lavender and lilac paper, warm cream and softly glowing butter-gold lighting, muted sage pine silhouettes, rich harmonious colors. Soft painted pop-up papercraft storybook illustration, delicate cut-paper layers, matte paper grain, gentle lighting, no photorealism. Upper two thirds: open violet starry sky with small delicate golden and lilac star glints, subtle layered lavender cloud wisps. Lower third only: a faraway whimsical skyline of small spiral paper towers with lilac conical roofs and warm illuminated windows, alternating with distant pine silhouettes and softly layered lavender hills. Everything in the scenery is far away, softly atmospheric; no foreground objects. Keep the sky clear and dominant and the entire skyline confined to the bottom third. The left and right edges should blend for horizontal wrapping: same sky hue and illumination at both ends, same distant hill and pine height at the two edges, no large landmark touching either edge. No people, human figures, faces or animals. No logos, letters, numbers, words, watermark, signage or UI. Absolutely no road, path, trail, track or bridge, and no game lane. Output only the finished panoramic background.
```

## z08-ground.png

```text
Use case: stylized-concept. Create exactly one final in-game ground texture, square 1:1 composition, a fully seamless repeating tile. Zone 8: heart carnival at night climax. Match the viewed z08-key.jpg design reference in plum-violet night palette, rose-pink accents, tiny cyan highlights and gentle golden lighting, and soft painted pop-up papercraft storybook material, without reproducing its scene layout. Ground only: a dense deep plum and muted aubergine carpet of small overlapping cut-paper moss flecks, evenly scattered small glowing pink heart-shaped flowers with tiny paper leaves, little gold confetti dots and tiny cyan sparkles. Rich harmonious magenta, blush pink, warm gold and restrained turquoise accents against plum; subtle matte paper grain and shallow soft cut-layer shadows. Medium-small details at even density edge to edge; small heart flowers must read as botanical motifs, not symbols printed in a user interface. Strict orthographic straight-down view of a perfectly flat surface. True toroidal seamless pattern: every motif cut by one edge continues exactly on the opposite edge; matching colors, density and illumination on all four borders. No perspective, horizon, vignette, border, frame, central focal object, large individual object or clearing. No people, human figures, faces or animals. No logos, letters, numbers, words, watermarks or UI. Absolutely no road, path, trail or track. No buildings, carnival rides, sky or landscape in this ground texture. Soft painted papercraft, never photorealistic. Output only the finished square texture.
```

## z08-backdrop.png

```text
Use case: stylized-concept. Create exactly one final in-game panoramic background texture for Zone 8, heart carnival at night climax. Use the widest available landscape generation aspect, aiming at a 4:1 horizon band (target later 2048 by 512). Match the viewed z08-key.jpg design reference: deep plum-violet night sky, rose and blush pink paper, lavender silhouettes, small turquoise highlights and rich warm cream-gold illuminated trim. Soft painted pop-up papercraft storybook illustration with delicate layered cut-paper shapes, matte paper grain, gentle soft lighting and a celebratory magical mood, never photorealism. Upper two thirds: mostly open plum night sky with small stars and a few delicate gold, pink and cyan fireworks, including a softly glowing heart-shaped firework made from little light dots; keep the fireworks airy rather than filling the sky. Lower third only: a faraway miniature glowing carnival skyline with a delicate ferris wheel, striped pink-and-cream carousel roof silhouettes, small pavilion roofs, warm golden pinpoint lights, distant muted-sage pines and layered lavender hills. Carousel silhouettes are architectural only, no riders or figures. All skyline scenery must remain small and distant along the bottom third; no foreground objects. Left and right edges blend for horizontal wrapping: same plum sky hue and lighting at both ends, same low distant skyline and hill heights at both edges, no large landmark touching an edge. No people, human figures, faces or animals. No logos, letters, numbers, words, watermark, signage or UI. Absolutely no road, path, trail, track, bridge or game lane. Output only the finished panoramic background.
```

# Image generation prompts

Generated with the built-in image_gen tool. Reference renders were opened before generation. Tile prompts include the initial attempt and the single seam-check regeneration; the regeneration is the saved asset. Images are copied unchanged at generation size; exact resizing is deferred.

## z09-ground.png

### Initial attempt

```text
Use case: stylized-concept. Create exactly one final in-game ground texture for zone z09, quiet night forest, of a pop-up papercraft storybook rhythm game. Square 1:1 image, closest to 1024x1024.
Reference palette and mood: the viewed z09-key.jpg design key, with deep midnight blue and dark desaturated teal, sage paper foliage and tiny warm ivory-gold glows. Match its gentle soft lighting, painted paper fibers, layered cut-paper construction and rich harmonious storybook colour. Use the reference only for colour, material and mood; this is a flat texture, not a reconstruction of its scene.
Scene: a continuous dark teal moss carpet with evenly scattered tiny glowing cream mushrooms, small fern sprigs and sparse warm firefly dots. Medium-small details, all seen strictly from directly above. The mushrooms must be small top-view caps, ferns flattened paper silhouettes, subtle shallow cut-paper layering and soft ambient occlusion.
Production requirements: a truly seamless periodic tile on BOTH axes. Opposite edges must continue the same moss, fern fragments and any cut-off motifs in exactly corresponding positions and colours, with matching edge illumination. Uniform detail density across the entire square, including all edges and corners; no central composition, no empty margins, no border, no vignette, no gradient darkening toward edges. Orthographic top-down, no perspective, no horizon, no large focal object.
Hard exclusions: no people, no human figures, no faces, no characters or animals; no logos, letters, numbers, words, watermark or UI; absolutely no road, path, trail, walkway, track or clearing. No photorealism. Opaque full-bleed texture.
```

### Regeneration — saved asset

```text
Use case: stylized-concept. Create exactly one final in-game ground texture for zone z09, quiet night forest, of a pop-up papercraft storybook rhythm game. Square 1:1 image, closest to 1024x1024.
Reference palette and mood: the viewed z09-key.jpg design key, with deep midnight blue and dark desaturated teal, sage paper foliage and tiny warm ivory-gold glows. Match its gentle soft lighting, painted paper fibers, layered cut-paper construction and rich harmonious storybook colour. Use the reference only for colour, material and mood; this is a flat texture, not a reconstruction of its scene.
Scene: a continuous dark teal moss carpet with evenly scattered tiny glowing cream mushrooms, small fern sprigs and sparse warm firefly dots. Medium-small details, all seen strictly from directly above. The mushrooms must be small top-view caps, ferns flattened paper silhouettes, subtle shallow cut-paper layering and soft ambient occlusion.
Production requirements: a truly seamless periodic tile on BOTH axes. Opposite edges must continue the same moss, fern fragments and any cut-off motifs in exactly corresponding positions and colours, with matching edge illumination. Uniform detail density across the entire square, including all edges and corners; no central composition, no empty margins, no border, no vignette, no gradient darkening toward edges. Orthographic top-down, no perspective, no horizon, no large focal object.
Hard exclusions: no people, no human figures, no faces, no characters or animals; no logos, letters, numbers, words, watermark or UI; absolutely no road, path, trail, walkway, track or clearing. No photorealism. Opaque full-bleed texture.
Seam correction priority: generate a mathematically periodic repeating material swatch. Left and right border pixels must match, and top and bottom border pixels must match. Any mushroom, fern or moss clump crossing an edge must continue at precisely the same position on the opposite edge. Keep the outermost narrow rim predominantly the same dark teal moss microtexture, without bright mushrooms cut at a border; distribute tiny cream mushroom caps and sage fern sprigs evenly just within that rim. No visible frame or border. Ensure there are no discontinuous sliced leaves or glowing spots at any repeating seam.
```

## z09-backdrop.png

### Saved asset

```text
Use case: stylized-concept. Create exactly one final in-game backdrop texture for zone z09, quiet night forest, of a pop-up papercraft storybook rhythm game. Use the widest available landscape panoramic aspect ratio, ideally 4:1 for a target 2048x512 horizon band.
Reference: match the viewed z09-key.jpg design key's palette, mood and material: midnight navy and deep muted blue-teal, sage and blue-green pine paper, a few tiny warm ivory-gold lantern glows, gentle diffuse nocturnal lighting, painted paper fibers and delicately layered cut-paper storybook construction. Use its colour and style only, do not reproduce its road or foreground scene.
Composition: an expansive deep teal night sky occupying the upper TWO THIRDS or more of the image, with faint sparse tiny distant glowing points. Along ONLY the bottom third, a continuous distant dense pine forest silhouette made of overlapping small folded-paper evergreen shapes, with atmospheric softer blue-teal forest layers behind and a scattering of tiny warm lantern lights nestled far away inside the tree line. All scenery distant; no big trees or objects near camera, no foreground, no ground plane extending toward viewer. Soft painted cut-paper layers, rich harmonious colour, quiet magical restful mood.
Wrapping: left and right edges have the same sky colours, comparable forest heights and density and consistent illumination so the panorama blends when repeated horizontally. Keep the horizon low and level overall; no central focal object, no vignette, no framing.
Hard exclusions: NO people, human figures, faces, characters or animals; NO logos, letters, numbers, words, watermark or UI; absolutely NO road, path, trail, walkway, track, bridge or route. No photorealism. Opaque full-bleed single panoramic image.
```

## z10-ground.png

### Initial attempt

```text
Use case: stylized-concept. Create exactly one final in-game ground texture for zone z10, sunrise grand reunion finale, of a pop-up papercraft storybook rhythm game. Square 1:1 image, closest to 1024x1024.
Reference palette and mood: match the viewed z10-key.jpg design key's warm cream paper, soft blossom pinks, pale butter yellow and golden light, mint and sage foliage, with tiny touches of muted lavender. Gentle sunrise lighting, softly painted paper fibers and shallow layered cut-paper construction. Rich harmonious luminous storybook colours, cheerful tender finale feeling. Use the reference for material, colour and mood, not its scene composition.
Scene: a continuous warm cream paper ground carpet densely and evenly scattered with medium-small pink and pale yellow paper flowers and mint leaves. Small folded cut-paper petals, delicate paper grain, subtle shallow relief and soft contact shadows. All flowers seen directly from above, varied five-petal blossoms and little daisies, evenly distributed in an organic repeating pattern. Cream substrate visible between small floral clusters.
Production requirements: truly seamless periodic tile on BOTH axes, matching opposite edge colours, details and illumination. Motifs crossing an edge must continue at precisely the same position on the opposite edge. Even medium-small detail density from edge to edge, including corners. Orthographic straight top-down view, no perspective, no horizon, no central focal object, no border or empty frame, no vignette, no lighting gradient.
Hard exclusions: NO people, human figures, faces, characters or animals; NO logos, letters, numbers, words, watermark or UI; absolutely NO road, path, trail, walkway, track, route or clearing. No photorealism. Opaque full-bleed square material swatch.
```

### Regeneration — saved asset

```text
Use case: stylized-concept. Create exactly one final in-game ground texture for zone z10, sunrise grand reunion finale, of a pop-up papercraft storybook rhythm game. Square 1:1 image, closest to 1024x1024.
Reference palette and mood: match the viewed z10-key.jpg design key's warm cream paper, soft blossom pinks, pale butter yellow and golden light, mint and sage foliage, with tiny touches of muted lavender. Gentle sunrise lighting, softly painted paper fibers and shallow layered cut-paper construction. Rich harmonious luminous storybook colours, cheerful tender finale feeling. Use the reference for material, colour and mood, not its scene composition.
Scene: a continuous warm cream paper ground carpet densely and evenly scattered with medium-small pink and pale yellow paper flowers and mint leaves. Small folded cut-paper petals, delicate paper grain, subtle shallow relief and soft contact shadows. All flowers seen directly from above, varied five-petal blossoms and little daisies, evenly distributed in an organic repeating pattern. Cream substrate visible between small floral clusters.
Production requirements: truly seamless periodic tile on BOTH axes, matching opposite edge colours, details and illumination. Motifs crossing an edge must continue at precisely the same position on the opposite edge. Even medium-small detail density from edge to edge, including corners. Orthographic straight top-down view, no perspective, no horizon, no central focal object, no border or empty frame, no vignette, no lighting gradient.
Hard exclusions: NO people, human figures, faces, characters or animals; NO logos, letters, numbers, words, watermark or UI; absolutely NO road, path, trail, walkway, track, route or clearing. No photorealism. Opaque full-bleed square material swatch.
Seam correction priority: this must be a periodic game material, not a cropped floral illustration. Align the left/right edges and top/bottom edges exactly, so a cut petal or leaf resumes at exactly the corresponding position on the other edge. Use smaller blossoms and leaves, a dense even scatter, and predominantly warm cream paper microtexture in the outermost very narrow edge area with no large flower centers sliced by the borders. Keep density visually even without a border or frame. Lighting and cream background hue must be constant across opposite edges.
```

## z10-backdrop.png

### Saved asset

```text
Use case: stylized-concept. Create exactly one final in-game backdrop texture for zone z10, sunrise grand reunion finale, of a pop-up papercraft storybook rhythm game. Use the widest available landscape panoramic aspect ratio, ideally 4:1 for a target 2048x512 horizon band.
Reference palette and mood: match the viewed z10-key.jpg design key's luminous golden sunrise, warm cream book paper, blush pink blossoms, butter yellow and gold highlights, sage and mint foliage, pale lavender atmospheric hills and clear soft sky blue. Soft painted papercraft storybook art, layered cut-paper shapes with visible subtle paper fibers, gentle warm lighting and rich harmonious tender celebratory colour. Use its material, palette and feeling only; do not reproduce the game road, characters or foreground objects.
Composition: the upper TWO THIRDS or more is spacious open sunrise sky, a soft vertical gradient from sky blue above through pale peach and glowing warm yellow near the low horizon, with a few very delicate faraway cut-paper clouds. Scenery confined entirely to the lower THIRD: distant small overlapping rolling papercraft hills in pastel mint, sage, cream and pale lavender, tiny pink flowering copses and a very small distant cream-and-gold heart-shaped freestanding gate on one hill. A few tiny pastel pink and yellow balloons float low near those distant hills, their fine strings attached to the scenery; keep all balloons and the gate small and far away. No sun with a face, no anthropomorphic shapes. Soft sunrise glow spread across the whole horizon without a large central sun disc. No foreground objects or terrain projecting toward viewer.
Horizontal wrap: equal sky colours and lighting at left/right edges, distant hill contours at compatible heights, allowing edges to blend when repeated. Uniform sky illumination across width, no vignette or frame. All scene detail stays low in a continuous distant horizon strip.
Hard exclusions: NO people, human figures, faces, characters or animals; NO logos, letters, numbers, words, watermark or UI; absolutely NO road, path, trail, walkway, track, bridge or route, including through the gate. No photorealism. Opaque full-bleed single panoramic image.
```


