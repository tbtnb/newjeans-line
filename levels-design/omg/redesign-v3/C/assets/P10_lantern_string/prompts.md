# Exact image generation prompts

Built-in image_gen; one call per image, in spec.tsv row order.

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create exactly ONE square 1:1 MODELING DESIGN SHEET hero image for the single asset Paper Lantern String, for the fan-made rhythm game level Bunny Pop-up Storybook.
Reference image: style-ref.jpg is STYLE ONLY. Match its sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte pastel paper, visible slight paper thickness and restrained fold lines, and warm gold-foil accents. Do not reproduce the environment.
Subject: one complete freestanding string of glowing paper lanterns suspended between two slim poles. Exact overall real dimensions including bases: width 6 m, depth 0.5 m, height 2 m; W:D:H = 6:0.5:2. It is a long, low, shallow asset, three times wider than tall, twelve times wider than deep. Both poles are straight and vertical, equally tall, with small simple shallow beveled square footplates and little gold caps. Matte lavender poles, gold foil collars and cord. A single thin gold cord with a shallow polygonal sag connects their tops.
Design for repeatable simple low-poly modeling: exactly seven lanterns, ordered left to right: lavender round, pink heart, gold five-point star, lavender round, gold five-point star, pink heart, lavender round. Each hangs from a short straight gold drop and tiny gold cap. All are real volumetric folded-paper shells, not flat icons: round lanterns use a few broad vertical facets, hearts have two lobes and a clear lower point with beveled faceted volume, stars have five clean points and shallow faceted front/back pyramidal volume. Lantern bodies approximately 0.40 m high; modest internal warm light, readable paper surfaces, no oversized bloom. Keep the arrangement and construction simple and clean with no extra ornaments.
Palette: pink #FF6FAE, gold #F7D98B, lavender #B9A6F0, warm lamp #FFC968.
Composition: single entire asset alone in three-quarter view from slightly above, mainly facing its long front so both poles and all seven lanterns are visible; show actual shallow depth. Center it on a plain soft pale-cream gradient background with generous margins. Soft studio light, gentle contact shadow. Clean high quality 3D papercraft model render intended for a modeller to build real low-poly geometry.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, extra props, sparkles, or decorative background.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the Paper Lantern String in the attached hero.png. The image is a technical turnaround for a low-poly modeller.
Input image: hero.png is the authoritative design reference. Preserve the identical two lavender poles, faceted gold pointed caps, gold collars, beveled lavender-and-gold square feet, thin sagging gold cord, short gold hanging stems and caps, and exactly seven lanterns. Left-to-right front order must remain lavender round, pink heart, gold five-point star, lavender round, gold five-point star, pink heart, lavender round. Preserve shell facets, fold lines, thickness, pastel paper and gold foil, and subtle warm lamp centers. No redesign.
Exact model bounding dimensions: W:D:H = 6:0.5:2, including feet and pole caps. True orthographic projection, zero perspective and zero camera tilt.
Layout: exactly three equal invisible vertical thirds. LEFT THIRD: FRONT view, looking straight at the broad face; full 6 m width horizontal and full 2 m height vertical, both poles and all seven lanterns seen straight on. MIDDLE THIRD: RIGHT SIDE view, looking along the full 6 m span from the right end; only 0.5 m depth horizontal and 2 m height vertical. The two poles and lanterns align and occlude one another naturally in this end-on projection; do not rotate it to reveal the front. RIGHT THIRD: TOP view, looking straight down; full 6 m width horizontal and 0.5 m depth vertical. Show the narrow upper edges and tops of lantern shells, cord and square feet in their correct positions, never a front silhouette.
Use one identical world-to-image scale for all three views. Consequently front is 3 times wider than tall, right-side is one quarter as wide as tall, top is 12 times wider than deep. Front and side share exactly the same height and baseline. Top width exactly equals front width, top depth exactly equals side width. An example proportional layout on a 1536 by 1024 canvas: front footprint 420 by 140 pixels, side footprint 35 by 140 pixels, top footprint 420 by 35 pixels. Center each view in its own equal third; front and side centered vertically on the same baseline; top centered vertically in its third. Generous blank margins are intentional; do not enlarge the narrow side view to fill its column. Nothing crosses between thirds. No inset, no fourth view, no divider.
Background: uniform flat light grey #E6E6E6, no floor, no horizon, absolutely no cast shadows on background, no ambient contact shadows. Neutral studio shading only on the geometry to explain its faceted surfaces; restrained warm internal lamp shading with no bloom spilling onto background.
Style: clean sculpted low-poly papercraft with flat-shaded facets, small soft bevels, matte paper, slight paper thickness and fold lines, gold foil accents. Palette pink #FF6FAE, gold #F7D98B, lavender #B9A6F0, lamp #FFC968.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, extra objects, decorative sparkles.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly ONE landscape 3:2 DETAIL CALLOUT MODELING PLATE using the attached hero.png as the authoritative design reference. Show exactly three separate key parts in ONE horizontal row, each centered in its own equal invisible column, fully contained with generous margins. LEFT column: the pink HEART LANTERN. MIDDLE column: the gold STAR LANTERN. RIGHT column: one complete lavender POLE. This is the strict left-to-right order. No other parts or lantern shapes.
Maintain identical geometry, colors, facets, material details, and fittings to hero.png. Use clear slightly elevated three-quarter detail views for all three parts. Individual detail enlargements are allowed so each part is readable within its column; do not force the lanterns to the same real-world scale as the full pole.
Heart: the exact volumetric pink paper heart with two lobes, center notch and tapered lower point; broad flat-shaded polygon facets, small edge bevels and folded-paper shell thickness; gold cap and short gold suspension stem with tiny round connector at top. Restrained warm amber internal glow. No extra decoration.
Star: the exact volumetric gold five-point star paper lantern with clean five-point silhouette, ridged radial triangular facets converging at the central peak, shallow back volume and paper-thickness edges; matching gold top cap and short suspension stem with tiny round connector. Restrained warm center. No extra decoration.
Pole: one complete straight slim faceted lavender pole, exact pointed faceted gold finial and cylindrical upper gold collar, lower gold collar and flared gold socket, shallow beveled square lavender footplate with gold rim, as seen in hero.png. Keep the pole tall and slim with the full base and cap visible. The source asset has overall W:D:H = 6:0.5:2 m, so this pole represents the 2 m height and its footplate the 0.5 m depth.
Show each as a separate isolated component, no connecting cord spanning the columns, no complete assembled string. Keep all three components in a single row with their centers balanced around the same horizontal midline.
Style: clean buildable real low-poly sculpted papercraft geometry, matte paper with slight thickness and fold lines, flat-shaded facets with soft bevels, restrained gold-foil accents, matching approved hero. Palette pink #FF6FAE, gold #F7D98B, lavender #B9A6F0, lamp #FFC968.
Background: perfectly uniform flat light grey #E6E6E6, no floor, no horizon, no cast shadows, no contact shadows or background gradient. Soft neutral lighting on the components only.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, sparkles, extra props, or fourth component.
```

