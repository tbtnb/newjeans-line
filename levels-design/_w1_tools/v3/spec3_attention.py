import sys, math
sys.path.insert(0, '/workspace/nj-w1-work')
from speclib import *
import spec_attention as S
bpm = 104.99
P = S.P
pier_color = P['denim']; arcade_colors = ['#F4F0DB', P['deep']]
collectibles = {'diamond': P['gold'], 'crown': P['gold']}
fork_taps = [25.9, 70.6, 124.5, 146.9]
arcades = [(98.8, 'Window arcade: the road runs through the gallery building'), (35.7, 'Roof-court passage')]
art = {'backdrop': 'art/sky.jpg', 'ground': {'src': 'art/ground-dots.jpg', 'scale': 40},
       'files': {'sky.jpg': 'soft summer sky backdrop with faint halftone dots', 'sky-dusk.jpg': 'warm outro sky (section backdrop)',
                 'ground-dots.jpg': 'ice-blue halftone ground tile', 'bunny-mural.jpg': '2022 EP bunny mural (cartoon bunny, no faces of people)',
                 'stadium-banner.jpg': 'coral/ivory stripe banner for the stadium stands', 'sticker-*.png': 'sticker decals lying beside the road'}}
B = 0.5714
sections = [
 {'t': 0, 'label': 'Intro', 'note': 'Sweep: two long straights and one big L on the sunny rooftop (L0).'},
 {'t': 9.607, 'label': 'Hook A', 'note': 'Staircase cluster NE on the bass entry, then a sawtooth zigzag (NE/NW legs every 4-5 taps) between roof blocks.', 'palette': {'skyTop': '#8DBCE4'}},
 {'t': 27.893, 'label': 'Verse 1', 'note': 'Switchbacks along the roof-court walls: lanes on the long vocal gaps, rungs on the short ones; narrow road 1.8; a roof-court passage wraps the road.', 'palette': {'fogEnd': 95}},
 {'t': 46.75, 'label': 'Pre-chorus 1', 'note': 'Sky bridge B1: one long SE staircase climbing +4 over the void.', 'palette': {'fogEnd': 130}},
 {'t': 62.18, 'label': 'Chorus 1', 'note': 'Rotating staircase that wraps the MV football pitch (SE -> SW -> NW legs); stands unfold; one fake fork ends in a broken edge.', 'palette': {'skyTop': '#7FB6E8', 'ground': '#BFE0D0'}},
 {'t': 83.32, 'label': 'Verse 2', 'note': 'Drop -4 at the end of chorus 1, then a square spiral that climbs +18 around the window clock tower (laps pass over each other), then switchbacks down the tower wall and through the window arcade.', 'palette': {'fogEnd': 100}},
 {'t': 101.6, 'label': 'Pre-chorus 2', 'note': 'Tight sawtooth corridor (legs of 3-4 taps), narrow road 1.7, ramping down -6; five amber windows easter egg.', 'palette': {'skyTop': '#A9C8EC', 'fogEnd': 140}},
 {'t': 117.03, 'label': 'Chorus 2', 'note': 'Drop -4, then a wide zigzag that passes OVER the hook and verse-1 roofs (multi-level crossings), terraces fan open.', 'palette': {'skyTop': '#78ACE6'}},
 {'t': 137.6, 'label': 'Final chorus', 'note': 'Staircase loop around the bunny relief (four diagonal legs) while climbing +6, crossing above the verse-1 switchbacks; 16th pairs on the snare fills.', 'palette': {'skyTop': '#5E8FD9', 'skyBottom': '#DCEBF7'}},
 {'t': 156.1, 'label': 'Outro', 'note': 'Drop -5 onto the cover square level, long release sweeps and a last pair of switchbacks into the deep-blue finish.', 'palette': {'skyTop': '#F2C9A8', 'skyBottom': '#FBEEDC', 'light': '#FFE3C4'}, 'backdrop': 'art/sky-dusk.jpg'},
]
camera = [{'t': 0, 'preset': 'iso', 'blend': 0, 'dist': 18},
 {'t': 9.607, 'preset': 'iso', 'blend': 1.5},
 {'t': 27.893, 'preset': 'iso', 'dist': 17, 'blend': 2.0},
 {'t': 46.75, 'preset': 'iso', 'dist': 22, 'pitch': 46, 'blend': 2.5},
 {'t': 62.18, 'preset': 'wide', 'dist': 26, 'blend': 1.2},
 {'t': 83.6, 'preset': 'side', 'yaw': 60, 'dist': 26, 'pitch': 40, 'blend': 1.5},
 {'t': 93.9, 'preset': 'iso', 'dist': 20, 'blend': 2.0},
 {'t': 101.6, 'preset': 'high', 'dist': 22, 'blend': 2.0},
 {'t': 117.03, 'preset': 'wide', 'dist': 25, 'blend': 1.2},
 {'t': 137.6, 'preset': 'high', 'dist': 24, 'blend': 1.5},
 {'t': 147.33, 'preset': 'iso', 'dist': 21, 'blend': 2.0},
 {'t': 156.1, 'preset': 'iso', 'dist': 19, 'blend': 2.5},
 {'t': 168.0, 'preset': 'wide', 'dist': 28, 'blend': 5.0}]
def objects(old):
    keep = []
    for o in old:
        if o.get('id') in ('stadium-pitch', 'cover-bunny-relief', 'b1-pillars'): continue
        keep.append(o)
    stickers = []
    for k, (t, n) in enumerate([(5.0, 'heart'), (14.5, 'star'), (31.0, 'bunny'), (52.0, 'heart'), (66.0, 'ball'), (88.0, 'window'), (108.0, 'window'),
                                (121.0, 'star'), (129.0, 'heart'), (142.0, 'bunny'), (152.0, 'ball'), (160.0, 'star'), (170.0, 'heart')]):
        stickers.append({'id': f'sticker-{k}', 't': t, 'side': (-1) ** k * 3.2, 'kind': 'image', 'src': f'art/sticker-{n}.png', 'size': [1.6, 0, 1.6], 'mode': 'flat', 'alpha': True})
    banners = [{'id': f'stand-banner-{i}', 't': 64.0 + 4.2 * i, 'side': 9.5, 'kind': 'image', 'src': 'art/stadium-banner.jpg', 'size': [6, 0, 2.2], 'mode': 'upright', 'y': 1.0,
                'appear': appear(62.18 + B * i, 'unfold', 0.6)} for i in range(4)]
    return keep + stickers + banners
def features(ctx):
    objs, evs, cams = [], [], []
    # window clock tower inside the verse-2 spiral
    m = ctx.move('verse2-spiral')
    top = m['ymax'] + 4; base = ctx.ylow - 6
    for r in (3.0, 2.4, 1.8, 1.3):
        p = ctx.find_clear(m['cx'], m['cz'], base, top, r, maxr=6)
        if p: break
    if p:
        h = top - base
        parts = [part('cylinder', [0, 0, 0], [2 * r, h, 2 * r], '#DCE7F4'), part('cone', [0, h, 0], [2 * r + 0.6, 2.2, 2 * r + 0.6], P['deep'])]
        parts += [part('box', [0, h - 3.0 - 1.4 * k, -r - 0.05], [0.9, 0.9, 0.12], P['gold']) for k in range(5)]
        parts += [part('disc', [0, h - 1.4, -r - 0.08], [1.6 * r, 0, 1.6 * r], '#FFFFFF')]
        objs.append({'id': 'window-clock-tower', 'kind': 'group', 'worldPos': [round(p[0], 2), round(base, 2), round(p[1], 2)], 'rot': 0, 'onroad': True,
                     'landmark': True, 'name': 'Window clock tower (the verse-2 spiral climbs around it)', 'parts': parts, 'radius': r,
                     'appear': appear(80.5, 'rise', 2.0), 'react': 'beat'})
        evs.append({'t': 83.39, 'type': 'light', 'target': 'window-clock-tower', 'level': 0.6, 'color': P['gold'], 'dur': 0.6, 'until': 93.5})
    # MV football pitch inside the chorus-1 wrap
    m = ctx.move('chorus1-wrap'); y = ctx.Y(m['t0'])
    for (w, d) in ((26, 16), (20, 13), (14, 9), (10, 7)):
        p = ctx.find_clear(m['cx'], m['cz'], y - 3, y + 1, math.hypot(w, d) / 2, maxr=14)
        if p: break
    if p:
        objs.append({'id': 'stadium-pitch', 'kind': 'group', 'worldPos': [round(p[0], 2), round(y - 0.4, 2), round(p[1], 2)], 'rot': 0, 'onroad': True, 'landmark': True,
                     'name': 'MV football pitch (chorus 1 staircase wraps it)', 'radius': math.hypot(w, d) / 2,
                     'parts': [part('box', [0, -0.5, 0], [w, 1.0, d], P['grass']), part('box', [0, 0.05, 0], [0.3, 0.05, d], '#FFFFFF'),
                               part('torus', [0, 0.05, 0], [d * 0.3, 0.2, d * 0.3], '#FFFFFF'), part('box', [-w / 2 + 0.3, 1.0, 0], [0.3, 2, d * 0.3], '#FFFFFF'),
                               part('box', [w / 2 - 0.3, 1.0, 0], [0.3, 2, d * 0.3], '#FFFFFF'), part('box', [0, -4, 0], [w, 7, d], P['denim'])],
                     'appear': appear(60.8, 'rise', 1.2)})
        evs.append({'t': 62.18, 'type': 'pulse', 'target': 'stadium-pitch', 'every': B * 2, 'until': 82.4})
    # bunny relief + mural at the centre of the final staircase loop
    m = ctx.move('final-loop'); y = ctx.Y(m['t0'])
    p = None
    for sc in (1.1, 0.9, 0.7, 0.5):
        p = ctx.find_clear(m['cx'], m['cz'], y - 2, y + 14 * sc, 8 * sc, maxr=10)
        if p: break
    if p:
        b = bunny_relief('cover-bunny-relief', None, 0, P['deep'], '#F7F6EE', scale=sc, landmark=True, name='M4 2022 EP cover bunny relief (final loop circles it)', appear=appear(137.6, 'rise', 2.0))
        b.pop('t'); b.pop('side'); b['worldPos'] = [round(p[0], 2), round(y - 1, 2), round(p[1], 2)]; b['rot'] = 45; b['onroad'] = True
        b['parts'].append({'kind': 'box', 'pos': [0, 2.2 * sc, 1.3 * sc], 'size': [8 * sc, 8 * sc, 0.15], 'color': '#FFFFFF', 'texture': 'art/bunny-mural.jpg'})
        objs.append(b)
        evs.append({'t': 137.6, 'type': 'pulse', 'target': 'cover-bunny-relief', 'every': B, 'until': 156.0})
    return objs, evs, cams
def events(old):
    out = [e for e in old if e.get('target') not in ('cover-bunny-relief', 'stadium-pitch')]
    out.append({'t': 156.26, 'type': 'burst', 'at': 'player', 'color': '#F4F0DB', 'amount': 30})
    return out
chart_notes = ('Attention 105 BPM (beat 0.5714 s, downbeat 0.464 s). 285 taps (legacy 139, 2.05x). Taps on measured accents: vocal syllables (demucs stem, -25.03 ms corrected), '
               'kick/snare/bass in hook and choruses; dotted vocal pickups are the motif. 8 two-tap 16th bursts (gap 0.151 s, i.e. 397 CPM) on real hi-hat/snare 16ths in fills '
               'and the final chorus (16th = 0.143 s at 105 BPM is below the 0.15 s schema floor, so these taps are nudged <= 9 ms). Engine judgment window ±68 ms in bursts, ±110 ms elsewhere.')
arcade_texture = 'art/window-wall.jpg'
