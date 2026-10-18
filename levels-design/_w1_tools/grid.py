import sys,json
s=sys.argv[1]; d=json.load(open(f'{s}.taps.json')); a=json.load(open(f'{s}.analysis.json'))
import importlib; cfg=importlib.import_module('cfg_'+s.replace('-','_')).cfg
P=a['beat_period']; ph=a['grid_phase']+cfg.get('bar_off',0)*P; res=int(sys.argv[2]) if len(sys.argv)>2 else 2
bars={}
for t in d['taps']:
    n=round((t['grid']-ph)/P*res); b=n//(4*res); bars.setdefault(b,['.']*(4*res)); bars[b][n%(4*res)]={'vocal_on':'v','kick_on':'k','snare_on':'s','mel_on':'m','bass_on':'b'}.get(t['tag'],'x')
sec=None
for b in range(0,int(a['duration']/P/4)+1):
    t=ph+b*4*P
    cur=[x[0] for x in d['stats'] if x[1]<=t+0.3]
    lab=cur[-1] if cur else ''
    if lab!=sec: print('--',lab); sec=lab
    print(f'{b:3d} {t:7.2f} |'+'|'.join(''.join(bars.get(b,['.']*(4*res))[i*res:(i+1)*res]) for i in range(4))+'|')
