# Worker w2 tools (OMG, Ditto, New Jeans, Super Shy)
Venv: `/workspace/venv-w2` (librosa 1.0, demucs 4, torch cpu, matplotlib, PIL). Work dir `/workspace/w2-work`; stems `/workspace/w2-stems/htdemucs/<slug>/`.
Run heavy audio jobs under `flock /workspace/.nj-heavy.lock` (demucs `-d cpu --segment 7 -j 1`).

1. demucs htdemucs on `public/audio/<slug>.mp3`. **Stems come out 25.03 ms (1104 samples @44.1 kHz) late** vs the gapless decode (browser/librosa); `analyze.py` shifts them.
2. `analyze.py <slug>` → `<slug>.json` (band-flux kick/snare/hat, per-stem onsets refined to the attack, RMS). `gridfit.py`/`setgrid.py` fit BPM/phase on the drum stem.
3. `rmap.py <slug>` → per-bar 16-step onset maps; bar patterns in `spec_<slug>.py` are hand-picked from these.
4. `spec_<slug>.py`: chart patterns (SECTIONS), WHY, speed/width, ELEV (levels), **ROUTE** (per-section motif + drift bearing), FORKS, BUILDINGS, ART, layout().
5. `finalize.sh <slug>`: `build.py` (taps snapped ±45 ms to the tagged stem; air-time fix; `route.py` beam planner with the exact v2.4 overlap rule; landmark pockets; fake forks; cut-away buildings; route.png + route-sections.png) → `report.py` (chart-report.md, analysis.json) → design.md (docs/<slug>_head.md + `route_doc.py` table + docs/<slug>_tail.md + `chartdoc.py`) → validate → copy into the clone.
6. `artgen.py <slug>`: procedural PIL art in the level palette → `<slug>/art/`. (GenerateImage was tried; its output path did not exist on the box, so procedural art was used. Prompts used, for a later re-render: OMG sky "soft sage→cream halftone-cloud sky with blush horizon"; ground "tileable halftone dots on sage"; poster "halftone black bunny, blank white mask, cream ground"; phone "black phone screen with chat bubbles and typing dots, no text"; decal "glass slipper + black cat on an open storybook sticker". Equivalent prompts per song are described in each design.md art table.)

## v4 difficulty calibration (fast bursts + CPM)
- `build.apply_bursts`: for each `spec.BURST_WINDOWS` (t0, t1, max) it looks for 2–4 real onsets, either in one stem or in a merged drum/vocal/melody stream inside a passage with ≥ 5.5 onsets/s, whose gaps are all in [`BURST_MIN` (0.152), `BURST_MAX` (0.19)] s. It replaces the taps around them, keeping ≥ 0.20 s to the neighbours. Lowering `BURST_MIN` to ~0.11 would chart true 16ths if the schema floor (0.15 s) is ever relaxed.
- `report.py` adds a "Difficulty calibration" section: avg CPM (taps ÷ length, and wiki-style mean of 60/gap), peak CPM, bursts, dotted-8th count, and a comparison table with the original Dancing Line levels.
