// The footer's language picker: one list for every page, so adding a language
// is one line here (plus its folder, hreflang tags and sitemap entries).
// The page names its own language in <details class="lang" data-lang="…">;
// the list replaces the fallback link the page carries.
(() => {
  const languages = [
    ['en-US', '/', 'English (US)'],
    ['ro', '/ro/', 'Română'],
  ];
  const picker = document.querySelector('details.lang');
  if (!picker) return;
  const here = picker.dataset.lang;
  const list = picker.querySelector('ul');
  list.replaceChildren(...languages.map(([code, path, name]) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = path; a.lang = code; a.hreflang = code; a.textContent = name;
    if (code === here) a.setAttribute('aria-current', 'page');
    li.append(a);
    return li;
  }));
  // Close on a click elsewhere or Escape.
  document.addEventListener('click', e => { if (!picker.contains(e.target)) picker.open = false; });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && picker.open) { picker.open = false; picker.querySelector('summary').focus(); } });
})();
