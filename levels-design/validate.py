#!/usr/bin/env python3
"""Validator for NewJeans Line v2 level data (schema v2.4). Builds the same centreline the engine builds.
Usage:  python3 validate.py <slug> [<slug> ...] [--dir DIR] [--repo REPO] [--no-preview]
  --dir  folder that contains <slug>/chart.json + layout.json (default: folder of this script, or $LEVEL_DIR)
  --repo repo root (for public/audio/<slug>.mp3 durations; default: parent of this script's folder, else /workspace/newjeans-line-rebuild)
Exit code 1 if any ERROR."""
import json, sys, os, math, subprocess
from pathlib import Path
SCRIPT = Path(__file__).resolve().parent

def opt(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv): return sys.argv[i + 1]
    return default
FLAG_ARGS = {'--dir', '--repo'}
args = []
skip = False
for i, a in enumerate(sys.argv[1:]):
    if skip: skip = False; continue
    if a in FLAG_ARGS: skip = True; continue
    if a.startswith('--'): continue
    args.append(a)
HERE = Path(opt('--dir') or os.environ.get('LEVEL_DIR') or SCRIPT)
REPO = Path(opt('--repo') or (SCRIPT.parent if (SCRIPT.parent / 'public/audio').exists() else '/workspace/newjeans-line-rebuild'))
PREVIEW = '--no-preview' not in sys.argv
HEAD = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
ORDER = ['N', 'E', 'S', 'W']
G = 30.0; AIR_MIN = 0.15; LAND_BEFORE = 0.05; MIN_AIR_GAP = 0.35
W_MIN, W_MAX, RATIO = 0.045, 0.11, 0.45
MIN_GAP = 0.105

def duration(slug):
    p = REPO / 'public/audio' / f'{slug}.mp3'
    if not p.exists(): return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout
    return float(out)

def speed_at(speeds, t):
    v = 9.0
    for s in speeds:
        if s['t'] <= t + 1e-9: v = s['v']
    return v

def build(chart, dur):
    speeds = sorted(chart.get('speed', []) or [{'t': 0, 'v': 9.0}], key=lambda s: s['t'])
    taps = chart['taps']
    h = ORDER.index(chart.get('startHeading', 'N'))
    nodes = [(0.0, 0.0, 0.0, h)]
    last = 'L'; dirs = []
    for tp in taps:
        d = tp.get('dir') or ('R' if last == 'L' else 'L'); dirs.append(d); last = d
    t0, x, z = 0.0, 0.0, 0.0
    bps = sorted(set([0.0] + [s['t'] for s in speeds]))
    for i, t in enumerate([tp['t'] for tp in taps] + [dur]):
        dist, a = 0.0, t0
        for b in [p for p in bps if t0 < p < t] + [t]:
            dist += (b - a) * speed_at(speeds, a); a = b
        dx, dz = HEAD[ORDER[h]]; x += dx * dist; z += dz * dist
        if i < len(taps): h = (h + (1 if dirs[i] == 'R' else -1)) % 4
        nodes.append((t, x, z, h)); t0 = t
    return nodes, dirs

def air_spans(layout, taps, dur):
    out = []
    for e in layout.get('elevation', []):
        if e['type'] not in ('fall', 'jump'): continue
        dy = e['dy']
        if dy < 0: vy = 2.0; d = (vy + math.sqrt(vy * vy - 2 * G * dy)) / G
        else: d = 0.6
        nxt = next((t for t in taps if t > e['t'] + 1e-6), dur)
        d = min(d, max(AIR_MIN, nxt - e['t'] - LAND_BEFORE))
        out.append((e['t'], e['t'] + d, dy, nxt))
    return out

def elev_at(layout, t):
    y = 0.0
    for e in layout.get('elevation', []):
        if e['type'] in ('fall', 'jump') and e['t'] <= t: y += e['dy']
        if e['type'] == 'ramp':
            if t >= e['t1']: y += e['dy']
            elif t > e['t0']: y += e['dy'] * (t - e['t0']) / (e['t1'] - e['t0'])
    return y

def windows(taps):
    w = []
    for i, t in enumerate(taps):
        p = t - taps[i - 1] if i > 0 else 9; n = taps[i + 1] - t if i + 1 < len(taps) else 9
        g = min(p, n); w.append(min(0.5 * g, max(W_MIN, min(W_MAX, RATIO * g))))
    return w

def main(slug):
    d = HERE / slug
    if not (d / 'chart.json').exists(): print(f'== {slug}: no chart.json in {d}'); return 1
    chart = json.loads((d / 'chart.json').read_text())
    layout = json.loads((d / 'layout.json').read_text()) if (d / 'layout.json').exists() else {}
    dur = duration(slug)
    errs, warns = [], []
    taps = [tp['t'] for tp in chart['taps']]
    if dur is None: dur = (taps[-1] + 5) if taps else 60; warns.append(f'audio not found under {REPO}; duration guessed')
    for a, b in zip(taps, taps[1:]):
        if b <= a: errs.append(f'taps not increasing at {a}->{b}')
        elif b - a < MIN_GAP: errs.append(f'gap {b-a:.3f}s < {MIN_GAP} at {a}')
    if taps and taps[0] < 1.0: errs.append('first tap < 1.0 s')
    if taps and taps[-1] > dur - 1.0: errs.append('last tap > duration-1')
    for tp in chart['taps']:
        if tp.get('dir') not in (None, 'L', 'R'): errs.append(f'bad dir {tp.get("dir")} at {tp["t"]}')
    # air-time rule
    for (a0, a1, dy, nxt) in air_spans(layout, taps, dur):
        if nxt - a0 < MIN_AIR_GAP: errs.append(f'{"fall" if dy < 0 else "jump"} at {a0} is only {nxt-a0:.3f}s before the next tap (need >= {MIN_AIR_GAP}s; no taps in mid-air)')
    for e in layout.get('elevation', []):
        if e['type'] == 'ramp' and not (e.get('t1', 0) > e.get('t0', 0)): errs.append(f'ramp needs t1 > t0 ({e})')
    nodes, dirs = build(chart, dur)
    segs = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
    widths = sorted(layout.get('road', {}).get('width', [{'t': 0, 'w': 2.2}]), key=lambda w: w['t'])
    def w_at(t):
        w = 2.2
        for x in widths:
            if x['t'] <= t: w = x['w']
        return w
    def bbox(s):
        (ta, xa, za, _), (tb, xb, zb, _) = s; W = max(w_at(ta), w_at(tb))
        return min(xa, xb) - W / 2, max(xa, xb) + W / 2, min(za, zb) - W / 2, max(za, zb) + W / 2
    boxes = [bbox(s) for s in segs]
    hits = 0; crossings = 0
    for i in range(len(segs)):
        for j in range(i + 2, len(segs)):
            a, b = boxes[i], boxes[j]
            if not (a[0] < b[1] and b[0] < a[1] and a[2] < b[3] and b[2] < a[3]): continue
            if segs[j][0][0] - segs[i][1][0] < 1.5: continue
            # height check over the overlapping sub-intervals: sample both segments
            ti = (segs[i][0][0] + segs[i][1][0]) / 2; tj = (segs[j][0][0] + segs[j][1][0]) / 2
            dyv = min(abs(elev_at(layout, segs[i][0][0] + f * (segs[i][1][0] - segs[i][0][0])) - elev_at(layout, segs[j][0][0] + g * (segs[j][1][0] - segs[j][0][0]))) for f in (0.02, 0.5, 0.98) for g in (0.02, 0.5, 0.98))
            if dyv < 3:
                hits += 1
                if hits <= 8: errs.append(f'road overlaps itself on the same level: seg@{segs[i][0][0]:.2f}s and seg@{segs[j][0][0]:.2f}s (dy {dyv:.1f} < 3)')
            else: crossings += 1
    if hits > 8: errs.append(f'... {hits} overlaps total')
    secs = sorted(chart.get('sections', []), key=lambda s: s['t'])
    print(f'== {slug}  duration {dur:.2f}s  taps {len(taps)}  dirs R/L {dirs.count("R")}/{dirs.count("L")}  multi-level crossings {crossings}')
    gaps = [b - a for a, b in zip(taps, taps[1:])]
    if gaps: print(f'   min gap {min(gaps):.3f}s  median gap {sorted(gaps)[len(gaps)//2]:.3f}s')
    best, cur, start, bs = 0, 0, 0, 0
    for i, g in enumerate(gaps):
        if g <= 0.3:
            if cur == 0: start = i
            cur += 1
            if cur > best: best, bs = cur, start
        else: cur = 0
    if taps:
        cpm = [sum(1 for u in taps if t <= u < t + 1.0) * 60 for t in taps]
        print(f'   peak density {max(cpm)} CPM (taps in any 1 s window x60), average {len(taps) / dur * 60:.0f} CPM; gaps < 0.15 s: {sum(1 for g in gaps if g < 0.15)}')
    if best: print(f'   fastest run: {best+1} taps (gaps<=0.30s) from {taps[bs]:.2f}s to {taps[bs+best]:.2f}s')
    if taps:
        w = windows(taps); print(f'   judgment window: min ±{min(w)*1000:.0f} ms, median ±{sorted(w)[len(w)//2]*1000:.0f} ms (engine rule)')
    # turn structure: same-direction runs (spirals/U-turns)
    run, maxrun = 1, 1
    for a, b in zip(dirs, dirs[1:]):
        run = run + 1 if a == b else 1; maxrun = max(maxrun, run)
    print(f'   longest same-direction run {maxrun} (>=2 = U-turn, >=4 = spiral)  elevation events {len(layout.get("elevation", []))}')
    for k, s in enumerate(secs):
        e = secs[k + 1]['t'] if k + 1 < len(secs) else dur
        n = sum(1 for t in taps if s['t'] <= t < e)
        print(f'   {s["t"]:7.2f}-{e:7.2f} {s.get("kind",""):7s} {s.get("label",""):28s} {n:4d} taps  {n/max(e-s["t"],1e-6):.2f}/s')
    if layout:
        if len(layout.get('diamonds', [])) != 10: errs.append(f'need exactly 10 diamonds (have {len(layout.get("diamonds", []))})')
        if len(layout.get('crowns', [])) != 2: errs.append(f'need exactly 2 crowns (have {len(layout.get("crowns", []))})')
        for dm in layout.get('diamonds', []):
            if any(abs(dm['t'] - t) < 0.2 for t in taps): warns.append(f'diamond at {dm["t"]} within 0.2s of a tap')
            if abs(dm.get('side', 0)) > w_at(dm['t']) / 2: errs.append(f'diamond at {dm["t"]} side {dm.get("side")} is off the road')
        for c in layout.get('crowns', []):
            if any(abs(c['t'] - t) < 0.3 for t in taps): warns.append(f'crown at {c["t"]} within 0.3s of a tap (checkpoint should sit on a calm straight)')
        # art references
        refs = []
        art = layout.get('art', {}) or {}
        if art.get('backdrop'): refs.append(art['backdrop'])
        for k in ('ground', 'road'):
            if isinstance(art.get(k), dict) and art[k].get('src'): refs.append(art[k]['src'])
        for s in layout.get('sections', []):
            if s.get('backdrop'): refs.append(s['backdrop'])
        def walk(o):
            if o.get('src'): refs.append(o['src'])
            if o.get('texture'): refs.append(o['texture'])
            for p in o.get('parts', []) or []: walk(p)
            if o.get('item'): walk(o['item'])
        for o in layout.get('objects', []): walk(o)
        for r in refs:
            if not (d / r).exists(): errs.append(f'missing art file {r}')
            elif (d / r).stat().st_size > 1.6e6: warns.append(f'art file {r} is large ({(d / r).stat().st_size/1e6:.1f} MB)')
        txt = json.dumps(layout).lower()
        for bad in ('guide', 'hint', 'marker', 'countdown', 'arrow'):
            if f'"{bad}' in txt or f'_{bad}' in txt: warns.append(f'layout mentions "{bad}": make sure nothing previews upcoming taps')
    xs = [n[1] for n in nodes]; zs = [n[2] for n in nodes]
    print(f'   extent x[{min(xs):.0f},{max(xs):.0f}] z[{min(zs):.0f},{max(zs):.0f}]')
    for e in errs: print('   ERROR', e)
    for w in warns[:12]: print('   warn', w)
    if PREVIEW:
        try:
            import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 10)); cols = plt.cm.tab10.colors
            for s in segs:
                t = s[0][0]; k = max([j for j, sc in enumerate(secs) if sc['t'] <= t] or [0])
                ax.plot([s[0][1], s[1][1]], [s[0][2], s[1][2]], color=cols[k % 10], lw=1.0 + max(0, elev_at(layout, t)) * 0.3)
            ax.set_aspect('equal'); ax.set_title(f'{slug}: {len(taps)} taps (line width ~ height)'); fig.savefig(d / 'preview.png', dpi=80); plt.close(fig)
        except Exception as ex:
            print('   (preview skipped:', ex, ')')
    return 1 if errs else 0

if __name__ == '__main__':
    sys.exit(max([main(s) for s in args] or [0]))
