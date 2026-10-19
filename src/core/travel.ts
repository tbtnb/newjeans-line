import { HEAD_VEC, posAt, spanIndexAt, type Route, type Span } from './path';
import type { TurnRecord } from './game';

// Actual input turns are integrated from the previous position. No projection back to the road.
const cache = new WeakMap<TurnRecord[], { route: Route; count: number; last: TurnRecord | undefined; spans: Span[] }>();
export function travelledSpans(route: Route, turns: TurnRecord[]): Span[] {
  const old = cache.get(turns);
  if (old?.route === route && old.count === turns.length && old.last === turns.at(-1)) return old.spans;
  const events = turns.filter(r => r.tapT >= 0 && r.tapT <= route.duration).slice().sort((a,b) => a.tapT-b.tapT);
  const times = [...new Set([0, route.duration, ...route.spans.flatMap(s => [s.t0,s.t1]), ...events.map(r => r.tapT)])].sort((a,b)=>a-b);
  const spans: Span[] = []; let x=route.spans[0].x0,z=route.spans[0].z0,h=route.spans[0].heading,j=0;
  for(let i=0;i<times.length-1;i++) {
    const t0=times[i],t1=times[i+1];
    while(j<events.length && events[j].tapT<=t0+1e-10) {h=route.headingAfter[events[j].index];j++;}
    const s=route.spans[spanIndexAt(route,(t0+t1)/2)];
    const a=posAt(route,t0),b=posAt(route,t1);
    spans.push({...s,t0,t1,x0:x,z0:z,y0:a.y,y1:b.y,heading:h,vy:s.vy-30*(t0-s.t0),turnIndex:-1});
    const [dx,dz]=HEAD_VEC[h];x+=dx*s.v*(t1-t0);z+=dz*s.v*(t1-t0);
  }
  cache.set(turns,{route,count:turns.length,last:turns.at(-1),spans});return spans;
}
