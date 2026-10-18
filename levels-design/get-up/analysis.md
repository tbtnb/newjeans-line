# Get Up: audio analysis notes

- File: `public/audio/get-up.mp3`, 36.23 s, used whole (never trimmed). Times are seconds from the first decoded sample.
- Grid: 120.022 BPM, 16th = 0.124977 s, phase 0.0854 s (bar 0 downbeat = 0.3354 s, bar = 1.99963 s). Fit quality (phase resultant) 0.329; drift per 20 s window: -0.7 ms.
- Calibration: librosa onset frames were -19.0 ms off the time-domain attacks (max slope of a 2 ms RMS envelope), so the grid is anchored to attacks; band layers were shifted by onsets +19.8 ms, kick -28.7 ms, snare -25.5 ms, hat -18.0 ms, bass -43.7 ms, vocal +33.9 ms.
- No demucs stems were used (so the 25 ms htdemucs latency does not apply).
- Groove: 120 BPM ambient interlude, 36 s: no drum kit, a soft pulse on the half-bar, stacked vocal harmonies swelling in two-bar phrases; grid confidence is low (resultant 0.33), so only clearly audible swells are used.
- Sections: from beat-synchronous chroma/MFCC/RMS novelty, snapped to bar lines and checked against the arrangement (see analysis.json `sections`).
- Verification: every tap is on the grid and was kept only when a real event lies within ±35 ms; measured attack offset median +4.6 ms (MAD 7.5 ms), see chart-report.md and chart-sync.csv.
