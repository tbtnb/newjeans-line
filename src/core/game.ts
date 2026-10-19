import type { LevelData } from './types';
import { buildRoute, spanIndexAt, spanPos, type Route } from './path';
import { linePos } from './linepath';
import { readableRoadWidths } from './roadwidth';
import {denseWindows,inDenseWindow,EdgeGrace} from './edgeassist';

export const WINDOW_MAX = 0.15;     // ± seconds, hard cap (sparse taps on a wide road)
export const WINDOW_MIN = 0.045;    // ± seconds, absolute floor
export const WINDOW_GAP_RATIO = 0.5; // window may never exceed half the neighbouring gap (neighbouring windows touch, never overlap)
/** Road-geometry tolerance (as in Dancing Line): a late tap survives while the head centre is still on the road past the
 * corner, i.e. (road width / 2) / speed; an early tap inside the same window snaps the turn onto the corner. */
export function geometricWindow(roadWidth: number, speed: number) { return roadWidth / 2 / Math.max(1e-6, speed); }
export function roadWidthAt(widths: { t: number; w: number }[] | undefined, t: number) {
  let w = 2.2; for (const x of [...(widths ?? [])].sort((a, b) => a.t - b.t)) if (x.t <= t + 1e-9) w = x.w; return w;
}
export const PERFECT = 0.04;
export const DEBOUNCE = 0.045;
/** Input events are delivered to JS after a frame or two; their timestamps are what we judge. The clock-driven
 * "late" failure therefore waits this long past the deadline so a queued (but in-time) event can still land. */
export const LATE_GRACE = 0.15;
export const LATE_GRACE_MAX = 0.4;

export type Status = 'ready' | 'playing' | 'paused' | 'failed' | 'complete';
export type FailKind = 'late' | 'early' | 'extra' | 'wall';
export interface TurnRecord { index: number; chartT: number; tapT: number; }
export interface Checkpoint { index: number; t: number; cursor: number; diamonds: number[]; }

export function judgmentWindows(taps: number[], geo?: (i: number) => number): number[] {
  return taps.map((t, i) => {
    const prev = i > 0 ? t - taps[i - 1] : Infinity;
    const next = i + 1 < taps.length ? taps[i + 1] - t : Infinity;
    const g = Math.min(prev, next);
    // per-tap window: the road-geometry tolerance, capped at WINDOW_MAX and at half the local minimum gap (neighbouring
    // windows never overlap, so one tap can never count twice); never below WINDOW_MIN unless the gap itself forbids it
    const want = Math.min(WINDOW_MAX, geo ? geo(i) : WINDOW_MAX);
    return Math.min(0.5 * g, Math.max(WINDOW_MIN, Math.min(want, WINDOW_GAP_RATIO * g)));
  });
}

/** Pure rhythm/route state machine. Time is ALWAYS the song time from the audio clock. */
export class Game {
  /** grace before a missing tap is declared late; the app widens it on slow frames (input is delivered once per frame) */
  lateGrace = LATE_GRACE;
  readonly level: LevelData;
  readonly route: Route;
  readonly taps: number[];
  readonly windows: number[];
  readonly earlyWindows: number[];
  private widths: number[] = [];
  private checkedUntil = 0;
  private dense:[number,number][]=[];private edgeGrace=new EdgeGrace();
  status: Status = 'ready';
  time = 0;
  cursor = 0;
  turns: TurnRecord[] = [];
  perfect = 0;
  good = 0;
  errorSum = 0;
  failKind: FailKind | null = null;
  failTime = 0;
  diamondsTaken = new Set<number>();
  crownsReached = new Set<number>();
  checkpointsUsed = new Set<number>();
  lastAccepted = -Infinity;
  startTime = 0;
  ignoredDuplicates = 0;
  onEvent: ((e: { type: string; [k: string]: unknown }) => void) | null = null;

  constructor(level: LevelData, options: {centerAssist?: boolean} = {}) {
    this.level = level;
    this.route = buildRoute(level.chart, level.layout.elevation ?? [], level.duration);
    this.route.denseAssist = level.id === 'omg';
    this.setCenterAssist(options.centerAssist !== false);
    this.widths = readableRoadWidths(this.route, t => roadWidthAt(level.layout.road?.width, t));
    this.taps = this.route.tapTimes;this.dense=denseWindows(this.taps);
    const spans = this.route.spans;
    const speedAt = (t: number) => { const s = spans.find(x => t >= x.t0 - 1e-9 && t < x.t1) ?? spans[spans.length - 1]; return s?.v ?? 9; };
    this.windows = judgmentWindows(this.taps, i => geometricWindow(roadWidthAt(level.layout.road?.width, this.taps[i]), speedAt(this.taps[i] - 1e-4)));
    this.earlyWindows = [...this.windows];

  }

  /** Apply at run preparation, never reinterpret turns mid-play. */
  setCenterAssist(enabled: boolean) { this.route.freeTurns = this.level.id === 'omg' && !enabled; }

  get progress() { return Math.max(0, Math.min(1, this.time / this.level.duration)); }

  /** Prepare a run that starts at song time t (0 or a checkpoint/rewind point). */
  prepare(t = 0, keepTurns = false) {
    this.status = 'ready';
    this.time = t; this.startTime = t;
    this.cursor = this.taps.findIndex(x => x > t + 1e-6); if (this.cursor < 0) this.cursor = this.taps.length;
    if (keepTurns) this.turns = this.turns.filter(r => r.chartT <= t && r.tapT <= t);
    else { this.turns = []; this.perfect = this.good = 0; this.errorSum = 0; }
    // corners before the start point count as taken exactly on the chart (checkpoint / rewind / mid-level start)
    const have = new Set(this.turns.map(r => r.index));
    for (let i = 0; i < this.cursor; i++) if (!have.has(i)) this.turns.push({ index: i, chartT: this.taps[i], tapT: this.taps[i] });
    this.turns.sort((a, b) => a.index - b.index);
    this.failKind = null; this.failTime = 0; this.ignoredDuplicates = 0; this.checkedUntil = t;
    this.lastAccepted = -Infinity;this.edgeGrace.reset();
    for (const i of [...this.diamondsTaken]) if (this.level.layout.diamonds[i].t > t) this.diamondsTaken.delete(i);
    for (const i of [...this.crownsReached]) if (this.level.layout.crowns[i].t > t + 1e-6) this.crownsReached.delete(i);
  }

  start() { if (this.status === 'ready') this.status = 'playing'; }
  pause() { if (this.status === 'playing') this.status = 'paused'; }
  resume() { if (this.status === 'paused') this.status = 'playing'; }

  private fail(kind: FailKind, t: number) {
    this.status = 'failed'; this.failKind = kind; this.failTime = t; this.time = t;
    this.onEvent?.({ type: 'fail', kind, t });
  }

  update(t: number) {
    if (this.status !== 'playing') return;
    t = Math.max(this.time, t);
    if (this.route.freeTurns) {
      // Give timestamped input its delivery grace, then sweep the real trajectory against the road.
      const end = Math.max(this.startTime, t - this.lateGrace);
      for (let q=this.checkedUntil; q<end-1e-9;) {
        q=Math.min(end,q+1/120);
        if (!this.edgeGrace.survives(q,this.roadDistance(q),inDenseWindow(this.dense,q))) { this.fail('wall',q); return; }
      }
      this.checkedUntil=end;
    } else if (this.cursor < this.taps.length) {
      const deadline = this.taps[this.cursor] + this.windows[this.cursor];
      if (t > deadline + this.lateGrace) { this.collect(deadline); this.fail('late', deadline); return; }
    }
    this.collect(t);
    this.time = t;
    if (t >= this.level.duration - 1e-3 && this.cursor >= this.taps.length) {
      this.status = 'complete'; this.time = this.level.duration;
      this.onEvent?.({ type: 'complete' });
    }
  }

  roadWidth(t:number){return this.widths[spanIndexAt(this.route,t)];}

  private roadDistance(t: number): number {
    const p = linePos(this.route, this.turns, t, this.cursor), idx = spanIndexAt(this.route,t);
    const current = this.route.spans[idx];
    // Falling is authored vertical motion; no invisible wall is introduced during flight.
    if (current.air) return 0;
    let distance=Infinity;
    for (let i=Math.max(0,idx-2); i<=Math.min(this.route.spans.length-1,idx+2); i++) {
      const s=this.route.spans[i]; if(s.air) continue;
      if(Math.abs(p.y-spanPos(s,Math.max(s.t0,Math.min(t,s.t1))).y)>0.8) continue;
      const [dx,dz]=s.heading===0?[0,1]:s.heading===1?[1,0]:s.heading===2?[0,-1]:[-1,0];
      const along=(p.x-s.x0)*dx+(p.z-s.z0)*dz,cross=(p.x-s.x0)*dz-(p.z-s.z0)*dx;
      const len=s.v*(s.t1-s.t0);
      const prev=this.route.spans[i-1], next=this.route.spans[i+1];
      const padStart=prev && prev.turnIndex>=0 && !prev.air ? -this.widths[i-1]/2 : i===0?1.5:0;
      const padEnd=s.turnIndex>=0 && next ? this.widths[i+1]/2 : i===this.route.spans.length-1?6:0;
      distance=Math.min(distance,Math.hypot(Math.max(0,Math.abs(cross)-this.widths[i]/2),Math.max(0,-padStart-along,along-len-padEnd)));
    }
    return distance;
  }

  private collect(t: number) {
    const { diamonds, crowns } = this.level.layout;
    diamonds.forEach((d, i) => { if (!this.diamondsTaken.has(i) && d.t <= t && d.t > this.startTime - 1e-6) { this.diamondsTaken.add(i); this.onEvent?.({ type: 'diamond', index: i, t: d.t }); } });
    crowns.forEach((c, i) => { if (!this.crownsReached.has(i) && c.t <= t && c.t > this.startTime + 1e-6) { this.crownsReached.add(i); this.onEvent?.({ type: 'crown', index: i, t: c.t }); } });
  }

  /** A player tap at song time t. Returns 'hit' | 'ignored' | 'fail'. */
  tap(t: number): 'hit' | 'ignored' | 'fail' {
    if (this.status !== 'playing') return 'ignored';
    if (t - this.lastAccepted < DEBOUNCE) { this.ignoredDuplicates++; return 'ignored'; }
    this.update(t);
    if (this.status !== 'playing') return 'fail';
    // judge by the event timestamp itself (it may be slightly older than this.time)
    if (this.cursor >= this.taps.length) { this.fail('extra', t); return 'fail'; }
    const T = this.taps[this.cursor];
    const err = t - T;
    if (!this.route.freeTurns && (err < -this.earlyWindows[this.cursor] - 1e-9 || err > this.windows[this.cursor] + 1e-9)) { this.fail(err < 0 ? 'early' : 'late', t); return 'fail'; }
    this.turns.push({ index: this.cursor, chartT: T, tapT: t });
    if (Math.abs(err) <= PERFECT) this.perfect++; else this.good++;
    this.errorSum += err;
    this.cursor++;
    this.lastAccepted = t;
    this.onEvent?.({ type: 'turn', index: this.cursor - 1, err, t });
    return 'hit';
  }

  /** Latest checkpoint reached in this attempt (or earlier attempts since last full restart). */
  latestCheckpoint(): number { let best = -1; for (const i of this.crownsReached) if (i > best) best = i; return best; }

  crownsEarned(): number {
    if (this.status !== 'complete') return 0;
    return 3 - this.checkpointsUsed.size;
  }
}
