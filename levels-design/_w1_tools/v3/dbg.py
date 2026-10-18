import sys, importlib
sys.path.insert(0, '.')
from chore import *; from util import *
Pm = importlib.import_module('plan_attention'); chart, T = taps('attention')
pl = Planner(T, Pm.dur, Pm.speed, Pm.widths, Pm.elev(T), Pm.moves(), start='N', max_tries=3000)
try: pl.solve()
except RuntimeError as e: print(e)
nodes, el, v = pl.fail_nodes
for n in nodes:
    if 78 < n[0] < 86: print([round(x, 2) if isinstance(x, float) else x for x in n], round(elev_at(el, n[0]), 2))
print([e for e in el])
