"""Top-down route plot: worker geometry (pre-audit) vs integrated, with worldPos landmarks. Usage: integb_plot.py <slug> <out.png>"""
import json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, __import__('os').path.dirname(__file__))
from common import ROOT
from integb_route import centreline
from integb_song import duration
sid, out = sys.argv[1], sys.argv[2]; dur = duration(sid); d = ROOT / f'levels-design/{sid}'
pre = d / 'pre-audit' if (d / 'pre-audit').exists() else d
fig, axs = plt.subplots(1, 2, figsize=(16, 8))
for ax, (lab, base) in zip(axs, [('worker design (pre-audit)', pre), ('integrated (levels-src)', ROOT / f'levels-src/{sid}')]):
    c = json.load(open(base / 'chart.json')); l = json.load(open(base / 'layout.json'))
    last = 'L'
    for tp in c['taps']: tp.setdefault('dir', 'R' if last == 'L' else 'L'); last = tp['dir']
    n = centreline(c, dur); secs = sorted(c['sections'], key=lambda s: s['t'])
    cols = plt.cm.tab20.colors
    for a, b in zip(n, n[1:]):
        k = max(i for i, s in enumerate(secs) if s['t'] <= a[0] + 1e-6) if secs and secs[0]['t'] <= a[0] + 1e-6 else 0
        ax.plot([a[1], b[1]], [a[2], b[2]], color=cols[k % 20], lw=1.4)
    for o in l['objects']:
        if 'worldPos' in o and (o.get('landmark') or o.get('egg')):
            ax.plot(o['worldPos'][0], o['worldPos'][2], 'k*' if o.get('landmark') else 'm^', ms=9); ax.annotate(o.get('id'), (o['worldPos'][0], o['worldPos'][2]), fontsize=7)
    ax.set_aspect('equal'); ax.set_title(f'{sid}: {lab}, {len(c["taps"])} taps'); ax.invert_xaxis() if False else None
plt.tight_layout(); plt.savefig(out, dpi=90); print(out)
