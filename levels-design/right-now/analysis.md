# right-now — audio analysis notes (worker 4)

- Audio: full mp3 as shipped, 160.41 s, not trimmed or edited.
- Tempo **172.00 BPM** constant (beat 348.84 ms, bar 1.3954 s); first downbeat (bar 0) at **0.335 s**.
- Grid: constant-tempo grid = robust linear fit of a DP beat tracker on the full-mix onset envelope, then shifted to the measured max-slope of clap/hat transients in the mix (librosa onset envelopes are ~25 ms late)
- Transient correction applied to the grid: -31 ms.
- Demucs (htdemucs) stems are **25.03 ms late** against the mix (delay measured for htdemucs by the project lead and confirmed on our drum stems); all stem onsets stored here are already shifted earlier by 25 ms + ~25 ms envelope lag (−50 ms total), so stem-based tap choices sit on the real attack.

## Sections (labels inferred, not from official metadata)

| # | label | kind | start s | bars | vocal | drums | bass | other | evidence |
|---|---|---|---|---|---|---|---|---|---|
| 0 | Intro | intro | 0.335 | 0–8 | 0.11 | 0.04 | 0.60 | 0.46 | novelty/agglom boundary within 0.02 s |
| 1 | Verse 1 | verse | 11.497 | 8–24 | 0.57 | 0.43 | 0.66 | 0.37 | novelty/agglom boundary within 0.38 s |
| 2 | Pre-chorus 1 | pre | 33.823 | 24–32 | 0.49 | 0.43 | 0.66 | 0.35 | novelty/agglom boundary within 0.38 s |
| 3 | Chorus 1 | chorus | 44.986 | 32–48 | 0.57 | 0.40 | 0.67 | 0.38 | set from stem levels / phrase count |
| 4 | Verse 2 | verse | 67.312 | 48–56 | 0.58 | 0.43 | 0.66 | 0.36 | set from stem levels / phrase count |
| 5 | Half-time bridge | bridge | 78.475 | 56–72 | 0.45 | 0.25 | 0.49 | 0.55 | novelty/agglom boundary within 0.03 s |
| 6 | Chorus 2 | chorus | 100.800 | 72–84 | 0.48 | 0.43 | 0.67 | 0.33 | novelty/agglom boundary within 0.33 s |
| 7 | Break | break | 117.545 | 84–88 | 0.53 | 0.14 | 0.70 | 0.45 | novelty/agglom boundary within 0.04 s |
| 8 | Final chorus | chorus | 123.126 | 88–104 | 0.52 | 0.43 | 0.65 | 0.45 | novelty/agglom boundary within 0.66 s |
| 9 | Outro | outro | 145.452 | 104–112 | 0.01 | 0.03 | 0.55 | 0.35 | novelty/agglom boundary within 0.03 s |

(Stem columns = mean per-bar level 0–1 over the section; they back the labels: e.g. drums≈0 + vocals → break/bridge, all high → chorus.)

## Method

librosa 1.0.0; HPSS(margin 1,2); band onset envs on percussive (kick 30-150Hz, snare/clap 1.5-6k, hat 6-11k) and harmonic (bass 30-200, vocal-band 300-3k proxy); beat_track tightness 400 with tempo hint; checkerboard novelty (L=16 beats) + agglomerative(14) for section candidates | demucs htdemucs stems (drums/bass/vocals/other) -> band onset envelopes; stem onset times corrected by -50 ms (25 ms demucs output delay + ~25 ms onset-envelope lag). Candidates only; the chart is curated in chart.json.

The machine-readable data is in `analysis.json` (beats, sections, candidates, per-bar stem levels, mix and stem onset candidates with strengths, 1 s RMS).
