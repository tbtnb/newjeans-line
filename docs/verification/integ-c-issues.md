# integ-c: integration notes and blockers (supernatural, how-sweet, bubble-gum, right-now)

Branch `integ-c` from `origin/rebuild` f80704c. Only per-song files touched; no engine code changed.
All playthroughs here are **scripted simulation** (tools/qa/play.mjs, CDP touch events at chart times, headless
Chrome + SwiftShader, `--quality low --scale 1.5`), not physical-device play and not proof of A/V sync.

## Pipeline used (same as OMG/the rebuild worker-design path)
1. `levels-design/<slug>/{chart,layout}.json` (designs-w4 a9a816b, byte-identical to rebuild f80704c) copied to `levels-src/<slug>/`.
   Taps (times, dirs) and layout (route geometry, elevation, landmarks, eggs, camera, diamonds/crowns) are unchanged,
   so How Sweet keeps its hand-reworked route (73 validator multi-level crossings). The route is NOT regenerated
   (route.py / ditto.py are Ditto-specific; regenerating would replace the designers' routes).
2. Art: `levels-design/<slug>/art/` from `origin/art-codex` (8b6ef1c; Codex GPT-6.1-Sol high) -> `levels-src/<slug>/art/`
   (hash-checked against 8b6ef1c). Supernatural and Bubble Gum use the regenerated Codex files (newer than rebuild's overlay).
3. `tools/charts/follows_from_reports.py <slug>`, then a manual `follows` for sections whose chart-report.md row says
   "shared pattern of <earlier section>" or where the keyword mapper picked the wrong band (marked `follows_src`).
   Metadata only; engine ignores it.
4. `chartlogic.py` -> `docs/verification/chartlogic/<slug>.md`; `levels-design/validate.py <slug> --dir levels-src`.
5. `node tools/build-levels.mjs <slug>` -> `src/levels/<slug>.json`; vite build; play.mjs + snap.mjs under `flock /workspace/.nj-heavy.lock`.

## Issues / blockers for the integrator
- **public/levels/<slug>/art is not tracked** (gitignored-by-convention: rebuild does not track public/levels/ditto either).
  The Pages deploy must run `node tools/build-levels.mjs` before `vite build`, or level art (backdrops, ground, posters) will 404
  and fall back to procedural. I followed the rebuild convention and did not commit public/levels.
- **right-now: analysis grid is at 2/3 tempo** (`analysis/right-now.grid.json` 114.79 BPM; song is 172 BPM per the W4 report).
  chartlogic flagged 210/411 taps off-grid against it. I added `meta: {bpm:172, beat0:0.335}` to levels-src/right-now/chart.json
  (extra key, ignored by the engine); chartlogic then reports 0 off-grid. The analysis file is shared and was not modified.
- follows_from_reports.py keyword mapper mis-maps some rows (e.g. "same drum figure as the Groove ... vocal phrases sit on top"
  -> vocal; "sample hits ... no drums yet" -> drums). Corrected per song via manual follows (see chart.json `follows_src`).
- Menu shows a toast `关卡数据缺失：attention` in my partial build (only ditto + my 4 levels are built in this tree). Expected; not a bug in the final 16-level build.
- Snapshots are static `?debug` preview frames (NOT motion), software-rendered (~14 fps in play).
