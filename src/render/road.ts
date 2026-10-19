import { CreateBox, Matrix, Mesh, Quaternion, Scene, StandardMaterial, Vector3, Color3 } from './bjs';
import { HEAD_VEC, spanPos, type Route } from '../core/path';
import type { Layout, Palette } from '../core/types';
import { hex } from './prefabs';
import { readableRoadWidths } from '../core/roadwidth';
import { RoadSightline } from './scenec/roadsightline';

interface Tile { t: number; reveal: number; mode: string; cx: number; cy: number; cz: number; len: number; w: number; yaw: number; pitch: number; seed: number; }
const TILE = 2.6;
const ANIM = 0.42;
const PAPER = { top: hex('#FFF5E1'), edge: hex('#E3AE45'), body: hex('#EED9B0') };

export function stepAt<T extends { t: number }>(list: T[] | undefined, t: number): T | undefined { let r: T | undefined; for (const x of list ?? []) if (x.t <= t + 1e-9) r = x; return r; }

export class Road {
  body: Mesh; top: Mesh;
  tiles: Tile[] = [];
  private mBody: Float32Array; private mTop: Float32Array;
  private animating = new Set<number>();
  private revealedUpTo = -1; // index into sorted tiles
  private order: number[] = [];
  readonly height: number;
  /** v2.8 hook: called after tile matrices change (showfx trims share the road-top instance buffer) */
  onFlush: (() => void) | null = null;
  get topBuffer() { return this.mTop; }

  /** concept C 'paper' style (key renders): cream top cap, a slightly wider gold step just under it, cream-tan body; unlit so the zone
   *  light never tints it. The gold step is a second set of instances on the body mesh (no extra draw call). */
  private paper = false;
  constructor(scene: Scene, route: Route, layout: Layout, paletteAt: (t: number) => Palette, opts?: { paper?: boolean }) {
    this.paper = !!opts?.paper;
    this.height = layout.road.height ?? 0.6;
    const widthAt = (t: number) => stepAt(layout.road.width, t)?.w ?? 2.2;
    const revealAt = (t: number) => stepAt(layout.road.reveal, t) ?? { t: 0, mode: 'static', lead: 2 };
    const spans = route.spans;
    const widths = this.paper ? readableRoadWidths(route, widthAt) : spans.map(s => widthAt(s.t0));
    const colorsBody: number[] = []; const colorsTop: number[] = [];
    for (let i = 0; i < spans.length; i++) {
      const s = spans[i];
      if (s.air) continue;
      const len = s.v * (s.t1 - s.t0);
      // Square corners without overlap: the span that ENDS at a turn owns the corner square (extends past the corner
      // centre by half of the NEXT span's width); the span that starts after a turn begins half of the PREVIOUS span's
      // width after the corner centre. Footprints tile the L exactly (also with a width change at the corner).
      const prevS = i > 0 ? spans[i - 1] : null, nextS = i + 1 < spans.length ? spans[i + 1] : null;
      const startsAfterTurn = !!prevS && prevS.turnIndex >= 0 && !prevS.air;
      const endsWithTurn = s.turnIndex >= 0 && !!nextS;
      const padStart = startsAfterTurn ? -widths[i - 1] / 2 : (i === 0 ? 1.5 : 0);
      const padEnd = endsWithTurn ? widths[i + 1] / 2 : (i === spans.length - 1 ? 6 : 0);
      const total = len + padStart + padEnd;
      if (total <= 1e-4) continue;
      const n = Math.max(1, Math.ceil(total / TILE));
      const [hx, hz] = HEAD_VEC[s.heading];
      const yaw = Math.atan2(hx, hz);
      const p0 = spanPos(s, s.t0);
      const slope = len > 0 ? (s.y1 - s.y0) / len : 0;
      for (let k = 0; k < n; k++) {
        const a = -padStart + total * k / n, b = -padStart + total * (k + 1) / n;
        const mid = (a + b) / 2;
        const tAt = s.t0 + Math.max(0, Math.min(len - 1e-6, a)) / s.v;
        const rv = revealAt(tAt);
        const tw = widths[i];
        const cy = p0.y + slope * Math.max(0, Math.min(len, mid));
        this.tiles.push({ t: tAt, reveal: rv.mode === 'static' ? -1e9 : tAt - rv.lead, mode: rv.mode, cx: p0.x + hx * mid, cy, cz: p0.z + hz * mid, len: b - a, w: tw, yaw, pitch: -Math.atan(slope), seed: (this.tiles.length * 0.618) % 1 });
        const pal = paletteAt(tAt);
        const cb = this.paper ? PAPER.body : hex(pal.roadSide), ct = this.paper ? PAPER.top : hex(pal.road);
        colorsBody.push(cb.r, cb.g, cb.b, 1); colorsTop.push(ct.r, ct.g, ct.b, 1);
      }
    }
    // final approach into the finish
    this.body = CreateBox('roadBody', { size: 1 }, scene);
    this.top = CreateBox('roadTop', { size: 1 }, scene);
    for (const [m, c] of [[this.body, '#ffffff'], [this.top, '#ffffff']] as const) {
      const mat = new StandardMaterial(m.name + 'M', scene);
      mat.diffuseColor = hex(c); mat.specularColor = new Color3(0.04, 0.04, 0.04);
      mat.emissiveColor = new Color3(0, 0, 0);
      if (this.paper) { mat.disableLighting = true; mat.emissiveColor = new Color3(1, 1, 1); mat.diffuseColor = new Color3(0, 0, 0); }
      m.material = mat; m.isPickable = false; m.alwaysSelectAsActiveMesh = true;
      if (this.paper) new RoadSightline(mat);
    }
    const N = this.tiles.length;
    const NB = this.paper ? 2 * N : N;   // paper: instances [N, 2N) of the body are the gold step
    if (this.paper) for (let i = 0; i < N; i++) colorsBody.push(PAPER.edge.r, PAPER.edge.g, PAPER.edge.b, 1);
    this.mBody = new Float32Array(NB * 16); this.mTop = new Float32Array(N * 16);
    if (this.paper) {   // v10 (concept C): only the tiles near the head are drawn - compact render copies of the full buffers (showfx keeps reading mTop)
      this.rBody = new Float32Array(NB * 16); this.rTop = new Float32Array(N * 16); this.cBody = new Float32Array(colorsBody); this.cTop = new Float32Array(colorsTop);
      this.rcBody = new Float32Array(NB * 4); this.rcTop = new Float32Array(N * 4);
      this.body.thinInstanceSetBuffer('matrix', this.rBody, 16, false); this.top.thinInstanceSetBuffer('matrix', this.rTop, 16, false);
      this.body.thinInstanceSetBuffer('color', this.rcBody, 4, false); this.top.thinInstanceSetBuffer('color', this.rcTop, 4, false);
    } else {
    this.body.thinInstanceSetBuffer('matrix', this.mBody, 16, false);
    this.top.thinInstanceSetBuffer('matrix', this.mTop, 16, false);
    this.body.thinInstanceSetBuffer('color', new Float32Array(colorsBody), 4, true);
    this.top.thinInstanceSetBuffer('color', new Float32Array(colorsTop), 4, true);
    }
    this.body.freezeWorldMatrix(); this.top.freezeWorldMatrix(); this.body.doNotSyncBoundingInfo = true; this.top.doNotSyncBoundingInfo = true;
    this.order = this.tiles.map((_, i) => i).sort((a, b) => this.tiles[a].reveal - this.tiles[b].reveal);
    this.seek(0);
  }

  private write(i: number, k: number) {
    // k: 0 hidden .. 1 settled
    const t = this.tiles[i];
    const e = k >= 1 ? 1 : 1 - Math.pow(1 - Math.max(0, k), 3);
    let dy = 0, scaleY = 1, alpha = 1, tilt = 0;
    if (k <= 0) alpha = 0;
    else if (k < 1) {
      switch (t.mode) {
        case 'rise': dy = -(1 - e) * (7 + t.seed * 4); break;
        case 'drop': dy = (1 - e) * (9 + t.seed * 5); break;
        case 'unfold': tilt = (1 - e) * Math.PI / 2; break;
        case 'fade': scaleY = e; break;
        default: break;
      }
    }
    const h = this.height;
    const s = alpha === 0 ? 0 : 1;
    const q = Quaternion.RotationYawPitchRoll(t.yaw, t.pitch + tilt, 0);
    // body [cy-h, cy-0.02] and top cap [cy-0.02, cy+0.02]: identical footprint, stacked (no coplanar overlapping faces);
    // tiles abut exactly (no overlap), length along the slope for ramp tiles
    const L = t.len / Math.cos(t.pitch);
    const mb = Matrix.Compose(new Vector3(t.w * s, (h - 0.02) * scaleY * s, L * s), q, new Vector3(t.cx, t.cy - 0.02 - (h - 0.02) / 2 * scaleY + dy, t.cz));
    const mt = Matrix.Compose(new Vector3(t.w * s, 0.04 * s, L * s), q, new Vector3(t.cx, t.cy + dy, t.cz));
    if (this.paper) {   // top cap 0.10 thick, gold step 0.12 tall and 0.32 m wider just under it, body below
      const T = 0.10, E = 0.12, bh = Math.max(0.05, h - T - E);
      const mt2 = Matrix.Compose(new Vector3(t.w * s, T * s, L * s), q, new Vector3(t.cx, t.cy + 0.02 - T / 2 + dy, t.cz));
      const me = Matrix.Compose(new Vector3((t.w + 0.32) * s, E * scaleY * s, (L + 0.32) * s), q, new Vector3(t.cx, t.cy + 0.02 - T - E / 2 * scaleY + dy, t.cz));
      const mb2 = Matrix.Compose(new Vector3(t.w * s, bh * scaleY * s, L * s), q, new Vector3(t.cx, t.cy + 0.02 - T - E - bh / 2 * scaleY + dy, t.cz));
      mb2.copyToArray(this.mBody, i * 16); me.copyToArray(this.mBody, (this.tiles.length + i) * 16); mt2.copyToArray(this.mTop, i * 16); return;
    }
    mb.copyToArray(this.mBody, i * 16); mt.copyToArray(this.mTop, i * 16);
  }

  /** Reset all tiles to their state at time t (restart / checkpoint). */
  seek(t: number) {
    this.now = t; this.win = [-1, -1];
    this.animating.clear();
    for (let i = 0; i < this.tiles.length; i++) {
      const k = (t - this.tiles[i].reveal) / ANIM;
      this.write(i, k);
      if (k > 0 && k < 1) this.animating.add(i);
    }
    this.revealedUpTo = -1;
    for (let j = 0; j < this.order.length; j++) if (this.tiles[this.order[j]].reveal <= t) this.revealedUpTo = j; else break;
    this.flush();
  }

  update(t: number) {
    this.now = t; const W = this.paper ? this.winOf(t) : null; let dirty = !!W && (W[0] !== this.win[0] || W[1] !== this.win[1]);
    while (this.revealedUpTo + 1 < this.order.length && this.tiles[this.order[this.revealedUpTo + 1]].reveal <= t) {
      this.revealedUpTo++; this.animating.add(this.order[this.revealedUpTo]);
    }
    for (const i of this.animating) {
      const k = (t - this.tiles[i].reveal) / ANIM;
      this.write(i, k); dirty = true;
      if (k >= 1) this.animating.delete(i);
    }
    if (dirty) this.flush();
  }

  private flush() {
    if (this.paper && this.rBody && this.rTop && this.cBody && this.cTop && this.rcBody && this.rcTop) {
      const [i0, i1] = this.winOf(this.now), k = Math.max(0, i1 - i0), N = this.tiles.length;
      this.rTop.set(this.mTop.subarray(i0 * 16, i1 * 16)); this.rBody.set(this.mBody.subarray(i0 * 16, i1 * 16)); this.rBody.set(this.mBody.subarray((N + i0) * 16, (N + i1) * 16), k * 16);
      this.rcTop.set(this.cTop.subarray(i0 * 4, i1 * 4)); this.rcBody.set(this.cBody.subarray(i0 * 4, i1 * 4)); this.rcBody.set(this.cBody.subarray((N + i0) * 4, (N + i1) * 4), k * 4);
      this.top.thinInstanceCount = k; this.body.thinInstanceCount = 2 * k;
      if (this.win[0] !== i0 || this.win[1] !== i1) { this.body.thinInstanceBufferUpdated('color'); this.top.thinInstanceBufferUpdated('color'); this.win = [i0, i1]; }
    }
    this.body.thinInstanceBufferUpdated('matrix'); this.top.thinInstanceBufferUpdated('matrix'); this.onFlush?.();
  }
  private rBody: Float32Array | null = null; private rTop: Float32Array | null = null; private cBody: Float32Array | null = null; private cTop: Float32Array | null = null;
  private rcBody: Float32Array | null = null; private rcTop: Float32Array | null = null; private now = 0; private win: [number, number] = [-1, -1];
  /** v10: tile index range drawn at song time t (tiles are in route order): 9 s behind the head to 24 s ahead */
  private winOf(t: number): [number, number] { const T = this.tiles, lo = (x: number) => { let a = 0, b = T.length; while (a < b) { const m = (a + b) >> 1; if (T[m].t < x) a = m + 1; else b = m; } return a; };
    return [lo(t - 9), lo(t + 24)]; }

  dispose() { this.body.material?.dispose(); this.top.material?.dispose(); this.body.dispose(); this.top.dispose(); }
}
