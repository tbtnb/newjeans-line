"""Ditto rhythm v3 (user rule: rhythmic logic beats density).
Each section follows ONE audible layer; the tap pattern is derived from that layer's average 16th-step strength over
the section's phrases, so repeated phrases get the same pattern; per-phrase steps whose own onset is faint are dropped
(no ghost onsets). Fill bars use the full mix and allow 16ths only where every step is clearly audible."""
import json
from common import ROOT
g = json.load(open(ROOT / 'analysis/ditto.grid.json')); B = g['bars']
EVEN = [s for s in range(16) if s % 2 == 0]; BEATS = [0, 4, 8, 12]; ALL = list(range(16))
# (bar0, bar1, label, kind, follows, threshold, allowed steps, phrase_bars, fill bars, note)
SECTIONS = [
    (0, 8, 'Intro · 雪原', 'intro', 'kick', -1, [0, 8, 12], 1, [], 'per-bar: only where a kick/choir entry is actually detected (>=0.45); long straights'),
    (8, 16, 'Hook · 雪林', 'verse', 'full', 0.55, ALL, 1, [15], 'Baltimore-club accents of the whole beat (1, e-and of 1, a-of-2, 4-and)'),
    (16, 24, 'Verse · 校舍', 'verse', 'full', 0.55, EVEN, 2, [], 'beat accents under the verse vocal'),
    (24, 31, 'Verse b · 走廊', 'verse', 'full', 0.6, EVEN, 2, [30], 'same layer, tighter'),
    (31, 40, 'Pre · 体育馆', 'pre', 'kick', 0.55, BEATS + [11], 2, [39], 'band drops out: kick only'),
    (40, 48, 'Chorus · 雪桥', 'chorus', 'full', 0.62, EVEN, 2, [47], 'chorus beat accents (vocal + snare land together)'),
    (48, 64, 'Post · Stay in the middle', 'post', 'full', 0.55, ALL, 4, [63], 'the "stay in the middle" groove, 4-bar phrase'),
    (64, 71, 'Bridge · 冰湖', 'bridge', 'kick', 0.45, EVEN, 1, [], 'thin groove: kick only, sparse'),
    (71, 79, 'Break · 夜', 'break', 'full', -2, BEATS + [2, 6, 10, 14], 1, [78], 'almost silent: per-bar, only clearly audible hits (>=0.45)'),
    (79, 96, 'Final · 黎明', 'chorus', 'full', 0.5, EVEN, 2, [86, 90, 94, 95], 'heaviest section: the chorus accents, denser, plus fills'),
    (96, 103, 'Outro · 光', 'outro', 'full', 0.75, [0, 8], 1, [], 'choir chords on half-bars, thinning out'),
]
FILL_THR, FILL16_THR = 0.7, 0.85

def s(bar, step, L): return B[bar][L][step] if bar < len(B) else 0.0

PAT = {}
def build():
    taps, secs = [], []
    for b0, b1, label, kind, L, thr, allowed, pb, fills, note in SECTIONS:
        secs.append({'bar': b0, 'label': label, 'kind': kind, 'follows': L, 'note': note})
        normal = [b for b in range(b0, b1) if b not in fills]
        # average strength per phrase-step over the section's normal bars
        acc = {}
        for b in normal:
            k = ((b - b0) % pb) * 16
            for st in allowed: acc.setdefault(k + st, []).append(s(b, st, L))
        pattern = sorted(k for k, v in acc.items() if sum(v) / len(v) >= thr)
        if thr < 0:   # per-bar mode for sparse sections: tap only where this bar has a clear onset
            for b in normal:
                for st in allowed:
                    if max(s(b, st, L), s(b, st, 'mid'), s(b, st, 'full')) >= (0.45 if thr == -1 else 0.6): taps.append((b, st, L))
            PAT[label] = 'per-bar'
            normal = []
        else: PAT[label] = pattern
        for b in normal:
            k0 = ((b - b0) % pb) * 16
            for st in [p - k0 for p in pattern if k0 <= p < k0 + 16]:
                if s(b, st, L) >= 0.4:      # drop ghost onsets in this phrase instance (chartlogic FAINT = 0.35)
                    taps.append((b, st, L))
        for b in fills:
            # fills: 8ths where the full mix is clear; 16ths only inside runs where every 16th is clearly audible
            row = [s(b, st, 'full') for st in range(16)]; sn = [max(s(b, st, 'snare'), s(b, st, 'kick'), s(b, st, 'hat')) for st in range(16)]
            strong16 = [st for st in range(16) if row[st] >= FILL16_THR or sn[st] >= FILL16_THR]
            run = []
            for st in range(16):
                if st in strong16: run.append(st)
                else:
                    if len(run) >= 3: break
                    run = []
            run = run if len(run) >= 3 else []
            run = run[:6]
            for st in range(16):
                if st in run or (st % 2 == 0 and row[st] >= FILL_THR):
                    taps.append((b, st, 'fill16' if st in run else 'fill'))
    return taps, secs, SECTIONS
