import { CreateBox, CreatePlane, Matrix, Mesh, Quaternion, Scene, StandardMaterial, TransformNode, Vector3, Vector4, VertexBuffer } from './bjs';
import { HEAD_VEC, spanPos, type Route } from '../core/path';
import type { Dressing, DressingProp, Palette } from '../core/types';
import { buildKind, hex, shade, uvRect, type Materials } from './prefabs';

interface Inst { tpl: number; idx: number; t: number; x: number; y: number; z: number; yaw: number; s: number; sy: number; r: number; h: number; k: number; hide: number; }
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const pop = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : 1 + 0.18 * Math.sin(Math.PI * x) - (1 - x) * (1 - x) * (1 - x) * 1.18 * (1 - x)); // overshoot rise

export function defaultProps(p: Palette, colors?: string[]): DressingProp[] {
  // v2.7: dressing.colors = theme colours (e.g. sampled from the level art) [light, mid, accent, dark, foliage]
  const c = colors ?? [];
  const light = c[0] ?? p.road, mid = c[1] ?? p.ambient, acc = c[2] ?? p.line, dark = c[3] ?? p.roadSide, g = c[4] ?? p.ground;
  return [
    { kind: 'box', size: [1.8, 2.6, 1.8], color: shade(light, -0.03), weight: 3, scale: [0.7, 1.3], scaleY: [0.6, 2.2] },
    { kind: 'group', parts: [{ kind: 'box', pos: [0, 0.8, 0], size: [1.5, 1.6, 1.5], color: shade(mid, 0.05) }, { kind: 'box', pos: [0, 1.95, 0], size: [1.0, 0.7, 1.0], color: shade(light, -0.02) }], weight: 2, scale: [0.8, 1.3], scaleY: [0.8, 1.6] },
    { kind: 'group', parts: [{ kind: 'cylinder', pos: [0, 0.45, 0], size: [0.3, 0.9, 0.3], color: dark }, { kind: 'cone', pos: [0, 1.8, 0], size: [1.5, 2.4, 1.5], color: c[4] ? g : shade(g, -0.28) }], weight: 2.5, scale: [0.7, 1.25], scaleY: [0.8, 1.4] },
    { kind: 'box', size: [0.8, 0.8, 0.8], color: acc, weight: 1.5, scale: [0.6, 1.1], scaleY: [0.6, 1.4] },
    { kind: 'box', size: [1.1, 0.9, 1.1], color: dark, weight: 1.2, scale: [0.6, 1.2], scaleY: [0.6, 2.4] },
  ];
}

/** Deterministic roadside set-dressing drawn with one thin-instanced mesh per prop type. */
export class Dressings {
  meshes: Mesh[] = []; insts: Inst[] = []; private bufs: Float32Array[] = []; private ownMats: StandardMaterial[] = []; private yawMode: string[] = [];
  private static readonly sc = new Vector3(); private static readonly tr = new Vector3(); private static readonly q = new Quaternion(); private static readonly m = new Matrix();
  private lead: number; private bounce: number; private dirty = new Set<number>();
  private lo = 0; // first instance index that may still animate (instances sorted by t)

  constructor(scene: Scene, mats: Materials, root: TransformNode, route: Route, d: Dressing, palette: Palette,
    widthAt: (t: number) => number, hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean, extraBlock: { x: number; z: number; r: number }[]) {
    this.lead = d.lead ?? 2.6; this.bounce = d.bounce ?? 0.12;
    const props = d.props?.length ? d.props : [...defaultProps(palette, d.colors), ...(d.art ?? [])];
    // templates: build the prop, bake part colours into vertex colours, merge into a single mesh
    const sizes: { r: number; h: number }[] = [];
    for (const [i, pr] of props.entries()) {
      if (pr.src) { const t = artTemplate(scene, mats, pr, i); t.mesh.parent = root; sizes.push(t.size); this.meshes.push(t.mesh); this.yawMode.push(pr.face ?? (pr.as === 'crate' || pr.as === 'tile' ? 'random' : pr.as === 'card' ? 'oncoming' : 'road')); continue; }
      this.yawMode.push('random');
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
      mesh.material = mat; this.ownMats.push(mat); mesh.parent = root; mesh.isPickable = false; mesh.alwaysSelectAsActiveMesh = true; mesh.name = 'dress' + i;
      this.meshes.push(mesh);
    }
    // deterministic placement
    let seed = (d.seed ?? 7) >>> 0;
    const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
    const secAt = (t: number) => { let s = { t: 0, density: d.density ?? 3.6, near: d.near ?? [0.4, 4] as [number, number], props: undefined as number[] | undefined, off: false }; for (const x of d.sections ?? []) if (x.t <= t + 1e-9) s = { t: x.t, density: x.density ?? d.density ?? 3.6, near: x.near ?? d.near ?? [0.4, 4], props: x.props, off: !!x.off }; return s; };
    const weights = props.map(p => p.weight ?? 1);
    if (!d.props?.length && d.art?.length) {
      // dressing.artShare: fraction of placements drawn from the art props (default 0.5); weights inside each group stay relative
      const nDef = props.length - d.art.length; const share = Math.min(0.95, Math.max(0, d.artShare ?? 0.5));
      let sd = 0, sa = 0; weights.forEach((w, i) => { if (i < nDef) sd += w; else sa += w; });
      if (sa > 0 && share > 0) { const f = (share / (1 - share)) * sd / sa; for (let i = nDef; i < weights.length; i++) weights[i] *= f; }
    }
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
              // art props face the road (front = local -z points at the road: yaw = atan2(-fx,-fz) with f = -side*right) or the oncoming line
              const ym = this.yawMode[tpl];
              const yaw = ym === 'road' ? Math.atan2(rx * side, rz * side) : ym === 'oncoming' ? Math.atan2(rx * side * 0.6 + hx * 0.8, rz * side * 0.6 + hz * 0.8) : [0, Math.PI / 2, Math.PI, -Math.PI / 2][Math.floor(rnd() * 4)];
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
    this.meshes.forEach((m, i) => { m.thinInstanceSetBuffer('matrix', this.bufs[i], 16, false); m.thinInstanceCount = counts[i]; m.freezeWorldMatrix(); m.doNotSyncBoundingInfo = true; });
    for (const mt of this.ownMats) mt.freeze();
  }

  private write(it: Inst, beatK: number) {
    const k = pop(it.k) * (1 - smooth(it.hide));
    const b = 1 + beatK;
    const D = Dressings; // no per-frame allocations: compose into cached scratch objects
    D.sc.set(it.s * k, it.sy * k * b, it.s * k); D.tr.set(it.x, it.y, it.z); Quaternion.RotationYawPitchRollToRef(it.yaw, 0, 0, D.q);
    Matrix.ComposeToRef(D.sc, D.q, D.tr, D.m);
    D.m.copyToArray(this.bufs[it.tpl], it.idx * 16); this.dirty.add(it.tpl);
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

  private flush() { for (const i of this.dirty) { this.meshes[i].thinInstanceBufferUpdated('matrix'); } this.dirty.clear(); } // meshes are alwaysSelectAsActiveMesh: no per-frame bounding refresh

  dispose() { for (const m of this.ownMats) m.dispose(); for (const m of this.meshes) m.dispose(); this.ownMats = []; this.meshes = []; this.insts = []; }
}

/** v2.7 textured dressing template: one mesh with UVs on the shared (cached) art material, base at y=0 like the primitive templates.
 *  Front = local -z. as: facade (box, art on the 4 sides, roof sampled from the art centre) | card (thin upright panel) | crate (art on every face) | tile (flat floor decal). */
function artTemplate(scene: Scene, mats: Materials, pr: DressingProp, i: number): { mesh: Mesh; size: { r: number; h: number } } {
  const as = pr.as ?? 'facade'; const uv = uvRect(pr.uv); const alpha = pr.alpha ?? /\.png$/i.test(pr.src ?? '');
  const cx = (uv.x + uv.z) / 2, cy = (uv.y + uv.w) / 2; const dot = new Vector4(cx - 0.01, cy - 0.01, cx + 0.01, cy + 0.01);
  let mesh: Mesh; let w: number, h: number, dd: number;
  if (as === 'tile') {
    w = pr.size?.[0] ?? 3; dd = pr.size?.[2] || pr.size?.[1] || 3; h = 0.05;
    mesh = CreatePlane('dressArt' + i, { width: w, height: dd, frontUVs: uv, backUVs: uv, sideOrientation: Mesh.DOUBLESIDE }, scene);
    mesh.rotation.x = Math.PI / 2; mesh.position.y = 0.03; mesh.bakeCurrentTransformIntoVertices();
  } else if (as === 'card') {
    w = pr.size?.[0] ?? 2.4; h = pr.size?.[1] ?? 2.4; dd = pr.size?.[2] ?? 0.12;
    mesh = CreateBox('dressArt' + i, { width: w, height: h, depth: dd, faceUV: [uv, uv, dot, dot, dot, dot], wrap: true }, scene);
    mesh.position.y = h / 2; mesh.bakeCurrentTransformIntoVertices();
  } else {
    w = pr.size?.[0] ?? 3; h = pr.size?.[1] ?? 4; dd = pr.size?.[2] ?? 3;
    const side = uv; const top = as === 'crate' ? uv : dot;
    mesh = CreateBox('dressArt' + i, { width: w, height: h, depth: dd, faceUV: [side, side, side, side, top, top], wrap: true }, scene);
    mesh.position.y = h / 2; mesh.bakeCurrentTransformIntoVertices();
  }
  mesh.material = mats.textured(pr.src ?? '', { alpha, emissive: pr.glow ?? 0.3 });
  mesh.isPickable = false; mesh.alwaysSelectAsActiveMesh = true;
  return { mesh, size: { r: Math.max(w, dd) / 2, h } };
}
