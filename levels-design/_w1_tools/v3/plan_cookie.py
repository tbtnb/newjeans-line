from util import drop_after
start = 'N'; dur = 233.43
speed = [{'t': 0, 'v': 10.0}]
widths = [{'t': 0, 'w': 2.4}, {'t': 12.33, 'w': 2.1}, {'t': 36.79, 'w': 2.2}, {'t': 49.02, 'w': 2.2}, {'t': 73.48, 'w': 1.8},
          {'t': 97.94, 'w': 2.0}, {'t': 110.17, 'w': 2.1}, {'t': 134.63, 'w': 1.9}, {'t': 159.09, 'w': 2.1}, {'t': 183.55, 'w': 2.2}, {'t': 208.01, 'w': 2.4}]
def elev(T):
    return [drop_after(T, 48.3, dy=-4, need=0.5),
            {'type': 'ramp', 't0': 110.6, 't1': 133.8, 'dy': 5},
            drop_after(T, 134.2, dy=-4, need=0.45),
            {'type': 'ramp', 't0': 159.5, 't1': 182.5, 'dy': 3},
            {'type': 'ramp', 't0': 209.0, 't1': 229.0, 'dy': -6}]
def moves():
    return [
     dict(name='intro-sweep', kind='alt', t0=0),
     dict(name='verse1-bench-switchbacks', kind='lserp', t0=12.33, A0='E', P='N', thr=0.5, toward=(20, 150)),
     dict(name='pre1-stair-spiral', kind='lspiral', t0=36.79, turn='R', thr=0.5, rate=True, dys=[1.6, 2.0, 2.4]),
     dict(name='chorus1-cd-horseshoe', kind='zig', t0=49.02, diags=['NE', 'SE', 'SW'], every=21, everys=[21, 19, 23, 17], toward=(90, 120)),
     dict(name='verse2-narrow-zigzag', kind='zig', t0=73.48, diags=['SE', 'NE'], every=3, everys=[3, 4, 2], cycle=True, toward=(160, 140)),
     dict(name='pre2-climb-spiral', kind='lspiral', t0=97.94, turn='R', thr=0.5, rate=True, dys=[1.4, 1.8, 2.2]),
     dict(name='chorus2-terrace-loop', kind='zig', t0=110.17, diags=['NW', 'SW', 'SE', 'NE'], every=16, everys=[16, 15, 17, 14]),
     dict(name='bridge-jersey-zigzag', kind='zig', t0=134.63, diags=['NE', 'NW'], every=5, everys=[5, 6, 4, 7], cycle=True, toward=(60, 260)),
     dict(name='final-wide-L', kind='zig', t0=159.09, diags=['SW', 'SE'], every=34, everys=[34, 30, 38], toward=(0, 120)),
     dict(name='dancebreak-spiral', kind='lspiral', t0=183.55, turn='L', thr=0.5, rate=True, dys=[1.0, 1.3, 1.6], rt1=196.0),
     dict(name='dancebreak-switch', kind='lserp', t0=196.5, A0='W', P='S', thr=0.5),
     dict(name='outro-descent', kind='alt', t0=208.01),
    ]
