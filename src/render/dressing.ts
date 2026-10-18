import { Matrix, Mesh, Quaternion, Scene, StandardMaterial, TransformNode, Vector3, VertexBuffer } from './bjs';
import { HEAD_VEC, spanPos, type Route } from '../core/path';
import type { Dressing, DressingProp, Palette } from '../core/types';
import { buildKind, hex, shade, type Materials } from './prefabs';

interface Inst { tpl: number; idx: number; t: number; x: number; y: number; z: number; yaw: number; s: number; sy: number; r: number; h: number; k: number; hide: number; }
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const pop = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : 1 + 0.18 * Math.sin(Math.PI * x) - (1 - x) * (1 - x) * (1 - x) * 1.18 * (1 - x)); // overshoot rise

export function defaultProps(p: Palette): DressingProp[] {
  const light = p.road, dark = p.roadSide, acc = p.line, mid = p.ambient, g = p.ground;
  return [
    { kind: 'box', size: [1.8, 2.6, 1.8], color: shade(light, -0.03), weight: 3, scale: [0.7, 1.3], scaleY: [0.6, 2.2] },
    { kind: 'group', parts: [{ kind: 'box', pos: [0, 0.8, 0], size: [1.5, 1.6, 1.5], color: shade(mid, 0.05) }, { kind: 'box', pos: [0, 1.95, 0], size: [1.0, 0.7, 1.0], color: shade(light, -0.02) }], weight: 2, scale: [0.8, 1.3], scaleY: [0.8, 1.6] },
    { kind: 'group', parts: [{ kind: 'cylinder', pos: [0, 0.45, 0], size: [0.3, 0.9, 0.3], color: dark }, { kind: 'cone', pos: [0, 1.8, 0], size: [1.5, 2.4, 1.5], color: shade(g, -0.28) }], weight: 2.5, scale: [0.7, 1.25], scaleY: [0.8, 1.4] },
    { kind: 'box', size: [0.8, 0.8, 0.8], color: acc, weight: 1.5, scale: [0.6, 1.1], scaleY: [0.6, 1.4] },
    { kind: 'box', size: [1.1, 0.9, 1.1], color: dark, weight: 1.2, scale: [0.6, 1.2], scaleY: [0.6, 2.4] },
  ];
}

/** Deterministic roadside set-dressing drawn with one thin-instanced mesh per prop type. */
export class Dressings {
  meshes: Mesh[] = []; insts: Inst[] = []; private bufs: Float32Array[] = [];
  private lead: number; private bounce: number; private dirty = new Set<number>();
  private lo = 0; // first instance index that may still animate (instances sorted by t)

  constructor(scene: Scene, mats: Materials, root: TransformNode, route: Route, d: Dressing, palette: Palette,
    widthAt: (t: number) => number, hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean, extraBlock: { x: number; z: number; r: number }[]) {
    this.lead = d.lead ?? 2.6; this.bounce = d.bounce ?? 0.12;
    const props = d.props?.length ? d.props : defaultProps(palette);
    // templates: build the prop, bake part colours into vertex colours, merge into a single mesh
    const sizes: { r: number; h: number }[] = [];
    for (const [i, pr] of props.entries()) {
      const holder = new TransformNode('dressTpl' + i, scene);
      buildKind(scene, mats, { ...pr, kind: pr.kind } as any, holder);
      const parts = holder.getChildMeshes(false).filter(m => m instanceof Mesh && m.getTotalVertices() > 0) as Mesh[];
      for (const m of parts) {
        const c = ((m.material as StandardMaterial | null)?.diffuseColor) ?? hex('#ffffff');
        const n = m.getTotalVertices(); const col = new Float32Array(n * 4);
        for (let v = 0; v < n; v++) { col[v * 4] = c.r; col[v * 4 + 1] = c.g; col[v * 4 + 2] = c.b; col[v * 4 + 3] = 1; }
        m.setVerticesData(VertexBuffer.ColorKind, col);
      }
      holder.computeWorldMatrix(true); const bv = holder.getHierarchyBoundingVectors(true);
      sizes.push({ r: Math.max(bv.max.x - bv.min.x, bv.max.z - bv.min.z) / 2, h: bv.max.y - Math.min(0, bv.min.y) });
      const merged = parts.length ? Mesh.MergeMeshes(parts, true, true, undefined, false, false) : null;
      holder.dispose();
      const mesh = merged ?? new Mesh('dressEmpty' + i, scene);
      const mat = new StandardMaterial('dressM' + i, scene); mat.specularColor.set(0.04, 0.04, 0.04);
      mesh.material = mat; mesh.parent = root; mesh.isPickable = false; mesh.alwaysSelectAsActiveMesh = true; mesh.name = 'dress' + i;
      this.meshes.push(mesh);
    }
    // deterministic placement
    let seed = (d.seed ?? 7) >>> 0;
    const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
    const secAt = (t: number) => { let s = { t: 0, density: d.density ?? 3.6, near: d.near ?? [0.4, 4] as [number, number], props: undefined as number[] | undefined, off: false }; for (const x of d.sections ?? []) if (x.t <= t + 1e-9) s = { t: x.t, density: x.density ?? d.density ?? 3.6, near: x.near ?? d.near ?? [0.4, 4], props: x.props, off: !!x.off }; return s; };
    const weights = props.map(p => p.weight ?? 1);
    const pick = (allowed?: number[]) => { const ids = allowed?.length ? allowed.filter(i => i < props.length) : props.map((_, i) => i); let tot = 0; for (const i of ids) tot += weights[i]; let r = rnd() * tot; for (const i of ids) { r -= weights[i]; if (r <= 0) return i; } return ids[ids.length - 1]; };
    const placed: { x: number; z: number; r: number }[] = [...extraBlock];
    const cell = new Map<string, number[]>(); const key = (x: number, z: number) => `${Math.floor(x / 6)},${Math.floor(z / 6)}`;
    for (const [i, b] of placed.entries()) { const k = key(b.x, b.z); (cell.get(k) ?? cell.set(k, []).get(k)!).push(i); }
    const free = (x: number, z: number, r: number) => {
      const cx = Math.floor(x / 6), cz = Math.floor(z / 6);
      for (let a = cx - 2; a <= cx + 2; a++) for (let b = cz - 2; b <= cz + 2; b++) for (const j of cell.get(`${a},${b}`) ?? []) { const q = placed[j]; if (Math.hypot(q.x - x, q.z - z) < q.r + r + 0.35) return false; }
      return true;
    };
    for (const sp of route.spans) {
      if (sp.air) continue;
      const len = sp.v * (sp.t1 - sp.t0); const [hx, hz] = HEAD_VEC[sp.heading]; const rx = hz, rz = -hx;
      for (const side of [1, -1]) {
        let u = rnd() * 2;
        while (u < len) {
          const t = sp.t0 + u / sp.v; const sec = secAt(t);
          const step = 10 / Math.max(0.05, sec.density);
          if (!sec.off) {
            const tpl = pick(sec.props); const pr = props[tpl];
            const s = (pr.scale ? pr.scale[0] + rnd() * (pr.scale[1] - pr.scale[0]) : 1);
            const sy = s * (pr.scaleY ? pr.scaleY[0] + rnd() * (pr.scaleY[1] - pr.scaleY[0]) : 1);
            const r = sizes[tpl].r * s, h = sizes[tpl].h * sy;
            const off = widthAt(t) / 2 + sec.near[0] + rnd() * (sec.near[1] - sec.near[0]) + r;
            const p = spanPos(sp, t); const x = p.x + rx * off * side, z = p.z + rz * off * side;
            if (!hits(x, z, r, p.y - 0.6, p.y + h) && free(x, z, r)) {
              const yaw = [0, Math.PI / 2, Math.PI, -Math.PI / 2][Math.floor(rnd() * 4)];
              const inst: Inst = { tpl, idx: 0, t, x, y: p.y - 0.6, z, yaw, s, sy, r, h, k: 0, hide: 0 };
              this.insts.push(inst); placed.push({ x, z, r }); const kk = key(x, z); (cell.get(kk) ?? cell.set(kk, []).get(kk)!).push(placed.length - 1);
            }
          }
          u += step * (0.6 + rnd() * 0.8);
        }
      }
    }
    this.insts.sort((a, b) => a.t - b.t);
    const counts = this.meshes.map(() => 0);
    for (const it of this.insts) it.idx = counts[it.tpl]++;
    this.bufs = counts.map(n => new Float32Array(Math.max(1, n) * 16));
    this.meshes.forEach((m, i) => { m.thinInstanceSetBuffer('matrix', this.bufs[i], 16, false); m.thinInstanceCount = counts[i]; });
  }

  private write(it: Inst, beatK: number) {
    const k = pop(it.k) * (1 - smooth(it.hide));
    const b = 1 + beatK;
    const m = Matrix.Compose(new Vector3(it.s * k, it.sy * k * b, it.s * k), Quaternion.RotationYawPitchRoll(it.yaw, 0, 0), new Vector3(it.x, it.y, it.z));
    m.copyToArray(this.bufs[it.tpl], it.idx * 16); this.dirty.add(it.tpl);
  }

  /** Reset to time t (restart / checkpoint). */
  seek(t: number) {
    for (const it of this.insts) { it.k = smooth((t - (it.t - this.lead)) / 0.35) >= 1 ? 1 : Math.max(0, Math.min(1, (t - (it.t - this.lead)) / 0.35)); it.hide = 0; this.write(it, 0); }
    this.lo = 0; this.flush();
  }

  /** occludes(x,y,z,r) -> true if the prop would cover the head / road just ahead (screen space). */
  update(t: number, dt: number, beatK: number, occludes: (x: number, y: number, z: number, r: number, h: number) => boolean) {
    while (this.lo < this.insts.length && this.insts[this.lo].t < t - 6) { const it = this.insts[this.lo]; if (it.k < 1 || it.hide > 0) { it.k = 1; it.hide = Math.max(0, it.hide - 1); this.write(it, 0); } this.lo++; }
    for (let i = this.lo; i < this.insts.length; i++) {
      const it = this.insts[i];
      if (it.t - this.lead > t + 0.05) break;
      const k = Math.min(1, Math.max(0, (t - (it.t - this.lead)) / 0.35));
      const near = Math.abs(it.t - t) < 2.5;
      const occ = occludes(it.x, it.y, it.z, it.r, it.h);
      const hide = dt <= 0 ? (occ ? 1 : 0) : Math.max(0, Math.min(1, it.hide + (occ ? 1 : -1) * dt * 7)); // dt 0 = seek/preview: settle instantly
      const bk = near ? beatK * this.bounce : 0;
      if (k !== it.k || hide !== it.hide || near) { it.k = k; it.hide = hide; this.write(it, bk); }
    }
    this.flush();
  }

  private flush() { for (const i of this.dirty) { this.meshes[i].thinInstanceBufferUpdated('matrix'); } if (this.dirty.size) this.meshes.forEach(m => m.thinInstanceRefreshBoundingInfo(false)); this.dirty.clear(); }

  dispose() { for (const m of this.meshes) { m.material?.dispose(); m.dispose(); } this.meshes = []; this.insts = []; }
}
