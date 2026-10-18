from util import drop_after
start = 'N'; dur = 175.01
speed = [{'t': 0, 'v': 8.0}]
widths = [{'t': 0, 'w': 2.3}, {'t': 10.927, 'w': 2.0}, {'t': 32.26, 'w': 2.2}, {'t': 42.927, 'w': 2.2}, {'t': 64.26, 'w': 1.9},
          {'t': 80.26, 'w': 2.4}, {'t': 85.594, 'w': 1.8}, {'t': 96.26, 'w': 2.1}, {'t': 117.594, 'w': 2.2}, {'t': 128.26, 'w': 1.9}, {'t': 143.594, 'w': 2.3}]
def elev(T):
    return [{'type': 'ramp', 't0': 32.6, 't1': 42.5, 'dy': 3.5},
            {'type': 'ramp', 't0': 96.6, 't1': 116.8, 'dy': 4},
            drop_after(T, 128.0, dy=-4, need=0.6)]
def moves():
    return [
     dict(name='intro-sweep', kind='alt', t0=0),
     dict(name='verse1-frame-switchbacks', kind='lserp', t0=10.927, A0='E', P='N', thr=1.2, toward=(40, 120)),
     dict(name='pre1-paper-stair', kind='stair', t0=32.26, diag='NE'),
     dict(name='chorus1-court-horseshoe', kind='zig', t0=42.927, diags=['NW', 'SW', 'SE'], every=6, everys=[6, 5, 7, 4]),
     dict(name='verse2-reed-switchbacks', kind='lserp', t0=64.26, A0='W', P='S', thr=1.2, toward=(10, 40)),
     dict(name='breath-straight', kind='alt', t0=80.26),
     dict(name='pre2-paper-corridor', kind='zig', t0=85.594, diags=['NE', 'SE'], every=2, everys=[2, 3], cycle=True),
     dict(name='chorus2-trestle-U', kind='zig', t0=96.26, diags=['NW', 'NE', 'SE'], every=6, everys=[6, 5, 7, 4], toward=(30, 170)),
     dict(name='bridge-quiet-switchbacks', kind='lserp', t0=117.594, A0='N', P='W', thr=1.0),
     dict(name='final-fan-terraces', kind='zig', t0=128.26, diags=['NW', 'NE'], every=3, everys=[3, 4, 2], cycle=True, toward=(30, 60)),
     dict(name='outro-long-steps', kind='stair', t0=143.594, diag='SE', toward=(40, 0)),
    ]
