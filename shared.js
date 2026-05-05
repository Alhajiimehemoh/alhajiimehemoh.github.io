/* shared.js — v7 — used on all pages */

/* ── Theme (runs immediately before paint) ── */
(function () {
  const saved = localStorage.getItem('theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', function () {

  /* ── Theme toggle button ── */
  const themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    themeBtn.textContent = isDark ? '☀' : '🌙';
  }

  /* ── Active nav link ── */
  document.querySelectorAll('.nav-links a, .mobile-nav a').forEach(a => {
    const url = new URL(a.href, location.href);
    if (url.pathname === location.pathname) a.classList.add('active');
  });

  /* ── Hamburger menu ── */
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      const open = mobileNav.classList.toggle('open');
      hamburger.classList.toggle('open', open);
    });
    document.addEventListener('click', e => {
      if (mobileNav.classList.contains('open') &&
          !mobileNav.contains(e.target) && !hamburger.contains(e.target)) {
        mobileNav.classList.remove('open');
        hamburger.classList.remove('open');
      }
    });
  }

  /* ── Scroll reveal ── */
  const revealEls = document.querySelectorAll('.reveal, .stagger');
  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('active'); revealObs.unobserve(e.target); }
    });
  }, { threshold: 0.08 });
  revealEls.forEach(el => revealObs.observe(el));

  /* ── Skill bars ── */
  const barObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('.skill-bar-fill').forEach(bar => {
        setTimeout(() => { bar.style.width = bar.dataset.width + '%'; }, 120);
      });
      barObs.unobserve(entry.target);
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.skill-bar-wrap').forEach(el => barObs.observe(el));

  /* ── Counter animation ── */
  function animateCounter(el, target, duration) {
    const start = performance.now();
    function step(now) {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(eased * target);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  const statsObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('[data-target]').forEach(el => {
        animateCounter(el, parseInt(el.dataset.target), 1400);
      });
      statsObs.unobserve(entry.target);
    });
  }, { threshold: 0.2 });
  document.querySelectorAll('.stats-strip').forEach(el => statsObs.observe(el));

  /* ── Back to top ── */
  const btt = document.getElementById('backToTop');
  if (btt) {
    window.addEventListener('scroll', () => btt.classList.toggle('visible', window.scrollY > 400));
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ── Page fade-out on internal links ── */
  document.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    const isInternal = !href.startsWith('http') && !href.startsWith('mailto:') &&
                       !href.startsWith('tel:') && !href.startsWith('#');
    if (isInternal) {
      a.addEventListener('click', e => {
        e.preventDefault();
        document.body.classList.add('fade-out');
        setTimeout(() => { window.location.href = href; }, 320);
      });
    }
  });

  /* ── 3D Tilt (desktop only) ── */
  if (window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.tilt').forEach(card => {
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const rotX = ((e.clientY - r.top  - r.height / 2) / r.height) * -6;
        const rotY = ((e.clientX - r.left - r.width  / 2) / r.width)  *  6;
        card.style.transform = `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-5px)`;
      });
      card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });
  }
});

/* ── Theme toggle global function ── */
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  const btn = document.querySelector('.theme-toggle');
  if (btn) btn.textContent = next === 'dark' ? '☀' : '🌙';
}

/* ── Hamburger global ── */
function toggleMenu() {
  const nav = document.getElementById('mobileNav');
  const btn = document.getElementById('hamburger');
  if (nav && btn) {
    const open = nav.classList.toggle('open');
    btn.classList.toggle('open', open);
  }
}
