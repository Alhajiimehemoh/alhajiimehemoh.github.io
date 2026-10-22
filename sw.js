const VERSION = 'v15-20261022';
const CORE = ["about.html", "capability-statement.html", "case-chw-card-studio.html", "case-dms.html", "case-epi-dashboard.html", "case-survey123.html", "community.html", "contact.html", "cv.html", "demo.html", "demo.js?v=15", "fonts/bricolage-grotesque-latin-var.woff2", "fonts/dm-sans-latin-var.woff2", "glossary.html", "hire.html", "images/favicon.svg", "index.html", "manifest.webmanifest", "note-backup-rule.html", "note-check-epi-data-quality.html", "note-choosing-data-collection-tool.html", "note-chw-reporting.html", "note-clean-data-in-excel.html", "note-dashboards-people-use.html", "note-data-decisions.html", "note-excel-to-database.html", "note-healthcare-technology.html", "note-ict-needs-assessment.html", "note-me-indicators.html", "note-my-journey.html", "note-power-bi-kpis.html", "note-protect-your-computer.html", "note-qr-code-registration.html", "note-small-business-it.html", "note-small-organisation-website.html", "note-stock-reconciliation.html", "note-survey123-mistakes.html", "now.html", "offline.html", "portfolio.html", "privacy.html", "request.html", "resources.html", "services.html", "shared.js?v=15", "style.css?v=15"];
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
