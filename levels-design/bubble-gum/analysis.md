# bubble-gum — audio analysis notes (worker 4)

- Audio: full mp3 as shipped, 200.27 s, not trimmed or edited.
- Tempo **105.01 BPM** constant (beat 571.39 ms, bar 2.2856 s); first downbeat (bar 0) at **2.055 s**.
- Grid: constant-tempo grid = robust linear fit of a DP beat tracker on the full-mix onset envelope, then shifted to the measured max-slope of clap/hat transients in the mix (librosa onset envelopes are ~25 ms late)
- Transient correction applied to the grid: -24 ms.
- Demucs (htdemucs) stems are **25.03 ms late** against the mix (delay measured for htdemucs by the project lead and confirmed on our drum stems); all stem onsets stored here are already shifted earlier by 25 ms + ~25 ms envelope lag (−50 ms total), so stem-based tap choices sit on the real attack.

## Sections (labels inferred, not from official metadata)

| # | label | kind | start s | bars | vocal | drums | bass | other | evidence |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Intro | intro | 2.055 | 0–7 | 0.00 | 0.00 | 0.37 | 0.38 | novelty/agglom boundary within 1.12 s |
| 1 | Verse 1 | verse | 18.054 | 7–15 | 0.39 | 0.23 | 0.36 | 0.34 | novelty/agglom boundary within 0.59 s |
| 2 | Pre-chorus 1 | pre | 36.339 | 15–24 | 0.46 | 0.21 | 0.42 | 0.43 | novelty/agglom boundary within 1.16 s |
| 3 | Chorus 1 | chorus | 56.909 | 24–34 | 0.46 | 0.26 | 0.46 | 0.43 | set from stem levels / phrase count |
| 4 | Breakdown | break | 79.764 | 34–39 | 0.41 | 0.07 | 0.03 | 0.27 | novelty/agglom boundary within 1.17 s |
| 5 | Verse 2 | verse | 91.192 | 39–51 | 0.36 | 0.21 | 0.45 | 0.33 | novelty/agglom boundary within 1.18 s |
| 6 | Pre-chorus 2 | pre | 118.619 | 51–59 | 0.43 | 0.22 | 0.40 | 0.48 | novelty/agglom boundary within 1.17 s |
| 7 | Chorus 2 | chorus | 136.903 | 59–71 | 0.55 | 0.22 | 0.43 | 0.50 | novelty/agglom boundary within 0.03 s |
| 8 | Final chorus | chorus | 164.330 | 71–83 | 0.44 | 0.28 | 0.55 | 0.47 | set from stem levels / phrase count |
| 9 | Outro | outro | 191.757 | 83–84 | 0.24 | 0.15 | 0.00 | 0.20 | novelty/agglom boundary within 0.02 s |

(Stem columns = mean per-bar level 0–1 over the section; they back the labels: e.g. drums≈0 + vocals → break/bridge, all high → chorus.)

## Method

librosa 1.0.0; HPSS(margin 1,2); band onset envs on percussive (kick 30-150Hz, snare/clap 1.5-6k, hat 6-11k) and harmonic (bass 30-200, vocal-band 300-3k proxy); beat_track tightness 400 with tempo hint; checkerboard novelty (L=16 beats) + agglomerative(14) for section candidates | demucs htdemucs stems (drums/bass/vocals/other) -> band onset envelopes; stem onset times corrected by -50 ms (25 ms demucs output delay + ~25 ms onset-envelope lag). Candidates only; the chart is curated in chart.json.

The machine-readable data is in `analysis.json` (beats, sections, candidates, per-bar stem levels, mix and stem onset candidates with strengths, 1 s RMS).
