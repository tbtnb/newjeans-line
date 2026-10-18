# Exact image generation prompts

Generated using the built-in image_gen tool, one call per spec.tsv row, in row order. All calls used transparent_background=false.

## kit.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET for eight small ground assets for a fan-made Dancing Line style rhythm game level, Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is an approved in-game render; use it ONLY as the art-style and material reference. Match its sculpted low-poly papercraft, flat-shaded polygon facets with soft bevels, matte pastel paper, slight paper thickness, visible physical fold lines, and selective gold-foil accents. The sheet must show clean, simple, buildable real low-poly meshes, with clear silhouettes and readable construction, no environmental scene.
Composition: exactly eight isolated items in an invisible 4-column by 2-row grid, reading left to right across the top row then the bottom row. Center each item within its equal cell with generous margins, no overlap. Each item uses the same three-quarter camera viewed slightly from above, front facing the bottom of the page. Use one consistent physical scale across every item; a one-metre-wide object is visibly much larger than a 0.3-metre pebble. Plain soft pale-cream background, soft studio lighting and very gentle contact shadows only.
Top row:
First cell: round pebble, about 0.3 m wide, a squat rounded low-poly lavender stone, irregular octagonal footprint, broad planar facets and softly bevelled edges.
Second cell: flat stepping stone, about 0.6 m wide, cream with a faint pink tint, a broad low irregular polygon slab, flat top with a few triangular facets, visibly thin bevelled sidewall.
Third cell: mossy stone, about 0.5 m wide, a squat grey-lavender faceted boulder with one contiguous mint-green paper moss cap sitting flush over part of its top; the cap has a simple angular outline and a thin visible paper edge.
Fourth cell: shore rock, about 1.0 m wide, a broad asymmetric low-poly boulder, pale sky-blue and muted teal facets, two simple angular raised peaks in one connected mesh.
Bottom row:
First cell: paper scrap, about 0.2 m wide, a small irregular coral-pink paper quadrilateral with one corner folded upward and clear paper thickness.
Second cell: star floor decal, about 0.4 m wide, a flat five-point pastel-pink paper star with a narrow gold-foil perimeter, thin real geometry, resting horizontally; NOT an upright ornament.
Third cell: gold foil flake, about 0.15 m wide, a small irregular angular gold foil polygon with two crisp folds and subtle warm gold facet variation, not crumpled noise.
Fourth cell: paper wave ripple, about 1.0 m wide, a single open crescent-shaped low strip of sky-blue paper with a pale mint inner face, rising gently from the surface, a simple angular curved wave ribbon with visible thin paper edges; no water, no particles, no base tile.
Use the pastel palette of mint, cream, coral, pink, lavender, gold, teal and sky blue from the approved world. All details must be geometry or simple material regions, suitable for a modeller to recreate. No extra objects or decoration. NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks or borders anywhere. Generate exactly one image.
```

## front.png

Reference image: `./kit.png`

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET: an orthographic FRONT-view plate of the exact eight ground assets in the supplied kit.png reference. The reference is the authoritative design; change only camera projection, layout spacing and background. Preserve each mesh silhouette, polygon construction, palette, moss outline, folds, paper thickness and gold trim. Do not redesign or add detail.
Background: perfectly uniform flat light grey #E6E6E6, no gradient, no floor, no cast shadows, no ambient shadow patches. Soft neutral illumination may describe the object's own facets.
Layout: exactly eight isolated objects, same invisible 4 columns x 2 rows grid and reading order as the reference. Each object centered in its own equal cell, with generous margins. Column centers at 12.5%, 37.5%, 62.5%, 87.5% of image width. Each row centered vertically within its half of the sheet, with objects standing on a shared invisible baseline within that row. No cell lines. Maintain a consistent physical scale across items rather than making them equally large: round pebble approximately 0.3 m wide, stepping stone 0.6 m, mossy stone 0.5 m, shore rock 1.0 m, scrap 0.2 m, star decal 0.4 m, foil flake 0.15 m, wave ripple 1.0 m. Largest objects fit comfortably inside their cells.
Camera: TRUE ORTHOGRAPHIC FRONT elevation for every item. Camera horizontal at object level, zero downward tilt, no perspective, no three-quarter rotation, no top-down component. Front is the near side facing the viewer in kit.png, the bottom-of-page direction in its ground plane. All objects retain their original ground orientation and are viewed from that direction. Do NOT tilt flat objects up to display their top faces. The star floor decal is seen edge-on as its thin horizontal gold-edged thickness; the paper scrap shows its low folded corner profile; the foil shows its angular folded profile. The rock front elevations show vertical silhouettes and frontal facets, not exposed top surfaces from an elevated camera.
Top row, left to right: the round faceted lavender pebble; the low cream and pale blush stepping-stone slab with its irregular bevelled perimeter; the lavender boulder with its one angular mint moss cap; the connected blue/teal shore rock with the tall peak on the left and lower peak on the right.
Bottom row, left to right: the coral-pink paper scrap with its one triangular upfold; the horizontal pink five-point star floor decal with narrow gold-foil perimeter; the small folded angular gold-foil flake; the open crescent-shaped sky-blue paper wave with pale mint inner face and the same angular curved construction and opening orientation as the reference.
Style: sculpted low-poly papercraft, matte paper, broad flat-shaded planar facets, soft bevels, subtle paper surface, actual fold lines and thin paper edges, clean geometry a modeller can build. Keep exactly these eight assets, nothing else. NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks or borders anywhere.
```

## top.png

Reference image: `./kit.png`

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET, a TRUE ORTHOGRAPHIC TOP-view plate of all eight exact ground assets in the supplied kit.png image. The input is the authoritative geometry and material design reference, not a camera reference. Reproject those same objects looking VERTICALLY STRAIGHT DOWN, camera optical axis perpendicular to the horizontal ground plane. Zero perspective and zero oblique angle. The image is a technical plan view: horizontal top faces face the viewer, vertical walls have no visible height, no frontal elevations, no isometric projection. Every object must be shown from precisely the same directly overhead camera.
Retain the exact design, colours, polygon facet construction, asymmetric footprints, moss cap outline, folds, gold star border, blue-and-mint crescent ripple, and paper materials from kit.png. Do not redesign, rotate objects in their ground plane, or add objects.
Layout: eight isolated assets in exactly the same reading order, on an invisible 4 columns x 2 rows grid, each centered in its own equal cell with full margins. Column centers are at 12.5%, 37.5%, 62.5%, 87.5% of the image width; row centers at 25% and 75% of image height. No grid marks. Use consistent physical scale across items: pebble 0.3 m, stepping stone 0.6 m, mossy stone 0.5 m, shore rock 1.0 m, paper scrap 0.2 m, star decal 0.4 m, foil flake 0.15 m, wave ripple 1.0 m. Largest object fits in its cell, small objects remain appropriately smaller.
Top row from left to right:
Round lavender pebble, its irregular rounded octagonal footprint and crown facets seen directly from above.
Flat cream-blush stepping stone, its broad irregular polygon top and triangular facet pattern seen directly from above.
Lavender mossy stone, its mint angular contiguous paper moss cap on top seen directly from above; preserve the cap's distinctive jagged boundary.
Blue/teal shore rock, its connected asymmetric two-peak footprint seen directly from above, taller peak on the left and lower peak on the right as in the reference.
Bottom row from left to right:
Coral-pink irregular paper scrap with its single triangular folded corner, seen directly from above.
Pink five-point star floor decal with a narrow gold perimeter, lying flat so its full five-point star shape is visible face-on in this top view, one point toward top of image.
Small folded angular gold-foil flake with its exact polygon silhouette and crisp crease planes, seen directly from above.
Open crescent-shaped blue paper wave ripple with a pale mint inner face and angular strip construction, viewed straight down; maintain its opening toward the right of the sheet exactly as in the reference.
Style: sculpted low-poly papercraft with broad flat-shaded facets, gentle bevels, matte pastel paper with subtle paper texture, slight actual thickness and crisp fold lines, selective gold foil. Simple buildable real meshes for a low-poly game. Neutral soft object illumination only.
Background: perfectly uniform flat light grey #E6E6E6 over the entire image, NO cast shadows, no background shading, no floor, no horizon, no gradient. No extra decoration. NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks or borders anywhere.
```

