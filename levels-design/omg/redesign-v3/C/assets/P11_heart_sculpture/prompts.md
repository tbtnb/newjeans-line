# Exact image generation prompts

## 1. hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create a square 1:1 MODELING DESIGN SHEET hero render for a real buildable low-poly game asset, Paper Heart Sculpture, in the fan-made Dancing Line style level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, planar flat-shaded triangular facets, small soft bevels, matte paper with visible slight thickness and restrained fold seams, pastel colours and gold-foil edging. Isolate the requested object; do not reproduce the reference environment.
Subject: ONE upright faceted pink paper heart sculpture mounted on ONE small cream stand. The entire assembled sculpture has exact physical overall bounding dimensions width 1.5 m, depth 0.6 m, height 1.6 m, W:D:H = 1.5:0.6:1.6. Design the heart as a clean symmetric classic heart silhouette with two rounded polygonal lobes, central upper notch, pointed lower tip, broad pink front and back with modest faceted convexity and a continuous thin gold rim around the heart perimeter. Use a sparse, deliberate triangular low-poly facet layout, not a smooth inflated balloon. Heart bounding box approximately W 1.5 m x D 0.6 m x H 1.2 m, from height 0.4 m to 1.6 m. Simple short cream rectangular support beneath the heart tip, attached to a shallow bevel-edged cream rectangular plinth; stand combined height 0.4 m, plinth width approximately 0.65 m and depth 0.45 m. The stand must be solid, stable, easy to model, and visible. No ornament or extra props.
Palette: pink #FF6FAE heart, gold #F7D98B thin rim, cream #FFF3DE stand. Show the gold as softly reflective foil with flat facets, no glow or glitter.
Composition: the complete single assembled asset, three-quarter view from slightly above, front and right side visible, centered with generous margins in a square canvas. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background.
Buildable geometry with clean boundaries and clear structural joins. No text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

## 2. views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the exact Paper Heart Sculpture in the reference hero.png. The input image is the definitive MODEL IDENTITY reference: retain its polygonal twin-lobed pink heart, central notch and pointed tip, front triangular facet topology, continuous gold perimeter rim, pink depth sidewalls, and cream short square pillar with gold top cap on the beveled rectangular cream plinth with narrow gold edge trim. Match this exact design, colours, materials and details. Do not redesign or add anything.
Physical assembled dimensions W:D:H = 1.5:0.6:1.6 metres exactly. Heart about 1.2 m high above the 0.4 m stand assembly. Pink #FF6FAE, gold #F7D98B, cream #FFF3DE. Sculpted low-poly papercraft with flat planar facets, slight paper thickness, small bevels, restrained fold lines and matte paper; gold foil without glow.
Canvas: landscape 3:2, completely uniform flat light grey #E6E6E6 background. No floor, horizon, background shading, ambient shadow or cast shadows. Only subtle facet shading on the objects.
Layout: exactly three invisible equal vertical thirds, no separators. LEFT third = true FRONT orthographic elevation, looking directly at the broad heart face; MIDDLE third = true SIDE orthographic elevation seen directly from the right, showing only the depth profile; RIGHT third = true TOP orthographic view looking vertically straight down, showing the edge-on depth of the upright heart and any visible stand surfaces. These are engineering projections of one identical model, not three perspective renders. No perspective, camera yaw or camera tilt in any view. Top view is NOT a front-facing heart silhouette.
Use the same world-to-pixel scale for every projection. Front and right-side share the exact baseline and exact height. The FRONT projected bounding box W:H = 1.5:1.6. The SIDE projected bounding box W:H = 0.6:1.6, thus only 40 percent the front width. The TOP projected bounding box W:H = 1.5:0.6, its width exactly equals FRONT width and its vertical depth exactly equals SIDE width. Centre each projection in its own third, with generous margins; nothing crosses a third boundary. Keep top projection centred vertically in the right third. For example at 1536x1024 canvas each front/top projected width can be 420 px, front/side height 448 px, side width and top depth 168 px. These measurements are layout instructions only and must never appear as marks or writing.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Exactly three assembled views, no extra detail thumbnails.
```

## 3. parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create one landscape 3:2 DETAIL CALLOUT MODELING PLATE of the exact Paper Heart Sculpture from input hero.png. The reference hero is the definitive model identity. Preserve its design, colour palette, facet pattern, geometry, material treatment, and gold edging exactly.
Uniform flat light grey #E6E6E6 background, no floor, horizon, cast shadows or background gradient.
Exactly TWO separately shown parts in ONE horizontal row, left to right, each centered in its own invisible equal-width column, with generous margins and no overlap. LEFT column: the complete faceted heart ONLY, detached from the stand, in a slightly elevated front-right three-quarter view. RIGHT column: the complete stand ONLY, the short cream square pillar with its gold cap attached to the shallow beveled rectangular cream plinth and its narrow gold edge trim, shown in a matching slightly elevated front-right three-quarter view. Show the entire detached heart and the entire stand, not cropped fragments. Enlarge the stand callout enough to clearly show its construction, while keeping both parts comfortably within their own columns. Both callouts centered at the same horizontal midline; no other objects, no assembled thumbnail, no exploded subcomponents.
The heart has two polygonal lobes, a central top notch, pointed bottom tip, broad pink front with the same sparse triangular facet arrangement as the reference, pink sidewall depth, and continuous thin gold perimeter rim. Keep real assembled overall dimensions W:D:H = 1.5:0.6:1.6 m as the design basis; detached heart approximately W 1.5 m x D 0.6 m x H 1.2 m, stand assembly approximately H 0.4 m. Do not turn the heart into a flat sheet, balloon, jewel or smooth plastic object.
Style: sculpted low-poly papercraft, flat-shaded facets, small soft bevels, matte paper with restrained paper grain, slight paper thickness and subtle fold seams, buildable solid geometry. Pink #FF6FAE, gold #F7D98B, cream #FFF3DE. Soft studio lighting on objects only; foil accents without glow.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

