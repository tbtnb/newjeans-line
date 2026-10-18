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
 dict(b0=48,b1=64,kind='verse',label='Verse 2 · 市场拱廊',pats=[A,B,C,A],over={63:'....k..k..k.k.k.'}),
 dict(b0=64,b1=66,kind='break',label='Break 2 · 观景台',auto=dict(src=['vocals'],thr=0.3,minsteps=4,c='v')),
 dict(b0=66,b1=72,kind='verse',label='Verse 3 · 下坡',pats=[C,B,A]),
 dict(b0=72,b1=80,kind='chorus',label='Final chorus · 五人广场',pats=[J,J4]),
 dict(b0=80,b1=88,kind='chorus',label='Final chorus b · 像素浮雕墙',pats=[J,JR]),
 dict(b0=88,b1=96,kind='chorus',label='Final chorus c · 巴士街',pats=[J,JR7],over={95:'k...k...k.......'}),
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
     dict(t=bar(48),label='Verse 2 · 市场拱廊',palette=dict(skyTop='#ffd6a8',skyBottom='#fff4e0',light='#ffe6c2'),camera='side',note='hillside tram line, yellow tram running parallel'),
     dict(t=bar(64),label='Break 2 · 观景台',camera='wide',note='viewpoint: whole town visible below'),
     dict(t=bar(66),label='Verse 3 · 下坡',camera='iso'),
     dict(t=bar(72),label='Final chorus · 五人广场',palette=dict(skyTop='#9ce7d4',skyBottom='#fff2f6',particles='confetti'),camera='high',note='big plaza; geometric dancers far off the road wave in sync'),
     dict(t=bar(80),label='Final chorus b · 像素浮雕墙',camera='iso'),
     dict(t=bar(88),label='Final chorus c · 巴士街',palette=dict(skyTop='#ffc9a8',skyBottom='#fff0e0'),camera='wide'),
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

# ---- v3 (2026-10-18): codex-ref alignment ("把心事跳成一座城", Lisbon afternoon: blue line through a pastel hill town)
#      + rich route choreography (L0 / +3 / +6 levels, Bridge A over the Verse-1 alleys, Bridge B over the final-chorus plaza).
_b=lambda n: 0.3562+n*1.6
ELEV=[dict(t0=_b(20.2),t1=_b(23.6),type='ramp',dy=3),          # V1 end: spiral up round the green courtyard -> +3 (Bridge A deck)
      dict(t=_b(40),type='fall',dy=-3),                        # Break: drop into the sunken fountain plaza (L0)
      dict(t0=_b(44.2),t1=_b(47.6),type='ramp',dy=6),          # Build: Lisbon stairway spiral -> +6 (market terrace)
      dict(t=103.0,type='fall',dy=-3),                        # Break 2: step down to the viewpoint (+3)
      dict(t0=_b(66.2),t1=_b(71.4),type='ramp',dy=-3),         # Verse 3: long downhill run -> L0
      dict(t=114.96,type='jump',dy=3),                        # Final chorus: jump onto Bridge B (+3) over the dancer plaza
      dict(t0=_b(80.2),t1=_b(83.0),type='ramp',dy=3),          # Final b: spiral up round the pixel-relief wall -> +6
      dict(t=139.96,type='fall',dy=-6)]                        # Final c: big drop to the bus street (L0)
A=lambda w=0.6,**k: dict(w_aim=w,**k)
ROUTE=[(0,'free',0,A(1.0)),(_b(4),'switch',90,A(0.3,thr=0.45)),                              # Intro: long straight past bike+bench, short switchbacks
       (_b(8),'meander',45,A(0.4)),(_b(12),'stair',0,A()),(_b(16),'switch',90,A(0.3,thr=0.42)), # V1: cobble zigzag corridor, staircase, wall switchbacks
       (_b(20),'spiral',None,A(0,hand='R',w_motif=2.5)),                                      # spiral up round courtyard B (+3)
       (_b(24),'stair',270,A(0.6,cross=2.0)),(_b(28),'stair',180,A(0.6,cross=1.5)),             # C1 on +3: staircases crossing back OVER the V1 alleys (Bridge A)
       (_b(32),'stair',90,A(0.6,cross=1.5)),(_b(36),'meander',0,A(0.4)),
       (_b(40),'free',None,A(0,cross=2.5)),                                                   # Break (L0): sweeping S under the chorus deck
       (_b(44),'spiral',None,A(0,hand='L',w_motif=2.5)),                                      # Build: stairway spiral to +6
       (_b(48),'switch',45,A(0.3,thr=0.5)),(_b(52),'meander',135,A(0.4)),                      # V2 on +6: arcade switchbacks, wrap through the market arcade
       (_b(56),'stair',180,A()),(_b(60),'switch',270,A(0.3,thr=0.45)),
       (_b(64),'free',None,A(1.0)),(_b(66),'stair',225,A(0.6,cross=1.5)),                      # viewpoint straight; downhill staircase
       (_b(72),'stair',90,A(0.6,cross=2.0)),(_b(76),'stair',0,A(0.6,cross=1.5)),               # FC on Bridge B over the plaza
       (_b(80),'stair',315,A(0.6,cross=1.5)),(_b(82),'stair',45,A(0.6,cross=1.5)),(_b(84),'meander',270,A(0.4)),          # FCb: spiral round the relief wall to +6
       (_b(88),'stair',180,A(0.6,cross=2.0)),(_b(92),'switch',90,A(0.3,thr=0.45)),(_b(95),'free',None,A(1.0))]
FORKS=[_b(6.5),_b(14.5),_b(30.5),_b(50.5),_b(68.5),_b(77.5),_b(90.5)]
BUILDINGS=[dict(id='courtyard_walls',t0=_b(9.2),t1=_b(11.8),color='#F4A39B',h=3.4),
           dict(id='market_arcade',t0=_b(52.2),t1=_b(54.8),color='#F4A39B',h=3.6)]
ART={'backdrop':'art/sky.jpg','ground':{'src':'art/ground-park.jpg','scale':34},
     'files':{'art/sky.jpg':'Lisbon afternoon sky #CDEDF1 with soft clouds (backdrop)',
              'art/ground-park.jpg':'park-green #BEE9C9 tile with paving dots (ground)',
              'art/awning-stripes.jpg':'coral/cream awning stripes (market arcade canopies)',
              'art/pixel-relief.jpg':'five-colour pixel relief for the teal stepped wall (landmark E)',
              'art/red-bike-decal.png':'flat red bicycle sticker (landmark A, transparent)',
              'art/bunny-tile.jpg':'white pixel bunny tile (egg E1, flips to five colour squares)'}}
FIVE=['#295BE7','#FF82D0','#F7CE63','#BEE9C9','#B1A6E8']
def layout(c):
    bar=c['bar']; g=c['gap_mid']; T=c['T']
    P=dict(skyTop='#B9E4EA',skyBottom='#CDEDF1',fog='#CDEDF1',fogStart=30,fogEnd=100,ground='#BEE9C9',groundY=-10,
           road='#FFF8ED',roadSide='#3B8A89',line='#295BE7',light='#FFF6E6',lightIntensity=1.15,ambient='#DDEFEA',particles=None)
    secs=[dict(t=0,label='Intro · 薄荷街角',camera='low',note='long straight past the red bike + bench (A), short switchbacks'),
          dict(t=bar(8),label='Verse 1 · 石砖小巷',palette=dict(road='#FBF1E2'),camera='iso',note='cobble zigzag corridor through cut-away courtyard walls, staircase, switchbacks along the teal wall'),
          dict(t=bar(20),label='Verse 1 end · 绿庭院螺旋',camera='high',note='square spiral up round the green courtyard (B) to +3'),
          dict(t=bar(24),label='Chorus 1 · 公园遮阳伞',palette=dict(particles='petals'),camera='wide',note='+3 deck: staircases cross OVER the verse alleys (Bridge A); parasols open on the kick'),
          dict(t=bar(40),label='Break · 下沉喷泉广场',palette=dict(skyTop='#C6EDF5',particles=None),camera='wide',note='drop to L0, sweeping S under the chorus deck'),
          dict(t=bar(44),label='Build · 里斯本阶梯',camera='side',note='stairway spiral to +6'),
          dict(t=bar(48),label='Verse 2 · 市场拱廊',palette=dict(skyTop='#F9D3C4',skyBottom='#FFF1E4',light='#FFE6CC'),camera='iso',note='+6 terrace: switchbacks under coral awnings, wrap through the market arcade (D); E1 bunny tile under the bench'),
          dict(t=bar(64),label='Break 2 · 观景台',camera='wide',dist=34,note='viewpoint straight: the whole town below'),
          dict(t=bar(66),label='Verse 3 · 下坡',camera='iso',note='downhill staircase back to L0'),
          dict(t=bar(72),label='Final chorus · 五人广场',palette=dict(particles='confetti'),camera='high',note='jump onto Bridge B over the five-dancer plaza (C)'),
          dict(t=bar(80),label='Final chorus b · 像素浮雕墙',camera='iso',note='spiral round the teal stepped wall with the five-colour pixel relief (E) to +6'),
          dict(t=bar(88),label='Final chorus c · 巴士街',palette=dict(skyTop='#F6C9B4',skyBottom='#FFF0E2'),camera='wide',note='big drop to the bus street; switchbacks to the finish')]
    cam=[dict(t=0,preset='low',blend=0),dict(t=bar(8),preset='iso',blend=2.0),dict(t=bar(20),preset='high',blend=1.2),dict(t=bar(24),preset='wide',blend=1.0),
         dict(t=bar(32),preset='iso',blend=1.5),dict(t=bar(40),preset='wide',blend=1.0),dict(t=bar(44),preset='side',blend=1.5),dict(t=bar(48),preset='iso',blend=2.0),
         dict(t=bar(64),preset='wide',dist=34,blend=1.2),dict(t=bar(66),preset='iso',blend=1.5),dict(t=bar(72),preset='high',blend=1.0,shake=0.1),
         dict(t=bar(80),preset='iso',blend=1.5),dict(t=bar(88),preset='wide',blend=1.5),dict(t=bar(92),preset='close',blend=2.0),dict(t=bar(95),preset='high',dist=30,blend=3.0)]
    O=[]
    O.append(dict(id='bike_bench',t=1.6,side=4.5,kind='group',radius=2.5,landmark=True,name='A 红色自行车与长椅',
                  parts=[dict(kind='torus',pos=[-0.8,0.5,0],size=[1,0.12,1],rot=[0,90,0],color='#333333'),dict(kind='torus',pos=[0.8,0.5,0],size=[1,0.12,1],rot=[0,90,0],color='#333333'),
                         dict(kind='box',pos=[0,0.9,0],size=[1.6,0.12,0.12],color='#E8463C'),dict(kind='box',pos=[0.6,1.3,0],size=[0.1,0.8,0.1],color='#E8463C'),
                         dict(kind='box',pos=[0,0.45,1.6],size=[2.2,0.15,0.6],color='#F4A39B'),dict(kind='box',pos=[0,0.8,1.9],size=[2.2,0.6,0.1],color='#F4A39B')]))
    O.append(dict(id='bike_decal',t=3.2,side=-4,y=0.02,kind='image',src='art/red-bike-decal.png',size=[3,0,1.8],mode='flat',alpha=True))
    O.append(dict(id='courtyard_green',t=bar(21.5),kind='group',radius=5,landmark=True,name='B 绿色庭院 (the V1 spiral winds round it)',
                  parts=[dict(kind='box',pos=[0,0.2,0],size=[6,0.4,6],color='#BEE9C9'),dict(kind='cylinder',pos=[0,1.6,0],size=[0.5,2.8,0.5],color='#8B6B4A'),
                         dict(kind='sphere',pos=[0,3.6,0],size=[3,2.4,3],color='#7FCF96')],react='beat'))
    for i in range(10):
        t=bar(25)+i*2.4
        O.append(dict(id=f'parasol{i}',t=t,side=(5.5 if i%2==0 else -5.5),kind='group',radius=2,
                      parts=[dict(kind='cylinder',pos=[0,1.2,0],size=[0.12,2.4,0.12],color='#FFFFFF'),dict(kind='cone',pos=[0,2.6,0],size=[3,0.8,3],color=FIVE[i%5])],
                      appear=dict(t=t-1.2,mode='unfold',dur=0.4),react='kick'))
    O.append(dict(id='fountain',t=bar(41.5),side=-8,kind='group',radius=4,landmark=True,name='下沉喷泉',
                  parts=[dict(kind='cylinder',pos=[0,0.4,0],size=[6,0.8,6],color='#FFF8ED'),dict(kind='cylinder',pos=[0,1.4,0],size=[1,2,1],color='#FFF8ED'),
                         dict(kind='sphere',pos=[0,2.8,0],size=[2,1.2,2],color='#9EDCEB')],react='beat',appear=dict(t=bar(40)-0.5,mode='rise',dur=1.0)))
    for i in range(6):
        t=bar(49)+i*2.2
        O.append(dict(id=f'awning{i}',t=t,side=(4.2 if i%2 else -4.2),kind='image',src='art/awning-stripes.jpg',size=[3.2,0,1.4],mode='upright',
                      appear=dict(t=t-1.4,mode='unfold',dur=0.4)))
    O.append(dict(id='market_flags',t=bar(53.5),pocket=True,kind='group',radius=3,landmark=True,name='D 市场拱廊 (coral awnings, columns, flags)',
                  parts=[dict(kind='cylinder',pos=[x,1.6,0],size=[0.35,3.2,0.35],color='#FFF8ED') for x in (-2,0,2)]+
                        [dict(kind='box',pos=[0,3.4,0],size=[5,0.3,1.6],color='#F4A39B',texture='art/awning-stripes.jpg')]+
                        [dict(kind='box',pos=[-2+i,3.9,0.8],size=[0.4,0.5,0.02],color=FIVE[i]) for i in range(5)]))
    O.append(dict(id='egg_bunny_tile',t=bar(57)+0.4,pocket=True,radius=1.5,kind='group',egg=True,name='E1 长椅下的白色像素兔砖 (flips once in the final chorus to show five colour squares)',
                  parts=[dict(kind='box',pos=[0,0.45,0],size=[1.8,0.12,0.6],color='#F4A39B'),dict(kind='plane',pos=[0,0.03,0],size=[0.8,0,0.8],color='#FFFFFF',texture='art/bunny-tile.jpg')]))
    O.append(dict(id='viewpoint_town',t=bar(64)+0.8,side=-26,y=-10,kind='group',radius=10,nopocket=True,name='观景台下的整座小城',
                  parts=[dict(kind='box',pos=[x*3,1.5,y*3],size=[2.6,3+(x*7+y*3)%4*1.2,2.6],color=['#FFF8ED','#F4A39B','#B1A6E8','#CDEDF1'][(x+y)%4]) for x in range(-2,3) for y in range(-2,3)]))
    for i in range(5):
        O.append(dict(id=f'dancer{i}',t=bar(73.5),side=-12,along=-8+i*4,kind='group',radius=1.5,landmark=(i==2),name='C 五人广场: five abstract dancer sculptures (no faces)' if i==2 else None,
                      parts=[dict(kind='cylinder',pos=[0,1.2,0],size=[0.8,2.4,0.8],color=FIVE[i]),dict(kind='sphere',pos=[0,2.8,0],size=[0.9,0.9,0.9],color='#FFF8ED')],
                      react='beat',appear=dict(t=bar(72)-0.6+i*0.2,mode='pop',dur=0.3)))
    O.append(dict(id='relief_wall',t=bar(81.5),kind='group',radius=4,landmark=True,name='E 青绿阶梯墙与五色像素浮雕',
                  parts=[dict(kind='box',pos=[0,1.5*(k+1),-k*0.8],size=[6-k,3,1.2],color='#3B8A89') for k in range(3)]+
                        [dict(kind='plane',pos=[0,4,0.62],size=[4.5,0,3],color='#FFFFFF',texture='art/pixel-relief.jpg')],react='kick'))
    O.append(dict(id='bus',t=bar(92),side=8,kind='group',radius=4,landmark=True,name='彩窗巴士',
                  parts=[dict(kind='box',pos=[0,1.7,0],size=[2.6,2.8,8],color='#FFF8ED')]+[dict(kind='box',pos=[1.31,2.2,-3+1.5*i],size=[0.05,0.9,1.2],color=FIVE[i]) for i in range(5)],
                  appear=dict(t=bar(90),mode='fade',dur=0.8)))
    O.append(dict(id='egg_bell',t=bar(93),side=5,kind='group',radius=1.2,egg=True,name='E2 自行车铃 (silent wobble on taps)',
                  parts=[dict(kind='sphere',pos=[0,1,0],size=[0.4,0.3,0.4],color='#F7CE63')],react='tap'))
    ev=[dict(t=bar(8),type='raise',target='courtyard_walls*',dur=0.8),dict(t=bar(24),type='burst',at='player',particles='petals'),
        dict(t=bar(40),type='color',palette=dict(skyTop='#C6EDF5'),dur=1.0),dict(t=bar(48),type='light',target='awning*',every=2*T,level=0.5,color='#FFFFFF',dur=0.3,until=bar(64)),
        dict(t=bar(72),type='burst',at='player',particles='confetti'),dict(t=bar(72)+0.2,type='spin',target='egg_bunny_tile',speed=1.0,until=bar(72)+0.8),
        dict(t=bar(80),type='pulse',target='relief_wall',every=T*2,until=bar(88)),
        dict(t=bar(88),type='color',palette=dict(skyTop='#F6C9B4'),dur=3.0)]
    cr=[g(x,0.8) for x in CROWN_T(bar)]
    dia=sorted(g(t,0.5) for t in [bar(3),bar(14),bar(28),bar(41),bar(46),bar(54),bar(65),bar(70),bar(84),bar(94)])
    return dict(id='super-shy',title='Super Shy',palette=P,road=dict(height=0.6,reveal=[dict(t=0,mode='rise',lead=1.6),dict(t=bar(24),mode='unfold',lead=1.4),
                dict(t=bar(40),mode='fade',lead=2.0),dict(t=bar(44),mode='rise',lead=1.4),dict(t=bar(72),mode='drop',lead=1.3)]),
                sections=secs,camera=cam,objects=O,events=ev,diamonds=[dict(t=t,side=0) for t in dia],
                crowns=[dict(t=x) for x in cr],finish=dict(kind='gate',color='#F7CE63'),collectibleColors=dict(diamond='#FF82D0',crown='#F7CE63'))
CROWN_T=lambda bar: [bar(41),bar(64)+0.5]

# ---- v4 difficulty calibration (title track: hard tier)
BURST_WINDOWS=[(36.5,39.0,1),(52.0,53.6,1),(62.5,64.5,1),(75.4,77.4,1),(101.0,103.0,1),(113.5,115.8,1),(115.5,154.0,4)]
TIER='hard (title track)'
