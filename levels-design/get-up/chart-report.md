# Get Up: chart report (worker 3)
| | value |
|---|---|
| legacy taps | 16 |
| new taps | **39** (x2.44) |
| grid | 120.022 BPM, 16th = 0.124977 s, phase 0.0854 s, attack calibration -19.0 ms |
| min gap | 0.250 s |
| fastest run | 2 taps with gaps <= 0.30 s, from 10.08 s to 10.33 s (also at 16.1, 20.1, 24.1, 26.1 s) |
| attack offset (measured attack minus tap time, strongest-quartile attacks; spread includes hats/consonants caught by the ±35 ms window) | median +4.6 ms, MAD 7.5 ms |
| recommended judgment | per-tap good window = half the local gap, capped at ±100 ms (floor ±45 ms, schema v2.5); densest runs that is ±100 ms; perfect ±50 ms everywhere; a tap more than ±125 ms away from an isolated beat is a miss |
| difficulty tier | **easy** |

## Density vs original Dancing Line (dlfm-wiki CPM)
| level | avg CPM | peak CPM |
|---|---|---|
| **Get Up (this chart)** | **65** (taps / duration × 60) | **180** (most taps in any 1 s × 60; validator metric); 240 as 60 / min gap |
| The Racing (hardest) | 220 | 440 |
| Amusement Park | - | 512 |
| Storm | - | 460 |
| The Chaos | 136 | 408 |
| Chinese Garden | 148 | 296 |
| Winter | 140 | 280 |
| The Piano | 125 | 250 |
| The Autumn | 96 | - |

Note: the wiki's 'avg CPM' is not plain taps/duration (The Racing: 357 taps / 144 s = 149 by our formula vs 220 on the wiki), so compare our avg against ~149 for The Racing; peak CPM uses the same 1-second-window idea as the validator.

16th bursts: 0 added taps at none (Get Up is the easy tier: no drums, no 16ths). Each burst tap sits on a real 16th event (snare/hat roll, flam or rapid vocal syllable, strength ≥ 0.5 within ±25 ms) at a fill, build-up, drop or final chorus.

## Per-section density
| section | t | old | new | new/s |
|---|---|---|---|---|
| After the rain · shallow water | 0.00-8.33 | 3 | 7 | 0.84 |
| One warm light | 8.33-16.33 | 4 | 10 | 1.25 |
| Horizon gathers | 16.33-24.33 | 4 | 12 | 1.50 |
| Five lights · moon-green grass | 24.33-32.33 | 4 | 9 | 1.13 |
| Last step | 32.33-36.23 | 1 | 1 | 0.26 |

## Spot checks (start, section changes, middle, end)
Offset = measured attack minus tap time (negative = attack slightly before the tap).

| t | bar:16th | tag | section | offset ms |
|---|---|---|---|---|
| 1.335 | 0:8 | kick | After the rain · shallow water | +4.9 |
| 2.335 | 1:0 | snare | After the rain · shallow water | -19.7 |
| 8.334 | 4:0 | kick | One warm light | +8.2 |
| 9.334 | 4:8 | snare | One warm light | -16.8 |
| 16.332 | 8:0 | kick | Horizon gathers | -13.6 |
| 17.332 | 8:8 | kick | Horizon gathers | -7.5 |
| 17.832 | 8:12 | kick | Horizon gathers | +7.5 |
| 24.331 | 12:0 | kick | Five lights · moon-green grass | +11.3 |
| 25.331 | 12:8 | snare | Five lights · moon-green grass | +3.1 |
| 33.329 | 16:8 | bass | Last step | -21.2 |

## Rationale
Get Up has no drums, so the chart rides the half-bar swells (16ths 0 and 8 at 120 BPM = every 1.0 s) and adds the pick-up on 16th 12/14 only where a vocal entry is audible. 39 taps (old 16) keeps the interlude meditative: no runs longer than two taps, wide road, slow speed. The last tap lands on the final vocal swell at 33.3 s and the line glides to the end of the 36 s file.
