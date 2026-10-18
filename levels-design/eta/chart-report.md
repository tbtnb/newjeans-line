# ETA: chart report (worker 3)
| | value |
|---|---|
| legacy taps | 232 |
| new taps | **410** (x1.77) |
| grid | 134.998 BPM, 16th = 0.111113 s, phase 0.0032 s, attack calibration -29.3 ms |
| min gap | 0.222 s |
| fastest run | 17 taps with gaps <= 0.30 s, from 131.00 s to 134.56 s |
| attack offset (measured attack minus tap time, strongest-quartile attacks; spread includes hats/consonants caught by the ±35 ms window) | median -2.5 ms, MAD 9.7 ms |
| recommended judgment | perfect ±45 ms, good ±90 ms, miss beyond ±110 ms (good < half the min gap; engine v2.3 uses grace-based judging on event timestamps) |

## Per-section density
| section | t | old | new | new/s |
|---|---|---|---|---|
| Intro · phone desk | 0.00-7.00 | 6 | 12 | 1.71 |
| Verse 1 · first message | 7.00-21.23 | 22 | 34 | 2.39 |
| Pre 1 · forwarding blocks | 21.23-35.45 | 23 | 40 | 2.81 |
| Chorus 1 · signal city hook | 35.45-47.89 | 21 | 41 | 3.29 |
| Stop 1 · E-T-A voice chops | 47.89-49.67 | 2 | 6 | 3.38 |
| Verse 2 · rumor mill | 49.67-63.89 | 24 | 38 | 2.67 |
| Pre 2 · fragments rising | 63.89-78.11 | 22 | 34 | 2.39 |
| Pre 3 · tower lift | 78.11-92.34 | 24 | 41 | 2.88 |
| Chorus 2 · assembled scene hook | 92.34-104.78 | 20 | 41 | 3.29 |
| Stop 2 · E-T-A voice chops | 104.78-106.56 | 3 | 6 | 3.37 |
| Final A · rush hour | 106.56-120.78 | 23 | 48 | 3.38 |
| Final B · arrival sprint | 120.78-135.00 | 23 | 56 | 3.94 |
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
| 92.560 | 51:2 | hat | Chorus 2 · assembled scene hook | -0.5 |
| 92.782 | 51:4 | bass | Chorus 2 · assembled scene hook | +20.4 |
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
The chart follows the groove instead of every hat: verses sit on the four-on-the-floor kick with small syncopated pickups (16th 14 = the "a" before the next downbeat), the pre-choruses build bar by bar from quarters to a full 8th run (bar 18 is E8), and both choruses use the hook's own rhythm (16ths 2-4-6-8-12-15 / 2-4-8-10-12-15), which is why the road turns on the off-beats there. The two "E-T-A" stops take the six voice chops exactly. The final A/B choruses are the climax: 8th runs every fourth bar and a 17-tap 8th run (131.0-134.6 s) into the outro, mirroring Dancing Line's long climax runs. The outro thins to one tap per bar so the ending breathes.
