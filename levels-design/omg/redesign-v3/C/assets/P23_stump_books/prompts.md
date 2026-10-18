# Exact image generation prompts

## hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create ONE square 1:1 modeling design sheet image for the single game asset P23_stump_books, "Stump with Books", for the fan-made Dancing Line style rhythm level Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft world: clean flat-shaded planar facets, softly beveled edges, matte paper surfaces, slight visible card thickness and intentional fold seams, restrained gold-foil accents. Do not reproduce its scene.
Subject: one squat paper tree stump supporting a small stack of three closed books with entirely blank covers and a tiny candle. The complete assembled object has real bounding dimensions width 1.2 m, depth 1.2 m, height 1.0 m, exactly W:D:H = 1.2:1.2:1 including books and candle flame. The stump has a broad simple polygonal root flare, a faceted tapered trunk, large clean bark folds and a flat cut top with a few broad polygonal concentric growth rings. Buildable low-poly geometry, no fine sculpted noise. Stump and roots occupy the full 1.2 m by 1.2 m footprint. The stump top is about 0.70 m above the base. A compact stack of three rectangular closed books occupies the left half of the stump top, with flat cream page blocks, teal and cream blank covers, tiny gold-foil corner accents, modest cover thickness and simple beveled spines. Place a single tiny cream pillar candle in a simple low polygon gold holder on the right half of the stump top, with one small solid low-poly warm golden flame. Keep every element supported and separate, no floating parts. Overall highest point is 1.0 m. Books are clearly smaller than stump. No other props or decorations.
Palette atlas: wood #C99A6B; deep teal #173A4A; warm cream #FFF3DE; candlelight/flame #FFC968; restrained gold foil. Use softer facet variations within these colors.
Composition: single complete assembled asset alone, three-quarter view from slightly above, front and right side visible, centered with generous margins, no cropping. Plain soft pale-cream gradient background. Soft studio light, gentle contact shadow. Modeling clarity takes priority over dramatic atmosphere. No environment, pedestal, scenery, glow clouds or effects.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, signatures or watermarks anywhere, including book covers and spines. Exactly one image.
```

## views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the exact assembled stump-with-books asset in the input reference hero.png.
Input image: hero.png is the authoritative DESIGN reference. Preserve the identical silhouette, low-poly facets, root count and shape, stump cut-top polygonal rings, three closed books, candle and holder, materials, colors and every gold detail. Do not redesign, embellish, or add props.
The complete assembled model bounding dimensions are width 1.2 m, depth 1.2 m, height 1.0 m: exactly W:D:H = 1.2:1.2:1. The width and depth of its root footprint are equal. Preserve the broad faceted wood stump and root flare, book stack on its left half, tiny candle on its right half. Books bottom to top: teal, cream, teal; all blank, with cream page blocks, gold corner details and spine bands. Candle is a cream low polygon pillar in an octagonal gold holder with a small faceted golden flame. Wood #C99A6B, teal #173A4A, cream #FFF3DE, candlelight #FFC968, gold-foil accents.
PLATE LAYOUT: exactly three equal invisible vertical thirds, with generous clean margins. LEFT third: FRONT elevation, camera horizontally level, looking straight at the book spines, absolutely no view down onto the stump or the books. MIDDLE third: RIGHT SIDE elevation, camera horizontally level, exactly 90 degrees clockwise around the model, no view down onto the stump or books. RIGHT third: TOP plan, camera looking vertically straight down, exactly perpendicular to the ground. These are three true orthographic projections of ONE identical model, with parallel lines and NO perspective or three-quarter tilt.
Use the SAME uniform drawing scale in all three thirds. Front and right-side views stand on the exact same horizontal baseline and have the exact same total height. Top-view footprint width equals front-view footprint width; top-view footprint depth equals right-side footprint width. Since W = D = 1.2 and H = 1.0, front and side full bounding boxes are 1.2 times as wide as tall, and the top bounding box is square. Center each projection within its own third; no element crosses between thirds; all parts fully visible within their view.
Background: uniform flat light gray #E6E6E6 everywhere, no gradient, no floor, no horizon, no cast shadows on background. Soft neutral ambient material shading only, preserving clean flat-shaded paper facets, bevels and visible card thickness. Technical modeling clarity, no drama.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, dividers, borders, people, logos, signatures or watermarks anywhere. Exactly three views, no insets, no extra objects.
```

## parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT MODELING PLATE showing the exact component designs from input reference hero.png, separated into ONE horizontal row.
Input image: hero.png is the authoritative DESIGN reference. Match its exact geometry, faceted silhouettes, materials, colors, book cover arrangement, gold details and candle design. This is a component breakdown of that existing model, not a redesign.
Layout: exactly THREE equal invisible vertical columns. Left to right, exactly this order:
LEFT column: the stump alone, completely removed from the books and candle, showing the full broad polygonal root flare, faceted tapered paper-wood trunk, top bevel and broad polygonal concentric growth rings. Entire stump visible.
MIDDLE column: the three closed books together as one small stack, separated from the stump and candle. Bottom teal book, middle cream book, top teal book. Preserve the reference cover thickness, clean cream page blocks, blank spines, gold spine bands and gold corner caps. Three-quarter close-up so covers, spines, page edges and paper thickness are easy for a modeler to read.
RIGHT column: the tiny candle alone together with its octagonal gold holder and single solid golden faceted flame, separated from the stump and books. Close-up of the cream faceted pillar, simple holder walls, top surface, short dark wick and polygonal flame. Preserve exact reference design; no extra melted wax, no extra ornament.
Each component group is centered in its own equal column with generous margin, and nothing crosses between columns. One row only, with the visual centers aligned horizontally. Independently enlarge the book stack and candle to make their geometry readable as detail callouts, while preserving each component's internal proportions. Stump stays the largest visual group. All three shown in consistent three-quarter views from slightly above, same camera orientation as hero.png. Clean, fully visible, no cropping. No duplicate component or extra assembled asset.
Full assembled reference dimensions are W:D:H = 1.2:1.2:1, with stump root footprint 1.2 m by 1.2 m and total assembled height 1.0 m; retain the same component proportions and construction when separated.
Style: sculpted low-poly papercraft, flat-shaded planar facets, soft bevels, matte paper with slight paper thickness and fold seams, restrained gold-foil accents, clean buildable low-poly mesh geometry. Wood #C99A6B, teal #173A4A, cream #FFF3DE, flame #FFC968, gold foil.
Background: uniform flat light gray #E6E6E6, no gradient, no floor, no horizon, no cast shadows on the background. Soft neutral studio material shading to reveal the facets.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, dividers, borders, people, logos, signatures or watermarks anywhere, including every book cover and spine. Exactly three separated component groups in one row, no insets.
```

