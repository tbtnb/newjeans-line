import json,sys,numpy as np,importlib.util
slug=sys.argv[1]; OUT=f'/workspace/newjeans-line-designs/{slug}'
OLD={'how-sweet':133,'bubble-gum':132,'supernatural':162,'right-now':216}[slug]
legacy=[l for l in json.load(open('/tmp/levels_main.json')) if l['id']==slug][0]
raw=json.load(open(f'{slug}.chart.raw.json')); ch=json.load(open(f'{OUT}/chart.json')); off=json.load(open(f'{slug}.offsets.json'))
an=json.load(open(f'{slug}.analysis.raw.json')); g=json.load(open(f'{slug}.grid.json')); son=json.load(open(f'{slug}.stem_onsets.json'))
z=np.load(f'{slug}.stems.npz'); fps=22050/256
sp=importlib.util.spec_from_file_location('s',f'specs/{slug.replace("-","_")}.py'); S=importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
dur=an['duration']; taps=[t['t'] for t in ch['taps']]; secs=ch['sections']
P=g['period']; bar0=g['bar0']
# ---- analysis.json
lv={}
for k in ['vocal_rms','drums_rms','other_rms','bass_rms']:
    x=z[k]/np.percentile(z[k],99); lv[k.replace('_rms','')]=[round(float(x[int(max(0,bar0+i*4*P)*fps):int((bar0+(i+1)*4*P)*fps)].mean()),3) for i in range(int((dur-bar0)/(4*P)))]
analysis={'slug':slug,'duration':dur,'tempo_bpm':round(60/P,3),'beat_period':round(P,5),
 'grid':{'t0_first_beat':round(g['t0'],4),'bar0':round(bar0,4),'downbeat_phase':g['phase'],'transient_correction_s':g['transient_corr'],
         'note':'constant-tempo grid = robust linear fit of a DP beat tracker on the full-mix onset envelope, then shifted to the measured max-slope of clap/hat transients in the mix (librosa onset envelopes are ~25 ms late)'},
 'beats':[round(g['t0']+i*P,3) for i in range(int((dur-g['t0'])/P)+1)],
 'sections':[{'t':s['t'],'label':s['label'],'kind':s['kind'],'bars':[sec['bars'][0],sec['bars'][1]]} for s,sec in zip(secs,S.SECTIONS)],
 'section_candidates':{'novelty_checkerboard':an['novelty_bounds'],'agglomerative':an['agglomerative_bounds']},
 'per_bar_levels_0to1':lv,
 'onset_candidates_mix':{k:[[round(a+g['transient_corr'],3),b] for a,b in v] for k,v in an['onsets'].items()},
 'onset_candidates_stems':{k:[[round(a-0.050,3),b] for a,b in v] for k,v in son.items()},
 'rms_1s':an['rms_1s'],
 'method':an['method']+' | demucs htdemucs stems (drums/bass/vocals/other) -> band onset envelopes; stem onset times corrected by -50 ms (25 ms demucs output delay + ~25 ms onset-envelope lag). Candidates only; the chart is curated in chart.json.'}
json.dump(analysis,open(f'{OUT}/analysis.json','w'))
# ---- stats
gaps=np.diff(taps)
def runs(th):
    best=(1,0);cur=1;st=0
    for i,gp in enumerate(gaps):
        if gp<=th: cur+=1
        else: cur=1; st=i+1
        if cur>best[0]: best=(cur,st)
    return best
fr=runs(0.30); fr2=runs(min(gaps)+0.005)
ofs={o['t']:o for o in off}
lines=[]
lines.append(f"# {ch.get('id')} — chart report (worker 4)\n")
lines.append(f"Audio: `public/audio/{slug}.mp3`, full length {dur:.2f} s, used as-is. Tempo {60/P:.2f} BPM (constant), grid bar0 = {bar0:.3f} s, bar = {4*P:.4f} s.\n")
lines.append("## Counts\n")
lines.append(f"| | legacy v1 | new |\n|---|---|---|\n| taps | {OLD} | **{len(taps)}** ({len(taps)/OLD:.2f}x) |\n| avg taps/s | {OLD/dur:.2f} | {len(taps)/dur:.2f} |\n| min gap | {min(np.diff(legacy['turns'])):.3f} s | {min(gaps):.3f} s |\n| fastest run (gaps <= 0.30 s) | - | {fr[0]} taps from {taps[fr[1]]:.2f} s |\n| longest run at the minimum gap ({min(gaps):.3f} s) | - | {fr2[0]} taps from {taps[fr2[1]]:.2f} s |\n")
lines.append(f"\nRecommended judgment window: **perfect ±{int(ch['judgment']['perfect']*1000)} ms, good ±{int(ch['judgment']['good']*1000)} ms, miss beyond ±{int(ch['judgment']['miss_beyond']*1000)} ms** ({ch['judgment']['note']}).\n")
lines.append("Humanly playable floor used: no two taps closer than %.3f s (%s).\n"%(min(gaps),'one 8th note'))
lines.append("\n## Per-section density\n\n| section | kind | start | end | taps | taps/s | max run (<=0.30 s) |\n|---|---|---|---|---|---|---|\n")
for i,s in enumerate(secs):
    e=secs[i+1]['t'] if i+1<len(secs) else dur
    ts=[t for t in taps if s['t']<=t<e]; gg=np.diff(ts) if len(ts)>1 else []
    mr=1;c=1
    for x in gg:
        c=c+1 if x<=0.30 else 1; mr=max(mr,c)
    lines.append(f"| {s['label']} | {s['kind']} | {s['t']:.2f} | {e:.2f} | {len(ts)} | {len(ts)/(e-s['t']):.2f} | {mr} |\n")
o=np.array([x['offset_ms'] for x in off if x['offset_ms'] is not None])
lines.append(f"\n## Sync measurement\n\nFor every tap the nearest transient in the **full mix** (band chosen by the tap's tag: 40–180 Hz for kick/bass, 300–3000 Hz for vocal/melody, 1.5–10 kHz for clap/hat; max-slope of the band envelope within ±60 ms) was measured. Salient transients found for {len(o)}/{len(off)} taps (the rest sit on soft vocal/synth onsets with no sharp attack). Offset = transient − tap: median {np.median(o):+.1f} ms, median |offset| {np.median(np.abs(o)):.1f} ms, 90th percentile |offset| {np.percentile(np.abs(o),90):.1f} ms.\n")
lines.append("\n| section | measured | median offset ms | median abs ms |\n|---|---|---|---|\n")
for i,s in enumerate(secs):
    e=secs[i+1]['t'] if i+1<len(secs) else dur
    oo=np.array([x['offset_ms'] for x in off if s['t']<=x['t']<e and x['offset_ms'] is not None])
    lines.append(f"| {s['label']} | {len(oo)} | {np.median(oo):+.1f} | {np.median(np.abs(oo)):.1f} |\n" if len(oo) else f"| {s['label']} | 0 | – | – |\n")
import bisect
allon=sorted([(a-0.05,b,k) for k,v in son.items() if k!='hat' for a,b in v if b>0.35]); tso=[a for a,_,_ in allon]; hit=[];
for t in taps:
    i=bisect.bisect_left(tso,t); c=[allon[j] for j in (i-1,i) if 0<=j<len(allon)]; d=min(c,key=lambda x:abs(x[0]-t))
    if abs(d[0]-t)<=0.06: hit.append((d[0]-t)*1000)
lines.append(f"\nCross-check on separated stems (demucs; times corrected −50 ms): {len(hit)}/{len(taps)} taps have a stem onset (drums/bass/vocals/other, strength > 0.35) within ±60 ms; median offset {np.median(hit):+.1f} ms, 90th pct |offset| {np.percentile(np.abs(hit),90):.1f} ms. Section-boundary taps are listed below.\n")
def ex(t):
    r=[x for x in raw['taps'] if x['t']==t][0]; f=ofs[t]
    return f"| {t:.3f} | {r['sec']} | bar {r['bar']} slot {r['slot8']}/{getattr(S,'SUB',16)} | {r['tag']} | {f['band']} | {'%+.1f'%f['offset_ms'] if f['offset_ms'] is not None else 'n/a (soft onset)'} |\n"
lines.append("\n## Spot checks (start / section changes / middle / end)\n\n| tap t (s) | section | grid position | tagged event | band | measured offset ms |\n|---|---|---|---|---|---|\n")
pick=taps[:4]
for s in secs[1:]:
    pick+= [t for t in taps if t>=s['t']][:2]
mid=dur/2; pick+= sorted(taps,key=lambda t:abs(t-mid))[:3]; pick+=taps[-4:]
for t in sorted(set(pick)): lines.append(ex(t))
open(f'{OUT}/chart-report.body.md','w').write(''.join(lines))
print(slug,len(taps),f'{len(taps)/OLD:.2f}x','fastest',fr,'min',min(gaps),'run@min',fr2)
