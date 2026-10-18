/** Line-skin picker: sheet with an animated 2D preview of the line and a card grid. Persists save.settings.skin. */
import { SKINS, getSkin, type SkinDef } from './skins';

interface Deps { getSkin(): string; setSkin(id: string): void; lineColor(): string; }
const $ = (id: string) => document.getElementById(id) as HTMLElement;

const imgCache = new Map<string, HTMLImageElement>();
function img(src: string) {
  let i = imgCache.get(src);
  if (!i) { i = new Image(); i.decoding = 'async'; i.src = './' + src; imgCache.set(src, i); }
  return i;
}
const ready = (i: HTMLImageElement | undefined): i is HTMLImageElement => !!i && i.complete && i.naturalWidth > 0;

function tinted(src: string, color: string) {
  const key = src + color; const c = tintCache.get(key); if (c) return c;
  const base = img(src); if (!ready(base)) return null;
  const cv = document.createElement('canvas'); cv.width = cv.height = 64; const x = cv.getContext('2d')!;
  x.drawImage(base, 0, 0, 64, 64); x.globalCompositeOperation = 'multiply'; x.fillStyle = color; x.fillRect(0, 0, 64, 64);
  x.globalCompositeOperation = 'destination-in'; x.drawImage(base, 0, 0, 64, 64);
  tintCache.set(key, cv); return cv;
}
const tintCache = new Map<string, HTMLCanvasElement>();

function shade(hex: string, k: number) {
  const n = parseInt(hex.slice(1), 16); const f = (v: number) => Math.max(0, Math.min(255, Math.round(v * k)));
  return `rgb(${f(n >> 16)},${f((n >> 8) & 255)},${f(n & 255)})`;
}

/** Animated isometric preview: a Dancing-Line style zig-zag with square corners, textured trail, head and turn bursts. */
class Preview {
  private cv: HTMLCanvasElement; private ctx: CanvasRenderingContext2D;
  private skin: SkinDef = SKINS[0]; private color = '#ffffff';
  private raf = 0; private t0 = 0; private parts: { x: number; z: number; y: number; vx: number; vz: number; vy: number; t: number; c: number }[] = [];
  private lastSeg = -1;
  private readonly lens = [3, 2, 4, 1.5, 2.5, 3.5, 2, 1.5];
  constructor(cv: HTMLCanvasElement) { this.cv = cv; this.ctx = cv.getContext('2d')!; }
  set(skin: SkinDef, color: string) { this.skin = skin; this.color = color; this.parts.length = 0; for (const p of [skin.tex, skin.burst.sprite, skin.shatter.sprite]) if (p) img(p); }
  start() { if (!this.raf) { this.t0 = performance.now(); const f = () => { this.raf = requestAnimationFrame(f); this.draw(); }; this.raf = requestAnimationFrame(f); } }
  stop() { cancelAnimationFrame(this.raf); this.raf = 0; }
  /** path point at distance d (alternating +x / +z), plus segment index and heading */
  private at(d: number) {
    let x = 0, z = 0, i = 0, rem = d;
    for (;; i++) { const L = this.lens[i % this.lens.length]; if (rem <= L) break; rem -= L; if (i % 2 === 0) x += L; else z += L; }
    if (i % 2 === 0) x += rem; else z += rem;
    return { x, z, i };
  }
  private draw() {
    const cv = this.cv, dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = cv.clientWidth, h = cv.clientHeight; if (!w || !h) return;
    if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
    const x = this.ctx; x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
    const s = this.skin, now = (performance.now() - this.t0) / 1000, speed = 2.6;
    const D = now * speed; const head = this.at(D);
    const S = Math.min(w, h) / 7.5; const c30 = Math.cos(Math.PI / 6), s30 = 0.5;
    const cx = w / 2, cy = h * 0.58;
    const P = (px: number, pz: number, py = 0): [number, number] => [cx + ((px - head.x) - (pz - head.z)) * c30 * S, cy + ((px - head.x) + (pz - head.z)) * s30 * S - py * S];
    // runs behind the head (last ~16 units)
    const runs: { ax: number; az: number; bx: number; bz: number; hx: boolean }[] = [];
    let d0 = Math.max(0, D - 16); let p = this.at(d0);
    for (let guard = 0; guard < 20; guard++) {
      let segEnd = 0, i = p.i; for (let k = 0; k <= i; k++) segEnd += this.lens[k % this.lens.length];
      const e = Math.min(D, segEnd); const q = this.at(e - 1e-6);
      runs.push({ ax: p.x, az: p.z, bx: q.x, bz: q.z, hx: i % 2 === 0 });
      if (e >= D) break; d0 = e + 1e-6; p = this.at(d0);
    }
    if (head.i !== this.lastSeg) { if (this.lastSeg >= 0) this.burst(head.x, head.z); this.lastSeg = head.i; }
    const H = 0.9, half = 0.5;
    const tex = s.tex ? img(s.tex) : undefined; const pat = ready(tex) && !s.levelColor ? x.createPattern(tex, 'repeat') : null;
    const base = s.levelColor ? this.color : s.trail;
    // draw runs back to front (older first); each run is a box from a-half to b+half
    for (const r of runs) {
      const x0 = Math.min(r.ax, r.bx) - half, x1 = Math.max(r.ax, r.bx) + half, z0 = Math.min(r.az, r.bz) - half, z1 = Math.max(r.az, r.bz) + half;
      const t00 = P(x0, z0, H), t10 = P(x1, z0, H), t11 = P(x1, z1, H), t01 = P(x0, z1, H);
      const b10 = P(x1, z0, 0), b11 = P(x1, z1, 0), b01 = P(x0, z1, 0);
      // right face (+x) and front face (+z)
      x.fillStyle = shade(pat ? '#c8ccd4' : base, 0.72); x.beginPath(); x.moveTo(...t10); x.lineTo(...t11); x.lineTo(...b11); x.lineTo(...b10); x.closePath(); x.fill();
      x.fillStyle = shade(pat ? '#c8ccd4' : base, 0.86); x.beginPath(); x.moveTo(...t01); x.lineTo(...t11); x.lineTo(...b11); x.lineTo(...b01); x.closePath(); x.fill();
      if (pat) { x.save(); x.beginPath(); x.moveTo(...t10); x.lineTo(...t11); x.lineTo(...b11); x.lineTo(...b10); x.closePath(); x.moveTo(...t01); x.lineTo(...t11); x.lineTo(...b11); x.lineTo(...b01); x.closePath(); x.clip(); x.globalAlpha = 0.55; x.fillStyle = pat; x.fill(); x.restore(); }
      // top face with the texture mapped u = across, v = along (affine map of the unit square)
      x.beginPath(); x.moveTo(...t00); x.lineTo(...t10); x.lineTo(...t11); x.lineTo(...t01); x.closePath();
      if (pat && ready(tex)) {
        x.save(); x.clip();
        const tl = s.texLen ?? 2; const len = r.hx ? x1 - x0 : z1 - z0;
        const o = P(x0, z0, H), ux = r.hx ? P(x0, z1, H) : P(x1, z0, H), vx = r.hx ? P(x1, z0, H) : P(x0, z1, H);
        const tw = tex.naturalWidth, th = tex.naturalHeight;
        x.transform((ux[0] - o[0]) / tw, (ux[1] - o[1]) / tw, (vx[0] - o[0]) / (th * len / tl), (vx[1] - o[1]) / (th * len / tl), o[0], o[1]);
        x.fillStyle = pat; x.fillRect(0, 0, tw, th * len / tl + 1);
        x.restore();
      } else { x.fillStyle = base; x.fill(); }
    }
    // head
    const ic = s.levelColor ? undefined : img(`skins/${s.id}/icon.png`);
    const [hx, hy] = P(head.x, head.z, H / 2);
    if (ready(ic)) { const sz = S * 2.3; x.drawImage(ic, hx - sz / 2, hy - sz * 0.62, sz, sz); }
    else {
      const t0 = P(head.x - half, head.z - half, H), t1 = P(head.x + half, head.z - half, H), t2 = P(head.x + half, head.z + half, H), t3 = P(head.x - half, head.z + half, H);
      const b1 = P(head.x + half, head.z - half, 0), b2 = P(head.x + half, head.z + half, 0), b3 = P(head.x - half, head.z + half, 0);
      x.fillStyle = shade(base, 0.72); x.beginPath(); x.moveTo(...t1); x.lineTo(...t2); x.lineTo(...b2); x.lineTo(...b1); x.fill();
      x.fillStyle = shade(base, 0.86); x.beginPath(); x.moveTo(...t3); x.lineTo(...t2); x.lineTo(...b2); x.lineTo(...b3); x.fill();
      x.fillStyle = shade(base, 1.08); x.beginPath(); x.moveTo(...t0); x.lineTo(...t1); x.lineTo(...t2); x.lineTo(...t3); x.fill();
    }
    // particles
    const dt = 1 / 60; const spr = s.burst.sprite;
    for (let i = this.parts.length - 1; i >= 0; i--) {
      const q = this.parts[i]; q.t += dt; const life = s.burst.life[1] * 1.6; if (q.t > life) { this.parts.splice(i, 1); continue; }
      q.vy += s.burst.gravity * 0.4 * dt; q.x += q.vx * dt; q.z += q.vz * dt; q.y += q.vy * dt;
      const [px, py] = P(q.x, q.z, q.y); const a = 1 - q.t / life; const sz = S * (s.burst.size[0] + s.burst.size[1]) * 1.4;
      const col = s.burst.colors[q.c]; const tc = spr ? tinted(spr, col) : null;
      x.globalAlpha = a;
      if (tc) x.drawImage(tc, px - sz / 2, py - sz / 2, sz, sz); else { x.fillStyle = s.levelColor ? '#ffffff' : col; x.beginPath(); x.arc(px, py, sz * 0.25, 0, Math.PI * 2); x.fill(); }
      x.globalAlpha = 1;
    }
  }
  private burst(px: number, pz: number) {
    const n = this.skin.levelColor ? 6 : Math.min(12, this.skin.burst.count);
    for (let i = 0; i < n; i++) { const a = Math.random() * Math.PI * 2, v = 0.6 + Math.random() * 1.2; this.parts.push({ x: px, z: pz, y: 0.9, vx: Math.cos(a) * v, vz: Math.sin(a) * v, vy: 1 + Math.random() * 1.5, t: 0, c: i % 2 }); }
  }
}

export function initSkinUI(d: Deps) {
  const sheet = $('skins'), grid = $('skin-grid');
  const preview = new Preview($('skin-canvas') as HTMLCanvasElement);
  const render = () => {
    const cur = getSkin(d.getSkin()).id;
    grid.innerHTML = SKINS.map(s => `<li><button class="skin-card${s.id === cur ? ' on' : ''}" data-id="${s.id}" aria-pressed="${s.id === cur}" style="--skin:${s.ui}">
      <span class="skin-ico">${s.levelColor ? '<i class="classic-cube"></i>' : `<img src="./skins/${s.id}/icon.png" alt="" loading="lazy"/>`}</span>
      <span class="skin-txt"><b>${s.name}</b><small>${s.nameEn}</small></span></button></li>`).join('');
    const s = getSkin(cur);
    $('skin-name').textContent = `${s.name} · ${s.nameEn}`; $('skin-desc').textContent = s.desc;
    sheet.style.setProperty('--skin', s.ui);
    preview.set(s, d.lineColor());
    const sn = document.getElementById('set-skin-name'); if (sn) sn.textContent = s.name;
  };
  grid.addEventListener('click', e => {
    const b = (e.target as HTMLElement).closest('button.skin-card') as HTMLElement | null; if (!b) return;
    d.setSkin(b.dataset.id!); render();
  });
  const open = () => { render(); sheet.classList.add('on'); preview.start(); };
  const close = () => { sheet.classList.remove('on'); preview.stop(); };
  $('btn-skins').onclick = open;
  const os = document.getElementById('btn-open-skins'); if (os) os.onclick = () => { document.getElementById('settings')?.classList.remove('on'); open(); };
  $('btn-close-skins').onclick = close;
  render();
  return { open, close, refresh: render };
}
