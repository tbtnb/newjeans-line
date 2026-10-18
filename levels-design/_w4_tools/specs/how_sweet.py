# How Sweet (125 BPM Miami bass). bar = 1.92 s; 16th grid 0.12 s, taps >= 2 sixteenths apart (0.24 s). bar0 = 0.362 s.
SECTIONS=[
 dict(bars=(0,4),label='Intro',kind='intro',tpb=1.5,w={'other':1.0}),
 dict(bars=(4,20),label='Verse 1',kind='verse',tpb=1.7,w={'vocal':1.1,'snare':1,'kick':0.8,'other':0.5}),
 dict(bars=(20,24),label='Pre-chorus 1',kind='pre',tpb=2.6,w={'kick':1,'snare':1,'vocal':0.8}),
 dict(bars=(24,40),label='Chorus 1',kind='chorus',tpb=2.3,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(40,56),label='Verse 2',kind='verse',tpb=1.7,w={'vocal':1.1,'snare':1,'kick':0.8,'other':0.5}),
 dict(bars=(56,72),label='Chorus 2',kind='chorus',tpb=2.5,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(72,80),label='Bridge',kind='bridge',tpb=2.0,w={'kick':1,'snare':1,'vocal':0.8}),
 dict(bars=(80,88),label='Build',kind='pre',tpb=2.4,w={'other':0.9,'vocal':1,'snare':0.8,'kick':0.6}),
 dict(bars=(88,104),label='Final chorus',kind='chorus',tpb=2.8,w={'kick':1,'snare':1,'vocal':0.9,'other':0.4}),
 dict(bars=(104,112),label='Outro',kind='outro',tpb=1.2,w={'other':1.0,'vocal':0.4}),
]
ADD=[]; REMOVE=[(0,0)]
# Hand phrase plans (Dancing Line-style 8th runs at phrase ends, on the synth/vocal 8th figure heard in the 'other'/'vocal' stems)
RUN='1000100010101010'
SECTIONS[2]['plan']={3:'0010000010101010'}           # bar 23: pre-chorus pickup run into Chorus 1
SECTIONS[3]['plan']={7:RUN,15:RUN}                    # bars 31,39
SECTIONS[5]['plan']={7:RUN,15:RUN}                    # bars 63,71
SECTIONS[7]['plan']={7:'1000100010101010'}            # bar 87: build ends with a run into the final chorus
SECTIONS[8]['plan']={3:'1000101010101010',7:RUN,11:'1000101010101010',15:'1010101010101010'}  # bars 91,95,99,103 (last = 8-run climax)
