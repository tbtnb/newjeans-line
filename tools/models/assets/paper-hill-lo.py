"""P25 Faceted paper hill, low filler (v8: replaces the decimated LOD, which tore a star-shaped crater into the top).
Same twin-crest silhouette as paper-hill on a 10-sided ring grid; folded facets alternate mint / mint-green; pearl cut edge; no flowers."""
BUDGET = 110
import math, importlib.util, os
spec_ = importlib.util.spec_from_file_location('ph', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paper-hill.py'))
ph = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(ph)

def build(P, spec):
    c = spec['colors']; n = 10; verts = []
    def height(x, y):
        left = max(0, 1 - ((x + .30) ** 2 / .96 ** 2 + (y - .04) ** 2 / 1.05 ** 2) ** .72)
        right = max(0, 1 - ((x - .55) ** 2 / .58 ** 2 + (y + .02) ** 2 / .98 ** 2) ** .72) * .78
        return max(left, right)
    for k, r in enumerate([1, .62, .28]):
        for i in range(n):
            a = 2 * math.pi * (i + .5 * k) / n; rr = r * (1 + .06 * math.sin(5 * a)); x = rr * math.cos(a); y = rr * math.sin(a)
            z = .10 + .03 * math.sin(3 * a) if k == 0 else .10 + height(x, y) + .03 * math.sin(i * 2.7 + k * 1.1)
            verts.append((x * 2.6, y * 1.4, z * 2.8))
    verts.append((-.72, 0, 2.62)); faces = []
    for k in range(2):
        for i in range(n):
            j = (i + 1) % n; faces.extend([(k * n + i, k * n + j, (k + 1) * n + i), (k * n + j, (k + 1) * n + j, (k + 1) * n + i)])
    for i in range(n): faces.append((2 * n + i, 2 * n + (i + 1) % n, 3 * n))
    fold = P.mix(c['mint'], c['green'], .28)
    ob = ph.mesh(P, 'folded hillside lo', verts, faces, c['mint'])
    P.paint(ob, fold, faces={f for f in range(len(faces)) if f % 3 == 1})
    rim = [(verts[i][0], verts[i][1], 0) for i in range(n)] + [verts[i] for i in range(n)]
    ph.mesh(P, 'pearl paper cut edge', rim, [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)] + [tuple(reversed(range(n)))], c['pearl'])
    ph.finish(P, spec)
