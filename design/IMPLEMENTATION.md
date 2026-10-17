# Frozen implementation interfaces after design

Read ART_DIRECTION.md, BRIEF.md and both research documents. The user’s final direction supersedes the old generic-theme instructions in CONTRACT.md. Use Babylon.js, never Three.js in final implementation. Existing game/audio/UI modules remain a tested starting point.

## Ownership

- Astra xhigh modeling: src/world-models.ts, src/level-design.ts. Real album-informed procedural meshes, scenery, landmark and Easter-egg models. No world.ts or UI edits.
- GPT-6.1 high scene coding: src/world.ts, optional src/world-geometry.ts. Native Babylon engine, scene, camera, road, trail, collectible geometry, resource lifecycle, model placement and rendering. No model-factory or UI edits.
- GPT-6.1 high UI: src/main.ts, src/style.css, src/storage.ts. Integrate album art, generated loading artwork, selected scene captions and dark/light palette with existing functioning UI. No world/model changes.
- GPT-6.1 high audio: scripts/prepare_audio.py, scripts/rhythm_audit.py, src/levels.json, reports/audio*.json/md, reports/rhythm*.json/md. True transient alignment audit and correction, four song-specific section labels/points; no game engine changes.
- Root: package/config/tests/deployment/docs, integration. All workers are not alone in the codebase and must preserve others’ work.

## Scene public API — unchanged

`new WorldRenderer(canvas:HTMLCanvasElement)`; `load(level:Level):void`; `render(snapshot:GameSnapshot, options:{mode:'menu'|'game';elapsed:number;quality?:'high'|'low';guide?:boolean}):void`; `resize():void`; `dispose():void`.

Main owns requestAnimationFrame and passes absolute elapsed seconds and the current game snapshot. Do NOT start a second Babylon runRenderLoop. Scene code calls scene.render() inside WorldRenderer.render(). Never attach camera controls that consume gameplay touches. Audio and input remain main/engine owned. Audio is the game clock.

World path starts at x=0,z=0 and alternates +x/-z using buildPath/positionAt/SPEED/TRACK_WIDTH from engine.ts. The public world coordinates must stay unchanged through migration; use Babylon scene.useRightHandedSystem=true if helpful. ROAD_TOP is 0.52. Ground/scenery use that height as the normal platform top. Player cube above road. Menu may use a compact curated route and surrounding scenery, game uses the real song route. Width and visible line thickness must agree with engine judgment.

## Album/level art data API (modeling agent owns)

`export type ArtFamily = 'denim'|'memory'|'pixel'|'mixtape'|'bloom';`

`export interface LevelArt { family:ArtFamily; scene:string; subtitle:string; description:string; cover:string; concept:string; dark:boolean; colors:{background:string;ground:string;road:string;roadSide:string;line:string;accent:string;secondary:string;ink:string}; chapters:string[]; egg:{at:number;name:string;type:string}; }`

`export function getLevelArt(id:string):LevelArt;`

Exactly16 named profiles. Family cover paths are `./art/covers/new-jeans.jpg`, `omg.jpg`, `get-up.jpg`, `how-sweet.jpg`, `supernatural.jpg`. Concepts are `./art/concepts/denim.png`, `memory.png`, `pixel.png`, `mixtape.png`, `bloom.png`. Map song New Jeans to get-up.jpg, not new-jeans.jpg. Root has copied all final images to public/art. Additional world-specific fields may be added compatibly; UI needs only declared fields. Data is source-of-truth for renderer colors, names and main imagery.

## Babylon model factory API (Astra implements; scene coder consumes)

`export class WorldModels { constructor(scene:Scene, art:LevelArt); createScenery(variant:number, chapter:number, seed:number):TransformNode; createLandmark(chapter:number):TransformNode; createEasterEgg():TransformNode; update(elapsed:number, progress:number):void; dispose():void; }`

- Every returned group has origin x=0,z=0 and normal platform top y=0.52. Caller positions group in world. Scenery footprint stays within +/-3 units of origin, height <=5. Landmark footprint within +/-4,height<=7. Egg footprint within +/-2,height<=3. Declare any exception before use.
- Put model groups outside the route; scene coder measures distance against the visible polyline and maintains >=1 road width clearance. Never place scenery at the line’s next corner.
- Scenery variant/chapter changes meaningful arrangements, not random color. Each profile has a unique landmark and actual modeled Easter egg from ART_DIRECTION. Factory update may animate owned models using elapsed/progress; store animations without leaking disposed instances.
- Share Babylon geometry/materials and use instancing or merged static meshes where useful. Hide source meshes safely; do not dispose resources still used by visible clones. Static low-poly motifs, no imported remote models/textures required. Background halftone may use a small procedural DynamicTexture; no per-frame texture drawing.
- Clear boundaries between gameplay road and scenery. Generated illustrations are UI/design assets; don't replace the actual 3D road with a bitmap.

## Scene performance and staging

Render only nearby route/scenery. Prefer pooled segments and instance clusters. Cap effective pixel ratio at1.5(high),1(low), and lower shadow work for low quality. Avoid reconstructing geometry/materials every frame. Stable isometric camera with smooth look-ahead. Scene changes at level.sections checkpoints while keeping old/new nearby scenery coherent. Billboard-like flat album motifs are allowed as 3D details; preserve readability.

Dark styling applies only where the art profile says dark. Main must make menu/HUD text readable against dark scenes and keep dialog text appropriate for its background. Menu and game composition must be checked at390×844,375×667,844×390 and1440×900. Do not claim mobile-device performance from a resized desktop window.

## Audio work after design

Preserve exact16 order. Four section labels come from LevelArt.chapters; boundaries must use actual audio structure/beat cues with explicit estimation status, not secretly claim manual verification. Existing charts already cover complete44m24.98s and MP3 payload integrity is verified. Focus additional work on correctly calibrated strong transient alignment, weak-onset handling, onset quantiles and drift. Don't change source audio. First test analysis method on synthetic transients so an STFT early/late bias is not mistaken for game offset.

## Verification sequence

Build/typecheck after all native Babylon interfaces exist. Unit/assets/storage tests, all16 deterministic chart completions, real browser flows and whole36s normal+practice GetUp. Screenshot representative album families and special maps/eggs. Only final Babylon and corrected-chart results count. Root handles repository creation and Pages deployment, then verifies the public build and real audio. No worker commits or publishes.
