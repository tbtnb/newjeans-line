import { HEAD_VEC, posAt, spanIndexAt, type Route } from './path';
import type { Heading, Vec3 } from './types';
import type { TurnRecord } from './game';

export const SETTLE = 0.28; // seconds for a slightly early/late turn to glide back onto the centreline

const ease = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

/**
 * Where the player's line actually is at time t, given the accepted turns so far.
 * Turns happen at the actual tap time; the small lateral error then eases back to the centreline,
 * so the drawn line never "teleports" and never leaves a correctly-tapped road.
 */
export function linePos(route: Route, turns: TurnRecord[], t: number, cursor: number): Vec3 {
  const taps = route.tapTimes;
  // last accepted turn with tapT <= t
  let k = turns.length - 1;
  while (k >= 0 && turns[k].tapT > t) k--;
  const lastIdx = k >= 0 ? turns[k].index : -1;
  const nextIdx = lastIdx + 1; // next chart turn not yet taken at time t
  const nextT = nextIdx < taps.length && nextIdx < Math.max(cursor, nextIdx + 1) ? taps[nextIdx] : Infinity;
  let base: Vec3;
  if (k >= 0 && t < turns[k].chartT) {
    // turned early: extend the new lane backwards from the corner
    const T = turns[k].chartT; const c = posAt(route, T + 1e-6); const h = route.headingAfter[turns[k].index];
    const v = route.spans[spanIndexAt(route, T + 1e-6)].v; const [dx, dz] = HEAD_VEC[h];
    base = { x: c.x + dx * v * (t - T), y: c.y, z: c.z + dz * v * (t - T) };
  } else if (t > nextT) {
    // past the chart corner without having turned (late tap pending or a miss): keep going straight
    const c = posAt(route, nextT - 1e-6); const s = route.spans[spanIndexAt(route, nextT - 1e-6)]; const [dx, dz] = HEAD_VEC[s.heading];
    base = { x: c.x + dx * s.v * (t - nextT), y: c.y, z: c.z + dz * s.v * (t - nextT) };
  } else base = posAt(route, t);
  if (k >= 0) {
    const r = turns[k]; const err = r.tapT - r.chartT;
    if (Math.abs(err) > 1e-6) {
      const f = 1 - ease((t - r.tapT) / SETTLE);
      if (f > 0) {
        const hPrev: Heading = r.index > 0 ? route.headingAfter[r.index - 1] : route.spans[0].heading;
        const hNew = route.headingAfter[r.index];
        const v = route.spans[spanIndexAt(route, r.chartT + 1e-6)].v;
        const [ax, az] = HEAD_VEC[hPrev]; const [bx, bz] = HEAD_VEC[hNew];
        base.x += err * v * (ax - bx) * f; base.z += err * v * (az - bz) * f;
      }
    }
  }
  return base;
}

/** Heading the line is visually travelling at time t. */
export function lineHeading(route: Route, turns: TurnRecord[], t: number): Heading {
  let k = turns.length - 1;
  while (k >= 0 && turns[k].tapT > t) k--;
  return k >= 0 ? route.headingAfter[turns[k].index] : route.spans[0].heading;
}
