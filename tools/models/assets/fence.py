"""Engine-only kit piece (no design sheet): papercraft picket fence segment for the C density pass (village / meadow zones).
1.6 m long, 0.8 m tall: six pointed cream pickets with pink rims on two pink rails; budget 160 tris. Front is -Y.
SIMPLIFICATIONS: no sheet to match; palette taken from the tulip-bed sheet fence (cream #FFF6E8, pink #F6A5C0 / #F7B8CF)."""
BUDGET = 160

def build(P, spec):
    objs = []
    L, H, n = 1.6, 0.8, 6
    pk = [(-0.06, 0.0), (0.06, 0.0), (0.06, H - 0.1), (0.0, H), (-0.06, H - 0.1)]
    for i in range(n):
        x = -L / 2 + 0.1 + i * (L - 0.2) / (n - 1)
        objs.append(P.prism(f'picket{i}', pk, 0.04, loc=(x, 0, 0), color='#FFF6E8', side_color='#F6A5C0'))
    for k, z in enumerate((0.22, 0.55)):
        objs.append(P.box(f'rail{k}', (L, 0.035, 0.07), loc=(0, 0.04, z), color='#F7B8CF', base=False))
    P.pivot('root', (0, 0, 0), objs)
