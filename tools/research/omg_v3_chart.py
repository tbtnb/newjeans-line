"""OMG v3: ONE rule set for the whole song (user 2026-10-18: '鼓点也可以有，但是你一首歌逻辑要一直').
  V  Vocal backbone: in every sung line, tap the line's first syllable, every syllable of the title hooks, and the clearest other
     syllables (word starts, strong onsets, long notes, on-beat). The same limits apply everywhere: <= VB vocal taps per bar,
     <= VW in any 2 s, fast pairs (<170 ms) only when both are clearly sung. Repeated lyrics/copied vocals = identical pattern.
  D  Drum fill: every beat (1-4) where the kick or snare really hits (onset >= 0.5) is tapped unless a vocal tap is within +-X s (0.2)
     or the beat falls inside a held note.            (MODE 'beat', chosen; MODE 'bb' = snare backbeats only, compared)
  H  Held note = a sung note lasting >= 1 beat (next syllable >= 1 beat later, vocal still sounding): no taps inside it -> straight.
  F  No vocal and no drums in a whole bar (outro piano): tap the lead instrument ('other' stem) onsets >= 0.5 on the 8th grid.
Timing: vocal onset snapped to the 16th grid within 40 ms / triplet within 25 ms, else onset; drums/instrument on the real onset if it
is within 20 ms of the grid, else the grid. Global minimum gap 0.105 s.
Usage: omg_v3_chart.py [--x 0.2] [--mode beat|bb] [--vb 5] [--dry] [--out chart.json]"""
import json, sys, numpy as np, librosa
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
opt = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
X = opt('--x', 0.2); MODE = opt('--mode', 'beat'); VB = opt('--vb', 5); VW = opt('--vw', 5)
LY = json.load(open(ROOT / 'analysis/omg.lyrics.json')); OLD = json.load(open(ROOT / 'analysis/research/omg-chart-451.json'))
P = OLD['meta']['beat_period']; B0 = OLD['meta']['beat0']; S16 = P / 4; DUR = json.load(open(ROOT / 'analysis/omg.json'))['duration']
syl = LY['syllables']; lines = LY['lines']
for i, s in enumerate(syl):
    s['i'] = i; s['next_gap'] = syl[i + 1]['t'] - s['t'] if i + 1 < len(syl) else 1.0; s['prev_gap'] = s['t'] - syl[i - 1]['t'] if i else 1.0
    q = (s['t'] - B0) / S16; k = int(round(q)); s['bar'], s['step'], s['err'] = k // 16, k % 16, (q - k) * S16
# ---------- V: vocal backbone (identical constants in every section) ----------
HOOKW = {'oh', 'my', 'god', 'baby', 'babe', 'crazy', 'glowing', 'know', 'mm-hm'}
def audible(s): return s['strength'] >= 0.3 or (s['first_of_line'] and s['prom_db'] > -6)
def score(s):
    v = min(s['strength'], 1.2) + 0.6 * s['first_of_word'] + 0.5 * min(1, s['next_gap'] / 0.45)
    v += 0.6 if s['step'] % 4 == 0 and abs(s['err']) < 0.04 else (0.25 if s['step'] % 2 == 0 and abs(s['err']) < 0.04 else 0)
    if s['kind'] == 'adlib': v -= 0.35
    if s['conf'] == 'prior': v -= 0.6
    if s['prev_gap'] < 0.15 and not s['first_of_word']: v -= 0.5
    return v
def forced(s):
    return audible(s) and (s['first_of_line'] or (s['kind'] == 'hook' and s['word'].lower().strip(".,?!'") in HOOKW))
MASTER = {}
for l in lines:
    cp = {s.get('copy_of') for w in l['words'] for s in w['syl']}
    if cp != {None}: MASTER[l['i']] = cp.pop()
chosen = set()
def ok_gap(s, strict=True):
    for j in chosen:
        o = syl[j]; g = abs(o['t'] - s['t'])
        if g < 0.105: return False
        if strict and g < 0.17 and min(o['strength'], s['strength']) < 0.55: return False
    return True
for s in sorted((s for s in syl if forced(s) and s['line'] not in MASTER), key=lambda s: (not s['first_of_line'], s['t'])):
    if ok_gap(s, strict=False): chosen.add(s['i'])
for b in sorted({s['bar'] for s in syl}):
    for s in sorted((s for s in syl if s['bar'] == b and s['line'] not in MASTER and s['i'] not in chosen and audible(s)), key=lambda s: -score(s)):
        if sum(syl[j]['bar'] == b for j in chosen) >= VB or score(s) < 0.9: continue
        if sum(abs(syl[j]['t'] - s['t']) < 1.0 for j in chosen) >= VW: continue
        if ok_gap(s): chosen.add(s['i'])
groups = {}
for l in lines:
    if l['i'] not in MASTER: groups.setdefault(l['text'].lower().strip(' ?!.'), []).append(l['i'])
for ids in groups.values():
    S_ = [[s for s in syl if s['line'] == i] for i in ids]
    if len(ids) < 2 or len({len(x) for x in S_}) != 1: continue
    pat = [2 * sum(x[k]['i'] in chosen for x in S_) >= len(ids) for k in range(len(S_[0]))]
    for x in S_:
        for s in x: chosen.discard(s['i'])
        for k, s in enumerate(x):
            if pat[k] and audible(s) and ok_gap(s, strict=False): chosen.add(s['i'])
for l in lines:
    if l['i'] in MASTER:
        for a, c in zip([s for s in syl if s['line'] == MASTER[l['i']]], [s for s in syl if s['line'] == l['i']]):
            if a['i'] in chosen: chosen.add(c['i'])
def qv(s):
    t = s['t']
    if abs(s['err']) <= 0.040: return B0 + round((t - B0) / S16) * S16
    S12 = P / 6; q = (t - B0) / S12
    return B0 + round(q) * S12 if abs((q - round(q)) * S12) <= 0.025 else t
vt = [{'t': round(qv(syl[i]), 3), 'kind': 'vocal', 'lyric': syl[i]['word'].strip(',.?!'), 'syl': syl[i]['s'], 'section': syl[i]['section']}
      for i in sorted(chosen) if not (syl[i]['conf'] == 'prior' and abs(syl[i]['err']) > 0.06 and not syl[i]['first_of_line'])]
# ---------- audio layers (aligned stems, calibrated onsets; cache from audit_taps.py) ----------
C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); LAG = np.mean(list(O.calibrate().values()))
PK = {k: O.peaks(C['env_' + k], LAG) for k in ('kick', 'snare', 'other')}
def peak(layer, t, w=0.035):
    pt, ps = PK[layer]; m = np.abs(pt - t) <= w
    if not m.any(): return 0.0, t
    j = np.where(m)[0][np.argmax(ps[m])]; return float(ps[j]), float(pt[j])
v = librosa.load('/workspace/w2-stems/htdemucs/omg/vocals.wav', sr=22050, mono=True)[0][552:]; ym = librosa.load(ROOT / 'public/audio/omg.mp3', sr=22050, mono=True)[0]
n = min(len(v), len(ym)); HOP = 256
rel = 20 * np.log10((librosa.feature.rms(y=v[:n], frame_length=2048, hop_length=HOP)[0] + 1e-9) / (librosa.feature.rms(y=ym[:n], frame_length=2048, hop_length=HOP)[0] + 1e-9))
def vocal_on(t): f = int(t * 22050 / HOP); return rel[max(0, f - 2):f + 3].max() > -14
# ---------- H: held notes ----------
held = []
for s in syl:
    if s['next_gap'] < P - 1e-3: continue
    e = s['t'] + 0.1
    while e < s['t'] + s['next_gap'] - 0.05 and vocal_on(e): e += 0.02
    if e - s['t'] >= P - 0.05: held.append((s['t'], e, s['word']))
def in_held(t): return any(a + X < t < b - 0.05 for a, b, w in held)
# ---------- D: drum fill ----------
VT = np.array([x['t'] for x in vt]); dt = []; skipped = {'vocal_near': 0, 'held': 0, 'no_drum': 0}
nbar = int((DUR - B0) / (4 * P)) + 1
for b in range(nbar):
    for q in ((1, 3) if MODE == 'bb' else (0, 1, 2, 3)):
        g = B0 + (4 * b + q) * P
        if g < 1.0 or g > DUR - 1.2: continue
        sv, st = peak('snare', g); kv, kt = peak('kick', g)
        hit = sv >= 0.5 if MODE == 'bb' else max(sv, kv) >= 0.5
        if not hit: skipped['no_drum'] += 1; continue
        if len(VT) and np.min(np.abs(VT - g)) <= X: skipped['vocal_near'] += 1; continue
        if in_held(g): skipped['held'] += 1; continue
        tt = st if (MODE == 'bb' or sv >= kv) else kt
        dt.append({'t': round(tt if abs(tt - g) <= 0.02 else g, 3), 'kind': 'drum', 'tag': 'snare' if (MODE == 'bb' or sv >= kv) else 'kick'})
# ---------- F: bars with no vocal and no drums -> lead instrument on 8ths ----------
ft = []
for b in range(nbar):
    a0, a1 = B0 + 4 * b * P, B0 + 4 * (b + 1) * P
    if any(a0 - 0.05 <= s['t'] < a1 for s in syl) or any(vocal_on(t) for t in np.arange(a0, a1, 0.1)): continue
    if any(max(peak('snare', B0 + (4 * b + q) * P)[0], peak('kick', B0 + (4 * b + q) * P)[0]) >= 0.5 for q in range(4)): continue
    last = -9
    for k in range(8):
        g = a0 + k * P / 2
        if g < 1.0 or g > DUR - 1.2: continue
        pv, pt_ = peak('other', g)
        if pv >= 0.5 and g - last >= 0.2: ft.append({'t': round(pt_ if abs(pt_ - g) <= 0.02 else g, 3), 'kind': 'inst', 'tag': 'other'}); last = g
taps = sorted(vt + dt + ft, key=lambda x: x['t']); out = []
for x in taps:
    if out and x['t'] - out[-1]['t'] < 0.105:
        if out[-1]['kind'] != 'vocal' and x['kind'] == 'vocal': out[-1] = x
        continue
    out.append(x)
T = np.array([x['t'] for x in out]); c1 = np.array([((T >= t) & (T < t + 1)).sum() for t in T]); c2 = np.array([((T >= t) & (T < t + 2)).sum() / 2 for t in T])
nv = sum(x['kind'] == 'vocal' for x in out)
print(f"X={X} mode={MODE}: {len(out)} taps = {nv} vocal + {sum(x['kind'] == 'drum' for x in out)} drum + {sum(x['kind'] == 'inst' for x in out)} inst; "
      f"{len(out) / DUR:.2f}/s; peak 1s {c1.max()}, peak 2s {c2.max():.1f}/s; min gap {np.diff(T).min():.3f}; drum beats skipped {skipped}; held notes {len(held)}")
json.dump({'rule': __doc__.split('Usage')[0].strip(), 'X': X, 'mode': MODE, 'taps': out, 'held': held, 'skipped': skipped}, open(ROOT / 'analysis/research/omg-v3-taps.json', 'w'), ensure_ascii=False, indent=0)
if '--dry' in sys.argv: sys.exit()
ch = json.loads((ROOT / 'levels-src/omg/chart.json').read_text())
ch['taps'] = [{'t': x['t'], 'tag': 'vocals' if x['kind'] == 'vocal' else x['tag'], **({'lyric': x['lyric'], 'syl': x['syl']} if x['kind'] == 'vocal' else {})} for x in out]
for k, s in enumerate(ch['sections']):
    s['follows'] = 'vocal'; s['follows_layers'] = 'vocals+kick+snare'
    s['follows_note'] = 'one rule for the whole song (omg_v3_chart.py): vocal syllables + every kick/snare beat with no vocal tap within 0.2 s and not inside a held note; lead instrument only in bars with no vocal and no drums'
ch['sections'][-1]['follows'] = 'mid'
ch['meta']['lyrics_chart'] = {'tool': 'tools/research/omg_v3_chart.py', 'rule': 'docs/research/omg-lyrics-chart.md (top)', 'X': X, 'mode': MODE,
                              'vocal_taps': nv, 'drum_taps': sum(x['kind'] == 'drum' for x in out), 'inst_taps': sum(x['kind'] == 'inst' for x in out),
                              'tap_fields': 'lyric = word, syl = syllable (debug only; engine ignores them)'}
Path(opt('--out', str(ROOT / 'levels-src/omg/chart.json'))).write_text(json.dumps(ch, indent=1, ensure_ascii=False))
