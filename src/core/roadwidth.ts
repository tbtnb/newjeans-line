import { spanPos, type Route } from './path';

/** Separate nearby parallel lanes without changing the authored route, speed or rhythm tolerance.
 * The gold ledge adds 0.32 m to the full width; leave another 0.30 m of visible ground between lanes. */
export function readableRoadWidths(route: Route, widthAt: (t: number) => number): number[] {
  const spans = route.spans;
  return spans.map((s, i) => {
    let w = widthAt(s.t0); const e = spanPos(s, s.t1), axis = s.heading % 2 ? 'x' : 'z', cross = axis === 'x' ? 'z' : 'x';
    const a = {x:s.x0, z:s.z0};
    for (let j = 0; j < spans.length; j++) {
      const o = spans[j];
      if (Math.abs(i-j) < 2 || s.air || o.air || s.heading % 2 !== o.heading % 2) continue;
      if (Math.min(s.y0,s.y1) > Math.max(o.y0,o.y1)+0.8 || Math.min(o.y0,o.y1) > Math.max(s.y0,s.y1)+0.8) continue;
      const b={x:o.x0,z:o.z0}, f=spanPos(o,o.t1);
      if (Math.max(a[axis],e[axis])+w/2 < Math.min(b[axis],f[axis]) || Math.max(b[axis],f[axis])+w/2 < Math.min(a[axis],e[axis])) continue;
      const separation=Math.abs(a[cross]-b[cross]);
      if (separation > 0.1) w=Math.min(w, Math.max(1.2, separation-0.62));
    }
    return w;
  });
}
