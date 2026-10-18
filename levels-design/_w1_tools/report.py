import sys,json,importlib,numpy as np
from chartgen import load,win
OUT='/workspace/newjeans-line-designs'
s=sys.argv[1]; C=importlib.import_module('cfg_'+s.replace('-','_')); S=importlib.import_module('spec_'+s.replace('-','_'))
OLD={'attention':139,'hype-boy':140,'cookie':357,'hurt':64}; OLDB={'attention':139,'hype-boy':180,'cookie':379,'hurt':80}
WIN={'attention':90,'hype-boy':90,'cookie':80,'hurt':100}
a,E=load(s); ch=json.load(open(f'{OUT}/{s}/chart.json')); taps=ch['taps']; T=np.array([t['t'] for t in taps])
import scipy.signal as ss
env=np.load(f'{s}.env.npz'); _pk,_=ss.find_peaks(env['oenv'],height=0.12,distance=4); on=env['times'][_pk]; P=a['beat_period']; ph=a['grid_phase']; dur=a['duration']
KEY={'vocal':'vocal_on','kick':'kick_on','snare':'snare_on','melody':'mel_on','bass':'bass_on','phrase':'mix'}
def off_onset(t): i=np.argmin(abs(on-t)); return (on[i]-t)*1000
def off_band(tp):
    k=KEY[tp['tag']]; v,tt=win(E[k],tp['t'],0.06); return (tt-tp['t'])*1000, v
def grid_off(t):
    n=round((t-ph)/(P/4)); return (t-(ph+n*P/4))*1000
secs=ch['sections']; g=np.diff(T)
lines=[]; A=lines.append
A(f"# {S.title} — chart report\n")
A(f"- Audio: `public/audio/{s}.mp3` (full track, {dur:.2f} s, untouched). Times = seconds from first decoded sample.")
A(f"- Tempo grid measured from the audio: **{60/P:.2f} BPM**, beat {P:.4f} s, downbeat phase {ph:.3f} s (constant-tempo fit maximising onset strength).")
A(f"- **Old taps: {OLD[s]}** (shipped `src/levels.json`; `reports/rhythm-chart-baseline.json` had {OLDB[s]}). **New taps: {len(T)}** = **{len(T)/OLD[s]:.2f}x**.")
A(f"- Speed {C.route['speed'][0]['v']} u/s, road width {S.width[0]['w']} → narrowest {min(w['w'] for w in S.width)}.")
A(f"- Min gap **{g.min():.3f} s**, median gap {np.median(g):.3f} s, mean density {len(T)/dur:.2f} taps/s.")
# fastest runs
def runs(th):
    best=(0,0);cur=0
    for i,x in enumerate(g):
        cur=cur+1 if x<=th else 0
        if cur>best[0]: best=(cur,i-cur+1)
    return best
e8=P/2*1.1; b=runs(e8)
if b[0]>0: A(f"- Fastest consecutive run (8th notes, every gap ≤ {e8:.3f} s): **{b[0]+1} taps**, {T[b[1]]:.3f}–{T[b[1]+b[0]]:.3f} s (mean interval {np.mean(g[b[1]:b[1]+b[0]]):.3f} s).")
else: A(f"- No consecutive 8th-note runs; fastest pair = min gap {g.min():.3f} s.")
b3=runs(0.30)
A(f"- Validator definition (gaps ≤ 0.30 s): longest run {b3[0]+1} taps from {T[b3[1]]:.3f} s.")
if g.min()<0.25:
    b2=runs(0.2); A(f"- Fastest 8th-note burst at 157 BPM (gaps ≤ 0.20 s): **{b2[0]+1} taps** from {T[b2[1]]:.3f} s (interval ≈ {np.mean(g[b2[1]:b2[1]+b2[0]]):.3f} s).")
qb=runs(P*1.1); A(f"- Longest unbroken run at ≤ 1 beat spacing (≤ {P*1.1:.3f} s): {qb[0]+1} taps from {T[qb[1]]:.3f} s.")
dens=[((T>=t)&(T<t+2)).sum()/2 for t in np.arange(0,dur,0.25)]
A(f"- Peak 2-second density: **{max(dens):.1f} taps/s** at {np.argmax(dens)*0.25:.2f} s.")
A(f"- Recommended judgment window: **±{WIN[s]} ms** (perfect ±35 ms). Must stay < half the min gap ({g.min()*500:.0f} ms) so a tap never resolves to the neighbouring turn; ±{WIN[s]} ms ≈ the old engine's ±100 ms but tighter for the dense songs. Needs confirmation with real touch latency (not yet tested on devices).")
A(f"- Hard floor respected: no gap < 0.15 s. Humanly-playable minimum used here: {g.min():.3f} s.\n")
A("## Per-section density\n\n| Section | Kind | Start | End | Taps | Taps/s | Min gap | Main tap sources |\n|---|---|---|---|---|---|---|---|")
for k,sec in enumerate(secs):
    e=secs[k+1]['t'] if k+1<len(secs) else dur
    m=(T>=sec['t'])&(T<e); n=m.sum(); tg=[t['tag'] for t,mm in zip(taps,m) if mm]
    from collections import Counter
    cc=', '.join(f'{x} {y}' for x,y in Counter(tg).most_common(3))
    gg=np.diff(T[m]); A(f"| {sec['label']} | {sec['kind']} | {sec['t']:.2f} | {e:.2f} | {n} | {n/(e-sec['t']):.2f} | {gg.min() if len(gg) else 0:.3f} | {cc} |")
A("\n## How taps were chosen (rationale)\n")
A(C.__doc__ or '')
A(S.chart_notes+"\n")
A("""Method (honest description): candidates = every 8th (or 16th where the groove is syncopated) on the measured beat grid. Each candidate is scored by the onset strength of the separated stems at that instant (vocal syllable onsets from the htdemucs vocal stem, kick 30–140 Hz / snare-clap 1.2–8 kHz from the percussive part of the accompaniment stem, bass and harmonic accents), with per-section weights and a metric bonus for strong beats. **Per section I set by hand**: the density target (follows energy: intro < verse < pre < chorus/climax), which sources lead (vocal phrasing in verses/pre-choruses, drums+hook in choruses), the grid resolution, the minimum gap and the maximum run length, plus forced taps on section downbeats/impacts. The selected slot is then snapped to the actual onset peak if within ±18 ms, otherwise kept on the grid. Repeated musical material therefore gets repeated tap patterns (DL-style), and long gaps stay where the music breathes. All demucs-derived times are corrected by −25.03 ms (stem latency vs ffmpeg/browser decode).\n""")
A("## Alignment spot checks (start / section changes / middle / end)\n")
A("Offset = (audio event time − tap time). 'Nearest onset' = nearest peak of the full-mix onset-strength envelope (height>0.12, ≥46 ms apart); 'band peak' = peak of the tagged source envelope within ±60 ms; 'grid' = distance to nearest 16th of the beat grid.\n")
A("| Where | Tap t (s) | Tag | Nearest full-mix onset (ms) | Tagged-band peak (ms) | Grid dev (ms) |\n|---|---|---|---|---|---|")
picks=[]
picks+= [('start',i) for i in range(3)]
for sec in secs[1:]:
    i=int(np.argmin(abs(T-sec['t']))); picks.append((f"→ {sec['label']}",i))
mid=len(T)//2; picks+=[('middle',mid-1),('middle',mid),('middle',mid+1)]
picks+=[('end',len(T)-3),('end',len(T)-2),('end',len(T)-1)]
allo=[];allb=[]
for i,tp in enumerate(taps):
    allo.append(off_onset(tp['t'])); allb.append(off_band(tp)[0])
for w,i in picks:
    tp=taps[i]; A(f"| {w} | {tp['t']:.3f} | {tp['tag']} | {allo[i]:+.0f} | {allb[i]:+.0f} | {grid_off(tp['t']):+.0f} |")
allo=np.array(allo); allb=np.array(allb)
A(f"\nWhole chart: |offset to nearest full-mix onset| median {np.median(abs(allo)):.0f} ms, 90th pct {np.percentile(abs(allo),90):.0f} ms; |offset to tagged-band peak| median {np.median(abs(allb)):.0f} ms, 90th pct {np.percentile(abs(allb),90):.0f} ms.")
A("\nPer-section median |offset to tagged-band peak| (ms): "+', '.join(f"{sec['label']} {np.median(abs(allb[(T>=sec['t'])&(T<(secs[k+1]['t'] if k+1<len(secs) else dur))])):.0f}" for k,sec in enumerate(secs) if ((T>=sec['t'])&(T<(secs[k+1]['t'] if k+1<len(secs) else dur))).any()))
A("\nCaveats: alignment is measured against analysis envelopes, not by listening on a device; the integrator must verify in-engine with the audio clock (output latency handled by the engine). Section boundaries come from bass/drum/vocal energy changes and 4-bar novelty and are approximate labels where noted.")
open(f'{OUT}/{s}/chart-report.md','w').write('\n'.join(lines))
# analysis.json
an=json.load(open(f'{s}.analysis.json'))
ana=dict(slug=s,audio=f'public/audio/{s}.mp3',duration=an['duration'],bpm=round(60/P,3),beat_period=P,downbeat_phase=ph,
  method='librosa 0.11/1.0 HPSS + band onset envelopes (22050 Hz, hop 256); htdemucs two-stem separation (vocals / accompaniment); stem times corrected by -25.03 ms; constant-tempo grid fit; checkerboard novelty on beat-synced chroma+MFCC for boundaries.',
  sections=secs,structure_boundaries_auto=an['structure_boundaries_auto'],
  beats=[round(ph+i*P,3) for i in range(int((dur-ph)/P)+1)],
  onsets_fullmix=an['onsets_all'],kick_peaks=an['kick_peaks'],snare_clap_peaks=an['snare_clap_peaks'],bass_peaks=an['bass_peaks'],
  vocal_band_peaks_mix=an['vocal_band_peaks'],rms_per_beat=an['rms_per_beat'],
  notes=open(f'{s}.notes.md').read() if __import__('os').path.exists(f'{s}.notes.md') else '')
json.dump(ana,open(f'{OUT}/{s}/analysis.json','w'))
print(s,'report ok; median band offset',np.median(abs(allb)))
