import json,sys
D='/workspace/newjeans-line-designs/'
STRUCT={
'omg':'Intro a-cappella vocal (bars 0-7) → snap/clap verse (8-15) → UK-garage kick verse (16-23) → halftime chorus with synth-hook answers (24-31) → garage verse 2 (32-47) → drumless bass/vocal pre (48-55) → chorus 2 (56-63) → post groove (64-70) → trap-kick bridge (71-78) → 1-bar break (79) → four-on-the-floor dance break (80-87) → final chorus ×2 (88-103) → synth-only outro (104-111).',
'ditto':'Choir intro (0-7) → Baltimore hat/snare verse (8-15) → jersey-club kick chorus K...|K...|K..K|..K. (16-23) → dense snare post (24-30) → drums out, vocal break (31-35) → claps on 2/4 (36-39) → full Baltimore beat for 24 bars (40-63) → drumless vocal bridge (64-71) → claps 2/4 (72-78) → full beat final (79-99) → fade/outro (100-103).',
'new-jeans':'Synth intro (0-3) → drums without bass (4-7) → 2-step verse with bass (8-19) → jersey-kick chorus (20-27) → off-beat clap break (28-31) → kick on 2/4 rebuild (32-35) → verse 2 (36-47) → chorus 2 (48-55) → synth outro (56-59).',
'super-shy':'Instrumental intro with beat (0-7) → broken-beat verse, kick 4/7/10/14 (8-23) → jersey-kick chorus (24-39) → drumless break (40-43) → build, kick on 2/4 (44-47) → verse 2 (48-63) → 2-bar break (64-65) → verse 3 (66-71) → final chorus 24 bars, bass enters at bar 80 (72-95).',
}
s=sys.argv[1]; a=json.load(open(f'{s}.json')); ch=json.load(open(D+s+'/chart.json'))
L=[f'# {s} — audio analysis notes (worker w2)\n',
f'- File: `public/audio/{s}.mp3` (full, untouched), decoded length {a["duration"]:.3f} s (gapless-trimmed decode, same as ffmpeg/librosa/browsers).',
f'- Tempo: **{a["bpm"]} BPM**, beat period {a["beat_period"]*1000:.2f} ms, first beat {a["beat0"]:.4f} s. Grid fitted by brute-force BPM/phase search maximizing demucs drum-stem onset strength on an 8th grid; per-20 s phase residual ≤ ±4 ms (no tempo drift).',
'- Stems: demucs htdemucs (drums/bass/vocals/other). **Pitfall found:** demucs wrote stems 1104 samples (25.03 ms @44.1 kHz) late relative to the gapless-trimmed mp3 decode; all stem onsets and the stem-fitted grid were shifted −25.03 ms (verified by cross-correlating the stem sum against the decoded mix: lag 552 samples @22.05 kHz for both OMG and Ditto).',
'- Onsets: kick = 30–130 Hz spectral flux of the drum stem, snare/clap = 1.2–6 kHz, hat = 7–11 kHz; vocal/bass/other = librosa onset_strength per stem; peak-picked and attack-refined to the steepest 2 ms RMS rise (±25 ms). All candidates (strength ≥ 0.12) are in `analysis.json`.',
f'- Structure (bar = 4 beats = {a["beat_period"]*4:.3f} s): {STRUCT[s]}',
'\n## Sections used by the chart\n','| start (s) | label | kind |','|---:|---|---|']
for x in ch['sections']: L.append(f'| {x["t"]:.3f} | {x["label"]} | {x["kind"]} |')
L.append('\n## Per-bar 16-step onset map (what the chart was hand-picked from)\n')
L.append('Columns per bar: K kick, S snare/clap, B bass, V vocal, O other/synth. Upper-case = strong (≥0.5), lower-case = weaker onset, "|" = beat. Times are bar starts (s).\n')
L.append('```'); L.append(open(f'rmap_{s}.txt').read().rstrip()); L.append('```')
open(D+s+'/analysis-notes.md','w').write('\n'.join(L)); print('ok',s)
