"""Add short fast bursts + off-beat syncopation where the stems have real fast events (user steering 11:48).
Hard floor: validator min gap 0.15 s, so the fastest legal subdivision is used:
  SN 109 BPM / BG 105 / HS 125: 8th-note TRIPLETS (0.183 / 0.190 / 0.160 s)  -- true 16ths (0.138/0.143/0.120 s) are below 0.15 s
  RN 172 BPM: 8ths are already 0.174 s; 16ths (0.087 s) impossible -> only syncopation.
Usage: burst.py <slug> <max_bursts> <max_sync>"""
import json, sys, numpy as np
slug, MAXB, MAXS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
W = '/workspace/w4'
raw = json.load(open(f'{W}/{slug}.chart.raw.orig.json')); g = json.load(open(f'{W}/{slug}.grid.json'))
P = g['period'] if 'period' in g else g['beat']
on = json.load(open(f'{W}/{slug}.stem_onsets.json'))
secs = raw['sections']; taps = [dict(t) for t in raw['taps']]
bar0 = g.get('bar0'); 
def sec_of(t): return ([s for s in secs if s['t'] <= t + 1e-6] or secs[:1])[-1]
HOT = ('pre', 'chorus', 'build', 'drop')
def strong(stem, q=45):
    a = np.array(on[stem]); thr = np.percentile(a[:, 1], q); return a[a[:, 1] >= thr][:, 0]
EV = {k: strong(k) for k in ('hat', 'snare', 'other', 'vocal', 'kick')}
def hit(t, tol=0.028, stems=('hat', 'snare', 'other', 'vocal')):
    best = None
    for k in stems:
        a = EV[k]; i = np.searchsorted(a, t)
        for j in (i - 1, i):
            if 0 <= j < len(a) and abs(a[j] - t) <= tol and (best is None or abs(a[j] - t) < best[0]): best = (abs(a[j] - t), k)
    return best
T = lambda: sorted(x['t'] for x in taps)
trip = P / 3
added = []; nb = 0
# candidate beats: the last beat of every 2-bar phrase inside hot sections (fills / pickups into the next phrase)
beats = [bar0 + k * P for k in range(int((raw['taps'][-1]['t'] - bar0) / P) + 1)]
cands = []
for k, b in enumerate(beats):
    s = sec_of(b)
    if s['kind'] not in HOT and 'build' not in s['label'].lower(): continue
    if (k % 4) != 3: continue
    m = [hit(b + trip), hit(b + 2 * trip)]
    if all(m) and trip >= 0.15:
        sc = sum(0.03 - x[0] for x in m) + (0.02 if (k % 8) == 7 else 0); cands.append((sc, b, m))
cands.sort(key=lambda c: -c[0])
for sc, b, m in cands:
    if nb >= MAXB: break
    new = [round(b + trip, 3), round(b + 2 * trip, 3)]
    # clear the beat interior, keep the beat tap and the next downbeat
    tt = T()
    taps = [x for x in taps if not (b + 0.03 < x['t'] < b + P - 0.03)]
    for nt in new: taps.append({'t': nt, 'tag': 'fill-triplet', 'src': m[new.index(nt)][1]})
    if not any(abs(x['t'] - b) < 0.03 for x in taps): taps.append({'t': round(b, 3), 'tag': 'fill-triplet'})
    if not any(abs(x['t'] - (b + P)) < 0.03 for x in taps): taps.append({'t': round(b + P, 3), 'tag': 'accent'})
    taps.sort(key=lambda x: x['t']); added.append(('triplet', round(b, 3), [x[1] for x in m])); nb += 1
# syncopation: off-beat 16ths ('e' = 1/4, 'a' = 3/4 of a beat) on strong snare/kick/vocal onsets, only where both neighbours stay >= 0.15 s
cs = []
for b in beats:
    sk = sec_of(b)['kind']
    if sk in ('intro', 'outro', 'break'): continue
    for frac in (0.25, 0.75):
        t = b + frac * P; h = hit(t, 0.025, ('snare', 'kick', 'vocal'))
        if h: cs.append(((0.03 - h[0]) + (0.02 if sk in HOT else 0), t, h[1], frac))
cs.sort(key=lambda c: -c[0]); ns = 0; syn = []
for sc, t, src, frac in cs:
    if ns >= MAXS: break
    tt = T(); i = np.searchsorted(tt, t)
    prev = tt[i - 1] if i > 0 else -9; nxt = tt[i] if i < len(tt) else 9e9
    if t - prev >= 0.15 and nxt - t >= 0.15 and not any(abs(t - x) < 1.2 for x in syn):
        taps.append({'t': round(t, 3), 'tag': 'synco-16th', 'src': src}); taps.sort(key=lambda x: x['t']); syn.append(round(t, 3)); ns += 1
tt = T(); gaps = np.diff(tt)
assert gaps.min() >= 0.149, gaps.min()
raw['taps'] = taps
json.dump(raw, open(f'{W}/{slug}.chart.raw.json', 'w'), indent=0)
print(slug, 'taps', len(raw['taps']), 'bursts', added, 'syncopations', syn, 'min gap', round(gaps.min(), 3))
