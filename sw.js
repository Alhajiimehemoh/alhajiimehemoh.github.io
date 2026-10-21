const VERSION = 'v11-20261021';
const CORE = ["about.html", "capability-statement.html", "case-chw-card-studio.html", "case-dms.html", "case-epi-dashboard.html", "case-survey123.html", "community.html", "contact.html", "cv.html", "demo.html", "demo.js?v=11", "fonts/public-sans-latin-400-normal.woff2", "fonts/zilla-slab-latin-700-normal.woff2", "glossary.html", "hire.html", "images/favicon.svg", "index.html", "manifest.webmanifest", "note-data-decisions.html", "note-healthcare-technology.html", "note-my-journey.html", "note-protect-your-computer.html", "note-small-business-it.html", "now.html", "offline.html", "portfolio.html", "privacy.html", "request.html", "resources.html", "services.html", "shared.js?v=11", "style.css?v=11"];
self.addEventListener('install', e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== VERSION).map(x => caches.delete(x)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(VERSION).then(x => x.put(req, c)); return r; })
      .catch(() => caches.match(req).then(r => r || caches.match('offline.html'))));
    return;
  }
  e.respondWith(caches.match(req).then(r => r || fetch(req).then(n => { const c = n.clone(); caches.open(VERSION).then(x => x.put(req, c)); return n; })));
});
