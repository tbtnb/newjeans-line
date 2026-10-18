# Exact image generation prompts

Generated with the built-in image_gen tool, one call per row in spec.tsv order. transparent_background was false for every call.

## hero.png

Reference: ./style-ref.jpg

```text
Use case: stylized-concept.
Create one square 1:1 MODELING DESIGN SHEET hero image for a buildable low-poly game asset in the fan-made Dancing Line style level "Bunny Pop-up Storybook".
Input image: style-ref.jpg is an approved world render, used ONLY as the art style reference. Extract its sculpted low-poly papercraft, broad flat-shaded facets, soft tiny bevels, matte paper with visible slight thickness, restrained fold lines and gold-foil accents. Do not reproduce the environment.
Subject: one isolated "Hanging Crescent Moon": a crescent moon made of layered pale-gold paper hanging on a fine string with exactly two tiny paper stars. Overall real assembled bounding dimensions including suspension string and stars are width 3 m, depth 0.4 m, height 4 m; maintain exactly W:D:H = 3:0.4:4. The crescent is a shallow solid paper construction with clearly buildable polygonal outlines and simple planar triangulated surfaces, sharp tapered horns opening to the right, neatly stacked contour layers and a few subtle fold creases. Use pale gold #F7D98B for its main face, cream #FFF3DE for exposed paper layers and sparse moon blue #BFD4F5 for a recessed backing layer. Thin restrained gold-foil edge accents, no glow. Fine straight suspension string and exactly two little faceted five-point paper stars belong to the same single hanging assembly; make their physical connections unambiguous. Keep all components within the stated shallow depth.
Composition: show this single complete asset alone in a three-quarter view from slightly above, fully visible with generous margins, centered on a plain soft pale-cream gradient background. Soft studio lighting, gentle contact shadow only. Low-poly geometry must remain legible, no painterly smearing or complex surface decoration.
Hard rules: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, scenery, stands or other props.
```

## views.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create one landscape 3:2 ORTHOGRAPHIC THREE-VIEW PLATE for a modeller, of the exact hanging crescent moon model in the input hero.png. hero.png is the authoritative DESIGN reference; preserve the identical model, contours, triangulated folds, layer structure, colours and every physical detail. This is a technical turnaround of that asset, not a redesign.
Asset: "Hanging Crescent Moon", layered pale-gold paper crescent, opening to the right in front view, fine suspension string and exactly two hanging faceted five-point paper stars. Preserve the cream and sparse pale-blue recessed paper layers, thin gold-foil trim, gold polygonal connectors and tiny attachment loops seen in the hero reference. Preserve the two stars' differing suspension lengths and positions. Overall assembly real dimensions, including suspension and stars, are width 3 m, depth 0.4 m, height 4 m, exactly W:D:H = 3:0.4:4. Thin shallow low-poly construction, broad matte flat-shaded planar facets, soft tiny bevels, slight paper thickness and restrained fold lines. Palette gold #F7D98B, moon blue #BFD4F5, cream #FFF3DE.
Background: completely flat uniform light grey #E6E6E6, no floor, no horizon, NO cast shadows on the background, no ambient background gradient. Neutral even lighting only to distinguish geometry faces.
Layout: exactly three equal vertical thirds with no visible separators. LEFT third contains FRONT orthographic elevation. MIDDLE third contains RIGHT SIDE orthographic elevation, looking directly from the asset's right side, so its shallow depth reads as a narrow layered edge-on profile. RIGHT third contains TOP orthographic view looking straight down, so its shallow depth reads as a low horizontal strip. Absolutely true parallel orthographic projection in all views: no perspective, no three-quarter view, no camera tilt. All three views use exactly the SAME pixels per metre. Front and side have the same full height and stand on the same invisible baseline. Top view width equals front view width, and top view depth equals side view width. Center each projection within its own third with clear margins; nothing crosses a third boundary. Render the suspension string fully with its upper end visible inside the frame, never cropped. Use the exact hero design projected from each direction, accepting that the stars and string can overlap edge-on in side/top projections.
Hard rules: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, extra parts, scenery or extra views.
```

## parts.png

Reference: ./hero.png

```text
Use case: stylized-concept.
Create one landscape 3:2 DETAIL CALLOUT PLATE for a modeller building a low-poly papercraft game asset. Input hero.png is the authoritative design reference: preserve the exact crescent silhouette, individual polygonal facets, folded paper construction, layer colours, gold trim, string hardware and exactly two five-point paper stars. No redesign.
The asset is "Hanging Crescent Moon" from "Bunny Pop-up Storybook": assembled dimensions width 3 m, depth 0.4 m, height 4 m, exactly W:D:H = 3:0.4:4. Colours gold #F7D98B, moon blue #BFD4F5, cream #FFF3DE. Matte paper, shallow layered low-poly geometry, flat-shaded sculpted facets, slight paper thickness, restrained fold creases, soft tiny bevels and thin gold-foil edge accents matching hero.png. All details must be physically buildable.
Background: uniform flat light grey #E6E6E6, no floor, no horizon, no cast shadow on the background. Soft neutral studio illumination showing facet shapes.
Layout: ONE horizontal row with EXACTLY TWO equal-width columns, no drawn column dividers. Every part stays entirely inside its own column with clear margins.
LEFT COLUMN: the layered crescent only, opening to the right, enlarged three-quarter close-up from slightly above, with its pale-gold triangulated face, cream middle layer and pale-blue recessed backing. Show the three shallow crescent contour layers slightly exploded apart along their depth axis so the modeller can see thickness and assembly order, while keeping the original matching contours and the complete crescent visible. Do not add suspension strings or stars in this column.
RIGHT COLUMN: the string and stars assembly only, separated from the crescent. Show the main upper hanging cord with its original small gold faceted connector and tiny attachment loop, plus the two secondary straight cords and their original gold connectors and exactly two folded five-point paper stars. Arrange these related string components together as a single coherent callout group, with upper cord at top and two star drops beneath, using the same unequal drop lengths and the same relative star sizes as hero.png. No crescent body or detached crescent fragment in this column. Keep every cord end, connector and star fully visible, with ample margins.
Hard rules: absolutely NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos, watermarks, decorative props or additional parts.
```

