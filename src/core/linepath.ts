import { HEAD_VEC, posAt, spanIndexAt, type Route } from './path';
import type { Heading, Vec3 } from './types';
import type { TurnRecord } from './game';


/**
 * Where the player's line is at time t, given the accepted turns so far.
 * The line always follows the authored centreline with perfectly square corners (as in Dancing Line): an accepted
 * early tap turns exactly at the corner; while a tap is still pending past its corner (late tap within the grace,
 * or a miss) the line keeps going straight past the corner, and snaps back to the centreline once the tap is accepted.
 * No easing / diagonal glide, so the trail is made only of axis-aligned straight runs.
 */
export function linePos(route: Route, turns: TurnRecord[], t: number, cursor: number): Vec3 {
  const nextT = pendingCorner(route, turns, t, cursor);
  if (t > nextT) {
    const c = posAt(route, nextT - 1e-6); const s = route.spans[spanIndexAt(route, nextT - 1e-6)]; const [dx, dz] = HEAD_VEC[s.heading];
    return { x: c.x + dx * s.v * (t - nextT), y: c.y, z: c.z + dz * s.v * (t - nextT) };
  }
  return posAt(route, t);
}

/** Chart time of the first corner not yet taken at time t (Infinity if none). */
export function pendingCorner(route: Route, turns: TurnRecord[], t: number, cursor: number): number {
  const taps = route.tapTimes;
  let k = turns.length - 1;
  while (k >= 0 && turns[k].tapT > t) k--;
  const nextIdx = (k >= 0 ? turns[k].index : -1) + 1;
  return nextIdx < taps.length && nextIdx < Math.max(cursor, nextIdx + 1) ? taps[nextIdx] : Infinity;
}

/** Heading the line is visually travelling at time t. */
export function lineHeading(route: Route, turns: TurnRecord[], t: number): Heading {
  let k = turns.length - 1;
  while (k >= 0 && turns[k].tapT > t) k--;
  return k >= 0 ? route.headingAfter[turns[k].index] : route.spans[0].heading;
}
