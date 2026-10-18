# Cool With You: audio analysis notes

- File: `public/audio/cool-with-you.mp3`, 147.88 s, used whole (never trimmed). Times are seconds from the first decoded sample.
- Grid: 134.995 BPM, 16th = 0.111115 s, phase 0.0011 s (bar 0 downbeat = 0.3344 s, bar = 1.77784 s). Fit quality (phase resultant) 0.637; drift per 20 s window: -1.2, +0.3, +4.9, +0.0, -3.2, -0.1, +4.0 ms.
- Calibration: librosa onset frames were -21.0 ms off the time-domain attacks (max slope of a 2 ms RMS envelope), so the grid is anchored to attacks; band layers were shifted by onsets +19.6 ms, kick -23.2 ms, snare -27.0 ms, hat -26.3 ms, bass -12.3 ms, vocal +37.2 ms.
- No demucs stems were used (so the 25 ms htdemucs latency does not apply).
- Groove: 135 BPM UK-garage two-step at half-time feel: kick on 1 and the "and" of 3 (16th 10), rim/snare on 2/4, swung hats; long airy vocal lines. A stripped hook (bars 24-32) and a near-silent break (48-52) before the build.
- Sections: from beat-synchronous chroma/MFCC/RMS novelty, snapped to bar lines and checked against the arrangement (see analysis.json `sections`).
- Verification: every tap is on the grid and was kept only when a real event lies within ±35 ms; measured attack offset median -7.1 ms (MAD 13.1 ms), see chart-report.md and chart-sync.csv.
