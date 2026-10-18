# Exact image generation prompts

Generated with the built-in image_gen tool, one call per row, in spec.tsv row order.

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create ONE square 1:1 MODELING DESIGN SHEET hero image for a low-poly mesh modeller, for the rhythm game level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE REFERENCE ONLY. Match its sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte pastel paper, slight paper thickness, visible fold seams and restrained gold-foil accents. Do not reproduce the scenery.
Subject: the single asset 'Paper Stair Segment', a short curved paper staircase segment with a thin rail, lilac and white. Overall real bounding dimensions including the rail: width 3 metres, depth 1.2 metres, height 2 metres, exact W:D:H = 3:1.2:2. This is a broad, shallow stair segment, not a tall narrow spiral.
Buildable design: six broad white treads with lilac risers and lilac folded-paper side cheeks. The tread front edges form matching gentle convex arcs in plan, approximated by a small number of straight polygon segments. Treads ascend toward the back; a single thin lilac rail on the right side follows the stair incline with simple slender posts. Very narrow pale-gold foil edging on the step noses and rail top. Rail has paper thickness and a simple low-poly rectangular cross section. Keep all components solid, coherent and easy to model; no floating decorative objects. Clean understated forms, no extraneous ornament.
Composition: show only ONE complete staircase in a three-quarter view from slightly above, showing the front, right side and tread tops; centred with generous clear margins on every side. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. Clearly readable mesh shapes.
Palette: lilac #E3D7FA, white #FFFFFF, pale gold #F7D98B.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere in the image. No environment, no floor platform, no extra assets.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a low-poly mesh modeller.
Input image: hero.png is the definitive ASSET DESIGN REFERENCE. Reproduce this exact paper staircase, its six white treads, lilac risers and folded side cheeks, segmented curved step noses, single right-hand rail, rail posts and pale-gold caps and trim. Preserve every component, colour and placement. The reference supplies object identity, not camera or background.
Asset: Paper Stair Segment, a short curved paper staircase segment with a thin rail. Overall bounding dimensions INCLUDING rail: width 3 m, depth 1.2 m, height 2 m, W:D:H = 3:1.2:2. Maintain this bounding proportion in the projections while preserving the reference design.
Camera/layout is paramount: true parallel orthographic projections with ZERO perspective. Exactly three equal invisible vertical thirds, with no dividers. LEFT third: FRONT view looking horizontally at the stair entrance, with width 3 and total height 2; do not show tread top surfaces through a tilted camera. MIDDLE third: SIDE view seen from the RIGHT, width/depth 1.2 and total height 2, the right-hand railing closest to the camera. RIGHT third: TOP view looking exactly vertically down, width 3 horizontally and depth 1.2 vertically. All three are projections of the SAME model with the SAME world-units-to-pixels scale. Front and side share exactly the same baseline and top height. Top width equals front width; top depth equals side width. Do not rotate or resize any view to fill its column.
For a 1536 by 1024 composition, centre the views at horizontal positions 256, 768 and 1280; approximate object bounds are front 420 wide by 280 high, side 168 wide by 280 high, top 420 wide by 168 high. Front and side baseline approximately 652, each view vertically centred around 512. These are invisible layout instructions only; draw no measurements. Each object centred in its own third, comfortable margins; nothing crosses thirds.
Style: sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper with slight thickness and fold seams; lilac #E3D7FA, white #FFFFFF, gold-foil accents #F7D98B. Neutral diffuse object shading for legibility.
Background: uniform flat light grey #E6E6E6 over the entire canvas. NO floor, horizon, cast shadow, contact shadow, ambient shadow on background, gradient or vignette.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Exactly three views, no extra parts or scene.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT PLATE for a low-poly mesh modeller.
Input image: hero.png is the definitive ASSET DESIGN REFERENCE. This is a disassembled parts study of that EXACT staircase, not a redesign. Preserve its six curved white treads, lilac risers and folded-paper side cheeks, right-hand lilac rail shape and posts, pale-gold caps and narrow gold-foil edging. Match all colours, thicknesses, bevels, faceted seams and component counts visible in the reference.
Asset: Paper Stair Segment, a short curved paper staircase segment with a thin rail, lilac and white. Assembled overall size including rail: W:D:H = 3:1.2:2, width 3 m, depth 1.2 m, height 2 m.
Layout: exactly TWO separate key-part assemblies in ONE horizontal row, left to right in this precise order: steps; rail. Exactly two equal invisible columns. Each part is centred in its own half with generous margins. Nothing crosses the central boundary. No panels or borders.
LEFT HALF: the complete six-step stair body, including its white tread surfaces, lilac risers, folded lilac supporting side cheeks and pale-gold step-nose trim, with the entire railing removed. Show the stair assembly clearly in a close three-quarter view from slightly above; all six step surfaces and the sculpted paper edge thickness must be readable. No rail or rail posts anywhere on the stair body.
RIGHT HALF: the complete matching single right-hand railing assembly detached from the stair body, displayed in a close three-quarter view with the same orientation. Include the continuous segmented lilac handrail with its narrow pale-gold top strip, the exact end and intermediate posts and cap/base shapes from the hero reference. Keep the posts in their original ascending arrangement relative to the handrail, exposing their separate bottom attachment faces. No staircase or tread pieces under this rail. Show only coherent buildable geometry, no loose decorative bits. The detached assembly is suspended against the background as a technical parts display.
Style: clean sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper with slight thickness and fold lines, lilac #E3D7FA, white #FFFFFF, restrained gold-foil accents #F7D98B. Soft neutral studio illumination on the objects.
Background: perfectly flat uniform light grey #E6E6E6. No floor, no horizon, no cast shadows or contact shadows on background, no gradient.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. Exactly the two listed key parts in one row; no assembled asset, additional views, extra objects, scenery or inset images.
```

