import type { Layout, Palette } from '../core/types';
import { hex } from './prefabs';

export const DEFAULT_PALETTE: Palette = {
  skyTop: '#cfe0ee', skyBottom: '#f6f2ea', fog: '#f2efe8', fogStart: 40, fogEnd: 120, ground: '#e8e2d6', groundY: -8,
  road: '#ffffff', roadSide: '#d9d2c4', line: '#ff8a3d', light: '#fff4e6', lightIntensity: 1.0, ambient: '#c9c4bb', particles: null,
};

interface KF { t: number; dur: number; pal: Palette; }
const COLOR_KEYS: (keyof Palette)[] = ['skyTop', 'skyBottom', 'fog', 'ground', 'road', 'roadSide', 'line', 'light', 'ambient'];
const NUM_KEYS: (keyof Palette)[] = ['fogStart', 'fogEnd', 'lightIntensity', 'groundY'];

function mix(a: string, b: string, k: number) {
  const x = hex(a), y = hex(b);
  const f = (p: number, q: number) => Math.round((p + (q - p) * k) * 255).toString(16).padStart(2, '0');
  return '#' + f(x.r, y.r) + f(x.g, y.g) + f(x.b, y.b);
}

/** Deterministic environment timeline: section palettes + colour events, blended over time. */
export class EnvTimeline {
  private kfs: KF[] = [];
  readonly base: Palette;
  constructor(layout: Layout) {
    this.base = { ...DEFAULT_PALETTE, ...layout.palette };
    const raw: { t: number; dur: number; pal: Partial<Palette> }[] = [];
    for (const s of layout.sections ?? []) if (s.palette) raw.push({ t: s.t, dur: 1.6, pal: s.palette });
    for (const e of layout.events ?? []) if (e.type === 'color' && e.palette) raw.push({ t: e.t, dur: e.dur ?? 1.5, pal: e.palette });
    raw.sort((a, b) => a.t - b.t);
    let cur = { ...this.base };
    this.kfs.push({ t: -1e9, dur: 0, pal: cur });
    for (const r of raw) { cur = { ...cur, ...r.pal }; this.kfs.push({ t: r.t, dur: Math.max(0.01, r.dur), pal: cur }); }
  }
  /** Palette at time t (fully settled targets, no blending) — used for road tile colours. */
  settled(t: number): Palette { let p = this.kfs[0].pal; for (const k of this.kfs) if (k.t <= t) p = k.pal; return p; }
  at(t: number): Palette {
    let i = 0; for (let j = 0; j < this.kfs.length; j++) if (this.kfs[j].t <= t) i = j;
    const k = this.kfs[i]; const prev = i > 0 ? this.kfs[i - 1].pal : k.pal;
    const f = Math.min(1, (t - k.t) / k.dur);
    if (f >= 1) return k.pal;
    const out: Palette = { ...k.pal };
    for (const key of COLOR_KEYS) (out as any)[key] = mix(prev[key] as string, k.pal[key] as string, f);
    for (const key of NUM_KEYS) { const a = prev[key] as number | null, b = k.pal[key] as number | null; (out as any)[key] = a === null || b === null ? b : a + (b - a) * f; }
    if (f < 0.5) out.particles = prev.particles;
    return out;
  }
}
