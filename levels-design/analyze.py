"""Per-song audio analysis: beat grid, band onsets (kick/snare-clap/hat), vocal/melodic onsets, sections.
Output: analysis/<id>.json. These are CANDIDATES only; charts are hand-curated in tools/charts/."""
import json, sys, numpy as np, librosa
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
ids = sys.argv[1:] or [p.stem for p in sorted((ROOT/'public/audio').glob('*.mp3'))]
for sid in ids:
    y, sr = librosa.load(ROOT/f'public/audio/{sid}.mp3', sr=22050, mono=True)
    dur = len(y)/sr
    hop = 256
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    def band(lo, hi):
        m = (freqs >= lo) & (freqs < hi)
        e = librosa.amplitude_to_db(S[m], ref=np.max)
        env = np.maximum(0, np.diff(e, axis=1)).mean(axis=0)
        env = np.concatenate([[0], env])
        return env / (env.max() + 1e-9)
    kick = band(30, 150); snare = band(1500, 5000); hat = band(7000, 11000); mid = band(200, 1500)
    full = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    tempo, beats = librosa.beat.beat_track(onset_envelope=full, sr=sr, hop_length=hop, tightness=200)
    bt = librosa.frames_to_time(beats, sr=sr, hop_length=hop)
    def peaks(env, delta):
        p = librosa.util.peak_pick(env, pre_max=4, post_max=4, pre_avg=10, post_avg=10, delta=delta, wait=6)
        return [(round(float(librosa.frames_to_time(i, sr=sr, hop_length=hop)), 4), round(float(env[i]), 3)) for i in p]
    fulln = full/(full.max()+1e-9)
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
    # 1-second loudness curve
    loud = [round(float(rms[(t >= s) & (t < s+1)].mean()), 4) for s in range(int(dur)+1) if ((t >= s) & (t < s+1)).any()]
    # structural segmentation via chroma+mfcc recurrence
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=512, n_mfcc=13)
    feat = np.vstack([librosa.util.normalize(chroma), librosa.util.normalize(mfcc)])
    k = max(6, int(dur/14))
    bounds = librosa.segment.agglomerative(feat, k)
    bt_sec = [round(float(x), 2) for x in librosa.frames_to_time(bounds, sr=sr, hop_length=512)]
    out = dict(id=sid, duration=round(dur, 4), tempo=float(np.atleast_1d(tempo)[0]), beats=[round(float(b), 4) for b in bt],
               onsets=peaks(fulln, 0.07), kick=peaks(kick, 0.08), snare=peaks(snare, 0.08), hat=peaks(hat, 0.1), mid=peaks(mid, 0.08),
               loudness=loud, segments=bt_sec)
    (ROOT/'analysis'/f'{sid}.json').write_text(json.dumps(out))
    print(sid, round(dur,1), 'tempo', round(out['tempo'],2), 'beats', len(bt), 'onsets', len(out['onsets']), flush=True)
