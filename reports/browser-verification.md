# Final browser verification — 2026-10-18

**Passed:** all 18 applicable Chrome checks, with two intentional desktop skips for phone-only cases. The main production run passed 17 checks; the final touch check already achieved two PERFECT turns but its observer used the canvas's test ID as an HTML ID. Correcting that test-only selector and rerunning the touch case passed. Application files stayed frozen throughout this production verification.

## Environment and exact build

- Google Chrome **155.0.8059.82**, headless native Chrome executable; Playwright **1.64.1**, macOS **26.5.1 (25F80)**.
- Native **WebGL 2 / ANGLE Metal Renderer / Apple M4**. No SwiftShader flag, fake audio, accelerated playback, or engine-state override.
- Production under test: `http://127.0.0.1:4175/`, Vite-built `dist/`, entry `assets/index-BCYvXIRq.js`.
- Served entry SHA256: `c7d67ddef619016d8974b6fd3dfa34a9af3e2fcd8e0f004585270b2a17ca55f1`.
- Chart SHA256: `c74248e047a7e0240f2e0260c0ccae975191d484572d79647c78b3a4aec7d7ec` (16 songs, 2,419 turns; Get Up 36.226667 seconds / 16 turns).
- Build receipt: [browser-production-build.json](browser-production-build.json). Scene-source hashes are recorded in [babylon-visual-audit.json](babylon-visual-audit.json).

## Production interactions and real audio

The desktop and iPhone-13 Chromium emulation projects each completed Get Up in **practice and normal mode** using the complete fetched/decoded MP3. Practice cases took 37.7 / 38.5 seconds including setup; normal cases took 38.5 / 38.9 seconds. Normal-mode automation observes the native AudioContext clock and sends ordinary Space key events. It asserts playback rate 1, decoded duration, real elapsed wall time, all 16 timed turns within 100 ms, 100% completion, 10 diamonds / 3 crowns, and persistence after refresh. Practice completion preserves empty normal records.

Additional passing checks cover:

- Native WebGL actually drawing multiple landscape meshes before initial UI screenshots.
- Pause stopping the native audio source, pixel-identical paused canvas over 800 ms, and resuming from a positive audio offset.
- No-input failure, premature-turn failure, retry, and return home.
- Real MP3 HTTP 503 recovery followed by a successful real download/decode.
- Search, all 16 songs, album filters, saved selection, all actual cover images loading, and matching scene captions.
- Settings persistence, real import-button/filechooser interaction, corrupt import preserving storage, and export download.
- Night menu/loading artwork/HUD/pause contrast, and controls inside 390×844, 375×667 and 844×390 layouts.
- Two browser-native touchscreen taps producing exactly two touch pointer events and two successful turns, without a duplicate-trigger failure.

Logs: [production run](browser-e2e-final.log), [focused touch retest](browser-e2e-touch-final.log). Production screenshots include [1440×900 menu](screenshots/production-menu-1440x900.png), [375×667 portrait](screenshots/mobile-375x667.png), [844×390 landscape](screenshots/mobile-844x390.png), and [night HUD](screenshots/mobile-supernatural-night-hud.png).

## Native scene, lifecycle and render audit

The development-only inspector imports the real final Babylon renderer, model factory, engine and chart. It captured **all 16 menus, 16 authored egg-time game states and 16 egg inspection views** across all five album families. Every egg had active rendered mesh geometry. These are deterministic scene states, **not complete song playthroughs**. The inspector is not a production build input.

[Review all captures](screenshots/babylon-final/index.html): [menu contact sheet](screenshots/babylon-final/contact-menu.png), [story contact sheet](screenshots/babylon-final/contact-story.png), [egg contact sheet](screenshots/babylon-final/contact-egg.png). All sheets and the representative production portrait, landscape and night HUD were visually reviewed: continuous roads, album-specific scenery, distinct egg props and readable controls are visible.

After each of three complete 16-level switch cycles (48 switches), the audit returned to New Jeans. All three comparable samples were identical:

| Meshes | Geometries | Materials | Textures | Transform nodes | Vertices |
|---:|---:|---:|---:|---:|---:|
| 317 | 237 | 27 | 0 | 95 | 26,768 |

The separate real NullEngine regression builds 672 models across all profiles, four chapters, scenery variants, landmarks and eggs. It checks finite/nonempty vertex data, valid indices, bounded geometry, stable data size on reuse, and zero owned meshes/materials/geometries/transform nodes after disposal.

After warmup, the inspector sampled 150 frames per viewport during a 1× wall-clock practice-state renderer workload:

| Viewport | Mean FPS | p95 frame time |
|---|---:|---:|
| 1440×900 | 60.13 | 16.8 ms |
| 390×844 | 60.19 | 16.8 ms |
| 375×667 | 60.30 | 16.7 ms |
| 844×390 | 60.22 | 16.8 ms |

Final visual audit exited **0**, with **zero page/console/HTTP errors**: [JSON](babylon-visual-audit.json), [log](babylon-visual-audit.log). The fixture's initial missing favicon was fixed in the fixture and the complete audit rerun cleanly.

## Limits

Phone layouts and touch use desktop Chrome emulation, not physical iPhone hardware or Safari. FPS is a short M4 desktop-GPU sample at device scale 1, not sustained phone performance or a GPU-memory profile. The audio checks prove real decoding, timing and full short-song completion; they do not provide human listening/rhythm-feel acceptance or complete real-time playthroughs of the other 15 songs. The separate 16-song deterministic engine tests cover chart completion. Public deployment and WebKit verification are separate root-owned checks.

An earlier DEV preflight was invalidated by Vite dependency reoptimization/reload while a diagnostic module was introduced; it is excluded from acceptance. The production run above has no HMR or diagnostic-module import. No app defect is inferred from that discarded run.
