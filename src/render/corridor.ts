// Corridor scenery (layout.corridor, schema v2.9): a far band of big set pieces (towers, arch rows, spotlight rigs,
// floating balloons, garden flowers/lanterns, curtains) lining both sides of a forward route, glowing floor light strips
// that chase with the beat, floor emblems, and finale fireworks. Everything is placed at load from the route (mean
// corridor = flowAnchor + RoadGrid clearance), so it survives a re-chart. Rendering: one thin-instanced quad per item and
// light group; only instances inside [t - tail, t + lead] are written each frame (compacted buffers, no allocations).
import { Color3, Matrix, Mesh, ParticleSystem, Quaternion, Scene, StandardMaterial, Texture, TransformNode, Vector3, VertexData } from './bjs';
import { anchor, flowAnchor, type Route } from '../core/path';
import type { CorridorSpec } from '../core/types';
import { hex } from './prefabs';

interface Inst { t: number; x: number; y: number; z: number; w: number; h: number; ph: number; yaw: number; }
interface Layer { mesh: Mesh; mat: StandardMaterial; buf: Float32Array; cap: number; list: Inst[]; lo: number; mode: 'bill' | 'flat'; float: number; tilt: number; rise: boolean;
  base: Color3; tex: Texture | null; lights: 'beat' | 'chase' | 'none' | 'strip'; grp: number; nGrp: number; add: boolean; alpha: number; }
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

function quad(scene: Scene, name: string, flat: boolean) {
  // unit quad, pivot at the bottom centre (upright) or centre (flat, facing up); front = -z for upright
  const m = new Mesh(name, scene); const vd = new VertexData();
  vd.positions = flat ? [-0.5, 0, -0.5, 0.5, 0, -0.5, 0.5, 0, 0.5, -0.5, 0, 0.5] : [-0.5, 0, 0, 0.5, 0, 0, 0.5, 1, 0, -0.5, 1, 0];
  vd.uvs = flat ? [0, 0, 1, 0, 1, 1, 0, 1] : [0, 0, 1, 0, 1, 1, 0, 1];
  vd.indices = flat ? [0, 2, 1, 0, 3, 2] : [0, 2, 1, 0, 3, 2];
  vd.normals = flat ? [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0] : [0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1];
  vd.applyToMesh(m); return m;
}

export class Corridor {
  private layers: Layer[] = []; private own: (Mesh | StandardMaterial | Texture | ParticleSystem)[] = [];
  private fw: { t: number; x: number; y: number; z: number; c: Color3; n: number }[] = []; private fwNext = 0; private ps: ParticleSystem | null = null; private fwAt = new Vector3();
  private lastT = -1e9; private beatI = 0;
  private lead: number; private tail: number;
  private static readonly sc = new Vector3(); private static readonly tr = new Vector3(); private static readonly q = new Quaternion(); private static readonly m = new Matrix();
  /** instances placed (for reports / tests) */
  count = 0;

  constructor(private scene: Scene, root: TransformNode, route: Route, private spec: CorridorSpec, artBase: string, quality: 'high' | 'low',
    widthAt: (t: number) => number, hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean, sparkTex: Texture | null, private beats: number[]) {
    this.lead = spec.lead ?? 6; this.tail = spec.tail ?? 4;
    let seed = 7; const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
    const lists: Inst[][] = spec.items.map(() => []);
    const skip = quality === 'low' ? 2 : 1;
    // ---- far band set pieces
    for (const b of spec.bands ?? []) {
      let k = 0;
      for (let t = b.t0 + (b.phase ?? 0); t <= b.t1; t += b.every, k++) {
        if (k % skip) continue;
        for (const side of (b.sides ?? 2) === 2 ? [1, -1] : [k % 2 ? -1 : 1]) {
          const ii = b.items[(k + (side < 0 ? (b.mirror ? 0 : 1) : 0)) % b.items.length]; const it = spec.items[ii];
          const sc = (b.scale?.[0] ?? 1) + rnd() * ((b.scale?.[1] ?? 1) - (b.scale?.[0] ?? 1));
          const w = it.size[0] * sc, h = it.size[1] * sc;
          const y = (b.y?.[0] ?? 0) + rnd() * ((b.y?.[1] ?? 0) - (b.y?.[0] ?? 0));
          // beside the actual road at t, offset across the corridor (flow frame), so pieces line the screen's left/right and
          // never stand ahead of the line; pushed out until clear of every road segment (incl. later zig-zags)
          let off = widthAt(t) / 2 + b.near[0] + rnd() * (b.near[1] - b.near[0]) + (it.flat ? w / 2 : w * 0.3);
          const clear = Math.max(w * 0.3 + 1.2, it.flat ? w / 2 + 0.6 : h * 0.36);
          const r0 = anchor(route, t, 0, 0, 0).pos, f0 = flowAnchor(route, t, 0, 0, 0).pos, f1 = flowAnchor(route, t, 1, 0, 0).pos;
          const rx = f1.x - f0.x, rz = f1.z - f0.z;
          const at = (o: number) => ({ x: r0.x + rx * side * o, y: r0.y + y, z: r0.z + rz * side * o });
          let a = at(off); let tries = 0;
          while (hits(a.x, a.z, clear, a.y - 2 - y, a.y + 3) && tries++ < 12) { off += 1.0; a = at(off); }
          if (tries > 12) continue;
          const yaw = it.flat ? rnd() * Math.PI * 2 : 0;
          lists[ii].push({ t, x: a.x, y: a.y - 0.6 + (it.flat ? 0.04 : 0), z: a.z, w, h: it.flat ? w : h, ph: rnd() * 6.28, yaw });
        }
      }
    }
    // ---- layers per item; 'chase' items split into two groups lit on alternate beats
    spec.items.forEach((it, ii) => {
      const L = lists[ii].sort((a, b) => a.t - b.t); if (!L.length) return;
      const tex = new Texture(artBase + it.src, scene, false, true, Texture.TRILINEAR_SAMPLINGMODE); tex.hasAlpha = true; tex.anisotropicFilteringLevel = 1; this.own.push(tex);
      const nG = it.lights === 'chase' ? 2 : 1;
      for (let g = 0; g < nG; g++) {
        const list = L.filter((_, i) => i % nG === g);
        const mesh = quad(scene, 'cor_' + ii + '_' + g, !!it.flat); mesh.parent = root;
        // unlit look: emissive texture (level = brightness, per light group) + the same texture as diffuse for its alpha
        const et = g === 0 ? tex : tex.clone(); if (g) this.own.push(et); et.level = it.glow ?? 1;
        const mat = new StandardMaterial('corM_' + ii + '_' + g, scene); mat.disableLighting = true; mat.diffuseTexture = tex; mat.emissiveTexture = et; mat.diffuseColor = Color3.Black(); mat.emissiveColor = Color3.Black(); mat.specularColor = Color3.Black();
        if (it.add) { mat.alphaMode = 1; mat.useAlphaFromDiffuseTexture = true; mat.backFaceCulling = false; mat.disableDepthWrite = true; }
        else { mat.transparencyMode = 1; mat.useAlphaFromDiffuseTexture = true; mat.alphaCutOff = it.cut ?? 0.4; mat.backFaceCulling = false; } // alpha test: no sorting, cheap
        const base = new Color3(1, 1, 1).scale(it.glow ?? 1);
        mesh.material = mat; mesh.isPickable = false; mesh.alwaysSelectAsActiveMesh = true; mesh.doNotSyncBoundingInfo = true;
        const cap = Math.min(list.length, spec.maxActive ?? 48); const buf = new Float32Array(Math.max(1, cap) * 16);
        mesh.thinInstanceSetBuffer('matrix', buf, 16, false); mesh.thinInstanceCount = 0;
        this.layers.push({ mesh, mat, buf, cap, list, lo: 0, mode: it.flat ? 'flat' : 'bill', float: it.float ?? 0, tilt: it.tilt ?? spec.tilt ?? 0.5, rise: it.rise !== false, base, tex: et, lights: it.lights ?? 'none', grp: g, nGrp: nG, add: !!it.add, alpha: it.alpha ?? 1 });
        this.own.push(mesh, mat); this.count += list.length;
      }
    });
    // ---- floor light strips: glowing dots parallel to the corridor, chasing forward with the beat (4 phase groups)
    if (sparkTex) for (const f of spec.floor ?? []) {
      const groups: Inst[][] = [[], [], [], []]; let k = 0;
      for (let t = f.t0; t <= f.t1; t += f.every * skip, k++) for (const o of f.offsets) for (const side of [1, -1]) {
        const off = widthAt(t) / 2 + o; const r0 = anchor(route, t, 0, 0, 0).pos, f0 = flowAnchor(route, t, 0, 0, 0).pos, f1 = flowAnchor(route, t, 1, 0, 0).pos;
        const a = { x: r0.x + (f1.x - f0.x) * side * off, y: r0.y, z: r0.z + (f1.z - f0.z) * side * off }; const s = f.size ?? 0.9;
        if (hits(a.x, a.z, s / 2 + 0.5, a.y - 1.5, a.y + 1)) continue;
        groups[k % 4].push({ t, x: a.x, y: a.y - 0.55, z: a.z, w: s, h: s, ph: 0, yaw: 0 });
      }
      const c = hex(f.color);
      groups.forEach((list, g) => {
        if (!list.length) return;
        const mesh = quad(scene, 'corFloor_' + g, true); mesh.parent = root;
        const mat = new StandardMaterial('corFloorM_' + g, scene); mat.disableLighting = true; mat.opacityTexture = sparkTex; mat.emissiveColor = c; mat.diffuseColor = Color3.Black(); mat.specularColor = Color3.Black();
        mat.alphaMode = 1; mat.disableDepthWrite = true; mat.backFaceCulling = false;
        mesh.material = mat; mesh.isPickable = false; mesh.alwaysSelectAsActiveMesh = true; mesh.doNotSyncBoundingInfo = true;
        const cap = Math.min(list.length, (spec.maxActive ?? 48) * 2); const buf = new Float32Array(Math.max(1, cap) * 16);
        mesh.thinInstanceSetBuffer('matrix', buf, 16, false); mesh.thinInstanceCount = 0;
        this.layers.push({ mesh, mat, buf, cap, list, lo: 0, mode: 'flat', float: 0, tilt: 0, rise: false, base: c, tex: null, lights: 'strip', grp: g, nGrp: 4, add: true, alpha: f.alpha ?? 0.8 });
        this.own.push(mesh, mat); this.count += list.length;
      });
    }
    // ---- fireworks: bursts high above the far band on given times
    if (sparkTex && spec.fireworks?.length) {
      for (const f of spec.fireworks) {
        const side = rnd() < 0.5 ? -1 : 1; const a = flowAnchor(route, f.t + 1.2, side * (widthAt(f.t) / 2 + (f.near ?? 12)), 0, 0).pos;
        const cs = f.colors ?? ['#ffd27a']; this.fw.push({ t: f.t, x: a.x, y: a.y + (f.height ?? 12), z: a.z, c: hex(cs[Math.floor(rnd() * cs.length)]), n: Math.round((f.amount ?? 90) / skip) });
      }
      this.fw.sort((a, b) => a.t - b.t);
      const ps = new ParticleSystem('corFireworks', quality === 'high' ? 700 : 300, scene);
      ps.particleTexture = sparkTex; ps.blendMode = ParticleSystem.BLENDMODE_ADD; ps.emitRate = 0; ps.manualEmitCount = 0; ps.emitter = this.fwAt;
      ps.minEmitBox = new Vector3(-0.2, -0.2, -0.2); ps.maxEmitBox = new Vector3(0.2, 0.2, 0.2);
      ps.direction1 = new Vector3(-1, -0.6, -1); ps.direction2 = new Vector3(1, 1, 1); ps.minEmitPower = 5; ps.maxEmitPower = 9;
      ps.minLifeTime = 1.1; ps.maxLifeTime = 1.8; ps.minSize = 0.5; ps.maxSize = 1.1; ps.gravity = new Vector3(0, -5, 0);
      ps.colorDead.set(0, 0, 0, 0); ps.updateSpeed = 1 / 60; ps.start(); this.ps = ps; this.own.push(ps);
    }
  }

  update(t: number, beatK: number, camPos: Vector3) {
    // beat index (parity drives the chase groups)
    const B = this.beats;
    if (t < this.lastT - 0.5) { this.beatI = 0; this.fwNext = 0; for (const l of this.layers) l.lo = 0; while (this.fwNext < this.fw.length && this.fw[this.fwNext].t < t) this.fwNext++; }
    while (this.beatI + 1 < B.length && B[this.beatI + 1] <= t) this.beatI++;
    const D = Corridor; const lead = this.lead, tail = this.tail;
    for (const L of this.layers) {
      const list = L.list; while (L.lo < list.length && list[L.lo].t < t - tail) L.lo++;
      let n = 0;
      for (let i = L.lo; i < list.length && n < L.cap; i++) {
        const s = list[i]; if (s.t > t + lead) break;
        const age = t - (s.t - lead); const e = L.rise ? smooth(age / 0.9) : 1;
        let y = s.y; if (L.mode === 'bill') y += -(1 - e) * s.h * 0.9 + (L.float ? Math.sin(t * 1.4 + s.ph) * L.float : 0);
        if (L.mode === 'bill') { const dx = camPos.x - s.x, dz = camPos.z - s.z; const pitch = Math.atan2(camPos.y - y - s.h * 0.5, Math.sqrt(dx * dx + dz * dz)) * L.tilt; Quaternion.RotationYawPitchRollToRef(Math.atan2(-dx, -dz), pitch, 0, D.q); D.sc.set(s.w, s.h, 1); }
        else { Quaternion.RotationYawPitchRollToRef(s.yaw, 0, 0, D.q); const k = L.lights === 'strip' ? 1 : e; D.sc.set(s.w * k, 1, s.h * k); }
        D.tr.set(s.x, y, s.z); Matrix.ComposeToRef(D.sc, D.q, D.tr, D.m); D.m.copyToArray(L.buf, n * 16); n++;
      }
      L.mesh.thinInstanceCount = n; L.mesh.isVisible = n > 0; if (n) L.mesh.thinInstanceBufferUpdated('matrix');
      // lights
      let k = 1;
      if (L.lights === 'beat') k = 0.82 + 0.4 * beatK;
      else if (L.lights === 'chase') k = (this.beatI % 2 === L.grp ? 0.8 + 0.55 * beatK : 0.8);
      else if (L.lights === 'strip') k = (this.beatI % 4 === L.grp ? 0.55 + 0.45 * beatK : 0.45);
      if (L.lights === 'strip') L.mat.alpha = L.alpha * k; else if (L.tex) L.tex.level = L.base.r * k;
    }
    // fireworks
    if (this.ps) while (this.fwNext < this.fw.length && this.fw[this.fwNext].t <= t) {
      const f = this.fw[this.fwNext++]; if (t - f.t > 0.3) continue;
      this.fwAt.set(f.x, f.y, f.z); this.ps.color1.set(f.c.r, f.c.g, f.c.b, 1); this.ps.color2.set(Math.min(1, f.c.r + 0.3), Math.min(1, f.c.g + 0.3), Math.min(1, f.c.b + 0.3), 1);
      this.ps.manualEmitCount = f.n;
    }
    this.lastT = t;
  }

  dispose() { for (const o of this.own) o.dispose(); this.own = []; this.layers = []; this.ps = null; }
}
