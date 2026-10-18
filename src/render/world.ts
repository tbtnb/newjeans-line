import {
  Color3, Color4, CreateBox, CreateDisc, CreateCylinder, CreateGround, CreatePlane, CreatePolyhedron, DirectionalLight, DynamicTexture, Engine, HemisphericLight,
  Matrix, Mesh, ParticleSystem, Quaternion, Scene, ShadowGenerator, StandardMaterial, Texture, TransformNode, Vector3,
} from './bjs';
import { anchor, flowAnchor, HEAD_VEC, posAt, spanIndexAt, spanPos, type Route } from '../core/path';
import { lineHeading, linePos, pendingCorner } from '../core/linepath';
import type { Game } from '../core/game';
import type { LevelData, Palette, SceneObject, SceneEvent, Heading } from '../core/types';
import { buildKind, hex, Materials, textPlane } from './prefabs';
import { Road, stepAt } from './road';
import { ShowFx } from './showfx';
import { Corridor } from './corridor';
import { Dressings } from './dressing';
import { EnvTimeline } from './env';
import { CameraRig } from './camera';
import { LineSkin } from './lineskin';

const LINE_W = 1.0, LINE_H = 0.9;
/** one straight trail run: axis-aligned box from a to b (heading h), extended by LINE_W/2 at both ends */
interface Run { a: Vector3; b: Vector3; h: number; slope: number; }
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

interface Obj { node: TransformNode; def: SceneObject; t: number; base: Vector3; baseScale: Vector3; baseRotY: number; hidden: boolean; id?: string; lit?: { mat: StandardMaterial; base: Color3 }[]; glow?: number; glowColor?: Color3; bc?: Vector3; br?: number; fade?: number; box?: number[]; }
const ART_KINDS = new Set(['standee', 'facade']);
const _cv = new Vector3();
interface Fx { mesh: Mesh; t0: number; dur: number; kind: string; vel?: Vector3; spin?: Vector3; from?: Vector3; }

function radialTexture(scene: Scene, name: string, inner = 'rgba(255,255,255,1)', outer = 'rgba(255,255,255,0)', square = false) {
  const tex = new DynamicTexture(name, { width: 128, height: 128 }, scene, false);
  const ctx = tex.getContext() as unknown as CanvasRenderingContext2D;
  ctx.clearRect(0, 0, 128, 128);
  if (square) { ctx.fillStyle = inner; ctx.fillRect(24, 24, 80, 80); }
  else { const g = ctx.createRadialGradient(64, 64, 0, 64, 64, 64); g.addColorStop(0, inner); g.addColorStop(0.35, inner.replace(/[\d.]+\)$/, '0.6)')); g.addColorStop(1, outer); ctx.fillStyle = g; ctx.fillRect(0, 0, 128, 128); }
  tex.hasAlpha = true; tex.update();
  return tex;
}

/** Road-occupancy grid for keeping scenery off the road. */
class RoadGrid {
  private cells = new Map<string, { x: number; z: number; y: number; r: number }[]>();
  constructor(route: Route, widthAt: (t: number) => number) {
    for (const s of route.spans) {
      if (s.air) continue;
      const len = s.v * (s.t1 - s.t0); const n = Math.max(1, Math.ceil(len / 0.8));
      for (let i = 0; i <= n; i++) { const t = s.t0 + (s.t1 - s.t0) * i / n; const p = spanPos(s, t); this.add(p.x, p.z, p.y, widthAt(t) / 2 + 0.5); }
    }
  }
  private key(x: number, z: number) { return `${Math.floor(x / 4)},${Math.floor(z / 4)}`; }
  private add(x: number, z: number, y: number, r: number) { const k = this.key(x, z); let c = this.cells.get(k); if (!c) this.cells.set(k, c = []); c.push({ x, z, y, r }); }
  /** true if a footprint of radius r at (x,z) with vertical span [y0,y1] collides with any road point */
  hits(x: number, z: number, r: number, y0 = -1e9, y1 = 1e9) {
    const cx = Math.floor(x / 4), cz = Math.floor(z / 4); const span = Math.ceil((r + 2) / 4);
    for (let i = cx - span; i <= cx + span; i++) for (let j = cz - span; j <= cz + span; j++) {
      for (const p of this.cells.get(`${i},${j}`) ?? []) if (Math.hypot(p.x - x, p.z - z) < p.r + r && y1 > p.y - 1.2 && y0 < p.y + 3.2) return true;
    }
    return false;
  }
}

export class World {
  engine: Engine; scene: Scene;
  private canvas: HTMLCanvasElement;
  private hemi: HemisphericLight; private sun: DirectionalLight; private shadows: ShadowGenerator | null = null;
  private level: LevelData | null = null; private game: Game | null = null; private route: Route | null = null;
  private root: TransformNode | null = null; private mats: Materials | null = null;
  private road: Road | null = null; private dress: Dressings | null = null; private occP: { x: number; y: number; z: number; r: number }[] = []; private occView: Matrix | null = null; private occTh = 1; private occAspect = 1; private env: EnvTimeline | null = null; rig: CameraRig | null = null;
  private ground: Mesh | null = null; private groundMat: StandardMaterial | null = null;
  private head: Mesh | null = null; private halo: Mesh | null = null; private headEdge = new Color3(0.3, 0.1, 0.15); private haloMat: StandardMaterial | null = null; private trail: Mesh | null = null; private trailMat: StandardMaterial | null = null; private headMat: StandardMaterial | null = null;
  private trailBuf = new Float32Array(16 * 64); private trailCount = 0; private runs: Run[] = []; private failRun: Run | null = null;
  private show: ShowFx | null = null; private corridor: Corridor | null = null;
  private objects: Obj[] = []; private faceCam: Obj[] = []; private groundTex: { t: number; tex: Texture }[] = []; private groundShown: Texture | null = null; private groundTint: Color3 | null = null; private byId = new Map<string, Obj[]>();
  private diamonds: { mesh: Mesh; t: number; taken: boolean; base: Vector3 }[] = [];
  private crowns: { node: TransformNode; t: number; taken: boolean; base: Vector3 }[] = [];
  private fx: Fx[] = []; private glowTex: DynamicTexture | null = null; private sparkTex: DynamicTexture | null = null;
  private particles: ParticleSystem | null = null; private particleKind: string | null = null;
  private events: SceneEvent[] = [];
  private lastTap = -10; private beats: number[] = []; private kicks: number[] = [];
  private lastTime = 0; private lastFrame = performance.now();
  private failAnim: { t0: number; pos: Vector3; dir: Vector3; pieces: Fx[] } | null = null;
  private quality: 'high' | 'low' = 'high';
  mode: 'menu' | 'play' = 'menu';
  fps = 60; private fpsAcc = 0; private fpsN = 0;
  onSky: ((top: string, bottom: string) => void) | null = null;
  /** full-screen backdrop image URL (or null) behind the transparent canvas */
  onBackdrop: ((url: string | null) => void) | null = null;
  private backdrops: { t: number; src: string }[] = []; private backdropShown: string | null | undefined;
  completeAt = -1;
  /** player-line skin (head/trail look, decor, turn + death particles) */
  skin: LineSkin;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.engine = new Engine(canvas, true, { preserveDrawingBuffer: false, stencil: false, alpha: true, antialias: true, powerPreference: 'high-performance' }, true);
    this.engine.setHardwareScalingLevel(1 / Math.min(window.devicePixelRatio || 1, 2));
    this.scene = new Scene(this.engine);
    this.scene.clearColor = new Color4(0, 0, 0, 0);
    this.scene.skipPointerMovePicking = true;
    this.scene.fogMode = Scene.FOGMODE_LINEAR;
    this.hemi = new HemisphericLight('hemi', new Vector3(0.2, 1, -0.3), this.scene);
    this.sun = new DirectionalLight('sun', new Vector3(-0.55, -1, 0.35), this.scene);
    this.sun.position = new Vector3(30, 60, -20);
    this.glowTex = radialTexture(this.scene, 'glow');
    this.sparkTex = radialTexture(this.scene, 'spark', 'rgba(255,255,255,1)', 'rgba(255,255,255,0)');
    this.skin = new LineSkin(this.scene, this.sparkTex);
  }

  /** switch the line skin (live, also between levels) */
  setSkin(id: string) { this.skin.apply(id); }

  setQuality(q: 'high' | 'low') {
    this.quality = q;
    this.engine.setHardwareScalingLevel(1 / Math.min(window.devicePixelRatio || 1, q === 'high' ? 2 : 1));
    if (this.level && this.game) this.setupShadows();
  }

  private setupShadows() {
    this.shadows?.dispose(); this.shadows = null;
    if (this.quality !== 'high' || !this.head || !this.trail) return;
    const sg = new ShadowGenerator(1024, this.sun);
    sg.usePercentageCloserFiltering = true; sg.filteringQuality = ShadowGenerator.QUALITY_LOW;
    sg.bias = 0.004; sg.normalBias = 0.02; sg.darkness = 0.55;
    this.sun.autoUpdateExtends = false; this.sun.autoCalcShadowZBounds = true;
    this.sun.orthoLeft = -26; this.sun.orthoRight = 26; this.sun.orthoTop = 26; this.sun.orthoBottom = -26;
    sg.addShadowCaster(this.head); sg.addShadowCaster(this.trail);
    for (const o of this.objects) if (o.def.landmark) for (const m of o.node.getChildMeshes()) sg.addShadowCaster(m);
    this.road!.top.receiveShadows = true; this.road!.body.receiveShadows = true;
    if (this.ground) this.ground.receiveShadows = true;
    this.shadows = sg;
  }

  unload() {
    this.skin.detach();
    for (const g of this.groundTex) g.tex.dispose(); this.faceCam = []; this.groundTex = []; this.groundShown = null; this.groundTint = null;
    this.particles?.dispose(); this.particles = null; this.particleKind = null;
    this.shadows?.dispose(); this.shadows = null;
    for (const f of this.fx) f.mesh.dispose(); this.fx = [];
    this.failAnim?.pieces.forEach(p => p.mesh.dispose()); this.failAnim = null;
    this.road?.dispose(); this.road = null;
    this.root?.dispose(false, true); this.root = null;
    this.mats?.dispose(); this.mats = null;
    this.trailMat?.dispose(); this.headMat?.dispose(); this.groundMat?.dispose();
    this.rig?.cam.dispose(); this.rig = null;
    this.objects = []; this.byId.clear(); this.diamonds = []; this.crowns = [];
    this.dress?.dispose(); this.dress = null; this.show?.dispose(); this.show = null; this.corridor?.dispose(); this.corridor = null;
    this.head = this.trail = this.ground = null;
    this.level = null; this.game = null; this.route = null;
    // dispose orphan textures/materials created by text planes
    for (const m of [...this.scene.materials]) if (m.name.startsWith('txtm')) { (m as StandardMaterial).diffuseTexture?.dispose(); m.dispose(); }
  }

  load(level: LevelData, game: Game) {
    this.unload();
    this.level = level; this.game = game; this.route = game.route;
    const L = level.layout; const route = game.route;
    this.root = new TransformNode('level', this.scene);
    this.mats = new Materials(this.scene); this.mats.artBase = `./levels/${level.id}/`;
    this.backdrops = [...(L.art?.backdrop ? [{ t: -1, src: L.art.backdrop }] : []), ...(L.sections ?? []).filter(s => s.backdrop).map(s => ({ t: s.t, src: s.backdrop! }))].sort((a, b) => a.t - b.t); this.backdropShown = undefined;
    this.env = new EnvTimeline(L);
    this.beats = L.beats ?? []; this.kicks = L.kicks ?? [];
    this.events = [...(L.events ?? [])].sort((a, b) => a.t - b.t);
    const widthAt = (t: number) => stepAt(L.road.width, t)?.w ?? 2.2;
    // road
    this.road = new Road(this.scene, route, L, t => this.env!.settled(t));
    this.road.body.parent = this.root; this.road.top.parent = this.root;
    if (L.art?.road?.src) { const rm = this.road.top.material as StandardMaterial; rm.diffuseTexture = new Texture(this.mats.artBase + L.art.road.src, this.scene); }
    // ground
    const pal = this.env.base;
    if (pal.groundY !== null && pal.groundY !== undefined) {
      this.ground = CreateGround('ground', { width: 1600, height: 1600, subdivisions: 1 }, this.scene);
      this.groundMat = new StandardMaterial('groundM', this.scene); this.groundMat.specularColor = Color3.Black();
      // themed ground (v2.7: sections[].ground switches the tile at section starts; tint multiplies it)
      const mk = (g: { src: string; scale?: number }) => { const gt = new Texture(this.mats!.artBase + g.src, this.scene); const rep = 1600 / (g.scale ?? 40); gt.uScale = rep; gt.vScale = rep; gt.anisotropicFilteringLevel = 1; return gt; }; // aniso off: a calm backdrop tile, and far cheaper on weak GPUs
      if (L.art?.ground?.src) this.groundTex.push({ t: -1, tex: mk(L.art.ground) });
      for (const sc of L.sections ?? []) if (sc.ground?.src) this.groundTex.push({ t: sc.t, tex: mk(sc.ground) });
      this.groundTex.sort((a, b) => a.t - b.t);
      if (this.groundTex.length) { this.groundMat.diffuseTexture = this.groundTex[0].tex; this.groundShown = this.groundTex[0].tex; }
      this.groundTint = L.art?.ground?.tint ? hex(L.art.ground.tint) : null;
      this.ground.material = this.groundMat; this.ground.position.y = pal.groundY; this.ground.isPickable = false; this.ground.parent = this.root;
    }
    // player line
    this.headMat = new StandardMaterial('headM', this.scene); this.headMat.specularColor = new Color3(0.1, 0.1, 0.1);
    this.trailMat = new StandardMaterial('trailM', this.scene); this.trailMat.specularColor = new Color3(0.05, 0.05, 0.05);
    this.head = CreateBox('head', { size: 1 }, this.scene); this.head.scaling.set(LINE_W * 1.06, LINE_H + 0.05, LINE_W * 1.06); /* slightly larger than the trail cross-section: no coplanar faces with the run it caps (z-fighting flicker) */ this.head.material = this.headMat; this.head.parent = this.root; this.head.enableEdgesRendering(0.95); this.head.edgesWidth = 5; // same-hue dark edge lines (crisp on GPU, no stencil outline shells)
    this.trail = CreateBox('trail', { size: 1 }, this.scene); this.trail.material = this.trailMat; this.trail.parent = this.root; this.trail.alwaysSelectAsActiveMesh = true;
    this.trailBuf = new Float32Array(16 * 256); this.trail.thinInstanceSetBuffer('matrix', this.trailBuf, 16, false); this.trail.thinInstanceCount = 0;
    this.skin.attach(this.head, this.headMat, this.trailMat, this.root);
    // soft contact halo on the road under the head (outline tint): finds the head in wide/dense frames; steady, never flashes
    this.halo = CreateDisc('halo', { radius: 0.95, tessellation: 40 }, this.scene); this.halo.parent = this.root; this.halo.isPickable = false; this.halo.rotation.x = Math.PI / 2;
    this.haloMat = new StandardMaterial('haloM', this.scene); this.haloMat.diffuseColor.set(0, 0, 0); this.haloMat.specularColor.set(0, 0, 0); this.haloMat.backFaceCulling = false;
    this.haloMat.disableLighting = true; this.haloMat.alpha = 0.32; this.haloMat.zOffset = -4; this.haloMat.disableDepthWrite = true; this.halo.material = this.haloMat;
    const ring = CreateDisc('haloOuter', { radius: 1.45, tessellation: 40 }, this.scene); ring.parent = this.halo; ring.position.z = 0.005; ring.isPickable = false; ring.material = this.haloMat; // two stacked discs = solid core + softer rim
    // scenery
    const grid = new RoadGrid(route, widthAt);
    const expanded: SceneObject[] = [];
    for (const o of L.objects ?? []) {
      if (o.kind === 'row' && o.item && o.t0 !== undefined && o.t1 !== undefined) {
        const v = route.spans[0].v; const step = (o.spacing ?? 1.5) / v;
        for (let t = o.t0; t <= o.t1 + 1e-6; t += step) for (const s of o.bothSides ? [1, -1] : [1]) {
          const side = (o.side ?? 2.5) * s;
          // rows close to the road line the actual road (DL edge rows); far rows follow the mean corridor
          const hug = Math.abs(side) < 5;
          const a = hug ? anchor(route, t, side, 0, o.y ?? 0) : flowAnchor(route, t, side, 0, o.y ?? 0); const sz = o.item.size ?? [1, 1, 1];
          if (grid.hits(a.pos.x, a.pos.z, Math.max(sz[0], sz[2]) / 2 + 0.6, a.pos.y - 3, a.pos.y + sz[1] + 3)) continue;
          expanded.push({ ...o.item, t, side, hug, y: o.y ?? 0, react: o.item.react ?? o.react, appear: o.item.appear ? { ...o.item.appear, t: t + (o.item.appear.t ?? 0) } : o.appear ? { ...o.appear, t: o.appear.t + (t - o.t0) * ((o as any).cascade ?? 0) } : undefined, id: o.id });
        }
      } else expanded.push(o);
    }
    for (const o of expanded) this.addObject(o, o.kind === 'row' ? undefined : grid);
    // roadside dressing (engine-placed props; layout.dressing tunes it, false disables)
    if (L.dressing !== false) {
      const block = this.objects.filter(o => o.br).map(o => ({ x: o.node.position.x + o.bc!.x, z: o.node.position.z + o.bc!.z, r: Math.min(8, o.br! * 0.8) }));
      this.dress = new Dressings(this.scene, this.mats, this.root, route, L.dressing ?? {}, this.env.base, widthAt, (x, z, r, y0, y1) => grid.hits(x, z, r, y0, y1), block);
    }
    if (L.fx) {
      // v2.8 show visuals (src/render/showfx.ts)
      const road = this.road;
      this.show = new ShowFx(this.scene, this.root, route, L, this.quality, widthAt, (x, z, r, y0, y1) => grid.hits(x, z, r, y0, y1),
        road ? { mesh: road.top, buffer: road.topBuffer, centers: Float32Array.from(road.tiles.flatMap(tl => [tl.cx, tl.cz])), setFlush: f => { road.onFlush = f; } } : null, L.fx.sprite ? new Texture(this.mats.artBase + L.fx.sprite, this.scene) : this.sparkTex ? this.sparkTex.clone() as Texture : null);
      this.show.addGlow(this.objects.filter(o => o.def.glowfx).flatMap(o => o.node.getChildMeshes() as Mesh[]));
    }
    if (L.corridor) {
      // v2.9 corridor scenery (src/render/corridor.ts)
      const spr = L.fx?.sprite ? new Texture(this.mats.artBase + L.fx.sprite, this.scene) : this.sparkTex ? this.sparkTex.clone() as Texture : null;
      this.corridor = new Corridor(this.scene, this.root, route, L.corridor, this.mats.artBase, this.quality, widthAt, (x, z, r, y0, y1) => grid.hits(x, z, r, y0, y1), spr, this.beats);
    }
    // objects targeted by 'light' events get their own materials so they can glow independently
    for (const e of this.events) if (e.type === 'light' && e.target) for (const o of this.targets(e.target)) if (!o.lit) {
      o.lit = [];
      for (const m of o.node.getChildMeshes()) { const src = m.material as StandardMaterial | null; if (!src) continue; const c = src.clone(src.name + '_lit') as StandardMaterial; m.material = c; o.lit.push({ mat: c, base: c.emissiveColor.clone() }); }
    }
    // percentage markers (DL style)
    for (let k = 1; k <= 9; k++) {
      const t = level.duration * k / 10;
      for (const side of [-(widthAt(t) / 2 + 2.4), widthAt(t) / 2 + 2.4, -(widthAt(t) / 2 + 4.5), widthAt(t) / 2 + 4.5]) {
        const a = anchor(route, t, side, 0, 0.03);
        if (grid.hits(a.pos.x, a.pos.z, 1.6, a.pos.y - 0.5, a.pos.y + 0.5)) continue;
        const p = textPlane(this.scene, `${k * 10}%`, '#00000055', [3.4, 0, 1.3]);
        p.parent = this.root; p.position.set(a.pos.x, a.pos.y + 0.03, a.pos.z);
        p.rotation.y = Math.atan2(HEAD_VEC[a.heading][0], HEAD_VEC[a.heading][1]) + Math.PI / 2 * Math.sign(side) * 0 ;
        break;
      }
    }
    // diamonds
    const gold = this.mats.get('#ffd54a', { emissive: 0.55 });
    const gemMat = L.collectibleColors?.diamond ? this.mats.get(L.collectibleColors.diamond, { emissive: 0.55 }) : gold;
    const crownMat = L.collectibleColors?.crown ? this.mats.get(L.collectibleColors.crown, { emissive: 0.55 }) : gold;
    L.diamonds.forEach(d => {
      const a = anchor(route, d.t, d.side ?? 0, 0, 1.15);
      const m = CreatePolyhedron('dia', { type: 1, size: 0.32 }, this.scene); m.scaling.y = 1.5; m.material = gemMat; m.parent = this.root; m.position.set(a.pos.x, a.pos.y, a.pos.z);
      this.diamonds.push({ mesh: m, t: d.t, taken: false, base: m.position.clone() });
    });
    // crowns
    L.crowns.forEach(c => {
      const a = anchor(route, c.t, 0, 0, 1.9);
      const n = new TransformNode('crown', this.scene); n.parent = this.root; n.position.set(a.pos.x, a.pos.y, a.pos.z);
      const band = CreateCylinder('cb', { diameter: 1.1, height: 0.38, tessellation: 20 }, this.scene); band.material = crownMat; band.parent = n;
      for (let i = 0; i < 5; i++) { const ang = i / 5 * Math.PI * 2; const sp = CreateCylinder('cs', { diameterTop: 0, diameterBottom: 0.3, height: 0.5, tessellation: 4 }, this.scene); sp.material = crownMat; sp.parent = n; sp.position.set(Math.cos(ang) * 0.48, 0.42, Math.sin(ang) * 0.48); }
      const gem = CreatePolyhedron('cg', { type: 1, size: 0.12 }, this.scene); gem.material = this.mats!.get('#ff5a6e', { emissive: 0.5 }); gem.parent = n; gem.position.set(0, 0.05, -0.56);
      this.crowns.push({ node: n, t: c.t, taken: false, base: n.position.clone() });
    });
    // finish: pyramid + light beam
    const end = posAt(route, level.duration);
    const hEnd = route.spans[route.spans.length - 1].heading; const [ex, ez] = HEAD_VEC[hEnd];
    const fin = new TransformNode('finish', this.scene); fin.parent = this.root; fin.position.set(end.x + ex * 3.2, end.y, end.z + ez * 3.2);
    fin.rotation.y = Math.atan2(ex, ez);
    const fk = L.finish?.kind ?? 'pyramid';
    if (fk === 'custom' && L.finish?.parts) buildKind(this.scene, this.mats, { kind: 'group', parts: L.finish.parts }, fin);
    else if (fk === 'gate') {
      const gc = L.finish?.color ?? pal.road, w = Math.max(3.2, widthAt(level.duration) + 1.6);
      buildKind(this.scene, this.mats, { kind: 'group', parts: [
        { kind: 'box', pos: [-w / 2, 0, 1.5], size: [0.7, 5.2, 0.7], color: gc }, { kind: 'box', pos: [w / 2, 0, 1.5], size: [0.7, 5.2, 0.7], color: gc },
        { kind: 'box', pos: [0, 5.2, 1.5], size: [w + 1.4, 0.7, 0.9], color: gc }, { kind: 'box', pos: [0, -0.3, 3], size: [w + 2.4, 0.3, 5], color: pal.roadSide }] }, fin);
    }
    else buildKind(this.scene, this.mats, { kind: 'pyramid', size: [6, 5, 6], color: L.finish?.color ?? pal.road }, fin);
    const beam = CreateCylinder('beam', { diameter: 2.2, height: 120, tessellation: 16 }, this.scene); beam.parent = fin; beam.position.y = 60;
    const bm = new StandardMaterial('beamM', this.scene); bm.emissiveColor = new Color3(1, 1, 1); bm.disableLighting = true; bm.alpha = 0.18; bm.backFaceCulling = false; beam.material = bm;
    // camera
    this.rig = new CameraRig(this.scene, route, L.camera ?? [], L.sections ?? [], (L.kicks?.length ? L.kicks : L.beats) ?? [], L.autoCamera !== false);
    this.scene.activeCamera = this.rig.cam;
    this.runs = []; this.failRun = null; this.trailCount = 0; this.completeAt = -1;
    this.setupShadows();
    this.seek(game.time);
  }

  private addObject(o: SceneObject, grid?: RoadGrid) {
    if (!this.route || !this.mats || !this.root) return;
    // on-road structures (bridges, decks under the road) without their own cue rise with the road reveal, so a
    // deck that belongs to a later overpass never floats over earlier parts of the route
    if (o.onroad && !o.appear && o.t !== undefined && o.t > 4) {
      const half = Math.max(...(o.size ?? [0, 0, 0]).filter((_, i) => i !== 1), 0) / 2 / (this.route.spans[0]?.v ?? 9);
      o = { ...o, appear: { t: o.t - half - 2.5, mode: 'rise', dur: 0.6 } };
    }
    const t = o.t ?? 0;
    let side = o.side ?? 0;
    const sz = o.size ?? [2, 2, 2];
    const rad = o.radius ?? (o.kind === 'group' ? 1.5 : Math.max(sz[0] ?? 1, sz[2] ?? 1) / 2);
    // v2.7 near-road placement: |side| = half road width + near + own radius (art props hug the actual road edge)
    const hug = o.hug ?? (o.near !== undefined);
    if (o.near !== undefined && !o.worldPos) side = (Math.sign(side) || 1) * ((stepAt(this.level!.layout.road.width, t)?.w ?? 2.2) / 2 + o.near + rad);
    if (grid && side !== 0 && !o.onroad && !o.worldPos && !['water', 'plane', 'disc', 'text', 'cloud', 'moon', 'sun', 'decal'].includes(o.kind) && (o.y ?? 0) < 4) {
      // keep scenery off the road: push outward until clear (scenery can be authored roughly by time)
      for (let k = 0; k < 16; k++) { const p = (hug ? anchor : flowAnchor)(this.route, t, side, o.along ?? 0, o.y ?? 0).pos; if (!grid.hits(p.x, p.z, rad, p.y - 0.5, p.y + (sz[1] ?? 2))) break; side += Math.sign(side) * (hug ? 0.75 : 1.5); }
    } else if (grid && o.kind === 'decal' && side !== 0 && !o.worldPos) {
      // floor decals may touch the road edge but never lie on the road
      const r2 = Math.max(sz[0] ?? 4, sz[2] ?? 4) / 2;
      for (let k = 0; k < 16; k++) { const p = (hug ? anchor : flowAnchor)(this.route, t, side, o.along ?? 0, o.y ?? 0).pos; if (!grid.hits(p.x, p.z, r2 * 0.8, p.y - 0.5, p.y + 0.5)) break; side += Math.sign(side) * 0.75; }
    }
    let pos, baseYaw;
    if (side === 0) { const a = anchor(this.route, t, 0, o.along ?? 0, o.y ?? 0); pos = a.pos; baseYaw = Math.atan2(HEAD_VEC[a.heading][0], HEAD_VEC[a.heading][1]); }
    else if (hug) { const a = anchor(this.route, t, side, o.along ?? 0, o.y ?? 0); pos = a.pos; baseYaw = Math.atan2(HEAD_VEC[a.heading][0], HEAD_VEC[a.heading][1]); }
    else { const a = flowAnchor(this.route, t, side, o.along ?? 0, o.y ?? 0); pos = a.pos; baseYaw = a.yaw; }
    if (o.worldPos) { pos = { x: o.worldPos[0], y: o.worldPos[1] ?? 0, z: o.worldPos[2] ?? 0 }; baseYaw = 0; }
    const holder = new TransformNode(o.id ?? 'obj', this.scene); holder.parent = this.root;
    holder.position.set(pos.x, pos.y, pos.z);
    // v2.7 face: point the object's front (local -z) at the road / the oncoming line; 'camera' is updated per frame
    if (o.face && o.face !== 'camera') {
      const a = anchor(this.route, t, 0, 0, 0); const [hx, hz] = HEAD_VEC[a.heading];
      let fx = a.pos.x - pos.x, fz = a.pos.z - pos.z; const d = Math.hypot(fx, fz);
      if (d < 0.3) { fx = -hz * Math.sign(side || 1); fz = hx * Math.sign(side || 1); } else { fx /= d; fz /= d; }
      if (o.face === 'oncoming') { fx = fx * 0.5 - hx * 0.866; fz = fz * 0.5 - hz * 0.866; }
      else if (o.face === 'travel') { fx = hx; fz = hz; }
      baseYaw = Math.atan2(-fx, -fz);
    }
    const rotY = baseYaw + (typeof o.rot === 'number' ? o.rot : Array.isArray(o.rot) ? o.rot[1] ?? 0 : 0) * Math.PI / 180;
    holder.rotation.y = rotY;
    if (Array.isArray(o.rot)) { holder.rotation.x = (o.rot[0] ?? 0) * Math.PI / 180; holder.rotation.z = (o.rot[2] ?? 0) * Math.PI / 180; }
    buildKind(this.scene, this.mats, o, holder);
    for (const m of holder.getChildMeshes()) { m.isPickable = false; m.doNotSyncBoundingInfo = true; }
    holder.computeWorldMatrix(true); const bv = holder.getHierarchyBoundingVectors(true);
    const bc = bv.min.add(bv.max).scale(0.5).subtract(holder.position), br = bv.max.subtract(bv.min).length() / 2;
    const obj: Obj = { node: holder, def: o, t, base: holder.position.clone(), baseScale: new Vector3(1, 1, 1), baseRotY: rotY, hidden: false, id: o.id, bc, br: Number.isFinite(br) ? br : 0, fade: 1 };
    if (ART_KINDS.has(o.kind) && Number.isFinite(br)) {
      // art props test occlusion against their projected box (a bounding sphere would fade a tall thin card far too eagerly)
      const P0 = holder.position; let x0 = bv.min.x - P0.x, x1 = bv.max.x - P0.x, z0 = bv.min.z - P0.z, z1 = bv.max.z - P0.z;
      if (o.face === 'camera') { const r = Math.max(-x0, x1, -z0, z1, bv.max.y - P0.y); x0 = z0 = -r; x1 = z1 = r; }
      obj.box = [x0, bv.min.y - P0.y, z0, x1, bv.max.y - P0.y, z1];
    }
    this.objects.push(obj); if (o.face === 'camera') this.faceCam.push(obj);
    if (o.id) { const l = this.byId.get(o.id) ?? []; l.push(obj); this.byId.set(o.id, l); }
  }

  private targets(id?: string): Obj[] {
    if (!id) return [];
    if (id.endsWith('*')) { const p = id.slice(0, -1); return this.objects.filter(o => o.id?.startsWith(p)); }
    return this.byId.get(id) ?? [];
  }

  /** Restore every time-dependent visual to time t (restart, checkpoint, rewind). */
  seek(t: number) {
    if (!this.game || !this.route) return;
    this.road?.seek(t); this.dress?.seek(t);
    this.failRun = null; this.runs = []; this.trailCount = 0; this.updateTrail(t, true);
    for (const d of this.diamonds) { d.taken = this.game.diamondsTaken.has(this.diamonds.indexOf(d)); d.mesh.setEnabled(!d.taken); d.mesh.scaling.set(1, 1.5, 1); d.mesh.position.copyFrom(d.base); }
    for (const c of this.crowns) { c.taken = c.t <= t + 1e-6; c.node.setEnabled(true); c.node.position.copyFrom(c.base); this.ghostCrown(c.node, c.taken); }
    for (const f of this.fx) f.mesh.dispose(); this.fx = [];
    this.failAnim?.pieces.forEach(p => p.mesh.dispose()); this.failAnim = null;
    this.head?.setEnabled(true); this.skin.reset();
    if (this.rig) { this.rig.freezeAt = null; this.rig.extraPitch = 0; this.rig.extraDist = 0; this.rig.snap(); }
    this.lastTime = t; this.completeAt = -1;
    this.applyTime(t, 0, true);
  }

  private ghostCrown(n: TransformNode, ghost: boolean) {
    for (const m of n.getChildMeshes()) m.visibility = ghost ? 0.25 : 1;
  }

  private v3(p: { x: number; y: number; z: number }) { return new Vector3(p.x, p.y + LINE_H / 2, p.z); }

  /** Trail = the centreline actually travelled, as straight axis-aligned runs (one box per run, grown in place).
   *  Runs come from the route spans up to min(t, pending corner); past a pending corner the last run extends to the
   *  head. Airborne spans draw nothing, so a jump/fall starts a new run on landing. */
  private updateTrail(t: number, full = false) {
    const g = this.game!, route = this.route!;
    const tc = Math.min(t, pendingCorner(route, g.turns, t, g.cursor));
    const runs: Run[] = [];
    for (const sp of route.spans) {
      if (sp.t0 >= tc) break;
      if (sp.air) continue;
      const a = this.v3(spanPos(sp, sp.t0)), b = this.v3(spanPos(sp, Math.min(sp.t1, tc)));
      const len = (Math.min(sp.t1, tc) - sp.t0) * sp.v; const slope = len > 1e-6 ? (b.y - a.y) / len : 0;
      const last = runs[runs.length - 1];
      if (last && last.h === sp.heading && Math.abs(last.slope - slope) < 1e-6 && Vector3.DistanceSquared(last.b, a) < 1e-6) last.b = b;
      else runs.push({ a, b, h: sp.heading, slope });
    }
    if (t > tc && runs.length) { const last = runs[runs.length - 1]; const [dx, dz] = HEAD_VEC[last.h as Heading]; const v = route.spans[spanIndexAt(route, tc - 1e-6)].v; last.b = last.b.add(new Vector3(dx * v * (t - tc), 0, dz * v * (t - tc))); }
    if (this.failRun) runs.push(this.failRun);
    // rewrite only runs that changed (normally just the last one)
    let first = full ? 0 : Math.min(this.runs.length, runs.length);
    for (let i = Math.min(this.runs.length, runs.length) - 1; i >= 0 && !full; i--) {
      const o = this.runs[i], n = runs[i];
      if (o.h === n.h && Vector3.DistanceSquared(o.a, n.a) < 1e-10 && Vector3.DistanceSquared(o.b, n.b) < 1e-10) break;
      first = i;
    }
    if (runs.length * 16 > this.trailBuf.length) {
      let n = this.trailBuf.length; while (runs.length * 16 > n) n *= 2;
      const nb = new Float32Array(n); nb.set(this.trailBuf); this.trailBuf = nb; this.trail!.thinInstanceSetBuffer('matrix', this.trailBuf, 16, false);
    }
    for (let i = first; i < runs.length; i++) this.writeRun(i, runs[i]);
    const changed = first < runs.length || runs.length !== this.trailCount;
    this.runs = runs; this.trailCount = runs.length;
    if (changed && this.trail) { this.trail.thinInstanceCount = this.trailCount; this.trail.thinInstanceBufferUpdated('matrix'); this.trail.thinInstanceRefreshBoundingInfo(false); }
  }

  private writeRun(i: number, r: Run) {
    const d = r.b.subtract(r.a); const len = d.length();
    const yaw = [0, Math.PI / 2, Math.PI, -Math.PI / 2][r.h];          // exact multiples of 90 degrees
    const pitch = len > 1e-6 ? -Math.asin(Math.max(-1, Math.min(1, d.y / len))) : 0;
    const m = Matrix.Compose(new Vector3(LINE_W, LINE_H, len + LINE_W), Quaternion.RotationYawPitchRoll(yaw, pitch, 0), r.a.add(r.b).scale(0.5));
    m.copyToArray(this.trailBuf, i * 16);
  }

  // ---- events from the game ----
  onTurn(t: number) {
    this.lastTap = t;
    if (!this.head || !this.glowTex) return;
    const m = CreatePlane('glow', { size: 1 }, this.scene);
    const mat = new StandardMaterial('glowM', this.scene); mat.diffuseTexture = this.glowTex; mat.opacityTexture = this.glowTex; mat.emissiveColor = this.skin.glowColor.clone(); mat.disableLighting = true; mat.alphaMode = Engine.ALPHA_ADD;
    m.material = mat; m.billboardMode = Mesh.BILLBOARDMODE_ALL; m.position.copyFrom(this.head.position); m.parent = this.root;
    this.fx.push({ mesh: m, t0: t, dur: 0.32, kind: 'glow' });
    this.skin.onTurn(this.head.position, t);
  }
  onDiamond(i: number, t: number) {
    const d = this.diamonds[i]; if (!d || d.taken) return; d.taken = true;
    this.fx.push({ mesh: d.mesh, t0: t, dur: 0.45, kind: 'collect', from: d.mesh.position.clone() });
    this.burst(d.mesh.position, '#ffe27a', 18);
  }
  onCrown(i: number, t: number) {
    const c = this.crowns[i]; if (!c || c.taken) return; c.taken = true;
    this.burst(c.node.position, '#ffd54a', 30);
    const ring = CreateCylinder('ring', { diameter: 1, height: 0.05, tessellation: 48 }, this.scene);
    const rm = new StandardMaterial('ringM', this.scene); rm.emissiveColor = hex('#ffe9a8'); rm.disableLighting = true; rm.alpha = 0.6; ring.material = rm;
    ring.position.copyFrom(c.base); ring.position.y -= 1.8; ring.parent = this.root;
    this.fx.push({ mesh: ring, t0: t, dur: 0.9, kind: 'ring' });
    this.fx.push({ mesh: c.node as unknown as Mesh, t0: t, dur: 0.8, kind: 'crown', from: c.base.clone() });
  }
  private burst(at: Vector3, color: string, n: number) {
    if (!this.sparkTex) return;
    const ps = new ParticleSystem('burst', n, this.scene);
    ps.particleTexture = this.sparkTex; ps.emitter = at.clone();
    const c = hex(color); ps.color1 = new Color4(c.r, c.g, c.b, 1); ps.color2 = new Color4(1, 1, 1, 1); ps.colorDead = new Color4(c.r, c.g, c.b, 0);
    ps.minSize = 0.12; ps.maxSize = 0.35; ps.minLifeTime = 0.25; ps.maxLifeTime = 0.6; ps.manualEmitCount = n; ps.minEmitPower = 2; ps.maxEmitPower = 5;
    ps.direction1 = new Vector3(-1, 1.5, -1); ps.direction2 = new Vector3(1, 2.5, 1); ps.gravity = new Vector3(0, -6, 0); ps.blendMode = ParticleSystem.BLENDMODE_ADD;
    ps.disposeOnStop = true; ps.targetStopDuration = 0.7; ps.start();
  }

  onFail(t: number, kind: string) {
    if (!this.head || !this.route || !this.game) return;
    const h: Heading = lineHeading(this.route, this.game.turns, t);
    let heading = h;
    if (kind === 'early' || kind === 'extra') { const dir = this.route.dirs[this.game.cursor] ?? 'R'; heading = ((h + (dir === 'R' ? 1 : 3)) % 4) as Heading; }
    const [dx, dz] = HEAD_VEC[heading];
    const pos = this.head.position.clone();
    this.failAnim = { t0: performance.now() / 1000, pos, dir: new Vector3(dx, 0, dz), pieces: [] };
    if (this.rig) { this.rig.freezeAt = pos.clone(); this.rig.shakeBoost = 0.5; }
  }

  private shatter(at: Vector3) {
    if (!this.failAnim || !this.head) return;
    this.head.setEnabled(false);
    const now = performance.now() / 1000;
    this.skin.onShatter(at);
    for (let i = 0, n = this.skin.shardCount; i < n; i++) {
      const m = CreateBox('shard', { size: 0.32 + Math.random() * 0.2 }, this.scene); m.material = this.headMat; m.parent = this.root; m.position.copyFrom(at);
      this.failAnim.pieces.push({ mesh: m, t0: now, dur: 1.6, kind: 'shard', vel: new Vector3((Math.random() - 0.5) * 7, 3 + Math.random() * 5, (Math.random() - 0.5) * 7), spin: new Vector3(Math.random() * 8, Math.random() * 8, Math.random() * 8) });
    }
  }

  // ---- per frame ----
  frame(t: number) {
    const now = performance.now(); const dt = Math.min(0.1, (now - this.lastFrame) / 1000); this.lastFrame = now;
    this.fpsAcc += dt; this.fpsN++; if (this.fpsAcc > 0.5) { this.fps = this.fpsN / this.fpsAcc; this.fpsAcc = 0; this.fpsN = 0; }
    // Babylon ages particles by updateSpeed per frame; tie it to real frame time so lifetimes are in seconds
    // on any frame rate (the line skin does the same for its own systems)
    const us = Math.min(0.1, Math.max(0.001, dt));
    for (const ps of this.scene.particleSystems) if (ps.name === 'burst' || ps.name === 'amb') (ps as ParticleSystem).updateSpeed = us;
    this.applyTime(t, dt, false);
    this.scene.render();
  }

  private applyTime(t: number, dt: number, seeking: boolean) {
    const g = this.game, route = this.route; if (!g || !route || !this.head || !this.env || !this.rig) return;
    const aspect = this.engine.getRenderWidth() / Math.max(1, this.engine.getRenderHeight()); this.rig.aspect = aspect;
    // environment
    const pal: Palette = this.env.at(t);
    this.applyPalette(pal);
    if (this.show) { const lb = this.lastBefore(this.beats, t); this.show.update(t, Math.exp(-(t - lb) * 9), p => this.burst(p, '#fff4c2', 40), this.head.position); }
    if (this.corridor && this.scene.activeCamera) { const lb = this.lastBefore(this.beats, t); this.corridor.update(t, Math.exp(-(t - lb) * 9), this.scene.activeCamera.position); }
    if (this.groundTex.length > 1 && this.groundMat) { let g = this.groundTex[0].tex; for (const x of this.groundTex) if (x.t <= t) g = x.tex; if (g !== this.groundShown) { this.groundShown = g; this.groundMat.diffuseTexture = g; } }
    if (this.backdrops.length) { let b: string | null = null; for (const x of this.backdrops) if (x.t <= t) b = x.src; if (b !== this.backdropShown) { this.backdropShown = b; this.onBackdrop?.(b ? this.mats!.artBase + b : null); } }
    // road reveal
    this.road?.update(t);
    // line
    const failed = g.status === 'failed';
    const lt = failed ? g.failTime : t;
    const lp = this.v3(linePos(route, g.turns, lt, g.cursor));
    if (!failed) {
      this.head.position.copyFrom(lp);
      if (!seeking && (g.status === 'playing' || g.status === 'complete')) {
        this.updateTrail(t);
      }
    } else if (this.failAnim) {
      const k = performance.now() / 1000 - this.failAnim.t0;
      const slide = Math.min(k, 0.22);
      const p = this.failAnim.pos.add(this.failAnim.dir.scale(9 * (slide - slide * slide / 0.44 * 0.5)));
      if (k < 0.22) {
        this.head.position.copyFrom(p);
        const hd = [[0, 1], [1, 0], [0, -1], [-1, 0]].findIndex(([x, z]) => Math.abs(x - this.failAnim!.dir.x) < 1e-6 && Math.abs(z - this.failAnim!.dir.z) < 1e-6);
        this.failRun = { a: this.failAnim.pos.clone(), b: p.clone(), h: Math.max(0, hd), slope: 0 }; this.updateTrail(g.failTime);
      }
      else if (this.head.isEnabled()) this.shatter(this.head.position.clone());
      for (const s of this.failAnim.pieces) {
        const e = performance.now() / 1000 - s.t0; s.vel!.y -= 22 * dt; s.mesh.position.addInPlace(s.vel!.scale(dt));
        s.mesh.rotation.addInPlace(s.spin!.scale(dt)); const f = Math.max(0, 1 - e / s.dur); s.mesh.scaling.setAll(f);
      }
    }
    // line colour
    this.skin.update(lt, pal.line, lineHeading(route, g.turns, lt), true);
    // readability outline around the head: dark rim on light heads, light rim on dark heads (works with every skin)
    if (this.head && this.headMat) { const c = this.headMat.diffuseColor; const lum = 0.3 * c.r + 0.59 * c.g + 0.11 * c.b;
      // dark rim of the same hue on light heads (classic pink -> deep rose, never white); light rim only on genuinely dark heads
      if (lum > 0.3) this.headEdge.set(c.r * 0.35, c.g * 0.35, c.b * 0.35); else this.headEdge.set(Math.min(1, c.r * 0.5 + 0.5), Math.min(1, c.g * 0.5 + 0.5), Math.min(1, c.b * 0.5 + 0.5));
      this.head.edgesColor.set(this.headEdge.r, this.headEdge.g, this.headEdge.b, 1); }
    if (this.halo && this.head && this.haloMat) { this.halo.position.set(this.head.position.x, this.head.position.y - this.head.scaling.y / 2 + 0.04, this.head.position.z);
      this.halo.setEnabled(this.head.isEnabled() && g.status !== 'failed'); this.haloMat.emissiveColor.copyFrom(this.headEdge);
      if (this.rig) { const d = this.rig.cam.position.subtract(this.head.getAbsolutePosition()).length(); this.halo.scaling.setAll(Math.min(1.8, Math.max(1, d / 40))); } } // grows a little on wide shots so the head stays findable
    // complete: line enters finish, camera rises
    if (g.status === 'complete') { if (this.completeAt < 0) this.completeAt = performance.now() / 1000; const k = smooth((performance.now() / 1000 - this.completeAt) / 2.2); this.rig.extraPitch = 18 * k; this.rig.extraDist = 14 * k; }
    // camera
    this.rig.menuOrbit = this.mode === 'menu'; this.rig.distScale = (this as any).__camScale ?? 1;
    this.rig.update(this.mode === 'menu' ? 0 : lt, failed ? this.head.position : lp, dt || 1 / 60);
    // shadow frustum follows the camera, snapped to whole shadow-map texels in light space (no shimmering edges)
    { const tg = this.rig.cam.getTarget(); const d = this.sun.direction.normalizeToNew(); const r = Vector3.Cross(Vector3.Up(), d).normalize(); const u = Vector3.Cross(d, r);
      const tex = 52 / 1024; const a = Math.round(Vector3.Dot(tg, r) / tex) * tex, b = Math.round(Vector3.Dot(tg, u) / tex) * tex, c = Vector3.Dot(tg, d);
      this.sun.position = r.scale(a).add(u.scale(b)).add(d.scale(c)).add(new Vector3(30, 60, -20)); }
    // collectibles
    const tt = performance.now() / 1000;
    for (const d of this.diamonds) if (!d.taken) { d.mesh.rotation.y = tt * 2.2; d.mesh.position.y = d.base.y + Math.sin(tt * 3 + d.t) * 0.12; }
    for (const c of this.crowns) if (!c.taken) { c.node.rotation.y = tt * 1.5; c.node.position.y = c.base.y + Math.sin(tt * 2) * 0.15; }
    // scenery animation
    this.animateObjects(t);
    this.fadeOccluders(t, dt);
    this.runEvents(t);
    // fx
    for (let i = this.fx.length - 1; i >= 0; i--) {
      const f = this.fx[i]; const k = (t - f.t0) / f.dur;
      if (k >= 1 || k < -0.05) { if (f.kind === 'crown') { (f.mesh as unknown as TransformNode).position.copyFrom(f.from!); this.ghostCrown(f.mesh as unknown as TransformNode, true); (f.mesh as unknown as TransformNode).scaling.setAll(1); } else if (f.kind === 'collect') f.mesh.setEnabled(false); else f.mesh.dispose(); this.fx.splice(i, 1); continue; }
      if (f.kind === 'glow') { f.mesh.scaling.setAll(1.2 + k * 2.6); (f.mesh.material as StandardMaterial).alpha = 0.55 * (1 - k); }
      if (f.kind === 'collect') { f.mesh.position.y = f.from!.y + k * 1.6; f.mesh.scaling.setAll((1 - k) * 1.4); }
      if (f.kind === 'ring') { f.mesh.scaling.set(1 + k * 9, 1, 1 + k * 9); (f.mesh.material as StandardMaterial).alpha = 0.6 * (1 - k); }
      if (f.kind === 'crown') { const n = f.mesh as unknown as TransformNode; n.position.y = f.from!.y + smooth(k) * 3; n.scaling.setAll(1 + k * 0.8); n.rotation.y += dt * 10; }
    }
    // particles
    { const ov = this.particleOverride(t); const want = ov === undefined ? pal.particles : ov; if (want !== this.particleKind) this.setParticles(want); }
    if (this.particles) (this.particles.emitter as Vector3).copyFrom(this.rig.cam.getTarget().add(new Vector3(0, 10, 0)));
    if (this.ground && this.groundMat) { if (pal.groundY !== null && pal.groundY !== undefined) this.ground.position.y = pal.groundY + this.minRoadY(lt); this.ground.position.x = this.rig.cam.getTarget().x; this.ground.position.z = this.rig.cam.getTarget().z; }
    this.lastTime = t;
  }

  private applyPalette(p: Palette) {
    const fog = hex(p.fog);
    this.scene.fogColor = fog; this.scene.fogStart = p.fogStart * 1.5; this.scene.fogEnd = p.fogEnd * 1.6;
    this.hemi.diffuse = hex(p.light); this.hemi.groundColor = hex(p.ambient).scale(0.6); this.hemi.intensity = 0.62;
    this.sun.diffuse = hex(p.light); this.sun.intensity = 0.5 * p.lightIntensity;
    if (this.groundMat) { const g = this.groundTint ?? hex(p.ground); this.groundMat.diffuseColor = g; this.groundMat.emissiveColor = g.scale(this.groundTint ? 0.18 : 0.08); }
    this.onSky?.(p.skyTop, p.skyBottom);
  }

  private setParticles(kind: string | null) {
    this.particles?.dispose(); this.particles = null; this.particleKind = kind;
    if (!kind || !this.rig) return;
    const square = kind === 'pixels' || kind === 'confetti';
    const ps = new ParticleSystem('amb', this.quality === 'high' ? 400 : 150, this.scene);
    ps.particleTexture = square ? radialTexture(this.scene, 'sq', 'rgba(255,255,255,1)', 'rgba(255,255,255,0)', true) : this.sparkTex!.clone() as Texture;
    ps.emitter = this.rig.cam.getTarget().clone();
    ps.minEmitBox = new Vector3(-30, -2, -30); ps.maxEmitBox = new Vector3(30, 4, 30);
    const cfg: Record<string, { c1: string; c2: string; size: [number, number]; grav: number; rate: number; life: [number, number]; dir: [number, number] }> = {
      snow: { c1: '#ffffff', c2: '#e8f2ff', size: [0.15, 0.4], grav: -1.2, rate: 80, life: [5, 9], dir: [-0.4, -1] },
      petals: { c1: '#ffc4d8', c2: '#fff0f4', size: [0.2, 0.45], grav: -0.8, rate: 50, life: [5, 9], dir: [-1, -0.5] },
      leaves: { c1: '#f2a541', c2: '#d9693a', size: [0.25, 0.5], grav: -1, rate: 40, life: [5, 9], dir: [-1.5, -0.6] },
      bubbles: { c1: '#ccf6ff', c2: '#ffffff', size: [0.2, 0.7], grav: 1.2, rate: 40, life: [4, 8], dir: [0, 0.6] },
      stars: { c1: '#fff7c2', c2: '#bfe3ff', size: [0.1, 0.3], grav: 0, rate: 60, life: [2, 5], dir: [0, 0.05] },
      dust: { c1: '#fff3d6', c2: '#ffffff', size: [0.06, 0.18], grav: 0.1, rate: 60, life: [4, 8], dir: [0.2, 0.1] },
      rain: { c1: '#b7c8e6', c2: '#dfe8f7', size: [0.05, 0.12], grav: -20, rate: 200, life: [0.6, 1.2], dir: [0, -8] },
      confetti: { c1: '#ff7aa8', c2: '#7ad7ff', size: [0.15, 0.3], grav: -2, rate: 70, life: [3, 6], dir: [0.4, -0.5] },
      pixels: { c1: '#9fd3ff', c2: '#ffb7e0', size: [0.2, 0.45], grav: 0.6, rate: 50, life: [3, 6], dir: [0, 0.4] },
    };
    const c = cfg[kind] ?? cfg.dust;
    const c1 = hex(c.c1), c2 = hex(c.c2);
    ps.color1 = new Color4(c1.r, c1.g, c1.b, 0.95); ps.color2 = new Color4(c2.r, c2.g, c2.b, 0.85); ps.colorDead = new Color4(c2.r, c2.g, c2.b, 0);
    ps.minSize = c.size[0]; ps.maxSize = c.size[1]; ps.minLifeTime = c.life[0]; ps.maxLifeTime = c.life[1];
    ps.emitRate = this.quality === 'high' ? c.rate : c.rate / 2.5; ps.gravity = new Vector3(0, c.grav, 0);
    ps.direction1 = new Vector3(c.dir[0], c.dir[1], -0.3); ps.direction2 = new Vector3(c.dir[0] * 0.3, c.dir[1] * 0.5, 0.3);
    ps.minEmitPower = 0.5; ps.maxEmitPower = 1.5; ps.minAngularSpeed = -2; ps.maxAngularSpeed = 2;
    ps.blendMode = kind === 'stars' || kind === 'bubbles' ? ParticleSystem.BLENDMODE_ADD : ParticleSystem.BLENDMODE_STANDARD;
    ps.preWarmCycles = 60; ps.start();
    this.particles = ps;
  }

  /** lowest road height reached up to t: the ground follows falls but stays put while the road climbs */
  private minRoadY(t: number) { let m = 0; for (const s of this.route!.spans) { if (s.t0 > t) break; if (!s.air) m = Math.min(m, s.y0, s.t1 <= t ? s.y1 : s.y0); } return m; }

  private lastBefore(list: number[], t: number) { let lo = 0, hi = list.length - 1, r = -1e9; while (lo <= hi) { const m = (lo + hi) >> 1; if (list[m] <= t) { r = list[m]; lo = m + 1; } else hi = m - 1; } return r; }

  /** Scenery between the camera and the line (or the next ~1.2 s of road) fades out so the road always reads. */
  /** Keep the line head and the road just ahead readable: any scenery whose projected bounding sphere overlaps a
   *  protected screen region around those points, and that is nearer to the camera than the point, fades out
   *  (cutaway). Screen-space so it also catches objects that are not exactly on the camera->head ray. */
  private fadeOccluders(t: number, dt: number) {
    if (!this.rig || !this.head || !this.route) return;
    const camN = this.rig.cam; const cam = camN.position;
    const view = camN.getViewMatrix(); const eng = this.scene.getEngine();
    const aspect = eng.getRenderWidth() / Math.max(1, eng.getRenderHeight());
    const th = Math.tan(camN.fov / 2);
    const dur = this.level!.duration;
    // protected points: head (bigger radius), road ahead at 0.5/1.0/1.6 s (smaller)
    const pts: [Vector3, number][] = [[this.head.position, 0.2]];
    for (const dtA of [0.5, 1.0, 1.6, 2.4, 3.2]) pts.push([this.v3(posAt(this.route, Math.min(dur, t + dtA))), dtA > 2 ? 0.06 : 0.12]);
    const P = pts.map(([p, r]) => { const v = Vector3.TransformCoordinates(p, view); return { x: v.x / (v.z * th * aspect), y: v.y / (v.z * th), z: v.z, r }; });
    this.occP = P; this.occView = view; this.occTh = th; this.occAspect = aspect;
    if (this.dress) {
      const lb = this.lastBefore(this.beats, t); const beatK = Math.exp(-(t - lb) * 9);
      const tmp = new Vector3();
      this.dress.update(t, dt, beatK, (x, y, z, r, h) => {
        tmp.set(x, y + h / 2, z); const v = Vector3.TransformCoordinates(tmp, view);
        const br = Math.hypot(r, h / 2);
        if (v.z - br < 5) return true; // never let a prop sit right in front of the lens
        const sx = v.x / (v.z * th * aspect), sy = v.y / (v.z * th), sr = br / (v.z * th);
        for (const q of P) { if (v.z - br * 0.5 >= q.z) continue; if (Math.hypot((sx - q.x) * aspect, sy - q.y) < sr * 0.85 + q.r) return true; }
        return false;
      });
    }
    const k = Math.min(1, dt * 10);
    for (const o of this.objects) {
      if (o.hidden || !o.br || o.def.kind === 'text' || o.def.kind === 'decal' || o.def.onroad) { if (o.fade !== 1 && !o.hidden) this.setFade(o, 1); continue; }
      let occ = false;
      if (o.box) {
        // projected screen rectangle of the art prop's box; fades when it covers the head (and, unless a landmark, the road just ahead)
        const b = o.box, n = o.node.position; let x0 = 9, x1 = -9, y0 = 9, y1 = -9, zmin = 1e9, behind = false;
        for (let i = 0; i < 8; i++) {
          Vector3.TransformCoordinatesFromFloatsToRef(n.x + b[i & 1 ? 3 : 0], n.y + b[i & 2 ? 4 : 1], n.z + b[i & 4 ? 5 : 2], view, _cv);
          if (_cv.z < 0.5) { behind = true; break; }
          const sx = _cv.x / (_cv.z * th * aspect), sy = _cv.y / (_cv.z * th);
          if (sx < x0) x0 = sx; if (sx > x1) x1 = sx; if (sy < y0) y0 = sy; if (sy > y1) y1 = sy; if (_cv.z < zmin) zmin = _cv.z;
        }
        if (behind) occ = true;
        else for (let qi = 0; qi < (o.def.landmark ? 1 : P.length); qi++) {
          const q = P[qi]; if (zmin >= q.z) continue; const m = q.r * 0.5;
          if (q.x > x0 - m / aspect && q.x < x1 + m / aspect && q.y > y0 - m && q.y < y1 + m) { occ = true; break; }
        }
        const want = occ ? 0.12 : 1; const f = o.fade! + (want - o.fade!) * k;
        if (Math.abs(f - o.fade!) > 0.003 || (want === 1 && o.fade !== 1 && Math.abs(f - 1) < 0.01)) this.setFade(o, Math.abs(f - 1) < 0.01 ? 1 : f);
        continue;
      }
      const c = o.node.position.add(o.bc!); const v = Vector3.TransformCoordinates(c, view);
      if (v.z > 0.5) {
        const sx = v.x / (v.z * th * aspect), sy = v.y / (v.z * th), sr = o.br! / (v.z * th);
        const lm = !!o.def.landmark;
        // anything big and close to the lens (a large chunk of the screen, in front of the line) gives way too,
        // landmarks included: they are meant to be seen from a distance, not to wall off the view
        if (v.z - o.br! * 0.5 < P[0].z && v.z < P[0].z * 0.75 && sr > 0.28) occ = true;
        for (const q of P) {                                         // landmarks give way only with a tighter footprint (below)
          if (occ) break;
          if (v.z - o.br! * 0.5 >= q.z) continue;                 // object is behind the protected point
          const dx = (sx - q.x) * aspect, dy = sy - q.y;           // compare in height-normalised units
          if (Math.hypot(dx, dy) < (lm ? sr * 0.6 + 0.04 : sr * 0.85 + q.r)) { occ = true; break; }
        }
      } else if (Vector3.Distance(c, cam) < o.br! + 1) occ = true; // camera inside/next to the object
      const want = occ ? 0.12 : 1; const f = o.fade! + (want - o.fade!) * k;
      if (Math.abs(f - o.fade!) > 0.003 || (want === 1 && o.fade !== 1 && Math.abs(f - 1) < 0.01)) this.setFade(o, Math.abs(f - 1) < 0.01 ? 1 : f);
    }
  }
  private setFade(o: Obj, f: number) { o.fade = f; for (const m of o.node.getChildMeshes()) m.visibility = f; }

  private animateObjects(t: number) {
    if (this.faceCam.length && this.rig) {
      const c = this.rig.cam.position;
      // yaw toward the camera and lean back toward it (pivot at the base, max ~63 deg) so the art reads from the high follow camera
      for (const o of this.faceCam) if (!o.hidden) {
        const dx = c.x - o.base.x, dz = c.z - o.base.z, dy = c.y - (o.base.y + o.bc!.y);
        o.node.rotation.y = Math.atan2(-dx, -dz); o.node.rotation.x = Math.min(1.1, Math.max(0, Math.atan2(dy, Math.hypot(dx, dz))));
      }
    }
    const lb = this.lastBefore(this.beats, t), lk = this.lastBefore(this.kicks, t);
    const beatK = Math.exp(-(t - lb) * 9), kickK = Math.exp(-(t - lk) * 10), tapK = Math.exp(-(t - this.lastTap) * 10);
    for (const o of this.objects) {
      const near = Math.abs(o.t - t) < 70 || o.def.landmark;
      if (!near) { if (!o.hidden) { o.node.setEnabled(false); o.hidden = true; } continue; }
      let sx = 1, sy = 1, sz = 1, dy = 0, alpha = 1, rx = 0;
      const ap = o.def.appear, ex = o.def.exit;
      if (ap) {
        const k = (t - ap.t) / (ap.dur ?? 0.7); const e = k <= 0 ? 0 : k >= 1 ? 1 : 1 - Math.pow(1 - k, 3);
        if (k <= 0) alpha = 0;
        else if (k < 1) switch (ap.mode) {
          case 'rise': dy -= (1 - e) * 12; break;
          case 'drop': dy += (1 - e) * 16; break;
          case 'pop': case 'grow': { const s = k < 1 ? e * (1 + 0.25 * Math.sin(k * Math.PI)) : 1; sx = sy = sz = s; break; }
          case 'unfold': rx = (1 - e) * Math.PI / 2; break;
          case 'fade': sx = sy = sz = e; break;
        }
      }
      if (ex) {
        const k = (t - ex.t) / (ex.dur ?? 0.7); const e = k <= 0 ? 0 : k >= 1 ? 1 : k * k;
        if (k >= 1) alpha = 0;
        else if (k > 0) switch (ex.mode) {
          case 'sink': dy -= e * 12; break;
          case 'fall': dy -= e * 20; rx += e * 0.6; break;
          case 'shrink': case 'fade': sx *= 1 - e; sy *= 1 - e; sz *= 1 - e; break;
        }
      }
      const r = o.def.react;
      if (r === 'tap') { dy -= tapK * 0.35; sy *= 1 - tapK * 0.08; }
      else if (r === 'beat') { const s = 1 + beatK * 0.07; sx *= s; sy *= s; sz *= s; }
      else if (r === 'kick') { const s = 1 + kickK * 0.1; sx *= s; sy *= s; sz *= s; }
      const vis = alpha > 0;
      if (vis === o.hidden) { o.node.setEnabled(vis); o.hidden = !vis; }
      if (!vis) continue;
      o.node.position.set(o.base.x, o.base.y + dy, o.base.z);
      o.node.scaling.set(sx * o.baseScale.x, sy * o.baseScale.y, sz * o.baseScale.z);
      if (o.def.appear?.mode === 'unfold') o.node.rotation.x = rx;
    }
  }

  /** particle kind forced by a 'particles' event active at t (undefined = use palette) */
  private particleOverride(t: number): string | null | undefined {
    let r: string | null | undefined;
    for (const e of this.events) { if (e.t > t) break; if (e.type !== 'particles') continue; const u = e.until as number | undefined; r = u === undefined || t < u ? ((e.particles as string | null) ?? null) : undefined; }
    return r;
  }

  private runEvents(t: number) {
    for (const o of this.objects) if (o.lit) o.glow = 0;
    for (const e of this.events) {
      if (e.t > t) break;
      const until = (e.until as number | undefined) ?? (e.t + (e.dur ?? 0.6));
      const persistent = e.type === 'raise' || e.type === 'lower' || e.type === 'light';
      if (!persistent && t > until + 1.5) continue;
      const tg = this.targets(e.target);
      switch (e.type) {
        case 'pulse': {
          const every = (e.every as number) || 0.5; if (t > until) break;
          const ph = ((t - e.t) % every) / every; const k = Math.exp(-ph * every * 9) * 0.12;
          for (const o of tg) if (!o.hidden) o.node.scaling.scaleInPlace(1 + k);
          break;
        }
        case 'raise': case 'lower': {
          // persistent move; optional 'converge' (0..1) drifts the targets toward their common centre
          const d0 = (e.dy as number) ?? 4;
          const k = smooth((t - e.t) / (e.dur ?? 1)); const dy = (e.type === 'lower' && d0 > 0 ? -d0 : d0) * k;
          const cv = ((e.converge as number) ?? 0) * k;
          let cx = 0, cz = 0; if (cv && tg.length) { for (const o of tg) { cx += o.base.x; cz += o.base.z; } cx /= tg.length; cz /= tg.length; }
          for (const o of tg) { o.node.position.y += dy; if (cv) { o.node.position.x += (cx - o.base.x) * cv; o.node.position.z += (cz - o.base.z) * cv; } }
          break;
        }
        case 'spin': { const k = (t - e.t); if (t <= until) for (const o of tg) o.node.rotation.y = o.baseRotY + k * ((e.speed as number) ?? 1.5); break; }
        case 'shake': if (t <= until && this.rig) this.rig.shakeBoost = Math.max(this.rig.shakeBoost, (e.amount as number) ?? 0.3); break;
        case 'flash': if (t - e.t < 0.05) document.documentElement.style.setProperty('--flash', String((e.amount as number) ?? 0.35)); break;
        case 'burst': if (t - e.t < 1 / 30 && t >= e.t) { const at = e.at === 'player' || !tg.length ? this.head!.position : tg[0].node.position; this.burst(at, (e.color as string) ?? '#ffffff', (e.amount as number) ?? 30); } break;
        case 'light': {
          if (!tg.length) { const k = smooth((t - e.t) / (e.dur ?? 1)); if (t <= until) this.sun.intensity *= 1 + (((e.amount as number) ?? 1.5) - 1) * k; break; }
          // targeted: objects glow (one after another when 'every' is set); stays on unless an explicit 'until' is given
          const off = e.until !== undefined && t > (e.until as number);
          const level = (e.level as number) ?? 1; const col = hex((e.color as string) ?? '#fff1c2');
          tg.forEach((o, i) => { const t0 = e.t + i * ((e.every as number) ?? 0); const k = off ? 0 : smooth((t - t0) / ((e.dur as number) ?? 0.5)); if (k > 0 && o.lit) { o.glow = level * k; o.glowColor = col; } });
          break;
        }
      }
    }
    for (const o of this.objects) if (o.lit) { const g = o.glow ?? 0; for (const l of o.lit) l.mat.emissiveColor.copyFrom(g > 0 && o.glowColor ? Color3.Lerp(l.base, o.glowColor, Math.min(1, g * 0.85)) : l.base); }
  }

  resize() { this.engine.resize(); }
  dispose() { this.unload(); this.skin.dispose(); this.scene.dispose(); this.engine.dispose(); }
  stats() { return { meshes: this.scene.meshes.length, active: this.scene.getActiveMeshes().length, fps: this.fps, trail: this.trailCount, tiles: this.road?.tiles.length ?? 0, objects: this.objects.length, drawCalls: (this.engine as any)._drawCalls?.current ?? null }; }
}
