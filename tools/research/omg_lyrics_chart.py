"""Re-chart OMG with the vocal as the primary layer (user feedback 2026-10-18: '跟歌词的配合可以更加多一点').
Source: analysis/omg.lyrics.json (syllable onsets). Fallback (no vocal): taps of the previous rule-based chart
(analysis/research/omg-chart-451.json, drum/synth layer) inside instrumental gaps only.
Rules (docs/research/charting-logic.md + lyric rules):
  * every sung line's first syllable is tapped (phrase start); title hooks ('Oh my, oh my God', 'baby', 'I'm going crazy') tap every syllable
  * other syllables ranked by: word-initial, vocal onset strength, note length (time to the next syllable), beat position
    (downbeat/backbeat bonus = keep strong downbeats when they coincide); chosen greedily under a per-bar budget
  * held notes / melismas: no extra taps (only syllable onsets are candidates, so a sustain is a straight)
  * fast syllable pairs (< 170 ms) only when both are clearly enunciated (strength >= 0.55) ; global min gap 0.105 s
  * copied choruses / post-choruses (vocal stem identical, see omg_lyrics.py) mirror the master's tap pattern exactly
  * timing: vocal onset snapped to the 16th grid if within 40 ms, to the triplet grid if within 25 ms, else the measured onset
Usage: omg_lyrics_chart.py [--dry]"""
import json, sys, numpy as np, librosa
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
LY = json.load(open(ROOT / 'analysis/omg.lyrics.json')); OLD = json.load(open(ROOT / 'analysis/research/omg-chart-451.json'))
P = OLD['meta']['beat_period']; B0 = OLD['meta']['beat0']; S16 = P / 4; BAR = 4 * P
DUR = json.load(open(ROOT / 'analysis/omg.json'))['duration']
syl = LY['syllables']; lines = LY['lines']
# per-syllable features
for i, s in enumerate(syl):
    s['i'] = i; s['next_gap'] = syl[i + 1]['t'] - s['t'] if i + 1 < len(syl) else 1.0; s['prev_gap'] = s['t'] - syl[i - 1]['t'] if i else 1.0
    q = (s['t'] - B0) / S16; k = int(round(q)); s['bar'], s['step'], s['err'] = k // 16, k % 16, (q - k) * S16
HOOKW = {'oh', 'my', 'god', 'baby', 'babe', 'crazy', 'glowing', 'know', 'mm-hm'}
def score(s):
    v = min(s['strength'], 1.2) + 0.6 * s['first_of_word'] + 0.5 * min(1, s['next_gap'] / 0.45)
    v += 0.6 if s['step'] % 4 == 0 and abs(s['err']) < 0.04 else (0.25 if s['step'] % 2 == 0 and abs(s['err']) < 0.04 else 0)
    if s['kind'] == 'adlib': v -= 0.35
    if s['conf'] == 'prior': v -= 0.6
    if s['prev_gap'] < 0.15 and not s['first_of_word']: v -= 0.5
    return v
def forced(s):
    if s['first_of_line'] and s['strength'] >= 0.3: return True
    w = s['word'].lower().strip(".,?!'")
    return s['kind'] == 'hook' and w in HOOKW and s['strength'] >= 0.35
# per-bar budgets by lyric section (difficulty ~ previous chart: 2-3 taps/s, peaks ~3/s)
BUD = {'Intro': 4, 'Verse 1': 5, 'Pre-Chorus 1': 5, 'Chorus 1': 6, 'Post-Chorus 1': 5, 'Verse 2': 6, 'Pre-Chorus 2': 5, 'Chorus 2': 6,
       'Post-Chorus 2': 5, 'Interlude': 5, 'Bridge': 6, 'Chorus 3': 6, 'Post-Chorus 3': 5}
MASTER = {}   # copied line -> master line (same syllable count)
for l in lines:
    cp = {s.get('copy_of') for w in l['words'] for s in w['syl']}
    if cp != {None}: MASTER[l['i']] = cp.pop()
WIN2 = 5
chosen = set()
def ok_gap(s, sel, strict=True):
    for j in sel:
        o = syl[j]; g = abs(o['t'] - s['t'])
        if g < 0.105: return False
        if strict and g < 0.17 and not (min(o['strength'], s['strength']) >= 0.55): return False
    return True
# pass 1: forced syllables (phrase starts, title hooks); hook 16th pairs like 'oh-my' are allowed down to the 0.105 s minimum
for s in sorted((s for s in syl if forced(s) and s['line'] not in MASTER), key=lambda s: (not s['first_of_line'], s['t'])):
    if ok_gap(s, [j for j in chosen if abs(syl[j]['t'] - s['t']) < 0.3], strict=False): chosen.add(s['i'])
# pass 2: remaining syllables by score under the per-bar budget
bars = sorted({s['bar'] for s in syl})
for b in bars:
    cand = [s for s in syl if s['bar'] == b and s['line'] not in MASTER and s['i'] not in chosen]
    if not cand: continue
    sec = max({c['section'] for c in cand}, key=lambda x: sum(c['section'] == x for c in cand)); budget = BUD[sec]
    for s in sorted(cand, key=lambda s: -score(s)):
        if sum(1 for j in chosen if syl[j]['bar'] == b) >= budget or score(s) < 0.9: continue
        if sum(1 for j in chosen if abs(syl[j]['t'] - s['t']) < 1.0) >= WIN2: continue   # density cap: <= WIN2 taps in any +-1 s
        if ok_gap(s, [j for j in chosen if abs(syl[j]['t'] - s['t']) < 0.3]): chosen.add(s['i'])
# phrase consistency: lines with the same text (pre-chorus ad-libs, pre-chorus 1 vs 2, post-chorus 3 vs 1) use one pattern:
# syllable k is tapped in every occurrence iff it was chosen in at least half of them
groups = {}
for l in lines:
    if l['i'] in MASTER: continue
    groups.setdefault(l['text'].lower().strip(' ?!.'), []).append(l['i'])
for key, ids in groups.items():
    if len(ids) < 2: continue
    S_ = [[s for s in syl if s['line'] == i] for i in ids]
    if len({len(x) for x in S_}) != 1: continue
    votes = [sum(x[k]['i'] in chosen for x in S_) for k in range(len(S_[0]))]
    pat = [v * 2 >= len(ids) for v in votes]
    for x in S_:
        for k, s in enumerate(x):
            chosen.discard(s['i'])
        for k, s in enumerate(x):
            if pat[k] and s['strength'] >= 0.25 and ok_gap(s, [j for j in chosen if abs(syl[j]['t'] - s['t']) < 0.3], strict=False): chosen.add(s['i'])
# mirror masters onto copies
for l in lines:
    if l['i'] not in MASTER: continue
    m = lines[MASTER[l['i']]]
    ms = [s for s in syl if s['line'] == m['i']]; cs = [s for s in syl if s['line'] == l['i']]
    for a, c in zip(ms, cs):
        if a['i'] in chosen: chosen.add(c['i'])
def qtime(s):
    t = s['t']; e16 = s['err']
    if abs(e16) <= 0.040: return B0 + round((t - B0) / S16) * S16, '16th'
    S12 = P / 6; q = (t - B0) / S12; e12 = (q - round(q)) * S12
    if abs(e12) <= 0.025: return B0 + round(q) * S12, 'triplet'
    return t, 'onset'
taps = []
for i in sorted(chosen):
    s = syl[i]
    if s['conf'] == 'prior' and abs(s['err']) > 0.06 and not s['first_of_line']: continue
    if s['strength'] < 0.3 and not (s['first_of_line'] and s['prom_db'] > -6): continue   # too faint to hear as a syllable
    t, how = qtime(s)
    taps.append({'t': round(t, 3), 'tag': 'vocals', 'lyric': s['word'].strip(',.?!'), 'syl': s['s'], 'src': f"{s['section']}|{how}"})
# instrumental gaps -> fallback to the previous drum/synth taps
S = np.array([s['t'] for s in syl]); gaps = [(1.0, S[0] - 0.25)]
for a, b in zip(S, S[1:]):
    if b - a > 1.25: gaps.append((a + 0.4, b - 0.25))
gaps.append((S[-1] + 0.45, DUR - 1.2))
# vocal presence (aligned stem vs mix): a held note keeps the line straight; only frames with no vocal fall back to the band
v = librosa.load('/workspace/w2-stems/htdemucs/omg/vocals.wav', sr=22050, mono=True)[0][552:]; ym = librosa.load(ROOT / 'public/audio/omg.mp3', sr=22050, mono=True)[0]
n = min(len(v), len(ym)); HOP = 256
rel = 20 * np.log10((librosa.feature.rms(y=v[:n], frame_length=2048, hop_length=HOP)[0] + 1e-9) / (librosa.feature.rms(y=ym[:n], frame_length=2048, hop_length=HOP)[0] + 1e-9))
def vocal_on(t): f = int(t * 22050 / HOP); return rel[max(0, f - 4):f + 5].max() > -14
fb = []; held_s = []
for a, b in gaps:
    if b - a < 0.3: continue
    for x in OLD['taps']:
        if a <= x['t'] <= b:
            if vocal_on(x['t']): held_s.append(x['t']); continue
            fb.append({'t': x['t'], 'tag': x.get('tag', 'drums'), 'src': 'fallback'})
print('fallback taps dropped because the vocal is still sounding (held note -> straight):', len(held_s), held_s[:12])
taps += fb; taps.sort(key=lambda x: x['t']); out = []
for x in taps:
    if out and x['t'] - out[-1]['t'] < 0.105:
        if out[-1]['src'] == 'fallback' and x['src'] != 'fallback': out[-1] = x
        continue
    out.append(x)
print(len(out), 'taps;', sum(x['src'] != 'fallback' for x in out), 'vocal,', sum(x['src'] == 'fallback' for x in out), 'fallback;', f'{len(out) / DUR:.2f}/s')
print('gaps used for fallback:', [(round(a, 2), round(b, 2)) for a, b in gaps if b - a >= 0.3])
if '--dry' in sys.argv: sys.exit()
ch = json.loads((ROOT / 'levels-src/omg/chart.json').read_text())
ch['taps'] = [{'t': x['t'], 'tag': x['tag'], **({'lyric': x['lyric'], 'syl': x['syl']} if 'lyric' in x else {})} for x in out]
# section follows: vocal everywhere except the instrumental outro / intro pads (label/time kept: they key the scenery + camera)
LYSEC = [(l['t0'], l['section']) for l in lines]
for k, s in enumerate(ch['sections']):
    e = ch['sections'][k + 1]['t'] if k + 1 < len(ch['sections']) else DUR
    n_v = sum(1 for x in out if s['t'] <= x['t'] < e and x['src'] != 'fallback'); n = sum(1 for x in out if s['t'] <= x['t'] < e)
    names = sorted({sec for t0, sec in LYSEC if s['t'] - 0.5 <= t0 < e}, key=lambda z: [t0 for t0, q in LYSEC if q == z][0])
    if n and n_v / n >= 0.5:
        s['follows'] = 'vocal'; s['follows_layers'] = 'vocals'; s['follows_note'] = f"lyrics: {', '.join(names)} (taps on sung syllables, analysis/omg.lyrics.json)"
    else:
        s['follows_note'] = (s.get('follows_note', '') + ' | no vocal here: kept the drum/synth layer').strip(' |')
ch['meta']['lyrics_chart'] = {'tool': 'tools/research/omg_lyrics_chart.py', 'lyrics': 'analysis/omg.lyrics.json', 'vocal_taps': sum(x['src'] != 'fallback' for x in out),
                              'fallback_taps': sum(x['src'] == 'fallback' for x in out), 'previous_taps': len(OLD['taps']), 'tap_fields': 'lyric = word, syl = syllable (debug only; engine ignores them)'}
(ROOT / 'levels-src/omg/chart.json').write_text(json.dumps(ch, indent=1, ensure_ascii=False))
json.dump(out, open(ROOT / 'analysis/research/omg-lyrics-taps.json', 'w'), ensure_ascii=False, indent=0)
