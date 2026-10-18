import math, sys
sys.path.insert(0, '/workspace/nj-w1-work')
from speclib import part, appear
def centered(ctx, move, oid, name, build, scales=(1.0, 0.8, 0.6, 0.45), y='start', maxr=12, landmark=True, egg=False, **kw):
    """Place a group at the clear centre of a route move (spiral, loop, U). build(scale) -> (parts, radius, height, y_off)."""
    m = ctx.move(move); yy = ctx.Y(m['t0']) if y == 'start' else ctx.ylow - 6 if y == 'ground' else y
    for sc in scales:
        parts, r, h, yo = build(sc)
        p = ctx.find_clear(m['cx'], m['cz'], yy + yo, yy + yo + h, r, maxr=maxr)
        if p:
            o = {'id': oid, 'kind': 'group', 'worldPos': [round(p[0], 2), round(yy + yo, 2), round(p[1], 2)], 'rot': kw.pop('rot', 0), 'onroad': True,
                 'name': name, 'parts': parts, 'radius': round(r, 2)}
            if landmark: o['landmark'] = True
            if egg: o['egg'] = True
            o.update(kw); return o, sc
    return None, None
def skyline(ctx, oid, name, build, near=(0, 0), maxr=60, **kw):
    parts, r, h, yo = build(1.0)
    p = ctx.find_clear(near[0], near[1], ctx.ylow - 6, 40, r, step=3, maxr=maxr)
    if not p: return None
    o = {'id': oid, 'kind': 'group', 'worldPos': [round(p[0], 2), round(ctx.ylow - 6, 2), round(p[1], 2)], 'rot': kw.pop('rot', 0), 'onroad': True, 'landmark': True,
         'name': name, 'parts': parts, 'radius': r}
    o.update(kw); return o
def stickers(items, src_prefix='art/sticker-', side=3.2, size=1.6):
    return [{'id': f'sticker-{k}', 't': t, 'side': (-1) ** k * side, 'kind': 'image', 'src': f'{src_prefix}{n}.png', 'size': [size, 0, size], 'mode': 'flat', 'alpha': True}
            for k, (t, n) in enumerate(items)]
