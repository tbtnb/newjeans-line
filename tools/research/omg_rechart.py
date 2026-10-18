"""Re-chart OMG from the audio with explicit charting rules (docs/research/charting-logic.md).
Each section names the layer(s) it follows and the grid steps it may use; a step becomes part of the section's
pattern when the layer has a clear onset there in most bars of the same phrase role (bar parity), so repeated
phrases get the same pattern (consistency), and a templated step is dropped in a bar where the layer is silent
(no ghost taps). Phrase-end bars may add fills/pickups that are strong in that bar only. Tap times are the
16th-grid times (grid fitted to gapless kick/snare onsets), nudged to the layer's real onset when it is within
+-18 ms (drums are quantised; vocals stay on the intended grid). Writes levels-src/omg/chart.json taps+sections
(directions are chosen afterwards by the route search).
Usage: omg_rechart.py [--dry]"""
import sys, json, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import onsets as O
ROOT = Path(__file__).resolve().parents[2]
C = dict(np.load(ROOT / 'analysis/research/omg-onsets.npz')); ENV = {k[4:]: C[k] for k in C if k.startswith('env_')}
LAG = -0.0072; P = json.load(open(ROOT / 'analysis/omg.grid.json'))['period']
sys.argv_saved = sys.argv; sys.argv = [sys.argv[0], 'omg']
from barmap import B0
sys.argv = sys.argv_saved
S16 = P / 4
def gt(bar, step): return B0 + (bar * 16 + step) * S16
def sal(L, t, w=0.025):
    f = int(round((t + LAG) * O.SR / O.HOP)); ww = int(w * O.SR / O.HOP); e = ENV[L]
    if f + ww >= len(e) - 1 or t > 211.0: return 0.0
    v = float(e[max(0, f - ww):f + ww + 1].max())
    if L in ('vocals', 'other', 'bass'):
        rel = ENV['rel_' + L][max(0, f - ww):f + ww + 1].max()
        if rel < -14: v *= 0.3     # present in the stem but buried in the mix
    return v
def lay(spec, t):
    """spec: 'kick+snare' -> max over layers"""
    return max(sal(L, t) for L in spec.split('+'))
PK = {L: O.peaks(ENV[L], LAG) for L in ['kick', 'snare', 'vocals', 'other', 'bass', 'full', 'hat']}
def peak_near(spec, t, tol=0.03):
    best = (t, 0.0)
    for L in spec.split('+'):
        pt, ps = PK[L]; w = np.where(np.abs(pt - t) <= tol)[0]
        for j in w:
            v = float(ps[j])
            if L in ('vocals', 'other', 'bass'):
                f = int(round((pt[j] + LAG) * O.SR / O.HOP))
                if ENV['rel_' + L][f] < -14: v *= 0.3
            if v > best[1]: best = (float(pt[j]), v)
    return best
def snap(t, spec, tol=0.018):
    best = None
    for L in spec.split('+'):
        pt, ps = PK[L]; w = np.where(np.abs(pt - t) <= tol)[0]
        for j in w:
            if best is None or ps[j] > best[1]: best = (pt[j], ps[j])
    return float(best[0]) if best is not None and best[1] >= 0.35 else t

# ---- section plan (bar ranges on the fitted grid; bar b starts at B0 + b*4P) ----
# rule fields: layer, steps (16th indices allowed), thr (clear onset), vote (fraction of same-role bars needing it)
SECTIONS = [
  dict(label='Intro · 病房走廊', kind='intro', bars=(0, 8), follows='other', mode='free',
       rules=[dict(layer='vocals', steps=range(0, 16, 2), thr=0.85, mingap=0.42, bars=(0, 7)),
              dict(layer='snare+kick', steps=[8, 12, 14], thr=0.8, mingap=0.2, bars=(7, 8))],
       note='intro melody (vocal ad-libs doubled by the synth; chosen on the vocal stem, sparse on purpose, 8th grid = intended rhythm), then the drum pickup into the verse'),
  dict(label='Verse 1 · 治疗桌与五椅', kind='verse', bars=(8, 16), follows='snare+kick',
       rules=[dict(layer='snare+kick', steps=[0, 6, 8, 14], thr=0.5, vote=0.6),
              dict(layer='vocals', steps=[4, 12], thr=0.9, vote=0.5)],
       note='clap groove 0/6/14 (+8) and the vocal accent on beat 2 when it is the loudest event'),
  dict(label='Verse 1b · 墙板外折', kind='verse', bars=(16, 24), follows='snare+kick',
       rules=[dict(layer='snare', steps=[0, 4, 12], thr=0.55, vote=0.6), dict(layer='bass+kick', steps=[10], thr=0.6, vote=0.6),
              dict(layer='snare+kick', steps=[14], thr=0.7, vote=0.6)],
       note='backbeat clap 2&4 + downbeat, bass/kick syncopation on 3-and; same 2-bar pattern'),
  dict(label='Chorus 1 · 黑兔舞台', kind='chorus', bars=(24, 32), follows='kick+snare',
       rules=[dict(layer='kick+snare', steps=[0, 2, 4, 8, 12, 14], thr=0.55, vote=0.6)],
       note='halftime kick/snare groove, same 2-bar pattern as every chorus'),
  dict(label='Verse 2 · 玻璃鞋', kind='verse', bars=(32, 40), follows='snare+kick', same_as='Verse 1b · 墙板外折'),
  dict(label='Verse 2b · 双折长短路', kind='pre', bars=(40, 48), follows='snare+kick', same_as='Verse 1b · 墙板外折'),
  dict(label='Pre · 手机桥', kind='break', bars=(48, 56), follows='vocals',
       rules=[dict(layer='vocals', steps=range(0, 16, 2), thr=0.75, mingap=0.2)], mode='free',
       note='breakdown: the drums drop out and the vocal leads, so the taps follow the sung syllables (8th grid, mostly on beats 1-3); sparse on purpose'),
  dict(label='Chorus 2 · 屏幕块', kind='chorus', bars=(56, 64), follows='kick+snare', same_as='Chorus 1 · 黑兔舞台'),
  dict(label='Post · 错列直角', kind='post', bars=(64, 71), follows='snare+kick', same_as='Verse 1b · 墙板外折'),
  dict(label='Bridge · 书页墙与猫', kind='bridge', bars=(71, 79), follows='kick+snare',
       rules=[dict(layer='snare+kick', steps=[0, 8], thr=0.6, vote=0.5), dict(layer='kick+snare', steps=[3, 6, 13], thr=0.7, vote=0.6)],
       note='trap kick 3-3-2 figure (3, 6, 13), now anchored on the downbeat snare and beat 3'),
  dict(label='Break · 书页合拢', kind='break', bars=(79, 80), follows='snare', mode='free',
       rules=[dict(layer='snare+kick', steps=[0, 8], thr=0.8, mingap=0.2)], note='stop-time hits on 1 and 3'),
  dict(label='Dance break · 舞台五墙', kind='drop', bars=(80, 88), follows='kick+snare',
       rules=[dict(layer='kick+snare', steps=[0, 4, 8, 12], thr=0.6, vote=0.6), dict(layer='snare+hat', steps=[2, 6, 10, 14], thr=0.85, vote=0.6)],
       note='four-on-the-floor + 8th snare/hat runs where the drum line plays them'),
  dict(label='Final chorus · 兔耳发夹', kind='chorus', bars=(88, 96), follows='kick+snare', same_as='Chorus 1 · 黑兔舞台'),
  dict(label='Final chorus b · 天桥', kind='chorus', bars=(96, 104), follows='kick+snare', same_as='Chorus 1 · 黑兔舞台'),
  dict(label='Outro · 尾奏琴键', kind='outro', bars=(104, 113), follows='other', mode='free',
       rules=[dict(layer='other', steps=range(0, 16, 2), thr=0.75, mingap=0.4)], note='piano/synth stabs only'),
]
BYL = {s['label']: s for s in SECTIONS}
for s in SECTIONS:
    if 'same_as' in s:
        src = BYL[s['same_as']]; s['rules'] = src['rules']; s.setdefault('note', src['note'] + ' (same pattern as ' + src['label'] + ')')
# phrase-end fills: strong full-mix/drum events in the last bar of each 4-bar phrase that the template does not cover
FILL_THR = 0.9
def choose():
    taps = []; secs = []; report = []
    for s in SECTIONS:
        b0, b1 = s['bars']
        CL = {'snare+kick': 'drums', 'kick+snare': 'drums', 'vocals': 'vocal', 'other': 'mid', 'bass+kick': 'kick', 'snare': 'snare'}
        secs.append({'t': round(gt(b0, 0), 3), 'label': s['label'], 'kind': s['kind'], 'follows': CL.get(s['follows'], s['follows']), 'follows_layers': s['follows'], 'follows_note': s['note']})
        chosen = set()
        if s.get('mode') == 'free':
            for r in s['rules']:
                last = -9; t0, t1 = gt(b0, 0) - 0.05, gt(b1, 0) - 0.05
                cands = sorted({round(t, 4) for L in r['layer'].split('+') for t in PK[L][0] if t0 <= t < t1})
                for t in cands:
                    tt, v = peak_near(r['layer'], t, 0.002)
                    if v < r['thr'] or t - last < r['mingap'] or t < 1.0 or t > 210.5: continue
                    q = (t - B0) / S16; k = int(round(q)); err = (q - k) * S16
                    if k % 16 not in r['steps'] or abs(err) > 0.045: continue   # only allowed grid steps (intended rhythm)
                    if 'bars' in r and not (r['bars'][0] <= k // 16 < r['bars'][1]): continue
                    tq = t if abs(err) <= 0.02 else gt(k // 16, k % 16)         # vocals: keep the intended grid time
                    chosen.add((k // 16, k % 16, r['layer'], tq)); last = t
        else:
            group = [g for g in SECTIONS if g['label'] == s['label'] or g.get('same_as', g['label']) == s.get('same_as', s['label'])]
            for r in s['rules']:
                for par in (0, 1):
                    bars = [b for b in range(b0, b1) if (b - b0) % 2 == par]
                    gbars = [b for g in group for b in range(*g['bars']) if (b - g['bars'][0]) % 2 == par]
                    for st in r['steps']:
                        hits = [b for b in gbars if lay(r['layer'], gt(b, st)) >= r['thr']]
                        if len(hits) >= r['vote'] * len(gbars):
                            for b in bars:
                                if lay(r['layer'], gt(b, st)) >= 0.35 and peak_near(r['layer'], gt(b, st), 0.035)[1] >= 0.3 and sal('full', gt(b, st)) >= 0.33: chosen.add((b, st, r['layer']))
                                else: report.append(f"{s['label']}: bar {b} step {st} dropped (no onset in the layer, {peak_near(r['layer'], gt(b, st))[1]:.2f})")
            # phrase-end fills
            for bar in range(b0 + 3, b1, 4):
                for st in range(0, 16, 2):
                    if any(c[0] == bar and c[1] == st for c in chosen): continue
                    t = gt(bar, st); v = max(sal('full', t), sal('snare', t), sal('kick', t))
                    if v >= FILL_THR and st >= 8 and sal('full', t) >= 0.35: chosen.add((bar, st, 'full+snare+kick')); report.append(f"{s['label']}: fill bar {bar} step {st} ({v:.2f})")
        for c in sorted(chosen):
            bar, st, L = c[:3]
            t = c[3] if len(c) > 3 else snap(gt(bar, st), L)
            taps.append({'t': round(t, 3), 'tag': L.split('+')[0], 'bar': bar, 'step': st})
    # dedupe and min gap 0.105 (keep the stronger)
    taps.sort(key=lambda x: x['t']); out = []
    for x in taps:
        if out and x['t'] - out[-1]['t'] < 0.105:
            if lay('full', x['t']) > lay('full', out[-1]['t']): out[-1] = x
            continue
        out.append(x)
    return out, secs, report

if __name__ == '__main__':
    taps, secs, report = choose()
    print(len(taps), 'taps')
    for r in report: print('  ', r)
    if '--dry' not in sys.argv:
        p = ROOT / 'levels-src/omg/chart.json'; ch = json.load(open(p))
        if '--out' in sys.argv: p = Path(sys.argv[sys.argv.index('--out') + 1])
        old = ch['taps']
        ch['taps'] = [{'t': x['t'], 'tag': x['tag']} for x in taps]
        ch['sections'] = secs
        m = ch.setdefault('meta', {})
        m['rechart'] = {'tool': 'tools/research/omg_rechart.py', 'rules': 'docs/research/charting-logic.md', 'grid': {'bpm': round(60 / P, 3), 'beat0': round(B0, 4), 'note': 'fitted to gapless-decoded kick/snare onsets (the demucs stems are 25.1 ms late and are re-aligned)'}, 'previous_taps': len(old)}
        m['beat0'] = round(B0, 4); m['beat_period'] = P
        for k in ('snap_sources', 'bursts', 'ghost_taps_removed', 'integration', 'integc_removed', 'integc_repair'): m.pop(k, None)
        json.dump(ch, open(p, 'w'), indent=1, ensure_ascii=False)
