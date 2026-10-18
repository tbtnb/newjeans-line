"""Syllable-level vocal timing for OMG -> analysis/omg.lyrics.json (chart-research, 2026-10-18).
Inputs
  * lyrics: Genius (https://genius.com/Newjeans-omg-lyrics, romanized https://genius.com/Genius-romanizations-newjeans-omg-romanized-lyrics),
    Verse 2 / Pre-Chorus 2 cross-checked with https://lyrics.lol/artist/3239944-NewJeans-%EB%89%B4%EC%A7%84%EC%8A%A4/lyrics/9837130-OMG-FRNK-Remix
  * vocal stem: demucs htdemucs vocals.wav shifted -1105 samples (25.1 ms, mp3 encoder delay) onto the gapless decode
  * word timing prior: faster-whisper large-v3 word timestamps on that stem (tools/research/omg_whisper.py,
    analysis/research/omg-whisper-large-v3.json); line windows below were set from it by hand (lyrics are canonical, whisper text is not)
Method: every canonical syllable gets a prior time (whisper syllable stream of the line, index-interpolated); then a monotonic DP snaps
syllables to calibrated vocal-stem onsets (log-mel flux, -7.2 ms attack correction) near the prior. Syllables with no onset nearby keep
the prior (conf 'prior'). strength = vocal-stem onset strength (99.5th pct = 1); prom = vocal level vs full mix in dB at that time."""
import json, re, sys, numpy as np, librosa
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
ROOT = Path(__file__).resolve().parents[2]
STEM = Path('/workspace/w2-stems/htdemucs/omg/vocals.wav'); STEM_LAG = 1105

SEC = {  # section: members per Genius headers
 'Intro': 'Hanni', 'Verse 1': 'Haerin, Minji, Danielle', 'Pre-Chorus 1': 'Hyein, Danielle, Minji, Haerin', 'Chorus 1': 'Hanni, Danielle',
 'Post-Chorus 1': 'Haerin, Hyein, Hanni', 'Verse 2': 'Minji, Danielle, Hanni', 'Pre-Chorus 2': 'Hyein, Hanni, Danielle, Minji',
 'Chorus 2': 'Hanni, Danielle', 'Post-Chorus 2': 'Haerin, Hyein', 'Interlude': 'Haerin, Hanni, All', 'Bridge': 'Hanni, Hyein, Danielle, Minji',
 'Chorus 3': 'Hanni, Danielle', 'Post-Chorus 3': 'Minji, Hyein, Haerin'}
ADL = "They keep on asking me, who is he?"
CH = [("Oh my, oh my God, 예상했어 나", 'hook'), ("I was really hoping that he will come through", 'lead'),
      ("Oh my, oh my God, 단 너뿐이야", 'hook'), ("Asking all the time about what I should do", 'lead')]
# (t0, t1, section, kind, text, member-if-known)
L = [
 (2.50, 6.6, 'Intro', 'lead', "이 노래는 it's about you, baby", 'Hanni'), (7.45, 9.4, 'Intro', 'lead', "Only you", 'Hanni'),
 (11.05, 12.9, 'Intro', 'lead', "You, you, you", 'Hanni'), (12.9, 14.75, 'Intro', 'lead', "You, you, you, you", 'Hanni'),
 (14.80, 18.25, 'Verse 1', 'lead', "내가 힘들 때 울 것 같을 때", 'Haerin'), (18.25, 19.15, 'Verse 1', 'adlib', "Mm-hm", None),
 (19.15, 21.95, 'Verse 1', 'lead', "기운도 이젠 나지 않을 때", 'Haerin'), (21.95, 22.55, 'Verse 1', 'adlib', "Mm-hm", None),
 (22.55, 23.75, 'Verse 1', 'lead', "It's you", 'Minji'), (23.75, 24.82, 'Verse 1', 'lead', "날 걱정하네", 'Danielle'),
 (24.82, 25.62, 'Verse 1', 'lead', "it's you", 'Minji'), (25.62, 26.68, 'Verse 1', 'lead', "날 웃게하네", 'Danielle'),
 (26.68, 29.40, 'Verse 1', 'lead', "말 안 해도 돼, boy, what do you say?", None),
]
for base, sec in ((29.40, 'Pre-Chorus 1'), (89.55, 'Pre-Chorus 2')):
    off = base - 29.40; w = [29.40, 30.42, 33.34, 34.44, 37.04, 38.22, 40.96, 42.02, 45.0] if sec.endswith('1') else [89.55, 91.0, 93.7, 94.98, 97.6, 98.74, 101.34, 102.46, 105.47]
    txt = ["멀리든 언제든지 달려와", "바쁜 척도 없이 넌 나타나", "이게 말이 되니 난 물어봐", "너는 말야, he's the one that's living in my system, baby"]
    for k in range(4):
        L.append((w[2 * k], w[2 * k + 1], sec, 'adlib', ADL, None)); L.append((w[2 * k + 1], w[2 * k + 2], sec, 'lead', txt[k], None))
for sec, w in (('Chorus 1', [45.0, 47.82, 52.30, 55.20, 59.40]), ('Chorus 2', [105.47, 108.28, 112.72, 115.62, 119.95]),
               ('Chorus 3', [165.55, 168.72, 173.15, 176.10, 179.62])):
    for k, (txt, kind) in enumerate(CH): L.append((w[k], w[k + 1], sec, kind, txt, None))
L.insert(next(i for i, x in enumerate(L) if x[2] == 'Chorus 3'), (164.30, 165.55, 'Bridge', 'lead', "'Cause he", None))
POST = ["No, I can never let him go", "너만 생각나, twenty-four", "난 행운아야 정말로", "I know, I know", "널 알기 전까지는 나", "의미 없었어 전부 다", "내 맘이 끝이 없는 걸"]
for sec, w, last in (('Post-Chorus 1', [59.40, 61.36, 63.06, 65.20, 66.22, 68.85, 70.84, 72.76, 75.20], "I know, I know, I'm going crazy, right?"),
                     ('Post-Chorus 2', [119.95, 121.84, 123.56, 125.68, 127.45, 129.2, 131.32, 133.22, 134.22], "I know, I know")):
    for k in range(7): L.append((w[k], w[k + 1], sec, 'lead', POST[k], None))
    L.append((w[7], w[8], sec, 'lead', last, None))
L += [
 (75.20, 77.05, 'Verse 2', 'lead', "어디서든, 몇 번이든", None), (77.05, 79.0, 'Verse 2', 'lead', "There ain't nothing else that I would hold on to", None),
 (79.0, 80.94, 'Verse 2', 'lead', "I hear his voice through all the noise", None), (80.94, 82.78, 'Verse 2', 'lead', "잠시라도 내 손 놓지 마, no, no", None),
 (82.78, 84.0, 'Verse 2', 'lead', "걱정 없잖아", None), (84.0, 86.45, 'Verse 2', 'lead', "'Cause I got someone", None),
 (86.45, 87.52, 'Verse 2', 'lead', "혼자라도 괜찮아", None), (87.52, 89.55, 'Verse 2', 'lead', "'Cause I love someone", None),
 (134.22, 135.28, 'Post-Chorus 2', 'adlib', "He's the one that's living in my system", None),
 (135.28, 139.6, 'Interlude', 'hook', "Baby, babe, baby, baby", None), (141.40, 143.2, 'Interlude', 'hook', "I'm going crazy, right?", None),
 (143.2, 147.4, 'Interlude', 'hook', "Baby, baby, babe, baby", None), (149.30, 150.66, 'Interlude', 'lead', "너와 나", None),
 (150.66, 153.4, 'Bridge', 'lead', "My heart is glowing, it's glowing up", None), (153.4, 154.25, 'Bridge', 'adlib', "Glow, glow", None),
 (154.25, 157.4, 'Bridge', 'lead', "너랑만 있으면 무서울 게 없어", None), (157.4, 158.15, 'Bridge', 'adlib', "No, no", None),
 (158.15, 160.68, 'Bridge', 'lead', "가득 메워진, 다 메워진", None), (160.68, 164.30, 'Bridge', 'lead', "My heart is glowing, it'd be glowing", None),
 (179.62, 182.42, 'Post-Chorus 3', 'lead', "No, I can never let him go", None), (182.42, 183.86, 'Post-Chorus 3', 'lead', "He's right there for me, twenty-four", None),
 (183.86, 186.14, 'Post-Chorus 3', 'lead', "난 행운아야 정말로", None), (186.14, 187.12, 'Post-Chorus 3', 'lead', "I know, I know", None),
 (187.12, 189.66, 'Post-Chorus 3', 'lead', "널 알기 전까지는 나", None), (189.66, 191.75, 'Post-Chorus 3', 'lead', "의미 없었어 전부 다", None),
 (191.75, 192.5, 'Post-Chorus 3', 'lead', "어떡해", None), (192.5, 194.2, 'Post-Chorus 3', 'lead', "My heart is glowing, it's glowing", None),
 (194.2, 198.2, 'Post-Chorus 3', 'lead', "My heart is glowing up so I can't sleep at night", None),
]
L.sort(key=lambda x: x[0])
EN = {'about': ['a', 'bout'], 'baby': ['ba', 'by'], 'only': ['on', 'ly'], 'really': ['real', 'ly'], 'hoping': ['hop', 'ing'], 'asking': ['ask', 'ing'],
      'never': ['nev', 'er'], 'twenty': ['twen', 'ty'], 'nothing': ['noth', 'ing'], 'someone': ['some', 'one'], 'crazy': ['cra', 'zy'],
      'going': ['go', 'ing'], 'glowing': ['glow', 'ing'], 'system': ['sys', 'tem'], 'living': ['liv', 'ing'], 'mm-hm': ['mm', 'hm'],
      'better': ['bet', 'ter'], 'even': ['e', 'ven'], 'goin': ['go', 'in'], 'glowin': ['glow', 'in'], '24': ['twen', 'ty', 'four']}
def syl(word):
    w = word.lower().strip(".,?!'\"()—-") if not word.lower().strip(".,?!'\"()").startswith('mm') else 'mm-hm'
    if not w: return []
    if re.search('[가-힣]', w): return [c for c in w if '가' <= c <= '힣']
    if w in EN: return EN[w]
    if '-' in w: return sum((syl(p) for p in w.split('-')), [])
    return [w]
def words(text): return [w for w in re.split(r"[\s,]+", text) if syl(w)]
# whisper syllable stream (time per syllable, evenly split inside each word)
WH = json.load(open(ROOT / 'analysis/research/omg-whisper-large-v3.json'))
ws = [w for s in WH for w in s['words']]; WS = []
for i, w in enumerate(ws):
    n = len(syl(w['w'].strip())) or 1; nxt = ws[i + 1]['s'] if i + 1 < len(ws) else w['e']; e = min(w['e'], nxt) if nxt > w['s'] else w['e']
    d = max(0.08, e - w['s']); WS += [w['s'] + k * d / n for k in range(n)]
WS = np.array(WS)
# vocal stem onsets
v = librosa.load(STEM, sr=O.SR, mono=True)[0][STEM_LAG:]; y = librosa.load(ROOT / 'public/audio/omg.mp3', sr=O.SR, mono=True)[0]
v = np.pad(v, (0, max(0, len(y) - len(v))))[:len(y)]
LAG = np.mean(list(O.calibrate().values()))
env = O.norm(O.flux(v, 80, 8000)); pt, ps = O.peaks(env, LAG, thr=0.06, wait_s=0.05)
rv = librosa.feature.rms(y=v, frame_length=1024, hop_length=O.HOP)[0]; ry = librosa.feature.rms(y=y, frame_length=1024, hop_length=O.HOP)[0]
rel = 20 * np.log10((rv + 1e-9) / (ry + 1e-9))
def prom(t): f = int(round((t + LAG) * O.SR / O.HOP)); return float(np.median(rel[max(0, f - 10):f + 40]))
keep = np.array([prom(t) > -16 for t in pt]); pt, ps = pt[keep], ps[keep]
P = 0.4724304864737013
# repeated sections whose vocal stems are sample copies (cross-correlation 0.93 / 0.91 at exactly 128 or 256 beats, +1.4 / +2.7 ms):
# their syllables must land identically, so each repeated line is aligned once on the averaged whisper prior and copied.
COPY = {'Chorus 2': ('Chorus 1', 128 * P + 0.0014), 'Chorus 3': ('Chorus 1', 256 * P + 0.0027), 'Post-Chorus 2': ('Post-Chorus 1', 128 * P + 0.0014)}
def prior(t0, t1, N):
    wsl = WS[(WS >= t0 - 0.06) & (WS < t1 - 0.03)]
    if len(wsl) >= 2: return np.interp(np.linspace(0, len(wsl) - 1, N) if N > 1 else [0], np.arange(len(wsl)), wsl), 'whisper'
    return t0 + 0.05 + (t1 - t0 - 0.15) * (np.arange(N) / max(1, N)), 'window'
def align(t0, t1, pri, psrc):
    N = len(pri); ci = np.where((pt >= t0 - 0.12) & (pt <= t1 + 0.04))[0]; C, CS = pt[ci], ps[ci]; M = len(C)
    sig = 0.06 if psrc == 'whisper' else 0.25; SKIP = 2.2; INF = 1e9
    best = [[(INF, None)] * (M + 1) for _ in range(N + 1)]; best[0] = [(0.0, None)] * (M + 1)
    for i in range(1, N + 1):
        for j in range(M + 1):
            cand = (best[i - 1][j][0] + SKIP, ('skip', j))
            if j > 0:
                k = j - 1; c = ((C[k] - pri[i - 1]) / sig) ** 2 - 1.5 * min(CS[k], 1.2)
                kk = int(np.searchsorted(C, C[k] - 0.09, 'right'))   # sung syllables >= 90 ms apart
                if best[i - 1][kk][0] + c < cand[0]: cand = (best[i - 1][kk][0] + c, ('use', k, kk))
                if best[i][j - 1][0] < cand[0]: cand = (best[i][j - 1][0], ('carry', j - 1))
            best[i][j] = cand
    assign = [None] * N; i, j = N, M
    while i > 0:
        op, a = best[i][j][1][:2]
        if op == 'carry': j = a; continue
        if op == 'use': assign[i - 1] = a; j = best[i][j][1][2]
        i -= 1
    return [(float(C[a]), 'onset') if a is not None and abs(C[a] - pri[n]) < 0.2 else (float(pri[n]), 'prior') for n, a in enumerate(assign)]
def strength_at(t):
    f = int(round((t + LAG) * O.SR / O.HOP)); return float(env[max(0, f - 3):f + 4].max())
info = []
for li, (t0, t1, sec, kind, text, mem) in enumerate(L):
    W = words(text); S = [(wi, s) for wi, w in enumerate(W) for s in syl(w)]
    pri, psrc = prior(t0, t1, len(S)); info.append((W, S, pri, psrc))
def master_of(li):
    t0, t1, sec, kind, text, mem = L[li]
    if sec not in COPY: return None
    ms, sh = COPY[sec]
    for mj, x in enumerate(L):
        if x[2] == ms and x[4] == text and abs(x[0] - (t0 - sh)) < 0.6: return mj, sh
    return None
copies = {}
for li in range(len(L)):
    m = master_of(li)
    if m: copies.setdefault(m[0], []).append((li, m[1]))
times = {}
for li, (t0, t1, sec, kind, text, mem) in enumerate(L):
    if master_of(li): continue
    W, S, pri, psrc = info[li]
    if li in copies and psrc == 'whisper':
        ps_ = [pri] + [info[cj][2] - sh for cj, sh in copies[li] if info[cj][3] == 'whisper']; pri = np.median(np.array(ps_), axis=0)
    times[li] = align(t0, t1, pri, psrc)
    for cj, sh in copies.get(li, []): times[cj] = [(t + sh, c) for t, c in times[li]]
lines, flat = [], []
for li, (t0, t1, sec, kind, text, mem) in enumerate(L):
    W, S, pri, psrc = info[li]; out_w = [{'w': w, 'syl': []} for w in W]
    for n, ((wi, s), (t, cf)) in enumerate(zip(S, times[li])):
        rec = {'s': s, 't': round(t, 3), 'strength': round(strength_at(t), 2), 'prom_db': round(prom(t), 1), 'conf': cf}
        if master_of(li): rec['copy_of'] = master_of(li)[0]
        out_w[wi]['syl'].append(rec)
        flat.append({**rec, 'word': W[wi], 'line': li, 'section': sec, 'kind': kind, 'first_of_word': len(out_w[wi]['syl']) == 1, 'first_of_line': n == 0})
    lines.append({'i': li, 't0': t0, 't1': t1, 'section': sec, 'members': SEC[sec], 'member': mem, 'kind': kind, 'text': text, 'prior': psrc, 'words': out_w,
                  'start': out_w[0]['syl'][0]['t'] if out_w and out_w[0]['syl'] else t0})
# enforce monotonic flat order (adjacent lines may overlap a little)
flat.sort(key=lambda r: r['t'])
doc = {'song': 'omg', 'sources': ['https://genius.com/Newjeans-omg-lyrics', 'https://genius.com/Genius-romanizations-newjeans-omg-romanized-lyrics',
       'https://lyrics.lol/artist/3239944-NewJeans-%EB%89%B4%EC%A7%84%EC%8A%A4/lyrics/9837130-OMG-FRNK-Remix'],
       'method': __doc__.split('Method: ')[1].strip(), 'stem_lag_samples_44k1': STEM_LAG, 'onset_lag_corr_ms': round(LAG * 1000, 1),
       'kinds': {'lead': 'main sung/rapped line', 'hook': 'title hook / chopped vocal hook', 'adlib': 'backing or ad-lib line (Genius parentheses)'},
       'timeline': [{'t': l['start'], 't_end': l['t1'], 'section': l['section'], 'kind': l['kind'], 'text': l['text']} for l in lines],
       'lines': lines, 'syllables': flat}
json.dump(doc, open(ROOT / 'analysis/omg.lyrics.json', 'w'), ensure_ascii=False, indent=1)
n = len(flat); on = sum(r['conf'] == 'onset' for r in flat)
print(f'{len(lines)} lines, {n} syllables, {on} snapped to a vocal onset ({on / n:.0%}), {n - on} kept prior')
