# super-shy — chart report (worker w2)

- Audio: `public/audio/super-shy.mp3`, full length 154.667 s, untouched. Grid: 150.0 BPM, beat0 0.3562 s (fit to demucs drum stem).
- **Old (v1) taps: 176 → new: 396  (×2.25)**. Average 2.56 taps/s (154 CPM).
- Min gap 152 ms (design floor = one 8th note = 200 ms; snapped taps never closer than road-geometry floor). Median gap 313 ms.
- **Fastest run: 6 consecutive taps at 8th-note spacing (200 ms ≈ 5.0 taps/s) from 137.141 s to 138.083 s.**
- 8th-note runs ≥6 taps: 4; ≥8 taps: 0. Longest 5: 6@137.1s, 6@142.5s, 6@145.7s, 6@148.9s, 5@44.3s
- Judgment window (engine rule v2.4: clamp(0.45 x min neighbour gap, 65, 110) ms each side, PERFECT ±40 ms): min ±68 ms, median ±110 ms, 151 of 396 taps below the ±110 ms cap. My recommendation stays perfect ±55 / accept ±95 ms where the music allows; the engine rule is what ships.
- Snapping: 346/396 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Difficulty calibration vs original Dancing Line levels

- Tier: **hard (title track)**.
- **Average CPM** (all taps ÷ song length × 60): **154** (2.56 taps/s).
- **Average CPM, wiki-style** (mean of instantaneous 60/gap over all gaps; the wiki does not publish its formula, but The Racing's 220 vs 149 by total ÷ length suggests a gap-based mean): **192** (median 192).
- **Peak CPM** (60 ÷ smallest gap): **395** (min gap 152 ms). Sustained peak over the densest 2 s: 10 taps = 300 CPM.
- Fast bursts (2-4 taps, gaps < 195 ms, i.e. faster than any 8th note at this tempo): **11**: 4@38.17s (377 CPM), 2@41.75s (309 CPM), 3@44.56s (312 CPM), 3@77.03s (375 CPM), 3@101.15s (323 CPM), 3@115.37s (345 CPM), 4@126.37s (359 CPM), 4@137.56s (395 CPM), 4@140.38s (392 CPM), 4@147.94s (392 CPM), 2@149.16s (309 CPM)
- Syncopation: 96 dotted-8th gaps (3 sixteenths ≈ 300 ms); 65 of 396 taps (16%) sit off the 8th grid (16th off-beats / tresillo pushes).
- Every burst tap sits on a real onset of the drum, vocal or melody stem inside a genuinely dense passage (fills, build-ups, drop entries, final choruses). True 16ths at 150 BPM are 100 ms apart, below the schema's hard 150 ms minimum gap, so straight 16th rolls cannot be charted; the bursts use the fastest real events that clear 150 ms (8th-note triplet hats, swung 16ths, rapid syllables). That caps the peak at about 330-395 CPM instead of 400-460: 60 ÷ 0.150 s is exactly 400 CPM, and The Racing's own 136 ms 16ths would fail this schema too. Reaching 400-460 CPM needs the integrator to lower the schema floor to about 0.13 s; the build already supports that (spec.BURST_MIN), and the true 16th rolls are present in the stems (e.g. hat/snare rolls in fills).

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
| **super-shy (this chart)** | 2:34 | 396 | 192 (wiki-style) / 154 (taps÷len) | 395 | engine window min ±68 ms, median ±110 ms, 151 of 396 taps below the ±110 ms cap |

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 薄荷街角 | intro | 13 | 0.99 | 2.5/s |
| 13.16 | Verse 1 · 石砖小巷 | verse | 61 | 2.38 | 3.5/s |
| 38.76 | Chorus 1 · 公园遮阳伞 | chorus | 79 | 3.09 | 4.0/s |
| 64.36 | Break · 下沉喷泉广场 | break | 8 | 1.25 | 2.0/s |
| 70.76 | Build · 里斯本阶梯 | pre | 16 | 2.50 | 3.5/s |
| 77.16 | Verse 2 · 市场拱廊 | verse | 64 | 2.50 | 4.0/s |
| 102.76 | Break 2 · 观景台 | break | 5 | 1.56 | 2.0/s |
| 105.96 | Verse 3 · 下坡 | verse | 22 | 2.29 | 3.5/s |
| 115.56 | Final chorus · 五人广场 | chorus | 37 | 2.89 | 4.0/s |
| 128.36 | Final chorus b · 像素浮雕墙 | chorus | 45 | 3.52 | 4.5/s |
| 141.16 | Final chorus c · 巴士街 | chorus | 46 | 3.40 | 5.0/s |

## Tag mix

kick: 355, hat: 13, vocal: 12, snare: 8, melody: 8

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
| change → Chorus 1 | 39.145 | kick | kick (str 0.91) | +0 | +19 |
| change → Break | 65.544 | vocal | vocals (str 0.59) | -0 | +13 |
| change → Build | 71.146 | kick | kick (str 0.40) | -0 | +16 |
| change → Verse 2 | 77.186 | hat | other (str 0.39) | +0 | -46 |
| change → Break 2 | 102.966 | vocal | other (str 0.16) | +0 | +0 |
| change → Verse 3 | 106.339 | kick | kick (str 0.62) | -0 | +33 |
| change → Final chorus | 115.727 | hat | snare (str 0.27) | -26 | +31 |
| change → Final chorus b | 128.362 | kick | kick (str 0.21) | +0 | +17 |
| change → Final chorus c | 141.156 | kick | vocals (str 0.25) | +2 | +23 |
| middle | 84.941 | kick | kick (str 0.62) | +0 | +0 |
| middle | 85.546 | kick | kick (str 0.54) | +0 | +27 |
| middle | 86.141 | kick | kick (str 0.66) | +0 | -0 |
| middle | 86.741 | kick | kick (str 0.51) | +0 | +4 |
| middle | 87.152 | kick | kick (str 0.36) | +0 | +26 |
| end | 152.141 | kick | kick (str 0.43) | +0 | +20 |
| end | 152.376 | kick | kick (str 0.22) | -0 | -27 |
| end | 152.739 | kick | kick (str 0.94) | -0 | -0 |
| end | 153.141 | kick | kick (str 0.71) | +0 | +0 |

Whole chart vs FULL-MIX onset detector (not used for snapping): 364/396 taps have a full-mix onset within 80 ms; |offset| median 8.9 ms, p90 33.5 ms.
- first 25%: n=73, median 6.7 ms, p90 30.1 ms
- 25-50%: n=86, median 9.2 ms, p90 39.8 ms
- 50-75%: n=91, median 7.6 ms, p90 31.1 ms
- last 25%: n=114, median 9.7 ms, p90 33.2 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.