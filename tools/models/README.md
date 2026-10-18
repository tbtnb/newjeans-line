# OMG-C modelling pipeline (concept C 兔子立体童话书)

Real low-poly papercraft meshes, built by Python (Blender bpy, headless) per asset, exported as meshopt-compressed .glb.

- Blender: 4.5.14 LTS official Linux tarball at `/workspace/tools/blender` (box; the Mac mini has no Blender). Headless Workbench + Cycles render work on the box (software GL).
- `tools/models/paper.py` – modelling kit: box/cyl/cone/ico/lathe/prism(paper cut-out)/card/blade + outlines (heart, star, ear, ellipse);
  flat per-face colours (`Col`, sRGB) from the zone palette; `bake_light()` bakes a fixed paper light (sun + sky + height AO) into the
  vertex colours (engine renders unlit, no realtime shadows); meshes are joined per pivot (`pivot_<name>` empties = animated parts).
- `tools/models/assets/<id>.py` – one script per asset: `build(P, spec)`; `BUDGET` = tri budget (spec.json `tris_budget` overrides).
- `tools/models/run.py` – Blender entry: build -> finalize (join/bake/count) -> raw glb + ortho front/side/top + iso renders + report json.
- `tools/models/build.sh <id>...` – run.py -> `gltfpack -cc -kn -km` (meshopt, named pivots kept) -> `public/models/omg-c/<id>.glb`
  -> `compare.py` -> `deliverables/omg-c-models/<id>-compare.jpg` (design three-view sheet from
  `levels-design/omg/redesign-v3/C/assets/<id>/` (front/side/top images, or sheet + spec.views crop boxes) above the model's renders;
  falls back to the zone render named in `tools/models/specs/<id>.json` until the sheet lands).

Conventions: metres, Blender Z-up, model front faces -Y, base on z=0. glTF export is Y-up; vertex colours are COLOR_0 (linear).
