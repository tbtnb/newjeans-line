# 跳舞的线 · NewJeans

A browser recreation of Dancing Line’s one-touch rhythm gameplay, built with TypeScript and Babylon.js. Sixteen full-length vocal tracks from the supplied NewJeans collection, each with a rhythm chart and a themed 3D world. Only the user’s requested sixteen songs are included; instrumental versions and the three other supplied songs are excluded. Six missing vocal files were downloaded from the user’s Quark shared collection and verified locally.

## Play

- Click **开始旅程**, then tap the scene / press **Space** at a corner to turn 90 degrees.
- Keep the growing line on the path. Missed or mistimed turns end the run.
- Collect 10 diamonds and crowns at 30%, 60%, and 100% of a song.
- Practice mode recovers missed turns and does not count toward normal records.
- Pause with the on-screen control; adjust audio, latency, visual quality and guidance in Settings.

The game has no backend or account. Progress and preferences stay in this browser’s local storage. Export a save in Settings to move it between browsers. Audio and chart data are static website assets.

## Develop

```sh
npm ci
npm run dev
npm test
npm run build
npm run test:e2e
```

`npm run dev` serves port 4173. Playwright browser installation may be needed on a new machine (`npx playwright install chromium`). For a production check, build and run `npm run preview -- --port 4173`.

For the WebKit smoke journey, install `npx playwright install webkit`, serve the production build on port 4175, and run `npm run test:webkit`. `PLAYWRIGHT_BASE_URL` can target another local or published URL. `CHROME_PATH` optionally selects an installed Chrome for the Chromium tests. The development-only deterministic scene inspector is exercised with `npm run test:visual` against the dev server; it is excluded from the production build.

## Album worlds and stories

The sixteen scene designs were researched and frozen before the final engine implementation. Five visual families come from the actual embedded album covers: denim blue, burgundy memory, pastel pixels, summer mixtapes, and rainbow flowers. Each song has its own staged environment, landmark and background Easter egg. See [the complete design](design/ART_DIRECTION.md), [songs 1–8 research](design/research-early.md) and [the remaining song research](design/research-later.md).

The five generated illustrations are loading-screen assets and visual references; the playable route and scenery are real Babylon.js geometry. Local album covers are used in the library. Story proposals and Easter eggs are original interpretations, distinguished from the cited artist/director statements.

## Sources and scope

Reference research used general/image search and targeted App Store, TapTap and gameplay searches. The [official App Store listing](https://apps.apple.com/us/app/dancing-line-music-game/id1177953618) and [official TapTap listing](https://www.taptap.cn/app/31429) describe the tap-to-turn, music-guided gameplay. [Classic UI screenshots](https://www.elespanol.com/elandroidelibre/aplicaciones/juegos/20170505/dancing-line-nuevo-musical-creadores-piano-tiles/213729439_0.html) informed the spare typography, diorama presentation, progress and crown/diamond motifs. Aggregate search and platform-targeted queries were used because the available search API does not expose named search-engine selection.

This is an independent fan project, not an official Dancing Line or NewJeans release. All scene models and interface code were newly implemented. It is a recreation of the core interaction and visual motifs, not a verified pixel-identical port or a copy of the original game’s levels, source code, UI assets or physics. The music comes from the user-supplied files; audio rights remain with their respective owners.

Rhythm charts are generated from real audio analysis and structured patterns, rather than hand-transcribed original-game charts. Analysis details are recorded in `reports/audio-analysis.json` and [the calibrated rhythm audit](reports/rhythm-audit-final.md). Strong transients are measured and corrected; weak/melodic passages remain estimates. The audit explicitly distinguishes independent checks from detector self-consistency and does not claim human listening validation.

## Verification

The final local checks cover 20 unit/model/asset/storage tests, including deterministic completion of all 16 charts, and [18 applicable production Chrome interaction checks](reports/browser-verification.md). Full real-audio Get Up runs cover normal and practice modes at 1× speed. All 16 scenes and Easter eggs were rendered and reviewed; 48 level switches preserved resource counts. [The scene gallery](reports/screenshots/babylon-final/index.html) and [audit data](reports/babylon-visual-audit.json) record the evidence and source hashes. Mobile browser emulation is not physical-phone testing.

The separate [WebKit production smoke](reports/webkit-production.json) passed real MP3 playback, full Get Up practice completion with pause/resume, two native touch turns, failure handling, persisted progress, three phone layouts and the night-level HUD. This ran on macOS WebKit with iPhone emulation.

## Deploy

The Vite build uses relative URLs for a GitHub Pages project path. Publish the contents of `dist/` on the `gh-pages` branch and configure GitHub Pages to serve that branch’s root. No secrets or backend configuration are needed in the browser build.
