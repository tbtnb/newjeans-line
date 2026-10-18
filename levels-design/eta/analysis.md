# ETA: audio analysis notes

- File: `public/audio/eta.mp3`, 151.37 s, used whole (never trimmed). Times are seconds from the first decoded sample.
- Grid: 134.998 BPM, 16th = 0.111113 s, phase 0.0032 s (bar 0 downbeat = 1.6699 s, bar = 1.77780 s). Fit quality (phase resultant) 0.87; drift per 20 s window: +2.0, -0.9, -0.1, +0.1, -2.8, -0.3, +0.5 ms.
- Calibration: librosa onset frames were -29.3 ms off the time-domain attacks (max slope of a 2 ms RMS envelope), so the grid is anchored to attacks; band layers were shifted by onsets +27.1 ms, kick -23.5 ms, snare -17.4 ms, hat -16.2 ms, bass +49.2 ms, vocal -4.8 ms.
- No demucs stems were used (so the 25 ms htdemucs latency does not apply).
- Groove: 135 BPM four-on-the-floor Jersey-club/pop: kick on every beat, snare/clap on 2 and 4, constant 16th hats, syncopated vocal hook landing on the "e" and "a" 16ths. Two a-cappella "E-T-A" voice-chop stops (bars 26 and 58) cut the drums for one bar.
- Sections: from beat-synchronous chroma/MFCC/RMS novelty, snapped to bar lines and checked against the arrangement (see analysis.json `sections`).
- Verification: every tap is on the grid and was kept only when a real event lies within ±35 ms; measured attack offset median -1.9 ms (MAD 10.0 ms), see chart-report.md and chart-sync.csv.
