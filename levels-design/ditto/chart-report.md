# ditto — chart report (worker w2)

- Audio: `public/audio/ditto.mp3`, full length 185.507 s, untouched. Grid: 134.0 BPM, beat0 0.311 s (fit to demucs drum stem).
- **Old (v1) taps: 181 → new: 422  (×2.33)**. Average 2.27 taps/s (136 CPM).
- Min gap 154 ms (design floor = one 8th note = 224 ms; snapped taps never closer than road-geometry floor). Median gap 336 ms.
- **Fastest run: 7 consecutive taps at 8th-note spacing (224 ms ≈ 4.5 taps/s) from 41.266 s to 42.624 s.**
- 8th-note runs ≥6 taps: 6; ≥8 taps: 0. Longest 5: 7@41.3s, 6@28.0s, 6@35.9s, 6@98.6s, 6@146.9s
- Judgment window (engine rule v2.4: clamp(0.45 x min neighbour gap, 65, 110) ms each side, PERFECT ±40 ms): min ±69 ms, median ±105 ms, 234 of 422 taps below the ±110 ms cap. My recommendation stays perfect ±60 / accept ±110 ms where the music allows; the engine rule is what ships.
- Snapping: 383/422 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Difficulty calibration vs original Dancing Line levels

- Tier: **hard (title track)**.
- **Average CPM** (all taps ÷ song length × 60): **136** (2.27 taps/s).
- **Average CPM, wiki-style** (mean of instantaneous 60/gap over all gaps; the wiki does not publish its formula, but The Racing's 220 vs 149 by total ÷ length suggests a gap-based mean): **184** (median 179).
- **Peak CPM** (60 ÷ smallest gap): **390** (min gap 154 ms). Sustained peak over the densest 2 s: 9 taps = 270 CPM.
- Fast bursts (2-4 taps, gaps < 195 ms, i.e. faster than any 8th note at this tempo): **11**: 4@21.84s (375 CPM), 4@27.98s (380 CPM), 3@33.96s (333 CPM), 3@38.69s (377 CPM), 4@74.21s (368 CPM), 4@84.35s (366 CPM), 4@105.85s (375 CPM), 3@141.22s (390 CPM), 4@151.19s (361 CPM), 4@164.51s (387 CPM), 4@170.94s (375 CPM)
- Syncopation: 86 dotted-8th gaps (3 sixteenths ≈ 336 ms); 74 of 422 taps (18%) sit off the 8th grid (16th off-beats / tresillo pushes).
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
| **ditto (this chart)** | 3:05 | 422 | 184 (wiki-style) / 136 (taps÷len) | 390 | engine window min ±69 ms, median ±105 ms, 234 of 422 taps below the ±110 ms cap |

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 录像带入口 | intro | 16 | 1.09 | 2.0/s |
| 14.64 | Verse 1 · 教室走廊 | verse | 39 | 2.72 | 4.5/s |
| 28.97 | Chorus 1 · 摄像机取景框 | chorus | 43 | 3.00 | 4.0/s |
| 43.30 | Post 1 · 屋顶坡道 | post | 32 | 2.55 | 3.0/s |
| 55.83 | Break · 雪地鹿岛 | break | 8 | 0.89 | 1.5/s |
| 64.79 | Verse 2a · 雾隙 | verse | 13 | 1.81 | 2.5/s |
| 71.95 | Verse 2 · 窗墙长 U | verse | 36 | 2.51 | 4.0/s |
| 86.28 | Chorus 2 · 屋顶空椅 | chorus | 44 | 3.07 | 4.0/s |
| 100.61 | Post 2 · 跨空桥 | post | 33 | 2.30 | 4.0/s |
| 114.94 | Bridge · 鹿回头 | bridge | 25 | 1.74 | 2.5/s |
| 129.27 | Pre · 取景屏 | pre | 20 | 1.60 | 3.0/s |
| 141.80 | Final chorus · 记忆庭院 | chorus | 56 | 3.47 | 4.0/s |
| 157.92 | Final post · 网点兔 | chorus | 44 | 3.07 | 4.0/s |
| 172.25 | Fade · 暖窗熄灭 | outro | 11 | 1.54 | 2.0/s |
| 179.41 | Outro · 录像带合上 | outro | 2 | 0.33 | 1.0/s |

## Tag mix

kick: 235, snare: 99, vocal: 48, melody: 40

## Section rationale (which audio events the taps follow)

- **Intro (0–14.6 s)** — choir/pad only: 2 taps per bar on the chord changes (beats 1 and 3) — 1 s+ gaps, the camcorder room.
- **Verse 1 (14.6–29.0 s)** — busy Baltimore hat/snare layer (S at steps 0, 5-6, 11, 14): taps on those snare accents (0,6,11,14) → syncopated, with bar 15 an 8-tap 8th fill into the chorus.
- **Chorus 1 (29.0–43.3 s)** — the iconic jersey-club kick K...|K...|K..K|..K. charted exactly (0,4,8,11,14); bars 20 and 23 add the kick-roll 8ths (7-tap runs).
- **Post 1 (43.3–55.8 s)** — snare-led 16th groove: taps on the loud snares (0,4,6,9,12,14 / 0,4,8,12,14) — 3–3.4 taps/s while the road climbs the bleachers.
- **Break & Verse 2a (55.8–72.0 s)** — drums cut out: taps follow the sung syllables (vocal stem onsets, ≥ 1 beat apart), then the light claps on 2 and 4 return — the breathing room (≈1 tap/s).
- **Verse 2 / Chorus 2 / Post 2 (72.0–114.9 s)** — full Baltimore beat: 3+3+2+3+3+2 sixteenth pattern (steps 0,3,6,8,11,14) following kick+snare, alternating with lighter 3–4-tap bars every other bar so phrases breathe; 7-tap 8th roll at 98.8 s.
- **Bridge & Pre (114.9–141.8 s)** — drumless vocal bridge, then claps on 2/4 with the vocal line — low density before the finale.
- **Final chorus / post (141.8–172.3 s)** — tresillo pattern + 8th-note kick rolls every 4th bar on a 1.8-wide road — hardest part.
- **Fade & outro (172.3–185.5 s)** — beat thins and fades: 5→2 taps per bar, last taps on the final snare hits.

## Alignment spot checks (offset = nearest detected onset − tap; independent of snapping source)

| where | tap t (s) | tag | nearest stem onset | stem offset ms | nearest full-mix onset offset ms |
|---|---:|---|---|---:|---:|
| start | 1.654 | vocal | none within 80 ms | — | — |
| start | 2.896 | vocal | vocals (str 0.15) | -0 | — |
| start | 3.917 | melody | other (str 0.24) | -0 | — |
| start | 4.789 | melody | none within 80 ms | — | — |
| change → Verse 1 | 14.639 | snare | other (str 0.58) | +5 | -18 |
| change → Chorus 1 | 29.399 | kick | kick (str 0.68) | +0 | -1 |
| change → Post 1 | 43.727 | snare | kick (str 0.34) | -0 | +1 |
| change → Break | 55.824 | vocal | vocals (str 0.58) | -0 | -0 |
| change → Verse 2a | 65.223 | snare | snare (str 0.36) | -0 | — |
| change → Verse 2 | 72.289 | kick | snare (str 0.19) | -17 | +19 |
| change → Chorus 2 | 86.281 | kick | other (str 0.62) | +5 | -14 |
| change → Post 2 | 100.929 | kick | kick (str 0.40) | +0 | +49 |
| change → Bridge | 115.175 | vocal | vocals (str 0.49) | -0 | +6 |
| change → Pre | 129.703 | snare | kick (str 0.15) | -0 | +31 |
| change → Final chorus | 141.803 | kick | bass (str 0.21) | +14 | -12 |
| change → Final post | 158.242 | kick | kick (str 0.44) | +0 | +22 |
| change → Fade | 172.251 | kick | bass (str 0.25) | -10 | -10 |
| change → Outro | 180.753 | snare | kick (str 0.42) | +0 | -65 |
| middle | 94.104 | kick | kick (str 0.27) | +0 | +43 |
| middle | 94.326 | kick | kick (str 0.72) | -0 | +24 |
| middle | 94.670 | kick | kick (str 0.28) | +0 | +8 |
| middle | 95.000 | kick | kick (str 0.35) | -0 | -3 |
| middle | 95.236 | kick | bass (str 0.30) | -1 | -13 |
| end | 178.504 | kick | kick (str 0.23) | -0 | +4 |
| end | 179.399 | snare | snare (str 0.51) | +0 | +0 |
| end | 180.753 | snare | kick (str 0.42) | +0 | -65 |
| end | 181.760 | snare | kick (str 0.14) | -0 | — |

Whole chart vs FULL-MIX onset detector (not used for snapping): 402/422 taps have a full-mix onset within 80 ms; |offset| median 13.5 ms, p90 43.8 ms.
- first 25%: n=90, median 10.0 ms, p90 40.4 ms
- 25-50%: n=98, median 12.4 ms, p90 39.7 ms
- 50-75%: n=96, median 15.7 ms, p90 48.8 ms
- last 25%: n=118, median 14.4 ms, p90 42.2 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.