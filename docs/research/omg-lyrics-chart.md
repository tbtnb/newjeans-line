# OMG chart v3: one rule for the whole song

**The rule (same in every section, no exceptions):**
1. **Vocal = backbone.** In every sung line, tap the line's first syllable, every syllable of the title hooks, and the clearest other syllables.
   The same limits apply everywhere: at most 5 vocal taps per bar and 5 in any 2 s. Repeated lyrics and copied vocals get the same pattern.
2. **Drums fill.** Every beat (1, 2, 3, 4) where the kick or snare really hits is tapped, unless a vocal tap is within ±0.20 s.
3. **Held notes stay straight.** A sung note lasting at least one beat gets no taps inside it, drums included.
4. **Fallback.** A bar with no vocal and no drums (only the outro piano) taps the piano onsets on the 8th grid.
5. **Same music = same pattern** follows from rules 1-4: they read only the audio and the lyrics, and the copied choruses and post-choruses have identical audio.
Timing: vocals snap to the 16th grid (within 40 ms) or the triplet grid (within 25 ms), otherwise they stay on the measured onset.
Drums and piano use the real onset when it is within 20 ms of the grid. Minimum gap is 0.105 s.

Why this rule: the user's feedback on the lyric chart (2026-10-18) was "鼓点也可以有，但是你一首歌逻辑要一直", i.e. drum taps are welcome but the logic must be consistent.
I compared candidates: snare backbeats only, ±0.12 s: 506 taps, 143/297 strong beats. Every kick/snare beat, ±0.15 s: 565 taps, 2.66/s, 6 taps in 1 s.
Every kick/snare beat, ±0.2 s (chosen) gives the best balance of lyric-following and groove.

## Proof: per-section counts (music sections from the lyrics)
Notes on the columns:
* "Drum beats" are beats with a real kick/snare hit.
* "Covered by vocal" means a vocal tap is within ±0.20 s, so the beat is already a tap and no drum tap is added.
* "Deviations" counts beats where the chart differs from rule 2 re-derived from the audio. It is 0 everywhere.
* Sections with few or no drum taps (Intro, Verse 1, Pre-Chorus 2) are not exceptions: the drums there are sparse or absent (only 6-19% of backbeats have a snare), so rule 2 rarely fires.

| section | time (s) | vocal taps | drum taps | piano taps | drum beats | covered by vocal | inside held note | held notes | taps/s | deviations |
|---|---|---|---|---|---|---|---|---|---|---|
| Intro | 0.0-14.8 | 18 | 0 | 0 | 2 | 1 | 1 | 8 | 1.22 | 0 |
| Verse 1 | 14.8-29.4 | 35 | 6 | 0 | 15 | 8 | 1 | 2 | 2.81 | 0 |
| Pre-Chorus 1 | 29.4-45.0 | 42 | 6 | 0 | 30 | 24 | 0 | 0 | 3.08 | 0 |
| Chorus 1 | 45.0-59.4 | 31 | 5 | 0 | 29 | 20 | 4 | 2 | 2.50 | 0 |
| Post-Chorus 1 | 59.4-75.2 | 44 | 7 | 0 | 31 | 24 | 0 | 0 | 3.23 | 0 |
| Verse 2 | 75.2-89.5 | 34 | 7 | 0 | 30 | 22 | 1 | 2 | 2.86 | 0 |
| Pre-Chorus 2 | 89.5-105.5 | 42 | 3 | 0 | 13 | 10 | 0 | 0 | 2.83 | 0 |
| Chorus 2 | 105.5-120.0 | 32 | 5 | 0 | 30 | 20 | 5 | 2 | 2.56 | 0 |
| Post-Chorus 2 | 120.0-135.3 | 43 | 7 | 0 | 30 | 22 | 1 | 1 | 3.26 | 0 |
| Interlude | 135.3-150.7 | 18 | 17 | 0 | 31 | 14 | 0 | 1 | 2.28 | 0 |
| Bridge | 150.7-165.6 | 29 | 12 | 0 | 31 | 18 | 1 | 1 | 2.75 | 0 |
| Chorus 3 | 165.6-179.6 | 31 | 5 | 0 | 27 | 20 | 2 | 2 | 2.56 | 0 |
| Post-Chorus 3 | 179.6-197.5 | 45 | 3 | 0 | 30 | 25 | 2 | 5 | 2.69 | 0 |
| Outro (instrumental) | 197.5-212.2 | 0 | 0 | 26 | 1 | 0 | 1 | 0 | 1.76 | 0 |

Totals: 553 taps = 444 vocal + 83 drum + 26 piano. Rule-2 deviations: 0.
Piano taps (rule 4) appear only in the outro, the only bars with neither vocal nor drums.

## Stats vs targets
| | lyric chart (v2, 478) | v3 | target |
|---|---|---|---|
| vocal taps kept (same syllable) | 454 | 443/454 (98%) | >= 85% |
| strong quarter-beat accents tapped | 113/297 | 176/297 | clearly up |
| average density | 2.25/s | 2.61/s | ~2.3-2.6/s |
| busiest 1 s | 5 taps | 5 taps | <= 5 |
| min gap | 0.118 s | 0.118 s | >= 0.105 |
| held-note straights | 26 notes | 26 notes, 0 taps inside | preserved |

## Verification
* `levels-design/validate.py`: 0 errors, 0 warnings including the new FORWARD rule (progress along the map axis never decreases; every 16 s window within 34 deg of it); 0 multi-level crossings (a forward-only map cannot cross itself); min judgment window ±53 ms; 16 gaps under 0.15 s (all fast sung syllables).
* Scripted playthrough (headless Chrome, CDP touch simulation; not a real device): complete, 545/553 perfect, 8 good, diamonds 10/10. Run 1 failed at 190.03 s: a 'late' miss on the tap at 189.928 (its neighbours are 0.236 s away). Every other tap in that run was off by at most 13 ms, so this looks like a stall in the software-rendered simulation (about 11-17 fps while another job shared the machine), not a chart problem. That run's log is analysis/research/omg-v3-play-run1-fail.json. Run 2 is the result shown here.
* Layout and route: forward-only route (tools/research/route_forward.py): headings only N (forward) / E / W (lateral). Each 2-bar phrase is a staircase to one side, alternating sides, inside a ±12 m corridor (actual extent x -21..16 m over 1077 m forward); plot in analysis/research/omg-forward-route.png. Elevation falls unchanged (on the '예' taps, >= 0.35 s air). Diamonds 26.498 -> 27.662 and 83.775 -> 84.275 moved off new drum taps; no other layout changes.
* Click track `deliverables/omg-clicks-v3.mp3`: the song plus two click sounds.
  * Vocal taps: a high 2.5 kHz tick.
  * Drum taps: a low 900 Hz knock.
  * Piano fallback: 1.6 kHz.

## Lyric timing
Syllable timing is unchanged from v2 (`analysis/omg.lyrics.json`).
* Sources: Genius lyrics, the demucs vocal stem shifted by the 25.1 ms encoder delay, whisper large-v3 word prior, and calibrated onsets.
* The copied choruses are aligned jointly.
* Spot checks: `analysis/research/lyrics-check/*.png`; against whisper word starts, |d| median 28 ms.

## Annotated timeline
One row per sung syllable, drum beat and piano tap. "pos" is bar.step on the 16th grid (127.003 BPM, beat0 0.011 s).

| time (s) | pos | section | lyric / layer | tap | rule / reason |
|---|---|---|---|---|---|
| 2.614 | 1.06 | Intro | 이 [이] | TAP | 1: phrase start |
| 3.226 | 1.11 | Intro | 노래는 [노] | TAP | 1: clear syllable |
| 3.415 | 1.13 | Intro | 노래는 [래] | TAP | 1: clear syllable |
| 3.685 | 1.15 | Intro | 노래는 [는] | - | 1: fast pair, not clearly sung |
| 3.833 | 2.00~ | Intro | it's [it's] | TAP | 1: clear syllable |
| 4.608 | 2.07 | Intro | about [a] | TAP | 1: clear syllable |
| 4.700 | 2.08 | Intro | about [bout] | - | 1: within 0.105 s of a tapped syllable |
| 4.802 | 2.09~ | Intro | you [you] | TAP | 1: clear syllable |
| 5.110 | 2.11 | Intro | baby [ba] | TAP | 1: clear syllable |
| 5.278 | 2.13~ | Intro | baby [by] | TAP | 1: clear syllable |
| 7.620 | 4.00~ | Intro | Only [on] | TAP | 1: phrase start |
| 7.945 | 4.03 | Intro | Only [ly] | TAP | 1: clear syllable |
| 8.265 | 4.06 | Intro | you [you] | TAP | 1: clear syllable |
| 11.251 | 5.15 | Intro | You [you] | TAP | 1: phrase start |
| 12.050 | 6.06 | Intro | you [you] | TAP | 1: clear syllable |
| 12.552 | 6.10 | Intro | you [you] | TAP | 1: clear syllable |
| 13.051 | 6.14~ | Intro | You [you] | TAP | 1: phrase start |
| 13.762 | 7.04~ | Intro | you [you] | TAP | 1: clear syllable |
| 13.954 | 7.06 | Intro | you [you] | TAP | 1: clear syllable |
| 14.184 | 7.08 | Intro | kick/snare beat | - | 2: covered by a vocal tap |
| 14.305 | 7.09 | Intro | you [you] | TAP | 1: clear syllable |
| 14.656 | 7.12 | Intro | kick/snare beat | - | 3: inside a held note (straight) |
| 14.967 | 7.15~ | Verse 1 | 내가 [내] | TAP | 1: phrase start |
| 15.129 | 8.00 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 15.260 | 8.01 | Verse 1 | 내가 [가] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 15.605 | 8.04 | Verse 1 | 힘들 [힘] | TAP | 1: clear syllable |
| 15.875 | 8.06 | Verse 1 | 힘들 [들] | TAP | 1: clear syllable |
| 16.293 | 8.10 | Verse 1 | 때 [때] | TAP | 1: clear syllable |
| 16.757 | 8.14 | Verse 1 | 울 [울] | TAP | 1: clear syllable |
| 17.018 | 9.00 | Verse 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 17.019 | 9.00 | Verse 1 | 것 [것] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 17.283 | 9.02 | Verse 1 | 같을 [같] | TAP | 1: clear syllable |
| 17.521 | 9.04 | Verse 1 | 같을 [을] | TAP | 1: clear syllable |
| 17.747 | 9.06 | Verse 1 | 때 [때] | TAP | 1: clear syllable |
| 17.963 | 9.08 | Verse 1 | kick/snare beat | - | 3: inside a held note (straight) |
| 18.293 | 9.11 | Verse 1 | Mm-hm [mm] | TAP | 1: phrase start |
| 18.673 | 9.14 | Verse 1 | Mm-hm [hm] | TAP | 1: clear syllable |
| 18.908 | 10.00 | Verse 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 19.260 | 10.03 | Verse 1 | 기운도 [기] | TAP | 1: phrase start |
| 19.381 | 10.04 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 19.492 | 10.05 | Verse 1 | 기운도 [운] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 19.637 | 10.06 | Verse 1 | 기운도 [도] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 19.853 | 10.08 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 19.904 | 10.08~ | Verse 1 | 이젠 [이] | TAP | 1: clear syllable |
| 20.098 | 10.10 | Verse 1 | 이젠 [젠] | TAP | 1: clear syllable |
| 20.348 | 10.12 | Verse 1 | 나지 [나] | TAP | 1: clear syllable |
| 20.705 | 10.15 | Verse 1 | 나지 [지] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 20.798 | 11.00 | Verse 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 21.033 | 11.02 | Verse 1 | 않을 [않] | TAP | 1: clear syllable |
| 21.314 | 11.04~ | Verse 1 | 않을 [을] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 21.587 | 11.07 | Verse 1 | 때 [때] | TAP | 1: clear syllable |
| 21.743 | 11.08 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 21.837 | 11.09 | Verse 1 | Mm-hm [mm] | TAP | 1: phrase start |
| 22.223 | 11.12 | Verse 1 | Mm-hm [hm] | TAP | 1: clear syllable |
| 22.626 | 11.15~ | Verse 1 | It's [it's] | TAP | 1: phrase start |
| 22.688 | 12.00 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 23.262 | 12.05 | Verse 1 | you [you] | TAP | 1: clear syllable |
| 23.633 | 12.08 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 23.802 | 12.09~ | Verse 1 | 날 [날] | TAP | 1: phrase start |
| 23.898 | 12.10 | Verse 1 | 걱정하네 [걱] | - | 1: within 0.105 s of a tapped syllable |
| 24.115 | 12.12 | Verse 1 | 걱정하네 [정] | TAP | 1: clear syllable |
| 24.345 | 12.14 | Verse 1 | 걱정하네 [하] | TAP | 1: clear syllable |
| 24.577 | 13.00 | Verse 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 24.652 | 13.01~ | Verse 1 | 걱정하네 [네] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 24.873 | 13.03~ | Verse 1 | it's [it's] | TAP | 1: phrase start |
| 25.154 | 13.05 | Verse 1 | you [you] | TAP | 1: clear syllable |
| 25.590 | 13.09~ | Verse 1 | 날 [날] | TAP | 1: phrase start |
| 25.749 | 13.10 | Verse 1 | 웃게하네 [웃] | - | 1: fast pair, not clearly sung |
| 26.011 | 13.12 | Verse 1 | 웃게하네 [게] | TAP | 1: clear syllable |
| 26.347 | 13.15 | Verse 1 | 웃게하네 [하] | - | 1: too faint |
| 26.467 | 14.00 | Verse 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 26.507 | 14.00 | Verse 1 | 웃게하네 [네] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 26.748 | 14.02~ | Verse 1 | 말 [말] | TAP | 1: phrase start |
| 26.922 | 14.04 | Verse 1 | 안 [안] | TAP | 1: clear syllable |
| 27.198 | 14.06 | Verse 1 | 해도 [해] | TAP | 1: clear syllable |
| 27.392 | 14.08 | Verse 1 | 해도 [도] | TAP | 1: clear syllable |
| 27.412 | 14.08 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 27.584 | 14.09~ | Verse 1 | 돼 [돼] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 28.144 | 14.14 | Verse 1 | boy [boy] | TAP | 1: clear syllable |
| 28.357 | 15.00 | Verse 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 28.504 | 15.01 | Verse 1 | what [what] | - | 1: fast pair, not clearly sung |
| 28.666 | 15.03~ | Verse 1 | do [do] | TAP | 1: clear syllable |
| 28.829 | 15.04 | Verse 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 28.887 | 15.04~ | Verse 1 | you [you] | TAP | 1: clear syllable |
| 29.084 | 15.06 | Verse 1 | say? [say] | TAP | 1: clear syllable |
| 29.421 | 15.09 | Pre-Chorus 1 | They [they] | TAP | 1: phrase start |
| 29.530 | 15.10 | Pre-Chorus 1 | keep [keep] | - | 1: fast pair, not clearly sung |
| 29.581 | 15.10~ | Pre-Chorus 1 | on [on] | - | 1: fast pair, not clearly sung |
| 29.672 | 15.11 | Pre-Chorus 1 | asking [ask] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 29.737 | 15.12 | Pre-Chorus 1 | asking [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 29.774 | 15.12 | Pre-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 29.874 | 15.13 | Pre-Chorus 1 | me [me] | - | 1: fast pair, not clearly sung |
| 29.980 | 15.14 | Pre-Chorus 1 | who [who] | TAP | 1: clear syllable |
| 30.031 | 15.14 | Pre-Chorus 1 | is [is] | TAP | 1: clear syllable |
| 30.158 | 15.15 | Pre-Chorus 1 | he? [he] | - | 1: fast pair, not clearly sung |
| 30.247 | 16.00 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 30.327 | 16.01 | Pre-Chorus 1 | 멀리든 [멀] | TAP | 1: phrase start |
| 30.538 | 16.02~ | Pre-Chorus 1 | 멀리든 [리] | TAP | 1: clear syllable |
| 30.719 | 16.04 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 31.087 | 16.07 | Pre-Chorus 1 | 멀리든 [든] | TAP | 1: clear syllable |
| 31.191 | 16.08 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 31.557 | 16.11 | Pre-Chorus 1 | 언제든지 [언] | TAP | 1: clear syllable |
| 31.664 | 16.12 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 31.865 | 16.14 | Pre-Chorus 1 | 언제든지 [제] | TAP | 1: clear syllable |
| 32.136 | 17.00 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 32.138 | 17.00 | Pre-Chorus 1 | 언제든지 [든] | TAP | 1: clear syllable |
| 32.411 | 17.02 | Pre-Chorus 1 | 언제든지 [지] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 32.596 | 17.04 | Pre-Chorus 1 | 달려와 [달] | TAP | 1: clear syllable |
| 32.609 | 17.04 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 32.878 | 17.06 | Pre-Chorus 1 | 달려와 [려] | TAP | 1: clear syllable |
| 33.081 | 17.08 | Pre-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 33.186 | 17.09 | Pre-Chorus 1 | 달려와 [와] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 33.386 | 17.11~ | Pre-Chorus 1 | They [they] | TAP | 1: phrase start |
| 33.450 | 17.11 | Pre-Chorus 1 | keep [keep] | - | 1: within 0.105 s of a tapped syllable |
| 33.490 | 17.11~ | Pre-Chorus 1 | on [on] | - | 1: within 0.105 s of a tapped syllable |
| 33.528 | 17.12 | Pre-Chorus 1 | asking [ask] | - | 1: fast pair, not clearly sung |
| 33.554 | 17.12 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 33.653 | 17.13 | Pre-Chorus 1 | asking [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 33.812 | 17.14 | Pre-Chorus 1 | me [me] | - | 1: within 0.105 s of a tapped syllable |
| 33.870 | 17.15 | Pre-Chorus 1 | who [who] | TAP | 1: clear syllable |
| 33.972 | 18.00~ | Pre-Chorus 1 | is [is] | - | 1: within 0.105 s of a tapped syllable |
| 34.026 | 18.00 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 34.196 | 18.01~ | Pre-Chorus 1 | he? [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 34.498 | 18.04 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 34.500 | 18.04 | Pre-Chorus 1 | 바쁜 [바] | TAP | 1: phrase start |
| 34.947 | 18.08 | Pre-Chorus 1 | 바쁜 [쁜] | TAP | 1: clear syllable |
| 35.333 | 18.11 | Pre-Chorus 1 | 척도 [척] | TAP | 1: clear syllable |
| 35.443 | 18.12 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 35.528 | 18.13 | Pre-Chorus 1 | 척도 [도] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 35.699 | 18.14 | Pre-Chorus 1 | 없이 [없] | TAP | 1: clear syllable |
| 35.879 | 19.00 | Pre-Chorus 1 | 없이 [이] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 35.916 | 19.00 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 36.056 | 19.01 | Pre-Chorus 1 | 넌 [넌] | TAP | 1: clear syllable |
| 36.388 | 19.04 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 36.433 | 19.04~ | Pre-Chorus 1 | 나타나 [나] | TAP | 1: clear syllable |
| 36.645 | 19.06 | Pre-Chorus 1 | 나타나 [타] | TAP | 1: clear syllable |
| 36.854 | 19.08 | Pre-Chorus 1 | 나타나 [나] | TAP | 1: clear syllable |
| 36.861 | 19.08 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 37.133 | 19.10 | Pre-Chorus 1 | They [they] | TAP | 1: phrase start |
| 37.333 | 19.12 | Pre-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 37.383 | 19.12~ | Pre-Chorus 1 | keep [keep] | - | 1: fast pair, not clearly sung |
| 37.450 | 19.13 | Pre-Chorus 1 | on [on] | - | 1: within 0.105 s of a tapped syllable |
| 37.472 | 19.13 | Pre-Chorus 1 | asking [ask] | - | 1: within 0.105 s of a tapped syllable |
| 37.487 | 19.13 | Pre-Chorus 1 | asking [ing] | - | 1: within 0.105 s of a tapped syllable |
| 37.543 | 19.14 | Pre-Chorus 1 | me [me] | TAP | 1: clear syllable |
| 37.594 | 19.14 | Pre-Chorus 1 | who [who] | TAP | 1: clear syllable |
| 37.740 | 19.15~ | Pre-Chorus 1 | is [is] | - | 1: fast pair, not clearly sung |
| 37.805 | 20.00 | Pre-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 37.972 | 20.01~ | Pre-Chorus 1 | he? [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 38.233 | 20.04~ | Pre-Chorus 1 | 이게 [이] | TAP | 1: phrase start |
| 38.278 | 20.04 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 38.613 | 20.07 | Pre-Chorus 1 | 이게 [게] | TAP | 1: clear syllable |
| 38.712 | 20.08 | Pre-Chorus 1 | 말이 [말] | - | 1: within 0.105 s of a tapped syllable |
| 39.069 | 20.11 | Pre-Chorus 1 | 말이 [이] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 39.223 | 20.12 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 39.310 | 20.13 | Pre-Chorus 1 | 되니 [되] | TAP | 1: clear syllable |
| 39.676 | 21.00 | Pre-Chorus 1 | 되니 [니] | TAP | 1: clear syllable |
| 39.695 | 21.00 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 39.963 | 21.02 | Pre-Chorus 1 | 난 [난] | TAP | 1: clear syllable |
| 40.168 | 21.04 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 40.201 | 21.04 | Pre-Chorus 1 | 물어봐 [물] | TAP | 1: clear syllable |
| 40.474 | 21.07~ | Pre-Chorus 1 | 물어봐 [어] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 40.640 | 21.08 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 40.700 | 21.09~ | Pre-Chorus 1 | 물어봐 [봐] | TAP | 1: clear syllable |
| 41.028 | 21.11 | Pre-Chorus 1 | They [they] | TAP | 1: phrase start |
| 41.112 | 21.12 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 41.234 | 21.13 | Pre-Chorus 1 | keep [keep] | - | 1: within 0.105 s of a tapped syllable |
| 41.295 | 21.14~ | Pre-Chorus 1 | asking [ask] | - | 1: within 0.105 s of a tapped syllable |
| 41.300 | 21.14~ | Pre-Chorus 1 | asking [ing] | TAP | 1: clear syllable |
| 41.310 | 21.14 | Pre-Chorus 1 | on [on] | TAP | 1: clear syllable |
| 41.335 | 21.14 | Pre-Chorus 1 | me [me] | TAP | 1: clear syllable |
| 41.373 | 21.14 | Pre-Chorus 1 | who [who] | TAP | 1: clear syllable |
| 41.475 | 21.15 | Pre-Chorus 1 | is [is] | - | 1: within 0.105 s of a tapped syllable |
| 41.585 | 22.00 | Pre-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 41.693 | 22.01 | Pre-Chorus 1 | he? [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 42.009 | 22.04~ | Pre-Chorus 1 | 너는 [너] | TAP | 1: phrase start |
| 42.057 | 22.04 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 42.456 | 22.07~ | Pre-Chorus 1 | 너는 [는] | TAP | 1: clear syllable |
| 42.530 | 22.08 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 42.712 | 22.10~ | Pre-Chorus 1 | 말야 [말] | TAP | 1: clear syllable |
| 43.002 | 22.12 | Pre-Chorus 1 | 말야 [야] | TAP | 1: clear syllable |
| 43.002 | 22.12 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 43.260 | 22.14 | Pre-Chorus 1 | he's [he's] | TAP | 1: clear syllable |
| 43.475 | 23.00 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 43.568 | 23.01 | Pre-Chorus 1 | the [the] | TAP | 1: clear syllable |
| 43.600 | 23.01 | Pre-Chorus 1 | one [one] | TAP | 1: clear syllable |
| 43.710 | 23.02 | Pre-Chorus 1 | that's [that's] | TAP | 1: clear syllable |
| 43.920 | 23.04 | Pre-Chorus 1 | living [liv] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 43.947 | 23.04 | Pre-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 43.948 | 23.04 | Pre-Chorus 1 | living [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 44.079 | 23.05 | Pre-Chorus 1 | in [in] | - | 1: fast pair, not clearly sung |
| 44.186 | 23.06 | Pre-Chorus 1 | my [my] | TAP | 1: clear syllable |
| 44.357 | 23.07~ | Pre-Chorus 1 | system [sys] | TAP | 1: clear syllable |
| 44.537 | 23.09 | Pre-Chorus 1 | system [tem] | - | 1: within 0.105 s of a tapped syllable |
| 44.630 | 23.10 | Pre-Chorus 1 | baby [ba] | TAP | 1: clear syllable |
| 44.798 | 23.11 | Pre-Chorus 1 | baby [by] | TAP | 1: clear syllable |
| 44.892 | 23.12 | Pre-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 45.065 | 23.13~ | Chorus 1 | Oh [oh] | TAP | 1: phrase start |
| 45.364 | 24.00 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 45.388 | 24.00 | Chorus 1 | my [my] | TAP | 1: title hook |
| 45.710 | 24.03 | Chorus 1 | oh [oh] | TAP | 1: title hook |
| 45.826 | 24.04 | Chorus 1 | my [my] | TAP | 1: title hook |
| 45.837 | 24.04 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 46.078 | 24.06 | Chorus 1 | God [god] | TAP | 1: title hook |
| 46.309 | 24.08 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 46.421 | 24.09 | Chorus 1 | 예상했어 [예] | TAP | 1: clear syllable |
| 46.782 | 24.12 | Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 46.903 | 24.13 | Chorus 1 | 예상했어 [상] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 47.231 | 25.00 | Chorus 1 | 예상했어 [했] | TAP | 1: clear syllable |
| 47.254 | 25.00 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 47.379 | 25.01 | Chorus 1 | 예상했어 [어] | - | 1: fast pair, not clearly sung |
| 47.623 | 25.03 | Chorus 1 | 나 [나] | TAP | 1: clear syllable |
| 47.726 | 25.04 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 47.843 | 25.05 | Chorus 1 | I [i] | TAP | 1: phrase start |
| 48.199 | 25.08 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 48.203 | 25.08 | Chorus 1 | was [was] | TAP | 1: clear syllable |
| 48.519 | 25.11 | Chorus 1 | really [real] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 48.624 | 25.12~ | Chorus 1 | really [ly] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 48.671 | 25.12 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 48.801 | 25.13 | Chorus 1 | hoping [hop] | TAP | 1: clear syllable |
| 49.123 | 26.00 | Chorus 1 | hoping [ing] | TAP | 1: clear syllable |
| 49.144 | 26.00 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 49.408 | 26.02 | Chorus 1 | that [that] | TAP | 1: clear syllable |
| 49.616 | 26.04 | Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 49.718 | 26.05 | Chorus 1 | he [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 49.918 | 26.07~ | Chorus 1 | will [will] | TAP | 1: clear syllable |
| 50.089 | 26.08 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 50.220 | 26.09 | Chorus 1 | come [come] | TAP | 1: clear syllable |
| 50.561 | 26.12 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 50.737 | 26.13~ | Chorus 1 | through [through] | TAP | 1: clear syllable |
| 51.506 | 27.04 | Chorus 1 | kick/snare beat | - | 3: inside a held note (straight) |
| 51.978 | 27.08 | Chorus 1 | kick/snare beat | - | 3: inside a held note (straight) |
| 52.328 | 27.11 | Chorus 1 | Oh [oh] | TAP | 1: phrase start |
| 52.451 | 27.12 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 52.899 | 28.00 | Chorus 1 | my [my] | TAP | 1: title hook |
| 52.923 | 28.00 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 53.172 | 28.02 | Chorus 1 | oh [oh] | TAP | 1: title hook |
| 53.390 | 28.04 | Chorus 1 | my [my] | TAP | 1: title hook |
| 53.396 | 28.04 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 53.642 | 28.06 | Chorus 1 | God [god] | TAP | 1: title hook |
| 53.868 | 28.08 | Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 54.023 | 28.09 | Chorus 1 | 단 [단] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 54.330 | 28.12 | Chorus 1 | 너뿐이야 [너] | TAP | 1: clear syllable |
| 54.341 | 28.12 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 54.594 | 28.14 | Chorus 1 | 너뿐이야 [뿐] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 54.813 | 29.00 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 54.829 | 29.00 | Chorus 1 | 너뿐이야 [이] | TAP | 1: clear syllable |
| 55.050 | 29.02 | Chorus 1 | 너뿐이야 [야] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 55.245 | 29.04~ | Chorus 1 | Asking [ask] | TAP | 1: phrase start |
| 55.285 | 29.04 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 55.694 | 29.07~ | Chorus 1 | Asking [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 55.758 | 29.08 | Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 56.014 | 29.10 | Chorus 1 | all [all] | TAP | 1: clear syllable |
| 56.230 | 29.12 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 56.298 | 29.13~ | Chorus 1 | the [the] | TAP | 1: clear syllable |
| 56.498 | 29.14 | Chorus 1 | time [time] | TAP | 1: clear syllable |
| 56.703 | 30.00 | Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 56.826 | 30.01 | Chorus 1 | about [a] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 56.977 | 30.02 | Chorus 1 | about [bout] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 57.175 | 30.04 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 57.192 | 30.04 | Chorus 1 | what [what] | TAP | 1: clear syllable |
| 57.462 | 30.06~ | Chorus 1 | I [i] | TAP | 1: clear syllable |
| 57.648 | 30.08 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 57.796 | 30.09 | Chorus 1 | should [should] | TAP | 1: clear syllable |
| 58.120 | 30.12 | Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 58.150 | 30.12 | Chorus 1 | do [do] | TAP | 1: clear syllable |
| 58.592 | 31.00 | Chorus 1 | kick/snare beat | - | 3: inside a held note (straight) |
| 59.065 | 31.04 | Chorus 1 | kick/snare beat | - | 3: inside a held note (straight) |
| 59.465 | 31.07~ | Post-Chorus 1 | No [no] | TAP | 1: phrase start |
| 59.772 | 31.10 | Post-Chorus 1 | I [i] | TAP | 1: clear syllable |
| 60.034 | 31.12 | Post-Chorus 1 | can [can] | TAP | 1: clear syllable |
| 60.199 | 31.14~ | Post-Chorus 1 | never [nev] | TAP | 1: clear syllable |
| 60.396 | 31.15 | Post-Chorus 1 | never [er] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 60.482 | 32.00 | Post-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 60.614 | 32.01 | Post-Chorus 1 | let [let] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 60.931 | 32.04 | Post-Chorus 1 | him [him] | TAP | 1: clear syllable |
| 60.955 | 32.04 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 61.163 | 32.06 | Post-Chorus 1 | go [go] | TAP | 1: clear syllable |
| 61.395 | 32.08 | Post-Chorus 1 | 너만 [너] | TAP | 1: phrase start |
| 61.427 | 32.08 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 61.645 | 32.10 | Post-Chorus 1 | 너만 [만] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 61.899 | 32.12 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 61.926 | 32.12 | Post-Chorus 1 | 생각나 [생] | TAP | 1: clear syllable |
| 62.147 | 32.14 | Post-Chorus 1 | 생각나 [각] | TAP | 1: clear syllable |
| 62.372 | 33.00 | Post-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 62.376 | 33.00 | Post-Chorus 1 | 생각나 [나] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 62.608 | 33.02 | Post-Chorus 1 | twenty-four [twen] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 62.843 | 33.04 | Post-Chorus 1 | twenty-four [ty] | TAP | 1: clear syllable |
| 62.844 | 33.04 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 62.988 | 33.05 | Post-Chorus 1 | twenty-four [four] | - | 1: within 0.105 s of a tapped syllable |
| 63.081 | 33.06 | Post-Chorus 1 | 난 [난] | TAP | 1: phrase start |
| 63.317 | 33.08 | Post-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 63.554 | 33.10 | Post-Chorus 1 | 행운아야 [행] | TAP | 1: clear syllable |
| 63.789 | 33.12 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 63.827 | 33.12 | Post-Chorus 1 | 행운아야 [운] | TAP | 1: clear syllable |
| 64.027 | 33.14 | Post-Chorus 1 | 행운아야 [아] | TAP | 1: clear syllable |
| 64.262 | 34.00 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 64.294 | 34.00 | Post-Chorus 1 | 행운아야 [야] | TAP | 1: clear syllable |
| 64.512 | 34.02 | Post-Chorus 1 | 정말로 [정] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 64.734 | 34.04 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 64.762 | 34.04 | Post-Chorus 1 | 정말로 [말] | TAP | 1: clear syllable |
| 64.979 | 34.06 | Post-Chorus 1 | 정말로 [로] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 65.206 | 34.08 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 65.212 | 34.08 | Post-Chorus 1 | I [i] | TAP | 1: phrase start |
| 65.392 | 34.10~ | Post-Chorus 1 | know [know] | TAP | 1: clear syllable |
| 65.679 | 34.12 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 65.760 | 34.13 | Post-Chorus 1 | I [i] | TAP | 1: clear syllable |
| 65.900 | 34.14 | Post-Chorus 1 | know [know] | TAP | 1: clear syllable |
| 66.151 | 35.00 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 66.239 | 35.01 | Post-Chorus 1 | 널 [널] | TAP | 1: phrase start |
| 66.624 | 35.04 | Post-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 67.420 | 35.11 | Post-Chorus 1 | 알기 [알] | TAP | 1: clear syllable |
| 67.551 | 35.12 | Post-Chorus 1 | 알기 [기] | TAP | 1: clear syllable |
| 67.569 | 35.12 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 67.711 | 35.13 | Post-Chorus 1 | 전까지는 [전] | TAP | 1: clear syllable |
| 68.041 | 36.00 | Post-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 68.042 | 36.00 | Post-Chorus 1 | 전까지는 [까] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 68.207 | 36.01~ | Post-Chorus 1 | 전까지는 [지] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 68.378 | 36.03 | Post-Chorus 1 | 전까지는 [는] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 68.513 | 36.04 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 68.669 | 36.05 | Post-Chorus 1 | 나 [나] | TAP | 1: clear syllable |
| 68.811 | 36.07~ | Post-Chorus 1 | 의미 [의] | TAP | 1: phrase start |
| 68.986 | 36.08 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 69.150 | 36.09~ | Post-Chorus 1 | 의미 [미] | TAP | 1: clear syllable |
| 69.377 | 36.11 | Post-Chorus 1 | 없었어 [없] | TAP | 1: clear syllable |
| 69.458 | 36.12 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 69.592 | 36.13 | Post-Chorus 1 | 없었어 [었] | TAP | 1: clear syllable |
| 69.879 | 37.00~ | Post-Chorus 1 | 없었어 [어] | - | 1: fast pair, not clearly sung |
| 69.931 | 37.00 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 70.010 | 37.01 | Post-Chorus 1 | 전부 [전] | TAP | 1: clear syllable |
| 70.364 | 37.04 | Post-Chorus 1 | 전부 [부] | TAP | 1: clear syllable |
| 70.403 | 37.04 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 70.639 | 37.06 | Post-Chorus 1 | 다 [다] | TAP | 1: clear syllable |
| 70.876 | 37.08 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 70.877 | 37.08 | Post-Chorus 1 | 내 [내] | TAP | 1: phrase start |
| 71.141 | 37.10 | Post-Chorus 1 | 맘이 [맘] | TAP | 1: clear syllable |
| 71.348 | 37.12 | Post-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 71.377 | 37.12 | Post-Chorus 1 | 맘이 [이] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 71.586 | 37.14 | Post-Chorus 1 | 끝이 [끝] | TAP | 1: clear syllable |
| 71.820 | 38.00 | Post-Chorus 1 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 71.869 | 38.00~ | Post-Chorus 1 | 끝이 [이] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 72.102 | 38.02~ | Post-Chorus 1 | 없는 [없] | TAP | 1: clear syllable |
| 72.291 | 38.04 | Post-Chorus 1 | 없는 [는] | TAP | 1: clear syllable |
| 72.293 | 38.04 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 72.497 | 38.06 | Post-Chorus 1 | 걸 [걸] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 72.761 | 38.08 | Post-Chorus 1 | I [i] | TAP | 1: phrase start |
| 72.765 | 38.08 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 73.098 | 38.11 | Post-Chorus 1 | know [know] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 73.238 | 38.12 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 73.272 | 38.12 | Post-Chorus 1 | I [i] | TAP | 1: clear syllable |
| 73.597 | 38.15 | Post-Chorus 1 | know [know] | TAP | 1: clear syllable |
| 73.710 | 39.00 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 73.829 | 39.01 | Post-Chorus 1 | I'm [i'm] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 74.148 | 39.04 | Post-Chorus 1 | going [go] | TAP | 1: clear syllable |
| 74.183 | 39.04 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 74.308 | 39.05 | Post-Chorus 1 | going [ing] | - | 1: fast pair, not clearly sung |
| 74.436 | 39.06 | Post-Chorus 1 | crazy [cra] | TAP | 1: clear syllable |
| 74.653 | 39.08 | Post-Chorus 1 | crazy [zy] | TAP | 1: clear syllable |
| 74.655 | 39.08 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 74.836 | 39.10~ | Post-Chorus 1 | right? [right] | TAP | 1: clear syllable |
| 75.127 | 39.12 | Post-Chorus 1 | kick/snare beat | - | 2: covered by a vocal tap |
| 75.266 | 39.13 | Verse 2 | 어디서든 [어] | TAP | 1: phrase start |
| 75.521 | 39.15 | Verse 2 | 어디서든 [디] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 75.600 | 40.00 | Verse 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 75.759 | 40.01~ | Verse 2 | 어디서든 [서] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 75.957 | 40.03 | Verse 2 | 어디서든 [든] | TAP | 1: clear syllable |
| 76.072 | 40.04 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 76.172 | 40.05 | Verse 2 | 몇 [몇] | TAP | 1: clear syllable |
| 76.545 | 40.08 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 76.560 | 40.08 | Verse 2 | 번이든 [번] | TAP | 1: clear syllable |
| 76.691 | 40.09 | Verse 2 | 번이든 [이] | - | 1: fast pair, not clearly sung |
| 76.906 | 40.11 | Verse 2 | 번이든 [든] | TAP | 1: clear syllable |
| 77.017 | 40.12 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 77.077 | 40.13~ | Verse 2 | There [there] | TAP | 1: phrase start |
| 77.472 | 41.00 | Verse 2 | ain't [ain't] | TAP | 1: clear syllable |
| 77.490 | 41.00 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 77.634 | 41.01 | Verse 2 | nothing [noth] | - | 1: fast pair, not clearly sung |
| 77.748 | 41.02 | Verse 2 | nothing [ing] | - | 1: fast pair, not clearly sung |
| 77.855 | 41.03 | Verse 2 | else [else] | TAP | 1: clear syllable |
| 77.962 | 41.04 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 78.040 | 41.05~ | Verse 2 | that [that] | TAP | 1: clear syllable |
| 78.093 | 41.05 | Verse 2 | I [i] | TAP | 1: clear syllable |
| 78.287 | 41.07 | Verse 2 | would [would] | - | 1: fast pair, not clearly sung |
| 78.398 | 41.08 | Verse 2 | hold [hold] | TAP | 1: clear syllable |
| 78.434 | 41.08 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 78.583 | 41.09 | Verse 2 | on [on] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 78.792 | 41.11 | Verse 2 | to [to] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 78.907 | 41.12 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 79.028 | 41.13 | Verse 2 | I [i] | TAP | 1: phrase start |
| 79.379 | 42.00 | Verse 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 79.512 | 42.01 | Verse 2 | hear [hear] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 79.628 | 42.02 | Verse 2 | his [his] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 79.776 | 42.03~ | Verse 2 | voice [voice] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 79.852 | 42.04 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 80.023 | 42.05~ | Verse 2 | through [through] | TAP | 1: clear syllable |
| 80.324 | 42.08 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 80.351 | 42.08 | Verse 2 | all [all] | TAP | 1: clear syllable |
| 80.563 | 42.10 | Verse 2 | the [the] | TAP | 1: clear syllable |
| 80.720 | 42.11~ | Verse 2 | noise [noise] | TAP | 1: clear syllable |
| 80.797 | 42.12 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 80.908 | 42.13 | Verse 2 | 잠시라도 [잠] | TAP | 1: phrase start |
| 81.045 | 42.14 | Verse 2 | 잠시라도 [시] | - | 1: fast pair, not clearly sung |
| 81.269 | 43.00 | Verse 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 81.271 | 43.00 | Verse 2 | 잠시라도 [라] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 81.448 | 43.02~ | Verse 2 | 잠시라도 [도] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 81.579 | 43.03~ | Verse 2 | 내 [내] | - | 1: fast pair, not clearly sung |
| 81.738 | 43.04 | Verse 2 | 손 [손] | TAP | 1: clear syllable |
| 81.741 | 43.04 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 81.898 | 43.05 | Verse 2 | 놓지 [놓] | - | 1: fast pair, not clearly sung |
| 82.072 | 43.07 | Verse 2 | 놓지 [지] | TAP | 1: clear syllable |
| 82.167 | 43.08~ | Verse 2 | 마 [마] | - | 1: within 0.105 s of a tapped syllable |
| 82.214 | 43.08 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 82.299 | 43.09 | Verse 2 | no [no] | - | 1: fast pair, not clearly sung |
| 82.452 | 43.10 | Verse 2 | no [no] | TAP | 1: clear syllable |
| 82.686 | 43.12 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 82.711 | 43.12 | Verse 2 | 걱정 [걱] | TAP | 1: phrase start |
| 82.853 | 43.13~ | Verse 2 | 걱정 [정] | - | 1: fast pair, not clearly sung |
| 83.159 | 44.00 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 83.161 | 44.00 | Verse 2 | 없잖아 [없] | TAP | 1: clear syllable |
| 83.326 | 44.01~ | Verse 2 | 없잖아 [잖] | - | 1: fast pair, not clearly sung |
| 83.631 | 44.04 | Verse 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 83.747 | 44.05 | Verse 2 | 없잖아 [아] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 84.049 | 44.08~ | Verse 2 | 'Cause [cause] | TAP | 1: phrase start |
| 84.104 | 44.08 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 84.576 | 44.12 | Verse 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 84.641 | 44.13~ | Verse 2 | I [i] | - | 1: fast pair, not clearly sung |
| 84.809 | 44.14 | Verse 2 | got [got] | TAP | 1: clear syllable |
| 85.033 | 45.00 | Verse 2 | someone [some] | TAP | 1: clear syllable |
| 85.048 | 45.00 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 85.314 | 45.02 | Verse 2 | someone [one] | TAP | 1: clear syllable |
| 85.521 | 45.04 | Verse 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 85.993 | 45.08 | Verse 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 86.464 | 45.12 | Verse 2 | 혼자라도 [혼] | TAP | 1: phrase start |
| 86.466 | 45.12 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 86.568 | 45.13 | Verse 2 | 혼자라도 [자] | - | 1: within 0.105 s of a tapped syllable |
| 86.705 | 45.14 | Verse 2 | 혼자라도 [라] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 86.937 | 46.00 | Verse 2 | 혼자라도 [도] | TAP | 1: clear syllable |
| 86.938 | 46.00 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 87.105 | 46.01~ | Verse 2 | 괜찮아 [괜] | - | 1: fast pair, not clearly sung |
| 87.245 | 46.03~ | Verse 2 | 괜찮아 [찮] | - | 1: fast pair, not clearly sung |
| 87.387 | 46.04 | Verse 2 | 괜찮아 [아] | TAP | 1: clear syllable |
| 87.411 | 46.04 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 87.575 | 46.05~ | Verse 2 | 'Cause [cause] | TAP | 1: phrase start |
| 87.883 | 46.08 | Verse 2 | kick/snare beat | - | 3: inside a held note (straight) |
| 88.356 | 46.12 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 88.394 | 46.12 | Verse 2 | I [i] | TAP | 1: clear syllable |
| 88.583 | 46.14 | Verse 2 | love [love] | TAP | 1: clear syllable |
| 88.828 | 47.00 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 88.940 | 47.01 | Verse 2 | someone [some] | TAP | 1: clear syllable |
| 89.300 | 47.04 | Verse 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 89.302 | 47.04 | Verse 2 | someone [one] | TAP | 1: clear syllable |
| 89.540 | 47.06 | Pre-Chorus 2 | They [they] | TAP | 1: phrase start |
| 90.002 | 47.10 | Pre-Chorus 2 | keep [keep] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 90.135 | 47.11 | Pre-Chorus 2 | on [on] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 90.246 | 47.12 | Pre-Chorus 2 | asking [ask] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 90.300 | 47.12~ | Pre-Chorus 2 | asking [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 90.394 | 47.13 | Pre-Chorus 2 | me [me] | - | 1: fast pair, not clearly sung |
| 90.545 | 47.15~ | Pre-Chorus 2 | who [who] | TAP | 1: clear syllable |
| 90.646 | 47.15~ | Pre-Chorus 2 | is [is] | - | 1: within 0.105 s of a tapped syllable |
| 90.718 | 48.00 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 90.809 | 48.01 | Pre-Chorus 2 | he? [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 91.061 | 48.03 | Pre-Chorus 2 | 멀리든 [멀] | TAP | 1: phrase start |
| 91.563 | 48.07 | Pre-Chorus 2 | 멀리든 [리] | TAP | 1: clear syllable |
| 91.903 | 48.10 | Pre-Chorus 2 | 멀리든 [든] | TAP | 1: clear syllable |
| 92.196 | 48.13~ | Pre-Chorus 2 | 언제든지 [언] | TAP | 1: clear syllable |
| 92.420 | 48.14~ | Pre-Chorus 2 | 언제든지 [제] | TAP | 1: clear syllable |
| 92.607 | 49.00 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 92.617 | 49.00 | Pre-Chorus 2 | 언제든지 [든] | TAP | 1: clear syllable |
| 92.881 | 49.02 | Pre-Chorus 2 | 언제든지 [지] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 93.080 | 49.04 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 93.119 | 49.04 | Pre-Chorus 2 | 달려와 [달] | TAP | 1: clear syllable |
| 93.317 | 49.06 | Pre-Chorus 2 | 달려와 [려] | TAP | 1: clear syllable |
| 93.549 | 49.08 | Pre-Chorus 2 | 달려와 [와] | - | 1: fast pair, not clearly sung |
| 93.682 | 49.09 | Pre-Chorus 2 | They [they] | TAP | 1: phrase start |
| 93.810 | 49.10 | Pre-Chorus 2 | keep [keep] | - | 1: fast pair, not clearly sung |
| 93.909 | 49.11 | Pre-Chorus 2 | on [on] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 94.045 | 49.12 | Pre-Chorus 2 | asking [ask] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 94.138 | 49.13 | Pre-Chorus 2 | asking [ing] | - | 1: within 0.105 s of a tapped syllable |
| 94.222 | 49.14 | Pre-Chorus 2 | me [me] | TAP | 1: clear syllable |
| 94.286 | 49.14 | Pre-Chorus 2 | who [who] | TAP | 1: clear syllable |
| 94.497 | 50.00 | Pre-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 94.498 | 50.00 | Pre-Chorus 2 | is [is] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 94.640 | 50.01 | Pre-Chorus 2 | he? [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 94.970 | 50.04 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 95.046 | 50.05~ | Pre-Chorus 2 | 바쁜 [바] | TAP | 1: phrase start |
| 95.424 | 50.08 | Pre-Chorus 2 | 바쁜 [쁜] | TAP | 1: clear syllable |
| 95.442 | 50.08 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 95.807 | 50.11 | Pre-Chorus 2 | 척도 [척] | TAP | 1: clear syllable |
| 95.914 | 50.12 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 95.917 | 50.12 | Pre-Chorus 2 | 척도 [도] | - | 1: fast pair, not clearly sung |
| 96.152 | 50.14 | Pre-Chorus 2 | 없이 [없] | TAP | 1: clear syllable |
| 96.344 | 51.00~ | Pre-Chorus 2 | 없이 [이] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 96.387 | 51.00 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 96.532 | 51.01 | Pre-Chorus 2 | 넌 [넌] | TAP | 1: clear syllable |
| 96.863 | 51.04 | Pre-Chorus 2 | 나타나 [나] | TAP | 1: clear syllable |
| 97.096 | 51.06 | Pre-Chorus 2 | 나타나 [타] | TAP | 1: clear syllable |
| 97.455 | 51.09 | Pre-Chorus 2 | 나타나 [나] | TAP | 1: clear syllable |
| 97.691 | 51.11 | Pre-Chorus 2 | They [they] | TAP | 1: phrase start |
| 97.798 | 51.12 | Pre-Chorus 2 | keep [keep] | - | 1: fast pair, not clearly sung |
| 97.935 | 51.13 | Pre-Chorus 2 | on [on] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 97.961 | 51.13 | Pre-Chorus 2 | asking [ask] | - | 1: fast pair, not clearly sung |
| 97.990 | 51.14~ | Pre-Chorus 2 | asking [ing] | - | 1: fast pair, not clearly sung |
| 98.025 | 51.14 | Pre-Chorus 2 | me [me] | - | 1: within 0.105 s of a tapped syllable |
| 98.123 | 51.15 | Pre-Chorus 2 | who [who] | TAP | 1: clear syllable |
| 98.254 | 52.00 | Pre-Chorus 2 | is [is] | - | 1: fast pair, not clearly sung |
| 98.277 | 52.00 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 98.364 | 52.01 | Pre-Chorus 2 | he? [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 98.749 | 52.04 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 98.767 | 52.04 | Pre-Chorus 2 | 이게 [이] | TAP | 1: phrase start |
| 99.188 | 52.08 | Pre-Chorus 2 | 이게 [게] | TAP | 1: clear syllable |
| 99.360 | 52.09 | Pre-Chorus 2 | 말이 [말] | TAP | 1: clear syllable |
| 99.516 | 52.10~ | Pre-Chorus 2 | 말이 [이] | - | 1: fast pair, not clearly sung |
| 99.763 | 52.13~ | Pre-Chorus 2 | 되니 [되] | TAP | 1: clear syllable |
| 100.027 | 52.15 | Pre-Chorus 2 | 되니 [니] | TAP | 1: clear syllable |
| 100.338 | 53.01~ | Pre-Chorus 2 | 난 [난] | TAP | 1: clear syllable |
| 100.651 | 53.04 | Pre-Chorus 2 | 물어봐 [물] | TAP | 1: clear syllable |
| 100.912 | 53.06 | Pre-Chorus 2 | 물어봐 [어] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 101.118 | 53.08 | Pre-Chorus 2 | 물어봐 [봐] | TAP | 1: clear syllable |
| 101.377 | 53.10 | Pre-Chorus 2 | They [they] | TAP | 1: phrase start |
| 101.592 | 53.12 | Pre-Chorus 2 | keep [keep] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 101.700 | 53.13 | Pre-Chorus 2 | on [on] | - | 1: fast pair, not clearly sung |
| 101.725 | 53.13 | Pre-Chorus 2 | asking [ask] | - | 1: fast pair, not clearly sung |
| 101.742 | 53.13~ | Pre-Chorus 2 | asking [ing] | - | 1: within 0.105 s of a tapped syllable |
| 101.757 | 53.13~ | Pre-Chorus 2 | me [me] | - | 1: within 0.105 s of a tapped syllable |
| 101.844 | 53.14 | Pre-Chorus 2 | who [who] | TAP | 1: clear syllable |
| 102.004 | 54.00~ | Pre-Chorus 2 | is [is] | - | 1: fast pair, not clearly sung |
| 102.056 | 54.00 | Pre-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 102.120 | 54.01~ | Pre-Chorus 2 | he? [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 102.497 | 54.04 | Pre-Chorus 2 | 너는 [너] | TAP | 1: phrase start |
| 102.991 | 54.08 | Pre-Chorus 2 | 너는 [는] | TAP | 1: clear syllable |
| 103.001 | 54.08 | Pre-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 103.321 | 54.11 | Pre-Chorus 2 | 말야 [말] | TAP | 1: clear syllable |
| 103.467 | 54.12 | Pre-Chorus 2 | 말야 [야] | TAP | 1: clear syllable |
| 103.710 | 54.14 | Pre-Chorus 2 | he's [he's] | TAP | 1: clear syllable |
| 103.908 | 55.00 | Pre-Chorus 2 | the [the] | TAP | 1: clear syllable |
| 104.082 | 55.01 | Pre-Chorus 2 | one [one] | TAP | 1: clear syllable |
| 104.183 | 55.02 | Pre-Chorus 2 | that's [that's] | - | 1: within 0.105 s of a tapped syllable |
| 104.308 | 55.03 | Pre-Chorus 2 | living [liv] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 104.418 | 55.04 | Pre-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 104.430 | 55.04 | Pre-Chorus 2 | living [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 104.471 | 55.04~ | Pre-Chorus 2 | in [in] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 104.657 | 55.06 | Pre-Chorus 2 | my [my] | TAP | 1: clear syllable |
| 104.781 | 55.07 | Pre-Chorus 2 | system [sys] | TAP | 1: clear syllable |
| 104.932 | 55.08~ | Pre-Chorus 2 | system [tem] | - | 1: fast pair, not clearly sung |
| 105.127 | 55.10 | Pre-Chorus 2 | baby [ba] | TAP | 1: clear syllable |
| 105.371 | 55.12 | Pre-Chorus 2 | baby [by] | TAP | 1: clear syllable |
| 105.538 | 55.13~ | Chorus 2 | Oh [oh] | TAP | 1: phrase start |
| 105.835 | 56.00 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 105.860 | 56.00 | Chorus 2 | my [my] | TAP | 1: title hook |
| 106.182 | 56.03 | Chorus 2 | oh [oh] | TAP | 1: title hook |
| 106.298 | 56.04 | Chorus 2 | my [my] | TAP | 1: title hook |
| 106.308 | 56.04 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 106.551 | 56.06 | Chorus 2 | God [god] | TAP | 1: title hook |
| 106.780 | 56.08 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 106.893 | 56.09 | Chorus 2 | 예상했어 [예] | TAP | 1: copied vocal = same pattern |
| 107.253 | 56.12 | Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 107.375 | 56.13 | Chorus 2 | 예상했어 [상] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 107.703 | 57.00 | Chorus 2 | 예상했어 [했] | TAP | 1: copied vocal = same pattern |
| 107.725 | 57.00 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 107.851 | 57.01 | Chorus 2 | 예상했어 [어] | - | 1: fast pair, not clearly sung |
| 108.095 | 57.03 | Chorus 2 | 나 [나] | TAP | 1: copied vocal = same pattern |
| 108.198 | 57.04 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 108.316 | 57.05 | Chorus 2 | I [i] | TAP | 1: phrase start |
| 108.670 | 57.08 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 108.676 | 57.08 | Chorus 2 | was [was] | TAP | 1: copied vocal = same pattern |
| 108.992 | 57.11 | Chorus 2 | really [real] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 109.096 | 57.12~ | Chorus 2 | really [ly] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 109.142 | 57.12 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 109.273 | 57.13 | Chorus 2 | hoping [hop] | TAP | 1: copied vocal = same pattern |
| 109.596 | 58.00 | Chorus 2 | hoping [ing] | TAP | 1: copied vocal = same pattern |
| 109.615 | 58.00 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 109.880 | 58.02 | Chorus 2 | that [that] | TAP | 1: copied vocal = same pattern |
| 110.087 | 58.04 | Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 110.191 | 58.05 | Chorus 2 | he [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 110.391 | 58.07~ | Chorus 2 | will [will] | TAP | 1: copied vocal = same pattern |
| 110.560 | 58.08 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 110.693 | 58.09 | Chorus 2 | come [come] | TAP | 1: copied vocal = same pattern |
| 111.032 | 58.12 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 111.209 | 58.13~ | Chorus 2 | through [through] | TAP | 1: copied vocal = same pattern |
| 111.505 | 59.00 | Chorus 2 | kick/snare beat | - | 3: inside a held note (straight) |
| 111.977 | 59.04 | Chorus 2 | kick/snare beat | - | 3: inside a held note (straight) |
| 112.449 | 59.08 | Chorus 2 | kick/snare beat | - | 3: inside a held note (straight) |
| 112.800 | 59.11 | Chorus 2 | Oh [oh] | TAP | 1: phrase start |
| 112.922 | 59.12 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 113.372 | 60.00 | Chorus 2 | my [my] | TAP | 1: title hook |
| 113.394 | 60.00 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 113.645 | 60.02 | Chorus 2 | oh [oh] | TAP | 1: title hook |
| 113.862 | 60.04 | Chorus 2 | my [my] | TAP | 1: title hook |
| 113.867 | 60.04 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 114.115 | 60.06 | Chorus 2 | God [god] | TAP | 1: title hook |
| 114.339 | 60.08 | Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 114.495 | 60.09 | Chorus 2 | 단 [단] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 114.803 | 60.12 | Chorus 2 | 너뿐이야 [너] | TAP | 1: copied vocal = same pattern |
| 114.812 | 60.12 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 115.067 | 60.14 | Chorus 2 | 너뿐이야 [뿐] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 115.284 | 61.00 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 115.302 | 61.00 | Chorus 2 | 너뿐이야 [이] | TAP | 1: copied vocal = same pattern |
| 115.523 | 61.02 | Chorus 2 | 너뿐이야 [야] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 115.717 | 61.04 | Chorus 2 | Asking [ask] | TAP | 1: phrase start |
| 115.756 | 61.04 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 116.167 | 61.07~ | Chorus 2 | Asking [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 116.229 | 61.08 | Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 116.486 | 61.10 | Chorus 2 | all [all] | TAP | 1: copied vocal = same pattern |
| 116.701 | 61.12 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 116.771 | 61.13~ | Chorus 2 | the [the] | TAP | 1: copied vocal = same pattern |
| 116.971 | 61.14 | Chorus 2 | time [time] | TAP | 1: copied vocal = same pattern |
| 117.174 | 62.00 | Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 117.299 | 62.01 | Chorus 2 | about [a] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 117.450 | 62.02~ | Chorus 2 | about [bout] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 117.646 | 62.04 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 117.665 | 62.04 | Chorus 2 | what [what] | TAP | 1: copied vocal = same pattern |
| 117.935 | 62.06~ | Chorus 2 | I [i] | TAP | 1: copied vocal = same pattern |
| 118.119 | 62.08 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 118.268 | 62.09 | Chorus 2 | should [should] | TAP | 1: copied vocal = same pattern |
| 118.591 | 62.12 | Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 118.622 | 62.12 | Chorus 2 | do [do] | TAP | 1: copied vocal = same pattern |
| 119.063 | 63.00 | Chorus 2 | kick/snare beat | - | 3: inside a held note (straight) |
| 119.536 | 63.04 | Chorus 2 | kick/snare beat | - | 3: inside a held note (straight) |
| 119.937 | 63.07~ | Post-Chorus 2 | No [no] | TAP | 1: phrase start |
| 120.245 | 63.10 | Post-Chorus 2 | I [i] | TAP | 1: copied vocal = same pattern |
| 120.506 | 63.12 | Post-Chorus 2 | can [can] | TAP | 1: copied vocal = same pattern |
| 120.672 | 63.14~ | Post-Chorus 2 | never [nev] | TAP | 1: copied vocal = same pattern |
| 120.869 | 63.15 | Post-Chorus 2 | never [er] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 120.953 | 64.00 | Post-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 121.087 | 64.01 | Post-Chorus 2 | let [let] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 121.403 | 64.04 | Post-Chorus 2 | him [him] | TAP | 1: copied vocal = same pattern |
| 121.426 | 64.04 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 121.635 | 64.06 | Post-Chorus 2 | go [go] | TAP | 1: copied vocal = same pattern |
| 121.867 | 64.08 | Post-Chorus 2 | 너만 [너] | TAP | 1: phrase start |
| 121.898 | 64.08 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 122.117 | 64.10 | Post-Chorus 2 | 너만 [만] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 122.370 | 64.12 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 122.399 | 64.12 | Post-Chorus 2 | 생각나 [생] | TAP | 1: copied vocal = same pattern |
| 122.619 | 64.14 | Post-Chorus 2 | 생각나 [각] | TAP | 1: copied vocal = same pattern |
| 122.843 | 65.00 | Post-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 122.848 | 65.00 | Post-Chorus 2 | 생각나 [나] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 123.081 | 65.02 | Post-Chorus 2 | twenty-four [twen] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 123.315 | 65.04 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 123.316 | 65.04 | Post-Chorus 2 | twenty-four [ty] | TAP | 1: copied vocal = same pattern |
| 123.461 | 65.05 | Post-Chorus 2 | twenty-four [four] | - | 1: within 0.105 s of a tapped syllable |
| 123.554 | 65.06 | Post-Chorus 2 | 난 [난] | TAP | 1: phrase start |
| 123.788 | 65.08 | Post-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 124.027 | 65.10 | Post-Chorus 2 | 행운아야 [행] | TAP | 1: copied vocal = same pattern |
| 124.260 | 65.12 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 124.300 | 65.12 | Post-Chorus 2 | 행운아야 [운] | TAP | 1: copied vocal = same pattern |
| 124.500 | 65.14 | Post-Chorus 2 | 행운아야 [아] | TAP | 1: copied vocal = same pattern |
| 124.733 | 66.00 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 124.767 | 66.00 | Post-Chorus 2 | 행운아야 [야] | TAP | 1: copied vocal = same pattern |
| 124.985 | 66.02 | Post-Chorus 2 | 정말로 [정] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 125.205 | 66.04 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 125.234 | 66.04 | Post-Chorus 2 | 정말로 [말] | TAP | 1: copied vocal = same pattern |
| 125.452 | 66.06 | Post-Chorus 2 | 정말로 [로] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 125.678 | 66.08 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 125.684 | 66.08 | Post-Chorus 2 | I [i] | TAP | 1: phrase start |
| 125.864 | 66.10~ | Post-Chorus 2 | know [know] | TAP | 1: copied vocal = same pattern |
| 126.150 | 66.12 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 126.233 | 66.13 | Post-Chorus 2 | I [i] | TAP | 1: copied vocal = same pattern |
| 126.372 | 66.14 | Post-Chorus 2 | know [know] | TAP | 1: copied vocal = same pattern |
| 126.622 | 67.00 | Post-Chorus 2 | kick/snare beat | - | 3: inside a held note (straight) |
| 127.095 | 67.04 | Post-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 127.520 | 67.08~ | Post-Chorus 2 | 널 [널] | TAP | 1: phrase start |
| 127.868 | 67.11~ | Post-Chorus 2 | 알기 [알] | TAP | 1: clear syllable |
| 128.022 | 67.12 | Post-Chorus 2 | 알기 [기] | TAP | 1: clear syllable |
| 128.040 | 67.12 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 128.178 | 67.13 | Post-Chorus 2 | 전까지는 [전] | TAP | 1: clear syllable |
| 128.297 | 67.14 | Post-Chorus 2 | 전까지는 [까] | - | 1: fast pair, not clearly sung |
| 128.512 | 68.00 | Post-Chorus 2 | 전까지는 [지] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 128.512 | 68.00 | Post-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 128.701 | 68.02~ | Post-Chorus 2 | 전까지는 [는] | - | 1: fast pair, not clearly sung |
| 128.849 | 68.03 | Post-Chorus 2 | 나 [나] | TAP | 1: clear syllable |
| 128.985 | 68.04 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 129.283 | 68.07~ | Post-Chorus 2 | 의미 [의] | TAP | 1: phrase start |
| 129.457 | 68.08 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 129.623 | 68.09~ | Post-Chorus 2 | 의미 [미] | TAP | 1: copied vocal = same pattern |
| 129.849 | 68.11 | Post-Chorus 2 | 없었어 [없] | TAP | 1: copied vocal = same pattern |
| 129.929 | 68.12 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 130.064 | 68.13 | Post-Chorus 2 | 없었어 [었] | TAP | 1: copied vocal = same pattern |
| 130.351 | 69.00~ | Post-Chorus 2 | 없었어 [어] | - | 1: fast pair, not clearly sung |
| 130.402 | 69.00 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 130.482 | 69.01 | Post-Chorus 2 | 전부 [전] | TAP | 1: copied vocal = same pattern |
| 130.836 | 69.04 | Post-Chorus 2 | 전부 [부] | TAP | 1: copied vocal = same pattern |
| 130.874 | 69.04 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 131.112 | 69.06 | Post-Chorus 2 | 다 [다] | TAP | 1: copied vocal = same pattern |
| 131.347 | 69.08 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 131.350 | 69.08 | Post-Chorus 2 | 내 [내] | TAP | 1: phrase start |
| 131.614 | 69.10 | Post-Chorus 2 | 맘이 [맘] | TAP | 1: copied vocal = same pattern |
| 131.819 | 69.12 | Post-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 131.849 | 69.12 | Post-Chorus 2 | 맘이 [이] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 132.058 | 69.14 | Post-Chorus 2 | 끝이 [끝] | TAP | 1: copied vocal = same pattern |
| 132.292 | 70.00 | Post-Chorus 2 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 132.341 | 70.00~ | Post-Chorus 2 | 끝이 [이] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 132.575 | 70.02~ | Post-Chorus 2 | 없는 [없] | TAP | 1: copied vocal = same pattern |
| 132.763 | 70.04 | Post-Chorus 2 | 없는 [는] | TAP | 1: copied vocal = same pattern |
| 132.764 | 70.04 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 132.969 | 70.06 | Post-Chorus 2 | 걸 [걸] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 133.235 | 70.08 | Post-Chorus 2 | I [i] | TAP | 1: phrase start |
| 133.236 | 70.08 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 133.606 | 70.11 | Post-Chorus 2 | know [know] | TAP | 1: clear syllable |
| 133.709 | 70.12 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 133.841 | 70.13 | Post-Chorus 2 | I [i] | TAP | 1: clear syllable |
| 133.949 | 70.14 | Post-Chorus 2 | know [know] | TAP | 1: clear syllable |
| 134.181 | 71.00 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 134.279 | 71.01 | Post-Chorus 2 | He's [he's] | TAP | 1: phrase start |
| 134.430 | 71.02 | Post-Chorus 2 | the [the] | - | 1: fast pair, not clearly sung |
| 134.577 | 71.03~ | Post-Chorus 2 | one [one] | - | 1: within 0.105 s of a tapped syllable |
| 134.654 | 71.04 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 134.680 | 71.04 | Post-Chorus 2 | that's [that's] | TAP | 1: clear syllable |
| 134.723 | 71.05~ | Post-Chorus 2 | living [liv] | - | 1: within 0.105 s of a tapped syllable |
| 134.793 | 71.05 | Post-Chorus 2 | living [ing] | - | 1: fast pair, not clearly sung |
| 134.895 | 71.06 | Post-Chorus 2 | in [in] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 134.999 | 71.07 | Post-Chorus 2 | my [my] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 135.092 | 71.08 | Post-Chorus 2 | system [sys] | - | 1: fast pair, not clearly sung |
| 135.126 | 71.08 | Post-Chorus 2 | kick/snare beat | - | 2: covered by a vocal tap |
| 135.214 | 71.09 | Post-Chorus 2 | system [tem] | TAP | 1: clear syllable |
| 135.284 | 71.09 | Interlude | Baby [ba] | TAP | 1: phrase start |
| 135.705 | 71.13 | Interlude | Baby [by] | TAP | 1: title hook |
| 135.986 | 71.15 | Interlude | babe [babe] | TAP | 1: title hook |
| 136.071 | 72.00 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 136.395 | 72.03 | Interlude | baby [ba] | TAP | 1: title hook |
| 136.543 | 72.04 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 137.016 | 72.08 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 137.488 | 72.12 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 137.500 | 72.12 | Interlude | baby [by] | TAP | 1: title hook |
| 137.961 | 73.00 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 138.282 | 73.03 | Interlude | baby [ba] | TAP | 1: title hook |
| 138.433 | 73.04 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 138.906 | 73.08 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 138.987 | 73.09 | Interlude | baby [by] | TAP | 1: title hook |
| 139.378 | 73.12 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 139.850 | 74.00 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 140.323 | 74.04 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 140.795 | 74.08 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 141.268 | 74.12 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 141.480 | 74.14 | Interlude | I'm [i'm] | TAP | 1: phrase start |
| 141.740 | 75.00 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 142.168 | 75.04~ | Interlude | going [go] | TAP | 1: clear syllable |
| 142.213 | 75.04 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 142.343 | 75.05 | Interlude | going [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 142.569 | 75.07 | Interlude | crazy [cra] | TAP | 1: title hook |
| 142.685 | 75.08 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 142.743 | 75.08~ | Interlude | crazy [zy] | TAP | 1: title hook |
| 142.911 | 75.10 | Interlude | right? [right] | - | 1: fast pair, not clearly sung |
| 143.157 | 75.12 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 143.277 | 75.13 | Interlude | Baby [ba] | TAP | 1: phrase start |
| 143.630 | 76.00 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 143.684 | 76.00~ | Interlude | Baby [by] | TAP | 1: title hook |
| 143.953 | 76.03 | Interlude | baby [ba] | TAP | 1: title hook |
| 144.102 | 76.04 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 144.575 | 76.08 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 144.850 | 76.10 | Interlude | baby [by] | TAP | 1: title hook |
| 145.047 | 76.12 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 145.520 | 77.00 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 145.762 | 77.02 | Interlude | babe [babe] | - | 1: too faint |
| 145.976 | 77.04 | Interlude | baby [ba] | TAP | 1: title hook |
| 145.992 | 77.04 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 146.072 | 77.05 | Interlude | baby [by] | - | 1: within 0.105 s of a tapped syllable |
| 146.464 | 77.08 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 146.937 | 77.12 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 147.409 | 78.00 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 147.882 | 78.04 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 148.354 | 78.08 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 148.827 | 78.12 | Interlude | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 149.299 | 79.00 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 149.442 | 79.01 | Interlude | 너와 [너] | TAP | 1: phrase start |
| 149.738 | 79.04 | Interlude | 너와 [와] | TAP | 1: clear syllable |
| 149.771 | 79.04 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 150.136 | 79.07 | Interlude | 나 [나] | TAP | 1: clear syllable |
| 150.244 | 79.08 | Interlude | kick/snare beat | - | 2: covered by a vocal tap |
| 150.728 | 79.12 | Bridge | My [my] | TAP | 1: phrase start |
| 150.960 | 79.14 | Bridge | heart [heart] | TAP | 1: clear syllable |
| 151.189 | 80.00 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 151.390 | 80.02 | Bridge | is [is] | - | 1: fast pair, not clearly sung |
| 151.517 | 80.03 | Bridge | glowing [glow] | TAP | 1: clear syllable |
| 151.661 | 80.04 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 151.796 | 80.05 | Bridge | glowing [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 152.054 | 80.07 | Bridge | it's [it's] | - | 1: fast pair, not clearly sung |
| 152.134 | 80.08 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 152.162 | 80.08 | Bridge | glowing [glow] | TAP | 1: clear syllable |
| 152.437 | 80.11~ | Bridge | glowing [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 152.606 | 80.12 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 152.745 | 80.13 | Bridge | up [up] | TAP | 1: clear syllable |
| 153.078 | 81.00 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 153.433 | 81.03 | Bridge | Glow [glow] | TAP | 1: phrase start |
| 153.551 | 81.04 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 153.800 | 81.06 | Bridge | glow [glow] | TAP | 1: clear syllable |
| 154.023 | 81.08 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 154.362 | 81.11 | Bridge | 너랑만 [너] | TAP | 1: phrase start |
| 154.496 | 81.12 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 154.736 | 81.14 | Bridge | 너랑만 [랑] | TAP | 1: clear syllable |
| 154.968 | 82.00 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 155.012 | 82.00~ | Bridge | 너랑만 [만] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 155.241 | 82.02 | Bridge | 있으면 [있] | TAP | 1: clear syllable |
| 155.441 | 82.04 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 155.447 | 82.04 | Bridge | 있으면 [으] | TAP | 1: clear syllable |
| 155.552 | 82.05 | Bridge | 있으면 [면] | - | 1: within 0.105 s of a tapped syllable |
| 155.680 | 82.06 | Bridge | 무서울 [무] | TAP | 1: clear syllable |
| 155.913 | 82.08 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 156.019 | 82.09 | Bridge | 무서울 [서] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 156.385 | 82.12 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 156.388 | 82.12 | Bridge | 무서울 [울] | TAP | 1: clear syllable |
| 156.634 | 82.14 | Bridge | 게 [게] | TAP | 1: clear syllable |
| 156.858 | 83.00 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 156.896 | 83.00 | Bridge | 없어 [없] | TAP | 1: clear syllable |
| 157.224 | 83.03 | Bridge | 없어 [어] | - | 1: too faint |
| 157.330 | 83.04 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 157.613 | 83.06~ | Bridge | No [no] | TAP | 1: phrase start |
| 157.740 | 83.07~ | Bridge | no [no] | - | 1: fast pair, not clearly sung |
| 157.803 | 83.08 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 158.199 | 83.11~ | Bridge | 가득 [가] | TAP | 1: phrase start |
| 158.275 | 83.12 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 158.524 | 83.14 | Bridge | 가득 [득] | TAP | 1: clear syllable |
| 158.748 | 84.00 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 158.875 | 84.01 | Bridge | 메워진 [메] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 159.220 | 84.04 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 159.223 | 84.04 | Bridge | 메워진 [워] | TAP | 1: clear syllable |
| 159.459 | 84.06 | Bridge | 메워진 [진] | TAP | 1: clear syllable |
| 159.693 | 84.08 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 159.694 | 84.08 | Bridge | 다 [다] | TAP | 1: clear syllable |
| 159.827 | 84.09 | Bridge | 메워진 [메] | - | 1: fast pair, not clearly sung |
| 160.056 | 84.11 | Bridge | 메워진 [워] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 160.165 | 84.12 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 160.451 | 84.14~ | Bridge | 메워진 [진] | TAP | 1: clear syllable |
| 160.637 | 85.00 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 160.710 | 85.01~ | Bridge | My [my] | TAP | 1: phrase start |
| 161.110 | 85.04 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 161.582 | 85.08 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 161.728 | 85.09 | Bridge | heart [heart] | TAP | 1: clear syllable |
| 162.055 | 85.12 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 162.527 | 86.00 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 162.631 | 86.01 | Bridge | is [is] | TAP | 1: clear syllable |
| 162.823 | 86.03~ | Bridge | glowing [glow] | TAP | 1: clear syllable |
| 163.000 | 86.04 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 163.078 | 86.05 | Bridge | glowing [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 163.386 | 86.07 | Bridge | it'd [it'd] | - | 1: fast pair, not clearly sung |
| 163.472 | 86.08 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 163.505 | 86.08 | Bridge | be [be] | TAP | 1: clear syllable |
| 163.711 | 86.10 | Bridge | glowing [glow] | TAP | 1: clear syllable |
| 163.944 | 86.12 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 164.010 | 86.13~ | Bridge | glowing [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 164.381 | 87.00 | Bridge | 'Cause [cause] | - | 1: too faint |
| 164.417 | 87.00 | Bridge | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 164.889 | 87.04 | Bridge | kick/snare beat | - | 2: covered by a vocal tap |
| 164.959 | 87.05~ | Bridge | he [he] | TAP | 1: clear syllable |
| 165.362 | 87.08 | Bridge | kick/snare beat | - | 3: inside a held note (straight) |
| 165.834 | 87.12 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 166.010 | 87.13~ | Chorus 3 | Oh [oh] | TAP | 1: phrase start |
| 166.307 | 88.00 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 166.333 | 88.00 | Chorus 3 | my [my] | TAP | 1: title hook |
| 166.655 | 88.03 | Chorus 3 | oh [oh] | TAP | 1: title hook |
| 166.771 | 88.04 | Chorus 3 | my [my] | TAP | 1: title hook |
| 167.023 | 88.06 | Chorus 3 | God [god] | TAP | 1: title hook |
| 167.251 | 88.08 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 167.366 | 88.09 | Chorus 3 | 예상했어 [예] | TAP | 1: copied vocal = same pattern |
| 167.724 | 88.12 | Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 167.848 | 88.13 | Chorus 3 | 예상했어 [상] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 168.176 | 89.00 | Chorus 3 | 예상했어 [했] | TAP | 1: copied vocal = same pattern |
| 168.196 | 89.00 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 168.324 | 89.01 | Chorus 3 | 예상했어 [어] | - | 1: fast pair, not clearly sung |
| 168.567 | 89.03 | Chorus 3 | 나 [나] | TAP | 1: copied vocal = same pattern |
| 168.669 | 89.04 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 168.788 | 89.05 | Chorus 3 | I [i] | TAP | 1: phrase start |
| 169.141 | 89.08 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 169.148 | 89.08 | Chorus 3 | was [was] | TAP | 1: copied vocal = same pattern |
| 169.464 | 89.11 | Chorus 3 | really [real] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 169.569 | 89.12~ | Chorus 3 | really [ly] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 169.614 | 89.12 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 169.746 | 89.13 | Chorus 3 | hoping [hop] | TAP | 1: copied vocal = same pattern |
| 170.068 | 90.00 | Chorus 3 | hoping [ing] | TAP | 1: copied vocal = same pattern |
| 170.086 | 90.00 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 170.353 | 90.02 | Chorus 3 | that [that] | TAP | 1: copied vocal = same pattern |
| 170.558 | 90.04 | Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 170.663 | 90.05 | Chorus 3 | he [he] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 170.863 | 90.07~ | Chorus 3 | will [will] | TAP | 1: copied vocal = same pattern |
| 171.031 | 90.08 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 171.165 | 90.09 | Chorus 3 | come [come] | TAP | 1: copied vocal = same pattern |
| 171.503 | 90.12 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 171.682 | 90.14~ | Chorus 3 | through [through] | TAP | 1: copied vocal = same pattern |
| 172.448 | 91.04 | Chorus 3 | kick/snare beat | - | 3: inside a held note (straight) |
| 172.921 | 91.08 | Chorus 3 | kick/snare beat | - | 3: inside a held note (straight) |
| 173.272 | 91.11 | Chorus 3 | Oh [oh] | TAP | 1: phrase start |
| 173.393 | 91.12 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 173.844 | 92.00 | Chorus 3 | my [my] | TAP | 1: title hook |
| 173.865 | 92.00 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 174.117 | 92.02 | Chorus 3 | oh [oh] | TAP | 1: title hook |
| 174.335 | 92.04 | Chorus 3 | my [my] | TAP | 1: title hook |
| 174.338 | 92.04 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 174.587 | 92.06 | Chorus 3 | God [god] | TAP | 1: title hook |
| 174.810 | 92.08 | Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 174.967 | 92.09 | Chorus 3 | 단 [단] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 175.275 | 92.12 | Chorus 3 | 너뿐이야 [너] | TAP | 1: copied vocal = same pattern |
| 175.283 | 92.12 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 175.539 | 92.14 | Chorus 3 | 너뿐이야 [뿐] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 175.755 | 93.00 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 175.774 | 93.00 | Chorus 3 | 너뿐이야 [이] | TAP | 1: copied vocal = same pattern |
| 175.995 | 93.02 | Chorus 3 | 너뿐이야 [야] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 176.189 | 93.04 | Chorus 3 | Asking [ask] | TAP | 1: phrase start |
| 176.228 | 93.04 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 176.639 | 93.07~ | Chorus 3 | Asking [ing] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 176.700 | 93.08 | Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 176.959 | 93.10 | Chorus 3 | all [all] | TAP | 1: copied vocal = same pattern |
| 177.172 | 93.12 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 177.243 | 93.13~ | Chorus 3 | the [the] | TAP | 1: copied vocal = same pattern |
| 177.443 | 93.14 | Chorus 3 | time [time] | TAP | 1: copied vocal = same pattern |
| 177.645 | 94.00 | Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 177.771 | 94.01 | Chorus 3 | about [a] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 177.922 | 94.02~ | Chorus 3 | about [bout] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 178.117 | 94.04 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 178.137 | 94.04 | Chorus 3 | what [what] | TAP | 1: copied vocal = same pattern |
| 178.407 | 94.06~ | Chorus 3 | I [i] | TAP | 1: copied vocal = same pattern |
| 178.590 | 94.08 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 178.741 | 94.09 | Chorus 3 | should [should] | TAP | 1: copied vocal = same pattern |
| 179.062 | 94.12 | Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 179.095 | 94.12 | Chorus 3 | do [do] | TAP | 1: copied vocal = same pattern |
| 179.709 | 95.01~ | Post-Chorus 3 | No [no] | TAP | 1: phrase start |
| 180.007 | 95.04 | Post-Chorus 3 | kick/snare beat | - | 3: inside a held note (straight) |
| 180.432 | 95.08~ | Post-Chorus 3 | I [i] | TAP | 1: clear syllable |
| 180.479 | 95.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 180.812 | 95.11 | Post-Chorus 3 | can [can] | TAP | 1: clear syllable |
| 180.952 | 95.12 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 181.303 | 95.15 | Post-Chorus 3 | never [nev] | TAP | 1: clear syllable |
| 181.424 | 96.00 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 181.428 | 96.00 | Post-Chorus 3 | never [er] | - | 1: fast pair, not clearly sung |
| 181.596 | 96.01~ | Post-Chorus 3 | let [let] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 181.935 | 96.04 | Post-Chorus 3 | him [him] | TAP | 1: clear syllable |
| 182.147 | 96.06 | Post-Chorus 3 | go [go] | TAP | 1: clear syllable |
| 182.369 | 96.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 182.487 | 96.09 | Post-Chorus 3 | He's [he's] | TAP | 1: phrase start |
| 182.632 | 96.10 | Post-Chorus 3 | right [right] | - | 1: fast pair, not clearly sung |
| 182.842 | 96.12 | Post-Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 182.937 | 96.13 | Post-Chorus 3 | there [there] | - | 1: fast pair, not clearly sung |
| 183.091 | 96.14 | Post-Chorus 3 | for [for] | TAP | 1: clear syllable |
| 183.326 | 97.00 | Post-Chorus 3 | me [me] | TAP | 1: clear syllable |
| 183.552 | 97.02 | Post-Chorus 3 | twenty-four [twen] | TAP | 1: clear syllable |
| 183.744 | 97.04~ | Post-Chorus 3 | twenty-four [ty] | TAP | 1: clear syllable |
| 183.744 | 97.04~ | Post-Chorus 3 | 난 [난] | TAP | 1: phrase start |
| 183.786 | 97.04 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 183.842 | 97.04~ | Post-Chorus 3 | twenty-four [four] | - | 1: within 0.105 s of a tapped syllable |
| 184.025 | 97.06 | Post-Chorus 3 | 행운아야 [행] | TAP | 1: clear syllable |
| 184.259 | 97.08 | Post-Chorus 3 | kick/snare beat | - | 3: inside a held note (straight) |
| 184.536 | 97.10~ | Post-Chorus 3 | 행운아야 [운] | TAP | 1: clear syllable |
| 184.731 | 97.12 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 184.870 | 97.13 | Post-Chorus 3 | 행운아야 [아] | TAP | 1: clear syllable |
| 185.175 | 98.00 | Post-Chorus 3 | 행운아야 [야] | TAP | 1: clear syllable |
| 185.204 | 98.00 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 185.401 | 98.02 | Post-Chorus 3 | 정말로 [정] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 185.676 | 98.04 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 185.691 | 98.04 | Post-Chorus 3 | 정말로 [말] | TAP | 1: clear syllable |
| 185.976 | 98.07~ | Post-Chorus 3 | 정말로 [로] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 186.149 | 98.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 186.220 | 98.09~ | Post-Chorus 3 | I [i] | TAP | 1: phrase start |
| 186.388 | 98.10 | Post-Chorus 3 | know [know] | TAP | 1: clear syllable |
| 186.621 | 98.12 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 186.640 | 98.12 | Post-Chorus 3 | I [i] | TAP | 1: clear syllable |
| 186.916 | 98.14~ | Post-Chorus 3 | know [know] | TAP | 1: clear syllable |
| 187.093 | 99.00 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 187.172 | 99.01 | Post-Chorus 3 | 널 [널] | TAP | 1: phrase start |
| 187.566 | 99.04 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 187.755 | 99.06~ | Post-Chorus 3 | 알기 [알] | TAP | 1: clear syllable |
| 188.038 | 99.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 188.141 | 99.09 | Post-Chorus 3 | 알기 [기] | TAP | 1: clear syllable |
| 188.501 | 99.12 | Post-Chorus 3 | 전까지는 [전] | TAP | 1: clear syllable |
| 188.511 | 99.12 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 188.812 | 99.15~ | Post-Chorus 3 | 전까지는 [까] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 188.983 | 100.00 | Post-Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 188.986 | 100.00 | Post-Chorus 3 | 전까지는 [지] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 189.151 | 100.01~ | Post-Chorus 3 | 전까지는 [는] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 189.322 | 100.03 | Post-Chorus 3 | 나 [나] | TAP | 1: clear syllable |
| 189.703 | 100.06 | Post-Chorus 3 | 의미 [의] | TAP | 1: phrase start |
| 189.928 | 100.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 189.932 | 100.08 | Post-Chorus 3 | 의미 [미] | TAP | 1: clear syllable |
| 190.155 | 100.10 | Post-Chorus 3 | 없었어 [없] | TAP | 1: clear syllable |
| 190.400 | 100.12 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 190.402 | 100.12 | Post-Chorus 3 | 없었어 [었] | TAP | 1: clear syllable |
| 190.649 | 100.14 | Post-Chorus 3 | 없었어 [어] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 190.873 | 101.00 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 190.884 | 101.00 | Post-Chorus 3 | 전부 [전] | TAP | 1: clear syllable |
| 191.287 | 101.04~ | Post-Chorus 3 | 전부 [부] | TAP | 1: clear syllable |
| 191.583 | 101.06 | Post-Chorus 3 | 다 [다] | TAP | 1: clear syllable |
| 191.804 | 101.08 | Post-Chorus 3 | 어떡해 [어] | TAP | 1: phrase start |
| 191.818 | 101.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 192.056 | 101.10 | Post-Chorus 3 | 어떡해 [떡] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 192.280 | 101.12 | Post-Chorus 3 | 어떡해 [해] | TAP | 1: clear syllable |
| 192.290 | 101.12 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 192.532 | 101.14 | Post-Chorus 3 | My [my] | TAP | 1: phrase start |
| 192.675 | 101.15 | Post-Chorus 3 | heart [heart] | - | 1: fast pair, not clearly sung |
| 192.763 | 102.00 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 192.881 | 102.01 | Post-Chorus 3 | is [is] | TAP | 1: clear syllable |
| 193.151 | 102.03 | Post-Chorus 3 | glowing [glow] | - | 1: within 0.105 s of a tapped syllable |
| 193.235 | 102.04 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 193.247 | 102.04 | Post-Chorus 3 | glowing [ing] | TAP | 1: clear syllable |
| 193.641 | 102.07~ | Post-Chorus 3 | it's [it's] | - | 1: fast pair, not clearly sung |
| 193.707 | 102.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 193.792 | 102.09 | Post-Chorus 3 | glowing [glow] | TAP | 1: clear syllable |
| 193.949 | 102.10 | Post-Chorus 3 | glowing [ing] | TAP | 1: clear syllable |
| 194.180 | 102.12 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 194.225 | 102.12~ | Post-Chorus 3 | My [my] | TAP | 1: phrase start |
| 194.373 | 102.14~ | Post-Chorus 3 | heart [heart] | - | 1: fast pair, not clearly sung |
| 194.652 | 103.00 | Post-Chorus 3 | kick/snare beat | TAP | 2: drum beat, no vocal within ±0.20 s |
| 194.765 | 103.01 | Post-Chorus 3 | is [is] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 194.921 | 103.02 | Post-Chorus 3 | glowing [glow] | - | 1: per-bar / 2 s limit (weaker syllable) |
| 195.066 | 103.04~ | Post-Chorus 3 | glowing [ing] | - | 1: fast pair, not clearly sung |
| 195.125 | 103.04 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 195.197 | 103.05~ | Post-Chorus 3 | up [up] | TAP | 1: clear syllable |
| 195.560 | 103.08 | Post-Chorus 3 | so [so] | TAP | 1: clear syllable |
| 195.597 | 103.08 | Post-Chorus 3 | kick/snare beat | - | 2: covered by a vocal tap |
| 195.865 | 103.10 | Post-Chorus 3 | I [i] | TAP | 1: clear syllable |
| 196.201 | 103.13 | Post-Chorus 3 | can't [can't] | - | 1: too faint |
| 196.445 | 103.15 | Post-Chorus 3 | sleep [sleep] | TAP | 1: clear syllable |
| 196.613 | 104.01~ | Post-Chorus 3 | at [at] | - | 1: fast pair, not clearly sung |
| 197.023 | 104.04 | Post-Chorus 3 | night [night] | TAP | 1: clear syllable |
| 197.487 | 104.08 | Outro (instrumental) | kick/snare beat | - | 3: inside a held note (straight) |
| 199.144 | 105.06 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 199.617 | 105.10 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 200.088 | 105.14 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 200.329 | 106.00 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 201.269 | 106.08 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 201.507 | 106.10 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 201.748 | 106.12 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 201.980 | 106.14 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 202.450 | 107.02 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 202.923 | 107.06 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 203.397 | 107.10 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 203.870 | 107.14 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 204.578 | 108.04 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 205.048 | 108.08 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 205.286 | 108.10 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 205.527 | 108.12 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 205.759 | 108.14 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 206.702 | 109.06 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 207.178 | 109.10 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 207.646 | 109.14 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 207.887 | 110.00 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 208.827 | 110.08 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 209.068 | 110.10 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 209.538 | 110.14 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 210.008 | 111.02 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
| 210.484 | 111.06 | Outro (instrumental) | piano | TAP | 4: no vocal, no drums: piano on 8ths |
