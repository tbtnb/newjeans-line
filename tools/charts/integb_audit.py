"""Rhythm-logic audit used by integrator B (user rule 2026-10-18: rhythm logic beats density).
Same thresholds as chartlogic.py / the Ditto trim in ditto.py:
  faint      : followed layer < 0.35 and full mix < 0.35 and every other band < 0.5
  off-layer  : followed layer < 0.35 while another band >= 0.6 (tap belongs to a different layer)
  weak-burst : local gap < 0.15 s and neither the full mix nor the followed layer >= 0.6
Strengths: per-band onset envelopes in analysis/<slug>.env.npz (99.5th-percentile normalised), max within +-30 ms of the tap.
The followed layer per section is chosen as the band that explains the section's taps best (fewest flags, then highest
median strength) unless the song script pins it. Taps are only removed, never added."""
import json, statistics as st
import numpy as np
from common import ROOT
BANDS = ['kick', 'snare', 'hat', 'mid', 'vocal']
CANDS = ['drums', 'kick', 'snare', 'hat', 'mid', 'vocal']

class Env:
    def __init__(self, sid):
        E = np.load(ROOT / f'analysis/{sid}.env.npz'); self.h = float(E['hop_s'])
        self.e = {k: E[k].astype(float) / 100 for k in ['kick', 'snare', 'hat', 'mid', 'full'] + (['vocal'] if 'vocal' in E.files else [])}
        if 'vocal' not in self.e: self.e['vocal'] = self.e['mid']
        self.e['drums'] = np.maximum(self.e['kick'], self.e['snare'])
    def s(self, t, L):
        f = int(round(t / self.h)); w = int(round(0.03 / self.h)); a = self.e[L]
        return float(a[max(0, f - w):f + w + 1].max()) if f < len(a) else 0.0

def flag(env, T, i, L):
    t = T[i]; sl = env.s(t, L); sf = env.s(t, 'full')
    oth = max(env.s(t, k) for k in ['kick', 'snare', 'hat', 'mid'] if k != L and not (L == 'drums' and k in ('kick', 'snare')))
    gap = min(T[i] - T[i - 1] if i else 9, T[i + 1] - T[i] if i + 1 < len(T) else 9)
    if sl < 0.35 and sf < 0.35 and oth < 0.5: return 'faint', sl, sf
    if sl < 0.35 and oth >= 0.6: return 'off-layer', sl, sf
    if gap < 0.15 and sf < 0.6 and sl < 0.6: return 'weak-burst', sl, sf
    return None, sl, sf

def sec_of(secs, t): return max((k for k, s in enumerate(secs) if s['t'] <= t + 1e-6), default=0)

def choose_layers(env, taps, secs, pinned):
    T = [x['t'] for x in taps]; out = {}
    for k, s in enumerate(secs):
        idx = [i for i, t in enumerate(T) if sec_of(secs, t) == k]
        if k in pinned: out[k] = pinned[k]; continue
        if not idx: out[k] = 'full'; continue
        best = None
        for L in CANDS:
            nfl = sum(1 for i in idx if flag(env, T, i, L)[0])
            med = st.median(env.s(T[i], L) for i in idx)
            key = (nfl, -med)
            if best is None or key < best[0]: best = (key, L)
        out[k] = best[1]
    return out

def audit(sid, chart, pinned=None, keep=()):
    """returns (kept_taps, removed[(t, why, layer, sl, sf)], layers{section index: layer})"""
    env = Env(sid); secs = sorted(chart['sections'], key=lambda s: s['t'])
    taps = sorted(chart['taps'], key=lambda x: x['t'])
    layers = choose_layers(env, taps, secs, pinned or {})
    removed = []
    for _ in range(4):
        T = [x['t'] for x in taps]; kept = []
        for i, x in enumerate(taps):
            L = layers[sec_of(secs, x['t'])]
            why, sl, sf = flag(env, T, i, L)
            if why and round(x['t'], 3) not in keep: removed.append((x['t'], why, L, round(sl, 2), round(sf, 2), x.get('tag')))
            else: kept.append(x)
        if len(kept) == len(taps): break
        taps = kept
    return taps, sorted(removed), layers
