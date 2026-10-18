# ditto — chart report (worker w2)

- Audio: `public/audio/ditto.mp3`, full length 185.507 s, untouched. Grid: 134.0 BPM, beat0 0.311 s (fit to demucs drum stem).
- **Old (v1) taps: 181 → new: 412  (×2.28)**. Average 2.22 taps/s (133 CPM).
- Min gap 110 ms (design floor = one 8th note = 224 ms; snapped taps never closer than road-geometry floor). Median gap 339 ms.
- **Fastest run: 7 consecutive taps at 8th-note spacing (224 ms ≈ 4.5 taps/s) from 41.266 s to 42.624 s.**
- 8th-note runs ≥6 taps: 7; ≥8 taps: 0. Longest 5: 7@41.3s, 6@35.9s, 6@98.6s, 6@140.9s, 6@146.9s
- Judgment window (engine rule v2.5 per tap: min(0.5·g, clamp(0.45·g, 45, 110)) ms each side, g = smaller neighbour gap; PERFECT ±40 ms): min ±49 ms, median ±106 ms, 223 of 412 taps below the ±110 ms cap. My recommendation stays perfect ±60 / accept ±110 ms where the music allows; the engine rule is what ships.
- Snapping: 372/412 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Difficulty calibration vs original Dancing Line levels

- Tier: **hard (title track)**.
- **Average CPM** (all taps ÷ song length × 60): **133** (2.22 taps/s).
- **Average CPM, wiki-style** (mean of instantaneous 60/gap over all gaps; the wiki does not publish its formula, but The Racing's 220 vs 149 by total ÷ length suggests a gap-based mean): **186** (median 177).
- **Peak CPM, instantaneous** (60 ÷ smallest gap): **545** (min gap 110 ms). Sustained peak over the densest 2 s: 10 taps = 300 CPM.
- Fast bursts (2-4 taps, gaps < 190 ms, i.e. clearly faster than an 8th note at this tempo): **7**: 4@28.04s (545 CPM), 3@74.40s (536 CPM), 3@114.01s (545 CPM), 3@140.88s (545 CPM), 4@142.67s (545 CPM), 4@152.57s (545 CPM), 4@167.76s (545 CPM)
- Syncopation: 82 dotted-8th gaps (3 sixteenths ≈ 336 ms); 61 of 412 taps (15%) sit off the 8th grid (16th off-beats / tresillo pushes).
- Every burst tap sits on a real onset of the drum, vocal or melody stem inside a genuinely dense passage (fills, build-ups, drop entries, final choruses); bursts are never placed on silence or used as filler. Schema v2.5 floor is 0.105 s; true 16ths at 134 BPM are 112 ms apart, so straight 16th rolls are charted directly.
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
| **ditto (this chart)** | 3:05 | 412 | 186 (wiki-style) / 133 (taps÷len) | 360 (1 s window) / 545 (60÷min gap) | engine window min ±49 ms, median ±106 ms, 223 of 412 taps below the ±110 ms cap |

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 录像带入口 | intro | 14 | 0.96 | 1.5/s |
| 14.64 | Verse 1 · 教室走廊 | verse | 37 | 2.58 | 4.5/s |
| 28.97 | Chorus 1 · 摄像机取景框 | chorus | 41 | 2.86 | 4.0/s |
| 43.30 | Post 1 · 屋顶坡道 | post | 32 | 2.55 | 3.0/s |
| 55.83 | Break · 雪地鹿岛 | break | 8 | 0.89 | 1.5/s |
| 64.79 | Verse 2a · 雾隙 | verse | 13 | 1.81 | 2.5/s |
| 71.95 | Verse 2 · 窗墙长 U | verse | 32 | 2.23 | 3.5/s |
| 86.28 | Chorus 2 · 屋顶空椅 | chorus | 44 | 3.07 | 4.0/s |
| 100.61 | Post 2 · 跨空桥 | post | 35 | 2.44 | 3.5/s |
| 114.94 | Bridge · 鹿回头 | bridge | 22 | 1.54 | 2.5/s |
| 129.27 | Pre · 取景屏 | pre | 22 | 1.75 | 3.5/s |
| 141.80 | Final chorus · 记忆庭院 | chorus | 56 | 3.47 | 5.0/s |
| 157.92 | Final post · 网点兔 | chorus | 43 | 3.00 | 4.5/s |
| 172.25 | Fade · 暖窗熄灭 | outro | 11 | 1.54 | 2.0/s |
| 179.41 | Outro · 录像带合上 | outro | 2 | 0.33 | 1.0/s |

## What the taps follow (one audible layer per section)

| section | layer followed | share | bursts (full-mix audible 16th figures) | notes |
|---|---|---:|---|---|
| Intro · 录像带入口 | synth / melody hook | 93% | - | sparse on purpose (breathing room); removed faint taps at 2.90, 14.41 s |
| Verse 1 · 教室走廊 | kick + snare drum groove | 100% | 28.04-28.40 s | same pattern every repeat of this phrase |
| Chorus 1 · 摄像机取景框 | kick + snare drum groove | 100% | - | same pattern every repeat of this phrase |
| Post 1 · 屋顶坡道 | snare / clap backbeat | 97% | - | same pattern every repeat of this phrase |
| Break · 雪地鹿岛 | vocal syllables | 100% | - | sparse on purpose (breathing room) |
| Verse 2a · 雾隙 | snare / clap backbeat | 62% | - | same pattern every repeat of this phrase |
| Verse 2 · 窗墙长 U | kick drum | 100% | 74.40-74.63 s | same pattern every repeat of this phrase; removed faint taps at 72.29 s |
| Chorus 2 · 屋顶空椅 | kick drum | 100% | - | same pattern every repeat of this phrase |
| Post 2 · 跨空桥 | kick drum | 100% | 114.01-114.23 s | same pattern every repeat of this phrase |
| Bridge · 鹿回头 | vocal syllables | 100% | - | same pattern every repeat of this phrase; removed faint taps at 119.53, 120.09, 123.15 s |
| Pre · 取景屏 | snare / clap backbeat | 74% | 140.88-141.10 s | same pattern every repeat of this phrase |
| Final chorus · 记忆庭院 | kick + snare drum groove | 100% | 152.57-152.98 s, 142.67-143.02 s | same pattern every repeat of this phrase |
| Final post · 网点兔 | kick drum | 100% | 167.76-168.10 s | same pattern every repeat of this phrase |
| Fade · 暖窗熄灭 | kick + snare drum groove | 100% | - | sparse on purpose (breathing room) |
| Outro · 录像带合上 | snare / clap backbeat | 100% | - | sparse on purpose (breathing room) |

## Tag mix

kick: 246, snare: 94, vocal: 41, melody: 17, hat: 14

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
| start | 3.917 | melody | other (str 0.24) | -0 | — |
| start | 4.789 | melody | none within 80 ms | — | — |
| start | 5.684 | melody | none within 80 ms | — | — |
| change → Verse 1 | 14.639 | snare | other (str 0.58) | +5 | -18 |
| change → Chorus 1 | 29.399 | kick | kick (str 0.68) | +0 | -1 |
| change → Post 1 | 43.727 | snare | kick (str 0.34) | -0 | +1 |
| change → Break | 55.824 | vocal | vocals (str 0.58) | -0 | -0 |
| change → Verse 2a | 65.223 | snare | snare (str 0.36) | -0 | — |
| change → Verse 2 | 72.607 | kick | kick (str 0.20) | +0 | +0 |
| change → Chorus 2 | 86.281 | kick | other (str 0.62) | +5 | -14 |
| change → Post 2 | 100.929 | kick | kick (str 0.40) | +0 | +49 |
| change → Bridge | 115.175 | vocal | vocals (str 0.49) | -0 | +6 |
| change → Pre | 129.703 | snare | kick (str 0.15) | -0 | +31 |
| change → Final chorus | 141.803 | kick | bass (str 0.21) | +14 | -12 |
| change → Final post | 158.577 | kick | kick (str 0.34) | +0 | +37 |
| change → Fade | 172.251 | kick | bass (str 0.25) | -10 | -10 |
| change → Outro | 180.753 | snare | kick (str 0.42) | +0 | -65 |
| middle | 95.891 | kick | kick (str 0.27) | -0 | +32 |
| middle | 96.117 | kick | kick (str 0.65) | -0 | +23 |
| middle | 96.764 | kick | kick (str 0.20) | +0 | +63 |
| middle | 97.011 | kick | kick (str 0.20) | +1 | +16 |
| middle | 97.347 | kick | kick (str 0.27) | -0 | +4 |
| end | 178.504 | kick | kick (str 0.23) | -0 | +4 |
| end | 179.399 | snare | snare (str 0.51) | +0 | +0 |
| end | 180.753 | snare | kick (str 0.42) | +0 | -65 |
| end | 181.760 | snare | kick (str 0.14) | -0 | — |

Whole chart vs FULL-MIX onset detector (not used for snapping): 392/412 taps have a full-mix onset within 80 ms; |offset| median 13.5 ms, p90 40.2 ms.
- first 25%: n=83, median 10.5 ms, p90 33.8 ms
- 25-50%: n=94, median 11.3 ms, p90 33.2 ms
- 50-75%: n=96, median 15.7 ms, p90 45.3 ms
- last 25%: n=119, median 14.9 ms, p90 39.8 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.