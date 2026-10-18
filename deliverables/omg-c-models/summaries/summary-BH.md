bunny-heart — 3213/4000 tris (80.3%; heart 1152); IoU front/side/top 0.846/0.812/0.926; size 6.5 × 6 × 10 m, delta 0%/0%/0%; simplifications: paper texture omitted, eight layered page leaves, pink face marks, principal gem creases retained, top-view ear placement follows front + hero.

Completed 12 rendered build/review iterations. Final raw front/side IoUs do NOT meet 0.90; top passes. This is a review candidate, not a claim of full silhouette acceptance. Final compare and metrics were both inspected after build 12.

Rebuilt from scratch with custom flat triangular meshes; no ico or smooth-shaded geometry. Thick solid folded ears have tapered backs and surface-conforming pink insets. Heart has a sharp cleft, central raised diamond, pointed tip and 1152 triangles. Face and sole patches follow the actual mesh planes. Gold cover rims and the central book hinge are geometry.

Palette/pivot audit: exact source hexes #FFF3DE, #FFF8EC, #FF6FAE, #FFC7DA, #FFFFFF, #F7D98B; zero smooth faces; four pivot groups (root 1733 tris, ears0 164, ears1 164, heart 1152); every mesh descends from root. Compressed GLB verified to preserve all four pivot names and vertex colours (101260 bytes, four meshes). See bunny-heart.BH-audit.json.

Remaining differences: ear footprint placement in the illustrated top view is wider/backward compared with front + hero; head and body facet layout is interpreted rather than traced one-for-one; the side body/book contour still differs. Reference-mask inspection also shows cream areas removed as background inside the forehead, ears, feet and pages. These interior losses penalize raw IoU independently of the outer contour. Diagnostics bunny-heart-front-difference.png and bunny-heart-side-difference.png use grey for overlap, magenta for design-only mask and cyan for model-only mask. Pipeline and designs were not changed.

| Iteration | Tris | Front | Side | Top |
|---|---:|---:|---:|---:|
| 1 | 3771 | 0.841 | 0.671 | 0.926 |
| 2 | 3255 | 0.842 | 0.810 | 0.926 |
| 3 | 3671 | 0.843 | 0.783 | 0.926 |
| 4 | 3231 | 0.842 | 0.782 | 0.926 |
| 5 | 3309 | 0.842 | 0.809 | 0.926 |
| 6 | 3369 | 0.842 | 0.808 | 0.926 |
| 7 | 3441 | 0.843 | 0.809 | 0.926 |
| 8 | 3337 | 0.847 | 0.810 | 0.926 |
| 9 | 3213 | 0.847 | 0.813 | 0.909 |
| 10 | 3213 | 0.846 | 0.809 | 0.926 |
| 11 | 3213 | 0.846 | 0.812 | 0.926 |
| 12 | 3213 | 0.846 | 0.812 | 0.926 |

Iteration 9 trialled 5.9 m depth; final uses the exact 6 m spec. Final version retains the controlled broad heart facets rather than iteration 8’s denser wrinkles.
