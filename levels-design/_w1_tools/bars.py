import json,sys,numpy as np
s=sys.argv[1]; a=json.load(open(f'{s}.analysis.json'))
r=np.array(a['rms_per_beat']);k=np.array(a['kick_per_beat']);sn=np.array(a['snare_per_beat']);v=np.array(a['vocal_per_beat'])
p=a['beat_period'];ph=a['grid_phase']
# sync returns len(grid)+1 segments: first segment before first beat
print(s,'bpm',a['bpm'],'phase',ph)
n=len(r)
for b in range(0,n-1,4):
    t=ph+(b)*p
    seg=slice(b+1,b+5)
    bar=lambda x:''.join(' .:-=+*#%@'[min(9,int(xx*9/ (np.percentile(x,98)+1e-9)))] for xx in x[seg])
    print(f'{b//4:3d} {t:7.2f}  rms {bar(r)} kick {bar(k)} sn {bar(sn)} voc {bar(v)}')
