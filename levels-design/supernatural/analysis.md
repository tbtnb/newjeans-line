# supernatural — audio analysis notes (worker 4)

- Audio: full mp3 as shipped, 191.00 s, not trimmed or edited.
- Tempo **109.00 BPM** constant (beat 550.46 ms, bar 2.2018 s); first downbeat (bar 0) at **0.332 s**.
- Grid: constant-tempo grid = robust linear fit of a DP beat tracker on the full-mix onset envelope, then shifted to the measured max-slope of clap/hat transients in the mix (librosa onset envelopes are ~25 ms late)
- Transient correction applied to the grid: -26 ms.
- Demucs (htdemucs) stems are **25.03 ms late** against the mix (delay measured for htdemucs by the project lead and confirmed on our drum stems); all stem onsets stored here are already shifted earlier by 25 ms + ~25 ms envelope lag (−50 ms total), so stem-based tap choices sit on the real attack.

## Sections (labels inferred, not from official metadata)

| # | label | kind | start s | bars | vocal | drums | bass | other | evidence |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Intro | intro | 0.332 | 0–4 | 0.10 | 0.16 | 0.00 | 0.03 | novelty/agglom boundary within 0.02 s |
| 1 | Groove | verse | 9.139 | 4–12 | 0.02 | 0.43 | 0.52 | 0.64 | novelty/agglom boundary within 0.54 s |
| 2 | Verse 1 | verse | 26.754 | 12–20 | 0.38 | 0.38 | 0.44 | 0.52 | novelty/agglom boundary within 0.58 s |
| 3 | Pre-chorus 1 | pre | 44.369 | 20–28 | 0.39 | 0.39 | 0.48 | 0.54 | novelty/agglom boundary within 0.57 s |
| 4 | Chorus 1 | chorus | 61.983 | 28–36 | 0.48 | 0.38 | 0.50 | 0.59 | novelty/agglom boundary within 0.04 s |
| 5 | Verse 2 | verse | 79.598 | 36–44 | 0.42 | 0.39 | 0.42 | 0.52 | novelty/agglom boundary within 0.58 s |
| 6 | Bridge | bridge | 97.213 | 44–52 | 0.43 | 0.21 | 0.50 | 0.57 | novelty/agglom boundary within 0.58 s |
| 7 | Chorus 2 | chorus | 114.828 | 52–60 | 0.46 | 0.39 | 0.40 | 0.68 | novelty/agglom boundary within 0.03 s |
| 8 | Interlude | break | 132.442 | 60–68 | 0.34 | 0.39 | 0.45 | 0.60 | set from stem levels / phrase count |
| 9 | Final chorus | chorus | 150.057 | 68–76 | 0.54 | 0.36 | 0.55 | 0.56 | set from stem levels / phrase count |
| 10 | Outro | outro | 167.672 | 76–84 | 0.25 | 0.09 | 0.39 | 0.52 | novelty/agglom boundary within 0.57 s |

(Stem columns = mean per-bar level 0–1 over the section; they back the labels: e.g. drums≈0 + vocals → break/bridge, all high → chorus.)

## Method

librosa 1.0.0; HPSS(margin 1,2); band onset envs on percussive (kick 30-150Hz, snare/clap 1.5-6k, hat 6-11k) and harmonic (bass 30-200, vocal-band 300-3k proxy); beat_track tightness 400 with tempo hint; checkerboard novelty (L=16 beats) + agglomerative(14) for section candidates | demucs htdemucs stems (drums/bass/vocals/other) -> band onset envelopes; stem onset times corrected by -50 ms (25 ms demucs output delay + ~25 ms onset-envelope lag). Candidates only; the chart is curated in chart.json.

The machine-readable data is in `analysis.json` (beats, sections, candidates, per-bar stem levels, mix and stem onset candidates with strengths, 1 s RMS).
