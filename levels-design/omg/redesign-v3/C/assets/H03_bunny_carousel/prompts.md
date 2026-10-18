# Exact image generation prompts

Generated with the built-in image_gen tool, one call per image, in spec.tsv row order.

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image of the single asset H03_bunny_carousel, Bunny Carousel, for the fan-made rhythm game level Bunny Pop-up Storybook.
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, broad flat-shaded facets, soft small bevels, matte pastel paper, visible slight paper thickness and selected fold seams, restrained gold-foil trims. Do not reproduce its environment.
Subject: a buildable pop-up paper carousel with a round low cylindrical platform, one central structural pole, a pink-and-gold striped radial scalloped canopy, a dimensional pink heart finial, exactly SIX separate bunny seats evenly spaced on SIX twisted poles instead of horses, and warm small light bulbs around the canopy rim. Each bunny is a clean faceted cream rabbit-shaped ride seat, upright ears with pink inner-ear panels, a simple seat area and small cyan saddle accent; no riders. Keep all geometry coherent and practically modelable, simplified polygonal shapes and thick paper panels, no wispy decoration. Poles connect platform to canopy underside. Use a modest, clearly visible spiral gold band on each cream ride pole. Platform has a cream top, pink fascia, gold edging, and a ring of small warm bulbs to support the later platform detail callout.
Exact overall bounding proportions: width 9 m, depth 9 m, height 9 m, W:D:H = 1:1:1 including heart finial and platform. Overall height equals full platform diameter. Round canopy no wider than platform. Make enough open vertical clearance that the bunny seats and six supports are readable. All six seats physically exist around the ring; natural occlusion is acceptable, do not cluster extra bunnies.
Palette: magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, pink #FF6FAE, cyan #7FE0E8, warm lamp #FFC968. Gold should read as subdued gold foil, not chrome. Bunny faces may have minimal inset dark dot eyes and a tiny nose, no writing.
Composition: a single complete isolated carousel, three-quarter view from slightly above, centred with generous margins on every side. Soft studio illumination, gentle contact shadow, plain soft pale-cream gradient background. Show all of the finial and base. Prioritize clean mesh construction and readable shape separation over ornamental detail.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, landscape, extra objects or additional views.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the Bunny Carousel in the supplied hero.png. Input image hero.png is the authoritative DESIGN reference. Reproduce the same single model, same materials, canopy panels, heart, scallops, gold diamond appliques, warm bulb placement, central pink-and-gold column, cream faceted bunny ride seats with pink ears and cyan gold-edged saddles, gold spiral cream ride poles, cream radial platform decking, pink fascia and gold trims. Preserve this identity, do not invent a new carousel or simplify away its key construction.
Background: perfectly uniform flat light grey #E6E6E6. NO floor, NO horizon, NO contact shadows or cast shadows on the background. Soft neutral material shading only; lamp lenses remain warm yellow without large glow halos.
Layout: exactly THREE equal invisible vertical thirds, each containing exactly ONE whole view centred within it with clear margin. LEFT third FRONT elevation, viewed level and horizontally straight at the front. MIDDLE third RIGHT SIDE elevation, seen from the right, exactly a 90-degree rotation from front. RIGHT third TOP plan, straight down vertically along the central column. TRUE ORTHOGRAPHIC projection in all three, absolutely no perspective or three-quarter views. Front and right-side projections must have no visible top surfaces of the horizontal circular platform. Top plan must show concentric platform and canopy circles, the radial striped roof and the heart finial seen directly overhead; do not tilt the top view to show more.
All three use exactly the SAME drawing scale. Model overall actual width 9 m, depth 9 m, height 9 m, W:D:H = 1:1:1. Thus front and side overall bounding boxes are identical squares and stand on precisely the SAME horizontal baseline, with equal heights. Top plan outer diameter equals both the front view width and the side view width at that same scale. Place all three view bounding boxes in an aligned row centred vertically, with matched tops and bottoms for the overall square envelopes. Do not enlarge or shrink the top view independently. Keep each view entirely inside its own third, with margin and separation; nothing overlaps or crosses thirds.
Subject construction: one round low cylindrical platform and matching scalloped radial pink-and-gold canopy, one central pole and heart finial, exactly SIX evenly spaced bunny seats around one ring on SIX twisted poles rather than horses, with physically consistent occlusion between views. Treat hidden elements correctly instead of moving seats to make them visible. Preserve canopy's cream/pink radial panels and gold seams, magenta scalloped valance with small gold diamonds, round warm bulbs, and all faceted papercraft forms from the hero.
Style: sculpted buildable low-poly papercraft, broad flat-shaded facets, soft small bevels, matte paper with slight thickness and fold lines, restrained gold foil. Palette magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, pink #FF6FAE, cyan #7FE0E8, lamp #FFC968.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, border lines, dimension lines, people, logos, watermarks, extra views, backgrounds or props. This is a clean technical turnaround without any annotations.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE for the Bunny Carousel in supplied hero.png. Input image hero.png is the authoritative DESIGN reference. Show its key parts separately as clean buildable real low-poly mesh components, faithfully preserving the hero's shapes, colours, geometry, ornament and paper construction. This is a disassembled component sheet, not a complete carousel.
Layout: ONE horizontal row of exactly FOUR separate part groups, left to right in the following order. Four equal invisible columns, each group centred in its own column with clear margins and gaps, no group crossing into another column. Use small three-quarter views from slightly above to reveal construction. Fit each group comfortably within its column; the groups can have independent close-up scales for legibility. No additional row, duplicate, inset or whole assembled carousel.
LEFTMOST column: the complete striped scalloped CANOPY WITH HEART FINIAL as one detached roof assembly. Exact hero shape: faceted conical shallow radial roof with alternating cream and pink panels and thin gold seams; magenta scalloped hanging valance edged cream and gold with gold diamond appliques and evenly spaced warm yellow round bulbs; low polygonal gold apex cap and dimensional faceted pink heart on top. Show slight paper thickness at the rim. No platform or long poles below this canopy.
SECOND column: ONE complete BUNNY SEAT ON ITS RIDE POLE. Copy a cream faceted leaping rabbit from hero, long upright angular ears with pink inner-ear panels, minimal dark eyes and small pink nose, cyan saddle bordered with gold and gold saddle girth. Its cream cylindrical pole has a clearly modeled gold spiral band and gold polygonal foot and top collar, running vertically through or structurally attached to the bunny. Show the full pole with margin at both ends. No extra bunny, platform or roof.
THIRD column: the detached ROUND PLATFORM WITH BULBS. Copy hero's low polygonal circular cylinder: cream top divided into radial paper sections, magenta/pink fascia, narrow upper and lower gold bands, small gold diamonds and cream vertical panels with raised gold diamonds. A ring of round warm bulbs on its upper fascia. Show the complete platform in a slightly elevated three-quarter view, no bunnies, poles or canopy on it. A small central mounting socket may be visible in the cream top.
RIGHTMOST column: the single detached CENTRAL POLE. Copy hero's thick faceted central column: alternating tall pink and cream faces with gold vertical edge strips, a broad gold base collar and faceted gold-and-pink capital under the roof. It is a straight structural column, distinct from the thin spiral ride pole. No heart, bunny, roof or round platform.
Materials and style: sculpted low-poly papercraft, broad flat-shaded facets and soft small bevels, matte pastel paper, subtle fold seams and real thin panel thickness, subdued gold-foil accents. Preserve palette magenta #FF4FA0, gold #F7D98B, cream #FFF3DE, pink #FF6FAE, cyan #7FE0E8, lamp #FFC968.
Background: perfectly uniform flat light grey #E6E6E6, no floor, no horizon, no cast shadows on the background. Neutral studio material shading; small warm lamp lenses, no large bloom.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos, watermarks, scenery, extra parts or unrelated decorations.
```

