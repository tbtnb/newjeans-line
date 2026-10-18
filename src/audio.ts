/**
 * Audio transport. The song clock is derived from the AudioContext output timestamp
 * (what is actually reaching the speakers), never from accumulated frame deltas.
 */
export class AudioTransport {
  private ctx: AudioContext | null = null;
  private gain: GainNode | null = null;
  private buffer: AudioBuffer | null = null;
  private source: AudioBufferSourceNode | null = null;
  private url: string | null = null;
  private loading: Promise<void> | null = null;
  private offset = 0;      // song position when the source started / where paused
  private startedAt = 0;   // context time at which `offset` is scheduled to be heard
  private lastReported = 0;
  private volume = 0.8;
  playing = false;

  context(): AudioContext {
    if (!this.ctx) {
      this.ctx = new AudioContext({ latencyHint: 'interactive' });
      this.gain = this.ctx.createGain();
      this.gain.gain.value = this.volume;
      this.gain.connect(this.ctx.destination);
    }
    return this.ctx;
  }

  /** Call synchronously inside a user gesture. */
  unlock() { const c = this.context(); if (c.state === 'suspended') void c.resume().catch(() => {}); }

  load(url: string): Promise<void> {
    if (this.url === url && this.buffer) return Promise.resolve();
    if (this.url === url && this.loading) return this.loading;
    this.stop(); this.buffer = null; this.url = url;
    const ctx = this.context();
    this.loading = (async () => {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`音频下载失败（HTTP ${res.status}）`);
      const bytes = await res.arrayBuffer();
      const buf = await ctx.decodeAudioData(bytes);
      if (this.url === url) this.buffer = buf;
    })();
    const p = this.loading;
    p.finally(() => { if (this.loading === p) this.loading = null; }).catch(() => {});
    return p;
  }

  get duration() { return this.buffer?.duration ?? 0; }
  get ready() { return !!this.buffer; }

  /** Context time that is currently audible. */
  private heardContextTime(perfNow = performance.now()): number {
    const c = this.ctx!;
    const ts = typeof c.getOutputTimestamp === 'function' ? c.getOutputTimestamp() : null;
    if (ts && ts.contextTime && ts.performanceTime && ts.contextTime > 0) {
      return ts.contextTime + (perfNow - ts.performanceTime) / 1000;
    }
    return c.currentTime - (c.outputLatency || 0) - (c.baseLatency || 0);
  }

  /** Song time currently heard. `perf` lets input events be mapped to the moment they happened. */
  songTime(perf?: number): number {
    if (!this.ctx || !this.playing) return this.offset;
    const t = this.offset + Math.max(0, this.heardContextTime(perf) - this.startedAt);
    return Math.min(this.duration, t);
  }

  /** Smooth, monotonic clock for rendering. The raw output timestamp advances in audio-callback-sized steps
   *  (10-40 ms on many phones/Bluetooth stacks), which made the line head stutter. We run a perf-clock-driven
   *  estimate and pull it toward the raw audio clock gently (snap on large jumps), so motion is smooth but never
   *  drifts from what is heard. `ahead` predicts the time at which this frame will actually be on screen. */
  private smooth = 0; private smoothPerf = 0;
  renderTime(ahead = 0): number {
    const now = performance.now();
    const raw = this.songTime(now);
    if (!this.playing) { this.smooth = raw; this.smoothPerf = now; this.lastReported = raw; return raw; }
    const pred = this.smooth + (now - this.smoothPerf) / 1000;
    const err = raw - pred;
    this.smooth = Math.abs(err) > 0.08 ? raw : pred + err * 0.12; this.smoothPerf = now;
    const t = Math.min(this.duration, this.smooth + ahead);
    this.lastReported = Math.max(this.lastReported, t); return this.lastReported;
  }

  async play(from: number) {
    const c = this.context();
    if (!this.buffer) throw new Error('歌曲还没有加载完成');
    if (c.state !== 'running') await c.resume();
    this.halt();
    this.offset = Math.max(0, Math.min(from, this.buffer.duration));
    const src = c.createBufferSource();
    src.buffer = this.buffer;
    src.connect(this.gain!);
    // schedule slightly ahead so the start time is exact, then the heard time of `offset` is startAt + outputLatency
    const startAt = c.currentTime + 0.05;
    src.start(startAt, this.offset);
    const outLat = (c.outputLatency || 0) + (c.baseLatency || 0);
    // heardContextTime() already subtracts output latency when using getOutputTimestamp; when using the fallback it subtracts it too.
    this.startedAt = startAt;
    void outLat;
    this.source = src;
    this.playing = true;
    this.lastReported = this.offset; this.smooth = this.offset; this.smoothPerf = performance.now();
    src.onended = () => { if (this.source === src) { this.playing = false; this.offset = this.buffer?.duration ?? 0; this.source = null; } };
  }

  private halt() {
    const s = this.source; this.source = null;
    if (s) { s.onended = null; try { s.stop(); } catch { /* ended */ } s.disconnect(); }
  }

  pause() { if (this.playing) { this.offset = this.songTime(); } this.playing = false; this.halt(); }
  stop() { this.playing = false; this.halt(); this.offset = 0; }

  /** Fade out then stop (fail). */
  fadeOut(sec = 0.6) {
    if (!this.ctx || !this.gain || !this.playing) return;
    const now = this.ctx.currentTime;
    const at = this.songTime();
    this.gain.gain.cancelScheduledValues(now);
    this.gain.gain.setValueAtTime(this.gain.gain.value, now);
    this.gain.gain.linearRampToValueAtTime(0.0001, now + sec);
    const src = this.source;
    setTimeout(() => {
      if (this.source === src) { this.halt(); this.playing = false; this.offset = at; }
      if (this.gain && this.ctx) { this.gain.gain.cancelScheduledValues(this.ctx.currentTime); this.gain.gain.setValueAtTime(this.volume, this.ctx.currentTime); }
    }, sec * 1000 + 30);
  }

  setVolume(v: number) {
    this.volume = Math.max(0, Math.min(1, v));
    if (this.gain && this.ctx) this.gain.gain.setTargetAtTime(this.volume, this.ctx.currentTime, 0.02);
  }

  /** Short UI click synthesized (not used during gameplay). */
  latencyInfo() { const c = this.ctx; return c ? { base: c.baseLatency || 0, output: c.outputLatency || 0, sampleRate: c.sampleRate } : null; }
}
