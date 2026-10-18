# omg — chart report (worker w2)

- Audio: `public/audio/omg.mp3`, full length 212.253 s, untouched. Grid: 127.004 BPM, beat0 0.0288 s (fit to demucs drum stem).
- **Old (v1) taps: 213 → new: 468  (×2.20)**. Average 2.20 taps/s (132 CPM).
- Min gap 156 ms (design floor = one 8th note = 236 ms; snapped taps never closer than road-geometry floor). Median gap 442 ms.
- **Fastest run: 11 consecutive taps at 8th-note spacing (236 ms ≈ 4.2 taps/s) from 162.054 s to 164.434 s.**
- 8th-note runs ≥6 taps: 16; ≥8 taps: 6. Longest 5: 11@162.1s, 11@184.0s, 11@191.6s, 9@43.3s, 9@168.9s
- Judgment window (engine rule v2.4: clamp(0.45 x min neighbour gap, 65, 110) ms each side, PERFECT ±40 ms): min ±70 ms, median ±110 ms, 212 of 468 taps below the ±110 ms cap. My recommendation stays perfect ±60 / accept ±110 ms where the music allows; the engine rule is what ships.
- Snapping: 354/468 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Difficulty calibration vs original Dancing Line levels

- Tier: **hard (title track)**.
- **Average CPM** (all taps ÷ song length × 60): **132** (2.20 taps/s).
- **Average CPM, wiki-style** (mean of instantaneous 60/gap over all gaps; the wiki does not publish its formula, but The Racing's 220 vs 149 by total ÷ length suggests a gap-based mean): **177** (median 136).
- **Peak CPM** (60 ÷ smallest gap): **385** (min gap 156 ms). Sustained peak over the densest 2 s: 10 taps = 300 CPM.
- Fast bursts (2-4 taps, gaps < 195 ms, i.e. faster than any 8th note at this tempo): **6**: 4@43.93s (385 CPM), 3@63.55s (345 CPM), 3@165.52s (385 CPM), 4@170.09s (385 CPM), 4@185.20s (382 CPM), 4@192.76s (382 CPM)
- Syncopation: 21 dotted-8th gaps (3 sixteenths ≈ 354 ms); 47 of 468 taps (10%) sit off the 8th grid (16th off-beats / tresillo pushes).
- Every burst tap sits on a real onset of the drum, vocal or melody stem inside a genuinely dense passage (fills, build-ups, drop entries, final choruses). True 16ths at 127 BPM are 118 ms apart, below the schema's hard 150 ms minimum gap, so straight 16th rolls cannot be charted; the bursts use the fastest real events that clear 150 ms (8th-note triplet hats, swung 16ths, rapid syllables). That caps the peak at about 330-395 CPM instead of 400-460: 60 ÷ 0.150 s is exactly 400 CPM, and The Racing's own 136 ms 16ths would fail this schema too. Reaching 400-460 CPM needs the integrator to lower the schema floor to about 0.13 s; the build already supports that (spec.BURST_MIN), and the true 16th rolls are present in the stems (e.g. hat/snare rolls in fills).

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
| **omg (this chart)** | 3:32 | 468 | 177 (wiki-style) / 132 (taps÷len) | 385 | engine window min ±70 ms, median ±110 ms, 212 of 468 taps below the ±110 ms cap |

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 病房走廊 | intro | 12 | 0.79 | 1.5/s |
| 15.15 | Verse 1 · 治疗桌与五椅 | verse | 29 | 1.92 | 2.5/s |
| 30.26 | Verse 1b · 墙板外折 | verse | 32 | 2.12 | 4.5/s |
| 45.38 | Chorus 1 · 黑兔舞台 | chorus | 42 | 2.78 | 3.5/s |
| 60.50 | Verse 2 · 玻璃鞋 | verse | 33 | 2.18 | 3.0/s |
| 75.62 | Verse 2b · 双折长短路 | pre | 29 | 1.92 | 3.0/s |
| 90.73 | Pre · 手机桥 | break | 28 | 1.85 | 4.0/s |
| 105.85 | Chorus 2 · 屏幕块 | chorus | 43 | 2.84 | 3.5/s |
| 120.97 | Post · 错列直角 | post | 23 | 1.74 | 2.5/s |
| 134.20 | Bridge · 书页墙与猫 | bridge | 40 | 2.65 | 3.5/s |
| 149.32 | Break · 书页合拢 | break | 3 | 1.59 | 1.5/s |
| 151.21 | Dance break · 舞台五墙 | drop | 47 | 3.11 | 4.5/s |
| 166.32 | Final chorus · 兔耳发夹 | chorus | 45 | 2.98 | 4.5/s |
| 181.44 | Final chorus b · 天桥 | chorus | 48 | 3.18 | 5.0/s |
| 196.56 | Outro · 尾奏琴键 | outro | 14 | 0.89 | 1.5/s |

## Tag mix

kick: 253, melody: 86, snare: 58, vocal: 28, bass: 24, hat: 19

## Section rationale (which audio events the taps follow)

- **Intro (0–15.2 s)** — a-cappella "OMG" vocal phrases only (no drums in the stem map): 12 taps on the sung syllable entries, 1–4 s gaps = the "waiting for the call" calm.
- **Verse 1 (15.2–30.3 s)** — finger-snap/clap layer enters with strong hits on step 6 and 14 (the "and" of 2 and 4) — taps on the clap downbeat + those syncopated snaps (s.....s.s.....s.): the first syncopation the player meets.
- **Verse 1b (30.3–45.4 s)** — full UK-garage kick enters (K...|k...|..k.|..kk / ..K.|k.kk|.kk.|K...): taps on the kicks, odd bars use the off-beat kick pair at steps 2/4 and 10/12 = call (even bar) / response (odd bar).
- **Chorus 1 / 2 / Final (45.4, 105.9, 166.4 s)** — halftime groove: kick 1, snare 3, kick on 4; the synth hook (other stem, "O" hits on steps 4/8/14 then 6/10/14) answers between drum hits, so even bars are drum-led and odd bars become a 6-tap 8th-note run (2,6,8,10,12,14) following the hook. Final chorus b adds the extra hook 8th (step 6) for the climax.
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
| change → Chorus 1 | 45.863 | melody | other (str 0.38) | +0 | +8 |
| change → Verse 2 | 60.952 | kick | kick (str 0.27) | -0 | +40 |
| change → Verse 2b | 76.070 | kick | kick (str 0.51) | +0 | +19 |
| change → Pre | 90.771 | bass | bass (str 0.16) | -0 | -40 |
| change → Chorus 2 | 106.359 | melody | other (str 0.31) | -0 | -15 |
| change → Post | 122.134 | kick | kick (str 0.77) | -0 | +50 |
| change → Bridge | 134.535 | kick | kick (str 0.54) | +0 | +13 |
| change → Break | 149.546 | snare | kick (str 0.16) | -0 | +33 |
| change → Dance break | 151.661 | kick | kick (str 0.33) | +0 | +23 |
| change → Final chorus | 166.808 | melody | other (str 0.33) | +0 | -8 |
| change → Final chorus b | 181.442 | kick | bass (str 0.20) | -3 | +25 |
| change → Outro | 197.058 | melody | other (str 0.70) | -0 | -17 |
| middle | 116.005 | melody | other (str 0.44) | +0 | +19 |
| middle | 116.247 | kick | bass (str 0.13) | -11 | +31 |
| middle | 116.483 | melody | other (str 0.21) | +10 | +1 |
| middle | 116.719 | kick | bass (str 0.32) | -4 | +38 |
| middle | 116.955 | melody | vocals (str 0.38) | +14 | +14 |
| end | 206.714 | melody | other (str 0.92) | +0 | -0 |
| end | 207.202 | melody | other (str 0.56) | +0 | +0 |
| end | 208.370 | melody | none within 80 ms | — | — |
| end | 209.555 | melody | other (str 0.51) | +0 | +0 |

Whole chart vs FULL-MIX onset detector (not used for snapping): 444/468 taps have a full-mix onset within 80 ms; |offset| median 15.5 ms, p90 42.3 ms.
- first 25%: n=91, median 10.7 ms, p90 39.2 ms
- 25-50%: n=107, median 23.1 ms, p90 43.8 ms
- 50-75%: n=123, median 18.5 ms, p90 44.3 ms
- last 25%: n=123, median 13.8 ms, p90 37.6 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.