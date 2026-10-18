"""P04 圆冠纸树 Round paper tree (z01/z02/z04/z06/z10 mid layer, thin-instanced) - built to the three-view sheet
levels-design/omg/redesign-v3/C/assets/P04_paper_tree_round: 2 x 2 x 3.5 m, budget 600 tris. Faceted geodesic crown
(per-facet mint tones), six-sided kraft trunk with four folded root flares. Pivot root = trunk base ('pops upright' every 4 bars)."""
BUDGET = 600
MINT, MINT2, MINT3, WOOD, WOOD2 = '#BDEBD8', '#A9DEC8', '#D2F3E5', '#D8A86E', '#C99A6B'

def build(P, spec):
    S = spec.get('size_m', {}); H = S.get('h', 3.5); W = S.get('w', 2.0)
    r = W / 2 * 0.98
    tone = lambda c, n: [MINT, MINT2, MINT3][int(abs(c.x * 7.1 + c.y * 3.3 + c.z * 5.7) * 3) % 3]
    crown = P.ico('crown', r, loc=(0, 0, H - r * 0.98), color=tone, subdiv=2, scale=(1, 1, 0.98), jitter=0.03)
    trunk = P.cyl('trunk', 0.2, H - 2 * r + 0.55, 6, loc=(0, 0, 0.25), r2=0.14, color=lambda c, n: WOOD if n.x + n.y < 0 else WOOD2)
    base = P.cyl('flare', 0.32, 0.3, 6, loc=(0, 0, 0), r2=0.2, color=WOOD2)
    roots = []
    for k in range(4):
        roots.append(P.prism(f'root{k}', [(0.1, 0), (0.85, 0), (0.1, 0.6)], 0.26, loc=(0, 0, 0), color=WOOD, rot=(0, 0, 45 + k * 90)))
    P.pivot('root', (0, 0, 0), [crown, trunk, base] + roots)
