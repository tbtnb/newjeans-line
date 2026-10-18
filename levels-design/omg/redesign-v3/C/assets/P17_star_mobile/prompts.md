# Image generation prompts

Generated with the built-in image_gen tool, one call per image in spec.tsv row order.

## hero.png

Reference: `./style-ref.jpg` (approved style reference).

```text
Use case: stylized-concept
Asset type: low-poly 3D modeling design sheet, single-asset hero render.
Create exactly one square 1:1 image of the Star Mobile for the fan-made Dancing Line style rhythm level Bunny Pop-up Storybook.
Input image: /Users/bit_1/nj-level-art/omg-c-assets/P17_star_mobile/style-ref.jpg is a STYLE REFERENCE ONLY. Match its sculpted low-poly papercraft, flat shaded triangular facets, soft tiny bevels, matte paper surfaces, slight cardstock thickness, visible restrained fold lines and selective gold foil accents. Do not reproduce its scene.
Subject: one hanging mobile made of gold paper stars and one small crescent suspended on thin straight strings from a bunny-ear shaped hanger. Make a simple buildable mobile: one horizontal lilac cardstock support hoop with two upright cream bunny ears attached at the back, cream inner ear panels and narrow gold edging, several well-separated faceted five-point gold paper stars and one smaller gold crescent dangling below at different heights. Thin gold suspension strings visibly join each pendant to the hoop. Keep construction clear, few polygons, solid paper thickness, simple planar folded surfaces, no filigree.
Overall real bounding size precisely width 1.5 m, depth 1.5 m, height 2.5 m, W:D:H = 1.5:1.5:2.5. Hoop spans equal width and depth. Height includes ears and longest pendant. Silhouette is tall and airy, not squat. Every component must be geometrically buildable.
Palette: gold #F7D98B, lilac #E3D7FA, cream #FFF3DE, gold foil only in restrained edge accents. Warm pastel shades, no glow.
Composition: SINGLE complete asset alone, three-quarter view from slightly above, centered with ample clear margins. Show the whole hanger, every string and all pendants without cropping. Soft studio light, subtle gentle contact shadow only, plain soft pale-cream gradient background. No extra scene props, no base or stand.
Hard prohibitions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

## views.png

Reference: `./hero.png` (first generated image; design reference).

```text
Use case: stylized-concept
Asset type: technical orthographic three-view modeling turnaround.
Create exactly ONE landscape 3:2 image.
Input image: /Users/bit_1/nj-level-art/omg-c-assets/P17_star_mobile/hero.png is the authoritative DESIGN REFERENCE. Show that exact SAME Star Mobile, not a redesigned variation. Preserve the low-poly lilac polygonal horizontal hoop with narrow gold trim, two upright bevel-faceted cream bunny ears with pale blush-lilac inset panels and gold inner trim, triangular gold suspension bridle and faceted central gold joint, thin straight gold cords and diamond-shaped gold joints. Preserve four five-point folded faceted gold stars: one large central star, medium upper left and upper right stars, one smaller lower left star; one small faceted crescent low on the right, and the small separate diamond end weight beside it. Preserve their sizes, placements and cord lengths in 3D. All pendant broad faces are parallel with the front plane, so they become thin edged profiles from the right. Stars have crisp planar fold facets and actual shallow thickness, crescent has a polygonal inner concave edge. Preserve all reference colors and construction.
Model bounding dimensions precisely W:D:H = 1.5:1.5:2.5. Width and depth are equal. Height includes hanger and all suspended components. Terminate the upper suspension neatly in a visible small loop above the central joint so the complete asset can fit inside the frame. No cropping or endless string.
Layout: exactly THREE equal INVISIBLE vertical thirds of the canvas. LEFT third FRONT elevation, MIDDLE third RIGHT SIDE elevation seen from the right, RIGHT third TOP plan straight down. True parallel orthographic projections, zero perspective, zero camera tilt in front and side, no isometric views. The front hoop must appear as a horizontal thin band with its real thickness, never as an ellipse; in the top view the horizontal hoop is circular/polygonal and the vertical ears and hanging pendants appear correctly foreshortened from above, never frontal symbols. Physical occlusion is correct.
All three views have exactly the same units-to-pixels scale. Front and side have exactly the same overall height and the same baseline. Top width equals front width, top depth equals side width. Use each third's center as its horizontal axis: front at one-sixth canvas width, side at one-half, top at five-sixths. Each complete view stays entirely within its own third with clear margins, no element crosses a third boundary. Center top view vertically within its own third. Front and side equal height about 72 percent of the canvas height, therefore each object's width and top-plan depth is about 43.2 percent of the canvas height.
Background is uniform flat light grey #E6E6E6 across the entire image. No floor, horizon, background shadows, ambient occlusion on the background or gradients. Soft neutral surface lighting only, to reveal matte cardstock facets and restrained gold foil. Geometry is simple and buildable, flat shaded and subtly beveled, slight paper thickness and fold creases.
Hard prohibitions: NO text, letters, numbers, labels, captions, arrows, grid lines, panel dividers, borders, dimension lines, people, logos or watermarks anywhere. Exactly three views of one model and nothing else.
```

## parts.png

Reference: `./hero.png` (first generated image; design reference).

```text
Use case: stylized-concept
Asset type: DETAIL CALLOUT PLATE for a low-poly mesh modeller.
Create exactly ONE landscape 3:2 image. Input image /Users/bit_1/nj-level-art/omg-c-assets/P17_star_mobile/hero.png is the authoritative DESIGN REFERENCE. Extract its exact parts, with identical geometry language, colors, fold facets, bevels, thickness, gold foil trim and paper material.
Layout: exactly THREE equal INVISIBLE vertical columns. Show the three listed key parts separately in ONE horizontal row, left to right in this precise order: LEFT bunny-ear hanger, MIDDLE paper star, RIGHT small crescent. Exactly one assembly or part per column, no duplicates. All three objects centered vertically at the same row height, each centered horizontally in its own third with ample margin; no part crosses into another third. They are isolated component close-ups and may be enlarged independently for clarity. No assembled mobile in addition to these three callouts.
LEFT: the hero's complete bunny-ear hanger assembly alone: thick horizontal polygonal lilac hoop with narrow gold top edging, two upright cream beveled faceted bunny ears at its back with pale blush-lilac inset panels edged in gold, its simple triangular gold suspension bridle and central faceted gold connector. Neatly terminate its upper cord with a small closed attachment loop inside the frame. Remove ALL hanging star/crescent pendants and ALL lower dangling strings; show the rigid hanger and upper suspension only. Clear three-quarter view from slightly above so the hoop depth and solid paper thickness are understandable.
MIDDLE: exactly one of the hero's gold five-point paper stars, isolated and enlarged as a component close-up. Match its raised central point, five triangular ridges, ten planar gold-toned facets, shallow thick cardstock perimeter and fine foil edge. A slight three-quarter front angle reveals its thickness. No string, no hanger, no additional bead.
RIGHT: exactly the hero's small gold crescent alone, isolated and enlarged as a component close-up, matching its open concave inner edge, two tapered tips, angular convex arc and coarse planar triangular gold facets. Same slight three-quarter front angle reveals its real shallow solid paper thickness. No string, no bead.
All components come from the SAME mobile with original overall W:D:H = 1.5:1.5:2.5; preserve the reference design. Sculpted low-poly papercraft, flat-shaded facets, tiny soft bevels, matte paper, restrained fold lines, selective gold foil edge accents. Gold #F7D98B, lilac #E3D7FA, cream #FFF3DE plus the reference's pale inset-panel shading. Buildable simple meshes, no delicate filigree.
Background: perfectly uniform flat light grey #E6E6E6. No floor, no cast shadows or contact shadows on the background, no horizon, no gradient. Soft neutral studio surface lighting to make facets clear, no glow.
Hard prohibitions: NO text, letters, numbers, labels, arrows, grid lines, column dividers, borders, dimension lines, people, logos or watermarks anywhere. Exactly the three requested part callouts in one row and nothing else.
```
