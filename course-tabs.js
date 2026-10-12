(() => {
  const tabs = [...document.querySelectorAll('.course-tabs [role="tab"]')];
  const select = (id, focus = false) => {
    tabs.forEach(tab => {
      const selected = tab.id === `tab-${id}`;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !selected;
      if (selected && focus) tab.focus();
    });
  };
  const fromHash = () => {
    if (location.hash === '#msu' || location.hash.startsWith('#msu-')) return 'msu';
    if (location.hash === '#mipt' || location.hash.startsWith('#lecture-') || location.hash.startsWith('#homework-')) return 'mipt';
    return document.querySelector('.course-tabs [aria-selected="true"]')?.id.slice(4) || 'mipt';
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab.id.slice(4)));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (i + 1) % tabs.length;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (i + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        location.hash = tabs[next].getAttribute('href');
        select(tabs[next].id.slice(4), true);
      }
    });
  });
  window.addEventListener('hashchange', () => select(fromHash()));
  select(fromHash());
})();
