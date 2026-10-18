"""Append the integ-b rhythm-logic audit to levels-design/<slug>/chart-report.md (idempotent: replaces its own section).
Usage: integb_report.py <slug> [...]"""
import json, sys, statistics as stt
sys.path.insert(0, __import__('os').path.dirname(__file__))
from common import ROOT
from integb_audit import Env, sec_of
NAME = {'drums': 'kick + snare drum groove (full mix)', 'kick': 'kick drum', 'snare': 'snare / clap backbeat', 'hat': 'hi-hat / shaker',
        'mid': 'melody / synth / vocal line (mid band)', 'vocal': 'lead vocal syllables (vocal stem, gated to the full mix)', 'full': 'full-mix accents'}
MARK = '## Rhythm-logic audit (integ-b)'
for sid in sys.argv[1:]:
    d = ROOT / f'levels-design/{sid}'; pre = json.load(open(d / 'pre-audit/chart.json')); new = json.load(open(d / 'chart.json'))
    env = Env(sid); secs = sorted(new['sections'], key=lambda s: s['t']); au = new['meta']['audit']
    T0 = [x['t'] for x in pre['taps']]; T1 = [x['t'] for x in new['taps']]
    L = [MARK, '', f"Audited on 2026-10-18 by integrator B against the user's rule *rhythm logic beats density* " + ("(W2 already audited this chart with stem analysis; this pass applies the same full-mix thresholds that were applied to Ditto, so a few W2 kick/burst taps that are not clear in the full mix were dropped). " if sid == 'super-shy' else "(this chart was made before the rule). ") +
         f"Taps **{len(T0)} → {len(T1)}** ({len(T1)-len(T0):+d}; {len(au['removed'])} removed, 0 added). Nothing was added to reach a CPM target.", '',
         'Method (same thresholds as `tools/charts/chartlogic.py` and the Ditto trim): each section follows the one band that best explains its taps; a tap is removed if it is '
         '**faint** (followed band < 0.35, full mix < 0.35, every other band < 0.5), **off-layer** (followed band < 0.35 while another band ≥ 0.6) or a **weak burst** '
         '(gap < 0.15 s and neither the full mix nor the followed band ≥ 0.6). Strengths are onset strengths per band, normalised to the song\'s 99.5th percentile, max within ±30 ms of the tap. '
         'Removing a tap removes a turn, so the route was repaired by `tools/charts/integb_route.py`, which keeps the worker\'s own turn sequence phrase by phrase wherever it stays legal; worldPos landmarks were moved with the road.', '',
         '### What the taps follow (per section)', '', '| section | time | taps follow | taps before → after | /s after | median strength of followed band | removed (faint / off-layer / weak burst) |', '|---|---|---|---|---|---|---|']
    for k, s in enumerate(secs):
        e = secs[k + 1]['t'] if k + 1 < len(secs) else 1e9
        a = [t for t in T0 if s['t'] <= t < e]; b = [t for t in T1 if s['t'] <= t < e]
        rm = [r for r in au['removed'] if s['t'] <= r['t'] < e]
        c = {w: sum(1 for r in rm if r['why'] == w) for w in ('faint', 'off-layer', 'weak-burst')}
        med = stt.median(env.s(t, s['follows']) for t in b) if b else 0
        dur = (min(e, T1[-1] + 3) - s['t'])
        L.append(f"| {s['label']} | {s['t']:.2f} | {NAME.get(s['follows'], s['follows'])} | {len(a)} → {len(b)} | {len(b)/max(dur,1e-6):.2f} | {med:.2f} | {c['faint']} / {c['off-layer']} / {c['weak-burst']} |")
    L += ['', '### Audit diff (removed taps)', '', '| t (s) | tag | reason | followed band | band strength | full-mix strength |', '|---|---|---|---|---|---|']
    for r in au['removed']: L.append(f"| {r['t']:.3f} | {r.get('tag') or ''} | {r['why']} | {r['layer']} | {r['layer_strength']:.2f} | {r['full_strength']:.2f} |")
    L += ['', 'Added taps: none.', '', f"Original (pre-audit) chart and layout: `levels-design/{sid}/pre-audit/`. Integrated copy: `levels-src/{sid}/`. chartlogic report after the audit: `docs/verification/{sid}-chartlogic.md`.", '']
    p = d / 'chart-report.md'; txt = p.read_text() if p.exists() else f'# {sid}: chart report\n'
    if MARK in txt: txt = txt[:txt.index(MARK)].rstrip() + '\n'
    p.write_text(txt.rstrip() + '\n\n' + '\n'.join(L)); print(p)
