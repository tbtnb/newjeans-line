# Exact image generation prompts

Generated with the built-in image_gen tool, one call per image in spec.tsv row order. transparent_background: false for every call.

## 1. hero.png

Reference image: ./style-ref.jpg

```text
Use case: stylized-concept.
Create exactly one square 1:1 MODELING DESIGN SHEET hero image for the single asset "Pop-up Paper Ward Bed" for a fan-made Dancing Line style rhythm game level, Bunny Pop-up Storybook.
Input image: /Users/bit_1/nj-level-art/omg-c-assets/H10_ward_bed_set/style-ref.jpg is an approved in-game STYLE REFERENCE ONLY. Match its sculpted low-poly papercraft, flat-shaded polygon facets with soft bevels, matte paper, slight sheet thickness, visible fold lines, restrained gold-foil edge accents and pastel colors. Do not reproduce its scene, castle, rabbits or scenery.
Subject: one complete, clean, buildable low-poly pop-up paper hospital bed assembly, including a mint-gray blanket and mint-gray pillow, one folding THREE-PANEL paper privacy curtain on the rear side of the bed, one small bedside lamp glowing warm, and visible structural fold tabs. Keep the design simple enough for a modeller to reproduce with actual low-poly meshes. Stiff folded paper rather than flowing fabric; no tiny clutter.
Overall exact assembly bounding-box proportions W:D:H = 3:2:2.4, representing width 3 m, depth 2 m, height 2.4 m. The broad front is the long side of the bed. Bed length runs left to right, pillow/head at left and foot at right. The three connected privacy panels span the rear width in a shallow accordion zigzag, highest point 2.4 m; exactly three panels with simple cream borders, mint-gray faces, coral lower edge accents and small gold hinge edges. The cream paper bed frame sits forward of this screen, with a low cream headboard at left, low cream footboard at right, a white mattress, a faceted mint-gray pillow at the left end, and a mint-gray folded blanket covering the right two-thirds. The small warm lamp stands beside the head at the left on a simple low folded cream bedside plinth; angular cream-and-gold stem, faceted cream shade, warm amber inner shade. All components form ONE cohesive asset. Show practical cream folded support tabs at the base of the screen and bed, with clear fold creases and paper thickness. Avoid added decorative symbols.
Palette: wardgray #B9CFC8, cream #FFF3DE, coral #FF7A6B, lamp light #FFC968, white #FFFFFF, with restrained warm gold-foil accents.
Camera/composition: single three-quarter view from slightly above, looking toward the broad front so the mattress, pillow, blanket, all three curtain panels, lamp and fold construction are readable. Entire asset completely visible, centered, generous margins on every side. Square canvas.
Background and lighting: plain soft pale-cream gradient background, soft studio light, gentle contact shadow below the assembly. No environment.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No extra views, inset panels or spare parts in this hero image.
```

## 2. views.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the Pop-up Paper Ward Bed.
Input image: /Users/bit_1/nj-level-art/omg-c-assets/H10_ward_bed_set/hero.png is the authoritative design reference. Depict the IDENTICAL complete assembly, same three hinged screen panels, bed, pillow, blanket, bedside lamp and its plinth, paper fold tabs, silhouettes, materials, palette and details. This is a technical turnaround of this model, not a redesign.
Background: perfectly uniform flat light grey #E6E6E6. No floor, no horizon, NO cast shadows on the background. Only restrained surface shading to describe the actual low-poly facets.
Layout: exactly THREE equal vertical thirds with no drawn separators. LEFT third FRONT view; MIDDLE third SIDE view seen from the RIGHT; RIGHT third TOP view straight down. Only these three views, each centered within its own third, with generous margins. Nothing crosses into any adjacent third. True orthographic parallel projection for all three, no perspective, no three-quarter angles, no isometric view. Front and right-side cameras are level, with no view down onto horizontal surfaces.
Coordinate convention: width X is the long left-to-right bed axis in the hero, depth Y is front-to-back toward the rear privacy curtain, height Z is vertical. FRONT looks straight at the bed's broad long side, showing pillow/head at left and foot at right, with the tall three-panel screen behind it and the lamp/plinth at far left. RIGHT SIDE looks from the foot end toward the pillow, so the footboard is nearest, the rear curtain is edge-on in profile behind it, and distant parts occlude correctly. TOP looks exactly vertically down, showing the bed footprint, pillow at left, blanket toward the right, lamp/plinth beside the head, and the shallow three-panel accordion footprint along the rear. Preserve actual component positions and folds under rotation; do not rotate individual components for visibility.
Exact complete assembly bounding proportions W:D:H = 3:2:2.4 (width 3 m, depth 2 m, height 2.4 m). SAME drawing scale in every view. Front width : side width : shared height = 3 : 2 : 2.4. Top width equals front width exactly; top depth equals side width exactly. Front and side share one baseline and have exactly the same overall height. For a 1536 x 1024 canvas, a suitable invisible layout is each third 512 pixels wide, front bounding size 400 wide by 320 high, side 267 wide by 320 high, top 400 wide by 267 high; center each at x=256, 768, 1280 respectively. Front and side baseline both y=700; center the top view near y=540. These layout coordinates are instructions only, never render them.
Materials: clean buildable sculpted low-poly papercraft with flat polygon facets, soft bevels, slight paper thickness and clear fold creases, cream frames, mint-gray pillow/blanket/screen panels, coral lower bands, thin restrained gold-foil edges and hinge details, warm amber lamp interior. Palette wardgray #B9CFC8, cream #FFF3DE, coral #FF7A6B, lamp #FFC968, white #FFFFFF. Match the reference design faithfully.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere. No perspective views, no extra objects, no extra views, no background shadows.
```

## 3. parts.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create exactly one landscape 3:2 DETAIL CALLOUT MODELING PLATE for the Pop-up Paper Ward Bed.
Input image: /Users/bit_1/nj-level-art/omg-c-assets/H10_ward_bed_set/hero.png is the authoritative design reference. Extract and display the actual parts of THIS SAME model; identical silhouette, folded construction, colors, facets, bevels, thickness and details, with no redesign.
Layout: exactly FOUR isolated component callouts in ONE horizontal row from left to right, each centered in its own equal-width invisible column. Column centers at 12.5%, 37.5%, 62.5%, 87.5% of canvas width. Every component stays fully inside its own column with ample margins and clear gaps between columns. Align their visual centers near the horizontal midline. No second row and no inset panels. Components may use independent close-up scales so all are clearly readable; preserve the proportions of each component.
FIRST column: the complete bed alone, with its cream folded paper frame, low headboard at left and footboard at right, gold top edges, coral lower bands, white mattress, faceted mint-gray pillow at the head, and mint-gray blanket covering the foot two-thirds. Show in a clear three-quarter view from slightly above. Remove the curtain and the bedside lamp/plinth from this bed callout.
SECOND column: the complete folding THREE-PANEL paper privacy curtain alone, exactly three rectangular panels in the same shallow accordion configuration as the hero, mint-gray triangular facets, cream borders, coral lower bands, slim gold hinge details and folded cream base supports. Show the full panel set in a clear slightly elevated three-quarter view, all three panels completely visible. Preserve three panels, never four.
THIRD column: the bedside lamp alone as a large readable close-up, same faceted cream shade with thin gold edges, glowing warm amber interior, angular cream-and-gold stem and polygonal base as in the hero. Lift it away from the bedside pedestal so only the lamp is shown.
FOURTH column: one structural cream paper fold tab from the base of the hero as a large isolated close-up. Show its simple triangular gusset / tent-fold support geometry, folded flat attachment flap, visible crease and slight paper thickness. This is an actual buildable folded paper support, not a symbol or arrow. Show in three-quarter view so the folded construction is readable.
Style: clean buildable low-poly papercraft with flat-shaded polygon facets, soft bevels, matte paper, slight paper thickness and fold lines, restrained gold-foil details. Palette wardgray #B9CFC8, cream #FFF3DE, coral #FF7A6B, lamp light #FFC968, white #FFFFFF. Match the hero exactly.
Background: plain perfectly uniform flat light grey #E6E6E6, no floor or horizon, no cast shadows on the background. Soft neutral studio shading on component surfaces only.
Full assembled model reference proportions are W:D:H = 3:2:2.4 (3 m by 2 m by 2.4 m); do not distort the component shapes while isolating them.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, divider lines, dimension lines, people, logos or watermarks anywhere. No additional items or repeated parts. Exactly the four specified callouts in the specified order in one row.
```

