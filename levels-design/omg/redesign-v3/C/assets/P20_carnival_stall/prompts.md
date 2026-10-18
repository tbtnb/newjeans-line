# Exact image generation prompts

Built-in image_gen; one call per image, in spec.tsv row order.

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image for a modeller building a real low-poly game mesh: asset P20_carnival_stall, Carnival Stall, for the fan-made Dancing Line style rhythm level Bunny Pop-up Storybook (NewJeans OMG).
Input image: style-ref.jpg is an approved world render; use it only as the art-style reference. Show only the requested stall, with no environment from the reference.
Subject: a small paper carnival stall with a striped scalloped awning, a counter with candy jars, string lights, and a heart sign without text. Exact overall bounding proportions W:D:H = 3:2:3.2, equivalent to width 3 m, depth 2 m, height 3.2 m including the heart sign. Make a coherent simple buildable structure with a rectangular counter base, four slim square paper posts, a folded pitched striped awning with scalloped front edge, a short string of faceted bulb lights under the awning, and a thick faceted heart sign mounted centrally above the roof. Keep the roof, sign, posts, counter, jars and lights clearly readable as separate solid low-poly components. Candy jars are a small set of simple low-sided cyan-tinted containers with polygonal candy pieces and gold lids, rendered as stylized solid geometry rather than realistic glass.
Style: match the supplied world: sculpted low-poly papercraft, flat-shaded facets, small soft bevels, matte paper surfaces, slight visible paper thickness, restrained fold lines, thin gold-foil edge accents. Pastel storybook treatment of magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, cyan #7FE0E8. Use alternating magenta and cream awning stripes, cream counter with magenta panels and fine gold trim, cyan accents, magenta heart with gold edging. Clean economical geometry, no fragile decorative clutter.
Composition: the single complete asset alone, three-quarter view from slightly above showing the front and its right side. Centre it with generous clear margins on every side; show all of the heart, awning, supports and base without cropping. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. No additional display base.
Hard constraints: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere in the image. No other assets. The image is a clear modelling reference, not a scene illustration.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a low-poly mesh modeller.
Input image: hero.png is the definitive design reference for asset P20_carnival_stall, Carnival Stall. Reproduce the SAME stall, exact same component shapes, colours, awning stripes, five candy jars in their original order, faceted gold-edged magenta heart, roof gable, finials, square posts, hanging faceted bulbs, counter panels, gold trim and cyan accents. Change only the camera and sheet presentation. Do not redesign or simplify away its distinctive parts.
Overall physical bounding dimensions including the heart sign: width 3 m, depth 2 m, height 3.2 m, W:D:H = 3:2:3.2. Preserve these exact relative extents in the projections. Use true orthographic projection, zero perspective, zero camera tilt. The orthographic front and right side show absolutely no top surfaces of horizontal planes; the top view looks straight vertically down.
Layout: plain uniform flat light grey #E6E6E6 background, no floor or horizon and NO cast shadows on the background. Exactly three equal vertical thirds with no drawn dividers. LEFT third: FRONT elevation, looking squarely at the candy counter and broad front awning. MIDDLE third: RIGHT SIDE elevation, looking squarely at the right narrow side of that same stall. RIGHT third: TOP plan, looking straight down onto its awning and edge-on heart sign; correctly occlude the jars beneath the roof rather than moving them.
All three views use precisely the SAME pixels-per-metre scale. Front and side stand on the same baseline and have the same overall height. Top view width equals front view width; top view depth equals side view width. For a 1536 x 1024 canvas, aim for front bounds 390 pixels wide x 416 high, side 260 wide x 416 high, top 390 wide x 260 high, with centres at x=256, x=768, x=1280; front and side baseline y=730 and top centred vertically in its third. These coordinates are layout guidance only and must NOT appear as text. Centre each view within its own third with ample margins; nothing crosses a third boundary.
Style: the exact sculpted low-poly papercraft of hero.png, flat-shaded facets, soft small bevels, matte paper, slight thickness and fold lines, gold-foil accents, palette magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, cyan #7FE0E8. Neutral even studio illumination on objects only, clean readable technical turnaround.
Hard constraints: exactly THREE views of ONE identical model. NO perspective, isometric or three-quarter views. NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No extra objects, no decorative background.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT PLATE for a low-poly mesh modeller.
Input image: hero.png is the definitive design reference for asset P20_carnival_stall, Carnival Stall. Extract and display the specified parts of that SAME model separately. Preserve its exact component shapes, magenta and cream stripe arrangement, gold trim, cyan accents, paper facets and ornamental details; do not invent a new stall.
Background: absolutely uniform flat light grey #E6E6E6, no gradient, no floor, no background cast shadows.
Layout: ONE horizontal row of exactly THREE separated close-up component groups, left to right in the following listed order. Each group is centred in its own equal-width column with generous empty margins. Keep every group entirely inside its own third, with no overlap, no connecting lines, no additional views and no extra loose pieces. Three-quarter views from slightly above, consistent camera angle, neutral soft studio object lighting.
LEFT third: the STRIPED AWNING assembly detached from the stall, with its folded pitched magenta-and-cream paper roof, thick scalloped front and side valances, thin gold edges, cyan gable panels, gold roof trim and corner finials exactly as seen in hero.png. Exclude the separately displayed heart sign and exclude the counter and tall support posts. Show paper thickness and folded construction clearly.
MIDDLE third: the COUNTER WITH JARS detached from the roof and tall posts. Keep the entire cream rectangular counter, magenta front and side inset panels, fine gold borders, cyan corner panels, front triangular magenta-and-gold hanging pennant, and all FIVE cyan low-sided candy jars with gold lids, matching hero.png in placement, relative sizes and contents: large pink-candy jar, smaller mixed-star jar, tall mixed pink-and-cream-candy jar, medium star-candy jar, smallest pink-candy jar, in that order across the counter. Show the counter and jars as one coherent component group.
RIGHT third: the HEART SIGN detached by itself, the same thick bevelled gold frame surrounding the faceted magenta paper heart as hero.png, with a slight three-quarter angle revealing its real solid thickness. No lettering or icon added.
Style: matching the reference's sculpted low-poly papercraft with flat-shaded polygon facets, soft small bevels, matte paper surfaces, subtle fold lines and thin paper thickness, restrained gold-foil accents. Palette magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, cyan #7FE0E8. Real buildable low-poly geometry, clean edges, readable modelling details. The full source model has W:D:H = 3:2:3.2; keep each part's shape and proportions faithful to that source. The detached parts may be enlarged individually to fill their columns.
Hard constraints: exactly these THREE component groups in ONE row. Absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere in the image. No complete assembled stall, no environment, no pedestal.
```

