# Exact image generation prompts

Generated with the built-in image_gen tool, one call per row in spec.tsv order.

## 1. hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image for a modeller building a real low-poly mesh for the fan-made Dancing Line style rhythm game level "Bunny Pop-up Storybook".
Input image: style-ref.jpg is an approved world STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded facets with soft small bevels, matte paper, slight cardstock thickness and genuine fold lines, restrained gold-foil accents and pastel colours. Do not reproduce the reference scene.
Subject: one single isolated asset P25_paper_hill, "Paper Hill Piece": a rolling low-poly paper hill piece, mint with a few tiny flowers. Real overall dimensions width 6 m, depth 3 m, height 2.5 m; maintain W:D:H = 6:3:2.5 exactly. Horizontal width is the long axis. Make one coherent gently rolling faceted hill with a broad main crest and a smaller connected shoulder, a flat bottom and simple buildable polygonal footprint. Large clean planar triangular facets, a few clearly visible actual scored fold creases; thin pearl paper edges. Tiny pearl flowers with green folded leaves attached sparingly to the slopes, flower centres may have a very small gold-foil accent. Flowers must stay tiny relative to the hill. Main palette mint #BDEBD8, green #6CCB5F, pearl #F3F1EA. No rocks, trees, book, platform, landscape or additional assets.
Composition: the single complete asset alone, three-quarter view from slightly above, show front, right side and upper slopes, comfortably centred with generous margins on all sides. Clear readable silhouette and all geometry visible, no cropping. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background.
Buildability: clean economical low-poly geometry, visible finite paper thickness, modest bevels, no painterly marks, no fuzzy grass, no dense details, no impossible folds.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

## 2. views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of P25_paper_hill, "Paper Hill Piece".
Input image: hero.png is the authoritative design and colour reference. Show the SAME hill mesh, silhouette, crest on the left and connected smaller shoulder on the right, polygonal footprint, triangular facet topology, pearl edge thickness, scored fold lines, pearl flowers, green folded leaves and tiny gold centres. Preserve their shapes and placement. Match the sculpted low-poly papercraft material: matte mint #BDEBD8, green #6CCB5F, pearl #F3F1EA, flat-shaded facets and slight bevels. Do not introduce a different hill.
Real dimensions: width 6 m along horizontal X, depth 3 m along Y, height 2.5 m along Z. Exact W:D:H = 6:3:2.5.
Layout: exactly THREE equal invisible vertical thirds. LEFT third contains FRONT view looking horizontally along the depth axis; MIDDLE third contains SIDE view seen from the RIGHT, looking horizontally along the width axis; RIGHT third contains TOP view looking vertically straight down. Each view centred in its own third with margin. Nothing crosses into another third.
Use TRUE ORTHOGRAPHIC projection in ALL views: zero perspective, no isometric view, no foreshortening. Front and right side stand on the SAME baseline, have the SAME height and use the SAME scale. Top width equals front width; top depth equals side width. In a conceptual 1536 by 1024 layout, the front fits width 432 and height 180, the right side fits width 216 and height 180, and the top fits width 432 and depth 216. Front centred at x256, right side centred at x768, top centred at x1280. Front and side baseline y610, top centred vertically around y520. These are invisible composition instructions only, never draw measurements or marks. Respect these proportional envelopes, including sparse tiny flower details.
Background: perfectly plain flat light grey #E6E6E6 throughout, no gradient, no floor, NO cast shadows or contact shadows on the background. Neutral even studio illumination on object facets only.
Hard rules: exactly three views of the same complete asset. NO text, letters, numbers, labels, arrows, grid lines, panel borders, dimension lines, people, logos or watermarks anywhere. All geometry fully visible with margins.
```

## 3. parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE for a modeller building P25_paper_hill, "Paper Hill Piece".
Input image: hero.png is the authoritative design reference. Preserve the identical design, colours, triangular facets, pearl edge thickness, paper material, fold construction, tiny pearl flowers with green folded leaves and small gold-foil centres. Sculpted low-poly papercraft, flat-shaded large planar facets with soft small bevels, matte cardstock. Main colours mint #BDEBD8, green #6CCB5F, pearl #F3F1EA.
Layout: exactly TWO separate isolated key-part displays in ONE horizontal row, left to right in the listed order, each centred within its own equal-width invisible column with generous margins and a clear gap between them. LEFT column = faceted hill. RIGHT column = fold line. No other objects or extra callouts.
LEFT: show the full identical faceted rolling hill mesh from the reference in a three-quarter view slightly from above, with its broad taller crest on the left and smaller connected shoulder to the right, the same polygonal footprint, sparse tiny flowers, scored triangular fold lines and pearl lower paper edge. Keep overall real width:depth:height proportions 6:3:2.5. Its complete silhouette must fit within the left half with margin.
RIGHT: show one enlarged close-up isolated sample of the ACTUAL fold-line construction from that same hill. A simple cropped patch of two adjacent mint triangular cardstock facets joined along one clearly visible scored V-shaped paper fold, slightly bent into the same hill angle. Show the narrow pearl-coloured paper core at the exposed cut edge, subtle paper thickness, clean low-poly planar surfaces and small bevels; the crease is actual buildable geometry, no ink stroke. This is a detached detail sample of the mint hill surface, not a different hill and not a flower study. Orient it in a readable close three-quarter view. It must fit fully in the right half with margin. No exploded shards or additional sample pieces.
Background: perfectly uniform flat light grey #E6E6E6, no gradient, no floor, no cast shadows on the background. Soft neutral studio illumination on the objects only.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos or watermarks anywhere.
```

