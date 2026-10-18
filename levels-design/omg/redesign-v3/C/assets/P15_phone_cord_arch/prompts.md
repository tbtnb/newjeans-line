# Exact image generation prompts

## hero.png

Reference: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create a square 1:1 MODELING DESIGN SHEET hero image for a low-poly rhythm game asset, Phone-Cord Vine Arch, in the Bunny Pop-up Storybook world.
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper, visible paper thickness and crisp fold lines, pastel colours and restrained gold-foil accents. Do not reproduce its scene.
Subject: one freestanding open arch constructed from a thick pink curly telephone-cord vine. A continuous, clean, evenly spaced low-poly helical cord follows an inverted U arch, from the left foot over the rounded crown down to the right foot. The telephone-cord loops are visibly three-dimensional, with readable open gaps, faceted polygonal cross sections, and clean non-intersecting geometry. Overall OUTERMOST dimensions including decorations: width 4 m, depth 0.6 m, height 3.5 m, exactly W:D:H = 4:0.6:3.5. This is a shallow gateway with a large clear walk-through opening. Cord terminates neatly at two flat resting feet, with small cream paper collars and narrow gold-foil bands integrated into the cord ends; no added plinth or platform.
Decorations: five small coral folded heart-shaped paper flowers attached directly to the cord, one at the crown, one on each upper shoulder, and one halfway up each upright; small mint folded paper leaves paired near the hearts, kept sparse so the coiled telephone-cord construction remains clear. Flowers have a simple cream inset fold and tiny gold-foil attachment; leaves are simple thick diamond/teardrop meshes with a single center ridge. Palette: pink #FF6FAE, mint #BDEBD8, coral #FF7A6B, cream #FFF3DE, with tiny gold-foil accents. All decorations stay inside the stated overall bounds. Clean buildable real low-poly geometry, no floating ornaments, no fuzzy fibers, no thin tangled vines.
Composition: the SINGLE complete asset alone, centered, three-quarter view from slightly above, enough angle to read the shallow depth, generous clear margins around every extremity. Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background. The arch front silhouette is broader than it is tall.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No scenic set, book, castle, bunny, phone handset, cables off the asset, additional objects, inset panels or extra views.
```

## views.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create a landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for low-poly mesh modeling.
Input image: hero.png is the exact MODEL AND MATERIAL reference. Depict the SAME Phone-Cord Vine Arch, preserving its exact coil construction and turn count, silhouette, feet, five coral heart flowers, mint leaves, folds, cream end collars, gold-foil details and all attachment locations. Do not redesign or add ornaments. Match the reference's sculpted low-poly matte papercraft, flat-shaded facets, soft bevels and slight paper thickness.
Overall outermost model dimensions including decorations: W:D:H = 4:0.6:3.5. Front is 4 wide by 3.5 high. Right side is 0.6 wide by 3.5 high. Top is 4 wide by 0.6 deep. All views are true orthographic parallel projections with absolutely no perspective, no three-quarter angles and no isometric angles.
Layout: exactly three equal invisible vertical thirds across the canvas. LEFT third: FRONT view looking straight at the open arch. MIDDLE third: SIDE view seen strictly from the right, showing the genuine narrow 0.6-depth profile with natural overlapping/occlusion of the arch and decorations; do not rotate to expose the opening. RIGHT third: TOP view looking straight down, showing the genuine shallow footprint with natural occlusion; do not tilt to expose the arch opening. Same world-unit-to-pixel scale in all three views. Front and side stand on the same invisible baseline and have exactly the same height. Top view width equals front view width; top view depth equals side view width. Center each view horizontally within its own third, top view centered vertically; ample margin and nothing crosses between thirds. The narrow side and shallow top must stay narrow and shallow, not enlarged to fill the space.
Plain uniform flat light-grey #E6E6E6 background edge to edge. No floor, no horizon, no cast shadows anywhere on the background, no ambient shadow blobs. Only soft neutral surface lighting to make the facets legible. Colours exactly as hero: pink #FF6FAE, mint #BDEBD8, coral #FF7A6B, cream #FFF3DE, tiny gold foil.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos or watermarks anywhere. Exactly three views of the same model, no additional parts or extra objects.
```

## parts.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create a landscape 3:2 DETAIL CALLOUT PLATE for low-poly mesh modeling.
Input image: hero.png is the exact MODEL AND MATERIAL reference for the Phone-Cord Vine Arch. Extract and enlarge its actual component designs without redesigning them. Preserve the same pink faceted telephone-cord cross section and loop pitch, coral folded heart-flower construction with cream fold and tiny gold attachment, and mint folded leaf shape and center ridge. Match sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper, visible paper thickness and crisp fold lines. Overall assembled asset proportions remain W:D:H = 4:0.6:3.5; this sheet shows component close-ups, not another assembled arch.
Exactly ONE horizontal row of THREE isolated key parts, left to right in this precise order, each centered in its own equal invisible column: LEFT = one short extracted coiled cord segment showing three connected helical turns with clearly readable gaps and neat cut ends; MIDDLE = one isolated complete heart flower, coral folded heart-shaped paper with the reference's cream inset fold and tiny gold-foil attachment; RIGHT = one isolated mint leaf with the reference's thick low-poly teardrop/diamond outline and single center fold ridge. Three-quarter close-up views reveal thickness, bevels, folds and how each component can be built as real geometry. Keep the three parts separate and centered on the same row, with generous margins and nothing crossing into another column. Each component must be readily readable at close-up scale. No assembled arch, no duplicate parts, no additional views, no scenery.
Background: uniform flat light grey #E6E6E6 edge to edge. No floor, horizon or cast shadows on the background. Soft neutral surface lighting only. Palette matches hero exactly: pink #FF6FAE, mint #BDEBD8, coral #FF7A6B, cream #FFF3DE, restrained gold foil.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos or watermarks anywhere.
```

