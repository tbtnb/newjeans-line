#!/usr/bin/env python3
"""integ-a: pick the flip weight for integ_a.py's local route repair per song. Score = relative distance of validate.py's
multi-level crossing count from the designer's + share of flipped turns (fidelity to the designer's route). Usage: integ_a_tune.py <slug> [...]"""
import os, re, subprocess, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def vcross(slug, d):
    out = subprocess.run([sys.executable, str(ROOT / 'levels-design/validate.py'), slug, '--dir', d], capture_output=True, text=True, cwd=ROOT).stdout
    return int(re.search(r'multi-level crossings (\d+)', out).group(1)), out.count('ERROR')
for slug in sys.argv[1:]:
    c0, _ = vcross(slug, 'levels-design'); res = []
    for w in (2, 3, 5, 8, 12, 20, 40):
        out = subprocess.run([sys.executable, str(ROOT / 'tools/charts/integ_a.py'), slug], env={**os.environ, 'FLIPW': str(w)}, capture_output=True, text=True, cwd=ROOT).stdout
        fl = int(re.search(r'dir flips (\d+)', out).group(1)); n = int(re.search(r'-> (\d+) taps', out).group(1))
        c, err = vcross(slug, 'levels-src')
        sc = abs(c - c0) / max(c0, 1) + fl / n + (99 if err else 0)
        res.append((sc, w, c, fl, err)); print(f'{slug} FLIPW={w}: crossings {c} (designer {c0}), flips {fl}/{n}, errors {err}, score {sc:.3f}', flush=True)
    best = min(res); print(f'{slug}: chosen FLIPW={best[1]}')
    subprocess.run([sys.executable, str(ROOT / 'tools/charts/integ_a.py'), slug], env={**os.environ, 'FLIPW': str(best[1])}, check=True, cwd=ROOT)
    p = ROOT / f'levels-src/{slug}/chart.json'; ch = json.loads(p.read_text())
    ch['meta']['integration']['flip_weight'] = best[1]; ch['meta']['integration']['crossings'] = {'designer': c0, 'shipped': best[2]}
    p.write_text(json.dumps(ch, indent=1, ensure_ascii=False))
