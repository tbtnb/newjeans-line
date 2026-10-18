# OMG chart audit (old chart: 402 taps) and re-chart (451 taps)

Branch `chart-research`. Raw data is in `analysis/research/`:
- `omg-audit-{old,new}.txt`
- `omg-sections-{old,new}.md`
- `omg-problems-{old,new}.txt`
- `omg-barmap-*.txt`
- `omg-profile-*.txt`
- `omg-taps-{old,new}.json`
- `omg-chartlogic-new.md`

## Method
- **Audio.** Gapless ffmpeg decode of `public/audio/omg.mp3`. It matches Chrome's `decodeAudioData` sample for sample (9,360,372 samples, cross-correlation lag 0).
- **Stems.**
  - The demucs stems in `/workspace/w2-stems/htdemucs/omg` are 1105 samples (25.1 ms) late, because they kept the mp3 encoder delay.
  - All stem analysis is shifted back by cross-correlation against the mix.
  - `tools/audio/vocal_env.py` had the same 25 ms lag and was fixed, and `analysis/omg.env.npz` regenerated. Other songs' envelopes were built from mp3 stems that are about 46 ms late and still need a re-run.
- **Onsets.** `tools/research/onsets.py` computes log-mel spectral flux (hop 128 at 44.1 kHz).
  - Calibrated on synthetic noise, kick and pluck hits: the peak is about 7 ms early, corrected with a -7.2 ms adjustment.
  - Peak picking keeps the strongest peak and suppresses neighbours within 60 ms (non-maximum suppression).
  - Layers: full mix; kick, snare and hat (bands of the drums stem); vocals; bass; other.
- **Grid.** 127.003 BPM, beat0 = 0.011 s, fitted on the gapless kick/snare. The old chart's meta beat0 of 0.0288 came from the late stems.

## 1. Per-tap timing: no systematic offset
Median offset from each old tap to the nearest strong onset:

| layer | median | IQR |
|---|---|---|
| full | +1.2 ms | -9.3..+3.3 |
| kick | +1.5 ms | |
| snare | +0.3 ms | |
| vocals | -0.3 ms | |

- **The old taps are not late or early.** The systematic chart offset is about +1 ms, which is negligible.
- The -17.8 ms "grid error" shows up only against the chart's own late meta grid. Against the true grid the taps are on time.
- Only 1 tap lacked an onset of at least 0.4.
- **Conclusion:** the off-beat feeling does not come from millisecond timing in the chart file. It comes from which beats were chosen (below). Any global latency or visual lag is handled by the audio/camera worker.

## 2. Grid snap / which beats are tapped (old chart)
Across the whole song:
- on quarter beats: 51%
- 8th off-beats: 41%
- 16ths: 8%
- strong quarter-beat accents tapped: 181/297

| section | follows (de facto) | on-beat | 16th | strong beats tapped | issue |
|---|---|---|---|---|---|
| Intro | vocal | 33% | 67% | 2/9 | 16th vocal syncopations (steps 5/9/13, 7/11) |
| Verse 1 | snare/vocal mix | 48% | 0 | 5/13 | 0/6/14 pattern skips backbeats |
| Verse 1b | snare | 43% | 3% | 12/26 | `0 10 14` bars skip beats 2–4 |
| Chorus 1 | drums | 68% | 0 | 20/24 | good; last bar `2 10 14` is off-beat only |
| Verse 2 | snare | 50% | 0 | 17/30 | `0 4 10 14` skips beats 3–4 |
| Verse 2b | snare | 55% | 3% | 16/28 | `2 10 12` skips the downbeat |
| Pre | bass | 26% | 0 | 3/12 | whole bars of off-beat-only taps `2 6 10 14` (bars 49, 51, 53) |
| Chorus 2 | drums | 73% | 0 | 19/24 | good |
| Post | syncopation | 26% | 13% | 6/23 | clap on 4/12 replaced by 10/14/2/7 |
| Bridge | synth figure | 22% | 49% | 9/23 | never taps the downbeat; `3 6 8 13 15` |
| Dance break | drums | 70% | 0 | 31/31 | good |
| Final chorus a/b | drums | 72–74% | 0 | 38/45 | good |
| Outro | piano | 9% | 0 | 1/7 | taps only step 14; skips the piano stabs on 1/3 |

## 3. Problems by time (old chart)
`step` = 16th position in the bar (0 = downbeat, 4/12 = backbeats). The full 35-row list is in `analysis/research/omg-problems-old.txt`. Grouped:

| time (s) | bar | section | taps (steps) | problem |
|---|---|---|---|---|
| 3.79, 13.24 | 2, 7 | Intro | 5 9 13 / 7 11 | off-beat-only bars with 16th syncopation on weak onsets |
| 11.35 | 6 | Intro | – | strong beats 2 and 4 not tapped |
| 15.13–26.47 | 8, 14 | Verse 1 | 6 8 14 / 0 6 8 14 | beats 1–2 / 2 and 4 (snare 2.3) not tapped |
| 30.25–41.58 | 16, 18, 22 | Verse 1b | 0 10 14 | beats 2–4 not tapped every other bar |
| 58.59 | 31 | Chorus 1 | 2 10 14 | phrase-end bar with no on-beat tap |
| 60.48–73.71 | 32–39 | Verse 2 | 0 4 10 14 | beats 3 and 4 not tapped in every even bar |
| 77.49–85.05 | 41–45 | Verse 2b | 2 10 12 | downbeat and beat 2 skipped |
| 90.72–102.06 | 48–54 | Pre | 2 6 10 14 | off-beat-only bars while the kick hits 1/3; weak tap 100.42 |
| 120.95–132.29 | 64–70 | Post | 0 10 14 / 2 7 10 12 | backbeat clap skipped; 16th at step 7 |
| 134.18–147.41 | 71–78 | Bridge | 3 6 8 13 15 | downbeat never tapped; mostly 16ths |
| 200.32, 207.88 | 106, 110 | Outro | 14 | piano stab on beat 3 (2.1–2.2) not tapped |

Chorus consistency: all four choruses already share the same A/B bar pair (`0 8 12 14` / `2 4 8 12`). Only the last bars differ, as fills.

## 4. Why it felt off-beat
1. **Skipped pulse.** About 40% of the strong quarter-beat accents (116/297) had no tap. Verses, Post and Bridge skip the backbeat clap or the downbeat. In Dancing Line a straight segment over a loud clap reads as "the turn missed the beat", the same complaint made on the wiki about the Racing level's last section.
2. **Off-beat-only bars.** In the Pre section (bars 49/51/53) the player turns only between kicks.
3. **16th syncopation on soft sounds.** The intro vocal and the bridge figure use positions 3/5/7/9/13/15 that are hard to feel against a loud 4/4 groove.
4. **Layer hopping inside sections** (vocal ↔ snare ↔ bass) with no musical reason.
5. **Not caused by the chart:** taps were within about 1 ms of real onsets, so any remaining "late" feel is global latency or render lag, handled by another worker.

## 5. Re-chart (451 taps)
Generator: `tools/research/omg_rechart.py`. Router: `tools/research/route_omg.py` (seed 25, beam 90).

**Section patterns**

| section | pattern |
|---|---|
| Verse 1 | 0/6/14 clap figure plus 4/8/12 on alternating bars |
| Verse 1b, Verse 2, Verse 2b, Post | 0 4 10 12 (+14) |
| Chorus (all 4 identical) | A bar `0 4 8 12 14`, B bar `2 4 8 12`, fill on bar 8 |
| Pre | vocal syllables, on-beat |
| Bridge | `0 3 6 8 13` + phrase-end fills |
| Dance break | 0/4/8/12 + 8ths |
| Outro | 22 piano stabs |
| Intro | 9 sparse taps on accents |

**Old vs new**

| metric | old | new |
|---|---|---|
| taps | 402 | 451 |
| on quarter beats | 51% | 66% |
| 16ths | 8% | 4% |
| strong beat accents tapped | 181/297 | 251/297 |
| off-beat-only bars | 6 | 0 |
| median onset offset (full) | +1.2 ms | +0.4 ms |
| median abs grid error | 17.9 ms (late meta grid) | 1.9 ms |
| taps with strongest onset < 0.4 | 1 | 0 within ±60 ms |
| borderline weak taps | – | 3 (0.39–0.40 at 3.79, 16.08, 45.13 s) |

Other figures for the new chart:
- Density: average 127 CPM, peak 360 CPM (1 s window).
- Gaps: minimum 0.116 s; three gaps under 0.15 s, all in bridge fills.

**Checks**
- chartlogic: faint 0, weak bursts 0, off-grid 0, hop 4. The four hops (14.903, 93.317, 100.875, 104.891 s) are kick/hat hits under vocal syllables, where chartlogic's band envelopes disagree with the stem detector.
- `levels-design/validate.py`: 0 errors.
- Scripted headless playthrough: complete, 451/451 perfect, 10/10 diamonds; timing error mean 1.5 ms, max 9 ms.
- Click tracks for listening:
  - old chart: `deliverables/omg-clicks.mp3`
  - new chart: `deliverables/omg-clicks-new.mp3`
