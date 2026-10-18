# Bubble Gum
Slug: `bubble-gum`

A glossy candy-pink gum cube carries a small inflated strawberry-milk bubble and a mint inset, leaving a solid pink gum ribbon with a soft white highlight and tiny mint-and-milk sprinkles. The cube remains clearly readable through each 90-degree turn; a compact bubble burst marks the tap, while death releases a wider cloud of translucent bubbles that expand into fading pop rings. Soft bevels, bright reflections, and a restrained five-color palette give this original skin a clean, cute Y2K casual-game finish.

## Exact palette

These are implementation colors; generated artwork contains shaded variations.

| Role | Hex | Use |
| --- | --- | --- |
| Head base | #F45C9D | Main opaque gum cube |
| Head accent / emissive | #A8E8CF | Small mint inset; subtle emission |
| Trail base | #F45C9D | Continuous solid ribbon |
| Trail edge / stitch | #D83F82 | Thin shaded lower bevel; continuous edge, no literal stitching |
| Burst particle 1 | #FFD6E5 | Strawberry-milk bubbles |
| Burst particle 2 | #A8E8CF | Mint-tinted accent bubbles |
| Death particle 1 | #F45C9D | Pink bubbles and occasional gum fragments |
| Death particle 2 | #FFD6E5 | Pale expanding pop rings |
| Picker UI accent | #A8E8CF | Selection border or indicator supplied by the UI |
| White gloss | #FFFDFE | Highlights and glints |

## Real-time materials

Recommended starting values for Babylon.js. Color multipliers below refer to linear intensity relative to the listed color. Set the cube width to 1 world unit for the particle values below.

| Part | StandardMaterial | PBRMaterial | Emission / alpha |
| --- | --- | --- | --- |
| Head gum | Diffuse head base; white specular at 0.85; specularPower 96 | Albedo head base; metallic 0; roughness 0.20; clear-coat intensity 0.8, roughness 0.12 | Base-colored emission 0.02; alpha 1 |
| Mint inset | Diffuse mint; white specular at 0.65; specularPower 72 | Albedo mint; metallic 0; roughness 0.24 | Mint emission 0.10; alpha 1 |
| Trail | White diffuse multiplier with trail.png; white specular at 0.60; specularPower 80 | White albedo multiplier with trail.png; metallic 0; roughness 0.25; clear-coat intensity 0.5 | Pink emission 0.015; alpha 1 |
| Attached bubble | Diffuse strawberry milk; white specular at 1.0; specularPower 128 | Albedo strawberry milk; metallic 0; roughness 0.10 | Emission 0.025; alpha 0.42 |
| Bubble sprites / rings | Unlit or softly emissive, particle.png with texture alpha | Unlit alpha-blended sprite material | Emission 0.15–0.25; per-particle alpha 0.55–0.85, fading to 0 |

Use a lightly bevelled cube, roughly 0.05 units at the edges. The attached bubble should be approximately 0.30 cube widths in diameter. Keep the trail opaque and its width constant through a mitered 90-degree corner. Use alpha blending for bubbles, not alpha testing; preserve their soft edges. Keep transparent bubble geometry separate from opaque head geometry.

Repeat trail.png in both U and V using wrap addressing. Map U along each straight trail segment; rotate the UV direction with the path after a turn. Start at one repeat per 3 cube widths of path and one repeat across the bar. Its gloss streaks are already painted in, so keep environment reflections soft. Use a white texture multiplier to avoid doubling the pink tint. Use mipmaps and linear filtering.

## Particle behavior

All counts are one-shot emissions per event; gravity vectors use Y as up.

| Event | Count and shape | Size in cube widths | Lifetime | Motion and gravity |
| --- | --- | --- | --- | --- |
| Tap / turn | 8 single bubble billboards: 6 milk-pink, 2 mint | 0.08–0.18; grow to 1.25× | 0.22–0.38 s | Radial outward speed 0.5–1.2 units/s, upward speed 0.25–0.55; gravity (0, 0.15, 0) |
| Death bubbles | 22 bubble billboards in the two death colors | 0.12–0.34; grow to 1.6× | 0.45–0.80 s | Radial speed 1.2–2.8 units/s, upward speed 0.4–1.0; gravity (0, 0.25, 0) |
| Death pop rings | Convert 6 of those bubbles into thin open rings | Start at bubble diameter; expand to 1.8× | Final 0.12–0.18 s of bubble lifetime | Inherit drift, then fade quickly; no added gravity |
| Optional gum shatter | 6 small bevelled mesh chips in pink, secondary to the bubbles | 0.04–0.09 | 0.30–0.50 s | Outward speed 1.0–2.0 units/s; gravity (0, -3.0, 0) |

Use particle.png as a single bubble, never as a multi-particle atlas. Apply multiplicative color tint gently so its white gloss stays readable. Keep full initial alpha for about 40% of a bubble's life, then ease to zero. Pop-ring geometry is a simple runtime annulus using the same palette; it needs no additional image. If using only billboards, finish with a quick scale-up and alpha fade, with a less explicit ring silhouette. Keep bursts below the moving cube's top plane whenever possible so the next corner remains visible.

## Deliverables and verification

- concept.png: 1536 × 1024, RGB, landscape 3:2 concept sheet with five unlabelled swatches.
- trail.png: 1254 × 1254, RGB, square repeating surface texture. Opposing-edge mean absolute RGB differences are approximately 1.4/2.1/1.9 horizontally and 0.9/1.9/2.3 vertically on a 0–255 scale; close edge continuity, not an assertion of identical edge pixels.
- particle.png: 1254 × 1254, RGBA. PIL verified all four corner alpha values are 0; visible bubble bounds at alpha ≥ 32 occupy approximately 85% of the image width.
- icon.png: 1254 × 1254, RGBA. PIL verified all four corner alpha values are 0.
- design.md: this art specification and exact generation prompts.

All four images were made with the built-in image_gen tool, one call per image, and copied unchanged from $CODEX_HOME/generated_images to the requested filenames. Native transparency passed verification, so no solid-magenta fallback or regeneration was needed. No additional deliverable files were created. The five-color sheet is a visual guide; the hex table above is authoritative for runtime colors.

## Exact image_gen prompts

### concept.png

Transparent background parameter: false.

```text
Use case: stylized-concept
Asset type: original casual rhythm-game skin concept sheet, landscape 3:2 (1536x1024).
Primary request: A cohesive bubblegum-pop skin for a tiny moving cube that leaves a solid bar trail and turns at right angles. Clean pale strawberry-milk background. Large hero at left: glossy candy-pink rounded-edge CUBE in 3/4 isometric view, still clearly cubical, with a small inflated translucent pale-pink gum bubble attached to its upper front corner, a broad white gloss highlight, and a tiny mint accent inset. No face. At upper right: thick solid pink gum ribbon/bar, a single connected 90-degree corner, isometric view, uniform width, rounded bevels, pale gloss streak along its top and sparse tiny mint and strawberry-milk sprinkles. Lower middle: a compact tap-turn burst of a few translucent pink bubbles and mint glints. Lower right: a larger death burst of translucent pink bubbles, several open circular bubble-pop rings, a few small pink gum fragments. Bottom: a tidy row of exactly five flat unlabelled color swatches.
Style/medium: polished clean cute Y2K-pastel 3D casual-game art, crisp silhouettes, soft gradients, controlled toy-like reflections, airy clear spacing, delicate contact shadows.
Palette: hot candy pink #F45C9D, strawberry milk #FFD6E5, mint #A8E8CF, white gloss #FFFDFE, deep rose pink #D83F82. Use these five in the swatches.
Constraints: all objects separate and clearly legible; head and ribbon shown as game assets, no environment. Original design only. Absolutely NO text, letters, numbers, labels, logos, brand marks, watermark, people, human faces or likenesses.
```

### trail.png

Transparent background parameter: false.

```text
Use case: stylized-concept
Asset type: square seamless tileable game texture, 1024x1024, for the TOP SURFACE of a solid gum trail bar.
Primary request: An edge-to-edge flat candy-pink glossy gum-ribbon surface texture with sparse tiny strawberry-milk and mint sugar sprinkle dashes and subtle soft lighter-pink highlight streaks. Fine restrained detail; predominantly smooth hot candy pink. The highlight streaks are thin, soft and horizontal, distributed evenly and extend naturally through side edges. Sparse tiny rounded mint and pale milk-pink sprinkles, all similarly small and evenly distributed. A flat planar albedo texture, orthographic top-down, uniform color and illumination.
Palette: base #F45C9D, gentle pale pink #FF9BC4 gloss streaks, occasional #FFD6E5 and #A8E8CF sprinkles, tiny #FFFDFE highlights.
Style: clean cute Y2K-pastel casual game, crisp small sprinkles, soft restrained gradients, glossy candy impression.
Critical constraints: perfectly SEAMLESS repeat in BOTH x and y directions, all four edges match their opposite edge; no borders or seams. Square entire canvas filled with the texture. NO perspective, vignette, cast shadow, directional shading gradient, central focal object, 3D cube, trail silhouette or ribbon outline, particles, bubble shapes, text, letters, numbers, logos, brand marks, watermarks, people or faces. Original design only.
```

### particle.png

Transparent background parameter: true.

```text
Use case: stylized-concept
Asset type: square transparent game particle sprite, 1024x1024, readable at 32 pixels.
Primary request: ONE single centered round soap/gum bubble, diameter approximately 80% of the canvas. A simple bold circular silhouette with a moderately thick pale strawberry-pink pearlescent rim and a very faint translucent pale-pink interior. One integrated broad white curved gloss highlight at upper left, a smaller integrated white glint at lower right. Clean smooth circular outline, uniform line thickness, simple strong silhouette. Light/white-ish tones suitable for color tinting in a game. Pink rim #FFD6E5, white gloss #FFFDFE, very faint pink interior.
Background: genuine transparent alpha, completely transparent corners and all space outside the ONE bubble; translucent interior.
Style: cute clean Y2K-pastel casual-game sprite, soft glossy shading only inside the bubble, crisp edges.
Constraints: exactly ONE bubble only, centered with generous equal margins. No secondary bubbles, separate sparkles, decorations, cast shadow, ground, scenery, checkerboard pattern, square backdrop, letters, words, numbers, logos, brand marks, watermarks, people or faces. Original design only.
```

### icon.png

Transparent background parameter: true.

```text
Use case: stylized-concept
Asset type: square transparent skin-picker UI thumbnail icon, 1024x1024, must read clearly at 64 pixels.
Primary request: One glossy candy-pink gum CUBE with lightly rounded bevelled edges, shown in 3/4 isometric view, with a small inflated translucent pale strawberry-pink bubble attached to its upper right/front edge. The head cube is the main shape, with a broad curved white gloss highlight on top and a single tiny mint lozenge inset on its visible front side, absolutely no face. A short thick solid pink trail stub extends behind the cube toward the upper-left, with a soft pale top highlight and only two tiny mint sprinkles. The bubble is small, about one-third of cube width. Cohesive centered compact silhouette; entire cube, bubble and short trail visible and collectively fill 80–85% of frame; comfortable clear padding. No extra objects.
Style: original clean cute Y2K-pastel casual-game 3D icon, crisp bold geometry, soft gradients, strong candy gloss, clear separation of top and two side planes, readable small.
Palette: candy pink #F45C9D, deep rose edge #D83F82, strawberry milk #FFD6E5, mint #A8E8CF, white gloss #FFFDFE.
Background: actual transparent alpha everywhere outside the subject, fully transparent corners; no background, ground plane, cast shadow, glow halo, badge, border or frame.
Constraints: no text, letters, numbers, official logos, brand marks, watermarks, people, human faces or likenesses. Original design only.
```

