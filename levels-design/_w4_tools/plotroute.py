import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib import cm, colors
from route import elev_at, world_of, HEAD, ORDER
def plot_route(path, nodes, elev, W, secs, title, objs=(), dia=(), crowns=(), blocks=None):
    fig, ax = plt.subplots(figsize=(13, 13))
    ys = [elev_at(elev, n[0]) for n in nodes]; lo, hi = min(ys), max(ys) if max(ys) > min(ys) else min(ys) + 1
    norm = colors.Normalize(lo, hi); cmap = cm.plasma
    st = [s['t'] for s in secs]
    segs = list(zip(nodes, nodes[1:]))
    order = sorted(range(len(segs)), key=lambda i: elev_at(elev, (segs[i][0][0] + segs[i][1][0]) / 2))
    for i in order:
        a, b = segs[i]; y = elev_at(elev, (a[0] + b[0]) / 2)
        hx, hz = HEAD[ORDER[a[3]]]; px, pz = -hz * W / 2, hx * W / 2
        x0, z0, x1, z1 = a[1] - hx * W / 2, a[2] - hz * W / 2, b[1] + hx * W / 2, b[2] + hz * W / 2
        ax.add_patch(Polygon([(x0 + px, z0 + pz), (x1 + px, z1 + pz), (x1 - px, z1 - pz), (x0 - px, z0 - pz)], closed=True,
                             fc=cmap(norm(y)), ec='k', lw=0.25, zorder=2 + y * 0.01))
    for i, s in enumerate(secs):
        x, z = world_of(nodes, s['t'] + 0.01)
        ax.annotate(f"{s['label']} {s['t']:.0f}s", (x, z), fontsize=9, weight='bold', color='#203040', zorder=50,
                    bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.7, lw=0))
    if blocks:
        for i, b in enumerate(blocks):
            x, z = world_of(nodes, b['t0'] + 0.01); ax.plot(x, z, 'o', ms=4, color='k', zorder=40)
            ax.annotate(b['tex'], (x, z), fontsize=7, xytext=(3, -9), textcoords='offset points', color='#555', zorder=45)
    for o in objs:
        if 'debugXZ' in o:
            x, z = o['debugXZ']; m = '*' if o.get('landmark') else ('X' if o.get('egg') else 's')
            ax.plot(x, z, m, color='r' if o.get('egg') else ('#111' if o.get('landmark') else '#7a7a7a'), ms=15 if o.get('landmark') else 5, zorder=30)
            if o.get('landmark') or o.get('egg'): ax.annotate(o.get('id', ''), (x, z), fontsize=7, xytext=(5, 5), textcoords='offset points', zorder=46)
    for d in dia:
        x, z = world_of(nodes, d['t']); ax.plot(x, z, 'D', color='deepskyblue', mec='k', ms=7, zorder=48)
    for c in crowns:
        x, z = world_of(nodes, c['t']); ax.plot(x, z, '^', color='gold', ms=13, mec='k', zorder=49)
    for e in elev:
        t = e.get('t', e.get('t0')); x, z = world_of(nodes, t)
        ax.annotate(f"{e['type']} {e['dy']:+g}", (x, z), fontsize=8, color='purple', xytext=(-10, 8), textcoords='offset points', zorder=47)
    ax.autoscale_view(); ax.set_aspect('equal'); ax.grid(alpha=0.2)
    sm = cm.ScalarMappable(norm=norm, cmap=cmap); fig.colorbar(sm, ax=ax, shrink=0.5, label='road height')
    ax.set_title(title); fig.savefig(path, dpi=75, bbox_inches='tight'); plt.close(fig)
def plot_sections(path, nodes, elev, W, secs, title, dur):
    import math
    n = len(secs); cols = 4; rows = math.ceil(n / cols)
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 4.2, rows * 4.2))
    ys = [elev_at(elev, nd[0]) for nd in nodes]; norm = colors.Normalize(min(ys), max(ys) if max(ys) > min(ys) else min(ys) + 1)
    segs = list(zip(nodes, nodes[1:]))
    for k, s in enumerate(secs):
        ax = axs.flat[k]; t0 = s['t']; t1 = secs[k + 1]['t'] if k + 1 < n else dur
        xs = []; zs = []
        for a, b in segs:
            if b[0] < t0 - 3 or a[0] > t1 + 3: continue
            inside = a[0] < t1 and b[0] > t0
            y = elev_at(elev, (a[0] + b[0]) / 2)
            hx, hz = HEAD[ORDER[a[3]]]; px, pz = -hz * W / 2, hx * W / 2
            x0, z0, x1, z1 = a[1] - hx * W / 2, a[2] - hz * W / 2, b[1] + hx * W / 2, b[2] + hz * W / 2
            ax.add_patch(Polygon([(x0 + px, z0 + pz), (x1 + px, z1 + pz), (x1 - px, z1 - pz), (x0 - px, z0 - pz)], closed=True,
                                 fc=cm.plasma(norm(y)) if inside else '#dddddd', ec='k', lw=0.3, zorder=3 if inside else 1))
            if inside: xs += [a[1], b[1]]; zs += [a[2], b[2]]
        # older road nearby (context), grey
        if xs:
            cx0, cx1, cz0, cz1 = min(xs) - 6, max(xs) + 6, min(zs) - 6, max(zs) + 6
            for a, b in segs:
                if b[0] < t0 - 3 and min(a[1], b[1]) < cx1 and max(a[1], b[1]) > cx0 and min(a[2], b[2]) < cz1 and max(a[2], b[2]) > cz0:
                    ax.plot([a[1], b[1]], [a[2], b[2]], color='#9aa', lw=1, zorder=0)
            L = max(cx1 - cx0, cz1 - cz0) / 2; mx = (cx0 + cx1) / 2; mz = (cz0 + cz1) / 2
            ax.set_xlim(mx - L, mx + L); ax.set_ylim(mz - L, mz + L)
            x, z = world_of(nodes, t0 + 0.01); ax.plot(x, z, 'go', ms=6, zorder=9)
        ax.set_aspect('equal'); ax.set_title(f"{s['label']} {t0:.1f}-{t1:.1f}s", fontsize=9); ax.tick_params(labelsize=6)
    for k in range(n, rows * cols): axs.flat[k].axis('off')
    fig.suptitle(title + ' — per-section zoom (green dot = section start; grey = older road nearby)'); fig.tight_layout()
    fig.savefig(path, dpi=60); plt.close(fig)
