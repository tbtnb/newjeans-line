# Exact image generation prompts

## hero.png

Reference: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create ONE square 1:1 modeling design sheet image for the single asset P02_mushroom_house, Paper Mushroom House, for the fan-made rhythm-game level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded planar facets, softly beveled edges, thick matte paper, subtle fold seams, pastel color treatment and restrained gold-foil trim. Do not reproduce its scene.
Subject: a clean, buildable standalone mushroom house. Overall real bounding dimensions width 2.5 m, depth 2.5 m, height 3 m: W:D:H exactly 2.5:2.5:3. A broad circular-in-plan coral mushroom cap, made from a modest number of broad polygonal radial panels, gently domed with a rounded faceted crown and overhanging rim. Cream polygonal spots lie flush against the cap surface as thin paper appliques. Cream slightly tapered polygonal stem forms the house, a flat bottom, one closed sun-yellow arched door on the front, and one small circular sun-yellow window centered on its right side. Door and window have thin gold-foil frames; window has a simple cross mullion and tiny green paper sill. Simple solid, opaque yellow window panes, no interior scene. Cap rim has visible cream paper thickness. Clearly readable construction with large mesh-friendly facets, restrained fold lines, no microdetails. Palette: coral #FF7A6B, cream #FFF3DE, sun yellow #FFD23F, green #6CCB5F, small gold accents.
Composition: single asset alone, three-quarter view seen from the front-right and slightly above, showing the front door, right-side window, and cap top. Entire object visible, generous margins, object centered. Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background.
Hard constraints: no landscape, base platform, grass, props, characters or people. NO text, letters, numbers, labels, arrows, grid lines, dimension lines, logos or watermarks anywhere. No sketch lines or wireframe. Make real low-poly geometry, not a painted illusion.
```

## views.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a modeller. The attached hero.png is the exact model identity reference: reproduce the SAME Paper Mushroom House, identical cap silhouette, faceting, cream spot placement, cream stem, yellow arched front door, thin gold frames, circular yellow cross-mullioned right-side window and tiny green sill, paper thickness, palette and detail. No redesign.
Overall real model dimensions W:D:H = 2.5:2.5:3 exactly. Make true parallel orthographic projections, no perspective or isometric camera.
Layout: exactly three equal invisible vertical thirds. LEFT third: FRONT elevation looking horizontally straight at the door. MIDDLE third: RIGHT SIDE elevation looking horizontally straight at the right-side window. RIGHT third: TOP plan looking vertically straight down onto the cap. Show exactly these three projections and nothing else. Same physical scale in all three views. Front and side stand on precisely the same baseline and have precisely the same total height. Cap width in top view equals cap width in front view; cap depth in top view equals cap width in side view. Front and side must show no cap top surface due to camera tilt: horizontal viewing axes. Top view is circular-in-plan faceted cap silhouette, with the same cream spots mapped consistently from the reference; hidden stem and door do not appear through the opaque cap. Each view centered within its third, generous margins, nothing crosses between thirds.
Material rendering: sculpted low-poly papercraft, matte pastel paper with broad flat-shaded facets, soft bevels, subtle folds, cream cut edges and restrained gold-foil accents, matching hero.png. Coral #FF7A6B, cream #FFF3DE, sun yellow #FFD23F, green #6CCB5F. Soft neutral illumination just enough to read facets.
Background: perfectly uniform flat light grey #E6E6E6, no floor, no cast shadows on the background, no horizon, no vignette, no gradient.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, panel borders, dimension lines, people, logos or watermarks anywhere. No extra views, no scenery, no props. This is a precise modeling turnaround, not three perspective renders.
```

## parts.png

Reference: `./hero.png`

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT PLATE for a low-poly modeller. Input hero.png is the exact model identity reference: preserve the SAME Paper Mushroom House design, colors, faceting, cap spots, stem, door, window and trims without redesign.
Exactly ONE horizontal row of THREE separate parts in left-to-right order, each centered in its own equal invisible column, with generous margins and gaps, nothing crossing a column:
LEFT: the spotted coral mushroom CAP alone, detached from stem, three-quarter view slightly from above, showing its broad radial polygon panels, exact cream spot arrangement, thin cream underside and real paper rim thickness.
MIDDLE: the cream STEM WITH its attached sun-yellow arched FRONT DOOR, cap removed. Three-quarter front-right view showing the buildable polygonal stem and its upper attachment surface. Keep the door shape, gold trim and small details exactly as in hero.png. The separately displayed right-side window is removed from this stem for the exploded assembly.
RIGHT: the WINDOW assembly alone as an enlarged close-up: the same small circular sun-yellow window from the right side of hero.png, simple cross mullion, thin gold-foil surround, opaque yellow panes, and tiny green paper sill. Show its shallow physical thickness with a very slight three-quarter angle; include no surrounding wall.
This is a separated component callout sheet: exactly these three components, no assembled whole-house duplicate. Keep parts proportional internally; window may be enlarged for construction visibility. Overall assembled house dimensions remain W:D:H = 2.5:2.5:3. Palette coral #FF7A6B, cream #FFF3DE, sun #FFD23F, green #6CCB5F.
Style: sculpted low-poly papercraft, broad clean flat-shaded facets, soft bevels, matte thick paper, subtle fold seams, restrained gold-foil details, clean buildable low-poly meshes matching hero.png. Soft neutral studio illumination to reveal forms.
Background: perfectly flat light grey #E6E6E6 throughout, no floor, no horizon, no cast shadows, no gradient.
Hard constraints: NO text, letters, numbers, labels, arrows, grid lines, column borders, dimension lines, people, logos or watermarks anywhere. No extra components, no scenery or props.
```
