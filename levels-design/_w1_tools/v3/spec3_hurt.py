import sys, math
sys.path.insert(0, '/workspace/nj-w1-work'); sys.path.insert(0, '/workspace/nj-w1-work/v3')
from speclib import *
from feat import *
import spec_hurt as S
P = S.P; bpm = 90.0; B = 0.6667
pier_color = P['navy']; arcade_colors = [P['ivory'], P['navy']]; arcade_texture = 'art/poster-frames.jpg'
collectibles = {'diamond': P['gold'], 'crown': P['gold']}
fork_taps = [25.0, 52.0, 105.0, 150.0]
arcades = [(10.927, 32.2, 'Portrait-frame gallery (one verse-1 lane runs through it)'), (117.594, 128.2, 'Quiet colonnade on the bridge')]
art = {'backdrop': 'art/sky.jpg', 'ground': {'src': 'art/ground-halftone.jpg', 'scale': 26},
       'files': {'sky.jpg': 'misty blue-grey morning sky', 'sky-dawn.jpg': 'dawn backdrop for the final chorus/outro (section backdrop)',
                 'ground-halftone.jpg': 'pale halftone ground', 'bunny-halftone-wall.jpg': 'halftone bunny wall (court landmark face)',
                 'poster-frames.jpg': 'five empty frames poster (arcade walls, billboards)', 'sticker-*.png': 'heart / star / bunny / drop / window decals'}}
sections = [
 {'t': 0, 'label': 'Intro', 'note': 'Sparse entrance, about one tap per bar on the intro chords; two long NE steps.'},
 {'t': 10.927, 'label': 'Verse 1', 'note': 'Frame switchbacks: long lanes on the held vocal lines, hairpins on the short syllable pairs; one lane runs through the portrait-frame gallery.', 'palette': {'fogEnd': 85}},
 {'t': 32.26, 'label': 'Pre-chorus 1', 'note': 'Paper staircase climbing NE (ramp +3.5); the unsent folded letter opens beside it.', 'palette': {'fogEnd': 110}},
 {'t': 42.927, 'label': 'Chorus 1', 'note': 'Three-leg staircase horseshoe around the quiet court and its halftone bunny wall; one fake fork.', 'palette': {'skyTop': '#BCD0E2'}},
 {'t': 64.26, 'label': 'Verse 2', 'note': 'Reed switchbacks heading back SW and passing OVER the verse-1 area (+3.5 above it).', 'palette': {'fogEnd': 90}},
 {'t': 80.26, 'label': 'Breath', 'note': 'Vocal-gap breath: one tap, long straight over still water.', 'palette': {'skyTop': '#D4E1EA', 'fogEnd': 130}},
 {'t': 85.594, 'label': 'Pre-chorus 2', 'note': 'Narrow paper corridor: short 2-3-tap zigzag (road 1.8).'},
 {'t': 96.26, 'label': 'Chorus 2', 'note': 'Ramp +4 onto the ear trestle: three-leg staircase U that crosses over the earlier route; five pixel bunnies under the trestle.', 'palette': {'skyTop': '#B4C8E0', 'ground': '#C8D9E6'}},
 {'t': 117.594, 'label': 'Bridge', 'note': 'Long quiet switchbacks through the colonnade, few bends.', 'palette': {'fogEnd': 140}},
 {'t': 128.26, 'label': 'Final chorus', 'note': 'Fall -4, then fan terraces: 2-4-tap zigzag steps; the frames open on alternating beats.', 'palette': {'skyTop': '#E2D3D3', 'skyBottom': '#F1E7E2'}, 'backdrop': 'art/sky-dawn.jpg'},
 {'t': 143.594, 'label': 'Outro', 'note': 'Long dawn staircase to the square quiet platform; frames stop moving.', 'palette': {'skyTop': '#F0DCCF', 'skyBottom': '#F7EEE6', 'light': '#FFE8D2'}},
]
camera = [{'t': 0, 'preset': 'iso', 'dist': 17, 'blend': 0}, {'t': 10.927, 'preset': 'high', 'dist': 19, 'blend': 2.5},
 {'t': 32.26, 'preset': 'side', 'yaw': -60, 'dist': 22, 'pitch': 35, 'blend': 3.0}, {'t': 42.927, 'preset': 'wide', 'dist': 24, 'blend': 2.0},
 {'t': 64.26, 'preset': 'high', 'dist': 21, 'blend': 2.5}, {'t': 80.26, 'preset': 'low', 'dist': 18, 'blend': 3.0},
 {'t': 85.594, 'preset': 'iso', 'dist': 17, 'blend': 2.0}, {'t': 96.26, 'preset': 'wide', 'dist': 25, 'blend': 2.0},
 {'t': 117.594, 'preset': 'side', 'yaw': 60, 'dist': 22, 'pitch': 30, 'blend': 3.0}, {'t': 128.26, 'preset': 'iso', 'dist': 20, 'blend': 2.0},
 {'t': 143.594, 'preset': 'wide', 'dist': 26, 'blend': 4.0}]
def objects(old):
    keep = [o for o in old if o.get('id') not in ('quiet-court', 'bunny-wall')]
    keep += stickers([(6.0, 'drop'), (18.0, 'heart'), (29.0, 'window'), (38.0, 'star'), (50.0, 'bunny'), (60.0, 'heart'), (72.0, 'drop'), (90.0, 'window'),
                      (104.0, 'star'), (112.0, 'bunny'), (122.0, 'drop'), (134.0, 'heart'), (148.0, 'star'), (158.0, 'bunny'), (166.0, 'heart')])
    keep += [{'id': f'frames-poster-{i}', 't': 45.0 + 7.0 * i, 'side': (-1) ** i * (5 + i), 'kind': 'image', 'src': 'art/poster-frames.jpg', 'size': [3, 0, 4], 'mode': 'billboard',
              'y': 0.5, 'appear': appear(42.927 + B * 2 * i, 'fade', 0.8)} for i in range(2)]
    return keep
def features(ctx):
    objs, evs, cams = [], [], []
    def court(sc):
        w = 16 * sc
        b = bunny_relief('x', 0, 0, P['cobalt'], P['ivory'], scale=0.8 * sc)
        return ([part('box', [0, -0.5, 0], [w, 1, w], P['ivory']), part('box', [0, 0.05, 0], [w - 3, 0.1, w - 3], '#D7E3EA')] +
                [dict(pp, pos=[pp['pos'][0], pp['pos'][1], pp['pos'][2] - w / 3]) for pp in b['parts']] +
                [part('box', [0, 3.5, -w / 3 - 0.6], [6 * sc, 6 * sc, 0.15], '#FFFFFF')], w * 0.7, 8, -0.5)
    o, sc = centered(ctx, 'chorus1-court-horseshoe', 'quiet-court', 'Quiet square court with the halftone bunny wall (chorus-1 horseshoe wraps it)', court, scales=(1.0, 0.75, 0.55, 0.4), appear=appear(41.5, 'rise', 1.5))
    if o:
        o['parts'][-1]['texture'] = 'art/bunny-halftone-wall.jpg'; objs.append(o)
        evs.append({'t': 42.927, 'type': 'pulse', 'target': 'quiet-court', 'every': B * 4, 'until': 64.0})
    return objs, evs, cams
def events(old):
    return [e for e in old if e.get('target') not in ('quiet-court', 'bunny-wall')]
chart_notes = open('/workspace/nj-w1-work/v3/hurt.notes.txt').read()
