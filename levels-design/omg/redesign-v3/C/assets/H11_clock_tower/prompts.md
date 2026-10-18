# Exact image generation prompts

Generated with the built-in image_gen tool, one call per image, in spec.tsv row order.

## hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image for the single asset H11_clock_tower, "Paper Clock Tower", for the fan-made rhythm-game level Bunny Pop-up Storybook.
Input image: style-ref.jpg is the approved art-style reference only. Match its sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte paper surfaces, slight paper thickness and restrained fold lines, gold-foil accents, and pastel colours. Do not copy its scene.
Subject: one clean, buildable freestanding paper clock tower with a square footprint, mint-gray and cream walls, a round cream clock face with dot hour markers only and gold hands, a roof crowned with two upright faceted bunny ears, and warm glowing arched windows. Use simple real low-poly geometry, flat planar panels and shallow bevels; everything must be plausible to model.
Exact overall physical proportions, INCLUDING plinth and bunny ears: width 3 m, depth 3 m, height 9 m, W:D:H = 3:3:9. A tall slender tower, not a squat house. A square stepped cream plinth, slim mint-gray square shaft with cream corner strips, a simple upper clock chamber, shallow four-sided folded-paper roof, two thick faceted cream bunny ears with coral inset faces. Keep roof and ears inside the base's 3 m square footprint. Front has one circular clock face in its upper chamber, with twelve small gold dots and two gold hands. Below it is one tall narrow warm amber arched window. Right wall has one matching arched window at the same elevation and a plain upper panel. Thin gold edging on plinth, chamber cornice and roof. No extra ornaments or surrounding props.
Palette: wardgray #B9CFC8, cream #FFF3DE, gold #F7D98B, coral #FF7A6B, lamp #FFC968.
Composition: single asset alone, three-quarter view from slightly above showing front and right side, centred, fully visible from plinth to ear tips with generous clear margins. Square 1:1 canvas. Plain soft pale-cream gradient studio background, soft studio illumination, gentle contact shadow. Readable solid geometric forms, restrained glow limited to window openings.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, extra objects, floating decorations or environment. Clock has dots only, absolutely no numerals.
```

## views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a low-poly modeller of H11_clock_tower "Paper Clock Tower".
Input image hero.png is the sole authoritative MODEL DESIGN reference. Reproduce that exact tower, colours, geometry, clock, hands, dot markers, windows, frame profiles, gold strips, roof and two faceted bunny ears. Do not redesign or add anything. Translate its perspective into true orthographic views. The asset is mint-gray #B9CFC8 and cream #FFF3DE matte thick papercraft with faceted soft bevels, gold foil #F7D98B, coral #FF7A6B inner ears and amber #FFC968 window panes. Keep all details of the reference: square two-tier cream plinth with gold rims, cream corner pilasters, one tall pointed arched mullioned window on front and one on right, the front-only round clock with dots and gold hands, blank right upper chamber, shallow square pyramid mint roof with gold hip edges and corner caps, two cream polygonal ears with coral insets. Use the reference's exact shapes.
Canvas/background: landscape 3:2. Entire background is perfectly flat solid light grey #E6E6E6. NO floor, horizon, ambient glow on background or cast shadows.
Layout: exactly THREE equal vertical thirds with invisible boundaries. LEFT third is FRONT elevation, straight on to the clock face. MIDDLE third is SIDE elevation viewed from the tower's RIGHT. RIGHT third is TOP plan, camera pointing vertically straight down. Nothing may cross into another third. Each view centred within its own third with generous margins. Exactly one view per third, three depictions total.
Geometric precision: use orthographic parallel projection, zero perspective, zero isometric tilt. Front and right elevations have identical overall height and share the exact same bottom baseline. Overall physical bounding box INCLUDING plinth and ears is width 3 m, depth 3 m, height 9 m, exactly W:D:H = 3:3:9. Render all THREE at one identical pixels-per-metre scale: if the front bounding width is 230 pixels the front height must be 690 pixels, side width 230 and side height 690, and top bounding square 230 by 230 pixels. The top view will thus be much smaller vertically than the standing elevations; never enlarge the top view to fill its column. Centre that small top plan vertically in its third. Roof ears in the top view must be properly foreshortened in plan and occlude the roof as actual geometry. Front elevation must show no right face; right elevation must show no front face and no front clock face except plausible edge thickness; top plan shows no vertical wall faces. Preserve the same bunny-ear positions, planes and construction in every view.
Lighting: soft neutral ambient object shading only to reveal facets, no cast shadows on the background. Buildable low-poly 3D papercraft geometry, crisp silhouette.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos, watermarks, extra objects or decorative symbols. Clock markers are dots only, never numerals.
```

## parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT PLATE for low-poly modelling of H11_clock_tower "Paper Clock Tower".
Input image hero.png is the authoritative design reference. Show exactly FOUR separated component assemblies from that SAME tower, in ONE horizontal row, left to right in the order below. Use four equal invisible columns, each assembly centred within its own column, fully visible with clear margins and no overlaps or crossing between columns. Vertically centre all four component assemblies in one row. These are isolated close-up modelling parts, not four complete towers, and not a two-row arrangement. Components can be independently sized for legibility.
LEFTMOST column: the CLOCK FACE. The exact cream shallow circular disc with softly bevelled rim, twelve raised gold dot hour markers, two faceted gold hands pointing as in the reference and faceted centre pin. No numerals. Show a slightly turned three-quarter close-up so the disc thickness is legible, no wall behind it.
SECOND column: the BUNNY-EAR ROOF assembly. The exact shallow four-sided mint-gray pyramid roof, thin gold hip-edge strips, gold corner caps and small gold centre cap, with the two thick upright faceted cream bunny ears and coral inset front faces. Keep the exact ear shapes, mounting positions and proportions from hero.png. Isolate the complete roof with its cream cornice and ears; omit the shaft and clock. Three-quarter view showing front and right.
THIRD column: the GLOWING ARCHED WINDOW assembly. The exact tall narrow pointed arch from hero.png, thick cream bevelled outer surround, gold/amber inner arch frame and mullions, warm lamp-yellow inset glazing divided into panes, cream sill and small mint-gray panel immediately under the sill. Show slight three-quarter thickness as a separate insert, omit the tower wall. Glow stays confined to glazing with no light spill on background.
RIGHTMOST column: the TOWER BASE assembly. The exact square stepped cream plinth from hero.png, broad low square lower tier with fine gold upper edge, narrower raised square upper tier, mint-gray inset upper tower-foot panel and gold edging. Isolate the base only, no windows, roof or tower shaft. Three-quarter view showing front and right so the square footprint, planar surfaces and step thicknesses are clear.
Style: match hero.png exactly, sculpted low-poly papercraft, flat-shaded polygon facets with soft bevels, matte paper, slight paper thickness and restrained fold lines, subtle gold-foil accents. Clean, real buildable low-poly geometry. Palette wardgray #B9CFC8, cream #FFF3DE, gold #F7D98B, coral #FF7A6B, lamp #FFC968.
Background: entire landscape 3:2 canvas perfectly flat solid light grey #E6E6E6, no floor or horizon, no cast shadows on background, no gradients. Soft neutral studio shading on components only.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, dividing lines, dimension lines, people, logos, watermarks, unrelated objects or decoration. Exactly four component groups in one row, in the requested order. Clock has dot markers only.
```

