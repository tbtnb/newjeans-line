"""Fit a constant-tempo beat grid and print a bar-by-bar onset 'score' (16th resolution) per band.
Usage: grid.py <slug> [start_bar end_bar] [--bpm X] [--beat0 T]
Output also saved to analysis/<slug>.grid.json: {period, beat0, bars:[{t, kick[16], snare[16], hat[16], mid[16], full[16]}]}"""
import sys, json, numpy as np, librosa
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opts = {sys.argv[i][2:]: sys.argv[i+1] for i in range(len(sys.argv)) if sys.argv[i].startswith('--')}
sid = args[0]
y, sr = librosa.load(ROOT/f'public/audio/{sid}.mp3', sr=22050, mono=True)
hop = 128
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
def band(lo, hi):
    m = (freqs >= lo) & (freqs < hi)
    e = np.log1p(S[m] * 10)
    env = np.maximum(0, np.diff(e, axis=1)).mean(axis=0)
    env = np.concatenate([[0], env])
    env = env / (np.percentile(env, 99.5) + 1e-9)
    return np.clip(env, 0, 1.5)
env = dict(kick=band(30, 120), snare=band(1200, 4500), hat=band(7000, 11000), mid=band(250, 2000))
full = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop); env['full'] = np.clip(full / (np.percentile(full, 99.5) + 1e-9), 0, 1.5)
ft = lambda t: int(round(t * sr / hop))
a = json.load(open(ROOT/f'analysis/{sid}.json'))
beats = np.array(a['beats'])
if 'bpm' in opts: period = 60 / float(opts['bpm'])
else:
    # robust regression of beat index vs time
    d = np.diff(beats); med = np.median(d)
    idx = np.concatenate([[0], np.cumsum(np.round(d / med))])
    keep = np.ones(len(beats), bool)
    for _ in range(3):
        A = np.vstack([idx[keep], np.ones(keep.sum())]).T
        p, b0 = np.linalg.lstsq(A, beats[keep], rcond=None)[0]
        res = beats - (idx * p + b0); keep = np.abs(res) < 0.03
    period = p
# phase: maximise kick+full energy on the beat over a range of offsets
beat0 = float(opts.get('beat0', beats[0]))
if 'beat0' not in opts:
    best, bo = -1, beat0
    for off in np.linspace(-period / 2, period / 2, 81):
        ts = beat0 + off + np.arange(-200, 600) * period; ts = ts[(ts > 0) & (ts < len(y) / sr - 0.1)]
        sc = sum(env['kick'][max(0, ft(t) - 2):ft(t) + 3].max() + env['full'][max(0, ft(t) - 2):ft(t) + 3].max() for t in ts)
        if sc > best: best, bo = sc, beat0 + off
    beat0 = bo
beat0 = beat0 - np.floor(beat0 / period) * period  # first beat >= 0
bar = 4 * period
nbars = int((len(y) / sr - beat0) / bar) + 1
bars = []
for i in range(nbars):
    t0 = beat0 + i * bar
    row = {'t': round(t0, 4)}
    for k, e in env.items():
        vals = []
        for s in range(16):
            t = t0 + s * period / 4; f = ft(t); w = max(1, ft(0.025))
            vals.append(round(float(e[max(0, f - w):f + w + 1].max()) if f < len(e) else 0, 2))
        row[k] = vals
    bars.append(row)
json.dump({'period': period, 'bpm': 60 / period, 'beat0': beat0, 'bars': bars}, open(ROOT/f'analysis/{sid}.grid.json', 'w'))
sym = lambda v: ' ' if v < 0.15 else '.' if v < 0.3 else 'o' if v < 0.5 else 'O' if v < 0.75 else '#'
lo, hi = (int(args[1]), int(args[2])) if len(args) >= 3 else (0, nbars)
print(f'{sid}: bpm {60/period:.3f} period {period:.5f} beat0 {beat0:.4f} bars {nbars}')
print('bar  time    | kick            | snare           | hat             | mid             | full')
for i in range(lo, min(hi, nbars)):
    r = bars[i]
    print(f'{i:3d} {r["t"]:7.2f} |' + '|'.join(''.join(sym(v) for v in r[k]) for k in ['kick', 'snare', 'hat', 'mid', 'full']))
