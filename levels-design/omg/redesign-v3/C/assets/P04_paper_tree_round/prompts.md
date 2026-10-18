# Image generation prompts

## 1. hero.png

Reference: `style-ref.jpg` (style only).

```text
Use case: stylized-concept.
Create a MODELING DESIGN SHEET hero render for one buildable low-poly game asset, Round Paper Tree, in the fan-made Dancing Line style level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE REFERENCE ONLY. Match its sculpted low-poly papercraft, flat-shaded pastel facets, softly bevelled paper edges, slight cardstock thickness, subtle fold lines and restrained gold-foil accents. Do not reproduce its environment.
Asset: ONE folded paper tree with one faceted ROUND crown and a simple wood-coloured trunk and root base. Use a single mint palette variant: crown mint #BDEBD8, trunk and roots wood #C99A6B. Green #6CCB5F, blush #FFC7DA and lavender are alternate production recolours, NOT additional trees, patches, or colour swatches in this image.
Geometry: total real size width 2 m, depth 2 m, height 3.5 m, exact W:D:H = 2:2:3.5. Crown is a clean roughly spherical closed triangulated low-poly volume, 2 m wide, 2 m deep, 2 m high, from height 1.5 m to 3.5 m, with broad readable triangular facets and a mildly flattened underside. Simple slim straight octagonal tapered trunk, approximately 0.30 m diameter, rises from the ground into the crown. Integrated compact root base consists of four simple tapered folded-paper root flares spreading to approximately 0.65 m, all wood coloured; no separate ground disc. A few very fine subdued gold-foil fold seams on the crown, not an overall wireframe. Preserve a round canopy silhouette. No branches protrude from the crown, no leaves attached as separate ornaments, no fruit or flowers.
Composition: square 1:1 image. Single whole asset alone, centred with generous margins, three-quarter view from slightly above. Show the entire crown, trunk and root base. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background.
Materials: matte thick paper/cardstock, flat-shaded planar facets, subtle physical fold seams, soft tiny bevels, no crumpled or noisy texture. Clean mesh construction suitable for a modeller, modest polygon count.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No extra assets, no scenery, no inset panels.
```

## 2. views.png

Reference: `hero.png` (exact asset design).

```text
Use case: stylized-concept.
Create a landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE for the exact Round Paper Tree in the provided hero.png reference image. The reference is the design authority: preserve the mint faceted round crown, its triangulation and thin gold-foil seams, wood-coloured slender polygonal trunk with its slight waist and folded seam, and four angular flared wood-coloured roots. Preserve the same colours, materials, facet structure and details. Do not add decorations or change the model.
The asset has exact real dimensions W:D:H = 2:2:3.5, width 2 m, depth 2 m, height 3.5 m. Its roughly spherical crown is 2 m wide, 2 m deep and 2 m high; crown bottom is at height 1.5 m. Keep these proportions exact.
Canvas and layout: landscape 3:2, preferably 1536 by 1024. Plain perfectly flat light grey #E6E6E6 background. Exactly THREE equal invisible vertical thirds. LEFT third contains only FRONT view, looking horizontally at the tree. MIDDLE third contains only RIGHT SIDE view, seen from the right, looking horizontally. RIGHT third contains only TOP view, camera looking straight down vertically.
These are TRUE ORTHOGRAPHIC projections, zero perspective, zero three-quarter angle, zero camera tilt for front and side. Use the SAME physical scale in all three views. At a 1536 by 1024 layout use 200 pixels per metre: front width 400 and height 700; right-side width 400 and height 700; top crown width 400 and depth 400. Centre each view horizontally in its own 512-pixel third, at x=256, 768 and 1280. Front and side stand on exactly the same invisible baseline, y=862, with the same top height, y=162. Top view is centred vertically in its third; it is a circle-like faceted crown footprint, with the smaller trunk and roots naturally occluded beneath it. Top-view width MUST equal front-view width, and top-view depth MUST equal side-view width. Generous clear margins, nothing touches or crosses another third. No visible dividers.
Render as a clean low-poly papercraft model turnaround: matte mint #BDEBD8 cardstock crown, wood #C99A6B trunk and root base, soft tiny bevels, slight paper thickness and fold lines, flat-shaded broad triangular facets with restrained gold-foil seam accents matching the hero. Neutral soft ambient lighting makes the planes readable; NO cast shadows anywhere on the background, NO floor, no horizon, no contact shadows or vignette.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Only the three exact projections of this same tree, no insets, swatches, extra parts or perspective illustrations.
```

## 3. parts.png

Reference: `hero.png` (exact asset design).

```text
Use case: stylized-concept.
Create a landscape 3:2 DETAIL CALLOUT MODELING PLATE of the exact Round Paper Tree in the provided hero.png reference image. This reference is the sole asset design authority. Separate its actual three components for a modeller, showing clean buildable low-poly meshes. Do not redesign any component.
Layout: ONE horizontal row with exactly THREE isolated parts, left to right in this exact order: faceted crown; trunk; root base. Each is centred in its own equal invisible vertical column, with generous margins and no overlaps. No full assembled tree, no extra panels, no repeated parts. The parts may be individually enlarged for clarity, with the crown fitting fully within the left column, the slender trunk clearly readable in the middle, and the complete four-root base fitting in the right column. Three-quarter views from slightly above, consistent orientation and lighting across the parts. All component silhouettes completely visible, no cropping.
LEFT: Only the exact mint roughly spherical faceted crown, as removed from the reference tree. Preserve the reference polygonal round silhouette, broad triangular facets, physical fold seams, tiny soft bevels and sparse fine gold-foil lines in the same positions. It is a closed buildable volume with a mildly flattened underside and a small hidden socket underneath for the trunk, not loose leaves or a hemispherical shell. Its actual model dimensions are 2 m wide by 2 m deep by 2 m high.
MIDDLE: Only the simple slim wood-coloured polygonal trunk removed from between the crown and root base. Preserve the octagonal tapered construction, slight waist, widening upper neck and visible horizontal folded seam from the hero. Show top cut face and complete lower end, clean mating surfaces, subtle cardstock thickness and fold seams. No canopy fragments, no roots attached. Do not turn it into a branch system.
RIGHT: Only the compact wood-coloured root base removed from the bottom of the trunk. Preserve its four angular folded tapered root flares, the four-pointed spread and central raised polygonal collar visible in the reference. Show the collar opening or clean seating face where the trunk joins. No trunk standing above it, no ground disc, soil, leaves, moss or additional roots.
Consistency: the assembled asset real size is W:D:H = 2:2:3.5, 2 m wide, 2 m deep, 3.5 m high. Crown mint #BDEBD8, trunk and root base wood #C99A6B, restrained gold-foil fold accents on the crown exactly as the hero. Matte paper, flat-shaded facets, slight physical paper thickness, subtle paper surface, soft tiny bevels. No green, blush or lavender variants in this plate.
Background: perfectly uniform flat light grey #E6E6E6. Neutral soft ambient studio illumination to reveal facets, NO cast shadows on background, NO floor, horizon, vignette or decorative environment.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. The written ordering and dimensions in this prompt are instructions only and must never appear as graphics.
```
