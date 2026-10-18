# Attention - chart report (designs-w1, v3, rhythm-logic audit)

- Audio: `public/audio/attention.mp3`, full track 178.00 s, untouched. Tempo grid measured from audio: **104.99 BPM**, beat 0.5715 s, downbeat phase 0.464 s. htdemucs stem envelopes shifted -25.03 ms before use.
- **Taps: legacy 139 -> previous designs-w1 chart 285 -> now 285** (2.05x legacy). Difficulty tier: hard (title track).
- Audit vs the override rules: 14 off-layer / faint taps removed, 32 one-off taps dropped and 43 taps added so repeated phrases share one pattern (each added slot had clear evidence in every repeat). 16th bursts: 3 inserted tap(s) at 77.185, 132.047, 150.335.
- Gaps: min **0.142 s**, median 0.297 s (floor 0.105 s).
- Fastest run (validator definition, gaps <= 0.30 s): **18 taps**, 73.61-78.19 s.
- Judgment window (engine rule min(0.5g, clamp(0.45g, 45, 110 ms)), g = local min gap): **min ±64 ms, median ±110 ms** - always <= half the local gap.

## Difficulty vs original Dancing Line

| Level | Taps / length | avg CPM (total taps / duration) | avg CPM (wiki-style) | peak CPM |
|---|---|---|---|---|
| **Attention (this chart)** | 285 / 2:58 | **96** | **202** (60/median gap; mean of 60/gap = 156) | **423** (60/min gap); 300 as taps-in-1 s x60 |
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
| Intro | 0.00 | 9.61 | 5 -> 5 | 0.52 | 1.698 | vocal | vocal syllables - one tap per sung syllable onset, held notes left open |
| Hook A | 9.61 | 27.89 | 32 -> 39 | 2.13 | 0.267 | drums | kick/snare backbeat and its syncopated pickups (the dotted/off-beat claps of the hook) |
| Verse 1 | 27.89 | 46.75 | 24 -> 17 | 0.90 | 0.278 | vocal | vocal syllables - one tap per sung syllable onset, held notes left open |
| Pre-chorus 1 | 46.75 | 62.18 | 22 -> 25 | 1.62 | 0.275 | vocal | vocal syllables - one tap per sung syllable onset, held notes left open |
| Chorus 1 | 62.18 | 83.32 | 46 -> 50 | 2.37 | 0.143 | drums | kick/snare backbeat and its syncopated pickups (the dotted/off-beat claps of the hook); 1 16th burst tap(s) on an audible fill, starting and ending on 8th/beat positions |
| Verse 2 | 83.32 | 101.60 | 20 -> 17 | 0.93 | 0.277 | vocal | vocal syllables - one tap per sung syllable onset, held notes left open |
| Pre-chorus 2 | 101.60 | 117.03 | 26 -> 24 | 1.56 | 0.162 | vocal | vocal syllables - one tap per sung syllable onset, held notes left open |
| Chorus 2 | 117.03 | 137.60 | 46 -> 46 | 2.24 | 0.143 | drums | kick/snare backbeat and its syncopated pickups (the dotted/off-beat claps of the hook); 1 16th burst tap(s) on an audible fill, starting and ending on 8th/beat positions |
| Final chorus | 137.60 | 156.10 | 45 -> 43 | 2.32 | 0.142 | drums | kick/snare backbeat and its syncopated pickups (the dotted/off-beat claps of the hook); 1 16th burst tap(s) on an audible fill, starting and ending on 8th/beat positions |
| Outro | 156.10 | 178.00 | 19 -> 19 | 0.87 | 0.267 | vocal | vocal syllables - one tap per sung syllable onset, held notes left open |

## Rules applied (user override, 11:55)

1. One layer per section (table above). Taps whose own-layer envelope was weak at the tap (another layer drove it) were removed, even when the full mix was loud there.
2. Repeated sections (Hook A / Chorus 1 / Chorus 2 / Final chorus; Verse 1 / Verse 2; Pre-chorus 1 / Pre-chorus 2) were aligned bar-by-bar on the 16th-slot grid: a slot is kept/added if most repeats have it and every repeat shows evidence; one-off slots were dropped unless very strong.
3. 16th bursts only where the onset of the FULL MIX (not a stem) is in the top percentile at the 16th off-position, with both neighbours on 8th positions and at least one on a beat - so a burst starts and ends on strong grid points (3-tap figures).
4. Held notes, breaks and outros keep their long gaps; no fills were added to reach CPM targets.
5. Faint onsets (layer < 0.22 or mix < 0.10 at the tap) removed unless they anchor a section start.

## Route (summary)

Route textures per section are listed in design.md; moves: intro (alt), hookA-stair (stair), hookA-zig (zig), verse1-switchback (lserp), pre1-skybridge (stair), chorus1-wrap (zig), verse2-spiral (lspiral), verse2-wall (lserp), pre2-sawtooth (zig), chorus2-zigzag (zig), final-loop (zig), outro-sweep (alt), outro-switch (lserp).

Not tested in the engine on a device; touch latency still needs confirming.
