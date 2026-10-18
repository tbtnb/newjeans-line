# integ-a: engine / pipeline issues found while integrating attention, hype-boy, cookie, hurt, new-jeans

All playthroughs referenced here are **scripted simulations** (tools/qa/play.mjs, CDP touch events at chart times, headless SwiftShader),
not physical-device play and not proof of audio/visual sync.

## 1. `onroad` landmarks are excluded from the occluder cutaway (data workaround applied)
- Engine: `src/render/world.ts` `fadeOccluders()` skips every object with `onroad: true`.
- The W1 designs (attention, hype-boy, cookie, hurt) mark their tall worldPos landmarks `onroad` (stair/diving/clock towers 19-31 u,
  bunny relief walls, arcade roofs, Cookie's CD disc). Result: Cookie's 19 u folding-stair tower covered the head and the road ahead
  during the pre-chorus spiral (first snapshot run, t = 43 s).
- Workaround (data only, `tools/charts/integ_a.py` `cutaway`): drop `onroad` from worldPos groups taller than 5 u. `onroad` otherwise
  only disables push-out, which worldPos objects skip anyway, so the only effect is that these objects can now fade when they occlude.
  Flat decks (pitch, pool, court, terrace), piers and fake forks keep `onroad`.
- Suggested engine fix (not done, engine untouched): let `onroad` objects fade too when they are taller than the road deck, or add an
  explicit `noCutaway` flag for true decks.

## 1b. Trimming a tap rotates the rest of the route (turn parity), so "local" repair is rigid-tail + nearby flips
- User rule (2026-10-18): remove every tap chartlogic flags as faint or off-layer. Each removed turn changes the heading parity,
  so no choice of the remaining directions can restore the designer's tail; the tail is carried as a rigid piece (rotated 90 deg
  about the edit) and up to 3 directions within +-4 taps of the edit are flipped so the whole route stays legal (route.py overlap
  rule, never worse than the designer route) and the multi-level crossing count stays near the designer's (integ_a_tune.py picks the
  flip weight per song). worldPos scenery and worldYaw camera cues move with the route. Weak bursts are NOT trimmed (not in the rule).
- Hurt loses 38 of 118 taps (32 off-layer: the vocal-stem onset is < 0.35 while a drum/mid band is >= 0.6 at those taps); this
  is the chartlogic verdict applied literally. If the parent prefers, the Hurt sections could be re-declared `mid` (melody) instead.

## 2. chartlogic grid mismatch on Hype Boy (report only)
- chartlogic refits the grid to 100.468 BPM and reports 195 "off-grid > 25 ms" taps. Hype Boy is ~100 BPM with a swung/syncopated
  vocal groove; the worker chart does not declare `meta.beat_period`, so the off-grid count is most likely a grid artifact, not
  mistimed taps. Layer strengths are high (median 0.60-0.93) and there are 0 off-layer taps.

## 3. Level registry
- No registry line was needed: `src/catalog.ts` already lists all 16 songs and loads `src/levels/<slug>.json` via `import.meta.glob`.
  `tools/build-levels.mjs <slug>` writes that file and copies `levels-src/<slug>/art` to `public/levels/<slug>/art` (not committed, as for Ditto).

## 4. Shared files touched (possible merge conflicts)
- `levels-design/cookie/art/*`, `levels-design/hurt/art/*`: overlaid from `origin/art-codex` 8b6ef1c (same filenames). Other integrators
  doing the same overlay produce identical bytes.
- New file `tools/charts/integ_a.py` (integ-a only). No engine, registry or shared tool file was modified.
