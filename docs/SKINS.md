# Line skins (branch `skins`)

Selectable looks for the player's line: head, trail, turn burst and death shatter. All skins are unlocked. `unlockHint`
exists in the data but nothing enforces it.

| id | Name | Look |
| --- | --- | --- |
| classic | 经典 | Default. Plain line coloured by the level palette (`pal.line`), same as before skins existed. |
| bunny | 兔兔 | Milk-white cube with pastel-blue bunny ears, a pink nose and a tail. The ears flick on each turn. Plush trail with pastel dots and blue edge trims. Turns burst into hearts. |
| denim | Y2K 牛仔 | Indigo twill denim with orange double stitching along both trail edges. Copper rivets and an orange tag on the head. Thread and denim-scrap particles. |
| bubble-gum | 泡泡糖 | Glossy candy-pink head. A translucent bubble on its nose shrinks on each turn and re-inflates. Pink gum trail with sprinkles. Pink and mint bubble particles. |
| phoning | 翻盖机 | Flip-phone LCD: mint-cyan backlit pixel-grid trail with navy borders, sampled with nearest-neighbour magnification. Antenna with a blinking pink tip. Pixel-star particles (additive). |
| film | Ditto 胶片 | Misty blue-grey film strip with sprocket holes on both edges, animated film grain and a faint sheen. Frosted head with a blinking red REC light and viewfinder corners. Snowflake particles. |
| supernatural | 超自然铬 | Chrome with a view-angle iridescent (holographic) sheen. Electric-blue and violet neon edge lines. A spinning 4-point Y2K star floats above the head. Star particles (additive). |

## Code
- `src/skins.ts`: the data-only registry (`SKINS`, `getSkin`, `DEFAULT_SKIN = 'classic'`). Adding a skin means one
  entry plus `public/skins/<id>/{trail,particle,icon}`.
- `src/render/lineskin.ts`: the `LineSkin` class, plus `LineSkinPlugin`, a StandardMaterial plugin. The plugin:
  - Computes box-space UVs in the shader: across the line = local x, along the run = distance from the run's back end in
    world units. The pattern does not swim as a run grows.
  - Adds iridescent sheen and animated grain, so the thin-instanced trail stays one draw call.
  - Is disabled for classic, so the classic shader is identical to before.
  - `LineSkin` also handles the head decor meshes and two pooled `ParticleSystem`s (turn and death), which reuse
    `manualEmitCount` instead of being created per event.
  - Per-frame `update()` allocates nothing. Classic recolours only when `pal.line` changes.
- `src/render/world.ts`: about 12 small hooks:
  - `skin` field, `setSkin(id)`.
  - `skin.attach` after the head and trail are created in `load()`; `skin.detach` at the top of `unload()`;
    `skin.reset` in `seek()`.
  - `skin.onTurn` in `onTurn()`, which also tints the turn glow with the skin colour.
  - `skin.onShatter` and `shardCount` in `shatter()`.
  - The line-colour line in `applyTime()` is replaced by `skin.update(...)`.
- `src/skinui.ts`: the picker sheet. It has an animated 2D isometric preview (zig-zag line with the real trail texture,
  head icon and tinted burst sprites) and a card grid, with portrait, landscape and desktop layouts.
- `index.html`:
  - Top-bar `#btn-skins`.
  - Settings row `#btn-open-skins` / `#set-skin-name`.
  - `<section id="skins">`.
- `src/style.css`: an appended `/* line skins */` block.
- `src/main.ts`:
  - The `initSkinUI` import and init.
  - `world.setSkin(save.settings.skin)` at startup.
  - Re-applies the skin after a save import.
- `src/storage.ts`:
  - `Settings.skin` (default `'classic'`).
  - `parseSave` keeps any id that matches `^[a-z0-9-]{1,32}$`, so unknown future ids round-trip and render as classic.
    Anything else becomes `'classic'`.
  - Older saves without the field load unchanged.

Gameplay and timing code (`src/core/*`, `audio.ts`) is untouched.

## Art
- Codex (`gpt-6.1-sol`, high) made the concept sheets and source textures on the Mac mini. See `levels-design/skins/`
  (concept.jpg, design.md with palette, material notes and prompts, src/ 512 px) and `levels-design/skins/CREDITS.md`.
- `tools/skins/build_skin_textures.py <raw dir>` builds the runtime files in `public/skins/` (about 320 KB total).

## QA
- `node tools/qa/skin-shots.mjs --url http://127.0.0.1:PORT/?debug --out deliverables/skins` captures the shots
  (scripted CDP touch simulation in OMG, from 18 s):
  - one in-play shot per skin, 0.16 s after a turn;
  - a deliberate miss, then a death shot;
  - the picker in 390x844, 844x390 and 1440x900, with a click on a card checking that the save and the world both
    switch skin.
- `python3 tools/skins/contact_sheet.py` builds the contact sheet.
