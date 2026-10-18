# Exact image generation prompts

Generated using the built-in image_gen tool, one call per image in spec.tsv row order. All calls used transparent_background=false.

## hero.png

Reference image: `./style-ref.jpg`.

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET image of a single buildable low-poly game asset, the Bunny Village Windmill for the fan-made Dancing Line style level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE REFERENCE ONLY. Match its sculpted low-poly papercraft, crisp flat-shaded polygon facets, soft bevels, matte paper, slight paper thickness, visible intentional fold lines, restrained gold-foil accents, pastel fairytale storybook language. Do not reproduce the scene.
Subject: one tall slender papercraft windmill with a coral-red bunny-ear roof cap, cream tower body, yellow door, exactly four paper sails on a simple front hub, and small flower boxes. Complete assembled object only. Use simple clean mesh forms a modeller can build: a tapered faceted tower, thick folded-paper roof with two upright bunny ears, four rigid folded-paper sails on wood supports, simple bevelled door and shallow flower boxes with a few polygonal flowers and green leaves. Minimal gold-foil edge trim; no ornamental clutter.
Physical overall bounding proportions, INCLUDING sails and bunny ears: width 4 metres, depth 3 metres, height 9 metres, exactly W:D:H = 4:3:9. Make the tall slim silhouette clear. The rotor fits inside the overall width, and both bunny ears and all sails remain fully visible. Palette: coral #FF7A6B, cream #FFF3DE, sun yellow #FFD23F, green #6CCB5F, wood #C99A6B, sparing gold foil.
Composition: single asset alone, three-quarter view from slightly above, show the front and its right side, fully visible with generous margins on every side. Square canvas. Plain soft pale-cream gradient background, soft neutral studio light, gentle contact shadow directly below. No environment or scenery, no plinth or separate ground slab.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, additional view panels, or inset images. Render clean real low-poly geometry, no painterly strokes, no impossible floating decorations.
```

## views.png

Reference image: `./hero.png`.

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the Bunny Village Windmill.
Input image hero.png: the sole authoritative MODEL AND MATERIAL REFERENCE. Depict exactly this same windmill, preserving its mesh design, coral bunny-ear roof cap, two long faceted cream-edged ears with coral interiors, tapered cream tower, yellow arched door and small coral awning, gold-foil trims, exactly four cream folded-paper sails in an X on wooden spars, faceted gold hub, arched yellow windows, wood flower boxes, simple cream and pink polygonal flowers and green leaves. Do not redesign, embellish, add parts, or change the sail arrangement. Low-poly papercraft with matte paper thickness, soft bevels, flat facets and fold seams.
Canvas: landscape 3:2. Uniform flat light grey #E6E6E6 background everywhere. No floor, horizon, gradient, background cast shadows, ambient-occlusion blobs, labels or drawn separators. Neutral even light that keeps facets readable.
Layout: exactly THREE invisible equal vertical thirds, each containing exactly ONE view. LEFT third: true orthographic FRONT elevation, looking straight at the sail hub and front yellow door. MIDDLE third: true orthographic RIGHT-SIDE elevation, seen from the model's right, precisely 90 degrees from front; the rotor is seen edge-on. RIGHT third: true orthographic TOP plan, looking straight vertically down, no visible vertical wall heights and no tilted camera.
Use a single common physical scale in all three views. Entire assembled object's true bounding dimensions INCLUDING rotor and bunny ears are W:D:H = 4:3:9 metres. Front and right-side share exactly the same baseline and exactly the same height. Front overall width is 4 units, side overall width is 3 units, both heights are 9 units. Top overall width matches front width EXACTLY, and top overall depth matches side width EXACTLY. Do not enlarge the top plan to fill its panel. Keep the same identity and geometry even where components occlude each other naturally.
Suggested precise visual layout on a 1536 by 1024 canvas: panel centres at horizontal positions 256, 768, 1280. Front and side baseline at vertical position 900, uppermost ear at 140, so both elevation heights are 760 pixels; front width about 338 pixels, side width about 253 pixels. Top is centred in its third at vertical position 512, width about 338 pixels and depth about 253 pixels. These measurements are COMPOSITION INSTRUCTIONS ONLY; render absolutely no measurements or lettering. All parts fully visible within their own third with comfortable margin, nothing crosses a panel boundary.
Hard exclusions: NO perspective, three-quarter views, extra views, inset details, text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks. This is a clean geometry turnaround for a low-poly modeller.
```

## parts.png

Reference image: `./hero.png`.

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE for the Bunny Village Windmill.
Input image hero.png: authoritative reference for the EXACT component designs, colours, materials, thicknesses, folds and details. Reproduce its components, not redesigned alternatives. Buildable sculpted low-poly papercraft geometry, flat-shaded facets with soft bevels, matte paper with slight thickness and fold lines, gold-foil accents. Palette coral #FF7A6B, cream #FFF3DE, sun #FFD23F, green #6CCB5F, wood #C99A6B.
Layout: ONE horizontal row only, FOUR equal invisible columns across the landscape 3:2 canvas. Each component group centred in its own column, separated by generous empty space. Every group completely contained within its column. No full windmill or extra inset views. Uniform flat light grey #E6E6E6 background, no floor, gradient, cast shadows or drawn column boundaries. Consistent neutral studio light, clear close-up three-quarter component views. Groups may be enlarged individually to show construction.
LEFTMOST column: exactly FOUR separate cream folded-paper sails with their wood spars, gold edge trims and bevelled gold corner caps, faithfully matching the four sails of hero.png. Arrange the four detached sail-and-spar units as a compact X-shaped exploded rotor group with a small empty central gap, showing their paper faces and folds. No hub in this column.
SECOND column: the complete coral faceted roof cap together with its TWO upright long bunny ears, cream outer rims, coral folded interiors, gold-foil eave band and small wood eave brackets, exactly like hero.png. Show this whole roof component detached from the tower, including its lower rim and paper thickness.
THIRD column: the yellow arched door assembly with its cream bevelled surround, small coral gabled awning with gold edging, simple gold diamond handle and small cream doorstep; and ONE matching wooden flower box with polygonal cream and pink flowers, yellow centres, green folded leaves and simple support brackets. These are two separately detached pieces within the same column, flower box above the door with clear space between; they form one grouped detail callout. Match hero.png faithfully.
RIGHTMOST column: the single faceted gold central rotor HUB with its short wooden axle and simple wooden mounting block, detached, close enough to see polygonal faces, bevels and assembly. Match hero.png, no added gears or mechanical complexity.
Preserve the shared design of a windmill with full assembled W:D:H = 4:3:9 metres; detached callouts are close-ups, not a re-proportioned new tower. Keep all four groups aligned in one row around a common horizontal centre and leave generous outer margins.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scene props or assembled full windmill. No perspective scenery or ground shadows.
```

