import sys, math
sys.path.insert(0, '/workspace/nj-w1-work'); sys.path.insert(0, '/workspace/nj-w1-work/v3')
from speclib import *
from feat import *
import spec_hype_boy as S
bpm = 100.0; P = S.P; B = 0.6
pier_color = P['cobalt']; arcade_colors = [P['aqua'], P['cobalt']]; arcade_texture = 'art/lockers.jpg'
collectibles = {'diamond': P['gold'], 'crown': P['gold']}
fork_taps = [31.0, 64.2, 101.3, 160.0]
arcades = [(19.45, 38.6, 'Locker canyon passage (road runs between the locker walls)'), (72.3, 91.4, 'Sports-hall gate')]
art = {'backdrop': 'art/sky.jpg', 'ground': {'src': 'art/ground-pooltile.jpg', 'scale': 30},
       'files': {'sky.jpg': 'summer pool sky', 'sky-lilac.jpg': 'lilac sky for chorus 2 / final (section backdrop)', 'ground-pooltile.jpg': 'aqua pool-tile ground',
                 'lockers.jpg': 'locker-door texture for the canyon arcade', 'poster-pool.jpg': 'pool poster with bunny', 'sticker-*.png': 'sticker decals beside the road'}}
sections = [
 {'t': 0, 'label': 'Intro riff', 'note': 'Beat-stepped NE staircase on the synth riff (one tap per beat), then two long sweeps over the start deck.'},
 {'t': 19.452, 'label': 'Verse 1', 'note': 'Locker canyon: tight sawtooth zigzag (legs of 2-4 taps) on the dembow syncopation, narrow road 1.8, the road passes through a locker passage.', 'palette': {'fogEnd': 90}},
 {'t': 38.652, 'label': 'Pre-chorus 1', 'note': 'Square spiral (L) climbing +12 around the diving tower; the laps pass over each other.', 'palette': {'fogEnd': 130}},
 {'t': 48.252, 'label': 'Build 1', 'note': 'Short SE staircase run off the tower top; fall -4 onto the pool deck right before the chorus.'},
 {'t': 53.052, 'label': 'Chorus 1', 'note': 'Open U of staircases around the summer pool (three diagonal legs); five-colour pillars answer the vocal; one fake fork.', 'palette': {'skyTop': '#86C3EA', 'ground': '#BFE6EE'}},
 {'t': 72.252, 'label': 'Post-chorus 1', 'note': 'Switchbacks down the bridge (lanes on the longer gaps), climbing +4; the sports-hall gate wraps one lane.'},
 {'t': 91.452, 'label': 'Verse 2', 'note': 'Diamond staircase loop around the sports court (four legs); the road closes the loop at a different height.', 'palette': {'fogEnd': 110}},
 {'t': 115.452, 'label': 'Pre-chorus 2', 'note': 'Fall -5 into the phone patio: a tight 2-tap zigzag corridor between phone screens (road 1.7); E1 flip phone.', 'palette': {'fogEnd': 85, 'skyTop': '#A9CBE8'}},
 {'t': 125.052, 'label': 'Build 2', 'note': 'Jump +3 onto the bridge deck B2, sparse build taps.'},
 {'t': 129.852, 'label': 'Chorus 2', 'note': 'One long sweeping NE staircase over the whole map (ramp +3) - the longest diagonal of the level.', 'palette': {'skyTop': '#B9B8EE', 'ground': P['lilac']}, 'backdrop': 'art/sky-lilac.jpg'},
 {'t': 149.052, 'label': 'Final chorus', 'note': 'Spiral staircase: five diagonal legs rotating around the five-colour pillar ring while climbing +6, crossing over its own start.', 'palette': {'skyTop': '#C8C3F0', 'skyBottom': '#F5F2FB'}},
 {'t': 170.652, 'label': 'Outro', 'note': 'Calm straight to the finish deck, little white bunny echo.', 'palette': {'skyTop': '#AFC9EE'}},
]
camera = [{'t': 0, 'preset': 'iso', 'dist': 18, 'blend': 0}, {'t': 19.452, 'preset': 'high', 'dist': 18, 'blend': 1.5},
 {'t': 38.652, 'preset': 'side', 'yaw': -60, 'dist': 24, 'pitch': 40, 'blend': 2.0}, {'t': 48.252, 'preset': 'iso', 'dist': 20, 'blend': 1.5},
 {'t': 53.052, 'preset': 'wide', 'dist': 25, 'blend': 1.0}, {'t': 62.652, 'preset': 'iso', 'dist': 21, 'blend': 2.0},
 {'t': 72.252, 'preset': 'iso', 'dist': 19, 'blend': 2.0}, {'t': 91.452, 'preset': 'high', 'dist': 22, 'blend': 2.0},
 {'t': 115.452, 'preset': 'high', 'dist': 17, 'blend': 1.5}, {'t': 125.052, 'preset': 'low', 'dist': 18, 'blend': 2.0},
 {'t': 129.852, 'preset': 'wide', 'dist': 25, 'blend': 1.2}, {'t': 149.052, 'preset': 'high', 'dist': 24, 'blend': 1.5},
 {'t': 158.652, 'preset': 'iso', 'dist': 21, 'blend': 2.0}, {'t': 170.652, 'preset': 'wide', 'dist': 28, 'blend': 4.0}]
def objects(old):
    keep = [o for o in old if o.get('id') not in ('pool', 'sports-court', 'cover-bunny-tower', 'b1-bridge-piers', 'b2-deck-piers')]
    keep += stickers([(4.0, 'heart'), (13.0, 'star'), (24.0, 'ball'), (33.0, 'bunny'), (45.0, 'star'), (58.0, 'heart'), (69.0, 'ball'), (80.0, 'bunny'),
                      (96.0, 'ball'), (108.0, 'star'), (119.0, 'phone'), (135.0, 'heart'), (143.0, 'bunny'), (155.0, 'star'), (165.0, 'heart')])
    keep += [{'id': f'pool-poster-{i}', 't': 55.0 + 6.5 * i, 'side': -(4.5 + i), 'kind': 'image', 'src': 'art/poster-pool.jpg', 'size': [3, 0, 4], 'mode': 'billboard',
              'y': 0.5, 'appear': appear(53.052 + B * i, 'pop', 0.4)} for i in range(3)]
    return keep
def features(ctx):
    objs, evs, cams = [], [], []
    def tower(sc):
        h = 15 * sc + 6
        return ([part('box', [0, h / 2, 0], [2.4 * sc, h, 2.4 * sc], P['ivory']), part('box', [1.8 * sc, h - 0.2, 0], [3.6 * sc, 0.3, 1.1], P['ivory']),
                 part('box', [0, h / 2, 0], [2.6 * sc, 0.6, 2.6 * sc], P['aqua']), part('cylinder', [0, 0.1, 0], [6 * sc, 0.2, 6 * sc], P['aqua'])], 3 * sc, h, -6)
    o, sc = centered(ctx, 'pre1-diving-spiral', 'diving-tower', 'Diving tower (the pre-chorus spiral climbs around it)', tower, scales=(1.0, 0.7, 0.5, 0.35), appear=appear(36.0, 'rise', 1.5), react='beat')
    if o: objs.append(o)
    def pool(sc):
        w, d = 20 * sc, 13 * sc
        return ([part('box', [0, -0.6, 0], [w, 1.2, d], P['ivory']), part('water', [0, -0.05, 0], [w - 3, 0.2, d - 3], P['aqua']),
                 part('box', [w / 2 - 1.5, 0.6, 0], [3, 0.3, 1.2], P['ivory']), part('box', [0, -4, 0], [w, 6, d], P['cobalt'])], math.hypot(w, d) / 2, 2, -0.5)
    o, sc = centered(ctx, 'chorus1-pool-U', 'pool', 'Summer pool + low diving board (chorus 1 U wraps it)', pool, scales=(1.0, 0.8, 0.6, 0.45, 0.35), appear=appear(51.5, 'unfold', 1.5))
    if o: objs.append(o); evs.append({'t': 53.052, 'type': 'pulse', 'target': 'pool', 'every': B * 2, 'until': 72.0})
    def court(sc):
        w, d = 18 * sc, 12 * sc
        return ([part('box', [0, -0.5, 0], [w, 1, d], '#6F8FE0'), part('box', [w / 4, -0.45, 0], [w / 2, 1, d], '#F2A6A6'), part('box', [0, 0.05, 0], [0.2, 0.05, d], '#FFFFFF'),
                 part('box', [w / 2 - 0.5, 1.2, 0], [0.3, 2.4, d / 3], '#E04848'), part('sphere', [-w / 6, 0.6, d / 6], [1, 1, 1], P['gold']),
                 part('box', [0, -4, 0], [w, 6, d], P['cobalt'])], math.hypot(w, d) / 2, 3, -0.5)
    o, sc = centered(ctx, 'verse2-court-loop', 'sports-court', 'MV sports court, red-white goal, yellow basketball (verse-2 loop circles it)', court, scales=(1.0, 0.8, 0.6, 0.45, 0.35), appear=appear(89.5, 'rise', 1.2))
    if o: objs.append(o)
    cols = ['#FF7185', '#F8CB56', '#57CDD1', '#8FA2F0', '#F4F1E8']
    def ring(sc):
        R = 4.5 * sc
        return ([part('box', [R * math.cos(2 * math.pi * k / 5), 2, R * math.sin(2 * math.pi * k / 5)], [1.6, 4, 1.6], c) for k, c in enumerate(cols)] +
                [part('cylinder', [0, 0, 0], [2 * R + 2, 0.3, 2 * R + 2], P['lilac'])], R + 1.2, 4.5, -0.3)
    o, sc = centered(ctx, 'final-spiral-stair', 'five-pillar-ring', 'Five-colour dance pillar ring (final spiral staircase rotates around it)', ring, scales=(1.0, 0.75, 0.5), appear=appear(148.0, 'rise', 1.0), react='beat')
    if o: objs.append(o); evs.append({'t': 149.052, 'type': 'light', 'target': 'five-pillar-ring', 'level': 0.7, 'every': B, 'until': 170.0})
    m = ctx.move('chorus1-pool-U')
    def btower(sc):
        b = bunny_relief('x', 0, 0, P['cobalt'], P['ivory'], scale=1.2)
        return (b['parts'] + [part('box', [0, 7.2, 1.0], [8.5, 8.5, 0.15], '#FFFFFF')], 10, 22, 0)
    o = skyline(ctx, 'cover-bunny-tower', '2022 EP cover bunny relief tower (skyline, seen from chorus 1, verse 2 and the final chorus)', btower, near=(m['cx'] - 40, m['cz'] + 10), rot=200, appear=appear(48.252, 'rise', 2.0))
    if o:
        o['parts'][-1]['texture'] = 'art/poster-pool.jpg'; objs.append(o)
    return objs, evs, cams
def events(old):
    return [e for e in old if e.get('target') not in ('b2-deck-piers', 'dance-pillar-0', 'sports-court')] + [{'t': 91.452, 'type': 'raise', 'target': 'sports-court', 'dur': 1.0}]
chart_notes = open('/workspace/nj-w1-work/v3/hype-boy.notes.txt').read()
