/**
 * Concept C placement (pure, no Babylon): route chunks (fixed arc length), deterministic scatter of each zone's layers along
 * both sides of the route, and set pieces by time/side. Re-running on a new chart re-flows everything along the new route.
 */
import { anchor, flowAnchor, type Route } from '../../core/path';
import type { SceneCSpec, SceneCZone } from '../../core/types';

export interface CInst { a: string; layer: string; x: number; y: number; z: number; yaw: number; s: number; c: number; zone: number; t: number; chunk: number; hi?: boolean }
export interface CSet extends CInst { popAt: number; label?: string; /** v6: zone hero (key camera nudges toward it) */ hero?: boolean }
export interface CImp { k: string; x: number; y: number; z: number; yaw: number; s: number; zone: number }
export interface CChunk { imp?: CImp[]; i: number; t0: number; t1: number; zone: number; minX: number; maxX: number; minZ: number; maxZ: number; y: number; items: CInst[];
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
  // key camera path (behind and above the flow); direction from a clamped +-1.5 s window so it never degenerates at the song ends
  const camPath: { t: number; x: number; z: number; gx: number; gz: number }[] = [];
  for (let t = 0; t <= o.duration; t += 0.25) { const ta = Math.max(0, Math.min(o.duration - 3, t - 1.5)), p0 = flowAnchor(route, ta, 0, 0, 0).pos, p1 = flowAnchor(route, ta + 3, 0, 0, 0).pos, p = flowAnchor(route, t, 0, 0, 0).pos;
    const dx = p1.x - p0.x, dz = p1.z - p0.z, L = Math.hypot(dx, dz) || 1; camPath.push({ t, x: p.x - dx / L * 37, z: p.z - dz / L * 37, gx: p.x - dx / L * 4, gz: p.z - dz / L * 4 }); }
  const nearCam = (x: number, z: number, t: number) => { const i0 = Math.max(0, Math.floor((t - 10) * 4)), i1 = Math.min(camPath.length - 1, Math.ceil((t + 3) * 4));
    for (let i = i0; i <= i1; i++) { const c = camPath[i]; if ((c.x - x) ** 2 + (c.z - z) ** 2 < 28 * 28) return true; } return false; };
  /** near band: the bottom of the key camera's frame (ground ~4 m behind the flow point, i.e. around the head); big masses there fill the screen */
  const MASSY = /tree|pine|forest|hill|hedge|bush/;   // v7: only green masses are kept out of the near band
  const nearBand = (x: number, z: number, t: number, r: number) => { const i0 = Math.max(0, Math.floor((t - 4) * 4)), i1 = Math.min(camPath.length - 1, Math.ceil((t + 2) * 4));
    for (let i = i0; i <= i1; i++) { const c = camPath[i]; if ((c.gx - x) ** 2 + (c.gz - z) ** 2 < r * r) return true; } return false; };
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
        if (L.layer === 'mid' && h > 2.6 && nearBand(a.pos.x, a.pos.z, t, (MASSY.test(L.asset) ? 16 : 3) + r)) { rejected++; continue; }   // big green masses stay out of the near band; houses / towers may hug the road (v7)
        const rp = anchor(route, t).pos;
        const yaw = A.shape === 'far' || L.layer === 'mid' ? Math.atan2(rp.x - a.pos.x, rp.z - a.pos.z) : R() * Math.PI * 2;
        const ci = chunkAt(t);
        const gy = L.layer === 'ground' || L.layer === 'mid' ? groundY(chunks[ci], a.pos.x, a.pos.z) + y0 : a.pos.y - o.roadH + y0;
        const col = () => (L.colors ?? [0])[Math.floor(R() * (L.colors ?? [0]).length)];
        chunks[ci].items.push({ a: L.asset, layer: L.layer, x: a.pos.x, y: gy, z: a.pos.z, yaw, s, c: col(), zone: zi, t, chunk: ci, ...(L.hi ? { hi: true } : {}) });
        placed++;
        if (L.cluster) {   // members around the centre (blob) or continuing along the road at the same offset (row); each one must clear the road too
          const Cn = L.cluster, m = Math.round(Cn.n[0] + R() * ((Cn.n[1] ?? Cn.n[0]) - Cn.n[0]));
          const q = anchor(route, t + 0.1).pos, v = Math.max(0.5, Math.hypot(q.x - rp.x, q.z - rp.z) / 0.1);
          for (let j = 1; j < m; j++) {
            let x: number, zz: number, ty = t, my = yaw; const ms = s * (0.8 + 0.4 * R());
            if (Cn.row) { ty = t + Math.ceil(j / 2) * (j % 2 ? 1 : -1) * Cn.r * s / v; if (ty < z.t0 || ty > t1) continue;
              const b = edge < 6 ? anchor(route, ty, off, 0, 0) : flowAnchor(route, ty, off, 0, 0); x = b.pos.x; zz = b.pos.z; const bp = anchor(route, ty).pos; my = Math.atan2(bp.x - x, bp.z - zz); }
            else { const an = R() * Math.PI * 2, rr = Cn.r * s * Math.sqrt(0.15 + 0.85 * R()); x = a.pos.x + Math.cos(an) * rr; zz = a.pos.z + Math.sin(an) * rr; my = L.layer === 'mid' ? yaw + (R() - 0.5) * 0.8 : R() * Math.PI * 2; }
            if (o.hits(x, zz, r * ms / s + pad, a.pos.y - 1, a.pos.y + A.h * ms) || (A.h * ms > 2.6 && nearBand(x, zz, ty, (MASSY.test(L.asset) ? 16 : 3) + r * ms / s))) { rejected++; continue; }
            const cj = chunkAt(ty);
            chunks[cj].items.push({ a: L.asset, layer: L.layer, x, y: groundY(chunks[cj], x, zz) + y0, z: zz, yaw: my, s: ms, c: col(), zone: zi, t: ty, chunk: cj, ...(L.hi ? { hi: true } : {}) }); placed++;
          }
        }
        break;
      }
    }
  });
  // impostor carpet: sprite cards facing back along the flow (towards the key camera), clear of every road segment
  spec.zones.forEach((z, zi) => {
    const I = z.impostors; if (!I) return; const t1 = Math.min(z.t1, o.duration); const W = I.sprites.reduce((a, b) => a + b[1], 0);
    const n = Math.round(I.count);
    for (let k = 0; k < n; k++) {
      const t = z.t0 + (k + R()) / n * (t1 - z.t0), side = R() < 0.5 ? -1 : 1, w = o.widthAt(t);
      let u = R() * W, id = I.sprites[0][0]; for (const [sid, sw] of I.sprites) { u -= sw; if (u <= 0) { id = sid; break; } }
      const s0 = I.scale[0] + R() * (I.scale[1] - I.scale[0]);
      const edge = I.near[0] + Math.pow(R(), 0.8) * (I.near[1] - I.near[0]);
      const s = s0 * (0.5 + 0.5 * Math.min(1, Math.max(0, (edge - 13) / 42)));   // v5: near cards mid-sized (x0.5 at 13 m -> full at 55 m), no mint blobs at the frame edges
      const a = flowAnchor(route, t, side * (w / 2 + edge), 0, 0);
      if (o.hits(a.pos.x, a.pos.z, 1.5 * s + 2.0, a.pos.y - 30, a.pos.y + 30) || nearCam(a.pos.x, a.pos.z, t)) { rejected++; continue; }
      const cp = camPath[Math.min(camPath.length - 1, Math.round(Math.max(0, t - 1.0) * 4))];   // face where the camera is when this card is in view
      const ci = chunkAt(t); const c = chunks[ci]; (c.imp ??= []).push({ k: id, x: a.pos.x, y: groundY(c, a.pos.x, a.pos.z), z: a.pos.z, yaw: Math.atan2(cp.x - a.pos.x, cp.z - a.pos.z), s, zone: zi });
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
      // heroes: footprint from the model width and hugging the road (the portrait key camera is only ~20 m wide at its look point)
      const hero = !!sp.hero, sc = sp.scale ?? 1, w = o.widthAt(sp.t), r = hero ? (A.w ?? A.h) * sc * 0.42 : A.h * sc * 0.45; const side = sp.side || 1;
      let off = side * (w / 2 + sp.dist + r); let a = flowAnchor(route, sp.t, off, 0, 0);
      for (let k = 0; k < 24 && o.hits(a.pos.x, a.pos.z, hero ? r * 0.8 + 0.8 : r + 1.5, a.pos.y - 1, a.pos.y + A.h * sc); k++) { off += side * (hero ? 1.0 : 1.5); a = flowAnchor(route, sp.t, off, 0, 0); }
      const rp = anchor(route, sp.t).pos;
      const popAt = drop && sp.t - drop.t < 8 && sp.t >= drop.t - 0.5 ? drop.t : snap(sp.t - 4);
      const sc0 = chunks[chunkAt(sp.t)];
      for (const [ea, en] of sp.entourage ?? []) {   // entourage: decor ringed around the hero (front half first), clear of the road
        const EA = spec.assets[ea]; if (!EA) continue;
        for (let k = 0; k < en; k++) for (let att = 0; att < 4; att++) {
          const ang = Math.atan2(rp.x - a.pos.x, rp.z - a.pos.z) + (R() - 0.5) * Math.PI * (att < 2 ? 1.3 : 2), rr = r * 0.75 + 1.5 + R() * 7;
          const x = a.pos.x + Math.sin(ang) * rr, zz = a.pos.z + Math.cos(ang) * rr, es = 1.3 + R() * 0.5;
          if (o.hits(x, zz, Math.max(EA.h, EA.w ?? 0) * es * 0.35 + 0.8, a.pos.y - 1, a.pos.y + EA.h * es)) { rejected++; continue; }
          const ci = chunkAt(sp.t); const ec = chunks[ci];
          ec.items.push({ a: ea, layer: 'mid', x, y: groundY(ec, x, zz), z: zz, yaw: Math.atan2(rp.x - x, rp.z - zz), s: es, c: (z.layers[0]?.colors ?? [0])[Math.floor(R() * (z.layers[0]?.colors ?? [0]).length)], zone: zi, t: sp.t, chunk: ci }); placed++; break;
        }
      }
      sets.push({ a: sp.asset, layer: 'land', x: a.pos.x, y: groundY(sc0, a.pos.x, a.pos.z), z: a.pos.z, yaw: Math.atan2(rp.x - a.pos.x, rp.z - a.pos.z), s: sc, c: 0, zone: zi, t: sp.t, chunk: chunkAt(sp.t), popAt, label: sp.label, ...(sp.hi ? { hi: true } : {}), ...(sp.hero ? { hero: true } : {}) });
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
