/**
 * Line skins (head + trail + turn burst + death shatter). Pure data so it can be unit-tested without Babylon.
 * Art: levels-design/skins/<id>/ (Codex concept sheets), runtime textures: public/skins/<id>/.
 * 'classic' is the original look (line colour follows each level's palette) and is the default, so saves without a
 * skin field look exactly as before.
 */
export type SkinDecor = 'none' | 'ears' | 'rivets' | 'bubble' | 'antenna' | 'rec' | 'star';

export interface ParticleSpec {
  /** sprite under public/skins/<id>/ (white-ish, tinted by colors); omitted = soft round spark */
  sprite?: string;
  colors: [string, string];
  count: number;
  size: [number, number];
  life: [number, number];
  power: [number, number];
  gravity: number;
  /** additive blending (glowy) instead of alpha blending */
  add?: boolean;
  /** max angular speed (rad/s) */
  spin?: number;
}

export interface SkinDef {
  id: string;
  name: string;
  nameEn: string;
  desc: string;
  /** classic only: colours come from the level palette (pal.line) */
  levelColor?: boolean;
  head: string;
  trail: string;
  /** emissive as a fraction of the tint colour */
  emissive: number;
  specular: number;
  specPower: number;
  /** seamless surface texture (multiplied over the tint) */
  tex?: string;
  /** head texture; default = tex, null = plain tinted head */
  headTex?: string | null;
  /** world units per texture tile along the run */
  texLen?: number;
  /** nearest-neighbour sampling (pixel art) */
  pixel?: boolean;
  /** view-angle iridescent sheen strength (chrome) */
  sheen?: number;
  /** white fresnel rim + soft highlight (glossy candy / plastic) */
  gloss?: number;
  /** animated film grain strength */
  grain?: number;
  decor: SkinDecor;
  decorColors: [string, string];
  /** colour of the soft glow ring on each turn */
  glow: string;
  burst: ParticleSpec;
  shatter: ParticleSpec & { shards: number };
  /** picker accent */
  ui: string;
  /** optional unlock rule; NOT enforced (all skins are unlocked) */
  unlockHint?: string;
}

export const DEFAULT_SKIN = 'classic';

export const SKINS: SkinDef[] = [
  {
    id: 'classic', name: '经典', nameEn: 'Classic', desc: '原版的纯色线条，颜色随关卡变化。', levelColor: true,
    head: '#ffffff', trail: '#ffffff', emissive: 0.22, specular: 0.08, specPower: 64, decor: 'none', decorColors: ['#ffffff', '#ffffff'],
    glow: '#ffffff',
    burst: { colors: ['#ffffff', '#ffffff'], count: 0, size: [0.16, 0.32], life: [0.2, 0.4], power: [1, 2], gravity: 0 },
    shatter: { colors: ['#ffffff', '#ffffff'], count: 0, size: [0.16, 0.32], life: [0.3, 0.6], power: [2, 4], gravity: -8, shards: 14 },
    ui: '#2c2a28',
  },
  {
    id: 'bunny', name: '兔兔', nameEn: 'Bunny', desc: '奶白方块戴上淡蓝兔耳，转弯时冒出小爱心。',
    head: '#f8fcff', trail: '#ffffff', emissive: 0.26, specular: 0.25, specPower: 48, tex: 'skins/bunny/trail.jpg', texLen: 2,
    headTex: null, gloss: 0.25, decor: 'ears', decorColors: ['#a9d9f5', '#f6bed1'], glow: '#d9f0ff',
    burst: { sprite: 'skins/bunny/particle.png', colors: ['#ff9cc2', '#86c9f2'], count: 9, size: [0.35, 0.67], life: [0.45, 0.8], power: [1.6, 3.2], gravity: 1.8, spin: 1.5 },
    shatter: { sprite: 'skins/bunny/particle.png', colors: ['#a9d9f5', '#f8fcff'], count: 26, size: [0.4, 0.8], life: [0.7, 1.3], power: [2.5, 5.5], gravity: -4, shards: 12, spin: 2 },
    ui: '#7fc0ea',
  },
  {
    id: 'denim', name: 'Y2K 牛仔', nameEn: 'Y2K Denim', desc: '靛蓝斜纹牛仔布配橘色双线缝边和铜铆钉。',
    head: '#ffffff', trail: '#ffffff', emissive: 0.12, specular: 0.06, specPower: 24, tex: 'skins/denim/trail.jpg', texLen: 2,
    decor: 'rivets', decorColors: ['#c8823f', '#f2a23a'], glow: '#ffd08a',
    burst: { sprite: 'skins/denim/particle.png', colors: ['#f2a23a', '#7fa6d6'], count: 8, size: [0.32, 0.58], life: [0.4, 0.7], power: [2, 3.6], gravity: -6, spin: 4 },
    shatter: { sprite: 'skins/denim/particle.png', colors: ['#3d5f9c', '#f2a23a'], count: 24, size: [0.4, 0.72], life: [0.7, 1.2], power: [3, 6], gravity: -12, shards: 16, spin: 5 },
    ui: '#3d5f9c',
  },
  {
    id: 'bubble-gum', name: '泡泡糖', nameEn: 'Bubble Gum', desc: '亮面糖果粉，转弯吹出会破掉的泡泡。',
    head: '#f45c9d', trail: '#ffffff', emissive: 0.2, specular: 0.85, specPower: 96, tex: 'skins/bubble-gum/trail.jpg', texLen: 2, headTex: null, gloss: 0.45,
    decor: 'bubble', decorColors: ['#ffd6e5', '#a8e8cf'], glow: '#ffc2e0',
    burst: { sprite: 'skins/bubble-gum/particle.png', colors: ['#ffd6e5', '#a8e8cf'], count: 8, size: [0.48, 0.96], life: [0.5, 0.9], power: [1, 2.4], gravity: 2.2 },
    shatter: { sprite: 'skins/bubble-gum/particle.png', colors: ['#f45c9d', '#ffd6e5'], count: 28, size: [0.48, 1.2], life: [0.8, 1.5], power: [2, 5], gravity: 1.5, shards: 10 },
    ui: '#ff6fb4',
  },
  {
    id: 'phoning', name: '翻盖机', nameEn: 'Phoning LCD', desc: '复古翻盖手机的背光点阵屏，像素颗粒四散。',
    head: '#ffffff', trail: '#ffffff', emissive: 0.45, specular: 0.05, specPower: 16, tex: 'skins/phoning/trail.png', texLen: 1, pixel: true, gloss: 0.15,
    decor: 'antenna', decorColors: ['#e5ebef', '#f6acc8'], glow: '#b6ffe9',
    burst: { sprite: 'skins/phoning/particle.png', colors: ['#6de8e8', '#f6acc8'], count: 10, size: [0.26, 0.45], life: [0.35, 0.6], power: [2, 4], gravity: -4, add: true },
    shatter: { sprite: 'skins/phoning/particle.png', colors: ['#6de8e8', '#f6acc8'], count: 36, size: [0.29, 0.54], life: [0.6, 1.2], power: [3, 6.5], gravity: -10, shards: 18 },
    ui: '#38c9a6',
  },
  {
    id: 'film', name: 'Ditto 胶片', nameEn: 'Ditto Film', desc: '雾蓝灰的胶片条带着颗粒和漏光，散落成雪。',
    head: '#dfe7ef', trail: '#ffffff', emissive: 0.22, specular: 0.15, specPower: 24, tex: 'skins/film/trail.jpg', texLen: 1, headTex: null, grain: 0.09, sheen: 0.06,
    decor: 'rec', decorColors: ['#ff5a4e', '#e9eef4'], glow: '#eef4ff',
    burst: { sprite: 'skins/film/particle.png', colors: ['#ffffff', '#8fa8c2'], count: 8, size: [0.29, 0.58], life: [0.6, 1.1], power: [0.8, 2], gravity: -0.8, spin: 1 },
    shatter: { sprite: 'skins/film/particle.png', colors: ['#ffffff', '#e8a868'], count: 30, size: [0.32, 0.72], life: [1, 1.8], power: [1.5, 4], gravity: -1.5, shards: 12, spin: 1 },
    ui: '#7f93a8',
  },
  {
    id: 'supernatural', name: '超自然铬', nameEn: 'Supernatural Chrome', desc: '液态铬面带全息虹彩和霓虹边，迸出 Y2K 四芒星。',
    head: '#dce5f0', trail: '#ffffff', emissive: 0.18, specular: 1, specPower: 192, tex: 'skins/supernatural/trail.jpg', texLen: 3, sheen: 0.5, gloss: 0.3,
    decor: 'star', decorColors: ['#f5faff', '#9165ff'], glow: '#bfe2ff',
    burst: { sprite: 'skins/supernatural/particle.png', colors: ['#bdefff', '#d9c7ff'], count: 9, size: [0.35, 0.7], life: [0.35, 0.65], power: [2, 4], gravity: 0, add: true, spin: 3 },
    shatter: { sprite: 'skins/supernatural/particle.png', colors: ['#edf5ff', '#9165ff'], count: 30, size: [0.4, 0.88], life: [0.6, 1.2], power: [3, 7], gravity: -3, shards: 14, add: true, spin: 4 },
    ui: '#3a9fff',
  },
];

export function getSkin(id: string | undefined | null): SkinDef {
  return SKINS.find(s => s.id === id) ?? SKINS[0];
}

/** valid-looking skin id (unknown ids are kept in the save so newer saves round-trip, but render as classic) */
export const isSkinId = (v: unknown): v is string => typeof v === 'string' && /^[a-z0-9-]{1,32}$/.test(v);
