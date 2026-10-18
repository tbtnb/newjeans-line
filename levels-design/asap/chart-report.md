# ASAP: chart report (worker 3)
| | value |
|---|---|
| legacy taps | 83 |
| new taps | **201** (x2.42) |
| grid | 130.012 BPM, 16th = 0.115374 s, phase -0.0049 s, attack calibration -17.3 ms |
| min gap | 0.115 s |
| fastest run | 11 taps with gaps <= 0.30 s, from 77.87 s to 79.72 s |
| attack offset (measured attack minus tap time, strongest-quartile attacks; spread includes hats/consonants caught by the ±35 ms window) | median -0.8 ms, MAD 1.5 ms |
| recommended judgment | per-tap good window = half the local gap, capped at ±100 ms (floor ±45 ms, schema v2.5); inside 16th bursts that is ±57 ms; perfect ±40 ms everywhere; a tap more than ±95 ms away from an isolated beat is a miss |
| difficulty tier | **hard** |

## Density vs original Dancing Line (dlfm-wiki CPM)
| level | avg CPM | peak CPM |
|---|---|---|
| **ASAP (this chart)** | **90** (taps / duration × 60) | **360** (most taps in any 1 s × 60; validator metric); 522 as 60 / min gap |
| The Racing (hardest) | 220 | 440 |
| Amusement Park | - | 512 |
| Storm | - | 460 |
| The Chaos | 136 | 408 |
| Chinese Garden | 148 | 296 |
| Winter | 140 | 280 |
| The Piano | 125 | 250 |
| The Autumn | 96 | - |

Note: the wiki's 'avg CPM' is not plain taps/duration (The Racing: 357 taps / 144 s = 149 by our formula vs 220 on the wiki), so compare our avg against ~149 for The Racing; peak CPM uses the same 1-second-window idea as the validator.

16th bursts: 12 added taps at 34.84 s (18:11, snare), 35.30 s (18:15, hat), 75.45 s (40:11, snare), 75.68 s (40:13, hat), 77.30 s (41:11, fx), 78.22 s (42:3, snare), 79.14 s (42:11, snare), 90.22 s (48:11, kick), 91.37 s (49:5, hat), 106.83 s (57:11, hat), 114.22 s (61:11, hat), 123.44 s (66:11, hat). Each burst tap sits on a real 16th event (snare/hat roll, flam or rapid vocal syllable, strength ≥ 0.5 within ±25 ms) at a fill, build-up, drop or final chorus.

## Per-section density
| section | t | old | new | new/s |
|---|---|---|---|---|
| Intro · snaps in the grass | 0.00-4.03 | 1 | 3 | 0.74 |
| Verse 1 · moon-green meadow | 4.03-11.42 | 3 | 8 | 1.08 |
| Verse 1b · clock in the sky | 11.42-26.18 | 9 | 13 | 0.88 |
| Pre · letters behind trees | 26.18-40.95 | 10 | 16 | 1.08 |
| Chorus 1 · swing of pendulums | 40.95-55.72 | 9 | 26 | 1.76 |
| Stop · held breath | 55.72-57.57 | 0 | 2 | 1.08 |
| Verse 2 · water garden | 57.57-72.33 | 11 | 22 | 1.49 |
| Dance break · stars in groups | 72.33-87.10 | 9 | 39 | 2.64 |
| Turnaround | 87.10-92.64 | 4 | 11 | 1.99 |
| Chorus 2 · the small house | 92.64-114.79 | 15 | 38 | 1.72 |
| Hush · lamp flickers | 114.79-120.33 | 5 | 4 | 0.72 |
| Final hook · lamp lights | 120.33-129.56 | 5 | 17 | 1.84 |
| Outro · pollen bunny | 129.56-134.39 | 2 | 2 | 0.41 |

## Spot checks (start, section changes, middle, end)
Offset = measured attack minus tap time (negative = attack slightly before the tap).

| t | bar:16th | tag | section | offset ms |
|---|---|---|---|---|
| 1.264 | 0:8 | snare | Intro · snaps in the grass | -7.8 |
| 2.187 | 1:0 | snare | Intro · snaps in the grass | -9.0 |
| 4.033 | 2:0 | bass | Verse 1 · moon-green meadow | -5.8 |
| 4.725 | 2:6 | hat | Verse 1 · moon-green meadow | +18.9 |
| 11.417 | 6:0 | vocal | Verse 1b · clock in the sky | -5.1 |
| 13.263 | 7:0 | kick | Verse 1b · clock in the sky | -4.0 |
| 26.185 | 14:0 | bass | Pre · letters behind trees | -32.1 |
| 27.339 | 14:10 | hat | Pre · letters behind trees | -0.9 |
| 40.953 | 22:0 | bass | Chorus 1 · swing of pendulums | +22.4 |
| 41.645 | 22:6 | vocal | Chorus 1 · swing of pendulums | -16.9 |
| 56.182 | 30:4 | snare | Stop · held breath | -1.1 |
| 56.644 | 30:8 | snare | Stop · held breath | -3.1 |
| 57.567 | 31:0 | kick | Verse 2 · water garden | -0.4 |
| 58.490 | 31:8 | kick | Verse 2 · water garden | -1.8 |
| 72.335 | 39:0 | kick | Dance break · stars in groups | -16.0 |
| 73.258 | 39:8 | kick | Dance break · stars in groups | -1.9 |
| 77.296 | 41:11 | fx | Dance break · stars in groups | -1.6 |
| 87.102 | 47:0 | kick | Turnaround | +0.0 |
| 88.025 | 47:8 | vocal | Turnaround | +0.8 |
| 92.640 | 50:0 | kick | Chorus 2 · the small house | +2.7 |
| 93.563 | 50:8 | kick | Chorus 2 · the small house | +0.8 |
| 114.792 | 62:0 | bass | Hush · lamp flickers | +12.6 |
| 116.638 | 63:0 | snare | Hush · lamp flickers | +3.5 |
| 120.792 | 65:4 | hat | Final hook · lamp lights | -17.6 |
| 121.253 | 65:8 | hat | Final hook · lamp lights | +26.1 |
| 129.560 | 70:0 | kick | Outro · pollen bunny | -3.0 |
| 131.406 | 71:0 | kick | Outro · pollen bunny | -3.0 |

## Rationale
ASAP is soft, so density stays moderate but musically placed: verses take the kick on 1 plus vocal pickups (16ths 6/10), the pre answers the vocal call-and-response (0-10, 0-6, 0-8), choruses end every phrase with a 6-tap 8th fill (0-6-8-10-12-14). The silent bar 30 has just the two snaps (that is where the line falls a level). The dance break is the busiest (34 taps with a full 8th bar each phrase, 9-tap runs at 77.9 s and 85.3 s); the hush drops to one tap per bar before the final hook.

## Rhythm-logic audit (integ-b)

Audited on 2026-10-18 by integrator B against the user's rule *rhythm logic beats density* (this chart was made before the rule). Taps **201 → 158** (-43; 43 removed, 0 added). Nothing was added to reach a CPM target.

Method (same thresholds as `tools/charts/chartlogic.py` and the Ditto trim): each section follows the one band that best explains its taps; a tap is removed if it is **faint** (followed band < 0.35, full mix < 0.35, every other band < 0.5), **off-layer** (followed band < 0.35 while another band ≥ 0.6) or a **weak burst** (gap < 0.15 s and neither the full mix nor the followed band ≥ 0.6). Strengths are onset strengths per band, normalised to the song's 99.5th percentile, max within ±30 ms of the tap. Removing a tap removes a turn, so the route was repaired by `tools/charts/integb_route.py`, which keeps the worker's own turn sequence phrase by phrase wherever it stays legal; worldPos landmarks were moved with the road.

### What the taps follow (per section)

| section | time | taps follow | taps before → after | /s after | median strength of followed band | removed (faint / off-layer / weak burst) |
|---|---|---|---|---|---|---|
| Intro · snaps in the grass | 0.00 | kick + snare drum groove (full mix) | 3 → 3 | 0.74 | 1.26 | 0 / 0 / 0 |
| Verse 1 · moon-green meadow | 4.03 | kick + snare drum groove (full mix) | 8 → 7 | 0.95 | 0.67 | 1 / 0 / 0 |
| Verse 1b · clock in the sky | 11.42 | kick + snare drum groove (full mix) | 13 → 11 | 0.74 | 0.67 | 2 / 0 / 0 |
| Pre · letters behind trees | 26.18 | hi-hat / shaker | 16 → 8 | 0.54 | 0.46 | 7 / 0 / 1 |
| Chorus 1 · swing of pendulums | 40.95 | kick + snare drum groove (full mix) | 26 → 14 | 0.95 | 0.43 | 12 / 0 / 0 |
| Stop · held breath | 55.72 | kick + snare drum groove (full mix) | 2 → 2 | 1.08 | 1.12 | 0 / 0 / 0 |
| Verse 2 · water garden | 57.57 | kick + snare drum groove (full mix) | 22 → 21 | 1.42 | 0.73 | 0 / 1 / 0 |
| Dance break · stars in groups | 72.33 | kick + snare drum groove (full mix) | 39 → 36 | 2.44 | 1.17 | 1 / 2 / 0 |
| Turnaround | 87.10 | melody / synth / vocal line (mid band) | 11 → 9 | 1.63 | 0.84 | 1 / 1 / 0 |
| Chorus 2 · the small house | 92.64 | kick + snare drum groove (full mix) | 38 → 32 | 1.44 | 0.82 | 2 / 1 / 3 |
| Hush · lamp flickers | 114.79 | kick + snare drum groove (full mix) | 4 → 3 | 0.54 | 0.87 | 1 / 0 / 0 |
| Final hook · lamp lights | 120.33 | kick + snare drum groove (full mix) | 17 → 10 | 1.08 | 0.42 | 5 / 0 / 2 |
| Outro · pollen bunny | 129.56 | kick + snare drum groove (full mix) | 2 → 2 | 0.41 | 0.53 | 0 / 0 / 0 |

### Audit diff (removed taps)

| t (s) | tag | reason | followed band | band strength | full-mix strength |
|---|---|---|---|---|---|
| 5.187 | kick | faint | drums | 0.31 | 0.16 |
| 14.186 | kick | faint | drums | 0.10 | 0.05 |
| 25.493 | vocal | faint | drums | 0.28 | 0.05 |
| 29.877 | vocal | faint | hat | 0.27 | 0.27 |
| 30.800 | vocal | faint | hat | 0.22 | 0.14 |
| 34.723 | bass | faint | hat | 0.30 | 0.12 |
| 34.838 | snare | weak-burst | hat | 0.42 | 0.49 |
| 35.415 | vocal | faint | hat | 0.25 | 0.23 |
| 37.261 | bass | faint | hat | 0.23 | 0.26 |
| 38.184 | kick | faint | hat | 0.28 | 0.13 |
| 39.107 | bass | faint | hat | 0.23 | 0.08 |
| 42.107 | vocal | faint | drums | 0.31 | 0.12 |
| 42.799 | bass | faint | drums | 0.32 | 0.32 |
| 47.183 | vocal | faint | drums | 0.23 | 0.18 |
| 48.337 | kick | faint | drums | 0.31 | 0.30 |
| 49.491 | vocal | faint | drums | 0.29 | 0.13 |
| 50.183 | bass | faint | drums | 0.32 | 0.26 |
| 52.952 | vocal | faint | drums | 0.26 | 0.17 |
| 54.567 | vocal | faint | drums | 0.22 | 0.16 |
| 54.798 | vocal | faint | drums | 0.18 | 0.11 |
| 55.028 | bass | faint | drums | 0.21 | 0.11 |
| 55.259 | bass | faint | drums | 0.21 | 0.06 |
| 55.490 | bass | faint | drums | 0.33 | 0.06 |
| 71.412 | bass | off-layer | drums | 0.30 | 0.23 |
| 75.565 | hat | off-layer | drums | 0.34 | 0.52 |
| 81.103 | vocal | faint | drums | 0.27 | 0.04 |
| 82.949 | hat | off-layer | drums | 0.33 | 0.24 |
| 90.333 | vocal | faint | mid | 0.17 | 0.13 |
| 91.371 | hat | off-layer | mid | 0.12 | 0.54 |
| 99.332 | bass | faint | drums | 0.26 | 0.21 |
| 106.716 | vocal | weak-burst | drums | 0.59 | 0.14 |
| 106.831 | hat | weak-burst | drums | 0.44 | 0.11 |
| 114.100 | vocal | faint | drums | 0.24 | 0.07 |
| 114.215 | hat | off-layer | drums | 0.32 | 0.14 |
| 114.331 | vocal | weak-burst | drums | 0.49 | 0.06 |
| 114.792 | bass | faint | drums | 0.34 | 0.07 |
| 121.715 | vocal | faint | drums | 0.16 | 0.06 |
| 123.330 | snare | weak-burst | drums | 0.49 | 0.58 |
| 123.445 | hat | weak-burst | drums | 0.29 | 0.12 |
| 125.868 | bass | faint | drums | 0.28 | 0.22 |
| 126.791 | vocal | faint | drums | 0.30 | 0.24 |
| 127.022 | vocal | faint | drums | 0.27 | 0.11 |
| 127.483 | vocal | faint | drums | 0.33 | 0.16 |

Added taps: none.

Original (pre-audit) chart and layout: `levels-design/asap/pre-audit/`. Integrated copy: `levels-src/asap/`. chartlogic report after the audit: `docs/verification/asap-chartlogic.md`.
