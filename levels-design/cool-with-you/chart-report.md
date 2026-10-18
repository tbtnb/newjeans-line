# Cool With You: chart report (worker 3)
| | value |
|---|---|
| legacy taps | 107 |
| new taps | **252** (x2.36) |
| grid | 134.995 BPM, 16th = 0.111115 s, phase 0.0011 s, attack calibration -21.0 ms |
| min gap | 0.111 s |
| fastest run | 15 taps with gaps <= 0.30 s, from 124.78 s to 127.89 s |
| attack offset (measured attack minus tap time, strongest-quartile attacks; spread includes hats/consonants caught by the ±35 ms window) | median -7.1 ms, MAD 13.1 ms |
| recommended judgment | per-tap good window = half the local gap, capped at ±100 ms (floor ±45 ms, schema v2.5); inside 16th bursts that is ±55 ms; perfect ±40 ms everywhere; a tap more than ±95 ms away from an isolated beat is a miss |
| difficulty tier | **moderate** |

## Density vs original Dancing Line (dlfm-wiki CPM)
| level | avg CPM | peak CPM |
|---|---|---|
| **Cool With You (this chart)** | **102** (taps / duration × 60) | **300** (most taps in any 1 s × 60; validator metric); 541 as 60 / min gap |
| The Racing (hardest) | 220 | 440 |
| Amusement Park | - | 512 |
| Storm | - | 460 |
| The Chaos | 136 | 408 |
| Chinese Garden | 148 | 296 |
| Winter | 140 | 280 |
| The Piano | 125 | 250 |
| The Autumn | 96 | - |

Note: the wiki's 'avg CPM' is not plain taps/duration (The Racing: 357 taps / 144 s = 149 by our formula vs 220 on the wiki), so compare our avg against ~149 for The Racing; peak CPM uses the same 1-second-window idea as the validator.

16th bursts: 4 added taps at 70.11 s (39:4, snare), 105.67 s (59:4, snare), 112.78 s (63:4, snare), 118.12 s (66:4, snare). Each burst tap sits on a real 16th event (snare/hat roll, flam or rapid vocal syllable, strength ≥ 0.5 within ±25 ms) at a fill, build-up, drop or final chorus.

## Per-section density
| section | t | old | new | new/s |
|---|---|---|---|---|
| Intro · empty gallery | 0.00-14.56 | 7 | 10 | 0.69 |
| Verse 1 · reflections wake | 14.56-28.78 | 12 | 22 | 1.55 |
| Verse 1b · rain curtain | 28.78-43.00 | 12 | 26 | 1.83 |
| Hook · moonlit pool (stripped) | 43.00-57.23 | 8 | 18 | 1.27 |
| Drop 1 · open courtyard | 57.23-71.45 | 12 | 37 | 2.60 |
| Verse 2 · two lights approach | 71.45-85.67 | 12 | 24 | 1.69 |
| Break · one light leaves | 85.67-92.78 | 5 | 7 | 0.98 |
| Build · wings unfold | 92.78-99.89 | 7 | 18 | 2.53 |
| Final drop A · feather storm | 99.89-114.12 | 12 | 38 | 2.67 |
| Final drop B · choosing to stay | 114.12-128.34 | 12 | 47 | 3.30 |
| Outro · open exit | 128.34-147.88 | 8 | 5 | 0.26 |

## Spot checks (start, section changes, middle, end)
Offset = measured attack minus tap time (negative = attack slightly before the tap).

| t | bar:16th | tag | section | offset ms |
|---|---|---|---|---|
| 2.779 | 1:6 | kick | Intro · empty gallery | +15.7 |
| 3.223 | 1:10 | bass | Intro · empty gallery | +30.1 |
| 14.557 | 8:0 | snare | Verse 1 · reflections wake | -29.2 |
| 15.668 | 8:10 | kick | Verse 1 · reflections wake | -18.2 |
| 28.780 | 16:0 | kick | Verse 1b · rain curtain | +13.7 |
| 29.891 | 16:10 | kick | Verse 1b · rain curtain | -25.7 |
| 43.003 | 24:0 | kick | Hook · moonlit pool (stripped) | +15.7 |
| 43.892 | 24:8 | kick | Hook · moonlit pool (stripped) | +15.5 |
| 57.225 | 32:0 | kick | Drop 1 · open courtyard | +21.8 |
| 57.892 | 32:6 | snare | Drop 1 · open courtyard | +17.1 |
| 71.448 | 40:0 | kick | Verse 2 · two lights approach | +31.4 |
| 72.559 | 40:10 | kick | Verse 2 · two lights approach | +32.1 |
| 79.671 | 44:10 | kick | Verse 2 · two lights approach | +30.7 |
| 85.671 | 48:0 | kick | Break · one light leaves | -22.6 |
| 87.449 | 49:0 | kick | Break · one light leaves | -6.3 |
| 92.782 | 52:0 | vocal | Build · wings unfold | +25.0 |
| 93.671 | 52:8 | kick | Build · wings unfold | -32.8 |
| 99.894 | 56:0 | vocal | Final drop A · feather storm | -34.1 |
| 100.560 | 56:6 | snare | Final drop A · feather storm | +28.3 |
| 114.116 | 64:0 | kick | Final drop B · choosing to stay | +15.4 |
| 114.450 | 64:3 | kick | Final drop B · choosing to stay | +12.3 |
| 128.339 | 72:0 | bass | Outro · open exit | +5.2 |
| 131.895 | 74:0 | kick | Outro · open exit | +20.9 |
| 139.006 | 78:0 | kick | Outro · open exit | +3.9 |

## Rationale
Two-step needs restraint: the kick pattern (1 and the "and" of 3, 16ths 0 and 10) carries the verses, with the 16th-6 ghost added every other bar; phrase-end bars get the garage fill (0-3-6-10[-12-14]). The stripped hook only takes downbeats and half-bars so the moonlit-pool section reads as long, calm straights. Drops add the snare on 12 and an 8th fill at each phrase end; the final drop B ends with two full 8th bars (15-tap run, 124.8-127.9 s), the densest moment, then the outro opens up to one tap every two bars.

## Rhythm-logic audit (integ-b)

Audited on 2026-10-18 by integrator B against the user's rule *rhythm logic beats density* (this chart was made before the rule). Taps **252 → 244** (-8; 8 removed, 0 added). Nothing was added to reach a CPM target.

Method (same thresholds as `tools/charts/chartlogic.py` and the Ditto trim): each section follows the one band that best explains its taps; a tap is removed if it is **faint** (followed band < 0.35, full mix < 0.35, every other band < 0.5), **off-layer** (followed band < 0.35 while another band ≥ 0.6) or a **weak burst** (gap < 0.15 s and neither the full mix nor the followed band ≥ 0.6). Strengths are onset strengths per band, normalised to the song's 99.5th percentile, max within ±30 ms of the tap. Removing a tap removes a turn, so the route was repaired by `tools/charts/integb_route.py`, which keeps the worker's own turn sequence phrase by phrase wherever it stays legal; worldPos landmarks were moved with the road.

### What the taps follow (per section)

| section | time | taps follow | taps before → after | /s after | median strength of followed band | removed (faint / off-layer / weak burst) |
|---|---|---|---|---|---|---|
| Intro · empty gallery | 0.00 | kick + snare drum groove (full mix) | 10 → 9 | 0.62 | 0.90 | 1 / 0 / 0 |
| Verse 1 · reflections wake | 14.56 | kick + snare drum groove (full mix) | 22 → 20 | 1.41 | 0.95 | 2 / 0 / 0 |
| Verse 1b · rain curtain | 28.78 | kick + snare drum groove (full mix) | 26 → 26 | 1.83 | 0.89 | 0 / 0 / 0 |
| Hook · moonlit pool (stripped) | 43.00 | kick + snare drum groove (full mix) | 18 → 18 | 1.27 | 0.73 | 0 / 0 / 0 |
| Drop 1 · open courtyard | 57.23 | kick + snare drum groove (full mix) | 37 → 36 | 2.53 | 0.78 | 0 / 1 / 0 |
| Verse 2 · two lights approach | 71.45 | kick + snare drum groove (full mix) | 24 → 24 | 1.69 | 0.94 | 0 / 0 / 0 |
| Break · one light leaves | 85.67 | melody / synth / vocal line (mid band) | 7 → 6 | 0.84 | 1.08 | 1 / 0 / 0 |
| Build · wings unfold | 92.78 | kick + snare drum groove (full mix) | 18 → 16 | 2.25 | 0.92 | 2 / 0 / 0 |
| Final drop A · feather storm | 99.89 | kick + snare drum groove (full mix) | 38 → 37 | 2.60 | 0.76 | 0 / 1 / 0 |
| Final drop B · choosing to stay | 114.12 | kick + snare drum groove (full mix) | 47 → 47 | 3.30 | 0.79 | 0 / 0 / 0 |
| Outro · open exit | 128.34 | kick + snare drum groove (full mix) | 5 → 5 | 0.37 | 0.97 | 0 / 0 / 0 |

### Audit diff (removed taps)

| t (s) | tag | reason | followed band | band strength | full-mix strength |
|---|---|---|---|---|---|
| 6.779 | bass | faint | drums | 0.16 | 0.01 |
| 16.335 | vocal | faint | drums | 0.18 | 0.16 |
| 17.891 | vocal | faint | drums | 0.21 | 0.10 |
| 70.781 | hat | off-layer | drums | 0.25 | 0.27 |
| 91.671 | bass | faint | mid | 0.21 | 0.12 |
| 98.338 | vocal | faint | drums | 0.24 | 0.13 |
| 99.671 | vocal | faint | drums | 0.20 | 0.12 |
| 113.450 | vocal | off-layer | drums | 0.19 | 0.37 |

Added taps: none.

Original (pre-audit) chart and layout: `levels-design/cool-with-you/pre-audit/`. Integrated copy: `levels-src/cool-with-you/`. chartlogic report after the audit: `docs/verification/cool-with-you-chartlogic.md`.
