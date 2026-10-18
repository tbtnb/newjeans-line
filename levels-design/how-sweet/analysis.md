# how-sweet — audio analysis notes (worker 4)

- Audio: full mp3 as shipped, 219.03 s, not trimmed or edited.
- Tempo **125.00 BPM** constant (beat 479.99 ms, bar 1.9200 s); first downbeat (bar 0) at **0.339 s**.
- Grid: constant-tempo grid = robust linear fit of a DP beat tracker on the full-mix onset envelope, then shifted to the measured max-slope of clap/hat transients in the mix (librosa onset envelopes are ~25 ms late)
- Transient correction applied to the grid: -23 ms.
- Demucs (htdemucs) stems are **25.03 ms late** against the mix (delay measured for htdemucs by the project lead and confirmed on our drum stems); all stem onsets stored here are already shifted earlier by 25 ms + ~25 ms envelope lag (−50 ms total), so stem-based tap choices sit on the real attack.

## Sections (labels inferred, not from official metadata)

| # | label | kind | start s | bars | vocal | drums | bass | other | evidence |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Intro | intro | 0.339 | 0–4 | 0.01 | 0.36 | 0.00 | 0.01 | novelty/agglom boundary within 0.01 s |
| 1 | Verse 1 | verse | 8.019 | 4–20 | 0.48 | 0.35 | 0.47 | 0.43 | novelty/agglom boundary within 0.03 s |
| 2 | Pre-chorus 1 | pre | 38.738 | 20–24 | 0.45 | 0.27 | 0.01 | 0.06 | novelty/agglom boundary within 0.48 s |
| 3 | Chorus 1 | chorus | 46.418 | 24–40 | 0.49 | 0.39 | 0.42 | 0.43 | novelty/agglom boundary within 0.02 s |
| 4 | Verse 2 | verse | 77.138 | 40–56 | 0.53 | 0.34 | 0.47 | 0.41 | set from stem levels / phrase count |
| 5 | Chorus 2 | chorus | 107.857 | 56–72 | 0.55 | 0.39 | 0.41 | 0.44 | novelty/agglom boundary within 0.91 s |
| 6 | Bridge | bridge | 138.576 | 72–80 | 0.26 | 0.14 | 0.15 | 0.45 | novelty/agglom boundary within 0.98 s |
| 7 | Build | pre | 153.936 | 80–88 | 0.32 | 0.30 | 0.47 | 0.47 | novelty/agglom boundary within 0.46 s |
| 8 | Final chorus | chorus | 169.295 | 88–104 | 0.50 | 0.39 | 0.41 | 0.52 | set from stem levels / phrase count |
| 9 | Outro | outro | 200.015 | 104–112 | 0.34 | 0.05 | 0.01 | 0.71 | novelty/agglom boundary within 0.51 s |

(Stem columns = mean per-bar level 0–1 over the section; they back the labels: e.g. drums≈0 + vocals → break/bridge, all high → chorus.)

## Method

librosa 1.0.0; HPSS(margin 1,2); band onset envs on percussive (kick 30-150Hz, snare/clap 1.5-6k, hat 6-11k) and harmonic (bass 30-200, vocal-band 300-3k proxy); beat_track tightness 400 with tempo hint; checkerboard novelty (L=16 beats) + agglomerative(14) for section candidates | demucs htdemucs stems (drums/bass/vocals/other) -> band onset envelopes; stem onset times corrected by -50 ms (25 ms demucs output delay + ~25 ms onset-envelope lag). Candidates only; the chart is curated in chart.json.

The machine-readable data is in `analysis.json` (beats, sections, candidates, per-bar stem levels, mix and stem onset candidates with strengths, 1 s RMS).
