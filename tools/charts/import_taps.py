#!/usr/bin/env python3
"""Import a tapper export (tapper/ page, format 'nj-tapper') into a playable chart.

  python3 tools/charts/import_taps.py <export.json> --song omg [--out DIR] [--dry-run] [--report r.json]
        [--grid export|chart] [--calib MS] [--fit-offset] [--allow-16] [--no-route] [--no-validate] [--keep-diamonds]

Pipeline (each step is reported, nothing is changed silently):
 1. calibration   t = t_raw - calibration_ms/1000 (taps edited on the timeline already carry a corrected t)
 2. offset check  median residual to the 1/8 grid is reported; --fit-offset subtracts it
 3. duplicates    taps closer than 60 ms are merged (mean time)
 4. snap          1/8 grid by default; 1/16 only inside clear fast runs (>= 3 taps with gaps <= 0.75 x 1/8);
                  taps more than 60 ms from their grid point are listed as QUESTIONABLE (still snapped)
 5. collisions    taps that land on the same grid slot are merged
 6. playability   min gap 0.105 s (later tap removed), first tap >= 1 s, last <= duration - 1 s,
                  no tap within 0.35 s after a fall/jump (validate.py MIN_AIR_GAP; tap removed)
 7. consistency   repeated sections (same `kind`) are compared on the 1/16 grid; differences are REPORTED only
 8. write         levels-src/<song>/chart.json (other chart fields kept; type -> tag; lyric/syl kept when a previous
                  tap is within 30 ms), route via tools/research/route_forward.py (forward-only), 10 diamonds re-placed
                  in the largest tap gap of each tenth of the song, then levels-design/validate.py must report 0 errors.
--out DIR writes <DIR>/<song>/ (chart+layout copied from levels-src, art symlinked) so tests never touch the real chart."""
import json, sys, os, shutil, subprocess, statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DUP, Q_MS, MIN_GAP, MIN_AIR_GAP, MATCH = 0.060, 60.0, 0.105, 0.35, 0.030

def opt(k, d=None):
    if k in sys.argv:
        i = sys.argv.index(k)
        if i + 1 < len(sys.argv): return sys.argv[i + 1]
    return d
flag = lambda k: k in sys.argv
pos = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and sys.argv[i - 1] not in
       ('--song', '--out', '--report', '--grid', '--calib')]
if not pos: print(__doc__); sys.exit(2)
exp = json.loads(Path(pos[0]).read_text())
if exp.get('format') != 'nj-tapper': sys.exit('not a tapper export (format != nj-tapper)')
song = opt('--song', exp.get('song'))
if not song: sys.exit('--song is required')
if exp.get('song') and exp['song'] != song: print(f'warn: export is for "{exp["song"]}", importing as "{song}"')
SRC = ROOT / 'levels-src' / song
OUTROOT = Path(opt('--out', str(ROOT / 'levels-src'))); OUT = OUTROOT / song
DRY = flag('--dry-run')

old = json.loads((SRC / 'chart.json').read_text()) if (SRC / 'chart.json').exists() else None
an = ROOT / f'analysis/{song}.json'
dur = exp.get('audio_duration') or (json.loads(an.read_text())['duration'] if an.exists() else None)
if not dur: sys.exit('audio duration unknown')

# ---- grid
meta = (old or {}).get('meta', {})
cg = (meta.get('rechart') or {}).get('grid') or {}
if opt('--grid', 'export') == 'chart' and (cg or meta.get('bpm')):
    bpm = cg.get('bpm', meta.get('bpm')); B0 = cg.get('beat0', meta.get('beat0', 0.0)); P = 60.0 / bpm; gsrc = 'chart meta'
else:
    P = exp.get('beat_period') or 60.0 / exp['bpm']; B0 = exp.get('beat0', 0.0); bpm = 60.0 / P; gsrc = 'export (' + str(exp.get('grid_source', '?')) + ')'
E8, E16 = P / 2, P / 4
snapto = lambda t, s: B0 + round((t - B0) / s) * s
print(f'== import_taps {song}: {len(exp["taps"])} raw taps, grid {bpm:.3f} BPM beat0 {B0:.3f} s from {gsrc}; audio {dur:.2f} s')

rep = {'song': song, 'raw': len(exp['taps']), 'grid': {'bpm': round(bpm, 4), 'beat0': B0, 'source': gsrc}, 'removed': [], 'questionable': [], 'merged': [], 'consistency': []}
# ---- 1 calibration
cal = float(opt('--calib', exp.get('calibration_ms', 0) or 0))
taps = []
for tp in exp['taps']:
    if tp.get('edited') and opt('--calib') is None: t = float(tp['t'])
    else: t = float(tp['t_raw']) - cal / 1000.0
    taps.append({'t': t, 'type': tp.get('type', 'tap'), 'raw': float(tp.get('t_raw', t))})
taps.sort(key=lambda x: x['t'])
print(f'1 calibration {cal:.0f} ms applied ({sum(1 for t in exp["taps"] if t.get("edited"))} timeline-edited taps keep their t)')
rep['calibration_ms'] = cal

# ---- 2 residual offset
res = [(t['t'] - snapto(t['t'], E8)) * 1000 for t in taps]
near = [r for r in res if abs(r) < 50]
off = st.median(near) if near else 0.0
print(f'2 median residual to the 1/8 grid {off:+.1f} ms (over {len(near)} near-grid taps)' + ('  -> subtracted (--fit-offset)' if flag('--fit-offset') else ('  (consider --fit-offset)' if abs(off) > 10 else '')))
if flag('--fit-offset'):
    for t in taps: t['t'] -= off / 1000.0
rep['residual_offset_ms'] = round(off, 1); rep['offset_fitted'] = flag('--fit-offset')

# ---- 3 duplicates
def merge_close(lst, thr, why):
    out = []
    for t in lst:
        if out and t['t'] - out[-1]['t'] < thr:
            a = out[-1]; rep['merged'].append({'t': round(a['t'], 3), 'with': round(t['t'], 3), 'why': why})
            n = a.get('n', 1); a['t'] = (a['t'] * n + t['t']) / (n + 1); a['n'] = n + 1
        else: out.append(dict(t))
    return out
n0 = len(taps); taps = merge_close(taps, DUP, 'duplicate < 60 ms')
print(f'3 duplicates merged: {n0 - len(taps)}')

# ---- 4 snap (1/16 only in fast runs)
fast = [False] * len(taps); i = 0
while i < len(taps):
    j = i
    while j + 1 < len(taps) and taps[j + 1]['t'] - taps[j]['t'] <= 0.75 * E8: j += 1
    if j - i + 1 >= 3:
        for k in range(i, j + 1): fast[k] = True
    i = j + 1
for t, f in zip(taps, fast):
    t['pre'] = t['t']; t['res'] = '1/16' if f else '1/8'; t['t'] = snapto(t['t'], E16 if f else E8)
    d = (t['pre'] - t['t']) * 1000
    if abs(d) > Q_MS: rep['questionable'].append({'t': round(t['pre'], 3), 'snapped': round(t['t'], 3), 'off_ms': round(d, 1), 'type': t['type']})
# isolated taps that sit right on a 1/16 off-beat: kept on 1/8 per the rule, but listed (or kept on 1/16 with --allow-16)
rep['sixteenth_hint'] = []
for t, f in zip(taps, fast):
    if f: continue
    s16 = snapto(t['pre'], E16)
    if abs(s16 - t['t']) > 1e-6 and abs(t['pre'] - s16) * 1000 < 20:
        rep['sixteenth_hint'].append({'t': round(t['pre'], 3), 'on16': round(s16, 3), 'snapped8': round(t['t'], 3)})
        if flag('--allow-16'): t['t'] = s16; t['res'] = '1/16'
moved = [abs(t['pre'] - t['t']) * 1000 for t in taps]
print(f'4 snapped {len(taps)} taps: {sum(fast)} on 1/16 (fast runs), {len(taps) - sum(fast)} on 1/8; mean move {st.mean(moved) if moved else 0:.1f} ms, max {max(moved) if moved else 0:.1f} ms; questionable (> {Q_MS:.0f} ms): {len(rep["questionable"])}')
if rep['sixteenth_hint']: print(f'   {len(rep["sixteenth_hint"])} isolated taps sit within 20 ms of a 1/16 off-beat: ' + ('kept on 1/16 (--allow-16)' if flag('--allow-16') else 'snapped to 1/8 per the rule; listen to them or pass --allow-16') + ', e.g. ' + ', '.join(str(h['t']) for h in rep['sixteenth_hint'][:6]))
for q in rep['questionable'][:20]: print(f'   QUESTIONABLE {q["t"]:8.3f}s -> {q["snapped"]:8.3f}s ({q["off_ms"]:+.0f} ms, {q["type"]})')

# ---- 5 collisions
out = []
for t in taps:
    if out and abs(t['t'] - out[-1]['t']) < 1e-6:
        rep['merged'].append({'t': round(t['t'], 3), 'with': round(t['pre'], 3), 'why': 'same grid slot'}); continue
    out.append(t)
print(f'5 same-slot collisions merged: {len(taps) - len(out)}'); taps = out

# ---- 6 playability
layout = json.loads((SRC / 'layout.json').read_text()) if (SRC / 'layout.json').exists() else {}
def drop(t, why): rep['removed'].append({'t': round(t['t'], 3), 'why': why})
keep = []
for t in taps:
    if t['t'] < 1.0: drop(t, 'before 1.0 s'); continue
    if t['t'] > dur - 1.0: drop(t, 'after duration-1'); continue
    if keep and t['t'] - keep[-1]['t'] < MIN_GAP - 1e-9: drop(t, f'gap {t["t"] - keep[-1]["t"]:.3f} < {MIN_GAP}'); continue
    keep.append(t)
taps = keep
for e in layout.get('elevation', []):
    if e.get('type') not in ('fall', 'jump'): continue
    bad = [t for t in taps if e['t'] + 1e-6 < t['t'] < e['t'] + MIN_AIR_GAP]
    for t in bad: drop(t, f'{e["type"]} at {e["t"]}: tap {t["t"] - e["t"]:.3f}s after (need >= {MIN_AIR_GAP})')
    taps = [t for t in taps if t not in bad]
print(f'6 playability removals: {len(rep["removed"])}')
for r in rep['removed'][:20]: print(f'   REMOVED {r["t"]:8.3f}s  {r["why"]}')

# ---- 7 consistency between repeated sections (report only)
secs = sorted((old or {}).get('sections', []), key=lambda s: s['t'])
bounds = [(s, secs[k + 1]['t'] if k + 1 < len(secs) else dur) for k, s in enumerate(secs)]
def pattern(a, b): return {round((t['t'] - a) / E16) for t in taps if a - 1e-6 <= t['t'] < b - 1e-6}
bykind = {}
for s, e in bounds: bykind.setdefault(s.get('kind', '?'), []).append((s, e))
for kind, lst in bykind.items():
    for (s1, e1), (s2, e2) in zip(lst, lst[1:]):
        L = min(e1 - s1['t'], e2 - s2['t']); p1, p2 = pattern(s1['t'], s1['t'] + L), pattern(s2['t'], s2['t'] + L)
        if not p1 and not p2: continue
        only1, only2 = sorted(p1 - p2), sorted(p2 - p1); sim = len(p1 & p2) / max(1, len(p1 | p2))
        item = {'kind': kind, 'a': s1.get('label', s1['t']), 'b': s2.get('label', s2['t']), 'similarity': round(sim, 2),
                'only_in_a': [round(s1['t'] + k * E16, 3) for k in only1][:12], 'only_in_b': [round(s2['t'] + k * E16, 3) for k in only2][:12]}
        rep['consistency'].append(item)
print(f'7 consistency (report only, nothing changed): {len(rep["consistency"])} repeated-section pairs compared')
for c in rep['consistency']:
    if c['similarity'] < 0.999:
        print(f'   {c["kind"]:7s} {str(c["a"])[:22]:22s} vs {str(c["b"])[:22]:22s} similarity {c["similarity"]:.2f}  only-A {len(c["only_in_a"])} only-B {len(c["only_in_b"])}  e.g. A {c["only_in_a"][:3]} B {c["only_in_b"][:3]}')

# ---- change report vs raw and vs the previous chart
final = [round(t['t'], 3) for t in taps]
rep['final'] = len(final)
print(f'== change report vs raw: {rep["raw"]} raw -> {len(final)} taps; merged {len(rep["merged"])}, removed {len(rep["removed"])}, moved by snapping {sum(1 for m in moved if m > 1)} (added 0: the converter never invents taps)')
if old:
    ot = [x['t'] for x in old['taps']]; used = set(); kept = mv = 0
    for t in final:
        j = min(range(len(ot)), key=lambda k: abs(ot[k] - t)) if ot else None
        if j is not None and j not in used and abs(ot[j] - t) <= MATCH:
            used.add(j); kept += abs(ot[j] - t) <= 0.001; mv += abs(ot[j] - t) > 0.001
    added = len(final) - kept - mv; removed = len(ot) - len(used)
    rep['vs_previous'] = {'previous': len(ot), 'same': kept, 'moved_le_30ms': mv, 'added': added, 'removed': removed}
    print(f'== change report vs previous chart ({len(ot)} taps): same {kept}, moved <= 30 ms {mv}, added {added}, removed {removed}')

if flag('--report'): pass
if opt('--report'): Path(opt('--report')).write_text(json.dumps(rep, indent=1, ensure_ascii=False))
if DRY: print('dry run: nothing written'); sys.exit(0)

# ---- 8 write chart, route, diamonds, validate
OUT.mkdir(parents=True, exist_ok=True)
if OUT.resolve() != SRC.resolve():
    if (SRC / 'layout.json').exists(): shutil.copy(SRC / 'layout.json', OUT / 'layout.json')
    if (SRC / 'art').exists() and not (OUT / 'art').exists(): os.symlink(SRC / 'art', OUT / 'art')
oldby = sorted((old or {}).get('taps', []), key=lambda x: x['t'])
TAG = {'drum': 'drum', 'vocal': 'vocals'}
newtaps = []
for t in taps:
    o = min(oldby, key=lambda x: abs(x['t'] - t['t'])) if oldby else None
    tp = {'t': round(t['t'], 3), 'tag': TAG.get(t['type']) or (o.get('tag') if o and abs(o['t'] - t['t']) <= MATCH else 'tap')}
    if o and abs(o['t'] - t['t']) <= MATCH:
        for k in ('lyric', 'syl'):
            if k in o: tp[k] = o[k]
    newtaps.append(tp)
ch = dict(old) if old else {'id': song, 'startHeading': 'N', 'speed': [{'t': 0, 'v': 10.0}], 'sections': [], 'meta': {}}
ch['taps'] = newtaps; ch.setdefault('meta', {})
ch['meta']['taps_import'] = {'tool': 'tools/charts/import_taps.py', 'export_tool': exp.get('tool'), 'exported': exp.get('exported'),
    'calibration_ms': cal, 'residual_offset_ms': rep['residual_offset_ms'], 'offset_fitted': rep['offset_fitted'], 'grid': rep['grid'],
    'raw': rep['raw'], 'final': len(newtaps), 'questionable': len(rep['questionable']), 'removed': len(rep['removed'])}
(OUT / 'chart.json').write_text(json.dumps(ch, indent=1, ensure_ascii=False))
print(f'8 wrote {OUT / "chart.json"} ({len(newtaps)} taps)')
if not flag('--no-route'):
    r = subprocess.run([sys.executable, str(ROOT / 'tools/research/route_forward.py'), '--song', song, '--dir', str(OUTROOT)], capture_output=True, text=True)
    print('   route_forward:', (r.stdout + r.stderr).strip())
    if r.returncode: sys.exit('route_forward failed')
if layout and not flag('--keep-diamonds'):
    lay = json.loads((OUT / 'layout.json').read_text()); T = [tp['t'] for tp in newtaps]
    a0, a1 = T[0], T[-1]; dms = []
    for k in range(10):
        lo, hi = a0 + (a1 - a0) * k / 10, a0 + (a1 - a0) * (k + 1) / 10
        best = max(((b - a, (a + b) / 2) for a, b in zip(T, T[1:]) if lo <= (a + b) / 2 < hi), default=None)
        dms.append({'t': round(best[1] if best else (lo + hi) / 2, 3), 'side': 0, 'moved': 'import_taps: largest tap gap in tenth %d' % (k + 1)})
    lay['diamonds'] = dms; (OUT / 'layout.json').write_text(json.dumps(lay, indent=1, ensure_ascii=False))
    print('   diamonds at', [d['t'] for d in dms])
if not flag('--no-validate'):
    args = [sys.executable, str(ROOT / 'levels-design/validate.py'), song, '--dir', str(OUTROOT), '--repo', str(ROOT)]
    if OUT.resolve() != SRC.resolve(): args.append('--no-preview')
    r = subprocess.run(args, capture_output=True, text=True); print(r.stdout.rstrip())
    nerr = r.stdout.count('ERROR'); print(f'== validate: {nerr} errors')
    if opt('--report'):
        rep['validate_errors'] = nerr; Path(opt('--report')).write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    if nerr: sys.exit(1)
if OUT.resolve() == SRC.resolve(): print('next: regenerate scenery for the new route (tools/art/omg_scene.py for OMG) and re-run the game tests')
