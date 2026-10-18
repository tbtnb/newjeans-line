# Hand-written per-section motifs (16th positions within a bar). db = grid index of bar-0 downbeat.
CONFIGS={}
E8=[0,2,4,6,8,10,12,14]
HOOK_A=[2,4,6,8,12,15]; HOOK_B=[2,4,8,10,12,15]
GV_A=[0,4,8,12,14]; GV_B=[0,4,6,8,12]
CONFIGS['eta']=dict(old=232,db=15,mingap=0.2,sections=[
 dict(bars=(0,3),label='Intro · phone desk',kind='intro',motif=[[0,6,10],[0,6,10,13],[0,4,6,10,13]]),
 dict(bars=(3,11),label='Verse 1 · first message',kind='verse',motif=[[0,4,8,12],[0,8,12],[0,4,8,12],[0,8,14]],fillpat=[0,4,8,10,12,14],override={10:[0,4,8,10,12,14]}),
 dict(bars=(11,19),label='Pre 1 · forwarding blocks',kind='pre',motif=[[0,8,12],[0,4,8,12],[0,8,12],[0,4,8,12,14],[0,4,8,12],[0,4,6,8,12,14],[0,2,4,6,8,12,14],E8],phrase=99,burst={18:[13,15]}),
 dict(bars=(19,26),label='Chorus 1 · signal city hook',kind='chorus',motif=[HOOK_A,HOOK_B],fillpat=[2,4,6,8,10,12,15],lastpat=[2,4,8,12]),
 dict(bars=(26,27),label='Stop 1 · E-T-A voice chops',kind='break',motif=[[2,4,7,9,11,13]]),
 dict(bars=(27,35),label='Verse 2 · rumor mill',kind='verse',motif=[[0,4,8,12],[0,4,8,14],[0,4,8,12],[0,6,8,12,14]],fillpat=[0,4,6,8,10,12,14]),
 dict(bars=(35,43),label='Pre 2 · fragments rising',kind='pre',motif=[[0,8,12],[0,4,8,12],[0,8,12],[0,4,8,12,14]],fillpat=[0,4,6,8,10,12,14]),
 dict(bars=(43,51),label='Pre 3 · tower lift',kind='pre',motif=[[0,4,8,12],GV_A,[0,4,8,12],[0,4,6,8,10,12,14]],lastpat=E8,burst={46:[15],50:[13,15]}),
 dict(bars=(51,58),label='Chorus 2 · assembled scene hook',kind='chorus',motif=[HOOK_A,HOOK_B],fillpat=[2,4,6,8,10,12,15],lastpat=[2,4,8,12],burst={51:[3],52:[3]}),
 dict(bars=(58,59),label='Stop 2 · E-T-A voice chops',kind='break',motif=[[2,4,7,9,11,13]]),
 dict(bars=(59,67),label='Final A · rush hour',kind='chorus',motif=[[0,4,8,12,14],[0,2,4,8,12,14]],fillpat=E8,burst={62:[13],64:[13]}),
 dict(bars=(67,75),label='Final B · arrival sprint',kind='chorus',motif=[[0,2,4,8,10,12,14],[0,4,6,8,12,14]],fillpat=E8,override={73:E8,74:[0,2,4,6,8,10,12]},burst={71:[13],73:[13],74:[13]}),
 dict(bars=(75,83),label='Outro · two bench lamps',kind='outro',motif=[[6,10,14],[0,8],[0,8],[0,8],[0],[0],[0],[0]],phrase=99),
])
CONFIGS['cool-with-you']=dict(old=107,db=3,mingap=0.2,sections=[
 dict(bars=(0,8),label='Intro · empty gallery',kind='intro',motif=[[0],[6,10],[0],[0,10]],minS=0.5),
 dict(bars=(8,16),label='Verse 1 · reflections wake',kind='verse',motif=[[0,10],[0,6,10]],override={9:[0,8,14]},fillpat=[0,3,6,10]),
 dict(bars=(16,24),label='Verse 1b · rain curtain',kind='pre',motif=[[0,10],[0,6,10]],fillpat=[0,3,6,10,12,14]),
 dict(bars=(24,32),label='Hook · moonlit pool (stripped)',kind='chorus',motif=[[0,8],[0,8],[0,8],[0,8,12]],minS=0.4),
 dict(bars=(32,40),label='Drop 1 · open courtyard',kind='drop',motif=[[0,6,10,12],[0,6,10]],fillpat=[0,3,6,8,10,12,14],burst={39:[4]}),
 dict(bars=(40,48),label='Verse 2 · two lights approach',kind='verse',motif=[[0,10],[0,6,10]],fillpat=[0,3,6,10,12]),
 dict(bars=(48,52),label='Break · one light leaves',kind='break',motif=[[0],[0,10],[0],[0,6,10]],minS=0.4),
 dict(bars=(52,56),label='Build · wings unfold',kind='pre',motif=[[0,8],[0,6,10],[0,4,6,10,12],[0,2,4,6,8,10,12,14]],phrase=99),
 dict(bars=(56,64),label='Final drop A · feather storm',kind='drop',motif=[[0,6,10,12],[0,6,10]],fillpat=[0,3,6,8,10,12,14],burst={59:[4],63:[4]}),
 dict(bars=(64,72),label='Final drop B · choosing to stay',kind='drop',motif=[[0,3,6,10,12],[0,6,10,12]],fillpat=[0,2,4,6,8,10,12,14],override={70:[0,2,4,6,8,10,12,14],71:[0,2,4,6,8,10,12]},burst={66:[4]}),
 dict(bars=(72,79),label='Outro · open exit',kind='outro',motif=[[0],[],[0,12],[],[0],[],[0]],phrase=99,minS=0.4),
])
CONFIGS['get-up']=dict(old=16,db=2,mingap=0.2,sections=[
 dict(bars=(0,4),label='After the rain · shallow water',kind='intro',motif=[[8],[0,8],[0,8],[0,8]],minS=0.3),
 dict(bars=(4,8),label='One warm light',kind='verse',motif=[[0,8,14],[0,8],[0,8],[0,8,14]],minS=0.3),
 dict(bars=(8,12),label='Horizon gathers',kind='chorus',motif=[[0,8,12],[0,8,14],[0,8,12],[0,8,14]],minS=0.3),
 dict(bars=(12,16),label='Five lights · moon-green grass',kind='outro',motif=[[0,8,14],[0,8],[0,8],[0,8]],minS=0.3),
 dict(bars=(16,17),label='Last step',kind='outro',motif=[[8]],minS=0.3),
])
CONFIGS['asap']=dict(old=83,db=3,mingap=0.2,sections=[
 dict(bars=(0,2),label='Intro · snaps in the grass',kind='intro',motif=[[8],[0,8]],minS=0.4),
 dict(bars=(2,6),label='Verse 1 · moon-green meadow',kind='verse',motif=[[0,6,10],[0,10],[0,8],[0,10]],minS=0.4),
 dict(bars=(6,14),label='Verse 1b · clock in the sky',kind='verse',motif=[[0],[0,8],[0],[0,6,10]],minS=0.4),
 dict(bars=(14,22),label='Pre · letters behind trees',kind='pre',motif=[[0,10],[0,6],[0,8],[0]],minS=0.4,burst={18:[11,15]}),
 dict(bars=(22,30),label='Chorus 1 · swing of pendulums',kind='chorus',motif=[[0,6,10],[0,10],[0,8],[0,6,8,10,12,14]],minS=0.35),
 dict(bars=(30,31),label='Stop · held breath',kind='break',motif=[[4,8]],minS=0.4),
 dict(bars=(31,39),label='Verse 2 · water garden',kind='verse',motif=[[0,8],[0,8],[0,8],[0,4,6,8,12]],minS=0.4),
 dict(bars=(39,47),label='Dance break · stars in groups',kind='drop',motif=[[0,8,12],[0,6,12],[0,8,12],[0,2,4,6,8,10,12,14]],minS=0.4,burst={40:[11,13],41:[11],42:[3,11]}),
 dict(bars=(47,50),label='Turnaround',kind='post',motif=[[0,8],[0,8,12],[0,4,8,12]],minS=0.4,burst={48:[11],49:[5]}),
 dict(bars=(50,62),label='Chorus 2 · the small house',kind='chorus',motif=[[0,8],[0,8],[0,8],[0,6,8,10,12,14]],minS=0.4,burst={57:[11],61:[11]}),
 dict(bars=(62,65),label='Hush · lamp flickers',kind='break',motif=[[0],[0,8],[0]],minS=0.3),
 dict(bars=(65,70),label='Final hook · lamp lights',kind='chorus',motif=[[4,8,12],[0,6,10],[0,8],[0,6,8,10,12,14],[0,8]],minS=0.3,burst={66:[11]}),
 dict(bars=(70,72),label='Outro · pollen bunny',kind='outro',motif=[[0],[0]],minS=0.3),
])
