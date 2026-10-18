# Exact image-generation prompts

## 1. hero.png

Reference: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero render for a buildable low-poly game asset: H19_paper_sun, Layered Paper Sun, for the rhythm-game world Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper, visible paper thickness and fold lines, pastel colours, restrained gold-foil accents. Do not reproduce its environment.
Subject: one upright layered paper sun disc with folded triangular rays in gold and pink, a gentle smiling face embossed, rising behind paper clouds. The COMPLETE assembly has exact overall W:D:H = 8:1:8, corresponding to 8 m wide, 1 m deep, 8 m high. It is a shallow upright decorative sculpture, not a sphere. Keep the full outer silhouette square in front elevation; cloud edges stay inside the outer sun width and the clouds end at the lowest ray level.
Buildable design: a sixteen-sided layered circular disc, with sixteen evenly spaced separate folded triangular rays alternating pale gold and pink. Simple low-poly shallow relief and crisp folded ridges, each ray a solid thin paper wedge with a central fold, no intricate filigree. Three concentric stepped paper disc layers: thin cream backing, gold rim, warm yellow front face. Embossed face consists of two small closed-eye curved ridges and one small gentle curved smile in warm gold, with two subtle peach cheek shapes. No lettering. In front of the lower disc sits one connected low-poly paper cloud cluster: cream faceted rounded lobes with a peach backing layer, thin solid edges, a few readable fold seams. Clouds partly overlap the bottom disc but leave the face fully visible. Every element has sensible thickness and physically connected construction.
Palette: sun yellow #FFD23F, pale gold #F7D98B, pink #FF6FAE, peach #FFC2A8, cream #FFF3DE. Gold foil only on the rim and restrained ray accents; no emissive glow.
Composition: single asset alone, three-quarter view from slightly above, showing the front, the right-hand shallow thickness, and a little of the upper edges. Completely visible with generous margins. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. Clean modelling reference, readable geometry and unobstructed silhouette.
Hard exclusions: no text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, pedestal, additional objects, or inset views.
```

## 2. views.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create one landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a low-poly modeller, ideally 1536 by 1024 pixels.
Input image: hero.png is the authoritative asset identity reference. Depict exactly this same Layered Paper Sun sculpture, preserving its ray arrangement, alternating pink and pale-gold folded rays, cream backing disc, gold rim, faceted yellow face, embossed golden closed eyes and curved smile, two peach polygonal cheeks, and connected cream faceted cloud cluster with peach backing at the lower front. Preserve all visible shapes, colours, folds, layer thicknesses and details. Reproject the same model; do not redesign it.
Overall real assembly proportions must be exactly W:D:H = 8:1:8 (8 m wide, 1 m deep, 8 m high), including rays and clouds. The model is an upright shallow paper relief; its full width and height are equal and its total front-to-back thickness is one eighth of that width. Clouds stay within the overall width and height. Paper geometry is solid, buildable, low-poly, with soft bevels, flat-shaded facets, matte paper surfaces, slight paper thickness, fold lines and restrained gold foil. Palette: yellow #FFD23F, gold #F7D98B, pink #FF6FAE, peach #FFC2A8, cream #FFF3DE.
Layout is exactly three equal vertical thirds with no visible dividers: LEFT third is the FRONT view looking straight at the face; MIDDLE third is the SIDE view seen from the object's RIGHT, looking exactly edge-on; RIGHT third is the TOP view looking straight down. True orthographic projection in every view: parallel rays, zero perspective, zero three-quarter rotation, no vanishing points. Front shows no right side; side shows the thin edge profile rather than a second face; top shows a very shallow horizontal edge profile rather than another frontal disc.
Use the SAME world-to-image scale in all three. For a 1536 by 1024 canvas, centre the views horizontally at 256, 768 and 1280 pixels. Front's complete bounding box is approximately 416 pixels wide and 416 pixels high; right side is 52 pixels wide and 416 pixels high; top is 416 pixels wide and 52 pixels deep. Front and side share the exact same baseline and same height. Centre every complete view vertically at the canvas mid-height; front and side baseline is approximately 720 pixels. The top width equals front width, and top depth equals side width. Keep substantial empty space above and below; do not enlarge the thin views to fill the frame. Each view entirely inside its own third with margin.
Background is perfectly flat uniform light grey #E6E6E6 from edge to edge, with no floor, horizon, gradient or cast shadows on the background. Use neutral diffuse modelling illumination to reveal the object facets only, no glow.
Hard exclusions: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, borders, extra views, people, logos, watermarks, scenery, pedestals or unrelated objects. Exactly three views of the identical complete model.
```

## 3. parts.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create one landscape 3:2 DETAIL CALLOUT PLATE for a modeller building low-poly meshes of H19_paper_sun, Layered Paper Sun.
Input image: hero.png is the authoritative identity reference. All parts must be extracted from that exact same design, preserving its colours, shapes, faceted surfaces, embossed expression, gold rim, fold construction, paper thickness and cloud shape. This is a clean component sheet, not an assembled scene.
Exactly THREE separated key-part displays in ONE horizontal row, left to right in the following order, one display centred within each of three equal-width columns. No visible column separators. Keep every display entirely within its own column, with generous empty margins and clear gaps.
LEFT: layered sun disc only, with the surrounding triangular rays and clouds removed. Show its sixteen-sided circular cream backing, stepped gold-foil rim and shallow faceted yellow face as slightly separated coaxial layers in a compact exploded three-quarter view, the assembled order and shallow solid thickness clearly readable. Keep the gold embossed closed-eye ridges and gentle curved smile and two peach polygonal cheeks attached to the yellow front face. All three layers form a single coherent component display; do not duplicate the face.
MIDDLE: one folded triangular ray extracted from the hero, choosing one pink ray with its pale-gold thin edge/backing. Show one isolated broad triangular paper wedge, central ridge and two planar folded pink facets, with a shallow solid back and softly bevelled edges, in a close-up three-quarter view. Clearly buildable simple mesh, no ornate detailing.
RIGHT: the paper cloud component extracted from the hero: one connected cluster of the same cream angular rounded lobes, large raised lobe toward the left and broad central lower lobe, smaller lobes toward the right, backed by the same peach silhouette layer. Show a three-quarter close-up revealing the faceted cream lobe geometry, peach backing offset and thin solid paper edges. Keep the entire cluster together as one component display.
Style: sculpted low-poly papercraft, flat-shaded facets, subtle soft bevels, matte paper with slight paper thickness and readable fold seams, restrained gold foil. Match hero.png exactly. Palette: sun #FFD23F, gold #F7D98B, pink #FF6FAE, peach #FFC2A8, cream #FFF3DE. Arrange all three component displays around the same horizontal midline, at readable close-up sizes; parts are not required to share a physical scale.
Background: uniform flat light grey #E6E6E6, no gradient, no floor, no horizon, no cast shadows on the background. Neutral diffuse studio illumination only on the parts.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, borders, people, logos, watermarks, pedestal, scenery, extra components, extra rows, assembled sun, or inset views. Exactly three component displays in one row: layered sun disc, folded ray, paper cloud.
```

