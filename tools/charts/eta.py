"""eta: worker W3 design (designs-w3 0890804) charted before the rhythm-logic rule -> audited here (integ-b).
Runs the rhythm-logic audit (tools/charts/integb_audit.py), repairs the route where taps were removed
(tools/charts/integb_route.py) and writes levels-src/eta/ + the revised levels-design/eta/ (original in pre-audit/)."""
from integb_song import run
run('eta', audit=True, meta={'old_tap_count': 232})
