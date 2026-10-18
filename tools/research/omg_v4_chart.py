"""OMG v4: grid-first vocal/BGM chart (docs/research/vocal-bgm-charting.md). ONE rule set for the whole song:
  G  Every tap sits exactly on the beat grid (127.003 BPM, beat0 0.011): 1/8 positions by default; no triplets, no raw onsets.
  D  Pulse: every quarter beat where the kick or snare/clap hits hard (onset >= DTHR) is tapped, in every section.
  V  Vocal: a sung syllable whose onset or P-centre (fastest rise of the 80-1000 Hz vocal envelope) lies within +-45 ms of a 1/8 point
     adds a tap there (phrase starts first, then word starts, then the strongest), at most VB vocal taps per bar.
     A syllable on a 1/16 'e'/'a' position is only tapped inside a clearly sung 16th run (>= 3 consecutive 16th syllables, strength >= 0.5);
     isolated 16th syllables are not tapped (they are corners on weak 16ths).
  H  Held notes (>= 1 beat): no vocal taps inside; the pulse (D) continues, so the groove never stops.
  S  Same lyric / copied vocal = same pattern (majority vote / mirror). Drumless bars (< 2 strong drum quarters): the pulse uses instrument/bass onsets (>= ITHR) on quarter beats instead.
Usage: omg_v4_chart.py [--dthr 0.8] [--vb 4] [--dry] [--out chart.json]"""
import json, sys, numpy as np, librosa, scipy.signal as ss
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
opt = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
DTHR = opt('--dthr', 0.8); VB = opt('--vb', 4); ITHR = opt('--ithr', 0.6); TOL8 = 0.045
LY = json.load(open(ROOT / 'analysis/omg.lyrics.json')); base = json.load(open(ROOT / 'levels-src/omg/chart.json'))
P = base['meta']['beat_period']; B0 = base['meta']['beat0']; S16 = P / 4; S8 = P / 2; DUR = json.load(open(ROOT / 'analysis/omg.json'))['duration']
syl = LY['syllables']; lines = LY['lines']
# P-centre estimate per syllable (acoustic model: moment of fastest rise of the low-band amplitude envelope)
v, sr = librosa.load('/workspace/nj-lyrics/omg-vocals-aligned.wav', sr=22050)
b, a = ss.butter(4, [80, 1000], btype='band', fs=sr); lo = np.abs(ss.hilbert(ss.filtfilt(b, a, v))); hop = 64
env = np.log(np.sqrt(np.convolve(lo ** 2, np.ones(441) / 441, 'same'))[::hop] + 1e-4); der = np.convolve(np.diff(env, prepend=env[0]), np.ones(5) / 5, 'same')
for i, s in enumerate(syl):
    i0, i1 = int((s['t'] - 0.02) * sr / hop), int((s['t'] + 0.12) * sr / hop)
    s['pc'] = (i0 + int(np.argmax(der[i0:i1]))) * hop / sr
    s['i'] = i; s['next_gap'] = syl[i + 1]['t'] - s['t'] if i + 1 < len(syl) else 1.0
def g8(t): return B0 + round((t - B0) / S8) * S8
def g16(t): return B0 + round((t - B0) / S16) * S16
for s in syl:
    cands = [(abs(x - g8(x)), g8(x)) for x in (s['t'], s['pc'])]; e, g = min(cands)
    s['g8'] = g if e <= TOL8 else None
    c16 = [(abs(x - g16(x)), g16(x)) for x in (s['t'], s['pc'])]; e16, gg = min(c16)
    s['g16'] = gg if e16 <= 0.03 else None
    s['bar'] = int((((s['g8'] or s['g16'] or s['t']) - B0) + 1e-6) // (4 * P))
HOOKW = {'oh', 'my', 'god', 'baby', 'babe', 'crazy', 'glowing', 'know', 'mm-hm'}
def audible(s): return s['strength'] >= 0.3 or (s['first_of_line'] and s['prom_db'] > -6)
# 16th runs: >= 3 consecutive syllables on consecutive 16th points, all clearly sung
run16 = set()
k = 0
while k < len(syl):
    j = k
    while j + 1 < len(syl) and syl[j]['g16'] is not None and syl[j + 1]['g16'] is not None and abs(syl[j + 1]['g16'] - syl[j]['g16'] - S16) < 0.01 \
            and syl[j]['line'] == syl[j + 1]['line']: j += 1
    if j - k + 1 >= 3 and all(syl[q]['strength'] >= 0.5 for q in range(k, j + 1)): run16.update(range(k, j + 1))
    k = j + 1
MASTER = {}
for l in lines:
    cp = {s.get('copy_of') for w in l['words'] for s in w['syl']}
    if cp != {None}: MASTER[l['i']] = cp.pop()
def slot(s): return s['g16'] if s['i'] in run16 else s['g8']
def prio(s):
    w = s['word'].lower().strip(".,?!'")
    return (0 if s['first_of_line'] else 1 if (s['kind'] == 'hook' and w in HOOKW) else 2 if s['first_of_word'] else 3, -s['strength'])
chosen = {}
for b in sorted({s['bar'] for s in syl}):
    cand = [s for s in syl if s['bar'] == b and s['line'] not in MASTER and audible(s) and slot(s) is not None]
    used = set(round(x, 3) for x in chosen.values())
    n = 0
    for s in sorted(cand, key=prio):
        g = round(slot(s), 3)
        if g in used: continue
        if n >= VB and s['i'] not in run16 and not s['first_of_line']: continue
        chosen[s['i']] = g; used.add(g); n += 1
# same lyric = same pattern (vote by syllable index), copies mirror their master
groups = {}
for l in lines:
    if l['i'] not in MASTER: groups.setdefault(l['text'].lower().strip(' ?!.'), []).append(l['i'])
for ids in groups.values():
    S_ = [[s for s in syl if s['line'] == i] for i in ids]
    if len(ids) < 2 or len({len(x) for x in S_}) != 1: continue
    pat = [2 * sum(x[q]['i'] in chosen for x in S_) >= len(ids) for q in range(len(S_[0]))]
    for x in S_:
        for q, s in enumerate(x):
            chosen.pop(s['i'], None)
            if pat[q] and slot(s) is not None and audible(s): chosen[s['i']] = round(slot(s), 3)
for l in lines:
    if l['i'] in MASTER:
        for m_, c_ in zip([s for s in syl if s['line'] == MASTER[l['i']]], [s for s in syl if s['line'] == l['i']]):
            if m_['i'] in chosen and slot(c_) is not None: chosen[c_['i']] = round(slot(c_), 3)
vt = {}
for i, g in chosen.items():
    s = syl[i]
    if g not in vt: vt[g] = {'t': g, 'kind': 'vocal', 'lyric': s['word'].strip(',.?!'), 'syl': s['s'], 'run16': i in run16}
# H is structural: a held note (gap to the next syllable >= 1 beat) has no syllables inside, so only the pulse (D) can tap there.
# D: pulse on strong quarter beats
C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); LAG = np.mean(list(O.calibrate().values()))
PK = {k: O.peaks(C['env_' + k], LAG) for k in ('kick', 'snare', 'other', 'bass')}
def pk(l, t, w=0.035): pt, ps = PK[l]; mm = np.abs(pt - t) <= w; return float(ps[mm].max()) if mm.any() else 0.0
dt = {}
for q in range(int((DUR - B0) / P) + 1):
    g = round(B0 + q * P, 3)
    if g < 1.0 or g > DUR - 1.2: continue
    if max(pk('kick', g), pk('snare', g)) >= DTHR: dt[g] = {'t': g, 'kind': 'drum', 'tag': 'snare' if pk('snare', g) >= pk('kick', g) else 'kick'}
# drumless bars (< 2 strong drum quarters): the pulse falls back to the instrument/bass onsets on the quarter beats
it = {}
for b in range(int((DUR - B0) / (4 * P)) + 1):
    a0 = B0 + 4 * b * P
    if sum(a0 - 0.01 <= g < a0 + 4 * P - 0.01 for g in dt) >= 2: continue
    for kk in range(4):
        g = round(a0 + kk * P, 3)
        if 1.0 <= g <= DUR - 1.2 and g not in dt and max(pk('other', g), pk('bass', g)) >= ITHR: it[g] = {'t': g, 'kind': 'inst', 'tag': 'other'}
allt = {}
for dct in (it, dt, vt):          # vocal wins a shared slot (the tap is the same; label it as vocal + drum)
    for g, x in dct.items():
        if g in allt and allt[g]['kind'] == 'drum' and x['kind'] == 'vocal': x = {**x, 'also_drum': True}
        allt[g] = x
out = [allt[g] for g in sorted(allt)]
T = np.array([x['t'] for x in out]); c1 = max(((T >= t) & (T < t + 1)).sum() for t in T)
nv = sum(x['kind'] == 'vocal' for x in out); nd = sum(x['kind'] == 'drum' for x in out); ni = sum(x['kind'] == 'inst' for x in out)
print(f"DTHR={DTHR} VB={VB}: {len(out)} taps = {nv} vocal ({sum(x.get('also_drum', False) for x in out)} on a drum beat too) + {nd} drum-only + {ni} inst; "
      f"{len(out) / DUR:.2f}/s; peak 1s {c1}; min gap {np.diff(T).min():.3f}; 16th-run syllables {len(run16)}")
json.dump({'rule': __doc__.split('Usage')[0].strip(), 'DTHR': DTHR, 'VB': VB, 'taps': out}, open(ROOT / 'analysis/research/omg-v4-taps.json', 'w'), ensure_ascii=False, indent=0)
if '--dry' in sys.argv: sys.exit()
ch = base
ch['taps'] = [{'t': x['t'], 'tag': 'vocals' if x['kind'] == 'vocal' else x['tag'], **({'lyric': x['lyric'], 'syl': x['syl']} if x['kind'] == 'vocal' else {}), **({'also': 'drum'} if x.get('also_drum') else {})} for x in out]
for s in ch['sections']:
    s['follows'] = 'vocal'; s['follows_layers'] = 'grid: strong kick/snare quarters + vocal syllables on 1/8'
    s['follows_note'] = 'v4 grid-first rule (omg_v4_chart.py, docs/research/vocal-bgm-charting.md)'
ch['meta']['lyrics_chart'] = {'tool': 'tools/research/omg_v4_chart.py', 'rule': 'docs/research/vocal-bgm-charting.md', 'DTHR': DTHR, 'VB': VB, 'vocal_taps': nv, 'drum_taps': nd, 'inst_taps': ni}
Path(opt('--out', str(ROOT / 'levels-src/omg/chart.json'))).write_text(json.dumps(ch, indent=1, ensure_ascii=False))
