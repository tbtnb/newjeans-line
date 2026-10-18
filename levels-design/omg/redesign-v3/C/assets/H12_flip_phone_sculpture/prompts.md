# Exact image generation prompts

## hero.png

Reference image: `./style-ref.jpg`

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero image for a modeller building a real low-poly game mesh for the fan-made Dancing Line style level "Bunny Pop-up Storybook".
Input image: style-ref.jpg is a STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte paper, slight paper thickness, readable fold lines, restrained gold-foil accents and pastel colours. Do not reproduce the reference scene.
Subject: ONE single asset, Paper Flip Phone Sculpture: a giant retro flip phone standing open upright on a small flower-shaped base. Coral outer shell, cream inner panels, a screen showing only a simple solid pink heart, blank rounded keypad buttons, a visible simple hinge and a short antenna. Use clean, economical, buildable polygon geometry, solid paper-board panels, shallow bevels, subtly faceted rounded corners and visibly separate pieces. No complicated ornament or fine surface noise. The open phone has an upper screen half and lower keypad half connected by the hinge; both form a tall upright sculpture with a slight natural bend at the hinge. A short antenna projects from the upper shell. Use a small low, layered peach-and-cream flower base with mint paper leaves, integrated under the phone. Restrained thin gold-foil edging.
Overall bounding proportions including antenna and flower base MUST be width : depth : height = 2.5 : 1.5 : 5 (physical size 2.5 m wide, 1.5 m deep, 5 m tall). Preserve the tall narrow silhouette; overall width is half overall height, overall depth is 30 percent of height.
Palette: coral #FF7A6B, cream #FFF3DE, pink #FF6FAE, peach #FFC2A8, mint #BDEBD8, small gold-foil accents.
Composition: asset alone, fully visible with generous margins, centered, three-quarter view from slightly above, showing the screen, keypad, right-hand thickness, hinge and flower base. Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background. A clear modelling reference, no scenic environment.
HARD EXCLUSIONS: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. All keypad buttons completely blank. The heart is the only screen graphic. Exactly one image.
```

## views.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE, ideally 1536 x 1024 pixels.
Input image hero.png is the definitive DESIGN AND MATERIAL reference. Reconstruct exactly the same Paper Flip Phone Sculpture from that image, including the same silhouette, open hinge angle, faceted coral shells, cream inset panels, thin gold-foil edging, pink faceted heart on pale pink screen, small cream earpiece, upper-right short cream antenna with gold collar and coral tip, right-side cream-and-gold button, twelve blank cream bevelled keypad buttons arranged in 3 columns and 4 rows, cream-and-coral polygonal barrel hinge with gold end rings, layered peach/cream/coral flower-shaped plinth, peach paper blossoms with gold centres, and mint faceted leaves. Do not redesign or simplify away distinctive pieces. Match the sculpted low-poly papercraft, flat-shaded facets with soft bevels, matte paper thickness and subtle fold seams.
Overall physical bounding box including antenna and flower base: W:D:H = 2.5:1.5:5 exactly. The front bounding width is half the total height; the right side bounding depth is 30 percent of the total height.
Technical layout: plain flat light grey #E6E6E6 background everywhere. Absolutely no floor, horizon, ambient gradient or cast shadows on the background. Exactly three equal vertical thirds, without visible dividing lines. LEFT third: true orthographic FRONT, straight on to the screen and keypad. MIDDLE third: true orthographic RIGHT SIDE, viewed from the sculpture's right, showing the open profile. RIGHT third: true orthographic TOP, straight down, showing the whole complete object's projected footprint, with accurate occlusion of lower pieces. Top view must not become an angled perspective or display the front face upright.
All three projections have IDENTICAL pixels-per-metre scale. Front and side share exactly the same baseline and the same total height including antenna. Top projected bounding width equals front projected bounding width; top projected depth equals side projected bounding width. For a 1536 x 1024 canvas, target front and side heights 760 pixels, front width and top width 380 pixels, side width and top depth 228 pixels. Centre front in the left third and side in the middle third, sharing a baseline at y=880; centre the top view within the right third. Keep comfortable margins within each third. No part crosses between thirds. Three complete separate views of ONE identical asset, no extra inset views.
Use gentle even studio illumination solely to describe the object facets, no background shadow. Palette exactly consistent with reference: coral #FF7A6B, cream #FFF3DE, pink #FF6FAE, peach #FFC2A8, mint #BDEBD8 and small gold accents.
HARD EXCLUSIONS: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. All keys blank; heart is the only screen graphic. True parallel orthographic projection, no perspective convergence, no three-quarter views.
```

## parts.png

Reference image: `./hero.png`

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE, ideally 1536 x 1024 pixels, for a real buildable low-poly mesh.
Input image hero.png is the definitive DESIGN AND MATERIAL reference for the Paper Flip Phone Sculpture. Preserve its geometry, colours, details, thickness, bevel treatment and gold accents exactly; do not redesign.
Background: completely flat uniform light grey #E6E6E6, no floor, no horizon, no gradient, no cast shadows on the background.
Layout: exactly FOUR detached key-part assemblies in ONE horizontal row, left to right in the specified order. Four equal invisible columns, each assembly centred in its own column with comfortable margin. No column lines, no crossing between columns, no extra full-phone miniature. Make close-up three-quarter modelling views with consistent camera direction and even soft illumination. Show clear buildable mesh edges and component construction.
LEFTMOST first column: SCREEN WITH HEART. The detached upper coral screen housing exactly as in hero.png, cream bevelled inner bezel, thin gold edging, pale pink screen, solid faceted pink heart, small cream earpiece. Show the upper housing's thickness and the reference short cream antenna with gold collar and coral faceted tip. Heart remains the only graphic on the screen.
SECOND column: BLANK KEYPAD. The detached lower coral keypad housing exactly as in hero.png, cream inset panel, thin gold edge, twelve cream bevelled blank rounded polygon buttons arranged three columns by four rows. Show the separate shallow raised buttons and the housing thickness. No symbols or marks on any key.
THIRD column: HINGE. The detached horizontal polygonal barrel hinge exactly as in hero.png: cream central barrel, coral bands toward both ends, cream ends and restrained gold-foil end rings. Present it as a simple modest exploded assembly with its end caps separated a small distance along the same horizontal barrel axis, all contained within this column, making assembly and low-poly construction obvious. No additional mechanical complexity.
RIGHTMOST fourth column: FLOWER BASE. The complete detached low flower-shaped pedestal exactly as in hero.png with layered coral bottom, cream middle, peach petal top and thin gold rim, the circular cream-and-gold phone mounting pad, peach folded polygon blossoms with gold centres and mint faceted paper leaves. Remove the phone from this base to reveal its mounting pad, preserve the base's original construction.
Style: sculpted low-poly papercraft with flat-shaded facets, soft geometric bevels, matte paper with slight solid thickness and fold lines, restrained gold-foil details. Same pastel palette as reference: coral #FF7A6B, cream #FFF3DE, pink #FF6FAE, peach #FFC2A8, mint #BDEBD8. No realistic electronics, no glossy plastic, no texture noise.
HARD EXCLUSIONS: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No header or caption. Exactly four parts in the stated single-row order.
```
