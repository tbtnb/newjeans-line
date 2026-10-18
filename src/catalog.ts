import type { LevelData } from './core/types';

export interface SongMeta { id: string; title: string; album: string; cover: string; accent: string; legacyTaps: number; }
const C = (a: string) => `./art/covers/${a}.jpg`;
/** Fixed order requested by the user. */
export const SONGS: SongMeta[] = [
  { id: 'attention', title: 'Attention', album: 'New Jeans', cover: C('new-jeans'), accent: '#5b8fd6', legacyTaps: 139 },
  { id: 'hype-boy', title: 'Hype Boy', album: 'New Jeans', cover: C('new-jeans'), accent: '#8a6fd8', legacyTaps: 140 },
  { id: 'cookie', title: 'Cookie', album: 'New Jeans', cover: C('new-jeans'), accent: '#d77a6a', legacyTaps: 357 },
  { id: 'hurt', title: 'Hurt', album: 'New Jeans', cover: C('new-jeans'), accent: '#8c86c4', legacyTaps: 64 },
  { id: 'omg', title: 'OMG', album: 'OMG', cover: C('omg'), accent: '#e08a5c', legacyTaps: 213 },
  { id: 'ditto', title: 'Ditto', album: 'OMG', cover: C('omg'), accent: '#6f8fb0', legacyTaps: 181 },
  { id: 'new-jeans', title: 'New Jeans', album: 'Get Up', cover: C('get-up'), accent: '#3fb79a', legacyTaps: 68 },
  { id: 'super-shy', title: 'Super Shy', album: 'Get Up', cover: C('get-up'), accent: '#4f8fe8', legacyTaps: 176 },
  { id: 'eta', title: 'ETA', album: 'Get Up', cover: C('get-up'), accent: '#f0a33c', legacyTaps: 232 },
  { id: 'cool-with-you', title: 'Cool With You', album: 'Get Up', cover: C('get-up'), accent: '#8f7fd6', legacyTaps: 107 },
  { id: 'get-up', title: 'Get Up', album: 'Get Up', cover: C('get-up'), accent: '#e08ab6', legacyTaps: 16 },
  { id: 'asap', title: 'ASAP', album: 'Get Up', cover: C('get-up'), accent: '#e86f96', legacyTaps: 83 },
  { id: 'how-sweet', title: 'How Sweet', album: 'How Sweet', cover: C('how-sweet'), accent: '#e8875a', legacyTaps: 133 },
  { id: 'bubble-gum', title: 'Bubble Gum', album: 'How Sweet', cover: C('how-sweet'), accent: '#35b3c0', legacyTaps: 132 },
  { id: 'supernatural', title: 'Supernatural', album: 'Supernatural', cover: C('supernatural'), accent: '#8a6fe0', legacyTaps: 162 },
  { id: 'right-now', title: 'Right Now', album: 'Supernatural', cover: C('supernatural'), accent: '#4fa6d6', legacyTaps: 216 },
];

const loaders = import.meta.glob<{ default: LevelData }>('./levels/*.json');
export function hasLevel(id: string) { return !!loaders[`./levels/${id}.json`]; }
export async function loadLevel(id: string): Promise<LevelData> {
  const l = loaders[`./levels/${id}.json`];
  if (!l) throw new Error(`关卡数据缺失：${id}`);
  return (await l()).default;
}
