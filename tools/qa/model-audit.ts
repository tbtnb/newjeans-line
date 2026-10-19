// OMG-C model audit harness (dev server: /tools/qa/model-audit.html). Loads each FINAL glb (post gltfpack) like the game does and
// reports geometry problems; renders 4 views (front-3/4, back-3/4, side, top) with BACK-FACE CULLING ON so flipped faces show as holes.
import { Engine } from '@babylonjs/core/Engines/engine';
import { Scene } from '@babylonjs/core/scene';
import { ArcRotateCamera } from '@babylonjs/core/Cameras/arcRotateCamera';
import { Viewport } from '@babylonjs/core/Maths/math.viewport';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { Color3, Color4 } from '@babylonjs/core/Maths/math.color';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import { loadModel } from '../../src/render/scenec/assets';
const eng = new Engine(document.getElementById('c') as HTMLCanvasElement, true, { preserveDrawingBuffer: true });
const scene = new Scene(eng); scene.clearColor = new Color4(0.85, 0.83, 0.8, 1);
const mat = new StandardMaterial('m', scene); mat.disableLighting = true; mat.emissiveColor = Color3.White(); mat.diffuseColor = Color3.Black(); mat.backFaceCulling = true;
const cams = [[-Math.PI / 2 - 0.6, 1.2], [Math.PI / 2 - 0.6, 1.2], [0, 1.45], [-Math.PI / 2, 0.02]].map(([a, b], i) => { const c = new ArcRotateCamera('c' + i, a, b, 10, Vector3.Zero(), scene); c.viewport = new Viewport(i * 0.25, 0, 0.25, 1); c.fov = 0.5; return c; });
scene.activeCameras = cams;
function audit(t: { pos: Float32Array; idx: Uint32Array }, h: number) {
  const P = t.pos, I = t.idx, nT = I.length / 3, eps = h * 1e-4;
  // weld by position
  const key = (i: number) => `${Math.round(P[i * 3] / eps)},${Math.round(P[i * 3 + 1] / eps)},${Math.round(P[i * 3 + 2] / eps)}`;
  const wid = new Map<string, number>(), W = new Int32Array(P.length / 3); for (let i = 0; i < W.length; i++) { const k = key(i); let w = wid.get(k); if (w === undefined) { w = wid.size; wid.set(k, w); } W[i] = w; }
  const par = new Int32Array(wid.size).map((_, i) => i); const f = (x: number): number => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
  let degen = 0; const dupe = new Set<string>(); let dupes = 0;
  const v = (i: number) => [P[i * 3], P[i * 3 + 1], P[i * 3 + 2]];
  const area: number[] = [], nrm: number[][] = [];
  for (let t3 = 0; t3 < nT; t3++) { const a = W[I[t3 * 3]], b = W[I[t3 * 3 + 1]], c = W[I[t3 * 3 + 2]]; par[f(a)] = f(b); par[f(b)] = f(c);
    const A = v(I[t3 * 3]), B = v(I[t3 * 3 + 1]), C = v(I[t3 * 3 + 2]); const u = [B[0] - A[0], B[1] - A[1], B[2] - A[2]], w = [C[0] - A[0], C[1] - A[1], C[2] - A[2]];
    const n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]], ar = Math.hypot(n[0], n[1], n[2]) / 2; area.push(ar); nrm.push(ar > 0 ? n.map(x => x / (2 * ar)) : [0, 0, 0]);
    if (ar < h * h * 1e-7) degen++; const s = [a, b, c].sort((x, y) => x - y).join(':'); if (dupe.has(s)) dupes++; else dupe.add(s); }
  // islands
  const isl = new Map<number, { tris: number[]; min: number[]; max: number[] }>();
  for (let t3 = 0; t3 < nT; t3++) { const r = f(W[I[t3 * 3]]); let o = isl.get(r); if (!o) { o = { tris: [], min: [1e9, 1e9, 1e9], max: [-1e9, -1e9, -1e9] }; isl.set(r, o); } o.tris.push(t3);
    for (let k = 0; k < 3; k++) { const p = v(I[t3 * 3 + k]); for (let d = 0; d < 3; d++) { o.min[d] = Math.min(o.min[d], p[d]); o.max[d] = Math.max(o.max[d], p[d]); } } }
  const L = [...isl.values()]; const gap = h * 0.012;
  const touch = (a: typeof L[0], b: typeof L[0]) => [0, 1, 2].every(d => a.min[d] <= b.max[d] + gap && b.min[d] <= a.max[d] + gap);
  // floating: island off the ground whose bbox touches no other island (follow connectivity from ground islands)
  const grounded = new Set<number>(); const q: number[] = []; L.forEach((o, i) => { if (o.min[1] < h * 0.02) { grounded.add(i); q.push(i); } });
  while (q.length) { const i = q.pop()!; L.forEach((o, j) => { if (!grounded.has(j) && touch(L[i], o)) { grounded.add(j); q.push(j); } }); }
  const floating = L.map((o, i) => ({ o, i })).filter(x => !grounded.has(x.i)).map(x => ({ tris: x.o.tris.length, y: +x.o.min[1].toFixed(3), c: x.o.min.map((m, d) => +((m + x.o.max[d]) / 2).toFixed(2)) }));
  // inverted closed islands (signed volume < 0) and open boundary edges per island
  let inverted = 0, openIsl = 0;
  for (const o of L) { const E = new Map<string, number>(); let vol = 0;
    for (const t3 of o.tris) { const ids = [0, 1, 2].map(k => W[I[t3 * 3 + k]]); for (let k = 0; k < 3; k++) { const a = ids[k], b = ids[(k + 1) % 3], kk = a < b ? a + ':' + b : b + ':' + a; E.set(kk, (E.get(kk) ?? 0) + 1); }
      const A = v(I[t3 * 3]), B = v(I[t3 * 3 + 1]), C = v(I[t3 * 3 + 2]); vol += (A[0] * (B[1] * C[2] - B[2] * C[1]) - A[1] * (B[0] * C[2] - B[2] * C[0]) + A[2] * (B[0] * C[1] - B[1] * C[0])) / 6; }
    let open = 0; for (const n of E.values()) if (n === 1) open++;
    if (open === 0 && vol > 0 && o.tris.length > 3) inverted++; /* Babylon loads glTF left-handed: outward closed parts have negative volume here */ if (open > 0 && o.tris.length > 8) openIsl++; }
  // z-fighting: coplanar overlapping tris from different islands (bucketed by plane)
  const bucket = new Map<string, number[]>(); const dOf = new Float64Array(nT); const isOf = new Int32Array(nT); L.forEach((o, i) => o.tris.forEach(t3 => isOf[t3] = i));
  for (let t3 = 0; t3 < nT; t3++) { if (area[t3] < h * h * 1e-5) continue; const n = nrm[t3], A = v(I[t3 * 3]); const d = n[0] * A[0] + n[1] * A[1] + n[2] * A[2]; dOf[t3] = d;
    const k = `${Math.round(n[0] * 60)},${Math.round(n[1] * 60)},${Math.round(n[2] * 60)},${Math.round(d / (h * 0.004))}`; (bucket.get(k) ?? bucket.set(k, []).get(k)!).push(t3); }
  let zf = 0; const zfAt: number[][] = [];
  const inTri = (p: number[], t3: number, n: number[]) => { const ax = Math.abs(n[0]) > Math.abs(n[1]) ? (Math.abs(n[0]) > Math.abs(n[2]) ? 0 : 2) : (Math.abs(n[1]) > Math.abs(n[2]) ? 1 : 2); const [i, j] = [0, 1, 2].filter(x => x !== ax);
    const T = [0, 1, 2].map(k => v(I[t3 * 3 + k])); const s = (a: number[], b: number[], c: number[]) => (b[i] - a[i]) * (c[j] - a[j]) - (b[j] - a[j]) * (c[i] - a[i]);
    const d1 = s(T[0], T[1], p), d2 = s(T[1], T[2], p), d3 = s(T[2], T[0], p); return (d1 > 0 && d2 > 0 && d3 > 0) || (d1 < 0 && d2 < 0 && d3 < 0); };
  for (const arr of bucket.values()) { if (arr.length < 2 || arr.length > 400) continue;
    for (let x = 0; x < arr.length; x++) for (let y = x + 1; y < arr.length; y++) { const a = arr[x], b = arr[y]; if (isOf[a] === isOf[b] || Math.abs(dOf[a] - dOf[b]) > h * 0.0012) continue;
      const cA = [0, 1, 2].map(d => (P[I[a * 3] * 3 + d] + P[I[a * 3 + 1] * 3 + d] + P[I[a * 3 + 2] * 3 + d]) / 3);
      if (inTri(cA, b, nrm[a])) { zf++; if (zfAt.length < 3) zfAt.push(cA.map(z => +z.toFixed(2))); } } }
  return { tris: nT, islands: L.length, degen, dupes, floating: floating.length, floatingAt: floating.slice(0, 4), inverted, openIslands: openIsl, zfight: zf, zfAt };
}
(window as any).auditModel = async (id: string) => {
  for (const m of [...scene.meshes]) m.dispose();
  const t = await loadModel(scene, '/', id, 1, id); t.container?.dispose();
  const r = audit(t, 1);
  const m = new Mesh('x', scene); const vd = new VertexData(); vd.positions = t.pos; vd.colors = t.col; vd.indices = t.idx; vd.applyToMesh(m); m.material = mat;
  let x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9; for (let i = 0; i < t.pos.length; i += 3) { x0 = Math.min(x0, t.pos[i]); x1 = Math.max(x1, t.pos[i]); z0 = Math.min(z0, t.pos[i + 2]); z1 = Math.max(z1, t.pos[i + 2]); }
  const R = Math.max(1, x1 - x0, z1 - z0) * 1.15 + 0.4; for (const c of cams) { c.target.set((x0 + x1) / 2, 0.5, (z0 + z1) / 2); c.radius = R * 3.2; }
  await scene.whenReadyAsync(); for (let i = 0; i < 3; i++) scene.render(); return r;
};
(window as any).auditReady = true;
eng.runRenderLoop(() => {});
