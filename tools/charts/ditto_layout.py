"""Ditto map: a winter-memory journey recorded on a camcorder (MV: snowy school, gym, frozen lake, 'Banhee' filming).
Section structure follows the chart; see docs/design/levels/ditto.md."""
from layoutkit import Layout
L = Layout('ditto'); T = L.T
d = L.d
d['palette'] = {'skyTop': '#b9cde0', 'skyBottom': '#eef1f4', 'fog': '#e9edf1', 'fogStart': 35, 'fogEnd': 110, 'ground': '#d5dee8', 'groundY': -5,
                'road': '#ffffff', 'roadSide': '#8ea2b9', 'line': '#2f4f7a', 'light': '#fff8ee', 'lightIntensity': 1.0, 'ambient': '#c3cfdc', 'particles': 'snow'}

# ---------- sections: environment progression ----------
L.section(0, 'Intro 雪原')
L.section(T(8), 'Hook 雪林', palette={'skyTop': '#a9c2da', 'ground': '#cbd7e2', 'roadSide': '#8399b0'})
L.section(T(16), 'Verse 校舍', palette={'skyTop': '#c9d6e3', 'skyBottom': '#f5f1ea', 'road': '#fbfaf7', 'roadSide': '#c7bba8', 'ground': '#efece6', 'line': '#334d7a'})
L.section(T(24), 'Verse b 走廊', palette={'skyTop': '#d7dbe2', 'roadSide': '#b9b0a2'})
L.section(T(31), 'Pre 体育馆', palette={'skyTop': '#e8d7c2', 'skyBottom': '#f7efe3', 'fog': '#f3e9dc', 'road': '#e6b97e', 'roadSide': '#a8743f', 'ground': '#d9c3a2', 'groundY': -3, 'line': '#2a3f6a', 'particles': 'dust'})
L.section(T(40), 'Chorus 雪桥', palette={'skyTop': '#9fbfe0', 'skyBottom': '#eaf1f7', 'fog': '#e4edf5', 'road': '#ffffff', 'roadSide': '#9db3c9', 'ground': '#d3dfea', 'groundY': -16, 'line': '#24497d', 'particles': 'snow'})
L.section(T(48), 'Post 广场', palette={'skyTop': '#a7b9e6', 'skyBottom': '#f2eef6', 'roadSide': '#a6a9d1', 'groundY': -8})
L.section(T(64), 'Bridge 冰湖', palette={'skyTop': '#5d6f99', 'skyBottom': '#a9b9d1', 'fog': '#9fb0c9', 'fogStart': 25, 'fogEnd': 90, 'ground': '#9fb8cf', 'groundY': -2.5, 'road': '#e9f1f8', 'roadSide': '#7f98b3', 'line': '#f2f6ff', 'light': '#cdd9ff', 'lightIntensity': 0.7, 'ambient': '#7d8db0'})
L.section(T(71), 'Break 夜', palette={'skyTop': '#1d2440', 'skyBottom': '#4a557a', 'fog': '#3e4868', 'fogStart': 18, 'fogEnd': 70, 'ground': '#3c4a6b', 'groundY': -6, 'road': '#dfe8ff', 'roadSide': '#55648c', 'line': '#ffffff', 'lightIntensity': 0.55, 'ambient': '#56628a', 'particles': 'stars'})
L.section(T(79), 'Final 黎明', palette={'skyTop': '#8fa6d8', 'skyBottom': '#ffd9cf', 'fog': '#f6d9d6', 'fogStart': 30, 'fogEnd': 110, 'ground': '#c9d6ea', 'groundY': -6, 'road': '#ffffff', 'roadSide': '#d3a9b8', 'line': '#3a3f80', 'light': '#fff0e0', 'lightIntensity': 1.05, 'ambient': '#c9b9cf', 'particles': 'snow'})
L.section(T(96), 'Outro 光', palette={'skyTop': '#f3e6ee', 'skyBottom': '#fffaf2', 'fog': '#fff6ef', 'roadSide': '#e2c7cf', 'line': '#4b4f8f', 'particles': 'dust'})

# ---------- road: narrows across the level; reveal style per section ----------
for bar, w in [(0, 2.6), (8, 2.3), (16, 2.1), (31, 2.3), (40, 1.9), (64, 2.1), (79, 1.75), (96, 2.4)]: L.width(T(bar) if bar else 0, w)
L.reveal(0, 'rise', 2.4); L.reveal(T(8), 'static'); L.reveal(T(31), 'unfold', 2.0); L.reveal(T(40), 'drop', 1.9)
L.reveal(T(48), 'static'); L.reveal(T(64), 'fade', 2.0); L.reveal(T(79), 'rise', 1.6); L.reveal(T(96), 'rise', 2.2)

# ---------- elevation: falls into the gym and onto the lake; ascent at dawn ----------
a, b = L.gap_after(T(31), 1.0); d['elevation'].append({'t': round(a + 0.12, 3), 'type': 'fall', 'dy': -3})      # step down into the gym
a, b = L.gap_after(T(71), 1.2); d['elevation'].append({'t': round(a + 0.15, 3), 'type': 'fall', 'dy': -4})      # drop to the night lake
d['elevation'].append({'t0': T(79), 't1': T(95), 'type': 'ramp', 'dy': 7})                                       # climb towards dawn
d['elevation'].append({'t0': T(97), 't1': T(102), 'type': 'ramp', 'dy': 3})

# ---------- camera: phrase-level changes ----------
L.cam(0, preset='wide', blend=0); L.cam(T(4), preset='iso', blend=4.5)
L.cam(T(16), preset='iso', yaw=-18, blend=2.0)
L.cam(T(24), preset='side', yaw=55, blend=2.5)
L.cam(T(31), preset='low', blend=2.0)
L.cam(T(39), preset='iso', pitch=58, dist=24, blend=1.2)
L.cam(T(44), preset='iso', yaw=22, blend=2.0)
L.cam(T(48), preset='iso', yaw=-25, blend=2.5); L.cam(T(52), yaw=25, blend=2.5); L.cam(T(56), preset='high', blend=2.5); L.cam(T(60), preset='iso', yaw=-20, blend=2.0)
L.cam(T(64), preset='top', blend=3.0)
L.cam(T(71), preset='close', yaw=35, blend=2.5)
L.cam(T(77), preset='iso', blend=2.5)
L.cam(T(79), preset='iso', pitch=46, yaw=-15, blend=1.0); L.cam(T(87), yaw=20, blend=2.0); L.cam(T(91), preset='high', blend=2.0)
L.cam(T(96), preset='wide', blend=4.0)

# ---------- scenery ----------
# Intro: snowfield, Banhee's camcorder (landmark), sparse pines, snow drifts
L.obj(id='camcorder', t=2.0, side=-9, kind='group', landmark=True, name='Banhee 的摄像机', react='beat', parts=[
    {'kind': 'box', 'pos': [0, 0, 0], 'size': [3.2, 3.0, 5.0], 'color': '#3b3f4a'},
    {'kind': 'cylinder', 'pos': [0, 1.0, -3.0], 'size': [2.2, 1.6, 2.2], 'rot': [90, 0, 0], 'color': '#23262d'},
    {'kind': 'disc', 'pos': [0, 1.5, -3.85], 'size': [1.6, 0, 1.6], 'rot': [-90, 0, 0], 'color': '#7fa7d9'},
    {'kind': 'sphere', 'pos': [1.1, 3.0, 1.6], 'size': [0.5, 0.5, 0.5], 'color': '#ff3b3b'},
    {'kind': 'box', 'pos': [-1.9, 1.0, 0.5], 'size': [0.4, 2.0, 3.0], 'color': '#5d6370'}])
L.scatter(0, T(8), 18, [{'kind': 'pine', 'size': [2.2, 5.5, 2.2], 'color': '#5f7f86', 'color2': '#6b5847'}, {'kind': 'rock', 'size': [3, 1.2, 3], 'color': '#ffffff'}], side_rng=(5, 16))
L.obj(id='intro-cloud', t=6, side=18, y=14, kind='cloud', size=[12, 4, 6], color='#ffffff')
# Hook: snow forest corridor, pines pulse on the kick; Tokki peeks from behind a pine (easter egg)
L.obj(id='pines', kind='row', t0=T(8), t1=T(16), side=3.4, spacing=2.4, bothSides=True,
      item={'kind': 'pine', 'size': [1.8, 4.2, 1.8], 'color': '#58787f', 'color2': '#6b5847', 'react': 'kick'},
      appear={'t': T(8) - 1.2, 'mode': 'rise', 'dur': 0.6}, cascade=0.0)
L.scatter(T(8), T(16), 26, [{'kind': 'pine', 'size': [3, 8, 3], 'color': '#4e6b72', 'color2': '#5a4a3c'}], side_rng=(7, 18))
L.obj(id='tokki', t=T(12, 8), side=-6.5, kind='group', egg=True, name='Tokki 兔子', parts=[
    {'kind': 'sphere', 'pos': [0, 0, 0], 'size': [1.2, 1.1, 1.2], 'color': '#ffffff'},
    {'kind': 'sphere', 'pos': [0, 1.0, 0], 'size': [0.9, 0.85, 0.9], 'color': '#ffffff'},
    {'kind': 'box', 'pos': [-0.22, 1.6, 0], 'size': [0.18, 0.9, 0.14], 'color': '#ffffff'},
    {'kind': 'box', 'pos': [0.22, 1.6, 0], 'size': [0.18, 0.9, 0.14], 'color': '#ffffff'},
    {'kind': 'sphere', 'pos': [0.2, 1.15, -0.4], 'size': [0.12, 0.12, 0.12], 'color': '#222222'},
    {'kind': 'sphere', 'pos': [-0.2, 1.15, -0.4], 'size': [0.12, 0.12, 0.12], 'color': '#222222'}],
    appear={'t': T(12), 'mode': 'pop', 'dur': 0.5})
# Verse: the school — tall facades rising with the downbeats, a clock tower
for i, bar in enumerate(range(16, 24)):
    side = (9 + (i % 3) * 2) * (1 if i % 2 else -1)
    L.obj(id=f'school{i}', t=T(bar, 6), side=side, kind='building', size=[9, 7 + (i % 3) * 2, 6], color='#efe6d6', color2='#8aa3c2',
          appear={'t': T(bar) - 1.6, 'mode': 'rise', 'dur': 0.9})
L.obj(id='clocktower', t=T(20), side=12, kind='group', landmark=True, name='钟楼', parts=[
    {'kind': 'box', 'pos': [0, 0, 0], 'size': [4, 16, 4], 'color': '#e9dcc6'},
    {'kind': 'pyramid', 'pos': [0, 16, 0], 'size': [4.6, 4, 4.6], 'color': '#6f86a8'},
    {'kind': 'disc', 'pos': [0, 13, -2.05], 'size': [2.6, 0, 2.6], 'rot': [-90, 0, 0], 'color': '#ffffff'},
    {'kind': 'box', 'pos': [0, 13.3, -2.12], 'size': [0.12, 1.0, 0.05], 'color': '#333333'}])
L.obj(id='lamps1', kind='row', t0=T(16), t1=T(24), side=3.0, spacing=7, bothSides=True, item={'kind': 'lamp', 'size': [0.4, 3.6, 0.4], 'color': '#ffe6a8', 'color2': '#56606f', 'react': 'beat'})
# Verse b: corridor — window panels on both sides react to every tap (Piano-key style)
L.obj(id='windows', kind='row', t0=T(24), t1=T(31), side=3.6, spacing=2.4, bothSides=True, item={'kind': 'box', 'size': [0.3, 2.2, 1.2], 'color': '#e4edf6', 'react': 'tap'})
L.obj(id='lockers', kind='row', t0=T(24), t1=T(31), side=6.5, spacing=1.2, bothSides=True, item={'kind': 'box', 'size': [0.9, 1.8, 1.0], 'color': '#7d9cc4', 'react': 'beat'})
# Pre: the gym — bleachers, hoops, banner
for i, bar in enumerate([32, 34, 36, 38]):
    L.obj(id=f'bleach{i}', t=T(bar), side=-9 if i % 2 else 9, kind='stairs', size=[10, 4, 5], rot=90 if i % 2 else -90, color='#c98e55', color2='#e3b17a', appear={'t': T(bar) - 1.5, 'mode': 'unfold', 'dur': 0.8})
for i, bar in enumerate([33, 37]):
    L.obj(id=f'hoop{i}', t=T(bar, 8), side=6 if i == 0 else -6, kind='group', landmark=True, name='篮球架', parts=[
        {'kind': 'cylinder', 'pos': [0, 0, 0], 'size': [0.3, 6, 0.3], 'color': '#333a45'},
        {'kind': 'box', 'pos': [0, 5.5, -0.6], 'size': [3, 2, 0.15], 'color': '#ffffff'},
        {'kind': 'torus', 'pos': [0, 5.0, -1.3], 'size': [1.0, 0.08, 1.0], 'color': '#ff6a2a'}], react='kick')
L.obj(id='banner', t=T(35), side=-7, y=4, kind='text', name='DITTO', size=[6, 0, 2], color='#2a3f6a')
# Chorus: snow bridge over a town far below — street lamps on the bridge kick-pulse, giant snowflakes
L.obj(id='bridgelamps', kind='row', t0=T(40), t1=T(48), side=2.4, spacing=4.5, bothSides=True, item={'kind': 'lamp', 'size': [0.35, 2.8, 0.35], 'color': '#fff2c2', 'color2': '#3f4a5c', 'react': 'kick'})
L.scatter(T(40), T(64), 40, [{'kind': 'building', 'size': [6, 9, 6], 'color': '#dfe6ee', 'color2': '#9fb1c6'}, {'kind': 'building', 'size': [5, 6, 5], 'color': '#f1e8dc', 'color2': '#b5a48e'},
                             {'kind': 'pine', 'size': [3, 7, 3], 'color': '#6b8a90', 'color2': '#5a4a3c'}], side_rng=(8, 24), y=-12)
for i in range(6):
    L.obj(id=f'flake{i}', t=T(40 + i * 1.5), side=(10 + i * 2) * (1 if i % 2 else -1), y=6 + i % 3 * 2, kind='star', size=[3, 3, 0.3], color='#ffffff', react='beat')
L.ev(T(40), 'flash', amount=0.4); L.ev(T(40), 'burst', at='player', color='#ffffff', amount=60)
for i in range(6): L.ev(T(40), 'spin', target=f'flake{i}', until=T(64), speed=0.8)
# Post: town square — houses, a film reel and a snow globe as landmarks
L.scatter(T(48), T(64), 30, [{'kind': 'building', 'size': [5, 5, 5], 'color': '#f3e3d3', 'color2': '#c27b6b'}, {'kind': 'tree', 'size': [2.5, 4, 2.5], 'color': '#9bb7b0', 'color2': '#6b5847'}, {'kind': 'lamp', 'size': [0.4, 3.5, 0.4], 'color': '#ffe0a3', 'color2': '#444'}], side_rng=(5, 16))
L.obj(id='reel', t=T(52), side=-13, y=2, kind='group', landmark=True, name='胶片盘', parts=[
    {'kind': 'torus', 'pos': [0, 5, 0], 'size': [9, 0.8, 9], 'rot': [90, 0, 0], 'color': '#2f3440'},
    {'kind': 'disc', 'pos': [0, 5, 0], 'size': [8.4, 0, 8.4], 'rot': [90, 0, 0], 'color': '#5a6274'},
    {'kind': 'cylinder', 'pos': [0, 5, 0], 'size': [1.4, 1.2, 1.4], 'rot': [90, 0, 0], 'color': '#c9ced8'}])
L.ev(T(52), 'spin', target='reel', until=T(64), speed=1.2)
L.obj(id='globe', t=T(58), side=12, kind='group', landmark=True, name='雪景球', parts=[
    {'kind': 'cylinder', 'pos': [0, 0, 0], 'size': [6, 1.5, 6], 'color': '#7a5a46'},
    {'kind': 'bubble', 'pos': [0, 1.2, 0], 'size': [7, 7, 7], 'color': '#d9ecff'},
    {'kind': 'building', 'pos': [0, 1.5, 0], 'size': [2, 2.4, 2], 'color': '#ffffff', 'color2': '#c27b6b'},
    {'kind': 'pine', 'pos': [1.8, 1.5, 0.8], 'size': [1, 2.4, 1], 'color': '#5f7f86'}], react='beat')
L.obj(id='sayit', t=T(55, 8), side=-4.2, kind='text', egg=True, name='say it ditto', size=[5.5, 0, 1.2], color='#6c7fb0')
# Bridge: frozen lake, moon, ice crystals that answer the taps
L.obj(id='moon', t=T(68), side=26, y=22, kind='moon', size=[9, 9, 9], color='#f4f1e6', landmark=True, name='月亮')
L.obj(id='crystals', kind='row', t0=T(64), t1=T(71), side=3.3, spacing=3.2, bothSides=True, item={'kind': 'crystal', 'size': [0.8, 2.4, 0.8], 'color': '#cfe6ff', 'react': 'tap'})
# Break: night — the camcorder's REC light appears again (memory), stars
L.obj(id='camcorder2', t=T(74), side=8, kind='group', landmark=True, name='回放', parts=[
    {'kind': 'box', 'pos': [0, 0, 0], 'size': [3.2, 3.0, 5.0], 'color': '#2a2e38'},
    {'kind': 'cylinder', 'pos': [0, 1.0, -3.0], 'size': [2.2, 1.6, 2.2], 'rot': [90, 0, 0], 'color': '#1a1c22'},
    {'kind': 'sphere', 'pos': [1.1, 3.0, 1.6], 'size': [0.6, 0.6, 0.6], 'color': '#ff3b3b'}], appear={'t': T(73), 'mode': 'fade', 'dur': 1.5})
L.obj(id='tokki2', t=T(76, 4), side=-5, kind='group', egg=True, name='Tokki 在冰上', parts=[
    {'kind': 'sphere', 'pos': [0, 0, 0], 'size': [1.0, 0.9, 1.0], 'color': '#ffffff'}, {'kind': 'sphere', 'pos': [0, 0.85, 0], 'size': [0.75, 0.7, 0.75], 'color': '#ffffff'},
    {'kind': 'box', 'pos': [-0.18, 1.35, 0], 'size': [0.15, 0.75, 0.12], 'color': '#ffffff'}, {'kind': 'box', 'pos': [0.18, 1.35, 0], 'size': [0.15, 0.75, 0.12], 'color': '#ffffff'}])
# Final: dawn — crystals rise with the road, the sun comes up
L.obj(id='sun', t=T(90), side=-30, y=4, kind='sun', size=[14, 14, 14], color='#ffd2b0', color2='#ffe9d6', landmark=True, name='朝阳')
L.ev(T(79), 'raise', target='sun', dur=T(95) - T(79), dy=22)
L.obj(id='icepillars', kind='row', t0=T(79), t1=T(96), side=3.0, spacing=3.0, bothSides=True, item={'kind': 'crystal', 'size': [0.9, 3.0, 0.9], 'color': '#ffe3ef', 'react': 'kick'},
      appear={'t': T(79) - 1.0, 'mode': 'rise', 'dur': 0.5}, cascade=1.0)
L.ev(T(79), 'flash', amount=0.5); L.ev(T(79), 'burst', at='player', color='#ffd6e6', amount=80)
L.ev(T(87), 'burst', at='player', color='#ffffff', amount=40); L.ev(T(91), 'burst', at='player', color='#ffffff', amount=40)
# Outro
L.scatter(T(96), T(103), 10, [{'kind': 'cloud', 'size': [8, 3, 5], 'color': '#ffffff'}], side_rng=(8, 20), y=6)

# ---------- collectibles ----------
for pct in [0.07, 0.15, 0.24, 0.33, 0.43, 0.52, 0.61, 0.70, 0.83, 0.93]:
    d['diamonds'].append({'t': L.gap_mid(pct * 185.5, 0.6)})
c1 = L.gap_after(T(31), 1.0); c2 = L.gap_after(T(71), 1.2)
d['crowns'] = [{'t': round(c1[0] + 0.05, 3)}, {'t': round(c2[0] + 0.05, 3)}]
L.save()
