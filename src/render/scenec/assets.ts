/**
 * Concept C asset templates: flat-shaded placeholders for every spec asset (available synchronously), swapped for the
 * meshopt-compressed glb models in public/models/omg-c/ as they arrive. A template is plain arrays already scaled to the
 * spec height (metres, standing on y=0, front +Z), so it can feed thin-instance meshes and per-chunk merges alike.
 * Models with named pivots also keep their AssetContainer so landmarks can be instantiated with animatable nodes.
 */
import type { Scene } from '@babylonjs/core/scene';
import type { AssetContainer } from '@babylonjs/core/assetContainer';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import type { SceneCSpec } from '../../core/types';
import { placeholder } from './geo';

export interface Template { id: string; pos: Float32Array; col: Float32Array; idx: Uint32Array; tris: number; model: boolean; container?: AssetContainer; scale: number }

export function fromGeo(id: string, g: { pos: number[]; col: number[]; idx: number[] }, h: number, w?: number, d?: number): Template {
  let ymax = 0, x0 = 1e9, x1 = -1e9, z0 = 1e9, z1 = -1e9;
  for (let i = 0; i < g.pos.length; i += 3) { ymax = Math.max(ymax, g.pos[i + 1]); x0 = Math.min(x0, g.pos[i]); x1 = Math.max(x1, g.pos[i]); z0 = Math.min(z0, g.pos[i + 2]); z1 = Math.max(z1, g.pos[i + 2]); }
  // uniform by height, or fitted to the design footprint when the sheet gives one (flat pieces like the book cover)
  const s = h / (ymax || 1); const sx = w ? w / Math.max(1e-3, x1 - x0) : s, sz = d ? d / Math.max(1e-3, z1 - z0) : s;
  const pos = new Float32Array(g.pos.length); for (let i = 0; i < pos.length; i += 3) { pos[i] = g.pos[i] * sx; pos[i + 1] = g.pos[i + 1] * s; pos[i + 2] = g.pos[i + 2] * sz; }
  return { id, pos, col: Float32Array.from(g.col), idx: Uint32Array.from(g.idx), tris: g.idx.length / 3, model: false, scale: s };
}

export function placeholders(spec: SceneCSpec) {
  const out = new Map<string, Template>();
  for (const [id, a] of Object.entries(spec.assets)) out.set(id, fromGeo(id, placeholder(a.shape), a.h, a.w, a.d));
  return out;
}

let loaderReady: Promise<typeof import('@babylonjs/core/Loading/sceneLoader')> | null = null;
function loader(base: string) {
  if (!loaderReady) loaderReady = (async () => {
    const [sl, mo] = await Promise.all([import('@babylonjs/core/Loading/sceneLoader'), import('@babylonjs/core/Meshes/Compression/meshoptCompression'),
      import('@babylonjs/loaders/glTF/2.0/glTFLoader'), import('@babylonjs/loaders/glTF/2.0/Extensions/EXT_meshopt_compression'), import('@babylonjs/loaders/glTF/2.0/Extensions/KHR_mesh_quantization')]);
    mo.MeshoptCompression.Configuration = { decoder: { url: `${base}meshopt/meshopt_decoder.js` } };
    return sl;
  })();
  return loaderReady;
}

const lin2srgb = (c: number) => Math.pow(Math.max(0, c), 1 / 2.2);

/** Load one model; returns a merged template (glTF linear vertex colours -> sRGB for the unlit material) + its container. */
export async function loadModel(scene: Scene, base: string, id: string, h: number, glb = id): Promise<Template> {
  const sl = await loader(base);
  const c = await sl.LoadAssetContainerAsync(`${base}models/omg-c/${glb}.glb`, scene);
  const pos: number[] = [], col: number[] = [], idx: number[] = []; const v = new Vector3();
  let ymin = 1e9, ymax = -1e9;
  for (const m of c.meshes) {
    const p = m.getVerticesData('position'); const ix = m.getIndices(); if (!p || !ix) continue;
    const cc = m.getVerticesData('color'); const stride = cc ? cc.length / (p.length / 3) : 0;
    const wm = m.computeWorldMatrix(true); const i0 = pos.length / 3;
    for (let i = 0; i < p.length / 3; i++) {
      Vector3.TransformCoordinatesFromFloatsToRef(p[i * 3], p[i * 3 + 1], p[i * 3 + 2], wm, v); pos.push(v.x, v.y, v.z); ymin = Math.min(ymin, v.y); ymax = Math.max(ymax, v.y);
      if (cc) col.push(lin2srgb(cc[i * stride]), lin2srgb(cc[i * stride + 1]), lin2srgb(cc[i * stride + 2]), 1); else col.push(1, 1, 1, 1);
    }
    for (let i = 0; i < ix.length; i++) idx.push(ix[i] + i0);
  }
  // colours of the container's own meshes too (landmark instances share this geometry)
  for (const m of c.meshes) {
    const cc = m.getVerticesData('color'); if (!cc) continue; const n = m.getTotalVertices(); const stride = cc.length / n;
    const out = new Float32Array(n * 4); for (let i = 0; i < n; i++) { out[i * 4] = lin2srgb(cc[i * stride]); out[i * 4 + 1] = lin2srgb(cc[i * stride + 1]); out[i * 4 + 2] = lin2srgb(cc[i * stride + 2]); out[i * 4 + 3] = 1; }
    m.setVerticesData('color', out, false, 4);
  }
  const s = h / Math.max(1e-3, ymax - Math.min(0, ymin));
  for (let i = 0; i < pos.length; i++) pos[i] *= s;
  return { id, pos: Float32Array.from(pos), col: Float32Array.from(col), idx: Uint32Array.from(idx), tris: idx.length / 3, model: true, container: c, scale: s };
}
