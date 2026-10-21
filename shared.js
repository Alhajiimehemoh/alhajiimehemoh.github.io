/* shared.js - v9 - menu, theme, contact form fallback. No scroll or tilt effects. */

/* Apply saved theme before first paint */
(function () {
  try {
    var saved = localStorage.getItem('theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
  } catch (e) { /* storage blocked: follow system theme */ }
})();

function isDarkNow() {
  var t = document.documentElement.getAttribute('data-theme');
  if (t) return t === 'dark';
  return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
}

function syncThemeButton() {
  var btn = document.getElementById('themeBtn');
  if (!btn) return;
  var dark = isDarkNow();
  btn.textContent = dark ? '☀' : '☾';
  btn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
}

document.addEventListener('DOMContentLoaded', function () {
  syncThemeButton();

  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = isDarkNow() ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      syncThemeButton();
    });
  }

  /* Mobile menu */
  var btn = document.getElementById('menuBtn');
  var nav = document.getElementById('mobileNav');
  function setMenu(open) {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (btn && nav) {
    btn.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); btn.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('open') && !nav.contains(e.target) && !btn.contains(e.target)) setMenu(false);
    });
  }

  /* Contact form: until a real Formspree ID replaces "xxxxabcd" in the form action,
     send the message through WhatsApp so no enquiry is lost. */
  var form = document.querySelector('form[action*="xxxxabcd"]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form);
      var text = 'Hello Alhaji, I am ' + (f.get('name') || '') + ' (' + (f.get('email') || '') + '). ' + (f.get('message') || '');
      window.open('https://wa.me/23279301430?text=' + encodeURIComponent(text), '_blank', 'noopener');
      var status = document.getElementById('formStatus');
      if (status) status.textContent = 'Opening WhatsApp with your message. Press send there to deliver it.';
    });
  }
});
