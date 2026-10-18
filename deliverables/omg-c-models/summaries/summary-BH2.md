# BH2 — bunny-heart refinement

bunny-heart: **3515/4000 tris (87.875%)**; **IoU front/side/top 0.950/0.922/0.927**; **6.5 × 6.0 × 10.0 m**, size delta **0% / 0% / 0%**; pivots **ears0, ears1, heart, root**; simplifications: paper grain omitted, stacked page leaves, tiny pink face marks, principal gem folds, top ear placement interpreted from front/hero.

## Iterations

All measurements use the unchanged v3 compare.py design mask. Iteration 00 is the supplied BH1 baseline. Every successful geometry iteration was built, its compare sheet opened, and its metrics read. Sources, raw GLBs, renders, metrics and compare sheets are archived as `build/bunny-heart.BH2-NN.*`.

| Iteration | Tris / 4000 | Use | Front IoU | Side IoU | Top IoU | Size delta W/D/H | Decision |
|---|---:|---:|---:|---:|---:|---|---|
| 00 | 3213 / 4000 | 80.33% | 0.957 | 0.898 | 0.927 | 0% / 0% / 0% | BH1 baseline, untouched backup; side below requested 0.92. |
| 01 | 3211 / 4000 | 80.28% | 0.949 | 0.862 | 0.927 | 0% / 0% / 0% | Rejected: excessive rump/foot depth, side silhouette too broad. |
| 02 | 3215 / 4000 | 80.38% | 0.956 | 0.923 | 0.927 | 0% / 0% / 0% | First all-view pass; corrected side proportions, fuller feet and head depth. |
| 03 | 3491 / 4000 | 87.28% | 0.954 | 0.921 | 0.927 | 0% / 0% / 0% | Larger pink ear panels, wider gem and additional triangular folds; rejected pale crown facets. |
| 04 | 3491 / 4000 | 87.28% | 0.954 | 0.923 | 0.927 | 0% / 0% / 0% | Removed pale heart patches; rebuilt bow on right neck in the YZ plane; balanced gem point. |
| 05 | 3515 / 4000 | 87.88% | 0.954 | 0.922 | 0.927 | 0% / 0% / 0% | Rounder crown and extra rump ring; rejected exaggerated heart microfolds. |
| 06 | 3515 / 4000 | 87.88% | 0.954 | 0.922 | 0.927 | 0% / 0% / 0% | Retained crown/rump; gentler gem facets and slightly narrower torso so heart reads wider. |
| 07 | 3515 / 4000 | 87.88% | 0.950 | 0.922 | 0.927 | 0% / 0% / 0% | SELECTED: widened ear middles 6%; all target IoUs pass and enlarged pink insets retained. |

## Final result and simplifications

- Preserved the BH1 sharp, flat paper construction and exact palette inputs. Spec hexes are unchanged; the existing shared `paper #FFF8EC` tone is retained for cream facet variation. No custom darkening or smooth shading.
- Added a rear rump section and a fuller crown; increased head depth and height, enlarged forward feet, kept pink pads attached to the actual foot facets, and moved hugging paws with the thicker gem.
- Heart is 4.23 m wide versus the main torso’s approximately 4.10 m; the two front lobe apices, centre ridge, bevel and added triangular folds are real geometry. Heart depth is approximately 2.02 m, versus 1.94 m in BH1. No glow, texture, or drawn crease lines.
- Ear middles are wider, pink insets cover substantially more of the front faces, and both ears remain solid folded shells with independent joint pivots. The right-neck bow now spreads fore/aft so it reads in side and top views.
- **Drawing compromise:** the top drawing places the ears much farther toward the book’s rear than their side projection allows. Ear placement therefore prioritizes front + hero and the side silhouette. The final top-view ear interiors remain more foreshortened than the top reference. Top IoU includes the book outline and does not measure internal feature placement.
- **Other simplifications:** no paper grain or printed page rules; pages use eight stacked leaves per half; tiny face marks use palette pink; gem microfacets are grouped around the principal creases rather than reproducing every illustrated triangle. Lighting remains the unmodified pipeline bake.
- The design silhouettes have aspect ratios approximately 0.658/0.559/1.000; the required physical dimensions imply 0.650/0.600/1.083. The exact-size constraint is retained, accounting for the remaining side/top aspect difference.

## Final verification

`npm_config_offline=true tools/models/build.sh bunny-heart` completed successfully. The final compare sheet was visually inspected. A separate GLB header/JSON audit verified 3515 exported triangles, all four named pivots, the reported dimensions, and all three IoUs >= 0.92. Receipt: `build/bunny-heart.BH2-final-audit.json`.

Final files: `tools/models/assets/bunny-heart.py`, `public/models/omg-c/bunny-heart.glb`, `deliverables/omg-c-models/bunny-heart-compare.jpg`. The selected source is also archived at `build/bunny-heart.BH2-07.py`.
