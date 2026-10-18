"""Pop-up paper castle (z04 landmark, ~14 m wide). Pivots: root (pop-up), flags (wave), gate (hinge)."""
BUDGET = 8000
WALL, WALL2, ROOF, ROOF2, PINK, GOLD, WIN = '#FFF3DE', '#F1E2C8', '#B9A6F0', '#D7C8FF', '#FF6FAE', '#F7D98B', '#FFC968'

def tower(P, name, x, y, r, h, roof_h, segs=8, flag=True):
    parts = [P.cyl(name + 'W', r, h, segs, loc=(x, y, 0), color=lambda c, n: P.mix(WALL, WALL2, 0.4 if n.x > 0 else 0.0))]
    parts.append(P.cyl(name + 'Rim', r * 1.12, 0.35, segs, loc=(x, y, h), color=GOLD))
    parts.append(P.cyl(name + 'R', r * 1.22, roof_h, segs, loc=(x, y, h + 0.35), color=lambda c, n: ROOF if (n.x + n.y) < 0 else ROOF2, r2=0))
    # two lit windows facing front
    for k, z in enumerate((h * 0.45, h * 0.75)):
        parts.append(P.prism(name + f'Win{k}', [(-0.22, 0), (0.22, 0), (0.22, 0.5), (0, 0.72), (-0.22, 0.5)], 0.08, loc=(x, y - r * 0.98, z), color=WIN))
    top = h + 0.35 + roof_h; fl = []
    if flag:
        pole = P.cyl(name + 'Pole', 0.05, 1.4, 4, loc=(x, y, top - 0.1), color=GOLD)
        hrt = P.prism(name + 'Hrt', P.heart(0.5, 10), 0.1, loc=(x, y, top + 1.25), color=GOLD)
        f = P.prism(name + 'Flag', [(0, 0), (1.3, 0.12), (1.0, 0.28), (1.3, 0.45), (0, 0.5)], 0.04, loc=(x + 0.05, y, top + 0.75), color=PINK)
        fl = [P.pivot(name + 'flag', (x, y, top + 1.0), [f])]; parts += [pole, hrt]
    return parts, fl

def build(P, spec):
    parts, flags = [], []
    # curtain wall with crenellations
    parts.append(P.box('wall', (11, 1.0, 3.6), loc=(0, 0.5, 0), color=WALL))
    for i in range(12):
        parts.append(P.box(f'cren{i}', (0.55, 1.05, 0.5), loc=(-5.2 + i * 0.945, 0.5, 3.6), color=WALL2))
    parts.append(P.box('trim', (11.2, 1.1, 0.2), loc=(0, 0.5, 3.3), color=GOLD))
    # keep
    parts.append(P.box('keep', (4.6, 3.6, 6.5), loc=(0, 2.6, 0), color=WALL))
    parts.append(P.cyl('keepRoof', 3.2, 3.6, 4, loc=(0, 2.6, 6.5), color=lambda c, n: ROOF if n.y < 0 else ROOF2, r2=0, rot=(0, 0, 45)))
    for k, x in enumerate((-1.2, 1.2)):
        parts.append(P.prism(f'kwin{k}', [(-0.35, 0), (0.35, 0), (0.35, 0.9), (0, 1.25), (-0.35, 0.9)], 0.08, loc=(x, 0.76, 3.6), color=WIN))
    # gate: arched pink door with gold rim (hinged, opens on the drop)
    parts.append(P.prism('gateRim', [(-1.25, 0), (1.25, 0), (1.25, 1.9), (0.9, 2.6), (0, 2.95), (-0.9, 2.6), (-1.25, 1.9)], 0.15, loc=(0, -0.05, 0), color=GOLD))
    door = P.prism('door', [(0, 0), (2.0, 0), (2.0, 1.75), (1.65, 2.35), (1.0, 2.6), (0, 2.6)], 0.12, loc=(-1.0, -0.15, 0), color=PINK)
    gate = P.pivot('gate', (-1.0, -0.15, 0), [door])
    hz = P.prism('gateHeart', P.heart(0.7, 10), 0.1, loc=(0, -0.2, 2.95), color=GOLD); parts.append(hz)
    # steps
    for i in range(4): parts.append(P.box(f'step{i}', (2.6 - i * 0.2, 0.55, 0.18), loc=(0, -0.6 - (3 - i) * 0.55, i * 0.18), color=PINK if i % 2 else '#FF8DC0'))
    # towers
    for name, x, y, r, h, rh in (('tL', -5.4, 0.5, 1.15, 6.0, 3.0), ('tR', 5.4, 0.5, 1.15, 6.0, 3.0), ('tBL', -3.0, 3.2, 0.95, 8.2, 2.8), ('tBR', 3.0, 3.2, 0.95, 8.2, 2.8), ('tC', 0, 4.4, 1.0, 10.5, 3.4)):
        p, f = tower(P, name, x, y, r, h, rh); parts += p; flags += f
    # banners on the wall
    for k, x in enumerate((-3.0, 3.0)):
        parts.append(P.prism(f'ban{k}', [(-0.45, 0), (0.45, 0), (0.45, 1.6), (0, 1.3), (-0.45, 1.6)][::-1], 0.05, loc=(x, -0.03, 1.2), color=PINK, rot=(0, 180, 0)))
    P.pivot('root', (0, 0, 0), parts + [gate] + flags)
