import sys, math
sys.path.insert(0, '/workspace/nj-w1-work'); sys.path.insert(0, '/workspace/nj-w1-work/v3')
from speclib import *
from feat import *
import spec_cookie as S
P = S.P; bpm = 157.0; B = 0.3822
pier_color = P['denim']; arcade_colors = [P['bench'], P['cobalt']]; arcade_texture = 'art/bunny-wall.jpg'
collectibles = {'diamond': P['gem'], 'crown': P['crown']}
fork_taps = [20.0, 60.0, 120.0, 170.0]
arcades = [(12.33, 36.7, 'Bench gallery (the verse-1 switchbacks pass under a black studio arch)'), (196.5, 207.9, 'Studio-flat hall of the dance break')]
art = {'backdrop': 'art/sky.jpg', 'ground': {'src': 'art/ground-studio.jpg', 'scale': 24},
       'files': {'sky.jpg': 'grey-blue studio sky with halftone dots', 'sky-violet.jpg': 'violet backdrop for the Jersey-club bridge (section backdrop)',
                 'ground-studio.jpg': 'periwinkle studio-floor stripes', 'poster-cd.jpg': 'CD poster with bunny (billboards around the chorus-1 horseshoe)',
                 'bunny-wall.jpg': 'cartoon bunny mural (arcade walls, bunny relief tower face)', 'sticker-*.png': 'cookie / CD / star / bunny / heart decals beside the road'}}
sections = [
 {'t': 0, 'label': 'Intro', 'note': 'Studio entrance: sparse taps on the kick/bass hits, two long sweeps between black flats.'},
 {'t': 12.33, 'label': 'Verse 1', 'note': 'Bench switchbacks: the long gaps become lanes along the five-seat bench wall, the short 8th pairs are the hairpins; passes under the bench-gallery arch.', 'palette': {'fogEnd': 90}},
 {'t': 36.79, 'label': 'Pre-chorus 1', 'note': 'Square spiral climbing around the folding stair tower (laps pass over each other) on the rising vocal phrase.', 'palette': {'fogEnd': 120}},
 {'t': 49.02, 'label': 'Chorus 1', 'note': 'Fall onto the open stage, then a three-leg staircase horseshoe (NE, SE, SW) around the 12-sided CD set piece; one fake fork.', 'palette': {'skyTop': '#5B78DE', 'skyBottom': '#C4CEF4'}},
 {'t': 73.48, 'label': 'Verse 2', 'note': 'Narrow sawtooth corridor (legs of 2-4 taps) - the bench motif compressed, road 1.8.', 'palette': {'fogEnd': 95}},
 {'t': 97.94, 'label': 'Pre-chorus 2', 'note': 'Second, steeper spiral climb (same vocal phrase as pre 1, same spiral texture).'},
 {'t': 110.17, 'label': 'Chorus 2', 'note': 'Four-leg staircase loop round the terrace (ramp +5), closing over its own start.', 'palette': {'skyTop': '#4E6CD8'}},
 {'t': 134.63, 'label': 'Jersey-club bridge', 'note': 'Fall -4, then a tight NE/NW zigzag corridor (legs 4-7) on the 3-3-2 club kicks; paired risers pulse on the kick.', 'palette': {'skyTop': P['violet'], 'skyBottom': '#D3CCF3', 'fogEnd': 85}, 'backdrop': 'art/sky-violet.jpg'},
 {'t': 159.09, 'label': 'Final chorus', 'note': 'One long sweeping staircase across the whole map (ramp +3) with the bunny relief tower on the skyline; one fake fork.', 'palette': {'skyTop': '#3E5FD6', 'skyBottom': '#D8DEF7'}},
 {'t': 183.55, 'label': 'Dance break', 'note': 'Choreography grid: sawtooth steps through rows of studio flats, then switchbacks through the studio-flat hall.', 'palette': {'skyTop': '#6F86D9'}},
 {'t': 208.01, 'label': 'Outro', 'note': 'Descending ramp (-6) to the quiet studio, long straights.', 'palette': {'skyTop': '#93A6E0', 'fogEnd': 140}},
]
camera = [{'t': 0, 'preset': 'iso', 'dist': 15, 'blend': 0}, {'t': 12.33, 'preset': 'high', 'dist': 17, 'blend': 2.0},
 {'t': 36.79, 'preset': 'side', 'yaw': -60, 'dist': 24, 'pitch': 40, 'blend': 2.0}, {'t': 49.02, 'preset': 'wide', 'dist': 24, 'blend': 1.0},
 {'t': 61.25, 'preset': 'iso', 'dist': 20, 'blend': 2.0}, {'t': 73.48, 'preset': 'high', 'dist': 17, 'blend': 2.0},
 {'t': 97.94, 'preset': 'side', 'yaw': 60, 'dist': 24, 'pitch': 40, 'blend': 2.0}, {'t': 110.17, 'preset': 'wide', 'dist': 25, 'blend': 1.0},
 {'t': 134.63, 'preset': 'high', 'dist': 16, 'blend': 1.0}, {'t': 152.97, 'preset': 'iso', 'dist': 19, 'blend': 2.0},
 {'t': 159.09, 'preset': 'wide', 'dist': 25, 'blend': 1.2}, {'t': 183.55, 'preset': 'high', 'dist': 20, 'blend': 2.0},
 {'t': 208.01, 'preset': 'iso', 'dist': 18, 'blend': 3.0}, {'t': 222.0, 'preset': 'wide', 'dist': 27, 'blend': 5.0}]
def objects(old):
    keep = [o for o in old if o.get('id') not in ('cd-set-piece', 'bunny-relief-wall', 'folding-stairs')]
    keep += stickers([(5.0, 'cookie'), (16.0, 'star'), (27.0, 'cd'), (33.0, 'bunny'), (45.0, 'cookie'), (66.0, 'heart'), (80.0, 'cd'), (92.0, 'cookie'),
                      (104.0, 'star'), (126.0, 'bunny'), (140.0, 'cd'), (151.0, 'heart'), (166.0, 'cookie'), (178.0, 'star'), (190.0, 'cd'), (214.0, 'bunny'), (225.0, 'cookie')])
    keep += [{'id': f'cd-poster-{i}', 't': 52.0 + 7.0 * i, 'side': (-1) ** i * (5 + i), 'kind': 'image', 'src': 'art/poster-cd.jpg', 'size': [3, 0, 4], 'mode': 'billboard',
              'y': 0.5, 'appear': appear(49.02 + B * 2 * i, 'pop', 0.4)} for i in range(3)]
    return keep
def features(ctx):
    objs, evs, cams = [], [], []
    def stair(sc):
        h = 14 * sc + 5
        return ([part('box', [0, h / 2, 0], [3 * sc, h, 3 * sc], P['ivory'])] +
                [part('box', [0, (k + 1) * h / 6, 1.6 * sc], [3 * sc, 0.4, 1.0], P['denim']) for k in range(5)], 2.6 * sc, h, -6)
    for mv, oid in (('pre1-stair-spiral', 'folding-stair-tower'), ('pre2-climb-spiral', 'folding-stair-tower-2')):
        o, sc = centered(ctx, mv, oid, 'Five-step folding stair tower (the pre-chorus spiral climbs around it)', stair, scales=(1.0, 0.7, 0.5, 0.35), appear=appear(ctx.move(mv)['t0'] - 1.5, 'unfold', 1.5))
        if o: objs.append(o)
    def cd(sc):
        R = 7 * sc
        return ([part('cylinder', [0, R + 0.5, 0], [2 * R, 0.6, 2 * R], '#CFE6FA', [90, 0, 0]), part('cylinder', [0, R + 0.5, -0.4], [R * 0.45, 0.7, R * 0.45], P['cobalt'], [90, 0, 0]),
                 part('box', [0, 0.25, 0], [2 * R, 0.5, 3], P['denim'])], R + 0.5, 2 * R + 1, -0.5)
    o, sc = centered(ctx, 'chorus1-cd-horseshoe', 'cd-set-piece', '12-sided graffiti CD set piece (chorus-1 horseshoe wraps it)', cd, scales=(1.0, 0.8, 0.6, 0.45), appear=appear(48.0, 'rise', 1.0))
    if o: objs.append(o); evs.append({'t': 49.02, 'type': 'spin', 'target': 'cd-set-piece', 'every': B * 4, 'until': 73.4})
    def terrace(sc):
        w = 16 * sc
        return ([part('box', [0, -0.6, 0], [w, 1.2, w], P['denim']), part('box', [0, 0.2, 0], [w - 4, 0.4, w - 4], P['peri'])] +
                [part('box', [-w / 3 + k * w / 6, 0.9, 0], [1.2, 1.0, 1.2], P['bench']) for k in range(5)], w * 0.7, 2, -0.5)
    o, sc = centered(ctx, 'chorus2-terrace-loop', 'terrace-bench', 'Terrace with the five-seat bench repeated (chorus-2 loop circles it)', terrace, scales=(1.0, 0.75, 0.55, 0.4), appear=appear(109.0, 'rise', 1.2))
    if o: objs.append(o)
    m = ctx.move('final-wide-L')
    def btower(sc):
        b = bunny_relief('x', 0, 0, P['cobalt'], P['ivory'], scale=1.25)
        return (b['parts'] + [part('box', [0, 7.2, 1.0], [8.5, 8.5, 0.15], '#FFFFFF')], 10, 22, 0)
    o = skyline(ctx, 'bunny-relief-wall', '2022 EP bunny relief tower (assembles at the final chorus)', btower, near=(m['cx'] + 35, m['cz']), rot=160, appear=appear(159.09, 'rise', 3.0))
    if o: o['parts'][-1]['texture'] = 'art/bunny-wall.jpg'; objs.append(o)
    return objs, evs, cams
def events(old):
    return [e for e in old if e.get('target') not in ('cd-set-piece',)]
chart_notes = open('/workspace/nj-w1-work/v3/cookie.notes.txt').read()
