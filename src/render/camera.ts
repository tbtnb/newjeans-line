import { FreeCamera, Scene, Vector3 } from './bjs';
import { posAt, type Route } from '../core/path';
import type { CameraCue } from '../core/types';

export interface CamParams { pitch: number; dist: number; fov: number; yawOff: number; worldYaw: number | null; roll: number; shake: number; lead: number; }
const PRESETS: Record<string, Partial<CamParams>> = {
  iso: { pitch: 52, dist: 31, fov: 36, yawOff: 0 },
  high: { pitch: 64, dist: 38, fov: 36, yawOff: 0 },
  low: { pitch: 32, dist: 24, fov: 42, yawOff: 0 },
  side: { pitch: 42, dist: 31, fov: 38, yawOff: 72 },
  top: { pitch: 80, dist: 42, fov: 36, yawOff: 0 },
  wide: { pitch: 46, dist: 50, fov: 40, yawOff: 0 },
  close: { pitch: 46, dist: 21, fov: 40, yawOff: 0 },
};
const BASE: CamParams = { pitch: 52, dist: 31, fov: 36, yawOff: 0, worldYaw: null, roll: 0, shake: 0, lead: 0.45 };
const smooth = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const angLerp = (a: number, b: number, k: number) => { let d = ((b - a + Math.PI * 3) % (Math.PI * 2)) - Math.PI; return a + d * k; };

function resolve(prev: CamParams, c: CameraCue): CamParams {
  const p: CamParams = { ...prev, ...(c.preset ? PRESETS[c.preset] ?? {} : {}) };
  if (c.preset) { p.worldYaw = null; p.roll = 0; p.shake = 0; }
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

  constructor(scene: Scene, private route: Route, cues: CameraCue[]) {
    this.cam = new FreeCamera('cam', new Vector3(0, 20, -20), scene);
    this.cam.minZ = 0.5; this.cam.maxZ = 600; this.cam.inputs.clear();
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
      worldYaw: c.to.worldYaw ?? null, roll: L(c.from.roll, c.to.roll), shake: L(c.from.shake, c.to.shake), lead: L(c.from.lead, c.to.lead),
      ...(c.to.worldYaw !== null && c.from.worldYaw === null ? { worldYawBlend: k } : {}) } as CamParams;
  }

  flowYaw(t: number): number {
    // mean travel direction over a window — continuous in t, ignores the zig-zag
    const a = posAt(this.route, t - 1.2), b = posAt(this.route, t + 2.8);
    let dx = b.x - a.x, dz = b.z - a.z;
    if (Math.hypot(dx, dz) < 3) { const c = posAt(this.route, t + 0.5); dx = c.x - a.x; dz = c.z - a.z; }
    return Math.atan2(dx, dz);
  }

  snap() { this.initialized = false; }

  update(t: number, head: { x: number; y: number; z: number }, dt: number) {
    const p = this.params(t);
    const flow = this.flowYaw(t);
    let desiredYaw = flow + p.yawOff * Math.PI / 180;
    const wy = (p as any).worldYawBlend;
    if (p.worldYaw !== null) desiredYaw = wy !== undefined ? angLerp(desiredYaw, p.worldYaw * Math.PI / 180, wy) : p.worldYaw * Math.PI / 180;
    if (this.menuOrbit) desiredYaw = flow + performance.now() / 9000;
    const fx = Math.sin(flow), fz = Math.cos(flow);
    const leadDist = p.lead * 9;
    const want = this.freezeAt ?? new Vector3(head.x + fx * leadDist, head.y, head.z + fz * leadDist);
    if (!this.initialized) { this.target.copyFrom(want); this.yaw = desiredYaw; this.ty = want.y; this.initialized = true; }
    const kPos = 1 - Math.exp(-dt * 7.5), kYaw = 1 - Math.exp(-dt * 2.2), kY = 1 - Math.exp(-dt * 3.0);
    this.target.x += (want.x - this.target.x) * kPos; this.target.z += (want.z - this.target.z) * kPos;
    this.ty += (want.y - this.ty) * kY; this.target.y = this.ty;

    this.yaw = angLerp(this.yaw, desiredYaw, kYaw);
    let dist = (p.dist + this.extraDist) * this.distScale;
    if (this.aspect < 0.95) dist *= Math.pow(Math.min(2.2, 0.95 / this.aspect), 0.35);
    const pitch = (p.pitch + this.extraPitch) * Math.PI / 180;
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
