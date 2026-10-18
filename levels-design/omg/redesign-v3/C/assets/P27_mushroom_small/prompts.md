# Exact image generation prompts

Generated using the built-in image_gen tool, one call per row in spec.tsv order.

## hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image for the low-poly game asset P27_mushroom_small, "Paper Mushroom Cluster", for the fan-made Dancing Line style rhythm level Bunny Pop-up Storybook.
Input image: style-ref.jpg is the approved world art-style reference ONLY. Match its sculpted low-poly papercraft, flat-shaded polygon facets, soft bevels, matte paper, slight paper thickness, visible fold seams, and restrained gold-foil edging. Do not reproduce its scene.
Subject: ONE isolated cluster of exactly THREE small paper mushrooms of three different heights. Overall physical bounding dimensions width 1 m, depth 1 m, height 0.8 m; exact W:D:H = 1:1:0.8, measured across the mushrooms themselves. Arrange the three mushrooms as a triangular group: tallest coral cap at the back, medium deep teal cap at front left, smallest coral cap at front right. All have cream stems. Keep all three caps and stems readable and geometrically distinct. Broad umbrella caps made from a small number of planar radial facets, shallow polygonal dome crowns, thick paper rims, simple cream faceted stems with subtle folded seams. Sparse cream polygon paper spots on caps; very fine gold-foil rim accents. All ornament is simple buildable geometry or flat material patches, no excessive microdetail. Palette: coral #FF7A6B, teal #173A4A, cream #FFF3DE, tiny gold accents. Compact charming pastel storybook prop with clean sensible mesh construction.
Composition: single asset alone, three-quarter view from slightly above, centered and completely visible with ample margins. Square 1:1 canvas. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. No plinth, base board, terrain, vegetation or other props.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No scenery. No smooth high-poly organic surfaces.
```

## views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the Paper Mushroom Cluster shown in the input hero.png. Input image is the definitive design reference. Preserve exactly the same three mushrooms, shapes, relative heights, arrangement, coral and teal cap colours, cream faceted stems, cream polygon raised spots, gold rim bands, fold seams, polygon topology language and paper materials. No redesign.
Overall model bounding dimensions are width 1 m, depth 1 m, height 0.8 m; W:D:H = 1:1:0.8. Three mushrooms form a triangular group: tall coral in back, medium teal front left, small coral front right. Preserve the hero's relative mushroom sizes and physical construction.
Canvas: landscape 3:2, uniform flat light grey #E6E6E6 background. Exactly three equal invisible vertical thirds, each containing ONE view of the complete cluster, centered with generous margin. LEFT third: true orthographic FRONT elevation, looking horizontally, no top-down tilt. MIDDLE third: true orthographic RIGHT SIDE elevation, looking horizontally from the model's right, no tilt. RIGHT third: true orthographic TOP plan, looking straight down vertically. No perspective, no isometric views. The front-view direction is the hero-facing side so medium teal appears left and small coral right; tall coral remains behind.
Use precisely identical physical scale in all three views. Front and side share the same baseline and same overall height. Because W equals D, front width equals side width equals top width equals top depth; each elevation height is 80 percent of its width. For layout, each model width should occupy about 26 percent of the full canvas width with clear gaps between thirds; the top silhouette occupies an equally wide square. Each view stays entirely within its own third, no crossing between columns.
Clean readable flat-shaded low-poly papercraft geometry, soft bevels, subtle matte paper texture, consistent neutral illumination that describes facets. No cast shadows on background, no floor, no horizon, no ambient-occlusion puddles. The background is completely uniform.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, borders, dimension lines, people, logos, watermarks or extra objects anywhere. Exactly three views, no inset panels.
```

## parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE for the Paper Mushroom Cluster in the input hero.png. This hero image is the definitive design reference: preserve identical construction, material colours, facet shapes, gold rim bands, cream raised polygon spots and paper fold seams. Asset bounding proportions W:D:H = 1:1:0.8.
Show exactly TWO separated key parts in ONE horizontal row, in this left-to-right order: cap, stem. Two equal invisible columns, each part centered within its own half with generous blank margins, nothing crosses the central boundary. Use only the tallest coral mushroom from the hero as the representative construction; no full cluster and no extra variants.
LEFT half: the detached coral umbrella CAP alone, three-quarter view from slightly above, showing its small polygonal crown, low-poly radial faceted dome, cream raised polygon spots in the reference pattern, narrow continuous gold-foil edge band, thin folded paper rim and a small readable glimpse of cream underside at the nearest rim. Exactly the reference cap, complete silhouette. No stem below it.
RIGHT half: the detached cream STEM alone, three-quarter view, matching the tall mushroom's tapered low-poly stem with slightly wider polygon foot, broad flat facets, soft minimal bevels, subtle paper fold seams, flat top attachment surface and closed polygon bottom. No cap above it. Preserve the stem's characteristic silhouette and material from hero.png.
Both parts shown at the same coherent physical magnification relative to each other, vertically centered in the same single row; the cap is naturally wider than the stem. These are clean buildable low-poly mesh parts, not diagrams with marks. Sculpted papercraft, matte cream paper and coral paper, restrained foil, soft flat shading, neutral studio illumination.
Background perfectly uniform flat light grey #E6E6E6. No floor, no horizon, no cast shadows on the background.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, borders, dimension lines, people, logos or watermarks anywhere. Exactly two separate pieces only: cap on left, stem on right. No additional insets or objects.
```

