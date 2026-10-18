# super-shy — chart report (worker w2)

- Audio: `public/audio/super-shy.mp3`, full length 154.667 s, untouched. Grid: 150.0 BPM, beat0 0.3562 s (fit to demucs drum stem).
- **Old (v1) taps: 176 → new: 388  (×2.20)**. Average 2.51 taps/s (151 CPM).
- Min gap 191 ms (design floor = one 8th note = 200 ms; snapped taps never closer than road-geometry floor). Median gap 341 ms.
- **Fastest run: 6 consecutive taps at 8th-note spacing (200 ms ≈ 5.0 taps/s) from 142.541 s to 143.556 s.**
- 8th-note runs ≥6 taps: 3; ≥8 taps: 0. Longest 5: 6@142.5s, 6@145.7s, 6@148.9s, 5@44.3s, 5@50.7s
- Recommended judgment window: perfect ±55 ms, accept ±95 ms. 150 BPM: 8th runs are 200 ms apart, so the accept window must stay below ±100 ms to keep neighbouring corners unambiguous; ±95 ms recommended (perfect ±55).
- Snapping: 332/388 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 薄荷街角 | intro | 13 | 0.99 | 2.5/s |
| 13.16 | Verse 1 · 石砖小巷 | verse | 60 | 2.34 | 3.5/s |
| 38.76 | Chorus 1 · 公园遮阳伞 | chorus | 80 | 3.13 | 4.0/s |
| 64.36 | Break · 下沉喷泉广场 | break | 8 | 1.25 | 2.0/s |
| 70.76 | Build · 里斯本阶梯 | pre | 16 | 2.50 | 3.5/s |
| 77.16 | Verse 2 · 山坡电车 | verse | 61 | 2.38 | 3.0/s |
| 102.76 | Break 2 · 观景台 | break | 5 | 1.56 | 2.0/s |
| 105.96 | Verse 3 · 下坡 | verse | 22 | 2.29 | 3.5/s |
| 115.56 | Final chorus · 广场集体舞 | chorus | 35 | 2.73 | 3.5/s |
| 128.36 | Final chorus b · 喷泉 | chorus | 44 | 3.44 | 4.0/s |
| 141.16 | Final chorus c · 巴士 | chorus | 44 | 3.26 | 4.5/s |

## Tag mix

kick: 376, vocal: 12

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
| change → Final chorus b | 128.362 | kick | kick (str 0.21) | +0 | +17 |
| change → Final chorus c | 141.156 | kick | vocals (str 0.25) | +2 | +23 |
| middle | 83.940 | kick | kick (str 0.46) | +0 | +13 |
| middle | 84.246 | kick | kick (str 0.36) | -0 | +4 |
| middle | 84.534 | kick | kick (str 0.65) | +0 | +2 |
| middle | 84.941 | kick | kick (str 0.62) | +0 | +0 |
| middle | 85.546 | kick | kick (str 0.54) | +0 | +27 |
| end | 152.141 | kick | kick (str 0.43) | +0 | +20 |
| end | 152.376 | kick | kick (str 0.22) | -0 | -27 |
| end | 152.739 | kick | kick (str 0.94) | -0 | -0 |
| end | 153.141 | kick | kick (str 0.71) | +0 | +0 |

Whole chart vs FULL-MIX onset detector (not used for snapping): 360/388 taps have a full-mix onset within 80 ms; |offset| median 8.3 ms, p90 33.3 ms.
- first 25%: n=72, median 6.3 ms, p90 32.6 ms
- 25-50%: n=86, median 8.9 ms, p90 37.7 ms
- 50-75%: n=88, median 7.0 ms, p90 30.0 ms
- last 25%: n=114, median 9.2 ms, p90 28.9 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.