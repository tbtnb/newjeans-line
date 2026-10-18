/**
 * Concept C placement (pure, no Babylon): route chunks (fixed arc length), deterministic scatter of each zone's layers along
 * both sides of the route, and set pieces by time/side. Re-running on a new chart re-flows everything along the new route.
 */
import { anchor, flowAnchor, type Route } from '../../core/path';
import type { SceneCSpec, SceneCZone } from '../../core/types';

export interface CInst { a: string; layer: string; x: number; y: number; z: number; yaw: number; s: number; c: number; zone: number; t: number; chunk: number; hi?: boolean }
export interface CSet extends CInst { popAt: number; label?: string }
export interface CChunk { i: number; t0: number; t1: number; zone: number; minX: number; maxX: number; minZ: number; maxZ: number; y: number; items: CInst[];
  /** raised page at the chunk's own road level (climbs): pad shrunk so it never covers a lower road; decor inside it sits on it */
  terr?: { y: number; pad: number } }
export interface CPlacement { chunks: CChunk[]; sets: CSet[]; stats: { placed: number; rejected: number } }

export function rng(seed: number) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

/** chunk boundaries (song times) every `len` metres of route (horizontal arc length; airborne spans count) */
export function chunkTimes(route: Route, duration: number, len: number): number[] {
  const out = [0]; let acc = 0;
  for (const s of route.spans) {
    const t1 = Math.min(s.t1, duration); if (t1 <= s.t0) continue;
    let t = s.t0; const v = s.v;
    while (acc + v * (t1 - t) >= len) { t += (len - acc) / v; acc = 0; out.push(t); }
    acc += v * (t1 - t);
  }
  if (duration - out[out.length - 1] > 0.3) out.push(duration); else out[out.length - 1] = duration;
  return out;
}

export function zoneIndexAt(spec: SceneCSpec, t: number) { let k = 0; for (let i = 0; i < spec.zones.length; i++) if (spec.zones[i].t0 <= t + 1e-6) k = i; return k; }

export interface PlaceOpts { duration: number; widthAt: (t: number) => number; roadH: number; hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean; density?: Partial<Record<string, number>>; seed?: number; beats?: number[] }

export function place(spec: SceneCSpec, route: Route, o: PlaceOpts): CPlacement {
  const R = rng(o.seed ?? 20261018);
  const ct = chunkTimes(route, o.duration, spec.chunk);
  const chunks: CChunk[] = ct.slice(0, -1).map((t0, i) => {
    const t1 = ct[i + 1]; let minX = 1e9, maxX = -1e9, minZ = 1e9, maxZ = -1e9, y = 1e9;
    for (let k = 0; k <= 8; k++) { const p = anchor(route, t0 + (t1 - t0) * k / 8).pos; minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x); minZ = Math.min(minZ, p.z); maxZ = Math.max(maxZ, p.z); y = Math.min(y, p.y); }
    return { i, t0, t1, zone: zoneIndexAt(spec, (t0 + t1) / 2), minX, maxX, minZ, maxZ, y: y - o.roadH, items: [] };
  });
  // a chunk's paper page reaches PAGE m past its route bbox: it must sit below every road it overlaps (falls / ramps), so the
  // page height is the lowest road among all chunks whose bbox touches the page rect (pages still terrace, never cover the road)
  const PAGE = spec.pagePad ?? 28; const own = chunks.map(c => c.y);
  for (const c of chunks) for (let j = 0; j < chunks.length; j++) { const o = chunks[j];
    if (o.maxX >= c.minX - PAGE && o.minX <= c.maxX + PAGE && o.maxZ >= c.minZ - PAGE && o.minZ <= c.maxZ + PAGE && own[j] < c.y) c.y = own[j]; }
  // terraces: where the page had to drop more than 0.5 m below its own road, raise a second page at road level whose pad stops
  // short of every lower road (2 m margin for the road width); kept only when it still reaches >= 5 m past the route
  chunks.forEach((c, k) => {
    const yh = own[k]; if (yh - c.y < 0.5) return; let pad = PAGE;
    for (let j = 0; j < chunks.length; j++) { const o = chunks[j]; if (own[j] >= yh - 0.5) continue;
      const gx = Math.max(o.minX - c.maxX, c.minX - o.maxX), gz = Math.max(o.minZ - c.maxZ, c.minZ - o.maxZ); pad = Math.min(pad, Math.max(gx, gz) - 2); }
    if (pad >= 5) c.terr = { y: yh, pad };
  });
  const groundY = (c: CChunk, x: number, z: number) => c.terr && x >= c.minX - c.terr.pad && x <= c.maxX + c.terr.pad && z >= c.minZ - c.terr.pad && z <= c.maxZ + c.terr.pad ? c.terr.y : c.y;
  const chunkAt = (t: number) => { let lo = 0, hi = chunks.length - 1; while (lo < hi) { const m = (lo + hi + 1) >> 1; if (chunks[m].t0 <= t) lo = m; else hi = m - 1; } return lo; };
  let placed = 0, rejected = 0;
  const clearNear = spec.clear?.near ?? 1.0, groundMaxH = spec.clear?.groundMaxH ?? 0.3;
  spec.zones.forEach((z: SceneCZone, zi) => {
    const t1 = Math.min(z.t1, o.duration);
    for (const L of z.layers) {
      const A = spec.assets[L.asset]; if (!A) continue;
      const n = Math.round(L.count * (o.density?.[L.layer] ?? 1));
      for (let k = 0; k < n; k++) for (let att = 0; att < 6; att++) {   // a spot over another road segment retries elsewhere (zig-zag routes)
        const t = z.t0 + (k + R()) / n * (t1 - z.t0);
        const side = R() < 0.5 ? -1 : 1, w = o.widthAt(t);
        const s = (L.scale[0] ?? 1) + R() * ((L.scale[1] ?? 1) - (L.scale[0] ?? 1)); const h = A.h * s;
        // tall things keep 1.5 road widths clear of every road segment (ground cover < groundMaxH may hug the edge)
        const minEdge = h < groundMaxH ? Math.max(L.near[0], 0.25) : Math.max(L.near[0], 1.5 * w);
        const edge = minEdge + Math.pow(R(), L.layer === 'ground' ? 1.6 : 1) * Math.max(0, L.near[1] - minEdge);
        const off = side * (w / 2 + edge);
        const a = edge < 6 ? anchor(route, t, off, 0, 0) : flowAnchor(route, t, off, 0, 0);
        const y0 = (L.y[0] ?? 0) + R() * ((L.y[1] ?? 0) - (L.y[0] ?? 0));
        const r = Math.max(0.15, Math.max(A.h, A.w ?? 0, A.d ?? 0) * s * (A.shape === 'far' ? 0.2 : 0.35));   // wide pieces (paper hills) need their width
        const pad = h < groundMaxH ? 0.15 : clearNear + 1.0 * w;
        if (y0 < 4 && o.hits(a.pos.x, a.pos.z, r + pad, a.pos.y - 1, a.pos.y + h)) { rejected++; continue; }
        const rp = anchor(route, t).pos;
        const yaw = A.shape === 'far' || L.layer === 'mid' ? Math.atan2(rp.x - a.pos.x, rp.z - a.pos.z) : R() * Math.PI * 2;
        const ci = chunkAt(t);
        const gy = L.layer === 'ground' || L.layer === 'mid' ? groundY(chunks[ci], a.pos.x, a.pos.z) + y0 : a.pos.y - o.roadH + y0;
        chunks[ci].items.push({ a: L.asset, layer: L.layer, x: a.pos.x, y: gy, z: a.pos.z, yaw, s, c: (L.colors ?? [0])[Math.floor(R() * (L.colors ?? [0]).length)], zone: zi, t, chunk: ci, ...(L.hi ? { hi: true } : {}) });
        placed++; break;
      }
    }
  });
  // set pieces: landmark / hero props at (t, side), pushed outward until clear of every road segment, facing the road
  const beats = o.beats ?? [];
  const snap = (t: number) => { let b = t, d = 1e9; for (const x of beats) { const e = Math.abs(x - t); if (e < d) { d = e; b = x; } } return d < 0.3 ? b : t; };
  const sets: CSet[] = [];
  spec.zones.forEach((z, zi) => {
    const drop = (z.moments ?? []).find(m => /DROP/i.test(m.label));
    for (const sp of z.setpieces) {
      const A = spec.assets[sp.asset]; if (!A || sp.t > o.duration) continue;
      const sc = sp.scale ?? 1, w = o.widthAt(sp.t), r = A.h * sc * 0.45; const side = sp.side || 1;
      let off = side * (w / 2 + sp.dist + r); let a = flowAnchor(route, sp.t, off, 0, 0);
      for (let k = 0; k < 24 && o.hits(a.pos.x, a.pos.z, r + 1.5, a.pos.y - 1, a.pos.y + A.h * sc); k++) { off += side * 1.5; a = flowAnchor(route, sp.t, off, 0, 0); }
      const rp = anchor(route, sp.t).pos;
      const popAt = drop && sp.t - drop.t < 8 && sp.t >= drop.t - 0.5 ? drop.t : snap(sp.t - 4);
      const sc0 = chunks[chunkAt(sp.t)];
      sets.push({ a: sp.asset, layer: 'land', x: a.pos.x, y: groundY(sc0, a.pos.x, a.pos.z), z: a.pos.z, yaw: Math.atan2(rp.x - a.pos.x, rp.z - a.pos.z), s: sc, c: 0, zone: zi, t: sp.t, chunk: chunkAt(sp.t), popAt, label: sp.label, ...(sp.hi ? { hi: true } : {}) });
    }
  });
  return { chunks, sets, stats: { placed, rejected } };
}

/** chunk index range [a, b] active at song time t (window behind/ahead in seconds) */
export function activeRange(chunks: CChunk[], t: number, behind: number, ahead: number): [number, number] {
  let a = 0; while (a < chunks.length - 1 && chunks[a].t1 < t - behind) a++;
  let b = a; while (b < chunks.length - 1 && chunks[b + 1].t0 <= t + ahead) b++;
  return [a, b];
}
