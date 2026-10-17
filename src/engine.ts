import type { GameOptions, GameSnapshot, GameStatus, Level, PathPoint, Point } from './types';

export const SPEED = 6;
export const TRACK_WIDTH = 1.5;
// The line has 0.15 units of clearance on either side of its centre.
const TURN_WINDOW = (TRACK_WIDTH / 2 - 0.15) / SPEED;
const PERFECT_WINDOW = 0.035;
const EPSILON = 1e-7;
const TRAIL_LIMIT = 180;
const TRAIL_SPACING = 0.08;
const paths = new WeakMap<Level, PathPoint[]>();

export function buildPath(level: Level): PathPoint[] {
  if (!Number.isFinite(level.duration) || level.duration <= 0) throw new Error('歌曲时长无效');
  const points: PathPoint[] = [{ x: 0, z: 0, time: 0 }];
  let direction = 0;
  let previous = 0;
  for (const time of [...level.turns, level.duration]) {
    if (!Number.isFinite(time) || time <= previous || time > level.duration) {
      throw new Error(`歌曲转弯时间无效：${time}`);
    }
    const last = points[points.length - 1];
    const distance = (time - previous) * SPEED;
    points.push({ x: last.x + (direction === 0 ? distance : 0), z: last.z - (direction === 1 ? distance : 0), time });
    direction = 1 - direction;
    previous = time;
  }
  return points;
}

function pathFor(level: Level): PathPoint[] {
  let path = paths.get(level);
  if (!path) { path = buildPath(level); paths.set(level, path); }
  return path;
}

function interpolate(path: PathPoint[], time: number): Point {
  const clamped = Math.max(0, Math.min(path[path.length - 1].time, Number.isFinite(time) ? time : 0));
  let low = 0;
  let high = path.length - 1;
  while (low + 1 < high) {
    const middle = (low + high) >> 1;
    if (path[middle].time <= clamped) low = middle;
    else high = middle;
  }
  const a = path[low];
  const b = path[high];
  const fraction = (clamped - a.time) / (b.time - a.time);
  return { x: a.x + (b.x - a.x) * fraction, z: a.z + (b.z - a.z) * fraction };
}

export function positionAt(level: Level, time: number): Point {
  return interpolate(pathFor(level), time);
}

export class GameEngine {
  readonly level: Level;
  private readonly options: Required<GameOptions>;
  private readonly path: PathPoint[];
  private status: GameStatus = 'ready';
  private time = 0;
  private position: Point = { x: 0, z: 0 };
  private segmentOrigin: Point = { x: 0, z: 0 };
  private segmentStart = 0;
  private direction: 0 | 1 = 0;
  private cursor = 0;
  private hits = 0;
  private combo = 0;
  private resolved = 0;
  private score = 0;
  private lastRating: GameSnapshot['lastRating'] = null;
  private failureReason: string | null = null;
  private trail: Point[] = [];

  constructor(level: Level, options: GameOptions = {}) {
    this.level = level;
    this.path = pathFor(level);
    this.options = {
      practice: options.practice ?? false,
      offsetMs: Number.isFinite(options.offsetMs) ? Math.max(-500, Math.min(500, options.offsetMs!)) : 0,
    };
    this.reset();
  }

  start(): GameSnapshot {
    if (this.status === 'ready') this.status = 'playing';
    return this.snapshot();
  }

  private clock(audioTime: number): number {
    if (!Number.isFinite(audioTime)) return this.time;
    // A decoded source stops exactly at duration. Ensure a positive latency
    // offset cannot leave the last fraction of the level permanently unfinished.
    if (audioTime >= this.level.duration) return this.level.duration;
    return Math.max(0, Math.min(this.level.duration, audioTime - this.options.offsetMs / 1000));
  }

  private moveTo(time: number): void {
    // Anchor each lane to its authored corner time. Integrating from the tap
    // time would make early-then-late valid inputs overshoot a later corner by
    // twice the tolerance. An early turn waits inside the corner footprint.
    const distance = Math.max(0, time - this.segmentStart) * SPEED;
    this.position = {
      x: this.segmentOrigin.x + (this.direction === 0 ? distance : 0),
      z: this.segmentOrigin.z - (this.direction === 1 ? distance : 0),
    };
    this.time = time;
    this.remember();
  }

  private remember(force = false): void {
    const last = this.trail[this.trail.length - 1];
    if (force || !last || Math.hypot(this.position.x - last.x, this.position.z - last.z) >= TRAIL_SPACING) {
      this.trail.push({ ...this.position });
      if (this.trail.length > TRAIL_LIMIT) this.trail.splice(0, this.trail.length - TRAIL_LIMIT);
    }
  }

  private turn(hit: boolean, error = 0): void {
    // A successful tap is inside the solid corner's footprint. Centre the line
    // at that corner before entering its new lane, so valid timing differences
    // never compound into an invisible collision several corners later.
    const corner = this.path[this.cursor + 1];
    this.position = { x: corner.x, z: corner.z };
    this.segmentOrigin = { ...this.position };
    this.segmentStart = corner.time;
    this.direction = this.direction === 0 ? 1 : 0;
    this.cursor++;
    this.resolved++;
    if (hit) {
      this.hits++;
      this.combo++;
      const absolute = Math.abs(error);
      this.lastRating = absolute <= PERFECT_WINDOW ? 'perfect' : 'good';
      this.score += absolute <= PERFECT_WINDOW ? 1 : 1 - 0.4 * (absolute - PERFECT_WINDOW) / (TURN_WINDOW - PERFECT_WINDOW);
    } else {
      this.combo = 0;
      this.lastRating = 'miss';
    }
    this.remember(true);
  }

  private fail(reason: string): void {
    this.status = 'failed';
    this.failureReason = reason;
    this.lastRating = 'miss';
    this.combo = 0;
    this.resolved++;
  }

  update(audioTime: number): GameSnapshot {
    if (this.status !== 'playing') return this.snapshot();
    const target = Math.max(this.time, this.clock(audioTime));
    while (this.cursor < this.level.turns.length) {
      const expected = this.level.turns[this.cursor];
      if (target <= expected + TURN_WINDOW + EPSILON) break;
      if (!this.options.practice) {
        this.moveTo(Math.max(this.time, expected + TURN_WINDOW));
        this.fail('转弯太晚了，在线到达拐角时轻点');
        return this.snapshot();
      }
      // Practice alone recovers missed corners. Resolve at the authored time so
      // large render-frame gaps cannot bend or shorten subsequent segments.
      this.moveTo(Math.max(this.time, expected));
      this.time = expected;
      this.turn(false);
    }
    this.moveTo(target);
    if (audioTime >= this.level.duration && this.time >= this.level.duration - EPSILON && this.cursor >= this.level.turns.length) {
      this.status = 'complete';
      this.time = this.level.duration;
    }
    return this.snapshot();
  }

  tap(audioTime: number): GameSnapshot {
    if (this.status !== 'playing') return this.snapshot();
    this.update(audioTime);
    if (this.status !== 'playing') return this.snapshot();
    const expected = this.level.turns[this.cursor];
    if (expected === undefined) {
      if (!this.options.practice) this.fail('前方还是直线，等到拐角再轻点');
      else { this.combo = 0; this.lastRating = 'miss'; this.resolved++; }
      return this.snapshot();
    }
    const error = this.time - expected;
    if (Math.abs(error) > TURN_WINDOW + EPSILON) {
      if (!this.options.practice) this.fail('转弯太早了，在线到达拐角时轻点');
      else { this.combo = 0; this.lastRating = 'miss'; this.resolved++; }
      return this.snapshot();
    }
    this.turn(true, error);
    return this.snapshot();
  }

  pause(): GameSnapshot {
    if (this.status === 'playing') this.status = 'paused';
    return this.snapshot();
  }

  resume(): GameSnapshot {
    if (this.status === 'paused') this.status = 'playing';
    return this.snapshot();
  }

  reset(startTime = 0): GameSnapshot {
    this.time = Math.max(0, Math.min(this.level.duration, Number.isFinite(startTime) ? startTime : 0));
    this.status = 'ready';
    this.cursor = this.level.turns.filter(time => time <= this.time).length;
    this.direction = this.cursor % 2 as 0 | 1;
    this.position = interpolate(this.path, this.time);
    const corner = this.path[this.cursor];
    this.segmentOrigin = { x: corner.x, z: corner.z };
    this.segmentStart = corner.time;
    this.hits = this.combo = this.resolved = this.score = 0;
    this.lastRating = null;
    this.failureReason = null;
    this.trail = [{ ...this.position }];
    return this.snapshot();
  }

  snapshot(): GameSnapshot {
    const progress = Math.max(0, Math.min(1, this.time / this.level.duration));
    return {
      status: this.status, time: this.time, progress, position: { ...this.position }, direction: this.direction,
      turnsHit: this.hits, nextTurn: this.level.turns[this.cursor] ?? null, combo: this.combo,
      diamonds: Math.min(10, Math.floor((progress + EPSILON) * 10)),
      crowns: Number(progress + EPSILON >= 0.3) + Number(progress + EPSILON >= 0.6) + Number(progress + EPSILON >= 1),
      accuracy: this.resolved ? Math.round(this.score / this.resolved * 1000) / 10 : 100,
      lastRating: this.lastRating, failureReason: this.failureReason, trail: this.trail.map(point => ({ ...point })),
    };
  }
}
