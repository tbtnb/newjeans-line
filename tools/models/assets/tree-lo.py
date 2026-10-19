"""tree-lo: low filler variant of P04 Round Paper Tree (masses / far ring). size = P04 size_m; budget 150; pivots root.
Replaces the decimated LOD (Blender DECIMATE collapse shattered the crown into loose shards and detached the roots).
SIMPLIFICATIONS: crown is a jittered subdiv-2 icosphere (80 facets), 6-sided trunk, 3 roots."""
import math, random

def build(P, spec):
    c = spec['colors']; random.seed(4)
    crown = P.ico('crown', 1.15, loc=(0, 0, 2.38), subdiv=2, color=c['mint'], scale=(1.0, 1.0, 0.95))
    for v in crown.data.vertices:   # paper facets: a little jitter, fuller underside
        v.co.x *= 1 + random.uniform(-0.06, 0.06); v.co.y *= 1 + random.uniform(-0.06, 0.06); v.co.z *= 1 + random.uniform(-0.04, 0.04)
        if v.co.z < 0: v.co.x *= 1.08; v.co.y *= 1.08
    crown.data.update()
    P.lathe('trunk', [(.20, 0), (.15, .45), (.14, 1.1), (.22, 1.55)], 6, color=c['wood'])
    for i in range(3):
        a = 2 * math.pi * i / 3 + 0.3
        P.prism('root', [(0.1, 0), (0.62, 0), (0.1, 0.42)], 0.16, loc=(0, 0, 0), color=c['wood'], rot=(0, 0, a))
