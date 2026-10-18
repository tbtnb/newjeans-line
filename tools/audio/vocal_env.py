"""Add a 'vocal' onset envelope (from a demucs vocals stem) to analysis/<slug>.env.npz.
Stems are not committed (large); paths searched: /workspace/nj-stems, /workspace/w2-stems, /workspace/nj-w1-work/sep (htdemucs).
The envelope is the stem's onset strength normalised to its 99.5th percentile, gated by presence: frames where the vocal
stem is > 18 dB below the full mix are zeroed (a vocal onset buried under the band is not 'audible in the full mix').
Usage: vocal_env.py <slug> [...]"""
import sys, numpy as np, librosa
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
BASES = ['/workspace/nj-stems/htdemucs', '/workspace/w2-stems/htdemucs', '/workspace/nj-w1-work/sep/htdemucs']
for sid in sys.argv[1:]:
    stem = next((Path(b) / sid / f for b in BASES for f in ('vocals.wav', 'vocals.mp3') if (Path(b) / sid / f).exists()), None)
    if not stem: print(sid, 'no vocal stem'); continue
    sr, hop = 22050, 128
    v, _ = librosa.load(stem, sr=sr, mono=True); y, _ = librosa.load(ROOT / f'public/audio/{sid}.mp3', sr=sr, mono=True)
    n = min(len(v), len(y)); v, y = v[:n], y[:n]
    on = librosa.onset.onset_strength(y=v, sr=sr, hop_length=hop); on = on / (np.percentile(on, 99.5) + 1e-9)
    rv = librosa.feature.rms(y=v, frame_length=2048, hop_length=hop)[0]; ry = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
    m = min(len(on), len(rv)); gate = (20 * np.log10((rv[:m] + 1e-9) / (ry[:m] + 1e-9))) > -18
    env = np.clip(on[:m] * gate, 0, 1.5)
    p = ROOT / f'analysis/{sid}.env.npz'; d = dict(np.load(p))
    L = len(d['full']); e = np.zeros(L); e[:min(L, m)] = env[:min(L, m)]
    d['vocal'] = (e * 100).astype(np.uint8); np.savez_compressed(p, **d)
    print(sid, 'vocal env from', stem)
