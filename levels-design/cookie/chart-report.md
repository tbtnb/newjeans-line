# Cookie — chart report

- Audio: `public/audio/cookie.mp3` (full track, 233.40 s, untouched). Times = seconds from first decoded sample.
- Tempo grid measured from the audio: **157.00 BPM**, beat 0.3822 s, downbeat phase 0.104 s (constant-tempo fit maximising onset strength).
- **Old taps: 357** (shipped `src/levels.json`; `reports/rhythm-chart-baseline.json` had 379). **New taps: 478** = **1.34x**.
- Speed 10.0 u/s, road width 2.4 → narrowest 2.0.
- Min gap **0.173 s**, median gap 0.382 s, mean density 2.05 taps/s.
- Fastest consecutive run (8th notes, every gap ≤ 0.210 s): **6 taps**, 135.774–136.730 s (mean interval 0.191 s).
- Validator definition (gaps ≤ 0.30 s): longest run 6 taps from 135.774 s.
- Fastest 8th-note burst at 157 BPM (gaps ≤ 0.20 s): **6 taps** from 135.774 s (interval ≈ 0.191 s).
- Longest unbroken run at ≤ 1 beat spacing (≤ 0.420 s): 9 taps from 114.946 s.
- Peak 2-second density: **4.5 taps/s** at 123.50 s.
- Recommended judgment window: **±80 ms** (perfect ±35 ms). Must stay < half the min gap (87 ms) so a tap never resolves to the neighbouring turn; ±80 ms ≈ the old engine's ±100 ms but tighter for the dense songs. Needs confirmation with real touch latency (not yet tested on devices).
- Hard floor respected: no gap < 0.15 s. Humanly-playable minimum used here: 0.173 s.

## Per-section density

| Section | Kind | Start | End | Taps | Taps/s | Min gap | Main tap sources |
|---|---|---|---|---|---|---|---|
| Intro | intro | 0.00 | 12.33 | 9 | 0.73 | 0.743 | kick 7, bass 2 |
| Verse 1 | verse | 12.33 | 36.79 | 46 | 1.88 | 0.175 | kick 23, snare 14, vocal 9 |
| Pre-chorus 1 | pre | 36.79 | 49.02 | 22 | 1.80 | 0.191 | vocal 21, kick 1 |
| Chorus 1 | chorus | 49.02 | 73.48 | 64 | 2.62 | 0.178 | kick 41, vocal 18, snare 5 |
| Verse 2 | verse | 73.48 | 97.94 | 44 | 1.80 | 0.185 | kick 24, vocal 10, snare 10 |
| Pre-chorus 2 | pre | 97.94 | 110.17 | 22 | 1.80 | 0.191 | vocal 20, kick 2 |
| Chorus 2 | chorus | 110.17 | 134.63 | 64 | 2.62 | 0.173 | kick 38, vocal 19, snare 7 |
| Jersey-club bridge | bridge | 134.63 | 159.09 | 76 | 3.11 | 0.174 | snare 48, kick 15, vocal 9 |
| Final chorus | chorus | 159.09 | 183.55 | 64 | 2.62 | 0.174 | kick 40, vocal 20, snare 4 |
| Dance break | break | 183.55 | 208.01 | 34 | 1.39 | 0.373 | kick 28, snare 4, vocal 2 |
| Outro | outro | 208.01 | 233.40 | 33 | 1.30 | 0.175 | vocal 29, kick 4 |

## How taps were chosen (rationale)


Cookie 157 BPM grid (half-time feel 78.5; beat 0.382 s, downbeat 0.104 s). 478 taps (old 357, 1.34x as schema asks ~1.2-1.4x). Taps on 8th grid (0.191 s) only where kick/snare/vocal really double; runs capped at 6 (chorus) / 10 (Jersey-club bridge, which follows the 3-3-2 club kick-snare syncopation) taps. Min gap 0.173 s. Recommended judgment window +-80 ms.

Method (honest description): candidates = every 8th (or 16th where the groove is syncopated) on the measured beat grid. Each candidate is scored by the onset strength of the separated stems at that instant (vocal syllable onsets from the htdemucs vocal stem, kick 30–140 Hz / snare-clap 1.2–8 kHz from the percussive part of the accompaniment stem, bass and harmonic accents), with per-section weights and a metric bonus for strong beats. **Per section I set by hand**: the density target (follows energy: intro < verse < pre < chorus/climax), which sources lead (vocal phrasing in verses/pre-choruses, drums+hook in choruses), the grid resolution, the minimum gap and the maximum run length, plus forced taps on section downbeats/impacts. The selected slot is then snapped to the actual onset peak if within ±18 ms, otherwise kept on the grid. Repeated musical material therefore gets repeated tap patterns (DL-style), and long gaps stay where the music breathes. All demucs-derived times are corrected by −25.03 ms (stem latency vs ffmpeg/browser decode).

## Alignment spot checks (start / section changes / middle / end)

Offset = (audio event time − tap time). 'Nearest onset' = nearest peak of the full-mix onset-strength envelope (height>0.12, ≥46 ms apart); 'band peak' = peak of the tagged source envelope within ±60 ms; 'grid' = distance to nearest 16th of the beat grid.

| Where | Tap t (s) | Tag | Nearest full-mix onset (ms) | Tagged-band peak (ms) | Grid dev (ms) |
|---|---|---|---|---|---|
| start | 1.254 | kick | -0 | -0 | +3 |
| start | 2.020 | kick | +0 | +0 | +5 |
| start | 3.170 | kick | -0 | -0 | +9 |
| → Verse 1 | 12.333 | snare | -3 | -26 | -0 |
| → Pre-chorus 1 | 36.792 | vocal | +0 | -23 | -0 |
| → Chorus 1 | 49.022 | kick | -28 | -40 | +0 |
| → Verse 2 | 73.480 | vocal | -0 | -0 | -1 |
| → Pre-chorus 2 | 98.325 | vocal | -0 | -0 | +3 |
| → Chorus 2 | 109.772 | vocal | +12 | +0 | -15 |
| → Jersey-club bridge | 135.201 | snare | -3 | -26 | -0 |
| → Final chorus | 159.463 | vocal | +12 | +0 | -6 |
| → Dance break | 183.163 | kick | -4 | -27 | -0 |
| → Outro | 208.213 | vocal | -11 | +0 | +17 |
| middle | 121.243 | vocal | +35 | -0 | -9 |
| middle | 121.634 | kick | -8 | -31 | -0 |
| middle | 121.823 | vocal | +12 | +0 | -2 |
| end | 225.584 | vocal | -2 | -25 | -0 |
| end | 226.349 | vocal | +34 | +34 | +0 |
| end | 228.659 | vocal | -0 | -0 | +17 |

Whole chart: |offset to nearest full-mix onset| median 5 ms, 90th pct 13 ms; |offset to tagged-band peak| median 28 ms, 90th pct 42 ms.

Per-section median |offset to tagged-band peak| (ms): Intro 0, Verse 1 26, Pre-chorus 1 21, Chorus 1 29, Verse 2 30, Pre-chorus 2 26, Chorus 2 29, Jersey-club bridge 30, Final chorus 28, Dance break 30, Outro 0

Caveats: alignment is measured against analysis envelopes, not by listening on a device; the integrator must verify in-engine with the audio clock (output latency handled by the engine). Section boundaries come from bass/drum/vocal energy changes and 4-bar novelty and are approximate labels where noted.