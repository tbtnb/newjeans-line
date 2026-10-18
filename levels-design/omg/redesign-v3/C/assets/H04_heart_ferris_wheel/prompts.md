# Exact image generation prompts

Generated with the built-in image_gen tool, one call per row, in spec.tsv order. All calls used transparent_background=false.

## hero.png

Reference: ./style-ref.jpg (style only).

```text
Use case: stylized-concept
Asset type: MODELING DESIGN SHEET, isolated hero for a modeller to build an actual low-poly game mesh.
Create exactly one square 1:1 image of the single asset 'Heart Ferris Wheel' for the fan-made rhythm-game level Bunny Pop-up Storybook. Input image is a STYLE REFERENCE ONLY: match its sculpted low-poly papercraft, flat-shaded planar facets, soft bevels, matte paper, subtle thickness, scored fold lines and restrained gold-foil edges. Do not reproduce its environment.
Subject: a buildable paper Ferris wheel with a clearly HEART-SHAPED open rim, two rounded polygonal lobes with a central notch above and a pointed bottom; straight spokes connect this heart rim to a single central axle hub. Exactly EIGHT small round gondola cabins hang upright from short pivoting hangers distributed around the heart rim. Simple faceted round cabins with cream shells, magenta lower bowls, cyan inset windows, small gold caps; identical construction for every cabin. Structural paper A-frame supports on the front and rear hold the axle and attach to one low rectangular beveled base. Keep structure intelligible and mechanically buildable, modest polygon count, solid paper thickness, no intricate decoration. Small alternating magenta and warm gold light-bulb studs follow the heart rim, with no bloom obscuring geometry.
Real overall dimensions including base and cabins: width 10 m, depth 4 m, height 13 m, exact W:D:H = 10:4:13. Tall silhouette, not a squat wide wheel. Heart rim magenta with gold-foil narrow trim, cream spokes, gold hub, cream A-frame legs with plum inset side faces, cream base with gold edge trim. Palette: magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, cyan #7FE0E8, plum #2A1640, lamp #FFC968.
Composition: the complete single asset alone, centred with generous empty margins, three-quarter view from slightly above that clearly shows the front heart shape and shallow structural depth. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. Clean geometry and easily readable connections, no surrounding props.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

## views.png

Reference: ./hero.png (asset identity).

```text
Use case: stylized-concept
Asset type: MODELING DESIGN SHEET, technical orthographic turnaround for a low-poly mesh modeller.
Input image: hero.png is the authoritative asset identity reference. Depict this SAME Heart Ferris Wheel design, same heart rim shape, faceted cream round gondolas with magenta lower bowls and cyan windows, gold caps, gold pivot hangers, alternating magenta/gold bulb studs, cream spokes, layered gold hub with magenta heart medallion, cream and plum A-frame legs, gold-trimmed cream rectangular base with its four small corner posts. Match its palette and actual details. Maintain the specified total of eight gondolas; show all unobscured cabins and account for any support occlusion in the orthographic projections. No redesign.
Create exactly one LANDSCAPE 3:2 image, an ORTHOGRAPHIC THREE-VIEW PLATE. Pure parallel projection, true orthographic, zero perspective or isometric angle, no vanishing points. Flat uniform light grey #E6E6E6 background, no floor, no horizon, no cast shadows, no ambient shadow patches behind or below the objects. Gentle studio material shading only on the meshes.
Layout: EXACTLY THREE equal invisible vertical thirds. LEFT third: FRONT view looking squarely at the heart face. MIDDLE third: RIGHT SIDE view looking squarely at the right edge, so the heart wheel reads as an edge-on shallow structural assembly and the front/rear support spacing is clear. RIGHT third: TOP view looking exactly straight down, showing the thin edge of the upright wheel and the footprint of the support/base; never show a second heart-shaped front face in the top view. All are the exact same object in the same wheel rotation.
Scale and proportions are mandatory: real overall width 10 m, depth 4 m, height 13 m, W:D:H = 10:4:13 including base and cabins. Use the SAME pixels per metre in all three views. Suggested composition on a 1536x1024 plate: front width 400 px and height 520 px; side width 160 px and height 520 px; top width 400 px and depth 160 px. Front and side have exactly aligned top extent and bottom baseline; top view centred vertically in its third. Centre each view in its own third with generous margin. Nothing crosses between thirds. Never stretch a view to fill its column.
Style: clean buildable sculpted low-poly papercraft, flat-shaded facets and soft bevels, slight matte paper thickness and scored folds, narrow gold-foil accents. Palette magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, cyan #7FE0E8, plum #2A1640, lamp #FFC968. No glow obscuring edges.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos or watermarks anywhere.
```

## parts.png

Reference: ./hero.png (asset identity).

```text
Use case: stylized-concept
Asset type: MODELING DESIGN SHEET, DETAIL CALLOUT PLATE for a low-poly game mesh modeller.
Input image: hero.png is the authoritative design reference. Extract the actual components of this SAME Heart Ferris Wheel; preserve the exact silhouette, construction, materials, colors, gold trim, faceted cabin design and support details. This is a component breakdown of that reference, not new variants.
Create exactly one LANDSCAPE 3:2 image. Plain flat uniform light grey #E6E6E6 background, no floor or horizon and no cast shadows on the background. Exactly FOUR equal invisible vertical columns, with FOUR isolated component groups centred across ONE single horizontal row, aligned by visual centres. Generous margins and empty gaps, no overlap or crossing columns. Components may use different enlargement scales to make their construction clear. Clean slightly elevated three-quarter views, soft object shading with readable planar facets. Display only these groups in exactly this left-to-right order:
LEFTMOST column: the complete polygonal HEART-SHAPED RIM alone, two lobes with central top notch and pointed bottom, thick magenta paper beam with narrow gold edge trim, alternating magenta and warm gold bulb studs along the rim. No spokes, cabins, hub, support or base in this group.
SECOND column: ONE round faceted GONDOLA CABIN, hanging gold pivot bracket and short hanger, gold cap, cream faceted upper shell, cyan window panels in cream-and-gold frames, magenta faceted lower bowl. Make this an enlarged close-up, slightly vertically exploded within its own column so roof/hanger, cabin shell and lower bowl are intelligible but recognizably the exact assembled cabin from the reference. No other cabin copies.
THIRD column: HUB AND SPOKES alone, layered low-poly gold circular hub with the small magenta heart medallion and cream radial spoke beams matching the reference wheel's heart-shaped spoke endpoints. Show the short axle subtly pulled back to make the connection clear. No rim, cabins, support legs or base.
RIGHTMOST column: complete A-FRAME LEGS AND BASE alone, front and rear cream paper structural A-frames with plum inset faces and gold edges mounted on the single cream rectangular base, gold trim and four short magenta-faced cream corner posts with gold pyramid caps, exactly as reference. No wheel rim, spokes, hub or gondolas.
Style: sculpted low-poly papercraft, flat-shaded facets, soft bevels, clean buildable real polygonal geometry, modest mesh complexity, slight paper thickness and scored fold lines, matte paper with restrained gold foil. Palette magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, cyan #7FE0E8, plum #2A1640, lamp #FFC968. Overall assembled asset proportions remain W:D:H = 10:4:13; component forms must fit that same reference assembly.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos or watermarks anywhere. No extra items or decorative scene.
```

