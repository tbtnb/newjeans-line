"""Build chart.json + layout.json + route.png for one song from: v3/<slug>.taps16.json (chart incl. 16th bursts),
plan_<slug>.py (route choreography moves + elevation), spec_<slug>.py (look, sections, camera, objects, events,
collectibles) and spec3_<slug>.py (v3 additions: section notes per route texture, features, art)."""
import sys, json, math, importlib, os
sys.path.insert(0, '/workspace/nj-w1-work/v3'); sys.path.insert(0, '/workspace/nj-w1-work')
from chore import *; from util import *
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
slug = sys.argv[1]; mod = slug.replace('-', '_')
OUT = f'/workspace/newjeans-line-designs/{slug}'; os.makedirs(OUT, exist_ok=True)
Pm = importlib.import_module('plan_' + mod); S = importlib.import_module('spec_' + mod); S3 = importlib.import_module('spec3_' + mod)
chart0, T = taps(slug); dur = Pm.dur
pl = Planner(T, dur, Pm.speed, Pm.widths, Pm.elev(T), Pm.moves(), start=Pm.start, max_tries=400000)
dirs, nodes, elev, choice = pl.solve()
elev = [{k: v for k, v in e.items() if not k.startswith('_')} for e in elev]
elev.sort(key=lambda e: e.get('t', e.get('t0')))
widths = Pm.widths
def W(t): return w_at(widths, t)
def Y(t): return elev_at(elev, t)
segs = list(zip(nodes, nodes[1:]))
def pos(t):
    for a, b in segs:
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / max(b[0] - a[0], 1e-9); return a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f, a[3]
    b = nodes[-1]; return b[1], b[2], b[3]
def seg_d(px, pz, a, b):
    ax, az, bx, bz = a[1], a[2], b[1], b[2]; vx, vz = bx - ax, bz - az; L = vx * vx + vz * vz
    f = 0 if L == 0 else max(0, min(1, ((px - ax) * vx + (pz - az) * vz) / L))
    return math.hypot(px - (ax + f * vx), pz - (az + f * vz)), a[0] + f * (b[0] - a[0])
def clear(px, pz, y0, y1, r, skip=None):
    """True if a vertical object spanning heights [y0,y1] with radius r at (px,pz) keeps clear of every road part."""
    for a, b in segs:
        if skip and skip[0] <= a[0] <= skip[1]: continue
        d, tt = seg_d(px, pz, a, b)
        yr = Y(tt)
        if yr < y0 - 1.0 or yr > y1 + 2.5: continue
        if d < r + W(tt) / 2 + 0.4: return False
    return True
class Ctx: pass
ctx = Ctx(); ctx.T = T; ctx.nodes = nodes; ctx.elev = elev; ctx.pos = pos; ctx.Y = Y; ctx.W = W; ctx.clear = clear; ctx.dur = dur
def move(name):
    m = next(m for m in pl.moves if m['name'] == name)
    ns = [n for n in nodes if m['t0'] - 1e-6 <= n[0] <= (T[m['_i1']] if m['_i1'] < len(T) else dur)]
    xs = [n[1] for n in ns]; zs = [n[2] for n in ns]
    return dict(t0=m['t0'], t1=ns[-1][0], cx=sum(xs) / len(xs), cz=sum(zs) / len(zs), bbox=(min(xs), max(xs), min(zs), max(zs)),
                ymin=min(Y(n[0]) for n in ns), ymax=max(Y(n[0]) for n in ns), nodes=ns)
ctx.move = move
ylow = min(min(Y(n[0]) for n in nodes), 0.0); ctx.ylow = ylow
def find_clear(x, z, y0, y1, r, step=1.0, maxr=25):
    for rr in np.arange(0, maxr, step):
        for k in range(max(1, int(2 * math.pi * rr / step))):
            a = 2 * math.pi * k / max(1, int(2 * math.pi * rr / step))
            px, pz = x + rr * math.cos(a), z + rr * math.sin(a)
            if clear(px, pz, y0, y1, r): return px, pz
    return None
ctx.find_clear = find_clear
YAW = {'N': 0, 'E': 90, 'S': 180, 'W': 270}
# ------------------------------------------------------------------ auto features
auto, cam_extra, feat_notes = [], [], []
# (1) pillars under raised road
cnt = 0; acc = 0.0
for a, b in segs:
    L = math.hypot(b[1] - a[1], b[2] - a[2]); acc += L
    tm = (a[0] + b[0]) / 2; y = Y(tm)
    if y - ylow < 2.5 or acc < 11: continue
    px, pz, _ = pos(tm); acc = 0
    h = y - 0.35 - (ylow - 6)
    # no other road between ground and this deck at this spot
    if not clear(px, pz, ylow - 6, y - 1.0, 0.45, skip=(tm - 3, tm + 3)): continue
    auto.append({'id': f'pier-{cnt}', 'kind': 'pillar', 'worldPos': [round(px, 2), round(ylow - 6, 2), round(pz, 2)], 'size': [0.7, round(h, 2), 0.7],
                 'color': S3.pier_color, 'onroad': True}); cnt += 1
# (2) crossings: over/under passes; camera lifts before passing under a higher deck
cross = []
B = [(min(a[1], b[1]) - W(a[0]) / 2, max(a[1], b[1]) + W(a[0]) / 2, min(a[2], b[2]) - W(a[0]) / 2, max(a[2], b[2]) + W(a[0]) / 2) for a, b in segs]
for j in range(len(segs)):
    for i in range(j - 1):
        if segs[j][0][0] - segs[i][1][0] < 1.5: continue
        bi, bj = B[i], B[j]
        if bi[0] < bj[1] and bj[0] < bi[1] and bi[2] < bj[3] and bj[2] < bi[3]:
            yi, yj = Y((segs[i][0][0] + segs[i][1][0]) / 2), Y((segs[j][0][0] + segs[j][1][0]) / 2)
            cross.append(dict(t_early=round(segs[i][0][0], 2), t_late=round(segs[j][0][0], 2), late_under=yj < yi, dy=round(yj - yi, 1)))
under = sorted(set(round(c['t_late'], 1) for c in cross if c['late_under']))
# (3) fake forks (visual only: a stub of decking continuing straight past a real corner, ending in a broken edge)
forks = []
for k, tf in enumerate(getattr(S3, 'fork_taps', [])):
    i = min(range(len(T)), key=lambda i: abs(T[i] - tf)); tc = T[i]
    x, z, _ = pos(tc - 1e-3); hin = next(a[3] for a, b in segs if a[0] <= tc - 1e-3 <= b[0])
    hx, hz = HEAD[hin]; w = W(tc); Lf = 5.0
    cx, cz = x + hx * (w / 2 + Lf / 2), z + hz * (w / 2 + Lf / 2)
    ok = all(clear(cx + hx * s, cz + hz * s, Y(tc) - 1, Y(tc) + 1, w * 0.45, skip=(tc - 1.0, tc + 1.0)) for s in (-Lf / 2 + 0.5, 0, Lf / 2))
    if not ok: continue
    forks.append(tc)
    auto.append({'id': f'fake-fork-{k}', 'kind': 'box', 'worldPos': [round(cx, 2), round(Y(tc) - 0.35, 2), round(cz, 2)], 'rot': YAW[hin],
                 'size': [round(w * 0.92, 2), 0.6, Lf], 'color': S.palette['road'], 'color2': S.palette['roadSide'], 'onroad': True,
                 'name': 'fake fork (scenery only, ends in a broken edge)', 'appear': {'t': round(tc - 1.6, 3), 'mode': 'rise', 'dur': 0.5},
                 'exit': {'t': round(tc + 1.2, 3), 'mode': 'fall', 'dur': 0.8}})
# (4) wrap-through buildings: arcade walls + roof beams around one long straight
def arcade_cands(entry):
    if len(entry) == 2: return [entry[0]], entry[1]
    t0, t1, name = entry
    ss = sorted([(b[0] - a[0], (a[0] + b[0]) / 2) for a, b in segs if a[0] >= t0 and b[0] <= t1], reverse=True)
    return [m for _, m in ss[:8]], name
arc_list = []
for entry in getattr(S3, 'arcades', []):
    cands_, name = arcade_cands(entry)
    arc_list.append((cands_, name))
for k, (cands_, name) in enumerate(arc_list):
  for tt in cands_:
      a, b = next((a, b) for a, b in segs if a[0] <= tt <= b[0])
      hx, hz = HEAD[a[3]]; rx, rz = hz, -hx; L = math.hypot(b[1] - a[1], b[2] - a[2]); w = W(tt); y = Y(tt)
      mx, mz = (a[1] + b[1]) / 2, (a[2] + b[2]) / 2; off = w / 2 + 0.9; parts = []
      ok = True
      for sgn in (-1, 1):
          for s in np.linspace(-L / 2 + w / 2 + 1.6, L / 2 - w / 2 - 1.6, max(2, int(L / 2))):
              if not clear(mx + rx * off * sgn + hx * s, mz + rz * off * sgn + hz * s, y, y + 5, 0.3, skip=(a[0] - 0.4, b[0] + 0.4)): ok = False
      if not ok: continue
      Lw = L - w - 2.6
      if Lw < 3: continue
      parts.append({'kind': 'box', 'pos': [-off, 2.4, 0], 'size': [0.6, 4.8, Lw], 'color': S3.arcade_colors[0]})
      parts.append({'kind': 'box', 'pos': [off, 2.4, 0], 'size': [0.6, 4.8, Lw], 'color': S3.arcade_colors[0]})
      if getattr(S3, 'arcade_texture', None):
          for sg in (-1, 1): parts.append({'kind': 'box', 'pos': [sg * (off - 0.32), 2.4, 0], 'size': [0.05, 3.6, Lw - 1.0], 'color': '#FFFFFF', 'texture': S3.arcade_texture})
      for s in np.arange(-Lw / 2 + 0.4, Lw / 2, 2.6):
          parts.append({'kind': 'box', 'pos': [0, 5.0, round(float(s), 2)], 'size': [2 * off + 0.6, 0.45, 0.5], 'color': S3.arcade_colors[1]})
      auto.append({'id': f'arcade-{k}', 'kind': 'group', 'worldPos': [round(mx, 2), round(y - 0.3, 2), round(mz, 2)], 'rot': YAW[a[3]], 'onroad': True,
                   'landmark': True, 'name': name, 'parts': parts, 'appear': {'t': round(a[0] - 2.5, 3), 'mode': 'rise', 'dur': 1.0}})
      cam_extra.append((a[0] - 0.5, b[0] + 0.5, {'preset': 'high', 'pitch': 66, 'blend': 0.6}))
      break
for tu in under:
    cam_extra.append((tu - 0.7, tu + 1.2, {'preset': 'high', 'blend': 0.5}))
# (5) song-specific v3 features (spiral towers, walls, etc.)
extra_objs, extra_events, extra_cam = S3.features(ctx)
for (t0, t1, cue) in extra_cam: cam_extra.append((t0, t1, cue))
# ------------------------------------------------------------------ camera merge
base = sorted(S3.camera if hasattr(S3, 'camera') else S.camera, key=lambda c: c['t'])
def active(t):
    c = base[0]
    for x in base:
        if x['t'] <= t: c = x
    return c
cam = list(base)
cam_extra.sort()
merged = []
for t0, t1, cue in cam_extra:
    if merged and t0 <= merged[-1][1]: merged[-1] = (merged[-1][0], max(merged[-1][1], t1), merged[-1][2]); continue
    merged.append((t0, t1, cue))
for t0, t1, cue in merged:
    cam = [c for c in cam if not (t0 < c['t'] < t1)]
    cam.append(dict(t=round(t0, 3), **cue))
    back = {k: v for k, v in active(t1).items() if k != 't'}; back['blend'] = 1.2
    cam.append(dict(t=round(t1, 3), **back))
cam.sort(key=lambda c: c['t'])
# ------------------------------------------------------------------ objects (anchored) + collectibles
objs = list(S3.objects(S.objects) if hasattr(S3, 'objects') else S.objects) + extra_objs + auto
cand = [round((T[i] + T[i + 1]) / 2, 3) for i in range(len(T) - 1) if T[i + 1] - T[i] >= 0.5]
crowns = []
for tt in S.crown_near:
    cc = [round((T[i] + T[i + 1]) / 2, 3) for i in range(len(T) - 1) if T[i + 1] - T[i] >= 0.6]
    crowns.append({'t': min(cc, key=lambda t: abs(t - tt))})
dia = []
for (t0, t1, n) in S.diamond_windows:
    c = [t for t in cand if t0 <= t < t1 and all(abs(t - x) > 3 for x in dia) and all(abs(t - x['t']) > 3 for x in crowns)]
    if len(c) < n: raise SystemExit(f'not enough diamond candidates in {t0}-{t1}: {len(c)}')
    idx = np.linspace(0, len(c) - 1, n + 2)[1:-1].round().astype(int); dia += [c[i] for i in idx]
assert len(dia) == 10
# ------------------------------------------------------------------ write chart.json
secs = chart0['sections']
chart = dict(id=slug, startHeading=Pm.start, speed=Pm.speed,
             taps=[dict(t=round(tp['t'], 3), dir=d, tag=tp['tag']) for tp, d in zip(chart0['taps'], dirs)],
             sections=secs, notes=S3.chart_notes,
             meta=dict(bpm=S3.bpm, bursts16=[round(tp['t'], 3) for tp in chart0['taps'] if tp.get('src') == '16th'],
                       route_moves=[dict(name=m['name'], kind=m['kind'], t0=m['t0'], variant={k: v for k, v in choice[m['name']].items() if v is not None}) for m in pl.moves]))
json.dump(chart, open(f'{OUT}/chart.json', 'w'), indent=1)
layout = dict(id=slug, title=S.title, palette=S3.palette if hasattr(S3, 'palette') else S.palette,
              road=dict(width=widths, height=0.6, reveal=S3.reveal if hasattr(S3, 'reveal') else S.reveal),
              elevation=elev, sections=S3.sections, camera=cam,
              objects=objs, events=sorted(S3.events(S.events) + extra_events, key=lambda e: e['t']),
              diamonds=[{'t': t, 'side': 0} for t in dia], crowns=crowns, finish=S.finish,
              collectibleColors=S3.collectibles, art=S3.art,
              route=dict(note='v3 route choreography; per-section textures', moves=[dict(name=m['name'], kind=m['kind'], t0=m['t0']) for m in pl.moves],
                         crossings=cross, fake_forks=forks),
              path=dict(note='computed centreline nodes [t, x, y(road height), z, heading after node]; N=+z, E=+x',
                        nodes=[[round(n[0], 3), round(n[1], 3), round(Y(n[0]), 3), round(n[2], 3), n[3]] for n in nodes]))
json.dump(layout, open(f'{OUT}/layout.json', 'w'), indent=1)
# ------------------------------------------------------------------ route.png
fig, ax = plt.subplots(figsize=(15, 15)); cols = plt.cm.tab20.colors
mvs = pl.moves
def mv_of(t): return max([k for k, m in enumerate(mvs) if m['t0'] <= t + 1e-6] or [0])
yr = [Y((a[0] + b[0]) / 2) for a, b in segs]; ymin, ymax = min(yr), max(yr)
order = np.argsort(yr)
for k in order:
    a, b = segs[k]; y = yr[k]; c = cols[(2 * mv_of(a[0])) % 20]
    lw = 1.6 + 3.2 * (y - ymin) / max(ymax - ymin, 1)
    ax.plot([a[1], b[1]], [a[2], b[2]], color='white', lw=lw + 2.2, solid_capstyle='butt', zorder=10 + y)
    ax.plot([a[1], b[1]], [a[2], b[2]], color=c, lw=lw, solid_capstyle='butt', zorder=10.1 + y)
for k, m in enumerate(mvs):
    x, z, _ = pos(m['t0'] + 0.01)
    ax.annotate(f"{m['name']} ({m['kind']}) {m['t0']:.1f}s y{Y(m['t0']):+.0f}", (x, z), fontsize=8, color=cols[(2 * k) % 20], zorder=200,
                xytext=(6, 6), textcoords='offset points', bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.75))
for c in cross:
    x, z, _ = pos(c['t_late'] + 0.05); ax.plot(x, z, 'x', color='purple', ms=7, zorder=150)
for o in objs:
    if o.get('worldPos') and (o.get('landmark') or o.get('egg')):
        ax.plot(o['worldPos'][0], o['worldPos'][2], '*', color='crimson' if o.get('egg') else 'k', ms=14, zorder=160)
        ax.annotate(o.get('name', o.get('id', '')), (o['worldPos'][0], o['worldPos'][2]), fontsize=7, xytext=(5, -10), textcoords='offset points', zorder=160)
for t in dia:
    x, z, _ = pos(t); ax.plot(x, z, 'D', color='deepskyblue', ms=7, mec='k', zorder=170)
for c in crowns:
    x, z, _ = pos(c['t']); ax.plot(x, z, '^', color='gold', ms=13, mec='k', zorder=170)
for e in elev:
    tt = e.get('t', e.get('t0')); x, z, _ = pos(tt)
    ax.annotate(f"{e['type']} {e['dy']:+g}", (x, z), fontsize=7, color='purple', zorder=180, xytext=(-30, -12), textcoords='offset points')
for tf in forks:
    x, z, _ = pos(tf); ax.plot(x, z, 'o', mfc='none', mec='darkorange', ms=12, zorder=165)
ax.plot(0, 0, 'go', ms=11, zorder=190); ax.plot(nodes[-1][1], nodes[-1][2], 'rs', ms=11, zorder=190)
ax.set_aspect('equal'); ax.grid(alpha=.25)
ax.set_title(f"{S.title}: {len(T)} taps | route textures coloured by move, line width = height ({ymin:+.0f}..{ymax:+.0f}) | x = multi-level crossing ({len(cross)}), "
             f"o = fake fork, * = landmark/egg, D = diamond, ^ = crown", fontsize=10)
fig.tight_layout(); fig.savefig(f'{OUT}/route.png', dpi=72); plt.close(fig)
print(slug, 'taps', len(T), 'crossings', len(cross), 'underpasses', len(under), 'forks', forks, 'piers', cnt, 'objs', len(objs), 'cams', len(cam))
