# Exact image generation prompts

## hero.png

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero render of a single low-poly game asset, the Heart Flower Patch for a fan-made Dancing Line style rhythm level, Bunny Pop-up Storybook.
Input image: style-ref.jpg is an ART STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded polygon facets, gentle bevels, matte paper, visible paper thickness and crisp fold creases, pastel colours and delicate gold-foil accents. Do not reproduce the scene.
Subject: one low rectangular paper planter filled with heart-shaped paper flowers in coral #FF7A6B, pink #FF6FAE and lavender #B9A6F0, on mint #BDEBD8 stems with folded mint leaves. Overall real dimensions exactly width 2.5 m, depth 1.5 m, height 0.9 m, measured from planter bottom to highest flower: W:D:H = 2.5:1.5:0.9. Width is the long front edge. Keep the whole patch broad and low. A buildable ivory paper tray with subtly clipped corners, shallow bevels, a narrow gold-foil rim, and a flat mint inset planting surface. The tray is approximately 0.22 m tall. Nine discrete heart flower heads in three staggered rows, three per row; coral, pink and lavender distributed across the rows. Flowers are simple thick heart silhouettes with one central fold and a few broad planar triangular facets, not many-petalled flowers. Straight polygonal mint stems and paired simple folded pointed leaves; varied stem heights with highest flower exactly 0.9 m above the base. All geometry must be clean, separated, plausible to model, readable and low-poly; no fuzzy vegetation or tangled overlapping details.
Composition: the single complete asset alone in a three-quarter view from slightly above, showing front, right side and planting surface. Square canvas, comfortable empty margins on every side. Soft studio light and a gentle contact shadow, plain soft pale-cream gradient background.
No text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No other props, scenery, sparkles or floating decorations.
```

## views.png

```text
Use case: stylized-concept.
Create a landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a modeller. The input hero.png is the exact design reference: show this same Heart Flower Patch model from three strictly orthographic cameras, retaining its nine coral, pink and lavender faceted thick paper heart flowers, their arrangement, mint stems and folded pointed leaves, mint faceted planting surface, and ivory low rectangular clipped-corner tray with narrow gold-foil rim and fine gold lower edge. Match the reference's exact design, colours, proportions and details. Matte paper with soft bevels, crisp central heart folds and low-poly planar facets; clean buildable geometry.
Overall real dimensions: width 2.5 m, depth 1.5 m, height 0.9 m; W:D:H exactly 2.5:1.5:0.9. Width is the long front edge of the tray. Palette: coral #FF7A6B, pink #FF6FAE, lavender #B9A6F0, mint #BDEBD8; ivory planter and gold-foil trim as in hero.png.
Canvas divided into EXACTLY THREE EQUAL VERTICAL THIRDS, with no drawn dividers. LEFT third: true FRONT elevation looking horizontally straight at the long front edge. MIDDLE third: true RIGHT SIDE elevation looking horizontally straight at the short right end. RIGHT third: true TOP plan looking vertically straight down. Zero perspective, zero isometric tilt, no visible top surfaces of horizontal tray rims in front or side elevation. Natural occlusion of the flower heads is allowed; retain all nine actual flower positions, never rearrange them to fit the views.
Use one identical pixels-per-metre scale in all three projections. For a 1536x1024 canvas, an ideal geometric footprint is front 420 pixels wide and 151 pixels tall, side 252 pixels wide and 151 pixels tall, top 420 pixels wide and 252 pixels deep. Front and side stand on exactly the same horizontal baseline, their highest point has exactly the same height. Top width equals front width; top depth equals side width. Centre each projection within its own third with generous clean margins; no view may cross its third. The top view depicts the actual narrow foreshortened edges of upright heart heads, stem locations and leaves from directly above, not upright hearts pasted on top.
Plain uniform flat light grey #E6E6E6 background. No floor or horizon, no cast shadows on background, no contact shadows; soft neutral material shading only within each object.
NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, extra objects or decorative marks anywhere. Only the three views of this exact model.
```

## parts.png

```text
Use case: stylized-concept.
Create one landscape 3:2 DETAIL CALLOUT PLATE for a low-poly modeller, using the provided hero.png as the exact design reference. This is the Heart Flower Patch asset from Bunny Pop-up Storybook. Extract the actual components of the same reference design, without redesigning them.
Exactly THREE SEPARATE KEY PARTS in ONE HORIZONTAL ROW, left to right in this exact order:
LEFT equal column: one detached coral #FF7A6B heart flower head only. Show its actual thick heart silhouette, central folded ridge, low-poly triangular facets, beveled perimeter and thin paper edge from a clear slightly elevated three-quarter angle. No stem attached.
MIDDLE equal column: one detached mint #BDEBD8 straight polygonal stem with its two pointed folded low-poly leaves, exactly matching the stem and leaves in hero.png. No flower head and no planter attached. Show the two leaves separated slightly from the stem to clarify the simple assembly, with visible clean gaps but no arrows, pins, labels or extra hardware. This is one central component group.
RIGHT equal column: the entire empty low ivory paper planter tray from hero.png, with its rectangular 2.5 m by 1.5 m footprint, shallow approximately 0.22 m height, clipped corners, soft bevels, gold-foil upper rim and fine gold lower edge, and mint faceted inset planting surface. Remove all nine flower heads, stems and leaves so the planter itself is fully visible. Slightly elevated three-quarter view.
The assembled asset envelope is width 2.5 m, depth 1.5 m, height 0.9 m; W:D:H = 2.5:1.5:0.9. Preserve each part's actual proportions; close-up display scales may differ between columns for legibility. Each part centred in its own equal vertical third with ample margin and empty space between groups; nothing crosses into another third. One row only, no sub-panels, no duplicate objects or colour variants.
Match the reference's sculpted low-poly papercraft style, matte pastel paper, subtle paper texture and thickness, planar flat-shaded facets, crisp folds, soft bevels, restrained gold-foil accents; all pieces must be simple buildable real geometry. Lighting only models the facets.
Plain completely uniform flat light grey #E6E6E6 background, no floor, no horizon, no cast shadows or contact shadows on the background.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No decorations, tools, scenery, extra parts or drawn connectors.
```

