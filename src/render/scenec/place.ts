/**
 * Concept C placement (pure, no Babylon): route chunks (fixed arc length), deterministic scatter of each zone's layers along
 * both sides of the route, and set pieces by time/side. Re-running on a new chart re-flows everything along the new route.
 */
import { anchor, flowAnchor, type Route } from '../../core/path';
import type { SceneCSpec, SceneCZone } from '../../core/types';

const fr = (x: number, z: number) => { const q = Math.sin(x * 12.9898 + z * 78.233) * 43758.5453; return q - Math.floor(q); };
export interface CInst { a: string; layer: string; x: number; y: number; z: number; yaw: number; s: number; c: number; zone: number; t: number; chunk: number; hi?: boolean; /** v8 palette variant index (rows step it so neighbours differ) */ v?: number }
export interface CSet extends CInst { popAt: number; label?: string; /** v6: zone hero (key camera nudges toward it) */ hero?: boolean }
export interface CImp { k: string; x: number; y: number; z: number; yaw: number; s: number; zone: number }
export interface CChunk { imp?: CImp[]; i: number; t0: number; t1: number; zone: number; minX: number; maxX: number; minZ: number; maxZ: number; y: number; items: CInst[];
  /** raised page at the chunk's own road level (climbs): pad shrunk so it never covers a lower road; decor inside it sits on it */
  terr?: { y: number; pad: number } }
/** v10 raised page bank beside the road: a run of flow-aligned quads (inner -> outer edge) at one top height; decor on it sits on it */
export interface CBank { zone: number; side: number; y: number; base: number; P: number[][]; T: number[]; ci: number[] }
export interface CPlacement { banks: CBank[]; chunks: CChunk[]; sets: CSet[]; stats: { placed: number; rejected: number; rj?: Record<string, number> } }

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

export interface PlaceOpts { duration: number; widthAt: (t: number) => number; roadH: number; hits: (x: number, z: number, r: number, y0: number, y1: number) => boolean; density?: Partial<Record<string, number>>; seed?: number; beats?: number[]; /** v10 key camera elevation (deg) for the head sightline slope */ camPitch?: number }

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
  const groundY0 = (c: CChunk, x: number, z: number) => c.terr && x >= c.minX - c.terr.pad && x <= c.maxX + c.terr.pad && z >= c.minZ - c.terr.pad && z <= c.maxZ + c.terr.pad ? c.terr.y : c.y;
  const chunkAt = (t: number) => { let lo = 0, hi = chunks.length - 1; while (lo < hi) { const m = (lo + hi + 1) >> 1; if (chunks[m].t0 <= t) lo = m; else hi = m - 1; } return lo; };
  // key camera path (behind and above the flow); direction from a clamped +-1.5 s window so it never degenerates at the song ends
  const camPath: { t: number; x: number; z: number; gx: number; gz: number }[] = [];
  for (let t = 0; t <= o.duration; t += 0.25) { const ta = Math.max(0, Math.min(o.duration - 3, t - 1.5)), p0 = flowAnchor(route, ta, 0, 0, 0).pos, p1 = flowAnchor(route, ta + 3, 0, 0, 0).pos, p = flowAnchor(route, t, 0, 0, 0).pos;
    const dx = p1.x - p0.x, dz = p1.z - p0.z, L = Math.hypot(dx, dz) || 1; camPath.push({ t, x: p.x - dx / L * 37, z: p.z - dz / L * 37, gx: p.x - dx / L * 20, gz: p.z - dz / L * 20 }); }   // v9: head-pinned frame bottom ~20 m behind the flow point
  // v8: nothing tall may ever stand between the key camera and the head. Sightline per 0.25 s: from the head (route point) back toward
  // the camera (flow direction, ~44 m out / ~32 m up in portrait); an object of radius r and height h within r + 1.5 m of that line
  // whose top reaches the sightline blocks the head. Checked over every route time within 14 s of the object's own time (zig-zags come back).
  const heads: { x: number; z: number; y: number; ux: number; uz: number }[] = camPath.map(c => { const p = anchor(route, c.t).pos; const dx = c.x - p.x, dz = c.z - p.z, L = Math.hypot(dx, dz) || 1; return { x: p.x, z: p.z, y: p.y, ux: dx / L, uz: dz / L }; });
  const slope = Math.tan((o.camPitch ?? 36) * Math.PI / 180);
  const blocksHead = (x: number, z: number, r: number, y0: number, h: number, t: number) => { const i0 = Math.max(0, Math.floor((t - 14) * 4)), i1 = Math.min(heads.length - 1, Math.ceil((t + 14) * 4));
    for (let i = i0; i <= i1; i++) { const H = heads[i], ex = x - H.x, ez = z - H.z, sAl = ex * H.ux + ez * H.uz; if (sAl < -r || sAl > 46) continue;
      const lat = Math.abs(ex * H.uz - ez * H.ux); if (lat > r + 1.5) continue; const rayY = H.y + 0.6 + Math.max(0, sAl - r) * slope; if (y0 + h > rayY - 0.3) return true; }
    return false; };
  const nearCam = (x: number, z: number, t: number) => { const i0 = Math.max(0, Math.floor((t - 10) * 4)), i1 = Math.min(camPath.length - 1, Math.ceil((t + 3) * 4));
    for (let i = i0; i <= i1; i++) { const c = camPath[i]; if ((c.x - x) ** 2 + (c.z - z) ** 2 < 28 * 28) return true; } return false; };
  /** near band: the bottom of the key camera's frame (ground ~4 m behind the flow point, i.e. around the head); big masses there fill the screen */
  const nearBand = (x: number, z: number, t: number, r: number) => { const i0 = Math.max(0, Math.floor((t - 3) * 4)), i1 = Math.min(camPath.length - 1, Math.ceil((t + 9) * 4));
    for (let i = i0; i <= i1; i++) { const c = camPath[i]; if ((c.gx - x) ** 2 + (c.gz - z) ** 2 < r * r) return true; } return false; };
  // ---- v10 page banks: raised page platforms lining both sides of the road (the keys' pop-up book), runs of 1.6-3.8 s with gaps,
  // each at its own height (stacked book cliffs), inner edge pushed out of the zig-zag until clear of every road, never across the
  // head's sightline, never half under a set piece (a hero either stands fully on a bank or the bank breaks around it)
  const foot = (A: { h: number; w?: number; d?: number }, s: number) => Math.max(A.w ?? A.h * 0.6, A.d ?? 0, 0.5) * s * 0.5;
  const banks: CBank[] = []; const bgrid = new Map<string, number[][]>();
  const inTri = (px: number, pz: number, a: number[], b: number[], c: number[]) => { const d1 = (px - b[0]) * (a[1] - b[1]) - (a[0] - b[0]) * (pz - b[1]), d2 = (px - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (pz - c[1]), d3 = (px - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (pz - a[1]);
    return !((d1 < 0 || d2 < 0 || d3 < 0) && (d1 > 0 || d2 > 0 || d3 > 0)); };
  const bankAt = (x: number, z: number): number | null => { let y: number | null = null; for (const e of bgrid.get(`${Math.floor(x / 4)},${Math.floor(z / 4)}`) ?? []) { const B = banks[e[0]], p = B.P[e[1]], q = B.P[e[1] + 1];
    const A = [p[0], p[1]], Bq = [q[0], q[1]], C = [q[2], q[3]], D = [p[2], p[3]]; if (inTri(x, z, A, Bq, C) || inTri(x, z, A, C, D)) y = Math.max(y ?? -1e9, B.y); } return y; };
  const bankAdd = (bi: number) => { const B = banks[bi]; for (let k = 0; k < B.P.length - 1; k++) { const p = B.P[k], q = B.P[k + 1];
    const xs = [p[0], p[2], q[0], q[2]], zs = [p[1], p[3], q[1], q[3]]; for (let i = Math.floor(Math.min(...xs) / 4); i <= Math.floor(Math.max(...xs) / 4); i++) for (let j = Math.floor(Math.min(...zs) / 4); j <= Math.floor(Math.max(...zs) / 4); j++) { const kk = `${i},${j}`; (bgrid.get(kk) ?? bgrid.set(kk, []).get(kk)!).push([bi, k]); } } };
  const groundY = (c: CChunk, x: number, z: number) => { const g = groundY0(c, x, z), b = bankAt(x, z); return b !== null && b > g ? b : g; };
  /** footprint of radius r at (x,z) lies wholly on one level (not straddling a bank edge; off-bank pieces also keep clear of the 1.5 m cliff strata) */
  const bankOk = (x: number, z: number, r: number) => { if (!banks.length) return true; const c0 = bankAt(x, z), rr = c0 === null ? r + 1.5 : r * 0.85;
    for (let k = 0; k < 8; k++) { const an = k * Math.PI / 4; if (bankAt(x + Math.cos(an) * rr, z + Math.sin(an) * rr) !== c0) return false; } return true; };
  /** v11: a piece straddling a bank edge snaps fully onto the bank (nearest spot within ~2r+2 m), else fully off it; null = no clear spot.
   *  rr = road clearance radius, (y0, h) its vertical span, occ radius for solids */
  const snapBank = (x: number, z: number, r: number, rr: number, y0: number, h: number, occR = 0, tree = false): [number, number] | null => {
    const ok = (px: number, pz: number) => bankOk(px, pz, r) && !o.hits(px, pz, rr, y0 - 1, y0 + h + 3) && !(occR && occHit(px, pz, occR, tree));
    for (const onBank of [true, false]) for (let d = 0.4; d <= 2 * r + 2.2; d += 0.4) for (let k = 0; k < 12; k++) { const an = k * Math.PI / 6 + d, px = x + Math.cos(an) * d, pz = z + Math.sin(an) * d;
      if ((bankAt(px, pz) !== null) === onBank && ok(px, pz)) return [px, pz]; }
    return null; };
  const setPos = (sp: SceneCZone['setpieces'][0]) => { const A = spec.assets[sp.asset]; if (!A) return null;
    const hero = !!sp.hero, sc = sp.scale ?? 1, w = o.widthAt(sp.t), r = hero ? (A.w ?? A.h) * sc * 0.42 : A.h * sc * 0.45; const side = sp.side || 1;
    const H = A.h * sc, cr = hero ? r * 0.8 + 0.8 : r + 1.5;
    if (hero || H >= 8) {   // v10: heroes / landmarks take the clear spot nearest the flow line (the key frame is ~20 m wide): search
      // +-1.5 s along the flow and both sides (own side preferred), first lateral offset clear of every road and of the head sightline
      let best: { a: ReturnType<typeof flowAnchor>; c: number } | null = null;
      for (const dt of [0, 0.5, -0.5, 1, -1, 1.5, -1.5]) for (const sd of [side, -side]) {
        const tt = Math.max(0, Math.min(o.duration, sp.t + dt));
        for (let off = w / 2 + Math.max(0.5, Math.min(sp.dist, 3)) + r * 0.8; off < 40; off += 1) { const a = flowAnchor(route, tt, sd * off, 0, 0);
          if (o.hits(a.pos.x, a.pos.z, cr, a.pos.y - 1, a.pos.y + H) || blocksHead(a.pos.x, a.pos.z, r, a.pos.y, H, sp.t)) continue;
          const c = off - r * 0.8 + 2.5 * Math.abs(dt) + (sd !== side ? 4 : 0); if (!best || c < best.c) best = { a, c }; break; } }
      if (best) return { a: best.a, r, hero, sc, A };
    }
    let off = side * (w / 2 + sp.dist + r); let a = flowAnchor(route, sp.t, off, 0, 0);
    for (let k = 0; k < 24 && o.hits(a.pos.x, a.pos.z, cr, a.pos.y - 1, a.pos.y + H); k++) { off += side * (hero ? 1.0 : 1.5); a = flowAnchor(route, sp.t, off, 0, 0); }
    for (let k = 0; k < 20 && blocksHead(a.pos.x, a.pos.z, r, a.pos.y, H, sp.t); k++) { off += side * 1.5; a = flowAnchor(route, sp.t, off, 0, 0); }   // v8: never between camera and head
    return { a, r, hero, sc, A }; };
  {
    const BR = rng((o.seed ?? 20261018) + 77);
    const SP: { x: number; z: number; r: number; t: number }[] = []; for (const z of spec.zones) for (const sp of z.setpieces) { if (sp.t > o.duration) continue; const q = setPos(sp); if (q) SP.push({ x: q.a.pos.x, z: q.a.pos.z, r: Math.max(q.r, foot(q.A, q.sc)), t: sp.t }); }
    const BT: number[] = []; spec.zones.forEach(z => { const L = z.t1 - z.t0; BT.push(Math.max(1.6, z.t0 + 0.6)); if (L > 20) BT.push(z.t0 + L / 2); });   // open-book spreads (scenec buildBookFg) own those spots
    spec.zones.forEach((z, zi) => {
      const cfg = z.banks; if (cfg === false) return; const HS = cfg?.h ?? [1.3, 1.8, 2.4, 3.0], WS = cfg?.w ?? [9, 15], t1 = Math.min(z.t1, o.duration) - 0.4;
      for (const side of [-1, 1]) {
        let t = z.t0 + 0.3 + BR() * 1.2;
        while (t < t1) {
          const len = 1.6 + BR() * 2.2, h = HS[Math.floor(BR() * HS.length)], W0 = WS[0] + BR() * (WS[1] - WS[0]); const tE = Math.min(t1, t + len);
          type S = { t: number; lin: number; base: number; ci: number; W: number };
          const run: S[] = []; const runs: S[][] = [];
          const cut = () => { if (run.length >= 3) runs.push(run.splice(0)); else run.length = 0; };
          for (let tt = t; tt <= tE + 1e-6; tt += 0.25) {
            if (BT.some(b => Math.abs(b - tt) < 1.2)) { cut(); continue; }
            const ci = chunkAt(tt), c = chunks[ci], f0 = flowAnchor(route, tt, 0, 0, 0).pos, f1 = flowAnchor(route, tt, side, 0, 0).pos, rx = f1.x - f0.x, rz = f1.z - f0.z, fx = -rz * side, fz = rx * side;   // r = outward unit
            const base = groundY0(c, f0.x, f0.z), w = o.widthAt(tt);
            const okAt = (lat: number) => { const x = f0.x + rx * lat, zz = f0.z + rz * lat; return !o.hits(x, zz, 1.3, base - 1, base + h + 2.5); };
            let lin = w / 2 + 2.2; while (lin < 16 && !(okAt(lin - 1.6) && okAt(lin) && okAt(lin + 2))) lin += 0.75;
            if (lin >= 16) { cut(); continue; }
            // set pieces: fully on the bank (widen it) or the bank breaks
            let W = W0, bad = false;
            for (const q of SP) { if (Math.abs(q.t - tt) > 12) continue; const dx = q.x - f0.x, dz = q.z - f0.z, al = dx * fx + dz * fz, lt = dx * rx + dz * rz; if (Math.abs(al) >= q.r + 1.3) continue;
              const ch = Math.sqrt(Math.max(0, (q.r + 1.3) ** 2 - al * al)); if (lt + ch < lin - 1.6 || lt - ch > lin + W + 1.5) continue;
              if (lt - ch >= lin + 0.3 && lt + ch + 0.6 - lin <= 24) W = Math.max(W, lt + ch + 0.6 - lin); else { bad = true; break; } }
            if (bad || !okAt(lin + W * 0.5) || !okAt(lin + W)) { cut(); continue; }
            if (run.length && (Math.abs(run[0].base - base) > 0.3 || Math.abs(run[run.length - 1].lin - lin) > 4)) cut();
            const pi = [f0.x + rx * lin, f0.z + rz * lin], pm = [f0.x + rx * (lin + W * 0.5), f0.z + rz * (lin + W * 0.5)], po = [f0.x + rx * (lin + W), f0.z + rz * (lin + W)];
            if (bankAt(pi[0], pi[1]) !== null || bankAt(pm[0], pm[1]) !== null || bankAt(po[0], po[1]) !== null) { cut(); continue; }
            if (blocksHead(pi[0], pi[1], 1.2, base, h, tt) || blocksHead(pm[0], pm[1], 1.2, base, h, tt)) { cut(); continue; }
            run.push({ t: tt, lin, base, ci, W });
          }
          cut();
          for (const R0 of runs) {   // one width per run (widest set piece), inner edge smoothed outward only
            const W = Math.max(...R0.map(q => q.W)), L = R0.map((q, k) => Math.max(q.lin, R0[k - 1]?.lin ?? 0, R0[k + 1]?.lin ?? 0));
            const B: CBank = { zone: zi, side, y: Math.max(...R0.map(q => q.base)) + h, base: Math.min(...R0.map(q => q.base)), P: [], T: [], ci: [] };
            R0.forEach((q, k) => { const f0 = flowAnchor(route, q.t, 0, 0, 0).pos, f1 = flowAnchor(route, q.t, side, 0, 0).pos, rx = f1.x - f0.x, rz = f1.z - f0.z;
              B.P.push([f0.x + rx * L[k], f0.z + rz * L[k], f0.x + rx * (L[k] + W), f0.z + rz * (L[k] + W)]); B.T.push(q.t); B.ci.push(q.ci); });
            banks.push(B); bankAdd(banks.length - 1);
          }
          t = tE + 0.25 + BR() * 0.7;
        }
      }
    });
  }
  let placed = 0, rejected = 0; const rj: Record<string, number> = {};
  // v8 audit: models no longer clip into each other - tall mid pieces keep their footprints apart (4 m hash grid), set pieces clear them after
  const occ = new Map<string, number[][]>(), oc = (x: number, z: number) => `${Math.floor(x / 4)},${Math.floor(z / 4)}`;
  const occHit = (x: number, z: number, r: number, tree = false) => { const cx = Math.floor(x / 4), cz = Math.floor(z / 4), n = Math.ceil(r / 4) + 2;
    for (let i = -n; i <= n; i++) for (let j = -n; j <= n; j++) for (const q of occ.get(`${cx + i},${cz + j}`) ?? []) if ((q[0] - x) ** 2 + (q[1] - z) ** 2 < ((q[2] + r) * (q[3] && tree ? 0.55 : 0.9)) ** 2) return true; return false; };
  const occAdd = (x: number, z: number, r: number, tree = false) => { const k = oc(x, z); (occ.get(k) ?? occ.set(k, []).get(k)!).push([x, z, r, tree ? 1 : 0]); };   // trees may interleave a little (paper groves), nothing else may
  const clearNear = spec.clear?.near ?? 1.0, groundMaxH = spec.clear?.groundMaxH ?? 0.3;
  spec.zones.forEach((z: SceneCZone, zi) => {
    const t1 = Math.min(z.t1, o.duration);
    // v8: big pieces claim their spots first (view rows, then by height), small decor fills around them
    const big = (L: typeof z.layers[0]) => L.layer !== 'mid' ? -1 : (L.view ? 100 : 0) + (spec.assets[L.asset]?.h ?? 0) * (L.scale[1] ?? 1);
    for (const L of [...z.layers].sort((p, q) => big(q) - big(p))) {
      const A = spec.assets[L.asset]; if (!A) continue;
      const n = Math.round(L.count * (o.density?.[L.layer] ?? 1));
      for (let k = 0; k < n; k++) for (let att = 0; att < 6; att++) {   // a spot over another road segment retries elsewhere (zig-zag routes)
        const T0 = L.tw ? Math.max(z.t0, L.tw[0]) : z.t0, T1 = L.tw ? Math.min(t1, L.tw[1]) : t1;   // v9: optional placement time window
        const t = T0 + (k + R()) / n * (T1 - T0);
        const side = R() < 0.5 ? -1 : 1, w = o.widthAt(t);
        const s = (L.scale[0] ?? 1) + R() * ((L.scale[1] ?? 1) - (L.scale[0] ?? 1)); const h = A.h * s;
        // tall things keep 1.5 road widths clear of every road segment (ground cover < groundMaxH may hug the edge)
        const view = L.view;   // v8 'view' layers: lateral offset from the FLOW line (the key camera's left / right), pushed out of the zig-zag until clear
        const minEdge = h < groundMaxH ? Math.max(L.near[0], 0.25) : h < 1.7 ? Math.max(L.near[0], 0.5) : h < 3.2 ? Math.max(L.near[0], 0.8 * w) : Math.max(L.near[0], 1.5 * w);
        const edge = view ? 99 : minEdge + Math.pow(R(), L.layer === 'ground' ? 1.6 : 1) * Math.max(0, L.near[1] - minEdge);
        let off = view ? side * (view[0] + R() * (view[1] - view[0])) : side * (w / 2 + edge);
        let a = edge < 6 ? anchor(route, t, off, 0, 0) : flowAnchor(route, t, off, 0, 0);
        const y0 = (L.y[0] ?? 0) + R() * ((L.y[1] ?? 0) - (L.y[0] ?? 0));
        const r = Math.max(0.15, Math.max(A.h, A.w ?? 0, A.d ?? 0) * s * (A.shape === 'far' ? 0.2 : 0.35));   // wide pieces (paper hills) need their width
        // v9: low pieces (< 1.7 m) may sit close to the road edge like the keys (they cannot hide a tile); mid-height ones keep a smaller margin
        const pad = h < groundMaxH ? 0.15 : h < 1.7 ? 0.35 + 0.1 * w : h < 3.2 ? clearNear * 0.6 + 0.3 * w : view ? clearNear + 0.5 * w : clearNear + 1.0 * w;
        if (view) for (let k = 0; k < 8 && o.hits(a.pos.x, a.pos.z, r + pad, a.pos.y - 1, a.pos.y + h); k++) { off += side * 1.25; a = flowAnchor(route, t, off, 0, 0); }
        if (y0 < 4 && o.hits(a.pos.x, a.pos.z, r + pad, a.pos.y - 1, a.pos.y + h)) { rejected++; rj[z.id + ' ' + L.asset + ' hit'] = (rj[z.id + ' ' + L.asset + ' hit'] ?? 0) + 1; continue; }
        if (L.layer === 'mid' && h > 1.2 && blocksHead(a.pos.x, a.pos.z, r, a.pos.y + y0, h, t)) { rejected++; rj[z.id + ' ' + L.asset + ' sight'] = (rj[z.id + ' ' + L.asset + ' sight'] ?? 0) + 1; continue; }
        const solid = L.layer === 'mid' && h >= 0.8 && !/fence|bunting|lantern-string|cord/.test(L.asset), fr0 = foot(A, s);
        const isTree = A.shape === 'tree' && !/hedge/.test(L.asset);
        if (solid && occHit(a.pos.x, a.pos.z, fr0, isTree)) { rejected++; rj[z.id + ' ' + L.asset + ' occ'] = (rj[z.id + ' ' + L.asset + ' occ'] ?? 0) + 1; continue; }
        if (L.layer === 'mid' && h > (view ? 3.5 : 2.6) && nearBand(a.pos.x, a.pos.z, t, (L.hug ? 3 : view ? 8 : 9) + r)) { rejected++; rj[z.id + ' ' + L.asset + ' near'] = (rj[z.id + ' ' + L.asset + ' near'] ?? 0) + 1; continue; }   // big pieces stay out of the near band; v7 'hug' layers (lit house rows) may line the road
        { const br = L.layer === 'ground' ? Math.min(r, 0.6) : fr0; if (!bankOk(a.pos.x, a.pos.z, br)) {   // v11: snap onto the bank instead of rejecting
          const q = snapBank(a.pos.x, a.pos.z, br, r + pad, a.pos.y, h, solid ? fr0 : 0, isTree); if (!q) { rejected++; rj[z.id + ' bank'] = (rj[z.id + ' bank'] ?? 0) + 1; continue; }
          a = { ...a, pos: { x: q[0], y: a.pos.y, z: q[1] } } as typeof a; rj[z.id + ' snap'] = (rj[z.id + ' snap'] ?? 0) + 1; } }
        const rp = anchor(route, t).pos;
        const fp = view ? flowAnchor(route, Math.max(0, t - 2.5), 0, 0, 0).pos : rp;   // view pieces face back along the flow (toward the key camera), not sideways
        const yaw = A.shape === 'far' || L.layer === 'mid' ? Math.atan2(fp.x - a.pos.x, fp.z - a.pos.z) + (view ? (R() - 0.5) * 0.5 : 0) : R() * Math.PI * 2;
        const ci = chunkAt(t);
        const gy = L.layer === 'ground' || L.layer === 'mid' ? groundY(chunks[ci], a.pos.x, a.pos.z) + y0 : a.pos.y - o.roadH + y0;
        const col = () => (L.colors ?? [0])[Math.floor(R() * (L.colors ?? [0]).length)];
        const v0 = Math.floor(fr(a.pos.x, a.pos.z) * 9973);   // not from R(): the layout stays the same
        chunks[ci].items.push({ a: L.asset, layer: L.layer, x: a.pos.x, y: gy, z: a.pos.z, yaw, s, c: col(), zone: zi, t, chunk: ci, v: v0, ...(L.hi ? { hi: true } : {}) });
        if (solid) occAdd(a.pos.x, a.pos.z, fr0, isTree);
        placed++;
        if (L.cluster) {   // members around the centre (blob) or continuing along the road at the same offset (row); each one must clear the road too
          const Cn = L.cluster, m = Math.round(Cn.n[0] + R() * ((Cn.n[1] ?? Cn.n[0]) - Cn.n[0]));
          const q = anchor(route, t + 0.1).pos, v = Math.max(0.5, Math.hypot(q.x - rp.x, q.z - rp.z) / 0.1);
          for (let j = 1; j < m; j++) {
            let x: number, zz: number, ty = t, my = yaw; const ms = s * (0.8 + 0.4 * R());
            if (Cn.row) { ty = t + Math.ceil(j / 2) * (j % 2 ? 1 : -1) * Cn.r * s / v; if (ty < z.t0 || ty > t1) continue;
              let b = edge < 6 ? anchor(route, ty, off, 0, 0) : flowAnchor(route, ty, off, 0, 0);
              if (view) { let o2 = off; for (let k = 0; k < 6 && o.hits(b.pos.x, b.pos.z, r * ms / s + pad, a.pos.y - 1, a.pos.y + A.h * ms); k++) { o2 += side * 1.25; b = flowAnchor(route, ty, o2, 0, 0); } }
              x = b.pos.x; zz = b.pos.z; const bp = anchor(route, ty).pos; my = view ? yaw : Math.atan2(bp.x - x, bp.z - zz); }
            else { const an = R() * Math.PI * 2, rr = Cn.r * s * Math.sqrt(0.15 + 0.85 * R()); x = a.pos.x + Math.cos(an) * rr; zz = a.pos.z + Math.sin(an) * rr; my = L.layer === 'mid' ? yaw + (R() - 0.5) * 0.8 : R() * Math.PI * 2; }
            if (o.hits(x, zz, r * ms / s + pad, a.pos.y - 1, a.pos.y + A.h * ms) || (A.h * ms > (view ? 3.5 : 2.6) && nearBand(x, zz, ty, (L.hug ? 3 : view ? 8 : 9) + r * ms / s))) { rejected++; rj[z.id + ' ' + L.asset + ' mhit'] = (rj[z.id + ' ' + L.asset + ' mhit'] ?? 0) + 1; continue; }
            if (L.layer === 'mid' && A.h * ms > 1.2 && blocksHead(x, zz, r * ms / s, a.pos.y + y0, A.h * ms, ty)) { rejected++; rj[z.id + ' ' + L.asset + ' msight'] = (rj[z.id + ' ' + L.asset + ' msight'] ?? 0) + 1; continue; }
            const alts = [L.asset, ...(L.alt ?? [])], ma = alts[j % alts.length], MA = spec.assets[ma] ?? A, mr = foot(MA, ms);
            const mt = MA.shape === 'tree' && !/hedge/.test(ma); if (solid && occHit(x, zz, mr, mt)) { rejected++; rj[z.id + ' ' + L.asset + ' mocc'] = (rj[z.id + ' ' + L.asset + ' mocc'] ?? 0) + 1; continue; }
            { const br = L.layer === 'ground' ? Math.min(r * ms / s, 0.6) : mr; if (!bankOk(x, zz, br)) { const q = snapBank(x, zz, br, r * ms / s + pad, a.pos.y, A.h * ms, solid ? mr : 0, mt); if (!q) { rejected++; continue; } x = q[0]; zz = q[1]; } }
            const cj = chunkAt(ty); if (solid) occAdd(x, zz, mr, mt);   // v8: rows alternate kinds and step the palette variant, so no piece repeats its neighbour
            chunks[cj].items.push({ a: ma, layer: L.layer, x, y: groundY(chunks[cj], x, zz) + y0, z: zz, yaw: my + (view ? (fr(zz, x) - 0.5) * 0.4 : 0), s: ms, c: col(), zone: zi, t: ty, chunk: cj, v: v0 + j, ...(L.hi ? { hi: true } : {}) }); placed++;
          }
        }
        break;
      }
    }
    // v11 bank plots: every raised page bank of the zone is a garden plot like the keys - dense flower patches over the whole top,
    // bushes / beds / trees in the middle and outer part, an occasional small house; all fully on the bank, clear of the sightline
    const PL = z.plots;
    if (PL) for (const B of banks) { if (B.zone !== zi) continue;
      for (let k = 0; k < B.P.length - 1; k++) {
        const p = B.P[k], q = B.P[k + 1], t = B.T[k], ci = B.ci[k], c = chunks[ci];
        const W = Math.hypot(p[2] - p[0], p[3] - p[1]), Lg = Math.hypot(q[0] - p[0], q[1] - p[1]), area = W * Lg;
        const at = (u: number, v: number) => { const ix = p[0] + (q[0] - p[0]) * v, iz = p[1] + (q[1] - p[1]) * v, ox = p[2] + (q[2] - p[2]) * v, oz = p[3] + (q[3] - p[3]) * v; return [ix + (ox - ix) * u, iz + (oz - iz) * u]; };
        const inner = at(0, 0.5); let seed = Math.floor(fr(p[0] * 1.3, p[1] * 0.7) * 1e6); const rr = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
        const put = (a: string, layer: string, x: number, zz: number, sc: number, j: number) => { const A = spec.assets[a]; if (!A) return false;
          const h = A.h * sc, f = foot(A, sc), solid = layer === 'mid' && h >= 0.8, tree = A.shape === 'tree' && !/hedge/.test(a);
          if (!bankOk(x, zz, layer === 'mid' ? f : 0.3) || bankAt(x, zz) === null) return false;
          if (o.hits(x, zz, Math.max(0.3, f) + 0.6, B.y - 1, B.y + h)) return false;
          if (layer === 'mid' && h > 1.2 && blocksHead(x, zz, f, B.y, h, t)) return false;
          if (layer === 'mid' && h > 2.6 && nearBand(x, zz, t, 9 + f)) return false;
          if (solid && occHit(x, zz, f, tree)) return false;
          if (solid) occAdd(x, zz, f, tree);
          c.items.push({ a, layer, x, y: B.y, z: zz, yaw: Math.atan2(inner[0] - x, inner[1] - zz) + (rr() - 0.5) * 1.4, s: sc, c: 0, zone: zi, t, chunk: ci, v: Math.floor(fr(x * 2.3, zz * 1.9) * 9973), ...(j % 2 ? { hi: true } : {}) });
          placed++; rj['plot ' + z.id] = (rj['plot ' + z.id] ?? 0) + 1; return true; };
        const S = PL.scale ?? [1.0, 1.4], SS = PL.sScale ?? [1.6, 3.0];
        // flower patches (ground layer, cheap): centre + 4-7 members within ~1.3 m
        for (let n = Math.round(area * PL.dSmall / 100 + rr()), i = 0; i < n; i++) { const [cx, cz] = at(0.05 + 0.9 * rr(), rr()), m = 4 + Math.floor(rr() * 4);
          for (let j = 0; j < m; j++) { const an = rr() * 6.283, d = j ? 0.4 + rr() * 0.9 : 0; put(PL.small[Math.floor(rr() * PL.small.length)], 'ground', cx + Math.cos(an) * d * SS[0] / 1.6, cz + Math.sin(an) * d * SS[0] / 1.6, SS[0] + rr() * (SS[1] - SS[0]), i + j); } }
        for (let n = Math.round(area * PL.dBig / 100 + rr() * 0.8), i = 0; i < n; i++) { const [x, zz] = at(0.25 + 0.7 * rr(), rr());
          put(PL.big[Math.floor(rr() * PL.big.length)], 'mid', x, zz, S[0] + rr() * (S[1] - S[0]), i); }
        if (PL.house?.length) for (let n = Math.floor(area * (PL.dHouse ?? 0) / 100 + rr()), i = 0; i < n; i++) { const [x, zz] = at(0.5 + 0.4 * rr(), rr());
          put(PL.house[Math.floor(rr() * PL.house.length)], 'mid', x, zz, 0.75 + rr() * 0.25, i + 1); }
      } }
    // v9 frame fill: the key frames are full edge to edge. Walk a flow-aligned grid over the zone; every cell with no solid piece within `free` m
    // gets a small blob of mixed fill kinds (cheap trees / piles), each member clear of the road, the sightline and the occupancy grid.
    const F = z.fill;
    if (F && F.kinds.length) {
      const dt = F.cell / 9; let fk = 0;
      for (let t = z.t0 + dt * 0.5; t < t1; t += dt) for (let off = -F.lat; off <= F.lat + 0.01; off += F.cell) {
        if (Math.abs(off) < 3) continue;
        const jx = (fr(t * 7.1, off) - 0.5) * F.cell * 0.7, jt = (fr(off, t * 3.3) - 0.5) * dt * 0.8;
        const a = flowAnchor(route, Math.min(t1, Math.max(z.t0, t + jt)), off + jx, 0, 0);
        rj['fill cells ' + z.id] = (rj['fill cells ' + z.id] ?? 0) + 1; if (occHit(a.pos.x, a.pos.z, F.free ?? 3.5)) { rj['fill occ ' + z.id] = (rj['fill occ ' + z.id] ?? 0) + 1; continue; }
        if (o.hits(a.pos.x, a.pos.z, 2.2, a.pos.y - 1, a.pos.y + 4)) { rj['fill road ' + z.id] = (rj['fill road ' + z.id] ?? 0) + 1; continue; }
        const m = Math.round(F.n[0] + fr(a.pos.z, a.pos.x) * ((F.n[1] ?? F.n[0]) - F.n[0]));
        const rp = anchor(route, t).pos, yaw0 = Math.atan2(rp.x - a.pos.x, rp.z - a.pos.z);
        for (let j = 0; j < m; j++) {
          const an = fr(j * 1.7 + a.pos.x, a.pos.z) * Math.PI * 2, rr = j === 0 ? 0 : F.r * Math.sqrt(0.2 + 0.8 * fr(a.pos.z + j, a.pos.x));
          let x = a.pos.x + Math.cos(an) * rr, zz = a.pos.z + Math.sin(an) * rr;
          const ma = F.kinds[(fk++) % F.kinds.length], MA = spec.assets[ma]; if (!MA) continue;
          const ms = F.scale[0] + fr(x, zz * 1.3) * ((F.scale[1] ?? F.scale[0]) - F.scale[0]), h = MA.h * ms, mr = foot(MA, ms), tr = MA.shape === 'tree';
          const rad = Math.max(0.15, Math.max(MA.h, MA.w ?? 0, MA.d ?? 0) * ms * 0.35), pad = h < 1.7 ? 0.35 + 0.1 * o.widthAt(t) : clearNear + 0.5 * o.widthAt(t);
          if (o.hits(x, zz, rad + pad, a.pos.y - 1, a.pos.y + h)) continue;
          if (h > 1.2 && blocksHead(x, zz, rad, a.pos.y, h, t)) continue;
          if (h > 2.5 && nearBand(x, zz, t, 10 + rad)) continue;   // frame bottom keeps low piles only (no giant near trees)
          if (h >= 0.8 && occHit(x, zz, mr, tr)) continue;
          if (!bankOk(x, zz, mr)) { const q = snapBank(x, zz, mr, rad + pad, a.pos.y, h, h >= 0.8 ? mr : 0, tr); if (!q) continue; x = q[0]; zz = q[1]; }
          const ci = chunkAt(t);
          chunks[ci].items.push({ a: ma, layer: 'mid', x, y: groundY(chunks[ci], x, zz), z: zz, yaw: yaw0 + (fr(zz, x) - 0.5) * 1.2, s: ms, c: 0, zone: zi, t, chunk: ci, v: Math.floor(fr(a.pos.x * 1.1, a.pos.z) * 9973) + j, hi: true });   // members step the palette like layer blobs
          if (h >= 0.8) occAdd(x, zz, mr, tr); placed++; rj['fill placed ' + z.id] = (rj['fill placed ' + z.id] ?? 0) + 1;
        }
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
      if (o.hits(a.pos.x, a.pos.z, 1.5 * s + 2.0, a.pos.y - 30, a.pos.y + 30) || nearCam(a.pos.x, a.pos.z, t) || nearBand(a.pos.x, a.pos.z, t, 18 + 1.5 * s)) { rejected++; continue; }   // v9: no flat cards in the (now built) frame bottom either
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
      const { a, r, sc } = setPos(sp)!;
      const rp = anchor(route, sp.t).pos;
      const popAt = drop && sp.t - drop.t < 8 && sp.t >= drop.t - 0.5 ? drop.t : snap(sp.t - 4);
      const sc0 = chunks[chunkAt(sp.t)];
      for (const [ea, en] of sp.entourage ?? []) {   // entourage: decor ringed around the hero (front half first), clear of the road
        const EA = spec.assets[ea]; if (!EA) continue;
        for (let k = 0; k < en; k++) for (let att = 0; att < 4; att++) {
          const ang = Math.atan2(rp.x - a.pos.x, rp.z - a.pos.z) + (R() - 0.5) * Math.PI * (att < 2 ? 1.3 : 2), rr = r * 0.75 + 1.5 + R() * 7;
          let x = a.pos.x + Math.sin(ang) * rr, zz = a.pos.z + Math.cos(ang) * rr; const es = 1.3 + R() * 0.5;
          if (o.hits(x, zz, Math.max(EA.h, EA.w ?? 0) * es * 0.35 + 0.8, a.pos.y - 1, a.pos.y + EA.h * es)) { rejected++; continue; }
          if (EA.h * es > 1.2 && blocksHead(x, zz, Math.max(EA.h, EA.w ?? 0) * es * 0.35, a.pos.y, EA.h * es, sp.t)) { rejected++; continue; }
          const ef = foot(EA, es); if (EA.h * es >= 0.8 && occHit(x, zz, ef, EA.shape === 'tree')) { rejected++; continue; }   // v9: entourage no longer clips decor (Mac sweep: bunny statue inside a grove)
          if (!bankOk(x, zz, ef)) { const q = snapBank(x, zz, ef, Math.max(EA.h, EA.w ?? 0) * es * 0.35 + 0.8, a.pos.y, EA.h * es, EA.h * es >= 0.8 ? ef : 0, EA.shape === 'tree'); if (!q) { rejected++; continue; } x = q[0]; zz = q[1]; }
          if (EA.h * es >= 0.8) occAdd(x, zz, ef, EA.shape === 'tree');
          const ci = chunkAt(sp.t); const ec = chunks[ci];
          ec.items.push({ a: ea, layer: 'mid', x, y: groundY(ec, x, zz), z: zz, yaw: Math.atan2(rp.x - x, rp.z - zz), s: es, c: (z.layers[0]?.colors ?? [0])[Math.floor(R() * (z.layers[0]?.colors ?? [0]).length)], zone: zi, t: sp.t, chunk: ci }); placed++; break;
        }
      }
      const fc = sp.face === 'cam' ? flowAnchor(route, Math.max(0, sp.t - 5), 0, 0, 0).pos : rp;   // v8: 'cam' pieces face back along the flow (the key camera), e.g. the ferris wheel's disc
      sets.push({ a: sp.asset, layer: 'land', x: a.pos.x, y: groundY(sc0, a.pos.x, a.pos.z), z: a.pos.z, yaw: Math.atan2(fc.x - a.pos.x, fc.z - a.pos.z), s: sc, c: 0, zone: zi, t: sp.t, chunk: chunkAt(sp.t), popAt, label: sp.label, ...(sp.hi ? { hi: true } : {}), ...(sp.hero ? { hero: true } : {}) });
    }
  });
  // set pieces win: tall decor inside a set piece's footprint goes (entourage rings start outside it)
  for (const st of sets) { const A = spec.assets[st.a]; if (!A) continue; const r = foot(A, st.s);
    for (let ci = Math.max(0, st.chunk - 2); ci <= Math.min(chunks.length - 1, st.chunk + 2); ci++) chunks[ci].items = chunks[ci].items.filter(it => {
      if (it.layer !== 'mid') return true; const B = spec.assets[it.a]; if (!B || B.h * it.s < 0.8) return true;
      const k = (it.x - st.x) ** 2 + (it.z - st.z) ** 2 < ((r + foot(B, it.s) * 0.6) * 0.85) ** 2; if (k) rejected++; return !k; }); }
  return { banks, chunks, sets, stats: { placed, rejected, rj } };
}

/** chunk index range [a, b] active at song time t (window behind/ahead in seconds) */
export function activeRange(chunks: CChunk[], t: number, behind: number, ahead: number): [number, number] {
  let a = 0; while (a < chunks.length - 1 && chunks[a].t1 < t - behind) a++;
  let b = a; while (b < chunks.length - 1 && chunks[b + 1].t0 <= t + ahead) b++;
  return [a, b];
}
