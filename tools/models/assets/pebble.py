"""Ground cover: faceted paper pebble (20 tris)."""
BUDGET = 20
def build(P, spec):
    P.ico('pebble', 0.14, loc=(0, 0, 0.07), color='#D8CCF0', subdiv=0, scale=(1.2, 1.0, 0.65), jitter=0.015)
