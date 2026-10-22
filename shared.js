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
      var apply = function () {
        document.documentElement.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (e) {}
        syncThemeButton();
      };
      var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (!document.startViewTransition || still) { apply(); return; }
      var r = themeBtn.getBoundingClientRect(), root = document.documentElement;
      var x = r.left + r.width / 2, y = r.top + r.height / 2;
      root.style.setProperty('--cx', x + 'px'); root.style.setProperty('--cy', y + 'px');
      root.style.setProperty('--cr', Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y)) + 'px');
      root.classList.add('theme-anim');
      var vt = document.startViewTransition(apply);
      vt.finished.finally(function () { root.classList.remove('theme-anim'); });
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
        if (count) { var noun = count.getAttribute('data-noun') || 'project'; count.textContent = t === 'all' ? '' : n + ' ' + noun + (n === 1 ? '' : 's') + ' shown'; }
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

/* v13 motion: header state, WhatsApp button visibility, scroll reveals */
document.addEventListener('DOMContentLoaded', function () {
  var root = document.documentElement, body = document.body;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var hero = document.querySelector('.hero');
  var onScroll = function () {
    var y = window.scrollY;
    body.classList.toggle('is-scrolled', y > 8);
    body.classList.toggle('at-top', !!hero && y < 360);
  };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  if (still || !('IntersectionObserver' in window)) return;
  var sel = '.section-head, .svc-card, .aud li, .sp-card, .gl, .more-card, .rn, .nfig, .callout, .ntable, .takeaways, .rel-card, .mini-dash, .proj-card, .note-card, .res-card, .tile, .reg-row, .steps li, .quote, .promo, .cta-band .wrap, .timeline li, .package, .plain, .faq, .facts, .note-card, .card, .kpi, .demo-card, .shot, .wide-photo, .about-grid > *';
  var els = document.querySelectorAll(sel);
  if (!els.length) return;
  root.classList.add('reveal-on');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting || en.boundingClientRect.top < 0) { en.target.classList.add('is-in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  var sweep = function () {
    document.querySelectorAll('.rv:not(.is-in)').forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight) { el.classList.add('is-in'); io.unobserve(el); }
    });
  };
  window.addEventListener('scroll', function () { clearTimeout(sweep.t); sweep.t = setTimeout(sweep, 120); }, { passive: true });
  els.forEach(function (el) {
    if (el.closest('.hero')) return;
    var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
    el.style.setProperty('--d', Math.min(sib, 5) * 70 + 'ms');
    el.classList.add('rv');
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight * 0.92) el.classList.add('is-in');
    else io.observe(el);
  });
});


/* v14 interaction layer: clock, back to top, spotlight, tilt, magnetic buttons, step line, counters */
document.addEventListener('DOMContentLoaded', function () {
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Live time in Bo (Sierra Leone uses GMT all year) */
  var clock = document.getElementById('boClock');
  if (clock) {
    var tickClock = function () {
      var d = new Date();
      var hh = String(d.getUTCHours()).padStart(2, '0'), mm = String(d.getUTCMinutes()).padStart(2, '0');
      clock.textContent = hh + ':' + mm + ' GMT';
      clock.setAttribute('datetime', d.toISOString());
    };
    tickClock(); setInterval(tickClock, 15000);
  }

  /* Back to top with progress ring */
  var top = document.getElementById('toTop'), ring = document.getElementById('toTopRing');
  if (top) {
    var upd = function () {
      var h = document.documentElement.scrollHeight - innerHeight, p = h > 0 ? scrollY / h : 0;
      top.classList.toggle('show', scrollY > 600);
      if (ring) ring.style.setProperty('--off', String(100 - p * 100));
    };
    addEventListener('scroll', upd, { passive: true }); upd();
    top.addEventListener('click', function () { scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' }); });
  }

  /* How I work: line fills and steps light up as you scroll */
  var line = document.querySelector('.steps-line');
  if (line) {
    var lis = line.querySelectorAll('li');
    var stepTick = function () {
      var r = line.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.35)));
      if (still) p = 1;
      line.style.setProperty('--p', p.toFixed(3));
      lis.forEach(function (li, i) { li.classList.toggle('lit', p >= (i + 0.5) / lis.length - 0.12); });
    };
    addEventListener('scroll', stepTick, { passive: true }); stepTick();
  }

  /* Count up numbers in the sample dashboard when it appears */
  var nums = document.querySelectorAll('[data-count]');
  if (nums.length && !still && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        var el = e.target, end = +el.getAttribute('data-count'), t0 = performance.now(), dur = 1400;
        var step = function (t) {
          var k = Math.min(1, (t - t0) / dur); k = 1 - Math.pow(1 - k, 3);
          el.textContent = Math.round(end * k); if (k < 1) requestAnimationFrame(step);
        };
        el.textContent = '0'; requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    nums.forEach(function (n) { cio.observe(n); });
  }

  if (!fine || still) return;

  /* Spotlight that follows the pointer on cards */
  document.addEventListener('pointermove', function (e) {
    var c = e.target.closest && e.target.closest('.tile, .quote, .package, .steps li, a.reg-row, .proj-card, .more-card, .svc-card');
    if (!c) return;
    var r = c.getBoundingClientRect();
    c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    c.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });

  /* Hero: soft glow follows the pointer, portrait tilts in 3D */
  var hero = document.querySelector('.hero');
  if (hero) {
    var glow = document.createElement('span'); glow.className = 'hero-glow'; glow.setAttribute('aria-hidden', 'true');
    hero.appendChild(glow);
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      glow.style.setProperty('--hx', (e.clientX - r.left) + 'px'); glow.style.setProperty('--hy', (e.clientY - r.top) + 'px');
    });
  }
  var art = document.querySelector('.hero-photo');
  if (art) {
    art.addEventListener('pointermove', function (e) {
      var r = art.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      art.classList.add('tilting');
      art.style.setProperty('--ry', (x * 10).toFixed(2) + 'deg'); art.style.setProperty('--rx', (-y * 8).toFixed(2) + 'deg');
      art.style.setProperty('--gx', ((x + 0.5) * 100) + '%'); art.style.setProperty('--gy', ((y + 0.5) * 100) + '%');
    });
    art.addEventListener('pointerleave', function () {
      art.classList.remove('tilting'); art.style.setProperty('--rx', '0deg'); art.style.setProperty('--ry', '0deg');
    });
  }

  /* Magnetic primary buttons */
  document.querySelectorAll('.btn-primary, .nav-cta').forEach(function (b) {
    b.addEventListener('pointermove', function (e) {
      var r = b.getBoundingClientRect();
      b.style.setProperty('--tx', ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px');
      b.style.setProperty('--ty', ((e.clientY - r.top - r.height / 2) * 0.3).toFixed(1) + 'px');
    });
    b.addEventListener('pointerleave', function () { b.style.setProperty('--tx', '0px'); b.style.setProperty('--ty', '0px'); });
  });
});

/* v15: sliding pill under the main navigation */
document.addEventListener('DOMContentLoaded', function () {
  var nav = document.querySelector('.nav-links');
  if (!nav || !window.matchMedia('(hover: hover)').matches) return;
  var pill = document.createElement('span'); pill.className = 'nav-pill'; pill.setAttribute('aria-hidden', 'true');
  nav.appendChild(pill); nav.classList.add('has-pill');
  var cur = nav.querySelector('a[aria-current=page]:not(.nav-cta)');
  var place = function (a, show) {
    if (!a) { pill.style.opacity = '0'; return; }
    pill.style.setProperty('--nx', a.offsetLeft + 'px'); pill.style.setProperty('--nw', a.offsetWidth + 'px');
    pill.style.opacity = show ? '1' : '0';
  };
  place(cur, !!cur);
  nav.querySelectorAll('a:not(.nav-cta)').forEach(function (a) { a.addEventListener('mouseenter', function () { place(a, true); }); });
  nav.addEventListener('mouseleave', function () { place(cur, !!cur); });
  addEventListener('resize', function () { place(cur, !!cur); });
});

/* v17: highlight the current section in the notes contents list */
document.addEventListener('DOMContentLoaded', function () {
  var links = document.querySelectorAll('.note-toc a');
  if (!links.length || !('IntersectionObserver' in window)) return;
  var map = {};
  links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (e.isIntersecting) {
        links.forEach(function (a) { a.classList.remove('on'); });
        var a = map[e.target.id]; if (a) a.classList.add('on');
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  document.querySelectorAll('.note-body h2[id], .case-body h2[id]').forEach(function (h) { io.observe(h); });
});
