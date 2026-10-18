# Exact generation prompts

## Row 1 — hero.png

Reference image: ./style-ref.jpg

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image for the single asset "Lake Paper Pavilion" for a fan-made Dancing Line style rhythm game level Bunny Pop-up Storybook.
Input image: style-ref.jpg is an approved in-game render; use it as an ART STYLE reference only, not a composition or environment to reproduce.
Subject: a small round paper pavilion on a tiny island, exactly six slim columns supporting a scalloped dome roof, one gold crescent finial on the roof apex, paper lanterns hanging under the eaves, and a single short flight of steps descending at the front toward the waterline. Include the island base as part of the single asset; do not add a surrounding lake, scenery, plants or unrelated props.
Overall real geometry bounding box including island, steps and crescent: width 5 m, depth 5 m, height 6 m, exactly W:D:H = 5:5:6. The front steps fit within this footprint. Six evenly spaced columns form a circular hexagonal arrangement, leave an open interior, and remain distinctly countable without extra supports. Use a simple twelve-segment faceted dome with six broad scalloped eave lobes, simple narrow gold edge trim and readable fold seams. Six small faceted warm paper lanterns hang between the columns. Use simple octagonal slim pearl columns with plain bevelled capitals and bases. Circular low-sided island plinth with layered paper edges, a pearl platform, and four broad front steps. Design clean connected volumes that a modeller can reproduce as actual low-poly meshes; no floating ornament other than physically suspended lanterns.
Art style: sculpted low-poly papercraft matching the approved reference, flat-shaded polygon facets, soft small bevels, matte paper with slight visible card thickness and restrained fold lines, selective gold-foil accents, pastel colours. Clean construction rather than intricate filigree.
Palette: pearl #F3F1EA for columns/platform/steps, moon #BFD4F5 and lilac #E3D7FA for alternating roof facets and layered island edges, gold #F7D98B for crescent and thin trims, lamp #FFC968 for lanterns. Crescent is a thick flat low-poly gold cutout oriented in the front-facing vertical plane.
Composition: single complete asset alone, three-quarter view from slightly above with front steps visible, centred with generous clear margins on all sides. Square canvas. Soft studio lighting and a gentle contact shadow. Plain soft pale-cream gradient background.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No secondary views, no exploded parts, no ground scenery, no extra assets.
```

## Row 2 — views.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the Lake Paper Pavilion shown in the supplied hero.png. Input image hero.png is the authoritative DESIGN reference: reproduce the identical asset, colours, geometry, roof scallops, crescent, six columns, lanterns, island and front steps. Change only the camera and sheet layout. This is a technical turnaround for building real low-poly geometry.
Background: perfectly flat uniform light grey #E6E6E6 across the whole canvas. No floor, no horizon, no cast shadows, no contact shadows, no vignette or gradient.
Layout: exactly three equal vertical thirds, without visible dividers. LEFT third: FRONT elevation looking horizontally straight at the front steps. MIDDLE third: RIGHT SIDE elevation seen horizontally from the asset's right. RIGHT third: TOP plan looking exactly vertically down. Each view is centred within its own third, with generous margin, and nothing crosses into another third. No additional views, insets, duplicates or detached parts.
Projection: true parallel orthographic projection in all three views, absolutely no perspective or three-quarter views. Front and right-side views show no top surfaces of the plinth or roof; vertical columns parallel, no convergence. Top view shows the roof from directly above, with only the island perimeter and front steps that naturally extend beyond the roof visible. Proper occlusion: do not make a transparent roof or show hidden columns through the roof.
Geometry proportions: the SAME physical scale for all three views, full asset bounding box W:D:H = 5:5:6 including crescent, island and steps. Use approximately 25 percent of total canvas width for each asset's five-metre width or depth, and 45 percent of total canvas height for the six-metre height. Front and side stand on exactly the same baseline, their crescent tops reach the same level, and their total heights match. Top view width exactly equals front view width; top view depth exactly equals side view width. Top view is centred vertically in its third. Crescent is a thin thick-paper gold cutout in the front-facing vertical plane, so its face is visible in front elevation, its narrow thickness in right-side elevation, and its narrow edge in top view.
Design invariants from reference: round faceted layered lilac island, pearl circular pavilion platform with thin gold perimeter, broad front flight of pearl steps with short solid pearl side cheeks edged in gold; six evenly spaced slim octagonal pearl columns with bevelled pearl capitals/bases and narrow gold collar rings; scalloped low-poly dome with alternating moon-blue and lilac faceted paper segments and gold scalloped edge trim; thick faceted gold crescent on a small gold apex pedestal; warm faceted paper lanterns suspended under the eaves between the columns. Preserve reference details including subtle geometric floor inlay wherever visible. No redesign.
Materials and palette: sculpted low-poly papercraft, flat shaded facets, soft small bevels, matte paper thickness and subtle folds, gold foil accents. Pearl #F3F1EA, moon #BFD4F5, lilac #E3D7FA, gold #F7D98B, lamp #FFC968. Neutral even studio illumination on the asset only, no shadows on background.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks or decorative scenery anywhere.
```

## Row 3 — parts.png

Reference image: ./hero.png

```text

```

