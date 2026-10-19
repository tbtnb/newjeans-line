/** Line-skin picker: sheet with an animated 3D preview of the line and a card grid. Persists save.settings.skin. */
import { SKINS, getSkin } from './skins';
import { SkinPreview } from './render/skinpreview';

interface Deps { getSkin(): string; setSkin(id: string): void; lineColor(): string; }
const $ = (id: string) => document.getElementById(id) as HTMLElement;

export function initSkinUI(d: Deps) {
  const sheet = $('skins'), grid = $('skin-grid');
  const preview = new SkinPreview($('skin-canvas') as HTMLCanvasElement);
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
