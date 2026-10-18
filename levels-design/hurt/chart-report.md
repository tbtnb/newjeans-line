# Hurt — chart report

- Audio: `public/audio/hurt.mp3` (full track, 175.01 s, untouched). Times = seconds from first decoded sample.
- Tempo grid measured from the audio: **90.00 BPM**, beat 0.6667 s, downbeat phase 0.260 s (constant-tempo fit maximising onset strength).
- **Old taps: 64** (shipped `src/levels.json`; `reports/rhythm-chart-baseline.json` had 80). **New taps: 144** = **2.25x**.
- Speed 7.5 u/s, road width 2.2 → narrowest 2.0.
- Min gap **0.316 s**, median gap 1.000 s, mean density 0.82 taps/s.
- Fastest consecutive run (8th notes, every gap ≤ 0.367 s): **4 taps**, 88.259–89.269 s (mean interval 0.337 s).
- Validator definition (gaps ≤ 0.30 s): longest run 1 taps from 1.927 s.
- Longest unbroken run at ≤ 1 beat spacing (≤ 0.733 s): 5 taps from 108.261 s.
- Peak 2-second density: **2.5 taps/s** at 139.25 s.
- Recommended judgment window: **±100 ms** (perfect ±35 ms). Must stay < half the min gap (158 ms) so a tap never resolves to the neighbouring turn; ±100 ms ≈ the old engine's ±100 ms but tighter for the dense songs. Needs confirmation with real touch latency (not yet tested on devices).
- Hard floor respected: no gap < 0.15 s. Humanly-playable minimum used here: 0.316 s.

## Per-section density

| Section | Kind | Start | End | Taps | Taps/s | Min gap | Main tap sources |
|---|---|---|---|---|---|---|---|
| Intro | intro | 0.00 | 10.93 | 5 | 0.46 | 0.992 | bass 3, kick 1, vocal 1 |
| Verse 1 | verse | 10.93 | 32.26 | 15 | 0.70 | 0.348 | vocal 15 |
| Pre-chorus 1 | pre | 32.26 | 42.93 | 9 | 0.84 | 0.661 | vocal 8, kick 1 |
| Chorus 1 | chorus | 42.93 | 64.26 | 21 | 0.98 | 0.322 | vocal 17, snare 4 |
| Verse 2 | verse | 64.26 | 80.26 | 14 | 0.88 | 0.321 | vocal 9, kick 4, snare 1 |
| Breath | break | 80.26 | 85.59 | 2 | 0.37 | 1.000 | vocal 1, snare 1 |
| Pre-chorus 2 | pre | 85.59 | 96.26 | 9 | 0.84 | 0.333 | vocal 8, snare 1 |
| Chorus 2 | chorus | 96.26 | 117.59 | 22 | 1.03 | 0.341 | vocal 17, snare 4, kick 1 |
| Bridge | bridge | 117.59 | 128.26 | 9 | 0.84 | 0.666 | vocal 9 |
| Final chorus | chorus | 128.26 | 143.59 | 18 | 1.17 | 0.316 | vocal 12, snare 4, kick 2 |
| Outro | outro | 143.59 | 175.01 | 20 | 0.64 | 0.316 | vocal 16, bass 2, snare 1 |

## How taps were chosen (rationale)


Hurt 90 BPM (beat 0.667 s, downbeat 0.260 s). 144 taps (old 64, 2.25x; still only 0.82 taps/s - the calmest level). Mostly vocal-phrase taps (demucs vocal stem, -25 ms corrected) with snare backbeat anchors; final chorus allows short 16th-note vocal pairs. Min gap 0.316 s. Recommended judgment window +-100 ms.

Method (honest description): candidates = every 8th (or 16th where the groove is syncopated) on the measured beat grid. Each candidate is scored by the onset strength of the separated stems at that instant (vocal syllable onsets from the htdemucs vocal stem, kick 30–140 Hz / snare-clap 1.2–8 kHz from the percussive part of the accompaniment stem, bass and harmonic accents), with per-section weights and a metric bonus for strong beats. **Per section I set by hand**: the density target (follows energy: intro < verse < pre < chorus/climax), which sources lead (vocal phrasing in verses/pre-choruses, drums+hook in choruses), the grid resolution, the minimum gap and the maximum run length, plus forced taps on section downbeats/impacts. The selected slot is then snapped to the actual onset peak if within ±18 ms, otherwise kept on the grid. Repeated musical material therefore gets repeated tap patterns (DL-style), and long gaps stay where the music breathes. All demucs-derived times are corrected by −25.03 ms (stem latency vs ffmpeg/browser decode).

## Alignment spot checks (start / section changes / middle / end)

Offset = (audio event time − tap time). 'Nearest onset' = nearest peak of the full-mix onset-strength envelope (height>0.12, ≥46 ms apart); 'band peak' = peak of the tagged source envelope within ±60 ms; 'grid' = distance to nearest 16th of the beat grid.

| Where | Tap t (s) | Tag | Nearest full-mix onset (ms) | Tagged-band peak (ms) | Grid dev (ms) |
|---|---|---|---|---|---|
| start | 1.927 | bass | +0 | -23 | +0 |
| start | 4.593 | bass | +5 | -53 | -0 |
| start | 7.260 | bass | +8 | -27 | -0 |
| → Verse 1 | 11.262 | vocal | +23 | -0 | +2 |
| → Pre-chorus 1 | 32.260 | kick | +4 | -19 | -0 |
| → Chorus 1 | 43.259 | vocal | +11 | -0 | -1 |
| → Verse 2 | 64.260 | kick | +1 | -34 | -0 |
| → Breath | 79.594 | vocal | +4 | +27 | +0 |
| → Pre-chorus 2 | 84.927 | snare | -0 | -35 | -0 |
| → Chorus 2 | 96.270 | vocal | -0 | -0 | +10 |
| → Bridge | 117.934 | vocal | +23 | +0 | +7 |
| → Final chorus | 128.261 | kick | +6 | -29 | +0 |
| → Outro | 143.594 | snare | -2 | -37 | -0 |
| middle | 90.604 | vocal | +0 | +0 | +10 |
| middle | 91.928 | vocal | +35 | -0 | +1 |
| middle | 92.927 | vocal | -12 | +22 | -0 |
| end | 166.580 | vocal | -12 | -0 | -14 |
| end | 167.602 | vocal | -0 | -0 | +8 |
| end | 168.263 | vocal | -46 | +0 | +2 |

Whole chart: |offset to nearest full-mix onset| median 10 ms, 90th pct 23 ms; |offset to tagged-band peak| median 18 ms, 90th pct 35 ms.

Per-section median |offset to tagged-band peak| (ms): Intro 23, Verse 1 0, Pre-chorus 1 19, Chorus 1 0, Verse 2 0, Breath 28, Pre-chorus 2 0, Chorus 2 10, Bridge 21, Final chorus 20, Outro 11

Caveats: alignment is measured against analysis envelopes, not by listening on a device; the integrator must verify in-engine with the audio clock (output latency handled by the engine). Section boundaries come from bass/drum/vocal energy changes and 4-bar novelty and are approximate labels where noted.