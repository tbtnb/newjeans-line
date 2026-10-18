"""chart-report.md, chart-sync.csv, analysis.json, analysis.md per song. Heavy part (audio decode) - run under flock."""
import json, sys, numpy as np, librosa
from configs import CONFIGS
from paths import WORK, OUT, AUDIO
JUDGE={'eta':(40,55,90),'cool-with-you':(40,55,95),'get-up':(50,100,125),'asap':(40,57,95)}
TIER={'eta':'hard','cool-with-you':'moderate','get-up':'easy','asap':'hard'}
ORIG=[('The Racing (hardest)',220,440),('Amusement Park','-',512),('Storm','-',460),('The Chaos',136,408),('Chinese Garden',148,296),('Winter',140,280),('The Piano',125,250),('The Autumn',96,'-')]
TITLE={'eta':'ETA','cool-with-you':'Cool With You','get-up':'Get Up','asap':'ASAP'}
GROOVE={
 'eta':'135 BPM four-on-the-floor Jersey-club/pop: kick on every beat, snare/clap on 2 and 4, constant 16th hats, syncopated vocal hook landing on the "e" and "a" 16ths. Two a-cappella "E-T-A" voice-chop stops (bars 26 and 58) cut the drums for one bar.',
 'cool-with-you':'135 BPM UK-garage two-step at half-time feel: kick on 1 and the "and" of 3 (16th 10), rim/snare on 2/4, swung hats; long airy vocal lines. A stripped hook (bars 24-32) and a near-silent break (48-52) before the build.',
 'get-up':'120 BPM ambient interlude, 36 s: no drum kit, a soft pulse on the half-bar, stacked vocal harmonies swelling in two-bar phrases; grid confidence is low (resultant 0.33), so only clearly audible swells are used.',
 'asap':'130 BPM soft house/R&B: muted kick on 1 and 3, finger snaps / rim on 2 and 4, gentle synth chords; vocal phrases breathe with 1-2 bar gaps. One silent "held breath" bar (30), a dance break with denser percussion (39-47), a hush (62-65) before the final hook.'}
PROSE={
 'eta':"""The chart follows the groove instead of every hat: verses sit on the four-on-the-floor kick with small syncopated pickups (16th 14 = the "a" before the next downbeat), the pre-choruses build bar by bar from quarters to a full 8th run (bar 18 is E8), and both choruses use the hook's own rhythm (16ths 2-4-6-8-12-15 / 2-4-8-10-12-15), which is why the road turns on the off-beats there. The two "E-T-A" stops take the six voice chops exactly. The final A/B choruses are the climax: 8th runs every fourth bar and a 19-tap run with 16th flams (131.0-134.7 s) into the outro, mirroring Dancing Line's long climax runs. The outro thins to one tap per bar so the ending breathes.""",
 'cool-with-you':"""Two-step needs restraint: the kick pattern (1 and the "and" of 3, 16ths 0 and 10) carries the verses, with the 16th-6 ghost added every other bar; phrase-end bars get the garage fill (0-3-6-10[-12-14]). The stripped hook only takes downbeats and half-bars so the moonlit-pool section reads as long, calm straights. Drops add the snare on 12 and an 8th fill at each phrase end; the final drop B ends with two full 8th bars (15-tap run, 124.8-127.9 s), the densest moment, then the outro opens up to one tap every two bars.""",
 'get-up':"""Get Up has no drums, so the chart rides the half-bar swells (16ths 0 and 8 at 120 BPM = every 1.0 s) and adds the pick-up on 16th 12/14 only where a vocal entry is audible. 39 taps (old 16) keeps the interlude meditative: no runs longer than two taps, wide road, slow speed. The last tap lands on the final vocal swell at 33.3 s and the line glides to the end of the 36 s file.""",
 'asap':"""ASAP is soft, so density stays moderate but musically placed: verses take the kick on 1 plus vocal pickups (16ths 6/10), the pre answers the vocal call-and-response (0-10, 0-6, 0-8), choruses end every phrase with a 6-tap 8th fill (0-6-8-10-12-14). The silent bar 30 has just the two snaps (that is where the line falls a level). The dance break is the busiest (34 taps with a full 8th bar each phrase, 9-tap runs at 77.9 s and 85.3 s); the hush drops to one tap per bar before the final hook."""}
def attack_offsets(slug,times):
    """same attack measure as fitgrid.py: 2 ms RMS (causal) in dB, 3 ms smoothing, max slope within +-35 ms, minus 2.5 ms filter delay"""
    import scipy.signal as ss
    y,sr=librosa.load(f'{AUDIO}/{slug}.mp3',sr=22050)
    e=np.sqrt(ss.lfilter(np.ones(44)/44,1,y**2)); le=20*np.log10(e+1e-6); le=ss.lfilter(np.ones(66)/66,1,le); der=np.diff(le)
    out=[]
    for t in times:
        a_=int((t-0.035)*sr); b_=int((t+0.035)*sr); k=np.argmax(der[a_:b_])
        out.append(((a_+k)/sr-0.0025-t, der[a_+k]))
    return out
def main(slug):
    C=CONFIGS[slug]; taps=json.load(open(f'{WORK}/{slug}.taps.json')); al=json.load(open(f'{WORK}/{slug}.al.json')); G=al['grid']
    old={x['id']:x for x in json.load(open(f'{WORK}/old_levels.json'))}[slug]['turns']
    chart=json.load(open(f'{OUT}/{slug}/chart.json')); secs=chart['sections']; dur=al['duration']
    T=np.array([x['t'] for x in taps]); g=np.diff(T)
    offs=attack_offsets(slug,T)
    sl=np.array([o[1] for o in offs]); clear=sl>=np.nanpercentile(sl,75)
    om=np.array([o[0] for o in offs])*1000
    med=np.nanmedian(om[clear]); mad=np.nanmedian(np.abs(om[clear]-med))
    best=cur=0; bs=st=0
    for i,x in enumerate(g):
        if x<=0.3:
            if cur==0: st=i
            cur+=1
            if cur>best: best,bs=cur,st
        else: cur=0
    runs=[]; cur=0
    for i,x in enumerate(g):
        if x<=0.3:
            if cur==0: st=i
            cur+=1
        else:
            if cur+1==best+1 and cur>0: runs.append(T[st])
            cur=0
    if cur==best and cur>0: runs.append(T[st])
    pf,gd,ms=JUDGE[slug]
    avg=len(T)/dur*60; peak1=max(int(((T>=t)&(T<t+1.0)).sum()) for t in T)*60; peakg=60/g.min()
    bursts=[x for x in taps if x.get('burst')]
    L=[f"# {TITLE[slug]}: chart report (worker 3)\n",
       f"| | value |\n|---|---|\n| legacy taps | {len(old)} |\n| new taps | **{len(T)}** (x{len(T)/len(old):.2f}) |\n| grid | {G['bpm']:.3f} BPM, 16th = {G['per16']:.6f} s, phase {G['phase']:.4f} s, attack calibration {G['attack_cal_ms']} ms |\n"
       f"| min gap | {g.min():.3f} s |\n| fastest run | {best+1} taps with gaps <= 0.30 s, from {T[bs]:.2f} s to {T[bs+best]:.2f} s{'' if len(runs)<2 else ' (also at '+', '.join(f'{r:.1f}' for r in runs[1:])+' s)'} |\n"
       f"| attack offset (measured attack minus tap time, strongest-quartile attacks; spread includes hats/consonants caught by the ±35 ms window) | median {med:+.1f} ms, MAD {mad:.1f} ms |\n"
       f"| recommended judgment | per-tap good window = half the local gap, capped at ±100 ms (floor ±45 ms, schema v2.5); {'inside 16th bursts' if bursts else 'densest runs'} that is ±{gd} ms; perfect ±{pf} ms everywhere; a tap more than ±{ms} ms away from an isolated beat is a miss |\n",
       f"| difficulty tier | **{TIER[slug]}** |\n",
       "\n## Density vs original Dancing Line (dlfm-wiki CPM)\n",
       f"| level | avg CPM | peak CPM |\n|---|---|---|\n| **{TITLE[slug]} (this chart)** | **{avg:.0f}** (taps / duration × 60) | **{peak1}** (most taps in any 1 s × 60; validator metric); {peakg:.0f} as 60 / min gap |\n",
       *[f"| {n} | {a} | {p_} |\n" for n,a,p_ in ORIG],
       "\nNote: the wiki's 'avg CPM' is not plain taps/duration (The Racing: 357 taps / 144 s = 149 by our formula vs 220 on the wiki), so compare our avg against ~149 for The Racing; peak CPM uses the same 1-second-window idea as the validator.\n",
       f"\n16th bursts: {len(bursts)} added taps at " + (', '.join(f"{x['t']:.2f} s ({x['pos']}, {x['tag']})" for x in bursts) if bursts else 'none (Get Up is the easy tier: no drums, no 16ths)') + ". Each burst tap sits on a real 16th event (snare/hat roll, flam or rapid vocal syllable, strength ≥ 0.5 within ±25 ms) at a fill, build-up, drop or final chorus.\n",
       "\n## Per-section density\n","| section | t | old | new | new/s |\n|---|---|---|---|---|\n"]
    for k,s in enumerate(secs):
        e=secs[k+1]['t'] if k+1<len(secs) else dur
        n_old=sum(1 for t in old if s['t']<=t<e); n=int(((T>=s['t'])&(T<e)).sum())
        L.append(f"| {s['label']} | {s['t']:.2f}-{e:.2f} | {n_old} | {n} | {n/max(e-s['t'],1e-6):.2f} |\n")
    L.append("\n## Spot checks (start, section changes, middle, end)\nOffset = measured attack minus tap time (negative = attack slightly before the tap).\n\n| t | bar:16th | tag | section | offset ms |\n|---|---|---|---|---|\n")
    idx={0,len(T)//2,len(T)-1}
    for s in secs:
        ii=[i for i,x in enumerate(T) if x>=s['t']][:2]; idx|=set(ii)
    for i in sorted(idx):
        L.append(f"| {T[i]:.3f} | {taps[i]['pos']} | {taps[i]['tag']} | {taps[i]['sec']} | {om[i]:+.1f} |\n")
    L.append("\n## Rationale\n"+PROSE[slug]+"\n")
    open(f'{OUT}/{slug}/chart-report.md','w').write(''.join(L))
    with open(f'{OUT}/{slug}/chart-sync.csv','w') as f:
        f.write('t,bar16,tag,section,attack_offset_ms,clear_attack\n')
        for i,x in enumerate(taps): f.write(f"{x['t']:.3f},{x['pos']},{x['tag']},\"{x['sec']}\",{om[i]:.1f},{int(clear[i])}\n")
    bar=16*G['per16']; t0=G['phase']+C['db']*G['per16']
    an=dict(slug=slug,method='librosa 1.0 HPSS + band-limited spectral flux (kick 30-150 Hz, snare 1.5-6 kHz, hat 7-11 kHz on the percussive layer; bass 40-250 Hz, vocal 300-3000 Hz on the harmonic layer); constant-tempo 16th grid fitted by phase resultant and calibrated to time-domain attacks; no demucs stems used.',
            grid=G,downbeats=[round(t0+n*bar,3) for n in range(int((dur-t0)/bar)+1)],
            novelty_bounds=al['novelty_bounds'],sections=[dict(t=s['t'],label=s['label'],kind=s['kind']) for s in secs],
            candidates={L_:[x for x in al[L_] if x.get('s',0)>=0.5] for L_ in ['onsets','kick','snare','hat','bass','vocal']},beats=al['beats'])
    json.dump(an,open(f'{OUT}/{slug}/analysis.json','w'))
    open(f'{OUT}/{slug}/analysis.md','w').write(f"""# {TITLE[slug]}: audio analysis notes\n
- File: `public/audio/{slug}.mp3`, {dur:.2f} s, used whole (never trimmed). Times are seconds from the first decoded sample.
- Grid: {G['bpm']:.3f} BPM, 16th = {G['per16']:.6f} s, phase {G['phase']:.4f} s (bar 0 downbeat = {t0:.4f} s, bar = {bar:.5f} s). Fit quality (phase resultant) {G['resultant']}; drift per 20 s window: {', '.join(f"{d[1]:+.1f}" for d in G['drift_ms_per20s'])} ms.
- Calibration: librosa onset frames were {G['attack_cal_ms']} ms off the time-domain attacks (max slope of a 2 ms RMS envelope), so the grid is anchored to attacks; band layers were shifted by {', '.join(f"{k} {v[0]:+.1f} ms" for k,v in G['layer_shift_ms'].items())}.
- No demucs stems were used (so the 25 ms htdemucs latency does not apply).
- Groove: {GROOVE[slug]}
- Sections: from beat-synchronous chroma/MFCC/RMS novelty, snapped to bar lines and checked against the arrangement (see analysis.json `sections`).
- Verification: every tap is on the grid and was kept only when a real event lies within ±35 ms; measured attack offset median {med:+.1f} ms (MAD {mad:.1f} ms), see chart-report.md and chart-sync.csv.
""")
    print(slug,len(T),'old',len(old),'run',best+1,'offset',round(med,1),round(mad,1))
if __name__=='__main__':
    for s in sys.argv[1:]: main(s)
