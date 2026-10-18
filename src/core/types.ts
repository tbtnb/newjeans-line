export type Heading = 0 | 1 | 2 | 3; // 0=N(+z) 1=E(+x) 2=S(-z) 3=W(-x)
export type Dir = 'L' | 'R';
export interface Vec3 { x: number; y: number; z: number; }

export interface ChartTap { t: number; dir?: Dir; tag?: string; }
export interface Section { t: number; label: string; kind: string; }
export interface Chart {
  id: string;
  startHeading?: 'N' | 'E' | 'S' | 'W';
  speed?: { t: number; v: number }[];
  taps: ChartTap[];
  sections: Section[];
  notes?: string;
}

export interface Palette {
  skyTop: string; skyBottom: string; fog: string; fogStart: number; fogEnd: number;
  ground: string; groundY: number | null; road: string; roadSide: string; line: string;
  light: string; lightIntensity: number; ambient: string; particles: string | null;
}

export interface ObjectAnim { t: number; mode: string; dur?: number; }
export interface Part { kind: string; uv?: number[]; glow?: number; pos?: number[]; size?: number[]; rot?: number[]; color?: string; color2?: string; texture?: string; src?: string; mode?: string; alpha?: boolean; }
export interface SceneObject {
  /** v2.8: include this object in the fx glow layer (layout.fx.glow) */
  glowfx?: boolean;
  id?: string; t?: number; side?: number; along?: number; y?: number; kind: string;
  size?: number[]; rot?: number | number[]; color?: string; color2?: string; parts?: Part[];
  appear?: ObjectAnim; exit?: ObjectAnim; react?: 'none' | 'beat' | 'tap' | 'kick';
  landmark?: boolean; egg?: boolean; name?: string;
  /** absolute world position [x,y,z] (overrides t/side anchoring); rot is then an absolute yaw in degrees */
  worldPos?: number[];
  /** part of / under the road (bridges, decks): never pushed off the road */
  onroad?: boolean;
  /** internal: row item anchored to the actual road edge rather than the mean corridor */
  hug?: boolean;
  radius?: number;
  /** kind 'image': texture path relative to the level folder (art/x.png); mode upright|flat|billboard */
  src?: string; mode?: string; alpha?: boolean; texture?: string;
  /** art props (v2.7): kind standee | facade | decal | image. uv = sub-rectangle [u0,v0,u1,v1] of src (0..1, top-left origin);
   *  glow = emissive amount of the art (default 0.25-0.4) */
  uv?: number[]; glow?: number;
  /** v2.7 orientation of the object's front (local -z): road = toward the road point at t; oncoming = toward the approaching
   *  line/camera (against the travel direction, turned 30 deg toward the road); camera = yaw-billboard every frame; travel = along travel */
  face?: 'road' | 'oncoming' | 'camera' | 'travel';
  /** v2.7 near-road placement: |side| = road half-width at t + near + the object's radius (sign of side picks the side, default right) */
  near?: number;
  // row
  t0?: number; t1?: number; spacing?: number; bothSides?: boolean; item?: SceneObject;
}
/** Camera cue. preset resets framing; the rest modify it from t (blended over `blend` s).
 *  Modifiers hold until the next cue: zoom (× distance), tilt (+° pitch), sway (+° yaw); orbit: slow yaw drift deg/s (±35° max);
 *  punch: push-in amount on kicks (0..0.1, default 0.025). layout.autoCamera=false disables label-driven defaults. */
export interface CameraCue { t: number; preset?: string; yaw?: number; worldYaw?: number; pitch?: number; dist?: number; fov?: number; blend?: number; shake?: number; roll?: number; lead?: number; zoom?: number; tilt?: number; sway?: number; orbit?: number; punch?: number; }
export interface SceneEvent { t: number; type: string; target?: string; every?: number; until?: number; palette?: Partial<Palette>; dur?: number; at?: string; particles?: string; amount?: number; [k: string]: unknown; }
export interface Elevation { type: 'fall' | 'jump' | 'ramp'; t?: number; t0?: number; t1?: number; dy: number; }
export interface Layout {
  id: string; title?: string;
  palette: Palette;
  road: { width: { t: number; w: number }[]; height?: number; reveal: { t: number; mode: string; lead: number }[] };
  elevation?: Elevation[];
  sections?: { t: number; label?: string; palette?: Partial<Palette>; camera?: string; note?: string; backdrop?: string; ground?: { src: string; scale?: number; tint?: string } }[];
  art?: { backdrop?: string; ground?: { src: string; scale?: number; tint?: string }; road?: { src: string } };
  camera?: CameraCue[];
  autoCamera?: boolean;
  objects?: SceneObject[];
  events?: SceneEvent[];
  diamonds: { t: number; side?: number }[];
  crowns: { t: number }[];
  finish?: { kind: string; parts?: Part[]; color?: string };
  /** Level end before the song ends (s): the route, finish gate, progress and completion use it; the music fades out over
   *  endFade seconds (default 1.5) and stops exactly there. Absent = the level lasts the whole audio file. */
  endTime?: number;
  endFade?: number;
  collectibleColors?: { diamond?: string; crown?: string };
  /** Roadside set-dressing (engine-placed props along both sides of every road segment). false disables it. */
  dressing?: Dressing | false;
  /** v2.8 show visuals (glow, image processing, beams, sparkles, road gloss/trims); see docs/SHOW_FX.md. Off when absent. */
  fx?: FxSpec;
  /** v2.9 corridor scenery (src/render/corridor.ts) */
  corridor?: CorridorSpec;
  beats?: number[]; // optional beat grid for react:'beat' scenery
  kicks?: number[];
  /** concept C scene (src/render/scenec): zone-driven, chunk-streamed low-poly papercraft scenery (replaces objects/dressing/fx/corridor) */
  scenec?: SceneCSpec;
}
/** Concept C placement spec (levels-src/<id>/scene-c.json, generated by tools/omgc/make_spec.py). All placement is by route
 *  time t + side, so it survives re-charts. */
export interface SceneCAsset { layer: 'ground' | 'mid' | 'land' | 'sky' | 'anim'; shape: string; h: number; /** design footprint (m) when a sheet exists */ w?: number; d?: number; design?: string; tris: number; /** true = public/models/omg-c/<asset id>.glb, string = glb id shared with another asset */ model?: boolean | string; tint?: number; names?: string[] }
export interface SceneCLayer { asset: string; layer: SceneCAsset['layer']; count: number; near: [number, number] | number[]; y: number[]; scale: number[]; colors?: number[] }
export interface SceneCSet { t: number; side: number; asset: string; dist: number; scale?: number; pop?: string; label?: string }
export interface SceneCZone { id: string; key?: string; t0: number; t1: number; name?: string; colors: string[]; palette: Partial<Palette> & { shade?: string }; layers: SceneCLayer[]; setpieces: SceneCSet[]; moments?: { t: number; label: string }[] }
export interface SceneCSpec { version: number; chunk: number; /** paper page margin around each chunk's route bbox (m, default 28) */ pagePad?: number; window: { behind: number; ahead: number }; clear?: { ground?: number; groundMaxH?: number; near?: number }; assets: Record<string, SceneCAsset>; zones: SceneCZone[] }
/** Roadside dressing (schema v2.6). Props are placed deterministically along both sides of every ground segment,
 *  never on the road footprint (any level) and never overlapping each other; they pop in ahead of the line on the beat,
 *  bounce on beats near the line and shrink away when they would cover the head or the road just ahead. */
export interface DressingProp { kind?: string; size?: number[]; color?: string; color2?: string; parts?: Part[]; weight?: number; scale?: [number, number]; scaleY?: [number, number];
  /** v2.7 art prop: textured template (one shared material per image; uv selects a sub-rectangle so one image acts as an atlas).
   *  as: facade (box, art wrapped on the sides) | card (upright standee card) | crate (art on all faces) | tile (flat floor decal) */
  src?: string; as?: 'facade' | 'card' | 'crate' | 'tile'; uv?: number[]; alpha?: boolean; glow?: number;
  /** orientation of art props: road (front faces the road, default for card/facade), oncoming, random */
  face?: 'road' | 'oncoming' | 'random'; }
export interface DressingSection { t: number; density?: number; near?: [number, number]; props?: number[]; off?: boolean; }
export interface Dressing {
  props?: DressingProp[];          // prop palette (default: blocks/trees/cubes coloured from palette road, roadSide, ambient, ground and line)
  density?: number;                // props per 10 road units per side (default 3.6)
  near?: [number, number];         // gap from the road edge, units (default [0.4, 4])
  sections?: DressingSection[];    // per-section overrides from time t
  lead?: number;                   // seconds ahead of the line at which props pop in (default 2.6)
  bounce?: number;                 // beat bounce amplitude near the line (default 0.12)
  seed?: number;
  /** v2.7 theme colours for the default (untextured) prop palette, e.g. sampled from the level art */
  colors?: string[];
  /** v2.7 art props mixed into the default palette (ignored when props is given; list them in props instead) */
  art?: DressingProp[];
  /** v2.7 fraction (0..0.95) of dressing placements drawn from `art` (default 0.5) */
  artShare?: number;
}
export interface LevelData {
  id: string; title: string; album: string; duration: number; bpm: number; audio: string; cover: string;
  difficulty: number; accent: string; chart: Chart; layout: Layout;
  /** full audio length when the level ends early (layout.endTime); duration is then the level length */
  audioDuration?: number; endFade?: number;
}

/** v2.9 corridor scenery: far-band set pieces, floor light strips, emblems, fireworks (src/render/corridor.ts). Times in s. */
export interface CorridorItem {
  /** texture (art/x.png, alpha); size [w, h] in m; glow = brightness (unlit); float = bob amplitude (m) */
  src: string; size: number[]; glow?: number; float?: number;
  /** lights: beat = pulse on every beat; chase = alternate instances light on alternate beats */
  lights?: 'beat' | 'chase' | 'none';
  /** flat = floor emblem lying on the ground (random yaw); add = additive blend (soft glow art); cut = alpha-test cutoff */
  flat?: boolean; add?: boolean; cut?: number; alpha?: number; rise?: boolean;
  /** lean toward the camera (0 = upright yaw billboard, 1 = full billboard) */
  tilt?: number;
}
export interface CorridorSpec {
  items: CorridorItem[];
  /** one placement every `every` s from t0 to t1 on both sides (sides 2) or alternating (1); near = [min, max] m beyond the road edge */
  bands?: { t0: number; t1: number; every: number; phase?: number; near: number[]; items: number[]; sides?: number; mirror?: boolean; y?: number[]; scale?: number[] }[];
  /** glowing floor dots in strips parallel to the corridor (offsets in m beyond the road edge), chasing forward on the beat */
  floor?: { t0: number; t1: number; every: number; offsets: number[]; color: string; size?: number; alpha?: number }[];
  fireworks?: { t: number; near?: number; height?: number; colors?: string[]; amount?: number }[];
  /** items are up `lead` s before the line reaches them and kept `tail` s after; maxActive caps instances per layer */
  lead?: number; tail?: number; maxActive?: number; tilt?: number;
}

/** v2.8 show visuals (src/render/showfx.ts). All times in seconds; all optional. */
export interface FxSpec {
  exposure?: number; contrast?: number;
  vignette?: { weight?: number; color?: string };
  glow?: { intensity?: number; kernel?: number };
  /** keyed grading: exposure / contrast / glow intensity from t on, blended over `blend` s */
  keys?: { t: number; exposure?: number; contrast?: number; glow?: number; blend?: number }[];
  /** beat-reactive exposure pulse from t to t1 */
  pulse?: { t: number; t1: number; amount?: number }[];
  /** exposure flash (+ star burst at the head unless sparkle:false) on drops */
  flashes?: { t: number; dur?: number; amount?: number; sparkle?: boolean }[];
  /** stage searchlight beams beside the road between t0 and t1, one every `every` s, alternating sides */
  beams?: { t0: number; t1: number; every?: number; colors?: string[]; height?: number; near?: number }[];
  /** twinkling glow sprites beside/above the road between t0 and t1 (density per second of route) */
  sparkles?: { t0: number; t1: number; density?: number; colors?: string[]; size?: number; spread?: number; height?: number }[];
  /** glossy road top and glowing edge trims (trim colour, emissive strength) */
  road?: { gloss?: number; trim?: string; trimGlow?: number; trimWidth?: number; topGlow?: number };
  /** caps (high quality; low halves beams and keeps 40 % of sparkles) */
  maxBeams?: number; maxSparkles?: number;
  /** sprite texture for sparkles and drop bursts (art/x.png); default: a soft radial dot */
  sprite?: string;
}
