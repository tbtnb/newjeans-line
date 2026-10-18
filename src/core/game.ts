import type { LevelData } from './types';
import { buildRoute, type Route } from './path';

export const WINDOW_MAX = 0.11;     // ± seconds, sparse taps
export const WINDOW_MIN = 0.045;    // ± seconds, absolute floor (16th bursts at 0.11 s gaps get ±49.5 ms)
export const WINDOW_GAP_RATIO = 0.45; // window may never exceed 45 % of the neighbouring gap (no ambiguity)
export const PERFECT = 0.04;
export const DEBOUNCE = 0.045;
/** Input events are delivered to JS after a frame or two; their timestamps are what we judge. The clock-driven
 * "late" failure therefore waits this long past the deadline so a queued (but in-time) event can still land. */
export const LATE_GRACE = 0.15;      // duplicate hardware events closer than this to an accepted tap are ignored

export type Status = 'ready' | 'playing' | 'paused' | 'failed' | 'complete';
export type FailKind = 'late' | 'early' | 'extra';
export interface TurnRecord { index: number; chartT: number; tapT: number; }
export interface Checkpoint { index: number; t: number; cursor: number; diamonds: number[]; }

export function judgmentWindows(taps: number[]): number[] {
  return taps.map((t, i) => {
    const prev = i > 0 ? t - taps[i - 1] : Infinity;
    const next = i + 1 < taps.length ? taps[i + 1] - t : Infinity;
    const g = Math.min(prev, next);
    // per-tap window: ≤ 45 % of the local minimum gap, so neighbouring windows never touch and one tap can never count twice
    return Math.min(0.5 * g, Math.max(WINDOW_MIN, Math.min(WINDOW_MAX, WINDOW_GAP_RATIO * g)));
  });
}

/** Pure rhythm/route state machine. Time is ALWAYS the song time from the audio clock. */
export class Game {
  readonly level: LevelData;
  readonly route: Route;
  readonly taps: number[];
  readonly windows: number[];
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

  constructor(level: LevelData) {
    this.level = level;
    this.route = buildRoute(level.chart, level.layout.elevation ?? [], level.duration);
    this.taps = this.route.tapTimes;
    this.windows = judgmentWindows(this.taps);
  }

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
    this.failKind = null;
    this.lastAccepted = -Infinity;
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
    if (this.cursor < this.taps.length) {
      const deadline = this.taps[this.cursor] + this.windows[this.cursor];
      if (t > deadline + LATE_GRACE) { this.collect(deadline); this.fail('late', deadline); return; }
    }
    this.collect(t);
    this.time = t;
    if (t >= this.level.duration - 1e-3 && this.cursor >= this.taps.length) {
      this.status = 'complete'; this.time = this.level.duration;
      this.onEvent?.({ type: 'complete' });
    }
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
    if (Math.abs(err) > this.windows[this.cursor]) { this.fail(err < 0 ? 'early' : 'late', t); return 'fail'; }
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
