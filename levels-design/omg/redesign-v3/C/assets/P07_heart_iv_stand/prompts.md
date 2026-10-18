# Image generation prompts

Generated using the built-in image_gen tool, one call per image in spec.tsv row order.

## hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create a MODELING DESIGN SHEET hero image for a modeller building a real low-poly game mesh, for the fan-made Dancing Line style rhythm level "Bunny Pop-up Storybook" (NewJeans OMG). Output square 1:1.
Input image: style-ref.jpg is an approved world render; use it ONLY as the style/material reference, not as a scene or composition to reproduce.
Subject: exactly ONE complete Heart IV Stand, isolated. A papercraft IV drip stand with a puffy coral-pink paper heart drip bag, a slim upright pole and simple hook, and a five-spoke wheeled base with exactly five little paper wheels, one on each spoke. Overall real dimensions are width 0.8 m, depth 0.8 m, height 2.2 m; preserve W:D:H = 0.8:0.8:2.2 exactly. The full base defines the width/depth; the tall slim pole gives the height. Make the heart bag a clearly readable thick heart volume made from a small number of broad flat polygon facets, with a paper seam around its edge, hung near the top of the pole by a simple paper hanging tab. A short simple cream outlet at the heart's bottom and one restrained blush paper drip tube running beside the pole; all details must be buildable polygonal geometry.
Palette: coral #FF7A6B for the heart, blush #FFC7DA secondary heart facets and small details, wardgray #B9CFC8 for pole and five-spoke base, cream #FFF3DE for the small paper wheels and connectors. Restrained narrow gold-foil accents on hook and pole collar, consistent with the reference.
Style: sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte paper, slight visible paper thickness, clean intentional fold lines, simple solid construction, pastel colors and subtle gold foil. No photorealistic metal or transparent plastic. Keep silhouette and construction very clear.
Composition: single asset alone, three-quarter view from slightly above; show the entire stand including every wheel, with ample margins, centred in a square. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. No set dressing.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, extra objects, or inset views anywhere in the image.
```

## views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create a landscape 3:2 ORTHOGRAPHIC THREE-VIEW modeling plate of the exact Heart IV Stand in the supplied hero.png reference. Input image role: hero.png is the authoritative object design, color, material, construction and detail reference. Reproject that same model faithfully; do not redesign or simplify away details.
Plain uniform flat light grey #E6E6E6 background, no floor, no horizon, no cast shadows on the background. Exactly three invisible equal vertical thirds: LEFT third FRONT view; MIDDLE third SIDE view seen from the object's right; RIGHT third TOP view straight down. No panel borders or dividing lines. Each entire view centred in its own third with ample margins, no overlap across thirds.
Camera is TRUE ORTHOGRAPHIC with parallel projection, absolutely no perspective and no three-quarter view. Front sees the broad face of the heart; right side shows its true narrow thickness; top is a strict vertical overhead projection. All three views use exactly the SAME world-to-image scale. Front and side stand on the same baseline and have the same total height. Top view overall width equals front view overall width; top view overall depth equals side view overall width. Do not enlarge the top view to fill its column. Overall real dimensions W:D:H = 0.8:0.8:2.2 exactly, including wheels, base and highest pole cap. At a common scale the top footprint is roughly 36.36 percent of the standing view height.
Preserve the reference's puffy faceted coral-pink thick heart paper drip bag with blush upper facets, edge seam, pink hanging tab with small gold diamond, angular gold hook extending from the tall wardgray pole, gold cap and collars, cream bottom outlet, pink angular tube loop and two pink pole clips, five-spoke wardgray base and exactly five cream polygonal wheels with gold axle discs. Keep all component positions and facet structure consistent across the three projections; allow physically correct occlusion.
Materials and palette identical to hero: coral #FF7A6B, blush #FFC7DA, wardgray #B9CFC8, cream #FFF3DE and restrained gold foil. Sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte paper with slight thickness and fold lines. Even neutral studio illumination for readable geometry, with shading on the object only.
NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, extra objects, inset views or additional views anywhere.
```

## parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create a landscape 3:2 DETAIL CALLOUT PLATE for a modeller building a real low-poly Heart IV Stand mesh. Input image hero.png is the authoritative reference for the EXACT object design, colors, materials, facet layout and construction; show its existing components separately without redesigning them.
Background is perfectly uniform flat light grey #E6E6E6. No floor, no horizon, no cast shadows on the background. Exactly THREE separated part assemblies in ONE horizontal row, left to right, each centred in its own invisible equal-width column, all fully visible with generous margins, nothing crossing into adjacent columns. No other rows, insets, duplicate parts, borders or dividing lines. Use clean three-quarter inspection views and neutral soft light that reveals facets on the parts only. Detail-callout scale: enlarge the bag and base to read clearly within their columns, keep the complete tall pole visible.
LEFT column: heart drip bag alone. The identical thick puffy coral-pink polygonal paper heart, blush upper facets, broad angular face facets, paper perimeter seam, pink hanging tab with its small gold diamond, cream bottom outlet with pink connector. Include the existing slim blush paper tube emerging from its bottom, with its angular loop neatly contained in this column. Do not include pole, hook, base or wheels.
MIDDLE column: pole and hook alone. The complete tall slender square-section wardgray paper pole from the reference, gold beveled top cap, angular gold hanging hook extending left from its upper end, gold upper collar, lower gold collar above the thicker short socket at the bottom, and the existing two blush tube clips. Remove the bag, tubing, wheels and five-spoke base so the pole and hook assembly is clear.
RIGHT column: complete wheeled base alone, detached from the pole. Same low polygon wardgray central hub and exactly five chunky tapered radial paper spokes, exactly five small cream faceted paper wheels with gold axle discs, one wheel per spoke. Rotate only the inspection camera sufficiently to make all five wheels readable. No vertical pole, hook or heart.
Match the supplied hero exactly: sculpted low-poly papercraft, broad flat-shaded facets, soft narrow bevels, matte paper, slight paper thickness and intentional fold lines, gold-foil accents. Palette coral #FF7A6B, blush #FFC7DA, wardgray #B9CFC8, cream #FFF3DE. Assembled object is W:D:H = 0.8:0.8:2.2 metres; maintain component proportions from that design, with callout magnification permitted for separated parts. All geometry must be clean, simple and buildable.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks or unrelated objects anywhere.
```

