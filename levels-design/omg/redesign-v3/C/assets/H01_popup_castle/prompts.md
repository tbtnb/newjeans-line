# Exact image generation prompts

Built-in image_gen; one call per image, in spec.tsv row order. transparent_background: false for each call.

## hero.png

Reference image: ./style-ref.jpg

```text
Use case: stylized-concept.
Create ONE square 1:1 MODELING DESIGN SHEET hero image of the single asset H01_popup_castle, "Pop-up Castle", for the fan-made Dancing Line style rhythm level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte paper surfaces, slight paper thickness, visible fold lines, restrained gold-foil accents and pastel palette. Do not reproduce its environment.
Subject: one complete huge pop-up paper castle rising out of one open book spread. Central keep plus EXACTLY FIVE distinct towers with simple faceted cone roofs, heart-shaped pink paper flags on gold poles, one central arched gate with broad stairs, warm glowing inset window panels, visible folded pop-up mounting tabs and hinges at the base. Make the structure clean, coherent and buildable as real low-poly meshes: thick paper slabs, polygonal tower shafts, simple roof cones, bevelled trim, clear joints, no floating architecture. Central keep is a rectangular crenellated mass, not a sixth cone-roof tower. Arrange the five cone-roof towers as a tall central rear tower, two medium outer rear towers, and two shorter front towers framing the arched gate. Make all five roofs separately visible in this hero view. Open book has a central spine crease, a few thick cream page layers and a blush cover with thin gold edging. Keep all decoration attached to the asset.
Overall bounding dimensions including book and flags: width 16 m, depth 10 m, height 18 m. W:D:H = 16:10:18 exactly; tall silhouette, book width less than overall vertical height. Book footprint is 16 by 10. No extra base or scenery.
Colours: blush #FFC7DA, lavender #B9A6F0, cream #FFF3DE, gold #F7D98B, warm lamp #FFC968, vivid pink accents #FF6FAE. Lavender faceted cone roofs, cream and blush castle walls, warm inset windows and subtle gold trim.
Composition: the SINGLE complete asset alone, centred, three-quarter view from slightly above, visible front and right side, fully visible including flag tips and book corners with generous margins. Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background. Production modeling concept render, crisp readable silhouette and geometry, simple controlled detail, no atmospheric haze.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines or dimension lines anywhere. No people, no logos, no watermarks. No surrounding landscape, extra books, path, bunny, flowers, stars or moon.
```

## views.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the exact Pop-up Castle asset in the attached hero.png. The image is the definitive design reference; reproduce its castle, book, topology, five tower placements, colours, crenellations, flag shapes, gold details, heart banners, gate, staircase, inset warm windows and visible folded mounting tabs without redesigning.
Use the SAME single object in three true orthographic projections. No perspective, no isometric views, no camera tilt in front or side. EXACTLY THREE equal vertical thirds, with no visible dividers. LEFT third: FRONT view straight on to the arched gate. MIDDLE third: RIGHT SIDE view looking horizontally from the object's right, front of castle toward the left of this side projection. RIGHT third: TOP view straight down, front of book toward image bottom. No fourth view or inset.
All three views must have the SAME uniform pixels-per-metre scale. Overall bounding dimensions including book and flags: W:D:H = 16:10:18, width 16 m, depth 10 m, height 18 m. Thus front bounding width:height = 16:18; side width:height = 10:18; top width:depth = 16:10. Do not enlarge the narrower side view or the top view to fill its third. Front and side stand on exactly the same baseline with the same overall height. Top view width equals front view width; top view depth equals side view width. Each projection centred in its own equal third, generous outer margins, nothing crosses into another third. Use a scale where the front and top widths occupy about 84 percent of their column width, and the full front and side heights occupy about 71 percent of image height; vertically centre all views with front and side sharing a baseline.
Design lock: open cream book with visible page thickness, blush cover and gold edging, central spine crease; rectangular crenellated central keep plus exactly five lavender faceted cone-roof towers, one tallest rear centre, two medium outer rear towers and two shorter front towers; gold poles with pink heart-shaped paper flags. Central pointed arched warm gate, broad cream stair run, paired short blush stair posts with gold faceted finials, blush heart banners, warm glowing pointed window panels, cream and blush polygonal walls, thin gold trim, triangular folded paper mounting tabs at the base. Show only features actually visible in each projection, with natural orthographic occlusion. Do not add towers to reveal hidden ones. Top projection must show roof footprints, book footprint, actual relative positions and the stair run from straight overhead.
Style: sculpted low-poly papercraft, crisp flat-shaded facets with soft bevels, matte paper, slight sheet thickness and fold lines, simple buildable geometry. Palette blush #FFC7DA, lavender #B9A6F0, cream #FFF3DE, gold #F7D98B, warm lamp #FFC968, pink #FF6FAE. Neutral even studio illumination with restrained warm window emission.
Background is entirely uniform flat light grey #E6E6E6. NO floor, NO ground plane, NO cast shadows on background, NO horizon, NO gradient.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines or dimension lines anywhere. No people, logos, watermarks or scenery. Exactly three views in the specified left-to-right order.
```

## parts.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT MODELING PLATE for the exact Pop-up Castle asset in the attached hero.png. The reference locks the design, colours, materials and all construction details. Show exactly FOUR detached key parts separately in ONE horizontal row, LEFT TO RIGHT in the order below. Each part must be centred in its own equal-width column, with clear empty gutters and ample margins; nothing touches or crosses into a neighbouring column. No column lines. Parts may be individually enlarged for readability, but must remain the same component designs as the hero. All four parts fully visible, consistent three-quarter inspection views, neutral even studio illumination. Background entirely uniform flat light grey #E6E6E6, no floor, no cast shadows, no horizon, no gradient.
LEFTMOST column: one complete cone-roof tower with heart flag. Extract the shorter front tower design: cream/blush octagonal paper shaft, pointed gold-framed warm glowing window, blush crenellated collar with gold rim, lavender faceted cone roof with gold cap, gold flagpole and folded vivid-pink heart-shaped flag, simple thick polygonal base. Single intact tower, fully visible.
SECOND column: arched gate and stairs module. Extract the hero's central cream and blush pointed-arch facade with gold moulding, small pink-and-gold heart medallion above the arch, warm golden opening, broad cream staircase and the two blush stair posts with faceted gold finials. All assembled as one freestanding portal-and-stair module, no surrounding castle wall or towers.
THIRD column: one glowing window panel detail. A single elongated pointed-arch cream paper wall panel with visible sheet thickness and fold edge, gold bevelled inset frame and warm yellow-orange luminous insert. Slight exploded separation between the wall backing, gold frame and glowing insert so the modeller can understand construction. Components stay close together wholly inside this column; no arrows.
RIGHTMOST column: one pop-up fold tab hinge detail. Close-up of the same cream paper triangular mounting brace and folded rectangular foot tab visible at the tower bases in the hero. Show its physical construction, slight cardstock thickness, crisp scored crease lines, a short upright cream wall fragment attached to a flat cream book-page fragment by a folded triangular gusset. Gently separate one matching folded tab just beside the assembled hinge inside the same column to reveal the simple fold. Keep this a mechanical paper component with a clear buildable shape, no decorations or invented metal hinge.
Style and materials: sculpted low-poly papercraft, flat-shaded polygon facets with soft bevels, matte paper, slight paper thickness, sparse fold lines, restrained gold-foil trim. Palette blush #FFC7DA, lavender #B9A6F0, cream #FFF3DE, gold #F7D98B, lamp #FFC968, pink #FF6FAE. Clean buildable real low-poly mesh shapes, crisp silhouettes, no fine noisy texture.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines or dimension lines anywhere. No people, logos, watermarks or scenery. Do not show the complete castle or the complete book; show only the four requested component groups in the specified one-row order.
```

