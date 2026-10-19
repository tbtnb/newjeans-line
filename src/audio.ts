/**
 * Audio transport. The song clock is derived from the AudioContext output timestamp
 * (what is actually reaching the speakers), never from accumulated frame deltas.
 */
// iOS: Web Audio uses the "ambient" session, so the ring/silent switch mutes it. 'playback' (Safari 17+) ignores the switch.
const IS_IOS = typeof navigator !== 'undefined' && (/iP(hone|ad|od)/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1));
const HAS_AUDIO_SESSION = typeof navigator !== 'undefined' && typeof (navigator as any).audioSession === 'object' && (navigator as any).audioSession !== null;
function setPlaybackSession() { try { if (HAS_AUDIO_SESSION && (navigator as any).audioSession.type !== 'playback') (navigator as any).audioSession.type = 'playback'; } catch { /* */ } }
// (set on the first gesture in unlock(), not at module load: no session side effects before the page is interactive)
const SILENT_WAV = 'data:audio/wav;base64,UklGRiwAAABXQVZFZm10IBAAAAABAAEARKwAAESsAAABAAgAZGF0YQgAAACAgICAgICAgA==';

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
  private playbackVersion = 0;
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
  /** Call synchronously inside a user gesture (click / touchend / keydown). Also recovers iOS 'interrupted' contexts. */
  unlock() {
    setPlaybackSession();
    const c = this.context();
    if (c.state !== 'running') {
      try { void c.resume().catch(() => {}); } catch { /* */ }
      try { const b = c.createBuffer(1, 1, c.sampleRate); const s = c.createBufferSource(); s.buffer = b; s.connect(c.destination); s.start(0); } catch { /* */ }
    }
    if (IS_IOS && !HAS_AUDIO_SESSION) {   // older iOS: a playing media element keeps Web Audio audible with the silent switch on
      if (!this.silentEl) { this.silentEl = new Audio(SILENT_WAV); this.silentEl.loop = true; this.silentEl.setAttribute('playsinline', ''); }
      if (this.silentEl.paused) void this.silentEl.play().catch(() => {});
    }
  }
  private silentEl: HTMLAudioElement | null = null;
  get state(): string { return this.ctx ? (this.ctx.state as string) : 'none'; }

  /** Download progress 0..1 (or -1 when the size is unknown) while load() runs. */
  onProgress: ((f: number, bytes: number) => void) | null = null;

  load(url: string): Promise<void> {
    if (this.url === url && this.buffer) return Promise.resolve();
    if (this.url === url && this.loading) return this.loading;
    this.stop(); this.buffer = null; this.url = url;
    const ctx = this.context();   // created early (as before): the song clock relies on a context that has been ticking
    this.loading = (async () => {
      const bytes = await this.download(url);
      // Decode on an OfflineAudioContext, never on the live context: on iOS the live context can sit 'suspended' /
      // 'interrupted' (no gesture yet, 'playback' audio session, call/Siri) and decodeAudioData on it may never settle.
      // AudioBuffers are context-independent; decoding at the live rate avoids a resample at play time.
      const rate = ctx.sampleRate;
      let dc: BaseAudioContext;
      try { dc = new OfflineAudioContext(2, 1, rate); } catch { dc = ctx; }
      const buf = await withTimeout(dc.decodeAudioData(bytes), 30000, '音频解码超时，请刷新重试');
      if (this.url === url) this.buffer = buf;
    })();
    const p = this.loading;
    p.finally(() => { if (this.loading === p) this.loading = null; }).catch(() => {});
    return p;
  }

  /** fetch with progress and a stall timeout (no bytes for 25 s = fail with a message instead of hanging forever). */
  private async download(url: string): Promise<ArrayBuffer> {
    const ac = typeof AbortController !== 'undefined' ? new AbortController() : null;
    let stall: ReturnType<typeof setTimeout> | undefined;
    const arm = () => { clearTimeout(stall); stall = setTimeout(() => ac?.abort(), 25000); };
    arm();
    try {
      const res = await fetch(url, ac ? { signal: ac.signal } : undefined);
      if (!res.ok) throw new Error(`音频下载失败（HTTP ${res.status}）`);
      const total = Number(res.headers.get('content-length')) || 0;
      if (!res.body || typeof res.body.getReader !== 'function') { arm(); return await res.arrayBuffer(); }
      const rd = res.body.getReader(); const parts: Uint8Array[] = []; let n = 0;
      for (;;) {
        const { done, value } = await rd.read(); if (done) break;
        parts.push(value); n += value.byteLength; arm();
        try { this.onProgress?.(total ? Math.min(1, n / total) : -1, n); } catch { /* */ }
      }
      const out = new Uint8Array(n); let o = 0; for (const c of parts) { out.set(c, o); o += c.byteLength; }
      return out.buffer;
    } catch (e) {
      if ((e as Error)?.name === 'AbortError') throw new Error('音频下载超时（网络太慢），请刷新重试');
      throw e;
    } finally { clearTimeout(stall); }
  }

  /** Song position where playback ends: the buffer end, or an earlier level end set with setEnd(). */
  private endAt: number | null = null; private endFade = 1.5;
  get duration() { const d = this.buffer?.duration ?? 0; return this.endAt !== null ? Math.min(d, this.endAt) : d; }
  /** Level ends before the audio does: fade out over `fade` s ending exactly at song time `end`, then stop (null = play to the end). */
  setEnd(end: number | null, fade = 1.5) { this.endAt = end; this.endFade = fade; }
  get ready() { return !!this.buffer; }

  /** Context time that is currently audible. */
  private heardContextTime(perfNow = performance.now()): number {
    const c = this.ctx!;
    const ts = typeof c.getOutputTimestamp === 'function' ? c.getOutputTimestamp() : null;
    if (ts && ts.contextTime && ts.performanceTime && ts.contextTime > 0) {
      return ts.contextTime + (perfNow - ts.performanceTime) / 1000;
    }
    // Safari may not expose a usable output timestamp. Preserve the original event time here too:
    // queued touch events must not be judged at their later JS delivery time.
    return c.currentTime - (c.outputLatency || 0) - (c.baseLatency || 0) - (performance.now() - perfNow) / 1000;
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
    const version=++this.playbackVersion;
    const c = this.context();
    if (!this.buffer) throw new Error('歌曲还没有加载完成');
    // resume() outside a gesture never settles on iOS: don't hang play() on it
    if (c.state !== 'running') await Promise.race([c.resume().catch(() => {}), new Promise(r => setTimeout(r, 1500))]);
    if(version!==this.playbackVersion)return false;
    this.halt();
    this.offset = Math.max(0, Math.min(from, this.duration));
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
    this.restoreGain();   // a previous level end / fail fade may have left the gain ramped down
    if (this.endAt !== null && this.endAt < this.buffer.duration) {
      // scheduled on the context clock, so the fade and the stop are sample-exact relative to the song
      const endCtx = startAt + (this.endAt - this.offset), g = this.gain!.gain;
      const fadeFrom = Math.max(startAt, endCtx - this.endFade);
      if (endCtx > startAt) { g.setValueAtTime(this.offset >= this.endAt - this.endFade ? this.volume * Math.max(0.0001, (this.endAt - this.offset) / this.endFade) : this.volume, fadeFrom); g.linearRampToValueAtTime(0.0001, endCtx); }
      src.stop(Math.max(startAt, endCtx));
    }
    this.source = src;
    this.playing = true;
    this.lastReported = this.offset; this.smooth = this.offset; this.smoothPerf = performance.now();
    src.onended = () => { if (this.source === src) { this.playing = false; this.offset = this.duration; this.source = null; this.restoreGain(); } };
    return true;
  }

  private halt() {
    const s = this.source; this.source = null;
    if (s) { s.onended = null; try { s.stop(); } catch { /* ended */ } s.disconnect(); }
    if (this.endAt !== null) this.restoreGain();
  }
  private restoreGain() { if (this.gain && this.ctx) { this.gain.gain.cancelScheduledValues(this.ctx.currentTime); this.gain.gain.setValueAtTime(this.volume, this.ctx.currentTime); } }

  pause() { this.playbackVersion++; if (this.playing) { this.offset = this.songTime(); } this.playing = false; this.halt(); }
  stop() { this.playbackVersion++; this.playing = false; this.halt(); this.offset = 0; }

  /** Fade out then stop (fail). */
  fadeOut(sec = 0.6) {
    if (!this.ctx || !this.gain || !this.playing) return;
    const now = this.ctx.currentTime;
    const at = this.songTime();
    this.gain.gain.cancelScheduledValues(now);
    this.gain.gain.setValueAtTime(this.gain.gain.value, now);
    this.gain.gain.linearRampToValueAtTime(0.0001, now + sec);
    const src = this.source, version=this.playbackVersion;
    setTimeout(() => {
      if(version!==this.playbackVersion)return;
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

function withTimeout<T>(p: Promise<T>, ms: number, msg: string): Promise<T> {
  return new Promise<T>((res, rej) => { const t = setTimeout(() => rej(new Error(msg)), ms); p.then(v => { clearTimeout(t); res(v); }, e => { clearTimeout(t); rej(e); }); });
}
