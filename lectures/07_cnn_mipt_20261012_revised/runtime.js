/* Native Reveal.js presentation with the approved local teaching animation. */
window.deckData = slides;
document.querySelectorAll('.math').forEach(element => katex.render(decodeURIComponent(element.dataset.tex), element, {displayMode: element.dataset.display === '1', throwOnError: true, strict: 'warn'}));
// Retain links saved before the Reveal migration; new links use Reveal's format.
if (/^#[^/]/.test(location.hash) && document.getElementById(location.hash.slice(1))) {
  history.replaceState(null, '', location.pathname + location.search + '#/' + location.hash.slice(1));
}
let motionTimer = null;
function pauseMotion() {
  if (motionTimer !== null) clearInterval(motionTimer);
  motionTimer = null;
  document.querySelectorAll('[data-motion-play]').forEach(button => { button.textContent = '▶ Пуск'; button.setAttribute('aria-pressed', 'false'); });
}

function motionPanel() { return Reveal.getCurrentSlide()?.querySelector('[data-motion]'); }

function renderMotion(panel, count) {
  const size = Number(panel.dataset.out);
  const total = size * size;
  count = Math.max(0, Math.min(total, count));
  panel.dataset.step = String(count);
  const index = Math.max(0, count - 1);
  const row = Math.floor(index / size);
  const col = index % size;
  const cell = Number(panel.dataset.cell);
  panel.querySelector('.scan-window').style.transform = `translate(${col * Number(panel.dataset.stride) * cell}px, ${row * Number(panel.dataset.stride) * cell}px)`;
  panel.querySelectorAll('.motion-output span').forEach((element, i) => { element.classList.toggle('revealed', i < count); element.classList.toggle('current', count > 0 && i === index); });
  const controls = panel.nextElementSibling;
  controls.querySelector('[data-motion-scrub]').value = String(count);
  controls.querySelector('[data-motion-count]').textContent = `${count}/${total}`;
  const label = count === 0 ? 'Выберите шаг или запустите анимацию.' : panel.dataset.motion === 'pool' ? `Максимум окна → ячейка (${row + 1}, ${col + 1})` : panel.dataset.motion === 'stride' ? `Позиция окна: (${row * Number(panel.dataset.stride)}, ${col * Number(panel.dataset.stride)})` : `Центр окна → ячейка (${row + 1}, ${col + 1})`;
  controls.nextElementSibling.textContent = label;
}

function advanceMotion() {
  const panel = motionPanel();
  if (!panel) return;
  const total = Number(panel.dataset.out) ** 2;
  renderMotion(panel, (Number(panel.dataset.step || 0) % total) + 1);
}

function toggleMotion() {
  const panel = motionPanel();
  if (!panel) return;
  if (motionTimer !== null) { pauseMotion(); return; }
  advanceMotion();
  motionTimer = setInterval(advanceMotion, 950);
  const button = Reveal.getCurrentSlide().querySelector('[data-motion-play]');
  button.textContent = 'Ⅱ Пауза';
  button.setAttribute('aria-pressed', 'true');
}



document.querySelectorAll('[data-motion-play]').forEach(button => button.addEventListener('click', toggleMotion));
document.querySelectorAll('[data-motion-step]').forEach(button => button.addEventListener('click', () => { pauseMotion(); advanceMotion(); }));
document.querySelectorAll('[data-motion-scrub]').forEach(input => input.addEventListener('input', () => { pauseMotion(); renderMotion(input.closest('.motion-controls').previousElementSibling, Number(input.value)); }));
Reveal.on('slidechanged', () => { pauseMotion(); });
Reveal.on('overviewshown', pauseMotion);
Reveal.on('paused', pauseMotion);
document.addEventListener('visibilitychange', () => { if (document.hidden) pauseMotion(); });
Reveal.initialize({
  width:1600, height:900, margin:0, minScale:0.1, maxScale:2,
  center:false, transition:'none', backgroundTransition:'none',
  hash:true, history:true, controls:true, progress:true,
  scrollActivationWidth:null,
  pdfMaxPagesPerSlide:1, pdfSeparateFragments:false, pdfPageHeightOffset:0,
  keyboardCondition:event => {
    if (!(event.target instanceof Element)) return true;
    if (event.target.closest('input,textarea,select,[contenteditable]')) return false;
    // Preserve native button/link activation without disabling presenter shortcuts after clicks.
    return !(event.target.closest('a,button') && ['Enter',' '].includes(event.key));
  },
  plugins:[]
}).then(() => {
  Reveal.addKeyBinding({keyCode:13,key:'ENTER',description:'Play / pause convolution animation'}, toggleMotion);
});
