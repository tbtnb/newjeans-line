import { FreeCamera, Scene, Vector3 } from './bjs';
import { posAt, type Route } from '../core/path';
import type { CameraCue } from '../core/types';

export interface CamParams { pitch: number; dist: number; fov: number; yawOff: number; worldYaw: number | null; roll: number; shake: number; lead: number; orbit: number; punch: number; zoom: number; tilt: number; sway: number; }
// Distances follow the original Dancing Line framing: high three-quarter view, the line in the lower third,
// several seconds of road visible ahead.
const PRESETS: Record<string, Partial<CamParams>> = {
  iso: { pitch: 50, dist: 41, fov: 36, yawOff: 0 },
  high: { pitch: 62, dist: 48, fov: 36, yawOff: 0 },
  low: { pitch: 36, dist: 34, fov: 42, yawOff: 0 },
  side: { pitch: 44, dist: 41, fov: 38, yawOff: 60 },
  top: { pitch: 78, dist: 54, fov: 36, yawOff: 0 },
  wide: { pitch: 48, dist: 52, fov: 40, yawOff: 0 },
  close: { pitch: 46, dist: 30, fov: 40, yawOff: 0 },
};
/** key camera elevation (deg). v10: 33 (was 36) so the skyline band shows a horizon in the top ~quarter; ?kp=NN overrides */
export const KEY_PITCH = (() => { const m = typeof location !== 'undefined' ? /[?&]kp=(\d+(?:\.\d+)?)/.exec(location.search) : null; return m ? +m[1] : 33; })();
const BASE: CamParams = { pitch: 50, dist: 41, fov: 36, yawOff: 0, worldYaw: null, roll: 0, shake: 0, lead: 0.85, orbit: 0, punch: 0.025, zoom: 1, tilt: 0, sway: 0 };
const MIN_DIST = 30;
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const angLerp = (a: number, b: number, k: number) => { let d = ((b - a + Math.PI * 3) % (Math.PI * 2)) - Math.PI; return a + d * k; };

function resolve(prev: CamParams, c: CameraCue): CamParams {
  const p: CamParams = { ...prev, ...(c.preset ? PRESETS[c.preset] ?? {} : {}) };
  if (c.preset) { p.worldYaw = null; p.roll = 0; p.shake = 0; }
  // modifiers hold until the next cue (each cue states its own; omitted = neutral)
  p.zoom = c.zoom ?? 1; p.tilt = c.tilt ?? 0; p.sway = c.sway ?? 0; p.orbit = c.orbit ?? 0; p.punch = c.punch ?? BASE.punch;
  if (c.pitch !== undefined) p.pitch = c.pitch;
  if (c.dist !== undefined) p.dist = c.dist;
  if (c.fov !== undefined) p.fov = c.fov;
  if (c.yaw !== undefined) { p.yawOff = c.yaw; p.worldYaw = null; }
  if (c.worldYaw !== undefined) p.worldYaw = c.worldYaw;
  if (c.roll !== undefined) p.roll = c.roll;
  if (c.shake !== undefined) p.shake = c.shake;
  if (c.lead !== undefined) p.lead = c.lead;
  return p;
}

export class CameraRig {
  cam: FreeCamera;
  private cues: { t: number; blend: number; from: CamParams; to: CamParams }[] = [];
  private target = new Vector3();
  private yaw = 0;
  private ty = 0;
  private initialized = false;
  shakeBoost = 0;
  aspect = 1;
  menuOrbit = false;
  freezeAt: Vector3 | null = null;
  extraPitch = 0; extraDist = 0;
  /** QA close-ups only (play.mjs --camScale); 1 in the game */
  distScale = 1;
  /** ?cam=key: framing of the concept-C key renders -- lower pitch looking along a long receding road, head in the lower
   *  third, authored side/top presets ignored (always along the flow); distance stays at or beyond the default's floor */
  keyMode = typeof location !== 'undefined' && /[?&]cam=key\b/.test(location.search);   // world.ts turns it on for the concept-C scene unless ?cam=old

  /** v6 key camera: hero focus (world.ts), eased weight w 0..1; the camera yaws toward it (capped) and zooms out a little */
  focus: ((t: number, head: { x: number; z: number }) => { x: number; z: number; w: number } | null) | null = null;
  private fw = 0; private fyaw = 0; private fsx = 0; private fsz = 0;
  private hits: number[] = []; private orbitAng = 0;
  /** last projected head position (fraction of the screen from the left / top), for QA (__njHeadLog) */
  lastFx = 0.5; lastFy = 0.5;
  /** key camera screen-space framing: the head is pinned at this fraction from the top (portrait ~0.42, landscape ~0.47);
   *  ?headpin=0 restores the old look-at-the-lead-point framing (QA baseline) */
  headPin = !(typeof location !== 'undefined' && /[?&]headpin=0\b/.test(location.search));

  constructor(scene: Scene, private route: Route, authored: CameraCue[], sections: { t: number; label?: string }[] = [], hits: number[] = [], auto = true) {
    this.cam = new FreeCamera('cam', new Vector3(0, 20, -20), scene);
    this.cam.minZ = 0.5; this.cam.maxZ = 800; this.cam.inputs.clear();
    this.hits = [...hits].sort((a, b) => a - b);
    const cues = auto ? autoCues(authored, sections) : authored;
    const sorted = [...cues].sort((a, b) => a.t - b.t);
    let cur: CamParams = { ...BASE };
    if (!sorted.length || sorted[0].t > 0) sorted.unshift({ t: 0, preset: 'iso', blend: 0 });
    for (const c of sorted) { const to = resolve(cur, c); this.cues.push({ t: c.t, blend: c.blend ?? 1.2, from: cur, to }); cur = to; }
  }

  params(t: number): CamParams {
    let i = 0; for (let j = 0; j < this.cues.length; j++) if (this.cues[j].t <= t) i = j;
    const c = this.cues[i]; const k = c.blend <= 0 ? 1 : smooth((t - c.t) / c.blend);
    const L = (a: number, b: number) => a + (b - a) * k;
    return { pitch: L(c.from.pitch, c.to.pitch), dist: L(c.from.dist, c.to.dist), fov: L(c.from.fov, c.to.fov), yawOff: L(c.from.yawOff, c.to.yawOff),
      worldYaw: c.to.worldYaw ?? null, roll: L(c.from.roll, c.to.roll), shake: L(c.from.shake, c.to.shake), lead: L(c.from.lead, c.to.lead), orbit: L(c.from.orbit, c.to.orbit), punch: L(c.from.punch, c.to.punch), zoom: L(c.from.zoom, c.to.zoom), tilt: L(c.from.tilt, c.to.tilt), sway: L(c.from.sway, c.to.sway),
      ...(c.to.worldYaw !== null && c.from.worldYaw === null ? { worldYawBlend: k } : {}) } as CamParams;
  }

  flowYaw(t: number): number {
    // mean travel direction over a window — continuous in t, ignores the zig-zag
    const a = posAt(this.route, t - 2.5), b = posAt(this.route, t + 4.5); // ~7 s window: a forward zig-zag reads as one steady direction (no swinging per leg)
    let dx = b.x - a.x, dz = b.z - a.z;
    if (Math.hypot(dx, dz) < 3) { const c = posAt(this.route, t + 0.5); dx = c.x - a.x; dz = c.z - a.z; }
    return Math.atan2(dx, dz);
  }

  snap() { this.initialized = false; }

  update(t: number, head: { x: number; y: number; z: number }, dt: number) {
    const p = this.params(t);
    // Gameplay framing must not pulse with each beat or inherit authored shake/zoom cues.
    // The road and head provide the rhythm; moving the whole view makes dense turns uncomfortable.
    const steady = this.keyMode && !this.menuOrbit;
    if (steady) { p.pitch = KEY_PITCH; p.dist = 46; p.fov = 42; p.yawOff = 0; p.sway = 0; p.orbit = 0; p.worldYaw = null; p.roll = 0; p.tilt = 0; p.lead = 2.4; p.punch = 0; p.shake = 0; p.zoom = 1; this.orbitAng = 0; delete (p as any).worldYawBlend; }
    const flow = this.flowYaw(t);
    // slow orbit (breakdowns): drifts while active, eases back when the cue ends; never more than ±35°
    if (p.orbit) this.orbitAng = Math.max(-35, Math.min(35, this.orbitAng + p.orbit * dt)); else this.orbitAng *= Math.exp(-dt * 0.6);
    let desiredYaw = flow + (p.yawOff + p.sway + this.orbitAng) * Math.PI / 180;
    const wy = (p as any).worldYawBlend;
    if (p.worldYaw !== null) desiredYaw = wy !== undefined ? angLerp(desiredYaw, p.worldYaw * Math.PI / 180, wy) : p.worldYaw * Math.PI / 180;
    if (this.menuOrbit) desiredYaw = flow + performance.now() / 9000;
    let fx = Math.sin(flow), fz = Math.cos(flow), fzoom = 0;
    if (this.keyMode && !this.menuOrbit && this.focus && !(typeof location !== 'undefined' && /[?&]focus=0\b/.test(location.search))) {   // hero framing: eased (weight + its own slow filter), never more than 40 deg off the flow
      const f = this.focus(t, head); const w = f ? f.w : 0;
      let goal = 0; if (f) { let d = Math.atan2(f.x - head.x, f.z - head.z) - flow; d = Math.atan2(Math.sin(d), Math.cos(d)); goal = Math.max(-0.6, Math.min(0.6, d * 0.7)) * w; }
      if (!this.initialized) { this.fyaw = goal; this.fw = w; }
      else {   // eased and rate-limited: at most ~14 deg/s of extra turn, zoom eases over ~1 s
        const step = (goal - this.fyaw) * (1 - Math.exp(-dt * 1.5)), lim = 0.25 * dt; this.fyaw += Math.max(-lim, Math.min(lim, step));
        this.fw += (w - this.fw) * (1 - Math.exp(-dt * 1.2)); }
      if (f) {   // and slide the look point up to 7 m toward the hero (weighted, eased) so it sits inside the frame, not on its edge
        let sx = (f.x - head.x) * 0.3 * w, sz = (f.z - head.z) * 0.3 * w; const sl = Math.hypot(sx, sz); if (sl > 7) { sx *= 7 / sl; sz *= 7 / sl; }
        const k = this.initialized ? 1 - Math.exp(-dt * 1.2) : 1; this.fsx += (sx - this.fsx) * k; this.fsz += (sz - this.fsz) * k;
      } else { const k = 1 - Math.exp(-dt * 1.2); this.fsx -= this.fsx * k; this.fsz -= this.fsz * k; }
      const off = this.fyaw; desiredYaw += off; fx = Math.sin(flow + off); fz = Math.cos(flow + off); fzoom = 12 * this.fw;
    }
    const leadDist = this.keyMode ? Math.max(MIN_DIST, p.dist) * (this.headPin ? 0.12 : 0.42) : Math.min(p.lead * 9, Math.max(MIN_DIST, p.dist) * 0.2);   // key: look well ahead, head sits low
    const want = this.freezeAt ?? new Vector3(head.x + fx * leadDist + this.fsx, head.y, head.z + fz * leadDist + this.fsz);
    if (!this.initialized) { this.target.copyFrom(want); this.yaw = desiredYaw; this.ty = want.y; this.initialized = true; }
    const kPos = 1 - Math.exp(-dt * 4.5), kYaw = 1 - Math.exp(-dt * 1.6), kY = 1 - Math.exp(-dt * 2.5);
    this.target.x += (want.x - this.target.x) * kPos; this.target.z += (want.z - this.target.z) * kPos;
    this.ty += (want.y - this.ty) * kY; this.target.y = this.ty;

    this.yaw = angLerp(this.yaw, desiredYaw, kYaw);
    // floor: older layouts authored very close distances (15-24); keep the DL-style overview
    let dist = (Math.max(MIN_DIST, p.dist) * p.zoom + this.extraDist + fzoom) * this.distScale;
    if (this.aspect < 0.95) dist *= Math.pow(Math.min(2.2, 0.95 / this.aspect), 0.35);
    dist = Math.min(dist, (56 + fzoom) * this.distScale + this.extraDist); // cap: wide/zoomed shots on portrait screens never shrink the head below readable size
    // beat punch: a quick push-in on strong hits (kicks), decaying in ~120 ms
    if (p.punch > 0 && this.hits.length && !this.menuOrbit) { const h = lastLE(this.hits, t); if (h > -1e8) dist *= 1 - p.punch * Math.exp(-(t - h) * 9); }
    const pitch = Math.min(84, p.pitch + p.tilt + this.extraPitch) * Math.PI / 180;
    const sh = steady ? 0 : p.shake + this.shakeBoost;
    const jitter = sh > 0 ? new Vector3((Math.random() - 0.5) * sh * 0.6, (Math.random() - 0.5) * sh * 0.6, (Math.random() - 0.5) * sh * 0.6) : Vector3.Zero();
    const pos = new Vector3(this.target.x - Math.sin(this.yaw) * Math.cos(pitch) * dist, this.target.y + Math.sin(pitch) * dist, this.target.z - Math.cos(this.yaw) * Math.cos(pitch) * dist);
    this.cam.position.copyFrom(pos.add(jitter));
    this.cam.fov = p.fov * Math.PI / 180;
    const roll = p.roll * Math.PI / 180;
    this.cam.upVector = new Vector3(Math.sin(roll) * Math.cos(this.yaw), Math.cos(roll), -Math.sin(roll) * Math.sin(this.yaw));
    let look = this.target.add(jitter.scale(0.5));
    if (this.keyMode && this.headPin && !this.menuOrbit) look = this.pinHead(head, p.fov * Math.PI / 180, look);
    this.cam.setTarget(look);
    this.measure(head, look);
    this.shakeBoost *= Math.exp(-dt * 6);
  }

  measure(head: { x: number; y: number; z: number }, look: Vector3) {
    const { f, r, u } = basis(this.cam.position, look), v = new Vector3(head.x, head.y, head.z).subtract(this.cam.position), d = Math.max(1e-3, Vector3.Dot(v, f)), th = Math.tan(this.cam.fov / 2);
    this.lastFy = (1 - Vector3.Dot(v, u) / d / th) / 2; this.lastFx = (1 + Vector3.Dot(v, r) / d / (th * this.aspect)) / 2;
  }
  /** Screen-space framing: turn the view about its right axis so the head projects at a fixed height (independent of pitch,
   *  distance, aspect, choreography, hero nudge and zone blends), then keep it inside the middle half horizontally.
   *  Returns the new look point (on the head's ground plane, so shadows / ground paint that follow getTarget() stay put). */
  pinHead(head: { x: number; y: number; z: number }, fov: number, look: Vector3): Vector3 {
    const a = this.aspect, fy = a <= 0.8 ? 0.42 : a >= 1.3 ? 0.47 : 0.42 + (a - 0.8) / 0.5 * 0.05;   // portrait 42 %, landscape 47 % from the top
    const th = Math.tan(fov / 2), pos = this.cam.position, dist = Math.max(1, Vector3.Distance(look, pos));
    let { f, u } = basis(pos, look); const v = new Vector3(head.x, head.y, head.z).subtract(pos);
    const dv = Math.atan2(Vector3.Dot(v, u), Vector3.Dot(v, f)) - Math.atan((1 - 2 * fy) * th);
    f = f.scale(Math.cos(dv)).add(u.scale(Math.sin(dv)));
    // horizontal: hero yaw / slide may push the head sideways; keep it within 25-75 % of the width
    const r2 = Vector3.Cross(Vector3.Up(), f).normalize(), lim = Math.atan(0.5 * th * a), hx = Math.atan2(Vector3.Dot(v, r2), Vector3.Dot(v, f));
    const dh = hx > lim ? hx - lim : hx < -lim ? hx + lim : 0;
    if (dh) { const c = Math.cos(dh), s = Math.sin(dh); f = new Vector3(f.x * c + f.z * s, f.y, -f.x * s + f.z * c); }
    const k = f.y < -0.05 ? (head.y - pos.y) / f.y : dist;   // ray -> head's ground plane
    return pos.add(f.scale(Math.min(Math.max(k, 5), 400)));
  }
}

/** camera basis (left-handed: x right, y up, z forward) */
function basis(pos: Vector3, look: Vector3) { const f = look.subtract(pos).normalize(); const r = Vector3.Cross(Vector3.Up(), f).normalize(); return { f, r, u: Vector3.Cross(f, r) }; }
function lastLE(a: number[], t: number) { let lo = 0, hi = a.length - 1, r = -1e9; while (lo <= hi) { const m = (lo + hi) >> 1; if (a[m] <= t) { r = a[m]; lo = m + 1; } else hi = m - 1; } return r; }

/** Default choreography from section labels. An authored cue at a section start that sets no modifiers gets the
 *  section's modifiers merged in (its preset/blend stay); sections without any cue get a modifier-only cue.
 *  Returns the full cue list (authored + defaults). */
const MODS = ['zoom', 'tilt', 'sway', 'orbit', 'punch'] as const;
export function autoCues(authored: CameraCue[], sections: { t: number; label?: string }[]): CameraCue[] {
  const out: CameraCue[] = authored.map(c => ({ ...c })); let sway = 1;
  for (const [i, s] of sections.entries()) {
    const l = (s.label ?? '').toLowerCase();
    const len = (sections[i + 1]?.t ?? s.t + 16) - s.t;
    const extra: CameraCue[] = [];
    let m: Partial<CameraCue>;
    if (/intro|前奏/.test(l)) m = { zoom: 1.12, tilt: 6, punch: 0.015 };
    else if (/pre|预副|build/.test(l)) { m = { zoom: 0.9, tilt: -6, punch: 0.02 }; extra.push({ t: s.t + len * 0.6, zoom: 0.95, tilt: -4, sway: 14 * sway, blend: len * 0.35, punch: 0.035 }); }
    else if (/chorus|副歌|hook|drop|dance/.test(l)) m = { zoom: 1.05, tilt: 4, sway: 20 * sway, punch: 0.05 };   // angled follow, alternating side per section = slow sweeps
    else if (/bridge|break|间奏|桥/.test(l)) m = { zoom: 1.05, orbit: 4 * sway, punch: 0.01 };
    else if (/outro|尾/.test(l)) m = { zoom: 1.2, tilt: 8, punch: 0.015 };
    else m = { sway: 24 * sway, punch: 0.025 };           // verse: three-quarter angled follow, side alternates each section (blended = sweep)
    sway = -sway;
    const at = out.find(c => Math.abs(c.t - s.t) < 1);
    if (at) { if (!MODS.some(k => at[k] !== undefined)) Object.assign(at, m); else continue; }
    else out.push({ t: s.t, blend: /chorus|副歌|hook|drop|dance/.test(l) ? 0.8 : 2.5, ...m });
    for (const e of extra) if (!out.some(c => c.t > s.t + 0.5 && c.t < s.t + len - 0.1)) out.push(e);
  }
  return out;
}
