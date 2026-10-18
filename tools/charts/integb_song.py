"""Integrator-B pipeline for one worker design (mirrors the Ditto integration: worker chart -> rhythm-logic audit ->
geometry regenerated where taps were removed -> levels-src/<slug>/). Used by tools/charts/<slug>.py.
Writes: levels-src/<slug>/{chart,layout}.json (+ art/), and when `audit=True` also the revised design back to
levels-design/<slug>/{chart,layout}.json with the original kept as levels-design/<slug>/pre-audit/."""
import json, shutil, subprocess
from pathlib import Path
from common import ROOT
from integb_audit import audit as run_audit, Env, sec_of
from integb_route import Repair, phrases_for, remap_worldpos

def duration(sid):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(ROOT / f'public/audio/{sid}.mp3')], capture_output=True, text=True).stdout)

def run(sid, audit=False, pins=None, keep=(), follows=None, notes='', meta=None, beat_grid=None, retime=None):
    dd = ROOT / f'levels-design/{sid}'
    src_chart = dd / ('pre-audit/chart.json' if (dd / 'pre-audit/chart.json').exists() else 'chart.json')
    src_layout = dd / ('pre-audit/layout.json' if (dd / 'pre-audit/layout.json').exists() else 'layout.json')
    chart = json.loads(src_chart.read_text()); layout = json.loads(src_layout.read_text())
    dur = duration(sid); log = []
    secs = sorted(chart['sections'], key=lambda s: s['t']); chart['sections'] = secs
    # fill explicit dirs so the worker's turn sequence is known per tap
    last = 'L'
    for tp in chart['taps']:
        tp.setdefault('dir', 'R' if last == 'L' else 'L'); last = tp['dir']
    orig = json.loads(json.dumps(chart))
    removed = []; layers = {}
    if audit:
        kept, removed, layers = run_audit(sid, chart, pins or {}, keep)
        # re-time: a flagged tap whose intended hit is one 16th away (a clear onset of the SAME section layer) is moved there
        for o, n in (retime or {}).items():
            src = next(x for x in orig['taps'] if abs(x['t'] - o) < 1e-3)
            kept.append({**src, 't': n, 'retimed_from': o}); kept.sort(key=lambda x: x['t'])
            removed = [r if abs(r[0] - o) > 1e-3 else (r[0], r[1] + f' -> re-timed to {n:.3f}', *r[2:]) for r in removed]
        if removed:
            taps = [x['t'] for x in kept]; odirs = [x['dir'] for x in kept]
            rep = Repair(chart, layout, dur)
            best = None
            for seed in range(1, 5):
                try: dirs, st = rep.search(taps, odirs, phrases_for(taps, secs), beam=40, seed=seed)
                except RuntimeError as e: log.append(f'seed {seed}: {e}'); continue
                sc = st['keep'] * 3 + st['flip'] * 1.5 + st['crossings'] * 0.01
                if best is None or sc > best[0]: best = (sc, dirs, st, seed)
            if best is None: raise RuntimeError('route repair failed: ' + '; '.join(log))
            _, dirs, st, seed = best
            for x, d in zip(kept, dirs): x['dir'] = d
            log.append(f"route repair seed {seed}: {len(st['patterns'])} phrases, kept worker turn sequence in {st['keep']}, mirrored in {st['flip']}, re-patterned {len(st['patterns'])-st['keep']-st['flip']} ({', '.join(p for p in st['patterns'] if p not in ('keep','flip'))}); search crossings {st['crossings']}")
        chart['taps'] = kept
    else:
        env = Env(sid); from integb_audit import choose_layers
        layers = choose_layers(env, chart['taps'], secs, pins or {})
    for k, s in enumerate(secs):
        if follows and k in follows: s['follows'] = follows[k]
        elif audit or 'follows' not in s: s['follows'] = layers.get(k, 'full')
    if audit:
        chart.setdefault('meta', {})['audit'] = {'by': 'integrator B (integ-b)', 'rule': 'one audible layer per section; no faint/off-layer taps; bursts only where clear in the full mix; taps only removed',
                                                 'taps_before': len(orig['taps']), 'taps_after': len(chart['taps']), 'retimed': len(retime or {}), 'removed': [{'t': r[0], 'why': r[1], 'layer': r[2], 'layer_strength': r[3], 'full_strength': r[4], 'tag': r[5]} for r in removed]}
        if removed:
            n = remap_worldpos(layout, orig, chart, dur, log)
            from integb_clearance import hits, nudge
            pre_layout = json.loads(src_layout.read_text())
            allowed = {x[0] for x in hits(orig, pre_layout, dur)}   # touches the worker already had (arches, gates) stay
            nudge(chart, layout, dur, allowed, log)
    # schema: event `target` is ONE id string (or 'prefix*'); worker arrays crash the engine (targets(): id.endsWith)
    ids = [o.get('id') for o in layout.get('objects', []) if o.get('id')]
    evs = []
    for e in layout.get('events', []):
        tg = e.get('target')
        if isinstance(tg, list):
            import os
            pre = os.path.commonprefix(tg)
            if pre and set(i for i in ids if i.startswith(pre)) == set(tg): evs.append({**e, 'target': pre + '*'}); log.append(f"event {e['type']}@{e['t']}: target list -> '{pre}*'")
            else:
                for k, one in enumerate(tg): evs.append({**e, 'target': one, 't': round(e['t'] + k * e.get('every', 0), 3), **({'every': 0} if 'every' in e else {})})
                log.append(f"event {e['type']}@{e['t']}: target list split into {len(tg)} events")
        else: evs.append(e)
    layout['events'] = sorted(evs, key=lambda e: e['t'])
    if meta: chart.setdefault('meta', {}).update(meta)
    from integb_dressing import DRESSING
    if sid in DRESSING: layout['dressing'] = DRESSING[sid]
    if beat_grid:   # (period, beat0): the music grid for beat/kick-reactive scenery when analysis/<slug>.grid.json is off
        P, b0 = beat_grid; layout['beats'] = [round(b0 + k * P, 3) for k in range(int((dur - b0) / P) + 1) if b0 + k * P >= 0]
    if notes: chart['notes'] = (chart.get('notes', '') + ' | ' + notes).strip(' |')
    out = ROOT / f'levels-src/{sid}'; out.mkdir(parents=True, exist_ok=True)
    (out / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
    (out / 'layout.json').write_text(json.dumps(layout, indent=1, ensure_ascii=False))
    if (out / 'art').exists(): shutil.rmtree(out / 'art')
    if (dd / 'art').exists(): shutil.copytree(dd / 'art', out / 'art')
    if audit:
        pa = dd / 'pre-audit'; pa.mkdir(exist_ok=True)
        if not (pa / 'chart.json').exists(): shutil.copy(dd / 'chart.json', pa / 'chart.json'); shutil.copy(dd / 'layout.json', pa / 'layout.json')
        (dd / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
        (dd / 'layout.json').write_text(json.dumps(layout, indent=1, ensure_ascii=False))
    print(f'{sid}: {len(orig["taps"])} -> {len(chart["taps"])} taps; removed {len(removed)}')
    for l in log: print('  ', l)
    return orig, chart, removed, layers
