FOLDER='ditto'; OLD=181; BEAT_OFFSET=0; MIN_GAP=0.21
JUDGE={'perfect':60,'good':110,'note':'±110 ms accept around the geometric corner; 8th runs are 224 ms apart so neighbouring windows never overlap (gap ≥ 2×110 ms is respected). Suggest the engine accept early taps only after the previous corner has been passed.'}
START_HEADING='N'
SPEED=[(0,10.2)]
WIDTH=[(0,2.2),(71.95,2.0),(114.94,2.2),(141.80,2.0),(157.92,1.8),(179.42,2.2)]
T_='k..k..k.k..k..k.'   # tresillo-ish 3+3+2+3+3+2 on the Baltimore kick/snare
SECTIONS=[
 dict(b0=0,b1=8,kind='intro',label='Intro · 录像带入口',pats=['m.......m.......'],
      over={0:'............v...',1:'.......v........',7:'m.......m...m.m.'}),
 dict(b0=8,b1=16,kind='verse',label='Verse 1 · 教室走廊',pats=['s.....s....s..s.'],
      over={15:'s.s.s...s.s.s.s.'}),
 dict(b0=16,b1=24,kind='chorus',label='Chorus 1 · 摄像机取景框',pats=['k...k...k..k..k.','k...k...k.....k.'],
      over={20:'k.k.k.k.k..k..k.',23:'k.k.k.k.k.k...k.'}),
 dict(b0=24,b1=31,kind='post',label='Post 1 · 屋顶坡道',pats=['s...s...s...s.s.','s.......s...s.s.']),
 dict(b0=31,b1=36,kind='break',label='Break · 雪地鹿岛',auto=dict(src=['vocals'],thr=0.35,minsteps=4,c='v')),
 dict(b0=36,b1=40,kind='verse',label='Verse 2a · 雾隙',auto=dict(src=['vocals'],thr=0.45,minsteps=4,c='v',ban=[2,3,10,11]),pats=['....s.......s...']),
 dict(b0=40,b1=48,kind='verse',label='Verse 2 · 窗墙长 U',pats=[T_,'k.......k.....k.','k...k.....k...k.','k.......k.....k.']),
 dict(b0=48,b1=56,kind='chorus',label='Chorus 2 · 屋顶空椅',pats=[T_,'k.....k.k.....k.',T_,'k...k.....k...k.'],over={55:'k.k.k.k.k..k..k.'}),
 dict(b0=56,b1=64,kind='post',label='Post 2 · 跨空桥',pats=[T_,'k.......k.....k.','k...k.....k...k.','k.k.k...k..k..k.'],over={63:'....k.....k.....'}),
 dict(b0=64,b1=72,kind='bridge',label='Bridge · 鹿回头',auto=dict(src=['vocals'],thr=0.3,minsteps=3,c='v')),
 dict(b0=72,b1=79,kind='pre',label='Pre · 取景屏',auto=dict(src=['vocals'],thr=0.4,minsteps=4,c='v',ban=[2,3,10,11]),pats=['....s.......s...']),
 dict(b0=79,b1=88,kind='chorus',label='Final chorus · 记忆庭院',pats=[T_,'k.....k.k.....k.',T_,'k.k.k.k.k..k..k.'],over={79:'k.k.k.k..k..s.s.'}),
 dict(b0=88,b1=96,kind='chorus',label='Final post · 网点兔',pats=[T_,'k.....k.k.....k.',T_,'k...k...k..k..k.']),
 dict(b0=96,b1=100,kind='outro',label='Fade · 暖窗熄灭',pats=['k...k.....k.....','k.......k.......']),
 dict(b0=100,b1=104,kind='outro',label='Outro · 录像带合上',pats=['................'],over={100:'s...........s...',101:'.....s..........'}),
]
NOTES=('134.0 BPM grid fitted to the drum stem (brute-force bpm/phase, per-20 s residual ≤ 4 ms). Patterns read from per-bar stem onset maps; '
       'the Baltimore/Jersey-club kick of the choruses is charted as a 3+3+2+3+3+2 (tresillo) 16th pattern, the iconic jersey kick K...|K...|K..K|..K. '
       'in Chorus 1 as 0,4,8,11,14. Drumless passages (break, bridge) follow the sung syllables (vocal stem, quantized to 16ths, ≥ 1 beat apart).')
MOTIFS=[(0,'stair'),(14.64,'meander'),(28.97,'stair'),(71.95,'stair'),(86.28,'stair'),(114.94,'stair'),(141.80,'stair')]
PIVOTS=[14.7,22.0,29.0,36.2,43.4,55.9,64.8,72.0,79.2,86.3,93.5,100.7,107.9,115.0,122.1,129.3,135.5,141.9,149.0,157.9,165.1,172.3,179.4]
ELEV=[dict(t0=43.5,t1=55.6,type='ramp',dy=3),dict(t=55.83,type='fall',dy=-7),dict(t0=72.0,t1=86.0,type='ramp',dy=6),
      dict(t=114.94,type='fall',dy=-6),dict(t0=129.4,t1=141.6,type='ramp',dy=4),dict(t=157.92,type='jump',dy=3),dict(t=172.25,type='fall',dy=-3)]
COMPACT=1.0
def layout(c):
    bar=c['bar']; g=c['gap_mid']
    P=dict(skyTop='#bcd3ea',skyBottom='#f2efe8',fog='#e6ecf2',fogStart=30,fogEnd=95,ground='#e9eef3',groundY=-12,
           road='#ffffff',roadSide='#a9b9c9',line='#2f5f8f',light='#fff4e2',lightIntensity=1.05,ambient='#b9c7d6',particles='snow')
    secs=[
     dict(t=0,label='Intro · 录像带入口',palette=dict(skyTop='#2b2f3a',skyBottom='#59606e',fog='#3a404c',ground='#2a2e36',road='#e9e4d8',roadSide='#7d7768',light='#ffe2b0',lightIntensity=0.8,particles='dust'),camera='close',note='dark room, camcorder + tape; road unspools like tape ribbon'),
     dict(t=bar(8),label='Verse 1 · 教室走廊',palette=dict(skyTop='#bcd3ea',particles='snow'),camera='iso',note='snowy school yard, locker corridor rows react to taps'),
     dict(t=bar(16),label='Chorus 1 · 摄像机取景框',palette=dict(road='#fdf6ec',roadSide='#d39b62',ground='#dfe6ec'),camera='high',note='open basketball court, jersey-kick staircase'),
     dict(t=bar(24),label='Post 1 · 屋顶坡道',camera='side',note='road climbs the bleachers (+3)'),
     dict(t=bar(31),label='Break · 雪地鹿岛',palette=dict(skyTop='#e8eef5',skyBottom='#ffffff',fog='#f4f7fb',fogStart=20,fogEnd=70,ground='#ffffff',roadSide='#c8d4e0'),camera='wide',note='fall off the bleachers into a white snowfield; deer on the horizon'),
     dict(t=bar(36),label='Verse 2a · 雾隙',camera='low'),
     dict(t=bar(40),label='Verse 2 · 窗墙长 U',palette=dict(skyTop='#a9c3dc',road='#ffffff',roadSide='#8fa6bd'),camera='iso',note='second locker corridor, ramping up to the roof'),
     dict(t=bar(48),label='Chorus 2 · 屋顶空椅',palette=dict(skyTop='#9fbfe0',skyBottom='#f7e9dc',light='#ffe8cc'),camera='high'),
     dict(t=bar(56),label='Post 2 · 跨空桥',camera='side'),
     dict(t=bar(64),label='Bridge · 鹿回头',palette=dict(skyTop='#5f7896',skyBottom='#c9d6e3',fog='#9fb0c4',ground='#f3f6fa',light='#dbe6ff',lightIntensity=0.8),camera='low',note='blue-hour snowfield, deer turns its head'),
     dict(t=bar(72),label='Pre · 取景屏',palette=dict(skyTop='#7f98b4'),camera='iso',note='film-frame gates over the road'),
     dict(t=bar(79),label='Final chorus · 记忆庭院',palette=dict(skyTop='#bcd3ea',skyBottom='#fff3e6',light='#fff0d8',lightIntensity=1.15),camera='iso'),
     dict(t=bar(88),label='Final post · 网点兔',camera='high'),
     dict(t=bar(96),label='Fade · 暖窗熄灭',palette=dict(skyTop='#3a3f4c',skyBottom='#6c7280',light='#ffe2b0',lightIntensity=0.8,particles='dust'),camera='close'),
     dict(t=bar(100),label='Outro · 录像带合上',camera='top'),
    ]
    cam=[dict(t=0,preset='close',blend=0),dict(t=bar(8),preset='iso',blend=2.5),dict(t=bar(16),preset='high',blend=1.2),dict(t=bar(24),preset='side',blend=2.0),
         dict(t=bar(31),preset='wide',blend=1.0),dict(t=bar(36),preset='low',blend=2.5),dict(t=bar(40),preset='iso',blend=1.5),dict(t=bar(48),preset='high',blend=1.2),
         dict(t=bar(56),preset='side',blend=2.0),dict(t=bar(64),preset='low',blend=3.0),dict(t=bar(68),preset='wide',blend=3.0),dict(t=bar(72),preset='iso',blend=2.0),
         dict(t=bar(79),preset='iso',blend=0.8,shake=0.1),dict(t=bar(88),preset='high',blend=1.5),dict(t=bar(96),preset='close',blend=3.0),dict(t=bar(100),preset='top',dist=24,blend=4.0)]
    O=[]
    O.append(dict(id='camcorder',t=1.2,side=6,along=4,kind='group',radius=3,landmark=True,name='老摄像机',
                  parts=[dict(kind='box',pos=[0,1.2,0],size=[2.2,1.6,3.6],color='#3a3a3a'),dict(kind='cylinder',pos=[0,1.2,2.3],size=[1.2,1.2,1.2],rot=[90,0,0],color='#222'),
                         dict(kind='sphere',pos=[0.7,2.1,1.2],size=[0.25,0.25,0.25],color='#ff2a2a')],appear=dict(t=0.4,mode='fade',dur=1.0)))
    O.append(dict(id='tape',t=6.0,side=-6,kind='cassette',size=[4,0.6,2.6],color='#2a2a2a',color2='#f2efe8',landmark=True,name='磁带',appear=dict(t=4.5,mode='drop',dur=0.8)))
    O.append(dict(id='lockers1',kind='row',t0=bar(8),t1=bar(16),side=2.1,spacing=1.4,bothSides=True,
                  item=dict(kind='box',size=[1.2,3.2,0.9],color='#7fa4c8',color2='#5d84ab',react='tap')))
    O.append(dict(id='school',t=bar(11),side=-22,kind='group',radius=8,landmark=True,name='雪中校舍',
                  parts=[dict(kind='box',pos=[0,4,0],size=[18,8,8],color='#efe7da'),dict(kind='box',pos=[0,8.6,0],size=[18.6,1.2,8.6],color='#ffffff'),
                         dict(kind='box',pos=[0,10.5,0],size=[3,3,3],color='#efe7da'),dict(kind='disc',pos=[0,10.5,1.55],size=[2,2,2],color='#ffffff')],
                  appear=dict(t=bar(9),mode='rise',dur=1.5)))
    O.append(dict(id='hoop',t=bar(18),side=9,kind='group',radius=2,landmark=True,name='篮球架',
                  parts=[dict(kind='cylinder',pos=[0,2.5,0],size=[0.3,5,0.3],color='#666'),dict(kind='box',pos=[0,5.4,-0.6],size=[2.4,1.6,0.15],color='#ffffff'),
                         dict(kind='torus',pos=[0,4.8,-1.1],size=[0.9,0.1,0.9],color='#e86a2a')],appear=dict(t=bar(16)-1,mode='rise',dur=0.8),react='kick'))
    O.append(dict(id='court',t=bar(20),side=0,y=-0.35,kind='plane',size=[34,1,34],color='#e8b07a',onroad=True,name='球场地面 (under road)'))
    O.append(dict(id='bleachers',t=bar(27),side=-10,kind='stairs',size=[10,5,6],color='#9fb3c8',landmark=True,name='看台',appear=dict(t=bar(24),mode='unfold',dur=1.2)))
    O.append(dict(id='deer',t=bar(33),side=-18,along=10,kind='group',radius=3,landmark=True,name='雪原上的鹿',
                  parts=[dict(kind='box',pos=[0,1.6,0],size=[2.2,1,0.8],color='#8b6a4e'),dict(kind='box',pos=[1.1,2.4,0],size=[0.5,1.2,0.5],color='#8b6a4e'),
                         dict(kind='box',pos=[1.4,3.0,0],size=[0.8,0.5,0.5],color='#8b6a4e'),dict(kind='box',pos=[-0.8,0.6,0.25],size=[0.2,1.2,0.2],color='#6d523c'),
                         dict(kind='box',pos=[0.8,0.6,0.25],size=[0.2,1.2,0.2],color='#6d523c'),dict(kind='box',pos=[1.4,3.7,0],size=[0.1,0.9,0.9],rot=[0,0,15],color='#d9c6a8')],
                  appear=dict(t=bar(32),mode='fade',dur=2.0),exit=dict(t=bar(36),mode='fade',dur=2.0)))
    for i in range(6):
        O.append(dict(id=f'footprint{i}',t=bar(36)+i*1.2,side=-2.2,y=-0.3,kind='disc',size=[0.5,0.05,0.8],color='#c8d4e0',appear=dict(t=bar(36)+i*1.2,mode='fade',dur=0.3)))
    O.append(dict(id='lockers2',kind='row',t0=bar(40),t1=bar(48),side=2.0,spacing=1.4,bothSides=True,
                  item=dict(kind='box',size=[1.2,3.4,0.9],color='#e7b7a3',color2='#c98f78',react='tap')))
    O.append(dict(id='watertower',t=bar(58),side=11,kind='group',radius=4,landmark=True,name='天台水塔',
                  parts=[dict(kind='cylinder',pos=[0,6,0],size=[4,3.5,4],color='#d9e2ea'),dict(kind='cone',pos=[0,8.3,0],size=[4.4,1.2,4.4],color='#9fb3c8'),
                         dict(kind='box',pos=[-1.4,2.2,0],size=[0.3,4.4,0.3],color='#888'),dict(kind='box',pos=[1.4,2.2,0],size=[0.3,4.4,0.3],color='#888')],
                  appear=dict(t=bar(56),mode='rise',dur=1.4)))
    O.append(dict(id='deer2',t=bar(67),side=14,along=6,kind='group',radius=3,landmark=True,name='回头的鹿 (head turns at 2:00)',
                  parts=[dict(kind='box',pos=[0,1.6,0],size=[2.2,1,0.8],color='#8b6a4e'),dict(kind='box',pos=[1.1,2.4,0],size=[0.5,1.2,0.5],color='#8b6a4e'),
                         dict(kind='box',pos=[1.4,3.0,0],size=[0.8,0.5,0.5],rot=[0,-60,0],color='#8b6a4e')],
                  appear=dict(t=bar(65),mode='fade',dur=2.0)))
    for i in range(7):
        t=bar(72)+i*1.79+0.9
        O.append(dict(id=f'filmgate{i}',t=t,side=0,kind='arch',size=[7,6,0.4],color='#1f1f1f',color2='#f2efe8',onroad=True,name='film frame gate (spans road, top at y=6)',
                      appear=dict(t=t-1.4,mode='drop',dur=0.5),exit=dict(t=t+1.5,mode='sink',dur=0.5)))
    O.append(dict(id='reel_l',t=bar(84),side=-12,kind='group',radius=5,landmark=True,name='磁带卷轴',
                  parts=[dict(kind='cylinder',pos=[0,1,0],size=[8,0.6,8],color='#2a2a2a'),dict(kind='cylinder',pos=[0,1.4,0],size=[2,0.6,2],color='#f2efe8')],react='beat',
                  appear=dict(t=bar(79),mode='rise',dur=1.0)))
    O.append(dict(id='reel_r',t=bar(92),side=12,kind='group',radius=5,
                  parts=[dict(kind='cylinder',pos=[0,1,0],size=[8,0.6,8],color='#2a2a2a'),dict(kind='cylinder',pos=[0,1.4,0],size=[2,0.6,2],color='#f2efe8')],react='beat',
                  appear=dict(t=bar(88),mode='rise',dur=1.0)))
    O.append(dict(id='room_tv',t=bar(101),side=7,kind='group',radius=3,landmark=True,name='小屏幕里的录像',
                  parts=[dict(kind='box',pos=[0,1.5,0],size=[3,2.4,2],color='#2b2b2b'),dict(kind='plane',pos=[0,1.6,-1.01],size=[2.4,1.8,1],color='#bcd3ea')]))
    O.append(dict(id='egg_cards',t=bar(13),side=-6,kind='group',radius=1.5,egg=True,name='A/B 小卡 (two MV versions)',
                  parts=[dict(kind='box',pos=[-0.6,1.6,0],size=[1,1.3,0.05],rot=[0,0,-6],color='#fff7e6'),dict(kind='box',pos=[0.6,1.6,0],size=[1,1.3,0.05],rot=[0,0,6],color='#e6f0ff')]))
    O.append(dict(id='egg_redlight',t=bar(102),side=-5,kind='group',radius=1.5,egg=True,name='红点仍亮 + 兔耳贴纸',
                  parts=[dict(kind='box',pos=[0,0.8,0],size=[1.4,1,2],color='#3a3a3a'),dict(kind='sphere',pos=[0.5,1.4,0.6],size=[0.2,0.2,0.2],color='#ff2a2a'),
                         dict(kind='box',pos=[-0.3,1.31,0],size=[0.15,0.02,0.5],color='#ffffff'),dict(kind='box',pos=[0.0,1.31,0],size=[0.15,0.02,0.5],color='#ffffff')]))
    ev=[dict(t=bar(8),type='light',target='school',dur=2.0),dict(t=bar(16),type='flash',dur=0.2),
        dict(t=bar(31),type='color',palette=dict(skyTop='#e8eef5',skyBottom='#ffffff'),dur=1.5),dict(t=bar(31),type='particles',particles='snow',dur=20),
        dict(t=bar(48),type='burst',at='player',particles='snow'),dict(t=bar(66),type='spin',target='deer2',dur=1.2),
        dict(t=bar(79),type='flash',dur=0.25),dict(t=bar(79),type='spin',target='reel_l',every=c['T'],until=bar(96)),
        dict(t=bar(96),type='color',palette=dict(skyTop='#3a3f4c'),dur=3.0)]
    cr=[g(x,1.0) for x in CROWN_T(bar)]
    dia=[g(t,0.5) for t in [bar(5),bar(13),bar(26),bar(33),bar(45),bar(60),bar(67),bar(76),bar(90),bar(98)]]
    return dict(id='ditto',title='Ditto',palette=P,road=dict(height=0.6,reveal=[dict(t=0,mode='unfold',lead=2.0),dict(t=bar(8),mode='rise',lead=1.8),
                dict(t=bar(31),mode='fade',lead=2.0),dict(t=bar(40),mode='rise',lead=1.6),dict(t=bar(64),mode='fade',lead=2.0),dict(t=bar(79),mode='rise',lead=1.4)]),
                sections=secs,camera=cam,objects=O,events=ev,diamonds=[dict(t=t,side=0) for t in dia],
                crowns=[dict(t=x) for x in cr],finish=dict(kind='custom',note='tape slot: line enters a giant cassette',parts=[dict(kind='cassette',pos=[0,0,4],size=[8,1.2,5],color='#2a2a2a')]))
WHY={
 'Intro (0–14.6 s)':'choir/pad only: 2 taps per bar on the chord changes (beats 1 and 3) — 1 s+ gaps, the camcorder room.',
 'Verse 1 (14.6–29.0 s)':'busy Baltimore hat/snare layer (S at steps 0, 5-6, 11, 14): taps on those snare accents (0,6,11,14) → syncopated, with bar 15 an 8-tap 8th fill into the chorus.',
 'Chorus 1 (29.0–43.3 s)':'the iconic jersey-club kick K...|K...|K..K|..K. charted exactly (0,4,8,11,14); bars 20 and 23 add the kick-roll 8ths (7-tap runs).',
 'Post 1 (43.3–55.8 s)':'snare-led 16th groove: taps on the loud snares (0,4,6,9,12,14 / 0,4,8,12,14) — 3–3.4 taps/s while the road climbs the bleachers.',
 'Break & Verse 2a (55.8–72.0 s)':'drums cut out: taps follow the sung syllables (vocal stem onsets, ≥ 1 beat apart), then the light claps on 2 and 4 return — the breathing room (≈1 tap/s).',
 'Verse 2 / Chorus 2 / Post 2 (72.0–114.9 s)':'full Baltimore beat: 3+3+2+3+3+2 sixteenth pattern (steps 0,3,6,8,11,14) following kick+snare, alternating with lighter 3–4-tap bars every other bar so phrases breathe; 7-tap 8th roll at 98.8 s.',
 'Bridge & Pre (114.9–141.8 s)':'drumless vocal bridge, then claps on 2/4 with the vocal line — low density before the finale.',
 'Final chorus / post (141.8–172.3 s)':'tresillo pattern + 8th-note kick rolls every 4th bar on a 1.8-wide road — hardest part.',
 'Fade & outro (172.3–185.5 s)':'beat thins and fades: 5→2 taps per bar, last taps on the final snare hits.',
}

# ---- v2 layout aligned with codex-ref (Ditto — 冬日录像带): grey-green campus in fog, coral line, cassette start/end
def layout(c):
    bar=c['bar']; g=c['gap_mid']; T=c['T']
    P=dict(skyTop='#DCE3DF',skyBottom='#EEF1EE',fog='#DCE3DF',fogStart=26,fogEnd=88,ground='#DCE3DF',groundY=-12,
           road='#F2F0E7',roadSide='#788A80',line='#C85F65',light='#FFF7EA',lightIntensity=1.0,ambient='#C3CCC7',particles='snow')
    secs=[
     dict(t=0,label='Intro · 录像带入口',palette=dict(fogEnd=60,particles=None),camera='low',note='cassette-box island; isolated wall slabs rise with the choir; distant warm window answers the hook'),
     dict(t=bar(8),label='Verse 1 · 教室走廊',camera='iso',note='narrow corridor around three classrooms (meander); a window opens per phrase; locker rows react to taps'),
     dict(t=bar(16),label='Chorus 1 · 摄像机取景框',camera='high',note='giant silver camcorder, flip screen opens; staircase on the jersey kick'),
     dict(t=bar(24),label='Post 1 · 屋顶坡道',camera='side',note='ramp H0->H1 (+3) toward the roof; crown C1 waits after the fall'),
     dict(t=bar(31),label='Break · 雪地鹿岛',palette=dict(skyTop='#E9EEEB',skyBottom='#FFFFFF',fog='#EEF2EF',fogStart=18,fogEnd=64,ground='#F4F6F3'),camera='wide',note='drums cut: drop 7 units into fog gap; snow island with the deer off-road'),
     dict(t=bar(36),label='Verse 2a · 雾隙',camera='low'),
     dict(t=bar(40),label='Verse 2 · 窗墙长 U',camera='iso',note='window walls unfold in canon; ramp up 6 to the roof'),
     dict(t=bar(48),label='Chorus 2 · 屋顶空椅',palette=dict(skyBottom='#F4EEE4',light='#FFF0DA'),camera='high',note='rooftop courtyard with five empty chairs; outer walls fold out on the hook'),
     dict(t=bar(56),label='Post 2 · 跨空桥',camera='side',note='bridge B1 across the fog void'),
     dict(t=bar(64),label='Bridge · 鹿回头',palette=dict(skyTop='#B9C4BF',skyBottom='#DDE3E0',fog='#C5CEC9',lightIntensity=0.85),camera='low',note='fall 6 back to the snow level; deer slowly turns its head at the phrase end'),
     dict(t=bar(72),label='Pre · 取景屏',camera='iso',note='off-road camcorder screen shows a sixth chair (E1); claps on 2 and 4'),
     dict(t=bar(79),label='Final chorus · 记忆庭院',palette=dict(skyTop='#DCE3DF',light='#FFF4E0',lightIntensity=1.1),camera='iso',note='window walls return in canon order, halftone bunny relief panel appears off-road'),
     dict(t=bar(88),label='Final post · 网点兔',camera='high',note='jump +3 to the courtyard rim, road narrows to 1.8'),
     dict(t=bar(96),label='Fade · 暖窗熄灭',palette=dict(skyTop='#C9D1CD',lightIntensity=0.85,particles=None),camera='close',note='warm windows go out one by one'),
     dict(t=bar(100),label='Outro · 录像带合上',camera='top',note='long straight west into the cassette end box, which slowly closes'),
    ]
    cam=[dict(t=0,preset='low',blend=0),dict(t=bar(8),preset='iso',blend=2.5),dict(t=bar(16),preset='high',blend=1.2),dict(t=bar(24),preset='side',blend=2.0),
         dict(t=bar(31),preset='wide',blend=1.0),dict(t=bar(36),preset='low',blend=2.5),dict(t=bar(40),preset='iso',blend=1.5),dict(t=bar(48),preset='high',dist=21,blend=1.2),
         dict(t=bar(56),preset='side',blend=2.0),dict(t=bar(64),preset='low',blend=3.0),dict(t=bar(68),preset='wide',blend=3.0),dict(t=bar(72),preset='iso',blend=2.0),
         dict(t=bar(79),preset='iso',blend=0.8,shake=0.08),dict(t=bar(88),preset='high',blend=1.5),dict(t=bar(96),preset='close',blend=3.0),dict(t=bar(100),preset='top',dist=24,blend=4.0)]
    O=[]
    O.append(dict(id='cassette_start',t=1.0,side=0,along=-3,y=-0.9,kind='cassette',size=[9,1.2,6],color='#272D32',color2='#F2F0E7',onroad=True,landmark=True,name='录像带入口 (the start platform is a cassette box)'))
    for i in range(4):
        t=2+i*3.2
        O.append(dict(id=f'wallslab{i}',t=t,side=(6 if i%2==0 else -6),kind='box',size=[0.6,5,4],color='#788A80',appear=dict(t=t-1.2,mode='rise',dur=1.0)))
    O.append(dict(id='warm_window',t=bar(6),side=-20,along=10,y=3,kind='box',size=[3,2,0.3],color='#D8BE93',name='远处暖窗',appear=dict(t=bar(6),mode='fade',dur=1.5)))
    O.append(dict(id='lockers1',kind='row',t0=bar(8),t1=bar(16),side=2.1,spacing=1.4,bothSides=True,item=dict(kind='box',size=[1.2,3.2,0.9],color='#788A80',color2='#AEB7BA',react='tap')))
    for i in range(3):
        O.append(dict(id=f'classroom{i}',t=bar(9)+i*4.2,side=-9,kind='group',radius=4,
                      parts=[dict(kind='box',pos=[0,2.5,0],size=[7,5,6],color='#788A80'),dict(kind='box',pos=[3.55,2.8,0],size=[0.1,1.8,4.6],color='#D8BE93')],
                      appear=dict(t=bar(8)+i*4.2,mode='rise',dur=1.0)))
    O.append(dict(id='camcorder',t=bar(18),side=-10,kind='group',radius=5,landmark=True,name='银色摄像机与翻折屏',
                  parts=[dict(kind='box',pos=[0,2.5,0],size=[4,4,7],color='#AEB7BA'),dict(kind='cylinder',pos=[0,2.5,4.4],size=[3,2,3],rot=[90,0,0],color='#272D32'),
                         dict(kind='box',pos=[2.6,2.8,0],size=[0.3,2.4,3.6],color='#272D32'),dict(kind='box',pos=[2.76,2.8,0],size=[0.05,2.0,3.2],color='#DCE3DF'),
                         dict(kind='box',pos=[-2.05,2.2,0],size=[0.15,0.8,4.2],color='#FFFFFF')],
                  appear=dict(t=bar(16)-1,mode='rise',dur=1.2)))
    O.append(dict(id='roof_ramp_rail',t=bar(27),side=-4,kind='stairs',size=[2,3,8],color='#AEB7BA'))
    O.append(dict(id='deer',t=bar(33),side=-16,along=8,kind='group',radius=4,landmark=True,name='雪地鹿岛',
                  parts=[dict(kind='box',pos=[0,-1,0],size=[9,3,8],color='#788A80'),dict(kind='box',pos=[0,0.55,0],size=[9.2,0.3,8.2],color='#F4F6F3'),
                         dict(kind='box',pos=[0,2.0,0],size=[2.2,1,0.8],color='#8A7F74'),dict(kind='box',pos=[1.1,2.8,0],size=[0.5,1.2,0.5],color='#8A7F74'),
                         dict(kind='box',pos=[1.4,3.4,0],size=[0.8,0.5,0.5],color='#8A7F74'),dict(kind='box',pos=[-0.8,1.1,0.25],size=[0.2,1.0,0.2],color='#6E655C'),
                         dict(kind='box',pos=[0.8,1.1,0.25],size=[0.2,1.0,0.2],color='#6E655C'),dict(kind='cone',pos=[-3,2.2,2],size=[0.3,3,0.3],color='#5C5650')],
                  appear=dict(t=bar(31),mode='fade',dur=2.0)))
    for i in range(5):
        t=bar(41)+i*2.8
        O.append(dict(id=f'windowwall{i}',t=t,side=(5 if i%2==0 else -5),kind='box',size=[0.5,5,4.5],color='#788A80',color2='#D8BE93',appear=dict(t=t-1.6,mode='unfold',dur=0.5)))
    O.append(dict(id='roof_chairs',t=bar(50),side=9,kind='group',radius=4,landmark=True,name='屋顶空椅组 (five chairs)',
                  parts=[dict(kind='box',pos=[0,-0.3,0],size=[8,0.6,7],color='#F2F0E7')]+[dict(kind='box',pos=[x,0.5,z],size=[0.6,1.0,0.6],color='#272D32') for x,z in [(-2.5,-1),(-1,1.5),(0.5,-1.5),(2,1),(2.8,-0.5)]],
                  react='none'))
    O.append(dict(id='bridge_b1',t=bar(58),side=0,y=-1.2,kind='bridge',size=[3,1,24],color='#F2F0E7',onroad=True,name='跨空桥 B1 (under-road truss across the fog)',landmark=True))
    O.append(dict(id='deer_turn',t=bar(67),side=14,along=6,kind='group',radius=3,landmark=True,name='回头的鹿',
                  parts=[dict(kind='box',pos=[0,1.6,0],size=[2.2,1,0.8],color='#8A7F74'),dict(kind='box',pos=[1.1,2.4,0],size=[0.5,1.2,0.5],color='#8A7F74'),
                         dict(kind='box',pos=[1.4,3.0,0],size=[0.8,0.5,0.5],color='#8A7F74')],appear=dict(t=bar(65),mode='fade',dur=2.0)))
    O.append(dict(id='screen_e1',t=bar(75),side=-8,kind='group',radius=2.5,egg=True,name='E1 取景屏里的第六把椅子',
                  parts=[dict(kind='box',pos=[0,1.4,0],size=[0.3,2.2,3.4],color='#272D32'),dict(kind='box',pos=[0.16,1.4,0],size=[0.05,1.9,3.0],color='#DCE3DF'),
                         dict(kind='box',pos=[0.2,1.0,0.6],size=[0.05,0.5,0.35],color='#272D32')],appear=dict(t=bar(74),mode='fade',dur=1.0)))
    O.append(dict(id='halftone_bunny',t=bar(86),side=12,y=0,kind='group',radius=4,landmark=True,name='网点兔浮雕 (OMG cover, black/white halftone)',
                  parts=[dict(kind='box',pos=[0,3,0],size=[0.4,5,5],color='#272D32')]+[dict(kind='box',pos=[-0.22,1.2+r*0.6,-2+c_*0.6],size=[0.05,0.3,0.3],color='#F2F0E7') for r in range(6) for c_ in range(7) if (r*7+c_)%3!=0],
                  appear=dict(t=bar(84),mode='rise',dur=1.4)))
    for i in range(5):
        O.append(dict(id=f'warmwin{i}',t=bar(96)+i*1.4,side=(-7 if i%2==0 else 7),y=2,kind='box',size=[2,1.5,0.3],color='#D8BE93',exit=dict(t=bar(96)+i*1.4+0.5,mode='fade',dur=0.6)))
    O.append(dict(id='cassette_end',t=bar(102),side=0,along=6,y=-0.9,kind='cassette',size=[9,1.2,6],color='#272D32',color2='#F2F0E7',onroad=True,landmark=True,name='录像带终点盒 (closes after finish)'))
    O.append(dict(id='egg_wristband',t=bar(19),side=-6.5,y=0,kind='group',radius=1,egg=True,name='摄像机握带上的白色护腕 (cast-arm nod)',
                  parts=[dict(kind='torus',pos=[0,0.4,0],size=[0.8,0.25,0.8],color='#FFFFFF')]))
    ev=[dict(t=bar(2),type='light',target='warm_window',dur=2.0),dict(t=bar(16),type='flash',dur=0.2),
        dict(t=bar(31),type='color',palette=dict(skyTop='#E9EEEB',skyBottom='#FFFFFF'),dur=1.5),dict(t=bar(48),type='burst',at='player',particles='snow'),
        dict(t=bar(70),type='spin',target='deer_turn',dur=1.6),dict(t=bar(79),type='flash',dur=0.25),
        dict(t=bar(96),type='color',palette=dict(skyTop='#C9D1CD'),dur=3.0)]
    cr=[g(x,1.0) for x in CROWN_T(bar)]
    dia=[g(t,0.5) for t in [bar(5),bar(13),bar(26),bar(33),bar(45),bar(60),bar(67),bar(76),bar(90),bar(98)]]
    return dict(id='ditto',title='Ditto',palette=P,road=dict(height=0.6,reveal=[dict(t=0,mode='rise',lead=2.0),dict(t=bar(8),mode='rise',lead=1.8),
                dict(t=bar(31),mode='fade',lead=2.0),dict(t=bar(40),mode='unfold',lead=1.6),dict(t=bar(64),mode='fade',lead=2.0),dict(t=bar(79),mode='rise',lead=1.4)]),
                sections=secs,camera=cam,objects=O,events=ev,diamonds=[dict(t=t,side=0) for t in dia],
                crowns=[dict(t=x) for x in cr],finish=dict(kind='custom',note='line enters the cassette end box',parts=[dict(kind='cassette',pos=[0,0,4],size=[8,1.2,5],color='#272D32')]),
                collectibleColors=dict(diamond='#87CBCD',crown='#D9B56B'))

CROWN_T=lambda bar: [bar(33),bar(70)]

# ---- v3 route choreography (2026-10-18 "routes too simple"). Overrides MOTIFS/PIVOTS/ELEV above.
_b=lambda n: 0.311+n*1.791045
ELEV=[dict(t0=_b(24.1),t1=_b(30.8),type='ramp',dy=3),        # Post 1: staggered folds climb to the roof (+3)
      dict(t=_b(31),type='fall',dy=-7),                      # Break: drop into the fog gap, snow island (-4)
      dict(t0=_b(40),t1=_b(47.8),type='ramp',dy=6),          # Verse 2: long-U window walls climb to the rooftop (+2)
      dict(t0=_b(56.2),t1=_b(60),type='ramp',dy=4),          # Post 2: bridge B1 climbs (+6) over Chorus 1
      dict(t=_b(64),type='fall',dy=-4),                      # Bridge (+2)
      dict(t0=_b(66),t1=_b(68.5),type='ramp',dy=-8),         # Bridge: spiral DOWN around the deer island (-6)
      dict(t0=_b(72.1),t1=_b(78.8),type='ramp',dy=4),        # Pre: climb back (-2)
      dict(t=_b(79),type='jump',dy=4),                       # Final chorus: jump onto the memory courtyard (+2)
      dict(t=_b(88),type='jump',dy=3),                       # Final post: courtyard rim (+5)
      dict(t=_b(96),type='fall',dy=-5)]                      # Fade: back to 0
A=lambda w=0.6,**k: dict(w_aim=w,**k)
ROUTE=[(0,'free',0,A(1.0)),(_b(4),'free',270,A(1.0)),                                   # Intro: long legs out of the cassette box
       (_b(8),'switch',90,A(0.25,thr=0.5)),(_b(12),'meander',180,A(0.35)),              # Verse 1: corridor U around the classrooms
       (_b(16),'stair',45,A()),(_b(18),'stair',315,A()),(_b(20),'stair',45,A()),(_b(22),'stair',315,A()),   # Chorus 1: Baltimore zigzag of stairs
       (_b(24),'switch',270,A(0.3,thr=0.4)),                                             # Post 1: staggered short folds up the roof ramp
       (_b(31),'free',180,A(1.0)),                                                       # Break: long legs on the snow island
       (_b(36),'meander',90,A(0.4)),
       (_b(40),'switch',0,A(0.3,thr=0.45)),                                              # Verse 2: long switchbacks along the window wall
       (_b(48),'stair',90,A()),(_b(50),'stair',180,A()),(_b(52),'stair',270,A()),(_b(54),'stair',0,A()),     # Chorus 2: staircase ring round the empty chairs
       (_b(56),'free',225,A(1.2,cross=1.5)),(_b(60),'stair',225,A(0.6,cross=1.5)),      # Post 2: bridge B1 sweeps over Chorus 1
       (_b(64),'switch',135,A(0.3,thr=0.45)),(_b(66),'spiral',None,A(0,hand='L',w_motif=2.5)),(_b(68.5),'stair',90,A()),   # Bridge: spiral down round the deer
       (_b(72),'free',270,A(1.0)),                                                       # Pre: long viewfinder legs (E1 screen)
       (_b(79),'switch',0,A(0.3,thr=0.3,cross=1.0)),(_b(83),'stair',300,A(0.6,cross=1.5)),   # Final chorus: unequal return folds, over the break
       (_b(88),'meander',60,A(0.4,cross=1.0)),(_b(92),'stair',150,A(0.6,cross=1.5)),
       (_b(96),'free',270,A(1.0))]                                                       # Fade/outro: long straight-ish west to the end box
FORKS=[_b(10.5),_b(26.3),_b(42.5),_b(61.2),_b(74.6),_b(90.4),_b(97.5)]
BUILDINGS=[dict(id='classrooms',t0=_b(8.2),t1=_b(11.8),color='#E4E8E3',h=3.0),     # Verse 1 switchbacks wind through the cut-away classroom block
           dict(id='rooftop_hut',t0=_b(48.3),t1=_b(49.9),color='#F2F0E7',h=2.6)]
ART={'backdrop':'art/sky.jpg','ground':{'src':'art/ground-snow.jpg','scale':30},
     'files':{'art/sky.jpg':'misty grey-green winter sky, falling snow specks, far pine silhouettes, warm window glow (backdrop)',
              'art/ground-snow.jpg':'chalk-white snow grain tile (ground)',
              'art/cassette-label.jpg':'cassette label: coral/green stripes, reels, no text (texture on the cassette start/end boxes)',
              'art/camcorder-screen.jpg':'flip-screen image: rooftop with SIX chairs, scanlines, REC dot (egg E1 screen)',
              'art/deer-decal.png':'grey-green deer silhouette sticker, transparent (snow island)',
              'art/halftone-bunny-relief.jpg':'halftone bunny relief (OMG cover motif) for the final-chorus wall'}}
def more_objects(c):
    bar=c['bar']
    return [dict(id='cassette_label_start',t=1.0,side=-6,y=0.1,kind='image',src='art/cassette-label.jpg',size=[6,0,3.75],mode='flat'),
            dict(id='cam_screen_e1',t=bar(75),side=-8,y=2.5,kind='image',src='art/camcorder-screen.jpg',size=[6.4,0,4],mode='upright',egg=True,
                 name='E1 camcorder screen: the rooftop with a sixth chair',appear=dict(t=bar(74),mode='unfold',dur=0.6)),
            dict(id='deer_sticker',t=bar(33),side=9,y=0,kind='image',src='art/deer-decal.png',size=[5,0,5],mode='billboard',alpha=True,appear=dict(t=bar(31)+0.5,mode='fade',dur=1.0)),
            dict(id='bunny_relief',t=bar(82),side=-11,y=0,kind='image',src='art/halftone-bunny-relief.jpg',size=[7,0,7],mode='upright',appear=dict(t=bar(79),mode='rise',dur=1.0))]

# ---- v4 difficulty calibration
BURST_WINDOWS=[(21.5,24.0,1),(26.5,29.2,1),(33.5,35.2,1),(38.0,40.0,1),(73.5,75.2,1),(84.0,86.5,1),(104.5,106.5,1),
               (113.0,115.5,1),(139.0,142.0,1),(141.8,172.0,3)]
