import { CreateBox, Matrix, Mesh, Quaternion, Scene, StandardMaterial, Vector3, Color3 } from './bjs';
import { HEAD_VEC, spanPos, type Route } from '../core/path';
import type { Layout, Palette } from '../core/types';
import { hex } from './prefabs';

interface Tile { reveal: number; mode: string; cx: number; cy: number; cz: number; len: number; w: number; yaw: number; pitch: number; seed: number; }
const TILE = 2.6;
const ANIM = 0.42;

export function stepAt<T extends { t: number }>(list: T[] | undefined, t: number): T | undefined { let r: T | undefined; for (const x of list ?? []) if (x.t <= t + 1e-9) r = x; return r; }

export class Road {
  body: Mesh; top: Mesh;
  tiles: Tile[] = [];
  private mBody: Float32Array; private mTop: Float32Array;
  private animating = new Set<number>();
  private revealedUpTo = -1; // index into sorted tiles
  private order: number[] = [];
  readonly height: number;

  constructor(scene: Scene, route: Route, layout: Layout, paletteAt: (t: number) => Palette) {
    this.height = layout.road.height ?? 0.6;
    const widthAt = (t: number) => stepAt(layout.road.width, t)?.w ?? 2.2;
    const revealAt = (t: number) => stepAt(layout.road.reveal, t) ?? { t: 0, mode: 'static', lead: 2 };
    const spans = route.spans;
    const colorsBody: number[] = []; const colorsTop: number[] = [];
    for (let i = 0; i < spans.length; i++) {
      const s = spans[i];
      if (s.air) continue;
      const len = s.v * (s.t1 - s.t0);
      const startsAfterTurn = i > 0 && spans[i - 1].turnIndex >= 0;
      const endsWithTurn = s.turnIndex >= 0 || (i === spans.length - 1);
      const w = widthAt(s.t0);
      const padStart = startsAfterTurn ? w / 2 : (i === 0 ? 1.5 : 0);
      const padEnd = endsWithTurn ? (i === spans.length - 1 ? 6 : w / 2) : 0;
      const total = len + padStart + padEnd;
      const n = Math.max(1, Math.ceil(total / TILE));
      const [hx, hz] = HEAD_VEC[s.heading];
      const yaw = Math.atan2(hx, hz);
      const p0 = spanPos(s, s.t0);
      const slope = len > 0 ? (s.y1 - s.y0) / len : 0;
      for (let k = 0; k < n; k++) {
        const a = -padStart + total * k / n, b = -padStart + total * (k + 1) / n;
        const mid = (a + b) / 2;
        const tAt = s.t0 + Math.max(0, Math.min(len, a)) / s.v;
        const rv = revealAt(tAt);
        const tw = widthAt(tAt);
        const cy = p0.y + slope * Math.max(0, Math.min(len, mid));
        this.tiles.push({ reveal: rv.mode === 'static' ? -1e9 : tAt - rv.lead, mode: rv.mode, cx: p0.x + hx * mid, cy, cz: p0.z + hz * mid, len: b - a, w: tw, yaw, pitch: -Math.atan(slope), seed: (this.tiles.length * 0.618) % 1 });
        const pal = paletteAt(tAt);
        const cb = hex(pal.roadSide), ct = hex(pal.road);
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
      m.material = mat; m.isPickable = false; m.alwaysSelectAsActiveMesh = true;
    }
    const N = this.tiles.length;
    this.mBody = new Float32Array(N * 16); this.mTop = new Float32Array(N * 16);
    this.body.thinInstanceSetBuffer('matrix', this.mBody, 16, false);
    this.top.thinInstanceSetBuffer('matrix', this.mTop, 16, false);
    this.body.thinInstanceSetBuffer('color', new Float32Array(colorsBody), 4, true);
    this.top.thinInstanceSetBuffer('color', new Float32Array(colorsTop), 4, true);
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
    const mb = Matrix.Compose(new Vector3(t.w * s, h * scaleY * s, (t.len + 0.05) * s), q, new Vector3(t.cx, t.cy - h / 2 * scaleY + dy, t.cz));
    const mt = Matrix.Compose(new Vector3(t.w * s * 1.001, 0.04 * s, (t.len + 0.08) * s), q, new Vector3(t.cx, t.cy + 0.0 + dy, t.cz));
    mb.copyToArray(this.mBody, i * 16); mt.copyToArray(this.mTop, i * 16);
  }

  /** Reset all tiles to their state at time t (restart / checkpoint). */
  seek(t: number) {
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
    let dirty = false;
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
    this.body.thinInstanceBufferUpdated('matrix'); this.top.thinInstanceBufferUpdated('matrix');
  }

  dispose() { this.body.material?.dispose(); this.top.material?.dispose(); this.body.dispose(); this.top.dispose(); }
}
