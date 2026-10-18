# Exact image generation prompts

Built-in image_gen; one call per row in spec.tsv order. All calls used transparent_background=false.

## hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create a square 1:1 MODELING DESIGN SHEET hero render of ONE isolated low-poly game asset: a rectangular Tulip Bed with Fence for the pastel pop-up storybook rhythm-game world.
Input image: the supplied style-ref.jpg is an approved STYLE reference only. Match its sculpted low-poly papercraft aesthetic, planar flat-shaded facets, softly bevelled edges, matte thick paper, visible subtle folds and restrained gold-foil edging. Do not reproduce its scene.
Subject: a clean, buildable rectangular shallow soil tray enclosed on all four sides by a short white pointed picket fence, holding orderly yellow, coral and white paper tulips with green stems and folded green leaves. Use simple repeated mesh components and coherent physical joins. Tulip cups are closed, angular folded-paper cups with distinct pointed petals, not daisies. Leave visible space between flowers. All geometry has real thickness.
Exact overall bounding proportions width:depth:height = 3:1.5:0.8 (3 m wide, 1.5 m deep, tallest flower 0.8 m). Long rectangular bed, twice as wide as deep, low overall silhouette. Fence about 0.4 m high, tray about 0.10 m high. Plant twelve tulips in two straight rows of six, alternating sun yellow, coral and white; flowers fit completely within the footprint. White fence with repeated pointed pickets and two horizontal rails; thin restrained gold-foil trim on the tray lip. Soil is a single simple flat muted warm-brown paper inset, without granular texture or stones.
Palette: sun #FFD23F, coral #FF7A6B, white #FFFFFF, green #6CCB5F, rendered as softly lit pastel matte paper while retaining the palette identity. Gold foil accents only on the narrow tray trim.
Composition: single complete asset alone, three-quarter view from slightly above, see the front long side and the right short side and the flower arrangement. Show the entire asset with generous clean margins. Plain soft pale-cream gradient studio background, soft studio light and gentle contact shadow. Crisp readable mesh shapes and component boundaries, attractive but practical for a low-poly modeller.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, extra props, sparkles, depth-of-field blur, or painterly imprecision.
```

## views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create a landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the exact Tulip Bed with Fence in the supplied hero.png reference. The reference is the authoritative object design: reproduce its twelve folded faceted paper tulips, their arrangement and yellow/coral/white colour placement, green stems and pointed folded leaves, short white pointed pickets, two horizontal white rails, four square corner posts with gold pyramid caps, shallow cream rectangular tray, narrow gold tray rim and flat brown soil. Preserve the reference's sculpted low-poly thick-paper construction, flat-shaded bevelled facets and subtle paper folds. Do not redesign any component.
Overall physical bounding box width:depth:height = 3:1.5:0.8 exactly. The long front width is 3 m, right-side depth 1.5 m, complete height 0.8 m.
Composition is exactly THREE equal vertical thirds with no visible dividers. LEFT third: true orthographic FRONT elevation looking straight at the long side, with no top or side faces visible. MIDDLE third: true orthographic RIGHT SIDE elevation looking straight at the short right end, no top or front faces visible. RIGHT third: true orthographic TOP plan looking vertically straight down, no perspective or vertical side faces.
All three projections use precisely the SAME pixels-per-metre scale. The front and side elevations have the SAME height and sit on the SAME invisible baseline. Front width is twice side width. Top-view width equals front-view width, top-view depth equals side-view width. For layout guidance only, each third's width is one unit; use an object front width of 0.82 unit, side width 0.41 unit, elevation height 0.219 unit, top footprint 0.82 by 0.41 unit. Centre every view in its own third with ample margins; nothing crosses a third boundary. Do not enlarge the side view to fill its column. Parallel projection only, zero perspective, zero isometric or three-quarter angle.
Background is perfectly uniform flat light grey #E6E6E6 throughout. No floor, horizon, ground plane, cast shadows, drop shadows or ambient shadow halo on background. Use neutral soft even studio illumination on object surfaces to read facets. Full component geometry remains crisp and buildable.
Palette matched to reference: sun #FFD23F, coral #FF7A6B, white #FFFFFF, green #6CCB5F, cream tray, muted warm-brown soil and restrained gold foil.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, decorations outside the object, or extra views. Exactly three views, front / right side / top from left to right.
```

## parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create a landscape 3:2 DETAIL CALLOUT MODELING PLATE for the exact Tulip Bed with Fence in supplied hero.png. Use hero.png as the authoritative design and material reference. Present exactly THREE key parts separately, in ONE horizontal row from left to right, each centred in its own equal-width invisible column, ample margins and no overlap:
LEFT column: one complete sun-yellow paper tulip, including the same angular pointed petal cup, green straight stem and two long pointed folded green leaves as the hero. A close-up three-quarter view showing the cup's polygonal construction, paper edge thickness, petal folds and simple buildable joints.
MIDDLE column: one representative white picket-fence module taken from the hero, a short straight section with three pointed white pickets connected by two horizontal rails and a single square corner post on its right end with the identical gold-foil pyramid cap. Show alone in a clean slightly elevated three-quarter view, preserving the hero's bevels, fence proportions and component construction.
RIGHT column: the complete empty rectangular soil tray taken from the hero, all flowers and fencing removed to expose its construction. Cream shallow rectangular walls, narrow gold-foil rim, flat muted warm-brown soil insert. The tray footprint is width:depth = 2:1, matching the 3 m by 1.5 m bed. Show alone from an elevated three-quarter view so both the brown inset surface and shallow sidewalls are legible.
Each column contains only its specified component. All three are centred at the same row's vertical midpoint. The component close-up magnifications can differ so each fits its own equal column. No additional inset views, duplicates, complete flower-bed assembly or stray pieces. The overall assembled asset has W:D:H = 3:1.5:0.8; these are its exact matching components, not redesigns.
Style: clean sculpted low-poly papercraft game geometry, planar flat-shaded facets with small soft bevels, matte thick paper and subtle fold lines, restrained gold-foil accents. Simple low-poly meshes that a modeller can build; crisp silhouettes and coherent joins. Colours exactly consistent with hero: sun #FFD23F, white #FFFFFF, green #6CCB5F, cream, brown and gold.
Background: perfectly flat uniform light grey #E6E6E6, no floor or horizon, no cast shadows or background shadow halos. Soft even neutral studio illumination on component surfaces.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, borders, people, logos, watermarks, scenery, extra props or decorative effects. Exactly one row with paper tulip, picket fence, soil tray in that left-to-right order.
```

