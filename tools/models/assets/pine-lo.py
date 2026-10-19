"""pine-lo: low filler variant of P05 Folded Paper Pine (masses / far ring). size = P05 size_m; budget 150; pivots root.
Replaces the decimated LOD (DECIMATE collapse merged the teal / mint facets into a half-mint, half-teal split).
SIMPLIFICATIONS: three 10-sided folded cones (teal faces, every other fold a lighter teal), 5-sided trunk."""
def build(P, spec):
    c = spec['colors']; teal = c['teal']; lite = P.mix(c['teal'], c['mint'], 0.22) if hasattr(P, 'mix') else teal
    P.cyl('trunk', 0.16, 0.7, segs=5, color=c['wood'])
    for k, (r, z, h) in enumerate(((1.05, 0.55, 1.6), (0.82, 1.45, 1.45), (0.56, 2.35, 1.65))):
        o = P.cyl(f'tier{k}', r, h, segs=10, loc=(0, 0, z), color=teal, r2=0.0)
        P.paint(o, lite, faces={p.index for p in o.data.polygons if p.index % 2 == 1})
