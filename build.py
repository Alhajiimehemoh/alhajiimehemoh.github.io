#!/usr/bin/env python3
"""Generates the static site into ./  Run:  python3 build.py
Settings live in site_config.py, notes in notes.json, layout in layout.py, extra pages in extras.py."""
import datetime, json, os, re
import site_config as C
from layout import *

TODAY = datetime.date.today().isoformat()


def partners():
    """Logos you have permission to show, or the employers' names as plain text."""
    if C.PARTNER_LOGOS:
        items = ''.join(
            '<a class="chip chip-logo" href="%s" target="_blank" rel="noopener"><img src="%s" alt="%s" height="28" loading="lazy"></a>' % (
                esc(p.get('url', '#')), esc(p['image']), esc(p['name'])) for p in C.PARTNER_LOGOS)
    else:
        items = ''.join('<span class="chip">%s</span>' % n for n in ['RHCI', 'SLIEPA', 'SLPP', 'Growth Centre'])
    return '<div class="chips" aria-label="Organisations I have worked with"><span class="chips-label">Worked with</span>%s</div>' % items


def certs_section():
    if not C.CERTIFICATIONS:
        return ''
    rows = ''
    for c in C.CERTIFICATIONS:
        name = esc(c['name'])
        if c.get('url'):
            name = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (esc(c['url']), name)
        rows += '<li>%s, %s%s</li>' % (name, esc(c.get('issuer', '')), (', ' + esc(str(c['year']))) if c.get('year') else '')
    return '<section class="section"><div class="wrap"><div class="section-head"><h2>Certifications and training</h2></div><ul class="plain">%s</ul></div></section>' % rows


# ------------------------------------------------------------------ tally hero art
def tally_svg():
    groups = [(30, 5), (140, 3), (250, 4), (360, 2)]  # x origin, count
    parts, i = [], 0
    for x, n in groups:
        for k in range(min(n, 4)):
            parts.append(f'<path class="tally" pathLength="1" style="--i:{i}" d="M{x + k * 22} 24 V104"/>')
            i += 1
        if n >= 5:
            parts.append(f'<path class="tally strike" pathLength="1" style="--i:{i}" d="M{x - 10} 88 L{x + 78} 40"/>')
            i += 1
    bars = []
    base = 300
    for j, (x, n) in enumerate(groups):
        h = n * 28
        bars.append(f'<rect class="bar" style="--i:{j}" x="{x}" y="{base - h}" width="64" height="{h}" rx="3"/>')
        bars.append(f'<text class="lbl" x="{x + 32}" y="322" text-anchor="middle">Week {j + 1}</text>')
    return ('<svg viewBox="0 0 460 332" role="img" aria-label="Illustration: groups of tally marks drawn on a register page, '
            'then four bars rising beneath them to form a chart.">'
            + ''.join(parts) + '<line class="axis" x1="10" y1="300" x2="450" y2="300"/>' + ''.join(bars) + '</svg>')


# ------------------------------------------------------------------ INDEX
index_body = f'''<div class="wrap">
  <section class="hero">
    <div class="hero-copy">
      <h1 data-i18n="hero.h1">I help health programmes turn field data into decisions.</h1>
      <p class="lede" data-i18n="hero.lede">I am a Data Officer and M&amp;E specialist at Rural Health Care Initiative in Bo District, Sierra Leone. I design Survey123 forms, Power BI dashboards and data systems that nurses, programme managers and donors can read at a glance.</p>
      <div class="actions">
        <a class="btn btn-primary" href="portfolio.html" data-i18n="hero.projects">See projects</a>
        <a class="btn" href="contact.html" data-i18n="hero.contact">Contact me</a>
        <a class="text-link" href="{CV}" target="_blank" rel="noopener" data-i18n="hero.cv">Download CV (PDF)</a>
      </div>
      <p class="fact" data-i18n="hero.fact">Based in Bo, Sierra Leone. Open to roles, contracts and consulting, onsite or remote.</p>
    </div>
    <figure class="hero-art">
      <div class="sheet">{tally_svg()}</div>
      <figcaption>Tally marks on a register become a chart. Illustration only.</figcaption>
    </figure>
  </section>
  <div class="chips" aria-label="Tools I work with"><span class="chips-label">Tools I use</span><span class="chip">Survey123</span><span class="chip">Power BI</span><span class="chip">Excel</span><span class="chip">PostgreSQL</span><span class="chip">Flask</span><span class="chip">Google Apps Script</span></div>
  {partners()}
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What I do</h2><p>Most of my work sits between the field and the report: getting clean data in, and getting clear answers out.</p></div>
    <div class="bento">
      <a class="tile tile-green wide" href="case-epi-dashboard.html">
        <span class="glyph glyph-bars" aria-hidden="true"><i style="--h:35%"></i><i style="--h:60%"></i><i style="--h:48%"></i><i style="--h:80%"></i><i style="--h:100%"></i></span>
        <div><h3>Dashboards and reporting</h3><p>Power BI and Excel reports built from Survey123 exports, designed to extend as each month's data arrives.</p></div>
        <span class="tile-link">See the EPI dashboard</span>
      </a>
      <a class="tile tile-ink slim" href="case-survey123.html">
        <span class="glyph glyph-checks" aria-hidden="true"><i style="--w:5.5rem"></i><i style="--w:4rem"></i><i style="--w:6.5rem"></i></span>
        <div><h3>Data collection and quality</h3><p>XLSForms with lookups, validation and QR autofill, plus checks for duplicates and GPS errors.</p></div>
        <span class="tile-link">See the Survey123 work</span>
      </a>
      <a class="tile slim" href="case-dms.html">
        <span class="glyph glyph-rows" aria-hidden="true"><i style="--w:70%"></i><i style="--w:92%"></i><i style="--w:55%"></i></span>
        <div><h3>Data systems</h3><p>Databases and web tools for programmes, supplies, staff and credentials.</p></div>
        <span class="tile-link">See the system design</span>
      </a>
      <a class="tile wide" href="services.html">
        <span class="glyph glyph-rows" aria-hidden="true"><i style="--w:45%"></i><i style="--w:80%"></i><i style="--w:62%"></i></span>
        <div><h3>IT support and training</h3><p>Networks, computers, backups and staff ICT training for offices, clinics and schools across Sierra Leone.</p></div>
        <span class="tile-link">See services and packages</span>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Selected work</h2><p>Case studies from my work at RHCI. Screenshots are not published because the data belongs to the organisation. Ask me for a walkthrough.</p></div>
    <div class="register">
      <a class="reg-row" href="case-epi-dashboard.html"><h3>EPI reporting dashboard</h3><p>A Power BI report built from monthly Survey123 immunisation exports, with views for nurses, management, the DHMT and donors.</p><span class="reg-status pill pill-dev">In development</span></a>
      <a class="reg-row" href="case-survey123.html"><h3>Survey123 forms and field tools</h3><p>Hospitalisation notification, malaria campaign registration with QR autofill, and an offline stock dashboard.</p><span class="reg-status pill pill-ok">Built</span></a>
      <a class="reg-row" href="case-chw-card-studio.html"><h3>CHW Card Studio</h3><p>Credential cards with QR verification for more than 1,000 Community Health Workers.</p><span class="reg-status pill pill-design">In design</span></a>
      <a class="reg-row" href="case-dms.html"><h3>Data Management System</h3><p>An 11-module system for tracking vaccine coverage and nutrition, using PostgreSQL, Flask and a PWA.</p><span class="reg-status pill pill-done">Designed</span></a>
    </div>
    <p style="margin-top:1.25rem"><a class="text-link" href="portfolio.html">All projects</a></p>
  </div>
</section>

<section class="section-tight">
  <div class="wrap"><div class="promo">
    <div><h2>See how a dashboard works</h2><p>Explore an interactive EPI dashboard built on sample data. Filter by facility and month, and switch between nurse, management and donor views.</p></div>
    <div class="actions"><a class="btn btn-primary" href="demo.html">Open the sample dashboard</a><a class="btn" href="resources.html">Free templates and checklists</a></div>
  </div></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>How I work</h2></div>
    <ol class="steps">
      <li><h3>Understand the need</h3><p>Who reads the report, and what decision does it support?</p></li>
      <li><h3>Design the data</h3><p>Forms, fields and checks that match how the field team really works.</p></li>
      <li><h3>Build and test</h3><p>Validate against real exports before anyone relies on the result.</p></li>
      <li><h3>Hand over and train</h3><p>Clear documentation, so your team can run it without me.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What colleagues say</h2></div>
    <div class="quotes">
      <figure class="quote" style="margin:0"><p>Alhaji has a remarkable ability to turn complex data challenges into simple, workable systems. His Excel dashboards transformed how we track and report health program data every month.</p><footer>Moses Hopanda Carter, Director of Projects, RHCI, Tikonko</footer></figure>
      <figure class="quote" style="margin:0"><p>Reliable, fast, and always willing to go the extra mile. Alhaji kept our IT systems running smoothly and trained staff effectively during a critical period for our organization.</p><footer>Foday Abdulai, District Secretary General, SLPP, Bo District</footer></figure>
      <figure class="quote" style="margin:0"><p>His networking setup gave us stable Wi-Fi across the entire office floor, something we struggled with for months. Professional, well-documented, and completed on time.</p><footer>IT client, Bo (office network setup)</footer></figure>
    </div>
  </div>
</section>

{cta()}'''

person_ld = {
    "@context": "https://schema.org", "@type": "Person", "name": "Alhaji Ibrahim Mehemoh",
    "url": BASE, "image": BASE + "images/profile.jpeg",
    "jobTitle": "Data Officer and Monitoring & Evaluation Specialist",
    "worksFor": {"@type": "Organization", "name": "Rural Health Care Initiative (RHCI)"},
    "address": {"@type": "PostalAddress", "addressLocality": "Bo", "addressCountry": "SL"},
    "email": EMAIL, "telephone": "+23279301430",
    "knowsAbout": ["Monitoring and evaluation", "Health data systems", "Survey123", "Power BI", "Excel reporting", "IT support"],
    "knowsLanguage": ["English", "Krio"],
}
page('index.html', 'Alhaji Ibrahim Mehemoh | Health Data and M&E Specialist in Bo, Sierra Leone',
     'Data Officer and M&E specialist in Bo, Sierra Leone. Survey123 forms, Power BI dashboards, data quality and health data systems for NGOs and health programmes.',
     index_body, ld=person_ld)

# ------------------------------------------------------------------ ABOUT
about_body = f'''<div class="wrap">
  <div class="page-head"><h1>About me</h1><p class="lede">I started in a computer training centre in Bo and now manage immunisation, home visit and malaria data for a health NGO.</p></div>
</div>
<section class="section">
  <div class="wrap about-grid">
    <div>
      <picture><source type="image/webp" srcset="images/profile-square.webp"><img class="portrait" src="images/profile.jpeg" width="320" height="320" alt="Portrait of Alhaji Ibrahim Mehemoh"></picture>
    </div>
    <div class="prose">
      <p>I am Alhaji Ibrahim Mehemoh, based in Bo, Sierra Leone. I trained in computer software, hardware and networking, then spent years teaching Microsoft Office and fixing computers before moving into data and IT roles in government, politics and the NGO sector.</p>
      <p>Since October 2024 I have worked at Rural Health Care Initiative (RHCI) as a Data Officer. I manage programme data for immunisation (EPI), home visits and malaria case management, build the Survey123 forms the field teams use, and supervise a contract Data Assistant. Working in health taught me that a good system is one that field staff actually use and managers actually trust.</p>
      <p>I am studying Computer Science and I am open to consulting, contracts and full-time roles in M&amp;E, health data and data systems. I work in English and Krio.</p>
      <div class="actions"><a class="btn btn-primary" href="{CV}" target="_blank" rel="noopener">Download CV (PDF)</a><a class="btn" href="contact.html">Contact me</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Experience</h2></div>
    <ul class="timeline">
      <li><span class="when">Oct 2024 to present</span><div><h3>Evaluator and Data Officer, RHCI, Tikonko</h3><p>Health data systems, CHW database management, dashboards, mobile data collection and M&amp;E reporting. Reported a 25% accuracy improvement in programme data.</p></div></li>
      <li><span class="when">Sep 2023 to Oct 2024</span><div><h3>Assistant IT Manager, SLIEPA, Freetown</h3><p>Agency-wide IT infrastructure, helpdesk, cybersecurity measures and staff ICT training. Reported 99% system availability.</p></div></li>
      <li><span class="when">Jan 2022 to Sep 2023</span><div><h3>IT and Data Officer, SLPP, Bo District</h3><p>Centralised membership databases, data analysis and digital campaign management. Reported a 30% increase in online engagement.</p></div></li>
      <li><span class="when">2016 to 2021</span><div><h3>ICT Tutor and Internet Cafe Attendant, Growth Centre, Bo</h3><p>Taught Microsoft Office to more than 200 students and handled hardware and network troubleshooting.</p></div></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap cols">
    <div>
      <h2>Education</h2>
      <ul class="plain">
        <li>BSc Computer Science (in progress)</li>
        <li>Diploma in Networking, Growth Centre Computer Training Institute, 2017 to 2019</li>
        <li>Diploma in Computer Hardware, Growth Centre Computer Training Institute, 2015 to 2017</li>
        <li>Diploma in Computer Software, Growth Centre Computer Training Institute, 2015 to 2016</li>
      </ul>
    </div>
    <div>
      <h2>Tools and skills</h2>
      <ul class="plain">
        <li><strong>Data and M&amp;E:</strong> Power BI, Excel, Survey123 and XLSForm, data cleaning and quality checks, indicator reporting</li>
        <li><strong>Systems:</strong> PostgreSQL and Flask design, Google Apps Script, HTML tools</li>
        <li><strong>Platforms compared:</strong> KoboToolbox, CommCare, ODK, DHIS2</li>
        <li><strong>IT:</strong> networking (LAN and Wi-Fi), hardware, WordPress, backups and basic security</li>
        <li><strong>Training:</strong> staff ICT and data skills</li>
      </ul>
    </div>
  </div>
</section>

{certs_section()}

<section class="section-tight"><div class="wrap">{picture("images/cover.jpeg", "A team meeting in a busy room with laptops, documents and a projector", 1080, 810, "wide-photo")}</div></section>

{cta('Want to work together?', 'Send me a short description of the report, form or system you need.')}'''
page('about.html', 'About | Alhaji Ibrahim Mehemoh',
     'Background of Alhaji Ibrahim Mehemoh: Data Officer at RHCI, trained in software, hardware and networking, working in health data and M&E in Bo, Sierra Leone.',
     about_body)

# ------------------------------------------------------------------ SERVICES
FAQ = [
    ('Where do you work?', 'Onsite in Bo and nearby areas, and remotely across Sierra Leone. Most data and dashboard work can be done remotely.'),
    ('How much does a data project cost?', 'IT support packages are priced in Leones above. Data and M&E projects are priced by scope after a short conversation. Use the request form to describe what you need and I will reply with a plan and a quote.'),
    ('What do you need from me to start?', 'A short description of what you report on, who reads the report, and a sample of your current forms or data exports. Remove names, phone numbers and other identifying details from any sample you send.'),
    ('Which tools do you use?', 'Survey123 and XLSForm for data collection, Power BI and Excel for dashboards and reports, PostgreSQL and Flask for larger systems, and Google Apps Script for lightweight tools. I can also advise on choosing between KoboToolbox, CommCare, ODK and DHIS2.'),
    ('How do you handle sensitive data?', 'Your data stays with you. I work from exports you control, and I never publish identifiable patient or staff information on this website.'),
    ('Do you train our staff?', 'Yes. I run hands-on training in Excel, data entry, data quality checks and basic dashboards for programme and facility staff.'),
    ('How quickly do you reply?', 'WhatsApp is the fastest way to reach me. Email suits longer documents and proposals.'),
]


def faq_html():
    items = ''.join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQ)
    return '<section class="section"><div class="wrap"><div class="section-head"><h2>Common questions</h2></div><div class="faq-list">%s</div></div></section>' % items


def faq_ld():
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}


def row2(h, p):
    return f'<li class="reg-row two"><h3>{h}</h3><p>{p}</p></li>'

services_body = f'''<div class="wrap">
  <div class="page-head"><h1>Services</h1><p class="lede">Data and M&amp;E work for health programmes and NGOs, plus practical IT support for offices, clinics and schools in Bo and across Sierra Leone.</p>
  <div class="actions"><a class="btn btn-primary" href="request.html">Request a quote</a><a class="btn" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div></div>
</div>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Data and M&amp;E</h2><p>Priced by scope. Send me your reporting need and I will reply with a plan and a quote.</p></div>
    <ul class="register">
      {row2('Dashboards and reports', 'Power BI and Excel dashboards that refresh from your survey exports, with views for field staff, managers and donors.')}
      {row2('Survey and form design', 'Survey123 XLSForms with lookups, skip logic, validation and QR autofill, tested before field use.')}
      {row2('Data quality audits', 'Checks for duplicates, GPS errors, impossible dose sequences, inconsistent village names and missing records, with a report per team or facility.')}
      {row2('M&amp;E reporting', 'Monthly and quarterly programme reports, indicator tracking and presentations for management, boards and donors.')}
      {row2('Data systems', 'Database and web tool design for tracking patients, supplies, staff or credentials.')}
      {row2('Training', 'Hands-on training in Excel, data entry, data quality and basic dashboards for programme and facility staff.')}
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>IT support</h2><p>Onsite in Bo and nearby areas. Remote support across Sierra Leone.</p></div>
    <ul class="register">
      {row2('Technical support and hardware', 'Repairs, RAM and SSD upgrades, software installation, virus removal, printer and scanner setup.')}
      {row2('Networking and internet', 'LAN and Wi-Fi setup, routers, network design and cable management for offices, NGOs and clinics.')}
      {row2('Web and digital', 'WordPress sites, domains and hosting, maintenance, professional email and basic graphics.')}
      {row2('Security and backups', 'Backup and recovery, antivirus and firewall setup, user accounts, access control and system checks.')}
      {row2('Office and NGO IT support', 'Support contracts, staff training, ICT consultancy and inventory tools.')}
    </ul>
  </div>
</section>

<section class="section" id="packages">
  <div class="wrap">
    <div class="section-head"><h2>IT support packages</h2><p>Prices in Leones. Final cost depends on the number of devices or users, travel distance and complexity. NGOs, clinics and schools can request a tailored quote.</p></div>
    <div class="packages">
      <div class="package"><h3>Starter</h3><p class="muted">Quick support</p><p class="price">Le 250 to Le 600</p><ul class="bullets"><li>Setup and basic troubleshooting</li><li>Printer setup</li><li>Basic cleanup</li></ul><a class="btn" href="request.html?service=IT+support+(Starter)">Request Starter</a></div>
      <div class="package featured"><h3>Standard</h3><p class="muted">Office setup</p><p class="price">Le 800 to Le 2,500</p><ul class="bullets"><li>Wi-Fi and router configuration</li><li>Staff PC setup</li><li>Basic network design</li><li>Excel reporting templates</li></ul><a class="btn btn-primary" href="request.html?service=IT+support+(Standard)">Request Standard</a></div>
      <div class="package"><h3>Premium</h3><p class="muted">Monthly contract</p><p class="price">Le 3,000+</p><ul class="bullets"><li>Ongoing support</li><li>Backups and security checks</li><li>Systems setup and staff training</li><li>Priority response</li></ul><a class="btn" href="request.html?service=IT+support+(Premium)">Book Premium</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>How a project runs</h2></div>
    <ol class="steps">
      <li><h3>Assess</h3><p>We agree what you need and who will use it.</p></li>
      <li><h3>Design</h3><p>I propose the form, system or setup and a fixed scope.</p></li>
      <li><h3>Build and test</h3><p>I deliver it and test it with your real data or equipment.</p></li>
      <li><h3>Hand over</h3><p>Documentation and training, so your team can keep it running.</p></li>
    </ol>
  </div>
</section>
{faq_html()}
{cta('Ready to start?', 'Describe the problem in a few lines. I will tell you what I would do and what it costs.')}'''
sv_ld = {
    "@context": "https://schema.org", "@type": "ProfessionalService",
    "name": "Alhaji Ibrahim Mehemoh, Data, M&E and IT Support", "url": BASE + "services.html",
    "image": BASE + "images/og-image.jpg", "telephone": "+23279301430", "email": EMAIL,
    "areaServed": {"@type": "Country", "name": "Sierra Leone"},
    "address": {"@type": "PostalAddress", "addressLocality": "Bo", "addressCountry": "SL"},
    "knowsAbout": ["Monitoring and evaluation", "Dashboards", "Survey design", "Computer networking", "IT support"],
}
page('services.html', 'Services | Data, M&E and IT Support in Sierra Leone',
     'Dashboards, Survey123 forms, data quality audits, M&E reporting, IT support and networking in Bo and across Sierra Leone. IT packages priced in Leones.',
     services_body, ld=[sv_ld, faq_ld()], crumbs=[('Services', None)])

# ------------------------------------------------------------------ PORTFOLIO
portfolio_body = f'''<div class="wrap">
  <div class="page-head"><h1>Projects</h1><p class="lede">Health data and M&amp;E work from my role at Rural Health Care Initiative, plus earlier IT and systems projects. Screenshots are not published because the data belongs to the organisation. Ask me for a walkthrough.</p></div>
</div>
<section class="section" id="projects">
  <div class="wrap">
    <div class="section-head"><h2>Case studies</h2></div>
    <div class="filters" role="group" aria-label="Filter projects by type"><button type="button" class="filter is-active" data-filter="all" aria-pressed="true">All</button><button type="button" class="filter" data-filter="health" aria-pressed="false">Health data</button><button type="button" class="filter" data-filter="systems" aria-pressed="false">Systems</button><button type="button" class="filter" data-filter="it" aria-pressed="false">IT and field tools</button></div>
    <p class="small muted" id="filterCount" role="status" aria-live="polite"></p>
    <div class="register" data-filter-target>
      <a class="reg-row" data-type="health" href="case-epi-dashboard.html"><h3>EPI reporting dashboard</h3><p>Power BI report from monthly Survey123 immunisation exports, plus the data quality checks behind it.</p><span class="reg-status pill pill-dev">In development</span></a>
      <a class="reg-row" data-type="health it" href="case-survey123.html"><h3>Survey123 forms and field tools</h3><p>Hospitalisation notification form, malaria campaign registration with QR autofill, an offline stock dashboard and a campaign inventory tracker.</p><span class="reg-status pill pill-ok">Built</span></a>
      <a class="reg-row" data-type="systems health" href="case-chw-card-studio.html"><h3>CHW Card Studio</h3><p>Issuing and verifying credential cards for more than 1,000 Community Health Workers.</p><span class="reg-status pill pill-design">In design</span></a>
      <a class="reg-row" data-type="systems health" href="case-dms.html"><h3>Data Management System</h3><p>An 11-module system for vaccine coverage and nutrition tracking, using PostgreSQL, Flask and a PWA.</p><span class="reg-status pill pill-done">Designed</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Earlier work</h2></div>
    <ul class="register" data-filter-target>
      <li class="reg-row two" data-type="health"><h3>Health facility reporting tools, RHCI</h3><div><p><strong>Problem:</strong> Manual reporting and inconsistent tracking reduced accuracy and slowed submissions.</p><p><strong>Solution:</strong> Excel tracking tools for MMS (multiple micronutrient supplements), CHW attendance, ultrasound reporting and inventory, with standard templates and a monthly reporting workflow.</p><p><strong>Outcome:</strong> More accurate data and smoother monthly submissions.</p></div></li>
      <li class="reg-row two" data-type="it"><h3>Office network and computer support</h3><div><p><strong>Problem:</strong> Frequent downtime, connectivity issues and recurring device problems.</p><p><strong>Solution:</strong> Router configuration, LAN and Wi-Fi improvements, a device setup checklist and a regular support routine.</p><p><strong>Outcome:</strong> Better uptime, fewer repeat issues and smoother daily operations.</p></div></li>
      <li class="reg-row two" data-type="health it"><h3>Vitamin Angels supply tracking</h3><div><p><strong>Problem:</strong> Unclear stock visibility for MMS, Vitamin A and Albendazole distribution.</p><p><strong>Solution:</strong> Excel templates and printed logbooks for recording each distribution.</p><p><strong>Outcome:</strong> Clearer stock visibility and accountability.</p></div></li>
    </ul>
  </div>
</section>
{cta('Want something similar for your team?', 'Tell me what you track today and what you need to report. I will suggest the simplest system that works.')}'''
page('portfolio.html', 'Projects | Alhaji Ibrahim Mehemoh',
     'Health data and M&E projects: a Power BI EPI dashboard, Survey123 forms, CHW credential cards and a data management system, from RHCI in Bo, Sierra Leone.',
     portfolio_body, crumbs=[('Projects', None)])


# ------------------------------------------------------------------ CASE STUDIES
def video_embed(url):
    m = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{6,})', url)
    if m:
        return '<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/%s" title="Video" loading="lazy" allowfullscreen></iframe></div>' % m.group(1)
    if url.lower().endswith('.mp4'):
        return '<video class="video" controls preload="none" src="%s"></video>' % esc(url)
    return '<p><a class="btn" href="%s" target="_blank" rel="noopener">Watch the video</a></p>' % esc(url)


def case_shots(slug):
    """Any images dropped into images/cases/<slug>/ appear here automatically."""
    d = os.path.join(OUT, 'images', 'cases', slug)
    if not os.path.isdir(d):
        return ''
    files = sorted(f for f in os.listdir(d) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')))
    if not files:
        return ''
    figs = ''
    for f in files:
        label = os.path.splitext(f)[0].replace('-', ' ').replace('_', ' ')
        figs += '<figure class="shot"><button type="button" class="shot-btn" data-full="images/cases/%s/%s" aria-label="Enlarge: %s"><img src="images/cases/%s/%s" alt="%s" loading="lazy"></button><figcaption>%s</figcaption></figure>' % (slug, f, esc(label), slug, f, esc(label), esc(label))
    return '<section class="section-tight"><h2>Screenshots</h2><div class="shots">%s</div></section>' % figs


def case(fn, title, desc, lede, facts, sections, nxt):
    f = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)
    s = ''
    for h, content in sections:
        s += f'<section class="section-tight"><div class="prose"><h2>{h}</h2>{content}</div></section>\n'
    slug = fn[:-5]
    result = C.CASE_RESULTS.get(slug)
    result_html = '<section class="section-tight"><div class="result"><strong>Result</strong><p>%s</p></div></section>' % esc(result) if result else ''
    video = C.CASE_VIDEOS.get(slug)
    video_html = ''
    if video:
        video_html = '<section class="section-tight"><h2>Walkthrough video</h2>%s</section>' % video_embed(video)
    shots = case_shots(slug)
    body = f'''<div class="wrap">
  <div class="page-head"><p class="crumb"><a href="portfolio.html">Projects</a></p><h1>{title}</h1><p class="lede">{lede}</p></div>
  <section class="section-tight" style="padding-top:2rem"><dl class="facts">{f}</dl></section>
  {result_html}
  {s}
  {shots}
  {video_html}
  <section class="section-tight"><div class="prose"><p class="muted">Screenshots are not published here because the data belongs to RHCI. I am happy to walk you through the work on a call.</p></div>
  <div class="note-nav"><a href="portfolio.html">All projects</a><a href="{nxt[0]}">Next: {nxt[1]}</a></div></section>
</div>
{cta()}'''
    page(fn, title + ' | Alhaji Ibrahim Mehemoh', desc, body, active='portfolio.html', crumbs=[('Projects', 'portfolio.html'), (title, None)],
         wa_text='Hello Alhaji, I read your %s case study and would like to talk.' % title)


case('case-epi-dashboard.html', 'EPI reporting dashboard',
     'Case study: a Power BI report built from monthly Survey123 immunisation exports at RHCI, with data quality checks for GPS, dose sequences and duplicates.',
     'A Power BI report that turns each monthly Survey123 immunisation export into the same trusted view, for people who need different levels of detail.',
     [('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('Role', 'Data Officer: design, build and data quality'),
      ('Status', 'In development'), ('Data source', 'Survey123 EPI exports, supplied monthly'),
      ('Tools', 'Power BI, Survey123, Excel'),
      ('Audience', 'Nurses, health facilities, RHCI management, the DHMT, the RHCI Board and donors')],
     [('The reporting question', '<p>EPI (immunisation) visit data is collected in Survey123 and exported as files. The challenge is to turn every new export into the same report without rebuilding it by hand, and to keep the numbers trustworthy as data volume grows.</p>'),
      ('What I built', '<p>A Power BI project built from the Survey123 EPI export, covering 1 January 2026 to date. It is designed to extend as each monthly export arrives, so the report grows instead of being rebuilt.</p><p>Different readers need different views. Nurses and facilities see their own work, RHCI management sees programme-wide results, and the DHMT, the Board and donors see summary reporting.</p>'),
      ('Data quality checks', '<p>Before numbers reach a dashboard, the records are checked. In March and April 2026 I ran a multi-stage analysis of the nurse datasets and produced a cleaned dataset. The checks cover:</p><ul class="bullets"><li>GPS validation</li><li>Dose sequence violations</li><li>Duplicate detection</li><li>Village name inconsistencies</li><li>Compliance tracking per nurse</li></ul><p>Each nurse received an Excel audit workbook, and management received consolidated Word reports and presentations.</p>'),
      ('How it is built', '<p>The work moves through staged checkpoints: foundation (data model and structure), build (measures and pages) and validation and handover (checking figures against the source export before release).</p>')],
     ('case-survey123.html', 'Survey123 forms and field tools'))

case('case-survey123.html', 'Survey123 forms and field tools',
     'Case study: Survey123 XLSForms for hospitalisation notification and malaria campaign registration, an offline stock dashboard and a campaign inventory tracker at RHCI.',
     'Forms and small tools that field and facility staff can use without training manuals, and that produce data a dashboard can trust.',
     [('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('Role', 'Form design, build and testing'),
      ('Status', 'Built'), ('Tools', 'Survey123 (XLSForm), Excel, HTML'),
      ('Audience', 'Field staff, facility staff, programme managers')],
     [('Hospitalisation notification form', '<p>A Survey123 form for staff hospitalisation notices, with cascading lookups. Choosing an employee limits the dependent list to that employee, which prevents mismatched records.</p>'),
      ('Malaria campaign registration and field visit form', '<p>A registration and visit form where a QR code autofills the patient details. Staff scan instead of retyping, which cuts typing errors and speeds up each visit.</p>'),
      ('Offline stock dashboard', '<p>A private dashboard that works offline on Survey123 CSV exports. It reports by day and by location and calculates stock as opening plus restock minus use, with Excel and PDF export.</p>'),
      ('Campaign inventory tracker', '<p>For a three-month mobile health campaign that visits four locations in rotation, I built an Excel tracker. It records stock taken on each trip, stock used and remaining after it, and the running balance at the central store.</p>')],
     ('case-chw-card-studio.html', 'CHW Card Studio'))

case('case-chw-card-studio.html', 'CHW Card Studio',
     'Case study: a credential system for more than 1,000 Community Health Workers, with printed cards, QR codes and online verification, specified for RHCI.',
     'A system to issue, print and verify credential cards for Community Health Workers, so anyone can check a card is genuine.',
     [('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('Role', 'Specification and design'),
      ('Status', 'In design'), ('Scale', 'More than 1,000 CHWs'),
      ('Planned stack', 'Google Sheets, Google Apps Script, Google Drive'),
      ('Audience', 'RHCI administrators, CHWs, facility staff and the public verifying a card')],
     [('What it does', '<ul class="bullets"><li>Gives each CHW a permanent ID</li><li>Produces standard CR80 cards with a QR code</li><li>Covers the card lifecycle: renewal, replacement, loss and revocation</li><li>Provides a public verification page that confirms a card is valid</li><li>Shows whether a CHW is Government-trained, MOMS-trained or dual-trained</li></ul>'),
      ('Why Google tools', '<p>Google Sheets acts as the database, Apps Script as the backend, and Drive stores photos and QR images. RHCI staff already know these tools, and there are no servers to run or pay for.</p>'),
      ('Related work already built', '<p>I built a staff medical ID card generator as a single-file HTML app. It reads a staff and dependants workbook, prints front and back cards at 85.6 by 53.98 mm, and adds QR verification and security patterns. The CHW system applies the same ideas at larger scale.</p>')],
     ('case-dms.html', 'Data Management System'))

case('case-dms.html', 'Data Management System',
     'Case study: an 11-module data management system for RHCI to track vaccine coverage and nutrition, designed with PostgreSQL, Flask and a progressive web app.',
     'An 11-module system for tracking vaccine coverage and nutrition, designed to work for nurses in the field and managers in the office.',
     [('Organisation', 'Rural Health Care Initiative (RHCI), Bo District'), ('Role', 'System design and documentation'),
      ('Status', 'Designed'), ('Stack', 'PostgreSQL, Flask, progressive web app (PWA)'),
      ('Users', 'Administrators and nurses, with role-based access')],
     [('What it covers', '<p>The first scope, written in November 2024, was a malaria vaccine coverage and nutrition tracking system. It includes:</p><ul class="bullets"><li>Patient management</li><li>Vaccine and nutrition tracking</li><li>Appointments and reminders</li><li>Missed appointment tracking</li><li>Dashboards, graphs and reports</li><li>Real-time notifications</li></ul>'),
      ('How the design changed', '<p>The first plan used SQL Server, ASP.NET Core and React. In January 2025 the database moved to PostgreSQL, and the system settled into its current Flask and PWA design. A PWA suits low connectivity because it installs on a phone and keeps working with a weak signal.</p>'),
      ('Documentation', '<p>I produced planning documents across several versions, covering the modules, roles and data model, so a developer or team can build from them.</p>')],
     ('case-epi-dashboard.html', 'EPI reporting dashboard'))

# ------------------------------------------------------------------ HIRE
hire_body = f'''<div class="wrap">
  <div class="page-head"><h1>Hire me</h1><p class="lede">I am open to full-time, contract and consulting work in M&amp;E, health data and data systems, onsite in Bo or remote.</p>
  <div class="actions"><a class="btn btn-primary" href="{CV}" target="_blank" rel="noopener">Download CV (PDF)</a><a class="btn" href="contact.html">Contact me</a></div></div>
</div>
<section class="section">
  <div class="wrap cols">
    <div>
      <h2>Roles I am looking for</h2>
      <ul class="plain">
        <li>M&amp;E officer or data officer</li>
        <li>Data analyst</li>
        <li>Survey and data collection specialist</li>
        <li>Systems administrator</li>
        <li>IT support and help desk</li>
        <li>Web administrator</li>
        <li>Network administrator</li>
      </ul>
    </div>
    <div>
      <h2>What I bring</h2>
      <ul class="bullets">
        <li>Years of running real programme data for a health NGO, from form to board report</li>
        <li>Survey123, Power BI and Excel skills, with attention to data quality</li>
        <li>IT support and networking background, so I understand the equipment behind the data</li>
        <li>Clear documentation and hands-on training for non-technical teams</li>
        <li>English and Krio</li>
      </ul>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>See the work first</h2><p>The projects page shows how I approach problems. I can share more detail and walk through the work on a call.</p></div>
    <p><a class="btn" href="portfolio.html">View projects</a></p>
  </div>
</section>
{cta('Let us talk about the role.', 'Send me the job description or the problem you want solved.')}'''
page('hire.html', 'Hire Me | Alhaji Ibrahim Mehemoh',
     'Hire Alhaji Ibrahim Mehemoh for M&E, health data, Survey123, dashboards, systems administration or IT support. Based in Bo, Sierra Leone; onsite or remote.',
     hire_body)

# ------------------------------------------------------------------ CONTACT
contact_body = f'''<div class="wrap">
  <div class="page-head"><h1>Contact</h1><p class="lede">WhatsApp is the fastest way to reach me. Email suits proposals and documents.</p>
  <div class="actions"><a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">WhatsApp now</a><a class="btn" href="mailto:{EMAIL}">Email me</a><button class="btn" type="button" data-copy="{EMAIL}">Copy email</button><a class="btn" href="tel:+23279301430">Call</a><a class="btn" href="{esc(C.BOOKING_URL) if C.BOOKING_URL else esc(wa_link('Hello Alhaji, I would like to book a 20-minute call. What times suit you this week?'))}" target="_blank" rel="noopener">Book a call</a></div></div>
</div>
<section class="section">
  <div class="wrap cols">
    <div>
      <dl class="facts" style="margin-bottom:0">
        <div><dt>WhatsApp and phone</dt><dd><a href="tel:+23279301430">+232 79 301 430</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="mailto:amehemohib@gmail.com">amehemohib@gmail.com</a></dd></div>
        <div><dt>Location</dt><dd>Bo, Sierra Leone. Onsite in Bo and nearby areas, remote across the country.</dd></div>
        <div><dt>CV</dt><dd><a href="{CV}" target="_blank" rel="noopener">Download as PDF</a></dd></div>
      </dl>
    </div>
    <div>
      <h2>Send a message</h2>
      <form {form_attrs()}>
        <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="field"><label for="cf-name">Your name</label><input id="cf-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="cf-email">Your email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="cf-message">What do you need?</label><textarea id="cf-message" name="message" rows="6" required></textarea></div>
        <button class="btn btn-primary" type="submit">Send message</button>
        <p class="small muted" id="formStatus" role="status" aria-live="polite" style="margin-top:.75rem"></p>
      </form>
      <p class="small muted">Prefer a structured request? Use the <a href="request.html">quote request form</a>.</p>
    </div>
  </div>
</section>'''
page('contact.html', 'Contact | Alhaji Ibrahim Mehemoh',
     'Contact Alhaji Ibrahim Mehemoh in Bo, Sierra Leone by WhatsApp, email or phone for data, M&E and IT support work.',
     contact_body, crumbs=[('Contact', None)])

# ------------------------------------------------------------------ NOTES (blog), from notes.json
NOTES = json.load(open(os.path.join(OUT, 'notes.json'), encoding='utf-8'))
for n in NOTES:
    n['fn'] = n['slug'] + '.html'
    n['html'] = md(n['body'])
    n['mins'] = reading_minutes(n['body'])
cats = sorted({n['category'] for n in NOTES})


def fmt_date(d):
    if not d:
        return ''
    try:
        return datetime.date.fromisoformat(d).strftime('%d %B %Y').lstrip('0')
    except ValueError:
        return d


def note_row(n):
    date = ('<time datetime="%s">%s</time> &middot; ' % (n['date'], fmt_date(n['date']))) if n.get('date') else ''
    return ('<a class="reg-row two" data-cat="%s" data-search="%s" href="%s"><h3>%s</h3><div><p>%s</p>'
            '<p class="small"><span class="pill pill-cat">%s</span> %s%d min read</p></div></a>') % (
        esc(n['category']), esc((n['title'] + ' ' + n['summary'] + ' ' + n['body']).lower()), n['fn'], esc(n['title']),
        esc(n['summary']), esc(n['category']), date, n['mins'])


rows = ''.join(note_row(n) for n in sorted(NOTES, key=lambda n: n.get('date') or '', reverse=True))
cat_btns = '<button type="button" class="filter is-active" data-cat="all" aria-pressed="true">All</button>' + ''.join(
    '<button type="button" class="filter" data-cat="%s" aria-pressed="false">%s</button>' % (esc(c), esc(c)) for c in cats)
notes_body = f'''<div class="wrap">
  <div class="page-head"><h1>Notes</h1><p class="lede">Short, practical posts on data, health systems, IT and cybersecurity.</p>
  <p class="small"><a href="feed.xml">Subscribe with RSS</a></p></div>
</div>
<section class="section">
  <div class="wrap">
    <div class="notes-tools">
      <label class="sr-only" for="noteSearch">Search notes</label>
      <input id="noteSearch" type="search" placeholder="Search notes" autocomplete="off">
      <div class="filters" role="group" aria-label="Filter notes by category">{cat_btns}</div>
    </div>
    <p class="small muted" id="noteCount" role="status" aria-live="polite"></p>
    <div class="register" id="noteList">{rows}</div>
    <p class="muted" id="noteEmpty" hidden>No notes match your search.</p>
  </div>
</section>
<section class="section">
  <div class="wrap cols">
    <div><h2>How I support communities</h2><p class="prose">I work with clinics, schools, offices, NGOs and community groups to reduce errors, strengthen coordination and improve decisions, using tools that fit local realities.</p></div>
    <div><h2>Focus areas</h2><ul class="plain"><li>Digital support: practical tech and simple data systems</li><li>Training: basic ICT and data skills for staff</li><li>Reporting and accountability: tracking supplies, attendance and activity</li></ul></div>
  </div>
</section>
{cta('Want to work together?', 'If your team needs a tracking system, reporting templates or training, send me a message.')}'''
page('community.html', 'Notes | Alhaji Ibrahim Mehemoh',
     'Short practical posts by Alhaji Ibrahim Mehemoh on health data systems, small business IT, cybersecurity habits and using data to decide.',
     notes_body, active='community.html', crumbs=[('Notes', None)])

# To add a note: add an entry to notes.json (or use admin.html to write it), then run: python3 build.py
for i, n in enumerate(NOTES):
    nxt = NOTES[(i + 1) % len(NOTES)]
    date = ('<time datetime="%s">%s</time> &middot; ' % (n['date'], fmt_date(n['date']))) if n.get('date') else ''
    page_url = BASE + n['fn']
    share_wa = esc(wa_link('%s %s' % (n['title'], page_url)))
    b = f'''<div class="wrap">
  <div class="page-head"><p class="crumb"><a href="community.html">Notes</a></p><h1>{esc(n['title'])}</h1><p class="lede">{esc(n['summary'])}</p>
  <p class="small muted">{date}{esc(n['category'])} &middot; {n['mins']} min read</p></div>
  <section class="section"><div class="note-body">{n['html']}
  <div class="share"><span class="muted small">Share:</span><a class="btn" href="{share_wa}" target="_blank" rel="noopener">WhatsApp</a><button class="btn" type="button" data-copy="{page_url}">Copy link</button></div>
  <div class="note-nav"><a href="community.html">All notes</a><a href="{nxt['fn']}">Next: {esc(nxt['title'])}</a></div></div></section>
</div>
{cta('Questions about your own data or IT setup?', 'Send me a message and I will point you in the right direction.')}'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": n['title'], "description": n['summary'],
           "author": {"@type": "Person", "name": "Alhaji Ibrahim Mehemoh", "url": BASE}, "mainEntityOfPage": page_url,
           "image": BASE + "images/og-image.jpg", "articleSection": n['category']}
    if n.get('date'):
        art["datePublished"] = n['date']
    page(n['fn'], n['title'] + ' | Alhaji Ibrahim Mehemoh', n['summary'], b, active='community.html', ld=art,
         og_type='article', crumbs=[('Notes', 'community.html'), (n['title'], None)],
         wa_text='Hello Alhaji, I read your note "%s" and have a question.' % n['title'])

# ------------------------------------------------------------------ 404
page('404.html', 'Page not found | Alhaji Ibrahim Mehemoh', 'This page does not exist.',
     '''<div class="wrap"><div class="page-head"><h1>That page does not exist</h1><p class="lede">The link may be old or mistyped. Try one of these instead.</p>
<div class="actions"><a class="btn btn-primary" href="index.html">Go to the home page</a><a class="btn" href="portfolio.html">See projects</a><a class="btn" href="contact.html">Contact me</a></div></div></div>''',
     noindex=True)

# ------------------------------------------------------------------ extra pages, feed, sitemap, PWA files
import extras
extras.build_all(NOTES, TODAY)
print('built', len(PAGES), 'indexed pages')
