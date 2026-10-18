# omg — chart report (worker w2)

- Audio: `public/audio/omg.mp3`, full length 212.253 s, untouched. Grid: 127.004 BPM, beat0 0.0288 s (fit to demucs drum stem).
- **Old (v1) taps: 213 → new: 459  (×2.15)**. Average 2.16 taps/s (130 CPM).
- Min gap 226 ms (design floor = one 8th note = 236 ms; snapped taps never closer than road-geometry floor). Median gap 451 ms.
- **Fastest run: 11 consecutive taps at 8th-note spacing (236 ms ≈ 4.2 taps/s) from 162.054 s to 164.434 s.**
- 8th-note runs ≥6 taps: 15; ≥8 taps: 2. Longest 5: 11@162.1s, 8@104.2s, 6@48.0s, 6@51.8s, 6@55.5s
- Recommended judgment window: perfect ±60 ms, accept ±110 ms. +-110 ms accept window around the geometric corner (early taps beyond -110 ms = turn too early => crash into wall; late beyond +110 ms = run off the edge). 8th-note runs here are 236 ms apart so windows never overlap.
- Snapping: 337/459 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 病房走廊 | intro | 12 | 0.79 | 1.5/s |
| 15.15 | Verse 1 · 治疗桌与五椅 | verse | 29 | 1.92 | 2.5/s |
| 30.26 | Verse 1b · 墙板外折 | verse | 30 | 1.98 | 3.5/s |
| 45.38 | Chorus 1 · 黑兔舞台 | chorus | 42 | 2.78 | 3.5/s |
| 60.50 | Verse 2 · 玻璃鞋 | verse | 32 | 2.12 | 2.5/s |
| 75.62 | Verse 2b · 双折长短路 | pre | 29 | 1.92 | 3.0/s |
| 90.73 | Pre · 手机桥 | break | 28 | 1.85 | 4.0/s |
| 105.85 | Chorus 2 · 屏幕块 | chorus | 43 | 2.84 | 3.5/s |
| 120.97 | Post · 错列直角 | post | 23 | 1.74 | 2.5/s |
| 134.20 | Bridge · 书页墙与猫 | bridge | 40 | 2.65 | 3.5/s |
| 149.32 | Break · 书页合拢 | break | 3 | 1.59 | 1.5/s |
| 151.21 | Dance break · 舞台五墙 | drop | 47 | 3.11 | 4.5/s |
| 166.32 | Final chorus · 兔耳发夹 | chorus | 43 | 2.84 | 3.5/s |
| 181.44 | Final chorus b · 天桥 | chorus | 44 | 2.91 | 4.0/s |
| 196.56 | Outro · 尾奏琴键 | outro | 14 | 0.89 | 1.5/s |

## Tag mix

kick: 263, melody: 89, snare: 58, vocal: 25, bass: 24

## Section rationale (which audio events the taps follow)

- **Intro (0–15.2 s)** — a-cappella "OMG" vocal phrases only (no drums in the stem map): 12 taps on the sung syllable entries, 1–4 s gaps = the "waiting for the call" calm.
- **Verse 1 (15.2–30.3 s)** — finger-snap/clap layer enters with strong hits on step 6 and 14 (the "and" of 2 and 4) — taps on the clap downbeat + those syncopated snaps (s.....s.s.....s.): the first syncopation the player meets.
- **Verse 1b (30.3–45.4 s)** — full UK-garage kick enters (K...|k...|..k.|..kk / ..K.|k.kk|.kk.|K...): taps on the kicks, odd bars use the off-beat kick pair at steps 2/4 and 10/12 = call (even bar) / response (odd bar).
- **Chorus 1 / 2 / Final (45.4, 105.9, 166.4 s)** — halftime groove: kick 1, snare 3, kick on 4; the synth hook (other stem, "O" hits on steps 4/8/14 then 6/10/14) answers between drum hits, so even bars are drum-led and odd bars become a 6-tap 8th-note run (2,6,8,10,12,14) following the hook. Final chorus b adds the extra hook 8th (step 6) for the climax.
- **Verse 2 / 2b / Post** — same garage kick but thinned to 4–5 taps per bar so the vocals breathe; Verse 2b inserts the vocal "V V v v" accent at step 8.
- **Pre (90.8–105.9 s)** — drums drop out, only bass (..B.|..B.|..B.|..B.) + vocal: taps follow the bass pulses at a relaxed 1.9/s while the road ramps up 8 units; bar 55 is a 7-tap 8th-note build into Chorus 2.
- **Bridge (134.2–149.3 s)** — new trap-style kick pattern (...k|..k.|k.k.|.k.k): taps on steps 3,6,8,13,15 / 3,6,8,10,13 — every bar starts on an off-beat, the hardest syncopation in the level, on a narrow 1.8-wide road at night.
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
| middle | 115.077 | melody | other (str 0.39) | -0 | +3 |
| middle | 115.517 | kick | kick (str 0.25) | +0 | +2 |
| middle | 116.005 | melody | other (str 0.44) | +0 | +19 |
| middle | 116.247 | kick | bass (str 0.13) | -11 | +31 |
| middle | 116.483 | melody | other (str 0.21) | +10 | +1 |
| end | 206.714 | melody | other (str 0.92) | +0 | -0 |
| end | 207.202 | melody | other (str 0.56) | +0 | +0 |
| end | 208.370 | melody | none within 80 ms | — | — |
| end | 209.555 | melody | other (str 0.51) | +0 | +0 |

Whole chart vs FULL-MIX onset detector (not used for snapping): 438/459 taps have a full-mix onset within 80 ms; |offset| median 15.5 ms, p90 42.1 ms.
- first 25%: n=90, median 10.7 ms, p90 37.8 ms
- 25-50%: n=106, median 23.3 ms, p90 43.8 ms
- 50-75%: n=123, median 18.5 ms, p90 44.3 ms
- last 25%: n=119, median 13.0 ms, p90 34.0 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.