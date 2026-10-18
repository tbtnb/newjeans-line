# Exact image generation prompts

Generated using the built-in image_gen tool, one call per row in spec.tsv order. All calls used transparent_background: false.

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create ONE square 1:1 MODELING DESIGN SHEET hero image for a modeller building a real low-poly game mesh for the fan-made Dancing Line style level "Bunny Pop-up Storybook" (NewJeans OMG). No text appears in the image.
Input image: style-ref.jpg is the approved world STYLE reference only. Match the sculpted low-poly papercraft pine trees in that world, not its environment or lighting spectacle.
Subject: ONE asset "Folded Paper Pine", alone: three stacked tapered faceted paper cones, smaller at the top, medium in the middle, largest at the bottom, on a short exposed wood-coloured trunk. Exactly three foliage tiers. Overall real dimensions width 1.6 m, depth 1.6 m, height 4 m; exact overall W:D:H = 1.6:1.6:4, a slender tall pine with square-equal width and depth extents. Make buildable solid polygonal cone meshes with eight broad radial facets, clean fold creases, subtle angular subdivisions, thin visible paper rim thickness, small soft bevels. Cones share a vertical axis and overlap clearly; no loose paper flaps. Simple short octagonal trunk.
Palette: teal #173A4A and mint #BDEBD8 on foliage facets, wood #C99A6B trunk. Teal and mint recur coherently across all three tiers, with alternating broad folded faces. Matte paper, flat-shaded sculpted facets, restrained paper texture. Tiny restrained gold-foil accent along the lower foliage rim only, following the approved world's gold detail; no ornaments.
Composition: single complete tree centered, three-quarter view from slightly above, with comfortable margins on all sides. Show all the trunk and the pointed apex. No base, pot, ground patch, surrounding props, or additional assets.
Background: plain soft pale-cream gradient. Soft studio illumination and a gentle contact shadow beneath the trunk. Crisp readable geometry suitable for modelling, not painterly.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, or watermarks anywhere.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the exact Folded Paper Pine in the supplied hero.png reference. This is a technical model turnaround, not a perspective illustration. Preserve the reference's identical three stacked faceted cone foliage tiers, their overlaps, triangular fold subdivisions, alternating teal #173A4A and mint #BDEBD8 paper panels, thin gold-foil rims, small soft bevels, and short octagonal wood #C99A6B trunk. Exactly three foliage cones; copy the model faithfully without adding or removing any design details.
Use the specified real overall dimensions W:D:H = 1.6:1.6:4. Maintain these exact slender proportions in true orthographic projection; the complete front elevation width is 40 percent of its height, and the right elevation width is also 40 percent of its height.
Layout: exactly THREE equal invisible vertical thirds. LEFT third: FRONT elevation, camera perfectly horizontal, no visible top surfaces. MIDDLE third: RIGHT SIDE elevation, seen from the right at exactly 90 degrees to the front, camera perfectly horizontal, no visible top surfaces. RIGHT third: TOP plan view, camera perfectly straight down along the vertical axis. True parallel orthographic projection for all three, with zero perspective convergence, zero isometric tilt. Front and side stand on the same baseline and have exactly the same total height. All three use exactly the SAME world-to-image scale: top-view width equals front-view width, and top-view depth equals side-view width; consequently the top view is a compact octagonal footprint, not a third upright tree. In the top view show the three concentric visible octagonal cone tiers with the upper cone covering the middle and lower centres, and their matching panel colours and narrow gold rims. Each complete view is centered horizontally and vertically in its own third, with generous margins; nothing crosses a third boundary. Suggested normalized layout: front and side heights 76 percent of canvas height, widths 30.4 percent of canvas height; top footprint has that same width and depth. The top view is centered at the plate's mid-height. No separators or borders.
Flat uniform light-grey #E6E6E6 background, no floor, no cast shadows anywhere on the background. Neutral even studio illumination on objects only; crisp matte paper flat shading and slight paper thickness, clean buildable low-poly geometry.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, or watermarks anywhere. Only the three required views of the one reference model.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT MODELING PLATE for the exact Folded Paper Pine model in the supplied hero.png reference. Preserve its identical cone shapes, tier proportions, eight-sided radial facets, fold-line subdivisions, alternating teal #173A4A and mint #BDEBD8 foliage panels, narrow gold-foil rim bands, matte paper finish, slight paper thickness and soft bevels. Reference complete asset overall real dimensions W:D:H = 1.6:1.6:4.
Layout: exactly TWO separate key-part callouts in ONE horizontal row, left to right in this exact order, each centered within its own equal half of the image with comfortable margins. No visible dividing line.
LEFT half: the STACKED CONES foliage assembly alone, with all three cones still stacked and overlapping on their common axis exactly as in the hero reference, smallest top, medium middle, largest bottom. Remove the trunk from this assembly so the separation is clear. Three-quarter view from slightly above, complete apex and all rims visible. Clean buildable polygonal paper shell geometry; show the same triangular folds and thin gold edging faithfully. No extra fourth cone.
RIGHT half: the TRUNK alone, detached and enlarged as a close-up so its simple octagonal solid structure is clear. Same short wood #C99A6B octagonal prism as in the hero, plain matte wood-coloured paper, small soft bevels, eight straight side facets and a flat octagonal top, no roots, branches, collar, bark carving or extra hardware. Three-quarter view from slightly above. Show its complete silhouette. This is a separate close-up, not another complete tree.
Both parts centered vertically in their own equal columns. The foliage assembly may be tall and the trunk close-up shorter and wider; each should be comfortably readable, no overlap or crossing the column boundary.
Background: perfectly flat uniform light grey #E6E6E6; no floor and no cast shadows on the background. Neutral even studio illumination on the parts only, clear flat-shaded surfaces and restrained paper grain. Technical low-poly modeling design reference, not an environment scene.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, or watermarks anywhere. Only the two listed separated components, once each, in the specified single-row order.
```

