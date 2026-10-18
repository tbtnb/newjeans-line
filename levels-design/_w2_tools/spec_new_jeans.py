FOLDER='new-jeans'; OLD=68; BEAT_OFFSET=0; MIN_GAP=0.21
JUDGE={'perfect':60,'good':115,'note':'±115 ms accept; the tightest pair is an 8th (224 ms) so windows stay disjoint. Short level with sparse old chart: keep the window generous so the jump in density reads as rhythm, not punishment.'}
START_HEADING='N'
SPEED=[(0,10.2)]
WIDTH=[(0,2.2),(36.19,2.0),(86.34,1.8),(100.67,2.2)]
SECTIONS=[
 dict(b0=0,b1=4,kind='intro',label='Intro · 方格纸',pats=['m.....m.........'],over={0:'......m.........',3:'m.....m.....m...'}),
 dict(b0=4,b1=8,kind='intro',label='Beat in · 蓝图线',pats=['..s.......s.....','..s.s.......s...'],over={7:'s...s.s.s...s...'}),
 dict(b0=8,b1=20,kind='verse',label='Verse 1 · 纸片房屋',pats=['k.........k.....','k.........k.....','k...s.....k.....','k.........k.....']),
 dict(b0=20,b1=28,kind='chorus',label='Chorus 1 · 五色尾迹',pats=['....k...k.....k.','s.......k.....k.'],over={27:'....k...k.k.k.k.'}),
 dict(b0=28,b1=32,kind='break',label='Break · 像素平面',pats=['..s.......s...s.','..s.......s.....']),
 dict(b0=32,b1=36,kind='break',label='Rebuild · 重新立起',pats=['..s.k.......k...','..s.......s.k...'],over={35:'..s.k.s.k.s.k...'}),
 dict(b0=36,b1=48,kind='verse',label='Verse 2 · 立体城市',pats=['k.........k.....','k.........k.....','k...s.....k.....','k.........k.....'],over={47:'k...k...k.k.k...'}),
 dict(b0=48,b1=56,kind='chorus',label='Chorus 2 · 飞行',pats=['....k...k..k..k.','s.......k..k..k.'],over={55:'....k...k.k.k.k.'}),
 dict(b0=56,b1=60,kind='outro',label='Outro · 牛仔徽章',pats=['m.....m.........','m...............'],over={59:'m...............'}),
]
NOTES=('134.0 BPM grid fitted to drum stem. Verse = UK-garage 2-step (kick 1 and the "and" of 3, snare 2) charted as kick 0/10 with snare 4 every other bar; '
       'chorus = jersey-style kick on 2, 3, 3a, 4+ (steps 4,8,11,14) + downbeat snare; break = off-beat claps (steps 2,6,10,14). '
       'Old chart had 68 taps (0.62/s, first tap at 7.96 s) — far sparser than the music; new chart roughly doubles+ to 1.4/s while keeping verses at 2–3 taps per bar.')
MOTIFS=[(0,'meander'),(7.51,'stair'),(14.67,'meander'),(36.16,'stair'),(50.49,'meander'),(57.65,'stair'),(64.82,'meander'),(86.31,'stair')]
PIVOTS=[7.6,14.7,21.9,29.0,36.2,43.4,50.5,57.7,64.9,72.0,79.2,86.4,93.5,100.7]
ELEV=[dict(t=36.16,type='jump',dy=3),dict(t=50.49,type='fall',dy=-6),dict(t0=64.9,t1=71.9,type='ramp',dy=3),dict(t=86.31,type='jump',dy=4),dict(t=100.64,type='fall',dy=-4)]
def layout(c):
    bar=c['bar']; g=c['gap_mid']
    P=dict(skyTop='#cfe6ff',skyBottom='#fdfcf7',fog='#eef4fb',fogStart=28,fogEnd=90,ground='#f7f6f0',groundY=-10,
           road='#ffffff',roadSide='#9ec3e6',line='#1f6fd1',light='#ffffff',lightIntensity=1.1,ambient='#cfdcea',particles=None)
    secs=[
     dict(t=0,label='Intro · 方格纸',palette=dict(skyTop='#f4f6f8',skyBottom='#ffffff',ground='#f8f9fb',road='#e8eef6',roadSide='#b7c6d8',line='#5a6b80'),camera='top',note='graph paper; road = pencil blueprint line, grid lines on ground'),
     dict(t=bar(4),label='Beat in · 蓝图线',palette=dict(road='#ffffff',roadSide='#9ec3e6',line='#1f6fd1'),camera='iso'),
     dict(t=bar(8),label='Verse 1 · 纸片房屋',palette=dict(skyTop='#cfe6ff'),camera='iso',note='paper houses pop up from the page (unfold)'),
     dict(t=bar(20),label='Chorus 1 · 五色尾迹',palette=dict(skyTop='#ffd1e8',skyBottom='#fff7fb',particles='pixels'),camera='high',note='jump: five colour trails (pink, blue, green, yellow, purple) launch into the sky'),
     dict(t=bar(28),label='Break · 像素平面',palette=dict(skyTop='#e9f1fb',road='#f2f6fb',particles=None),camera='top',note='fall back onto the flat pixel plane'),
     dict(t=bar(32),label='Rebuild · 重新立起',camera='iso'),
     dict(t=bar(36),label='Verse 2 · 立体城市',palette=dict(skyTop='#bfe0ff',ground='#e9f0f7'),camera='side'),
     dict(t=bar(48),label='Chorus 2 · 飞行',palette=dict(skyTop='#ffc7e1',skyBottom='#e8f6ff',particles='pixels'),camera='wide'),
     dict(t=bar(56),label='Outro · 牛仔徽章',palette=dict(skyTop='#3d5f8f',skyBottom='#7f9fc7',ground='#3f5f88',roadSide='#2e4a70',light='#ffffff'),camera='high',note='camera pulls back: the city was a badge on a denim jacket'),
    ]
    cam=[dict(t=0,preset='top',blend=0),dict(t=bar(4),preset='iso',blend=2.5),dict(t=bar(20),preset='high',blend=1.0),dict(t=bar(24),preset='iso',yaw=60,blend=2.0),
         dict(t=bar(28),preset='top',blend=1.0),dict(t=bar(32),preset='iso',blend=2.0),dict(t=bar(36),preset='side',blend=1.5),dict(t=bar(42),preset='iso',blend=2.0),
         dict(t=bar(48),preset='wide',blend=0.9),dict(t=bar(52),preset='low',blend=2.0),dict(t=bar(56),preset='high',dist=34,blend=5.0)]
    O=[]
    O.append(dict(id='grid_lines',kind='row',t0=0.5,t1=bar(8),side=3.5,spacing=2.0,bothSides=True,item=dict(kind='box',size=[0.06,0.02,6],color='#b7c6d8')))
    O.append(dict(id='pencil',t=2.0,side=6,along=3,kind='group',radius=3,landmark=True,name='铅笔',
                  parts=[dict(kind='cylinder',pos=[0,0.4,0],size=[0.6,7,0.6],rot=[90,30,0],color='#f2c94c'),dict(kind='cone',pos=[0,0.4,3.9],size=[0.6,0.9,0.6],rot=[90,30,0],color='#e8c39e')]))
    for i,t in enumerate([bar(9),bar(11),bar(13),bar(15),bar(17),bar(19)]):
        if i in (1,4): continue
        O.append(dict(id=f'paperhouse{i}',t=t,side=(11 if i%2==0 else -11),kind='group',radius=2.5,
                      parts=[dict(kind='box',pos=[0,1.2,0],size=[3,2.4,3],color='#ffffff'),dict(kind='cone',pos=[0,3.1,0],size=[3.6,1.4,3.6],rot=[0,45,0],color=['#ff8fc3','#7fb8ff','#7fe0a8','#ffd86b','#b99cff','#ff8fc3'][i])],
                      appear=dict(t=t-1.5,mode='unfold',dur=0.6),react='kick'))
    trail_cols=['#ff7eb6','#5aa8ff','#5ad69a','#ffd23f','#a98bff']
    for i,col in enumerate(trail_cols):
        O.append(dict(id=f'trail{i}',t=bar(21)+i*0.45,side=-12-i*2.5,y=7+i*1.5,kind='box',size=[1.2,1.2,40],color=col,landmark=(i==2),name='五色超能力尾迹' if i==2 else None,
                      appear=dict(t=bar(20)+i*c['T'],mode='grow',dur=1.2),exit=dict(t=bar(28),mode='fade',dur=1.0)))
    O.append(dict(id='pixel_heart',t=bar(30),side=-10,y=0,kind='group',radius=3,landmark=True,name='像素爱心',
                  parts=[dict(kind='box',pos=[x*0.8,y*0.8+1,0],size=[0.8,0.8,0.8],color='#ff5fa2') for x,y in [(-1,2),(1,2),(-2,1),(0,1),(2,1),(-2,0),(-1,0),(0,0),(1,0),(2,0),(-1,-1),(0,-1),(1,-1),(0,-2)]]+[dict(kind='box',pos=[-2*0.8,3*0.8,0],size=[0.01,0.01,0.01],color='#ff5fa2')],
                  appear=dict(t=bar(28),mode='pop',dur=0.4),react='beat'))
    for i in range(6):
        t=bar(37)+i*3.58
        O.append(dict(id=f'tower{i}',t=t,side=(10 if i%2==0 else -10),kind='building',size=[4,8+2*(i%3),4],color='#ffffff',color2=trail_cols[i%5],appear=dict(t=t-1.8,mode='rise',dur=0.9)))
    O.append(dict(id='city_core',t=bar(44),side=-22,kind='group',radius=6,landmark=True,name='立体玩具城',
                  parts=[dict(kind='box',pos=[0,5,0],size=[5,10,5],color='#ffffff'),dict(kind='box',pos=[4,3,2],size=[3,6,3],color='#7fb8ff'),dict(kind='box',pos=[-4,4,-1],size=[3,8,3],color='#ff8fc3'),
                         dict(kind='sphere',pos=[0,11,0],size=[2.4,2.4,2.4],color='#ffd86b')],appear=dict(t=bar(42),mode='rise',dur=1.6)))
    O.append(dict(id='badge',t=bar(58),side=0,y=-6,kind='disc',size=[40,1,40],color='#5677a8',color2='#ffffff',onroad=True,landmark=True,name='牛仔外套徽章 (huge disc under the whole outro area)',
                  appear=dict(t=bar(56),mode='fade',dur=2.0)))
    O.append(dict(id='denim_stitch',kind='row',t0=bar(56),t1=bar(60)-0.5,side=3.2,spacing=0.8,bothSides=True,item=dict(kind='box',size=[0.12,0.05,0.5],color='#f2c94c')))
    O.append(dict(id='egg_plant',t=bar(17)+0.5,side=-4.5,kind='group',radius=1,egg=True,name='点头的小植物',
                  parts=[dict(kind='cylinder',pos=[0,0.4,0],size=[0.8,0.8,0.8],color='#c97b4a'),dict(kind='sphere',pos=[0,1.2,0],size=[1,1,1],color='#5ad69a')],react='tap'))
    O.append(dict(id='egg_bunny_glint',t=bar(59),side=-6,y=0.2,kind='group',radius=1.5,egg=True,name='徽章反光里的兔耳',
                  parts=[dict(kind='box',pos=[-0.3,1,0],size=[0.3,1.4,0.05],color='#ffffff'),dict(kind='box',pos=[0.3,1,0],size=[0.3,1.4,0.05],color='#ffffff')],appear=dict(t=bar(59),mode='fade',dur=0.6)))
    ev=[dict(t=bar(4),type='color',palette=dict(road='#ffffff',line='#1f6fd1'),dur=1.0),dict(t=bar(20),type='burst',at='player',particles='pixels'),
        dict(t=bar(28),type='color',palette=dict(skyTop='#e9f1fb'),dur=0.5),dict(t=bar(48),type='burst',at='player',particles='confetti'),
        dict(t=bar(56),type='color',palette=dict(skyTop='#3d5f8f'),dur=4.0)]
    cr=[g(x,0.9) for x in CROWN_T(bar)]
    dia=[g(t,0.5) for t in [bar(2),bar(6),bar(10),bar(16),bar(25),bar(30),bar(40),bar(45),bar(52),bar(57)]]
    return dict(id='new-jeans',title='New Jeans',palette=P,road=dict(height=0.6,reveal=[dict(t=0,mode='fade',lead=2.0),dict(t=bar(8),mode='unfold',lead=1.6),
                dict(t=bar(28),mode='static',lead=2.0),dict(t=bar(36),mode='rise',lead=1.5)]),
                sections=secs,camera=cam,objects=O,events=ev,diamonds=[dict(t=t,side=0) for t in dia],
                crowns=[dict(t=x) for x in cr],finish=dict(kind='gate'))
WHY={
 'Intro (0–7.5 s)':'synth stabs only (other stem "O" on steps 0 and 6): 2 taps per bar — the line is drawn on graph paper.',
 'Beat in (7.5–14.7 s)':'drums without bass: taps on the snare accents at steps 2,4,12 (syncopated 2-step snares), 8-tap fill in bar 7.',
 'Verse 1 / 2':'garage 2-step: kick on 1 and the "and" of 3 (steps 0,10) every bar, plus snare on beat 2 every other bar — 2–3 taps per bar so the rap-like vocal sits on a readable pulse.',
 'Chorus 1 / 2':'jersey kick on 2, 3, 3a, 4+ (steps 4,8,11,14) under the "new hair, new tee" hook; the downbeat snare starts every other bar; bar 27/55 ends with an 8th kick roll (5 taps).',
 'Break (50.5–57.7 s)':'kick drops, only off-beat claps on steps 2,6,10,14: the player taps off the beat for 4 bars (syncopation test).',
 'Rebuild (57.7–64.9 s)':'kick returns on beats 2 and 4 with off-beat claps: "..s.k" call-response pairs, 7-tap run in bar 35.',
 'Outro (100.7–109 s)':'drums stop, synth stabs: 1–2 taps per bar, camera pulls back.',
}

CROWN_T=lambda bar: [bar(28)+0.4,bar(47)]
