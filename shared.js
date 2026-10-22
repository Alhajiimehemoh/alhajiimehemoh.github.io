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
        .then(function (r) { if (!r.ok) throw 0; form.reset(); if (status) status.textContent = 'Thank you. Your message was sent and I will reply soon.'; var ok = form.parentNode.querySelector('.sent'); if (ok) { form.hidden = true; ok.hidden = false; } })
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
  var sel = '.section-head, .reader, .foot-logo, .me-open, .laptop, .hs, .role-card, .story li, .sk-card, .principles li, .beyond li, .pf li, .get-list li, .svc-card, .aud li, .sp-card, .gl, .more-card, .rn, .nfig, .callout, .ntable, .takeaways, .rel-card, .mini-dash, .proj-card, .note-card, .res-card, .tile, .reg-row, .steps li, .quote, .promo, .cta-band .wrap, .timeline li, .package, .plain, .faq, .facts, .note-card, .card, .kpi, .demo-card, .shot, .wide-photo, .about-grid > *';
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

/* v21: 'Which service do I need?' finder */
document.addEventListener('DOMContentLoaded', function () {
  var opts = document.querySelectorAll('.fd-opt');
  if (!opts.length) return;
  var empty = document.querySelector('.fd-empty');
  opts.forEach(function (o) {
    o.setAttribute('aria-pressed', 'false');
    o.addEventListener('click', function () {
      var k = o.getAttribute('data-svc');
      opts.forEach(function (x) { x.setAttribute('aria-pressed', x === o ? 'true' : 'false'); });
      if (empty) empty.hidden = true;
      document.querySelectorAll('.fd-res').forEach(function (r) { r.hidden = r.getAttribute('data-res') !== k; });
      if (window.innerWidth < 960) { var out = document.querySelector('.fd-out'); if (out) out.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
    });
  });
});

/* v25: word-by-word headings, count-up stats, card tilt, hero parallax */
(function () {
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.addEventListener('DOMContentLoaded', function () {
    if (!still) {
      document.querySelectorAll('.section-head h2').forEach(function (h) {
        if (h.querySelector('*')) return;
        var words = h.textContent.split(/(\s+)/), out = '', n = 0;
        words.forEach(function (w) { if (/^\s+$/.test(w)) out += w; else out += '<span class="sh-word" style="--w:' + (n++) + '">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>'; });
        h.innerHTML = out;
      });
    }
    /* count up glance numbers */
    var gls = document.querySelectorAll('.gl b[data-count]');
    if (gls.length && !still && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return; io.unobserve(e.target);
          var el = e.target, end = +el.getAttribute('data-count'), t0 = performance.now();
          var step = function (t) { var k = Math.min(1, (t - t0) / 1100); k = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(end * k); if (k < 1) requestAnimationFrame(step); else el.parentNode.classList.add('counted'); };
          el.textContent = '0'; requestAnimationFrame(step);
        });
      }, { threshold: .5 });
      gls.forEach(function (g) { io.observe(g); });
    }
    if (still || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    /* tilt */
    document.querySelectorAll('.proj-card, .rel-card, .res-card, .note-card, .svc-card').forEach(function (c) {
      c.classList.add('tilt');
      c.addEventListener('pointermove', function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        c.classList.add('tilting'); c.style.setProperty('--try', (x * 6).toFixed(2) + 'deg'); c.style.setProperty('--trx', (-y * 5).toFixed(2) + 'deg');
      });
      c.addEventListener('pointerleave', function () { c.classList.remove('tilting'); });
    });
    /* hero parallax */
    var hp = document.querySelector('.hero-photo');
    if (hp) {
      var tick = function () { var y = Math.min(window.scrollY, 600); hp.style.setProperty('--py', (y * 0.08).toFixed(1) + 'px'); document.querySelectorAll('.hero .float-badge').forEach(function (b, i) { b.style.setProperty('--pb', (y * (i % 2 ? -0.06 : 0.12)).toFixed(1) + 'px'); }); };
      window.addEventListener('scroll', tick, { passive: true });
    }
  });
})();

/* v26: laptops: tabs, number count, typing code */
document.addEventListener('DOMContentLoaded', function () {
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var tabs = document.querySelectorAll('.lp-tabs button');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
      document.querySelectorAll('.laptop').forEach(function (l) {
        var on = l.getAttribute('data-lp') === t.getAttribute('data-lp');
        l.classList.toggle('is-active', on);
        if (on) { l.classList.remove('is-in'); void l.offsetWidth; requestAnimationFrame(function () { l.classList.add('is-in'); run(l); }); }
      });
    });
  });
  var hl = function (txt) {
    var e = txt.replace(/&/g, '&amp;').replace(/</g, '&lt;');
    e = e.replace(/(&quot;|")([^"]*?)(&quot;|")/g, '<span class="str">"$2"</span>');
    e = e.replace(/\b(import|as|print)\b/g, '<span class="kw">$1</span>');
    e = e.replace(/\.(read_csv|drop_duplicates|groupby|sum|plot)\(/g, '.<span class="fn">$1</span>(');
    return e;
  };
  function run(l) {
    if (l.dataset.ran) return; l.dataset.ran = '1';
    l.querySelectorAll('[data-to]').forEach(function (b) {
      var end = +b.getAttribute('data-to'), suf = b.getAttribute('data-suf') || '', t0 = null;
      if (still) { b.textContent = end.toLocaleString() + suf; return; }
      setTimeout(function () {
        var step = function (t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1200); k = 1 - Math.pow(1 - k, 3); b.textContent = Math.round(end * k).toLocaleString() + suf; if (k < 1) requestAnimationFrame(step); };
        requestAnimationFrame(step);
      }, 1300);
    });
    var ty = l.querySelector('.typer');
    if (ty) {
      var full = ty.getAttribute('data-text'), py = !!l.querySelector('.py');
      if (still) { ty.innerHTML = py ? hl(full) : full.replace(/</g, '&lt;'); l.classList.add('typed'); return; }
      ty.classList.add('caret'); var i = 0;
      setTimeout(function tick() {
        i += py ? 2 : 1; var part = full.slice(0, i);
        ty.innerHTML = py ? hl(part) : part.replace(/&/g, '&amp;').replace(/</g, '&lt;');
        if (i < full.length) setTimeout(tick, py ? 22 : 45); else { ty.classList.remove('caret'); l.classList.add('typed'); }
      }, 1400);
    }
  }
  if (!('IntersectionObserver' in window)) { document.querySelectorAll('.laptop').forEach(run); return; }
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting && e.target.offsetParent) { run(e.target); } }); }, { threshold: .35 });
  document.querySelectorAll('.laptop').forEach(function (l) { io.observe(l); });
});

/* v28: intro, cursor, rotating words, ripple, wordmark letters, shapes, theme spin */
(function () {
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  try { if (!still && !sessionStorage.getItem('introSeen')) { document.documentElement.classList.add('show-intro'); sessionStorage.setItem('introSeen', '1'); setTimeout(function () { document.documentElement.classList.remove('show-intro'); }, 2600); } } catch (e) {}
  document.addEventListener('DOMContentLoaded', function () {
    var b = document.body;
    if (location.pathname.endsWith('/') || location.pathname.endsWith('index.html')) b.classList.add('page-index');
    /* floating shapes on heads */
    document.querySelectorAll('.page-head, .case-hero, .note-hero, .about-hero, .svc-hero').forEach(function (h) {
      var d = document.createElement('div'); d.className = 'float-shapes'; d.setAttribute('aria-hidden', 'true'); d.innerHTML = '<i></i><i></i><i></i><i></i>'; h.appendChild(d);
    });
    /* section numbers on home */
    if (b.classList.contains('page-index')) {
      var n = 0;
      document.querySelectorAll('main .section-head').forEach(function (sh) {
        n++; var t = document.createElement('span'); t.className = 'sh-num'; t.textContent = (n < 10 ? '0' : '') + n + ' /'; sh.insertBefore(t, sh.firstChild);
      });
    }
    /* wordmark letters */
    var wm = document.querySelector('.wordmark');
    if (wm && !wm.querySelector('.wm-l')) {
      var dot = wm.querySelector('span'); var txt = wm.firstChild && wm.firstChild.nodeType === 3 ? wm.firstChild.textContent : '';
      if (txt) { var h = ''; txt.split('').forEach(function (c, i) { h += '<span class="wm-l" style="--l:' + i + '">' + c + '</span>'; }); wm.firstChild.remove(); wm.insertAdjacentHTML('afterbegin', h); }
    }
    /* theme spin */
    var tb = document.getElementById('themeBtn');
    if (tb) tb.addEventListener('click', function () { tb.classList.remove('spin'); void tb.offsetWidth; tb.classList.add('spin'); setTimeout(function () { tb.classList.remove('spin'); }, 600); });
    /* ripple */
    document.addEventListener('pointerdown', function (e) {
      var btn = e.target.closest && e.target.closest('.btn'); if (!btn || still) return;
      var r = btn.getBoundingClientRect(), sz = Math.max(r.width, r.height), sp = document.createElement('span');
      sp.className = 'ripple'; sp.style.width = sp.style.height = sz + 'px'; sp.style.left = (e.clientX - r.left - sz / 2) + 'px'; sp.style.top = (e.clientY - r.top - sz / 2) + 'px';
      btn.appendChild(sp); setTimeout(function () { sp.remove(); }, 650);
    });
    /* rotating words */
    var rot = document.querySelector('.rot');
    if (rot && !still) {
      var words = rot.getAttribute('data-words').split('|'), i = 0;
      setInterval(function () {
        rot.classList.remove('in'); rot.classList.add('out');
        setTimeout(function () { i = (i + 1) % words.length; rot.textContent = words[i]; rot.classList.remove('out'); rot.classList.add('in'); }, 340);
      }, 2400);
    }
    /* custom cursor */
    if (still || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    var dotEl = document.querySelector('.cursor-dot'), ring = document.querySelector('.cursor-ring');
    if (!dotEl || !ring) return;
    var mx = 0, my = 0, rx = 0, ry = 0, on = false;
    document.addEventListener('pointermove', function (e) {
      mx = e.clientX; my = e.clientY; dotEl.style.transform = 'translate(' + mx + 'px,' + my + 'px)';
      if (!on) { on = true; rx = mx; ry = my; b.classList.add('has-cursor'); }
      var t = e.target.closest && e.target.closest('a, button, summary, label, .fd-opt, input, select, textarea');
      b.classList.toggle('cursor-hover', !!t);
    }, { passive: true });
    document.addEventListener('pointerleave', function () { b.classList.remove('has-cursor'); on = false; });
    document.addEventListener('pointerdown', function () { b.classList.add('cursor-down'); });
    document.addEventListener('pointerup', function () { b.classList.remove('cursor-down'); });
    (function loop() { rx += (mx - rx) * .18; ry += (my - ry) * .18; ring.style.transform = 'translate(' + rx + 'px,' + ry + 'px)'; requestAnimationFrame(loop); })();
  });
})();

/* v30: contact page: open now, clock, character count */
document.addEventListener('DOMContentLoaded', function () {
  var d = new Date(), day = d.getUTCDay();
  var on = document.getElementById('openNow');
  if (on) on.textContent = day === 0 ? 'Closed on Sundays. Message me and I will reply on Monday' : 'Open today, Monday to Saturday';
  document.querySelectorAll('.hours li').forEach(function (li) { if (+li.getAttribute('data-day') === day) li.classList.add('today'); });
  var c2 = document.getElementById('boClock2');
  if (c2) { var t = function () { var n = new Date(); c2.textContent = 'Now ' + String(n.getUTCHours()).padStart(2, '0') + ':' + String(n.getUTCMinutes()).padStart(2, '0') + ' in Bo'; }; t(); setInterval(t, 15000); }
  var ta = document.getElementById('cf-message'), cnt = document.getElementById('cfCount');
  if (ta && cnt) ta.addEventListener('input', function () { cnt.textContent = ta.value.length; });
});

/* v32: footer logo replays its build each time it scrolls into view, or when tapped */
document.addEventListener('DOMContentLoaded', function () {
  var f = document.querySelector('.foot-logo');
  if (!f) return;
  function play() { f.classList.remove('lg-play'); void f.offsetWidth; f.classList.add('lg-play'); }
  f.addEventListener('click', play);
  if (!('IntersectionObserver' in window)) { play(); return; }
  new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) play(); }); }, { threshold: .9 }).observe(f);
});
