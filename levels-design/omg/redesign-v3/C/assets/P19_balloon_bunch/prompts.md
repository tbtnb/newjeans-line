# Exact image generation prompts

Generated with the built-in image_gen tool, one call per row in spec.tsv.

## hero.png

Reference image: ./style-ref.jpg

```text
Use case: stylized-concept
Create exactly ONE square 1:1 modeling design sheet image for a low-poly mesh artist building the asset Balloon Bunch for the fan-made Dancing Line style rhythm game level Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is the approved WORLD STYLE reference only. Match its sculpted low-poly papercraft, clean flat-shaded polygon facets, softened narrow bevels, matte pastel paper, slight paper thickness, restrained fold seams and gold-foil accents. Do not reproduce the environment.
Subject: a single complete bunch of THREE faceted paper balloons, tied by three separate slender gold paper cords to one small faceted gold paper weight. The three balloon shapes are a magenta heart on the upper left, a cyan bunny-head on the upper right with two upright polygonal ears and no face, and a pink round balloon slightly lower between and behind them. Each balloon is a closed inflated low-poly volume with a tiny folded paper neck at its bottom. The round balloon is a true faceted sphere, the heart has real convex thickness, and the bunny-head is a rounded faceted volume with solid thick tapered ears. The gold cords are clean thin buildable polygonal strips, gently angled from the balloon necks to one common tie point on the weight. No loose curly ribbons. The small weight is a squat bevelled low-poly gold polyhedron with a simple raised folded paper tie at its top.
Exact full assembled bounding proportions W:D:H = 1.2:1.2:3.5, real size 1.2 m wide by 1.2 m deep by 3.5 m tall, measured from bottom of weight to tallest bunny ear. Arrange the balloon cluster in depth as well as width so its depth bound equals its width bound. Long open cords occupy the middle of the tall silhouette, balloons at the top and small weight at the bottom.
Palette atlas: magenta #FF4FA0 for the heart; cyan #7FE0E8 for the bunny; pink #FF6FAE for the round balloon; gold #F7D98B for the cords, weight and very restrained seam accents. Facet shading may vary these colors naturally.
Composition: single asset alone, three-quarter view from slightly above, fully visible including ears and weight, centered with generous clear margins. Plain soft pale-cream gradient background, soft studio lighting, gentle contact shadow under the weight only.
Make the forms clean, simple and buildable as real low-poly geometry, with readable polygon topology and restrained folds. No floating sparkles or scenery.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere in the image.
```

## views.png

Reference image: ./hero.png

```text
Use case: stylized-concept
Create exactly ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW modeling design plate for the Balloon Bunch asset.
Input image: hero.png is the definitive ASSET DESIGN reference. Reproduce the identical three balloons, faceted topology, proportions of the parts, materials, colors, neck collars, gold seams, three straight gold cords and small gold weight. Do not invent a variant. The reference shows a magenta faceted heart at left, cyan faceted bunny-head at right with two tall ears and pale cream inner-ear panels edged by thin gold foil, a pink faceted round balloon lower and behind the other two, small flared matching balloon necks with gold collars, and a small squat gold faceted pouch-shaped weight with a cinched polygonal neck. No face. Match its matte papercraft texture, flat triangular facets, soft narrow bevels and restrained gold foil. Palette: magenta #FF4FA0, cyan #7FE0E8, gold #F7D98B, pink #FF6FAE.
The exact assembled real-world bounds are W:D:H = 1.2:1.2:3.5. Maintain these dimensions in the orthographic projections, including the long cords. Prioritize accurate 1.2-wide by 3.5-tall front and 1.2-deep by 3.5-tall side silhouettes. Preserve the reference's balloon shapes while spacing in depth to give the full bunch equal width and depth.
Layout: exactly three invisible equal vertical thirds, no panel borders. LEFT third: FRONT view, camera horizontal along the front axis, no yaw or pitch. MIDDLE third: RIGHT SIDE view, camera horizontal exactly 90 degrees around the same model. RIGHT third: TOP view, camera straight down exactly 90 degrees, showing actual depth arrangement and natural occlusion. These are projections of one unchanged assembled model, not three rearrangements and not three-quarter views.
Use the SAME orthographic scale in all three views. A helpful layout target on a 1536 by 1024 canvas is 240 pixels per metre: the front and side each occupy 288 pixels width and 840 pixels height, centered horizontally at x=256 and x=768, with the same base at y=932 and highest point at y=92; the top occupies 288 by 288 pixels centered at x=1280, y=512. Treat these coordinates as layout instructions only; do not draw measurements. The top view must be much shorter on the page than the front and side because true depth is 1.2 m and height is 3.5 m. Front and side same height, shared baseline; top width exactly equals front width, top depth exactly equals side width. Nothing crosses thirds, each has clear margins.
Background: uniform flat light grey #E6E6E6 throughout, no gradient, no floor, no horizon, NO cast shadows on background. Neutral even lighting may softly describe facets on the objects only.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Only the three specified orthographic projections.
```

## parts.png

Reference image: ./hero.png

```text
Use case: stylized-concept
Create exactly ONE landscape 3:2 DETAIL CALLOUT modeling design plate for the Balloon Bunch asset.
Input image: hero.png is the definitive ASSET DESIGN reference. Show the listed key parts separately in one horizontal row, left to right in this exact order: heart balloon; bunny balloon; weight. Exactly three parts, each centered in its own invisible equal-width column with generous margins. Nothing crosses column boundaries. Use close three-quarter views from slightly above, consistent across the parts, showing enough thickness for a low-poly mesh artist to build each shape. The parts may be enlarged individually for clear construction detail; preserve each part's actual shape and proportions from the reference.
LEFT column: the identical magenta faceted inflated paper heart from hero.png, with the same two rounded angular lobes, central cleft, pointed bottom, flat triangular polygon surfaces, thin gold seam accents and small gold collar above its flared magenta folded-paper neck. Show the complete isolated heart and neck. Omit its long cord.
MIDDLE column: the identical cyan bunny-head balloon from hero.png: rounded faceted closed volume, two tall thick tapered polygonal ears, the same pale cream inner-ear panels and thin gold inner-ear edges, no face, same collar and small cyan flared folded-paper neck. Show complete ears, head and neck. Preserve the ear asymmetry, polygon facets and exact design in the reference. Omit its long cord.
RIGHT column: the identical small gold faceted paper weight from hero.png, enlarged to show its construction: squat polygonal pouch-like body with a flat stable bottom, broad angular shoulders, cinched narrow upper neck and raised low-poly rim where the cords attach. Show that same closed geometry, paper folds, matte gold panels and slight foil highlights. No redesigned box or substitute weight. Omit the long cords.
Style: sculpted low-poly papercraft, clean buildable solid meshes, flat-shaded facets, softened narrow bevels, matte paper with slight paper thickness and restrained fold lines; match hero.png faithfully. Palette atlas: magenta #FF4FA0, cyan #7FE0E8, gold #F7D98B, pink #FF6FAE; cream inner-ear inserts exactly as in hero.png. The complete parent asset's proportions are W:D:H = 1.2:1.2:3.5; this sheet isolates its component parts.
Background: uniform flat light grey #E6E6E6, no gradient, no floor, no horizon, no cast shadows on the background. Soft neutral object shading only.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No round balloon, no assembled bunch, no duplicate parts, no scenery; only the three specified isolated parts in one row.
```

