#!/usr/bin/env python3
"""integ-a: ship a worker design (levels-design/<slug>/) into levels-src/<slug>/ unchanged.
Rhythm AND route are the designer's (taps, dirs, elevation, scenery); nothing is re-searched because the worker
designs already pass validate.py v2.5 with 0 errors and their route sections are what design.md describes.
Art: levels-design/<slug>/art already carries the art-codex overlay (rebuild f80704c), copied as-is.
Optional per-song data patches live in PATCHES below (each one documented in docs/verification/integ-a-<slug>.md).
Usage: integ_a.py <slug> [...]"""
import json, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def cutaway(chart, layout):
    """Tall worldPos landmarks (towers, relief walls, arcade roofs, CD disc) were marked `onroad`, which the engine
    excludes from the screen-space occluder cutaway (world.ts fadeOccluders), so e.g. Cookie's 19 u stair tower hid the
    head and the road ahead (deliverables/cookie/snap/t043.png before the patch). `onroad` only also disables push-out,
    which worldPos objects skip anyway, so dropping it on groups taller than 5 u only lets them fade when they occlude.
    Flat decks (pitch, pool, court, terrace), piers and fake forks keep `onroad`."""
    for o in layout.get('objects', []):
        if not o.get('onroad') or o.get('kind') != 'group' or not o.get('worldPos'): continue
        h = max([p.get('pos', [0, 0, 0])[1] + p.get('size', [0, 0, 0])[1] for p in o.get('parts', [])] or [0])
        if h > 5: o.pop('onroad'); o['integNote'] = 'onroad dropped by integ-a so the occluder cutaway can fade it'
PATCHES = {'attention': cutaway, 'hype-boy': cutaway, 'cookie': cutaway, 'hurt': cutaway}
for slug in sys.argv[1:]:
    src = ROOT / f'levels-design/{slug}'; dst = ROOT / f'levels-src/{slug}'
    dst.mkdir(parents=True, exist_ok=True)
    chart = json.loads((src / 'chart.json').read_text()); layout = json.loads((src / 'layout.json').read_text())
    chart.setdefault('meta', {})['source'] = f'levels-design/{slug} (worker design, integrated by integ-a)'
    if slug in PATCHES: PATCHES[slug](chart, layout)
    (dst / 'chart.json').write_text(json.dumps(chart, indent=1, ensure_ascii=False))
    (dst / 'layout.json').write_text(json.dumps(layout, indent=1, ensure_ascii=False))
    if (dst / 'art').exists(): shutil.rmtree(dst / 'art')
    if (src / 'art').exists(): shutil.copytree(src / 'art', dst / 'art')
    print(f'{slug}: {len(chart["taps"])} taps, {len(layout.get("objects", []))} objects -> {dst.relative_to(ROOT)}')
subprocess.run([sys.executable, str(ROOT / 'tools/charts/follows_from_reports.py'), *sys.argv[1:]], check=True)   # section 'follows' layers from the worker chart-reports
