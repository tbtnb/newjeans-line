# levels-design/
Design hand-off area between the design workers and the integrator. Read **SCHEMA.md** first, then **REFERENCE.md** (the original Dancing Line research plus the route-choreography bar).
- `validate.py <slug> --dir levels-design`: engine-exact centreline, air-time rule, overlap/crossing rule, 10 diamonds / 2 crowns, art file checks.
- `analyze.py [slug]`: the librosa candidate analysis used for `analysis/<slug>.json` (run from the repo root; needs librosa).
- `<slug>/`: per-song design (chart.json, layout.json, design.md, art/), committed by workers on branches `designs-w1..w4`.
