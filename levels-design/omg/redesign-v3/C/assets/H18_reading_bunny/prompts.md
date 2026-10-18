# Exact image generation prompts

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero render for a modeller building a real low-poly game mesh, for the rhythm-game world Bunny Pop-up Storybook.
Input image: style-ref.jpg is ONLY the approved material and art-style reference. Match its sculpted low-poly papercraft, planar flat-shaded facets, small soft bevels, matte coloured paper, slight sheet thickness and visible intentional fold seams, restrained gold-foil edge accents and gentle pastel warmth. Do not reproduce its surrounding world.
Subject: the single asset "Reading Bunny under Mushroom": a small cream paper bunny sitting under a big teal paper mushroom, reading a big open book with completely blank pages; a tiny curved lamp glowing warm gold; a few small fireflies. Include a simple mint mossy polygonal base as part of this one assembled asset. The mushroom canopy shelters the bunny and book; make every component clean, visibly separable and buildable with simple low-poly geometry. Use an angular folded mushroom cap, stout simple stem, faceted seated bunny with long paper ears and small paws supporting the open folded book. Lamp is a small bent polygonal stem and simple shade. Fireflies are only a few simple tiny golden geometric forms, no trails or visual clutter.
Physical overall bounding-box dimensions width 3 m, depth 3 m, height 3.5 m: W:D:H = 3:3:3.5, including the base and cap. Preserve these proportions. Palette: teal #173A4A, cream #FFF3DE, lamp #FFC968, mint #BDEBD8, navy #1F2350. Gold foil used sparingly.
Composition: single assembled asset alone, three-quarter view from slightly above, entire object fully visible with generous margins. Soft studio illumination, gentle contact shadow. Plain soft pale-cream gradient background, no environment.
Model clarity: large readable facets, paper thickness, simple bevels, restrained folds, no painterly geometry or fuzzy fur.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Book pages entirely blank. Exactly one image.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the exact assembled asset in the supplied hero.png reference. This is a technical mesh turnaround, not a beauty render.
Input image hero.png: definitive reference for geometry, design, colours, component placements and all details. Preserve that identical Reading Bunny under Mushroom model: wide low-poly teal mushroom canopy with cream radial folded underside, fine gold edges/seams and small gold star ornaments; thick cream faceted stem behind the cream seated long-eared bunny, pink inner ears and foot pads, dark navy eyes, big open navy/gold-bound book with blank cream pages, curved angular gold lamp to the bunny's left, a few golden fireflies, thick faceted mint mossy base with its existing leaves, small flowers and rocks. Do not redesign, add, omit, mirror or rearrange components.
Overall physical bounding box W:D:H = 3:3:3.5 (3 m wide, 3 m deep, 3.5 m high). Use this exact ratio for the three projections.
Canvas: flat uniform light grey #E6E6E6, no background shadows, no floor, no gradient. Exactly three equal invisible vertical thirds. LEFT third: straight-on FRONT orthographic view, book and bunny face toward viewer. MIDDLE third: true RIGHT SIDE orthographic view, camera looks from the model's right, bunny faces toward the left of this panel. RIGHT third: true TOP orthographic view, straight vertically down; show the canopy and the naturally occluded components correctly, no cutaways or transparent surfaces.
All three use identical world-units-to-image scale, no perspective or foreshortening from perspective. Front and side have identical total height and share exactly the same horizontal bottom baseline. Top silhouette width equals front silhouette width; top silhouette depth equals side silhouette width. Since width and depth are both 3 m, top footprint is equally wide and deep. Fit everything inside each third with clear margins. For precision on a 1536x1024 layout, third centres are x=256,768,1280; use approximately 420px per 3m, front and side total heights approximately 490px, common baseline y=760; centre top view in its own third. No visible lines between thirds.
Match sculpted low-poly papercraft: flat-shaded planar facets, subtle soft bevels, matte paper, slight sheet thickness and fold lines, restrained gold foil. Neutral even studio material lighting solely to distinguish facets, zero cast shadows on background. The entire asset must be visible within each third and nothing may cross thirds.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Book pages blank. Exactly three views and no other insets.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE for the Reading Bunny under Mushroom asset. Input image hero.png is the definitive design reference: extract the SAME geometry, colours, materials and details into isolated buildable components, without redesigning them.
Layout: exactly FOUR separate key parts, in ONE horizontal row, left to right in this exact order, each centred in its own equal invisible vertical column with ample margins and air between parts. No part crosses another column. Show each part once, at a useful close-up scale to explain its mesh construction; isolated three-quarter views from slightly above, consistent orientation. Uniform flat light grey #E6E6E6 background, no floor, no cast shadows on background, no dividing lines.
Leftmost column: big mushroom CAP ONLY, detached from stem. Exact hero teal faceted canopy with thin gold outer rim and selected gold fold seams, existing small raised gold star/diamond ornaments, cream thick folded radial underside visible at the near edge. Make its thickness and simple polygon topology readable. No mushroom stem or bunny here.
Second column: bunny WITH its open book as one isolated assembly, removed from surroundings. Exact hero seated cream faceted long-eared bunny, pink inner ears and foot pads, dark navy polygon eyes, pink tiny nose, paws holding the large open book, blank thick cream page layers, navy book cover with restrained gold corner bindings. Include full ears and feet with margins. No base, lamp or mushroom in this column.
Third column: tiny LAMP ONLY, detached, same hero angular curved gold stem with its simple foot, hinged bent top and flared polygonal shade, warm pale-gold glowing lamp inside. All lamp pieces readable and physically buildable; no fireflies or environment around it.
Rightmost column: mossy BASE ONLY, same hero thick low-poly mint polygonal disk with gold rim accents and its existing faceted leaves, little cream flowers and lavender rocks; remove mushroom, bunny, book and lamp so the attachment surface and low-poly contours can be understood. Keep the original base silhouette and botanical placements.
Match approved hero style exactly: sculpted low-poly papercraft, broad flat-shaded planar facets with small soft bevels, matte coloured paper, subtle paper thickness, clear fold seams and restrained gold foil. Palette teal #173A4A, cream #FFF3DE, lamp #FFC968, mint #BDEBD8, navy #1F2350, with the hero's existing minor decorative colours unchanged. The assembled source model has total W:D:H = 3:3:3.5; preserve actual part proportions internally, while allowing separate callouts to be magnified for readability.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Book pages entirely blank. Exactly four callouts in one row, no additional insets or assembled asset.
```

