# Exact image generation prompts

## 1. hero.png

Reference: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero image for a modeller building a real low-poly mesh for the fan-made Dancing Line style rhythm game level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte thick paper, visible cut edges and fold creases, delicate gold foil, and pastel storybook aesthetic. Do not copy its scene or add scenery.
Subject: exactly one assembled Pop-up Pull Tab Mechanism, isolated and fully visible with generous margins. A horizontal paper slider strip terminating at the left in a solid round tab handle, running through two simple folded paper guide loops on a narrow base, and a folded paper lever that connects the slider to a raised rectangular pop-up panel. Show the mechanism in one fixed partly raised pose. The panel is a plain cream rectangle with subtly clipped corners, a thin inset gold-foil border, and coral paper on its reverse. The round handle is a simple low-poly circular coral paper disc with a narrow gold rim and cream inset face, no hole, joined directly to the coral slider strip. The folded lever is a cream zigzag paper linkage with clear straight segments, fold lines, and small gold fold-edge accents; keep it visible beside/behind the panel. Clean practical construction, a few broad planar polygons, shallow bevels, realistic paper thickness, simple physically connected parts, no metal machinery, no floating parts.
Exact overall assembled proportions: width 1.5 m along left-right X, depth 0.3 m along front-back Y, height 1.2 m along vertical Z; W:D:H = 1.5:0.3:1.2, measured across the complete asset including the left handle and the raised panel. A broad tall assembly with very shallow depth. Keep all components within this bounding box. Use cream #FFF3DE, gold #F7D98B, coral #FF7A6B only, with natural shaded variants.
Composition: single asset alone, three-quarter view from slightly above, see front and right side so the slider, round handle, guide loops, panel and folded linkage can be understood. Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background. No floor horizon. Object fills about 80 percent of the frame and is not cropped.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, decorative scenery, extra objects, or inset views anywhere. This is a clean buildable low-poly model concept, not an illustration of a whole book.
```

## 2. views.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create one landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a modeller building the low-poly Pop-up Pull Tab Mechanism shown in the input hero.png.
Input image: hero.png is the authoritative object design and material reference. Reproduce this SAME assembled model in the SAME fixed raised pose, with identical geometry, colours, panel position, slider position, handle, guide loops, folded lever, and gold accents. Do not redesign it.
Subject: a coral horizontal slider ending on the left in a solid faceted round coral tab with gold annular rim and cream inset face; two cream gold-edged folded guide loops on a long shallow cream gold-edged base; a cream zigzag folded linkage on the right supporting the raised cream clipped-corner rectangular panel with its thin inset gold border and coral reverse. Preserve all visible details from hero.png. Low-poly planar paper construction, subtle bevels, matte paper thickness and fold creases, gold foil. Palette cream #FFF3DE, gold #F7D98B, coral #FF7A6B, natural flat-shaded variants.
Exact whole-asset W:D:H = 1.5:0.3:1.2, including all components. X is horizontal slider direction, Y is shallow depth, Z is height. Use parallel projection, absolutely no perspective, no isometric or three-quarter views.
Composition: exactly THREE equal vertical thirds without visible dividers. LEFT THIRD: true FRONT elevation looking along Y, see the cream faces of the panel and circular tab, slider perfectly horizontal. MIDDLE THIRD: true RIGHT SIDE elevation looking along X from the right, revealing the shallow depth and zigzag lever; no invented broad front face. RIGHT THIRD: true TOP plan looking straight down along Z, slider horizontal, panel seen edge-on from above in its raised pose.
All THREE views use exactly the same pixels per metre, no fitting each view to its column. In the left third, overall front width is 1.5 units and height is 1.2 units. In the middle third, overall side width is only 0.3 units, exactly ONE FIFTH the front view width; side height exactly matches front height, 1.2 units. Front and side share the same horizontal baseline and top height. In the right third, top width exactly equals front width, 1.5 units, and top depth exactly equals side width, 0.3 units. Thus the right-side elevation is tall and very narrow, and the top plan is long and very shallow. Centre each projection inside its own third with clear margins, nothing crosses into another third. Suggested invisible layout on a 1536x1024 canvas: front centred at x256, side at x768, top at x1280; front and side baseline y672, height320 pixels; front and top width400 pixels; side width and top depth80 pixels. These coordinates are layout instructions ONLY and must not be printed.
Background: uniform flat light grey #E6E6E6 across the entire image. No floor, horizon, cast shadows, ambient shadow blobs, scene, or gradient. Neutral soft illumination to reveal facets on the object only.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos, watermarks, additional views or additional objects anywhere. Show exactly the three orthographic projections specified.
```

## 3. parts.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create one landscape 3:2 DETAIL CALLOUT PLATE for a modeller building the Pop-up Pull Tab Mechanism in input hero.png.
Input image: hero.png is the authoritative design reference. Extract and show its listed three key parts separately, preserving the exact design, colours, paper construction, facets, bevels, thickness, and gold accents. No redesign.
Layout: ONE horizontal row of exactly THREE separate parts, left to right in the stated order, each centred in its own equal-width invisible vertical column with ample margin. Column centres at one sixth, one half, and five sixths of canvas width. No item may cross a column boundary. Use close-up three-quarter views with consistent camera direction and soft neutral lighting, so the thickness and folded construction are clear. Exploded apart means the three listed components are detached from each other; do not show assembled mechanisms or repeat parts.
LEFT COLUMN: round tab handle ONLY. The same solid low-poly circular disc from hero.png: faceted coral outer circumference and edge, narrow gold annular rim, cream inset circular face, no hole. Show the full disc at useful close-up size.
MIDDLE COLUMN: slider strip ONLY. The same long straight coral rectangular paper slider from hero.png, thin gold paper edge, small bevels, rectangular section, clearly much longer than its height, viewed at a shallow three-quarter angle and fitted entirely within its column. Detach the round handle; no guide loops or base accompany this strip.
RIGHT COLUMN: folded lever ONLY. The same cream zigzag folded paper linkage from the right end of hero.png, with its straight broad planar segments, gold edging, clear fold creases, and lower attachment flap, in the identical bent pose. Detach the raised panel and base; show just the complete linkage.
Materials: sculpted low-poly papercraft, matte paper, slight paper thickness, flat-shaded facets with soft bevels, gold-foil details. Palette cream #FFF3DE, gold #F7D98B, coral #FF7A6B with natural shaded variants. Clean geometry that a modeller can build.
Background: absolutely uniform flat light grey #E6E6E6. No floor or horizon, no cast shadows on background, no gradients. Gentle shading on the parts themselves only.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dividing lines, dimension lines, people, logos, watermarks, additional objects, panel, guide loops, base, full assembly or inset views anywhere. Exactly the three listed detached components, in one row, in that order.
```

