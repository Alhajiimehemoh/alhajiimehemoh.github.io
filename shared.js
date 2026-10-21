/* shared.js - v11 - theme, menu, forms, filters, search, lightbox, copy, Krio, offline. */

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

  /* Forms: without a Formspree ID, send the message through WhatsApp so no enquiry is lost. */
  document.querySelectorAll('form[data-fallback="wa"]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form), parts = [];
      f.forEach(function (v, k) { if (v && k.charAt(0) !== '_') parts.push(k + ': ' + v); });
      var text = 'Hello Alhaji, a message from your website.\n' + parts.join('\n');
      window.open('https://wa.me/23279301430?text=' + encodeURIComponent(text), '_blank', 'noopener');
      var status = document.getElementById('formStatus');
      if (status) status.textContent = 'Opening WhatsApp with your message. Press send there to deliver it.';
    });
  });
  /* Real Formspree forms: send in the background and show a status */
  document.querySelectorAll('form[action*="formspree.io"]:not([data-fallback])').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = document.getElementById('formStatus');
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw 0; form.reset(); if (status) status.textContent = 'Thank you. Your message was sent and I will reply soon.'; })
        .catch(function () { if (status) status.textContent = 'Sorry, that did not send. Please use WhatsApp or email instead.'; });
    });
  });

  /* Preselect service from ?service= */
  var sel = document.getElementById('rq-service');
  if (sel) {
    var want = new URLSearchParams(location.search).get('service');
    if (want) Array.prototype.forEach.call(sel.options, function (o) { if (o.text.toLowerCase().indexOf(want.toLowerCase()) === 0) sel.value = o.value || o.text; });
  }

  /* Reading progress bar */
  var bar = document.getElementById('progress');
  if (bar) {
    var tick = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, window.scrollY / h * 100) : 0) + '%';
    };
    window.addEventListener('scroll', tick, { passive: true }); tick();
  }

  /* Copy buttons, print buttons */
  document.addEventListener('click', function (e) {
    var c = e.target.closest && e.target.closest('[data-copy]');
    if (c) {
      var val = c.getAttribute('data-copy'), old = c.textContent;
      var done = function () { c.textContent = 'Copied'; setTimeout(function () { c.textContent = old; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(val).then(done, done); else done();
    }
    if (e.target.closest && e.target.closest('[data-print]')) window.print();
  });

  /* Project filter */
  var pf = document.querySelectorAll('.filter[data-filter]');
  if (pf.length) {
    var items = document.querySelectorAll('[data-filter-target] [data-type]');
    var count = document.getElementById('filterCount');
    pf.forEach(function (b) {
      b.addEventListener('click', function () {
        var t = b.getAttribute('data-filter'), n = 0;
        pf.forEach(function (x) { var on = x === b; x.classList.toggle('is-active', on); x.setAttribute('aria-pressed', on); });
        items.forEach(function (it) {
          var show = t === 'all' || (' ' + it.getAttribute('data-type') + ' ').indexOf(' ' + t + ' ') > -1;
          it.hidden = !show; if (show) n++;
        });
        if (count) count.textContent = t === 'all' ? '' : n + ' project' + (n === 1 ? '' : 's') + ' shown';
      });
    });
  }

  /* Notes search and category filter */
  var q = document.getElementById('noteSearch');
  if (q) {
    var rows = document.querySelectorAll('#noteList [data-cat]'), cat = 'all';
    var cb = document.querySelectorAll('.filter[data-cat]');
    var run = function () {
      var term = q.value.trim().toLowerCase(), n = 0;
      rows.forEach(function (r) {
        var ok = (cat === 'all' || r.getAttribute('data-cat') === cat) && (!term || r.getAttribute('data-search').indexOf(term) > -1);
        r.hidden = !ok; if (ok) n++;
      });
      document.getElementById('noteEmpty').hidden = n > 0;
      document.getElementById('noteCount').textContent = n + ' note' + (n === 1 ? '' : 's');
    };
    q.addEventListener('input', run);
    cb.forEach(function (b) { b.addEventListener('click', function () {
      cat = b.getAttribute('data-cat');
      cb.forEach(function (x) { var on = x === b; x.classList.toggle('is-active', on); x.setAttribute('aria-pressed', on); });
      run();
    }); });
    run();
  }

  /* Screenshot lightbox */
  var shots = document.querySelectorAll('.shot-btn');
  if (shots.length && window.HTMLDialogElement) {
    var dlg = document.createElement('dialog'); dlg.className = 'lightbox';
    dlg.innerHTML = '<img alt=""><button class="btn" type="button">Close</button>';
    document.body.appendChild(dlg);
    var img = dlg.querySelector('img');
    shots.forEach(function (b) { b.addEventListener('click', function () {
      img.src = b.getAttribute('data-full'); img.alt = b.getAttribute('aria-label').replace('Enlarge: ', ''); dlg.showModal();
    }); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.tagName === 'BUTTON') dlg.close(); });
  }

  /* Krio toggle (only present when KRIO_ENABLED) */
  var lb = document.getElementById('langBtn');
  if (lb) {
    var orig = {};
    var apply = function (map) {
      document.querySelectorAll('[data-i18n]').forEach(function (el) {
        var k = el.getAttribute('data-i18n');
        if (!(k in orig)) orig[k] = el.innerHTML;
        if (map && map[k]) el.textContent = map[k]; else el.innerHTML = orig[k];
      });
      document.documentElement.lang = map ? 'kri' : 'en';
      lb.textContent = map ? 'EN' : 'KR';
      lb.setAttribute('aria-label', map ? 'Switch language to English' : 'Switch language to Krio');
    };
    var load = function (on) {
      if (!on) { apply(null); return; }
      fetch('lang/kri.json').then(function (r) { return r.json(); }).then(apply).catch(function () {});
    };
    var cur = false; try { cur = localStorage.getItem('lang') === 'kri'; } catch (e) {}
    if (cur) load(true);
    lb.addEventListener('click', function () {
      cur = !cur; try { localStorage.setItem('lang', cur ? 'kri' : 'en'); } catch (e) {}
      load(cur);
    });
  }
});

/* Offline support */
if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) {
  window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
}
