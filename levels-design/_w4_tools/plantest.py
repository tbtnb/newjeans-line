import json, sys, importlib.util, subprocess
sys.path.insert(0, '/workspace/w4')
from route import *; from choreo import *
slug = sys.argv[1]
sp = importlib.util.spec_from_file_location('d', f'/workspace/w4/designs/{slug.replace("-","_")}.py'); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
raw = json.load(open(f'/workspace/w4/{slug}.chart.raw.json')); taps = [r['t'] for r in raw['taps']]
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'/workspace/nj-design-w4/public/audio/{slug}.mp3'],capture_output=True,text=True).stdout)
W = max(w['w'] for w in D.WIDTH); D.ELEV = snap_elev(D.ELEV, taps); print(D.ELEV)
dirs, best = search(taps, D.SPEED, dur, D.BLOCKS, D.ELEV, W, margin=getattr(D,'MARGIN',1.0), beam=getattr(D,'BEAM',6), start=D.START)
nodes = build(taps, dirs, D.SPEED, dur, D.START)
print('final overlaps/cross', overlap_count(nodes, D.ELEV, W, 0))
from plotroute import plot_route
plot_route(f'/workspace/w4/{slug}.plan.png', nodes, D.ELEV, W, raw['sections'], slug, blocks=D.BLOCKS)
json.dump(dirs, open(f'/workspace/w4/{slug}.dirs.json', 'w'))
from plotroute import plot_sections
plot_sections(f'/tmp/{slug}.plansec.png', nodes, D.ELEV, W, raw['sections'], slug, dur)
print('hit pairs', overlaps(nodes, D.ELEV, W, margin=0)[:12])
