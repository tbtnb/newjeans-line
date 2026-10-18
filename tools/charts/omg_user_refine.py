"""Refine the user's OMG taps (v2): every tap on the musical event the user meant, keeping their pattern.
v1 (omg_user_snap.py) estimated the hand offset from the taps' own grid phase (local average) and used audio onsets only as a
tie-breaker. v2 anchors everything on the audio:
  1. offset: per tap, cross-correlate the taps in a +-10 s window (>= 16 taps) with a combined onset envelope (kick, snare,
     vocal, bass, synth onsets from the stems, latency-calibrated, Gaussian 15 ms) over lags -140..+60 ms; median over 9 taps.
     Compared with v1's phase-based local offset in the report.
  2. evidence per 1/16 slot g: strongest onset near g (drums/bass/synth +-30 ms; vocal stem and lyric-aligned syllables -50..+35 ms, since the stem onset is the
     syllable attack, ahead of its p-center), weighted kick/snare/vocal 1.0, bass/synth 0.8, x0.3 when the stem is buried in
     the mix (rel < -14 dB).
  3. Viterbi over the 1/16 slots within +-120 ms of the offset-corrected tap. Cost = position error (sigma 30 ms) - 3 x evidence +
     1/16 off-beat penalty 2 (8 when the 1/16 slot has no real onset, ev < 0.6) + interval error vs the user's own gap to the previous tap (sigma 30 ms, gaps < 1.2 s). Consecutive slots
     are >= 0.15 s apart (2 sixteenths), so no tap is merged or invented.
  4. empty-slot pass: a tap whose slot has no real onset (evidence < 0.35) moves to the adjacent 1/16 or 1/8 slot when that slot
     has a strong onset (>= 0.6), is free, keeps the order, and the corrected tap is within 75 ms of it (plausible hand error).
  4b. reviewed decisions (REVIEW): one Verse-2 vocal run, withdrawn because it needs a gap < 0.15 s (listed in the report).
  5. copy consistency (chorus/post 2 = chorus/post 1 + 128 beats): same tapped moment -> same slot (stronger evidence).
Final times are the grid slot times (the 127.003 BPM grid sits on the drums: snare onsets median 0 ms off it).
Usage: omg_user_refine.py <export.json> <out_export.json>"""
import json, sys, numpy as np
from pathlib import Path
from scipy.ndimage import gaussian_filter1d
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/research')); import onsets as O
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src)); T = np.array([x['t_raw'] for x in d['taps']]) - (d.get('calibration_ms') or 0) / 1000
P = d['beat_period']; B0 = d['beat0']; S16 = P / 4; n = len(T)
C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); LAG = np.mean(list(O.calibrate().values()))
LAYERS = {'kick': (1.0, -.03, .03), 'snare': (1.0, -.03, .03), 'vocals': (1.0, -.05, .035), 'bass': (0.8, -.03, .03), 'other': (0.8, -.03, .03)}
PK = {L: O.peaks(C['env_' + L], LAG) for L in LAYERS}
# sung syllables from the lyric alignment (analysis/omg.lyrics.json: onset-confirmed 1.0, prior-only 0.5), same window as vocals
_SY = [x for x in json.load(open(ROOT / 'analysis/omg.lyrics.json'))['syllables']]
LAYERS['syllable'] = (1.0, -.05, .035)
PK['syllable'] = (np.array([x['t'] for x in _SY]), np.array([min(1.0, x['strength']) * (1.0 if x['conf'] == 'onset' else 0.5) for x in _SY]))
def buried(L, t):
    if L not in ('vocals', 'bass', 'other'): return False
    f = int(round((t + LAG) * O.SR / O.HOP)); return C['env_rel_' + L][min(f, len(C['env_rel_' + L]) - 1)] < -14
def ev(g):
    best = (0.0, '-', 0.0)
    for L, (w, a, b) in LAYERS.items():
        pt, ps = PK[L]
        for j in np.where((pt >= g + a) & (pt <= g + b))[0]:
            v = min(1.0, float(ps[j])) * w * (0.3 if buried(L, pt[j]) else 1.0)
            if v > best[0]: best = (v, L, float(pt[j] - g))
    return best
EVC = {}
def evk(k):
    if k not in EVC: EVC[k] = ev(B0 + k * S16)
    return EVC[k]
# 1. onset-anchored offset
FS = 1000; N = int((T.max() + 5) * FS); E = np.zeros(N)
for L, (w, a, b) in LAYERS.items():
    for t, s in zip(*PK[L]):
        i = int(round(t * FS))
        if 0 <= i < N: E[i] = max(E[i], w * min(1.0, float(s)) * (0.3 if buried(L, t) else 1.0))
E = gaussian_filter1d(E, 15); LAGS = np.arange(-140, 61)
def xoff(X):
    idx = np.round(X * FS).astype(int); return int(LAGS[np.argmax([E[np.clip(idx - l, 0, N - 1)].sum() for l in LAGS])])
raw_off = []
for t in T:
    w = 10.0
    while ((np.abs(T - t) <= w).sum() < 16): w += 1
    raw_off.append(xoff(T[np.abs(T - t) <= w]))
raw_off = np.array(raw_off, float)
off = np.array([np.median(raw_off[max(0, i - 4):i + 5]) for i in range(n)]) / 1000
glob = xoff(T)
U = T - off
# 3. Viterbi
MINGAP = 0.15   # min tap gap (judgment windows never overlap on the wider road)
SA, SI, WEV, PEN16, PEN16_WEAK, WIN = 0.030, 0.030, 3.0, 2.0, 8.0, 0.120
cands = [[k for k in range(int(np.floor((u - WIN - B0) / S16)), int(np.ceil((u + WIN - B0) / S16)) + 1) if abs(B0 + k * S16 - u) <= WIN] for u in U]
def node(i, k):
    e = (U[i] - (B0 + k * S16)) / SA; v = evk(k)[0]
    return e * e - WEV * v + ((PEN16 if v >= 0.6 else PEN16_WEAK) if k % 2 else 0.0)   # a 1/16 off-beat needs a real onset there
def trans(i, kp, k):
    if (k - kp) * S16 < MINGAP: return 1e18
    gap = T[i] - T[i - 1]
    if gap >= 1.2: return 0.0
    e = (gap - (k - kp) * S16) / SI; return e * e
cost = [np.array([node(0, k) for k in cands[0]])]; back = [None]
for i in range(1, n):
    row, br = [], []
    for k in cands[i]:
        c = [cost[-1][j] + trans(i, kp, k) for j, kp in enumerate(cands[i - 1])]; j = int(np.argmin(c))
        row.append(c[j] + node(i, k)); br.append(j)
    cost.append(np.array(row)); back.append(br)
j = int(np.argmin(cost[-1])); path = [0] * n
for i in range(n - 1, -1, -1): path[i] = cands[i][j]; j = back[i][j] if i else 0
why = ['viterbi'] * n
# 4. empty-slot pass
moved_empty = []
for i in range(n):
    k = path[i]
    if evk(k)[0] >= 0.35: continue
    opts = []
    for dk in (-2, -1, 1, 2):
        k2 = k + dk; g2 = B0 + k2 * S16
        if evk(k2)[0] < 0.6 or abs(U[i] - g2) > 0.075: continue
        if (i > 0 and k2 <= path[i - 1]) or (i < n - 1 and k2 >= path[i + 1]): continue
        opts.append((-evk(k2)[0] + abs(U[i] - g2) * 10, k2))
    if opts:
        k2 = min(opts)[1]; moved_empty.append({'i': i, 'from': round(B0 + k * S16, 3), 'to': round(B0 + k2 * S16, 3), 'ev_from': round(evk(k)[0], 2), 'ev_to': round(evk(k2)[0], 2), 'layer': evk(k2)[1]})
        path[i] = k2; why[i] = 'empty slot -> adjacent onset'
# 4b. reviewed vocal run (Verse 2, "There ain't nothing else that I would hold on to"): the user tapped the sung syllables, which
# sit on 1/16 off-beats; raw taps vs the lyric syllable onsets are -53/-6/-20/-41/+32/-32 ms (their usual anticipation vs syllables
# is -25 ms), while vs the straight-8th slots v1 chose they would be -98..-146 ms (60 ms more than their local -57 ms). The
# 1/16 alternatives in this run carry the vocal onsets (else 1.0, I 0.84) and the kick on 'would' (1.0).
REVIEW = {77.628: (77.608, 'vocal run: "noth-" (syllable 77.634, raw tap -6 ms) on e'), 77.835: (77.844, 'vocal run: "else" (77.855) on a'),
          78.052: (78.080, 'vocal run: "I" (78.093) on e'), 78.319: (78.316, 'vocal run: "would" (78.287) + kick on a'),
          78.551: (78.553, 'vocal run: "on" (78.583) on e')}
# Withdrawn (2026-10-18): this reading needs a 0.118 s gap (77.490 -> 77.608), below the 0.15 s minimum tap gap of the
# wider-road judgment windows; every alternative that keeps >= 0.15 s inside this run is either the straight-8th v1 reading
# or moves "ain't" off its syllable. The run stays on v1's 8th slots (kick/snare 1.0 on each); listed in the report.
REVIEW_APPLIED = False
review_withdrawn = []
for i in range(n):
    r_ = REVIEW.get(round(float(T[i]), 3))
    if r_: review_withdrawn.append({'t_raw': round(float(T[i]), 3), 'kept': round(B0 + path[i] * S16, 3), 'proposed': r_[0], 'why': r_[1]})
# 5. copy consistency
copyfix = []
for i in range(n):
    if not (44.9 <= T[i] <= 75.3): continue
    for jj in range(n):
        if abs(T[jj] - T[i] - 128 * P) < 0.040 and path[i] + 512 != path[jj]:
            ki, kj = path[i], path[jj] - 512
            if (ki % 2) != (kj % 2): k = ki if ki % 2 == 0 else kj
            else: k = ki if evk(ki)[0] + evk(ki + 512)[0] >= evk(kj)[0] + evk(kj + 512)[0] else kj
            if all((i2 == i or path[i2] != k) and (i2 == jj or path[i2] != k + 512) for i2 in range(n)) and \
               all(path[a] < path[a + 1] for a in range(n - 1) if a not in (i - 1, i, jj - 1, jj)) and \
               (i == 0 or path[i - 1] < k) and (i == n - 1 or k < path[i + 1]) and (path[jj - 1] < k + 512) and (jj == n - 1 or k + 512 < path[jj + 1]):
                copyfix.append({'a_raw': round(float(T[i]), 3), 'b_raw': round(float(T[jj]), 3), 'a_from': round(B0 + path[i] * S16, 3), 'b_from': round(B0 + path[jj] * S16, 3),
                                'a_to': round(B0 + k * S16, 3), 'b_to': round(B0 + (k + 512) * S16, 3)})
                path[i], path[jj] = k, k + 512; why[i] = why[jj] = 'copy consistency'
assert all(path[i] < path[i + 1] for i in range(n - 1))
S = np.array([B0 + k * S16 for k in path])
# compare with v1
v1 = json.load(open(ROOT / 'analysis/user/omg-user-snap.json'))
v1slot = [x['slot16'] for x in v1['taps']]; v1off = np.array([x['local_off_ms'] for x in v1['taps']])
flags_v1 = {f['t_raw']: f for f in v1['flags']}
taps = []
for i in range(n):
    e2 = evk(path[i]); e1 = evk(v1slot[i])
    r = why[i] if path[i] != v1slot[i] else ''
    if r == 'viterbi':
        r = 'onset evidence + onset-anchored offset' if e2[0] > e1[0] + 0.1 else 'onset-anchored offset (position)'
    second = sorted((node(i, k), k) for k in cands[i])
    taps.append({'i': i, 't_raw': round(float(T[i]), 4), 'off_ms': round(float(off[i]) * 1000, 1), 'off_v1_ms': float(v1off[i]), 'u': round(float(U[i]), 4),
                 'slot16': int(path[i]), 't': round(float(S[i]), 4), 'pos': ['1/4', 'e', '&', 'a'][path[i] % 4], 'err_ms': round(float(U[i] - S[i]) * 1000, 1),
                 'ev': round(e2[0], 2), 'layer': e2[1], 'onset_dt_ms': round(e2[2] * 1000, 1),
                 'v1_t': round(B0 + v1slot[i] * S16, 4), 'v1_ev': round(e1[0], 2), 'v1_layer': e1[1], 'changed': path[i] != v1slot[i], 'reason': r,
                 'v1_flag': flags_v1.get(round(float(T[i]), 3), {}).get('why')})
pos = np.array(path) % 4
rep = {'n': n, 'global_offset_onset_ms': glob, 'global_offset_v1_ms': v1['global_offset_ms'],
       'offset_onset_ms': {'min': round(float(off.min() * 1000), 1), 'median': round(float(np.median(off) * 1000), 1), 'max': round(float(off.max() * 1000), 1)},
       'offset_diff_vs_v1_ms': {'median_abs': round(float(np.median(np.abs(off * 1000 - v1off))), 1), 'max_abs': round(float(np.abs(off * 1000 - v1off).max()), 1)},
       'grid': {'quarter': int((pos == 0).sum()), '8th_offbeat': int((pos == 2).sum()), '16th_e': int((pos == 1).sum()), '16th_a': int((pos == 3).sum())},
       'changed': int(sum(t['changed'] for t in taps)), 'review_withdrawn': review_withdrawn, 'empty_slot_moves': moved_empty, 'copy_consistency_fixes': copyfix,
       'err_after_ms': {'abs_median': round(float(np.median(np.abs(U - S)) * 1000), 1), 'p90': round(float(np.percentile(np.abs(U - S) * 1000, 90)), 1), 'abs_max': round(float(np.abs(U - S).max() * 1000), 1)},
       'on_onset': {'ev>=0.6': int(sum(t['ev'] >= 0.6 for t in taps)), 'ev>=0.35': int(sum(t['ev'] >= 0.35 for t in taps)), 'v1 ev>=0.6': int(sum(t['v1_ev'] >= 0.6 for t in taps)), 'v1 ev>=0.35': int(sum(t['v1_ev'] >= 0.35 for t in taps))},
       'min_gap': round(float(np.diff(S).min()), 3), 'taps': taps}
json.dump(rep, open(ROOT / 'analysis/user/omg-user-refine.json', 'w'), indent=1, ensure_ascii=False)
e = dict(d); e['taps'] = [{'t_raw': x['t_raw'], 't': round(float(s), 4), 'type': x.get('type', 'tap'), 'edited': True} for x, s in zip(d['taps'], S)]
e['snap'] = {'tool': 'tools/charts/omg_user_refine.py', 'global_offset_ms': glob}
json.dump(e, open(dst, 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k != 'taps'}, indent=1, ensure_ascii=False))
for t in taps:
    if t['changed']: print(t['t_raw'], t['v1_t'], '->', t['t'], t['pos'], 'ev', t['v1_ev'], t['v1_layer'], '->', t['ev'], t['layer'], 'err', t['err_ms'], t['reason'])
