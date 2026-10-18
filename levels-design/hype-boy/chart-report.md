# Hype Boy - chart report (designs-w1, v3, rhythm-logic audit)

- Audio: `public/audio/hype-boy.mp3`, full track 176.59 s, untouched. Tempo grid measured from audio: **99.99 BPM**, beat 0.6000 s, downbeat phase 0.252 s. htdemucs stem envelopes shifted -25.03 ms before use.
- **Taps: legacy 140 -> previous designs-w1 chart 308 -> now 327** (2.34x legacy). Difficulty tier: hard (title track).
- Audit vs the override rules: 7 off-layer / faint taps removed, 6 one-off taps dropped and 48 taps added so repeated phrases share one pattern (each added slot had clear evidence in every repeat). 16th bursts: 2 inserted tap(s) at 35.805, 37.907.
- Gaps: min **0.148 s**, median 0.433 s (floor 0.105 s).
- Fastest run (validator definition, gaps <= 0.30 s): **4 taps**, 163.48-164.35 s.
- Judgment window (engine rule min(0.5g, clamp(0.45g, 45, 110 ms)), g = local min gap): **min ±67 ms, median ±110 ms** - always <= half the local gap.

## Difficulty vs original Dancing Line

| Level | Taps / length | avg CPM (total taps / duration) | avg CPM (wiki-style) | peak CPM |
|---|---|---|---|---|
| **Hype Boy (this chart)** | 327 / 2:56 | **111** | **139** (60/median gap; mean of 60/gap = 158) | **405** (60/min gap); 300 as taps-in-1 s x60 |
| The Racing (hardest) | 357 / 2:24 | 149 | 220 | 440 |
| The Chaos | - | - | 136 | 408 |
| Chinese Garden | - | - | 148 | 296 |
| Winter | - | - | 140 | 280 |
| Piano | - | - | 125 | 250 |
| Autumn | - | - | 96 | - |

Wiki-style avg CPM is approximated as 60 / median tap gap (the wiki does not publish its formula; for The Racing total/duration gives 149 while the wiki says 220, so it is clearly a playing-tempo measure rather than taps per minute of audio). Peak CPM = 60 / shortest gap, which reproduces the wiki numbers (Racing 16ths at 110 BPM = 0.136 s = 440).

## Per-section density and what the taps follow

| Section | Start | End | Taps (before audit -> now) | Taps/s | Min gap | Layer | What the taps follow |
|---|---|---|---|---|---|---|---|
| Intro riff | 0.00 | 19.45 | 17 -> 17 | 0.87 | 0.600 | synth | the lead synth riff notes (one per beat) |
| Verse 1 | 19.45 | 38.65 | 31 -> 42 | 2.19 | 0.148 | drums | moombahton kick/snare (3+3+2 dembow syncopation); 2 16th burst tap(s) on an audible fill, starting and ending on 8th/beat positions |
| Pre-chorus 1 | 38.65 | 48.25 | 12 -> 10 | 1.04 | 0.300 | vocal | vocal call-and-response phrase onsets |
| Build 1 | 48.25 | 53.05 | 9 -> 9 | 1.88 | 0.300 | drums | moombahton kick/snare (3+3+2 dembow syncopation) |
| Chorus 1 | 53.05 | 72.25 | 40 -> 43 | 2.24 | 0.267 | drums | moombahton kick/snare (3+3+2 dembow syncopation) |
| Post-chorus 1 | 72.25 | 91.45 | 37 -> 37 | 1.93 | 0.151 | drums | moombahton kick/snare (3+3+2 dembow syncopation) |
| Verse 2 | 91.45 | 115.45 | 41 -> 46 | 1.92 | 0.165 | drums | moombahton kick/snare (3+3+2 dembow syncopation) |
| Pre-chorus 2 | 115.45 | 125.05 | 11 -> 10 | 1.04 | 0.300 | vocal | vocal call-and-response phrase onsets |
| Build 2 | 125.05 | 129.85 | 9 -> 8 | 1.67 | 0.290 | drums | moombahton kick/snare (3+3+2 dembow syncopation) |
| Chorus 2 | 129.85 | 149.05 | 42 -> 46 | 2.40 | 0.162 | drums | moombahton kick/snare (3+3+2 dembow syncopation) |
| Final chorus | 149.05 | 170.65 | 58 -> 59 | 2.73 | 0.151 | drums | moombahton kick/snare (3+3+2 dembow syncopation) |
| Outro | 170.65 | 176.59 | 1 -> 0 | 0.00 | nan | vocal | vocal call-and-response phrase onsets; deliberately near-empty (break / held notes - breathing room) |

## Rules applied (user override, 11:55)

1. One layer per section (table above). Taps whose own-layer envelope was weak at the tap (another layer drove it) were removed, even when the full mix was loud there.
2. Repeated sections (Verse 1 / Verse 2; Pre-chorus 1 / Pre-chorus 2; Build 1 / Build 2; Chorus 1 / Chorus 2 / Final chorus) were aligned bar-by-bar on the 16th-slot grid: a slot is kept/added if most repeats have it and every repeat shows evidence; one-off slots were dropped unless very strong.
3. 16th bursts only where the onset of the FULL MIX (not a stem) is in the top percentile at the 16th off-position, with both neighbours on 8th positions and at least one on a beat - so a burst starts and ends on strong grid points (3-tap figures).
4. Held notes, breaks and outros keep their long gaps; no fills were added to reach CPM targets.
5. Faint onsets (layer < 0.22 or mix < 0.10 at the tap) removed unless they anchor a section start.

## Route (summary)

Route textures per section are listed in design.md; moves: intro-steps (stair), intro-sweep (alt), verse1-locker-zigzag (zig), pre1-diving-spiral (lspiral), build1-run (stair), chorus1-pool-U (zig), post1-switchbacks (lserp), verse2-court-loop (zig), pre2-phone-corridor (zig), build2-jump (alt), chorus2-overpass-stair (stair), final-spiral-stair (zig), outro (alt).

Not tested in the engine on a device; touch latency still needs confirming.
