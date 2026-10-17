/** One decoded song at a time; playback and pause positions use the audio clock. */
export class AudioTransport {
  private context: AudioContext | null = null;
  private gain: GainNode | null = null;
  private buffer: AudioBuffer | null = null;
  private source: AudioBufferSourceNode | null = null;
  private loadedUrl: string | null = null;
  private request: AbortController | null = null;
  private loadVersion = 0;
  private sourceVersion = 0;
  private offset = 0;
  private startedAt = 0;
  private volume = 0.75;
  private disposed = false;

  private ensureContext(): AudioContext {
    if (this.disposed) throw new Error('音频播放器已关闭');
    if (!this.context) {
      this.context = new AudioContext({ latencyHint: 'interactive' });
      this.gain = this.context.createGain();
      this.gain.gain.value = this.volume;
      this.gain.connect(this.context.destination);
    }
    return this.context;
  }

  async load(url: string): Promise<void> {
    const context = this.ensureContext();
    // load() is called directly by the start gesture, before fetch/decode awaits.
    // Unlock the silent context now so iOS retains that gesture authorization.
    if (context.state === 'suspended') void context.resume().catch(() => {});
    if (this.loadedUrl === url && this.buffer) return;
    const version = ++this.loadVersion;
    this.request?.abort();
    const request = new AbortController();
    this.request = request;
    this.stop();
    this.buffer = null;
    this.loadedUrl = null;
    try {
      const response = await fetch(url, { signal: request.signal });
      if (!response.ok) throw new Error(`音频下载失败（HTTP ${response.status}）`);
      const bytes = await response.arrayBuffer();
      if (version !== this.loadVersion || this.disposed) throw new DOMException('已切换歌曲', 'AbortError');
      let decoded: AudioBuffer;
      try { decoded = await context.decodeAudioData(bytes); }
      catch (error) {
        if (version !== this.loadVersion || this.disposed) throw new DOMException('已切换歌曲', 'AbortError');
        throw new Error('无法解码音频，请重试或换一首歌曲', { cause: error });
      }
      if (version !== this.loadVersion || this.disposed) throw new DOMException('已切换歌曲', 'AbortError');
      this.buffer = decoded;
      this.loadedUrl = url;
    } catch (error) {
      if (request.signal.aborted || version !== this.loadVersion || this.disposed) {
        throw new DOMException('已切换歌曲', 'AbortError');
      }
      if (error instanceof Error && error.message.startsWith('音频下载失败')) throw error;
      if (error instanceof Error && error.message.startsWith('无法解码音频')) throw error;
      throw new Error('音频加载失败，请检查网络后重试', { cause: error });
    } finally {
      if (this.request === request) this.request = null;
    }
  }

  async play(from?: number): Promise<void> {
    const context = this.ensureContext();
    if (!this.buffer) throw new Error('歌曲还没有加载完成');
    // Call resume before yielding: this is the user gesture that unlocks audio
    // on Safari and mobile browsers. Loading a song itself never starts audio.
    const unlock = context.state === 'suspended' ? context.resume() : Promise.resolve();
    const buffer = this.buffer;
    const loadVersion = this.loadVersion;
    // Capture the position before stopping an already-playing source.
    const requested = from === undefined ? this.currentTime : from;
    this.haltSource();
    this.offset = Math.max(0, Math.min(buffer.duration, Number.isFinite(requested) ? requested : 0));
    const version = this.sourceVersion;
    await unlock;
    if (this.disposed || loadVersion !== this.loadVersion || version !== this.sourceVersion || this.buffer !== buffer) return;
    if (context.state !== 'running') throw new Error('浏览器尚未允许播放音频，请再次轻点开始');
    if (this.offset >= buffer.duration) return;
    const source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(this.gain!);
    this.startedAt = context.currentTime;
    this.source = source;
    source.onended = () => {
      if (this.source !== source || this.sourceVersion !== version) return;
      this.offset = buffer.duration;
      this.source = null;
      source.disconnect();
    };
    source.start(0, this.offset);
  }

  private haltSource(): void {
    this.sourceVersion++;
    const source = this.source;
    this.source = null;
    if (source) {
      source.onended = null;
      try { source.stop(); } catch { /* An ended source needs no further stop. */ }
      source.disconnect();
    }
  }

  pause(): void {
    this.offset = this.currentTime;
    this.haltSource();
  }

  stop(): void {
    this.haltSource();
    this.offset = 0;
  }

  get currentTime(): number {
    if (!this.source || !this.context) return this.offset;
    return Math.min(this.duration, this.offset + Math.max(0, this.context.currentTime - this.startedAt));
  }

  get duration(): number { return this.buffer?.duration ?? 0; }

  setVolume(value: number): void {
    this.volume = Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : this.volume;
    if (this.gain && this.context) this.gain.gain.setTargetAtTime(this.volume, this.context.currentTime, 0.02);
  }

  destroy(): void {
    if (this.disposed) return;
    this.disposed = true;
    this.loadVersion++;
    this.request?.abort();
    this.request = null;
    this.stop();
    this.buffer = null;
    this.loadedUrl = null;
    this.gain?.disconnect();
    this.gain = null;
    const context = this.context;
    this.context = null;
    if (context && context.state !== 'closed') void context.close().catch(() => {});
  }
}
