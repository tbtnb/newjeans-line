# omg — chart report (worker w2)

- Audio: `public/audio/omg.mp3`, full length 212.253 s, untouched. Grid: 127.004 BPM, beat0 0.0288 s (fit to demucs drum stem).
- **Old (v1) taps: 213 → new: 412  (×1.93)**. Average 1.94 taps/s (116 CPM).
- Min gap 118 ms (design floor = one 8th note = 236 ms; snapped taps never closer than road-geometry floor). Median gap 470 ms.
- **Fastest run: 11 consecutive taps at 8th-note spacing (236 ms ≈ 4.2 taps/s) from 162.054 s to 164.434 s.**
- 8th-note runs ≥6 taps: 3; ≥8 taps: 2. Longest 5: 11@162.1s, 8@104.2s, 7@62.6s, 5@144.3s, 5@151.7s
- Judgment window (engine rule v2.5 per tap: min(0.5·g, clamp(0.45·g, 45, 110)) ms each side, g = smaller neighbour gap; PERFECT ±40 ms): min ±53 ms, median ±110 ms, 131 of 412 taps below the ±110 ms cap. My recommendation stays perfect ±60 / accept ±110 ms where the music allows; the engine rule is what ships.
- Snapping: 359/412 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Difficulty calibration vs original Dancing Line levels

- Tier: **hard (title track)**.
- **Average CPM** (all taps ÷ song length × 60): **116** (1.94 taps/s).
- **Average CPM, wiki-style** (mean of instantaneous 60/gap over all gaps; the wiki does not publish its formula, but The Racing's 220 vs 149 by total ÷ length suggests a gap-based mean): **157** (median 128).
- **Peak CPM, instantaneous** (60 ÷ smallest gap): **508** (min gap 118 ms). Sustained peak over the densest 2 s: 9 taps = 270 CPM.
- Fast bursts (2-4 taps, gaps < 195 ms, i.e. clearly faster than an 8th note at this tempo): **2**: 3@63.08s (508 CPM), 3@144.79s (462 CPM)
- Syncopation: 18 dotted-8th gaps (3 sixteenths ≈ 354 ms); 33 of 412 taps (8%) sit off the 8th grid (16th off-beats / tresillo pushes).
- Every burst tap sits on a real onset of the drum, vocal or melody stem inside a genuinely dense passage (fills, build-ups, drop entries, final choruses); bursts are never placed on silence or used as filler. Schema v2.5 floor is 0.105 s; true 16ths at 127 BPM are 118 ms apart, so straight 16th rolls are charted directly.
- **Peak CPM, validator style** (most taps in any 1 s window × 60, as printed by validate.py and used for the 400-460 target): **360**.

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
| **omg (this chart)** | 3:32 | 412 | 157 (wiki-style) / 116 (taps÷len) | 360 (1 s window) / 508 (60÷min gap) | engine window min ±53 ms, median ±110 ms, 131 of 412 taps below the ±110 ms cap |

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 病房走廊 | intro | 11 | 0.73 | 1.5/s |
| 15.15 | Verse 1 · 治疗桌与五椅 | verse | 29 | 1.92 | 2.5/s |
| 30.26 | Verse 1b · 墙板外折 | verse | 30 | 1.98 | 3.5/s |
| 45.38 | Chorus 1 · 黑兔舞台 | chorus | 32 | 2.12 | 3.0/s |
| 60.50 | Verse 2 · 玻璃鞋 | verse | 35 | 2.32 | 4.0/s |
| 75.62 | Verse 2b · 双折长短路 | pre | 29 | 1.92 | 3.0/s |
| 90.73 | Pre · 手机桥 | break | 28 | 1.85 | 4.0/s |
| 105.85 | Chorus 2 · 屏幕块 | chorus | 30 | 1.98 | 3.0/s |
| 120.97 | Post · 错列直角 | post | 23 | 1.74 | 2.5/s |
| 134.20 | Bridge · 书页墙与猫 | bridge | 41 | 2.71 | 4.0/s |
| 149.32 | Break · 书页合拢 | break | 3 | 1.59 | 1.5/s |
| 151.21 | Dance break · 舞台五墙 | drop | 46 | 3.04 | 4.5/s |
| 166.32 | Final chorus · 兔耳发夹 | chorus | 32 | 2.12 | 3.0/s |
| 181.44 | Final chorus b · 天桥 | chorus | 29 | 1.92 | 3.0/s |
| 196.56 | Outro · 尾奏琴键 | outro | 14 | 0.89 | 1.5/s |

## What the taps follow (one audible layer per section)

| section | layer followed | share | bursts (full-mix audible 16th figures) | notes |
|---|---|---:|---|---|
| Intro · 病房走廊 | vocal syllables | 100% | - | sparse on purpose (breathing room); removed faint taps at 15.00 s |
| Verse 1 · 治疗桌与五椅 | kick + snare drum groove | 100% | - | same pattern every repeat of this phrase |
| Verse 1b · 墙板外折 | kick drum | 100% | - | same pattern every repeat of this phrase |
| Chorus 1 · 黑兔舞台 | kick + snare drum groove | 91% | - | same pattern every repeat of this phrase |
| Verse 2 · 玻璃鞋 | kick + snare drum groove | 100% | 63.08-63.31 s | same pattern every repeat of this phrase |
| Verse 2b · 双折长短路 | kick drum | 86% | - | same pattern every repeat of this phrase |
| Pre · 手机桥 | bassline | 86% | - | sparse on purpose (breathing room) |
| Chorus 2 · 屏幕块 | kick + snare drum groove | 100% | - | same pattern every repeat of this phrase; removed faint taps at 119.91, 120.14, 120.62 s |
| Post · 错列直角 | kick + snare drum groove | 100% | - | same pattern every repeat of this phrase |
| Bridge · 书页墙与猫 | kick drum | 100% | 144.79-145.06 s | same pattern every repeat of this phrase |
| Break · 书页合拢 | kick + snare drum groove | 100% | - | sparse on purpose (breathing room) |
| Dance break · 舞台五墙 | kick drum | 100% | - | same pattern every repeat of this phrase; removed faint taps at 158.53 s |
| Final chorus · 兔耳发夹 | kick + snare drum groove | 100% | - | same pattern every repeat of this phrase |
| Final chorus b · 天桥 | kick + snare drum groove | 100% | - | same pattern every repeat of this phrase |
| Outro · 尾奏琴键 | synth / melody hook | 100% | - | sparse on purpose (breathing room) |

## Tag mix

kick: 260, snare: 93, bass: 24, vocal: 21, melody: 14

## Section rationale (which audio events the taps follow)

- **Intro (0–15.2 s)** — a-cappella "OMG" vocal phrases only (no drums in the stem map): 12 taps on the sung syllable entries, 1–4 s gaps = the "waiting for the call" calm.
- **Verse 1 (15.2–30.3 s)** — finger-snap/clap layer enters with strong hits on step 6 and 14 (the "and" of 2 and 4) — taps on the clap downbeat + those syncopated snaps (s.....s.s.....s.): the first syncopation the player meets.
- **Verse 1b (30.3–45.4 s)** — full UK-garage kick enters (K...|k...|..k.|..kk / ..K.|k.kk|.kk.|K...): taps on the kicks, odd bars use the off-beat kick pair at steps 2/4 and 10/12 = call (even bar) / response (odd bar).
- **Chorus 1 / 2 / Final (45.4, 105.9, 166.4 s)** — ONE layer, the halftime drum groove you can hear in the full mix: odd bars kick 1, snare 3, kick 4 + the snare pickup on the last 8th (k.......s...k.s.), even bars the syncopated double kick on the e/and of 1-2, snare 3, kick 4 (..k.k...s...k...). The same 2-bar pattern repeats in every chorus so it can be learned; the synth hook is no longer charted between drum hits.
- **Verse 2 / 2b / Post** — same garage kick but thinned to 4–5 taps per bar so the vocals breathe; Verse 2b inserts the vocal "V V v v" accent at step 8.
- **Pre (90.8–105.9 s)** — drums drop out, only bass (..B.|..B.|..B.|..B.) + vocal: taps follow the bass pulses at a relaxed 1.9/s while the phone bridge ramps up 6 units; bar 55 is a 7-tap 8th-note build into Chorus 2.
- **Bridge (134.2–149.3 s)** — new trap-style kick pattern (...k|..k.|k.k.|.k.k): taps on steps 3,6,8,13,15 / 3,6,8,10,13 — every bar starts on an off-beat, the hardest syncopation in the level, on a narrow 1.8-wide road inside the library.
- **Break (149.3 s)** — one bar of near silence (2 snare hits + 1 kick): 3 taps, camera to top view.
- **Dance break (151.2–166.4 s)** — four-on-the-floor kick with 8th-note kick fills: long 8th runs (6, 8 and an 11-tap run on bars 86–87) — the densest passage (3.1 taps/s, 4.2/s peak).
- **Outro (196.6–212.3 s)** — drums stop, only the synth stabs remain: 2 taps per bar on the stabs, last tap > 1 s before the end.

## Alignment spot checks (offset = nearest detected onset − tap; independent of snapping source)

| where | tap t (s) | tag | nearest stem onset | stem offset ms | nearest full-mix onset offset ms |
|---|---:|---|---|---:|---:|
| start | 2.371 | vocal | vocals (str 0.74) | -0 | -0 |
| start | 2.898 | vocal | vocals (str 0.55) | +0 | +0 |
| start | 4.371 | vocal | vocals (str 0.28) | -0 | -3 |
| start | 4.840 | vocal | vocals (str 0.87) | -0 | +3 |
| change → Verse 1 | 15.834 | snare | kick (str 0.26) | +0 | +46 |
| change → Verse 1b | 31.426 | kick | kick (str 0.46) | +0 | +40 |
| change → Chorus 1 | 46.304 | snare | kick (str 0.19) | +0 | +14 |
| change → Verse 2 | 60.952 | kick | kick (str 0.27) | -0 | +40 |
| change → Verse 2b | 76.070 | kick | kick (str 0.51) | +0 | +19 |
| change → Pre | 90.771 | bass | bass (str 0.16) | -0 | -40 |
| change → Chorus 2 | 106.777 | snare | kick (str 0.32) | +0 | +0 |
| change → Post | 122.134 | kick | kick (str 0.77) | -0 | +50 |
| change → Bridge | 134.535 | kick | kick (str 0.54) | +0 | +13 |
| change → Break | 149.546 | snare | kick (str 0.16) | -0 | +33 |
| change → Dance break | 151.661 | kick | kick (str 0.33) | +0 | +23 |
| change → Final chorus | 167.249 | snare | kick (str 0.23) | +0 | +0 |
| change → Final chorus b | 182.380 | snare | kick (str 0.27) | -0 | +12 |
| change → Outro | 197.058 | melody | other (str 0.70) | -0 | -17 |
| middle | 111.265 | snare | kick (str 0.25) | +0 | +1 |
| middle | 111.737 | kick | kick (str 0.29) | +1 | +5 |
| middle | 111.995 | kick | kick (str 0.23) | +0 | -6 |
| middle | 112.458 | snare | snare (str 0.33) | +0 | -10 |
| middle | 112.919 | kick | kick (str 0.50) | +0 | +21 |
| end | 206.714 | melody | other (str 0.92) | +0 | -0 |
| end | 207.202 | melody | other (str 0.56) | +0 | +0 |
| end | 208.370 | melody | none within 80 ms | — | — |
| end | 209.555 | melody | other (str 0.51) | +0 | +0 |

Whole chart vs FULL-MIX onset detector (not used for snapping): 398/412 taps have a full-mix onset within 80 ms; |offset| median 15.9 ms, p90 43.0 ms.
- first 25%: n=84, median 12.0 ms, p90 37.5 ms
- 25-50%: n=105, median 23.7 ms, p90 46.8 ms
- 50-75%: n=113, median 19.4 ms, p90 44.5 ms
- last 25%: n=96, median 12.9 ms, p90 37.5 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.