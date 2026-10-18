# ditto — chart report (worker w2)

- Audio: `public/audio/ditto.mp3`, full length 185.507 s, untouched. Grid: 134.0 BPM, beat0 0.311 s (fit to demucs drum stem).
- **Old (v1) taps: 181 → new: 406  (×2.24)**. Average 2.19 taps/s (131 CPM).
- Min gap 222 ms (design floor = one 8th note = 224 ms; snapped taps never closer than road-geometry floor). Median gap 339 ms.
- **Fastest run: 7 consecutive taps at 8th-note spacing (224 ms ≈ 4.5 taps/s) from 41.266 s to 42.624 s.**
- 8th-note runs ≥6 taps: 6; ≥8 taps: 0. Longest 5: 7@41.3s, 6@35.9s, 6@98.6s, 6@141.3s, 6@146.9s
- Judgment window (engine rule v2.4: clamp(0.45 x min neighbour gap, 65, 110) ms each side, PERFECT ±40 ms): min ±100 ms, median ±106 ms, 211 of 406 taps below the ±110 ms cap. My recommendation stays perfect ±60 / accept ±110 ms where the music allows; the engine rule is what ships.
- Snapping: 360/406 taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).

## Per-section density

| t (s) | section | kind | taps | taps/s | densest 2 s |
|---|---|---|---:|---:|---:|
| 0.00 | Intro · 录像带入口 | intro | 16 | 1.09 | 2.0/s |
| 14.64 | Verse 1 · 教室走廊 | verse | 36 | 2.51 | 4.0/s |
| 28.97 | Chorus 1 · 摄像机取景框 | chorus | 41 | 2.86 | 4.0/s |
| 43.30 | Post 1 · 屋顶坡道 | post | 32 | 2.55 | 3.0/s |
| 55.83 | Break · 雪地鹿岛 | break | 8 | 0.89 | 1.5/s |
| 64.79 | Verse 2a · 雾隙 | verse | 13 | 1.81 | 2.5/s |
| 71.95 | Verse 2 · 窗墙长 U | verse | 31 | 2.16 | 3.5/s |
| 86.28 | Chorus 2 · 屋顶空椅 | chorus | 44 | 3.07 | 4.0/s |
| 100.61 | Post 2 · 跨空桥 | post | 33 | 2.30 | 3.5/s |
| 114.94 | Bridge · 鹿回头 | bridge | 25 | 1.74 | 2.5/s |
| 129.27 | Pre · 取景屏 | pre | 19 | 1.52 | 2.5/s |
| 141.80 | Final chorus · 记忆庭院 | chorus | 54 | 3.35 | 4.0/s |
| 157.92 | Final post · 网点兔 | chorus | 41 | 2.86 | 3.5/s |
| 172.25 | Fade · 暖窗熄灭 | outro | 11 | 1.54 | 2.0/s |
| 179.41 | Outro · 录像带合上 | outro | 2 | 0.33 | 1.0/s |

## Tag mix

kick: 253, snare: 94, vocal: 45, melody: 14

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
| middle | 94.670 | kick | kick (str 0.28) | +0 | +8 |
| middle | 95.000 | kick | kick (str 0.35) | -0 | -3 |
| middle | 95.236 | kick | bass (str 0.30) | -1 | -13 |
| middle | 95.891 | kick | kick (str 0.27) | -0 | +32 |
| middle | 96.117 | kick | kick (str 0.65) | -0 | +23 |
| end | 178.504 | kick | kick (str 0.23) | -0 | +4 |
| end | 179.399 | snare | snare (str 0.51) | +0 | +0 |
| end | 180.753 | snare | kick (str 0.42) | +0 | -65 |
| end | 181.760 | snare | kick (str 0.14) | -0 | — |

Whole chart vs FULL-MIX onset detector (not used for snapping): 385/406 taps have a full-mix onset within 80 ms; |offset| median 12.6 ms, p90 40.9 ms.
- first 25%: n=83, median 9.1 ms, p90 36.4 ms
- 25-50%: n=93, median 11.2 ms, p90 33.3 ms
- 50-75%: n=97, median 15.6 ms, p90 47.9 ms
- last 25%: n=112, median 12.7 ms, p90 39.8 ms

Caveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.