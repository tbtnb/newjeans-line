export type Theme = 'meadow'|'sky'|'city'|'moon'|'dream'|'temple'|'candy'|'ocean'|'neon'|'sunset';
export interface Level { id:string; title:string; artist:string; album:string; duration:number; bpm:number; offset:number; difficulty:1|2|3|4|5; theme:Theme; accent:string; audio:string; turns:number[]; sections:{at:number;label:string}[]; instrumental:boolean; }
export interface Point { x:number; z:number; }
export interface PathPoint extends Point { time:number; }
export type GameStatus = 'ready'|'playing'|'paused'|'failed'|'complete';
export interface GameSnapshot { status:GameStatus; time:number; progress:number; position:Point; direction:0|1; turnsHit:number; nextTurn:number|null; combo:number; diamonds:number; crowns:number; accuracy:number; lastRating:'perfect'|'good'|'miss'|null; failureReason:string|null; trail:Point[]; }
export interface GameOptions { practice?:boolean; offsetMs?:number; }
export interface LevelRecord { best:number; diamonds:number; crowns:number; attempts:number; completed:boolean; }
export interface Preferences { volume:number; offsetMs:number; quality:'high'|'low'; vibration:boolean; guide:boolean; }
export interface SaveData { version:1; selected:string; records:Record<string,LevelRecord>; settings:Preferences; }
