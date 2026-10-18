# ASAP: audio analysis notes

- File: `public/audio/asap.mp3`, 134.39 s, used whole (never trimmed). Times are seconds from the first decoded sample.
- Grid: 130.012 BPM, 16th = 0.115374 s, phase -0.0049 s (bar 0 downbeat = 0.3412 s, bar = 1.84598 s). Fit quality (phase resultant) 0.789; drift per 20 s window: +1.3, +11.0, -1.8, -2.6, -0.6, +4.5 ms.
- Calibration: librosa onset frames were -17.3 ms off the time-domain attacks (max slope of a 2 ms RMS envelope), so the grid is anchored to attacks; band layers were shifted by onsets +15.7 ms, kick -13.3 ms, snare -28.3 ms, hat -29.7 ms, bass -4.6 ms, vocal +23.1 ms.
- No demucs stems were used (so the 25 ms htdemucs latency does not apply).
- Groove: 130 BPM soft house/R&B: muted kick on 1 and 3, finger snaps / rim on 2 and 4, gentle synth chords; vocal phrases breathe with 1-2 bar gaps. One silent "held breath" bar (30), a dance break with denser percussion (39-47), a hush (62-65) before the final hook.
- Sections: from beat-synchronous chroma/MFCC/RMS novelty, snapped to bar lines and checked against the arrangement (see analysis.json `sections`).
- Verification: every tap is on the grid and was kept only when a real event lies within ±35 ms; measured attack offset median -0.8 ms (MAD 1.5 ms), see chart-report.md and chart-sync.csv.
