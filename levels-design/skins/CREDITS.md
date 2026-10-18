# Line skin art credits

All skin art in `levels-design/skins/<skin>/` and the runtime textures derived from it in `public/skins/<skin>/` was
generated for this fan project by **Codex** (`codex exec -m gpt-6.1-sol -c model_reasoning_effort=high`, built-in
`image_gen` tool) on the project owner's Mac mini, 2026-10-18, from the briefs in `tools/skins/skins.tsv`
(run script: `tools/skins/codex-run.sh`). Each `design.md` is Codex's own spec for that skin: palette hex codes, material
and particle notes and the exact image prompts.

The designs are original "inspired-by" interpretations of NewJeans-era motifs (bunny, Y2K denim, bubblegum pop,
flip-phone LCD, Ditto film, Supernatural chrome). No official logo, brand mark, lettering or likeness of any person is
used. NewJeans and related names belong to their respective owners; this is a non-commercial fan project.

Runtime processing (`tools/skins/build_skin_textures.py`, no AI): resize to 256 px trail tiles (u = across the line,
v = along it; some rotated 90 degrees), thin edge trims drawn for bunny/supernatural/phoning, particle sprites
desaturated to 128 px so the game can tint them, icons cropped to content at 128 px.

| Skin | Concept | Runtime files |
| --- | --- | --- |
| bunny 兔兔 | bunny/concept.jpg | public/skins/bunny/{trail.jpg, particle.png, icon.png} |
| denim Y2K 牛仔 | denim/concept.jpg | public/skins/denim/{trail.jpg, particle.png, icon.png} |
| bubble-gum 泡泡糖 | bubble-gum/concept.jpg | public/skins/bubble-gum/{trail.jpg, particle.png, icon.png} |
| phoning 翻盖机 | phoning/concept.jpg | public/skins/phoning/{trail.png, particle.png, icon.png} |
| film Ditto 胶片 | film/concept.jpg | public/skins/film/{trail.jpg, particle.png, icon.png} |
| supernatural 超自然铬 | supernatural/concept.jpg | public/skins/supernatural/{trail.jpg, particle.png, icon.png} |
