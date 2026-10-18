# super-shy — chart report (worker w2)

- Audio: `public/audio/super-shy.mp3`, full length 154.667 s, untouched. Grid: 150.0 BPM, beat0 0.3562 s (fit to demucs drum stem).
- **Old (v1) taps: 176 → new: 378  (×2.15)**. Average 2.44 taps/s (147 CPM).
- Min gap 111 ms (design floor = one 8th note = 200 ms; snapped taps never closer than road-geometry floor). Median gap 383 ms.
- **Fastest run: 5 consecutive taps at 8th-note spacing (200 ms ≈ 5.0 taps/s) from 130.741 s to 131.552 s.**
- 8th-note runs ≥6 taps: 0; ≥8 taps: 0. Longest 5: 5@130.7s, 5@137.1s, 4@38.1s, 4@145.7s, 3@36.8s
- Judgment window (engine rule v2.5 per tap: min(0.5·g, clamp(0.45·g, 45, 110)) ms each side, g = smaller neighbour gap; PERFECT ±40 ms): min ±50 ms, median ±110 ms, 117 of 378 taps below the ±110 ms cap. My recommendation stays perfect ±55 / accept ±95 ms where the music allows; the engine rule is what ships.
- Snapping: 335/378 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Difficulty calibration vs original Dancing Line levels

- Tier: **hard (title track)**.
- **Average CPM** (all taps ÷ song length × 60): **147** (2.44 taps/s).
- **Average CPM, wiki-style** (mean of instantaneous 60/gap over all gaps; the wiki does not publish its formula, but The Racing's 220 vs 149 by total ÷ length suggests a gap-based mean): **181** (median 157).
- **Peak CPM, instantaneous** (60 ÷ smallest gap): **541** (min gap 111 ms). Sustained peak over the densest 2 s: 9 taps = 270 CPM.
- Fast bursts (2-4 taps, gaps < 170 ms, i.e. clearly faster than an 8th note at this tempo): **4**: 3@36.78s (541 CPM), 2@113.71s (492 CPM), 3@128.15s (517 CPM), 2@134.12s (500 CPM)
- Syncopation: 94 dotted-8th gaps (3 sixteenths ≈ 300 ms); 57 of 378 taps (15%) sit off the 8th grid (16th off-beats / tresillo pushes).
- Every burst tap sits on a real onset of the drum, vocal or melody stem inside a genuinely dense passage (fills, build-ups, drop entries, final choruses); bursts are never placed on silence or used as filler. Schema v2.5 floor is 0.105 s; true 16ths at 150 BPM are 100 ms apart (below the floor, so 16th rolls here are charted only where the real onsets drift to >= 105 ms or as triplet/swung figures).
- **Peak CPM, validator style** (most taps in any 1 s window × 60, as printed by validate.py and used for the 400-460 target): **300**.

| level | length | taps | avg CPM | peak CPM | notes |
|---|---|---:|---:|---:|---|
| The Racing | 2:24 | 357 | 220 (wiki) / 149 (taps÷len) | 440 | 16ths at 110 BPM, ~136 ms |
| The Chaos | 1:54 | | 136 | 408 | |
| Chinese Garden | | | 148 | 296 | narrowest window ±45.8 ms |
| Amusement Park | | | | 512 | |
| Storm | | | | 460 | |
| Autumn | | | 96 | | |
| Winter | | | 140 | 280 | |
| Piano | | | 125 | 250 | |
| **super-shy (this chart)** | 2:34 | 378 | 181 (wiki-style) / 147 (taps÷len) | 300 (1 s window) / 541 (60÷min gap) | engine window min ±50 ms, median ±110 ms, 117 of 378 taps below the ±110 ms cap |

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 薄荷街角 | intro | 13 | 0.99 | 2.5/s |
| 13.16 | Verse 1 · 石砖小巷 | verse | 62 | 2.42 | 4.0/s |
| 38.76 | Chorus 1 · 公园遮阳伞 | chorus | 72 | 2.81 | 3.5/s |
| 64.36 | Break · 下沉喷泉广场 | break | 8 | 1.25 | 2.0/s |
| 70.76 | Build · 里斯本阶梯 | pre | 15 | 2.34 | 3.0/s |
| 77.16 | Verse 2 · 市场拱廊 | verse | 61 | 2.38 | 3.0/s |
| 102.76 | Break 2 · 观景台 | break | 5 | 1.56 | 2.0/s |
| 105.96 | Verse 3 · 下坡 | verse | 24 | 2.50 | 3.5/s |
| 115.56 | Final chorus · 五人广场 | chorus | 36 | 2.81 | 3.5/s |
| 128.36 | Final chorus b · 像素浮雕墙 | chorus | 43 | 3.36 | 4.0/s |
| 141.16 | Final chorus c · 巴士街 | chorus | 39 | 2.89 | 4.0/s |

## What the taps follow (one audible layer per section)

| section | layer followed | share | bursts (full-mix audible 16th figures) | notes |
|---|---|---:|---|---|
| Intro · 薄荷街角 | kick drum | 100% | - | sparse on purpose (breathing room) |
| Verse 1 · 石砖小巷 | kick drum | 100% | 36.78-37.05 s | same pattern every repeat of this phrase |
| Chorus 1 · 公园遮阳伞 | kick drum | 100% | - | same pattern every repeat of this phrase; removed faint taps at 40.14, 44.56, 50.96, 52.64, 57.35, 59.04, 59.34, 64.06 s |
| Break · 下沉喷泉广场 | vocal syllables | 100% | - | sparse on purpose (breathing room) |
| Build · 里斯本阶梯 | kick drum | 100% | - | same pattern every repeat of this phrase; removed faint taps at 76.56 s |
| Verse 2 · 市场拱廊 | kick drum | 100% | - | same pattern every repeat of this phrase |
| Break 2 · 观景台 | vocal syllables | 80% | - | sparse on purpose (breathing room) |
| Verse 3 · 下坡 | kick drum | 100% | 113.53-113.83 s | same pattern every repeat of this phrase |
| Final chorus · 五人广场 | kick drum | 100% | 128.15-128.39 s | same pattern every repeat of this phrase |
| Final chorus b · 像素浮雕墙 | kick drum | 100% | 133.94-134.24 s | same pattern every repeat of this phrase; removed faint taps at 140.56 s |
| Final chorus c · 巴士街 | kick drum | 100% | 142.38-142.74 s | same pattern every repeat of this phrase; removed faint taps at 142.96, 143.36, 146.56, 149.36, 149.76 s |

## Tag mix

kick: 357, vocal: 12, melody: 6, hat: 3

## Section rationale (which audio events the taps follow)

- **Intro (0–13.2 s)** — drums + synth before the vocals: taps on the kick on beat 2 and the "and" of 3 (steps 4,10), 1–2 per bar; bar 7 previews the verse groove.
- **Verse 1 / 2 / 3** — skippy broken-beat kick on steps 4,7,10,14 (3+3+4 sixteenths = 300/300/400 ms): the signature "shy" bounce, alternated with 2-tap bars so the vocal phrases breathe; phrase-end bars add a kick/snare 8th fill.
- **Chorus 1 / Final** — jersey-style kick 0,4,8,11,14 under "I'm super shy, super shy"; the 4th bar of each phrase is an 8th-note kick roll (6–7 taps at 200 ms). Final chorus c alternates 5-tap and 7-tap bars (hardest).
- **Break / Break 2** — drums cut: taps on vocal syllables ≥ 1 beat apart (0.4 s+), the breathing room before the stair climb.
- **Build (70.8–77.2 s)** — kick on 2 and 4 returning, densifying to an 8th run — synced with the road ramping up the Lisbon stairway.

## Alignment spot checks (offset = nearest detected onset − tap; independent of snapping source)

| where | tap t (s) | tag | nearest stem onset | stem offset ms | nearest full-mix onset offset ms |
|---|---:|---|---|---:|---:|
| start | 2.343 | kick | kick (str 0.47) | -0 | -0 |
| start | 3.947 | kick | kick (str 0.33) | -0 | +5 |
| start | 4.543 | kick | kick (str 0.45) | -0 | -5 |
| start | 5.543 | kick | kick (str 0.35) | +0 | -1 |
| change → Verse 1 | 13.545 | kick | kick (str 0.45) | -0 | +38 |
| change → Chorus 1 | 38.775 | kick | kick (str 0.30) | +0 | +27 |
| change → Break | 65.544 | vocal | vocals (str 0.59) | -0 | +13 |
| change → Build | 71.146 | kick | kick (str 0.40) | -0 | +16 |
| change → Verse 2 | 77.545 | kick | kick (str 0.49) | +0 | +18 |
| change → Break 2 | 102.966 | vocal | other (str 0.16) | +0 | +0 |
| change → Verse 3 | 106.339 | kick | kick (str 0.62) | -0 | +33 |
| change → Final chorus | 115.939 | kick | kick (str 0.85) | -0 | +26 |
| change → Final chorus b | 128.389 | melody | other (str 0.41) | +0 | -10 |
| change → Final chorus c | 141.156 | kick | vocals (str 0.25) | +2 | +23 |
| middle | 84.534 | kick | kick (str 0.65) | +0 | +2 |
| middle | 84.941 | kick | kick (str 0.62) | +0 | +0 |
| middle | 85.546 | kick | kick (str 0.54) | +0 | +27 |
| middle | 86.141 | kick | kick (str 0.66) | +0 | -0 |
| middle | 86.741 | kick | kick (str 0.51) | +0 | +4 |
| end | 152.141 | kick | kick (str 0.43) | +0 | +20 |
| end | 152.376 | kick | kick (str 0.22) | -0 | -27 |
| end | 152.739 | kick | kick (str 0.94) | -0 | -0 |
| end | 153.141 | kick | kick (str 0.71) | +0 | +0 |

Whole chart vs FULL-MIX onset detector (not used for snapping): 360/378 taps have a full-mix onset within 80 ms; |offset| median 8.7 ms, p90 33.3 ms.
- first 25%: n=74, median 6.3 ms, p90 32.1 ms
- 25-50%: n=82, median 9.2 ms, p90 36.9 ms
- 50-75%: n=90, median 7.5 ms, p90 31.3 ms
- last 25%: n=114, median 9.5 ms, p90 29.3 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.

## Rhythm-logic audit (integ-b)

Audited on 2026-10-18 by integrator B against the user's rule *rhythm logic beats density* (W2 already audited this chart with stem analysis; this pass applies the same full-mix thresholds that were applied to Ditto, so a few W2 kick/burst taps that are not clear in the full mix were dropped). Taps **378 → 364** (-14; 14 removed, 0 added). Nothing was added to reach a CPM target.

Method (same thresholds as `tools/charts/chartlogic.py` and the Ditto trim): each section follows the one band that best explains its taps; a tap is removed if it is **faint** (followed band < 0.35, full mix < 0.35, every other band < 0.5), **off-layer** (followed band < 0.35 while another band ≥ 0.6) or a **weak burst** (gap < 0.15 s and neither the full mix nor the followed band ≥ 0.6). Strengths are onset strengths per band, normalised to the song's 99.5th percentile, max within ±30 ms of the tap. Removing a tap removes a turn, so the route was repaired by `tools/charts/integb_route.py`, which keeps the worker's own turn sequence phrase by phrase wherever it stays legal; worldPos landmarks were moved with the road.

### What the taps follow (per section)

| section | time | taps follow | taps before → after | /s after | median strength of followed band | removed (faint / off-layer / weak burst) |
|---|---|---|---|---|---|---|
| Intro · 薄荷街角 | 0.00 | melody / synth / vocal line (mid band) | 13 → 13 | 0.99 | 0.69 | 0 / 0 / 0 |
| Verse 1 · 石砖小巷 | 13.16 | kick + snare drum groove (full mix) | 62 → 60 | 2.34 | 0.56 | 1 / 0 / 1 |
| Chorus 1 · 公园遮阳伞 | 38.76 | kick + snare drum groove (full mix) | 72 → 71 | 2.77 | 0.50 | 1 / 0 / 0 |
| Break · 下沉喷泉广场 | 64.36 | kick + snare drum groove (full mix) | 8 → 8 | 1.25 | 0.38 | 0 / 0 / 0 |
| Build · 里斯本阶梯 | 70.76 | melody / synth / vocal line (mid band) | 15 → 14 | 2.19 | 0.78 | 1 / 0 / 0 |
| Verse 2 · 市场拱廊 | 77.16 | kick + snare drum groove (full mix) | 61 → 60 | 2.34 | 0.62 | 0 / 1 / 0 |
| Break 2 · 观景台 | 102.76 | lead vocal syllables (vocal stem, gated to the full mix) | 5 → 4 | 1.25 | 1.27 | 0 / 1 / 0 |
| Verse 3 · 下坡 | 105.96 | kick + snare drum groove (full mix) | 24 → 22 | 2.29 | 0.65 | 0 / 1 / 1 |
| Final chorus · 五人广场 | 115.56 | melody / synth / vocal line (mid band) | 36 → 34 | 2.66 | 0.55 | 0 / 1 / 1 |
| Final chorus b · 像素浮雕墙 | 128.36 | kick + snare drum groove (full mix) | 43 → 40 | 3.12 | 0.82 | 2 / 0 / 1 |
| Final chorus c · 巴士街 | 141.16 | kick + snare drum groove (full mix) | 39 → 38 | 2.54 | 0.94 | 1 / 0 / 0 |

### Audit diff (removed taps)

| t (s) | tag | reason | followed band | band strength | full-mix strength |
|---|---|---|---|---|---|
| 37.053 | kick | weak-burst | drums | 0.57 | 0.45 |
| 38.356 | kick | faint | drums | 0.21 | 0.21 |
| 42.347 | kick | faint | drums | 0.29 | 0.21 |
| 76.356 | kick | faint | mid | 0.19 | 0.14 |
| 97.742 | kick | off-layer | drums | 0.30 | 0.43 |
| 105.941 | kick | off-layer | vocal | 0.20 | 1.50 |
| 112.129 | kick | off-layer | drums | 0.30 | 0.16 |
| 113.706 | hat | weak-burst | drums | 0.55 | 0.07 |
| 117.156 | kick | off-layer | mid | 0.32 | 0.25 |
| 128.153 | melody | weak-burst | mid | 0.48 | 0.32 |
| 130.956 | kick | faint | drums | 0.25 | 0.14 |
| 134.121 | kick | weak-burst | drums | 0.43 | 0.21 |
| 137.358 | kick | faint | drums | 0.25 | 0.18 |
| 146.156 | kick | faint | drums | 0.30 | 0.25 |

Added taps: none.

Original (pre-audit) chart and layout: `levels-design/super-shy/pre-audit/`. Integrated copy: `levels-src/super-shy/`. chartlogic report after the audit: `docs/verification/super-shy-chartlogic.md`.
