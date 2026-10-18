# ETA: chart report (worker 3)
| | value |
|---|---|
| legacy taps | 232 |
| new taps | **422** (x1.82) |
| grid | 134.998 BPM, 16th = 0.111113 s, phase 0.0032 s, attack calibration -29.3 ms |
| min gap | 0.111 s |
| fastest run | 19 taps with gaps <= 0.30 s, from 131.00 s to 134.67 s |
| attack offset (measured attack minus tap time, strongest-quartile attacks; spread includes hats/consonants caught by the ±35 ms window) | median -1.9 ms, MAD 10.0 ms |
| recommended judgment | per-tap good window = half the local gap, capped at ±100 ms (floor ±45 ms, schema v2.5); inside 16th bursts that is ±55 ms; perfect ±40 ms everywhere; a tap more than ±90 ms away from an isolated beat is a miss |
| difficulty tier | **hard** |

## Density vs original Dancing Line (dlfm-wiki CPM)
| level | avg CPM | peak CPM |
|---|---|---|
| **ETA (this chart)** | **167** (taps / duration × 60) | **420** (most taps in any 1 s × 60; validator metric); 541 as 60 / min gap |
| The Racing (hardest) | 220 | 440 |
| Amusement Park | - | 512 |
| Storm | - | 460 |
| The Chaos | 136 | 408 |
| Chinese Garden | 148 | 296 |
| Winter | 140 | 280 |
| The Piano | 125 | 250 |
| The Autumn | 96 | - |

Note: the wiki's 'avg CPM' is not plain taps/duration (The Racing: 357 taps / 144 s = 149 by our formula vs 220 on the wiki), so compare our avg against ~149 for The Racing; peak CPM uses the same 1-second-window idea as the validator.

16th bursts: 12 added taps at 35.12 s (18:13, hat), 35.34 s (18:15, vocal), 85.12 s (46:15, vocal), 92.00 s (50:13, snare), 92.23 s (50:15, vocal), 92.67 s (51:3, vocal), 94.45 s (52:3, vocal), 113.34 s (62:13, vocal), 116.89 s (64:13, vocal), 129.34 s (71:13, vocal), 132.89 s (73:13, vocal), 134.67 s (74:13, hat). Each burst tap sits on a real 16th event (snare/hat roll, flam or rapid vocal syllable, strength ≥ 0.5 within ±25 ms) at a fill, build-up, drop or final chorus.

## Per-section density
| section | t | old | new | new/s |
|---|---|---|---|---|
| Intro · phone desk | 0.00-7.00 | 6 | 12 | 1.71 |
| Verse 1 · first message | 7.00-21.23 | 22 | 34 | 2.39 |
| Pre 1 · forwarding blocks | 21.23-35.45 | 23 | 42 | 2.95 |
| Chorus 1 · signal city hook | 35.45-47.89 | 21 | 41 | 3.29 |
| Stop 1 · E-T-A voice chops | 47.89-49.67 | 2 | 6 | 3.38 |
| Verse 2 · rumor mill | 49.67-63.89 | 24 | 38 | 2.67 |
| Pre 2 · fragments rising | 63.89-78.11 | 22 | 34 | 2.39 |
| Pre 3 · tower lift | 78.11-92.34 | 24 | 44 | 3.09 |
| Chorus 2 · assembled scene hook | 92.34-104.78 | 20 | 43 | 3.46 |
| Stop 2 · E-T-A voice chops | 104.78-106.56 | 3 | 6 | 3.37 |
| Final A · rush hour | 106.56-120.78 | 23 | 50 | 3.52 |
| Final B · arrival sprint | 120.78-135.00 | 23 | 59 | 4.15 |
| Outro · two bench lamps | 135.00-151.37 | 19 | 13 | 0.79 |

## Spot checks (start, section changes, middle, end)
Offset = measured attack minus tap time (negative = attack slightly before the tap).

| t | bar:16th | tag | section | offset ms |
|---|---|---|---|---|
| 1.670 | 0:0 | snare | Intro · phone desk | +1.8 |
| 2.337 | 0:6 | vocal | Intro · phone desk | -9.6 |
| 7.003 | 3:0 | snare | Verse 1 · first message | +0.0 |
| 7.448 | 3:4 | kick | Verse 1 · first message | +0.6 |
| 21.226 | 11:0 | snare | Pre 1 · forwarding blocks | -18.0 |
| 22.115 | 11:8 | kick | Pre 1 · forwarding blocks | -21.5 |
| 35.670 | 19:2 | hat | Chorus 1 · signal city hook | +0.6 |
| 35.893 | 19:4 | kick | Chorus 1 · signal city hook | +20.6 |
| 48.115 | 26:2 | kick | Stop 1 · E-T-A voice chops | +7.4 |
| 48.337 | 26:4 | kick | Stop 1 · E-T-A voice chops | -6.1 |
| 49.671 | 27:0 | snare | Verse 2 · rumor mill | -1.4 |
| 50.115 | 27:4 | kick | Verse 2 · rumor mill | +1.5 |
| 63.893 | 35:0 | snare | Pre 2 · fragments rising | +22.1 |
| 64.782 | 35:8 | kick | Pre 2 · fragments rising | -21.7 |
| 78.115 | 43:0 | snare | Pre 3 · tower lift | -24.3 |
| 78.560 | 43:4 | kick | Pre 3 · tower lift | +1.1 |
| 79.893 | 44:0 | snare | Pre 3 · tower lift | +0.1 |
| 92.560 | 51:2 | hat | Chorus 2 · assembled scene hook | -0.5 |
| 92.671 | 51:3 | vocal | Chorus 2 · assembled scene hook | -7.6 |
| 105.005 | 58:2 | kick | Stop 2 · E-T-A voice chops | +2.0 |
| 105.227 | 58:4 | kick | Stop 2 · E-T-A voice chops | -7.1 |
| 106.560 | 59:0 | snare | Final A · rush hour | -1.4 |
| 107.005 | 59:4 | kick | Final A · rush hour | +0.4 |
| 120.783 | 67:0 | snare | Final B · arrival sprint | +21.2 |
| 121.005 | 67:2 | snare | Final B · arrival sprint | +25.7 |
| 135.672 | 75:6 | vocal | Outro · two bench lamps | -16.6 |
| 136.116 | 75:10 | vocal | Outro · two bench lamps | +1.5 |
| 147.450 | 82:0 | snare | Outro · two bench lamps | +3.5 |

## Rationale
The chart follows the groove instead of every hat: verses sit on the four-on-the-floor kick with small syncopated pickups (16th 14 = the "a" before the next downbeat), the pre-choruses build bar by bar from quarters to a full 8th run (bar 18 is E8), and both choruses use the hook's own rhythm (16ths 2-4-6-8-12-15 / 2-4-8-10-12-15), which is why the road turns on the off-beats there. The two "E-T-A" stops take the six voice chops exactly. The final A/B choruses are the climax: 8th runs every fourth bar and a 19-tap run with 16th flams (131.0-134.7 s) into the outro, mirroring Dancing Line's long climax runs. The outro thins to one tap per bar so the ending breathes.

## Rhythm-logic audit (integ-b)

Audited on 2026-10-18 by integrator B against the user's rule *rhythm logic beats density* (this chart was made before the rule). Taps **422 → 413** (-9; 9 removed, 0 added). Nothing was added to reach a CPM target.

Method (same thresholds as `tools/charts/chartlogic.py` and the Ditto trim): each section follows the one band that best explains its taps; a tap is removed if it is **faint** (followed band < 0.35, full mix < 0.35, every other band < 0.5), **off-layer** (followed band < 0.35 while another band ≥ 0.6) or a **weak burst** (gap < 0.15 s and neither the full mix nor the followed band ≥ 0.6). Strengths are onset strengths per band, normalised to the song's 99.5th percentile, max within ±30 ms of the tap. Removing a tap removes a turn, so the route was repaired by `tools/charts/integb_route.py`, which keeps the worker's own turn sequence phrase by phrase wherever it stays legal; worldPos landmarks were moved with the road.

### What the taps follow (per section)

| section | time | taps follow | taps before → after | /s after | median strength of followed band | removed (faint / off-layer / weak burst) |
|---|---|---|---|---|---|---|
| Intro · phone desk | 0.00 | melody / synth / vocal line (mid band) | 12 → 12 | 1.71 | 0.91 | 0 / 0 / 0 |
| Verse 1 · first message | 7.00 | kick + snare drum groove (full mix) | 34 → 34 | 2.39 | 0.73 | 0 / 0 / 0 |
| Pre 1 · forwarding blocks | 21.23 | kick + snare drum groove (full mix) | 42 → 41 | 2.88 | 0.91 | 0 / 0 / 1 |
| Chorus 1 · signal city hook | 35.45 | kick + snare drum groove (full mix) | 41 → 41 | 3.29 | 0.97 | 0 / 0 / 0 |
| Stop 1 · E-T-A voice chops | 47.89 | kick + snare drum groove (full mix) | 6 → 6 | 3.38 | 0.50 | 0 / 0 / 0 |
| Verse 2 · rumor mill | 49.67 | kick + snare drum groove (full mix) | 38 → 38 | 2.67 | 0.90 | 0 / 0 / 0 |
| Pre 2 · fragments rising | 63.89 | kick + snare drum groove (full mix) | 34 → 34 | 2.39 | 0.84 | 0 / 0 / 0 |
| Pre 3 · tower lift | 78.11 | melody / synth / vocal line (mid band) | 44 → 44 | 3.09 | 0.90 | 0 / 0 / 0 |
| Chorus 2 · assembled scene hook | 92.34 | kick + snare drum groove (full mix) | 43 → 40 | 3.21 | 0.96 | 0 / 0 / 3 |
| Stop 2 · E-T-A voice chops | 104.78 | kick + snare drum groove (full mix) | 6 → 5 | 2.81 | 0.54 | 1 / 0 / 0 |
| Final A · rush hour | 106.56 | kick + snare drum groove (full mix) | 50 → 49 | 3.45 | 0.81 | 0 / 0 / 1 |
| Final B · arrival sprint | 120.78 | kick + snare drum groove (full mix) | 59 → 56 | 3.94 | 0.74 | 0 / 0 / 3 |
| Outro · two bench lamps | 135.00 | kick + snare drum groove (full mix) | 13 → 13 | 0.84 | 0.88 | 0 / 0 / 0 |

### Audit diff (removed taps)

| t (s) | tag | reason | followed band | band strength | full-mix strength |
|---|---|---|---|---|---|
| 35.115 | hat | weak-burst | drums | 0.57 | 0.59 |
| 92.560 | hat | weak-burst | drums | 0.49 | 0.51 |
| 92.671 | vocal | weak-burst | drums | 0.42 | 0.18 |
| 94.449 | vocal | weak-burst | drums | 0.44 | 0.21 |
| 105.783 | vocal | faint | drums | 0.33 | 0.05 |
| 116.894 | vocal | weak-burst | drums | 0.45 | 0.26 |
| 129.338 | vocal | weak-burst | drums | 0.41 | 0.15 |
| 132.894 | vocal | weak-burst | drums | 0.47 | 0.28 |
| 134.672 | hat | weak-burst | drums | 0.52 | 0.46 |

Added taps: none.

Original (pre-audit) chart and layout: `levels-design/eta/pre-audit/`. Integrated copy: `levels-src/eta/`. chartlogic report after the audit: `docs/verification/eta-chartlogic.md`.
