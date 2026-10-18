// Show visuals (layout.fx, schema v2.8): glow layer, scene image processing (contrast / exposure / vignette), beat-reactive
// exposure pulses, drop sparkle flashes, stage searchlight beams, twinkling glow sprites, glossy road + glowing edge trims.
// Everything is data-driven and off unless a level sets layout.fx. Camera-agnostic: it only reads scene.activeCamera.
// Per frame: no allocations (scratch vectors/matrices), instanced meshes, one material per colour.
import { Color3, Color4, CreateBox, CreateCylinder, GlowLayer, Matrix, Mesh, ParticleSystem, Quaternion, Scene, StandardMaterial, Texture, TransformNode, Vector3 } from './bjs';
import { anchor, type Route } from '../core/path';
import type { FxSpec, Layout } from '../core/types';
import { hex } from './prefabs';

interface Beam { t: number; x: number; y: number; z: number; ph: number; tpl: number; idx: number; h: number; }
interface Spark { t: number; x: number; y: number; z: number; s: number; ph: number; c: Color4; }
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const stepVal = <T extends { t: number }>(l: T[] | undefined, t: number) => { let r: T | undefined; for (const x of l ?? []) if (x.t <= t + 1e-9) r = x; return r; };

export class ShowFx {
  private glow: GlowLayer | null = null;
  private beams: Beam[] = []; private beamMeshes: Mesh[] = []; private beamBufs: Float32Array[] = []; private beamMats: StandardMaterial[] = [];
  private sparks: Spark[] = []; private ps: ParticleSystem | null = null;
  private trim: Mesh | null = null; private own: (Mesh | StandardMaterial | Texture)[] = [];
  private keys: NonNullable<FxSpec['keys']>; private dirty = new Set<number>(); private lastFlash = -1;
  private static readonly sc = new Vector3(); private static readonly tr = new Vector3(); private static readonly q = new Quaternion(); private static readonly m = new Matrix();
  readonly fx: FxSpec;

  constructor(private scene: Scene, root: TransformNode, private route: Route, L: Layout, private quality: 'high' | 'low',
    widthAt: (t: number) => number, hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean,
    roadTop: { mesh: Mesh; buffer: Float32Array; setFlush: (f: () => void) => void } | null, private sparkTex: Texture | null) {
    this.fx = L.fx ?? {}; const fx = this.fx;
    this.keys = [...(fx.keys ?? [])].sort((a, b) => a.t - b.t);
    // scene image processing (applied inside the material shaders: no post-process pass, keeps the transparent canvas)
    const ip = scene.imageProcessingConfiguration;
    ip.contrast = fx.contrast ?? 1; ip.exposure = fx.exposure ?? 1;
    if (fx.vignette && quality === 'high') { ip.vignetteEnabled = true; ip.vignetteWeight = fx.vignette.weight ?? 1.5; const vc = hex(fx.vignette.color ?? '#000000'); ip.vignetteColor = new Color4(vc.r, vc.g, vc.b, 0); ip.vignetteStretch = 0.4; }
    // glow layer: only meshes that opt in (trims, beams, objects with glowfx) -> emissive halos
    if (fx.glow && quality === 'high') {
      this.glow = new GlowLayer('fxGlow', scene, { mainTextureRatio: 0.35, blurKernelSize: fx.glow.kernel ?? 48 });
      this.glow.intensity = fx.glow.intensity ?? 0.9;
    }
    // glossy road top + glowing edge trims sharing the road-top instance matrices (so trims reveal exactly with the tiles)
    if (fx.road && roadTop) {
      const tm = roadTop.mesh.material as StandardMaterial | null;
      if (tm && fx.road.gloss) { const g = fx.road.gloss; tm.specularColor = new Color3(g, g, g); tm.specularPower = 48; }
      if (fx.road.trim) {
        const a = CreateBox('fxTrimA', { width: 0.07, height: 3.0, depth: 1.0 }, scene); a.position.set(0.5, 0.5, 0);
        const b = CreateBox('fxTrimB', { width: 0.07, height: 3.0, depth: 1.0 }, scene); b.position.set(-0.5, 0.5, 0);
        const m = Mesh.MergeMeshes([a, b], true)!; m.name = 'fxTrim';
        const mat = new StandardMaterial('fxTrimM', scene); const c = hex(fx.road.trim);
        mat.diffuseColor = c; mat.emissiveColor = c.scale(fx.road.trimGlow ?? 0.8); mat.specularColor = new Color3(0.3, 0.3, 0.3);
        m.material = mat; m.isPickable = false; m.alwaysSelectAsActiveMesh = true;
        m.thinInstanceSetBuffer('matrix', roadTop.buffer, 16, false);
        roadTop.setFlush(() => m.thinInstanceBufferUpdated('matrix'));
        this.trim = m; this.own.push(m, mat); this.glow?.addIncludedOnlyMesh(m);
      }
    }
    // searchlight beams: route-relative (time window + spacing), both sides alternating, never on a road footprint
    const cols: string[] = [];
    for (const b of fx.beams ?? []) {
      const every = b.every ?? 1.2; let side = 1; let k = 0;
      for (let t = b.t0; t <= b.t1; t += every, k++) {
        side = -side; const near = b.near ?? 3;
        const off = widthAt(t) / 2 + near + 1;
        let a = anchor(route, t, side * off, 0, 0).pos; let tries = 0;
        let s = side * off; while (hits(a.x, a.z, 1.2, a.y - 1, a.y + 2) && tries++ < 8) { s += side * 1.5; a = anchor(route, t, s, 0, 0).pos; }
        if (tries > 8) continue;
        const col = (b.colors ?? ['#ffffff'])[k % (b.colors?.length ?? 1)];
        let tpl = cols.indexOf(col); if (tpl < 0) { tpl = cols.length; cols.push(col); }
        this.beams.push({ t, x: a.x, y: a.y - 0.6, z: a.z, ph: k * 1.7, tpl, idx: 0, h: b.height ?? 40 });
      }
    }
    if (this.beams.length) {
      const counts = cols.map(() => 0); for (const b of this.beams) b.idx = counts[b.tpl]++;
      cols.forEach((c, i) => {
        const m = CreateCylinder('fxBeam' + i, { diameterTop: 5, diameterBottom: 0.5, height: 1, tessellation: 18, cap: Mesh.NO_CAP }, scene);
        m.bakeTransformIntoVertices(Matrix.Translation(0, 0.5, 0)); // pivot at the lamp
        const mat = new StandardMaterial('fxBeamM' + i, scene); const cc = hex(c);
        mat.emissiveColor = cc; mat.diffuseColor = Color3.Black(); mat.disableLighting = true; mat.alpha = 0.16; mat.backFaceCulling = false;
        mat.alphaMode = 1; // ALPHA_ADD
        m.material = mat; m.isPickable = false; m.alwaysSelectAsActiveMesh = true; m.parent = root;
        const buf = new Float32Array(Math.max(1, counts[i]) * 16); m.thinInstanceSetBuffer('matrix', buf, 16, false); m.thinInstanceCount = counts[i];
        this.beamMeshes.push(m); this.beamBufs.push(buf); this.beamMats.push(mat); this.own.push(m, mat);
      });
    }
    // twinkling glow sprites beside / above the road (one particle system, static particles, beat-scaled)
    const nMul = quality === 'high' ? 1 : 0.4;
    let seed = 99; const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
    for (const sp of fx.sparkles ?? []) {
      const n = Math.round((sp.t1 - sp.t0) * (sp.density ?? 3) * nMul); const cs = (sp.colors ?? ['#fff3c4']).map(c => { const h = hex(c); return new Color4(h.r, h.g, h.b, 1); });
      for (let i = 0; i < n; i++) {
        const t = sp.t0 + rnd() * (sp.t1 - sp.t0); const side = rnd() < 0.5 ? -1 : 1;
        const a = anchor(route, t, side * (widthAt(t) / 2 + 2 + rnd() * (sp.spread ?? 10)), 0, 0).pos;
        this.sparks.push({ t, x: a.x, y: a.y + 0.5 + rnd() * (sp.height ?? 8), z: a.z, s: (sp.size ?? 0.6) * (0.5 + rnd()), ph: rnd() * 6.28, c: cs[i % cs.length] });
      }
    }
    if (this.sparks.length && sparkTex) {
      const ps = new ParticleSystem('fxSparks', this.sparks.length, scene);
      ps.particleTexture = sparkTex; ps.blendMode = ParticleSystem.BLENDMODE_ADD; ps.emitRate = 0; ps.manualEmitCount = this.sparks.length;
      ps.minLifeTime = ps.maxLifeTime = 1e9; ps.minEmitPower = ps.maxEmitPower = 0; ps.gravity = Vector3.Zero();
      ps.emitter = Vector3.Zero(); let si = 0;
      ps.startPositionFunction = (_w, pos, p) => { const s = this.sparks[si % this.sparks.length]; (p as any).sid = si++; pos.set(s.x, s.y, s.z); };
      ps.updateFunction = () => {}; // positions are static; sizes/colours are written in update()
      ps.start(); this.ps = ps; this.own.push(sparkTex);
    }
  }

  /** Attach objects that should glow (layout objects with glowfx: true). */
  addGlow(meshes: Mesh[]) { if (this.glow) for (const m of meshes) this.glow.addIncludedOnlyMesh(m); }

  update(t: number, beatK: number, flashAt: (p: Vector3) => void, headPos: Vector3) {
    const fx = this.fx; const ip = this.scene.imageProcessingConfiguration;
    // keyed exposure / contrast / glow (1 s smooth blend between keys) + beat pulses
    const cur = stepVal(this.keys, t); let prevK: typeof cur; for (const k of this.keys) { if (cur && k.t >= cur.t) break; prevK = k; }
    const bl = cur ? smooth((t - cur.t) / (cur.blend ?? 1)) : 1;
    const lerp = (a: number | undefined, b: number | undefined, d: number) => (a ?? d) + ((b ?? d) - (a ?? d)) * bl;
    let ex = lerp(prevK?.exposure ?? fx.exposure, cur?.exposure ?? fx.exposure, 1);
    const ct = lerp(prevK?.contrast ?? fx.contrast, cur?.contrast ?? fx.contrast, 1);
    const pulse = stepVal(fx.pulse, t); if (pulse && t < pulse.t1) ex += (pulse.amount ?? 0.15) * beatK;
    for (const f of fx.flashes ?? []) { const d = t - f.t; if (d >= 0 && d < (f.dur ?? 0.5)) ex += (f.amount ?? 0.5) * (1 - d / (f.dur ?? 0.5)); }
    ip.exposure = ex; ip.contrast = ct;
    if (this.glow) this.glow.intensity = lerp(prevK?.glow ?? fx.glow?.intensity, cur?.glow ?? fx.glow?.intensity, 0.9) * (1 + beatK * 0.25);
    // drop sparkle: one burst at the head per flash
    for (const f of fx.flashes ?? []) if (f.sparkle !== false && t >= f.t && t - f.t < 0.05 && this.lastFlash !== f.t) { this.lastFlash = f.t; flashAt(headPos); }
    // beams: rise in with the road lead, sweep with time, pulse on the beat
    if (this.beams.length) {
      const D = ShowFx; const dirty = this.dirty; dirty.clear();
      for (const b of this.beams) {
        const dt = t - (b.t - 2.2);
        let k = dt < 0 ? 0 : dt > 0.6 ? 1 : smooth(dt / 0.6); if (t > b.t + 14) k = Math.max(0, 1 - (t - b.t - 14) / 1.5);
        const sw = Math.sin(t * 1.3 + b.ph) * 0.45, sw2 = Math.cos(t * 0.9 + b.ph) * 0.3;
        D.sc.set(k * (1 + beatK * 0.25), b.h * k, k * (1 + beatK * 0.25)); D.tr.set(b.x, b.y, b.z); Quaternion.RotationYawPitchRollToRef(0, sw, sw2, D.q);
        Matrix.ComposeToRef(D.sc, D.q, D.tr, D.m); D.m.copyToArray(this.beamBufs[b.tpl], b.idx * 16); dirty.add(b.tpl);
      }
      for (const i of dirty) { this.beamMeshes[i].thinInstanceBufferUpdated('matrix'); this.beamMats[i].alpha = 0.12 + beatK * 0.1; }
    }
    // sparkles: appear with the road lead, twinkle, gone 20 s after
    if (this.ps) {
      const P = (this.ps as any).particles as any[];
      for (const p of P) {
        const s = this.sparks[p.sid ?? 0]; if (!s) continue;
        const vis = t > s.t - 2.2 && t < s.t + 20 ? 1 : 0;
        const tw = 0.55 + 0.45 * Math.sin(t * 3 + s.ph);
        p.size = vis * s.s * (tw + beatK * 0.6);
        p.color.set(s.c.r, s.c.g, s.c.b, vis);
      }
    }
  }

  dispose() {
    this.glow?.dispose(); this.glow = null; this.ps?.dispose(); this.ps = null;
    for (const o of this.own) o.dispose(); this.own = []; this.beamMeshes = []; this.beams = []; this.sparks = [];
    const ip = this.scene.imageProcessingConfiguration; ip.exposure = 1; ip.contrast = 1; ip.vignetteEnabled = false;
  }
}
