# 提示词模板（摘自 omg-design-v3 实际使用过的 prompts.md）

> `<...>` 为要替换的内容。完整原文见 `levels-design/omg/redesign-v3/C/assets/<id>/prompts.md`、`C/prompts/zNN.md`、`deliverables/omg-c-paint/prompts.md`。

## 1. 区域 key 渲染（C/prompts/z04.md，References: ./style-ref.jpg, ./cam-ref.png）
```text
Use case: stylized-concept.
Purpose: DESIGN-STAGE approval render for a fan-made Dancing Line style mobile rhythm game, song <SONG>, concept <C> "<Bunny Pop-up Storybook>". Do not put any of these words in the image.
Style reference: the provided style-ref.jpg is the approved visual language. Match its sculpted low-poly pop-up book world closely: <主题材质与形状语言>. Every object must feel buildable as an actual low-poly 3D mesh. Chunky sculpted miniature diorama, flat-shaded facets, softly bevelled edges, matte and satin materials with a few glossy accents. Paper is a physical folded material with thickness, creases and dimensional construction; never a flat illustrated sticker. ...
Zone <N> palette and mood: "<区名>", <段落情绪>. <hex 色板>. ...
HARD CONSTRAINTS: no people, no human figures, no human faces, no likeness of any real person. Bunny sculptures have blank faceted faces as in the reference. Absolutely no text, letters, numerals, logos, signatures or watermarks anywhere; any flags or signs are blank or only heart silhouettes. No UI. No photorealism. No flat 2D sticker cut-outs ...
Asset type: IN-GAME KEY RENDER. One image, portrait 2:3.
Reference roles: image 1 style-ref.jpg controls art style ... Image 2 cam-ref.png controls ONLY the high camera angle, road-to-cube scale and right-angle zig-zag geometry; completely ignore image 2's art style, props, decorations, UI and text.
Camera and route: high three-quarter top-down view, looking down about 60 degrees and looking forward along the route, exactly like a Dancing Line mobile screenshot. A SINGLE wide, continuous, unbranched <road material> zig-zags in successive RIGHT-ANGLE steps from the bottom edge to the top of frame through the middle. ... Road width about 2.3 times the width of its small square line head. ... The <road> is the brightest, clearest element and its upcoming turns remain unobstructed. No scenery on the driving surface. Keep a clean 1–2 road-width margin beside the road free of tall props so the road and head read instantly.
Scene: <主件1> stands beside the road in the middle distance. Opposite it, <主件2>. Both landmarks stay lateral to the route. <天空/灯串/远景>.
Density: richly layered, element-rich diorama like the approved reference. Fill foreground ... OFF the clean route corridor with <地被>. Repeat <中景> in rhythm along both sides beyond the route margins. Large pop-up landmarks rise from outer page edges. ... Design coherence and gameplay readability take priority over confetti density.
```
> 注意：当时 key 图里线头在“lower third”。游戏现在把线头固定在离顶部 42%（用户要求），新出 key 图时应改成线头在画面中部偏上，避免设计和游戏取景不一致。

## 2. 单件 detail 渲染（z04-d1-castle）
```text
Asset type: DETAIL RENDER. One image, landscape 3:2. One key set-piece model only, centered and fully visible in a three-quarter elevated asset-presentation view, with generous breathing room. Plain soft <背景渐变> gradient background and a simple studio ground with soft contact shadow; no surrounding level, road, UI or separate scene props.
Subject: <详细形体、材料、颜色、可动结构如何弹出>.
```

## 3. 资产 hero（3/4 插图，H02 hero.png，Reference: ./style-ref.jpg）
```text
Use case: stylized-concept.
Create exactly ONE square 1:1 modeling design sheet image for the single asset <ID>, <Name>, for the rhythm game level <Level>.
Input image: style-ref.jpg is a STYLE REFERENCE only. ... Isolate the requested asset; do not reproduce the environment.
Subject: <形体>. Clear clean buildable low-poly geometry, modest polygon count, broad planes, solid closed volumes, separate simple paper-layer pieces. Use <name #hex> for <part> ...
Proportions: complete asset including base has exact bounding dimensions width <W> m, depth <D> m, height <H> m; W:D:H = <W:D:H>. ...
Composition: SINGLE asset alone in a three-quarter view from slightly above, fully visible with generous margins on every side. Square 1:1 canvas. Soft studio light, gentle contact shadow, plain soft pale-cream gradient background. ...
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere in the image.
```

## 4. 正交三视图（H02 views.png / H01 prompts-views2.md，Reference: ./hero.png）
```text
Create exactly ONE landscape 3:2 ORTHOGRAPHIC THREE-VIEW MODELING PLATE of the same <Name> shown in the input hero.png. The input is the authoritative reference ... Reproject this same model; do not redesign or embellish it.
True orthographic projection, NO perspective, NO three-quarter views. Exactly three equal vertical thirds with invisible boundaries: LEFT third FRONT view ...; MIDDLE third SIDE view looking from the <asset>'s RIGHT side; RIGHT third TOP view looking straight down. ...
The complete asset including base has exact W:D:H = <..>. Use IDENTICAL uniform world-to-image scale in all three views. Front and side must share exactly the same baseline and height; ... The top view is naturally much shorter than the two upright views: do not enlarge it to fill its column. ... front toward the bottom of the image.
... Flat uniform light grey #E6E6E6 background. NO floor, NO horizon, NO cast or contact shadows on the background, NO vignette.
Hard exclusions: NO text, letters, numbers, labels, arrows, grid lines, dimension lines, people, logos or watermarks anywhere.
```
重出版（views2）额外写：“The top view must NOT show a front elevation or front vertical faces”、“Do not enlarge the side view to fill its slot or shrink the top view independently”、无粒子/特效/分离装饰。

## 5. 部件特写（H02 parts.png）
```text
Create exactly ONE landscape 3:2 DETAIL CALLOUT MODELING PLATE of the <Name> from the input hero.png. ... separate component studies of that same low-poly model, not new designs.
Layout: exactly FOUR isolated component groups arranged in ONE horizontal row ... First column: <部件1> ... Nothing crosses between columns. All four complete silhouettes visible and uncropped.
```

## 6. 无缝地面贴图（deliverables/omg-c-paint/prompts.md z01-ground）
```text
Asset type: final seamless square ground texture for <game>, <zNN>-ground.png.
Create ONE square 1:1 texture, camera exactly vertically overhead, orthographic, flat ground surface filling the entire image. <内容>. Match the <mood> palette of the viewed <zNN>-key.jpg: <颜色>. ... quiet carpet suitable for gameplay. No single focal object.
CRITICAL: truly seamless repeating texture in BOTH axes. Opposite left/right and top/bottom edges must have matching colors, density, texture and continuing motifs ... no center glow, no corner darkening, no vignette, no border ...
Hard exclusions: NO people ... roads or paths. No landscape scene, trees, hills, buildings ...
```

## 7. 全景背景（z01-backdrop）
```text
Generate ONE image in the widest available landscape aspect, aiming for a very wide 4:1 panorama. ... The upper TWO THIRDS of the entire image is open <sky>. The distant scenery is strictly confined to the BOTTOM THIRD ... Keep the left and right edges at identical sky colors and matching low hill heights and tones so the panorama blends when wrapped.
```
