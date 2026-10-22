"""Shared layout and helpers for build.py and extras.py. Edit site-wide things here."""
import html, json, os, re, urllib.parse
import site_config as C

BASE = 'https://alhajiimehemoh.github.io/'
WA = 'https://wa.me/23279301430'
EMAIL = 'alhajiimehemoh@gmail.com'
CV = 'Alhaji_Ibrahim_Mehemoh_CV.pdf'
OUT = os.path.dirname(os.path.abspath(__file__))
from aimlogo import aim_logo
CSS_V = '36'

NAV = [('portfolio.html', 'Projects', 'nav.projects'), ('services.html', 'Services', 'nav.services'),
       ('resources.html', 'Resources', 'nav.resources'), ('community.html', 'Notes', 'nav.notes'),
       ('about.html', 'About', 'nav.about'), ('hire.html', 'Hire me', 'nav.hire'),
       ('contact.html', 'Contact', 'nav.contact')]

PAGES = []          # pages listed in sitemap.xml
SITE_FILES = []     # extra files the offline cache should keep


def esc(s):
    return html.escape(s, quote=True)


def wa_link(text=''):
    return WA + ('?text=' + urllib.parse.quote(text) if text else '')


def form_action():
    return 'https://formspree.io/f/' + (C.FORMSPREE_ID or 'xxxxabcd')


def form_attrs():
    """Attributes for every form: real Formspree when configured, WhatsApp fallback otherwise."""
    if C.FORMSPREE_ID:
        return 'action="%s" method="POST"' % form_action()
    return 'action="%s" method="POST" data-fallback="wa"' % form_action()


def socials():
    items = [('LinkedIn', C.LINKEDIN), ('GitHub', C.GITHUB), ('TikTok', C.TIKTOK), ('YouTube', C.YOUTUBE)]
    return [(n, u) for n, u in items if u]


def analytics_snippet():
    p, i = C.ANALYTICS_PROVIDER, C.ANALYTICS_ID
    if p == 'goatcounter' and i:
        return f'\n  <script data-goatcounter="https://{esc(i)}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
    if p == 'plausible' and i:
        return f'\n  <script defer data-domain="{esc(i)}" src="https://plausible.io/js/script.js"></script>'
    return ''


def picture(name, alt, width, height, cls='', sizes='100vw', eager=False):
    """Serve WebP with the original JPEG as fallback."""
    base, ext = os.path.splitext(name)
    loading = '' if eager else ' loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{base}.webp">'
            f'<img class="{cls}" src="{name}" width="{width}" height="{height}" alt="{esc(alt)}"{loading}></picture>')


def ld_script(obj):
    return '\n  <script type="application/ld+json">\n%s\n  </script>' % json.dumps(obj, indent=2, ensure_ascii=False)


def page(fn, title, desc, body, active=None, ld=None, noindex=False, sitemap=True, wa_text=None,
         crumbs=None, og_type='website', progress=True, body_class='', extra_head='', preload_hero=False):
    active = active or fn
    url = BASE if fn == 'index.html' else BASE + fn
    links = ''.join(
        '<a href="%s"%s%s data-i18n="%s">%s</a>' % (h, ' class="nav-cta"' if h == 'contact.html' else '',
                                                     ' aria-current="page"' if h == active else '', k, t)
        for h, t, k in NAV)

    # ---- structured data
    blocks = []
    if ld:
        blocks += ld if isinstance(ld, list) else [ld]
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
        for n, (label, href) in enumerate(crumbs, start=2):
            items.append({"@type": "ListItem", "position": n, "name": label, "item": BASE + href if href else url})
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if fn == 'index.html':
        blocks.append({"@context": "https://schema.org", "@type": "WebSite", "name": "Alhaji Ibrahim Mehemoh",
                       "url": BASE, "inLanguage": "en"})
    ldtags = ''.join(ld_script(b) for b in blocks)

    robots = 'noindex, follow' if noindex else 'index, follow'
    if wa_text is None:
        short = title.split('|')[0].strip()
        wa_text = f'Hello Alhaji, I am on your website ({short} page) and would like to talk.'
    wa_href = wa_link(wa_text)
    lang_btn = ('<button class="icon-btn lang-btn" id="langBtn" type="button" aria-label="Switch language to Krio">KR</button>'
                if C.KRIO_ENABLED else '')
    same = socials()
    soc_html = ''.join(f'<li><a href="{esc(u)}" target="_blank" rel="me noopener">{n}</a></li>' for n, u in same)
    soc_block = f'<ul class="social">{soc_html}</ul>' if soc_html else ''
    gbp = f'\n          <li><a href="{esc(C.GOOGLE_BUSINESS_URL)}" target="_blank" rel="noopener">Find me on Google Maps</a></li>' if C.GOOGLE_BUSINESS_URL else ''
    preload = ''
    if preload_hero:
        preload = '\n  <link rel="preload" as="image" type="image/webp" href="images/cover-640.webp">'

    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="theme-color" content="#0F2430">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">

  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:image" content="{BASE}images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{BASE}images/og-image.jpg">

  <link rel="icon" href="images/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="images/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="images/apple-touch-icon.png">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="alternate" type="application/rss+xml" title="Notes by Alhaji Ibrahim Mehemoh" href="feed.xml">
  <link rel="preload" href="fonts/bricolage-grotesque-latin-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/dm-sans-latin-var.woff2" as="font" type="font/woff2" crossorigin>{preload}
  <link rel="stylesheet" href="style.css?v={CSS_V}">
  <script src="shared.js?v={CSS_V}"></script>{analytics_snippet()}{extra_head}{ldtags}
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Skip to main content</a>
<div class="progress" id="progress" aria-hidden="true"></div>
<div class="cursor-dot" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>
<div class="intro" aria-hidden="true">{aim_logo("i", "aim-intro")}</div>

<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="index.html">{aim_logo("h", "aim-head")}<span>Alhaji Ibrahim Mehemoh</span></a>
    <nav class="nav-links" aria-label="Main">{links}</nav>
    <div class="header-tools">
      {lang_btn}
      <button class="icon-btn" id="themeBtn" type="button" aria-label="Switch to dark theme">&#9790;</button>
      <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobileNav"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="mobile-nav" id="mobileNav" aria-label="Mobile">
    <div class="wrap">{links}</div>
  </nav>
</header>

<main id="main">
{body}
</main>

<button class="to-top" id="toTop" type="button" aria-label="Back to top"><svg viewBox="0 0 48 48" aria-hidden="true"><circle class="tt-track" cx="24" cy="24" r="21"/><circle class="tt-ring" id="toTopRing" cx="24" cy="24" r="21" pathLength="100"/><path class="tt-arrow" d="M24 31V17M17.5 23.5 24 17l6.5 6.5"/></svg></button>
<a class="whatsapp-fab" href="{esc(wa_href)}" target="_blank" rel="noopener">WhatsApp</a>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h2>Alhaji Ibrahim Mehemoh</h2>
        <p class="muted">Data Officer and M&amp;E specialist. Bo, Sierra Leone.</p>
        {soc_block}
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp +232 79 301 430</a></li>
          <li><a href="request.html">Request a quote</a></li>
          <li><a href="{CV}" target="_blank" rel="noopener">Download CV (PDF)</a></li>{gbp}
        </ul>
      </div>
      <div>
        <h2>Explore</h2>
        <ul>
          <li><a href="portfolio.html">Projects</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="resources.html">Free resources</a></li>
          <li><a href="demo.html">Sample dashboard</a></li>
          <li><a href="community.html">Notes</a></li>
        </ul>
      </div>
      <div>
        <h2>More</h2>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="now.html">What I am doing now</a></li>
          <li><a href="glossary.html">Glossary</a></li>
          <li><a href="capability-statement.html">Capability statement</a></li>
          <li><a href="cv.html">Web CV</a></li>
          <li><a href="privacy.html">Privacy</a></li>
        </ul>
      </div>
    </div>
    <p class="foot-logo">{aim_logo("f", "aim-foot", "AIM logo")}</p>
    <p class="wordmark" aria-hidden="true">Mehemoh<span>.</span></p>
    <p class="foot-note">&copy; 2026 Alhaji Ibrahim Mehemoh &middot; <a href="rss.html">RSS</a></p>
  </div>
</footer>
</body>
</html>
'''
    with open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
        f.write(out)
    if sitemap and not noindex:
        PAGES.append(fn)


def cta(heading='Need a dashboard, a data collection form or IT support?',
        text='Tell me what you need to report on and who will read it. I will reply with a plan and a quote.',
        wa_text='Hello Alhaji, I would like to talk about a project.'):
    book = ('<a class="btn" href="%s" target="_blank" rel="noopener">Book a call</a>' % esc(C.BOOKING_URL)
            if C.BOOKING_URL else
            '<a class="btn" href="%s" target="_blank" rel="noopener">Book a call</a>' % esc(
                wa_link('Hello Alhaji, I would like to book a 20-minute call. What times suit you this week?')))
    return f'''<section class="cta-band section">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="actions">
      <a class="btn btn-primary" href="{esc(wa_link(wa_text))}" target="_blank" rel="noopener">Message on WhatsApp</a>
      <a class="btn" href="request.html">Request a quote</a>
      {book}
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- small markdown for notes
def md(text):
    """Tiny markdown: paragraphs, '## ' headings, '- ' bullets, **bold**, [text](url)."""
    def inline(s):
        s = esc(s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+|[\w./#-]+)\)', r'<a href="\2">\1</a>', s)
        return s
    out, items = [], []

    def flush():
        nonlocal items
        if items:
            out.append('<ul class="bullets">' + ''.join(f'<li>{inline(i)}</li>' for i in items) + '</ul>')
            items = []
    for block in re.split(r'\n\s*\n', text.strip()):
        lines = block.split('\n')
        if all(l.startswith('- ') for l in lines):
            items += [l[2:] for l in lines]
            flush()
        elif block.startswith('## '):
            flush(); out.append(f'<h2>{inline(block[3:])}</h2>')
        else:
            flush(); out.append(f'<p>{inline(" ".join(lines))}</p>')
    flush()
    return '\n'.join(out)


def reading_minutes(text):
    return max(1, round(len(re.findall(r'\w+', text)) / 200))
