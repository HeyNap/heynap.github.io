// The footer's language picker (written into every page by
// tools/build-locales.py): closes on a click elsewhere or Escape.
(() => {
  const picker = document.querySelector('details.lang');
  if (!picker) return;
  document.addEventListener('click', e => { if (!picker.contains(e.target)) picker.open = false; });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && picker.open) { picker.open = false; picker.querySelector('summary').focus(); } });
})();
