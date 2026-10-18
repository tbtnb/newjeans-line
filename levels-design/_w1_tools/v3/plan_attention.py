from util import drop_after
start = 'N'; dur = 178.05
speed = [{'t': 0, 'v': 9.0}]
widths = [{'t': 0, 'w': 2.3}, {'t': 9.607, 'w': 2.1}, {'t': 27.893, 'w': 1.8}, {'t': 46.75, 'w': 2.1}, {'t': 62.18, 'w': 2.0},
          {'t': 83.32, 'w': 2.0}, {'t': 101.6, 'w': 1.7}, {'t': 117.03, 'w': 1.9}, {'t': 137.6, 'w': 1.9}, {'t': 156.1, 'w': 2.2}]
def elev(T):
    return [{'type': 'ramp', 't0': 47.7, 't1': 61.8, 'dy': 4},
            drop_after(T, 82.4, dy=-4),
            {'type': 'ramp', 't0': 103.2, 't1': 116.6, 'dy': -6},
            drop_after(T, 117.0, dy=-4),
            {'type': 'ramp', 't0': 138.0, 't1': 155.5, 'dy': 6}, drop_after(T, 156.0, dy=-5)]
def moves():
    return [
     dict(name='intro', kind='alt', t0=0),
     dict(name='hookA-stair', kind='stair', t0=9.607, diag='NE'),
     dict(name='hookA-zig', kind='zig', t0=18.75, diags=['NE', 'NW'], every=4, everys=[4, 3, 5], cycle=True, toward=(40, 130)),
     dict(name='verse1-switchback', kind='lserp', t0=27.893, A0='E', P='N', thr=0.8, toward=(60, 210)),
     dict(name='pre1-skybridge', kind='stair', t0=46.6, diag='SE', toward=(150, 160)),
     dict(name='chorus1-wrap', kind='zig', t0=62.18, diags=['SE', 'SW', 'NW'], every=12, everys=[12, 10, 14, 16], toward=(130, 90)),
     dict(name='verse2-spiral', kind='lspiral', t0=83.32, turn='R', thr=0.5, rate=True, dys=[1.8, 2.1], rt1=93.5),
     dict(name='verse2-wall', kind='lserp', t0=93.9, A0='W', P='S', thr=0.8, toward=(110, 40)),
     dict(name='pre2-sawtooth', kind='zig', t0=101.6, diags=['NW', 'SW'], every=3, everys=[3, 4, 2], cycle=True, toward=(40, 40)),
     dict(name='chorus2-zigzag', kind='zig', t0=117.03, diags=['NW', 'NE'], every=8, everys=[8, 7, 10], cycle=True, toward=(0, 130)),
     dict(name='final-loop', kind='zig', t0=137.6, diags=['NW', 'SW', 'SE', 'NE'], every=11, everys=[11, 10, 12, 9], toward=(-20, 160)),
     dict(name='outro-sweep', kind='alt', t0=156.1, toward=(-30, 220)),
     dict(name='outro-switch', kind='lserp', t0=163.8, A0='E', P='N', thr=1.0, toward=(0, 250)),
    ]
