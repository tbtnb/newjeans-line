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

  private hits: number[] = []; private orbitAng = 0;

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
    if (this.keyMode && !this.menuOrbit) { p.pitch = 36; p.dist = 46; p.fov = 42; p.yawOff = 0; p.sway = 0; p.orbit = 0; p.worldYaw = null; p.roll = 0; p.tilt = 0; p.lead = 2.4; delete (p as any).worldYawBlend; }
    const flow = this.flowYaw(t);
    // slow orbit (breakdowns): drifts while active, eases back when the cue ends; never more than ±35°
    if (p.orbit) this.orbitAng = Math.max(-35, Math.min(35, this.orbitAng + p.orbit * dt)); else this.orbitAng *= Math.exp(-dt * 0.6);
    let desiredYaw = flow + (p.yawOff + p.sway + this.orbitAng) * Math.PI / 180;
    const wy = (p as any).worldYawBlend;
    if (p.worldYaw !== null) desiredYaw = wy !== undefined ? angLerp(desiredYaw, p.worldYaw * Math.PI / 180, wy) : p.worldYaw * Math.PI / 180;
    if (this.menuOrbit) desiredYaw = flow + performance.now() / 9000;
    const fx = Math.sin(flow), fz = Math.cos(flow);
    const leadDist = this.keyMode ? Math.max(MIN_DIST, p.dist) * 0.42 : Math.min(p.lead * 9, Math.max(MIN_DIST, p.dist) * 0.2);   // key: look well ahead, head sits low
    const want = this.freezeAt ?? new Vector3(head.x + fx * leadDist, head.y, head.z + fz * leadDist);
    if (!this.initialized) { this.target.copyFrom(want); this.yaw = desiredYaw; this.ty = want.y; this.initialized = true; }
    const kPos = 1 - Math.exp(-dt * 4.5), kYaw = 1 - Math.exp(-dt * 1.6), kY = 1 - Math.exp(-dt * 2.5);
    this.target.x += (want.x - this.target.x) * kPos; this.target.z += (want.z - this.target.z) * kPos;
    this.ty += (want.y - this.ty) * kY; this.target.y = this.ty;

    this.yaw = angLerp(this.yaw, desiredYaw, kYaw);
    // floor: older layouts authored very close distances (15-24); keep the DL-style overview
    let dist = (Math.max(MIN_DIST, p.dist) * p.zoom + this.extraDist) * this.distScale;
    if (this.aspect < 0.95) dist *= Math.pow(Math.min(2.2, 0.95 / this.aspect), 0.35);
    dist = Math.min(dist, 56 * this.distScale + this.extraDist); // cap: wide/zoomed shots on portrait screens never shrink the head below readable size
    // beat punch: a quick push-in on strong hits (kicks), decaying in ~120 ms
    if (p.punch > 0 && this.hits.length && !this.menuOrbit) { const h = lastLE(this.hits, t); if (h > -1e8) dist *= 1 - p.punch * Math.exp(-(t - h) * 9); }
    const pitch = Math.min(84, p.pitch + p.tilt + this.extraPitch) * Math.PI / 180;
    const sh = p.shake + this.shakeBoost;
    const jitter = sh > 0 ? new Vector3((Math.random() - 0.5) * sh * 0.6, (Math.random() - 0.5) * sh * 0.6, (Math.random() - 0.5) * sh * 0.6) : Vector3.Zero();
    const pos = new Vector3(this.target.x - Math.sin(this.yaw) * Math.cos(pitch) * dist, this.target.y + Math.sin(pitch) * dist, this.target.z - Math.cos(this.yaw) * Math.cos(pitch) * dist);
    this.cam.position.copyFrom(pos.add(jitter));
    this.cam.fov = p.fov * Math.PI / 180;
    const roll = p.roll * Math.PI / 180;
    this.cam.upVector = new Vector3(Math.sin(roll) * Math.cos(this.yaw), Math.cos(roll), -Math.sin(roll) * Math.sin(this.yaw));
    this.cam.setTarget(this.target.add(jitter.scale(0.5)));
    this.shakeBoost *= Math.exp(-dt * 6);
  }
}

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
