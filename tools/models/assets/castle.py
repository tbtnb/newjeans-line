"""H01 弹出立体城堡 Pop-up Castle (z04 drop landmark, z10 reprise) - built to the three-view sheet
levels-design/omg/redesign-v3/C/assets/H01_popup_castle (size 14.8 x 12 x 18 m incl. book base + flags, budget 6000 tris).
Front faces -Y. Pivots (spec.json): root = page fold (whole pops up on the DROP), tower0..4 = tower bases (staggered scale-y pop,
1/8 beat apart), flag0..4 = pole tops (swing +-15 deg on the beat). Windows are lamp-coloured cut-outs (glow pulse = engine side)."""
BUDGET = 6000
CREAM, CREAM2, BLUSH, BLUSH2, LAV, LAV2, GOLD, LAMP, PINK, COVER = '#FFF3DE', '#F6E6CF', '#FFC7DA', '#F9B6CB', '#B9A6F0', '#CFC0FA', '#F7D98B', '#FFC968', '#FF6FAE', '#F08CA8'
PAGE = 0.8   # page top (castle stands on the open book)

def book(P):
    parts = [P.box('cover', (14.8, 12.0, 0.22), loc=(0, 0, 0), color=COVER)]
    for s in (-1, 1):   # two page blocks, gently sloped into the spine (V), gold fore-edge
        parts.append(P.prism(f'pages{s}', [(0, 0.22), (s * 7.1, 0.22), (s * 7.1, 0.62), (s * 3.0, 0.85), (0, 0.6)][::s], 11.4, loc=(0, 0, 0), color=lambda c, n: CREAM if n.z > 0.5 else CREAM2, side_color=None))
        parts.append(P.box(f'edge{s}', (0.12, 11.4, 0.4), loc=(s * 7.1, 0, 0.22), color=GOLD))
        for y in (-5.75, 5.75): parts.append(P.box(f'corner{s}{y}', (0.7, 0.5, 0.28), loc=(s * 7.05, y, 0), color=GOLD))
    return parts

def windows(P, name, x, y, z0, r, n=1, w=0.42, h=1.1):
    out = []
    for k in range(n):
        out.append(P.prism(f'{name}win{k}', [(-w / 2, 0), (w / 2, 0), (w / 2, h * 0.7), (0, h), (-w / 2, h * 0.7)], 0.06, loc=(x, y - r - 0.02, z0 + k * (h + 0.9)), color=LAMP))
    return out

def tower(P, i, x, y, r, top, roof, banner=False):
    """octagonal tower: body (blush/cream facets), gold crenellated rim, lavender cone, gold finial + pole, heart flag"""
    two = lambda a, b: (lambda c, n: a if n.x < -0.2 or n.y < -0.6 else b)
    body = [P.cyl(f't{i}body', r, top - PAGE, 8, loc=(x, y, PAGE), color=two(CREAM, BLUSH))]
    body.append(P.cyl(f't{i}base', r * 1.12, 0.7, 8, loc=(x, y, PAGE), color=GOLD))
    body.append(P.cyl(f't{i}rim', r * 1.2, 0.55, 8, loc=(x, y, top), color=two(BLUSH, BLUSH2)))
    body.append(P.cyl(f't{i}rimg', r * 1.24, 0.12, 8, loc=(x, y, top + 0.55), color=GOLD))
    body.append(P.cyl(f't{i}roof', r * 1.18, roof, 8, loc=(x, y, top + 0.67), r2=0, color=two(LAV, LAV2)))
    body += windows(P, f't{i}', x, y, PAGE + (top - PAGE) * 0.42, r * 0.93, n=1 if top < 9 else 2)
    if banner: body.append(P.prism(f't{i}ban', [(-0.38, 0), (0.38, 0), (0.38, 1.7), (0, 1.45), (-0.38, 1.7)][::-1], 0.04, loc=(x + r * 0.35, y - r * 0.95, PAGE + 1.4), color=PINK))
    apex = top + 0.67 + roof
    body.append(P.ico(f't{i}fin', 0.16, loc=(x, y, apex), color=GOLD, subdiv=1))
    body.append(P.cyl(f't{i}pole', 0.06, 1.25, 4, loc=(x, y, apex), color=GOLD))
    fl = P.prism(f't{i}flag', [(0, 0)] + [(0.9 + px * 0.85, pz * 0.85 - 0.75) for px, pz in P.heart(1.0, 10)], 0.05, loc=(x + 0.05, y, apex + 1.2), color=PINK)
    flag = P.pivot(f'flag{i}', (x, y, apex + 1.2), [fl])
    return P.pivot(f'tower{i}', (x, y, PAGE), body + [flag])

def crenels(P, name, x0, x1, y, z, n, color=BLUSH2, depth=0.5):
    step = (x1 - x0) / n
    return [P.box(f'{name}{k}', (step * 0.55, depth, 0.5), loc=(x0 + step * (k + 0.5), y, z), color=color) for k in range(n)]

def build(P, spec):
    parts = book(P)
    # back wall + inner hall (blush), side walls, front wall
    parts.append(P.box('backwall', (8.8, 0.9, 7.8), loc=(0, 2.8, PAGE), color=BLUSH)); parts += crenels(P, 'bcr', -4.4, 4.4, 2.8, PAGE + 7.8, 9)
    parts.append(P.box('hall', (6.0, 3.6, 6.4), loc=(0, 0.9, PAGE), color=lambda c, n: BLUSH if n.y < -0.5 else BLUSH2))
    for s in (-1, 1):
        parts.append(P.box(f'sidewall{s}', (0.8, 4.2, 5.6), loc=(s * 4.35, 0.7, PAGE), color=BLUSH2)); parts += crenels(P, f'scr{s}', -0.5, 0.5, 0.7, PAGE + 5.6, 1, depth=3.6)
        parts.append(P.box(f'frontwall{s}', (2.6, 0.7, 4.6), loc=(s * 2.75, -1.5, PAGE), color=CREAM)); parts += crenels(P, f'fcr{s}', s * 1.45, s * 4.05, -1.5, PAGE + 4.6, 3, color=CREAM2)
        parts.append(P.prism(f'gem{s}', [(0, 0), (0.25, 0.4), (0, 0.8), (-0.25, 0.4)], 0.05, loc=(s * 2.6, -1.88, PAGE + 2.6), color=GOLD))
    # gatehouse: cream block with gable, gold-rimmed glowing arched door, heart medallion
    parts.append(P.box('gate', (3.4, 1.8, 5.2), loc=(0, -1.9, PAGE), color=CREAM))
    parts.append(P.prism('gable', [(-1.9, 0), (1.9, 0), (0, 1.35)], 1.9, loc=(0, -1.9, PAGE + 5.2), color=CREAM2, side_color=GOLD))
    parts.append(P.prism('doorRim', [(-1.25, 0), (1.25, 0), (1.25, 2.4), (0.85, 3.25), (0, 3.55), (-0.85, 3.25), (-1.25, 2.4)], 0.08, loc=(0, -2.83, PAGE), color=GOLD))
    parts.append(P.prism('door', [(-1.05, 0), (1.05, 0), (1.05, 2.3), (0.7, 3.05), (0, 3.3), (-0.7, 3.05), (-1.05, 2.3)], 0.08, loc=(0, -2.9, PAGE), color=LAMP))
    parts.append(P.prism('medal', P.heart(0.6, 10), 0.06, loc=(0, -2.86, PAGE + 4.05), color=PINK))
    # stairs down to the page + two finial pillars
    for k in range(5): parts.append(P.box(f'step{k}', (2.6, 0.5, (5 - k) * 0.32), loc=(0, -3.05 - k * 0.5, PAGE), color=CREAM if k % 2 else CREAM2))
    for s in (-1, 1):
        parts.append(P.box(f'pil{s}', (0.75, 0.75, 1.5), loc=(s * 1.75, -4.4, PAGE), color=BLUSH))
        parts.append(P.cyl(f'pilg{s}', 0.42, 0.18, 4, loc=(s * 1.75, -4.4, PAGE + 1.5), color=GOLD, rot=(0, 0, 45)))
        parts.append(P.cyl(f'pilf{s}', 0.3, 0.75, 4, loc=(s * 1.75, -4.4, PAGE + 1.68), r2=0, color=GOLD, rot=(0, 0, 45)))
    # pop-up fold tabs (triangular paper braces at the tower feet)
    for k, (x, y, ry) in enumerate(((-5.9, -1.4, 90), (5.9, -1.4, 90), (-6.0, 2.8, 90), (6.0, 2.8, 90), (-3.3, -3.0, 0), (3.3, -3.0, 0))):
        parts.append(P.card(f'tab{k}', [(-0.7, 0), (0.7, 0), (0, 1.6)], loc=(x, y, PAGE), color=CREAM2, rot=(0, 0, ry)))
    # keep (square, tallest) with banner, then the 4 octagonal towers
    keep = [P.box('keep', (3.2, 3.2, 12.1), loc=(0, 4.2, PAGE), color=lambda c, n: CREAM if n.y < -0.5 else BLUSH)]
    keep.append(P.box('keepRim', (3.8, 3.8, 0.6), loc=(0, 4.2, PAGE + 12.1), color=BLUSH2)); keep += crenels(P, 'kcr', -1.9, 1.9, 2.4, PAGE + 12.7, 4)
    keep.append(P.box('keepRimG', (3.9, 3.9, 0.12), loc=(0, 4.2, PAGE + 12.0), color=GOLD))
    keep.append(P.cyl('keepRoof', 2.05, 3.1, 8, loc=(0, 4.2, PAGE + 12.7), r2=0, color=lambda c, n: LAV if n.x < -0.2 or n.y < -0.6 else LAV2))
    keep += windows(P, 'keep', 0, 4.2, PAGE + 9.2, 1.6, n=1, w=0.55, h=1.4); keep.append(P.prism('keepWin2', [(-0.25, 0), (0.25, 0), (0.25, 0.8), (0, 1.1), (-0.25, 0.8)], 0.06, loc=(0.75, 2.58, PAGE + 9.4), color=LAMP))
    keep.append(P.prism('keepBan', [(-0.7, 0), (0.7, 0), (0.7, 2.6), (0, 2.2), (-0.7, 2.6)][::-1], 0.05, loc=(0, 2.56, PAGE + 6.0), color=PINK))
    keep.append(P.prism('keepBanH', P.heart(0.8, 10), 0.03, loc=(0, 2.52, PAGE + 7.1), color=BLUSH))
    ka = PAGE + 15.8; keep += [P.ico('kfin', 0.2, loc=(0, 4.2, ka), color=GOLD, subdiv=1), P.cyl('kpole', 0.07, 1.4, 4, loc=(0, 4.2, ka), color=GOLD)]
    kflag = P.pivot('flag0', (0, 4.2, ka + 1.35), [P.prism('kflag', [(0, 0)] + [(1.1 + px * 1.05, pz * 1.05 - 0.9) for px, pz in P.heart(1.0, 10)], 0.05, loc=(0.06, 4.2, ka + 1.35), color=PINK)])
    t0 = P.pivot('tower0', (0, 4.2, PAGE), keep + [kflag])
    towers = [t0, tower(P, 1, -4.4, 2.8, 1.35, PAGE + 9.9, 2.9), tower(P, 2, 4.4, 2.8, 1.35, PAGE + 9.9, 2.9),
              tower(P, 3, -4.3, -1.4, 1.25, PAGE + 5.4, 2.6, banner=True), tower(P, 4, 4.3, -1.4, 1.25, PAGE + 5.4, 2.6, banner=True)]
    P.pivot('root', (0, 0, 0), parts + towers)
