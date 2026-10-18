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
export interface Part { kind: string; pos?: number[]; size?: number[]; rot?: number[]; color?: string; color2?: string; texture?: string; src?: string; mode?: string; alpha?: boolean; }
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
  sections?: { t: number; label?: string; palette?: Partial<Palette>; camera?: string; note?: string; backdrop?: string }[];
  art?: { backdrop?: string; ground?: { src: string; scale?: number }; road?: { src: string } };
  camera?: CameraCue[];
  autoCamera?: boolean;
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
export interface DressingProp { kind: string; size?: number[]; color?: string; color2?: string; parts?: Part[]; weight?: number; scale?: [number, number]; scaleY?: [number, number]; }
export interface DressingSection { t: number; density?: number; near?: [number, number]; props?: number[]; off?: boolean; }
export interface Dressing {
  props?: DressingProp[];          // prop palette (default: blocks/trees/cubes coloured from palette road, roadSide, ambient, ground and line)
  density?: number;                // props per 10 road units per side (default 3.6)
  near?: [number, number];         // gap from the road edge, units (default [0.4, 4])
  sections?: DressingSection[];    // per-section overrides from time t
  lead?: number;                   // seconds ahead of the line at which props pop in (default 2.6)
  bounce?: number;                 // beat bounce amplitude near the line (default 0.12)
  seed?: number;
}
export interface LevelData {
  id: string; title: string; album: string; duration: number; bpm: number; audio: string; cover: string;
  difficulty: number; accent: string; chart: Chart; layout: Layout;
}
