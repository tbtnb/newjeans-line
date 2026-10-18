"""Snap the user's OMG tapper export to the beat grid while keeping their rhythm (their chart; we only fix hand error).
  1. offset: humans tapping along anticipate the beat (negative mean asynchrony), so the taps are compared with the grid by a
     LOCAL circular mean of their 1/8-grid phase (+-12 s window). The global estimate is cross-checked by onset cross-correlation
     in omg_user_analyze.py.
  2. snap: Viterbi over candidate 1/16 slots per tap. Cost = position error (sigma 25 ms) - small bonus for a real onset at the slot (tie-breaker) + interval error vs the user's own gap
     to the previous tap (sigma 30 ms, gaps < 1.2 s; their gaps carry the rhythm even when their phase drifts) + a penalty for
     1/16 off-beat slots ('e'/'a') so a 1/16 is only chosen when the user clearly tapped one. Slots strictly increase (min 1/16 =
     0.118 s > 0.105 s min gap), so no two taps merge and none is invented.
  3. flags: taps whose best and second-best slot cost are close (ambiguous) or whose corrected error is > 50 ms.
Writes a tapper export with edited, snapped `t` (import_taps.py keeps edited taps as they are) and analysis/user/omg-user-snap.json.
Usage: omg_user_snap.py <export.json> <out_export.json>"""
import json, sys, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src)); T = np.array([x['t_raw'] for x in d['taps']]) - (d.get('calibration_ms') or 0) / 1000
P = d['beat_period']; B0 = d['beat0']; S16 = P / 4; E8 = P / 2
SA, SI, PEN16, W = 0.025, 0.030, 2.5, 12.0
def phase_off(X):
    return float(np.angle(np.mean(np.exp(1j * (((X - B0) / E8) % 1) * 2 * np.pi)))) / (2 * np.pi) * E8
glob = phase_off(T)
loc = np.array([phase_off(T[np.abs(T - t) <= W]) for t in T])
U = T - loc
cands = []
for u in U:
    k0 = int(round((u - B0) / S16)); cands.append([k for k in range(k0 - 2, k0 + 3)])
# music evidence (tie-breaker only): strongest drum/vocal/bass/other onset within 30 ms of the slot
sys.path.insert(0, str(ROOT / 'tools/research'))
import onsets as O
_C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); _LAG = np.mean(list(O.calibrate().values()))
_PK = [O.peaks(_C['env_' + k], _LAG) for k in ('kick', 'snare', 'vocals', 'bass', 'other')]
def onset_at(t):
    v = 0.0
    for pt, ps in _PK:
        m = np.abs(pt - t) < 0.03
        if m.any(): v = max(v, float(ps[m].max()))
    return min(1.0, v)
BON = 1.0
def node_cost(i, k):
    e = (U[i] - (B0 + k * S16)) / SA; return e * e + (PEN16 if k % 2 else 0.0) - BON * onset_at(B0 + k * S16)
n = len(U); INF = 1e18
cost = [[node_cost(0, k) for k in cands[0]]]; back = [[-1] * 5]
for i in range(1, n):
    gap = T[i] - T[i - 1]; row = []; br = []
    for k in cands[i]:
        best, bj = INF, -1
        for j, kp in enumerate(cands[i - 1]):
            if k <= kp: continue
            c = cost[-1][j]
            if gap < 1.2: e = (gap - (k - kp) * S16) / SI; c += e * e
            if c < best: best, bj = c, j
        row.append(best + node_cost(i, k)); br.append(bj)
    cost.append(row); back.append(br)
j = int(np.argmin(cost[-1])); path = [0] * n
for i in range(n - 1, -1, -1): path[i] = cands[i][j]; j = back[i][j]
# copy consistency: chorus/post-chorus 2 are sample copies of 1 (+128 beats). When the user tapped the same moment in both
# (raw times within 40 ms after the shift) but the snap chose different slots, both get the same slot (the 1/8 one if exactly
# one is on 1/8, else the one with the stronger onset). Listed in the report.
copyfix = []
for i in range(n):
    if not (44.9 <= T[i] <= 75.3): continue
    for j in range(n):
        if abs(T[j] - T[i] - 128 * P) < 0.040 and path[i] + 512 != path[j]:
            ki, kj = path[i], path[j] - 512
            if (ki % 2) != (kj % 2): k = ki if ki % 2 == 0 else kj
            else: k = ki if onset_at(B0 + ki * S16) >= onset_at(B0 + kj * S16) else kj
            ok = all((i2 == i or path[i2] != k) and (i2 == j or path[i2] != k + 512) for i2 in range(n))
            if ok:
                copyfix.append({'a_raw': round(float(T[i]), 3), 'a_from': round(B0 + ki * S16, 3), 'b_raw': round(float(T[j]), 3), 'b_from': round(B0 + (kj + 512) * S16, 3),
                                'a_to': round(B0 + k * S16, 3), 'b_to': round(B0 + (k + 512) * S16, 3)})
                path[i], path[j] = k, k + 512
S = np.array([B0 + k * S16 for k in path])
# ambiguity: re-evaluate each tap's local alternatives with neighbours fixed
flags = []
for i in range(n):
    def lc(k):
        c = node_cost(i, k)
        for jn in (i - 1, i + 1):
            if 0 <= jn < n and abs(T[i] - T[jn]) < 1.2:
                if (jn < i and k <= path[jn]) or (jn > i and k >= path[jn]): return INF
                e = (abs(T[i] - T[jn]) - abs(k - path[jn]) * S16) / SI; c += e * e
        return c
    alt = sorted((lc(k), k) for k in cands[i])
    err = (U[i] - S[i]) * 1000
    amb = alt[1][0] - alt[0][0] < 2.0 and alt[1][0] < INF
    if amb or abs(err) > 50:
        flags.append({'t_raw': round(float(T[i]), 3), 'snapped': round(float(S[i]), 3), 'err_ms': round(float(err), 1),
                      'alt': round(float(B0 + alt[1][1] * S16), 3) if alt[1][0] < INF else None, 'why': 'ambiguous slot' if amb else 'error > 50 ms'})
pos = np.array(path) % 4
mv = (S - T) * 1000; mvc = (S - U) * 1000
rep = {'n_in': int(len(T)), 'n_out': int(len(S)), 'global_offset_ms': round(glob * 1000, 1),
       'local_offset_ms': {'min': round(float(loc.min()) * 1000, 1), 'median': round(float(np.median(loc)) * 1000, 1), 'max': round(float(loc.max()) * 1000, 1)},
       'grid': {'quarter': int((pos == 0).sum()), '8th_offbeat': int((pos == 2).sum()), '16th_e': int((pos == 1).sum()), '16th_a': int((pos == 3).sum())},
       'move_vs_raw_ms': {'median': round(float(np.median(mv)), 1), 'abs_max': round(float(np.abs(mv).max()), 1)},
       'move_after_offset_ms': {'abs_median': round(float(np.median(np.abs(mvc))), 1), 'p90': round(float(np.percentile(np.abs(mvc), 90)), 1), 'abs_max': round(float(np.abs(mvc).max()), 1),
                                'hist': {f'<{b}': int((np.abs(mvc) < b).sum()) for b in (10, 20, 30, 40, 50, 60, 80)}},
       'min_gap': round(float(np.diff(S).min()), 3), 'flags': flags, 'copy_consistency_fixes': copyfix,
       'sixteenths': [{'t': round(float(S[i]), 3), 't_raw': round(float(T[i]), 3), 'pos': 'e' if pos[i] == 1 else 'a'} for i in range(n) if pos[i] % 2],
       'taps': [{'t_raw': round(float(T[i]), 4), 'local_off_ms': round(float(loc[i]) * 1000, 1), 't': round(float(S[i]), 4), 'slot16': int(path[i])} for i in range(n)]}
json.dump(rep, open(ROOT / 'analysis/user/omg-user-snap.json', 'w'), indent=1)
e = dict(d); e['taps'] = [{'t_raw': x['t_raw'], 't': round(float(s), 4), 'type': x.get('type', 'tap'), 'edited': True} for x, s in zip(d['taps'], S)]
e['snap'] = {'tool': 'tools/charts/omg_user_snap.py', 'global_offset_ms': rep['global_offset_ms']}
json.dump(e, open(dst, 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k not in ('taps', 'sixteenths')}, indent=1))
print('sixteenths:', [(x['t'], x['pos']) for x in rep['sixteenths']])
