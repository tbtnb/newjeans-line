/**
 * Page-turn transition between concept C zones: a DOM overlay (no draw calls) — a curled paper edge with a soft shadow
 * sweeps right-to-left across the screen in ~0.9 s at each zone start. The sheet itself stays translucent through the
 * middle third of the screen so the road and the head never disappear.
 */
export class PageTurn {
  private el: HTMLDivElement | null = null; private times: { t: number; color: string }[];
  constructor(host: HTMLElement | null, times: { t: number; color: string }[], private dur = 0.9) {
    this.times = times;
    if (!host || typeof document === 'undefined') return;
    const el = document.createElement('div'); el.className = 'nj-pageturn';
    Object.assign(el.style, { position: 'absolute', inset: '0', pointerEvents: 'none', overflow: 'hidden', display: 'none', zIndex: '2' });
    el.innerHTML = '<div class="pt-sheet" style="position:absolute;top:-10%;bottom:-10%;width:60%;transform-origin:left center;"></div>';
    host.appendChild(el); this.el = el;
  }
  update(t: number) {
    if (!this.el) return;
    let cur: { t: number; color: string } | null = null; for (const x of this.times) if (t >= x.t && t < x.t + this.dur) cur = x;
    if (!cur) { if (this.el.style.display !== 'none') this.el.style.display = 'none'; return; }
    const k = (t - cur.t) / this.dur, e = k * k * (3 - 2 * k);
    const sheet = this.el.firstElementChild as HTMLDivElement;
    this.el.style.display = 'block';
    // sheet left edge sweeps from 100% to -60%; leading curl = bright edge + shadow band, body fades to ~25% opacity
    sheet.style.left = `${100 - e * 160}%`;
    sheet.style.transform = `skewX(${-8 + 8 * e}deg)`;
    sheet.style.background = `linear-gradient(90deg, rgba(0,0,0,0.18) 0%, ${cur.color} 2.5%, #fffdf6 6%, ${cur.color}cc 12%, ${cur.color}40 40%, ${cur.color}00 100%)`;
    sheet.style.opacity = String(Math.sin(Math.PI * k) * 0.95);
  }
  dispose() { this.el?.remove(); this.el = null; }
}
