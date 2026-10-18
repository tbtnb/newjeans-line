#!/usr/bin/env python3
"""OMG v2 'Y2K Starlight Stage' scenery generator (route-relative, survives a re-chart).

Reads levels-src/omg/chart.json sections (kinds + times) and writes levels-design/omg/art-props.json:
section themes (palette / backdrop / ground / particles), fx (v2.8 show visuals), dressing palette per section,
set pieces and landmarks as time windows (tools/art/artkit.py picks the exact times/sides from the current route;
the engine resolves positions against the real road at load). Then run:
  python3 tools/art/omg_scene.py && python3 tools/art/artkit.py omg levels-design/omg/art-props.json
"""
import json, math
from pathlib import Path

C = json.loads(Path('levels-src/omg/chart.json').read_text())
L = json.loads(Path('levels-src/omg/layout.json').read_text())
secs = C['sections']
# level end: layout.endTime when the level stops before the song (the last section then becomes the finale)
EARLY = bool(L.get('endTime')); end = L['endTime'] if EARLY else C['taps'][-1]['t'] + 6
A = lambda n: f'art/v2/{n}'

# ---- section themes (by musical role, so a re-chart with the same song structure keeps working)
def theme(i):
    s = secs[i]; k = s['kind']; nxt = secs[i + 1]['kind'] if i + 1 < len(secs) else None
    nch = sum(1 for x in secs[:i] if x['kind'] == 'chorus')
    if EARLY and i == len(secs) - 1: return 'finale'   # the level ends here: fireworks + curtains at the end
    if k == 'intro': return 'dream'
    if k == 'outro': return 'calm'
    if k == 'bridge' or (k == 'break' and secs[i - 1]['kind'] == 'bridge'): return 'garden'
    if k == 'chorus': return 'finale' if nch >= 2 else 'stage'
    if k == 'drop': return 'rise'
    if nxt in ('chorus',) or k == 'pre': return 'rise'
    if k == 'post': return 'stage'
    return 'ward'

T = {
 'dream':  dict(palette=dict(skyTop='#b9b4f0', skyBottom='#ffe1f0', fog='#e9dcff', fogStart=40, fogEnd=135, ground='#ffffff', road='#ffffff', roadSide='#e9c98a', line='#ff8fc0', light='#fff3ff', lightIntensity=1.1, ambient='#e8dcff', particles='dust'),
                backdrop=A('sky-dream.jpg'), ground=dict(src=A('ground-ward.jpg'), scale=24)),
 'ward':   dict(palette=dict(skyTop='#a9b6f2', skyBottom='#ffd9ec', fog='#e3d9ff', fogStart=38, fogEnd=125, ground='#f4f0ff', road='#ffffff', roadSide='#e2bf7a', line='#ff8fc0', light='#fff6f0', lightIntensity=1.05, ambient='#e0d6ff', particles='bubbles'),
                backdrop=A('sky-dream.jpg'), ground=dict(src=A('ground-ward.jpg'), scale=24)),
 'rise':   dict(palette=dict(skyTop='#3a2f7a', skyBottom='#b98ad8', fog='#5a4a9a', fogStart=36, fogEnd=120, ground='#8a80c0', road='#ffffff', roadSide='#e6c37c', line='#ff7ab6', light='#ffd9f2', lightIntensity=0.95, ambient='#9a8ad8', particles='stars'),
                backdrop=A('sky-stage.jpg'), ground=dict(src=A('ground-stage.jpg'), scale=30)),
 'stage':  dict(palette=dict(skyTop='#1c1a52', skyBottom='#6b4fb0', fog='#2c2668', fogStart=34, fogEnd=118, ground='#8a80c0', road='#ffffff', roadSide='#f0c56a', line='#ff6fb1', light='#ffe6fa', lightIntensity=1.0, ambient='#8270cc', particles='confetti'),
                backdrop=A('sky-stage.jpg'), ground=dict(src=A('ground-stage.jpg'), scale=30)),
 'finale': dict(palette=dict(skyTop='#24185e', skyBottom='#d06fb8', fog='#3b2a78', fogStart=34, fogEnd=120, ground='#8a80c0', road='#ffffff', roadSide='#ffd27a', line='#ff5fa8', light='#fff0fb', lightIntensity=1.1, ambient='#9a7ad8', particles='confetti'),
                backdrop=A('sky-stage.jpg'), ground=dict(src=A('ground-stage.jpg'), scale=30)),
 'garden': dict(palette=dict(skyTop='#4b4a9a', skyBottom='#c8b4ec', fog='#6a64b0', fogStart=34, fogEnd=115, ground='#9a94c8', road='#ffffff', roadSide='#c9b37a', line='#ff9ccf', light='#dfe6ff', lightIntensity=0.85, ambient='#9a9ae0', particles='petals'),
                backdrop=A('sky-moon.jpg'), ground=dict(src=A('ground-garden.jpg'), scale=26)),
 'calm':   dict(palette=dict(skyTop='#9aa4e8', skyBottom='#ffe6f2', fog='#ddd4ff', fogStart=40, fogEnd=140, ground='#f6f0ff', road='#ffffff', roadSide='#e2bf7a', line='#ff9cc8', light='#fff6f6', lightIntensity=1.0, ambient='#e0d8ff', particles='stars'),
                backdrop=A('sky-moon.jpg'), ground=dict(src=A('ground-garden.jpg'), scale=26)),
}
themes = [theme(i) for i in range(len(secs))]
rng = [(s['t'], secs[i + 1]['t'] if i + 1 < len(secs) else end, themes[i]) for i, s in enumerate(secs)]
def spans(*names): return [(a, b) for a, b, th in rng if th in names]

# ---- dressing: themed textured props + theme colours; sections pick the subset per theme
art = [
  dict(src=A('ward-facade.jpg'), **{'as': 'facade'}, size=[3.2, 4.4, 3.0], weight=1, scale=[0.8, 1.2], scaleY=[0.8, 1.5]),   # 5
  dict(src=A('stage-facade.jpg'), **{'as': 'facade'}, size=[3.4, 3.4, 3.0], weight=1, scale=[0.8, 1.2], scaleY=[0.9, 1.6]),  # 6
  dict(src=A('heart-pill.png'), **{'as': 'card'}, size=[1.6, 1.6, 0.05], weight=1, scale=[0.8, 1.3], scaleY=[1, 1], glow=0.5), # 7
  dict(src=A('call-bubble.png'), **{'as': 'card'}, size=[2.2, 1.65, 0.05], weight=1, scale=[0.8, 1.2], scaleY=[1, 1], glow=0.5), # 8
  dict(src=A('ward-bed.png'), **{'as': 'card'}, size=[2.6, 1.95, 0.05], weight=1, scale=[0.8, 1.1], scaleY=[1, 1]),          # 9
  dict(src=A('mural-stars.png'), **{'as': 'tile'}, size=[3, 0, 3], weight=1, scale=[0.8, 1.3], scaleY=[1, 1], glow=0.6),     # 10
  dict(src=A('flip-phone.png'), **{'as': 'card'}, size=[1.5, 2.0, 0.05], weight=1, scale=[0.8, 1.2], scaleY=[1, 1], glow=0.5), # 11
  dict(src=A('wreath-star.png'), **{'as': 'tile'}, size=[3, 0, 3], weight=1, scale=[0.8, 1.3], scaleY=[1, 1], glow=0.6),     # 12
  dict(src=A('wreath-flower.png'), **{'as': 'tile'}, size=[3, 0, 3], weight=1, scale=[0.8, 1.3], scaleY=[1, 1], glow=0.6),   # 13
  dict(src=A('wreath-ribbon.png'), **{'as': 'tile'}, size=[3, 0, 3], weight=1, scale=[0.8, 1.3], scaleY=[1, 1], glow=0.6),   # 14
  dict(src=A('wreath-moon.png'), **{'as': 'tile'}, size=[3, 0, 3], weight=1, scale=[0.8, 1.3], scaleY=[1, 1], glow=0.6),     # 15
]
dsec = []
PROPS = {'dream': [0, 1, 5, 12, 14], 'ward': [0, 1, 5, 14, 15], 'rise': [3, 6, 10, 15], 'stage': [3, 6, 12, 15],
         'finale': [6, 10, 12, 13, 14, 15], 'garden': [7, 13, 15], 'calm': [0, 5, 13, 14]}   # heart wreath varies: star / flower / ribbon-bunny / moon
DENS = {'dream': 3.0, 'ward': 3.4, 'rise': 3.4, 'stage': 3.8, 'finale': 4.2, 'garden': 3.0, 'calm': 2.4}   # forward route: one stretch of road in view at a time, so pack the 2-6 m band densely
for a, b, th in rng: dsec.append(dict(t=a, props=PROPS[th], density=DENS[th]))
dressing = dict(colors=['#fff4fb', '#c9b8ff', '#ff8fc0', '#3a2f7a', '#8fd0ff'], art=art, artShare=0.6, near=[2.0, 6], lead=4.5, sections=dsec)

import re as _re
_g = [tp['t'] for tp in C['taps'] if _re.search(r'\bgod\b', str(tp.get('lyric', '')), _re.I)]
if Path('analysis/omg.lyrics.json').exists():
    _g = [x['t'] for x in json.loads(Path('analysis/omg.lyrics.json').read_text())['syllables'] if x['word'].lower().strip(',.?!') == 'god' and x['t'] < end - 1]
def drop_near(a):
    # giant bunny rises (appear mode 'rise') at the first 'God' hit of the chorus starting at a, else 2 s in
    g = [x for x in _g if a - 0.5 <= x <= a + 12]
    return (g[0] + 0.3) if g else a + 2

# ---- landmarks / set pieces (time windows; artkit picks times + sides on the current route)
O = []
def add(kind, src, size, w, count=1, **k): O.append(dict(kind=kind, src=A(src), size=size, window=list(w), count=count, **k))
st = lambda src, size, w, count=1, **k: add('standee', src, size, w, count, face=k.pop('face', 'camera'), **k)
for a, b in spans('dream', 'calm'):
    st('bunny-giant.png', [6, 6, 0], (a + 1.5, min(b, a + 6)), 1, landmark=True, glow=0.45, near=2.5, id='bunny_intro')
    st('ward-bed.png', [5.5, 4.1, 0], (a + 4, b - 1), 1, near=2)
    add('decal', 'wreath-flower.png', [6, 0, 6], (a + 1, b - 1), 1, face='road', glow=0.6)
for a, b in spans('ward'):
    st('ward-bed.png', [5.5, 4.1, 0], (a + 1, b - 1), 1, near=2)
    add('facade', 'ward-facade.jpg', [5, 6, 3], (a + 1, b - 1), 2, face='road', color='#fff4fb', color2='#c9b8ff', near=2)
    st('call-bubble.png', [4, 3, 0.8], (a + 2, b - 1), 1, color='#ffd27a', color2='#ffd27a', near=1.5, glowfx=True, id='call')
for a, b in spans('rise'):
    st('flip-phone.png', [4.2, 5.6, 0], (a + 1, b - 1), 2, near=2.5, glowfx=True, id='phone')
    add('facade', 'stage-facade.jpg', [6, 6, 3], (a + 1, b - 1), 1, face='road', color='#2a2460', color2='#ffd27a', near=3)
for i, (a, b) in enumerate(spans('stage', 'finale')):
    big = i == 0 or b - a > 14
    st('star-arch.png', [7, 5.25, 0], (a + 0.3, a + 2.5), 1, landmark=True, glowfx=True, near=2, face='camera', id='arch')
    if big: st('bunny-giant.png', [8, 8, 0], (a + 3, a + 8), 1, landmark=True, near=3, id='bunny_rise', appear=dict(t=round(drop_near(a), 3), mode='rise', dur=2.2))
    st('flip-phone.png', [4.2, 5.6, 0], (a + 2, b - 1), 2, near=2.5, glowfx=True, id='phone')
    add('facade', 'stage-facade.jpg', [6, 6, 3], (a + 1, b - 1), 1, face='road', color='#2a2460', color2='#ffd27a', near=3)
    add('decal', 'wreath-ribbon.png', [7, 0, 7], (a + 1, b - 1), 1, face='road', glow=0.7)
for a, b in spans('garden'):
    st('bunny-giant.png', [6, 6, 0], (a + 1, a + 5), 1, landmark=True, near=3)
    add('decal', 'wreath-moon.png', [7, 0, 7], (a + 1, b - 1), 1, face='road', glow=0.7)
    st('heart-pill.png', [3, 3, 0.5], (a + 1, b - 1), 1, color='#c9b37a', color2='#c9b37a', near=2, react='beat')

# ---- events: set pieces that animate with the music (keyed off the lyric chart where possible)
import re
ev = []
taps = C['taps']
gods = [tp['t'] for tp in taps if re.search(r'\bgod\b', str(tp.get('lyric', '')), re.I)]   # "Oh my god" hits
_lf = Path('analysis/omg.lyrics.json')   # sung 'god' times from the lyric alignment (the chart may be hand-tapped without lyrics)
if _lf.exists():
    gods = [x['t'] for x in json.loads(_lf.read_text())['syllables'] if x['word'].lower().strip(',.?!') == 'god' and x['t'] < end - 1]
drops = []
for g in gods:
    if not drops or g - drops[-1][0] > 20:
        nxt = next((tp['t'] for tp in taps if tp['t'] > g + 1e-6), g)
        drops.append((g, nxt))
drops = [d for _, d in drops]
if not drops: drops = [s['t'] for s, th in zip(secs, themes) if th in ('stage', 'finale')][:3]
for g in gods:  # phone screens light up one after another on every 'Oh my god'
    ev.append(dict(t=round(g, 3), type='light', target='art-phone', every=0.07, dur=0.15, color='#ffb3e0', level=1.4, until=round(g + 2.4, 3)))
for d in drops:
    ev.append(dict(t=round(d, 3), type='burst', at='player', color='#ffe7a8', amount=60))
for s, th in zip(secs, themes):
    if th == 'ward': ev.append(dict(t=round(s['t'] + 1, 3), type='light', target='art-call', every=0.4, dur=0.4, color='#ffe7a8', level=0.8, until=round(s['t'] + 9, 3)))
ev.sort(key=lambda e: e['t'])

# ---- fx: show visuals
keys, pulse, flashes, beams, sparkles = [], [], [], [], []
GR = {'dream': (0.97, 1.05, 0.5), 'ward': (0.97, 1.05, 0.5), 'rise': (1.0, 1.12, 0.55), 'stage': (1.0, 1.12, 0.6), 'finale': (1.02, 1.15, 0.7), 'garden': (0.95, 1.1, 0.8), 'calm': (1.0, 1.0, 0.5)}
for a, b, th in rng:
    e, c, g = GR[th]; keys.append(dict(t=round(a, 3), exposure=e, contrast=c, glow=g, blend=1.2))
    if th in ('stage', 'finale', 'rise'): pulse.append(dict(t=round(a, 3), t1=round(b, 3), amount=0.12 if th == 'rise' else 0.18))
    if th in ('rise', 'stage', 'finale'):
        beams.append(dict(t0=round(a + 0.5, 3), t1=round(b - 0.5, 3), every=2.2 if th != 'rise' else 3.0, colors=['#ff9ad5', '#9fd8ff', '#c9a8ff', '#ffe08a'], height=45, near=3.5))
    sp = {'dream': 0.5, 'ward': 0.3, 'rise': 1.0, 'stage': 1.6, 'finale': 2.0, 'garden': 1.2, 'calm': 0.6}[th]
    sparkles.append(dict(t0=round(a, 3), t1=round(b, 3), density=sp, colors=['#fff3c4', '#ffc4e8', '#c4e4ff'], size=0.9 if th in ('stage', 'finale') else 0.6, spread=12, height=9))
flashes = [dict(t=round(d, 3), dur=0.7, amount=0.55) for d in drops]
fx = dict(exposure=1.0, contrast=1.05, keys=keys, pulse=pulse,
          flashes=flashes, beams=beams, sparkles=sparkles, road=dict(gloss=0.2, trim='#ffe08a', trimGlow=1.2, trimWidth=0.11, topGlow=0.05), maxBeams=28, maxSparkles=120, sprite=A('sparkle.png'))


# ---- corridor (schema v2.9): far band of big set pieces 6-20 m off the road, floor light strips, emblems, fireworks.
# Rhythm: placements land on bar lines of the song grid (127 BPM), so towers / arches / balloons pass in time with the music.
try: BEATS = json.loads(Path('src/levels/omg.json').read_text())['layout']['beats']
except Exception: BEATS = []
BEAT = 60 / 127; BAR = BEAT * 4; B0 = BEATS[0] if BEATS else 0.031
def on_bar(t): return B0 + math.ceil((t - B0) / BAR - 1e-6) * BAR
CI = []
def item(src, w, h, **k): CI.append(dict(src=A(src), size=[w, h], **k)); return len(CI) - 1
I = dict(
  arch=item('star-arch.png', 7.5, 5.0, glow=1.0, lights='chase'),
  tower=item('light-tower.png', 6.4, 9.6, glow=1.05, lights='chase'),
  rig=item('spot-rig.png', 6.6, 4.4, glow=1.05, lights='beat'),
  bball=item('bunny-balloon.png', 3.2, 4.8, glow=1.0, float=0.45),
  hball=item('heart-balloon.png', 2.8, 4.2, glow=1.0, float=0.5),
  sball=item('star-balloon.png', 2.8, 4.2, glow=1.0, float=0.5),
  phone=item('flip-phone.png', 3.4, 5.1, glow=1.0, lights='beat'),
  flower=item('moon-flower.png', 3.6, 5.4, glow=1.0, lights='beat'),
  lantern=item('lantern.png', 2.2, 4.8, glow=1.0, lights='chase'),
  moon=item('crescent-moon.png', 6, 6, glow=1.0, float=0.3),
  curtain=item('curtain.png', 12, 8, glow=0.95, lights='beat'),
  bunny=item('bunny-giant.png', 7, 7, glow=0.95),
  wstar=item('wreath-star.png', 5, 5, flat=True, glow=0.55, lights='beat'),
  wflower=item('wreath-flower.png', 5, 5, flat=True, glow=0.55, lights='beat'),
  wribbon=item('wreath-ribbon.png', 5, 5, flat=True, glow=0.55, lights='beat'),
  wmoon=item('wreath-moon.png', 5, 5, flat=True, glow=0.55, lights='beat'),
)
bands, floor, fireworks = [], [], []
def band(a, b, every_bars, items, near, phase=0, **k):
    bands.append(dict(t0=round(on_bar(a + 0.2) + phase * BAR, 3), t1=round(b - 0.3, 3), every=round(every_bars * BAR, 4), near=near, items=[I[x] for x in items], **k))
for a, b, th in rng:
    if th in ('dream', 'calm'):
        band(a, b, 1, ['arch'], [3.5, 7], mirror=True)
        band(a, b, 1, ['bball', 'hball', 'sball'], [4, 10], phase=0.5, y=[3, 6], sides=1)
        band(a, b, 2, ['wstar', 'wribbon'], [2.5, 6], phase=0.75, sides=1)
    elif th == 'ward':
        band(a, b, 1, ['tower', 'phone'], [3.5, 6], mirror=True)
        band(a, b, 1, ['arch'], [6, 9], phase=0.5, sides=1)
        band(a, b, 1, ['bball', 'hball'], [5, 11], phase=0.5, y=[3, 7], sides=1)
        band(a, b, 4, ['arch'], [7, 11], phase=1)
        band(a, b, 2, ['wstar', 'wribbon', 'wmoon'], [2.5, 6], phase=0.75, sides=1)
    elif th == 'rise':
        band(a, b, 1, ['tower'], [3.5, 6], mirror=True)
        band(a, b, 1, ['rig'], [5.5, 9], phase=0.5)
        band(a, b, 1, ['phone', 'sball'], [5, 11], phase=0.5, y=[1, 5], sides=1)
        band(a, b, 2, ['wmoon', 'wstar'], [2.5, 6], phase=0.75, sides=1)
    elif th in ('stage', 'finale'):
        band(a, b, 1, ['tower'], [3.5, 6], mirror=True)
        band(a, b, 1, ['arch', 'rig'], [5.5, 9], phase=0.5)
        band(a, b, 0.5, ['bball', 'hball', 'sball', 'phone'], [5, 12], phase=0.25, y=[3, 8], sides=1)
        band(a, b, 1, ['wstar', 'wribbon', 'wmoon', 'wflower'], [2.5, 6], phase=0.5, sides=1)
        if th == 'finale':
            band(a, b, 8, ['curtain'], [9, 13], phase=0)
            band(a, b, 4, ['bunny'], [7, 11], phase=2, sides=1)
            t = on_bar(a + 0.2)
            while t < b - 0.5:   # low and close (6 m up, 8 m out) so they are inside the gameplay framing
                fireworks.append(dict(t=round(t, 3), near=8, height=6, colors=['#ffd27a', '#ff9ad5', '#9fd8ff', '#c9a8ff'], amount=90)); t += BAR
            if EARLY and b >= end - 0.01:   # finish: curtains flank the last two bars, a double salvo on the last downbeats
                band(b - 2 * BAR - 0.2, b + 0.3, 1, ['curtain'], [5, 8], mirror=True)
                for tt in (b - 2 * BAR, b - BAR, b - BAR / 2):
                    for nr in (7, 10): fireworks.append(dict(t=round(tt, 3), near=nr, height=6, colors=['#ffd27a', '#ff9ad5', '#9fd8ff', '#c9a8ff'], amount=110))
    elif th == 'garden':
        band(a, b, 0.5, ['flower', 'lantern'], [3, 6.5], mirror=True)
        band(a, b, 2, ['bunny'], [6, 9], phase=1, sides=1)
        band(a, b, 4, ['moon'], [8, 13], phase=1, y=[6, 9])
        band(a, b, 1, ['bball', 'sball'], [5, 11], phase=0.5, y=[3, 7], sides=1)
        band(a, b, 1, ['wflower', 'wmoon'], [2.5, 6], phase=0.5, sides=1)
    fl = {'dream': '#ffc4e8', 'calm': '#ffc4e8', 'ward': '#c9b8ff', 'rise': '#ff9ad5', 'stage': '#ffd27a', 'finale': '#ff9ad5', 'garden': '#9fd8ff'}[th]
    if fl: floor.append(dict(t0=round(a, 3), t1=round(b, 3), every=round(BEAT / 2, 4), offsets=[1.5, 3.2], color=fl, size=1.0, alpha=1.0))
corridor = dict(items=CI, bands=bands, floor=floor, fireworks=fireworks, lead=6.5, tail=4, maxActive=40)

sections = [dict(t=s['t'], palette=T[th]['palette'], backdrop=T[th]['backdrop'], ground=T[th]['ground']) for s, th in zip(secs, themes)]
spec = dict(keep=['fakefork'], minclear=3.0, objects=O, dressing=dressing, fx=fx, events=ev, corridor=corridor, revealLead=2.8,
            art=dict(backdrop=A('sky-dream.jpg'), ground=dict(src=A('ground-ward.jpg'), scale=24)),
            palette=T['dream']['palette'], sections_by_time=sections)
Path('levels-design/omg/art-props.json').write_text(json.dumps(spec, indent=1, ensure_ascii=False) + '\n')
print('themes', list(zip([round(s["t"], 1) for s in secs], themes)))
print(len(O), 'object specs,', len(ev), 'events; drops', drops, 'gods', gods)
