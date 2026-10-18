# Exact image generation prompts

Built-in image_gen; one call per image, in spec.tsv row order.

## kit.png

Reference: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create a square 1:1 MODELING DESIGN SHEET for a modeller building real low-poly game meshes for the fan-made Dancing Line style level Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is a STYLE REFERENCE only. Match its sculpted low-poly papercraft, flat-shaded facets with soft bevels, pastel paper and restrained gold-foil accents. Do not reproduce its scene.
Show exactly EIGHT separate small ground-plant assets in a strict invisible 4 columns by 2 rows grid. Reading order left to right then top to bottom:
Top row: (1) paper grass tuft, approximately 0.4 m high, a compact fan of folded pointed mint and teal blades; (2) five-petal paper flower, approximately 0.3 m high, exactly five pale pink folded petals, small faceted gold center, mint stem and two leaves; (3) single tulip, approximately 0.4 m high, coral-pink faceted folded cup on a mint stem with two pointed leaves; (4) heart flower, approximately 0.35 m high, a single pink folded heart-shaped flower with a thin gold-foil rim on a mint stem with two leaves.
Bottom row: (5) tiny mushroom, approximately 0.3 m high, low-poly coral-pink umbrella cap with a few cream polygon paper spots, cream stalk; (6) clover patch, approximately 0.4 m across, a compact group of mint and teal trifoliate clovers with heart-shaped folded leaflets; (7) reed tuft, approximately 0.8 m high, slender teal folded reeds with three simple cream-and-gold seed heads and pointed mint leaves; (8) fern, approximately 0.6 m high, mint and teal folded fronds with paired angular leaflets and a few softly lavender tips.
All eight assets must share one consistent world scale, so the reeds are twice the height of the grass and tulip, and the short flower is visibly much smaller. No enlarging small items to fill cells. Each entire item centered in its own equal cell with generous blank margins; nothing overlaps or crosses into another cell. Entire sheet has generous outer margins. Each asset viewed from the same three-quarter camera slightly above, front faces toward the viewer, bases down. Consistent soft studio lighting and subtle local contact shadows only.
Plain soft pale-cream background. Clean buildable geometry: low polygon count, visibly folded planes, slight paper thickness, softly beveled edges, matte paper surfaces, simple attached stems and leaves, restrained gold foil. No painterly fuzz, no dense botanical detail, no added decorative props, no pots, no scenery, no platforms or separate display bases.
HARD RULES: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Only the eight requested assets.
```

## front.png

Reference: `./kit.png`

```text
Use case: stylized-concept.
Create a square 1:1 MODELING DESIGN SHEET: orthographic FRONT views of the exact eight low-poly papercraft assets in the provided kit.png reference image.
Input image: kit.png is the definitive DESIGN AND LAYOUT reference. Preserve every asset's identity, shape, number of petals and leaves, folds, faceted structure, colors, gold details, and proportions. Change the camera and background only.
Exactly the same invisible 4 columns by 2 rows grid and reading order as the reference. Top row: paper grass tuft (approximately 0.4 m high), five-petal paper flower (approximately 0.3 m high), single tulip (approximately 0.4 m high), heart flower (approximately 0.35 m high). Bottom row: tiny mushroom (approximately 0.3 m high), clover patch (approximately 0.4 m across), reed tuft (approximately 0.8 m high), fern (approximately 0.6 m high).
Each item is a true orthographic FRONT elevation, camera level and horizontally facing the asset, looking along its front-to-back axis. No perspective, no isometric angle, no camera tilt, no looking down. Vertical stems remain vertical. Show the exact front silhouette and geometry that a modeller would build from the reference; do not invent a new arrangement or simplify away details.
Use the SAME world scale for all eight items, matching their relative sizes in kit.png. Reeds twice as tall as grass and tulip; do not enlarge small items. Each asset centered horizontally within its own equal cell with generous margin, bases on a common baseline within each row. Nothing crosses a cell boundary. All items completely visible.
Plain perfectly flat solid light grey #E6E6E6 background, no floor, no horizon, no cast shadows, no contact shadows, no background gradients, no ambient shadow halos. Gentle neutral object lighting can reveal the existing flat-shaded facets, slight paper thickness, soft bevels, matte paper and gold-foil material.
HARD RULES: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Only the same eight assets from the reference, each seen straight from the front.
```

## top.png

Reference: `./kit.png`

```text
Use case: stylized-concept.
Create a square 1:1 MODELING DESIGN SHEET: orthographic TOP views of the exact eight low-poly papercraft assets in the provided kit.png reference image.
Input image: kit.png is the definitive DESIGN AND LAYOUT reference. Preserve every asset's identity, shape, number of petals and leaves, folds, faceted structure, colors, gold details, and proportions. Change the camera and background only.
Exactly the same invisible 4 columns by 2 rows grid and reading order as the reference. Top row: paper grass tuft (approximately 0.4 m high), five-petal paper flower (approximately 0.3 m high), single tulip (approximately 0.4 m high), heart flower (approximately 0.35 m high). Bottom row: tiny mushroom (approximately 0.3 m high), clover patch (approximately 0.4 m across), reed tuft (approximately 0.8 m high), fern (approximately 0.6 m high).
Each item is a true orthographic TOP plan view, camera exactly vertically above looking straight down along the vertical stem axis, without perspective, without tilt, without an isometric angle. The camera-facing fronts from the kit correspond to the bottom edge of each cell. Show the actual horizontal footprint and correct foreshortening: vertical stems and upright flowers must be viewed end-on or edge-on where physically appropriate, not tipped forward to expose a front elevation. Mushroom cap is seen from directly above and occludes its stalk; folded grass, clover and fern reveal their authentic radial or spreading footprints. This is technical modeling reference, not a set of attractive front-facing icons.
Use the SAME world scale for all eight items, matching their relative dimensions in kit.png; no independent resizing to fill cells. Each item's actual projected footprint centered in its own equal cell, with generous margin. Nothing crosses a cell boundary. All items completely visible.
Plain perfectly flat solid light grey #E6E6E6 background, no floor, no horizon, no cast shadows, no contact shadows, no background gradients, no ambient shadow halos. Gentle neutral object lighting can reveal the existing flat-shaded facets, slight paper thickness, soft bevels, matte paper and gold-foil material.
HARD RULES: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Only the same eight assets from the reference, each seen straight down from above.
```

