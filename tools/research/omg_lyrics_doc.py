"""Write docs/research/omg-lyrics-chart.md: lyric-annotated timeline of the vocal-primary OMG chart (one row per sung syllable +
the instrumental fallback taps). Reasons are reconstructed from the generator's rules (omg_lyrics_chart.py), main reason only."""
import json, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
d = json.load(open(ROOT / 'analysis/omg.lyrics.json')); c = json.load(open(ROOT / 'levels-src/omg/chart.json'))
T = np.array([x['t'] for x in c['taps']]); P = c['meta']['beat_period']; B0 = c['meta']['beat0']; S16 = P / 4
syl = d['syllables']; HOOK = {'oh', 'my', 'god', 'baby', 'babe', 'crazy', 'glowing', 'know', 'mm-hm'}
def tapped(t): return np.min(np.abs(T - t)) <= 0.05
def pos(t):
    q = (t - B0) / S16; k = int(round(q)); e = (q - k) * S16
    return f"{k // 16}.{k % 16:02d}" + ('' if abs(e) < 0.04 else '~')
rows = []
groups = {}
for l in d['lines']: groups.setdefault(l['text'].lower().strip(' ?!.'), []).append(l['i'])
for i, s in enumerate(syl):
    tp = tapped(s['t']); w = s['word'].lower().strip(".,?!'")
    near = [o for o in syl if o is not s and tapped(o['t']) and abs(o['t'] - s['t']) < 0.17]
    if tp:
        if 'copy_of' in s: r = f"same as line {s['copy_of']} (copied vocal, mirrored)"
        elif s['first_of_line']: r = 'phrase start'
        elif s['kind'] == 'hook' and w in HOOK: r = 'title hook: every syllable'
        elif len(groups[d['lines'][s['line']]['text'].lower().strip(' ?!.')]) > 1: r = 'repeated phrase pattern'
        else: r = ('word start' if s['first_of_word'] else 'clear syllable') + (', on the beat' if pos(s['t']).split('.')[1] in ('00', '04', '08', '12') else '')
    else:
        if s['strength'] < 0.3: r = 'too faint to hear as a new syllable'
        elif any(abs(o['t'] - s['t']) < 0.105 for o in near): r = 'within 105 ms of a tapped syllable (min gap)'
        elif near: r = 'fast pair, not clearly enunciated'
        elif s['kind'] == 'adlib': r = 'ad-lib under the lead: kept sparse'
        elif s['conf'] == 'prior': r = 'timing uncertain (no clear onset)'
        else: r = 'density budget (bar / 2 s cap): weaker than the chosen syllables'
    rows.append((s['t'], pos(s['t']), s['section'], s['word'], s['s'], 'TAP' if tp else '-', r))
S = np.array([s['t'] for s in syl])
for x in c['taps']:
    if 'lyric' not in x: rows.append((x['t'], pos(x['t']), 'instrumental', '', '', 'TAP', f"no vocal: {x.get('tag')} layer (previous rule-based chart)"))
rows.sort()
ntap = sum(r[5] == 'TAP' for r in rows); nv = sum(1 for x in c['taps'] if 'lyric' in x)
play = ROOT / 'deliverables/omg-lyrics-play.json'
pl = json.load(open(play))['summary'] if play.exists() else None
pls = (f"scripted playthrough (headless Chrome, CDP touch simulation; not a real device): {pl['status']}, {pl['perfect']}/{pl['taps']} perfect, "
       f"{pl['good']} good, diamonds {pl['diamonds']}/10" if pl else 'scripted playthrough: pending')
HEAD = f"""# OMG lyric chart (vocal-primary re-chart)

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
| taps | 451 | {len(c['taps'])} |
| taps on a sung syllable (+-50 ms) | 185 (41%) | {nv} ({nv / len(c['taps']):.0%}) |
| taps during sung lines that land on a syllable | 44% | 100% |
| line starts tapped | 11/86 | 85/86 |
| syllables tapped | 191/681 | 464/681 |
| strong drum quarter-beat accents tapped | 251/297 | 113/297 (trade-off: vocal wins) |
| average / peak density | 2.12/s; 6 taps in 1 s | {len(c['taps']) / 212.25:.2f}/s; 5 taps in 1 s, 300 CPM |

The new chart has 28 bars with no tap on a quarter beat. In every one of them the vocal itself is syncopated, so the vocal wins, per the user's request.

## Verification
* `levels-design/validate.py`: 0 errors, 473 multi-level crossings. Minimum judgment window ±53 ms; 16 gaps under 0.15 s, all real fast syllables.
* chartlogic flags many taps as "faint" or "hop". Its band/vocal envelopes do not tell sung syllables apart:
  whisper word starts, which are independent of my alignment, score the same as random times inside sung lines (median 0.28 vs 0.26).
  So these flags are expected for a legato vocal layer and are not timing errors.
* {pls}.
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
"""
out = [HEAD.rstrip('\n')]
for t, p, sec, w, sy, tp, r in rows: out.append(f'| {t:.3f} | {p} | {sec} | {w} | {sy} | {tp} | {r} |')
(ROOT / 'docs/research/omg-lyrics-chart.md').write_text('\n'.join(out) + '\n')
print(len(rows), 'rows')
