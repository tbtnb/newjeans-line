import json, sys
slug = sys.argv[1]; OUT = f'/workspace/newjeans-line-designs/{slug}'
L = json.load(open(f'{OUT}/layout.json')); C = json.load(open(f'{OUT}/chart.json'))
o = []
o.append('## Generated facts (from layout.json / chart.json)\n\n')
o.append(f"- Road width {L.get('road')}; start heading {C.get('startHeading')}; speed {C.get('speed')}\n")
o.append('- Elevation: ' + '; '.join(f"{e.get('type')} {e.get('dy'):+} @ {e.get('t', e.get('t0'))}{'–'+str(e['t1']) if 't1' in e else ''} ({e.get('note','')})" for e in L.get('elevation', [])) + '\n')
o.append('- Camera: ' + '; '.join(f"{c['t']}s {c.get('mode', c.get('preset',''))}" for c in L.get('camera', [])) + '\n')
o.append('- Diamonds (t): ' + ', '.join(str(d['t']) for d in L['diamonds']) + f"; crowns (checkpoints): {', '.join(str(c['t']) for c in L['crowns'])}\n")
lm = [x for x in L['objects'] if x.get('landmark')]; eg = [x for x in L['objects'] if x.get('egg')]
o.append('- Landmarks: ' + '; '.join(f"`{x['id']}` ({x.get('name','')})" for x in lm) + '\n')
o.append('- Easter eggs: ' + '; '.join(f"`{x['id']}` ({x.get('name','')})" for x in eg) + '\n')
fk = [x for x in L['objects'] if x['id'].startswith('fork')]
o.append(f"- Fake-out forks (visual only, road-coloured dead-end stubs that rise 2 s early and sink after the corner; they are revealed together with the road (same lead), so they add no timing information and only fake a straight continuation): {', '.join(x['id'] for x in fk)}\n")
o.append(f"- Objects: {len(L['objects'])} total; events: {len(L.get('events', []))}\n")
art = L.get('art', {}); imgs = sorted({x.get('src') for x in L['objects'] if x.get('src')} | {p.get('texture') for x in L['objects'] for p in x.get('parts', []) or [] if p.get('texture')})
o.append(f"- Art wired into layout: backdrop `{art.get('backdrop')}`, ground `{(art.get('ground') or {}).get('src')}`, images/textures {', '.join('`'+i+'`' for i in imgs if i)}\n")
open(f'{OUT}/design.facts.md', 'w').write(''.join(o)); print(''.join(o))
