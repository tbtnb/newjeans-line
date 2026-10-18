"""Ground cover: paper grass tuft (5 folded blades, <=24 tris)."""
BUDGET = 24
def build(P, spec):
    import math
    cols = ['#9ACB8E', '#86BC7C', '#AED7A0']
    bl = []
    for i in range(5):
        a = 2 * math.pi * i / 5 + P._rng.uniform(-0.3, 0.3); r = 0.07
        bl.append(P.blade(f'b{i}', 0.16, P._rng.uniform(0.32, 0.5), loc=(r * math.cos(a), r * math.sin(a), 0), color=cols[i % 3], rot=(P._rng.uniform(-12, 12), 0, math.degrees(a) + 90), bend=0.25))
    P.join(bl, 'grass')
