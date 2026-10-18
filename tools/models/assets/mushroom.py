"""Ground cover: small faceted paper mushroom (<=60 tris)."""
BUDGET = 60
def build(P, spec):
    st = P.cyl('stem', 0.07, 0.16, 6, loc=(0, 0, 0), color='#F6E7C8', r2=0.06)
    cap = P.lathe('cap', [(0.0, 0.14), (0.2, 0.15), (0.17, 0.24), (0.0, 0.3)], 7, color='#FFA9C4', jitter=0.008)
    P.join([st, cap], 'mushroom')
