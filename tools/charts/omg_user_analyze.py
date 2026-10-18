"""Analyse the user's OMG tapper export: systematic offset (onset cross-correlation + circular grid fit), drift, jitter,
grid classes, and repeat consistency (sections 128 beats apart). Writes analysis/user/omg-user-taps-analysis.json."""
import json, sys, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
src = sys.argv[1] if len(sys.argv) > 1 else '/workspace/nj-input/omg-user-taps-v1.json'
d = json.load(open(src)); T = np.array([x['t_raw'] for x in d['taps']]); P = d['beat_period']; B0 = d['beat0']; S16 = P / 4
out = {'n': len(T), 'first': float(T[0]), 'last': float(T[-1]), 'min_gap': round(float(np.diff(T).min()), 3)}
# A. offset by circular mean on the 1/8 grid (period 236 ms), refined by onset cross-correlation (drums + vocals)
ph = ((T - B0) / (P / 2)) % 1 * 2 * np.pi; circ = float(np.angle(np.mean(np.exp(1j * ph))) / (2 * np.pi) * P / 2)
out['offset_circular_8th_ms'] = round(circ * 1000, 1)
sys.path.insert(0, str(ROOT / 'tools/research')); import onsets as O
C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); LAG = np.mean(list(O.calibrate().values()))
PK = {k: O.peaks(C['env_' + k], LAG) for k in ('full', 'kick', 'snare', 'vocals')}
def score(lag):
    s = 0
    for k in PK:
        pt, ps = PK[k]
        for t in T - lag:
            m = np.abs(pt - t) < 0.03; s += ps[m].max() if m.any() else 0
    return s / len(T) / len(PK)
lags = np.arange(-0.12, 0.0101, 0.0025); sc = [score(l) for l in lags]
out['offset_onset_xcorr_ms'] = round(float(lags[int(np.argmax(sc))]) * 1000, 1)
OFF = circ  # taps minus true time (negative = taps early)
U = T - OFF
r16 = (U - B0) / S16; k16 = np.round(r16).astype(int); res = (r16 - k16) * S16 * 1000
pos = k16 % 4
out['offset_used_ms'] = round(OFF * 1000, 1)
# drift per 30 s block
def circ_off(X): return float(np.angle(np.mean(np.exp(1j * (((X - B0) / (P / 2)) % 1) * 2 * np.pi)))) / (2 * np.pi) * P / 2 * 1000
out['offset_by_block_ms'] = {f'{a}-{a + 30}': round(circ_off(T[(T >= a) & (T < a + 30)]), 1) for a in range(0, 160, 30)}
# jitter = residual to the nearest 1/16 after offset (only taps within +-45 ms)
m = np.abs(res) < 45
out['jitter_sd_ms'] = round(float(np.std(res[m])), 1); out['jitter_abs_median_ms'] = round(float(np.median(np.abs(res))), 1)
out['grid_class'] = {'quarter': int((pos == 0).sum()), '8th_offbeat': int((pos == 2).sum()), '16th_e': int((pos == 1).sum()), '16th_a': int((pos == 3).sum())}
# triplet-ish: closer to a P/3 point than to any 1/16 point by > 15 ms
r3 = (U - B0) / (P / 3); d3 = np.abs(r3 - np.round(r3)) * P / 3 * 1000
trip = [(round(float(t), 3), round(float(a), 1), round(float(b), 1)) for t, a, b in zip(U, np.abs(res), d3) if b + 15 < a and np.round(r3[list(U).index(t)]) % 3 != 0]
out['triplet_ish'] = trip
out['far_from_grid_gt45ms'] = [round(float(t), 3) for t, r_ in zip(U, res) if abs(r_) >= 45]
# 16th taps listed with neighbours
out['sixteenths'] = [{'t': round(float(U[i]), 3), 'pos': 'e' if pos[i] == 1 else 'a', 'res_ms': round(float(res[i]), 1)} for i in range(len(U)) if pos[i] % 2 == 1]
# repeat consistency: verse1..post1 (14.8-75.2) vs verse2..post2 (+128 beats)
slots = set(int(k) for k in k16)
def sec_cmp(name, a0, a1, shift=128 * 4):
    A = sorted(s for s in slots if a0 <= B0 + s * S16 < a1); Bs = sorted(s - shift for s in slots if a0 <= B0 + (s - shift) * S16 < a1)
    sa, sb = set(A), set(Bs)
    # tolerate +-1 sixteenth as "slip"
    onlyA = sorted(sa - sb); onlyB = sorted(sb - sa)
    near = [(x, y) for x in onlyA for y in onlyB if abs(x - y) == 1]
    return {'section': name, 'a': [round(a0, 1), round(a1, 1)], 'b': [round(a0 + shift * S16, 1), round(a1 + shift * S16, 1)], 'taps_a': len(sa), 'taps_b': len(sb),
            'same': len(sa & sb), 'jaccard': round(len(sa & sb) / max(1, len(sa | sb)), 2),
            'only_a': [round(B0 + s * S16, 3) for s in onlyA], 'only_b_at': [round(B0 + (s + shift) * S16, 3) for s in onlyB],
            'off_by_one_16th_pairs': [(round(B0 + x * S16, 3), round(B0 + (y + shift) * S16, 3)) for x, y in near]}
out['repeats'] = [sec_cmp('Verse', 14.8, 29.4), sec_cmp('Pre-Chorus', 29.4, 45.0), sec_cmp('Chorus', 45.0, 59.4), sec_cmp('Post-Chorus', 59.4, 75.2)]
# within-chorus repeats: chorus phrase repeats every 4 bars (16 beats)? compare halves
out['chorus_halves'] = [sec_cmp('Chorus1 half', 45.0, 52.2, 64), sec_cmp('Chorus2 half', 105.5, 112.7, 64), sec_cmp('Post1 half', 59.4, 67.0, 64), sec_cmp('Post2 half', 120.0, 127.6, 64)]
Path(ROOT / 'analysis/user').mkdir(parents=True, exist_ok=True)
json.dump(out, open(ROOT / 'analysis/user/omg-user-taps-analysis.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('sixteenths',)}, indent=1)[:9000])
