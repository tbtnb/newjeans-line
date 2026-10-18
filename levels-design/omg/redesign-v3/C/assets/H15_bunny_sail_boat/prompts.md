# Exact image generation prompts

## 1. hero.png

Reference image: ./style-ref.jpg

```text
Use case: stylized-concept.
Create ONE square 1:1 modeling design sheet hero render of a single asset, the Bunny-Sail Paper Boat, for the fan-made rhythm game level Bunny Pop-up Storybook.
Input image: style-ref.jpg is the approved world STYLE reference only. Match its sculpted low-poly papercraft, flat-shaded facets, soft bevels, matte paper, subtle paper thickness and clear fold lines, pastel colours, restrained gold-foil accents. Do not reproduce the environment.
Subject: a clean, buildable folded paper boat with a single bunny-head-shaped paper sail on a simple mast, and one small glowing lantern fixed at the bow. Overall real dimensions W:D:H = 3:1.4:3 metres exactly. Define width X as the long bow-to-stern hull axis, depth Y across the narrow hull, height Z from keel to ear tips. The broadside FRONT is the X-Z plane; the bow is at the right end in the front view. Sail lies in the X-Z plane. Keep the entire assembled silhouette as tall as its hull is long.
Hull: a simple open origami boat, pointed bow and stern, angular folded triangular sides, visible inner paper surfaces, pearl exterior and lilac interior/fold panels, slim gold-foil upper rim, a few large clean planar facets with bevelled edges. No fussy decoration.
Sail: one continuous bunny-head silhouette with a broad angular round head and two upright long polygonal ears, pearl paper with lilac inset ear panels and subtle moon-blue fold facets. Faceted shallow folded paper construction, slight actual edge thickness, no face, eyes, nose, mouth or symbol. A single simple slender gold mast behind the sail, rising from the middle of the hull; coherent visible connection.
Lantern: small buildable faceted hexagonal lantern mounted at the right-hand pointed bow, gold frame and cap, warm lamp-coloured glowing panels. Gentle contained glow.
Exact palette: pearl #F3F1EA, lilac #E3D7FA, moon #BFD4F5, lamp #FFC968, gold #F7D98B.
Composition: single fully assembled asset alone, three-quarter view from slightly above, showing broadside, hull interior and paper thickness. Show the entire object including ears, keel and lantern, centred with generous margins. Soft studio lighting, gentle contact shadow, plain soft pale-cream gradient background.
This is a modeller's geometry reference: readable large polygon planes, no fuzzy edges, no impossible floating connections, no painted illusion of structural pieces. No scenery, water, display plinth or extra objects. Absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

## 2. views.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW modeling plate of the exact Bunny-Sail Paper Boat shown in the supplied hero.png reference image. The reference is the authoritative asset design; preserve its geometry, colours, fold pattern, bunny-ear shape, pearl and lilac hull, gold rim, gold mast with faceted finial and collars, and the small warm lantern at the right-hand bow. No redesign.
Canvas: 1536 by 1024, landscape 3:2. Entire background is uniform flat light grey #E6E6E6, with no floor, horizon, cast shadow or ambient vignette. Three equal invisible vertical thirds, each 512 pixels wide. Exactly ONE view in each third. Nothing crosses between thirds. No visible dividers.
LEFT third: true orthographic FRONT view of the boat's broadside, showing its full long hull and bunny silhouette face-on, bow lantern at the right. Camera looks horizontally toward the X-Z plane, no view down into the hull.
MIDDLE third: true orthographic SIDE view seen from the RIGHT, looking horizontally along the hull's length directly at the bow. This is a narrow end-on boat view: the lantern is in front, mast behind, bunny sail appears edge-on as a thin folded paper section, never as a second face-on bunny. No perspective, no three-quarter angle.
RIGHT third: true orthographic TOP view, camera straight down along Z. Show the open long diamond-shaped origami hull interior, mast cross section, bow lantern top, and the thin sail seen from directly above as its actual narrow folded edge. Do not tilt the sail toward the camera to show its face.
Geometry axes and exact proportions: overall width X (long bow-to-stern axis) = 3 m, depth Y (narrow beam) = 1.4 m, height Z (keel to highest tip) = 3 m. Front overall bounding rectangle is 3 wide by 3 tall. Right side overall bounding rectangle is 1.4 wide by 3 tall. Top overall bounding rectangle is 3 wide by 1.4 tall. Use exactly the SAME pixels-per-metre scale in ALL THREE views: front and top widths equal, front and side heights equal, top depth equals side width.
Precise layout guide, invisible in image: each object's view centered horizontally at x=256, 768, 1280 respectively. Front and side each 420 pixels tall, spanning y=300 to y=720, with the same baseline at y=720. Front is 420 pixels wide; side is 196 pixels wide. Top is 420 pixels wide by 196 pixels deep and centered around y=510. Keep margins on all sides. Preserve the exact asset proportions rather than enlarging the side view to fill its column.
Material and shading: sculpted low-poly papercraft with real thin paper edges, crisp folds, broad flat-shaded facets, subtle bevels and matte paper, restrained gold foil. Exact palette pearl #F3F1EA, lilac #E3D7FA, moon #BFD4F5, lamp #FFC968, gold #F7D98B. Neutral soft material illumination only, warm lantern panels with contained glow but no background light spill.
Technical orthographic turnaround, clean and buildable as real low-poly geometry. Entire asset visible in each view. Absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery or extra objects anywhere.
```

## 3. parts.png

Reference image: ./hero.png

```text
Use case: stylized-concept.
Create ONE landscape 3:2 DETAIL CALLOUT PLATE for a low-poly modeller. Use the supplied hero.png as the authoritative reference: this must be the SAME Bunny-Sail Paper Boat broken into exactly four separate key component assemblies. Preserve the reference's design, colours, folds, faceting and details.
Canvas 1536 by 1024, landscape 3:2. Uniform flat light grey #E6E6E6 background throughout. No floor, horizon, cast background shadows, vignette or extra objects. Exactly ONE horizontal row of four parts, left to right, each centred in its own equal invisible column of width 384 pixels. Column centres x=192, 576, 960, 1344. Parts separated by generous negative space; nothing crosses column boundaries. No visible grid or dividers. Centre each part vertically around y=512; use independent close-up scales so each shape is readable with margins.
LEFTMOST column: BUNNY-HEAD SAIL only, detached from mast. Show the reference's complete continuous faceted pearl bunny head and two upright long angular ears with lilac inner panels and pale moon-blue fold facets. Face-on with a very slight three-quarter turn to reveal shallow folded thickness. No facial features. No mast, boat or lantern in this column. Preserve the exact bunny outline and panel design.
SECOND column: FOLDED HULL only, detached from sail, mast and lantern. Three-quarter view slightly above to clearly show the open lilac folded interior, pearl exterior triangular facets, slim gold-foil upper rim and pointed ends. Long narrow origami hull, width-to-depth 3:1.4; preserve the exact reference hull construction and fold pattern. No sail or mast remnants.
THIRD column: BOW LANTERN only, detached. A close-up three-quarter view of exactly the small gold-framed glowing lantern from the reference: faceted warm lamp panels, polygonal tapered body, low pyramidal gold roof, diamond finial, gold base and small mounting foot. Restrained glow confined to the luminous panels. No hull, rope, mast or added stand.
RIGHTMOST column: MAST only, detached. The full simple slender straight gold polygonal mast from the reference, including its diamond-shaped faceted top finial, matching square collars and plain bottom mounting end. Show the full height, slight three-quarter view, clean buildable geometry. No sail, hull or lantern. Do not invent ropes, rigging, extra beams or complex hardware.
Style: match hero.png and its sculpted low-poly papercraft world, flat-shaded broad facets, soft bevels, matte paper with slight physical paper thickness and fold lines, restrained gold-foil accents, pastel colours. Exact palette pearl #F3F1EA, lilac #E3D7FA, moon #BFD4F5, lamp #FFC968, gold #F7D98B. Neutral soft studio material lighting without cast shadows on the background.
The four columns together are ONE clean modeling parts sheet, no assembled boat or duplicate parts. Absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```

