# Exact image generation prompts

## Row 1 — hero.png

Reference: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create a square 1:1 MODELING DESIGN SHEET hero render for a low-poly game asset, the Giant Flip Phone Tower from a fan-made Dancing Line style level, Bunny Pop-up Storybook.
Input image: style-ref.jpg is ONLY the approved world art-style reference; use its sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte paper, visible slight paper thickness and subtle fold lines, restrained gold-foil accents and pastel colours. Do not reproduce the scene.
Subject: one single tower-sized papercraft flip phone standing open upright as a landmark, long extendable antenna topped by a five-point gold star, a heart screen, a blank geometric keypad, and a telephone-cord spiral wrapped around its base. Exact overall assembled bounding proportions including the antenna, star and cord: width 5 m, depth 3 m, height 12 m, W:D:H = 5:3:12. Tall slender tower silhouette, not a squat ordinary phone.
Buildable geometry: two thick bevelled rectangular phone panels joined by a simple exposed cylindrical horizontal hinge, open nearly straight with the upper panel tilted slightly backward; upper front has a lavender inset rectangular screen containing one large faceted pink heart with a thin gold edge, lower front has a cream inset keypad with twelve blank raised rounded-rectangle keys in a 3-column by 4-row arrangement. Coral shell, cream panel faces, pink keys, lavender hinge and cord. A straight telescoping antenna emerges from the upper left corner and rises well above the phone; simple nested straight segments, gold five-point star cap. The cord is a chunky faceted lavender helix wrapping around the lower body as a stable oval foot, with a short connected end; the full base footprint is included in the 5:3 width-to-depth ratio. Gold foil only as narrow borders, hinge caps, antenna segments and star. Use simple clean manifold-looking solid parts with restrained facet counts, clear separations, no floating decorative pieces.
Palette atlas: coral #FF7A6B, cream #FFF3DE, pink #FF6FAE, lavender #B9A6F0, gold #F7D98B.
Composition: the single complete asset alone, centred, three-quarter view from slightly above, front and right side visible, with generous margins around every extremity including star and cord. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. Product render clarity suitable for a modeller, no environment.
Hard exclusions: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Keypad keys are completely blank. No extra objects.
```

## Row 2 — views.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create a landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for low-poly mesh modeling. The attached hero.png is the authoritative identity reference: show exactly this same Giant Flip Phone Tower, same component geometry, assembly, colours, gold edging, facet treatment and details. This is a technical turnaround, not a new design.
Plain perfectly flat light grey #E6E6E6 background over the entire canvas. No floor or horizon, no cast shadows or ambient shadow blobs on the background. Soft neutral object shading only.
Divide the canvas into exactly three equal vertical thirds, WITHOUT drawing division lines. LEFT third: FRONT view looking directly at the heart and keypad. MIDDLE third: SIDE view seen directly from the object's RIGHT side. RIGHT third: TOP view looking straight down. All three cameras are truly orthographic with parallel rays, no perspective, no three-quarter or isometric views. Do not rotate the model into a new pose: only move the camera.
Exact overall assembled dimensions, including star antenna and cord base: W:D:H = 5:3:12. Use exactly the SAME world-to-image scale for all three views. For a 1536 by 1024 composition, a useful layout is overall front width 340 and height 816, right-side width 204 and height 816, top width 340 and depth 204. Centre the front at x=256 and the side at x=768; both stand on the same invisible baseline y=920 with star top y=104. Centre the top view in the third at x=1280, y=512. These coordinates and dimensions are layout instructions only: render absolutely no measurements. Keep the objects fully inside their own thirds with clear margins. Top silhouette width equals front silhouette width; top silhouette depth equals side silhouette width. Front and side views have exactly equal total height and aligned star tips and bottoms.
Preserve the reference model: tall bevelled coral upper and lower phone panels, nearly upright open flip-phone stance, slight upper-panel backward lean and lower-panel slant as shown in the hero, horizontal lavender cylindrical hinge with gold end caps, cream frame around the lavender rectangular screen, central faceted pink heart edged gold, cream keypad backing with exactly twelve blank pink bevelled keys in 3 columns and 4 rows, lavender faceted coiled telephone cord wrapped around the base with its gold side socket, upper-left telescoping lavender-and-gold antenna with a faceted five-point gold star. The top view must show physically correct overhead visibility and occlusion of this unchanged upright assembly, not the entire front face laid flat.
Palette: coral #FF7A6B, cream #FFF3DE, pink #FF6FAE, lavender #B9A6F0, gold #F7D98B. Sculpted low-poly papercraft with matte paper, soft bevels, subtle fold seams, small paper thickness, gold-foil accents. Clean buildable solid geometry.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, extra objects or extra views anywhere. Every keypad key is blank.
```

## Row 3 — parts.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create a landscape 3:2 DETAIL CALLOUT PLATE for a modeller building the Giant Flip Phone Tower low-poly game mesh. Input image hero.png is the authoritative reference for component identity, proportions, colours, materials, faceting, trims and assembly details. Extract its exact components; do not redesign them.
Background: plain uniform flat light grey #E6E6E6. No floor, horizon, cast shadows on the background or background gradients. Neutral soft studio shading on the objects only.
Layout: ONE horizontal row of exactly FOUR separate component groups, left to right in this exact order, each centred within its own equal-width invisible vertical column, clear margins, no overlap or crossing between columns. Use each column for a clear close-up, with the four groups balanced around the same horizontal centreline. There are no visible column dividers.
LEFT / first column: the entire extendable telescoping antenna with its faceted five-point gold star, alternating nested lavender and gold straight shaft segments and gold base collar, removed from the phone. Show complete from star tip to mounting foot in a clear three-quarter close-up with visible paper thickness.
SECOND column: the heart screen module taken out of the upper phone panel, cream thick bevelled rectangular frame with fine gold border, lavender inset backing and the faceted pink heart outlined gold. Show a shallow three-quarter exploded close-up: screen backing, rim and pink heart separated by small readable gaps along the module's depth axis, still one coherent group, clearly expressing the original assembled relationship. Preserve the reference heart shape and frame corners.
THIRD column: the lavender telephone-cord spiral base alone, the same chunky segmented low-poly coil in an oval wrap from the reference, including its short connector end and gold side socket. Three-quarter slightly overhead close-up, open central cavity and buildable faceted cord cross section clearly visible, no phone body present.
FOURTH / last column: the complete keypad module alone, cream bevelled backing with fine gold perimeter and exactly twelve raised pink blank bevelled keys in the reference's 3 columns by 4 rows. Shallow three-quarter close-up, with keys subtly lifted above the backing to show their separate buildable solids while keeping the exact 3-by-4 placement and spacing. No extra buttons.
Keep the reference sculpted low-poly papercraft style: flat-shaded facets with soft bevels, matte paper, slight paper thickness and subtle fold seams, restrained gold-foil highlights. Palette coral #FF7A6B, cream #FFF3DE, pink #FF6FAE, lavender #B9A6F0, gold #F7D98B. These are component detail close-ups of one asset whose assembled overall W:D:H is 5:3:12, not four complete phones.
Hard exclusions: absolutely NO text, letters, numbers, labels, arrows, leader lines, grid lines, dimension lines, people, logos, watermarks or extra objects anywhere. All keypad keys completely blank. Exactly one row, exactly four groups.
```
