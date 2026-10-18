# Attention — chart report

- Audio: `public/audio/attention.mp3` (full track, 178.00 s, untouched). Times = seconds from first decoded sample.
- Tempo grid measured from the audio: **104.99 BPM**, beat 0.5715 s, downbeat phase 0.464 s (constant-tempo fit maximising onset strength).
- **Old taps: 139** (shipped `src/levels.json`; `reports/rhythm-chart-baseline.json` had 139). **New taps: 277** = **1.99x**.
- Speed 9.0 u/s, road width 2.2 → narrowest 1.9.
- Min gap **0.267 s**, median gap 0.303 s, mean density 1.56 taps/s.
- Fastest consecutive run (8th notes, every gap ≤ 0.314 s): **12 taps**, 129.904–133.047 s (mean interval 0.286 s).
- Validator definition (gaps ≤ 0.30 s): longest run 12 taps from 129.904 s.
- Longest unbroken run at ≤ 1 beat spacing (≤ 0.629 s): 20 taps from 148.477 s.
- Peak 2-second density: **4.0 taps/s** at 130.75 s.
- Recommended judgment window: **±90 ms** (perfect ±35 ms). Must stay < half the min gap (133 ms) so a tap never resolves to the neighbouring turn; ±90 ms ≈ the old engine's ±100 ms but tighter for the dense songs. Needs confirmation with real touch latency (not yet tested on devices).
- Hard floor respected: no gap < 0.15 s. Humanly-playable minimum used here: 0.267 s.

## Per-section density

| Section | Kind | Start | End | Taps | Taps/s | Min gap | Main tap sources |
|---|---|---|---|---|---|---|---|
| Intro | intro | 0.00 | 9.61 | 5 | 0.52 | 1.698 | vocal 5 |
| Hook A | chorus | 9.61 | 27.89 | 32 | 1.75 | 0.267 | vocal 15, snare 11, bass 4 |
| Verse 1 | verse | 27.89 | 46.75 | 24 | 1.27 | 0.278 | vocal 16, kick 5, snare 2 |
| Pre-chorus 1 | pre | 46.75 | 62.18 | 22 | 1.43 | 0.275 | vocal 20, kick 2 |
| Chorus 1 | chorus | 62.18 | 83.32 | 44 | 2.08 | 0.268 | snare 21, vocal 12, bass 7 |
| Verse 2 | verse | 83.32 | 101.60 | 20 | 1.09 | 0.277 | vocal 18, kick 1, snare 1 |
| Pre-chorus 2 | pre | 101.60 | 117.03 | 24 | 1.56 | 0.271 | vocal 22, kick 2 |
| Chorus 2 | chorus | 117.03 | 137.60 | 44 | 2.14 | 0.271 | snare 17, vocal 15, bass 7 |
| Final chorus | chorus | 137.60 | 156.10 | 43 | 2.32 | 0.274 | snare 18, vocal 13, kick 6 |
| Outro | outro | 156.10 | 178.00 | 19 | 0.87 | 0.267 | vocal 19 |

## How taps were chosen (rationale)


Attention 105 BPM (beat 0.5714 s, downbeat grid 0.464 s). 277 taps (old 139, 2.0x). Taps on measured audio accents: vocal syllables (demucs stem, -25 ms corrected) in verses/pre, kick/snare/bass in hook & choruses; dotted vocal pickups (beat 2.5 / 4.5) are the motif. Min gap 0.267 s (8ths). Fastest run 12 consecutive 8ths in Chorus 2. Recommended judgment window +-90 ms (perfect +-35 ms).

Method (honest description): candidates = every 8th (or 16th where the groove is syncopated) on the measured beat grid. Each candidate is scored by the onset strength of the separated stems at that instant (vocal syllable onsets from the htdemucs vocal stem, kick 30–140 Hz / snare-clap 1.2–8 kHz from the percussive part of the accompaniment stem, bass and harmonic accents), with per-section weights and a metric bonus for strong beats. **Per section I set by hand**: the density target (follows energy: intro < verse < pre < chorus/climax), which sources lead (vocal phrasing in verses/pre-choruses, drums+hook in choruses), the grid resolution, the minimum gap and the maximum run length, plus forced taps on section downbeats/impacts. The selected slot is then snapped to the actual onset peak if within ±18 ms, otherwise kept on the grid. Repeated musical material therefore gets repeated tap patterns (DL-style), and long gaps stay where the music breathes. All demucs-derived times are corrected by −25.03 ms (stem latency vs ffmpeg/browser decode).

## Alignment spot checks (start / section changes / middle / end)

Offset = (audio event time − tap time). 'Nearest onset' = nearest peak of the full-mix onset-strength envelope (height>0.12, ≥46 ms apart); 'band peak' = peak of the tagged source envelope within ±60 ms; 'grid' = distance to nearest 16th of the beat grid.

| Where | Tap t (s) | Tag | Nearest full-mix onset (ms) | Tagged-band peak (ms) | Grid dev (ms) |
|---|---|---|---|---|---|
| start | 1.335 | vocal | -11 | +0 | +14 |
| start | 3.622 | vocal | -11 | +0 | +15 |
| start | 5.909 | vocal | -11 | +0 | +16 |
| → Hook A | 9.608 | bass | +5 | -41 | +0 |
| → Verse 1 | 27.887 | vocal | +12 | +0 | -8 |
| → Pre-chorus 1 | 46.765 | vocal | -12 | -0 | +11 |
| → Chorus 1 | 62.184 | bass | +45 | -36 | +0 |
| → Verse 2 | 83.329 | vocal | -4 | +31 | +0 |
| → Pre-chorus 2 | 101.912 | vocal | -11 | +0 | +10 |
| → Chorus 2 | 117.046 | vocal | +17 | -64 | +0 |
| → Final chorus | 137.619 | snare | +6 | -41 | -0 |
| → Outro | 156.201 | vocal | -12 | -0 | +9 |
| middle | 91.044 | vocal | -10 | +25 | +0 |
| middle | 91.336 | vocal | -12 | -0 | +7 |
| middle | 92.472 | vocal | -10 | +25 | -0 |
| end | 170.469 | vocal | +0 | +0 | -10 |
| end | 171.607 | vocal | +23 | +0 | -15 |
| end | 172.768 | vocal | +0 | +0 | +3 |

Whole chart: |offset to nearest full-mix onset| median 5 ms, 90th pct 12 ms; |offset to tagged-band peak| median 26 ms, 90th pct 39 ms.

Per-section median |offset to tagged-band peak| (ms): Intro 0, Hook A 24, Verse 1 24, Pre-chorus 1 28, Chorus 1 31, Verse 2 10, Pre-chorus 2 0, Chorus 2 34, Final chorus 32, Outro 0

Caveats: alignment is measured against analysis envelopes, not by listening on a device; the integrator must verify in-engine with the audio clock (output latency handled by the engine). Section boundaries come from bass/drum/vocal energy changes and 4-bar novelty and are approximate labels where noted.