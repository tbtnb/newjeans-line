import json,sys,importlib,numpy as np
from pathlib import Path
sys.path.insert(0,'/workspace/w2-work')
slug=sys.argv[1]; spec=importlib.import_module(f'spec_{slug.replace("-","_")}')
D=Path('/workspace/newjeans-line-designs')/spec.FOLDER
a=json.load(open(f'/workspace/w2-work/{slug}.json'))
ch=json.load(open(D/'chart.json')); L=json.load(open(D/'layout.json'))
taps=[t['t'] for t in ch['taps']]; tags=[t['tag'] for t in ch['taps']]; src=ch['meta']['snap_sources']
dur=a['duration']; secs=ch['sections']
def nearest(t,keys,thr=0.12,win=0.08):
    best=None
    for k in keys:
        for x,s in a.get(k,[]):
            if s<thr: continue
            d=x-t
            if abs(d)<=win and (best is None or abs(d)<abs(best[0])): best=(d,k,s)
    return best
ALL=['kick','snare','vocals','bass','other','onsets_full']
gaps=np.diff(taps)
# runs: consecutive gaps <= 1.15*min 8th
eighth=a['beat_period']/2
def runs(th):
    out=[];cur=[0]
    for i,g in enumerate(gaps):
        if g<=th: cur.append(i+1)
        else:
            if len(cur)>1: out.append(cur)
            cur=[i+1]
    if len(cur)>1: out.append(cur)
    return out
r8=runs(eighth*1.15); best=max(r8,key=len) if r8 else []
lines=[f'# {ch["id"]} — chart report (worker w2)\n',
f'- Audio: `public/audio/{slug}.mp3`, full length {dur:.3f} s, untouched. Grid: {a["bpm"]} BPM, beat0 {ch["meta"]["beat0"]} s (fit to demucs drum stem).',
f'- **Old (v1) taps: {spec.OLD} → new: {len(taps)}  (×{len(taps)/spec.OLD:.2f})**. Average {len(taps)/dur:.2f} taps/s ({len(taps)/dur*60:.0f} CPM).',
f'- Min gap {gaps.min()*1000:.0f} ms (design floor = one 8th note = {eighth*1000:.0f} ms; snapped taps never closer than road-geometry floor). Median gap {np.median(gaps)*1000:.0f} ms.',
f'- **Fastest run: {len(best)} consecutive taps at 8th-note spacing ({eighth*1000:.0f} ms ≈ {1/eighth:.1f} taps/s) from {taps[best[0]]:.3f} s to {taps[best[-1]]:.3f} s.**' if best else '',
f'- 8th-note runs ≥6 taps: {sum(1 for r in r8 if len(r)>=6)}; ≥8 taps: {sum(1 for r in r8 if len(r)>=8)}. Longest 5: '+', '.join(f'{len(r)}@{taps[r[0]]:.1f}s' for r in sorted(r8,key=len,reverse=True)[:5]),
f'- Recommended judgment window: perfect ±{spec.JUDGE["perfect"]} ms, accept ±{spec.JUDGE["good"]} ms. {spec.JUDGE["note"]}',
f'- Snapping: {sum(1 for s in src if s!="grid")}/{len(src)} taps sit on a detected onset of their tagged stem (±45 ms search, attack refined on 2 ms RMS); the rest sit on the fitted grid (where the onset was ambiguous or snapping would have broken the geometry floor).',
'\n## Per-section density\n','| t (s) | section | kind | taps | taps/s | densest 2 s |','|---|---|---|---:|---:|---:|']
for i,s in enumerate(secs):
    e=secs[i+1]['t'] if i+1<len(secs) else dur
    ts=[t for t in taps if s['t']<=t<e]
    dens=max([sum(1 for u in ts if x<=u<x+2) for x in ts] or [0])
    lines.append(f'| {s["t"]:.2f} | {s["label"]} | {s["kind"]} | {len(ts)} | {len(ts)/max(e-s["t"],1e-6):.2f} | {dens/2:.1f}/s |')
lines.append('\n## Tag mix\n'); 
from collections import Counter
lines.append(', '.join(f'{k}: {v}' for k,v in Counter(tags).most_common()))
lines.append('\n## Section rationale (which audio events the taps follow)\n')
for lab,txt in spec.WHY.items(): lines.append(f'- **{lab}** — {txt}')
# spot checks
lines.append('\n## Alignment spot checks (offset = nearest detected onset − tap; independent of snapping source)\n')
lines.append('| where | tap t (s) | tag | nearest stem onset | stem offset ms | nearest full-mix onset offset ms |'); lines.append('|---|---:|---|---|---:|---:|')
picks=[]
picks+= [('start',i) for i in range(4)]
for s in secs[1:]:
    k=next((i for i,t in enumerate(taps) if t>=s['t']-0.01),None)
    if k is not None: picks.append((f'change → {s["label"].split(" · ")[0]}',k)); 
mid=len(taps)//2; picks+=[('middle',mid+j) for j in range(-2,3)]
picks+=[('end',len(taps)-4+j) for j in range(4)]
offs=[]
for w,i in picks:
    nb=nearest(taps[i],ALL[:-1]); nf=nearest(taps[i],['onsets_full'],0.05)
    lines.append(f'| {w} | {taps[i]:.3f} | {tags[i]} | ' + (f'{nb[1]} (str {nb[2]:.2f}) | {nb[0]*1000:+.0f}' if nb else 'none within 80 ms | —') +' | '+(f'{nf[0]*1000:+.0f}' if nf else '—')+' |')
allo=[nearest(t,['onsets_full'],0.05) for t in taps]; ao=np.array([abs(x[0])*1000 for x in allo if x]); 
lines.append(f'\nWhole chart vs FULL-MIX onset detector (not used for snapping): {len(ao)}/{len(taps)} taps have a full-mix onset within 80 ms; |offset| median {np.median(ao):.1f} ms, p90 {np.percentile(ao,90):.1f} ms.')
for nm,(lo,hi) in {'first 25%':(0,dur*.25),'25-50%':(dur*.25,dur*.5),'50-75%':(dur*.5,dur*.75),'last 25%':(dur*.75,dur)}.items():
    xs=[abs(x[0])*1000 for t,x in zip(taps,allo) if x and lo<=t<hi]
    lines.append(f'- {nm}: n={len(xs)}, median {np.median(xs):.1f} ms, p90 {np.percentile(xs,90):.1f} ms')
lines.append('\nCaveat: these offsets are measured against the same librosa/demucs onset detector family used for candidates (self-consistency, not an independent listening test). Grid-placed taps on soft vocal entries can show 20–60 ms offsets to the nearest transient; that is a detector limit, not a deliberate shift. No human listening or real-device test has been done by this worker.')
(D/'chart-report.md').write_text('\n'.join(lines))
# analysis.json (compact)
an={k:a[k] for k in ['id','duration','bpm','beat_period','beat0','beats','grid_note'] if k in a}
for k in ['kick','snare','hat','vocals','bass','other','onsets_full']:
    if k in a: an[k]=[x for x in a[k] if x[1]>=0.12]
an['beat_rms']=a.get('beat_rms'); an['sections']=secs
an['method']=('librosa 0.11 + demucs htdemucs 4-stem separation (drums/bass/vocals/other). kick = 30-130 Hz flux of drum stem, snare/clap = 1.2-6 kHz flux of drum stem, '
 'hat = 7-11 kHz; vocal/bass/other = onset_strength of each stem; peak-picked, attack refined to steepest 2 ms RMS rise. Beat grid: brute-force BPM/phase fit maximizing drum-stem onset strength on an 8th grid. '
 'Sections: bar-level 16-step onset maps per stem (see analysis-notes.md) + RMS + recurrence novelty, labelled by structure.')
(D/'analysis.json').write_text(json.dumps(an))
print('report ok', D)
