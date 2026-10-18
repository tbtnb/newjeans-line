// Audio engine for the tapper. All tap times are SONG seconds at the moment the user HEARD the music
// (AudioContext output clock, like the game), never Date.now().
export type Clicker = (ctxTime: number, kind: 'tap' | 'drum' | 'vocal' | 'metro' | 'metroHi') => void;

export class Player {
  ctx: AudioContext | null = null;
  buffer: AudioBuffer | null = null;
  url: string | null = null;
  private src: AudioBufferSourceNode | null = null;
  private el: HTMLAudioElement | null = null; private elNode: MediaElementAudioSourceNode | null = null;
  private gain: GainNode | null = null; private clickGain: GainNode | null = null;
  playing = false; rate = 1; keepPitch = true;
  private from = 0; private startCtx = 0;              // buffer path: song = from + (heardCtx - startCtx) * rate
  private anchorSong = 0; private anchorPerf = 0;      // media path: song = anchorSong + (perf - anchorPerf) * rate
  private pausedAt = 0;
  onEnded: (() => void) | null = null;
  get mediaPath() { return this.rate !== 1 && this.keepPitch && !!this.el; }

  ensure() {
    if (!this.ctx) {
      const AC = (window.AudioContext || (window as any).webkitAudioContext) as typeof AudioContext;
      this.ctx = new AC({ latencyHint: 'interactive' });
      this.gain = this.ctx.createGain(); this.gain.connect(this.ctx.destination);
      this.clickGain = this.ctx.createGain(); this.clickGain.gain.value = 0.55; this.clickGain.connect(this.ctx.destination);
    }
    if (this.ctx.state === 'suspended') void this.ctx.resume();
    return this.ctx;
  }

  /** resolves once the output clock is live (getOutputTimestamp reports real times), so heard-time mapping is stable */
  async ready() {
    const ctx = this.ensure(); if (ctx.state !== 'running') { try { await ctx.resume(); } catch { /* */ } }
    for (let i = 0; i < 60; i++) { const ts = (ctx as any).getOutputTimestamp?.(); if (!ts || (ts.contextTime > 0 && ts.performanceTime > 0 && ctx.currentTime > 0.05)) break; await new Promise(r => setTimeout(r, 25)); }
  }
  async load(data: ArrayBuffer, blobUrl: string) {
    const ctx = this.ensure();
    this.stop(); this.pausedAt = 0;
    this.buffer = await ctx.decodeAudioData(data.slice(0));
    if (this.url) URL.revokeObjectURL(this.url);
    this.url = blobUrl;
    if (this.elNode) { try { this.elNode.disconnect(); } catch { /* */ } }
    this.el = new Audio(); this.el.src = blobUrl; this.el.preload = 'auto'; (this.el as any).preservesPitch = true; (this.el as any).webkitPreservesPitch = true;
    this.elNode = ctx.createMediaElementSource(this.el); this.elNode.connect(this.gain!);
    this.el.onended = () => { if (this.mediaPath && this.playing) { this.playing = false; this.pausedAt = this.duration; this.onEnded?.(); } };
  }
  get duration() { return this.buffer?.duration ?? 0; }

  /** ctx time that is being heard right now, and the perf time it corresponds to */
  private heardNow(): { ctxT: number; perf: number } {
    const ctx = this.ctx!;
    const ts = (ctx as any).getOutputTimestamp?.();
    if (ts && ts.contextTime > 0 && ts.performanceTime > 0) return { ctxT: ts.contextTime, perf: ts.performanceTime };
    const lat = (ctx as any).outputLatency ?? ctx.baseLatency ?? 0;
    return { ctxT: ctx.currentTime - lat, perf: performance.now() };
  }
  /** ctx time heard at a given performance.now() time (e.g. an input event's timeStamp) */
  heardCtxAt(perf: number) { const h = this.heardNow(); return h.ctxT + (perf - h.perf) / 1000; }

  /** song time heard at performance time perf (event.timeStamp); null if not playing */
  songAtPerf(perf: number): number {
    if (!this.playing) return this.pausedAt;
    if (this.mediaPath) { this.syncAnchor(); const lat = (this.ctx as any).outputLatency ?? this.ctx!.baseLatency ?? 0; return this.anchorSong + ((perf - this.anchorPerf) / 1000) * this.rate - lat * this.rate; }
    return this.from + (this.heardCtxAt(perf) - this.startCtx) * this.rate;
  }
  songNow() { return this.songAtPerf(performance.now()); }
  /** ctx time at which song time s will be heard (for scheduling clicks) */
  ctxForSong(s: number) {
    if (this.mediaPath) { const now = this.songNow(); return this.ctx!.currentTime + (s - now) / this.rate; }
    // heard ctx timeline == scheduling timeline (a source started at ctx time T is heard at output contextTime T)
    return this.startCtx + (s - this.from) / this.rate;
  }
  private syncAnchor() {
    if (!this.el) return; const now = performance.now(); const pred = this.anchorSong + ((now - this.anchorPerf) / 1000) * this.rate;
    const ct = this.el.currentTime; if (Math.abs(pred - ct) > 0.04 || this.anchorPerf === 0) { this.anchorSong = ct; this.anchorPerf = now; }
  }

  play(from: number) {
    const ctx = this.ensure(); if (!this.buffer) return;
    this.stopSources();
    from = Math.max(0, Math.min(from, this.duration - 0.01));
    this.playing = true; this.from = from;
    if (this.mediaPath) {
      const el = this.el!; el.playbackRate = this.rate; (el as any).preservesPitch = true; el.currentTime = from; this.anchorPerf = 0; void el.play(); this.syncAnchor();
    } else {
      const s = ctx.createBufferSource(); s.buffer = this.buffer; s.playbackRate.value = this.rate; s.connect(this.gain!);
      this.startCtx = ctx.currentTime + 0.06; s.start(this.startCtx, from);
      s.onended = () => { if (this.src === s && this.playing) { this.playing = false; this.pausedAt = this.duration; this.onEnded?.(); } };
      this.src = s;
    }
  }
  private stopSources() {
    if (this.src) { try { this.src.onended = null; this.src.stop(); } catch { /* */ } this.src = null; }
    if (this.el && !this.el.paused) this.el.pause();
  }
  stop() { if (this.playing) this.pausedAt = Math.max(0, Math.min(this.songNow(), this.duration)); this.playing = false; this.stopSources(); }
  seek(t: number) { const was = this.playing; this.stop(); this.pausedAt = Math.max(0, Math.min(t, this.duration)); if (was) this.play(this.pausedAt); }
  get position() { return this.playing ? this.songNow() : this.pausedAt; }

  /** short synthesized click at ctx time t */
  click: Clicker = (t, kind) => {
    const ctx = this.ctx; if (!ctx || t < ctx.currentTime - 0.01) return;
    const o = ctx.createOscillator(); const g = ctx.createGain();
    const f = kind === 'drum' ? 180 : kind === 'vocal' ? 1320 : kind === 'metroHi' ? 1760 : kind === 'metro' ? 1100 : 880;
    o.type = kind === 'drum' ? 'triangle' : 'sine'; o.frequency.setValueAtTime(f, t); if (kind === 'drum') o.frequency.exponentialRampToValueAtTime(60, t + 0.08);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(kind === 'drum' ? 0.9 : 0.5, t + 0.002); g.gain.exponentialRampToValueAtTime(0.0001, t + (kind === 'drum' ? 0.12 : 0.06));
    o.connect(g); g.connect(this.clickGain!); o.start(t); o.stop(t + 0.15);
  };
}

/** min/max peaks per bucket for the waveform */
export function peaks(buf: AudioBuffer, perSec = 400) {
  const n = Math.ceil(buf.duration * perSec); const mn = new Float32Array(n), mx = new Float32Array(n);
  const chs = Array.from({ length: buf.numberOfChannels }, (_, i) => buf.getChannelData(i)); const step = buf.sampleRate / perSec;
  for (let i = 0; i < n; i++) {
    let a = 1, b = -1; const s0 = Math.floor(i * step), s1 = Math.min(chs[0].length, Math.floor((i + 1) * step));
    for (let s = s0; s < s1; s += 2) { let v = 0; for (const c of chs) v += c[s]; v /= chs.length; if (v < a) a = v; if (v > b) b = v; }
    mn[i] = a > b ? 0 : a; mx[i] = a > b ? 0 : b;
  }
  return { mn, mx, perSec };
}
