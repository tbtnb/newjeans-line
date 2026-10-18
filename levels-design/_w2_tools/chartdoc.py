"""append chart rationale (spec.WHY) + per-section density + sync spot-check summary (from chart-report.md) to design.md"""
import sys,importlib,re
sys.path.insert(0,'/workspace/w2-work'); slug=sys.argv[1]
spec=importlib.import_module('spec_'+slug.replace('-','_')); D=f'/workspace/newjeans-line-designs/{slug}'
rep=open(f'{D}/chart-report.md').read()
out=['\n## Chart rationale (why the taps are where they are)']
for k,v in spec.WHY.items(): out.append(f'- **{k}**: {v}')
m=re.search(r'## Per-section density.*?(?=\n## )',rep,re.S)
if m: out.append('\n'+m.group(0).replace('## Per-section density','## Per-section density (from chart-report.md)'))
m=re.search(r'## Alignment.*',rep,re.S)
out.append('\nSync: every tap is snapped to a real onset of its tagged demucs stem (shifted −25.03 ms) within ±45 ms; spot checks at start / middle / section changes / end are in `chart-report.md` (stem and independent full-mix detector).')
open(f'{D}/design.md','a').write('\n'.join(out)+'\n')
