#!/usr/bin/env python3
"""Validator for NewJeans Line v2 level data. Usage: validate.py <slug> [--repo /path/to/repo]
Builds the exact centerline the engine builds (speed steps, 90deg turns, elevation), checks rules, writes preview.png."""
import json, sys, math, subprocess
from pathlib import Path
HERE = Path(__import__('os').environ.get('LEVEL_DIR') or Path(__file__).resolve().parent)
args = [a for a in sys.argv[1:] if not a.startswith('--')]
repo = Path('/workspace/newjeans-line-rebuild')
if '--repo' in sys.argv: repo = Path(sys.argv[sys.argv.index('--repo') + 1])
HEAD = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
ORDER = ['N', 'E', 'S', 'W']

def duration(slug):
    for r in [repo, Path('/workspace/newjeans-line-rebuild')]:
        p = r / 'public/audio' / f'{slug}.mp3'
        if p.exists():
            out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True).stdout
            return float(out)
    return None

def speed_at(speeds, t):
    v = 9.0
    for s in speeds:
        if s['t'] <= t: v = s['v']
    return v

def build(chart, layout, dur):
    speeds = sorted(chart.get('speed', [{'t': 0, 'v': 9.0}]), key=lambda s: s['t'])
    taps = chart['taps']
    h = ORDER.index(chart.get('startHeading', 'N'))
    nodes = [(0.0, 0.0, 0.0, h)]  # t, x, z, heading index
    last = 'L'
    times = [tp['t'] for tp in taps] + [dur]
    dirs = []
    for tp in taps:
        d = tp.get('dir') or ('R' if last == 'L' else 'L')
        dirs.append(d); last = d
    t0, x, z = 0.0, 0.0, 0.0
    bps = sorted(set([0.0] + [s['t'] for s in speeds]))
    for i, t in enumerate(times):
        # integrate distance over speed steps
        dist, a = 0.0, t0
        for b in [p for p in bps if t0 < p < t] + [t]:
            dist += (b - a) * speed_at(speeds, a); a = b
        dx, dz = HEAD[ORDER[h]]
        x += dx * dist; z += dz * dist
        if i < len(taps):
            h = (h + (1 if dirs[i] == 'R' else -1)) % 4
        nodes.append((t, x, z, h)); t0 = t
    return nodes, dirs

def elev_at(layout, t):
    y = 0.0
    for e in layout.get('elevation', []):
        if e['type'] in ('fall', 'jump') and e['t'] <= t: y += e['dy']
        if e['type'] == 'ramp':
            if t >= e['t1']: y += e['dy']
            elif t > e['t0']: y += e['dy'] * (t - e['t0']) / (e['t1'] - e['t0'])
    return y

def main(slug):
    d = HERE / slug
    chart = json.loads((d / 'chart.json').read_text())
    layout = json.loads((d / 'layout.json').read_text()) if (d / 'layout.json').exists() else {}
    dur = duration(slug)
    errs, warns = [], []
    taps = [tp['t'] for tp in chart['taps']]
    for a, b in zip(taps, taps[1:]):
        if b <= a: errs.append(f'taps not increasing at {a}->{b}')
        elif b - a < 0.15: errs.append(f'gap {b-a:.3f}s < 0.15 at {a}')
    if taps and taps[0] < 1.0: errs.append('first tap < 1.0 s')
    if taps and dur and taps[-1] > dur - 1.0: errs.append('last tap > duration-1')
    nodes, dirs = build(chart, layout, dur)
    # self intersection (segment vs non-adjacent segment, same height)
    segs = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
    W = max([w['w'] for w in layout.get('road', {}).get('width', [{'w': 2.2}])] or [2.2])
    def bbox(s):
        (ta, xa, za, _), (tb, xb, zb, _) = s
        return min(xa, xb) - W / 2, max(xa, xb) + W / 2, min(za, zb) - W / 2, max(za, zb) + W / 2
    boxes = [bbox(s) for s in segs]
    hits = 0
    for i in range(len(segs)):
        for j in range(i + 2, len(segs)):
            a, b = boxes[i], boxes[j]
            if segs[j][0][0] - segs[i][1][0] < 1.5: continue  # neighbouring stair steps may merge into one band (DL-authentic)
            if a[0] < b[1] and b[0] < a[1] and a[2] < b[3] and b[2] < a[3]:
                ti = (segs[i][0][0] + segs[i][1][0]) / 2; tj = (segs[j][0][0] + segs[j][1][0]) / 2
                if abs(elev_at(layout, ti) - elev_at(layout, tj)) < 3:
                    hits += 1
                    if hits <= 8: errs.append(f'road overlaps itself: seg@{segs[i][0][0]:.2f}s and seg@{segs[j][0][0]:.2f}s')
    if hits > 8: errs.append(f'... {hits} overlaps total')
    # stats
    secs = sorted(chart.get('sections', []), key=lambda s: s['t'])
    print(f'== {slug}  duration {dur:.2f}s  taps {len(taps)}  dirs R/L {dirs.count("R")}/{dirs.count("L")}')
    gaps = [b - a for a, b in zip(taps, taps[1:])]
    if gaps: print(f'   min gap {min(gaps):.3f}s  median gap {sorted(gaps)[len(gaps)//2]:.3f}s')
    # fastest run: longest run of consecutive gaps <= 0.3s
    best, cur, start, bs = 0, 0, 0, 0
    for i, g in enumerate(gaps):
        if g <= 0.3:
            if cur == 0: start = i
            cur += 1
            if cur > best: best, bs = cur, start
        else: cur = 0
    if best: print(f'   fastest run: {best+1} taps (gaps<=0.30s) from {taps[bs]:.2f}s to {taps[bs+best]:.2f}s')
    for k, s in enumerate(secs):
        e = secs[k + 1]['t'] if k + 1 < len(secs) else dur
        n = sum(1 for t in taps if s['t'] <= t < e)
        print(f'   {s["t"]:7.2f}-{e:7.2f} {s.get("kind",""):7s} {s.get("label",""):24s} {n:4d} taps  {n/max(e-s["t"],1e-6):.2f}/s')
    if len(layout.get('diamonds', [])) not in (0, 10): errs.append('need exactly 10 diamonds')
    if len(layout.get('crowns', [])) not in (0, 2): errs.append('need exactly 2 crowns')
    for dm in layout.get('diamonds', []):
        if any(abs(dm['t'] - t) < 0.2 for t in taps): warns.append(f'diamond at {dm["t"]} within 0.2s of a tap')
    xs = [n[1] for n in nodes]; zs = [n[2] for n in nodes]
    print(f'   extent x[{min(xs):.0f},{max(xs):.0f}] z[{min(zs):.0f},{max(zs):.0f}]')
    for e in errs: print('   ERROR', e)
    for w in warns[:10]: print('   warn', w)
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 10))
        cols = plt.cm.tab10.colors
        for i, s in enumerate(segs):
            t = s[0][0]; k = max([j for j, sc in enumerate(secs) if sc['t'] <= t] or [0])
            ax.plot([s[0][1], s[1][1]], [s[0][2], s[1][2]], color=cols[k % 10], lw=1.5)
        for o in layout.get('objects', []):
            if 't' in o:
                # approximate anchor
                for a, b in segs:
                    if a[0] <= o['t'] <= b[0]:
                        f = (o['t'] - a[0]) / max(b[0] - a[0], 1e-9); px = a[1] + (b[1] - a[1]) * f; pz = a[2] + (b[2] - a[2]) * f
                        hx, hz = HEAD[ORDER[a[3]]]; rx, rz = hz, -hx
                        px += rx * o.get('side', 0) + hx * o.get('along', 0); pz += rz * o.get('side', 0) + hz * o.get('along', 0)
                        ax.plot(px, pz, 's' if not o.get('landmark') else '*', color='k' if not o.get('egg') else 'r', ms=4 if not o.get('landmark') else 12)
                        break
        ax.set_aspect('equal'); ax.set_title(f'{slug}: {len(taps)} taps'); fig.savefig(d / 'preview.png', dpi=90); plt.close(fig)
    except Exception as ex:
        print('   (preview skipped:', ex, ')')
    return 1 if errs else 0

if __name__ == '__main__':
    sys.exit(max([main(s) for s in args] or [0]))
