/* Shared site theme. Notebook cells and slide decks are not executed here. */
(() => {
  const key = 'girafe-course-theme';
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  const valid = value => ['light', 'dark', 'system'].includes(value);
  let preference = 'system';
  try { const saved = localStorage.getItem(key); if (valid(saved)) preference = saved; } catch {}
  const apply = () => {
    document.documentElement.dataset.theme = preference === 'system'
      ? (media.matches ? 'dark' : 'light') : preference;
  };
  apply();
  media.addEventListener('change', apply);
  document.addEventListener('DOMContentLoaded', () => {
    const select = document.querySelector('#theme-choice');
    if (!select) return;
    select.value = preference;
    select.addEventListener('change', () => {
      preference = select.value;
      try { localStorage.setItem(key, preference); } catch {}
      apply();
    });
    window.addEventListener('storage', event => {
      if (event.key !== key) return;
      preference = valid(event.newValue) ? event.newValue : 'system';
      select.value = preference;
      apply();
    });
  });
})();
