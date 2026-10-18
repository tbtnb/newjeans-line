"""Onset detection with calibrated latency for chart audits (chart-research, 2026-10-18).
Envelope: log-mel spectral flux, n_fft 1024 @ 44.1 kHz (23 ms), hop 128 (2.9 ms), centred frames.
Latency is measured on synthetic transients (noise hits, kick-like sine drops, plucked tones) at known times and
subtracted, so reported onset times are attack times (when the sound starts), not envelope peaks."""
import numpy as np, librosa
SR, HOP, NFFT = 44100, 128, 1024

def flux(y, fmin=None, fmax=None, sr=SR):
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=NFFT, hop_length=HOP, n_mels=96, fmin=fmin or 20, fmax=fmax or sr / 2, center=True)
    L = librosa.power_to_db(S, ref=np.max(S) + 1e-12, top_db=80)
    d = np.maximum(0, np.diff(L, axis=1, prepend=L[:, :1])).mean(axis=0)
    return d

def norm(e):
    return e / (np.percentile(e, 99.5) + 1e-9)

def peaks(e, lag=0.0, thr=0.12, wait_s=0.06):
    """local maxima above thr (normalised), at least wait_s apart. returns arrays (times, strengths); times corrected by lag"""
    # local maxima (+-17 ms) above a running mean, then strongest-first non-maximum suppression within wait_s
    # (librosa's `wait` keeps the EARLIEST peak and drops a stronger one right after it, which hides real hits)
    idx = librosa.util.peak_pick(e, pre_max=6, post_max=6, pre_avg=40, post_avg=10, delta=0.02, wait=0)
    idx = idx[e[idx] >= thr]
    order = idx[np.argsort(-e[idx])]; keep = []; W = wait_s * SR / HOP
    taken = np.zeros(len(e), bool)
    for i in order:
        lo, hi = max(0, int(i - W)), int(i + W) + 1
        if taken[lo:hi].any(): continue
        taken[i] = True; keep.append(i)
    idx = np.array(sorted(keep), dtype=int)
    return idx * HOP / SR - lag, e[idx]

def calibrate():
    rng = np.random.default_rng(0); n = SR * 12; y = rng.normal(0, 0.003, n)
    T = np.arange(0.5, 11.5, 0.37)
    kinds = []
    for i, t in enumerate(T):
        k = i % 3; s = int(t * SR); m = int(0.25 * SR); tt = np.arange(m) / SR
        if k == 0: x = rng.normal(0, 0.4, m) * np.exp(-tt / 0.05)            # snare/clap-like noise hit
        elif k == 1: x = 0.8 * np.sin(2 * np.pi * (50 * tt + 60 * 0.03 * (1 - np.exp(-tt / 0.03)) * 3)) * np.exp(-tt / 0.12)   # kick-like
        else: x = 0.4 * np.sin(2 * np.pi * 440 * tt) * np.exp(-tt / 0.2) * np.minimum(1, tt / 0.004)   # plucked tone
        y[s:s + m] += x; kinds.append(k)
    e = norm(flux(y)); pt, ps = peaks(e)
    lags = [[], [], []]
    for t, k in zip(T, kinds):
        j = np.argmin(np.abs(pt - t))
        if abs(pt[j] - t) < 0.05: lags[k].append(pt[j] - t)
    return {name: float(np.median(l)) for name, l in zip(['noise', 'kick', 'pluck'], lags)}

if __name__ == '__main__':
    print(calibrate())
