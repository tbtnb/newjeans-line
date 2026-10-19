"""Recheck the original decoded audio, then micro-align existing beat slots only.
Requires numpy/scipy/librosa/ffmpeg. Run from repository root; report only, never rewrites the chart.
The frozen baseline allows the evidence to be reproduced after applying the reviewed corrections.
"""
import json,numpy as np,sys,subprocess,hashlib
from pathlib import Path
sys.path.insert(0,'tools/research');import onsets as O
from scipy.signal import correlate,correlation_lags
root=Path('.')
C=dict(np.load('analysis/research/omg-onsets.npz'))
lag=float(np.mean(list(O.calibrate().values())));print('lag',lag,flush=True)
y=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i','public/audio/omg.mp3','-f','f32le','-ac','1','-ar','44100','pipe:1']),dtype='<f4')
fresh=O.norm(O.flux(y));pt,ps=O.peaks(fresh,lag,thr=.25,wait_s=.05)
# Independent verification that saved stem evidence belongs to this decoded mix, with no time shift.
a=fresh[:min(len(fresh),len(C['env_full']))];b=C['env_full'][:len(a)];cc=correlate(a,b,mode='full',method='fft');ls=correlation_lags(len(a),len(b));m=abs(ls)<50;shift=int(ls[m][np.argmax(cc[m])]);print('cached_full_lag_samples',shift*O.HOP, 'corr',np.corrcoef(a,b)[0,1],flush=True)
PK={k:O.peaks(C['env_'+k],lag) for k in ['kick','snare','vocals','bass','other']}
ch=json.load(open('analysis/user/omg-timing-20261019-baseline.json'));old=[x['t']for x in ch['taps']];ref=json.load(open('analysis/user/omg-user-refine.json'))['taps'][1:]
rows=[];changes=[]
for i,t in enumerate(old):
 row={'index':i,'raw':ref[i]['t_raw'],'before':t,'after':t,'prior_layer':ref[i]['layer'],'decision':'keep intended grid slot'}
 # Preserve the regular 47% phrase; don't reintroduce the old delayed sixteenth.
 if not 75.1<=t<=77.1:
  candidates=[]
  for layer in ['kick','snare']:
   ts,ss=PK[layer]
   for j in np.where((abs(ts-t)<=.025)&(ss>=.65))[0]:
    k=int(np.argmin(abs(pt-ts[j])))
    if abs(pt[k]-ts[j])>.009 or ps[k]<.35:continue
    # Require the corrected sound to remain on the user's original beat/subbeat.
    score=min(float(ss[j]),1)+min(float(ps[k]),1)-abs(float(ts[j])-t)*10
    candidates.append((score,float(ts[j]),layer,float(ss[j]),float(pt[k]),float(ps[k])))
  if candidates:
   best=max(candidates);nt=round(best[1],3)
   if .008<=abs(nt-t)<=.025 and (i==0 or nt-old[i-1]>=.19) and (i==len(old)-1 or old[i+1]-nt>=.19):
    row.update(after=nt,decision='strong drum attack confirmed by freshly decoded full mix',layer=best[2],stem_strength=round(best[3],3),mix_onset=round(best[4],4),mix_strength=round(best[5],3),delta_ms=round((nt-t)*1000))
    changes.append(row)
 rows.append(row)
report={'audio_sha256':hashlib.sha256(Path('public/audio/omg.mp3').read_bytes()).hexdigest(),'fresh_audio_samples':len(y),'saved_full_mix_correlation':float(np.corrcoef(a,b)[0,1]),'saved_full_lag_samples':shift*O.HOP,'detector_calibration_ms':lag*1000,'rule':'Preserve all 361 intended beat/subbeat slots and directions. Only move 8–25ms to a strong kick/snare attack confirmed within 9ms by fresh full-mix analysis; retain 47% regular phrase and ambiguous vocal runs. No added or removed taps.','changed':len(changes),'changes':changes,'taps':rows}
Path('analysis/user/omg-timing-20261019.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['taps']},ensure_ascii=False,indent=2),flush=True)
