import json
def taps(slug):
    c = json.load(open(f'/workspace/newjeans-line-designs/{slug}/chart.json'))
    tt = json.load(open(f'/workspace/nj-w1-work/v3/{slug}.taps16.json'))
    c['taps'] = tt
    return c, [t['t'] for t in tt]
def drop_after(T, t, need=0.55, off=0.06, dy=-3, typ='fall'):
    """fall/jump placed just after the first tap at/after t that is followed by a gap >= need (air-time rule >=0.35 s)."""
    for a, b in zip(T, T[1:]):
        if a >= t - 1e-6 and b - a >= need: return {'type': typ, 't': round(a + off, 3), 'dy': dy}
    raise ValueError(f'no gap for drop after {t}')
