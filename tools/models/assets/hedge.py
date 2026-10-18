"""Engine-only kit piece (no design sheet): long papercraft flower hedge for the C 'big continuous masses' pass.
~6 m long, 1.1 m tall, 1.3 m deep: four overlapping faceted green lobes with blush / cream paper flowers on top; budget 560 tris.
SIMPLIFICATIONS: no sheet; palette from the tree sheet (green #6CCB5F, mint #BDEBD8, blush #FFC7DA) plus tulip-bed cream."""
BUDGET = 560

def build(P, spec):
    objs = []
    for i, (x, s) in enumerate(((-2.2, 0.95), (-0.75, 1.1), (0.75, 1.05), (2.2, 0.9))):
        objs.append(P.ico(f'lobe{i}', 1.0, loc=(x, 0, 0.5 * s), subdiv=1, color='#6CCB5F' if i % 2 else '#86D47A', scale=(1.0 * s, 0.65, 0.6 * s), jitter=0.06))
    cols = ['#FFC7DA', '#FFF6E8', '#F6A5C0']
    for k in range(11):
        x = -2.7 + k * 0.54; y = (-0.35, 0.1, 0.35)[k % 3]; z = 0.95 + 0.12 * ((k * 7) % 3) / 2
        objs.append(P.ico(f'flower{k}', 0.17, loc=(x, y, z), subdiv=0, color=cols[k % 3], scale=(1, 1, 0.7)))
    P.pivot('root', (0, 0, 0), objs)
