# Exact image generation prompts

Built-in image_gen; one call per image, in spec.tsv row order.

## hero.png

Reference: ./style-ref.jpg (world style).

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image for a modeller building a real low-poly mesh for the fan-made Dancing Line style rhythm-game level Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is the approved WORLD STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded planar facets, softly bevelled edges, pastel colours, matte paper, visible slight paper thickness and restrained fold lines, with gold-foil accents. Do not reproduce its scenery.
Subject: one Paper Gift Box asset, alone, with a ribbon and bow and its separate lid slightly open. Choose one coherent colourway: lavender #B9A6F0 box and lid, pink #FF6FAE broad paper ribbon and bow, gold #F7D98B narrow foil trim. No additional colour-variant boxes.
Geometry and proportions: overall assembled bounding envelope is exactly width 0.8 m, depth 0.8 m, height 0.8 m, W:D:H = 1:1:1 INCLUDING bow and slightly open lid. Use a squat hollow square box body, shallow square removable cap lid, and compact angular folded-paper bow so the total asset fits this cubic envelope. Thin substantial card walls, tidy folded corner seams, simple bevels. Lid rear edge stays close to the rear rim and front edge is lifted a little, exposing a narrow dark lavender gap and a little pale lavender interior. One broad pink band runs vertically down the centre of the front face and corresponding rear face; a perpendicular band wraps the side faces. Matching crossed ribbon bands on the lid, a compact symmetrical two-loop faceted paper bow with a central angular knot and two short folded tails attached to the lid. Gold foil is a narrow clean border along the lid lip and fine ribbon edges. Bow loops are simple angular folded strips with actual thickness, no fluid cloth, curls, or filigree. Keep ribbon segments attached to their respective box or lid pieces so both parts can be modelled separately. Clean simple buildable low-poly geometry, no excessive surface triangulation or decorative objects.
Composition: single complete asset, three-quarter view from slightly above, front and right side visible, centred with generous clear margins; no cropping. Plain soft pale-cream gradient background. Soft studio illumination, gentle contact shadow under the asset, clear readable planar shading, no glow.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, extra objects or inset views.
```

## views.png

Reference: ./hero.png (object design).

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the Paper Gift Box shown in the supplied hero.png reference. The reference is the definitive object design: reproduce the identical geometry, colour distribution, ribbon widths, folded bow, angular knot, forked tails, gold trim, shallow lid, narrow opening, bevels and fold seams. This is the same single asset, not colour variants.
Style: sculpted low-poly papercraft, planar flat-shaded facets with soft bevels, matte lavender #B9A6F0 paper with slight thickness, pink #FF6FAE ribbon and two hollow angular folded-paper bow loops, gold #F7D98B foil along ribbon edges and lid lip. Clean buildable geometry. Preserve the slightly open lid pose from the reference. Overall assembled W:D:H = 0.8:0.8:0.8 metres = 1:1:1, including bow and open lid. Body is squat so the bow and shallow cap fit within the cubic total envelope.
Background: perfectly flat uniform light grey #E6E6E6, no gradient, no floor, no horizon, no cast shadows on the background. Use only subtle facet shading on the object itself.
Layout: exactly three equal vertical thirds, with NO visible dividing lines. LEFT THIRD contains exactly one FRONT elevation, camera horizontal and perpendicular to the front face. MIDDLE THIRD contains exactly one RIGHT SIDE elevation, camera horizontal looking from the object's right side, showing the depth direction horizontally. RIGHT THIRD contains exactly one TOP plan, camera straight down perpendicular to the ground. Every view is TRUE ORTHOGRAPHIC with zero perspective, zero isometric projection, zero three-quarter rotation. Front face rectangular edges stay horizontal and vertical; the side elevation shows the narrow lid opening and gentle lid tilt accurately. In the top view the box perimeter is a square, with the exact crossed pink bands and same bow and tails seen directly overhead.
Scale and positioning: identical world-unit-to-pixel scale in all three views. Front and right-side elevations share exactly the same baseline and exactly the same overall height. Top-view width equals front-view width, and top-view depth equals side-view width. Use approximately 76 percent of each third's width for the full object, with generous margins. Each view is centred in its own third; no object or detail crosses a third boundary. No extra views, no insets, no exploded parts.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery or extra objects.
```

## parts.png

Reference: ./hero.png (object design).

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE for the Paper Gift Box in the supplied hero.png reference, for a modeller building clean low-poly meshes. hero.png is the definitive DESIGN reference: keep exactly its lavender box, shallow lavender cap lid, pink crossed ribbons, gold foil edging, hollow angular two-loop bow, faceted central knot, two forked ribbon tails, soft bevels, card thickness and fold seams. Match its sculpted low-poly papercraft, flat-shaded facets and matte paper surface. Colours are lavender #B9A6F0, pink #FF6FAE and gold #F7D98B.
Exactly TWO separate parts in ONE horizontal row, left to right, each centred in its own equal half-width column with clear margins. No dividing line.
LEFT HALF: the box body alone with the lid completely removed, seen three-quarter from slightly above, front and right walls visible. Show the hollow square container, pale lavender inner walls and flat interior bottom, thin sturdy paper-card wall thickness, clean folded corner seams, soft bevels and the vertical pink ribbon bands with narrow gold edges on the outer walls. No bow, no lid, no loose parts inside.
RIGHT HALF: the complete separate shallow cap LID WITH BOW attached, seen three-quarter from slightly above, the same orientation as the reference. Retain exactly its lavender lid with narrow gold lower lip, crossed broad pink bands edged in gold, two hollow faceted folded-strip pink bow loops with gold edges, central polygonal knot, and two short forked paper tails spreading toward the front corners. The cap lip and slight thickness must be clearly readable. Keep lid, ribbon and bow together as one assembly; no additional breakdown or duplicate bow. No box body below this lid.
The two displayed parts are exactly the components of the reference asset with assembled overall dimensions width 0.8 m, depth 0.8 m, height 0.8 m, W:D:H = 1:1:1 including open lid and bow. Use a consistent model scale for both parts; lid footprint fits over the box footprint. Parts are separated horizontally and never overlap or cross the central column boundary. Readable close-up construction detail, generous margins, both fully in frame.
Background: perfectly flat uniform light grey #E6E6E6, no gradient, no floor, no horizon, no cast shadows on the background. Soft neutral light with restrained shading on the objects themselves.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, extra objects or inset views.
```

