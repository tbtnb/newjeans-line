# Exact image generation prompts

## hero.png

Reference image: ./style-ref.jpg

```text
Use case: stylized-concept.
Create ONE square 1:1 MODELING DESIGN SHEET hero image for a low-poly game asset: Giant Storybook Cover for the fan-made Dancing Line style level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE REFERENCE ONLY. Match its sculpted low-poly papercraft, flat-shaded facets, softly beveled edges, matte paper, slight paper thickness and visible fold lines, restrained gold-foil accents and pastel colours. Do not reproduce its scene.
Subject: one giant hardback storybook lying horizontally, partially open in a very shallow ajar pose. Exact overall bounding-box proportions WIDTH:DEPTH:HEIGHT = 14:10:1.5, including the raised cover and emblem. Width is the long horizontal cover dimension, depth the shorter cover dimension, height the entire low profile. The low total height is essential: no steeply raised cover, no upright book. A shallow angular cream page block is visible beneath the slightly lifted mint upper cover; lower mint cover rests flat. Long spine runs along the left depth edge. Use a simple low-poly spine with three broad raised bands. Thick pastel mint hard covers, subtle bevels, four simple folded gold corner protectors, cream page block edges rendered as a few clean stacked paper layers with shallow edge grooves. Upper cover has one central raised emblem: a pearl bunny head silhouette with two long polygonal ears and no facial features, joined to a small gold heart immediately below its head. Build the emblem from shallow, clean extruded polygons. No other decorative motifs.
Palette: mint #BDEBD8, pearl #F3F1EA, pale gold #F7D98B, cream #FFF3DE, deeper gold foil #E9B949.
Composition: single asset alone, three-quarter view from slightly above showing the upper cover, fore-edge and spine, fully visible with generous margins. Clean, buildable real low-poly geometry; a modeller must be able to distinguish covers, page block, corner protectors, emblem and spine bands. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No scenery, props, floating decorations or glowing effects.
```

## views.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the exact giant storybook shown in the reference hero.png. Input image hero.png is the definitive OBJECT DESIGN reference. Preserve its mint beveled hard covers, shallow ajar pose, cream stacked page block with fine horizontal grooves, faceted pearl bunny-head emblem with two pointed ears and no face, small faceted gold heart directly under the head, recessed inset cover border, folded gold corner protectors, and broad faceted mint spine with FOUR gold wraparound bands. Match all visible design details and materials; do not redesign.
Exact overall real proportions WIDTH:DEPTH:HEIGHT = 14:10:1.5. The height is the entire asset including the slightly lifted cover and raised emblem. Make it a very low, wide, horizontal object. Retain the shallow opening within that height.
Plate layout is exactly three equal vertical thirds with no visible dividing lines. LEFT THIRD: true orthographic FRONT elevation looking horizontally toward the long fore-edge opposite the spine, showing width 14 and total height 1.5. MIDDLE THIRD: true orthographic RIGHT SIDE elevation looking horizontally at the short right edge, showing depth 10 and total height 1.5. RIGHT THIRD: true orthographic TOP plan looking straight down, showing width 14 and depth 10, long width horizontal, spine on left, bunny ears toward the top. These are three projections of ONE identical model. No perspective, no isometric projection, no oblique camera, no visible upper cover surface in the front or side elevations except physically visible raised-edge silhouettes.
Use exactly the SAME world-to-pixel scale in all three projections: front width = top width; side width = top depth; front height = side height. For a 1536 by 1024 composition use approximately 28 pixels per metre: front and top width 392 px, side width and top depth 280 px, front and side total height 42 px. Centre each projection horizontally within its own 512 px-wide third. Front and side stand on a shared invisible baseline around y=652 px; centre top plan vertically around y=512 px. Keep generous blank margins. No object or detail crosses into a neighbouring third. Do not enlarge the thin elevations to fill the available height.
Uniform flat light grey #E6E6E6 background everywhere, no gradient, no floor, NO cast shadows on background, no contact shadows, no ambient ground plane. Soft neutral studio shading only on the objects to reveal facets and construction.
Style: sculpted low-poly papercraft, flat-shaded polygon facets, soft bevels, matte paper with slight thickness and fold lines, restrained gold-foil accents, clean buildable real low-poly geometry. Colours mint #BDEBD8, pearl #F3F1EA, gold #F7D98B, cream #FFF3DE, foil #E9B949.
Hard constraints: exactly THREE views only. NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No extra detail panels or decorative props.
```

## parts.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT MODELING PLATE for the giant storybook in the reference hero.png. Input image hero.png is the definitive OBJECT DESIGN reference. Preserve its exact design, colours, faceted geometry and materials. Show precisely FOUR isolated key parts as clean close-up modelling studies, separated in ONE horizontal row, left to right in this exact order. Each part is centred within its own equal-width column; no column outlines, no separators, no visible grid. Keep every part wholly inside its column with clear blank margins. These are enlarged construction details, not four whole books.
LEFTMOST column: the embossed bunny-heart emblem alone, detached from the cover. Match the reference's pearl faceted oval bunny head, two long pointed polygonal ears extending upward, no facial features, and small faceted gold heart attached immediately below the head. Show the raised emblem in a slightly tilted near-front three-quarter view so its shallow extruded paper thickness and beveled perimeter are clear. No cover behind it.
SECOND column: ONE gold corner protector alone, detached from the book. Match the reference's folded triangular gold cap, angular facets, bevels and short return lips wrapping over the cover thickness. Three-quarter close-up clearly showing the fold and buildable thickness. No extra corner protectors.
THIRD column: ONE isolated short section of the cream page block edge. Match the reference's broad cream paper slab with several simple stacked horizontal paper layers and fine parallel recessed grooves; show its top surface and exposed long edge in three-quarter close-up. Use clean low-poly beveled layers, readable thickness and no tiny individual paper sheets. No cover attached.
RIGHTMOST column: ONE detached mint spine section in full length with FOUR gold wraparound raised bands, matching the reference hero's broad rounded-polygon spine, beveled faceted ends and four evenly spaced gold straps. Orient the long spine upright within its column; three-quarter close-up shows its thickness and the straps wrapping around the faceted mint body. No whole book, no cover attached.
All four parts share a coherent physical design for the same low horizontal giant storybook whose overall assembled WIDTH:DEPTH:HEIGHT is 14:10:1.5. Parts may be enlarged independently for legibility, but do not alter their shapes or construction. Arrange their visual centres on one shared horizontal centreline, a single row only.
Style: sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper with subtle paper thickness and fold lines, restrained gold-foil accents; clean buildable real low-poly geometry. Palette mint #BDEBD8, pearl #F3F1EA, gold #F7D98B, cream #FFF3DE, foil #E9B949.
Uniform perfectly flat light grey #E6E6E6 background, no gradient, no floor, no cast shadows on background, no contact shadows. Soft neutral illumination and shading on the parts themselves only.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Exactly four separated part studies in one row, no extra objects, no repeated views, no inset panels.
```

