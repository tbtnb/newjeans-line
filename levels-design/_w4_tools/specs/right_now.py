# Right Now (172 BPM drum & bass). bar = 1.395 s; grid = 8 eighths per bar (0.174 s). bar0 = 0.366 s.
SUB=8
MIN_GAP=0.15
METRIC=[0.35,-0.1,0.1,-0.05,0.3,-0.1,0.1,-0.05]
SECTIONS=[
 dict(bars=(0,8),label='Intro',kind='intro',tpb=1.5,maxrun=1,w={'other':1.0,'vocal':0.5}),
 dict(bars=(8,24),label='Verse 1',kind='verse',tpb=3.2,maxrun=2,w={'kick':1,'snare':1,'vocal':0.8,'bass':0.3}),
 dict(bars=(24,32),label='Pre-chorus 1',kind='pre',tpb=3.8,maxrun=2,w={'kick':0.9,'snare':1,'vocal':1.0}),
 dict(bars=(32,48),label='Chorus 1',kind='chorus',tpb=4.6,maxrun=3,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(48,56),label='Verse 2',kind='verse',tpb=3.4,maxrun=2,w={'kick':1,'snare':1,'vocal':0.9}),
 dict(bars=(56,72),label='Half-time bridge',kind='bridge',tpb=2.4,maxrun=2,w={'snare':1,'vocal':1.1,'other':0.6,'kick':0.6}),
 dict(bars=(72,84),label='Chorus 2',kind='chorus',tpb=4.8,maxrun=3,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(84,88),label='Break',kind='break',tpb=1.5,maxrun=1,w={'other':1,'vocal':0.8}),
 dict(bars=(88,104),label='Final chorus',kind='chorus',tpb=5.3,maxrun=4,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(104,112),label='Outro',kind='outro',tpb=1.5,maxrun=1,w={'other':1.0}),
]
ADD=[]; REMOVE=[(0,0)]
