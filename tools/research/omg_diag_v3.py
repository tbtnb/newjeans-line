"""Diagnose the v3 OMG chart (vocal backbone + drum fill) for the vocal/BGM research doc. Writes analysis/research/omg-diag-v3.json."""
import json, sys, numpy as np, librosa, scipy.signal as ss
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
c = json.load(open(sys.argv[1] if len(sys.argv) > 1 else ROOT / 'levels-src/omg/chart.json')); d = json.load(open(ROOT / 'analysis/omg.lyrics.json'))
P = c['meta']['beat_period']; B0 = c['meta']['beat0']; S16 = P / 4; S8 = P / 2
taps = c['taps']; T = np.array([x['t'] for x in taps]); V = [x for x in taps if x.get('lyric')]; VT = np.array([x['t'] for x in V])
def dev(t, s): q = (t - B0) / s; return (q - round(q)) * s
def step(t): return int(round((t - B0) / S16)) % 16
out = {}
# 1. tap grid categories
cat = {'quarter': 0, '8th_off': 0, '16th_weak(e/a)': 0, 'triplet': 0, 'off_grid': 0}
for t in VT:
    if abs(dev(t, S16)) < 0.004:
        s = step(t); cat['quarter' if s % 4 == 0 else '8th_off' if s % 2 == 0 else '16th_weak(e/a)'] += 1
    elif abs(dev(t, P / 6)) < 0.004 or abs(dev(t, P / 3)) < 0.004: cat['triplet'] += 1
    else: cat['off_grid'] += 1
out['vocal_tap_grid'] = cat; out['vocal_taps'] = len(VT)
offg = [abs(dev(t, S16)) * 1000 for t in VT if not (abs(dev(t, S16)) < 0.004)]
out['vocal_tap_abs_dev_from_16th_ms_nonsnapped'] = {'n': len(offg), 'median': round(float(np.median(offg)), 1) if offg else 0}
out['vocal_tap_abs_dev_from_8th_ms'] = {'median': round(float(np.median([abs(dev(t, S8)) * 1000 for t in VT])), 1), 'share_within_15ms': round(float(np.mean([abs(dev(t, S8)) < 0.015 for t in VT])), 3)}
# 2. syllable onsets vs grid, and p-centre estimate (fastest rise of the 80-1000 Hz vocal envelope = acoustic P-centre model)
v, sr = librosa.load('/workspace/nj-lyrics/omg-vocals-aligned.wav', sr=22050)
b, a = ss.butter(4, [80, 1000], btype='band', fs=sr); lo = np.abs(ss.hilbert(ss.filtfilt(b, a, v)))
hop = 64; env = np.sqrt(np.convolve(lo ** 2, np.ones(441) / 441, 'same'))[::hop]; envd = np.log(env + 1e-4); der = np.diff(envd, prepend=envd[0])
der = np.convolve(der, np.ones(5) / 5, 'same')
pcs = []
for s in d['syllables']:
    i0, i1 = int((s['t'] - 0.02) * sr / hop), int((s['t'] + 0.12) * sr / hop)
    if i1 <= i0: continue
    j = i0 + int(np.argmax(der[i0:i1])); pcs.append((s['t'], j * hop / sr, s))
po = np.array([pc - t for t, pc, s in pcs]) * 1000
out['pcentre_minus_onset_ms'] = {'median': round(float(np.median(po)), 1), 'p25': round(float(np.percentile(po, 25)), 1), 'p75': round(float(np.percentile(po, 75)), 1)}
on_dev = np.array([dev(t, S16) for t, pc, s in pcs]) * 1000; pc_dev = np.array([dev(pc, S16) for t, pc, s in pcs]) * 1000
m = (np.abs(on_dev) < 45)
out['syllable_onset_signed_dev_from_16th_ms'] = {'median': round(float(np.median(on_dev[m])), 1), 'abs_median': round(float(np.median(np.abs(on_dev[m]))), 1)}
m2 = (np.abs(pc_dev) < 45)
out['pcentre_signed_dev_from_16th_ms'] = {'median': round(float(np.median(pc_dev[m2])), 1), 'abs_median': round(float(np.median(np.abs(pc_dev[m2]))), 1)}
# taps placed on raw onsets/early snaps: how early vs the p-centre
tp = []
for t in VT:
    k = np.argmin([abs(pc - t) if False else abs(st - t) for st, pc, s in pcs]); tp.append((pcs[k][1] - t) * 1000)
out['pcentre_minus_vocal_tap_ms'] = {'median': round(float(np.median(tp)), 1), 'share_tap_earlier_than_pcentre_by_>25ms': round(float(np.mean(np.array(tp) > 25)), 3)}
# 3. strong drum beats vs vocal taps
C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); LAG = np.mean(list(O.calibrate().values()))
PK = {k: O.peaks(C['env_' + k], LAG) for k in ('kick', 'snare')}
def pk(l, t): pt, ps = PK[l]; mm = np.abs(pt - t) <= 0.035; return float(ps[mm].max()) if mm.any() else 0.0
strong = [B0 + i * P for i in range(int((212 - B0) / P)) if max(pk('kick', B0 + i * P), pk('snare', B0 + i * P)) >= 0.8]
untapped = [g for g in strong if np.min(np.abs(T - g)) > 0.03]
flam = [g for g in untapped if np.min(np.abs(VT - g)) <= 0.16]
out['strong_drum_beats'] = len(strong); out['strong_drum_beats_untapped'] = len(untapped)
out['strong_drum_beats_with_vocal_tap_30_160ms_off'] = len(flam)
# 4. one-tap-line feel: weak-16th taps, isolated weak taps, per-bar density spread, same lyric different pattern count
weak = [t for t in VT if abs(dev(t, S16)) < 0.004 and step(t) % 2 == 1]
iso = [t for t in weak if not any(abs(u - t - S16) < 0.01 or abs(t - u - S16) < 0.01 for u in T)]
out['weak16_isolated'] = len(iso)
bars = {}
for t in T: bars.setdefault(int((t - B0) // (4 * P)), 0); bars[int((t - B0) // (4 * P))] += 1
cnt = np.array(list(bars.values())); out['taps_per_bar'] = {'min': int(cnt.min()), 'median': float(np.median(cnt)), 'max': int(cnt.max()), 'std': round(float(cnt.std()), 2)}
nb = list(bars.values()); out['adjacent_bar_density_jumps_ge4'] = int(sum(abs(a - b) >= 4 for a, b in zip(nb, nb[1:])))
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else ROOT / 'analysis/research/omg-diag-v3.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
