"""cool-with-you: worker W3 design (designs-w3 0890804) charted before the rhythm-logic rule -> audited here (integ-b).
Runs the rhythm-logic audit (tools/charts/integb_audit.py), repairs the route where taps were removed
(tools/charts/integb_route.py) and writes levels-src/cool-with-you/ + the revised levels-design/cool-with-you/ (original in pre-audit/)."""
from integb_song import run
run('cool-with-you', audit=True, meta={'old_tap_count': 107})
