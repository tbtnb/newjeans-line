"""asap: worker W3 design (designs-w3 0890804) charted before the rhythm-logic rule -> audited here (integ-b).
Tempo: the full-mix onsets fit 130.0 BPM (97 % of strong onsets within 25 ms of the 16th grid) - the worker's 130.012 BPM
grid - while analysis/asap.grid.json says 129.52 BPM (drifts ~0.4 s by the end). So the chart declares its grid in meta
(chartlogic.py then uses it) and the layout carries its own beat list for beat-reactive scenery."""
from integb_song import run
P = 60 / 130.012; B0 = round(1.264 - 8 * P / 4, 4)   # first tap 1.264 s = bar 0, 16th 8 (worker's grid)
run('asap', audit=True, meta={'bpm': 130.012, 'beat_period': P, 'beat0': B0, 'old_tap_count': 83}, beat_grid=(P, B0))
