# Exact image generation prompts

Generated with the built-in image_gen tool, one call per image, in spec.tsv row order.

## hero.png

Reference: ./style-ref.jpg (style reference)

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero image for a low-poly game asset, Sitting Bunny Statue, for the pastel pop-up storybook world in the supplied style reference. The reference image is STYLE ONLY: borrow its sculpted faceted papercraft, soft beveled edges, matte paper, visible paper thickness and restrained fold lines, pastel palette and delicate gold-foil accents. Do not copy its scene or include a book, heart prop, castle, stars, plants or other scenery.
Show a single complete sitting bunny statue alone on its round grass base, three-quarter view from slightly above. Clean, buildable real low-poly geometry: large planar facets on the pearl head and pear-shaped seated body, two long upright folded polygonal ears with recessed blush inner-ear panels, two small front paws resting against the belly, two broad seated hind feet, and a small mint folded-paper bow under the chin. Calm simple blank faceted face, like the bunny in the style reference. A low circular green grass plinth has a simple faceted bevel and an extremely fine gold-foil rim, with no individual grass blades. All pieces are solid and geometrically coherent; no floating ornaments or painted fake geometry.
Exact overall bounding-box proportions including base and ears: width:depth:height = 1.6:1.4:2.4. The widest span is the hind feet, 1.6; the circular base diameter and overall depth are 1.4; total height is 2.4. Preserve this tall compact seated silhouette. Palette: pearl #F3F1EA, blush #FFC7DA, mint #BDEBD8, green #6CCB5F, plus only the fine gold-foil rim. Flat-shaded polygon facets, soft bevels, paper rather than plush or glossy plastic.
Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background. Entire asset centered with generous clear margins, ears and base fully visible, no cropping. This is a clean modeller's build reference, not an environment illustration.
Hard constraints: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

## views.png

Reference: ./hero.png (design reference)

```text
Use case: stylized-concept.
Create one landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a modeller, using the supplied hero.png as the exact design reference for the SAME Sitting Bunny Statue. Preserve its exact faceted pearl head and seated body, blank face, two tall splayed folded ears with blush recessed inner panels, mint collar and small faceted bow with central knot and two tails under the chin, two little front paws, broad seated hind feet with blush sole panels, low circular faceted green grass base, and extremely fine gold-foil base rim. Preserve silhouette, ear angles, part placement, colours and facet construction; do not redesign or add details. Sculpted low-poly papercraft, flat-shaded planar facets with soft bevels, matte paper thickness and restrained fold lines. Palette pearl #F3F1EA, blush #FFC7DA, mint #BDEBD8, green #6CCB5F and the reference's thin gold rim.
Layout: EXACTLY three equal invisible vertical thirds, with exactly one view centered in each. LEFT third: true orthographic FRONT view, looking straight at the bunny face and bow. MIDDLE third: true orthographic SIDE view seen from the bunny's RIGHT, looking horizontally at its right profile, nose direction toward the left of the sheet. RIGHT third: true orthographic TOP view, looking vertically straight down, bunny's front toward the bottom of the sheet. These are three projections of a single identical 3D model, with no perspective, no isometric view, no three-quarter view, no elevated front or side camera. Use exactly the SAME world-unit-to-pixel scale in all three views. Front and side stand on exactly the same baseline and have exactly the same overall height. Top-view total width equals front-view total width; top-view total depth equals side-view total width. Stated overall W:D:H = 1.6:1.4:2.4; the top footprint width:depth is 1.6:1.4. Keep all projected geometry within each view's own third, with clear margins and no overlaps or cropping. Vertical centering is appropriate for the top projection; do not stretch it to match the height of the front view.
Flat uniform light grey #E6E6E6 background edge to edge, no floor, no horizon, no contact or cast shadows on the background, no ambient ground shadow. Soft neutral studio illumination only to reveal the mesh facets, no dramatic gradients. This is a precise, clean, buildable modelling turnaround.
Hard constraints: absolutely NO text, letters, numbers, labels, arrows, grid lines, dividers, border lines, dimension lines, people, logos or watermarks anywhere. Only the three projected views of the complete bunny statue and base.
```

## parts.png

Reference: ./hero.png (design reference)

```text
Use case: stylized-concept.
Create one landscape 3:2 DETAIL CALLOUT PLATE for a low-poly modeller. Use the supplied hero.png as the exact design and material reference for the Sitting Bunny Statue. Show ONLY its following three detached component groups, separately, in ONE horizontal row, left to right in this exact order, each centered within its own equal invisible column with generous margin and no overlaps:
LEFT column: the pair of folded ears, detached together as one component group, preserving their exact tall tapered polygon silhouettes, splayed angles, pearl folded outer shells, recessed blush inner-ear panels, flat facets, narrow rims and visible paper thickness from the hero. Show the complete ears from their tips to their attachment roots, in a clear close-up three-quarter front view that reveals their construction. No head.
MIDDLE column: the mint bow detached, preserving the exact hero's two angular faceted loops, small central polygon knot, two folded hanging ribbon tails and narrow neck-band attachment. Show one complete bow assembly in a clear close-up near-front three-quarter view with all folds and thickness readable. No body.
RIGHT column: the round green grass base detached and empty, preserving the exact hero's low circular polygonal plinth, faceted green top, bevelled polygonal green sidewall and very thin continuous gold-foil rim. Show the complete base from slightly above at three-quarter view so its top and thickness are clear. No bunny, no feet, no grass blades and no added ornaments.
This is one orderly row of three large isolated detail groups, no assembled bunny elsewhere, no extra inset views. Components may be enlarged individually for clear modelling details; preserve their internal shape and exact design. Equal column centers are at one-sixth, one-half and five-sixths of the image width. Keep each component group wholly in its own third and visually center all three groups around the horizontal middle of the sheet.
Style: sculpted low-poly papercraft, real buildable solid geometry, flat-shaded planar polygon facets with soft bevels, matte paper with slight paper thickness and restrained crease lines. Match the hero's exact colours: pearl #F3F1EA, blush #FFC7DA, mint #BDEBD8, green #6CCB5F, and the fine gold-foil base rim. The parent asset has W:D:H = 1.6:1.4:2.4; preserve the reference component designs.
Background: completely flat uniform light grey #E6E6E6 edge to edge, no floor, no horizon, no background gradient, no cast or contact shadows on the background. Soft neutral illumination on the component surfaces to reveal facets.
Hard constraints: absolutely NO text, letters, numbers, labels, arrows, grid lines, dividing lines, borders, dimension lines, people, logos or watermarks anywhere.
```

