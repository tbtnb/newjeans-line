import sys, json, importlib, time
sys.path.insert(0, '/workspace/nj-w1-work/v3')
from chore import *; from util import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
slug = sys.argv[1]; Pm = importlib.import_module('plan_' + slug.replace('-', '_'))
chart, T = taps(slug); dur = Pm.dur
t0 = time.time()
pl = Planner(T, dur, Pm.speed, Pm.widths, Pm.elev(T), Pm.moves(), start=Pm.start, max_tries=Pm.__dict__.get("max_tries", 400000))
try:
    dirs, nodes, elev, choice = pl.solve()
except RuntimeError as e:
    print('FAIL', e, 'tries', pl.tries)
    nodes, elev, v = pl.fail_nodes; print('variant', v)
    fig, ax = plt.subplots(figsize=(12, 12))
    for a, b in zip(nodes, nodes[1:]):
        c = 'r' if a[0] > 60 else 'b'
        ax.plot([a[1], b[1]], [a[2], b[2]], color=c, lw=1 + 0.3 * max(0, elev_at(elev, a[0]) + 4))
        if a[0] > 70: ax.annotate(f'{a[0]:.1f}', (a[1], a[2]), fontsize=6)
    ax.set_aspect('equal'); fig.savefig(f'{slug}.fail.png', dpi=60); sys.exit(1)
print('solved in', round(time.time() - t0, 1), 's tries', pl.tries)
for m in pl.moves: print(f"  {m['name']:16s} {m['kind']:7s} {m['t0']:7.2f} taps {m['_i1']-m['_i0']:3d} -> {choice[m['name']]}")
print('elev', [{k: v for k, v in e.items()} for e in elev])
json.dump({'dirs': dirs, 'nodes': nodes, 'elev': elev, 'choice': choice}, open(f'{slug}.route.json', 'w'))
fig, ax = plt.subplots(figsize=(12, 12)); cols = plt.cm.tab20.colors
secs = chart['sections']
for a, b in zip(nodes, nodes[1:]):
    k = [i for i, x in enumerate(secs) if x['t'] <= a[0] + 1e-6][-1]
    y = elev_at(elev, (a[0] + b[0]) / 2)
    ax.plot([a[1], b[1]], [a[2], b[2]], color=cols[(2 * k) % 20], lw=1.2 + 0.4 * max(0, y + 4), solid_capstyle='butt', zorder=2 + y)
for k, x in enumerate(secs):
    for a, b in zip(nodes, nodes[1:]):
        if a[0] <= x['t'] <= b[0]:
            ax.annotate(f"{x['label']}", (a[1], a[2]), fontsize=9, color='k'); break
ax.plot(0, 0, 'go', ms=8); ax.set_aspect('equal'); ax.grid(alpha=.3)
fig.savefig(f'{slug}.try.png', dpi=60); plt.close(fig)
