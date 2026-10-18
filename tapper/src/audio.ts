// Audio engine for the tapper. All tap times are SONG seconds at the moment the user HEARD the music
// (AudioContext output clock, like the game), never Date.now().
export type Clicker = (ctxTime: number, kind: 'tap' | 'drum' | 'vocal' | 'metro' | 'metroHi') => void;

// ---- iOS / Safari audio robustness ----
// * Web Audio on iOS uses the "ambient" audio session: the ring/silent switch MUTES it (HTML media is not muted).
//   navigator.audioSession.type = 'playback' (Safari 17+, iOS 17+) moves the page to the playback category.
//   Older iOS: a silent looping <audio> element started in a gesture does the same.
// * An AudioContext only starts inside a user gesture (touchend / click / keydown; NOT pointerdown on iOS) and can drop to
//   'suspended' or the iOS-only 'interrupted' state after calls, Siri, lock screen or tab switches: unlock() re-resumes it.
// * resume() called outside a gesture stays pending forever on iOS, so it is never awaited without a timeout.
export const IS_IOS = /iP(hone|ad|od)/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
export const HAS_AUDIO_SESSION = typeof (navigator as any).audioSession === 'object' && (navigator as any).audioSession !== null;
export function setPlaybackSession() { try { if (HAS_AUDIO_SESSION && (navigator as any).audioSession.type !== 'playback') (navigator as any).audioSession.type = 'playback'; } catch { /* */ } }
setPlaybackSession();
const SILENT_WAV = 'data:audio/wav;base64,UklGRsEIAABXQVZFZm10IBAAAAABAAEARKwAAESsAAABAAgAZGF0YZ0IAACAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIA=';
const withTimeout = <T>(p: Promise<T>, ms: number) => Promise.race([p, new Promise<void>(r => setTimeout(r, ms))]);

export class Player {
  ctx: AudioContext | null = null;
  buffer: AudioBuffer | null = null;
  url: string | null = null;
  private src: AudioBufferSourceNode | null = null;
  private el: HTMLAudioElement | null = null; private silentEl: HTMLAudioElement | null = null;
  private clockLive = false; onState: ((s: string) => void) | null = null; onBlocked: (() => void) | null = null;
  private gain: GainNode | null = null; private clickGain: GainNode | null = null;
  playing = false; rate = 1; keepPitch = true;
  private from = 0; private startCtx = 0;              // buffer path: song = from + (heardCtx - startCtx) * rate
  private anchorSong = 0; private anchorPerf = 0;      // media path: song = anchorSong + (perf - anchorPerf) * rate
  private pausedAt = 0;
  onEnded: (() => void) | null = null;
  get mediaPath() { return this.rate !== 1 && this.keepPitch && !!this.el; }

  /** the real-time context; created lazily (ideally inside a gesture via unlock()) */
  ensure() {
    if (!this.ctx) {
      const AC = (window.AudioContext || (window as any).webkitAudioContext) as typeof AudioContext;
      try { this.ctx = new AC({ latencyHint: 'interactive' }); } catch { this.ctx = new AC(); }
      this.gain = this.ctx.createGain(); this.gain.connect(this.ctx.destination);
      this.clickGain = this.ctx.createGain(); this.clickGain.gain.value = 0.55; this.clickGain.connect(this.ctx.destination);
      this.ctx.onstatechange = () => { if (this.ctx!.state !== 'running') this.clockLive = false; this.onState?.(this.ctx!.state as string); };
    }
    return this.ctx;
  }
  get state(): string { return this.ctx ? (this.ctx.state as string) : 'none'; }
  get locked() { return this.state !== 'running'; }

  /** call SYNCHRONOUSLY from a user-gesture handler (click / touchend / keydown). Safe to call often. */
  unlock() {
    setPlaybackSession();
    const ctx = this.ensure();
    if (ctx.state !== 'running') {
      try { void ctx.resume().catch(() => {}); } catch { /* */ }
      try { const b = ctx.createBuffer(1, 1, ctx.sampleRate); const s = ctx.createBufferSource(); s.buffer = b; s.connect(ctx.destination); s.start(0); } catch { /* */ }
    }
    // iOS without navigator.audioSession: a playing (silent) media element keeps Web Audio audible with the silent switch on
    if (IS_IOS && !HAS_AUDIO_SESSION) {
      if (!this.silentEl) { const a = new Audio(SILENT_WAV); a.loop = true; a.setAttribute('playsinline', ''); (a as any).playsInline = true; this.silentEl = a; }
      if (this.silentEl.paused) void this.silentEl.play().catch(() => {});
    }
    // (no muted "priming" of the slow-playback <audio>: in WebKit a primed-then-paused element can ignore playbackRate;
    //  instead the slow path is started synchronously inside the gesture, see main.ts togglePlay / startRec)
    this.onState?.(ctx.state as string);
  }

  /** resolves once the context runs and the output clock is live (getOutputTimestamp reports real times). Never hangs. */
  async ready() {
    const ctx = this.ensure();
    if (ctx.state !== 'running') { try { await withTimeout(ctx.resume(), 1500); } catch { /* */ } }
    if (this.clockLive && ctx.state === 'running') return;
    for (let i = 0; i < 60; i++) { const ts = (ctx as any).getOutputTimestamp?.(); if (!ts || (ts.contextTime > 0 && ts.performanceTime > 0 && ctx.currentTime > 0.05)) break; await new Promise(r => setTimeout(r, 25)); }
    this.clockLive = ctx.state === 'running';
  }
  /** true if play() can start right now with a stable clock (lets gesture handlers start media synchronously) */
  get readyNow() { return !!this.ctx && this.ctx.state === 'running' && this.clockLive; }

  /** decode without needing a running (gesture-unlocked) context; mediaUrl = network URL (or blob: for local files) */
  async load(data: ArrayBuffer, mediaUrl: string) {
    this.stop(); this.pausedAt = 0;
    const dc: BaseAudioContext = this.ctx ?? new OfflineAudioContext(2, 1, 48000);
    this.buffer = await dc.decodeAudioData(data.slice(0));
    if (this.url?.startsWith('blob:') && this.url !== mediaUrl) URL.revokeObjectURL(this.url);
    this.url = mediaUrl;
    if (this.el) { this.el.pause(); this.el.removeAttribute('src'); this.el.load(); }
    // slow + keep-pitch playback plays this element DIRECTLY (no MediaElementSource: it is silent in some iOS versions)
    const el = new Audio(); el.preload = 'metadata'; el.setAttribute('playsinline', ''); (el as any).playsInline = true;
    (el as any).preservesPitch = true; (el as any).webkitPreservesPitch = true; el.src = mediaUrl;
    el.onended = () => { if (this.mediaPath && this.playing) { this.playing = false; this.pausedAt = this.duration; this.onEnded?.(); } };
    // Safari resets playbackRate to defaultPlaybackRate when media (re)loads or starts: re-apply the wanted rate
    // WebKit can also keep playing at 1.0 while playbackRate reads 0.75 (rate set before the media is ready): force a real change
    const fixRate = () => { if (this.mediaPath && this.playing) this.forceRate(); };
    for (const ev of ['loadeddata', 'canplay', 'playing']) el.addEventListener(ev, fixRate);
    this.el = el;
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
  private forceRate() { const el = this.el; if (!el) return; el.defaultPlaybackRate = this.rate; el.playbackRate = this.rate === 1 ? 0.99 : 1; el.playbackRate = this.rate; (el as any).preservesPitch = true; }
  private rateProbe = { ct: -1, perf: 0, fixes: 0, start: 0 };
  /** watchdog: measured element speed must match the wanted rate (WebKit sometimes silently ignores playbackRate) */
  private checkRate() {
    const el = this.el; if (!el || el.paused || el.readyState < 3) { this.rateProbe.ct = -1; this.rateProbe.start = performance.now(); return; }
    const now = performance.now(), pr = this.rateProbe;
    if (pr.ct < 0) { if (now - pr.start < 1000) return; pr.ct = el.currentTime; pr.perf = now; return; }   // skip start-up buffering
    const dt = (now - pr.perf) / 1000; if (dt < 1.5) return;
    const speed = (el.currentTime - pr.ct) / dt; pr.ct = el.currentTime; pr.perf = now;
    if (Math.abs(speed - this.rate) > 0.2 * this.rate && pr.fixes < 3) { pr.fixes++; this.forceRate(); this.anchorPerf = 0; }
  }
  private syncAnchor() {
    if (this.mediaPath && this.playing) this.checkRate();
    if (!this.el) return; const now = performance.now(); const pred = this.anchorSong + ((now - this.anchorPerf) / 1000) * this.rate;
    const ct = this.el.currentTime; if (Math.abs(pred - ct) > 0.04 || this.anchorPerf === 0) { this.anchorSong = ct; this.anchorPerf = now; }
  }

  play(from: number) {
    const ctx = this.ensure(); if (!this.buffer) return;
    this.stopSources();
    from = Math.max(0, Math.min(from, this.duration - 0.01));
    this.playing = true; this.from = from;
    if (this.mediaPath) {
      const el = this.el!; el.muted = false; el.defaultPlaybackRate = this.rate; el.playbackRate = this.rate; (el as any).preservesPitch = true; (el as any).webkitPreservesPitch = true; el.currentTime = from; this.anchorPerf = 0; this.rateProbe = { ct: -1, perf: 0, fixes: 0, start: performance.now() };
      void el.play().then(() => { this.forceRate(); for (const ms of [200, 600]) setTimeout(() => { if (this.mediaPath && this.playing && this.el === el) this.forceRate(); }, ms); }, () => { if (this.mediaPath && this.playing && this.el === el && el.paused) { this.playing = false; this.pausedAt = from; this.onBlocked?.(); } }); this.syncAnchor();
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
