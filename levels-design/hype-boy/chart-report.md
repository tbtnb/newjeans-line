# Hype Boy — chart report

- Audio: `public/audio/hype-boy.mp3` (full track, 176.59 s, untouched). Times = seconds from first decoded sample.
- Tempo grid measured from the audio: **99.99 BPM**, beat 0.6000 s, downbeat phase 0.252 s (constant-tempo fit maximising onset strength).
- **Old taps: 140** (shipped `src/levels.json`; `reports/rhythm-chart-baseline.json` had 180). **New taps: 295** = **2.11x**.
- Speed 9.0 u/s, road width 2.2 → narrowest 1.9.
- Min gap **0.267 s**, median gap 0.450 s, mean density 1.67 taps/s.
- Fastest consecutive run (8th notes, every gap ≤ 0.330 s): **7 taps**, 66.862–68.657 s (mean interval 0.299 s).
- Validator definition (gaps ≤ 0.30 s): longest run 4 taps from 76.463 s.
- Longest unbroken run at ≤ 1 beat spacing (≤ 0.660 s): 52 taps from 148.329 s.
- Peak 2-second density: **3.5 taps/s** at 66.75 s.
- Recommended judgment window: **±90 ms** (perfect ±35 ms). Must stay < half the min gap (133 ms) so a tap never resolves to the neighbouring turn; ±90 ms ≈ the old engine's ±100 ms but tighter for the dense songs. Needs confirmation with real touch latency (not yet tested on devices).
- Hard floor respected: no gap < 0.15 s. Humanly-playable minimum used here: 0.267 s.

## Per-section density

| Section | Kind | Start | End | Taps | Taps/s | Min gap | Main tap sources |
|---|---|---|---|---|---|---|---|
| Intro riff | intro | 0.00 | 19.45 | 17 | 0.87 | 0.600 | snare 14, melody 3 |
| Verse 1 | verse | 19.45 | 38.65 | 30 | 1.56 | 0.284 | kick 13, snare 9, vocal 8 |
| Pre-chorus 1 | pre | 38.65 | 48.25 | 11 | 1.15 | 0.300 | vocal 10, kick 1 |
| Build 1 | pre | 48.25 | 53.05 | 9 | 1.88 | 0.300 | vocal 4, snare 3, kick 2 |
| Chorus 1 | chorus | 53.05 | 72.25 | 39 | 2.03 | 0.267 | vocal 20, kick 16, snare 2 |
| Post-chorus 1 | post | 72.25 | 91.45 | 35 | 1.82 | 0.283 | kick 18, vocal 15, snare 2 |
| Verse 2 | verse | 91.45 | 115.45 | 41 | 1.71 | 0.289 | kick 22, vocal 10, snare 9 |
| Pre-chorus 2 | pre | 115.45 | 125.05 | 11 | 1.15 | 0.300 | vocal 10, kick 1 |
| Build 2 | pre | 125.05 | 129.85 | 8 | 1.67 | 0.290 | snare 4, vocal 3, kick 1 |
| Chorus 2 | chorus | 129.85 | 149.05 | 40 | 2.08 | 0.299 | kick 22, vocal 15, snare 2 |
| Final chorus | chorus | 149.05 | 170.65 | 53 | 2.45 | 0.279 | kick 28, vocal 13, snare 10 |
| Outro | outro | 170.65 | 176.59 | 1 | 0.17 | 0.000 | kick 1 |

## How taps were chosen (rationale)


Hype Boy 100 BPM (beat 0.600 s, downbeat 0.252 s). 295 taps (old 140, 2.11x). 16th grid used for syncopation (moombah/dembow kick 1, a-of-2, 3, a-of-4; snare 3+3+2) but never two adjacent 16ths: min gap 0.267 s. Intro on riff beats, pre-choruses are vocal call-and-response, choruses mix kick/snare with vocal hook syllables. Recommended judgment window +-90 ms.

Method (honest description): candidates = every 8th (or 16th where the groove is syncopated) on the measured beat grid. Each candidate is scored by the onset strength of the separated stems at that instant (vocal syllable onsets from the htdemucs vocal stem, kick 30–140 Hz / snare-clap 1.2–8 kHz from the percussive part of the accompaniment stem, bass and harmonic accents), with per-section weights and a metric bonus for strong beats. **Per section I set by hand**: the density target (follows energy: intro < verse < pre < chorus/climax), which sources lead (vocal phrasing in verses/pre-choruses, drums+hook in choruses), the grid resolution, the minimum gap and the maximum run length, plus forced taps on section downbeats/impacts. The selected slot is then snapped to the actual onset peak if within ±18 ms, otherwise kept on the grid. Repeated musical material therefore gets repeated tap patterns (DL-style), and long gaps stay where the music breathes. All demucs-derived times are corrected by −25.03 ms (stem latency vs ffmpeg/browser decode).

## Alignment spot checks (start / section changes / middle / end)

Offset = (audio event time − tap time). 'Nearest onset' = nearest peak of the full-mix onset-strength envelope (height>0.12, ≥46 ms apart); 'band peak' = peak of the tagged source envelope within ±60 ms; 'grid' = distance to nearest 16th of the beat grid.

| Where | Tap t (s) | Tag | Nearest full-mix onset (ms) | Tagged-band peak (ms) | Grid dev (ms) |
|---|---|---|---|---|---|
| start | 1.452 | melody | -1 | +34 | -0 |
| start | 2.652 | melody | +7 | +42 | -0 |
| start | 5.052 | snare | +10 | -25 | -0 |
| → Verse 1 | 19.453 | kick | +5 | -18 | -0 |
| → Pre-chorus 1 | 38.505 | kick | +5 | +29 | +0 |
| → Build 1 | 48.255 | snare | -4 | -39 | -0 |
| → Chorus 1 | 53.046 | kick | -46 | -0 | -10 |
| → Post-chorus 1 | 71.957 | kick | +13 | -33 | +0 |
| → Verse 2 | 91.458 | kick | +5 | -29 | -0 |
| → Pre-chorus 2 | 115.310 | kick | +12 | +24 | +0 |
| → Build 2 | 125.060 | snare | -9 | -44 | -0 |
| → Chorus 2 | 129.861 | kick | +8 | -27 | +0 |
| → Final chorus | 149.062 | kick | -25 | -25 | +0 |
| → Outro | 172.463 | kick | -8 | -20 | -0 |
| middle | 95.666 | kick | +0 | +0 | +8 |
| middle | 96.258 | kick | +0 | -23 | -0 |
| middle | 97.458 | vocal | -4 | +31 | -0 |
| end | 167.963 | kick | -1 | -36 | -0 |
| end | 168.263 | kick | +0 | -34 | -0 |
| end | 172.463 | kick | -8 | -20 | -0 |

Whole chart: |offset to nearest full-mix onset| median 6 ms, 90th pct 35 ms; |offset to tagged-band peak| median 26 ms, 90th pct 38 ms.

Per-section median |offset to tagged-band peak| (ms): Intro riff 35, Verse 1 26, Pre-chorus 1 31, Build 1 25, Chorus 1 0, Post-chorus 1 20, Verse 2 26, Pre-chorus 2 29, Build 2 15, Chorus 2 27, Final chorus 28, Outro 20

Caveats: alignment is measured against analysis envelopes, not by listening on a device; the integrator must verify in-engine with the audio clock (output latency handled by the engine). Section boundaries come from bass/drum/vocal energy changes and 4-bar novelty and are approximate labels where noted.