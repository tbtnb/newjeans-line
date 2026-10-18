"""Re-audit charts against the 11:55 rhythmic-logic rules (user override):
 (1) one audible layer per section, (2) repeated phrases -> same pattern, (3) 16th bursts only where the figure is prominent in the FULL MIX,
 starting/ending on beats, (4) breathing room, (5) no taps on faint onsets.  Input: <slug>.chart.raw.orig.json (curated chart before burst.py).
 Output: <slug>.chart.raw.json + <slug>.audit.json (log).  Usage: audit.py <slug> [max_bursts]"""
import json, sys, numpy as np, collections
slug = sys.argv[1]; MAXB = int(sys.argv[2]) if len(sys.argv) > 2 else 6
raw = json.load(open(f'{slug}.chart.raw.orig.json')); g = json.load(open(f'{slug}.grid.json'))
an = json.load(open(f'/workspace/newjeans-line-designs/{slug}/analysis.json')); OM = {k: np.array(v) for k, v in an['onset_candidates_mix'].items()}
MED = {k: float(np.median(v[:, 1])) for k, v in OM.items()}
P = g['period']; B0 = g['bar0']; SUB = 8 if max(t['slot8'] for t in raw['taps']) < 8 else 16
secs = raw['sections']; dur = an['duration']
def sec_i(t): return max([i for i, s in enumerate(secs) if s['t'] <= t + 1e-6] or [0])
def mix(t, band, tol=0.04):
    a = OM[band]; d = np.abs(a[:, 0] - t); m = d <= tol
    return float(a[m, 1].max()) / MED[band] if m.any() else 0.0
DR = {'kick', 'clap', 'bass'}; ME = {'vocal', 'melody'}
BAND = {'kick': 'kick', 'bass': 'kick', 'clap': 'snare', 'vocal': 'vocal', 'melody': 'all', 'phrase': 'all', 'accent': 'all'}
def slot_time(bar, slot): return round(B0 + bar * 4 * P + slot * 4 * P / SUB, 3)
taps = [dict(t) for t in raw['taps']]; log = collections.defaultdict(list)
# ---- (1) layer per section
layer = {}
for i, s in enumerate(secs):
    inn = [t for t in taps if sec_i(t['t']) == i]
    nd = sum(t['tag'] in DR for t in inn); nm = sum(t['tag'] in ME for t in inn)
    layer[i] = 'drums' if (nd >= nm or s['kind'] not in ('intro', 'outro', 'break')) else 'melodic'
keep = []
for t in taps:
    i = sec_i(t['t']); L = layer[i]; ok = (t['tag'] in DR) if L == 'drums' else (t['tag'] in ME or t['tag'] == 'phrase')
    if t['tag'] == 'phrase': ok = True
    if not ok:
        if L == 'drums':
            k, sn = mix(t['t'], 'kick', 0.035), mix(t['t'], 'snare', 0.035)
            if max(k, sn) >= 1.0: t['tag'] = 'kick' if k >= sn else 'clap'; log['retag'].append(t['t']); ok = True
        else:
            if max(mix(t['t'], 'vocal', 0.035), mix(t['t'], 'all', 0.035)) >= 1.0: t['tag'] = 'melody'; log['retag'].append(t['t']); ok = True
    if not ok: log['off_layer_removed'].append((t['t'], t['tag'])); continue
    keep.append(t)
taps = keep
# ---- (5) faint onsets
keep = []
for t in taps:
    rb, ra = mix(t['t'], BAND.get(t['tag'], 'all')), mix(t['t'], 'all')
    if rb < 0.7 and ra < 0.7 and t['tag'] != 'phrase': log['faint_removed'].append((t['t'], t['tag'], round(rb, 2), round(ra, 2))); continue
    keep.append(t)
taps = keep
# ---- (2) repetition
def pat(bar): return frozenset(t['slot8'] for t in taps if t['bar'] == bar)
def lay_ok(bar, slot, i):
    tt = slot_time(bar, slot)
    if layer[i] == 'drums': return max(mix(tt, 'kick', 0.035), mix(tt, 'snare', 0.035)) >= 0.8
    return max(mix(tt, 'vocal', 0.035), mix(tt, 'all', 0.035)) >= 0.8
def set_pat(bar, P_new, i, why):
    global taps
    old = pat(bar); add = P_new - old; rem = old - P_new
    if any(not lay_ok(bar, s, i) for s in add): return False
    trial = [t for t in taps if not (t['bar'] == bar and t['slot8'] in rem)] + [{'t': slot_time(bar, s), 'tag': ('kick' if mix(slot_time(bar, s), 'kick', 0.035) >= mix(slot_time(bar, s), 'snare', 0.035) else 'clap') if layer[i] == 'drums' else 'melody', 'bar': bar, 'slot8': s, 'sec': secs[i]['label'], 'rep': why} for s in add]
    tt = sorted(x['t'] for x in trial)
    if min(np.diff(tt)) < 0.15: return False
    taps = sorted(trial, key=lambda x: x['t']); log['unified'].append((bar, why, sorted(add), sorted(rem))); return True
bars_of = {i: list(range(*[b for b in an['sections'][i]['bars']])) for i in range(len(secs))} if len(an['sections']) == len(secs) else None
if bars_of:
    # across instances of the same kind (chorus 1 / chorus 2 / final chorus ...): per bar index pick ONE pattern for all instances:
    # the densest candidate whose every slot is audible (layer onset in the mix) in every instance; fill bars (last bar) excluded
    kinds = collections.defaultdict(list)
    for i, s in enumerate(secs): kinds[s['kind']].append(i)
    for k, idx in kinds.items():
        if k in ('intro', 'outro') or len(idx) < 2: continue
        n_b = min(len(bars_of[i]) for i in idx) - 1
        for n in range(n_b):
            bs = [(bars_of[i][n], i) for i in idx]; ps = [pat(b) for b, _ in bs]
            if len(set(ps)) == 1: continue
            for cand in sorted(set(ps), key=lambda x: -len(x)):
                if all(len(cand ^ p_) <= 2 and all(lay_ok(b, sl, i) for sl in cand) for (b, i), p_ in zip(bs, ps)):
                    for (b, i), p_ in zip(bs, ps):
                        if p_ != cand: set_pat(b, cand, i, f'{k} instances bar {n}')
                    break
    # within a section: bar i+4 repeats bar i (phrase call/answer), last bar (fill) excluded
    for i, bl in bars_of.items():
        for n in range(len(bl) - 5):
            ba, bb = bl[n], bl[n + 4]
            if bb == bl[-1]: continue
            pa, pb = pat(ba), pat(bb)
            if pa != pb and len(pa ^ pb) <= 2: set_pat(bb, pa, i, f'{secs[i]["label"]} bar {n} (+4)')
# ---- (3) 16th bursts, full-mix check
q = P / 4; bursts = []
if q >= 0.105:
    cands = []
    for i, s in enumerate(secs):
        if s['kind'] in ('intro', 'outro') or not bars_of: continue
        bl = bars_of[i]
        for n, bar in enumerate(bl):
            if (n % 4) != 3: continue
            b = B0 + bar * 4 * P + 3 * P   # last beat of a 4-bar phrase
            inner = [b + k * q for k in (1, 2, 3)]
            sc = [max(mix(x, 'snare', 0.025), mix(x, 'hat', 0.025), mix(x, 'all', 0.025)) for x in inner]
            ends = [max(mix(b, 'snare'), mix(b, 'kick'), mix(b, 'all')), max(mix(b + P, 'snare'), mix(b + P, 'kick'), mix(b + P, 'all'))]
            if min(sc) >= 1.05 and min(ends) >= 1.0: cands.append((min(sc), round(b, 3), i, bar))
    for sc, b, i, bar in sorted(cands, reverse=True)[:MAXB]:
        taps = [t for t in taps if not (b + 0.03 < t['t'] < b + P - 0.03)]
        for k in range(0, 5):
            tt = round(b + k * q, 3)
            if not any(abs(t['t'] - tt) < 0.03 for t in taps): taps.append({'t': tt, 'tag': 'fill-16th' if 0 < k < 4 else 'clap', 'bar': bar + (1 if k == 4 else 0), 'slot8': (12 + 4 * k // 4 * (SUB // 16)) if k < 4 else 0, 'sec': secs[i]['label']})
        taps.sort(key=lambda x: x['t']); bursts.append((b, round(sc, 2), secs[i]['label']))
    log['bursts_16th'] = sorted(bursts)
tt = [t['t'] for t in taps]; gaps = np.diff(tt)
assert gaps.min() >= 0.104, gaps.min()
taps = [t for t in taps if 1.0 <= t['t'] <= dur - 1]
raw['taps'] = taps; json.dump(raw, open(f'{slug}.chart.raw.json', 'w'), indent=0)
lay = {secs[i]['label']: layer[i] for i in layer}; log['layers'] = lay
json.dump(log, open(f'{slug}.audit.json', 'w'), indent=1)
print(slug, len(raw['taps']), 'from', len(json.load(open(f'{slug}.chart.raw.orig.json'))['taps']), {k: len(v) for k, v in log.items() if isinstance(v, list)}, 'bursts', bursts, 'min gap', round(float(gaps.min()), 3))
