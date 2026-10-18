# Hurt - chart report (designs-w1, v3, rhythm-logic audit)

- Audio: `public/audio/hurt.mp3`, full track 175.01 s, untouched. Tempo grid measured from audio: **90.00 BPM**, beat 0.6667 s, downbeat phase 0.260 s. htdemucs stem envelopes shifted -25.03 ms before use.
- **Taps: legacy 64 -> previous designs-w1 chart 144 -> now 118** (1.84x legacy). Difficulty tier: moderate (ballad).
- Audit vs the override rules: 15 off-layer / faint taps removed, 13 one-off taps dropped and 2 taps added so repeated phrases share one pattern (each added slot had clear evidence in every repeat). 16th bursts: 0 inserted tap(s) at none.
- Gaps: min **0.316 s**, median 1.324 s (floor 0.105 s).
- Fastest run (validator definition, gaps <= 0.30 s): **1 taps**, 168.26-168.26 s.
- Judgment window (engine rule min(0.5g, clamp(0.45g, 45, 110 ms)), g = local min gap): **min ±110 ms, median ±110 ms** - always <= half the local gap.

## Difficulty vs original Dancing Line

| Level | Taps / length | avg CPM (total taps / duration) | avg CPM (wiki-style) | peak CPM |
|---|---|---|---|---|
| **Hurt (this chart)** | 118 / 2:55 | **40** | **45** (60/median gap; mean of 60/gap = 64) | **190** (60/min gap); 180 as taps-in-1 s x60 |
| The Racing (hardest) | 357 / 2:24 | 149 | 220 | 440 |
| The Chaos | - | - | 136 | 408 |
| Chinese Garden | - | - | 148 | 296 |
| Winter | - | - | 140 | 280 |
| Piano | - | - | 125 | 250 |
| Autumn | - | - | 96 | - |

Wiki-style avg CPM is approximated as 60 / median tap gap (the wiki does not publish its formula; for The Racing total/duration gives 149 while the wiki says 220, so it is clearly a playing-tempo measure rather than taps per minute of audio). Peak CPM = 60 / shortest gap, which reproduces the wiki numbers (Racing 16ths at 110 BPM = 0.136 s = 440).

Honest peak 190 CPM is below the 400-460 "title track" reference. That is deliberate (user override: rhythmic logic beats density): there are no 16th figures prominent enough in the full mix to justify bursts.

## Per-section density and what the taps follow

| Section | Start | End | Taps (before audit -> now) | Taps/s | Min gap | Layer | What the taps follow |
|---|---|---|---|---|---|---|---|
| Intro | 0.00 | 10.93 | 5 -> 5 | 0.46 | 0.992 | drums | the bass/chord hits that open each bar (about one per bar) |
| Verse 1 | 10.93 | 32.26 | 15 -> 17 | 0.80 | 0.336 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Pre-chorus 1 | 32.26 | 42.93 | 9 -> 8 | 0.75 | 0.661 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Chorus 1 | 42.93 | 64.26 | 21 -> 17 | 0.80 | 0.322 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Verse 2 | 64.26 | 80.26 | 14 -> 7 | 0.44 | 0.662 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Breath | 80.26 | 85.59 | 2 -> 1 | 0.19 | nan | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills); deliberately near-empty (break / held notes - breathing room) |
| Pre-chorus 2 | 85.59 | 96.26 | 9 -> 7 | 0.66 | 0.335 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Chorus 2 | 96.26 | 117.59 | 22 -> 18 | 0.84 | 0.341 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Bridge | 117.59 | 128.26 | 9 -> 9 | 0.84 | 0.666 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Final chorus | 128.26 | 143.59 | 18 -> 12 | 0.78 | 0.316 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |
| Outro | 143.59 | 175.01 | 20 -> 17 | 0.54 | 0.316 | vocal | vocal phrase onsets and held-note releases (sung syllables only, no drum fills) |

## Rules applied (user override, 11:55)

1. One layer per section (table above). Taps whose own-layer envelope was weak at the tap (another layer drove it) were removed, even when the full mix was loud there.
2. Repeated sections (Verse 1 / Verse 2; Pre-chorus 1 / Pre-chorus 2; Chorus 1 / Chorus 2 / Final chorus) were aligned bar-by-bar on the 16th-slot grid: a slot is kept/added if most repeats have it and every repeat shows evidence; one-off slots were dropped unless very strong.
3. 16th bursts only where the onset of the FULL MIX (not a stem) is in the top percentile at the 16th off-position, with both neighbours on 8th positions and at least one on a beat - so a burst starts and ends on strong grid points (3-tap figures).
4. Held notes, breaks and outros keep their long gaps; no fills were added to reach CPM targets.
5. Faint onsets (layer < 0.22 or mix < 0.10 at the tap) removed unless they anchor a section start.

## Route (summary)

Route textures per section are listed in design.md; moves: intro-sweep (alt), verse1-frame-switchbacks (lserp), pre1-paper-stair (stair), chorus1-court-horseshoe (zig), verse2-reed-switchbacks (lserp), breath-straight (alt), pre2-paper-corridor (zig), chorus2-trestle-U (zig), bridge-quiet-switchbacks (lserp), final-fan-terraces (zig), outro-long-steps (stair).

Not tested in the engine on a device; touch latency still needs confirming.
