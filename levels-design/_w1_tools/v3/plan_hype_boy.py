from util import drop_after
start = 'N'; dur = 176.64
speed = [{'t': 0, 'v': 9.0}]
widths = [{'t': 0, 'w': 2.3}, {'t': 19.452, 'w': 1.8}, {'t': 38.652, 'w': 2.1}, {'t': 53.052, 'w': 2.1}, {'t': 72.252, 'w': 2.0},
          {'t': 91.452, 'w': 2.0}, {'t': 115.452, 'w': 1.7}, {'t': 125.052, 'w': 2.0}, {'t': 129.852, 'w': 2.0}, {'t': 149.052, 'w': 1.9}, {'t': 170.652, 'w': 2.3}]
def elev(T):
    return [drop_after(T, 52.4, dy=-4),
            {'type': 'ramp', 't0': 73.0, 't1': 90.5, 'dy': 4},
            drop_after(T, 115.2, dy=-5),
            drop_after(T, 125.0, dy=3, typ='jump', need=0.5),
            {'type': 'ramp', 't0': 130.2, 't1': 148.6, 'dy': 3},
            {'type': 'ramp', 't0': 149.4, 't1': 169.8, 'dy': 6}]
def moves():
    return [
     dict(name='intro-steps', kind='stair', t0=0, diag='NE'),
     dict(name='intro-sweep', kind='alt', t0=12.0),
     dict(name='verse1-locker-zigzag', kind='zig', t0=19.452, diags=['NW', 'NE'], every=3, everys=[3, 4, 2], cycle=True, toward=(30, 120)),
     dict(name='pre1-diving-spiral', kind='lspiral', t0=38.652, turn='L', thr=0.5, rate=True, dys=[1.3, 1.6, 2.0]),
     dict(name='build1-run', kind='stair', t0=48.252, diag='SE'),
     dict(name='chorus1-pool-U', kind='zig', t0=53.052, diags=['SE', 'NE', 'NW'], every=13, everys=[13, 12, 14, 11], toward=(110, 140)),
     dict(name='post1-switchbacks', kind='lserp', t0=72.252, A0='E', P='S', thr=0.42, toward=(120, 60)),
     dict(name='verse2-court-loop', kind='zig', t0=91.452, diags=['SW', 'NW', 'NE', 'SE'], every=10, everys=[10, 11, 9, 12, 8, 13, 14], toward=(80, 80)),
     dict(name='pre2-phone-corridor', kind='zig', t0=115.452, diags=['SW', 'SE'], every=2, everys=[2, 3, 4], cycle=True),
     dict(name='build2-jump', kind='alt', t0=125.052),
     dict(name='chorus2-overpass-stair', kind='stair', t0=129.852, diag='NW', toward=(20, 110)),
     dict(name='final-spiral-stair', kind='zig', t0=149.052, diags=['NE', 'SE', 'SW', 'NW', 'NE'], every=11, everys=[11, 10, 12, 9], toward=(40, 140)),
     dict(name='outro', kind='alt', t0=170.6),
    ]
