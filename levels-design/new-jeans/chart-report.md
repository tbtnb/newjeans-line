# new-jeans — chart report (worker w2)

- Audio: `public/audio/new-jeans.mp3`, full length 108.987 s, untouched. Grid: 134.0 BPM, beat0 0.347 s (fit to demucs drum stem).
- **Old (v1) taps: 68 → new: 168  (×2.47)**. Average 1.54 taps/s (92 CPM).
- Min gap 165 ms (design floor = one 8th note = 224 ms; snapped taps never closer than road-geometry floor). Median gap 670 ms.
- **Fastest run: 6 consecutive taps at 8th-note spacing (224 ms ≈ 4.5 taps/s) from 63.251 s to 64.377 s.**
- 8th-note runs ≥6 taps: 1; ≥8 taps: 0. Longest 5: 6@63.3s, 5@99.7s, 4@49.6s, 3@13.3s, 3@85.4s
- Judgment window (engine rule v2.4: clamp(0.45 x min neighbour gap, 65, 110) ms each side, PERFECT ±40 ms): min ±74 ms, median ±110 ms, 43 of 168 taps below the ±110 ms cap. My recommendation stays perfect ±60 / accept ±115 ms where the music allows; the engine rule is what ships.
- Snapping: 142/168 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Difficulty calibration vs original Dancing Line levels

- Tier: **moderate (EP opener, not a title track: only a few bursts)**.
- **Average CPM** (all taps ÷ song length × 60): **92** (1.54 taps/s).
- **Average CPM, wiki-style** (mean of instantaneous 60/gap over all gaps; the wiki does not publish its formula, but The Racing's 220 vs 149 by total ÷ length suggests a gap-based mean): **126** (median 90).
- **Peak CPM** (60 ÷ smallest gap): **364** (min gap 165 ms). Sustained peak over the densest 2 s: 7 taps = 210 CPM.
- Fast bursts (2-4 taps, gaps < 195 ms, i.e. faster than any 8th note at this tempo): **1**: 3@89.32s (364 CPM)
- Syncopation: 13 dotted-8th gaps (3 sixteenths ≈ 336 ms); 7 of 168 taps (4%) sit off the 8th grid (16th off-beats / tresillo pushes).
- Every burst tap sits on a real onset of the drum, vocal or melody stem inside a genuinely dense passage (fills, build-ups, drop entries, final choruses). True 16ths at 134 BPM are 112 ms apart, below the schema's hard 150 ms minimum gap, so straight 16th rolls cannot be charted; the bursts use the fastest real events that clear 150 ms (8th-note triplet hats, swung 16ths, rapid syllables). That caps the peak at about 330-395 CPM instead of 400-460: 60 ÷ 0.150 s is exactly 400 CPM, and The Racing's own 136 ms 16ths would fail this schema too. Reaching 400-460 CPM needs the integrator to lower the schema floor to about 0.13 s; the build already supports that (spec.BURST_MIN), and the true 16th rolls are present in the stems (e.g. hat/snare rolls in fills).

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
| **new-jeans (this chart)** | 1:48 | 168 | 126 (wiki-style) / 92 (taps÷len) | 364 | engine window min ±74 ms, median ±110 ms, 43 of 168 taps below the ±110 ms cap |

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 方格纸 | intro | 8 | 1.07 | 1.5/s |
| 7.51 | Beat in · 蓝图线 | intro | 13 | 1.81 | 3.0/s |
| 14.68 | Verse 1 · 纸片房屋 | verse | 26 | 1.21 | 2.0/s |
| 36.17 | Chorus 1 · 五色尾迹 | chorus | 26 | 1.81 | 3.0/s |
| 50.50 | Break · 像素平面 | break | 10 | 1.40 | 2.0/s |
| 57.66 | Rebuild · 重新立起 | break | 16 | 2.23 | 3.5/s |
| 64.83 | Verse 2 · 立体城市 | verse | 29 | 1.35 | 2.5/s |
| 86.32 | Chorus 2 · 飞行 | chorus | 34 | 2.37 | 3.0/s |
| 100.64 | Outro · 牛仔徽章 | outro | 6 | 0.72 | 1.5/s |

## Tag mix

kick: 110, snare: 41, melody: 17

## Section rationale (which audio events the taps follow)

- **Intro (0–7.5 s)** — synth stabs only (other stem "O" on steps 0 and 6): 2 taps per bar — the line is drawn on graph paper.
- **Beat in (7.5–14.7 s)** — drums without bass: taps on the snare accents at steps 2,4,12 (syncopated 2-step snares), 8-tap fill in bar 7.
- **Verse 1 / 2** — garage 2-step: kick on 1 and the "and" of 3 (steps 0,10) every bar, plus snare on beat 2 every other bar — 2–3 taps per bar so the rap-like vocal sits on a readable pulse.
- **Chorus 1 / 2** — jersey kick on 2, 3, 3a, 4+ (steps 4,8,11,14) under the "new hair, new tee" hook; the downbeat snare starts every other bar; bar 27/55 ends with an 8th kick roll (5 taps).
- **Break (50.5–57.7 s)** — kick drops, only off-beat claps on steps 2,6,10,14: the player taps off the beat for 4 bars (syncopation test).
- **Rebuild (57.7–64.9 s)** — kick returns on beats 2 and 4 with off-beat claps: "..s.k" call-response pairs, 7-tap run in bar 35.
- **Outro (100.7–109 s)** — drums stop, synth stabs: 1–2 taps per bar, camera pulls back.

## Alignment spot checks (offset = nearest detected onset − tap; independent of snapping source)

| where | tap t (s) | tag | nearest stem onset | stem offset ms | nearest full-mix onset offset ms |
|---|---:|---|---|---:|---:|
| start | 1.026 | melody | other (str 0.25) | +0 | +0 |
| start | 2.156 | melody | other (str 0.30) | -0 | -0 |
| start | 2.850 | melody | other (str 0.25) | +0 | +0 |
| start | 3.945 | melody | other (str 0.35) | -0 | -0 |
| change → Beat in | 7.725 | snare | snare (str 0.81) | +0 | +11 |
| change → Verse 1 | 15.781 | kick | other (str 0.24) | +0 | +0 |
| change → Chorus 1 | 36.623 | kick | kick (str 0.18) | +0 | +29 |
| change → Break | 50.710 | snare | kick (str 0.33) | +0 | -8 |
| change → Rebuild | 57.874 | snare | snare (str 0.59) | +0 | +20 |
| change → Verse 2 | 65.931 | kick | kick (str 0.24) | -0 | +3 |
| change → Chorus 2 | 86.762 | kick | kick (str 0.25) | +0 | +29 |
| change → Outro | 100.668 | melody | other (str 0.26) | +0 | +6 |
| middle | 56.976 | snare | kick (str 0.19) | -0 | — |
| middle | 57.874 | snare | snare (str 0.59) | +0 | +20 |
| middle | 58.108 | kick | kick (str 0.20) | -14 | -14 |
| middle | 58.990 | kick | kick (str 0.29) | +0 | +1 |
| middle | 59.662 | snare | snare (str 0.57) | +0 | +2 |
| end | 102.460 | melody | other (str 0.39) | +0 | +0 |
| end | 104.228 | melody | snare (str 0.47) | -11 | +28 |
| end | 104.899 | melody | vocals (str 0.78) | -4 | +23 |
| end | 106.039 | melody | other (str 0.45) | +0 | +0 |

Whole chart vs FULL-MIX onset detector (not used for snapping): 145/168 taps have a full-mix onset within 80 ms; |offset| median 6.4 ms, p90 36.5 ms.
- first 25%: n=34, median 2.2 ms, p90 28.5 ms
- 25-50%: n=36, median 6.5 ms, p90 37.2 ms
- 50-75%: n=37, median 2.8 ms, p90 23.2 ms
- last 25%: n=38, median 18.9 ms, p90 46.2 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.