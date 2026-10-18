# Exact image generation prompts

Generated using the built-in image_gen tool, one call per row in spec.tsv order. All calls used transparent_background=false.

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero render of a single Confetti Cannon asset for the fan-made rhythm game level Bunny Pop-up Storybook.
The supplied style-ref.jpg is a STYLE REFERENCE only: match its sculpted low-poly papercraft world, flat shaded polygon facets, soft narrow bevels, matte paper, visible paper thickness and restrained fold seams, pastel colours and warm gold-foil edge accents. Do not reproduce its environment.
Subject: a paper confetti cannon shaped like a rolled book-page barrel on a little wheeled base with a bow, bursting heart and five-point star paper confetti. Overall modeled assembly bounding-box proportions exactly W:D:H = 3:2:2.5, including the fixed confetti burst. Use cream #FFF3DE, pink #FF6FAE, gold #F7D98B, lavender #B9A6F0 and magenta #FF4FA0.
Make it clean and buildable as real low-poly geometry. Define front as the bow-facing broad side of the carriage, width left-to-right; depth front-to-back. A compact lavender beveled paper carriage on four simple low-sided wheels with gold hubs. One pink folded-paper bow fixed at centre front. One hollow cream polygonal rolled-page barrel with a clear curled paper overlap seam, modest gold rim bands, supported by two simple lavender side cradles; barrel points upward and toward the front. The page surface is blank. Confetti is a small readable burst of separate thick paper hearts and five-point stars, pink and magenta hearts, gold and lavender stars, with simple centre folds. Keep burst close to muzzle and compact within the specified overall proportions. No smoke, no ribbons, no particles or light effects. Separate paper meshes, no visual tangles.
Composition: the single complete asset alone, three-quarter view from slightly above showing front and right side, entirely visible with generous margins. Soft studio light, gentle contact shadow only, plain soft pale-cream gradient background. Crisp silhouette, modeling clarity rather than elaborate illustration.
Hard rules: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, or watermarks anywhere. No book base, scenery, extra props or border.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create a landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the EXACT SAME Confetti Cannon model in the supplied hero.png design reference. This is a technical turnaround for building low-poly geometry.
Reference role: hero.png locks the object design, colours, construction and individual details. Preserve its cream hollow faceted rolled-book-page barrel, curled overlap on its right flank, two gold barrel bands, lavender rear cap, two lavender angular trunnion supports with gold faceted pivot caps, lavender gold-edged rectangular carriage, four low-sided lavender wheels with cream faces and gold hubs, front pink gold-edged folded bow with faceted gold knot and two tails, and the same compact burst of thick folded pink/magenta hearts and gold/lavender five-point stars. Blank paper, no writing. Sculpted low-poly papercraft, flat facets, soft narrow bevels, paper thickness and fold seams, matte paper and modest gold foil. Palette cream #FFF3DE, pink #FF6FAE, gold #F7D98B, lavender #B9A6F0, magenta #FF4FA0.
Use exactly three equal invisible vertical thirds of the canvas, generous outer and inter-view margins. LEFT THIRD: true orthographic FRONT view looking directly toward the bow-facing broad front of the carriage, centered and symmetrical carriage, see the barrel muzzle above the bow. MIDDLE THIRD: true orthographic RIGHT SIDE view, see the barrel profile rising toward the front (front points left in this side view). RIGHT THIRD: true orthographic TOP view, camera straight down, front of carriage toward bottom of plate. Exactly one complete asset in each third, including identical confetti positions projected from the same 3D assembly. NO perspective or isometric views, NO three-quarter angles, NO underside view. Parallel projection, no foreshortening from perspective.
Geometric scale is crucial: overall W:D:H = 3:2:2.5 including the confetti burst. Use identical pixels per model unit in all three views. Suggested overall projected bounds: front width 360 and height 300; side width 240 and height 300; top width 360 and depth 240, adjusted together if canvas is larger. Front and side share the exact same baseline and top height. Top width equals front width; top depth equals side width. Center each view within its own equal third; keep all parts wholly inside its third.
Background is uniform flat light grey #E6E6E6, all the way to every edge. No floor, horizon, gradients, cast shadows, ambient shadow patches or scenery. Neutral diffuse material illumination only, use facets to explain geometry.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, panel borders, dimension lines, people, logos or watermarks anywhere. Only the three views, with empty space separating them.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create a landscape 3:2 DETAIL CALLOUT MODELING PLATE for the Confetti Cannon in the supplied hero.png. The hero.png is the exact design and material reference. Show its key parts separately, as clean buildable low-poly mesh studies, in ONE SINGLE HORIZONTAL ROW from left to right. Exactly FOUR equal invisible columns, each part group centered in its own column with wide margins; nothing crosses between columns. No assembled full cannon and no second row.
LEFTMOST COLUMN: only the detached rolled-page barrel, three-quarter view from slightly above, matching hero.png: hollow cream low-sided polygonal cylinder with substantial paper edge thickness and warm cream interior, wide faceted open muzzle, narrow gold foil band around the muzzle and another near the closed lavender rear cap, visible sculpted curled-paper overlap on its right flank. Blank unprinted page. No carriage, bow or flying confetti in this column.
SECOND COLUMN: only the detached lavender wheeled carriage INCLUDING its pink bow, three-quarter view from slightly above, matching hero.png: gold-edged low-poly rectangular lavender base, exactly FOUR wheels total with lavender polygonal tyres, cream faces, gold bevel rings and faceted gold hubs; two angular lavender upright barrel cradles with gold faceted pivot caps; front pink folded bow with gold edge trim, gold faceted centre knot and two pink tails. Empty space between the cradles, no barrel. Keep the entire wheeled-base-and-bow group within this column.
THIRD COLUMN: one representative separate pink heart confetti piece matching the large folded hearts in hero.png, enlarged close-up in three-quarter view so its thickness and faceted centre fold are readable. Simple extruded paper heart silhouette with flat pink and magenta facets and narrow paper edges, no ornament, no stand.
RIGHTMOST COLUMN: one representative separate GOLD FIVE-POINT STAR confetti piece matching the large gold star in hero.png, enlarged close-up in three-quarter view so its paper thickness and raised radial folded facets are readable. Exactly five points, clean extruded silhouette, simple buildable geometry, no ornament, no stand.
All four groups centered along the same horizontal midline. The first two assembly parts may occupy about three quarters of their column width; enlarge the heart and star to roughly half to two thirds of their column width for useful close-up modeling detail. All parts entirely visible, generous top and bottom empty margins.
Style matches hero.png and the approved storybook world: sculpted low-poly papercraft, flat-shaded facets with soft narrow bevels, matte paper with slight thickness and fold lines, gold-foil accents; palette cream #FFF3DE, pink #FF6FAE, gold #F7D98B, lavender #B9A6F0, magenta #FF4FA0. Clean studio material shading. Plain uniform FLAT light grey #E6E6E6 background with no floor, gradient, horizon or cast shadows.
Hard rules: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, panel borders, people, logos, or watermarks. Do not add extra parts or duplicate items.
```

