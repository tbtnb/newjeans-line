"""Engine-only kit piece (no design sheet): merged papercraft forest mass (C 'big continuous masses' pass) that reads as one solid
shape instead of a scatter of single trees. ~8 x 6 m footprint, ~5.5 m tall: seven faceted canopies of mixed size in mint/green
with a few blush accents and three short trunks; budget 640 tris.
SIMPLIFICATIONS: no sheet; palette from the round paper tree sheet."""
BUDGET = 640

def build(P, spec):
    objs = []
    C = [(-2.8, 0.4, 1.6, 1.5), (-1.0, -0.8, 2.0, 1.9), (1.0, 0.6, 2.2, 2.1), (2.9, -0.5, 1.7, 1.6), (0.0, 1.9, 1.5, 1.4), (-2.0, 2.0, 1.3, 1.2), (2.2, 2.2, 1.4, 1.3)]
    cols = ['#BDEBD8', '#6CCB5F', '#9EDFB8', '#7FD08A', '#BDEBD8', '#6CCB5F', '#A8E3C4']
    for i, (x, y, r, z) in enumerate(C):
        objs.append(P.ico(f'canopy{i}', r, loc=(x, y, z + r * 0.75), subdiv=1, color=cols[i], scale=(1, 1, 0.92), jitter=0.05))
        if i in (0, 2, 3): objs.append(P.cyl(f'trunk{i}', 0.22, z + 0.2, segs=5, loc=(x, y - r * 0.55, 0), color='#C99A6B', r2=0.16))
    for k, (x, y, z) in enumerate(((-1.2, -1.9, 3.6), (1.4, -1.0, 4.4), (3.2, -1.4, 3.0))):
        objs.append(P.ico(f'blossom{k}', 0.28, loc=(x, y, z), subdiv=0, color='#FFC7DA'))
    P.pivot('root', (0, 0, 0), objs)
