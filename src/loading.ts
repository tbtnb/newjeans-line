/** Weighted, completed-work progress. Never advances by elapsed time. */
export type LoadStage = 'audio' | 'models' | 'road' | 'render';
const weights: Record<LoadStage, number> = { audio: 40, models: 30, road: 25, render: 5 };
export class LoadingProgress {
  private values: Record<LoadStage, number> = { audio: 0, models: 0, road: 0, render: 0 };
  constructor(private emit: (percent: number, detail: string) => void) {}
  update(stage: LoadStage, fraction: number, detail: string) {
    if (Number.isFinite(fraction) && fraction >= 0) this.values[stage] = Math.max(this.values[stage], Math.min(1, fraction));
    const sum = (Object.keys(weights) as LoadStage[]).reduce((n, k) => n + weights[k] * this.values[k], 0);
    const complete = Object.values(this.values).every(f => f === 1);
    this.emit(complete ? 100 : Math.min(99, Math.floor(sum)), detail);
  }
}
