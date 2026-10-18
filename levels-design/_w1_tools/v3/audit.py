"""Chart audit (user rules, 2026-10-18 11:55):
 (1) each section follows ONE musical layer -> a tap must be supported by that section's layer envelope;
 (5) no taps on ghost notes / faint onsets -> a tap must also be a visible onset in the FULL MIX;
 (2) repeated phrases get the same tap pattern -> bar-aligned slot consensus between repeats of the same section type;
 (4) sparse sections stay sparse -> nothing is ever added outside consensus.
Usage: audit.py <slug> -> v3/<slug>.audited.json + printed per-section report."""
import sys, json, os, numpy as np
os.chdir('/workspace/nj-w1-work'); sys.path.insert(0, '/workspace/nj-w1-work')
from chartgen import load, fps
s = sys.argv[1]
DR, VO, SY = 'drums', 'vocal', 'synth'
LAYERS = {
 'attention': {'Intro': VO, 'Hook A': DR, 'Verse 1': VO, 'Pre-chorus 1': VO, 'Chorus 1': DR, 'Verse 2': VO, 'Pre-chorus 2': VO, 'Chorus 2': DR, 'Final chorus': DR, 'Outro': VO},
 'hype-boy': {'Intro riff': SY, 'Verse 1': DR, 'Pre-chorus 1': VO, 'Build 1': DR, 'Chorus 1': DR, 'Post-chorus 1': DR, 'Verse 2': DR, 'Pre-chorus 2': VO, 'Build 2': DR, 'Chorus 2': DR, 'Final chorus': DR, 'Outro': VO},
 'cookie': {'Intro': DR, 'Verse 1': DR, 'Pre-chorus 1': VO, 'Chorus 1': DR, 'Verse 2': DR, 'Pre-chorus 2': VO, 'Chorus 2': DR, 'Jersey-club bridge': DR, 'Final chorus': DR, 'Dance break': DR, 'Outro': VO},
 'hurt': {'Intro': DR, 'Verse 1': VO, 'Pre-chorus 1': VO, 'Chorus 1': VO, 'Verse 2': VO, 'Breath': VO, 'Pre-chorus 2': VO, 'Chorus 2': VO, 'Bridge': VO, 'Final chorus': VO, 'Outro': VO},
}[s]
GROUPS = {
 'attention': [['Hook A', 'Chorus 1', 'Chorus 2', 'Final chorus'], ['Verse 1', 'Verse 2'], ['Pre-chorus 1', 'Pre-chorus 2']],
 'hype-boy': [['Verse 1', 'Verse 2'], ['Pre-chorus 1', 'Pre-chorus 2'], ['Build 1', 'Build 2'], ['Chorus 1', 'Chorus 2', 'Final chorus']],
 'cookie': [['Verse 1', 'Verse 2'], ['Pre-chorus 1', 'Pre-chorus 2'], ['Chorus 1', 'Chorus 2', 'Final chorus']],
 'hurt': [['Verse 1', 'Verse 2'], ['Pre-chorus 1', 'Pre-chorus 2'], ['Chorus 1', 'Chorus 2', 'Final chorus']],
}[s]
c = json.load(open(f'/workspace/newjeans-line-designs/{s}/chart.json'))
taps = [dict(t=x['t'], tag=x['tag']) for x in c['taps']]
a, E = load(s); P = a['beat_period']; ph = a['grid_phase']; dur = a['duration']
env = np.load(f'{s}.env.npz'); n = len(E['mix'])
def nrm(x): x = np.asarray(x[:n], float); return x / (np.percentile(x, 99.5) + 1e-9)
MIX = nrm(env['oenv'])
LAY = {DR: np.maximum(E['kick_on'][:n], E['snare_on'][:n]), VO: E['vocal_on'][:n], SY: np.maximum(E['mel_on'][:n], nrm(env['hat']) * 0.7)}
def pk(x, t, w):
    i0 = max(0, int((t - w) * fps)); i1 = min(n - 1, int((t + w) * fps) + 1); return float(x[i0:i1 + 1].max())
secs = c['sections']
def sec_of(t): return max([x for x in secs if x['t'] <= t + 1e-6], key=lambda x: x['t'])
def sec_end(x):
    k = secs.index(x); return secs[k + 1]['t'] if k + 1 < len(secs) else dur
TH_L, TH_M, TH_STRONG = 0.22, 0.10, 0.55
kept, removed = [], []
for tp in taps:
    sx = sec_of(tp['t']); L = LAYERS[sx['label']]
    lv, mv = pk(LAY[L], tp['t'], 0.03), pk(MIX, tp['t'], 0.025)
    tp['layer'] = L; tp['lv'] = round(lv, 2); tp['mv'] = round(mv, 2)
    anchor = abs(tp['t'] - sx['t']) < 0.2
    ok = (lv >= TH_L and mv >= TH_M) or (mv >= TH_STRONG and lv >= 0.1) or (anchor and mv >= 0.2)
    (kept if ok else removed).append(tp)
print(f'{s}: {len(taps)} taps, removed {len(removed)} (off-layer or faint): ' + ', '.join(f"{x['t']:.2f}({x['layer'][0]} l{x['lv']} m{x['mv']})" for x in removed[:40]))
# ---- repeated phrase consensus (bar-aligned 16th slots)
db = a['downbeat'] if 'downbeat' in a else ph
BAR = 4 * P; Q = P / 4
def slot(t, s0): return int(round((t - s0) / Q))
T = sorted(kept, key=lambda x: x['t'])
added, dropped = [], []
for grp in GROUPS:
    reps = [x for x in secs if x['label'] in grp]
    if len(reps) < 2: continue
    # align every repeat on its nearest downbeat
    def s0(x): return db + round((x['t'] - db) / BAR) * BAR
    spans = [(s0(x), sec_end(x)) for x in reps]
    Lmin = min(e - b for b, e in spans)
    sets = []
    for (b, e) in spans:
        sets.append({slot(tp['t'], b): tp for tp in T if b - 0.05 <= tp['t'] < b + Lmin - 0.05})
    allslots = set().union(*[set(x) for x in sets])
    for sl in sorted(allslots):
        have = [sl in st for st in sets]
        if all(have): continue
        # evidence at this slot in every repeat
        ev = []
        for (b, e), st in zip(spans, sets):
            t = b + sl * Q; L = LAYERS[sec_of(t)['label']]
            ev.append((pk(LAY[L], t, 0.03), pk(MIX, t, 0.025)))
        strong = [lv >= 0.32 and mv >= 0.16 for lv, mv in ev]
        if sum(have) * 2 >= len(have) and all(strong):
            for k, ((b, e), st) in enumerate(zip(spans, sets)):
                if not have[k]:
                    t = b + sl * Q; i0 = int((t - 0.018) * fps); i1 = int((t + 0.018) * fps)
                    j = i0 + int(np.argmax(MIX[i0:i1 + 1])); tt = j / fps if abs(j / fps - t) <= 0.018 else t
                    nt = dict(t=round(tt, 3), tag='kick' if LAYERS[sec_of(t)['label']] == DR else 'vocal', layer='consensus'); T.append(nt); added.append(nt['t'])
        else:
            for k, st in enumerate(sets):
                if have[k]:
                    tp = st[sl]; lv, mv = ev[k]
                    if not (lv >= 0.45 and mv >= 0.25):   # keep a one-off only when it is a clear, strong accent
                        if tp in T: T.remove(tp); dropped.append(tp['t'])
T.sort(key=lambda x: x['t'])
# enforce prior min gap (no new 16ths here)
out = []
for tp in T:
    if out and tp['t'] - out[-1]['t'] < 0.16:
        if tp.get('layer') == 'consensus': continue
        if out[-1].get('layer') == 'consensus': out[-1] = tp; continue
    out.append(tp)
print(f'   consensus: +{len(added)} -{len(dropped)}  -> {len(out)} taps')
rep = {}
for x in secs:
    e = sec_end(x); k = [tp for tp in out if x['t'] <= tp['t'] < e]; k0 = [tp for tp in taps if x['t'] <= tp['t'] < e]
    rep[x['label']] = dict(layer=LAYERS[x['label']], before=len(k0), after=len(k))
    print(f"   {x['label']:22s} {LAYERS[x['label']]:6s} {len(k0):3d} -> {len(k):3d}")
json.dump(dict(taps=[dict(t=tp['t'], tag=tp['tag']) for tp in out], report=rep, removed=[x['t'] for x in removed], dropped=dropped, added=added),
          open(f'/workspace/nj-w1-work/v3/{s}.audited.json', 'w'), indent=0)
