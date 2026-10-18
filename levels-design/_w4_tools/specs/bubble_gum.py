# Bubble Gum (105 BPM). bar = 2.286 s; 16th grid 0.143 s, taps >= 2 sixteenths apart (0.286 s). bar0 = 2.079 s.
SECTIONS=[
 dict(bars=(0,7),label='Intro',kind='intro',tpb=1.3,w={'other':1.0}),
 dict(bars=(7,15),label='Verse 1',kind='verse',tpb=2.4,w={'vocal':1.1,'snare':0.9,'kick':0.8,'other':0.5}),
 dict(bars=(15,24),label='Pre-chorus 1',kind='pre',tpb=3.0,w={'vocal':1.0,'snare':1,'kick':0.9,'other':0.5}),
 dict(bars=(24,34),label='Chorus 1',kind='chorus',tpb=3.7,w={'kick':0.5,'snare':0.6,'vocal':1.6,'other':0.4}),
 dict(bars=(34,39),label='Breakdown',kind='break',tpb=1.6,w={'vocal':1.2,'other':0.6}),
 dict(bars=(39,51),label='Verse 2',kind='verse',tpb=2.4,w={'vocal':1.1,'snare':0.9,'kick':0.8,'other':0.6}),
 dict(bars=(51,59),label='Pre-chorus 2',kind='pre',tpb=2.9,w={'vocal':1.0,'snare':1,'kick':0.9,'other':0.5}),
 dict(bars=(59,71),label='Chorus 2',kind='chorus',tpb=3.8,w={'kick':0.5,'snare':0.6,'vocal':1.6,'other':0.4}),
 dict(bars=(71,83),label='Final chorus',kind='chorus',tpb=4.2,w={'kick':0.5,'snare':0.6,'vocal':1.6,'other':0.4}),
 dict(bars=(83,84),label='Outro',kind='outro',tpb=1,w={'snare':1,'vocal':1}),
]
ADD=[]; REMOVE=[]
SECTIONS[2]['plan']={8:'1000100010101010'}   # bar 23: pre-chorus pickup (kick+clap build) -> 4-tap 8th run into Chorus 1
SECTIONS[6]['plan']={7:'1000100010101010'}   # bar 58: same pickup into Chorus 2 (call/response with bar 23)
