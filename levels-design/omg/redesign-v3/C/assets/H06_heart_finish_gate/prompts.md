# Exact image generation prompts

Generated with the built-in image_gen tool, one call per image, in spec.tsv row order.

## hero.png

Reference image: ./style-ref.jpg

```text
Use case: stylized-concept.
Create ONE square 1:1 MODELING DESIGN SHEET hero render of the single asset "Heart Finish Gate" for the fan-made Dancing Line style rhythm game level Bunny Pop-up Storybook (NewJeans OMG). The supplied image is a STYLE REFERENCE ONLY: match its sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte thick paper, visible page layers and fold lines, gold-foil accents and pastel palette. Do not reproduce its scene.
Subject: a giant freestanding heart-shaped finish arch made of curled cream book pages with gold edges, small warm glowing bulbs following the heart outline, two small faceted bunny statues at its two feet, and a folded page-ribbon crown at the top. A clear walk-through opening between the two grounded feet. The heart's two rounded angular lobes and central upper notch must read clearly; lower sides taper inward toward two separate feet, keeping the center passage open. Use a few broad, clean folded page bands with visible thickness and simple gold edging, not numerous thin loose sheets. The two matching cream-white low-poly bunny statues have long faceted ears with blush inner panels and hold small pink hearts. Ribbon crown is an unprinted cream folded page bow with gold edges and two short blush-backed tails, attached to the upper center. All pieces must be clean, mechanically buildable low-poly meshes, visible planar facets, modest bevels, no wispy or floating details.
Overall real dimensions INCLUDING feet, bunnies and crown: width 12 m, depth 3 m, height 11 m. Keep W:D:H exactly 12:3:11, a broad almost-square front silhouette and shallow extrusion. Keep all ornaments inside that overall bounding box.
Palette: cream #FFF3DE, gold #F7D98B, pink #FF6FAE, blush #FFC7DA, lamp #FFC968, white #FFFFFF. Gold is subtle foil edging; bulbs are small polygonal lamp beads with restrained warm glow.
Composition: single complete assembled asset alone, three-quarter view from slightly above, enough side visible to explain the shallow 3 m depth. Fully visible with generous margins. Plain soft pale-cream gradient background. Soft neutral studio light and gentle contact shadow only. Crisp modeling-readable geometry.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No surrounding scenery, extra props, track, castle or book landscape.
```

## views.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a low-poly modeller. The supplied hero.png image is the authoritative DESIGN reference. Depict exactly that same Heart Finish Gate, with identical cream layered curled-page heart arch, gold edges, polygonal amber bulbs on the front outline, two cream faceted bunny statues holding pink hearts at the feet, pink ear insets, trapezoidal plinths, pink page undersides, and the same folded cream-and-gold page bow crown with pink-backed tails. Preserve all part shapes, arrangement and details. Style: sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper with slight thickness and fold lines, subtle gold foil. Not a redesign.
Overall assembled bounding-box proportions MUST be W:D:H = 12:3:11 including crown and bases. The arch is shallow in depth. Use a true orthographic parallel camera for every view, ZERO perspective, ZERO three-quarter angles.
Layout: exactly THREE invisible equal vertical thirds, no dividers. LEFT third: straight-on FRONT view of complete gate, both bunnies visible symmetrically. MIDDLE third: exact right SIDE elevation, looking from the right perpendicular to the side; show narrow depth silhouette, front and rear surfaces in exact profile, near bunny occluding far bunny naturally. RIGHT third: exact TOP plan, looking straight down perpendicular to the ground; show actual shallow footprint, top facets, bow top, bunny ear tops and plinths with proper physical occlusion. Never show a heart-shaped front elevation laid flat as the top view.
All three projections use precisely the SAME scale. Front and side views stand on the SAME baseline and have identical total height. Top-view width equals front-view width; top-view depth equals side-view width. Quantitative layout guidance: overall view widths front:side:top = 12:3:12, overall view heights front:side:top = 11:11:3. Each view centred within its own third, with comfortable margins; no projection crosses into any other third. Center the shallow top plan vertically in its third. Do not enlarge the narrow side view to fill its third.
Background: perfectly flat uniform light grey #E6E6E6, no floor, no horizon, no cast shadows or contact shadows on background. Soft neutral material lighting only; preserve readable faceted surface shading. Bulb warmth is subtle and does not spill onto the background.
Palette: cream #FFF3DE, gold #F7D98B, pink #FF6FAE, blush #FFC7DA, lamp #FFC968, white #FFFFFF.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dividing lines, dimension lines, people, logos or watermarks anywhere. Only three complete projections of this same asset.
```

## parts.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT PLATE for a low-poly modeller. The supplied hero.png is the authoritative design reference: show separate key parts extracted from that EXACT Heart Finish Gate, no redesign. Match its sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper thickness and folds, subtle gold foil, cream layered pages, blush undersides, faceted glowing lamp beads and featureless faceted cream bunny holding a pink heart.
Background is perfectly flat uniform light grey #E6E6E6 with no floor, horizon or background cast shadows. Soft neutral studio illumination only, with readable material shading. Exactly FOUR isolated parts in ONE horizontal row, from left to right in this exact order:
LEFTMOST column: one curled page segment from the arch, a short gently bent thick cream page band with two or three visible layered edges, clean fold planes, gold border and a glimpse of blush paper underside. Show a detached buildable segment, not a complete arch.
SECOND column: one short separate curved section of the gold-trimmed cream lamp mounting band, carrying a row of three small polygonal warm amber bulbs exactly matching the lamps on the hero's heart outline. Show the bead shape and mounting thickness clearly; restrained warm glow, no bloom on background.
THIRD column: one complete bunny statue at the foot, exactly as in hero: faceted cream-white rabbit with two long polygonal upright ears with pink inner panels, featureless faceted rounded head, small paws holding one faceted pink heart, squat seated body and feet, mounted on its matching small cream trapezoidal plinth with gold trim. Retain the small folded blush-backed page accents behind its base.
RIGHTMOST column: the complete page-ribbon crown detached from the arch, exactly matching the hero's cream folded page bow: two broad angular loops, thick central band, gold paper edges, blush interior and two short pointed pink-backed tails. No added ornaments.
Layout: four invisible equal-width columns, each part centered in its own quarter at the same row center; generous empty gaps and outer margins; no component crosses its quarter. Three-quarter detail views from slightly above, consistent lighting and crisp focus. Magnify small parts for modelling clarity while keeping each whole component visible. Only these four components, no duplicate views, no assembled gate.
Palette: cream #FFF3DE, gold #F7D98B, pink #FF6FAE, blush #FFC7DA, lamp #FFC968, white #FFFFFF.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, column lines, dimension lines, people, logos or watermarks anywhere.
```

