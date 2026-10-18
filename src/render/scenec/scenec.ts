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
import { TransformNode } from '@babylonjs/core/Meshes/transformNode';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { Color3 } from '@babylonjs/core/Maths/math.color';
import { Quaternion, Vector3 } from '@babylonjs/core/Maths/math.vector';
import type { Route } from '../../core/path';
import type { SceneCSpec } from '../../core/types';
import { activeRange, place, type CChunk, type CInst, type CPlacement, type CSet } from './place';
import { loadModel, placeholders, type Template } from './assets';

export type Tier = 'high' | 'low';
export const TIERS: Record<Tier, { density: Record<string, number>; ahead: number; behind: number; lod: number }> = {
  high: { density: { ground: 1, mid: 1, sky: 1, anim: 1 }, ahead: 8, behind: 3, lod: 35 },
  low: { density: { ground: 0.5, mid: 0.7, sky: 0.6, anim: 0 }, ahead: 6, behind: 2, lod: 22 },
};
const hash = (x: number, z: number) => { const s = Math.sin(x * 12.9898 + z * 78.233) * 43758.5453; return s - Math.floor(s); };
const spring = (x: number) => x <= 0 ? 0 : 1 - Math.exp(-x * 7) * Math.cos(x * 13);
const hexRGB = (h: string) => { const n = parseInt(h.replace('#', ''), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; };

interface TI { id: string; mesh: Mesh; mats: Float32Array; cols: Float32Array; cap: number; items: CInst[]; tris: number }
interface Piv { node: TransformNode; kind: string; i: number; base: Quaternion | null; baseS: Vector3; baseP: Vector3 }
interface SetE { def: CSet; node: TransformNode; hinge: TransformNode; far: Mesh | null; near: TransformNode | null; nearMeshes: Mesh[]; piv: Piv[]; tris: number; on: boolean; lodFar: boolean }

export interface CStats { chunks: [number, number]; chunkMeshes: number; types: number; instances: number; sets: number; tris: number; zone: number; models: number; /** visible tris if every asset were modelled at its full spec budget */ trisAtBudget: number }

export class SceneC {
  readonly plc: CPlacement; readonly spec: SceneCSpec;
  private tm: Map<string, Template>; private mat: StandardMaterial; private root: TransformNode;
  private types = new Map<string, TI>(); private chunkMesh = new Map<number, Mesh>(); private sets: SetE[] = [];
  private range: [number, number] = [-1, -1]; private tier: Tier; private zoneCols: number[][][];
  private disposed = false; private time = 0; models = 0; last: CStats | null = null;

  constructor(private scene: Scene, parent: TransformNode, route: Route, spec: SceneCSpec, o: { duration: number; widthAt: (t: number) => number; roadH: number; hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean; beats: number[]; base: string; tier: Tier }) {
    this.spec = spec; this.tier = o.tier;
    this.root = new TransformNode('scenec', scene); this.root.parent = parent;
    this.plc = place(spec, route, { duration: o.duration, widthAt: o.widthAt, roadH: o.roadH, hits: o.hits, beats: o.beats });
    this.zoneCols = spec.zones.map(z => z.colors.map(hexRGB));
    this.tm = placeholders(spec);
    const m = new StandardMaterial('paperC', scene);
    m.disableLighting = true; m.diffuseColor = Color3.Black(); m.emissiveColor = Color3.White(); // unlit: emissive x vertex colour x instance colour m.specularColor = Color3.Black(); m.backFaceCulling = false;
    this.mat = m;
    for (const s of this.plc.sets) this.sets.push(this.makeSet(s));
    // swap in built models as they load (placeholders until then; a missing model simply keeps its placeholder)
    for (const [id, a] of Object.entries(spec.assets)) if (a.model) loadModel(scene, o.base, id, a.h, typeof a.model === 'string' ? a.model : id).then(t => { if (this.disposed) { t.container?.dispose(); return; } this.tm.set(id, t); this.models++; this.refreshAsset(id); }).catch(e => console.warn('omg-c model', id, e));
  }

  setTier(t: Tier) { if (t === this.tier) return; this.tier = t; for (const m of this.chunkMesh.values()) m.dispose(); this.chunkMesh.clear(); this.range = [-1, -1]; }

  private keep(it: CInst) { return hash(it.x, it.z) < (TIERS[this.tier].density[it.layer] ?? 1); }
  private colOf(it: CInst, model: boolean) { const c = this.zoneCols[it.zone][it.c] ?? [1, 1, 1]; const k = model ? 0.3 : 0.85; return [1 + (c[0] - 1) * k, 1 + (c[1] - 1) * k, 1 + (c[2] - 1) * k]; }
  private yOf(it: CInst) { return it.layer === 'ground' || it.layer === 'mid' || it.layer === 'land' ? this.plc.chunks[it.chunk].y : it.y; }

  private meshFrom(name: string, t: Template) {
    const m = new Mesh(name, this.scene); const vd = new VertexData(); vd.positions = t.pos; vd.colors = t.col; vd.indices = t.idx; vd.applyToMesh(m, true);
    m.material = this.mat; m.isPickable = false; m.parent = this.root; return m;
  }

  // ---- ground chunks (merged static) ----
  private buildChunk(c: CChunk) {
    const pos: number[] = [], col: number[] = [], idx: number[] = []; const pg = 28;
    const gc = hexRGB(this.spec.zones[c.zone].palette.ground ?? '#eeeeee');
    const y = c.y - 0.004 * (c.i % 3);
    // paper page under the chunk (terraces with the route's falls), slightly darker rim band reads as the page edge
    const x0 = c.minX - pg, x1 = c.maxX + pg, z0 = c.minZ - pg, z1 = c.maxZ + pg;
    pos.push(x0, y, z0, x1, y, z0, x1, y, z1, x0, y, z1); for (let k = 0; k < 4; k++) col.push(gc[0], gc[1], gc[2], 1); idx.push(0, 1, 2, 0, 2, 3);
    for (const it of c.items) {
      if (it.layer !== 'ground' || !this.keep(it)) continue;
      const t = this.tm.get(it.a); if (!t) continue; const ic = this.colOf(it, t.model);
      const cs = Math.cos(it.yaw), sn = Math.sin(it.yaw), s = it.s, i0 = pos.length / 3;
      for (let i = 0; i < t.pos.length; i += 3) {
        const lx = t.pos[i] * s, ly = t.pos[i + 1] * s, lz = t.pos[i + 2] * s;
        pos.push(it.x + lx * cs + lz * sn, y + 0.002 + ly, it.z - lx * sn + lz * cs);
        const j = i / 3 * 4; col.push(t.col[j] * ic[0], t.col[j + 1] * ic[1], t.col[j + 2] * ic[2], 1);
      }
      for (let i = 0; i < t.idx.length; i++) idx.push(t.idx[i] + i0);
    }
    const m = new Mesh(`cchunk${c.i}`, this.scene); const vd = new VertexData(); vd.positions = pos; vd.colors = col; vd.indices = idx; vd.applyToMesh(m, false);
    m.material = this.mat; m.isPickable = false; m.parent = this.root; m.freezeWorldMatrix(); (m as any).__tris = idx.length / 3;
    return m;
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
    for (let i = a; i <= b; i++) for (const it of this.plc.chunks[i].items) if (it.layer !== 'ground' && this.keep(it)) this.typeOf(it.a).items.push(it);
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
        if (it.layer === 'mid') sy = Math.max(0.02, spring(t - (it.t - 5)));               // pops up 5 s before the line passes
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
    node.position.set(s.x, this.plc.chunks[s.chunk].y, s.z); node.rotation.y = s.yaw; node.scaling.setAll(s.s);
    const hinge = new TransformNode('hinge', this.scene); hinge.parent = node;
    const e: SetE = { def: s, node, hinge, far: null, near: null, nearMeshes: [], piv: [], tris: 0, on: true, lodFar: false };
    this.buildSetVisual(e); this.setOn(e, false);
    return e;
  }
  private buildSetVisual(e: SetE) {
    e.far?.dispose(); e.near?.dispose(false, false); e.far = null; e.near = null; e.nearMeshes = []; e.piv = [];
    const t = this.tm.get(e.def.a)!; e.tris = t.tris;
    e.far = this.meshFrom(`cfar_${e.def.a}`, t); e.far.parent = e.hinge;
    if (t.container) {
      const inst = t.container.instantiateModelsToScene(n => `${n}_${e.def.t}`, false);
      const r = new TransformNode(`cnear_${e.def.a}`, this.scene); r.parent = e.hinge; r.scaling.setAll(t.scale);
      for (const n of inst.rootNodes) n.parent = r;
      for (const m of r.getChildMeshes()) { m.material = this.mat; m.isPickable = false; e.nearMeshes.push(m as Mesh); }
      for (const n of r.getDescendants(false) as TransformNode[]) {
        const mm = /pivot_([a-z]+)(\d*)/i.exec(n.name); if (!mm || mm[1] === 'root') continue;
        e.piv.push({ node: n, kind: mm[1].toLowerCase(), i: +(mm[2] || 0), base: n.rotationQuaternion?.clone() ?? null, baseS: n.scaling.clone(), baseP: n.position.clone() });
      }
      e.near = r;
    }
    e.lodFar = !e.near; this.applyLod(e);
  }
  private applyLod(e: SetE) { e.far?.setEnabled(e.on && (e.lodFar || !e.near)); e.near?.setEnabled(e.on && !e.lodFar && !!e.near); }
  private setOn(e: SetE, on: boolean) { if (e.on === on) return; e.on = on; e.node.setEnabled(on); this.applyLod(e); }
  private animSet(e: SetE, t: number, beatK: number, cam: Vector3 | null) {
    const d = e.def; const on = t >= d.popAt - 1.5 && t <= d.t + 4; this.setOn(e, on); if (!on) return;
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
    if (this.spec.assets[id]?.layer === 'ground') { for (const m of this.chunkMesh.values()) m.dispose(); this.chunkMesh.clear(); this.range = [-1, -1]; }
    for (const e of this.sets) if (e.def.a === id) { this.buildSetVisual(e); const on = e.on; e.on = !on; this.setOn(e, on); }
  }

  update(t: number, dt: number, beatK: number, cam: Vector3 | null) {
    this.time += dt; const T = TIERS[this.tier];
    const [a, b] = activeRange(this.plc.chunks, t, T.behind, T.ahead);
    if (a !== this.range[0] || b !== this.range[1]) {
      for (const [i, m] of this.chunkMesh) if (i < a || i > b) { m.dispose(); this.chunkMesh.delete(i); }
      for (let i = a; i <= b; i++) if (!this.chunkMesh.has(i)) this.chunkMesh.set(i, this.buildChunk(this.plc.chunks[i]));
      this.range = [a, b]; this.refill(a, b);
    }
    this.writeTypes(t, beatK);
    let tris = 0, inst = 0, sets = 0, tb = 0; const A = this.spec.assets;
    for (const e of this.sets) { this.animSet(e, t, beatK, cam); if (e.on) { sets++; tris += e.tris; tb += Math.max(e.tris, A[e.def.a]?.tris ?? 0); } }
    for (const [i, m] of this.chunkMesh) { tris += (m as any).__tris; tb += 2; for (const it of this.plc.chunks[i].items) if (it.layer === 'ground' && this.keep(it)) tb += Math.max(this.tm.get(it.a)?.tris ?? 0, A[it.a]?.tris ?? 0); }
    let types = 0; for (const ti of this.types.values()) if (ti.items.length) { types++; inst += ti.items.length; tris += ti.items.length * ti.tris; tb += ti.items.length * Math.max(ti.tris, A[ti.id]?.tris ?? 0); }
    let zone = 0; for (let i = 0; i < this.spec.zones.length; i++) if (this.spec.zones[i].t0 <= t) zone = i;
    this.last = { chunks: [a, b], chunkMeshes: this.chunkMesh.size, types, instances: inst, sets, tris, zone, models: this.models, trisAtBudget: tb };
  }

  dispose() {
    this.disposed = true;
    for (const [id, t] of this.tm) if (t.container) { t.container.dispose(); this.tm.delete(id); }
    this.root.dispose(false, false); this.mat.dispose();
  }
}
