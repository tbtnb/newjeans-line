/**
 * Concept C v4 "painted" layer -- cheap tricks instead of geometry:
 *  - PageFade: zone pages fade out at their outer rims with a world-space dither (opaque pass, no sorting), so neighbouring
 *    zones / terraces blend instead of reading as hard floating islands.
 *  - Impostors: one merged mesh of camera-facing sprite cards (atlas rendered from the real models in Blender) for every
 *    chunk in the window -> the mid / far distance becomes a dense carpet in one draw call.
 *  - Backdrop: a painted horizon band (open cylinder around the camera) per zone, cross-faded at zone changes.
 */
import type { Scene } from '@babylonjs/core/scene';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { CreateCylinder } from '@babylonjs/core/Meshes/Builders/cylinderBuilder';
import type { TransformNode } from '@babylonjs/core/Meshes/transformNode';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { Material } from '@babylonjs/core/Materials/material';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { MaterialPluginBase } from '@babylonjs/core/Materials/materialPluginBase';
import { Color3 } from '@babylonjs/core/Maths/math.color';
import type { Vector3 } from '@babylonjs/core/Maths/math.vector';
import type { CChunk } from './place';
import type { SceneCSpec } from '../../core/types';
import { Cutaway } from './cutaway';

export class PageFade extends MaterialPluginBase {
  constructor(m: Material) { super(m, 'PageFade', 310, { PAGEFADE: false }); this._enable(true); }
  prepareDefines(d: Record<string, unknown>) { d.PAGEFADE = true; }
  getClassName() { return 'PageFade'; }
  getCustomCode(type: string) {
    if (type !== 'fragment') return null;
    return { CUSTOM_FRAGMENT_BEFORE_FRAGCOLOR: `
#if defined(PAGEFADE) && defined(VERTEXCOLOR)
{ float n = fract(sin(dot(floor(vPositionW.xz * 6.0), vec2(12.9898, 78.233))) * 43758.5453); if (vColor.a < n * 0.98 + 0.01) discard; color.a = 1.0; }
#endif
` };
  }
}

const unlit = (name: string, scene: Scene) => { const m = new StandardMaterial(name, scene); m.disableLighting = true; m.diffuseColor = Color3.Black(); m.emissiveColor = Color3.White(); m.specularColor = Color3.Black(); return m; };

type Atlas = { size: number[]; sprites: Record<string, { uv: number[]; w: number; h: number }> };
export class Impostors {
  private mat: StandardMaterial; private atlas: Atlas | null = null; private mesh: Mesh | null = null; private sig = ''; tris = 0;
  constructor(private scene: Scene, private root: TransformNode, private chunks: CChunk[], private spec: SceneCSpec, base: string, private night: boolean[], private density: number) {
    const m = unlit('paperCImp', scene); const tex = new Texture(base + 'models/omg-c/imp/atlas.webp', scene, false, false, Texture.TRILINEAR_SAMPLINGMODE);
    tex.hasAlpha = true; m.diffuseTexture = tex; m.useAlphaFromDiffuseTexture = true;   /* alpha test runs after all alpha computations: the texture alpha must feed it */ m.transparencyMode = Material.MATERIAL_ALPHATEST; m.alphaCutOff = 0.45; m.backFaceCulling = false;
    new Cutaway(m); this.mat = m;
    fetch(base + 'models/omg-c/imp/atlas.json').then(r => r.json()).then(a => { this.atlas = a; this.sig = ''; }).catch(e => console.warn('omg-c impostor atlas', e));
  }
  update(a: number, b: number) {
    if (!this.atlas) return; const sig = a + ':' + b; if (sig === this.sig) return; this.sig = sig;
    this.mesh?.dispose(); this.mesh = null; this.tris = 0;
    const pos: number[] = [], uv: number[] = [], col: number[] = [], idx: number[] = []; const S = this.atlas.sprites;
    const hash = (x: number, z: number) => { const s = Math.sin(x * 12.9898 + z * 78.233) * 43758.5453; return s - Math.floor(s); };
    for (let i = a; i <= b; i++) for (const it of this.chunks[i].imp ?? []) {
      const sp = S[it.k]; if (!sp || hash(it.x, it.z) > this.density) continue;
      const k0 = Math.min(it.s, 11 / sp.h), w = sp.w * k0, h = sp.h * k0, c = Math.cos(it.yaw), s = Math.sin(it.yaw), i0 = pos.length / 3, y0 = it.y - 0.08 * h;
      const rx = c * w / 2, rz = -s * w / 2;   // card right vector (local +x rotated by yaw)
      pos.push(it.x - rx, y0, it.z - rz, it.x + rx, y0, it.z + rz, it.x + rx, y0 + h, it.z + rz, it.x - rx, y0 + h, it.z - rz);
      const [u0, v0, u1, v1] = sp.uv; uv.push(u0, v1, u1, v1, u1, v0, u0, v0);   // texture loaded with invertY=false: v grows downwards like the atlas json
      const k = this.night[it.zone] ? 0.9 : 1.0 - 0.12 * hash(it.z, it.x); for (let n = 0; n < 4; n++) col.push(k, k, k, 1);
      idx.push(i0, i0 + 1, i0 + 2, i0, i0 + 2, i0 + 3);
    }
    if (!idx.length) return;
    const m = new Mesh('cimp', this.scene); const vd = new VertexData(); vd.positions = pos; vd.uvs = uv; vd.colors = col; vd.indices = idx; vd.applyToMesh(m, false);
    m.hasVertexAlpha = false; m.material = this.mat; m.isPickable = false; m.parent = this.root; m.freezeWorldMatrix(); this.mesh = m; this.tris = idx.length / 3;
  }
  setDensity(d: number) { if (d !== this.density) { this.density = d; this.sig = ''; } }
  visible() { return !!this.mesh; }
  dispose() { this.mesh?.dispose(); this.mat.diffuseTexture?.dispose(); this.mat.dispose(); }
}

export class Backdrop {
  private a: Mesh; private b: Mesh; private ma: StandardMaterial; private mb: StandardMaterial; private tex = new Map<number, Texture>(); private cur = -1; private fadeT = 1;
  constructor(private scene: Scene, root: TransformNode, private spec: SceneCSpec, private base: string, readonly R = 300) {
    const mk = (n: string) => { const m = CreateCylinder(n, { diameter: 2 * R, height: 1, tessellation: 48, cap: Mesh.NO_CAP, sideOrientation: Mesh.BACKSIDE }, scene);
      const mat = unlit(n + 'M', scene); mat.fogEnabled = false; mat.backFaceCulling = false; m.material = mat; m.isPickable = false; m.parent = root; m.infiniteDistance = false; m.setEnabled(false); return [m, mat] as const; };
    [this.a, this.ma] = mk('cbackA'); [this.b, this.mb] = mk('cbackB');
  }
  private texOf(zi: number) {
    let t = this.tex.get(zi); const f = this.spec.zones[zi].backdrop; if (t || !f) return t ?? null;
    t = new Texture(this.base + f, this.scene, false, true, Texture.TRILINEAR_SAMPLINGMODE); t.wrapU = Texture.WRAP_ADDRESSMODE; t.wrapV = Texture.CLAMP_ADDRESSMODE; t.uScale = -3; this.tex.set(zi, t); return t;
  }
  /** zi: current zone; cam: camera position; y: band bottom (below the lowest page in view); dt for the cross-fade */
  update(zi: number, cam: Vector3, y: number, dt: number) {
    const t = zi < 0 ? null : this.texOf(zi);
    if (!t || !t.isReady()) { this.a.setEnabled(false); this.b.setEnabled(false); return; }
    if (zi !== this.cur) {   // B takes the old texture and fades out over A with the new one
      if (this.cur >= 0 && this.ma.diffuseTexture) { this.mb.diffuseTexture = this.ma.diffuseTexture; this.fadeT = 0; }
      this.ma.diffuseTexture = t; this.cur = zi;
    }
    this.fadeT = Math.min(1, this.fadeT + dt / 1.6);
    const H = this.R * 0.62;
    for (const m of [this.a, this.b]) { m.position.set(cam.x, y + H / 2, cam.z); m.scaling.y = H; }
    this.b.scaling.x = this.b.scaling.z = 0.985;   // the fading copy sits just inside (no z-fight)
    this.a.setEnabled(true); this.a.renderingGroupId = 0;
    const fb = this.fadeT < 1; this.b.setEnabled(fb); this.mb.alpha = 1 - this.fadeT; this.b.alphaIndex = 1;
  }
  dispose() { this.a.dispose(); this.b.dispose(); this.ma.dispose(); this.mb.dispose(); for (const t of this.tex.values()) t.dispose(); }
}
