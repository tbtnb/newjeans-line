"""Per-tap transient audit. Usage: audit_taps.py <slug> [chart.json] [--out analysis/research/<slug>-taps.json]
Layers: full mix; demucs stems (drums -> kick <150 Hz, snare/clap 1-8 kHz, hat >7 kHz; vocals; bass; other).
For each tap: nearest calibrated onset per layer within +-90 ms (offset = onset - tap, + means the sound comes AFTER the
tap time), strengths (normalised to each layer's 99.5th pct), 16th-grid position and snap error.
Also lists strong onsets with no tap within 70 ms (candidate missed accents)."""
import sys, json, numpy as np, librosa
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
ROOT = Path(__file__).resolve().parents[2]
args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[i - 1].startswith('--')]
sid = args[0]; chart_p = Path(args[1]) if len(args) > 1 else ROOT / f'levels-src/{sid}/chart.json'
out_p = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else ROOT / f'analysis/research/{sid}-taps.json'
LAG = np.mean(list(O.calibrate().values()))
STEMS = next(Path(b) / sid for b in ['/workspace/w2-stems/htdemucs', '/workspace/nj-stems/htdemucs'] if (Path(b) / sid).exists())
def load(p): return librosa.load(p, sr=O.SR, mono=True)[0]
cache = ROOT / f'analysis/research/{sid}-onsets.npz'
if cache.exists():
    C = dict(np.load(cache)); ENV = {k[4:]: C[k] for k in C if k.startswith('env_')}
else:
    full = load(ROOT / f'public/audio/{sid}.mp3')
    st = {k: load(STEMS / f'{k}.wav') for k in ['drums', 'vocals', 'bass', 'other'] if (STEMS / f'{k}.wav').exists()}
    # demucs stems were rendered from a decode that keeps the mp3 encoder delay; align them to the gapless decode
    # (= what Chrome's decodeAudioData returns, verified) by cross-correlating the stem sum with the mix
    ssum = sum(st.values()); seg = slice(O.SR * 30, O.SR * 40); M = 4000
    STEM_LAG = int(np.argmax(np.correlate(ssum[seg.start - M:seg.stop + M], full[seg], 'valid'))) - M
    print('stem lag vs gapless mix:', STEM_LAG, 'samples', round(STEM_LAG / O.SR * 1000, 1), 'ms')
    st = {k: (y[STEM_LAG:] if STEM_LAG >= 0 else np.concatenate([np.zeros(-STEM_LAG), y]))[:len(full)] for k, y in st.items()}
    st = {k: np.pad(y, (0, len(full) - len(y))) for k, y in st.items()}
    ENV = {'full': O.norm(O.flux(full))}
    if 'drums' in st:
        d = st['drums']; ENV['kick'] = O.norm(O.flux(d, fmax=150)); ENV['snare'] = O.norm(O.flux(d, 1000, 8000)); ENV['hat'] = O.norm(O.flux(d, 7000, 16000))
    for k in ['vocals', 'bass', 'other']:
        if k in st: ENV[k] = O.norm(O.flux(st[k]))
    # presence gate for stems: rms in dB relative to the full mix
    rf = librosa.feature.rms(y=full, frame_length=1024, hop_length=O.HOP)[0]
    for k, y in st.items():
        r = librosa.feature.rms(y=y, frame_length=1024, hop_length=O.HOP)[0]; ENV['rel_' + k] = 20 * np.log10((r + 1e-9) / (rf + 1e-9))
    cache.parent.mkdir(parents=True, exist_ok=True); np.savez_compressed(cache, **{'env_' + k: v for k, v in ENV.items()})
LAYERS = [k for k in ['full', 'kick', 'snare', 'hat', 'vocals', 'bass', 'other'] if k in ENV]
PK = {k: O.peaks(ENV[k], LAG) for k in LAYERS}
g = json.load(open(ROOT / f'analysis/{sid}.grid.json')); P, B0 = g['period'], g['beat0']
chart = json.load(open(chart_p)); taps = chart['taps']
m = chart.get('meta', {})
if m.get('beat_period'): P, B0 = m['beat_period'], m.get('beat0', B0)
def gridpos(t):
    q = (t - B0) / (P / 4); k = int(round(q)); return k // 16, k % 16, (q - k) * P / 4
rows = []
for x in taps:
    t = x['t']; bar, step, err = gridpos(t); r = {'t': t, 'tag': x.get('tag'), 'dir': x.get('dir'), 'bar': bar, 'step': step, 'grid_err_ms': round(err * 1000, 1)}
    for k in LAYERS:
        pt, ps = PK[k]; w = np.where(np.abs(pt - t) <= 0.09)[0]
        if len(w):
            j = w[np.argmax(ps[w] - 2.0 * np.abs(pt[w] - t))]   # strong and near
            r[k] = [round(float(pt[j] - t) * 1000, 1), round(float(ps[j]), 2)]
        else: r[k] = None
    rows.append(r)
# missed strong onsets
T = np.array([x['t'] for x in taps])
missed = []
for k in LAYERS:
    pt, ps = PK[k]
    for t, s in zip(pt, ps):
        if s < (0.7 if k != 'full' else 0.6): continue
        if k in ('vocals', 'bass', 'other', 'kick', 'snare', 'hat'):
            f = int(round((t + LAG) * O.SR / O.HOP))
            rel = ENV.get('rel_' + {'kick': 'drums', 'snare': 'drums', 'hat': 'drums'}.get(k, k))
            if rel is not None and f < len(rel) and rel[f] < -12: continue
        if len(T) and np.min(np.abs(T - t)) <= 0.07: continue
        bar, step, err = gridpos(t)
        missed.append({'t': round(float(t), 3), 'layer': k, 's': round(float(s), 2), 'bar': bar, 'step': step, 'grid_err_ms': round(err * 1000, 1)})
missed.sort(key=lambda r: r['t'])
out_p.parent.mkdir(parents=True, exist_ok=True)
json.dump({'slug': sid, 'lag_corr_ms': round(LAG * 1000, 1), 'grid': {'period': P, 'beat0': B0}, 'taps': rows, 'missed': missed}, open(out_p, 'w'), indent=0)
# summary
def med(a): return float(np.median(a)) if len(a) else float('nan')
print(f'{sid}: {len(rows)} taps, onset lag correction {LAG*1000:.1f} ms, grid {60/P:.3f} BPM beat0 {B0:.4f}')
for k in LAYERS:
    offs = [r[k][0] for r in rows if r[k] and r[k][1] >= 0.5]
    print(f'  {k:7s} taps with strong onset within 90ms: {len(offs):3d}  median offset {med(offs):+6.1f} ms  IQR {np.percentile(offs,25) if offs else 0:+.1f}..{np.percentile(offs,75) if offs else 0:+.1f}')
best = []
for r in rows:
    c = [(r[k][1], r[k][0]) for k in LAYERS if r[k] and abs(r[k][0]) <= 60]
    best.append(max(c) if c else (0, None))
nos = sum(1 for s, o in best if s < 0.4)
print(f'  taps whose strongest onset (any layer, +-60ms) < 0.4: {nos}')
print(f'  median |grid err| {med([abs(r["grid_err_ms"]) for r in rows]):.1f} ms; grid err median {med([r["grid_err_ms"] for r in rows]):+.1f} ms')
print(f'  strong onsets with no tap within 70 ms: {len(missed)}')
