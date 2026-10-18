"""Print per-bar 16-step maps: taps vs strong onsets per layer (gapless-aligned, calibrated). Usage: barmap.py <slug> [chart.json] [--from bar] [--to bar]"""
import sys, json, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
ROOT = Path(__file__).resolve().parents[2]
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[i - 1].startswith('--')]; sid = args[0]
chart = json.load(open(args[1] if len(args) > 1 else ROOT / f'levels-src/{sid}/chart.json'))
C = dict(np.load(ROOT / f'analysis/research/{sid}-onsets.npz')); ENV = {k[4:]: C[k] for k in C if k.startswith('env_')}
LAG = -0.0072
g = json.load(open(ROOT / f'analysis/{sid}.grid.json')); P = g['period']
def fit_b0():
    pk, ps = O.peaks(np.maximum(ENV['kick'], ENV['snare']), LAG); m = ps > 0.5; pk = pk[m]
    best = None
    for b in np.arange(0, P / 4, 0.0005):
        q = (pk - b) / (P / 4); e = np.abs(q - np.round(q)) * P / 4; sc = np.median(e)
        if best is None or sc < best[0]: best = (sc, b)
    return best[1], best[0]
B0, res = fit_b0()
if __name__ == '__main__':
    print(f'grid {60/P:.3f} BPM, beat0(fit to gapless kick/snare) {B0:.4f} s (+k*{P/4:.4f}), median residual {res*1000:.1f} ms')
    PK = {k: O.peaks(ENV[k], LAG) for k in ['kick', 'snare', 'vocals', 'other', 'bass', 'full', 'hat']}
    T = [x['t'] for x in chart['taps']]
    fb = int(sys.argv[sys.argv.index('--from') + 1]) if '--from' in sys.argv else 0
    tb = int(sys.argv[sys.argv.index('--to') + 1]) if '--to' in sys.argv else 999
    nb = int((len(ENV['full']) * O.HOP / O.SR - B0) / (4 * P)) + 1
    def row(times, strengths, bar, thr):
        s = ['.'] * 16
        for t, v in zip(times, strengths):
            q = (t - B0) / (P / 4); k = int(round(q))
            if k // 16 == bar and v >= thr: s[k % 16] = '#' if v >= 0.8 else ('+' if v >= 0.55 else '-')
        return ''.join(s)
    secs = sorted(chart.get('sections', []), key=lambda s: s['t'])
    for bar in range(max(fb, 0), min(nb, tb + 1)):
        t0 = B0 + bar * 4 * P
        lab = [s['label'] for s in secs if t0 - 0.2 <= s['t'] < t0 + 4 * P - 0.2]
        tp = ['.'] * 16
        for t in T:
            q = (t - B0) / (P / 4); k = int(round(q))
            if k // 16 == bar: tp[k % 16] = 'X'
        segs = [''.join(tp)] + [row(*PK[k], bar, 0.35) for k in ['kick', 'snare', 'hat', 'vocals', 'other', 'bass', 'full']]
        f = lambda x: ' '.join(x[i:i + 4] for i in range(0, 16, 4))
        print(f'{bar:3d} {t0:7.2f} TAP {f(segs[0])} | K {f(segs[1])} | S {f(segs[2])} | H {f(segs[3])} | V {f(segs[4])} | O {f(segs[5])} | B {f(segs[6])} | F {f(segs[7])} {"<< "+lab[0] if lab else ""}')
