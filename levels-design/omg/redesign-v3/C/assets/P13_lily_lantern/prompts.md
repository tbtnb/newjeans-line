# Exact image generation prompts

Generated in spec.tsv row order using the built-in image_gen tool, one call per image. All calls used transparent_background: false.

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Asset type: low-poly mesh MODELING DESIGN SHEET, hero image for the fan-made Dancing Line style rhythm-game level Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is an approved in-game render; use it only for the sculpted low-poly papercraft visual language, pastel palette, matte paper facets, gentle bevels and restrained gold-foil accents. Do not reproduce its environment.
Create exactly one isolated asset: Paper Lily Lantern. A compact assembly of overlapping mint paper lily pads supporting one glowing pink-white lotus lantern flower. Overall real-world bounding dimensions precisely width 1.2 m, depth 1.2 m, height 0.8 m, W:D:H = 1.2:1.2:0.8. The lily-pad footprint supplies the full width and depth. One main near-circular polygonal lily pad with a simple radial notch, with two smaller overlapping pads. One central open lotus flower with two tidy rings of broad, pointed, folded low-poly petals around a small warm lamp core; blush outer petals and pearl inner petals. Make the flower upright and tall enough that the whole assembly has the specified height. Clean clearly separable buildable components, broad planar facets, a small number of vertices, subtle bevels, visible paper edge thickness, crisp folds and simple radial pad creases. Restrained thin gold-foil accents on selected petal edges and the lamp rim. No stems, wires or floating decorations.
Palette: blush #FFC7DA, pearl #F3F1EA, mint #BDEBD8, lamp #FFC968. Matte paper, flat-shaded sculpted facets; the inner lamp softly glows pink-white and warm cream without obscuring geometry. All petal tips and pad contours remain crisp and readable.
Composition: square 1:1 image. Single asset alone, three-quarter view from slightly above. Show the whole asset completely with generous margins. Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background. Modeling concept render, not a scene.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines or dimension lines anywhere. No people, logos or watermarks. No extra objects, water or landscape.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Asset type: low-poly mesh MODELING DESIGN SHEET, orthographic three-view plate.
Input image: hero.png is the definitive design reference. Depict exactly this same Paper Lily Lantern assembly, preserving the exact number, shape, arrangement and layering of the blush outer lotus petals, pearl inner petals, gold-rimmed faceted warm lamp core, and three mint notched polygonal lily pads (one large main pad, two smaller side pads). Preserve the folded facets, paper thickness, gold edging, colours and all details. Do not redesign it.
Output landscape 3:2. Background uniform flat light grey #E6E6E6, absolutely no gradient, no floor and no cast shadows on the background.
Exactly three equal vertical thirds with no drawn separators. LEFT third: true orthographic FRONT view at zero elevation, facing the front notch of the main pad. MIDDLE third: true orthographic RIGHT SIDE view at zero elevation, camera rotated exactly 90 degrees around the same asset. RIGHT third: true orthographic TOP view, straight down from directly above. Absolutely no perspective or isometric camera in any view. Front and side must not show elevated top surfaces through camera tilt. Top view must show the lotus concentrically from above, with no front elevation.
All three projections use identical pixels per metre. Overall dimensions of the complete assembly W:D:H = 1.2:1.2:0.8 metres. Front silhouette bounding width:height = 3:2; right-side silhouette bounding width:height = 3:2; top silhouette bounding width:depth = 1:1. Front and side stand on exactly the same baseline and have exactly equal height; top view width equals front view width and top depth equals side view width. Arrange the front and side vertically centred on the same horizontal line; centre the top view in its third. Each projection fully contained in its own equal-width third, with generous clear margin, nothing crosses into another third. Choose one shared scale small enough to fit all three.
Matte sculpted low-poly papercraft, broad planar flat-shaded facets, soft bevels, slight paper grain and visible fold lines, restrained gold foil. Blush #FFC7DA, pearl #F3F1EA, mint #BDEBD8, lamp #FFC968. Subtle neutral ambient lighting and restrained lamp emission that do not obscure the contours or cast any background shadows. Crisp buildable geometry.
Hard rules: exactly three views of one identical asset; NO text, letters, numbers, labels, arrows, grid lines or dimension lines anywhere. No people, logos, watermarks, extra objects, water, scene or landscape.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Asset type: low-poly mesh MODELING DESIGN SHEET, detail callout plate.
Input image: hero.png is the definitive Paper Lily Lantern design reference. Extract its actual components without redesigning them. Match the identical shapes, folded facets, construction, colours, paper edge thickness, gold-foil edging and lamp details.
Output landscape 3:2 DETAIL CALLOUT PLATE on uniform flat light grey #E6E6E6, no gradient, no floor, no cast background shadows. Exactly TWO equal-width columns, unmarked, with the two separate parts arranged in ONE horizontal row left to right. Each component is centred in its own equal column and fully visible with generous margins; nothing crosses the middle.
LEFT COLUMN: the complete lotus flower lantern alone, removed from the lily-pad base, shown enlarged in a clear three-quarter view from slightly above. Preserve both rings of broad pointed folded petals: blush exterior, pearl interior, thin gold edges, and the same central warm faceted lantern body with its polygonal gold rim. Show its actual buildable petal layering and clean base attachment area. No lily pad in this column.
RIGHT COLUMN: one detached main lily pad, exactly the large mint polygonal notched lily pad from the hero, alone in a clear three-quarter view from above, exposing its radial triangular fold facets, wedge-shaped notch, thin gold perimeter and paper thickness along the side. No lotus flower or smaller pads in this column.
These are separate close-up components from the same overall assembly with real-world overall W:D:H = 1.2:1.2:0.8 metres. Display the two pieces at useful comparable close-up scales while preserving their actual geometry and proportions. The lantern's petals must remain buildable broad planar polygon meshes with crisp fold ridges, small soft bevels, no impossible curves or wispy edges.
Style: approved sculpted low-poly papercraft world, matte paper with slight grain, flat-shaded facets, pastel colours and restrained gold foil. Palette blush #FFC7DA, pearl #F3F1EA, mint #BDEBD8, lamp #FFC968. Soft neutral studio illumination; warm restrained lamp glow does not obscure the mesh.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines or dimension lines anywhere. No people, logos or watermarks. Exactly the two requested parts, no duplicated views, no extra objects, water, landscape or scene.
```

