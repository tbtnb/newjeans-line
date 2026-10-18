# Cookie - chart report (designs-w1, v3, rhythm-logic audit)

- Audio: `public/audio/cookie.mp3`, full track 233.40 s, untouched. Tempo grid measured from audio: **157.00 BPM**, beat 0.3822 s, downbeat phase 0.104 s. htdemucs stem envelopes shifted -25.03 ms before use.
- **Taps: legacy 357 -> previous designs-w1 chart 478 -> now 500** (1.40x legacy). Difficulty tier: hard (title track).
- Audit vs the override rules: 6 off-layer / faint taps removed, 8 one-off taps dropped and 36 taps added so repeated phrases share one pattern (each added slot had clear evidence in every repeat). 16th bursts: 0 inserted tap(s) at none.
- Gaps: min **0.173 s**, median 0.382 s (floor 0.105 s).
- Fastest run (validator definition, gaps <= 0.30 s): **6 taps**, 135.77-136.73 s.
- Judgment window (engine rule min(0.5g, clamp(0.45g, 45, 110 ms)), g = local min gap): **min ±78 ms, median ±86 ms** - always <= half the local gap.

## Difficulty vs original Dancing Line

| Level | Taps / length | avg CPM (total taps / duration) | avg CPM (wiki-style) | peak CPM |
|---|---|---|---|---|
| **Cookie (this chart)** | 500 / 3:53 | **129** | **157** (60/median gap; mean of 60/gap = 190) | **347** (60/min gap); 360 as taps-in-1 s x60 |
| The Racing (hardest) | 357 / 2:24 | 149 | 220 | 440 |
| The Chaos | - | - | 136 | 408 |
| Chinese Garden | - | - | 148 | 296 |
| Winter | - | - | 140 | 280 |
| Piano | - | - | 125 | 250 |
| Autumn | - | - | 96 | - |

Wiki-style avg CPM is approximated as 60 / median tap gap (the wiki does not publish its formula; for The Racing total/duration gives 149 while the wiki says 220, so it is clearly a playing-tempo measure rather than taps per minute of audio). Peak CPM = 60 / shortest gap, which reproduces the wiki numbers (Racing 16ths at 110 BPM = 0.136 s = 440).

Honest peak 347 CPM is below the 400-460 "title track" reference. That is deliberate (user override: rhythmic logic beats density): the song's 16th grid (0.096 s at 157 BPM) is below the 0.105 s gap floor, so no 16th bursts are possible; the hardest figures are the 8th-note club-kick runs.

## Per-section density and what the taps follow

| Section | Start | End | Taps (before audit -> now) | Taps/s | Min gap | Layer | What the taps follow |
|---|---|---|---|---|---|---|---|
| Intro | 0.00 | 12.33 | 9 -> 9 | 0.73 | 0.743 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Verse 1 | 12.33 | 36.79 | 46 -> 55 | 2.25 | 0.175 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Pre-chorus 1 | 36.79 | 49.02 | 22 -> 22 | 1.80 | 0.191 | vocal | vocal syllables of the rising/falling phrase |
| Chorus 1 | 49.02 | 73.48 | 64 -> 67 | 2.74 | 0.178 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Verse 2 | 73.48 | 97.94 | 44 -> 53 | 2.17 | 0.185 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Pre-chorus 2 | 97.94 | 110.17 | 22 -> 21 | 1.72 | 0.191 | vocal | vocal syllables of the rising/falling phrase |
| Chorus 2 | 110.17 | 134.63 | 64 -> 65 | 2.66 | 0.173 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Jersey-club bridge | 134.63 | 159.09 | 76 -> 76 | 3.11 | 0.174 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Final chorus | 159.09 | 183.55 | 64 -> 68 | 2.78 | 0.174 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Dance break | 183.55 | 208.01 | 34 -> 34 | 1.39 | 0.373 | drums | half-time kick/snare groove (8th doubles only where the kick really doubles) |
| Outro | 208.01 | 233.40 | 33 -> 30 | 1.18 | 0.175 | vocal | vocal syllables of the rising/falling phrase |

## Rules applied (user override, 11:55)

1. One layer per section (table above). Taps whose own-layer envelope was weak at the tap (another layer drove it) were removed, even when the full mix was loud there.
2. Repeated sections (Verse 1 / Verse 2; Pre-chorus 1 / Pre-chorus 2; Chorus 1 / Chorus 2 / Final chorus) were aligned bar-by-bar on the 16th-slot grid: a slot is kept/added if most repeats have it and every repeat shows evidence; one-off slots were dropped unless very strong.
3. 16th bursts only where the onset of the FULL MIX (not a stem) is in the top percentile at the 16th off-position, with both neighbours on 8th positions and at least one on a beat - so a burst starts and ends on strong grid points (3-tap figures).
4. Held notes, breaks and outros keep their long gaps; no fills were added to reach CPM targets.
5. Faint onsets (layer < 0.22 or mix < 0.10 at the tap) removed unless they anchor a section start.

## Route (summary)

Route textures per section are listed in design.md; moves: intro-sweep (alt), verse1-bench-switchbacks (lserp), pre1-stair-spiral (lspiral), chorus1-cd-horseshoe (zig), verse2-narrow-zigzag (zig), pre2-climb-spiral (lspiral), chorus2-terrace-loop (zig), bridge-jersey-zigzag (zig), final-wide-L (zig), dancebreak-sawtooth (zig), dancebreak-switch (lserp), outro-descent (alt).

Not tested in the engine on a device; touch latency still needs confirming.
