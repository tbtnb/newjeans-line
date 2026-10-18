Worker w2 tools (OMG, Ditto, New Jeans, Super Shy). Venv: /workspace/venv-w2 (librosa 1.0, demucs, matplotlib). Work dir: /workspace/w2-work (analysis json per song), stems: /workspace/w2-stems/htdemucs.
1. demucs -n htdemucs on public/audio/<slug>.mp3  → stems (NOTE: stems come out 25.03 ms late vs the gapless decode; analysis jsons are corrected by -552 samples @22.05k).
2. analyze.py <slug> → /workspace/w2-work/<slug>.json ; gridfit.py/setgrid.py refit BPM/phase on the drum stem.
3. rmap.py <slug> → per-bar 16-step onset maps (used to hand-pick bar patterns).
4. spec_<slug>.py = the hand-authored chart patterns, route motifs/pivots, elevation, layout; build.py <slug> → chart.json/layout.json/route.png (beam-searched dirs, overlap-free); report.py → chart-report.md + analysis.json; notes.py → analysis-notes.md.
