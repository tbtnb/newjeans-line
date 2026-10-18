# Supernatural (109 BPM, NJS). bar = 2.202 s, eighth = 0.275 s. bar0 = 0.358 s.



SECTIONS=[
 dict(bars=(0,4),label='Intro',kind='intro',tpb=2,w={'snare':1,'vocal':0.8,'other':0.6}),
 dict(bars=(4,12),label='Groove',kind='verse',tpb=2.8,w={'kick':1,'snare':1.1,'other':0.6,'bass':0.5}),
 dict(bars=(12,20),label='Verse 1',kind='verse',tpb=3.2,w={'kick':0.8,'snare':1,'vocal':0.9,'bass':0.3}),
 dict(bars=(20,28),label='Pre-chorus 1',kind='pre',tpb=4.5,w={'kick':0.8,'snare':1,'vocal':1.0}),
 dict(bars=(28,36),label='Chorus 1',kind='chorus',tpb=5.0,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(36,44),label='Verse 2',kind='verse',tpb=3.6,w={'kick':0.8,'snare':1,'vocal':1.0}),
 dict(bars=(44,52),label='Bridge',kind='bridge',tpb=2.5,w={'vocal':1.3,'kick':0.6,'snare':0.6,'other':0.4}),
 dict(bars=(52,60),label='Chorus 2',kind='chorus',tpb=5.5,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(60,68),label='Interlude',kind='break',tpb=3,w={'other':1.0,'snare':0.9,'vocal':0.5}),
 dict(bars=(68,76),label='Final chorus',kind='chorus',tpb=6.0,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(76,84),label='Outro',kind='outro',tpb=2,w={'snare':1,'other':0.8,'vocal':0.6}),
]
ADD=[]; REMOVE=[]
SECTIONS[3]['plan']={7:'1010101010101010'}      # bar 27: pre-chorus build, snare roll -> 8-tap eighth run into chorus downbeat
SECTIONS[6]['plan']={7:'1010101010101000'}      # bar 51: drum fill re-entry (snare hits on 1,2,3) -> 7-tap run (Dancing Line style 7-burst)
SECTIONS[9]['plan']={7:'1010101010001000'}      # bar 75: last chorus bar, settle before outro
REMOVE=[(0,0),(0,4)]                           # first tap must be >= 1.0 s
