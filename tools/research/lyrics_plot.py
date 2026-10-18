"""Spot-check plot: vocal-stem spectrogram + onset envelope with aligned syllables. Usage: lyrics_plot.py out.png t0,t1 [t0,t1 ...]"""
import sys, json, numpy as np, librosa, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fp = next((f for f in fm.findSystemFonts() if any(k in f for k in ('NotoSansCJK', 'NanumGothic', 'wqy', 'Noto Sans CJK', 'DroidSansFallback'))), None)
if fp: fm.fontManager.addfont(fp); plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
d = json.load(open('analysis/omg.lyrics.json')); v, sr = librosa.load('/workspace/nj-lyrics/omg-vocals-aligned.wav', sr=22050)
spans = [tuple(map(float, a.split(','))) for a in sys.argv[2:]]
fig, axs = plt.subplots(len(spans), 1, figsize=(16, 3.2 * len(spans)))
for ax, (a, b) in zip(np.atleast_1d(axs), spans):
    x = v[int(a * sr):int(b * sr)]; S = librosa.power_to_db(librosa.feature.melspectrogram(y=x, sr=sr, n_fft=1024, hop_length=128, n_mels=80, fmax=8000), ref=np.max)
    ax.imshow(S, origin='lower', aspect='auto', extent=[a, b, 0, 80], cmap='magma', vmin=-70)
    for s in d['syllables']:
        if a <= s['t'] <= b:
            ax.axvline(s['t'], color='cyan' if s['conf'] == 'onset' else 'red', lw=1)
            ax.text(s['t'] + 0.005, 72 if s['first_of_word'] else 64, s['s'], color='white', fontsize=9)
    ax.set_xlim(a, b)
fig.tight_layout(); fig.savefig(sys.argv[1], dpi=70)
