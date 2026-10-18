# OMG lyric chart (vocal-primary re-chart)

Why: after playing the 451-tap rule-based chart, the user said on 2026-10-18 "我感觉这个可以跟歌词的配合可以更加多一点，就是这个卡点".
They want the taps to follow the lyrics. This chart makes the vocal the primary layer wherever someone is singing.

## Lyric timing (analysis/omg.lyrics.json)
* Lyrics: Genius, Korean + English ([original](https://genius.com/Newjeans-omg-lyrics), [romanized](https://genius.com/Genius-romanizations-newjeans-omg-romanized-lyrics)).
  Verse 2 and Pre-Chorus 2 are cross-checked against the [FRNK remix lyric page](https://lyrics.lol/artist/3239944-NewJeans-%EB%89%B4%EC%A7%84%EC%8A%A4/lyrics/9837130-OMG-FRNK-Remix), because Genius hides that block.
* Vocal stem: demucs vocals, shifted 1105 samples (25.1 ms, the mp3 encoder delay) onto the gapless decode the game plays.
* Word prior: faster-whisper large-v3 word timestamps on the stem. Whisper's text is not used, only its timing.
  Whisper mishears some words (e.g. "You better tell me who is he" for the ad-lib), but its syllable counts match the lyrics.
* Syllables: Hangul = one syllable per character; English words come from a hand-made syllable table.
  A monotonic dynamic-programming pass snaps each syllable to a calibrated vocal-stem onset near its prior (syllables at least 90 ms apart).
  The 3 choruses and post-choruses 1/2 are sample copies of each other: the vocal stems cross-correlate at 0.93 / 0.91 at exactly 128 / 256 beats.
  Those lines are aligned once on the averaged prior and copied, so the repeats are identical by construction.
* Result: 86 lines and 681 syllables; 94% snapped to an onset, 6% keep the prior.
  Each syllable carries a strength, its vocal prominence vs the mix, the section and member(s) from the Genius headers, and lead/hook/ad-lib.
  There is also a line timeline.
* Spot checks, all on the vocal stem:
  * Spectrogram views with the syllable marks (`analysis/research/lyrics-check/check1.png`, `check2.png`):
    chorus hook, verse 1, pre-chorus, fast English rap in verse 2, interlude "baby" chops, bridge, post-chorus.
    Marks sit on the note/consonant boundaries. The weakest areas are the chopped interlude and the fast pre-chorus ad-libs.
  * Independent check against whisper word starts: median difference -4 ms, |d| median 28 ms; 73% within 50 ms, 90% within 100 ms.
  * Nobody has listened to it yet: the click track below is for listening.

## Chart rules
* Every sung line's first syllable is tapped (85/86; the faint "'Cause he" pickup at 164.38 is not).
* Title hooks tap every syllable: "Oh my, oh my God", the interlude "baby" chops, "I'm going crazy", "I know, I know", "Mm-hm".
* Other syllables are ranked by word start, onset strength, note length, and beat position (bonus when a downbeat or backbeat coincides),
  then picked greedily per bar.
* Held notes and melismas are not tapped, so they stay straight (only syllable onsets can be taps).
* Fast pairs under 170 ms need both syllables clearly enunciated. Minimum gap is 0.105 s; at most 5 taps in any 2 s window around a candidate.
* Lines with the same text use one pattern, chosen by majority vote across the repeats (pre-chorus ad-libs, pre-chorus 1 vs 2, post-chorus 3).
  The copied choruses and post-choruses mirror chorus 1 exactly.
* Timing: snapped to the 16th grid within 40 ms or to the triplet grid within 25 ms, otherwise the measured onset.
  Counts: 369 on 16ths, 56 on triplets, 29 on raw onsets. Syllable onset minus tap: median +2 ms, |d| median 14 ms, max 40 ms.
* No vocal: the taps of the previous rule-based chart are kept, but only where the vocal stem is silent.
  That is 24 taps: interlude gaps 139.8-140.8 and 148.4, plus the outro piano 198-210.
  Previous-chart taps that fall during a held vocal note are dropped, so the note stays straight.

## Before / after
| | 451-tap chart (rule-based) | lyric chart |
|---|---|---|
| taps | 451 | 478 |
| taps on a sung syllable (+-50 ms) | 185 (41%) | 454 (95%) |
| taps during sung lines that land on a syllable | 44% | 100% |
| line starts tapped | 11/86 | 85/86 |
| syllables tapped | 191/681 | 464/681 |
| strong drum quarter-beat accents tapped | 251/297 | 113/297 (trade-off: vocal wins) |
| average / peak density | 2.12/s; 6 taps in 1 s | 2.25/s; 5 taps in 1 s, 300 CPM |

The new chart has 28 bars with no tap on a quarter beat. In every one of them the vocal itself is syncopated, so the vocal wins, per the user's request.

## Verification
* `levels-design/validate.py`: 0 errors, 473 multi-level crossings. Minimum judgment window ±53 ms; 16 gaps under 0.15 s, all real fast syllables.
* chartlogic flags many taps as "faint" or "hop". Its band/vocal envelopes do not tell sung syllables apart:
  whisper word starts, which are independent of my alignment, score the same as random times inside sung lines (median 0.28 vs 0.26).
  So these flags are expected for a legato vocal layer and are not timing errors.
* scripted playthrough (headless Chrome, CDP touch simulation; not a real device): complete, 478/478 perfect, 0 good, diamonds 10/10.
* Layout changes, all on OMG only (no art-props dependency):
  * the chorus falls moved onto the tap at "예" (45.382→46.427, 105.853→106.898, 166.323→167.369), because a fall needs ≥0.35 s before the next tap;
  * 6 diamonds moved off taps: 8.238→8.529, 26.71→26.498, 53.162→52.673, 83.885→83.775, 99.941→98.499, 150.717→150.466.
  The route is the seed-5 search (route.py). All scenery is route-relative.
* Click track: `deliverables/omg-clicks-lyrics.mp3` (song + 478 clicks).

## Lyric-annotated timeline (one row per sung syllable + instrumental taps)
* The pos column is bar.step on the 16th grid (127.003 BPM, beat0 0.011 s). A trailing ~ means the syllable onset is more than 40 ms off a 16th (triplet or raw onset).
* The reason is the main rule that decided the syllable.

| time (s) | pos | section | word | syllable | tap | reason |
|---|---|---|---|---|---|---|
| 2.614 | 1.06 | Intro | 이 | 이 | TAP | phrase start |
| 3.226 | 1.11 | Intro | 노래는 | 노 | TAP | word start |
| 3.415 | 1.13 | Intro | 노래는 | 래 | TAP | clear syllable |
| 3.685 | 1.15 | Intro | 노래는 | 는 | - | fast pair, not clearly enunciated |
| 3.833 | 2.00~ | Intro | it's | it's | TAP | word start |
| 4.608 | 2.07 | Intro | about | a | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 4.700 | 2.08 | Intro | about | bout | - | within 105 ms of a tapped syllable (min gap) |
| 4.802 | 2.09~ | Intro | you | you | TAP | word start |
| 5.110 | 2.11 | Intro | baby | ba | TAP | word start |
| 5.278 | 2.13~ | Intro | baby | by | TAP | clear syllable |
| 7.620 | 4.00~ | Intro | Only | on | TAP | phrase start |
| 7.945 | 4.03 | Intro | Only | ly | TAP | clear syllable |
| 8.265 | 4.06 | Intro | you | you | TAP | word start |
| 11.251 | 5.15 | Intro | You | you | TAP | phrase start |
| 12.050 | 6.06 | Intro | you | you | TAP | word start |
| 12.552 | 6.10 | Intro | you | you | TAP | word start |
| 13.051 | 6.14~ | Intro | You | you | TAP | phrase start |
| 13.762 | 7.04~ | Intro | you | you | TAP | word start |
| 13.954 | 7.06 | Intro | you | you | TAP | word start |
| 14.305 | 7.09 | Intro | you | you | TAP | word start |
| 14.967 | 7.15~ | Verse 1 | 내가 | 내 | TAP | phrase start |
| 15.260 | 8.01 | Verse 1 | 내가 | 가 | - | timing uncertain (no clear onset) |
| 15.605 | 8.04 | Verse 1 | 힘들 | 힘 | TAP | word start, on the beat |
| 15.875 | 8.06 | Verse 1 | 힘들 | 들 | TAP | clear syllable |
| 16.293 | 8.10 | Verse 1 | 때 | 때 | TAP | word start |
| 16.757 | 8.14 | Verse 1 | 울 | 울 | TAP | word start |
| 17.019 | 9.00 | Verse 1 | 것 | 것 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 17.283 | 9.02 | Verse 1 | 같을 | 같 | TAP | word start |
| 17.521 | 9.04 | Verse 1 | 같을 | 을 | TAP | clear syllable, on the beat |
| 17.747 | 9.06 | Verse 1 | 때 | 때 | TAP | word start |
| 18.293 | 9.11 | Verse 1 | Mm-hm | mm | TAP | phrase start |
| 18.673 | 9.14 | Verse 1 | Mm-hm | hm | TAP | repeated phrase pattern |
| 19.260 | 10.03 | Verse 1 | 기운도 | 기 | TAP | phrase start |
| 19.492 | 10.05 | Verse 1 | 기운도 | 운 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 19.637 | 10.06 | Verse 1 | 기운도 | 도 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 19.904 | 10.08~ | Verse 1 | 이젠 | 이 | TAP | word start |
| 20.098 | 10.10 | Verse 1 | 이젠 | 젠 | TAP | clear syllable |
| 20.348 | 10.12 | Verse 1 | 나지 | 나 | TAP | word start, on the beat |
| 20.705 | 10.15 | Verse 1 | 나지 | 지 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 21.033 | 11.02 | Verse 1 | 않을 | 않 | TAP | word start |
| 21.314 | 11.04~ | Verse 1 | 않을 | 을 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 21.587 | 11.07 | Verse 1 | 때 | 때 | TAP | word start |
| 21.837 | 11.09 | Verse 1 | Mm-hm | mm | TAP | phrase start |
| 22.223 | 11.12 | Verse 1 | Mm-hm | hm | TAP | repeated phrase pattern |
| 22.626 | 11.15~ | Verse 1 | It's | it's | TAP | phrase start |
| 23.262 | 12.05 | Verse 1 | you | you | TAP | repeated phrase pattern |
| 23.802 | 12.09~ | Verse 1 | 날 | 날 | TAP | phrase start |
| 23.898 | 12.10 | Verse 1 | 걱정하네 | 걱 | - | within 105 ms of a tapped syllable (min gap) |
| 24.115 | 12.12 | Verse 1 | 걱정하네 | 정 | TAP | clear syllable, on the beat |
| 24.345 | 12.14 | Verse 1 | 걱정하네 | 하 | TAP | clear syllable |
| 24.652 | 13.01~ | Verse 1 | 걱정하네 | 네 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 24.873 | 13.03~ | Verse 1 | it's | it's | TAP | phrase start |
| 25.154 | 13.05 | Verse 1 | you | you | TAP | repeated phrase pattern |
| 25.590 | 13.09~ | Verse 1 | 날 | 날 | TAP | phrase start |
| 25.749 | 13.10 | Verse 1 | 웃게하네 | 웃 | - | fast pair, not clearly enunciated |
| 26.011 | 13.12 | Verse 1 | 웃게하네 | 게 | TAP | clear syllable, on the beat |
| 26.347 | 13.15 | Verse 1 | 웃게하네 | 하 | - | too faint to hear as a new syllable |
| 26.507 | 14.00 | Verse 1 | 웃게하네 | 네 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 26.748 | 14.02~ | Verse 1 | 말 | 말 | TAP | phrase start |
| 26.922 | 14.04 | Verse 1 | 안 | 안 | TAP | word start, on the beat |
| 27.198 | 14.06 | Verse 1 | 해도 | 해 | TAP | word start |
| 27.392 | 14.08 | Verse 1 | 해도 | 도 | TAP | clear syllable, on the beat |
| 27.584 | 14.09~ | Verse 1 | 돼 | 돼 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 28.144 | 14.14 | Verse 1 | boy | boy | TAP | word start |
| 28.504 | 15.01 | Verse 1 | what | what | - | fast pair, not clearly enunciated |
| 28.666 | 15.03~ | Verse 1 | do | do | TAP | word start |
| 28.887 | 15.04~ | Verse 1 | you | you | TAP | word start |
| 29.084 | 15.06 | Verse 1 | say? | say | TAP | word start |
| 29.421 | 15.09 | Pre-Chorus 1 | They | they | TAP | phrase start |
| 29.530 | 15.10 | Pre-Chorus 1 | keep | keep | - | fast pair, not clearly enunciated |
| 29.581 | 15.10~ | Pre-Chorus 1 | on | on | - | fast pair, not clearly enunciated |
| 29.672 | 15.11 | Pre-Chorus 1 | asking | ask | - | ad-lib under the lead: kept sparse |
| 29.737 | 15.12 | Pre-Chorus 1 | asking | ing | - | ad-lib under the lead: kept sparse |
| 29.874 | 15.13 | Pre-Chorus 1 | me | me | - | fast pair, not clearly enunciated |
| 29.980 | 15.14 | Pre-Chorus 1 | who | who | TAP | repeated phrase pattern |
| 30.031 | 15.14 | Pre-Chorus 1 | is | is | TAP | repeated phrase pattern |
| 30.158 | 15.15 | Pre-Chorus 1 | he? | he | - | fast pair, not clearly enunciated |
| 30.327 | 16.01 | Pre-Chorus 1 | 멀리든 | 멀 | TAP | phrase start |
| 30.538 | 16.02~ | Pre-Chorus 1 | 멀리든 | 리 | TAP | repeated phrase pattern |
| 31.087 | 16.07 | Pre-Chorus 1 | 멀리든 | 든 | TAP | repeated phrase pattern |
| 31.557 | 16.11 | Pre-Chorus 1 | 언제든지 | 언 | TAP | repeated phrase pattern |
| 31.865 | 16.14 | Pre-Chorus 1 | 언제든지 | 제 | TAP | repeated phrase pattern |
| 32.138 | 17.00 | Pre-Chorus 1 | 언제든지 | 든 | TAP | repeated phrase pattern |
| 32.411 | 17.02 | Pre-Chorus 1 | 언제든지 | 지 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 32.596 | 17.04 | Pre-Chorus 1 | 달려와 | 달 | TAP | repeated phrase pattern |
| 32.878 | 17.06 | Pre-Chorus 1 | 달려와 | 려 | TAP | repeated phrase pattern |
| 33.186 | 17.09 | Pre-Chorus 1 | 달려와 | 와 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 33.386 | 17.11~ | Pre-Chorus 1 | They | they | TAP | phrase start |
| 33.450 | 17.11 | Pre-Chorus 1 | keep | keep | - | within 105 ms of a tapped syllable (min gap) |
| 33.490 | 17.11~ | Pre-Chorus 1 | on | on | - | within 105 ms of a tapped syllable (min gap) |
| 33.528 | 17.12 | Pre-Chorus 1 | asking | ask | - | fast pair, not clearly enunciated |
| 33.653 | 17.13 | Pre-Chorus 1 | asking | ing | - | ad-lib under the lead: kept sparse |
| 33.812 | 17.14 | Pre-Chorus 1 | me | me | - | within 105 ms of a tapped syllable (min gap) |
| 33.870 | 17.15 | Pre-Chorus 1 | who | who | TAP | repeated phrase pattern |
| 33.972 | 18.00~ | Pre-Chorus 1 | is | is | - | within 105 ms of a tapped syllable (min gap) |
| 34.196 | 18.01~ | Pre-Chorus 1 | he? | he | - | ad-lib under the lead: kept sparse |
| 34.500 | 18.04 | Pre-Chorus 1 | 바쁜 | 바 | TAP | phrase start |
| 34.947 | 18.08 | Pre-Chorus 1 | 바쁜 | 쁜 | TAP | repeated phrase pattern |
| 35.333 | 18.11 | Pre-Chorus 1 | 척도 | 척 | TAP | repeated phrase pattern |
| 35.528 | 18.13 | Pre-Chorus 1 | 척도 | 도 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 35.699 | 18.14 | Pre-Chorus 1 | 없이 | 없 | TAP | repeated phrase pattern |
| 35.879 | 19.00 | Pre-Chorus 1 | 없이 | 이 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 36.056 | 19.01 | Pre-Chorus 1 | 넌 | 넌 | TAP | repeated phrase pattern |
| 36.433 | 19.04~ | Pre-Chorus 1 | 나타나 | 나 | TAP | repeated phrase pattern |
| 36.645 | 19.06 | Pre-Chorus 1 | 나타나 | 타 | TAP | repeated phrase pattern |
| 36.854 | 19.08 | Pre-Chorus 1 | 나타나 | 나 | TAP | repeated phrase pattern |
| 37.133 | 19.10 | Pre-Chorus 1 | They | they | TAP | phrase start |
| 37.383 | 19.12~ | Pre-Chorus 1 | keep | keep | - | fast pair, not clearly enunciated |
| 37.450 | 19.13 | Pre-Chorus 1 | on | on | - | within 105 ms of a tapped syllable (min gap) |
| 37.472 | 19.13 | Pre-Chorus 1 | asking | ask | - | within 105 ms of a tapped syllable (min gap) |
| 37.487 | 19.13 | Pre-Chorus 1 | asking | ing | - | within 105 ms of a tapped syllable (min gap) |
| 37.543 | 19.14 | Pre-Chorus 1 | me | me | TAP | repeated phrase pattern |
| 37.594 | 19.14 | Pre-Chorus 1 | who | who | TAP | repeated phrase pattern |
| 37.740 | 19.15~ | Pre-Chorus 1 | is | is | - | fast pair, not clearly enunciated |
| 37.972 | 20.01~ | Pre-Chorus 1 | he? | he | - | ad-lib under the lead: kept sparse |
| 38.233 | 20.04~ | Pre-Chorus 1 | 이게 | 이 | TAP | phrase start |
| 38.613 | 20.07 | Pre-Chorus 1 | 이게 | 게 | TAP | repeated phrase pattern |
| 38.712 | 20.08 | Pre-Chorus 1 | 말이 | 말 | - | within 105 ms of a tapped syllable (min gap) |
| 39.069 | 20.11 | Pre-Chorus 1 | 말이 | 이 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 39.310 | 20.13 | Pre-Chorus 1 | 되니 | 되 | TAP | repeated phrase pattern |
| 39.676 | 21.00 | Pre-Chorus 1 | 되니 | 니 | TAP | repeated phrase pattern |
| 39.963 | 21.02 | Pre-Chorus 1 | 난 | 난 | TAP | repeated phrase pattern |
| 40.201 | 21.04 | Pre-Chorus 1 | 물어봐 | 물 | TAP | repeated phrase pattern |
| 40.474 | 21.07~ | Pre-Chorus 1 | 물어봐 | 어 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 40.700 | 21.09~ | Pre-Chorus 1 | 물어봐 | 봐 | TAP | repeated phrase pattern |
| 41.028 | 21.11 | Pre-Chorus 1 | They | they | TAP | phrase start |
| 41.234 | 21.13 | Pre-Chorus 1 | keep | keep | - | within 105 ms of a tapped syllable (min gap) |
| 41.295 | 21.14~ | Pre-Chorus 1 | asking | ask | - | within 105 ms of a tapped syllable (min gap) |
| 41.300 | 21.14~ | Pre-Chorus 1 | asking | ing | TAP | repeated phrase pattern |
| 41.310 | 21.14 | Pre-Chorus 1 | on | on | TAP | repeated phrase pattern |
| 41.335 | 21.14 | Pre-Chorus 1 | me | me | TAP | repeated phrase pattern |
| 41.373 | 21.14 | Pre-Chorus 1 | who | who | TAP | repeated phrase pattern |
| 41.475 | 21.15 | Pre-Chorus 1 | is | is | - | within 105 ms of a tapped syllable (min gap) |
| 41.693 | 22.01 | Pre-Chorus 1 | he? | he | - | ad-lib under the lead: kept sparse |
| 42.009 | 22.04~ | Pre-Chorus 1 | 너는 | 너 | TAP | phrase start |
| 42.456 | 22.07~ | Pre-Chorus 1 | 너는 | 는 | TAP | repeated phrase pattern |
| 42.712 | 22.10~ | Pre-Chorus 1 | 말야 | 말 | TAP | repeated phrase pattern |
| 43.002 | 22.12 | Pre-Chorus 1 | 말야 | 야 | TAP | repeated phrase pattern |
| 43.260 | 22.14 | Pre-Chorus 1 | he's | he's | TAP | repeated phrase pattern |
| 43.568 | 23.01 | Pre-Chorus 1 | the | the | TAP | repeated phrase pattern |
| 43.600 | 23.01 | Pre-Chorus 1 | one | one | TAP | repeated phrase pattern |
| 43.710 | 23.02 | Pre-Chorus 1 | that's | that's | TAP | repeated phrase pattern |
| 43.920 | 23.04 | Pre-Chorus 1 | living | liv | - | timing uncertain (no clear onset) |
| 43.948 | 23.04 | Pre-Chorus 1 | living | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 44.079 | 23.05 | Pre-Chorus 1 | in | in | - | fast pair, not clearly enunciated |
| 44.186 | 23.06 | Pre-Chorus 1 | my | my | TAP | repeated phrase pattern |
| 44.357 | 23.07~ | Pre-Chorus 1 | system | sys | TAP | repeated phrase pattern |
| 44.537 | 23.09 | Pre-Chorus 1 | system | tem | - | within 105 ms of a tapped syllable (min gap) |
| 44.630 | 23.10 | Pre-Chorus 1 | baby | ba | TAP | repeated phrase pattern |
| 44.798 | 23.11 | Pre-Chorus 1 | baby | by | TAP | repeated phrase pattern |
| 45.065 | 23.13~ | Chorus 1 | Oh | oh | TAP | phrase start |
| 45.388 | 24.00 | Chorus 1 | my | my | TAP | title hook: every syllable |
| 45.710 | 24.03 | Chorus 1 | oh | oh | TAP | title hook: every syllable |
| 45.826 | 24.04 | Chorus 1 | my | my | TAP | title hook: every syllable |
| 46.078 | 24.06 | Chorus 1 | God | god | TAP | title hook: every syllable |
| 46.421 | 24.09 | Chorus 1 | 예상했어 | 예 | TAP | repeated phrase pattern |
| 46.903 | 24.13 | Chorus 1 | 예상했어 | 상 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 47.231 | 25.00 | Chorus 1 | 예상했어 | 했 | TAP | repeated phrase pattern |
| 47.379 | 25.01 | Chorus 1 | 예상했어 | 어 | - | fast pair, not clearly enunciated |
| 47.623 | 25.03 | Chorus 1 | 나 | 나 | TAP | repeated phrase pattern |
| 47.843 | 25.05 | Chorus 1 | I | i | TAP | phrase start |
| 48.203 | 25.08 | Chorus 1 | was | was | TAP | repeated phrase pattern |
| 48.519 | 25.11 | Chorus 1 | really | real | TAP | repeated phrase pattern |
| 48.624 | 25.12~ | Chorus 1 | really | ly | - | fast pair, not clearly enunciated |
| 48.801 | 25.13 | Chorus 1 | hoping | hop | TAP | repeated phrase pattern |
| 49.123 | 26.00 | Chorus 1 | hoping | ing | TAP | repeated phrase pattern |
| 49.408 | 26.02 | Chorus 1 | that | that | TAP | repeated phrase pattern |
| 49.718 | 26.05 | Chorus 1 | he | he | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 49.918 | 26.07~ | Chorus 1 | will | will | TAP | repeated phrase pattern |
| 50.220 | 26.09 | Chorus 1 | come | come | TAP | repeated phrase pattern |
| 50.737 | 26.13~ | Chorus 1 | through | through | TAP | repeated phrase pattern |
| 52.328 | 27.11 | Chorus 1 | Oh | oh | TAP | phrase start |
| 52.899 | 28.00 | Chorus 1 | my | my | TAP | title hook: every syllable |
| 53.172 | 28.02 | Chorus 1 | oh | oh | TAP | title hook: every syllable |
| 53.390 | 28.04 | Chorus 1 | my | my | TAP | title hook: every syllable |
| 53.642 | 28.06 | Chorus 1 | God | god | TAP | title hook: every syllable |
| 54.023 | 28.09 | Chorus 1 | 단 | 단 | TAP | repeated phrase pattern |
| 54.330 | 28.12 | Chorus 1 | 너뿐이야 | 너 | TAP | repeated phrase pattern |
| 54.594 | 28.14 | Chorus 1 | 너뿐이야 | 뿐 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 54.829 | 29.00 | Chorus 1 | 너뿐이야 | 이 | TAP | repeated phrase pattern |
| 55.050 | 29.02 | Chorus 1 | 너뿐이야 | 야 | TAP | repeated phrase pattern |
| 55.245 | 29.04~ | Chorus 1 | Asking | ask | TAP | phrase start |
| 55.694 | 29.07~ | Chorus 1 | Asking | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 56.014 | 29.10 | Chorus 1 | all | all | TAP | repeated phrase pattern |
| 56.298 | 29.13~ | Chorus 1 | the | the | TAP | repeated phrase pattern |
| 56.498 | 29.14 | Chorus 1 | time | time | TAP | repeated phrase pattern |
| 56.826 | 30.01 | Chorus 1 | about | a | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 56.977 | 30.02 | Chorus 1 | about | bout | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 57.192 | 30.04 | Chorus 1 | what | what | TAP | repeated phrase pattern |
| 57.462 | 30.06~ | Chorus 1 | I | i | TAP | repeated phrase pattern |
| 57.796 | 30.09 | Chorus 1 | should | should | TAP | repeated phrase pattern |
| 58.150 | 30.12 | Chorus 1 | do | do | TAP | repeated phrase pattern |
| 59.465 | 31.07~ | Post-Chorus 1 | No | no | TAP | phrase start |
| 59.772 | 31.10 | Post-Chorus 1 | I | i | TAP | repeated phrase pattern |
| 60.034 | 31.12 | Post-Chorus 1 | can | can | TAP | repeated phrase pattern |
| 60.199 | 31.14~ | Post-Chorus 1 | never | nev | TAP | repeated phrase pattern |
| 60.396 | 31.15 | Post-Chorus 1 | never | er | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 60.614 | 32.01 | Post-Chorus 1 | let | let | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 60.931 | 32.04 | Post-Chorus 1 | him | him | TAP | repeated phrase pattern |
| 61.163 | 32.06 | Post-Chorus 1 | go | go | TAP | repeated phrase pattern |
| 61.395 | 32.08 | Post-Chorus 1 | 너만 | 너 | TAP | phrase start |
| 61.645 | 32.10 | Post-Chorus 1 | 너만 | 만 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 61.926 | 32.12 | Post-Chorus 1 | 생각나 | 생 | TAP | repeated phrase pattern |
| 62.147 | 32.14 | Post-Chorus 1 | 생각나 | 각 | TAP | repeated phrase pattern |
| 62.376 | 33.00 | Post-Chorus 1 | 생각나 | 나 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 62.608 | 33.02 | Post-Chorus 1 | twenty-four | twen | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 62.843 | 33.04 | Post-Chorus 1 | twenty-four | ty | TAP | repeated phrase pattern |
| 62.988 | 33.05 | Post-Chorus 1 | twenty-four | four | - | within 105 ms of a tapped syllable (min gap) |
| 63.081 | 33.06 | Post-Chorus 1 | 난 | 난 | TAP | phrase start |
| 63.554 | 33.10 | Post-Chorus 1 | 행운아야 | 행 | TAP | repeated phrase pattern |
| 63.827 | 33.12 | Post-Chorus 1 | 행운아야 | 운 | TAP | repeated phrase pattern |
| 64.027 | 33.14 | Post-Chorus 1 | 행운아야 | 아 | TAP | repeated phrase pattern |
| 64.294 | 34.00 | Post-Chorus 1 | 행운아야 | 야 | TAP | repeated phrase pattern |
| 64.512 | 34.02 | Post-Chorus 1 | 정말로 | 정 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 64.762 | 34.04 | Post-Chorus 1 | 정말로 | 말 | TAP | repeated phrase pattern |
| 64.979 | 34.06 | Post-Chorus 1 | 정말로 | 로 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 65.212 | 34.08 | Post-Chorus 1 | I | i | TAP | phrase start |
| 65.392 | 34.10~ | Post-Chorus 1 | know | know | TAP | repeated phrase pattern |
| 65.760 | 34.13 | Post-Chorus 1 | I | i | TAP | repeated phrase pattern |
| 65.900 | 34.14 | Post-Chorus 1 | know | know | TAP | repeated phrase pattern |
| 66.239 | 35.01 | Post-Chorus 1 | 널 | 널 | TAP | phrase start |
| 67.420 | 35.11 | Post-Chorus 1 | 알기 | 알 | TAP | repeated phrase pattern |
| 67.551 | 35.12 | Post-Chorus 1 | 알기 | 기 | TAP | repeated phrase pattern |
| 67.711 | 35.13 | Post-Chorus 1 | 전까지는 | 전 | TAP | repeated phrase pattern |
| 68.042 | 36.00 | Post-Chorus 1 | 전까지는 | 까 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 68.207 | 36.01~ | Post-Chorus 1 | 전까지는 | 지 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 68.378 | 36.03 | Post-Chorus 1 | 전까지는 | 는 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 68.669 | 36.05 | Post-Chorus 1 | 나 | 나 | TAP | repeated phrase pattern |
| 68.811 | 36.07~ | Post-Chorus 1 | 의미 | 의 | TAP | phrase start |
| 69.150 | 36.09~ | Post-Chorus 1 | 의미 | 미 | TAP | repeated phrase pattern |
| 69.377 | 36.11 | Post-Chorus 1 | 없었어 | 없 | TAP | repeated phrase pattern |
| 69.592 | 36.13 | Post-Chorus 1 | 없었어 | 었 | TAP | repeated phrase pattern |
| 69.879 | 37.00~ | Post-Chorus 1 | 없었어 | 어 | - | fast pair, not clearly enunciated |
| 70.010 | 37.01 | Post-Chorus 1 | 전부 | 전 | TAP | repeated phrase pattern |
| 70.364 | 37.04 | Post-Chorus 1 | 전부 | 부 | TAP | repeated phrase pattern |
| 70.639 | 37.06 | Post-Chorus 1 | 다 | 다 | TAP | repeated phrase pattern |
| 70.877 | 37.08 | Post-Chorus 1 | 내 | 내 | TAP | phrase start |
| 71.141 | 37.10 | Post-Chorus 1 | 맘이 | 맘 | TAP | repeated phrase pattern |
| 71.377 | 37.12 | Post-Chorus 1 | 맘이 | 이 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 71.586 | 37.14 | Post-Chorus 1 | 끝이 | 끝 | TAP | repeated phrase pattern |
| 71.869 | 38.00~ | Post-Chorus 1 | 끝이 | 이 | - | timing uncertain (no clear onset) |
| 72.102 | 38.02~ | Post-Chorus 1 | 없는 | 없 | TAP | repeated phrase pattern |
| 72.291 | 38.04 | Post-Chorus 1 | 없는 | 는 | TAP | repeated phrase pattern |
| 72.497 | 38.06 | Post-Chorus 1 | 걸 | 걸 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 72.761 | 38.08 | Post-Chorus 1 | I | i | TAP | phrase start |
| 73.098 | 38.11 | Post-Chorus 1 | know | know | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 73.272 | 38.12 | Post-Chorus 1 | I | i | TAP | word start, on the beat |
| 73.597 | 38.15 | Post-Chorus 1 | know | know | TAP | word start |
| 73.829 | 39.01 | Post-Chorus 1 | I'm | i'm | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 74.148 | 39.04 | Post-Chorus 1 | going | go | TAP | word start, on the beat |
| 74.308 | 39.05 | Post-Chorus 1 | going | ing | - | fast pair, not clearly enunciated |
| 74.436 | 39.06 | Post-Chorus 1 | crazy | cra | TAP | word start |
| 74.653 | 39.08 | Post-Chorus 1 | crazy | zy | TAP | clear syllable, on the beat |
| 74.836 | 39.10~ | Post-Chorus 1 | right? | right | TAP | word start |
| 75.266 | 39.13 | Verse 2 | 어디서든 | 어 | TAP | phrase start |
| 75.521 | 39.15 | Verse 2 | 어디서든 | 디 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 75.759 | 40.01~ | Verse 2 | 어디서든 | 서 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 75.957 | 40.03 | Verse 2 | 어디서든 | 든 | TAP | clear syllable |
| 76.172 | 40.05 | Verse 2 | 몇 | 몇 | TAP | word start |
| 76.560 | 40.08 | Verse 2 | 번이든 | 번 | TAP | word start, on the beat |
| 76.691 | 40.09 | Verse 2 | 번이든 | 이 | - | fast pair, not clearly enunciated |
| 76.906 | 40.11 | Verse 2 | 번이든 | 든 | TAP | clear syllable |
| 77.077 | 40.13~ | Verse 2 | There | there | TAP | phrase start |
| 77.472 | 41.00 | Verse 2 | ain't | ain't | TAP | word start, on the beat |
| 77.634 | 41.01 | Verse 2 | nothing | noth | - | fast pair, not clearly enunciated |
| 77.748 | 41.02 | Verse 2 | nothing | ing | - | fast pair, not clearly enunciated |
| 77.855 | 41.03 | Verse 2 | else | else | TAP | word start |
| 78.040 | 41.05~ | Verse 2 | that | that | TAP | word start |
| 78.093 | 41.05 | Verse 2 | I | i | TAP | word start |
| 78.287 | 41.07 | Verse 2 | would | would | - | fast pair, not clearly enunciated |
| 78.398 | 41.08 | Verse 2 | hold | hold | TAP | word start, on the beat |
| 78.583 | 41.09 | Verse 2 | on | on | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 78.792 | 41.11 | Verse 2 | to | to | TAP | word start |
| 79.028 | 41.13 | Verse 2 | I | i | TAP | phrase start |
| 79.512 | 42.01 | Verse 2 | hear | hear | TAP | word start |
| 79.628 | 42.02 | Verse 2 | his | his | - | fast pair, not clearly enunciated |
| 79.776 | 42.03~ | Verse 2 | voice | voice | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 80.023 | 42.05~ | Verse 2 | through | through | TAP | word start |
| 80.351 | 42.08 | Verse 2 | all | all | TAP | word start, on the beat |
| 80.563 | 42.10 | Verse 2 | the | the | TAP | word start |
| 80.720 | 42.11~ | Verse 2 | noise | noise | TAP | word start |
| 80.908 | 42.13 | Verse 2 | 잠시라도 | 잠 | TAP | phrase start |
| 81.045 | 42.14 | Verse 2 | 잠시라도 | 시 | - | fast pair, not clearly enunciated |
| 81.271 | 43.00 | Verse 2 | 잠시라도 | 라 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 81.448 | 43.02~ | Verse 2 | 잠시라도 | 도 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 81.579 | 43.03~ | Verse 2 | 내 | 내 | - | fast pair, not clearly enunciated |
| 81.738 | 43.04 | Verse 2 | 손 | 손 | TAP | word start, on the beat |
| 81.898 | 43.05 | Verse 2 | 놓지 | 놓 | - | fast pair, not clearly enunciated |
| 82.072 | 43.07 | Verse 2 | 놓지 | 지 | TAP | clear syllable |
| 82.167 | 43.08~ | Verse 2 | 마 | 마 | - | within 105 ms of a tapped syllable (min gap) |
| 82.299 | 43.09 | Verse 2 | no | no | - | fast pair, not clearly enunciated |
| 82.452 | 43.10 | Verse 2 | no | no | TAP | word start |
| 82.711 | 43.12 | Verse 2 | 걱정 | 걱 | TAP | phrase start |
| 82.853 | 43.13~ | Verse 2 | 걱정 | 정 | - | fast pair, not clearly enunciated |
| 83.161 | 44.00 | Verse 2 | 없잖아 | 없 | TAP | word start, on the beat |
| 83.326 | 44.01~ | Verse 2 | 없잖아 | 잖 | - | fast pair, not clearly enunciated |
| 83.747 | 44.05 | Verse 2 | 없잖아 | 아 | - | timing uncertain (no clear onset) |
| 84.049 | 44.08~ | Verse 2 | 'Cause | cause | TAP | phrase start |
| 84.641 | 44.13~ | Verse 2 | I | i | - | fast pair, not clearly enunciated |
| 84.809 | 44.14 | Verse 2 | got | got | TAP | word start |
| 85.033 | 45.00 | Verse 2 | someone | some | TAP | word start, on the beat |
| 85.314 | 45.02 | Verse 2 | someone | one | TAP | clear syllable |
| 86.464 | 45.12 | Verse 2 | 혼자라도 | 혼 | TAP | phrase start |
| 86.568 | 45.13 | Verse 2 | 혼자라도 | 자 | - | within 105 ms of a tapped syllable (min gap) |
| 86.705 | 45.14 | Verse 2 | 혼자라도 | 라 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 86.937 | 46.00 | Verse 2 | 혼자라도 | 도 | TAP | clear syllable, on the beat |
| 87.105 | 46.01~ | Verse 2 | 괜찮아 | 괜 | - | fast pair, not clearly enunciated |
| 87.245 | 46.03~ | Verse 2 | 괜찮아 | 찮 | - | fast pair, not clearly enunciated |
| 87.387 | 46.04 | Verse 2 | 괜찮아 | 아 | TAP | clear syllable, on the beat |
| 87.575 | 46.05~ | Verse 2 | 'Cause | cause | TAP | phrase start |
| 88.394 | 46.12 | Verse 2 | I | i | TAP | word start, on the beat |
| 88.583 | 46.14 | Verse 2 | love | love | TAP | word start |
| 88.940 | 47.01 | Verse 2 | someone | some | TAP | word start |
| 89.302 | 47.04 | Verse 2 | someone | one | TAP | clear syllable, on the beat |
| 89.540 | 47.06 | Pre-Chorus 2 | They | they | TAP | phrase start |
| 90.002 | 47.10 | Pre-Chorus 2 | keep | keep | - | ad-lib under the lead: kept sparse |
| 90.135 | 47.11 | Pre-Chorus 2 | on | on | - | ad-lib under the lead: kept sparse |
| 90.246 | 47.12 | Pre-Chorus 2 | asking | ask | - | ad-lib under the lead: kept sparse |
| 90.300 | 47.12~ | Pre-Chorus 2 | asking | ing | - | ad-lib under the lead: kept sparse |
| 90.394 | 47.13 | Pre-Chorus 2 | me | me | - | fast pair, not clearly enunciated |
| 90.545 | 47.15~ | Pre-Chorus 2 | who | who | TAP | repeated phrase pattern |
| 90.646 | 47.15~ | Pre-Chorus 2 | is | is | - | within 105 ms of a tapped syllable (min gap) |
| 90.809 | 48.01 | Pre-Chorus 2 | he? | he | - | ad-lib under the lead: kept sparse |
| 91.061 | 48.03 | Pre-Chorus 2 | 멀리든 | 멀 | TAP | phrase start |
| 91.563 | 48.07 | Pre-Chorus 2 | 멀리든 | 리 | TAP | repeated phrase pattern |
| 91.903 | 48.10 | Pre-Chorus 2 | 멀리든 | 든 | TAP | repeated phrase pattern |
| 92.196 | 48.13~ | Pre-Chorus 2 | 언제든지 | 언 | TAP | repeated phrase pattern |
| 92.420 | 48.14~ | Pre-Chorus 2 | 언제든지 | 제 | TAP | repeated phrase pattern |
| 92.617 | 49.00 | Pre-Chorus 2 | 언제든지 | 든 | TAP | repeated phrase pattern |
| 92.881 | 49.02 | Pre-Chorus 2 | 언제든지 | 지 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 93.119 | 49.04 | Pre-Chorus 2 | 달려와 | 달 | TAP | repeated phrase pattern |
| 93.317 | 49.06 | Pre-Chorus 2 | 달려와 | 려 | TAP | repeated phrase pattern |
| 93.549 | 49.08 | Pre-Chorus 2 | 달려와 | 와 | - | fast pair, not clearly enunciated |
| 93.682 | 49.09 | Pre-Chorus 2 | They | they | TAP | phrase start |
| 93.810 | 49.10 | Pre-Chorus 2 | keep | keep | - | fast pair, not clearly enunciated |
| 93.909 | 49.11 | Pre-Chorus 2 | on | on | - | ad-lib under the lead: kept sparse |
| 94.045 | 49.12 | Pre-Chorus 2 | asking | ask | - | ad-lib under the lead: kept sparse |
| 94.138 | 49.13 | Pre-Chorus 2 | asking | ing | - | within 105 ms of a tapped syllable (min gap) |
| 94.222 | 49.14 | Pre-Chorus 2 | me | me | TAP | repeated phrase pattern |
| 94.286 | 49.14 | Pre-Chorus 2 | who | who | TAP | repeated phrase pattern |
| 94.498 | 50.00 | Pre-Chorus 2 | is | is | - | ad-lib under the lead: kept sparse |
| 94.640 | 50.01 | Pre-Chorus 2 | he? | he | - | ad-lib under the lead: kept sparse |
| 95.046 | 50.05~ | Pre-Chorus 2 | 바쁜 | 바 | TAP | phrase start |
| 95.424 | 50.08 | Pre-Chorus 2 | 바쁜 | 쁜 | TAP | repeated phrase pattern |
| 95.807 | 50.11 | Pre-Chorus 2 | 척도 | 척 | TAP | repeated phrase pattern |
| 95.917 | 50.12 | Pre-Chorus 2 | 척도 | 도 | - | fast pair, not clearly enunciated |
| 96.152 | 50.14 | Pre-Chorus 2 | 없이 | 없 | TAP | repeated phrase pattern |
| 96.344 | 51.00~ | Pre-Chorus 2 | 없이 | 이 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 96.532 | 51.01 | Pre-Chorus 2 | 넌 | 넌 | TAP | repeated phrase pattern |
| 96.863 | 51.04 | Pre-Chorus 2 | 나타나 | 나 | TAP | repeated phrase pattern |
| 97.096 | 51.06 | Pre-Chorus 2 | 나타나 | 타 | TAP | repeated phrase pattern |
| 97.455 | 51.09 | Pre-Chorus 2 | 나타나 | 나 | TAP | repeated phrase pattern |
| 97.691 | 51.11 | Pre-Chorus 2 | They | they | TAP | phrase start |
| 97.798 | 51.12 | Pre-Chorus 2 | keep | keep | - | fast pair, not clearly enunciated |
| 97.935 | 51.13 | Pre-Chorus 2 | on | on | - | ad-lib under the lead: kept sparse |
| 97.961 | 51.13 | Pre-Chorus 2 | asking | ask | - | fast pair, not clearly enunciated |
| 97.990 | 51.14~ | Pre-Chorus 2 | asking | ing | - | fast pair, not clearly enunciated |
| 98.025 | 51.14 | Pre-Chorus 2 | me | me | - | within 105 ms of a tapped syllable (min gap) |
| 98.123 | 51.15 | Pre-Chorus 2 | who | who | TAP | repeated phrase pattern |
| 98.254 | 52.00 | Pre-Chorus 2 | is | is | - | fast pair, not clearly enunciated |
| 98.364 | 52.01 | Pre-Chorus 2 | he? | he | - | ad-lib under the lead: kept sparse |
| 98.767 | 52.04 | Pre-Chorus 2 | 이게 | 이 | TAP | phrase start |
| 99.188 | 52.08 | Pre-Chorus 2 | 이게 | 게 | TAP | repeated phrase pattern |
| 99.360 | 52.09 | Pre-Chorus 2 | 말이 | 말 | TAP | repeated phrase pattern |
| 99.516 | 52.10~ | Pre-Chorus 2 | 말이 | 이 | - | fast pair, not clearly enunciated |
| 99.763 | 52.13~ | Pre-Chorus 2 | 되니 | 되 | TAP | repeated phrase pattern |
| 100.027 | 52.15 | Pre-Chorus 2 | 되니 | 니 | TAP | repeated phrase pattern |
| 100.338 | 53.01~ | Pre-Chorus 2 | 난 | 난 | TAP | repeated phrase pattern |
| 100.651 | 53.04 | Pre-Chorus 2 | 물어봐 | 물 | TAP | repeated phrase pattern |
| 100.912 | 53.06 | Pre-Chorus 2 | 물어봐 | 어 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 101.118 | 53.08 | Pre-Chorus 2 | 물어봐 | 봐 | TAP | repeated phrase pattern |
| 101.377 | 53.10 | Pre-Chorus 2 | They | they | TAP | phrase start |
| 101.592 | 53.12 | Pre-Chorus 2 | keep | keep | - | ad-lib under the lead: kept sparse |
| 101.700 | 53.13 | Pre-Chorus 2 | on | on | - | fast pair, not clearly enunciated |
| 101.725 | 53.13 | Pre-Chorus 2 | asking | ask | - | fast pair, not clearly enunciated |
| 101.742 | 53.13~ | Pre-Chorus 2 | asking | ing | - | within 105 ms of a tapped syllable (min gap) |
| 101.757 | 53.13~ | Pre-Chorus 2 | me | me | - | within 105 ms of a tapped syllable (min gap) |
| 101.844 | 53.14 | Pre-Chorus 2 | who | who | TAP | repeated phrase pattern |
| 102.004 | 54.00~ | Pre-Chorus 2 | is | is | - | fast pair, not clearly enunciated |
| 102.120 | 54.01~ | Pre-Chorus 2 | he? | he | - | ad-lib under the lead: kept sparse |
| 102.497 | 54.04 | Pre-Chorus 2 | 너는 | 너 | TAP | phrase start |
| 102.991 | 54.08 | Pre-Chorus 2 | 너는 | 는 | TAP | repeated phrase pattern |
| 103.321 | 54.11 | Pre-Chorus 2 | 말야 | 말 | TAP | repeated phrase pattern |
| 103.467 | 54.12 | Pre-Chorus 2 | 말야 | 야 | TAP | repeated phrase pattern |
| 103.710 | 54.14 | Pre-Chorus 2 | he's | he's | TAP | repeated phrase pattern |
| 103.908 | 55.00 | Pre-Chorus 2 | the | the | TAP | repeated phrase pattern |
| 104.082 | 55.01 | Pre-Chorus 2 | one | one | TAP | repeated phrase pattern |
| 104.183 | 55.02 | Pre-Chorus 2 | that's | that's | - | within 105 ms of a tapped syllable (min gap) |
| 104.308 | 55.03 | Pre-Chorus 2 | living | liv | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 104.430 | 55.04 | Pre-Chorus 2 | living | ing | - | timing uncertain (no clear onset) |
| 104.471 | 55.04~ | Pre-Chorus 2 | in | in | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 104.657 | 55.06 | Pre-Chorus 2 | my | my | TAP | repeated phrase pattern |
| 104.781 | 55.07 | Pre-Chorus 2 | system | sys | TAP | repeated phrase pattern |
| 104.932 | 55.08~ | Pre-Chorus 2 | system | tem | - | fast pair, not clearly enunciated |
| 105.127 | 55.10 | Pre-Chorus 2 | baby | ba | TAP | repeated phrase pattern |
| 105.371 | 55.12 | Pre-Chorus 2 | baby | by | TAP | repeated phrase pattern |
| 105.538 | 55.13~ | Chorus 2 | Oh | oh | TAP | same as line 21 (copied vocal, mirrored) |
| 105.860 | 56.00 | Chorus 2 | my | my | TAP | same as line 21 (copied vocal, mirrored) |
| 106.182 | 56.03 | Chorus 2 | oh | oh | TAP | same as line 21 (copied vocal, mirrored) |
| 106.298 | 56.04 | Chorus 2 | my | my | TAP | same as line 21 (copied vocal, mirrored) |
| 106.551 | 56.06 | Chorus 2 | God | god | TAP | same as line 21 (copied vocal, mirrored) |
| 106.893 | 56.09 | Chorus 2 | 예상했어 | 예 | TAP | same as line 21 (copied vocal, mirrored) |
| 107.375 | 56.13 | Chorus 2 | 예상했어 | 상 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 107.703 | 57.00 | Chorus 2 | 예상했어 | 했 | TAP | same as line 21 (copied vocal, mirrored) |
| 107.851 | 57.01 | Chorus 2 | 예상했어 | 어 | - | fast pair, not clearly enunciated |
| 108.095 | 57.03 | Chorus 2 | 나 | 나 | TAP | same as line 21 (copied vocal, mirrored) |
| 108.316 | 57.05 | Chorus 2 | I | i | TAP | same as line 22 (copied vocal, mirrored) |
| 108.676 | 57.08 | Chorus 2 | was | was | TAP | same as line 22 (copied vocal, mirrored) |
| 108.992 | 57.11 | Chorus 2 | really | real | TAP | same as line 22 (copied vocal, mirrored) |
| 109.096 | 57.12~ | Chorus 2 | really | ly | - | within 105 ms of a tapped syllable (min gap) |
| 109.273 | 57.13 | Chorus 2 | hoping | hop | TAP | same as line 22 (copied vocal, mirrored) |
| 109.596 | 58.00 | Chorus 2 | hoping | ing | TAP | same as line 22 (copied vocal, mirrored) |
| 109.880 | 58.02 | Chorus 2 | that | that | TAP | same as line 22 (copied vocal, mirrored) |
| 110.191 | 58.05 | Chorus 2 | he | he | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 110.391 | 58.07~ | Chorus 2 | will | will | TAP | same as line 22 (copied vocal, mirrored) |
| 110.693 | 58.09 | Chorus 2 | come | come | TAP | same as line 22 (copied vocal, mirrored) |
| 111.209 | 58.13~ | Chorus 2 | through | through | TAP | same as line 22 (copied vocal, mirrored) |
| 112.800 | 59.11 | Chorus 2 | Oh | oh | TAP | same as line 23 (copied vocal, mirrored) |
| 113.372 | 60.00 | Chorus 2 | my | my | TAP | same as line 23 (copied vocal, mirrored) |
| 113.645 | 60.02 | Chorus 2 | oh | oh | TAP | same as line 23 (copied vocal, mirrored) |
| 113.862 | 60.04 | Chorus 2 | my | my | TAP | same as line 23 (copied vocal, mirrored) |
| 114.115 | 60.06 | Chorus 2 | God | god | TAP | same as line 23 (copied vocal, mirrored) |
| 114.495 | 60.09 | Chorus 2 | 단 | 단 | TAP | same as line 23 (copied vocal, mirrored) |
| 114.803 | 60.12 | Chorus 2 | 너뿐이야 | 너 | TAP | same as line 23 (copied vocal, mirrored) |
| 115.067 | 60.14 | Chorus 2 | 너뿐이야 | 뿐 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 115.302 | 61.00 | Chorus 2 | 너뿐이야 | 이 | TAP | same as line 23 (copied vocal, mirrored) |
| 115.523 | 61.02 | Chorus 2 | 너뿐이야 | 야 | TAP | same as line 23 (copied vocal, mirrored) |
| 115.717 | 61.04 | Chorus 2 | Asking | ask | TAP | same as line 24 (copied vocal, mirrored) |
| 116.167 | 61.07~ | Chorus 2 | Asking | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 116.486 | 61.10 | Chorus 2 | all | all | TAP | same as line 24 (copied vocal, mirrored) |
| 116.771 | 61.13~ | Chorus 2 | the | the | TAP | same as line 24 (copied vocal, mirrored) |
| 116.971 | 61.14 | Chorus 2 | time | time | TAP | same as line 24 (copied vocal, mirrored) |
| 117.299 | 62.01 | Chorus 2 | about | a | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 117.450 | 62.02~ | Chorus 2 | about | bout | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 117.665 | 62.04 | Chorus 2 | what | what | TAP | same as line 24 (copied vocal, mirrored) |
| 117.935 | 62.06~ | Chorus 2 | I | i | TAP | same as line 24 (copied vocal, mirrored) |
| 118.268 | 62.09 | Chorus 2 | should | should | TAP | same as line 24 (copied vocal, mirrored) |
| 118.622 | 62.12 | Chorus 2 | do | do | TAP | same as line 24 (copied vocal, mirrored) |
| 119.937 | 63.07~ | Post-Chorus 2 | No | no | TAP | same as line 25 (copied vocal, mirrored) |
| 120.245 | 63.10 | Post-Chorus 2 | I | i | TAP | same as line 25 (copied vocal, mirrored) |
| 120.506 | 63.12 | Post-Chorus 2 | can | can | TAP | same as line 25 (copied vocal, mirrored) |
| 120.672 | 63.14~ | Post-Chorus 2 | never | nev | TAP | same as line 25 (copied vocal, mirrored) |
| 120.869 | 63.15 | Post-Chorus 2 | never | er | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 121.087 | 64.01 | Post-Chorus 2 | let | let | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 121.403 | 64.04 | Post-Chorus 2 | him | him | TAP | same as line 25 (copied vocal, mirrored) |
| 121.635 | 64.06 | Post-Chorus 2 | go | go | TAP | same as line 25 (copied vocal, mirrored) |
| 121.867 | 64.08 | Post-Chorus 2 | 너만 | 너 | TAP | same as line 26 (copied vocal, mirrored) |
| 122.117 | 64.10 | Post-Chorus 2 | 너만 | 만 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 122.399 | 64.12 | Post-Chorus 2 | 생각나 | 생 | TAP | same as line 26 (copied vocal, mirrored) |
| 122.619 | 64.14 | Post-Chorus 2 | 생각나 | 각 | TAP | same as line 26 (copied vocal, mirrored) |
| 122.848 | 65.00 | Post-Chorus 2 | 생각나 | 나 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 123.081 | 65.02 | Post-Chorus 2 | twenty-four | twen | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 123.316 | 65.04 | Post-Chorus 2 | twenty-four | ty | TAP | same as line 26 (copied vocal, mirrored) |
| 123.461 | 65.05 | Post-Chorus 2 | twenty-four | four | - | within 105 ms of a tapped syllable (min gap) |
| 123.554 | 65.06 | Post-Chorus 2 | 난 | 난 | TAP | same as line 27 (copied vocal, mirrored) |
| 124.027 | 65.10 | Post-Chorus 2 | 행운아야 | 행 | TAP | same as line 27 (copied vocal, mirrored) |
| 124.300 | 65.12 | Post-Chorus 2 | 행운아야 | 운 | TAP | same as line 27 (copied vocal, mirrored) |
| 124.500 | 65.14 | Post-Chorus 2 | 행운아야 | 아 | TAP | same as line 27 (copied vocal, mirrored) |
| 124.767 | 66.00 | Post-Chorus 2 | 행운아야 | 야 | TAP | same as line 27 (copied vocal, mirrored) |
| 124.985 | 66.02 | Post-Chorus 2 | 정말로 | 정 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 125.234 | 66.04 | Post-Chorus 2 | 정말로 | 말 | TAP | same as line 27 (copied vocal, mirrored) |
| 125.452 | 66.06 | Post-Chorus 2 | 정말로 | 로 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 125.684 | 66.08 | Post-Chorus 2 | I | i | TAP | same as line 28 (copied vocal, mirrored) |
| 125.864 | 66.10~ | Post-Chorus 2 | know | know | TAP | same as line 28 (copied vocal, mirrored) |
| 126.233 | 66.13 | Post-Chorus 2 | I | i | TAP | same as line 28 (copied vocal, mirrored) |
| 126.372 | 66.14 | Post-Chorus 2 | know | know | TAP | same as line 28 (copied vocal, mirrored) |
| 127.520 | 67.08~ | Post-Chorus 2 | 널 | 널 | TAP | phrase start |
| 127.868 | 67.11~ | Post-Chorus 2 | 알기 | 알 | TAP | repeated phrase pattern |
| 128.022 | 67.12 | Post-Chorus 2 | 알기 | 기 | TAP | repeated phrase pattern |
| 128.178 | 67.13 | Post-Chorus 2 | 전까지는 | 전 | TAP | repeated phrase pattern |
| 128.297 | 67.14 | Post-Chorus 2 | 전까지는 | 까 | - | fast pair, not clearly enunciated |
| 128.512 | 68.00 | Post-Chorus 2 | 전까지는 | 지 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 128.701 | 68.02~ | Post-Chorus 2 | 전까지는 | 는 | - | fast pair, not clearly enunciated |
| 128.849 | 68.03 | Post-Chorus 2 | 나 | 나 | TAP | repeated phrase pattern |
| 129.283 | 68.07~ | Post-Chorus 2 | 의미 | 의 | TAP | same as line 30 (copied vocal, mirrored) |
| 129.623 | 68.09~ | Post-Chorus 2 | 의미 | 미 | TAP | same as line 30 (copied vocal, mirrored) |
| 129.849 | 68.11 | Post-Chorus 2 | 없었어 | 없 | TAP | same as line 30 (copied vocal, mirrored) |
| 130.064 | 68.13 | Post-Chorus 2 | 없었어 | 었 | TAP | same as line 30 (copied vocal, mirrored) |
| 130.351 | 69.00~ | Post-Chorus 2 | 없었어 | 어 | - | fast pair, not clearly enunciated |
| 130.482 | 69.01 | Post-Chorus 2 | 전부 | 전 | TAP | same as line 30 (copied vocal, mirrored) |
| 130.836 | 69.04 | Post-Chorus 2 | 전부 | 부 | TAP | same as line 30 (copied vocal, mirrored) |
| 131.112 | 69.06 | Post-Chorus 2 | 다 | 다 | TAP | same as line 30 (copied vocal, mirrored) |
| 131.350 | 69.08 | Post-Chorus 2 | 내 | 내 | TAP | same as line 31 (copied vocal, mirrored) |
| 131.614 | 69.10 | Post-Chorus 2 | 맘이 | 맘 | TAP | same as line 31 (copied vocal, mirrored) |
| 131.849 | 69.12 | Post-Chorus 2 | 맘이 | 이 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 132.058 | 69.14 | Post-Chorus 2 | 끝이 | 끝 | TAP | same as line 31 (copied vocal, mirrored) |
| 132.341 | 70.00~ | Post-Chorus 2 | 끝이 | 이 | - | timing uncertain (no clear onset) |
| 132.575 | 70.02~ | Post-Chorus 2 | 없는 | 없 | TAP | same as line 31 (copied vocal, mirrored) |
| 132.763 | 70.04 | Post-Chorus 2 | 없는 | 는 | TAP | same as line 31 (copied vocal, mirrored) |
| 132.969 | 70.06 | Post-Chorus 2 | 걸 | 걸 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 133.235 | 70.08 | Post-Chorus 2 | I | i | TAP | phrase start |
| 133.606 | 70.11 | Post-Chorus 2 | know | know | TAP | repeated phrase pattern |
| 133.841 | 70.13 | Post-Chorus 2 | I | i | TAP | repeated phrase pattern |
| 133.949 | 70.14 | Post-Chorus 2 | know | know | TAP | repeated phrase pattern |
| 134.279 | 71.01 | Post-Chorus 2 | He's | he's | TAP | phrase start |
| 134.430 | 71.02 | Post-Chorus 2 | the | the | - | fast pair, not clearly enunciated |
| 134.577 | 71.03~ | Post-Chorus 2 | one | one | - | within 105 ms of a tapped syllable (min gap) |
| 134.680 | 71.04 | Post-Chorus 2 | that's | that's | TAP | word start, on the beat |
| 134.723 | 71.05~ | Post-Chorus 2 | living | liv | - | within 105 ms of a tapped syllable (min gap) |
| 134.793 | 71.05 | Post-Chorus 2 | living | ing | - | fast pair, not clearly enunciated |
| 134.895 | 71.06 | Post-Chorus 2 | in | in | - | ad-lib under the lead: kept sparse |
| 134.999 | 71.07 | Post-Chorus 2 | my | my | - | ad-lib under the lead: kept sparse |
| 135.092 | 71.08 | Post-Chorus 2 | system | sys | - | fast pair, not clearly enunciated |
| 135.214 | 71.09 | Post-Chorus 2 | system | tem | TAP | clear syllable |
| 135.284 | 71.09 | Interlude | Baby | ba | TAP | phrase start |
| 135.705 | 71.13 | Interlude | Baby | by | TAP | title hook: every syllable |
| 135.986 | 71.15 | Interlude | babe | babe | TAP | title hook: every syllable |
| 136.395 | 72.03 | Interlude | baby | ba | TAP | title hook: every syllable |
| 137.500 | 72.12 | Interlude | baby | by | TAP | title hook: every syllable |
| 138.282 | 73.03 | Interlude | baby | ba | TAP | title hook: every syllable |
| 138.987 | 73.09 | Interlude | baby | by | TAP | title hook: every syllable |
| 139.849 | 74.00 | instrumental |  |  | TAP | no vocal: snare layer (previous rule-based chart) |
| 140.563 | 74.06 | instrumental |  |  | TAP | no vocal: kick layer (previous rule-based chart) |
| 140.793 | 74.08 | instrumental |  |  | TAP | no vocal: snare layer (previous rule-based chart) |
| 141.480 | 74.14 | Interlude | I'm | i'm | TAP | phrase start |
| 142.168 | 75.04~ | Interlude | going | go | TAP | word start |
| 142.343 | 75.05 | Interlude | going | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 142.569 | 75.07 | Interlude | crazy | cra | TAP | title hook: every syllable |
| 142.743 | 75.08~ | Interlude | crazy | zy | TAP | title hook: every syllable |
| 142.911 | 75.10 | Interlude | right? | right | - | fast pair, not clearly enunciated |
| 143.277 | 75.13 | Interlude | Baby | ba | TAP | phrase start |
| 143.684 | 76.00~ | Interlude | Baby | by | TAP | title hook: every syllable |
| 143.953 | 76.03 | Interlude | baby | ba | TAP | title hook: every syllable |
| 144.850 | 76.10 | Interlude | baby | by | TAP | title hook: every syllable |
| 145.762 | 77.02 | Interlude | babe | babe | - | too faint to hear as a new syllable |
| 145.976 | 77.04 | Interlude | baby | ba | TAP | title hook: every syllable |
| 146.072 | 77.05 | Interlude | baby | by | - | within 105 ms of a tapped syllable (min gap) |
| 148.354 | 78.08 | instrumental |  |  | TAP | no vocal: snare layer (previous rule-based chart) |
| 149.442 | 79.01 | Interlude | 너와 | 너 | TAP | phrase start |
| 149.738 | 79.04 | Interlude | 너와 | 와 | TAP | clear syllable, on the beat |
| 150.136 | 79.07 | Interlude | 나 | 나 | TAP | word start |
| 150.728 | 79.12 | Bridge | My | my | TAP | phrase start |
| 150.960 | 79.14 | Bridge | heart | heart | TAP | word start |
| 151.390 | 80.02 | Bridge | is | is | - | fast pair, not clearly enunciated |
| 151.517 | 80.03 | Bridge | glowing | glow | TAP | word start |
| 151.796 | 80.05 | Bridge | glowing | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 152.054 | 80.07 | Bridge | it's | it's | - | fast pair, not clearly enunciated |
| 152.162 | 80.08 | Bridge | glowing | glow | TAP | word start, on the beat |
| 152.437 | 80.11~ | Bridge | glowing | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 152.745 | 80.13 | Bridge | up | up | TAP | word start |
| 153.433 | 81.03 | Bridge | Glow | glow | TAP | phrase start |
| 153.800 | 81.06 | Bridge | glow | glow | TAP | word start |
| 154.362 | 81.11 | Bridge | 너랑만 | 너 | TAP | phrase start |
| 154.736 | 81.14 | Bridge | 너랑만 | 랑 | TAP | clear syllable |
| 155.012 | 82.00~ | Bridge | 너랑만 | 만 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 155.241 | 82.02 | Bridge | 있으면 | 있 | TAP | word start |
| 155.447 | 82.04 | Bridge | 있으면 | 으 | TAP | clear syllable, on the beat |
| 155.552 | 82.05 | Bridge | 있으면 | 면 | - | within 105 ms of a tapped syllable (min gap) |
| 155.680 | 82.06 | Bridge | 무서울 | 무 | TAP | word start |
| 156.019 | 82.09 | Bridge | 무서울 | 서 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 156.388 | 82.12 | Bridge | 무서울 | 울 | TAP | clear syllable, on the beat |
| 156.634 | 82.14 | Bridge | 게 | 게 | TAP | word start |
| 156.896 | 83.00 | Bridge | 없어 | 없 | TAP | word start, on the beat |
| 157.224 | 83.03 | Bridge | 없어 | 어 | - | too faint to hear as a new syllable |
| 157.613 | 83.06~ | Bridge | No | no | TAP | phrase start |
| 157.740 | 83.07~ | Bridge | no | no | - | fast pair, not clearly enunciated |
| 158.199 | 83.11~ | Bridge | 가득 | 가 | TAP | phrase start |
| 158.524 | 83.14 | Bridge | 가득 | 득 | TAP | clear syllable |
| 158.875 | 84.01 | Bridge | 메워진 | 메 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 159.223 | 84.04 | Bridge | 메워진 | 워 | TAP | clear syllable, on the beat |
| 159.459 | 84.06 | Bridge | 메워진 | 진 | TAP | clear syllable |
| 159.694 | 84.08 | Bridge | 다 | 다 | TAP | word start, on the beat |
| 159.827 | 84.09 | Bridge | 메워진 | 메 | - | fast pair, not clearly enunciated |
| 160.056 | 84.11 | Bridge | 메워진 | 워 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 160.451 | 84.14~ | Bridge | 메워진 | 진 | TAP | clear syllable |
| 160.710 | 85.01~ | Bridge | My | my | TAP | phrase start |
| 161.728 | 85.09 | Bridge | heart | heart | TAP | word start |
| 162.631 | 86.01 | Bridge | is | is | TAP | word start |
| 162.823 | 86.03~ | Bridge | glowing | glow | TAP | word start |
| 163.078 | 86.05 | Bridge | glowing | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 163.386 | 86.07 | Bridge | it'd | it'd | - | fast pair, not clearly enunciated |
| 163.505 | 86.08 | Bridge | be | be | TAP | word start, on the beat |
| 163.711 | 86.10 | Bridge | glowing | glow | TAP | word start |
| 164.010 | 86.13~ | Bridge | glowing | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 164.381 | 87.00 | Bridge | 'Cause | cause | - | too faint to hear as a new syllable |
| 164.959 | 87.05~ | Bridge | he | he | TAP | word start |
| 166.010 | 87.13~ | Chorus 3 | Oh | oh | TAP | same as line 21 (copied vocal, mirrored) |
| 166.333 | 88.00 | Chorus 3 | my | my | TAP | same as line 21 (copied vocal, mirrored) |
| 166.655 | 88.03 | Chorus 3 | oh | oh | TAP | same as line 21 (copied vocal, mirrored) |
| 166.771 | 88.04 | Chorus 3 | my | my | TAP | same as line 21 (copied vocal, mirrored) |
| 167.023 | 88.06 | Chorus 3 | God | god | TAP | same as line 21 (copied vocal, mirrored) |
| 167.366 | 88.09 | Chorus 3 | 예상했어 | 예 | TAP | same as line 21 (copied vocal, mirrored) |
| 167.848 | 88.13 | Chorus 3 | 예상했어 | 상 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 168.176 | 89.00 | Chorus 3 | 예상했어 | 했 | TAP | same as line 21 (copied vocal, mirrored) |
| 168.324 | 89.01 | Chorus 3 | 예상했어 | 어 | - | fast pair, not clearly enunciated |
| 168.567 | 89.03 | Chorus 3 | 나 | 나 | TAP | same as line 21 (copied vocal, mirrored) |
| 168.788 | 89.05 | Chorus 3 | I | i | TAP | same as line 22 (copied vocal, mirrored) |
| 169.148 | 89.08 | Chorus 3 | was | was | TAP | same as line 22 (copied vocal, mirrored) |
| 169.464 | 89.11 | Chorus 3 | really | real | TAP | same as line 22 (copied vocal, mirrored) |
| 169.569 | 89.12~ | Chorus 3 | really | ly | - | within 105 ms of a tapped syllable (min gap) |
| 169.746 | 89.13 | Chorus 3 | hoping | hop | TAP | same as line 22 (copied vocal, mirrored) |
| 170.068 | 90.00 | Chorus 3 | hoping | ing | TAP | same as line 22 (copied vocal, mirrored) |
| 170.353 | 90.02 | Chorus 3 | that | that | TAP | same as line 22 (copied vocal, mirrored) |
| 170.663 | 90.05 | Chorus 3 | he | he | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 170.863 | 90.07~ | Chorus 3 | will | will | TAP | same as line 22 (copied vocal, mirrored) |
| 171.165 | 90.09 | Chorus 3 | come | come | TAP | same as line 22 (copied vocal, mirrored) |
| 171.682 | 90.14~ | Chorus 3 | through | through | TAP | same as line 22 (copied vocal, mirrored) |
| 173.272 | 91.11 | Chorus 3 | Oh | oh | TAP | same as line 23 (copied vocal, mirrored) |
| 173.844 | 92.00 | Chorus 3 | my | my | TAP | same as line 23 (copied vocal, mirrored) |
| 174.117 | 92.02 | Chorus 3 | oh | oh | TAP | same as line 23 (copied vocal, mirrored) |
| 174.335 | 92.04 | Chorus 3 | my | my | TAP | same as line 23 (copied vocal, mirrored) |
| 174.587 | 92.06 | Chorus 3 | God | god | TAP | same as line 23 (copied vocal, mirrored) |
| 174.967 | 92.09 | Chorus 3 | 단 | 단 | TAP | same as line 23 (copied vocal, mirrored) |
| 175.275 | 92.12 | Chorus 3 | 너뿐이야 | 너 | TAP | same as line 23 (copied vocal, mirrored) |
| 175.539 | 92.14 | Chorus 3 | 너뿐이야 | 뿐 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 175.774 | 93.00 | Chorus 3 | 너뿐이야 | 이 | TAP | same as line 23 (copied vocal, mirrored) |
| 175.995 | 93.02 | Chorus 3 | 너뿐이야 | 야 | TAP | same as line 23 (copied vocal, mirrored) |
| 176.189 | 93.04 | Chorus 3 | Asking | ask | TAP | same as line 24 (copied vocal, mirrored) |
| 176.639 | 93.07~ | Chorus 3 | Asking | ing | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 176.959 | 93.10 | Chorus 3 | all | all | TAP | same as line 24 (copied vocal, mirrored) |
| 177.243 | 93.13~ | Chorus 3 | the | the | TAP | same as line 24 (copied vocal, mirrored) |
| 177.443 | 93.14 | Chorus 3 | time | time | TAP | same as line 24 (copied vocal, mirrored) |
| 177.771 | 94.01 | Chorus 3 | about | a | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 177.922 | 94.02~ | Chorus 3 | about | bout | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 178.137 | 94.04 | Chorus 3 | what | what | TAP | same as line 24 (copied vocal, mirrored) |
| 178.407 | 94.06~ | Chorus 3 | I | i | TAP | same as line 24 (copied vocal, mirrored) |
| 178.741 | 94.09 | Chorus 3 | should | should | TAP | same as line 24 (copied vocal, mirrored) |
| 179.095 | 94.12 | Chorus 3 | do | do | TAP | same as line 24 (copied vocal, mirrored) |
| 179.709 | 95.01~ | Post-Chorus 3 | No | no | TAP | phrase start |
| 180.432 | 95.08~ | Post-Chorus 3 | I | i | TAP | repeated phrase pattern |
| 180.812 | 95.11 | Post-Chorus 3 | can | can | TAP | repeated phrase pattern |
| 181.303 | 95.15 | Post-Chorus 3 | never | nev | TAP | repeated phrase pattern |
| 181.428 | 96.00 | Post-Chorus 3 | never | er | - | fast pair, not clearly enunciated |
| 181.596 | 96.01~ | Post-Chorus 3 | let | let | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 181.935 | 96.04 | Post-Chorus 3 | him | him | TAP | repeated phrase pattern |
| 182.147 | 96.06 | Post-Chorus 3 | go | go | TAP | repeated phrase pattern |
| 182.487 | 96.09 | Post-Chorus 3 | He's | he's | TAP | phrase start |
| 182.632 | 96.10 | Post-Chorus 3 | right | right | - | fast pair, not clearly enunciated |
| 182.937 | 96.13 | Post-Chorus 3 | there | there | - | fast pair, not clearly enunciated |
| 183.091 | 96.14 | Post-Chorus 3 | for | for | TAP | word start |
| 183.326 | 97.00 | Post-Chorus 3 | me | me | TAP | word start, on the beat |
| 183.552 | 97.02 | Post-Chorus 3 | twenty-four | twen | TAP | word start |
| 183.744 | 97.04~ | Post-Chorus 3 | twenty-four | ty | TAP | clear syllable |
| 183.744 | 97.04~ | Post-Chorus 3 | 난 | 난 | TAP | phrase start |
| 183.842 | 97.04~ | Post-Chorus 3 | twenty-four | four | - | within 105 ms of a tapped syllable (min gap) |
| 184.025 | 97.06 | Post-Chorus 3 | 행운아야 | 행 | TAP | repeated phrase pattern |
| 184.536 | 97.10~ | Post-Chorus 3 | 행운아야 | 운 | TAP | repeated phrase pattern |
| 184.870 | 97.13 | Post-Chorus 3 | 행운아야 | 아 | TAP | repeated phrase pattern |
| 185.175 | 98.00 | Post-Chorus 3 | 행운아야 | 야 | TAP | repeated phrase pattern |
| 185.401 | 98.02 | Post-Chorus 3 | 정말로 | 정 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 185.691 | 98.04 | Post-Chorus 3 | 정말로 | 말 | TAP | repeated phrase pattern |
| 185.976 | 98.07~ | Post-Chorus 3 | 정말로 | 로 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 186.220 | 98.09~ | Post-Chorus 3 | I | i | TAP | phrase start |
| 186.388 | 98.10 | Post-Chorus 3 | know | know | TAP | repeated phrase pattern |
| 186.640 | 98.12 | Post-Chorus 3 | I | i | TAP | repeated phrase pattern |
| 186.916 | 98.14~ | Post-Chorus 3 | know | know | TAP | repeated phrase pattern |
| 187.172 | 99.01 | Post-Chorus 3 | 널 | 널 | TAP | phrase start |
| 187.755 | 99.06~ | Post-Chorus 3 | 알기 | 알 | TAP | repeated phrase pattern |
| 188.141 | 99.09 | Post-Chorus 3 | 알기 | 기 | TAP | repeated phrase pattern |
| 188.501 | 99.12 | Post-Chorus 3 | 전까지는 | 전 | TAP | repeated phrase pattern |
| 188.812 | 99.15~ | Post-Chorus 3 | 전까지는 | 까 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 188.986 | 100.00 | Post-Chorus 3 | 전까지는 | 지 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 189.151 | 100.01~ | Post-Chorus 3 | 전까지는 | 는 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 189.322 | 100.03 | Post-Chorus 3 | 나 | 나 | TAP | repeated phrase pattern |
| 189.703 | 100.06 | Post-Chorus 3 | 의미 | 의 | TAP | phrase start |
| 189.932 | 100.08 | Post-Chorus 3 | 의미 | 미 | TAP | repeated phrase pattern |
| 190.155 | 100.10 | Post-Chorus 3 | 없었어 | 없 | TAP | repeated phrase pattern |
| 190.402 | 100.12 | Post-Chorus 3 | 없었어 | 었 | TAP | repeated phrase pattern |
| 190.649 | 100.14 | Post-Chorus 3 | 없었어 | 어 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 190.884 | 101.00 | Post-Chorus 3 | 전부 | 전 | TAP | repeated phrase pattern |
| 191.287 | 101.04~ | Post-Chorus 3 | 전부 | 부 | TAP | repeated phrase pattern |
| 191.583 | 101.06 | Post-Chorus 3 | 다 | 다 | TAP | repeated phrase pattern |
| 191.804 | 101.08 | Post-Chorus 3 | 어떡해 | 어 | TAP | phrase start |
| 192.056 | 101.10 | Post-Chorus 3 | 어떡해 | 떡 | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 192.280 | 101.12 | Post-Chorus 3 | 어떡해 | 해 | TAP | clear syllable, on the beat |
| 192.532 | 101.14 | Post-Chorus 3 | My | my | TAP | phrase start |
| 192.675 | 101.15 | Post-Chorus 3 | heart | heart | - | fast pair, not clearly enunciated |
| 192.881 | 102.01 | Post-Chorus 3 | is | is | TAP | word start |
| 193.151 | 102.03 | Post-Chorus 3 | glowing | glow | - | within 105 ms of a tapped syllable (min gap) |
| 193.247 | 102.04 | Post-Chorus 3 | glowing | ing | TAP | clear syllable, on the beat |
| 193.641 | 102.07~ | Post-Chorus 3 | it's | it's | - | fast pair, not clearly enunciated |
| 193.792 | 102.09 | Post-Chorus 3 | glowing | glow | TAP | word start |
| 193.949 | 102.10 | Post-Chorus 3 | glowing | ing | TAP | clear syllable |
| 194.225 | 102.12~ | Post-Chorus 3 | My | my | TAP | phrase start |
| 194.373 | 102.14~ | Post-Chorus 3 | heart | heart | - | fast pair, not clearly enunciated |
| 194.765 | 103.01 | Post-Chorus 3 | is | is | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 194.921 | 103.02 | Post-Chorus 3 | glowing | glow | - | density budget (bar / 2 s cap): weaker than the chosen syllables |
| 195.066 | 103.04~ | Post-Chorus 3 | glowing | ing | - | fast pair, not clearly enunciated |
| 195.197 | 103.05~ | Post-Chorus 3 | up | up | TAP | word start |
| 195.560 | 103.08 | Post-Chorus 3 | so | so | TAP | word start, on the beat |
| 195.865 | 103.10 | Post-Chorus 3 | I | i | TAP | word start |
| 196.201 | 103.13 | Post-Chorus 3 | can't | can't | - | too faint to hear as a new syllable |
| 196.445 | 103.15 | Post-Chorus 3 | sleep | sleep | TAP | word start |
| 196.613 | 104.01~ | Post-Chorus 3 | at | at | - | fast pair, not clearly enunciated |
| 197.023 | 104.04 | Post-Chorus 3 | night | night | TAP | word start, on the beat |
| 198.201 | 104.14 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 199.144 | 105.06 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 199.618 | 105.10 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 200.088 | 105.14 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 201.269 | 106.08 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 201.980 | 106.14 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 202.450 | 107.02 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 202.924 | 107.06 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 203.397 | 107.10 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 203.870 | 107.14 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 204.578 | 108.04 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 205.048 | 108.08 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 205.759 | 108.14 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 206.702 | 109.06 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 207.178 | 109.10 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 207.646 | 109.14 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 208.827 | 110.08 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 209.538 | 110.14 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 210.008 | 111.02 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
| 210.484 | 111.06 | instrumental |  |  | TAP | no vocal: other layer (previous rule-based chart) |
