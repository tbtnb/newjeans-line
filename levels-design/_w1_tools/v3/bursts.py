"""Add short 16th-note bursts (2-4 taps) only where the audio has a real 16th event (hat/snare fill, rapid vocal
syllable, synth arp), inside allowed zones (fills before section changes, pre-chorus builds, drops, final choruses).
Gap floor 0.151 s (schema minimum 0.15 s): an inserted tap may be nudged by at most 10 ms to respect it.
Usage: bursts.py <slug>  -> v3/<slug>.taps16.json (list of {t, tag, src})"""
import sys, json, numpy as np
sys.path.insert(0, '/workspace/nj-w1-work')
from chartgen import load, fps
import os; os.chdir('/workspace/nj-w1-work'); s = sys.argv[1]
CFG = {
 'attention': dict(pct=76, budget=22, zones=[(42.0, 46.75), (56.0, 62.2), (74.0, 83.3), (110.0, 117.1), (128.0, 137.6), (137.6, 156.1)]),
 'hype-boy': dict(pct=84, budget=22, zones=[(34.0, 38.7), (48.2, 53.1), (66.0, 72.3), (88.0, 91.5), (125.0, 129.9), (143.0, 149.1), (149.05, 170.6)]),
 'cookie': dict(pct=90, budget=0, zones=[]),
 'hurt': dict(pct=88, budget=6, zones=[(125.0, 128.3), (128.26, 143.6)]),
}[s]
FLOOR, NUDGE = 0.151, 0.010
c = json.load(open(f'/workspace/newjeans-line-designs/{s}/chart.json'))
taps = [dict(t=x['t'], tag=x['tag'], src='chart') for x in c['taps']]
a, E = load(s); P = a['beat_period']; ph = a['grid_phase']
env = np.load(f'/workspace/nj-w1-work/{s}.env.npz')
n = len(E['mix'])
def nrm(x): x = x[:n]; return x / (np.percentile(x, 99.5) + 1e-9)
hat, sn, mix = nrm(env['hat']), nrm(env['snare']), nrm(env['oenv'])
voc = E['vocal_on'][:n]
SC = np.maximum.reduce([mix, 0.85 * hat, 0.9 * sn, 0.9 * voc])
def sal(t, w=0.02):
    i0 = max(0, int((t - w) * fps)); i1 = min(n - 1, int((t + w) * fps) + 1); seg = SC[i0:i1 + 1]; j = int(np.argmax(seg))
    return float(seg[j]), (i0 + j) / fps
# threshold: strong among all 16th off-positions of the song
g16 = ph + np.arange(int((a['duration'] - ph) / (P / 4))) * P / 4
offs = [sal(t)[0] for k, t in enumerate(g16) if k % 2 == 1]
thr = float(np.percentile(offs, CFG['pct']))
print(s, 'P', round(P, 4), '16th', round(P / 4, 4), 'thr', round(thr, 3))
def inzone(t): return any(z0 <= t < z1 for z0, z1 in CFG['zones'])
cands = []
T = [x['t'] for x in taps]
for i in range(len(T) - 1):
    A, B = T[i], T[i + 1]
    k0 = int(np.ceil((A - ph) / (P / 4) + 0.3)); k1 = int(np.floor((B - ph) / (P / 4) - 0.3))
    for k in range(k0, k1 + 1):
        tg = ph + k * P / 4
        if not inzone(tg): continue
        if (k % 2) == 0 and B - A < P * 0.8: continue  # only true 16th positions inside 8th-or-shorter gaps
        v, tp = sal(tg)
        if v < thr: continue
        if v < 0.6 * min(sal(A)[0], sal(B)[0]): continue
        t = tp if abs(tp - tg) <= 0.012 else tg
        lo, hi = A + FLOOR, B - FLOOR
        if lo > hi: continue
        t2 = min(max(t, lo), hi)
        if abs(t2 - t) > NUDGE: continue
        if not (t2 - A < 0.2 or B - t2 < 0.2): continue   # must create an actual 16th-speed gap
        cands.append((v, round(t2, 3), i))
cands.sort(reverse=True)
added = []
def runlen(ts, t):
    ts = sorted(ts + [t]); i = ts.index(t); L = 1; j = i
    while j > 0 and ts[j] - ts[j - 1] < 0.2: L += 1; j -= 1
    j = i
    while j + 1 < len(ts) and ts[j + 1] - ts[j] < 0.2: L += 1; j += 1
    return L, ts
cur = list(T)
for v, t, i in cands:
    if len(added) >= CFG['budget']: break
    L, ts = runlen(cur, t)
    if L > 4: continue
    k = ts.index(t)
    if k > 0 and t - ts[k - 1] < FLOOR - 1e-6: continue
    if k + 1 < len(ts) and ts[k + 1] - t < FLOOR - 1e-6: continue
    cur = ts; added.append((t, v))
out = taps + [dict(t=t, tag='hat' if hat[int(t * fps)] >= max(sn[int(t * fps)], voc[int(t * fps)]) else 'vocal' if voc[int(t * fps)] > sn[int(t * fps)] else 'snare', src='16th') for t, v in added]
out.sort(key=lambda x: x['t'])
gaps = np.diff([x['t'] for x in out])
print('added', len(added), 'total', len(out), 'min gap', round(float(gaps.min()), 3), 'at', sorted(t for t, v in added))
json.dump(out, open(f'/workspace/nj-w1-work/v3/{s}.taps16.json', 'w'), indent=0)
