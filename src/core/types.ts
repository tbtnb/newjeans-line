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
export interface CameraCue { t: number; preset?: string; yaw?: number; worldYaw?: number; pitch?: number; dist?: number; fov?: number; blend?: number; shake?: number; roll?: number; lead?: number; }
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
  objects?: SceneObject[];
  events?: SceneEvent[];
  diamonds: { t: number; side?: number }[];
  crowns: { t: number }[];
  finish?: { kind: string; parts?: Part[]; color?: string };
  collectibleColors?: { diamond?: string; crown?: string };
  /** Roadside set-dressing (engine-placed props along both sides of every road segment). false disables it. */
  dressing?: Dressing | false;
  beats?: number[]; // optional beat grid for react:'beat' scenery
  kicks?: number[];
}
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
}
export interface LevelData {
  id: string; title: string; album: string; duration: number; bpm: number; audio: string; cover: string;
  difficulty: number; accent: string; chart: Chart; layout: Layout;
}
