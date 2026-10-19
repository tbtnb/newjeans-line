import type { Chart, Dir, Elevation, Heading, Vec3 } from './types';

export const HEAD_VEC: Record<Heading, [number, number]> = { 0: [0, 1], 1: [1, 0], 2: [0, -1], 3: [-1, 0] };
const HEAD_NAME: Record<string, Heading> = { N: 0, E: 1, S: 2, W: 3 };
export const DEFAULT_SPEED = 9;
export const GRAVITY = 30;

/** One straight piece of the route with constant speed and heading. */
export interface Span {
  t0: number; t1: number; x0: number; z0: number; y0: number; y1: number;
  heading: Heading; v: number;
  /** air: parabola between y0 and y1 with initial vertical speed vy */
  air: boolean; vy: number;
  /** index of the chart tap that ENDS this span (turn), or -1 */
  turnIndex: number;
}

export interface Route {
  freeTurns?: boolean; // OMG: turn at the actual input position, without centreline snapping
  spans: Span[];
  duration: number;
  dirs: Dir[];
  tapTimes: number[];
  headingAfter: Heading[]; // heading after tap i
}

/** Airtime for a fall/jump. The line must be back on the road before the next tap, so the flight is shortened
 * (steeper parabola, same gravity) when the next tap comes sooner than the natural flight time. */
export const AIR_MIN = 0.15, AIR_LAND_BEFORE_TAP = 0.05;
export function airTime(dy: number, maxDur = Infinity): { dur: number; vy: number } {
  let dur: number, vy: number;
  if (dy < 0) { vy = 2; dur = (vy + Math.sqrt(vy * vy - 2 * GRAVITY * dy)) / GRAVITY; } else { dur = 0.6; vy = (dy + GRAVITY * dur * dur / 2) / dur; }
  if (dur > maxDur) { dur = Math.max(AIR_MIN, maxDur); vy = (dy + GRAVITY * dur * dur / 2) / dur; }
  return { dur, vy };
}

export function buildRoute(chart: Chart, elevation: Elevation[] = [], duration: number): Route {
  const taps = chart.taps.map(t => t.t);
  const dirs: Dir[] = [];
  let last: Dir = 'L';
  for (const tap of chart.taps) { const d: Dir = tap.dir ?? (last === 'L' ? 'R' : 'L'); dirs.push(d); last = d; }
  const speeds = [...(chart.speed ?? [])].sort((a, b) => a.t - b.t);
  const speedAt = (t: number) => { let v = DEFAULT_SPEED; for (const s of speeds) if (s.t <= t + 1e-9) v = s.v; return v; };
  // collect breakpoints
  const air: { t0: number; t1: number; dy: number; vy: number }[] = [];
  const ramps: { t0: number; t1: number; dy: number }[] = [];
  for (const e of elevation) {
    if (e.type === 'ramp') ramps.push({ t0: e.t0!, t1: e.t1!, dy: e.dy });
    else { const next = taps.find(t => t > e.t! + 1e-6) ?? duration; const a = airTime(e.dy, next - e.t! - AIR_LAND_BEFORE_TAP); air.push({ t0: e.t!, t1: Math.min(e.t! + a.dur, duration), dy: e.dy, vy: a.vy }); }
  }
  const bp = new Set<number>([0, duration, ...taps, ...speeds.map(s => s.t), ...air.flatMap(a => [a.t0, a.t1]), ...ramps.flatMap(r => [r.t0, r.t1])]);
  const points = [...bp].filter(t => t >= 0 && t <= duration).sort((a, b) => a - b);
  // base height (without ramps' partial) at time t
  const baseY = (t: number) => {
    let y = 0;
    for (const a of air) if (t >= a.t1 - 1e-9) y += a.dy;
    for (const r of ramps) { if (t >= r.t1) y += r.dy; else if (t > r.t0) y += r.dy * (t - r.t0) / (r.t1 - r.t0); }
    return y;
  };
  const spans: Span[] = [];
  let heading: Heading = HEAD_NAME[chart.startHeading ?? 'N'];
  let x = 0, z = 0;
  const headingAfter: Heading[] = [];
  let tapCursor = 0;
  const tapIndex = new Map(taps.map((t, i) => [t, i]));
  for (let i = 0; i + 1 < points.length; i++) {
    const t0 = points[i], t1 = points[i + 1];
    if (t1 - t0 < 1e-6) continue;
    const v = speedAt(t0);
    const inAir = air.find(a => t0 >= a.t0 - 1e-9 && t1 <= a.t1 + 1e-9);
    let y0: number, y1: number, vy = 0;
    if (inAir) {
      // parabola anchored at the air start
      const yStart = baseY(inAir.t0 - 1e-6);
      const yy = (t: number) => yStart + inAir.vy * (t - inAir.t0) - GRAVITY * (t - inAir.t0) ** 2 / 2;
      y0 = yy(t0); y1 = yy(t1); vy = inAir.vy - GRAVITY * (t0 - inAir.t0);
    } else { y0 = baseY(t0 + 1e-9); y1 = baseY(t1 - 1e-9); }
    const ti = tapIndex.get(t1);
    spans.push({ t0, t1, x0: x, z0: z, y0, y1, heading, v, air: !!inAir, vy, turnIndex: ti ?? -1 });
    const [dx, dz] = HEAD_VEC[heading];
    x += dx * v * (t1 - t0); z += dz * v * (t1 - t0);
    if (ti !== undefined) {
      heading = ((heading + (dirs[ti] === 'R' ? 1 : 3)) % 4) as Heading;
      headingAfter[ti] = heading; tapCursor++;
    }
  }
  void tapCursor;
  return { spans, duration, dirs, tapTimes: taps, headingAfter };
}

export function spanIndexAt(route: Route, t: number): number {
  const s = route.spans;
  let lo = 0, hi = s.length - 1;
  if (t <= s[0].t0) return 0;
  if (t >= s[hi].t0) return hi;
  while (lo < hi) { const m = (lo + hi + 1) >> 1; if (s[m].t0 <= t) lo = m; else hi = m - 1; }
  return lo;
}

export function spanPos(s: Span, t: number): Vec3 {
  const dt = t - s.t0;
  const [dx, dz] = HEAD_VEC[s.heading];
  const y = s.air ? s.y0 + s.vy * dt - GRAVITY * dt * dt / 2 : s.y0 + (s.y1 - s.y0) * (s.t1 > s.t0 ? dt / (s.t1 - s.t0) : 0);
  return { x: s.x0 + dx * s.v * dt, y, z: s.z0 + dz * s.v * dt };
}

/** Centerline position at time t (extrapolates beyond the end along the last heading). */
export function posAt(route: Route, t: number): Vec3 { return spanPos(route.spans[spanIndexAt(route, t)], t); }
export function headingAt(route: Route, t: number): Heading { return route.spans[spanIndexAt(route, t)].heading; }

/** World position of an anchor: path point at t, `side` units to the right of travel, `along` forward, `y` up. */
export function anchor(route: Route, t: number, side = 0, along = 0, y = 0): { pos: Vec3; heading: Heading } {
  let i = spanIndexAt(route, t);
  // anchors are placed relative to the ground road, never in-air
  while (i > 0 && route.spans[i].air) i--;
  const s = route.spans[i];
  const p = spanPos(s, Math.min(Math.max(t, s.t0), s.t1));
  const [hx, hz] = HEAD_VEC[s.heading];
  const rx = hz, rz = -hx; // right-hand vector in left-handed y-up coords (N -> E is a right turn)
  return { pos: { x: p.x + rx * side + hx * along, y: p.y + y, z: p.z + rz * side + hz * along }, heading: s.heading };
}

export function routeBounds(route: Route) {
  let minX = 0, maxX = 0, minZ = 0, maxZ = 0, minY = 0, maxY = 0;
  for (const s of route.spans) {
    const e = spanPos(s, s.t1);
    for (const p of [{ x: s.x0, y: s.y0, z: s.z0 }, e]) {
      minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x); minZ = Math.min(minZ, p.z); maxZ = Math.max(maxZ, p.z);
      minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y);
    }
  }
  return { minX, maxX, minZ, maxZ, minY, maxY };
}

/** Mean travel position/direction around t (ignores the zig-zag). Used to line scenery along the corridor like DL. */
export function flowFrame(route: Route, t: number, win = 1.2): { x: number; y: number; z: number; fx: number; fz: number } {
  let x = 0, y = 0, z = 0; const n = 9;
  for (let i = 0; i < n; i++) { const p = posAt(route, t - win + (2 * win * i) / (n - 1)); x += p.x; y += p.y; z += p.z; }
  const a = posAt(route, t - win * 1.5), b = posAt(route, t + win * 1.5);
  let fx = b.x - a.x, fz = b.z - a.z; const l = Math.hypot(fx, fz) || 1; fx /= l; fz /= l;
  if (Math.hypot(b.x - a.x, b.z - a.z) < 1) { const [hx, hz] = HEAD_VEC[headingAt(route, t)]; fx = hx; fz = hz; }
  return { x: x / n, y: y / n, z: z / n, fx, fz };
}

export function flowAnchor(route: Route, t: number, side = 0, along = 0, y = 0): { pos: Vec3; yaw: number } {
  const f = flowFrame(route, t);
  const rx = f.fz, rz = -f.fx;
  const g = anchor(route, t, 0, 0, 0).pos.y; // ground height = road height at t (not averaged across falls)
  return { pos: { x: f.x + rx * side + f.fx * along, y: g + y, z: f.z + rz * side + f.fz * along }, yaw: Math.atan2(f.fx, f.fz) };
}
