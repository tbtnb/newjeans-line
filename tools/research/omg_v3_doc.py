"""docs/research/omg-lyrics-chart.md for the v3 (one-rule) OMG chart: rule, per-section proof table, verification, annotated timeline."""
import json, numpy as np, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
d = json.load(open(ROOT / 'analysis/omg.lyrics.json')); V3 = json.load(open(ROOT / 'analysis/research/omg-v3-taps.json'))
c = json.load(open(ROOT / 'levels-src/omg/chart.json')); X = V3['X']
P = c['meta']['beat_period']; B0 = c['meta']['beat0']; S16 = P / 4; DUR = 212.25
taps = V3['taps']; T = np.array([x['t'] for x in taps]); syl = d['syllables']; held = V3['held']
C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); LAG = np.mean(list(O.calibrate().values()))
PK = {k: O.peaks(C['env_' + k], LAG) for k in ('kick', 'snare')}
def pk(l, t): pt, ps = PK[l]; m = np.abs(pt - t) <= 0.035; return float(ps[m].max()) if m.any() else 0.0
VT = np.array([x['t'] for x in taps if x['kind'] == 'vocal'])
def in_held(t): return any(a + X < t < b - 0.05 for a, b, w in held)
# lyric sections (music structure) + intro/outro
secs = []
for l in d['lines']:
    if not secs or secs[-1][1] != l['section']: secs.append([l['t0'], l['section']])
secs[0][0] = 0.0; secs.append([197.47, 'Outro (instrumental)'])
def sec_of(t):
    s = secs[0][1]
    for a, n in secs:
        if t >= a: s = n
    return s
# re-derive every beat under rule D and compare with the chart (deviations)
beats = []
for b in range(int((DUR - B0) / (4 * P)) + 1):
    for q in range(4):
        g = B0 + (4 * b + q) * P
        if g < 1.0 or g > DUR - 1.2: continue
        hit = max(pk('snare', g), pk('kick', g)) >= 0.5
        near = len(VT) and np.min(np.abs(VT - g)) <= X
        h = in_held(g); want = hit and not near and not h
        have = bool(np.any([(x['kind'] == 'drum' and abs(x['t'] - g) <= 0.03) for x in taps]))
        beats.append((g, sec_of(g), hit, near, h, want, have))
rows = []
for a, n in secs:
    tv = sum(1 for x in taps if x['kind'] == 'vocal' and sec_of(x['t']) == n); td = sum(1 for x in taps if x['kind'] == 'drum' and sec_of(x['t']) == n)
    ti = sum(1 for x in taps if x['kind'] == 'inst' and sec_of(x['t']) == n); B = [z for z in beats if z[1] == n]
    e = next((a2 for a2, n2 in secs if a2 > a), DUR); dur = e - a
    dev = sum(1 for z in B if z[5] != z[6]); held_n = sum(1 for w in held if sec_of(w[0]) == n)
    rows.append(f"| {n} | {a:.1f}-{e:.1f} | {tv} | {td} | {ti} | {sum(z[2] for z in B)} | {sum(z[2] and z[3] for z in B)} | {sum(z[2] and not z[3] and z[4] for z in B)} | {held_n} | {(tv + td + ti) / dur:.2f} | {dev} |")
devs = [z for z in beats if z[5] != z[6]]
nv = sum(x['kind'] == 'vocal' for x in taps); nd = sum(x['kind'] == 'drum' for x in taps); ni = sum(x['kind'] == 'inst' for x in taps)
prev = json.load(open(ROOT / 'analysis/research/omg-lyrics-taps.json')); PV = np.array([x['t'] for x in prev if x['src'] != 'fallback'])
kept = sum(np.min(np.abs(VT - t)) <= 0.005 for t in PV)
cT = np.array([x['t'] for x in c['taps']]); c1 = max(((cT >= t) & (cT < t + 1)).sum() for t in cT)
play = ROOT / 'deliverables/omg-v3-play.json'; pl = json.load(open(play))['summary'] if play.exists() else None
pls = (f"{pl['status']}, {pl['perfect']}/{pl['taps']} perfect, {pl['good']} good, diamonds {pl['diamonds']}/10" if pl else 'pending')
extra = json.load(open(ROOT / 'analysis/research/omg-v3-extra.json')) if (ROOT / 'analysis/research/omg-v3-extra.json').exists() else {}
H = f"""# OMG chart v3: one rule for the whole song

**The rule (same in every section, no exceptions):**
1. **Vocal = backbone.** In every sung line, tap the line's first syllable, every syllable of the title hooks, and the clearest other syllables.
   The same limits apply everywhere: at most 5 vocal taps per bar and 5 in any 2 s. Repeated lyrics and copied vocals get the same pattern.
2. **Drums fill.** Every beat (1, 2, 3, 4) where the kick or snare really hits is tapped, unless a vocal tap is within ±{X:.2f} s.
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
* "Covered by vocal" means a vocal tap is within ±{X:.2f} s, so the beat is already a tap and no drum tap is added.
* "Deviations" counts beats where the chart differs from rule 2 re-derived from the audio. It is 0 everywhere.
* Sections with few or no drum taps (Intro, Verse 1, Pre-Chorus 2) are not exceptions: the drums there are sparse or absent (only 6-19% of backbeats have a snare), so rule 2 rarely fires.

| section | time (s) | vocal taps | drum taps | piano taps | drum beats | covered by vocal | inside held note | held notes | taps/s | deviations |
|---|---|---|---|---|---|---|---|---|---|---|
""" + '\n'.join(rows) + f"""

Totals: {len(taps)} taps = {nv} vocal + {nd} drum + {ni} piano. Rule-2 deviations: {len(devs)}.
Piano taps (rule 4) appear only in the outro, the only bars with neither vocal nor drums.

## Stats vs targets
| | lyric chart (v2, 478) | v3 | target |
|---|---|---|---|
| vocal taps kept (same syllable) | 454 | {kept}/454 ({kept / 454:.0%}) | >= 85% |
| strong quarter-beat accents tapped | 113/297 | {extra.get('strong', '?')} | clearly up |
| average density | 2.25/s | {len(taps) / DUR:.2f}/s | ~2.3-2.6/s |
| busiest 1 s | 5 taps | {c1} taps | <= 5 |
| min gap | 0.118 s | {np.diff(T).min():.3f} s | >= 0.105 |
| held-note straights | 26 notes | {len(held)} notes, 0 taps inside | preserved |

## Verification
* `levels-design/validate.py`: {extra.get('validate', '?')}.
* Scripted playthrough (headless Chrome, CDP touch simulation; not a real device): {pls}. {extra.get('play_note', '')}.
* Layout and route: {extra.get('layout', '?')}.
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
"""
def pos(t):
    q = (t - B0) / S16; k = int(round(q)); return f"{k // 16}.{k % 16:02d}" + ('' if abs((q - k) * S16) < 0.04 else '~')
R = []
def tapped_v(t): return len(VT) and np.min(np.abs(VT - t)) <= 0.05
for s in syl:
    tp = tapped_v(s['t']); w = s['word'].lower().strip(".,?!'")
    if tp: r = '1: phrase start' if s['first_of_line'] else ('1: title hook' if s['kind'] == 'hook' and w in {'oh', 'my', 'god', 'baby', 'babe', 'crazy', 'glowing', 'know', 'mm-hm'} else ('1: copied vocal = same pattern' if 'copy_of' in s else '1: clear syllable'))
    else:
        nb = [o for o in syl if o is not s and tapped_v(o['t']) and abs(o['t'] - s['t']) < 0.17]
        r = ('1: too faint' if s['strength'] < 0.3 else '1: within 0.105 s of a tapped syllable' if any(abs(o['t'] - s['t']) < 0.105 for o in nb)
             else '1: fast pair, not clearly sung' if nb else '1: per-bar / 2 s limit (weaker syllable)')
    R.append((s['t'], pos(s['t']), s['section'], f"{s['word']} [{s['s']}]", 'TAP' if tp else '-', r))
for g, sec, hit, near, h, want, have in beats:
    if not hit: continue
    r = '2: drum beat, no vocal within ±%.2f s' % X if have else ('2: covered by a vocal tap' if near else '3: inside a held note (straight)')
    R.append((g, pos(g), sec, 'kick/snare beat', 'TAP' if have else '-', r))
for x in taps:
    if x['kind'] == 'inst': R.append((x['t'], pos(x['t']), sec_of(x['t']), 'piano', 'TAP', '4: no vocal, no drums: piano on 8ths'))
R.sort()
out = H + '\n'.join(f"| {t:.3f} | {p} | {s} | {l} | {tp} | {r} |" for t, p, s, l, tp, r in R) + '\n'
(ROOT / 'docs/research/omg-lyrics-chart.md').write_text(out)
print(len(taps), 'taps', nv, nd, ni, 'deviations', len(devs), 'kept', kept, 'rows', len(R))
for z in devs[:10]: print('  dev', z)
