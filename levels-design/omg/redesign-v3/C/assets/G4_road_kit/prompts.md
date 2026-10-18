# Exact image generation prompts

## 1. kit.png

Reference: ./style-ref.jpg (style only)

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET for G4_road_kit, seven small modular road and bridge assets for the fan-made Dancing Line style rhythm-game level Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is the approved world STYLE REFERENCE ONLY. Match its sculpted low-poly papercraft, flat-shaded facets, soft tiny bevels, matte pastel paper, slight paper thickness and fold lines, and restrained warm gold-foil edges. Show clean buildable real low-poly geometry, not an environment illustration.
Composition: exactly four equal columns by two equal rows, an invisible grid, reading left to right across the upper row then lower row. Exactly SEVEN separated items; lower-right eighth cell completely EMPTY. Each asset wholly inside its own cell with generous margins. All items shown from the SAME three-quarter camera slightly above, same orientation and consistent world scale. Soft studio illumination and very gentle contact shading on a plain soft pale-cream background. No scenery, bases, pedestals, or extra props.
Seven cells in this exact order:
Upper-left: cream paper road straight tile, about 2.2 m long, an unmarked flat cream rectangular roadway with subtly beveled thick folded-paper sides and thin gold-foil border strips along both long edges.
Upper second: matching cream paper road CORNER tile, about 2.2 m overall, a clean 90-degree L-shaped footprint with constant road width, same thickness and gold edging along the inner and outer turning edges.
Upper third: separate gold-foil edge trim, about 2.2 m long, a slim straight gold folded-paper strip with a simple angular L cross-section, no road slab attached.
Upper-right: plank bridge tile, about 2.2 m long, a straight low bridge deck made of six broad pale peach and cream paper planks across two simple muted teal support runners; visible gaps and folded edges, no ropes or tall rails.
Lower-left: floating cardboard bridge tile, about 2.2 m long, a cream-top thick layered cardboard rectangular deck, warm tan exposed layered edge and simple folded mint underside support tabs; no ground support or hanging objects.
Lower second: page-strip road tile, about 2.2 m long, an ivory narrow rectangular layered-paper road strip with a shallow lifted fold at one short end and subtle parallel page layers visible along its side; a slim pastel pink inset strip runs lengthwise.
Lower third: carnival glowing edge, about 2.2 m long, a narrow straight pastel lavender curb strip with restrained gold trim and six evenly spaced small faceted warm ivory-gold luminous bulbs mounted along its top; buildable polygonal bulbs, no halo cloud or floating particles.
Palette: cream, mint, coral, pink, lavender, muted gold, teal and sky-blue, restrained like the reference. Make paper geometry and assembly legible. All long modules have comparable 2.2 m length at a consistent world scale.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks. No decorative stars, hearts, bunny figures, castles, flowers, books, background setting or game UI. Only the seven requested modules.
```

## 2. front.png

Reference: ./kit.png (exact designs)

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET: the true ORTHOGRAPHIC FRONT ELEVATIONS of the seven modular low-poly papercraft road assets in the supplied kit.png reference image.
Input image: kit.png is the authoritative DESIGN AND GRID REFERENCE. Preserve exactly its seven designs, geometry, relative dimensions, paper layering, bevels, fold seams, colours, materials, six alternating peach/cream bridge planks, mint-teal supports, gold edging, pink inset strip and six faceted carnival bulbs. Rotate the camera only; do not redesign.
Layout: exactly the same invisible 4 columns by 2 rows grid and reading order as the reference. Upper row: cream straight road tile; 90-degree L-shaped cream road corner tile; separate gold-foil edge trim; six-plank bridge tile. Lower row: layered floating cardboard bridge tile with mint supports; layered ivory page-strip road with pink stripe and folded short end; lavender-and-gold carnival edge with exactly six warm ivory-gold faceted bulbs; last lower-right cell EMPTY. Seven objects only. Equal columns and equal rows, each object centered in its own cell, fully contained with margins, nothing crosses cells.
Camera: TRUE ORTHOGRAPHIC FRONT views, zero perspective, zero camera yaw, zero downward tilt. For the straight modules choose the broad long-side front elevation so their approximately 2.2 m lengths run HORIZONTALLY across each cell; long edges perfectly horizontal. View at the object's height, not from above: flat horizontal road/deck top surfaces must NOT be visible. See only front-facing vertical faces and the visible frontal silhouettes of raised or folded parts. The L-corner uses the same world axes as the straight module and reads as its correct projected frontal silhouette, not a 3D L viewed obliquely. The bridge shows its correct six plank edge silhouettes above its long teal runner; the floating cardboard shows tan page layers and mint underside supports; the page-strip shows its thin layered side and upturned end; the carnival edge shows all six bulbs in a horizontal line. Preserve material colours, including pink only where actually visible from this elevation; never force hidden top designs onto front faces.
Render as clean shaded low-poly papercraft geometry with matte paper thickness, subtle folds, soft bevels, flat-shaded facets and muted gold foil, consistent with kit.png. Consistent world scale across all assets, never enlarge the narrow trim to fill its cell. Each row uses a consistent baseline for the bottoms of the objects; allow generous surrounding margin.
Background: uniform flat light grey exactly #E6E6E6, edge to edge. Neutral ambient studio illumination on the objects only. NO cast shadows on the background, NO contact shadows, NO floor, NO horizon, NO gradient.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks. No extra objects, scenery, pedestals, frames, decoration, UI or perspective.
```

## 3. top.png

Reference: ./kit.png (exact designs)

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET, a true ORTHOGRAPHIC TOP PLAN of the seven modular low-poly papercraft road assets in the supplied kit.png reference.
Input image: kit.png is the authoritative DESIGN AND GRID REFERENCE. Preserve exactly the same seven objects, silhouettes, assembly, proportions, relative scale, bevels, fold seams, layered paper, colours and materials. Only replace the camera with a perfectly straight-down orthographic camera.
Grid layout: exactly 4 equal columns by 2 equal rows, invisible grid. Seven items in reference reading order: UPPER LEFT cream straight road tile, UPPER SECOND cream 90-degree L-shaped road corner, UPPER THIRD separate gold-foil trim strip, UPPER RIGHT six-plank bridge with teal runners, LOWER LEFT floating layered cardboard bridge with mint underside supports, LOWER SECOND ivory layered page-strip road with pink lengthwise inset stripe and lifted folded end, LOWER THIRD lavender and gold carnival edge with exactly six small faceted warm ivory-gold bulbs, LOWER RIGHT EMPTY. Each wholly centered within its own equal cell, all seven visible with margins, nothing crosses cells, eighth cell completely empty.
Camera and alignment: truly orthographic TOP views, looking exactly vertically downward, no perspective, no oblique view, no horizon, no visible vertical side faces. Every long straight module runs HORIZONTALLY from left to right in its cell. All parallel edges parallel on the page, right angles remain exact right angles. Use the same consistent world scale: the approximately 2.2 m long modules have comparable horizontal lengths. Do not enlarge narrow strips to match the widths of the road decks. Corner footprint is a genuine constant-width 90-degree L, not a filled rectangle.
Detailed invariants from kit.png: straight road has cream unmarked surface and gold foil strips along BOTH long edges; L-corner has the same cream surface and gold edging along its inner and outer turning edges; independent gold trim is a narrow folded channel; bridge has exactly SIX broad alternating pale cream/peach planks arranged along its length, with narrow gaps and muted teal runners visible only where they protrude beyond the deck; floating cardboard bridge has a plain cream top, warm tan layered rim and mint underside tabs visible only if not occluded from overhead; page-strip has ivory top, slim straight pink lengthwise inset and folded short end; carnival strip has lavender top and gold edge lines with exactly SIX evenly spaced small polygonal ivory-gold bulbs seen directly from overhead, centered along its length. Do not add or remove parts.
Art style: sculpted buildable low-poly papercraft matching reference, matte paper, slight thickness, subtle fold lines, tiny soft bevels, flat-shaded faceted bulbs and muted gold foil. Clean technical asset sheet rather than scene illustration.
Background: perfectly uniform FLAT LIGHT GREY #E6E6E6 edge to edge. Neutral ambient object shading only, NO cast shadows, NO contact shadows, NO floor, NO background gradient, no glow halos.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, extra props, bases, scenery, UI or decoration. Exactly the seven referenced objects in the specified positions.
```
