/**
 * Concept C runtime ("兔子立体童话书"): streams the placement (place.ts) around the line head.
 *  - ground cover: one merged static mesh per 20 m chunk (props + the chunk's paper page), built when the chunk enters the window
 *  - mid / sky / anim props: one thin-instance mesh per asset type, refilled when the chunk window moves; pop-up spring, bob, beat pulse
 *  - set pieces / landmarks: pop-up-book hinge spring at popAt (the drop for drop pieces), named-pivot beat hooks
 *    (heart/pulse, ears, gate/lid hinge, flag wave, tower pop, bob, spin, wheel, swing, clock hand), LOD = one merged mesh beyond the LOD distance
 *  - one unlit vertex-colour material for everything (lighting baked into vertex colours), no realtime shadows
 */
import type { Scene } from '@babylonjs/core/scene';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { VertexBuffer } from '@babylonjs/core/Buffers/buffer';
import type { Camera } from '@babylonjs/core/Cameras/camera';
import { CreatePlane } from '@babylonjs/core/Meshes/Builders/planeBuilder';
import { TransformNode } from '@babylonjs/core/Meshes/transformNode';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { Color3 } from '@babylonjs/core/Maths/math.color';
import { DynamicTexture } from '@babylonjs/core/Materials/Textures/dynamicTexture';
import { Constants } from '@babylonjs/core/Engines/constants';
import { Quaternion, Vector3 } from '@babylonjs/core/Maths/math.vector';
import { anchor, flowAnchor, type Route } from '../../core/path';
import type { SceneCSpec } from '../../core/types';
import { activeRange, place, type CChunk, type CInst, type CPlacement, type CSet } from './place';
import { loadModel, placeholders, type Template } from './assets';
import { CUT, Cutaway } from './cutaway';
import { Backdrop, Impostors, PageFade } from './paint';
import { ColorCurves } from '@babylonjs/core/Materials/colorCurves';
import { Color4 } from '@babylonjs/core/Maths/math.color';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { Material } from '@babylonjs/core/Materials/material';
import { variantCols, STRETCH, nVariants } from './variants';

export type Tier = 'high' | 'low';
export const TIERS: Record<Tier, { density: Record<string, number>; ahead: number; behind: number; lod: number }> = {
  high: { density: { ground: 1, mid: 1, sky: 1, anim: 1 }, ahead: 8, behind: 3, lod: 35 },
  low: { density: { ground: 0.5, mid: 0.7, sky: 0.6, anim: 0 }, ahead: 6, behind: 2, lod: 22 },
};
const hash = (x: number, z: number) => { const s = Math.sin(x * 12.9898 + z * 78.233) * 43758.5453; return s - Math.floor(s); };
/** lamp-like decor: glow head height (fraction of the piece's height) and halo radius (m per unit scale) -- night zones only */
const LAMP: Record<string, [number, number]> = { 'firefly-lamp': [0.85, 0.7], 'lily-lamp': [0.55, 0.9], 'lantern-string': [0.75, 0.8], 'lantern-tower': [0.75, 2.2],
  'star-chime': [0.8, 0.7], 'iv-heart': [0.8, 0.5], 'spiral-tower': [0.85, 2.0], 'stall': [0.6, 1.4], 'mushroom-house': [0.4, 1.2], 'bunny-house': [0.4, 1.2], 'book-stack': [0.9, 0.5], 'heart-sculpt': [0.6, 0.8],
  'pine': [0.55, 0.9], 'pine-lo': [0.55, 0.9], 'tree': [0.6, 0.9], 'tree-lo': [0.6, 0.9], 'tree-bush-lo': [0.6, 0.8], 'mushroom-group': [0.6, 0.5], 'flower-heart': [1.2, 0.55] };   // night trees: fairy-light glow
/** hero window glow: lit windows on the road-facing (+z) side, count per set piece; castle / wheel / carousel glow in every zone, the rest at night */
const WIN: Record<string, number> = { castle: 9, 'ferris-wheel': 8, carousel: 6, 'clock-tower': 4, windmill: 3, 'lantern-tower': 4, 'phone-tower': 5, 'spiral-tower': 5, 'tall-tower': 5,
  pavilion: 4, stall: 2, 'bunny-house': 3, 'mushroom-house': 2, 'heart-gate': 4, 'page-wall': 3, 'reading-bunny': 2, 'book-cover': 3 };
/** v6: palette fixes on loaded models: greenish (mint) vertex colours remapped by a channel ratio (keeps the shading) */
const RECOL: Record<string, [number, number, number]> = { 'book-cover': [0xF6 / 0xBD, 0xB8 / 0xEB, 0xCB / 0xD8] };   // mint #BDEBD8 -> sheet pink #F6B8CB
function recolor(id: string, t: { col?: ArrayLike<number> & { [i: number]: number }; container?: { meshes: any[] } | null }) {
  const k = RECOL[id]; if (!k) return;
  const fix = (c: { [i: number]: number; length: number }) => { for (let i = 0; i + 2 < c.length; i += 4) { const r = c[i], g = c[i + 1], b = c[i + 2]; if (g > r + 0.04 && g >= b) { c[i] = Math.min(1, r * k[0]); c[i + 1] = g * k[1]; c[i + 2] = Math.min(1, b * k[2]); } } };
  if (t.col) fix(t.col as any);
  for (const m of t.container?.meshes ?? []) { const d = m.getVerticesData?.(VertexBuffer.ColorKind); if (d) { fix(d); m.setVerticesData(VertexBuffer.ColorKind, d, false, 4); } }
}
const WIN_ALWAYS = new Set(['castle', 'ferris-wheel', 'carousel']);
/** v6: impostor sprites that get a lit window / lamp glow at night (glow height as a fraction of the card height) */
const IMPLIT: Record<string, number> = { 'mushroom-house': 0.38, 'bunny-house': 0.4, 'lantern-tower': 0.72, 'firefly-lamp': 0.85, 'lily-lamp': 0.6, 'spiral-tower': 0.6, castle: 0.45, 'star-chime': 0.8, stall: 0.5, carousel: 0.45, 'ferris-wheel': 0.5, 'clock-tower': 0.6 };
type ChunkM = { g: Mesh; m: Mesh | null; glow: Mesh | null; t0: number; tris: number; y: number; L: { pos: number[]; col: number[]; uv: number[]; idx: number[] } | null };
const spring = (x: number) => x <= 0 ? 0 : 1 - Math.exp(-x * 7) * Math.cos(x * 13);
const hexRGB = (h: string) => { const n = parseInt(h.replace('#', ''), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; };

interface TI { id: string; mesh: Mesh; mats: Float32Array; cols: Float32Array; cap: number; items: CInst[]; tris: number }
interface Piv { node: TransformNode; kind: string; i: number; base: Quaternion | null; baseS: Vector3; baseP: Vector3 }
interface SetE { def: CSet; node: TransformNode; hinge: TransformNode; far: Mesh | null; near: TransformNode | null; nearMeshes: Mesh[]; piv: Piv[]; tris: number; on: boolean; lodFar: boolean }

export interface CStats { chunks: [number, number]; chunkMeshes: number; types: number; instances: number; sets: number; tris: number; zone: number; models: number; /** visible tris if every asset were modelled at its full spec budget */ trisAtBudget: number; /** tris of everything in the chunk window (incl. off-screen chunks); `tris` counts only frustum-visible chunks / sets */ trisWindow?: number }

export class SceneC {
  readonly plc: CPlacement; readonly spec: SceneCSpec;
  private tm: Map<string, Template>; private mat: StandardMaterial; private matSet: StandardMaterial; private root: TransformNode;
  private types = new Map<string, TI>(); private chunkMesh = new Map<number, ChunkM>(); private night: boolean[] = []; private matNight!: StandardMaterial; private matGlow!: StandardMaterial; private dirtyAt = -1; private glowAll: Mesh | null = null; private glowSig = ''; private pages: Mesh[] = []; private stackGeo: { p: number[]; c: number[]; i: number[] }[] = []; private bankGeo: { p: number[]; c: number[]; i: number[] }[] = []; private stacks: Mesh | null = null; private stackSig = ''; private pageMats: StandardMaterial[] = []; private sets: SetE[] = [];
  private range: [number, number] = [-1, -1]; private tier: Tier; private zoneCols: number[][][];
  private imp: Impostors | null = null; private back: Backdrop | null = null; private groundTex = new Map<number, Texture>(); private base = './'; curZone = 0;  private route!: Route;
  private hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean; private pop = 5; private disposed = false; private time = 0; models = 0; last: CStats | null = null;

  constructor(private scene: Scene, parent: TransformNode, route: Route, spec: SceneCSpec, o: { duration: number; widthAt: (t: number) => number; roadH: number; hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean; beats: number[]; base: string; tier: Tier }) {
    this.spec = spec; this.tier = o.tier; this.base = o.base; this.route = route; this.hits = o.hits;
    this.root = new TransformNode('scenec', scene); this.root.parent = parent;
    this.plc = place(spec, route, { duration: o.duration, widthAt: o.widthAt, roadH: o.roadH, hits: o.hits, beats: o.beats, density: spec.density });
    this.zoneCols = spec.zones.map(z => z.colors.map(hexRGB));
    this.tm = placeholders(spec);
    const m = new StandardMaterial('paperC', scene);
    // unlit: emissive x vertex colour x instance colour; double-sided (paper cards)
    m.disableLighting = true; m.diffuseColor = Color3.Black(); m.emissiveColor = Color3.White(); m.specularColor = Color3.Black(); m.backFaceCulling = false;
    this.mat = m;
    // set pieces / landmarks skip fog so hero creams and pinks stay clean in the dark zones (like the key renders)
    this.matSet = m.clone('paperCSet'); this.matSet.fogEnabled = false;
    this.buildPages();
    // night zones: decor skips fog and gets a colour lift so it reads on navy; lamps get additive halos (no realtime lights)
    this.night = spec.zones.map(z => { const g = hexRGB(z.palette.ground ?? '#eeeeee'); return 0.299 * g[0] + 0.587 * g[1] + 0.114 * g[2] < 0.45; });
    this.matNight = m.clone('paperCNight'); this.matNight.fogEnabled = false;
    const tex = new DynamicTexture('cglow', 64, scene, true); const ctx = tex.getContext() as CanvasRenderingContext2D;
    const gr = ctx.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,236,170,1)'); gr.addColorStop(0.35, 'rgba(255,214,120,0.55)'); gr.addColorStop(1, 'rgba(255,190,90,0)');
    ctx.fillStyle = gr; ctx.fillRect(0, 0, 64, 64); tex.update(); tex.hasAlpha = true;
    const gm = new StandardMaterial('paperCGlow', scene); gm.disableLighting = true; gm.diffuseTexture = tex; gm.useAlphaFromDiffuseTexture = true; gm.diffuseColor = Color3.Black();
    gm.emissiveColor = Color3.White(); gm.specularColor = Color3.Black(); gm.alphaMode = Constants.ALPHA_ADD; gm.disableDepthWrite = true; gm.backFaceCulling = false; gm.fogEnabled = false;
    this.matGlow = gm;
    this.applyLook();
    this.imp = new Impostors(scene, this.root, this.plc.chunks, spec, o.base, this.night, o.tier === 'low' ? 0.18 : 1); this.back = new Backdrop(scene, this.root, spec, o.base);
    for (const mm of [this.mat, this.matSet, this.matNight, this.matGlow]) new Cutaway(mm);   // after the page clones: pages / road are never cut
    { const seen = new Map<string, number>(); for (const s of this.plc.sets) { const k = s.zone + ':' + s.a, n = seen.get(k) ?? 0; seen.set(k, n + 1); if (s.v === undefined) s.v = n; this.sets.push(this.makeSet(s)); } }   // v8: repeated set pieces step through palette variants
    // swap in built models as they load (placeholders until then; a missing model simply keeps its placeholder)
    for (const [id, a] of Object.entries(spec.assets)) if (a.model) loadModel(scene, o.base, id, a.h, typeof a.model === 'string' ? a.model : id).then(t => { if (this.disposed) { t.container?.dispose(); return; } recolor(id, t); this.tm.set(id, t); this.models++; this.refreshAsset(id); }).catch(e => console.warn('omg-c model', id, e));
  }

  private dropChunk(c: ChunkM) { c.g.dispose(); c.m?.dispose(); c.glow?.dispose(); }
  private rebuildGlow(t: number) {
    const on = [...this.chunkMesh.entries()].filter(([, c]) => c.L && t > c.t0 - this.pop + 0.2).map(([i]) => i);
    const sOn = this.sets.filter(e => e.on && t > e.def.popAt + 0.5 && WIN[e.def.a] && (this.night[e.def.zone] || WIN_ALWAYS.has(e.def.a)));
    const sig = on.join(',') + '|' + sOn.map(e => this.sets.indexOf(e)).join(',') + '|' + this.range.join(':') + this.tier;
    if (sig === this.glowSig) return; this.glowSig = sig; this.glowAll?.dispose(); this.glowAll = null; if (!on.length && !sOn.length) return;
    const pos: number[] = [], col: number[] = [], uv: number[] = [], idx: number[] = [];
    for (const i of on) { const c = this.chunkMesh.get(i)!, L = c.L!, i0 = pos.length / 3;
      for (let k = 0; k < L.pos.length; k += 3) pos.push(L.pos[k], L.pos[k + 1] + c.y, L.pos[k + 2]);
      col.push(...L.col); uv.push(...L.uv); for (const x of L.idx) idx.push(x + i0); }
    for (const e of sOn) {   // windows: small warm quads on a grid over the front face + one soft halo; quads in the piece's local xy plane
      const d = e.def, A = this.spec.assets[d.a], H = A?.h ?? 6, W = (A?.w ?? H * 0.6), D = (A?.d ?? W * 0.8), n = WIN[d.a], cs = Math.cos(d.yaw), sn = Math.sin(d.yaw), sc = d.s;
      const P = (lx: number, ly: number, lz: number) => [d.x + (lx * cs + lz * sn) * sc, d.y + ly * sc, d.z + (-lx * sn + lz * cs) * sc];
      const q = (cx: number, cy: number, cz: number, r: number, k: number) => { const i0 = pos.length / 3;
        for (const [dx, dy] of [[-r, -r], [r, -r], [r, r], [-r, r]]) pos.push(...P(cx + dx, cy + dy, cz));
        uv.push(0, 0, 1, 0, 1, 1, 0, 1); for (let m = 0; m < 4; m++) col.push(k, k * 0.9, k * 0.7, 1); idx.push(i0, i0 + 1, i0 + 2, i0, i0 + 2, i0 + 3); };
      const cols = Math.ceil(Math.sqrt(n)), rows = Math.ceil(n / cols), z = D * 0.52 + 0.05;
      for (let k = 0; k < n; k++) { const cx = cols > 1 ? (-0.3 + 0.6 * (k % cols) / (cols - 1)) * W : 0, cy = (0.28 + 0.45 * (rows > 1 ? Math.floor(k / cols) / (rows - 1) : 0.5)) * H;
        q(cx, cy, z, Math.max(0.35, H * 0.05), 0.75); }
      q(0, H * 0.5, z + 0.2, H * 0.42, this.night[d.zone] ? 0.22 : 0.12);
    }
    if (this.tier === 'high' && this.range[0] >= 0) {   // v6: lit windows on night impostor cards (houses / towers / lamps) in the distance
      const N = this.plc.chunks.length;
      for (let i = this.range[0]; i <= Math.min(N - 1, this.range[1] + 3); i++) for (const im of this.plc.chunks[i].imp ?? []) {
        if (!this.night[im.zone]) continue; const lk = IMPLIT[im.k]; if (!lk) continue;
        const H = Math.min(11, (this.spec.assets[im.k]?.h ?? 3) * im.s), ux = Math.cos(im.yaw), uz = -Math.sin(im.yaw), fx = Math.sin(im.yaw) * 0.4, fz = Math.cos(im.yaw) * 0.4;
        const q = (cy: number, r: number, k: number) => { const i0 = pos.length / 3;
          for (const [dx, dy] of [[-r, -r], [r, -r], [r, r], [-r, r]]) pos.push(im.x + ux * dx + fx, im.y + cy + dy, im.z + uz * dx + fz);
          uv.push(0, 0, 1, 0, 1, 1, 0, 1); for (let m = 0; m < 4; m++) col.push(k, k * 0.88, k * 0.62, 1); idx.push(i0, i0 + 1, i0 + 2, i0, i0 + 2, i0 + 3); };
        q(H * lk, Math.max(0.3, H * 0.09), 0.7); q(H * lk, H * 0.32, 0.14);
      }
    }
    if (this.tier === 'high') {   // cheap bloom: every halo quad gets a 2.3x larger, faint copy (same mesh, no post pass)
      const nq = idx.length / 6;
      for (let q = 0; q < nq; q++) { const v0 = idx[q * 6]; if (col[v0 * 4] < 0.15) continue;   /* v6: soft halos (glowing flowers, impostor windows) skip the bloom copy: overdraw */ let cx = 0, cy = 0, cz = 0; for (let k = 0; k < 4; k++) { cx += pos[(v0 + k) * 3] / 4; cy += pos[(v0 + k) * 3 + 1] / 4; cz += pos[(v0 + k) * 3 + 2] / 4; }
        const j0 = pos.length / 3;
        for (let k = 0; k < 4; k++) { const b = (v0 + k) * 3; pos.push(cx + (pos[b] - cx) * 2.3, cy + (pos[b + 1] - cy) * 2.3, cz + (pos[b + 2] - cz) * 2.3); uv.push(uv[(v0 + k) * 2], uv[(v0 + k) * 2 + 1]);
          const c = (v0 + k) * 4; col.push(col[c] * 0.2, col[c + 1] * 0.2, col[c + 2] * 0.2, 1); }
        idx.push(j0, j0 + 1, j0 + 2, j0, j0 + 2, j0 + 3); }
    }
    const m = new Mesh('cglow', this.scene); const vd = new VertexData(); vd.positions = pos; vd.colors = col; vd.uvs = uv; vd.indices = idx; vd.applyToMesh(m, false);
    m.material = this.matGlow; m.isPickable = false; m.parent = this.root; this.glowAll = m;
  }
  // ---- v7 night sky strip: a camera-parented band over the top ~30% of the screen (moon, stars, silhouette skyline; tools/omgc/sky_strip.py),
  // drawn after the scene (rendering group 1), faded in and out with the night zones. The key camera's pitch shows almost no real sky.
  private sky: Mesh | null = null; private skyMat: StandardMaterial | null = null; private skyV = 0; private skyD = 70; skyT = 0; private skyKind = ''; private skyTex = new Map<string, Texture>();
  /** v8: one band, texture per zone kind (night / day / dusk / twilight); a kind change fades out, swaps, fades back in */
  updateSky(cam: Camera, aspect: number, dt: number) {
    const Z = this.spec.zones[this.curZone], kind = Z?.sky ?? (this.night[this.curZone] ? 'night' : '');
    const want = kind && kind === this.skyKind ? 1 : 0, k = dt > 0 ? 1 - Math.exp(-dt * 1.6) : 1;
    this.skyV += (want - this.skyV) * k;
    if (kind && kind !== this.skyKind && this.skyV < 0.03) {   // swap the texture while invisible
      this.skyKind = kind; let tx = this.skyTex.get(kind);
      if (!tx) { tx = new Texture(this.base + `models/omg-c/paint/sky-${kind}.webp`, this.scene, true, true); tx.hasAlpha = true; this.skyTex.set(kind, tx); }
      if (!this.sky) {
        const m = CreatePlane('csky', { size: 1 }, this.scene); const mat = new StandardMaterial('cskyMat', this.scene);
        mat.useAlphaFromDiffuseTexture = true; mat.disableLighting = true; mat.emissiveColor = new Color3(1, 1, 1); mat.diffuseColor = new Color3(0, 0, 0);
        mat.backFaceCulling = false; mat.fogEnabled = false; mat.disableDepthWrite = true; mat.transparencyMode = Material.MATERIAL_ALPHABLEND;
        m.material = mat; m.isPickable = false; m.alphaIndex = -10; m.parent = cam; this.sky = m; this.skyMat = mat;   // in the main group, depth-tested 70 m out: the far carpet hides behind it, tall heroes / houses nearer than that stand in front of the sky
      }
      this.skyMat!.diffuseTexture = tx;
    }
    if (!this.sky) return;
    const on = this.skyV > 0.01; this.sky.setEnabled(on); if (!on) return;
    // v8b: band depth follows the far road - 70 m by default, pushed back past any road point (next 8 s) that would fall inside the band,
    // so with the head-pinned shallower camera the band never eats the far road at the top of a night frame
    const th = Math.tan((cam.fov || 0.8) / 2), V = cam.getViewMatrix(); let far = 70;
    for (let k = 0; k <= 32; k++) { const p = anchor(this.route, this.skyT + k * 0.25).pos; const v = Vector3.TransformCoordinates(new Vector3(p.x, p.y, p.z), V);
      if (v.z > 1 && Math.abs(v.x) < v.z * th * aspect * 1.05 && v.y > v.z * th * 0.35) far = Math.max(far, v.z + 6); }
    this.skyD += (Math.min(260, far) - this.skyD) * (this.skyD < far ? 1 : k * 0.5);
    const d = this.skyD, hh = d * th, hw = hh * aspect, bh = hh * 2 * 0.3;   // band = top 30% of the view
    this.sky.scaling.set(hw * 2, bh, 1); this.sky.position.set(0, hh - bh / 2, d);
    const tx = this.skyMat!.diffuseTexture as Texture, us = Math.min(1, (hw * 2 / bh) / (1024 / 384)); tx.uScale = us; tx.uOffset = 1 - us;   // keep proportions, crop toward the moon / sun side
    this.skyMat!.alpha = this.skyV;
  }
  private dropChunks() { for (const c of this.chunkMesh.values()) this.dropChunk(c); this.chunkMesh.clear(); this.range = [-1, -1]; }
  setTier(t: Tier) { if (t === this.tier) return; this.tier = t; this.dropChunks(); this.applyLook(); this.glowSig = ''; this.imp?.setDensity(t === 'low' ? 0.18 : 1); }
  /** high tier: warm key tint + soft vignette (in-shader image processing, no pass); bloom = soft outer halo copies in the glow mesh (rebuildGlow) */
  private applyLook() {
    const ip = this.scene.imageProcessingConfiguration, hi = this.tier === 'high';
    ip.vignetteEnabled = hi; ip.colorCurvesEnabled = hi;
    if (hi) {
      ip.vignetteWeight = 1.25; ip.vignetteStretch = 0.6; ip.vignetteColor = new Color4(0.32, 0.18, 0.3, 0); ip.vignetteCameraFov = 0.7;
      const cc = new ColorCurves(); cc.globalHue = 38; cc.globalDensity = 14; cc.globalSaturation = 12; cc.highlightsHue = 45; cc.highlightsDensity = 18; cc.shadowsHue = 300; cc.shadowsDensity = 10; ip.colorCurves = cc;
    }
  }

  /** QA (tools/qa/repcount.mjs): the palette variant an item actually renders with */
  variantOf(it: CInst) { const n = nVariants(it.a); return n < 2 ? 0 : (it.v ?? Math.floor(hash(it.x * 3.1, it.z * 1.7) * 9973)) % n; }
  private keep(it: CInst) { if (it.hi && this.tier === 'low') return false; const lm = this.tier === 'low' ? this.spec.zones[it.zone]?.lowMul ?? 1 : 1; return hash(it.x, it.z) < (TIERS[this.tier].density[it.layer] ?? 1) * lm; }   // v9: per-zone low-tier thinning (z08 carnival)
  private colOf(it: CInst, model: boolean) { const c = this.zoneCols[it.zone][it.c] ?? [1, 1, 1]; const k = model ? 0.12 : 0.85; return [1 + (c[0] - 1) * k, 1 + (c[1] - 1) * k, 1 + (c[2] - 1) * k]; }
  private yOf(it: CInst) { return it.y; }   // ground / mid / land: the page or terrace level chosen at placement

  private meshFrom(name: string, t: Template) {
    const m = new Mesh(name, this.scene); const vd = new VertexData(); vd.positions = t.pos; vd.colors = t.col; vd.indices = t.idx; vd.applyToMesh(m, true);
    m.material = this.mat; m.isPickable = false; m.parent = this.root; return m;
  }

  // ---- zone pages: one static mesh per zone (the union of its chunks' padded page quads, terraced with the route's falls).
  // Neighbouring zones overlap by the pad; a per-zone polygon offset gives a fixed order (later zone on top) instead of the
  // interleaved staircase the per-chunk quads produced. Only the zones touching the chunk window are enabled.
  /** painted ground tile of a zone (shared by its page and the base ground under everything) */
  groundTexOf(zi: number) {
    let t = this.groundTex.get(zi); const f = this.spec.zones[zi]?.ground; if (t || !f) return t ?? null;
    t = new Texture(this.base + f, this.scene, false, true, Texture.TRILINEAR_SAMPLINGMODE); t.anisotropicFilteringLevel = 4; t.level = this.spec.zones[zi]?.nightLevel ?? 1;   /* v6: night carpets brightened */ this.groundTex.set(zi, t); return t;
  }
  tileOf(zi: number) { return this.spec.zones[zi]?.tile ?? 25; }
  private buildPages() {
    const pg = this.spec.pagePad ?? 28, Z = this.spec.zones.length;
    const RS: number[][] = []; for (const c of this.plc.chunks) for (let k = 0; k < 6; k++) { const p = anchor(this.route, c.t0 + (c.t1 - c.t0) * k / 6).pos; RS.push([p.x, p.z, c.zone]); }   // road samples by zone
    const ownZ = (zi: number, x: number, z: number) => { let dO = 1e9, dX = 1e9; for (const r of RS) { const d = (r[0] - x) ** 2 + (r[1] - z) ** 2; if (r[2] === zi) { if (d < dO) dO = d; } else if (d < dX) dX = d; }
      return Math.min(1, Math.max(0, (Math.sqrt(dX) - Math.sqrt(dO)) / 16 + 0.5)); };
    const R: { x0: number; z0: number; x1: number; z1: number; y: number; ci: number; zi: number }[] = [];
    for (let zi = 0; zi < Z; zi++) {
      const Zs = this.spec.zones[zi], tex = this.groundTexOf(zi), tile = Zs.tile ?? 25;
      const pos: number[] = [], col: number[] = [], idx: number[] = [], uv: number[] = []; const gc = tex ? [1, 1, 1] : hexRGB(Zs.palette.ground ?? '#eeeeee');
      // each page rect is a 4x4 grid: the outer ring has alpha 0 (dithered fade over F m), so overlapping zones / terraces blend
      // each page rect is a 7x7 grid; alpha = rim fade (F m) x zone ownership: a point belongs to the zone whose road is nearest,
      // blended over ~16 m, so the next zone's page never covers this zone's road area (and vice versa)
      const own = (x: number, z: number) => ownZ(zi, x, z);
      let ci = 0;
      const rect = (x0: number, z0: number, x1: number, z1: number, y: number) => {
        const N = 7, i0 = pos.length / 3; R.push({ x0, z0, x1, z1, y, ci, zi });
        for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { const x = x0 + (x1 - x0) * i / (N - 1), z = z0 + (z1 - z0) * j / (N - 1);
          const rim = 1;   // v5: hard page edges, finished by the page-stack mesh (buildStacks) instead of a dithered rim fade
          pos.push(x, y, z); uv.push(x / tile, z / tile); col.push(gc[0], gc[1], gc[2], rim * own(x, z)); }
        for (let j = 0; j < N - 1; j++) for (let i = 0; i < N - 1; i++) { const q = i0 + j * N + i; idx.push(q, q + N, q + N + 1, q, q + N + 1, q + 1); }
      };
      for (const c of this.plc.chunks) {
        if (c.zone !== zi) continue; ci = c.i; const y = c.y - 0.004 * (c.i % 3);
        rect(c.minX - pg, c.minZ - pg, c.maxX + pg, c.maxZ + pg, y);
        if (c.terr) { const p = c.terr.pad; rect(c.minX - p, c.minZ - p, c.maxX + p, c.maxZ + p, c.terr.y - 0.004 * (c.i % 3)); }   // raised page (climb)
      }
      for (const B of this.plc.banks) { if (B.zone !== zi) continue;   // v10 raised page banks: their tops are this zone's page (same texture / draw)
        for (let k = 0; k < B.P.length - 1; k++) { const p = B.P[k], q = B.P[k + 1], i0 = pos.length / 3;
          for (const v of [[p[0], p[1]], [q[0], q[1]], [q[2], q[3]], [p[2], p[3]]]) { pos.push(v[0], B.y, v[1]); uv.push(v[0] / tile, v[1] / tile); col.push(gc[0], gc[1], gc[2], 1); }
          idx.push(i0, i0 + 1, i0 + 2, i0, i0 + 2, i0 + 3); } }
      const m = new Mesh(`cpage_z${zi}`, this.scene);
      if (pos.length) { const vd = new VertexData(); vd.positions = pos; vd.colors = col; vd.uvs = uv; vd.indices = idx; vd.applyToMesh(m, false); m.hasVertexAlpha = true; }   /* vColor.a only reaches the shader with VERTEXALPHA; the material is pinned opaque */
      const mat = this.mat.clone(`paperCPage${zi}`); mat.zOffset = 2 * (Z - 1 - zi); this.pageMats.push(mat);   // positive = pushed back; the latest zone has 0
      mat.transparencyMode = Material.MATERIAL_OPAQUE; if (tex) mat.diffuseTexture = tex; new PageFade(mat);
      m.material = mat; m.isPickable = false; m.parent = this.root; m.freezeWorldMatrix(); m.setEnabled(false); (m as any).__tris = idx.length / 3;
      this.pages.push(m);
    }
    this.buildStacks(R, ownZ);
  }

  // ---- v5 page-stack edges + paper cliffs: every page edge that is not covered by another page at the same height or above gets
  // three stepped cream page layers with gold ledges (the open-book edge), then three paper strata down toward the ground below.
  // Geometry is precomputed per chunk as long runs (~24 tris each) and merged for the chunk window into one mesh (1 draw, high tier).
  private buildStacks(R: { x0: number; z0: number; x1: number; z1: number; y: number; ci: number; zi: number }[], ownZ: (zi: number, x: number, z: number) => number) {
    const N = this.plc.chunks.length; for (let i = 0; i < N; i++) this.stackGeo.push({ p: [], c: [], i: [] });
    // v8b: page-stack cliffs in lilac / blush paper (cream + gold read as a road branch beside the real road)
    const CREAM = [0.96, 0.94, 0.99], CREAM2 = [0.9, 0.87, 0.96], GOLD = [0.93, 0.6, 0.74], GOLD2 = [0.98, 0.74, 0.84], TAN = [0.86, 0.8, 0.94], TAN2 = [0.76, 0.69, 0.88];
    const covered = (r: typeof R[0], x: number, z: number) => { let lo = -1e9; for (const q of R) { if (q === r || x <= q.x0 || x >= q.x1 || z <= q.z0 || z >= q.z1) continue; if (q.y >= r.y - 0.05) return null; lo = Math.max(lo, q.y); } return lo; };
    const DAYC = [CREAM, CREAM2, GOLD, GOLD2, TAN, TAN2];   // night zones: paper in moonlight (dimmer, slightly blue) so the cliffs don't glare on the navy carpet
    const NIGHTC = DAYC.map(c => [c[0] * 0.62, c[1] * 0.62, c[2] * 0.72]);
    const NT = this.spec.zones.map(z => { const g = hexRGB(z.palette.ground ?? '#eeeeee'); return 0.299 * g[0] + 0.587 * g[1] + 0.114 * g[2] < 0.45; });
    const ST = 3;
    for (const r of R) {
      const G = this.stackGeo[r.ci];
      // edges: [ax, az, bx, bz, nx, nz]
      const E = [[r.x0, r.z0, r.x1, r.z0, 0, -1], [r.x1, r.z0, r.x1, r.z1, 1, 0], [r.x1, r.z1, r.x0, r.z1, 0, 1], [r.x0, r.z1, r.x0, r.z0, -1, 0]];
      for (const [ax, az, bx, bz, nx, nz] of E) {
        const L = Math.hypot(bx - ax, bz - az), n = Math.max(1, Math.round(L / ST)), dx = (bx - ax) / L, dz = (bz - az) / L;
        let run0 = -1, runLo = 0;
        const flush = (k1: number) => {
          if (run0 < 0) return; const e0 = run0 === 0 ? -1.8 : run0 * L / n, e1 = k1 === n ? L + 1.8 : k1 * L / n;
          this.emitStack(G, ax + dx * e0, az + dz * e0, ax + dx * e1, az + dz * e1, nx, nz, r.y, Math.max(runLo, r.y - 14), NT[r.zi] ? NIGHTC : DAYC); run0 = -1; };
        for (let k = 0; k < n; k++) {
          const s = (k + 0.5) * L / n, x = ax + dx * s, z = az + dz * s, lo = covered(r, x + nx * 0.6, z + nz * 0.6);
          const ok = lo !== null && ownZ(r.zi, x - nx * 1.5, z - nz * 1.5) > 0.45 && r.y - lo > 0.3 && !this.hits(x + nx * 1.2, z + nz * 1.2, 1.6, lo - 1, r.y + 2);   // v8: no page edge across a road
          const loQ = lo === null ? 0 : Math.round(Math.max(lo, r.y - 14));
          if (ok && run0 >= 0 && loQ !== runLo) flush(k);
          if (ok && run0 < 0) { run0 = k; runLo = loQ; } else if (!ok) flush(k);
        }
        flush(n);
      }
    }
    // v10 page banks: every edge gets the page-layer + strata cliff (inner edges face the road); both tiers (bankGeo)
    for (let i = 0; i < N; i++) this.bankGeo.push({ p: [], c: [], i: [] });
    const sat = (h: string) => { const c = hexRGB(h); return Math.max(...c) - Math.min(...c); };
    const COV = this.spec.zones.map(z => { const k = [...z.colors].sort((a, b) => sat(b) - sat(a))[0] ?? '#F29BB8'; return hexRGB(k); });
    for (const B of this.plc.banks) {
      const night = NT[B.zone], n = B.P.length, lo = Math.max(B.base, B.y - 14) - 0.05, cov = COV[B.zone].map(v => v * (night ? 0.8 : 0.92));
      for (let k = 0; k < n - 1; k++) { const p = B.P[k], q = B.P[k + 1], G = this.bankGeo[B.ci[k]];
        let ox = p[2] - p[0], oz = p[3] - p[1]; const ol = Math.hypot(ox, oz) || 1; ox /= ol; oz /= ol;
        this.emitBank(G, p[0], p[1], q[0], q[1], -ox, -oz, B.y, lo, cov, night, true);   // inner edge (toward the road): full page block
        this.emitBank(G, p[2], p[3], q[2], q[3], ox, oz, B.y, lo, cov, night, false); }   // outer edge
      for (const [k, k2] of [[0, 1], [n - 1, n - 2]]) { const p = B.P[k], q = B.P[k2]; let fx = (p[0] + p[2] - q[0] - q[2]) / 2, fz = (p[1] + p[3] - q[1] - q[3]) / 2; const fl = Math.hypot(fx, fz) || 1;
        this.emitBank(this.bankGeo[B.ci[k]], p[0], p[1], p[2], p[3], fx / fl, fz / fl, B.y, lo, cov, night, true); }   // run ends
    }
    this.buildBookFg(NT);
    const m = this.mat.clone('paperCStack'); m.backFaceCulling = false; m.diffuseTexture = null; this.matStack = m;
  }
  // ---- v8 open-book foreground: at every zone border (and mid-zone in the long ones) the road crosses a giant open book: both
  // pages lie beside the road with their outer edges curling up and over, a page block under them, and stacks of closed books
  // at the outer corners. Merged into the page-stack mesh of the chunk (no extra draw call; high tier).
  private buildBookFg(NT: boolean[]) {
    const ch = this.plc.chunks, Z = this.spec.zones; if (!ch.length) return;
    const chunkAt = (t: number) => { let k = 0; for (let i = 0; i < ch.length; i++) if (ch[i].t0 <= t) k = i; return k; };
    const T: number[] = [];
    Z.forEach(z => { const L = z.t1 - z.t0; T.push(Math.max(1.6, z.t0 + 0.6)); if (L > 20) T.push(z.t0 + L / 2); });
    // v8b: page paper is a cool lilac-white with a blush rim and lilac page block, so it never reads as a (cream / gold) road tile
    const CR = [0.97, 0.95, 0.99], CR2 = [0.9, 0.86, 0.95], GO = [0.98, 0.66, 0.78], UND = [0.84, 0.78, 0.92];
    const BK = [[0.96, 0.72, 0.8], [0.8, 0.72, 0.94], [0.74, 0.91, 0.85], [0.72, 0.85, 0.96], [1.0, 0.86, 0.62], [0.98, 0.62, 0.7]];
    let seed = 7; const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    for (const tb of T) {
      const ci = chunkAt(tb), c = ch[ci], G = this.stackGeo[ci], zi = c.zone, night = NT[zi];
      const dim = (k: number[]) => night ? [k[0] * 0.66, k[1] * 0.66, k[2] * 0.76] : k;
      const y0 = (c.terr ? c.terr.y : c.y) + 0.04;
      const fr = flowAnchor(this.route, tb, 0, 0, 0); const fx = Math.sin(fr.yaw), fz = Math.cos(fr.yaw), rx = fz, rz = -fx;
      const P = (side: number, lat: number, along: number, y: number) => [fr.pos.x + rx * lat * side + fx * along, y, fr.pos.z + rz * lat * side + fz * along];
      const tri = (a: number[], b: number[], cc: number[], ca: number[], cb: number[], cc2: number[]) => { const i0 = G.p.length / 3; G.p.push(...a, ...b, ...cc); G.c.push(...ca, 1, ...cb, 1, ...cc2, 1); G.i.push(i0, i0 + 1, i0 + 2); };
      const quad = (a: number[], b: number[], cc: number[], d: number[], ca: number[], cb = ca) => { tri(a, b, cc, ca, ca, cb); tri(a, cc, d, ca, cb, cb); };
      for (const side of [-1, 1]) {
        // inner edge: pushed out of the zig-zag until the page footprint is clear of every road
        let lat = 2.6; const PW = 9, PL = 14;
        const clear = (l: number) => { for (const a of [-PL / 2, 0, PL / 2]) for (const u of [0.1, 0.5, 0.9]) { const q = P(side, l + u * PW, a, 0); if (this.hits(q[0], q[2], 1.2, y0 - 1, y0 + 3)) return false; } return true; };
        let k = 0; while (!clear(lat) && k < 10) { lat += 1.5; k++; } if (k >= 10) continue;
        // v8 audit: decor standing where the page lifts / curls would poke through it - those pieces go (chunk meshes are built later)
        for (let q = Math.max(0, ci - 3); q <= Math.min(ch.length - 1, ci + 3); q++) ch[q].items = ch[q].items.filter(it => {
          if (it.layer !== 'mid' && it.layer !== 'ground') return true; if ((this.spec.assets[it.a]?.h ?? 0) * it.s < 0.35) return true;
          const dx = it.x - fr.pos.x, dz = it.z - fr.pos.z, lt = (dx * rx + dz * rz) * side, al = dx * fx + dz * fz;
          return !(lt > lat + 0.4 * PW && lt < lat + PW + 2.6 && Math.abs(al) < PL / 2 + 1.2); });
        // page sheet: flat for 60% of its width, then a curl of radius R up and back over (cream, shaded by the curl angle; gold rim)
        const NU = 12, NA = 6, R = 1.1, flat = 0.66, rise = 0.0;   // v8b: lower curl - with the head-pinned camera a 2 m roll stood up like a wall in the lower frame   // page rises from the spine (open-book hump), then rolls up and over at the outer edge
        const prof = (u: number) => { if (u <= flat) { const k = u / flat; return [lat + u * PW, rise * Math.sin(k * Math.PI / 2) + 0.35 * Math.max(0, k - 0.75) ** 2 * 16, 0]; } const th = (u - flat) / (1 - flat) * 2.7; return [lat + flat * PW + R * Math.sin(th), rise + 0.35 + R * (1 - Math.cos(th)), th]; };
        for (let i = 0; i < NU; i++) for (let j = 0; j < NA; j++) {
          const u0 = i / NU, u1 = (i + 1) / NU, a0 = -PL / 2 + PL * j / NA, a1 = -PL / 2 + PL * (j + 1) / NA;
          const p0 = prof(u0), p1 = prof(u1), sh = (th: number) => 1 - 0.13 * Math.sin(th * 0.9), c0 = dim(CR.map(v => v * sh(p0[2]))), c1 = dim((i === NU - 1 ? GO : CR).map(v => v * sh(p1[2])));
          quad(P(side, p0[0], a0, y0 + p0[1]), P(side, p0[0], a1, y0 + p0[1]), P(side, p1[0], a1, y0 + p1[1]), P(side, p1[0], a0, y0 + p1[1]), c0, c1);
        }
        // page block under the flat part: three stepped page layers along the near / far ends (the book's thickness)
        for (const a of [-PL / 2, PL / 2]) for (let L = 0; L < 3; L++) { const yy = y0 - 0.22 * L, o = 0.25 * L * Math.sign(a);
          quad(P(side, lat, a + o, yy), P(side, lat + flat * PW + R, a + o, yy), P(side, lat + flat * PW + R, a + o, yy - 0.22), P(side, lat, a + o, yy - 0.22), dim(L ? CR2 : GO), dim(UND)); }
        // stacks of closed books at the outer corners
        for (const a of [-PL / 2 - 1.2, PL / 2 + 1.0]) {
          const bl = lat + flat * PW + R * 1.6 + 1.2 + rnd() * 1.5; let yy = y0; const n = 2 + Math.floor(rnd() * 3);
          for (let b = 0; b < n; b++) {
            const bw = 2.6 - b * 0.25 + rnd() * 0.3, bd = 1.8 - b * 0.15, bh = 0.42 + rnd() * 0.2, ang = (rnd() - 0.5) * 0.6, col = dim(BK[Math.floor(rnd() * BK.length)]);
            const cs = Math.cos(ang), sn = Math.sin(ang), C = (dx: number, dz: number, y: number) => P(side, bl + dx * cs - dz * sn, a + dx * sn + dz * cs, y);
            const v = [[-bw / 2, -bd / 2], [bw / 2, -bd / 2], [bw / 2, bd / 2], [-bw / 2, bd / 2]];
            quad(C(v[0][0], v[0][1], yy + bh), C(v[1][0], v[1][1], yy + bh), C(v[2][0], v[2][1], yy + bh), C(v[3][0], v[3][1], yy + bh), col);   // cover
            for (let e = 0; e < 4; e++) { const A = v[e], B = v[(e + 1) % 4], pages = e === 1 || e === 3 ? dim(CR) : col.map(x => x * 0.85);
              quad(C(A[0], A[1], yy + bh), C(B[0], B[1], yy + bh), C(B[0], B[1], yy), C(A[0], A[1], yy), e === 0 ? dim(GO) : pages); }
            yy += bh;
          }
        }
      }
    }
  }
  private matStack!: StandardMaterial;
  private emitStack(G: { p: number[]; c: number[]; i: number[] }, ax: number, az: number, bx: number, bz: number, nx: number, nz: number, y: number, lo: number, C: number[][]) {
    const quad = (o0: number, y0: number, o1: number, y1: number, c0: number[], c1: number[]) => {   // from (offset o0, height y0) to (o1, y1) along the run
      const b = G.p.length / 3;
      G.p.push(ax + nx * o0, y0, az + nz * o0, bx + nx * o0, y0, bz + nz * o0, bx + nx * o1, y1, bz + nz * o1, ax + nx * o1, y1, az + nz * o1);
      G.c.push(...c0, 1, ...c0, 1, ...c1, 1, ...c1, 1); G.i.push(b, b + 1, b + 2, b, b + 2, b + 3); };
    const [CR, CR2, GO, GO2, TA, TA2] = C; let o = 0, h = y;
    // three page layers: a thin gold top edge then cream faces, each stepping out onto a gold ledge
    for (let k = 0; k < 3; k++) { const d = 0.3; quad(o, h, o, h - d, k ? (k & 1 ? CR2 : CR) : GO2, k ? (k & 1 ? CR2 : CR) : GO); h -= d; quad(o, h, o + 0.3, h, GO, GO2); o += 0.3; }
    // v6 paper cliff: a staircase of page strata (~0.9 m each, stepping out 0.5 m onto cream / gold ledges) down to the page below,
    // instead of one tall plain face (the z07 'cream wall')
    const rest = Math.max(0.5, h - lo), ns = Math.max(2, Math.min(9, Math.round(rest / 0.9))), sd = rest / ns;
    for (let k = 0; k < ns; k++) { const c0 = k & 1 ? TA : CR2, c1 = k & 1 ? TA2 : TA; quad(o, h, o, h - sd, c0, c1); h -= sd;
      if (k < ns - 1) { const g = k % 3 === 1; quad(o, h, o + 0.5, h, g ? GO : CR, g ? GO2 : CR2); o += 0.5; } }
  }
  /** v10 bank edge as a closed book seen from its fore-edge: a coloured cover lip (overhangs 0.14 m), then the page block as thin
   * alternating paper-white / lilac-grey leaves (0.16 m) down to the bottom cover. Vertical (no stepped ledges: from the key camera
   * ledges read as extra road-like stripes). `full` = leaf lines; outer edges get a plain block. */
  private emitBank(G: { p: number[]; c: number[]; i: number[] }, ax: number, az: number, bx: number, bz: number, nx: number, nz: number, y: number, lo: number, cov: number[], night: boolean, full: boolean) {
    const q = (o0: number, y0: number, o1: number, y1: number, c0: number[], c1: number[]) => { const b = G.p.length / 3;
      G.p.push(ax + nx * o0, y0, az + nz * o0, bx + nx * o0, y0, bz + nz * o0, bx + nx * o1, y1, bz + nz * o1, ax + nx * o1, y1, az + nz * o1);
      G.c.push(...c0, 1, ...c0, 1, ...c1, 1, ...c1, 1); G.i.push(b, b + 1, b + 2, b, b + 2, b + 3); };
    const d = (c: number[]) => night ? [c[0] * 0.62, c[1] * 0.62, c[2] * 0.72] : c;
    const W1 = d([0.98, 0.96, 0.95]), W2 = d([0.86, 0.83, 0.9]), cv2 = cov.map(v => v * 0.8), L = 0.14;
    q(0, y + 0.02, L, y + 0.02, cov, cov); q(L, y + 0.02, L, y - 0.14, cov, cv2); q(L, y - 0.14, 0, y - 0.14, cv2, cv2);   // top cover lip
    const h = y - 0.14 - lo - 0.16; if (h <= 0.05) return;
    if (!full) { q(0, y - 0.14, 0, lo + 0.16, W2, W2); } else {
      const n = Math.max(2, Math.round(h / 0.16)), s = h / n; let yy = y - 0.14;
      for (let k = 0; k < n; k++) { const c = k & 1 ? W2 : W1; q(-0.02 * (k & 1), yy, -0.02 * (k & 1), yy - s, c, c); yy -= s; } }
    q(0, lo + 0.16, L, lo + 0.16, cv2, cv2); q(L, lo + 0.16, L, lo, cv2, cv2);   // bottom cover
  }
  private refreshStacks(a: number, b: number) {
    const on = this.tier === 'high', sig = `${a}:${b}`; if (sig === this.stackSig) return; this.stackSig = sig;
    this.stacks?.dispose(); this.stacks = null;
    const p: number[] = [], c: number[] = [], idx: number[] = [];
    for (const GG of on ? [this.stackGeo, this.bankGeo] : [this.bankGeo])   // v10: bank cliffs on both tiers, page-stack edges / book spreads high only
      for (let i = a; i <= b; i++) { const G = GG[i]; if (!G) continue; const o = p.length / 3; for (const v of G.p) p.push(v); for (const v of G.c) c.push(v); for (const v of G.i) idx.push(v + o); }
    if (!idx.length) return; const m = new Mesh('cstacks', this.scene); const vd = new VertexData(); vd.positions = p; vd.colors = c; vd.indices = idx; vd.applyToMesh(m, false);
    m.material = this.matStack; m.isPickable = false; m.parent = this.root; m.freezeWorldMatrix(); (m as any).__tris = idx.length / 3; this.stacks = m;
  }

  // ---- chunks: ground cover (static) + mid layer (merged, pops per chunk) + lamp halos (night zones), all vertex-colour merged ----
  private buildChunk(c: CChunk): ChunkM {
    const night = this.night[c.zone], lift = night ? 0.32 : 0, lc = hexRGB(this.spec.zones[c.zone].palette.light ?? '#FFE8B0');   // lift toward the zone's warm light
    const G = { pos: [] as number[], col: [] as number[], idx: [] as number[] }, M = { pos: [] as number[], col: [] as number[], idx: [] as number[] };
    const L = { pos: [] as number[], col: [] as number[], uv: [] as number[], idx: [] as number[] };
    const quad = (p: number[][], k: number) => { const i0 = L.pos.length / 3; for (const q of p) L.pos.push(q[0], q[1], q[2]); L.uv.push(0, 0, 1, 0, 1, 1, 0, 1); for (let n = 0; n < 4; n++) L.col.push(k, k * 0.86, k * 0.6, 1);   /* v7: warm halos */ L.idx.push(i0, i0 + 1, i0 + 2, i0, i0 + 2, i0 + 3); };
    for (const it of c.items) {
      if ((it.layer !== 'ground' && it.layer !== 'mid') || !this.keep(it)) continue;
      const t = this.tm.get(it.a); if (!t) continue; const ic = this.colOf(it, t.model);
      const B = it.layer === 'ground' ? G : M, y0 = it.layer === 'ground' ? it.y + 0.002 : it.y - c.y;   // mid: relative to the chunk pivot
      const cs = Math.cos(it.yaw), sn = Math.sin(it.yaw), s = it.s, i0 = B.pos.length / 3;
      // v8 repetition pass: palette variant (rows step through them, so neighbours differ) + per-instance height stretch
      const tc = variantCols(it.a, t.col as any, it.v ?? Math.floor(hash(it.x * 3.1, it.z * 1.7) * 9973)), sy = STRETCH.has(it.a) ? 0.88 + 0.3 * hash(it.z, it.x) : 1;
      for (let i = 0; i < t.pos.length; i += 3) {
        const lx = t.pos[i] * s, ly = t.pos[i + 1] * s * sy, lz = t.pos[i + 2] * s;
        B.pos.push(it.x + lx * cs + lz * sn, y0 + ly, it.z - lx * sn + lz * cs);
        const j = i / 3 * 4; let r = tc[j] * ic[0], g = tc[j + 1] * ic[1], b = tc[j + 2] * ic[2];
        if (lift) { r += (lc[0] - r) * lift; g += (lc[1] - g) * lift; b += (lc[2] - b) * lift; }
        B.col.push(r, g, b, 1);
      }
      for (let i = 0; i < t.idx.length; i++) B.idx.push(t.idx[i] + i0);
      const lp = night ? LAMP[it.a] : undefined;
      if (lp) {   // halo: a pool of light on the page + two crossed quads at the lamp head
        const h = (this.spec.assets[it.a]?.h ?? 1) * s, r = lp[1] * s * 1.4, hy = it.y - c.y + h * lp[0], gy = it.y - c.y + 0.03;   // relative to the chunk pivot (c.y)
        const tree = /pine|tree|mushroom-group|flower-heart/.test(it.a), R = r * 2.0;
        if (!tree) quad([[it.x - R, gy, it.z - R], [it.x + R, gy, it.z - R], [it.x + R, gy, it.z + R], [it.x - R, gy, it.z + R]], 0.11);   // v7: dimmer light pools
        const fl = it.a === 'flower-heart', kq = fl ? 0.13 : tree ? 0.24 : 0.42, rq = fl ? r * 0.7 : r;   // glowing flowers: small, soft
        quad([[it.x - rq, hy - rq, it.z], [it.x + rq, hy - rq, it.z], [it.x + rq, hy + rq, it.z], [it.x - rq, hy + rq, it.z]], kq);
        quad([[it.x, hy - rq, it.z - rq], [it.x, hy - rq, it.z + rq], [it.x, hy + rq, it.z + rq], [it.x, hy + rq, it.z - rq]], kq);
      }
    }
    const mk = (name: string, B: { pos: number[]; col: number[]; idx: number[]; uv?: number[] }, mat: StandardMaterial) => {
      if (!B.pos.length) return null; const m = new Mesh(name, this.scene); const vd = new VertexData(); vd.positions = B.pos; vd.colors = B.col; vd.indices = B.idx; if (B.uv) vd.uvs = B.uv;
      vd.applyToMesh(m, false); m.material = mat; m.isPickable = false; m.parent = this.root; return m; };
    const mat = night ? this.matNight : this.mat;
    const g = mk(`cchunk${c.i}`, G, mat) ?? new Mesh(`cchunk${c.i}`, this.scene); g.parent = this.root; g.freezeWorldMatrix();
    const m = mk(`cmid${c.i}`, M, mat); if (m) { m.position.y = c.y; m.scaling.y = 0.02; }
    // halos are merged across the whole window into one additive mesh (rebuildGlow), shown once their chunk has popped
    return { g, m, glow: null, t0: c.t0, tris: (G.idx.length + M.idx.length + L.idx.length) / 3, y: c.y, L: L.pos.length ? L : null };
  }

  // ---- thin-instance types ----
  private typeOf(id: string) {
    let ti = this.types.get(id);
    if (!ti) {
      const t = this.tm.get(id)!; const mesh = this.meshFrom(`cti_${id}`, t); mesh.alwaysSelectAsActiveMesh = true;
      ti = { id, mesh, mats: new Float32Array(16 * 16), cols: new Float32Array(4 * 16), cap: 16, items: [], tris: t.tris };
      mesh.thinInstanceSetBuffer('matrix', ti.mats, 16, false); mesh.thinInstanceSetBuffer('color', ti.cols, 4, false); mesh.thinInstanceCount = 0;
      this.types.set(id, ti);
    }
    return ti;
  }
  private refill(a: number, b: number) {
    for (const ti of this.types.values()) ti.items = [];
    if (a < 0 || b < 0) return;   // window not placed yet (or invalidated by a ground refresh): the next update refills
    for (let i = a; i <= b; i++) for (const it of this.plc.chunks[i].items) if (it.layer !== 'ground' && it.layer !== 'mid' && this.keep(it)) this.typeOf(it.a).items.push(it);
    for (const ti of this.types.values()) {
      if (ti.items.length > ti.cap) { ti.cap = Math.max(ti.items.length, ti.cap * 2); ti.mats = new Float32Array(16 * ti.cap); ti.cols = new Float32Array(4 * ti.cap); ti.mesh.thinInstanceSetBuffer('matrix', ti.mats, 16, false); ti.mesh.thinInstanceSetBuffer('color', ti.cols, 4, false); }
      const model = this.tm.get(ti.id)!.model;
      ti.items.forEach((it, k) => { const c = this.colOf(it, model); ti.cols.set([c[0], c[1], c[2], 1], k * 4); });
      ti.mesh.thinInstanceBufferUpdated('color'); ti.mesh.thinInstanceCount = ti.items.length; ti.mesh.setEnabled(ti.items.length > 0);
    }
  }
  private writeTypes(t: number, beatK: number) {
    const time = this.time;
    for (const ti of this.types.values()) {
      if (!ti.items.length) continue; const M = ti.mats;
      for (let k = 0; k < ti.items.length; k++) {
        const it = ti.items[k]; let s = it.s, sy = 1, x = it.x, y = this.yOf(it), z = it.z; const ph = (it.x * 0.37 + it.z * 0.61) % 6.283;
        if (it.layer === 'mid') sy = Math.max(0.02, spring(t - (it.t - this.pop)));               // pops up before the line passes
        else if (it.layer === 'sky') { y += Math.sin(time * 1.1 + ph) * 0.25; s *= 1 + 0.06 * beatK; }
        else if (it.layer === 'anim') { x += Math.sin(time * 0.5 + ph) * 1.2; y += it.a === 'petal' ? -((time * 0.4 + ph) % 3) : Math.sin(time * 2 + ph) * 0.3; }
        const c = Math.cos(it.yaw), sn = Math.sin(it.yaw), o = k * 16;
        M[o] = c * s; M[o + 1] = 0; M[o + 2] = -sn * s; M[o + 3] = 0; M[o + 4] = 0; M[o + 5] = s * sy; M[o + 6] = 0; M[o + 7] = 0;
        M[o + 8] = sn * s; M[o + 9] = 0; M[o + 10] = c * s; M[o + 11] = 0; M[o + 12] = x; M[o + 13] = y; M[o + 14] = z; M[o + 15] = 1;
      }
      ti.mesh.thinInstanceBufferUpdated('matrix');
    }
  }

  // ---- set pieces ----
  private makeSet(s: CSet): SetE {
    const node = new TransformNode(`cset_${s.a}`, this.scene); node.parent = this.root;
    node.position.set(s.x, s.y, s.z); node.rotation.y = s.yaw; node.scaling.setAll(s.s);
    const hinge = new TransformNode('hinge', this.scene); hinge.parent = node;
    const e: SetE = { def: s, node, hinge, far: null, near: null, nearMeshes: [], piv: [], tris: 0, on: true, lodFar: false };
    this.buildSetVisual(e); this.setOn(e, false);
    return e;
  }
  private buildSetVisual(e: SetE) {
    e.far?.dispose(); e.near?.dispose(false, false); e.far = null; e.near = null; e.nearMeshes = []; e.piv = [];
    const t = this.tm.get(e.def.a)!; e.tris = t.tris;
    const vi = e.def.v ?? 0; e.far = this.meshFrom(`cfar_${e.def.a}`, vi ? { ...t, col: variantCols(e.def.a, t.col as any, vi) as any } : t); e.far.parent = e.hinge; e.far.material = this.matSet;
    if (t.container) {
      const inst = t.container.instantiateModelsToScene(n => `${n}_${e.def.t}`, false, { doNotInstantiate: true });   // always clone (as before v8): palette variants need own geometry, and instances of the container's meshes (not in the scene) would not render
      const r = new TransformNode(`cnear_${e.def.a}`, this.scene); r.parent = e.hinge; r.scaling.setAll(t.scale);
      for (const n of inst.rootNodes) n.parent = r;
      for (const m of r.getChildMeshes()) { m.material = this.matSet; m.isPickable = false; e.nearMeshes.push(m as Mesh);
        if (vi) { const d = m.getVerticesData('color'); if (d && d.length === m.getTotalVertices() * 4 && typeof (m as Mesh).makeGeometryUnique === 'function') { (m as Mesh).makeGeometryUnique(); m.setVerticesData('color', Float32Array.from(variantCols(e.def.a, d as any, vi, false)), false, 4); } } }
      for (const n of r.getDescendants(false) as TransformNode[]) {
        const mm = /pivot_([a-z]+)(\d*)/i.exec(n.name); if (!mm || mm[1] === 'root') continue;
        e.piv.push({ node: n, kind: mm[1].toLowerCase(), i: +(mm[2] || 0), base: n.rotationQuaternion?.clone() ?? null, baseS: n.scaling.clone(), baseP: n.position.clone() });
      }
      e.near = r;
      // v5: a near copy only earns its extra draws when it animates (pivots); static models stay on the merged 1-draw mesh,
      // and the static (non-pivot) parts of an animated copy are merged into one mesh (castle: 6 draws -> 2)
      if (!e.piv.length && e.nearMeshes.length > 1) { r.dispose(false, false); e.near = null; e.nearMeshes = []; }
      else if (e.nearMeshes.length > 2) {
        const pv = new Set(e.piv.map(p => p.node)); const moving = (m: Mesh) => { for (let n = m.parent; n && n !== r; n = n.parent) if (pv.has(n as TransformNode)) return true; return pv.has(m as any); };
        const st = e.nearMeshes.filter(m => !moving(m) && m.getTotalVertices() > 0);
        if (st.length > 1) {
          r.parent = null; r.computeWorldMatrix(true); for (const m of st) m.computeWorldMatrix(true);
          const mg = Mesh.MergeMeshes(st, true, true, undefined, false, false);
          if (mg) { mg.bakeTransformIntoVertices(r.getWorldMatrix().clone().invert()); mg.parent = r; mg.material = this.matSet; mg.isPickable = false; e.nearMeshes = [mg, ...e.nearMeshes.filter(m => !st.includes(m))]; }
          r.parent = e.hinge;
        }
      }
    }
    e.lodFar = !e.near; this.applyLod(e);
  }
  private applyLod(e: SetE) { e.far?.setEnabled(e.on && (e.lodFar || !e.near)); e.near?.setEnabled(e.on && !e.lodFar && !!e.near); }
  private setOn(e: SetE, on: boolean) { if (e.on === on) return; e.on = on; e.node.setEnabled(on); this.applyLod(e); }
  private animSet(e: SetE, t: number, beatK: number, cam: Vector3 | null) {
    const d = e.def; const on = t >= d.popAt - 1.5 && t <= d.t + 10 && !(d.hi && this.tier === 'low'); this.setOn(e, on); if (!on) return;
    e.hinge.rotation.x = -Math.PI / 2 * (1 - spring(t - d.popAt));                     // pop-up book: lies flat, springs upright
    if (cam) { const far = Vector3.Distance(cam, e.node.position) > TIERS[this.tier].lod; if (far !== e.lodFar) { e.lodFar = far; this.applyLod(e); } }
    if (e.lodFar) return;
    const time = this.time;
    for (const p of e.piv) {
      let rx = 0, ry = 0, rz = 0, sc = 1;
      // glTF local axes of a pivot: Blender X = x, Blender Z (up) = y, Blender Y (front-back) = z
      if (p.kind === 'heart' || p.kind === 'pulse') sc = 1 + 0.12 * beatK;
      else if (p.kind === 'lid') rx = -1.1 * Math.min(1, Math.max(0, (t - d.popAt - 0.6) / 0.8));      // hinge open about Blender X
      else if (p.kind === 'spin') ry = time * (0.6 + 0.15 * p.i) * (p.i % 2 ? -1 : 1);                   // about Blender Z
      else if (p.kind === 'wheel') rz = time * 0.5 * (p.i % 2 ? -1 : 1);                                // about Blender Y (front axis)
      else if (p.kind === 'swing') rx = 0.18 * Math.sin(time * 2.2 + p.i * 0.9);                        // pendulum about Blender X
      else if (p.kind === 'hand') { const s = t * 2, k = Math.floor(s), f = Math.min(1, (s - k) * 6); rz = -(k + f) * Math.PI / 30 * (p.i ? 1 : 12); }   // ticks each half second
      else if (p.kind === 'ears' || p.kind === 'ear') rx = -0.22 * beatK;
      else if (p.kind === 'gate') ry = -1.3 * Math.min(1, Math.max(0, (t - d.popAt - 0.6) / 0.8));
      else if (p.kind === 'flag') ry = 0.35 * Math.sin(time * 5 + p.i * 1.3);
      else if (p.kind === 'tower') { const k = spring(t - d.popAt - 0.15 - p.i * 0.07); p.node.scaling.set(p.baseS.x, p.baseS.y * Math.max(0.02, k), p.baseS.z); continue; }   // towers pop 1/8 beat apart
      else if (p.kind === 'bob') { p.node.position.y = p.baseP.y + 0.15 * beatK; continue; }
      p.node.scaling.copyFrom(p.baseS).scaleInPlace(sc);
      const q = Quaternion.RotationYawPitchRoll(ry, rx, rz); p.node.rotationQuaternion = p.base ? p.base.multiply(q) : q;
    }
  }

  private refreshAsset(id: string) {
    const ti = this.types.get(id); if (ti) { const t = this.tm.get(id)!; const vd = new VertexData(); vd.positions = t.pos; vd.colors = t.col; vd.indices = t.idx; vd.applyToMesh(ti.mesh, true); ti.tris = t.tris; this.refill(this.range[0], this.range[1]); }
    if (this.dirtyAt < 0) this.dirtyAt = this.time;   // ground + mid are merged per chunk: rebuild (throttled) once models land
    for (const e of this.sets) if (e.def.a === id) { this.buildSetVisual(e); const on = e.on; e.on = !on; this.setOn(e, on); }
  }

  update(t: number, dt: number, beatK: number, cam: Vector3 | null, head?: Vector3 | null) {
    this.skyT = t;
    if (cam && head) { CUT.cam.copyFrom(cam); CUT.head.copyFrom(head); }
    this.time += dt; const T = TIERS[this.tier];
    if (this.dirtyAt >= 0 && this.time - this.dirtyAt > 0.4) { this.dirtyAt = -1; this.dropChunks(); }
    const key = typeof location === 'undefined' || !/[?&]cam=old\b/.test(location.search);   // key camera sees further ahead; v9: the head-pinned frame shows ~6 s of road behind the head (its lower third was unbuilt)
    this.pop = key ? 8.5 : 5;
    const [a, b] = activeRange(this.plc.chunks, t, key ? (this.tier === 'high' ? 4.5 : 4) : T.behind, key ? T.ahead + (this.tier === 'high' ? 2 : 0) : T.ahead);
    if (a !== this.range[0] || b !== this.range[1]) {
      for (const [i, m] of this.chunkMesh) if (i < a || i > b) { this.dropChunk(m); this.chunkMesh.delete(i); }
      for (let i = a; i <= b; i++) if (!this.chunkMesh.has(i)) this.chunkMesh.set(i, this.buildChunk(this.plc.chunks[i]));
      this.range = [a, b]; this.refill(a, b);
      const on = new Set<number>(); for (let i = a; i <= b; i++) on.add(this.plc.chunks[i].zone); this.pages.forEach((p, zi) => p.setEnabled(on.has(zi)));
    }
    this.writeTypes(t, beatK);
    this.imp?.update(a, Math.min(this.plc.chunks.length - 1, b + 3));
    this.refreshStacks(a, Math.min(this.plc.chunks.length - 1, b + 2));   // impostors reach further ahead than the decor window
    if (cam && this.back) { let zi = this.plc.chunks[a].zone, ylo = 1e9; for (let i = a; i <= b; i++) { const c = this.plc.chunks[i]; if (c.t0 <= t) zi = c.zone; ylo = Math.min(ylo, c.y); }
      this.back.update(this.tier === 'high' ? zi : -1, cam, ylo - 25, dt || 0.016); this.curZone = zi; }
    this.rebuildGlow(t);
    let tris = 0, inst = 0, sets = 0, tb = 0, win = 0; const A = this.spec.assets;
    for (const e of this.sets) { this.animSet(e, t, beatK, cam); if (e.on) { sets++; win += e.tris; if (!this.scene.frustumPlanes || !e.far || (e.far.computeWorldMatrix(), e.far.isInFrustum(this.scene.frustumPlanes))) tris += e.tris; tb += Math.max(e.tris, A[e.def.a]?.tris ?? 0); } }
    if (this.stacks) { const st = (this.stacks as any).__tris; tris += st; tb += st; win += st; }
    for (const p of this.pages) if (p.isEnabled()) { tris += (p as any).__tris; tb += (p as any).__tris; }
    if (this.imp) { tris += this.imp.tris; tb += this.imp.tris; win += this.imp.tris; }
    const fp = this.scene.frustumPlanes;
    const vis = (x: Mesh | null) => !!x && x.isEnabled() && (!fp || x.isInFrustum(fp));
    const triOf = (x: Mesh | null) => x ? x.getTotalIndices() / 3 : 0;
    for (const [i, m] of this.chunkMesh) {
      win += m.tris; tris += (vis(m.g) ? triOf(m.g) : 0) + (vis(m.m) ? triOf(m.m) : 0) + (m.glow && vis(m.m ?? m.glow) ? triOf(m.glow) : 0); if (m.m) m.m.scaling.y = Math.max(0.02, spring(t - (m.t0 - this.pop)));   // merged mid layer pops up per chunk (5 s ahead; v8 key camera 8.5 s: its upper half looks ~60-90 m ahead)
      for (const it of this.plc.chunks[i].items) if ((it.layer === 'ground' || it.layer === 'mid') && this.keep(it)) tb += Math.max(this.tm.get(it.a)?.tris ?? 0, A[it.a]?.tris ?? 0); }
    let types = 0; for (const ti of this.types.values()) if (ti.items.length) { types++; inst += ti.items.length; tris += ti.items.length * ti.tris; win += ti.items.length * ti.tris; tb += ti.items.length * Math.max(ti.tris, A[ti.id]?.tris ?? 0); }
    let zone = 0; for (let i = 0; i < this.spec.zones.length; i++) if (this.spec.zones[i].t0 <= t) zone = i;
    this.last = { chunks: [a, b], chunkMeshes: this.chunkMesh.size, types, instances: inst, sets, tris, zone, models: this.models, trisAtBudget: tb, trisWindow: win };
  }

  dispose() {
    this.disposed = true;
    for (const [id, t] of this.tm) if (t.container) { t.container.dispose(); this.tm.delete(id); }
    { const ip = this.scene.imageProcessingConfiguration; ip.vignetteEnabled = false; ip.colorCurvesEnabled = false; } this.imp?.dispose(); this.back?.dispose(); for (const t of this.groundTex.values()) t.dispose(); this.root.dispose(false, false); this.glowAll?.dispose(); this.matGlow.diffuseTexture?.dispose(); this.matGlow.dispose(); this.matNight.dispose(); this.mat.dispose(); this.matSet.dispose(); for (const m of this.pageMats) m.dispose(); this.sky?.dispose(); this.skyMat?.dispose(); for (const t of this.skyTex.values()) t.dispose();
  }
}
