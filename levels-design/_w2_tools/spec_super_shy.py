FOLDER='super-shy'; OLD=176; BEAT_OFFSET=0; MIN_GAP=0.19
JUDGE={'perfect':55,'good':95,'note':'150 BPM: 8th runs are 200 ms apart, so the accept window must stay below ±100 ms to keep neighbouring corners unambiguous; ±95 ms recommended (perfect ±55).'}
START_HEADING='N'
SPEED=[(0,11.0)]
WIDTH=[(0,2.0),(38.76,1.9),(77.16,1.8),(115.56,1.9),(128.36,1.7)]
A='....k..k..k...k.'; B='....k.....k.....'; C='k...k..k..k...k.'
J='k...k...k..k..k.'; J4='k...k...k.....k.'; JR='k...k...k.k.k.k.'; JR7='k.k.k.k.k..k..k.'
SECTIONS=[
 dict(b0=0,b1=8,kind='intro',label='Intro · 薄荷街角',pats=['....k.....k.....','....k...........'],over={0:'................',7:'....k..k..k...k.'}),
 dict(b0=8,b1=24,kind='verse',label='Verse 1 · 石砖小巷',pats=[A,B,A,C],over={23:'....k..k..k.k.k.'}),
 dict(b0=24,b1=40,kind='chorus',label='Chorus 1 · 公园遮阳伞',pats=[J,J4,J,JR],over={39:'k...k...k..k.k.k'}),
 dict(b0=40,b1=44,kind='break',label='Break · 下沉喷泉广场',auto=dict(src=['vocals'],thr=0.3,minsteps=4,c='v')),
 dict(b0=44,b1=48,kind='pre',label='Build · 里斯本阶梯',pats=['....k.......k...','k...k.....k.k...','k...k.....k.k...','k...k...k.k.k.k.']),
 dict(b0=48,b1=64,kind='verse',label='Verse 2 · 山坡电车',pats=[A,B,C,A],over={63:'....k..k..k.k.k.'}),
 dict(b0=64,b1=66,kind='break',label='Break 2 · 观景台',auto=dict(src=['vocals'],thr=0.3,minsteps=4,c='v')),
 dict(b0=66,b1=72,kind='verse',label='Verse 3 · 下坡',pats=[C,B,A]),
 dict(b0=72,b1=80,kind='chorus',label='Final chorus · 广场集体舞',pats=[J,J4]),
 dict(b0=80,b1=88,kind='chorus',label='Final chorus b · 喷泉',pats=[J,JR]),
 dict(b0=88,b1=96,kind='chorus',label='Final chorus c · 巴士',pats=[J,JR7],over={95:'k...k...k.......'}),
]
NOTES=('150.0 BPM grid (drum-stem fit, residual ≤ 2 ms). Verses follow the broken-beat kick on steps 4,7,10,14 (3+3+4 sixteenths: the skippy "shy" groove); '
       'choruses follow the jersey-style kick on 0,4,8,11,14; 8th-note kick runs (200 ms) close each 4-bar phrase. Drumless breaks follow the vocal syllables.')
MOTIFS=[(0,'stair'),(13.16,'meander'),(38.76,'stair'),(64.36,'meander'),(70.76,'stair'),(77.16,'meander'),(102.76,'stair')]
PIVOTS=[13.2,19.6,26.0,32.4,38.8,45.2,51.6,58.0,64.4,70.8,77.2,83.6,90.0,96.4,102.8,106.0,115.6,122.0,128.4,134.8,141.2,147.6]
ELEV=[dict(t=64.36,type='fall',dy=-4),dict(t0=70.9,t1=77.0,type='ramp',dy=6),dict(t0=106.0,t1=115.4,type='ramp',dy=-2),
      dict(t=115.56,type='jump',dy=3),dict(t=141.16,type='fall',dy=-3)]
def layout(c):
    bar=c['bar']; g=c['gap_mid']
    P=dict(skyTop='#a8e6d8',skyBottom='#fff8e8',fog='#eaf7f2',fogStart=30,fogEnd=100,ground='#f3ead8',groundY=-10,
           road='#fffdf6',roadSide='#e2c79e',line='#ff5c8a',light='#fff3dc',lightIntensity=1.2,ambient='#d7efe7',particles=None)
    secs=[
     dict(t=0,label='Intro · 薄荷街角',palette=dict(skyTop='#bdeee2'),camera='low',note='mint street corner, small bike, flags half hidden behind windows'),
     dict(t=bar(8),label='Verse 1 · 石砖小巷',palette=dict(road='#f6efe2',roadSide='#d9b98d'),camera='iso',note='cobblestone alleys; tiled (azulejo) facades both sides'),
     dict(t=bar(24),label='Chorus 1 · 公园遮阳伞',palette=dict(skyTop='#8fe0cd',ground='#cfe9b8',particles='petals'),camera='high',note='park opens; parasols open on the kick'),
     dict(t=bar(40),label='Break · 下沉喷泉广场',palette=dict(skyTop='#c9f1ff',particles=None),camera='wide',note='drop into a sunken fountain plaza'),
     dict(t=bar(44),label='Build · 里斯本阶梯',camera='side',note='road climbs a long stairway (+6)'),
     dict(t=bar(48),label='Verse 2 · 山坡电车',palette=dict(skyTop='#ffd6a8',skyBottom='#fff4e0',light='#ffe6c2'),camera='side',note='hillside tram line, yellow tram running parallel'),
     dict(t=bar(64),label='Break 2 · 观景台',camera='wide',note='viewpoint: whole town visible below'),
     dict(t=bar(66),label='Verse 3 · 下坡',camera='iso'),
     dict(t=bar(72),label='Final chorus · 广场集体舞',palette=dict(skyTop='#9ce7d4',skyBottom='#fff2f6',particles='confetti'),camera='high',note='big plaza; geometric dancers far off the road wave in sync'),
     dict(t=bar(80),label='Final chorus b · 喷泉',camera='iso'),
     dict(t=bar(88),label='Final chorus c · 巴士',palette=dict(skyTop='#ffc9a8',skyBottom='#fff0e0'),camera='wide'),
    ]
    cam=[dict(t=0,preset='low',blend=0),dict(t=bar(8),preset='iso',blend=2.0),dict(t=bar(16),preset='iso',yaw=60,blend=2.0),dict(t=bar(24),preset='high',blend=1.0),
         dict(t=bar(32),preset='iso',blend=1.5),dict(t=bar(40),preset='wide',blend=1.0),dict(t=bar(44),preset='side',blend=1.5),dict(t=bar(56),preset='iso',blend=2.0),
         dict(t=bar(64),preset='wide',dist=34,blend=1.2),dict(t=bar(66),preset='iso',blend=1.5),dict(t=bar(72),preset='high',blend=1.0,shake=0.1),
         dict(t=bar(80),preset='iso',blend=1.5),dict(t=bar(88),preset='wide',blend=1.5),dict(t=bar(92),preset='close',blend=2.0),dict(t=bar(95),preset='high',dist=30,blend=3.0)]
    O=[]
    O.append(dict(id='bike',t=1.5,side=4.5,along=3,kind='group',radius=2,landmark=True,name='街角小自行车',
                  parts=[dict(kind='torus',pos=[-0.8,0.5,0],size=[1,0.12,1],rot=[0,90,0],color='#333'),dict(kind='torus',pos=[0.8,0.5,0],size=[1,0.12,1],rot=[0,90,0],color='#333'),
                         dict(kind='box',pos=[0,0.9,0],size=[1.6,0.12,0.12],color='#ff5c8a'),dict(kind='box',pos=[0.6,1.3,0],size=[0.1,0.8,0.1],color='#ff5c8a')]))
    O.append(dict(id='azulejo_row',kind='row',t0=bar(8),t1=bar(24),side=4.0,spacing=3.2,bothSides=True,
                  item=dict(kind='building',size=[2.8,6,2.6],color='#ffffff',color2='#5aa8d8',react='tap')))
    for i in range(10):
        t=bar(25)+i*2.4
        O.append(dict(id=f'parasol{i}',t=t,side=(5.5 if i%2==0 else -5.5),kind='group',radius=2,
                      parts=[dict(kind='cylinder',pos=[0,1.2,0],size=[0.12,2.4,0.12],color='#ffffff'),dict(kind='cone',pos=[0,2.6,0],size=[3,0.8,3],color=['#ff8fb1','#7fd8c6','#ffd86b','#a3c8ff','#ffb38a'][i%5])],
                      appear=dict(t=t-1.2,mode='unfold',dur=0.4),react='kick'))
    O.append(dict(id='fountain',t=bar(41),side=-9,kind='group',radius=4,landmark=True,name='下沉喷泉',
                  parts=[dict(kind='cylinder',pos=[0,0.4,0],size=[7,0.8,7],color='#f0e6d2'),dict(kind='cylinder',pos=[0,1.4,0],size=[1,2,1],color='#f0e6d2'),
                         dict(kind='sphere',pos=[0,2.8,0],size=[2,1.2,2],color='#9ee3ff')],react='beat',appear=dict(t=bar(40)-0.5,mode='rise',dur=1.0)))
    O.append(dict(id='stairs_side',t=bar(45),side=4,kind='stairs',size=[3,6,10],color='#f3ead8',name='里斯本阶梯扶栏'))
    O.append(dict(id='tram',t=bar(50),side=-6,kind='group',radius=3,landmark=True,name='黄色电车',
                  parts=[dict(kind='box',pos=[0,1.6,0],size=[2.4,2.6,6],color='#ffd23f'),dict(kind='box',pos=[0,3.05,0],size=[2.5,0.3,6.1],color='#ffffff'),
                         dict(kind='box',pos=[1.21,1.9,0],size=[0.05,0.9,4.6],color='#7fc8e8')],appear=dict(t=bar(48),mode='fade',dur=0.8)))
    O.append(dict(id='viewpoint_town',t=bar(64)+0.8,side=-26,y=-10,kind='group',radius=10,landmark=True,name='观景台下的整座小城',
                  parts=[dict(kind='box',pos=[x*3,1.5+(x*7+y*3)%4,y*3],size=[2.6,3+(x*7+y*3)%4*1.2,2.6],color=['#ffffff','#ffe1c4','#ffd0dc','#d4f1ea'][(x+y)%4]) for x in range(-2,3) for y in range(-2,3)]))
    for i in range(5):
        O.append(dict(id=f'dancer{i}',t=bar(73),side=-14,along=-8+i*4,kind='group',radius=1.5,landmark=(i==2),name='远处的同步舞者' if i==2 else None,
                      parts=[dict(kind='cylinder',pos=[0,1,0],size=[0.8,2,0.8],color=['#ff8fb1','#7fd8c6','#ffd86b','#a3c8ff','#ffb38a'][i]),dict(kind='sphere',pos=[0,2.4,0],size=[0.9,0.9,0.9],color='#fff1e0')],
                      react='beat',appear=dict(t=bar(72)-0.6+i*0.2,mode='pop',dur=0.3)))
    O.append(dict(id='fountain2',t=bar(82),side=10,kind='group',radius=4,landmark=True,name='广场大喷泉',
                  parts=[dict(kind='cylinder',pos=[0,0.5,0],size=[8,1,8],color='#f0e6d2'),dict(kind='cylinder',pos=[0,2,0],size=[1.2,3,1.2],color='#f0e6d2'),dict(kind='sphere',pos=[0,4,0],size=[3,2,3],color='#9ee3ff')],react='kick'))
    O.append(dict(id='bus',t=bar(92),side=8,kind='group',radius=4,landmark=True,name='彩窗巴士',
                  parts=[dict(kind='box',pos=[0,1.7,0],size=[2.6,2.8,8],color='#ffffff'),dict(kind='box',pos=[1.31,2.2,-2],size=[0.05,0.9,1.4],color='#ff8fb1'),
                         dict(kind='box',pos=[1.31,2.2,0],size=[0.05,0.9,1.4],color='#7fd8c6'),dict(kind='box',pos=[1.31,2.2,2],size=[0.05,0.9,1.4],color='#ffd86b')],
                  appear=dict(t=bar(90),mode='fade',dur=0.8)))
    O.append(dict(id='greeting_card',t=bar(95)+0.4,side=-5,y=0.5,kind='box',size=[1.6,1.1,0.06],color='#fff1f5',color2='#ff5c8a',name='终于翻到正面的问候卡',react='none',appear=dict(t=bar(95),mode='unfold',dur=0.6)))
    O.append(dict(id='egg_bunny_parasol',t=bar(27)+0.3,side=-7.5,kind='group',radius=1.2,egg=True,name='伞后迷你兔 (returns waving at the end)',
                  parts=[dict(kind='sphere',pos=[0,0.5,0],size=[0.8,0.8,0.8],color='#ffffff'),dict(kind='box',pos=[-0.15,1.1,0],size=[0.12,0.5,0.12],color='#ffffff'),dict(kind='box',pos=[0.15,1.1,0],size=[0.12,0.5,0.12],color='#ffffff')]))
    O.append(dict(id='egg_bunny_wave',t=bar(94),side=-6,kind='group',radius=1.2,egg=True,name='迷你兔挥手',
                  parts=[dict(kind='sphere',pos=[0,0.5,0],size=[0.8,0.8,0.8],color='#ffffff'),dict(kind='box',pos=[-0.15,1.1,0],size=[0.12,0.5,0.12],color='#ffffff'),dict(kind='box',pos=[0.15,1.1,0],size=[0.12,0.5,0.12],color='#ffffff'),dict(kind='box',pos=[0.5,0.7,0],size=[0.4,0.1,0.1],rot=[0,0,40],color='#ffffff')],react='beat'))
    O.append(dict(id='egg_bell',t=bar(93),side=5,kind='group',radius=1.5,egg=True,name='自行车铃 (silent wobble)',
                  parts=[dict(kind='sphere',pos=[0,1,0],size=[0.4,0.3,0.4],color='#ffd23f')],react='tap'))
    ev=[dict(t=bar(8),type='raise',target='azulejo_row',dur=0.8),dict(t=bar(24),type='burst',at='player',particles='petals'),
        dict(t=bar(40),type='color',palette=dict(skyTop='#c9f1ff'),dur=1.0),dict(t=bar(48),type='light',target='tram',dur=2.0),
        dict(t=bar(72),type='burst',at='player',particles='confetti'),dict(t=bar(72),type='pulse',target='fountain2',every=c['T']*2,until=bar(96)),
        dict(t=bar(88),type='color',palette=dict(skyTop='#ffc9a8'),dur=3.0)]
    cr=[g(x,0.8) for x in CROWN_T(bar)]
    dia=[g(t,0.5) for t in [bar(3),bar(14),bar(28),bar(41),bar(46),bar(54),bar(65),bar(70),bar(84),bar(94)]]
    dia=sorted(dia)
    return dict(id='super-shy',title='Super Shy',palette=P,road=dict(height=0.6,reveal=[dict(t=0,mode='rise',lead=1.6),dict(t=bar(24),mode='unfold',lead=1.4),
                dict(t=bar(40),mode='fade',lead=2.0),dict(t=bar(44),mode='rise',lead=1.4),dict(t=bar(72),mode='drop',lead=1.3)]),
                sections=secs,camera=cam,objects=O,events=ev,diamonds=[dict(t=t,side=0) for t in dia],
                crowns=[dict(t=x) for x in cr],finish=dict(kind='gate'))
WHY={
 'Intro (0–13.2 s)':'drums + synth before the vocals: taps on the kick on beat 2 and the "and" of 3 (steps 4,10), 1–2 per bar; bar 7 previews the verse groove.',
 'Verse 1 / 2 / 3':'skippy broken-beat kick on steps 4,7,10,14 (3+3+4 sixteenths = 300/300/400 ms): the signature "shy" bounce, alternated with 2-tap bars so the vocal phrases breathe; phrase-end bars add a kick/snare 8th fill.',
 'Chorus 1 / Final':'jersey-style kick 0,4,8,11,14 under "I\'m super shy, super shy"; the 4th bar of each phrase is an 8th-note kick roll (6–7 taps at 200 ms). Final chorus c alternates 5-tap and 7-tap bars (hardest).',
 'Break / Break 2':'drums cut: taps on vocal syllables ≥ 1 beat apart (0.4 s+), the breathing room before the stair climb.',
 'Build (70.8–77.2 s)':'kick on 2 and 4 returning, densifying to an 8th run — synced with the road ramping up the Lisbon stairway.',
}

CROWN_T=lambda bar: [bar(41),bar(64)+0.5]
