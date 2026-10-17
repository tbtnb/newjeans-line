import type { LevelRecord, Preferences, SaveData } from './types';

const KEY = 'newjeans-line.save.v1';
export const defaultSettings: Preferences = { volume: 0.75, offsetMs: 0, quality: 'high', vibration: true, guide: true };
export const emptyRecord = (): LevelRecord => ({ best: 0, diamonds: 0, crowns: 0, attempts: 0, completed: false });
const object = (value: unknown): value is Record<string, unknown> => !!value && typeof value === 'object' && !Array.isArray(value);
const finite = (value: unknown, min: number, max: number) => typeof value === 'number' && Number.isFinite(value) && value >= min && value <= max;

/** Imports are deliberately strict: a corrupt file must never silently erase progress. */
export function validateSave(value: unknown, ids: string[]): SaveData {
  if (!object(value) || value.version !== 1 || typeof value.selected !== 'string' || !ids.includes(value.selected)) throw new Error('这不是有效的 NewJeans Line 存档，或歌曲版本不匹配。');
  const prefs = value.settings;
  if (!object(prefs) || !finite(prefs.volume, 0, 1) || !finite(prefs.offsetMs, -500, 500) || !['high', 'low'].includes(prefs.quality as string) || typeof prefs.vibration !== 'boolean' || typeof prefs.guide !== 'boolean') throw new Error('存档中的设置不完整或超出范围。');
  if (!object(value.records)) throw new Error('存档中的游戏记录无效。');
  const records: Record<string, LevelRecord> = {};
  for (const [id, entry] of Object.entries(value.records)) {
    if (!ids.includes(id) || !object(entry) || !finite(entry.best, 0, 1) || !finite(entry.diamonds, 0, 10) || !Number.isInteger(entry.diamonds) || !finite(entry.crowns, 0, 3) || !Number.isInteger(entry.crowns) || !finite(entry.attempts, 0, 1e9) || !Number.isInteger(entry.attempts) || typeof entry.completed !== 'boolean') throw new Error('存档包含无法识别的歌曲或记录。');
    const best = entry.best as number;
    const availableCrowns = Number(best + 1e-7 >= 0.3) + Number(best + 1e-7 >= 0.6) + Number(best + 1e-7 >= 1);
    if (entry.completed !== (best === 1) || (entry.crowns as number) > availableCrowns || (entry.diamonds as number) > Math.floor(best * 10 + 1e-6)) throw new Error('存档中的成绩与收集记录不一致。');
    records[id] = { best: entry.best as number, diamonds: entry.diamonds as number, crowns: entry.crowns as number, attempts: entry.attempts as number, completed: entry.completed as boolean };
  }
  return { version: 1, selected: value.selected, records, settings: { volume: prefs.volume as number, offsetMs: prefs.offsetMs as number, quality: prefs.quality as Preferences['quality'], vibration: prefs.vibration, guide: prefs.guide } };
}

export function loadSave(ids: string[], initial: string): SaveData {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return validateSave(JSON.parse(raw), ids);
  } catch { /* Private mode and an obsolete or corrupt save use safe defaults. */ }
  return { version: 1, selected: initial, records: {}, settings: { ...defaultSettings } };
}

export function persistSave(save: SaveData): boolean {
  try { localStorage.setItem(KEY, JSON.stringify(save)); return true; } catch { return false; }
}
