/** Save data v2. Old v1 saves (key newjeans-line.save.v1) are migrated and the v1 key is kept untouched as a backup. */
export interface LevelRecord { best: number; diamonds: number; crowns: number; attempts: number; completed: boolean; perfect?: number; taps?: number; }
/** skin: line skin id (added after v2 shipped; missing in older saves = 'classic', the original look) */
export interface Settings { volume: number; offsetMs: number; quality: 'high' | 'low'; vibration: boolean; skin: string; }
export interface SaveData { version: 2; selected: string; records: Record<string, LevelRecord>; settings: Settings; migratedFrom?: number; legacy?: unknown; }

export const KEY_V2 = 'newjeans-line.save.v2';
export const KEY_V1 = 'newjeans-line.save.v1';
export const defaultSettings: Settings = { volume: 0.8, offsetMs: 0, quality: 'high', vibration: true, skin: 'classic' };
export const emptyRecord = (): LevelRecord => ({ best: 0, diamonds: 0, crowns: 0, attempts: 0, completed: false });

const isObj = (v: unknown): v is Record<string, any> => !!v && typeof v === 'object' && !Array.isArray(v);
const num = (v: unknown, lo: number, hi: number, d: number) => (typeof v === 'number' && Number.isFinite(v) ? Math.max(lo, Math.min(hi, v)) : d);

function normRecord(r: unknown): LevelRecord | null {
  if (!isObj(r)) return null;
  const best = num(r.best, 0, 1, 0);
  return {
    best, diamonds: Math.round(num(r.diamonds, 0, 10, 0)), crowns: Math.round(num(r.crowns, 0, 3, 0)),
    attempts: Math.round(num(r.attempts, 0, 1e9, 0)), completed: r.completed === true || best >= 1,
    ...(typeof r.perfect === 'number' ? { perfect: r.perfect } : {}), ...(typeof r.taps === 'number' ? { taps: r.taps } : {}),
  };
}

/** Accepts v2 or v1 objects. Throws on unrecognisable data so an import never silently wipes progress. */
export function parseSave(value: unknown, ids: string[], fallbackSelected: string): SaveData {
  if (!isObj(value) || (value.version !== 1 && value.version !== 2)) throw new Error('这不是有效的 NewJeans Line 存档。');
  if (!isObj(value.records)) throw new Error('存档中的游戏记录无效。');
  const records: Record<string, LevelRecord> = {};
  const unknown: Record<string, unknown> = {};
  for (const [id, r] of Object.entries(value.records)) {
    const n = normRecord(r);
    if (n && ids.includes(id)) records[id] = n; else unknown[id] = r;
  }
  const s = isObj(value.settings) ? value.settings : {};
  const settings: Settings = {
    volume: num(s.volume, 0, 1, defaultSettings.volume), offsetMs: num(s.offsetMs, -300, 300, 0),
    quality: s.quality === 'low' ? 'low' : 'high', vibration: s.vibration !== false,
    skin: typeof s.skin === 'string' && /^[a-z0-9-]{1,32}$/.test(s.skin) ? s.skin : defaultSettings.skin,
  };
  const out: SaveData = { version: 2, selected: ids.includes(value.selected) ? value.selected : fallbackSelected, records, settings };
  if (value.version === 1) out.migratedFrom = 1;
  else if (value.migratedFrom) out.migratedFrom = value.migratedFrom;
  // preserve anything we don't understand (e.g. future songs or legacy fields) instead of dropping it
  if (Object.keys(unknown).length) out.legacy = { records: unknown };
  else if (value.legacy) out.legacy = value.legacy;
  return out;
}

export function loadSave(ids: string[], initial: string, store: Pick<Storage, 'getItem'> = localStorage): SaveData {
  for (const key of [KEY_V2, KEY_V1]) {
    try { const raw = store.getItem(key); if (raw) return parseSave(JSON.parse(raw), ids, initial); } catch { /* try next */ }
  }
  return { version: 2, selected: initial, records: {}, settings: { ...defaultSettings } };
}

export function persistSave(save: SaveData, store: Pick<Storage, 'setItem'> = localStorage): boolean {
  try { store.setItem(KEY_V2, JSON.stringify(save)); return true; } catch { return false; }
}

export function mergeRecord(old: LevelRecord | undefined, run: { progress: number; diamonds: number; crowns: number; completed: boolean; perfect?: number; taps?: number }): LevelRecord {
  const r = old ? { ...old } : emptyRecord();
  r.attempts += 1;
  r.best = Math.max(r.best, run.progress);
  r.diamonds = Math.max(r.diamonds, run.diamonds);
  r.crowns = Math.max(r.crowns, run.crowns);
  r.completed = r.completed || run.completed;
  if (run.completed && run.perfect !== undefined) r.perfect = Math.max(r.perfect ?? 0, run.perfect);
  if (run.taps !== undefined) r.taps = run.taps;
  return r;
}
