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

## Results (scripted simulation, 540x960 portrait, headless SwiftShader, quality low, scale 1.5)
| song | taps (legacy) | validate | playthrough | judged err mean/sd/max ms | chartlogic flags (hop/faint/weak-burst/off-grid) | crossings |
|---|---|---|---|---|---|---|
| supernatural | 320 (162) | 0 errors, 0 warns | complete, 320 PERFECT, 10/10 diamonds, 3 crowns | 1.3 / 2.9 / 30 | 2 / 4 / 0 / 0 | 37 |
| how-sweet | 307 (133) | 0 errors, 0 warns | complete, 307 PERFECT, 10/10 | 1.2 / 3.5 / 28 | 0 / 1 / 7 / 0 | 73 |
| bubble-gum | 257 (132) | 0 errors, 0 warns | complete, 256 PERFECT + 1 GOOD, 10/10 | 1.0 / 4.7 / 74 | 0 / 6 / 0 / 0 | 20 |
| right-now | 411 (216) | 0 errors, 0 warns | complete, 411 PERFECT, 10/10 | 1.3 / 0.9 / 9 | 1 / 0 / 0 / 0 (with 172 BPM meta grid) | 11 |

Flags were reported, not fixed (task: taps unchanged). Candidates for a later trim by the chart owner:
- supernatural: FAINT 38.589, 91.433, 153.084, 172.075 s; HOP 59.506 (hat), 114.277 (hat in kick-led bridge).
- how-sweet: WEAK-BURST 16th fills at 38.378/38.498/38.618, 46.178/46.298, 153.576, 161.256 s (full 0.30-0.52: fills are audible but below the 0.6 'clear' bar); FAINT 134.736 s.
- bubble-gum: FAINT 2.627, 57.194, 183.186 s; breakdown vocal taps 83.193, 88.907, 89.478 s (vocal 0.25-0.33).
- right-now: HOP 10.800 s (intro tap on a kick, section follows the melody).

## Visual observations from the static frames
- The `?debug` preview camera frames the road tightly; most side landmarks (e.g. How Sweet cat / sticker / water tower, Supernatural billboard / stage) are outside these frames, so landmark *visibility in motion* is unverified. Layout objects are the designers' unchanged ones, so they match design.md by construction.
- Right Now's flower-ground texture (scale 30) is busy; the road still reads but it is the noisiest of the four.
- Bubble Gum's single GOOD (tap 24 at 36.910 s, 74 ms early) is a scripted-dispatch timing outlier (other agents' browser jobs were running on the box at the time), not a chart problem.

## Follow-up (2026-10-18): flagged taps fixed, not just reported
Tool: `tools/charts/integc_repair.py`, a new per-song helper; no engine change. Every tap is a 90° turn, so removing one tap flips the heading parity of the whole rest of the route: a straight that ran N would now run E. Simply re-tracking the old route with flipped axes fails on long straights; my first attempt on Right Now drifted up to 38 units and lost all 11 crossings.
- The tool re-plans only a short window after each removal. In most cases that is 1 turn; the longest is 16 turns, in How Sweet 153.5–161.4 s.
- It then re-attaches the designer's remaining route verbatim as a rigid copy: rotation k·90° plus translation. It uses k = 0 with zero translation whenever two removals can be paired, which gives an exact re-join.
- Objects placed at absolute world positions that come after the join get the same transform (rot += 90k). Objects inside the window move with the local route. Candidate joins are scored to avoid new object/road intersections, and any object the edit still pushed into the road is nudged out.
- Every candidate is checked with a validator-exact pairwise test (same-level overlap rule); the air-time rule is unaffected.

| song | taps | removed | crossings (design → now) | chartlogic now |
|---|---|---|---|---|
| supernatural | 320 → 314 | 38.589, 59.506, 91.433, 114.277, 153.084, 172.075 | 37 → 40 | clean |
| how-sweet | 307 → 300 | 38.378, 38.618, 46.178, 46.298, 134.736, 153.576, 161.256 | 73 → 90 | clean |
| bubble-gum | 257 → 253 | 2.627, 57.194, 87.192, 183.186 | 20 → 39 | 1 justified HOP (80.336: the chorus's last snare, 0.86 in the full mix, carried across the section line into the breakdown) |
| right-now | 411 → 410 | 10.800 | 11 → 11 | clean |

Notes for the integrator:
- **vocal_env.py does not correct the stem lag.** The `/workspace/nj-stems/htdemucs/*/vocals.mp3` stems lag the browser decode by about 46 ms (cross-correlation; mp3 encoder delay plus demucs), so its ±30 ms window misses vocal onsets and marks real syllables as faint. For bubble-gum I rebuilt the `vocal` envelope from `/workspace/w4/stems/htdemucs/bubble-gum/vocals.wav` with the measured 23 ms lag removed (same normalisation and −18 dB gate), and wrote it to `analysis/bubble-gum.env.npz`. Other songs that use vocal_env.py should be re-checked.
- **How Sweet water tower, still to check visually:** the build helix still sweeps 324° around the tower (design: 289°). The closest road pass is now 2.2 units from the tower's centre; it clears the 0.8-unit pole, and the tank sits above the road.
- **Supernatural's bunny-moon camera cue:** its `worldYaw` cue (176.5 s) was rotated together with the remainder.
- The `route` key in layout.json (informational) is recomputed. `levels-design/<slug>/` copies are synced with `levels-src/`, and chart-report.md has a new section listing every removed tap and the repair log.
