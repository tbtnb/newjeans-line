FOLDER='omg'; OLD=213; BEAT_OFFSET=0; MIN_GAP=0.20; JUDGE={'perfect':60,'good':110,'note':'+-110 ms accept window around the geometric corner (early taps beyond -110 ms = turn too early => crash into wall; late beyond +110 ms = run off the edge). 8th-note runs here are 236 ms apart so windows never overlap.'}
START_HEADING='N'
SPEED=[(0,10.0)]
WIDTH=[(0,2.2),(105.88,2.0),(134.22,1.8),(166.35,2.0),(181.47,1.8)]
# ---- chart: 16-step patterns per bar (bar = 1.8898 s @127.0 BPM). letters = tap + musical tag source
# k kick, s snare/clap, v vocal, m melody/synth (other stem), b bass, x any
SECTIONS=[
 dict(b0=0,b1=8,kind='intro',label='Intro · 病房走廊',pats=['................'],
      over={1:'....v...v.......',2:'.....v...v...v..',4:'v..v....v.......',6:'...........v....',7:'.......v...v...v'}),
 dict(b0=8,b1=16,kind='verse',label='Verse 1 · 治疗桌与五椅',pats=['s.....s.s.....s.','s.....s.......s.'],
      over={15:'s...s...s.....s.'}),
 dict(b0=16,b1=24,kind='verse',label='Verse 1b · 墙板外折',pats=['k.........k...k.','..k.k.....k.k...'],
      over={23:'k.k.k..k..k.k...'}),
 dict(b0=24,b1=32,kind='chorus',label='Chorus 1 · 黑兔舞台',pats=['k...m...s...k.m.','..k...m.k.m.k.m.'],
      over={31:'..s.....v.v...v.'}),
 dict(b0=32,b1=40,kind='verse',label='Verse 2 · 玻璃鞋',pats=['k...k.....k...s.','..k.k.....k.k...']),
 dict(b0=40,b1=48,kind='pre',label='Verse 2b · 双折长短路',pats=['k...k...v.....k.','..k.......k.k...'],
      over={47:'k.k.k..k..k.....'}),
 dict(b0=48,b1=56,kind='break',label='Pre · 手机桥',pats=['b.........b.....','..b...b...b...b.'],
      over={55:'..b.v.b.v.b.v.b.'}),
 dict(b0=56,b1=64,kind='chorus',label='Chorus 2 · 屏幕块',pats=['k...m...s...k.m.','..k...m.k.m.k.m.'],
      over={63:'..s.s..v.v...v..'}),
 dict(b0=64,b1=71,kind='post',label='Post · 错列直角',pats=['k.........k...s.','..k....k..k.k...']),
 dict(b0=71,b1=79,kind='bridge',label='Bridge · 书页墙与猫',pats=['...k..k.k....k.k','...k..k.k.k..k..']),
 dict(b0=79,b1=80,kind='break',label='Break · 书页合拢',pats=['..s.....k.......']),
 dict(b0=80,b1=88,kind='drop',label='Dance break · 舞台五墙',pats=['k...k.k.k.k.k...','k...k...k...k.k.'],
      over={86:'k.k.k.k.k.k.k.k.',87:'k...k.k.k.k.k...'}),
 dict(b0=88,b1=96,kind='chorus',label='Final chorus · 兔耳发夹',pats=['k...m...s...k.m.','..k...m.k.m.k.m.']),
 dict(b0=96,b1=104,kind='chorus',label='Final chorus b · 天桥',pats=['k...m.m.s...k.m.','..k...m.k.m.k.m.'],
      over={103:'..s.s...........'}),
 dict(b0=104,b1=112,kind='outro',label='Outro · 尾奏琴键',pats=['....m.........m.','......m...m.....'],
      over={111:'................'}),
]
NOTES=('Hand-built on a 127.0 BPM grid fitted to the drum stem (residual 8 ms). Each bar pattern was chosen from per-bar 16-step onset maps of the '
       'demucs stems (kick/clap/bass/vocal/synth) and every tap is snapped to the nearest real onset of its tagged stem within 45 ms. '
       'Chorus = halftime kick/snare + the synth hook answering on the off-8ths (call-and-response); bridge = syncopated trap kick; '
       'dance break = four-on-the-floor 8th runs (8-tap and 10-tap runs).')
# ---- route
MOTIFS=[(0,'stair'),(15.17,'meander'),(30.29,'stair'),(60.52,'meander'),(75.64,'stair'),(121.0,'meander'),(134.22,'stair'),(151.23,'stair'),(196.58,'meander')]
PIVOTS=[15.3,30.4,45.5,53.0,60.6,68.2,75.7,83.3,90.9,98.4,106.0,113.5,121.1,134.3,141.9,151.3,158.9,166.4,173.9,181.5,189.0,196.6,204.2]
ELEV=[dict(t=45.41,type='fall',dy=-4),dict(t0=91.0,t1=98.0,type='ramp',dy=8),dict(t=105.88,type='fall',dy=-4),
      dict(t0=134.4,t1=147.0,type='ramp',dy=6),dict(t=166.35,type='fall',dy=-6),dict(t=196.58,type='fall',dy=-2)]
COMPACT=1.0
def layout(c):
    bar=c['bar']; g=c['gap_mid']
    P=dict(skyTop='#f6c9d6',skyBottom='#fff4f2',fog='#fbe7ea',fogStart=34,fogEnd=110,ground='#f3dfe3',groundY=-14,
           road='#ffffff',roadSide='#e9a9b8',line='#e0314f',light='#fff1ec',lightIntensity=1.1,ambient='#e8c9d2',particles=None)
    secs=[
     dict(t=0,label='Intro · 病房走廊',palette=dict(skyTop='#fbe9ee',fog='#fff3f5',particles=None),camera='iso',note='milky void, one phone on a desk; road = thin circuit trace'),
     dict(t=bar(8),label='Verse 1 · 治疗桌与五椅',palette=dict(skyTop='#f6c9d6',particles='dust'),camera='iso',note='meander traces between stacked message bubbles'),
     dict(t=bar(16),label='Verse 1b · 墙板外折',camera='iso'),
     dict(t=bar(24),label='Chorus 1 · 黑兔舞台',palette=dict(skyTop='#ff9fb7',skyBottom='#ffe3ea',road='#fff7f9',particles='bubbles'),camera='high',note='fall into the call-ring plaza'),
     dict(t=bar(32),label='Verse 2 · 玻璃鞋',palette=dict(skyTop='#f4b9c8',ground='#e6cfd6'),camera='side'),
     dict(t=bar(40),label='Verse 2b · 双折长短路',palette=dict(skyTop='#d9c4f0',fog='#efe4fa'),camera='iso'),
     dict(t=bar(48),label='Pre · 手机桥',palette=dict(skyTop='#cdb7e6',light='#f3e9ff',lightIntensity=0.85,particles=None),camera='low'),
     dict(t=bar(56),label='Chorus 2 · 屏幕块',palette=dict(skyTop='#ff8fae',skyBottom='#ffe9ef',particles='bubbles'),camera='wide'),
     dict(t=bar(64),label='Post · 错列直角',camera='iso'),
     dict(t=bar(71),label='Bridge · 书页墙与猫',palette=dict(skyTop='#3d2a52',skyBottom='#9a6f9e',fog='#6e4f7a',road='#fbe8ff',roadSide='#a37ab8',light='#ffd9f0',ambient='#7c5a8c',particles='stars'),camera='close'),
     dict(t=bar(79),label='Break · 书页合拢',camera='top'),
     dict(t=bar(80),label='Dance break · 舞台五墙',palette=dict(skyTop='#ff6f91',skyBottom='#ffd0dc',road='#ffffff',particles='confetti'),camera='iso'),
     dict(t=bar(88),label='Final chorus · 兔耳发夹',palette=dict(skyTop='#ffb3c6',skyBottom='#fff5f7',particles='bubbles'),camera='wide'),
     dict(t=bar(96),label='Final chorus b · 天桥',camera='iso'),
     dict(t=bar(104),label='Outro · 尾奏琴键',palette=dict(skyTop='#ffd9c9',skyBottom='#fff8f0',light='#ffe6c8',particles='dust'),camera='high'),
    ]
    cam=[dict(t=0,preset='iso',blend=0),dict(t=bar(8),preset='iso',yaw=30,blend=2.0),dict(t=bar(24),preset='high',blend=1.2),
         dict(t=bar(32),preset='side',blend=2.0),dict(t=bar(40),preset='iso',blend=1.5),dict(t=bar(48),preset='low',blend=2.0),
         dict(t=bar(56),preset='wide',blend=0.9),dict(t=bar(60),preset='iso',blend=2.0),dict(t=bar(71),preset='close',blend=1.5),
         dict(t=bar(79),preset='top',blend=0.8),dict(t=bar(80),preset='iso',blend=0.6,shake=0.15),dict(t=bar(88),preset='wide',blend=1.2),
         dict(t=bar(92),preset='iso',blend=2.0),dict(t=bar(104),preset='high',dist=26,blend=4.0)]
    O=[]
    O.append(dict(id='phone',t=1.5,side=7,along=6,kind='phone',size=[3,0.4,6],color='#ffffff',color2='#e0314f',landmark=True,name='亮屏的电话',
                  appear=dict(t=0.5,mode='rise',dur=1.0),react='none'))
    O.append(dict(id='desk',t=1.5,side=7,along=6,y=-0.8,kind='box',size=[10,0.6,12],color='#f8e1e6'))
    for i,t in enumerate([bar(8)+0.4,bar(10)+0.4,bar(12)+0.4,bar(14)+0.4]):
        O.append(dict(id=f'bubble{i}',t=t,side=(-8 if i%2 else 8),y=1.5+i*0.6,kind='bubble',size=[2.5,2,1],color='#ffffff',color2='#ff9fb7',
                      appear=dict(t=t-1.6,mode='pop',dur=0.4),react='beat'))
    O.append(dict(id='trace_row',kind='row',t0=bar(8),t1=bar(16),side=1.9,spacing=1.6,bothSides=True,
                  item=dict(kind='box',size=[0.25,0.12,1.0],color='#e9a9b8',react='tap')))
    O.append(dict(id='ring',t=bar(24)+0.5,side=0,along=0,y=-1.5,kind='torus',size=[30,1,30],color='#ff7f9f',landmark=True,onroad=True,name='通话光环 (ring around the chorus plaza, under the road)',
                  appear=dict(t=bar(24)-1.0,mode='grow',dur=1.2)))
    for i in range(5):
        t=bar(25)+i*3.78
        O.append(dict(id=f'msgbox{i}',t=t,side=(9 if i%2==0 else -9),y=-1,kind='box',size=[3,3,3],color='#ffffff',color2='#e0314f',
                      appear=dict(t=t-2.0,mode='unfold',dur=0.6),react='kick'))
    O.append(dict(id='catroof',t=bar(34),side=-10,kind='group',radius=4,landmark=True,name='猫的屋顶',
                  parts=[dict(kind='box',pos=[0,2,0],size=[6,4,6],color='#ffffff'),dict(kind='cone',pos=[0,5,0],size=[7,2.5,7],rot=[0,45,0],color='#e9a9b8'),
                         dict(kind='box',pos=[-1.2,6.6,0],size=[0.7,1.1,0.4],rot=[0,0,20],color='#333'),dict(kind='box',pos=[1.2,6.6,0],size=[0.7,1.1,0.4],rot=[0,0,-20],color='#333'),
                         dict(kind='sphere',pos=[0,6.2,0],size=[1.6,1.4,1.4],color='#333')],appear=dict(t=bar(33),mode='rise',dur=1.2)))
    O.append(dict(id='castle',t=bar(42),side=12,kind='group',radius=5,landmark=True,name='玻璃城堡',
                  parts=[dict(kind='box',pos=[0,3,0],size=[7,6,5],color='#efe4fa'),dict(kind='cylinder',pos=[-3.5,5,0],size=[2,10,2],color='#ffffff'),
                         dict(kind='cylinder',pos=[3.5,5,0],size=[2,10,2],color='#ffffff'),dict(kind='cone',pos=[-3.5,11,0],size=[2.6,3,2.6],color='#e0314f'),
                         dict(kind='cone',pos=[3.5,11,0],size=[2.6,3,2.6],color='#e0314f')],appear=dict(t=bar(40)+1,mode='rise',dur=1.6)))
    O.append(dict(id='signal_bars',t=bar(50),side=-9,kind='group',radius=3,landmark=True,name='信号格',
                  parts=[dict(kind='box',pos=[-1.5,0.75,0],size=[0.8,1.5,0.8],color='#e0314f'),dict(kind='box',pos=[-0.5,1.5,0],size=[0.8,3,0.8],color='#e0314f'),
                         dict(kind='box',pos=[0.5,2.25,0],size=[0.8,4.5,0.8],color='#f4b9c8'),dict(kind='box',pos=[1.5,3,0],size=[0.8,6,0.8],color='#f4b9c8')]))
    O.append(dict(id='dome',t=bar(58),side=-42,y=0,kind='arch',size=[44,24,3],color='#ffd6e0',name='通话穹顶 (giant call-ring arch, far left)',landmark=True,
                  appear=dict(t=bar(56)-0.5,mode='grow',dur=1.5),exit=dict(t=bar(64),mode='fade',dur=2)))
    O.append(dict(id='moon',t=bar(74),side=-24,y=14,kind='moon',size=[6,6,6],color='#fff3c4',landmark=True,name='问号月亮',appear=dict(t=bar(71),mode='fade',dur=2)))
    for i in range(8):
        t=bar(80)+i*1.89
        O.append(dict(id=f'speaker{i}',t=t,side=(7 if i%2==0 else -7),kind='box',size=[2,4,2],color='#ffffff',color2='#e0314f',
                      appear=dict(t=t-1.5,mode='drop',dur=0.5),react='kick'))
    for i in range(5):
        O.append(dict(id=f'lamp{i}',t=bar(106)+0.3,side=8+i*0.0,along=-6+i*3,kind='lamp',size=[1,4,1],color='#fff2d6',landmark=(i==2),name='五盏灯' if i==2 else None,
                      appear=dict(t=bar(104)+i*0.95,mode='pop',dur=0.4)))
    O.append(dict(id='egg_catbox',t=bar(37)+0.5,side=-5,kind='group',radius=1.5,egg=True,name='纸箱猫耳',
                  parts=[dict(kind='box',pos=[0,0.6,0],size=[1.6,1.2,1.6],color='#c79a6b'),dict(kind='cone',pos=[-0.4,1.5,0],size=[0.4,0.6,0.4],color='#333'),
                         dict(kind='cone',pos=[0.4,1.5,0],size=[0.4,0.6,0.4],color='#333')],appear=dict(t=bar(38)+0.5,mode='rise',dur=0.3)))
    O.append(dict(id='egg_dots',t=bar(108),side=-10,y=6,kind='group',radius=3,egg=True,name='三个圆点→三颗星',
                  parts=[dict(kind='star',pos=[-2,0,0],size=[1,1,1],color='#ffd84a'),dict(kind='star',pos=[0,0,0],size=[1,1,1],color='#ffd84a'),dict(kind='star',pos=[2,0,0],size=[1,1,1],color='#ffd84a')],
                  appear=dict(t=bar(107),mode='pop',dur=0.5)))
    ev=[dict(t=bar(24),type='burst',at='player',particles='bubbles'),dict(t=bar(24),type='pulse',target='ring',every=c['T']*2,until=bar(32)),
        dict(t=bar(56),type='color',palette=dict(skyTop='#ff8fae'),dur=1.0),dict(t=bar(56),type='pulse',target='dome',every=c['T']*2,until=bar(64)),
        dict(t=bar(71),type='color',palette=dict(skyTop='#3d2a52'),dur=1.5),dict(t=bar(79),type='lower',target='speaker0',dur=0.3),
        dict(t=bar(80),type='flash',dur=0.25),dict(t=bar(88),type='burst',at='player',particles='confetti'),
        dict(t=bar(104),type='light',target='lamp2',dur=4.0)]
    cr=[g(x,1.0) for x in CROWN_T(bar)]
    dia=[g(t,0.5) for t in [bar(4),bar(14),bar(28),bar(44),bar(52),bar(62),bar(76),bar(84),bar(98),bar(106)]]
    return dict(id='omg',title='OMG',palette=P,road=dict(height=0.6,reveal=[dict(t=0,mode='rise',lead=1.8),dict(t=bar(24),mode='unfold',lead=1.6),
                dict(t=bar(71),mode='drop',lead=1.4),dict(t=bar(80),mode='rise',lead=1.4),dict(t=bar(104),mode='fade',lead=2.0)]),
                sections=secs,camera=cam,objects=O,events=ev,diamonds=[dict(t=t,side=0) for t in dia],
                crowns=[dict(t=x) for x in cr],finish=dict(kind='gate'))
WHY={
 'Intro (0–15.2 s)':'a-cappella "OMG" vocal phrases only (no drums in the stem map): 12 taps on the sung syllable entries, 1–4 s gaps = the "waiting for the call" calm.',
 'Verse 1 (15.2–30.3 s)':'finger-snap/clap layer enters with strong hits on step 6 and 14 (the "and" of 2 and 4) — taps on the clap downbeat + those syncopated snaps (s.....s.s.....s.): the first syncopation the player meets.',
 'Verse 1b (30.3–45.4 s)':'full UK-garage kick enters (K...|k...|..k.|..kk / ..K.|k.kk|.kk.|K...): taps on the kicks, odd bars use the off-beat kick pair at steps 2/4 and 10/12 = call (even bar) / response (odd bar).',
 'Chorus 1 / 2 / Final (45.4, 105.9, 166.4 s)':'halftime groove: kick 1, snare 3, kick on 4; the synth hook (other stem, "O" hits on steps 4/8/14 then 6/10/14) answers between drum hits, so even bars are drum-led and odd bars become a 6-tap 8th-note run (2,6,8,10,12,14) following the hook. Final chorus b adds the extra hook 8th (step 6) for the climax.',
 'Verse 2 / 2b / Post':'same garage kick but thinned to 4–5 taps per bar so the vocals breathe; Verse 2b inserts the vocal "V V v v" accent at step 8.',
 'Pre (90.8–105.9 s)':'drums drop out, only bass (..B.|..B.|..B.|..B.) + vocal: taps follow the bass pulses at a relaxed 1.9/s while the phone bridge ramps up 6 units; bar 55 is a 7-tap 8th-note build into Chorus 2.',
 'Bridge (134.2–149.3 s)':'new trap-style kick pattern (...k|..k.|k.k.|.k.k): taps on steps 3,6,8,13,15 / 3,6,8,10,13 — every bar starts on an off-beat, the hardest syncopation in the level, on a narrow 1.8-wide road inside the library.',
 'Break (149.3 s)':'one bar of near silence (2 snare hits + 1 kick): 3 taps, camera to top view.',
 'Dance break (151.2–166.4 s)':'four-on-the-floor kick with 8th-note kick fills: long 8th runs (6, 8 and an 11-tap run on bars 86–87) — the densest passage (3.1 taps/s, 4.2/s peak).',
 'Outro (196.6–212.3 s)':'drums stop, only the synth stabs remain: 2 taps per bar on the stabs, last tap > 1 s before the end.',
}

# ---- v2 layout aligned with codex-ref (concept.png / blueprint.png / design.md): ward -> identity fantasy -> piano tail
def layout(c):
    bar=c['bar']; g=c['gap_mid']; T=c['T']
    P=dict(skyTop='#DCE4DA',skyBottom='#EEF1EA',fog='#DCE4DA',fogStart=32,fogEnd=105,ground='#B8C8BC',groundY=-14,
           road='#F3F0E8',roadSide='#25282B',line='#EFA6B1',light='#FFF8EE',lightIntensity=1.05,ambient='#C9D3CB',particles=None)
    secs=[
     dict(t=0,label='Intro · 病房走廊',palette=dict(skyTop='#D3DCD3',fogEnd=80),camera='iso',note='closed ward corridor, door-frame pairs give the beat scale; ceiling lights come on with the synth plucks'),
     dict(t=bar(8),label='Verse 1 · 治疗桌与五椅',camera='iso',note='meander around the treatment table and five chairs; low walls tighten the space'),
     dict(t=bar(16),label='Verse 1b · 墙板外折',camera='iso',note='ward wall panels fold outward one by one (pre-chorus feel), staircase widens'),
     dict(t=bar(24),label='Chorus 1 · 黑兔舞台',palette=dict(skyTop='#E4EAE1',fogEnd=120),camera='high',note='fall 4 units onto the open stage level; the black low-poly bunny on its halftone base + five stage walls rise on the hook'),
     dict(t=bar(32),label='Verse 2 · 玻璃鞋',camera='side',note='glass slipper sculpture on a plinth, camera swings to side view'),
     dict(t=bar(40),label='Verse 2b · 双折长短路',camera='iso'),
     dict(t=bar(48),label='Pre · 手机桥',palette=dict(light='#F4F6FF',lightIntensity=0.95),camera='low',note='road becomes the long phone bridge B1 (black screen, cream body) climbing L1->L2 (+8)'),
     dict(t=bar(56),label='Chorus 2 · 屏幕块',palette=dict(skyTop='#E8EDE4'),camera='wide',note='fall onto staggered right-angle road; phone-screen blocks lift off-road on the kicks'),
     dict(t=bar(64),label='Post · 错列直角',camera='iso'),
     dict(t=bar(71),label='Bridge · 书页墙与猫',palette=dict(skyTop='#9FAEA6',skyBottom='#C7D0C8',fog='#AAB6AE',ambient='#9AA79F',lightIntensity=0.85),camera='close',note='compressed angular S between book-page walls, road narrows to 1.8 and slopes up; black cat on a shelf'),
     dict(t=bar(79),label='Break · 书页合拢',camera='top',note='one-bar subtraction: pages close inward (stop outside clearance)'),
     dict(t=bar(80),label='Dance break · 舞台五墙',palette=dict(skyTop='#E4EAE1',lightIntensity=1.15),camera='iso',note='five stage walls flip open on the four-on-the-floor; line passes over the start corridor on a bridge (+6)'),
     dict(t=bar(88),label='Final chorus · 兔耳发夹',camera='wide',note='two unequal rectangular hairpins = bunny ears; skybridge B2'),
     dict(t=bar(96),label='Final chorus b · 天桥',camera='iso'),
     dict(t=bar(104),label='Outro · 尾奏琴键',palette=dict(skyTop='#E9ECE6',skyBottom='#F6F4EE',lightIntensity=0.95),camera='high',note='long straight-ish meander to the halftone end plinth; three off-road piano keys; distant layers lower with the piano tail'),
    ]
    cam=[dict(t=0,preset='iso',blend=0),dict(t=bar(8),preset='iso',dist=16,blend=2.0),dict(t=bar(16),preset='iso',blend=2.0),dict(t=bar(24),preset='high',dist=21,blend=1.2),
         dict(t=bar(32),preset='side',blend=2.0),dict(t=bar(40),preset='iso',blend=1.5),dict(t=bar(48),preset='low',blend=2.0),
         dict(t=bar(56),preset='wide',blend=0.9),dict(t=bar(60),preset='iso',blend=2.0),dict(t=bar(71),preset='high',pitch=62,dist=15,blend=1.5),
         dict(t=bar(79),preset='top',blend=0.8),dict(t=bar(80),preset='iso',blend=0.6,shake=0.12),dict(t=bar(88),preset='wide',blend=1.2),
         dict(t=bar(92),preset='iso',blend=2.0),dict(t=bar(104),preset='high',dist=24,blend=4.0)]
    O=[]
    for i in range(4):
        t=1.2+i*3.6
        O.append(dict(id=f'ward_door{i}',t=t,side=(3.2 if i%2==0 else -3.2),kind='group',radius=1.6,
                      parts=[dict(kind='box',pos=[0,1.6,0],size=[0.4,3.2,2.6],color='#C9D3CB'),dict(kind='box',pos=[0,1.4,0],size=[0.45,2.6,1.9],color='#8FA39A'),
                             dict(kind='box',pos=[0,3.4,0],size=[0.5,0.25,1.4],color='#FFFFFF')],react='none',appear=dict(t=max(0.2,t-1.8),mode='rise',dur=0.6)))
    O.append(dict(id='ward_light_row',kind='row',t0=0.5,t1=bar(8),side=3.0,spacing=3.78,bothSides=True,item=dict(kind='box',size=[0.9,0.12,0.4],color='#FFFFFF',react='beat')))
    O.append(dict(id='ward_bed',t=6.0,side=-6,kind='group',radius=2,parts=[dict(kind='box',pos=[0,0.6,0],size=[1.8,0.3,3.4],color='#E6E8E2'),dict(kind='box',pos=[0,1.0,-1.6],size=[1.8,0.9,0.1],color='#AEB7BA')]))
    O.append(dict(id='table_five_chairs',t=bar(10),side=-7,kind='group',radius=4,landmark=True,name='治疗桌与五把椅子',
                  parts=[dict(kind='box',pos=[0,0.9,0],size=[3.2,0.2,1.8],color='#F3F0E8'),dict(kind='box',pos=[0,0.45,0],size=[0.3,0.9,0.3],color='#25282B')]+
                        [dict(kind='box',pos=[x,0.5,z],size=[0.6,1.0,0.6],color='#25282B') for x,z in [(-2.2,0),(2.2,0),(-1,1.6),(1,1.6),(0,-1.6)]],
                  appear=dict(t=bar(9),mode='rise',dur=0.8)))
    for i in range(5):
        t=bar(17)+i*2.8
        O.append(dict(id=f'wallpanel{i}',t=t,side=(4.2 if i%2==0 else -4.2),kind='box',size=[0.3,4.5,3.5],color='#C9D3CB',
                      appear=dict(t=t-1.5,mode='rise',dur=0.5),exit=dict(t=bar(23)+2,mode='fall',dur=0.7),react='none'))
    O.append(dict(id='bunny',t=bar(26),side=11,kind='group',radius=5,landmark=True,name='黑兔雕塑 (OMG cover, low-poly black bunny on halftone plinth)',
                  parts=[dict(kind='box',pos=[0,1.2,0],size=[7,2.4,6],color='#B8C8BC'),dict(kind='box',pos=[0,2.45,0],size=[5,0.1,5],color='#F3F0E8'),
                         dict(kind='sphere',pos=[0,4.6,0],size=[4.6,4.2,4.2],color='#25282B'),dict(kind='box',pos=[0,4.0,-2.0],size=[1.6,1.0,0.3],color='#F3F0E8'),
                         dict(kind='cone',pos=[-1.0,8.0,0],size=[1.2,4.0,1.0],rot=[0,0,8],color='#25282B'),dict(kind='cone',pos=[1.0,8.0,0],size=[1.2,4.0,1.0],rot=[0,0,-8],color='#25282B')],
                  appear=dict(t=bar(24)-0.6,mode='rise',dur=1.4),react='kick'))
    O.append(dict(id='halftone_tiles',kind='row',t0=bar(24),t1=bar(26),side=2.6,spacing=0.9,bothSides=False,item=dict(kind='box',size=[0.5,0.08,0.5],color='#25282B')))
    for i in range(5):
        t=bar(24)+0.5+i*T*2
        O.append(dict(id=f'stagewall{i}',t=bar(27)+i*0.6,side=16+i*1.2,along=-3+i*1.5,kind='box',size=[0.5,7,4],color='#F3F0E8',
                      appear=dict(t=t,mode='rise',dur=0.6),react='none'))
    O.append(dict(id='glass_slipper',t=bar(34),side=-8,kind='group',radius=2.5,landmark=True,name='玻璃鞋',
                  parts=[dict(kind='box',pos=[0,0.6,0],size=[3,1.2,3],color='#B8C8BC'),dict(kind='box',pos=[0,1.5,0.3],size=[0.9,0.5,2.0],color='#DDF2F6'),
                         dict(kind='cylinder',pos=[0,1.8,-0.7],size=[0.15,1.0,0.15],color='#DDF2F6')],appear=dict(t=bar(33),mode='rise',dur=1.0)))
    O.append(dict(id='phone_bridge_body',t=bar(52),side=0,y=-0.7,kind='box',size=[6,0.4,30],color='#F3F0E8',onroad=True,name='手机桥 B1 body (under the road, follows the climb; integrator may stretch along path)',landmark=True))
    O.append(dict(id='phone_screen',t=bar(52),side=4.5,y=-0.5,kind='phone',size=[5,0.5,10],color='#F3F0E8',color2='#25282B',name='手机屏幕 (off-road side)',
                  appear=dict(t=bar(48),mode='unfold',dur=1.0)))
    O.append(dict(id='signal_bars',t=bar(50),side=-9,kind='group',radius=3,name='信号格',
                  parts=[dict(kind='box',pos=[-1.5+k,0.75*(k+1),0],size=[0.8,1.5*(k+1),0.8],color='#25282B') for k in range(4)]))
    for i in range(5):
        t=bar(57)+i*2.5
        O.append(dict(id=f'screenblock{i}',t=t,side=(9 if i%2==0 else -9),kind='box',size=[3,0.4,5],color='#25282B',color2='#F3F0E8',
                      appear=dict(t=t-1.6,mode='rise',dur=0.5),react='kick'))
    for i in range(6):
        t=bar(72)+i*2.4
        O.append(dict(id=f'bookpage{i}',t=t,side=(3.6 if i%2==0 else -3.6),kind='box',size=[0.15,5,3.2],rot=(12 if i%2==0 else -12),color='#F3F0E8',
                      appear=dict(t=t-1.5,mode='unfold',dur=0.5),exit=dict(t=bar(79)+0.3,mode='fall',dur=0.6)))
    O.append(dict(id='cat_shelf',t=bar(75),side=-7,kind='group',radius=2.5,landmark=True,name='书架上的黑猫',
                  parts=[dict(kind='box',pos=[0,1.5,0],size=[2.6,3,1.2],color='#C9D3CB'),dict(kind='sphere',pos=[0,3.4,0],size=[0.9,0.8,0.7],color='#25282B'),
                         dict(kind='sphere',pos=[0,4.0,0],size=[0.6,0.6,0.6],color='#25282B'),dict(kind='cone',pos=[-0.2,4.4,0],size=[0.2,0.35,0.2],color='#25282B'),
                         dict(kind='cone',pos=[0.2,4.4,0],size=[0.2,0.35,0.2],color='#25282B')]))
    for i in range(5):
        O.append(dict(id=f'stage5_{i}',t=bar(81)+i*1.6,side=(8 if i%2==0 else -8),kind='box',size=[0.5,6,4],color='#F3F0E8',
                      appear=dict(t=bar(80)+i*T*2,mode='unfold',dur=0.4),react='kick'))
    O.append(dict(id='ear_sculpture_l',t=bar(90),side=-12,kind='cone',size=[2.4,9,1.6],color='#25282B',landmark=True,name='兔耳双雕塑',appear=dict(t=bar(88),mode='rise',dur=1.2)))
    O.append(dict(id='ear_sculpture_r',t=bar(90),side=-15,along=2,kind='cone',size=[2.4,8,1.6],color='#25282B',appear=dict(t=bar(88)+0.3,mode='rise',dur=1.2)))
    for i in range(3):
        O.append(dict(id=f'piano_key{i}',t=bar(105)+i*1.9,side=(6 if i%2==0 else -6),kind='box',size=[1.2,0.5,4],color=('#F3F0E8' if i!=1 else '#25282B'),react='tap',
                      landmark=(i==1),name='尾奏琴键' if i==1 else None,appear=dict(t=bar(104)+i*1.9,mode='rise',dur=0.6)))
    O.append(dict(id='end_plinth',t=bar(106),side=-14,kind='group',radius=3,parts=[dict(kind='box',pos=[0,0.5,0],size=[5,1,5],color='#B8C8BC'),dict(kind='box',pos=[0,1.05,0],size=[3.6,0.1,3.6],color='#25282B')]))
    O.append(dict(id='egg_cat_ears',t=bar(77)+0.5,side=-5,kind='group',radius=1.5,egg=True,name='E1 猫影：长音时书页阴影组成猫耳，猫转头',
                  parts=[dict(kind='cone',pos=[-0.4,0.3,0],size=[0.5,0.7,0.1],color='#5A6660'),dict(kind='cone',pos=[0.4,0.3,0],size=[0.5,0.7,0.1],color='#5A6660')],
                  appear=dict(t=bar(77),mode='fade',dur=0.8),exit=dict(t=bar(78)+1,mode='fade',dur=0.8)))
    O.append(dict(id='egg_three_dots',t=bar(108),side=-10,y=6,kind='group',radius=3,egg=True,name='E2 来电三点 -> 三颗小星',
                  parts=[dict(kind='star',pos=[-2,0,0],size=[1,1,1],color='#E3BD60'),dict(kind='star',pos=[0,0,0],size=[1,1,1],color='#E3BD60'),dict(kind='star',pos=[2,0,0],size=[1,1,1],color='#E3BD60')],
                  appear=dict(t=bar(107),mode='pop',dur=0.5)))
    ev=[dict(t=bar(8),type='light',target='ward_light_row',dur=1.0),dict(t=bar(24),type='burst',at='player',particles='dust'),
        dict(t=bar(24),type='raise',target='bunny',dur=1.4),dict(t=bar(56),type='flash',dur=0.2),
        dict(t=bar(71),type='color',palette=dict(skyTop='#9FAEA6'),dur=1.5),dict(t=bar(79),type='lower',target='bookpage0',dur=0.4),
        dict(t=bar(80),type='flash',dur=0.25),dict(t=bar(88),type='raise',target='ear_sculpture_l',dur=1.2),
        dict(t=bar(104),type='color',palette=dict(skyTop='#E9ECE6'),dur=4.0),dict(t=bar(106),type='lower',target='stage5_0',dur=3.0)]
    cr=[g(x,1.0) for x in CROWN_T(bar)]
    dia=[g(t,0.5) for t in [bar(4),bar(14),bar(28),bar(44),bar(52),bar(62),bar(76),bar(84),bar(98),bar(106)]]
    return dict(id='omg',title='OMG',palette=P,road=dict(height=0.6,reveal=[dict(t=0,mode='rise',lead=1.8),dict(t=bar(24),mode='unfold',lead=1.6),
                dict(t=bar(71),mode='drop',lead=1.4),dict(t=bar(80),mode='rise',lead=1.4),dict(t=bar(104),mode='fade',lead=2.0)]),
                sections=secs,camera=cam,objects=O,events=ev,diamonds=[dict(t=t,side=0) for t in dia],
                crowns=[dict(t=x) for x in cr],finish=dict(kind='custom',note='halftone end plinth with the black bunny silhouette',parts=[dict(kind='box',pos=[0,0,4],size=[6,1,6],color='#25282B')]),
                collectibleColors=dict(diamond='#88C7D5',crown='#E3BD60'))

CROWN_T=lambda bar: [bar(48)+0.5,bar(79)+0.5]

# ---- v3 route choreography (2026-10-18 user feedback: richer routes). Overrides MOTIFS/PIVOTS/ELEV above.
_b=lambda n: 0.0288+n*1.88971
ELEV=[dict(t=_b(24),type='fall',dy=-4),                      # Chorus 1 drops onto the stage floor (-4)
      dict(t0=_b(33),t1=_b(35),type='ramp',dy=8),            # Verse 2: spiral staircase around the glass-slipper tower (-4 -> +4)
      dict(t0=_b(48.3),t1=_b(52),type='ramp',dy=6),          # Pre: phone bridge climbs (+4 -> +10), sweeps over Chorus 1
      dict(t=_b(56),type='fall',dy=-6),                      # Chorus 2 drop (+4)
      dict(t0=_b(71.2),t1=_b(78),type='ramp',dy=4),          # Bridge: book-page switchbacks climb (+8)
      dict(t=_b(88),type='fall',dy=-8),                      # Final chorus falls back to the ward level (0)
      dict(t0=_b(96.2),t1=_b(99.5),type='ramp',dy=5),        # Final chorus b: skybridge B2 (+5) over the hairpins
      dict(t=_b(104),type='fall',dy=-5)]                     # Outro: back to 0
A=lambda aim,w=0.6,**k: dict(w_aim=w,**k)
ROUTE=[(0,'free',0,A(0,1.0)),(_b(4),'free',90,A(0,1.0)),
       (_b(8),'switch',90,A(0,0.25,thr=0.5)),                       # Verse 1: serpentine switchbacks along the ward wall
       (_b(16),'meander',0,A(0,0.3)),                                # Verse 1b: tight zigzag corridor between wall panels
       (_b(24),'stair',135,A(0)),(_b(26),'stair',225,A(0)),(_b(28),'stair',135,A(0)),(_b(30),'stair',45,A(0)),   # Chorus 1: zigzag of staircases
       (_b(32),'switch',270,A(0,0.3,thr=0.5)),(_b(33),'spiral',None,A(0,0,hand='R',w_motif=2.5)),(_b(35),'stair',300,A(0)),
       (_b(38),'meander',270,A(0,0.4)),(_b(42),'stair',0,A(0)),(_b(44),'switch',60,A(0,0.4,thr=0.4)),
       (_b(48),'free',150,A(0,1.2,cross=1.5)),                       # Pre: long sweeping phone bridge crossing over Chorus 1
       (_b(56),'stair',90,A(0)),(_b(58),'stair',180,A(0)),(_b(60),'stair',270,A(0)),(_b(62),'stair',0,A(0)),   # Chorus 2: ring of staircases
       (_b(64),'switch',270,A(0,0.3,thr=0.45)),(_b(68),'meander',180,A(0,0.4)),
       (_b(71),'switch',200,A(0,0.3,thr=0.4)),                       # Bridge: narrow climbing switchbacks between book pages
       (_b(79),'free',None,{}),
       (_b(80),'stair',330,A(0,0.5,cross=1.5)),(_b(82),'stair',60,A(0,0.5,cross=1.5)),(_b(84),'stair',330,A(0,0.5,cross=1.5)),(_b(86),'stair',60,A(0,0.5,cross=1.5)),
       (_b(88),'spiral',None,A(0,0,hand='L',w_motif=1.2)),(_b(89),'stair',90,A(0)),(_b(90),'spiral',None,A(0,0,hand='L',w_motif=1.2)),(_b(91),'stair',90,A(0)),  # bunny-ear hairpins
       (_b(92),'meander',180,A(0,0.4)),
       (_b(96),'stair',270,A(0,0.5,cross=1.5)),(_b(98),'stair',180,A(0,0.5,cross=1.5)),(_b(100),'stair',90,A(0,0.5,cross=1.5)),(_b(102),'stair',0,A(0,0.5,cross=1.5)),
       (_b(104),'free',180,A(0,0.8))]
FORKS=[_b(18.5),_b(37.2),_b(66.3),_b(93.1),_b(107.4),_b(122.6),_b(169.2)]
BUILDINGS=[dict(id='ward_block',t0=_b(16.2),t1=_b(19.8),color='#C9D3CB',h=3.0),      # Verse 1b: the zigzag runs through a cut-away ward
           dict(id='library',t0=_b(72.2),t1=_b(75.8),color='#F3F0E8',h=4.2)]         # Bridge: switchbacks inside the book-page library
ART={'backdrop':'art/sky.jpg','ground':{'src':'art/ground-halftone.jpg','scale':36},
     'files':{'art/sky.jpg':'soft sage->cream sky with halftone clouds and a blush horizon (backdrop)',
              'art/ground-halftone.jpg':'tileable halftone dots on sage (ground, from the OMG cover print)',
              'art/bunny-poster.jpg':'halftone black bunny poster, blank white mask, no features (stage wall posters)',
              'art/phone-screen.jpg':'black phone screen with chat bubbles + typing dots, no text (phone bridge face)',
              'art/slipper-cat-decal.png':'glass slipper + black cat on a storybook, transparent sticker (fairy-tale identity)'}}
def more_objects(c):
    bar=c['bar']
    return [dict(id='poster_bunny_a',t=bar(25),side=-10,kind='image',src='art/bunny-poster.jpg',size=[5.4,0,7.2],mode='upright',appear=dict(t=bar(24)-0.4,mode='unfold',dur=0.6)),
            dict(id='poster_bunny_b',t=bar(81),side=10,kind='image',src='art/bunny-poster.jpg',size=[5.4,0,7.2],mode='upright',appear=dict(t=bar(80)-0.4,mode='unfold',dur=0.6),react='kick'),
            dict(id='phone_face',t=bar(50),side=8,y=0.5,kind='image',src='art/phone-screen.jpg',size=[5,0,9],mode='upright',appear=dict(t=bar(48),mode='rise',dur=0.8)),
            dict(id='slipper_sticker',t=bar(34),side=-9,y=2,kind='image',src='art/slipper-cat-decal.png',size=[6,0,4.5],mode='billboard',alpha=True,appear=dict(t=bar(33),mode='pop',dur=0.5)),
            dict(id='cat_sticker',t=bar(76),side=9,y=3,kind='image',src='art/slipper-cat-decal.png',size=[5,0,3.75],mode='billboard',alpha=True,appear=dict(t=bar(75),mode='pop',dur=0.5))]
