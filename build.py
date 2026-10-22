#!/usr/bin/env python3
"""Generates the static site into ./  Run:  python3 build.py
Settings live in site_config.py, notes in notes.json, layout in layout.py, extra pages in extras.py."""
import datetime, json, os, re
import site_config as C
from layout import *
from art import cover, icon

TODAY = datetime.date.today().isoformat()


def partners():
    """Organisation logos used with permission, other employers as plain text."""
    logos = [('RHCI', 'Rural Health Care Initiative', 'images/brand/rhci-logo.webp', 116), ('SLIEPA', 'SLIEPA', 'images/brand/sliepa-logo.png', 92)]
    items = ''.join('<span class="chip chip-logo" title="%s"><img src="%s" alt="%s" height="38" style="height:38px;width:auto" loading="lazy"></span>' % (t, src, t) for _, t, src, w in logos)
    items += ''.join('<span class="chip">%s</span>' % n for n in ['SLPP', 'Growth Centre'])
    return '<div class="chips" aria-label="Organisations I have worked with"><span class="chips-label">Worked with</span>%s</div>' % items

def case_cover(slug):
    d = os.path.join(OUT, 'images', 'cases', slug)
    if os.path.isdir(d):
        f = sorted(x for x in os.listdir(d) if x.endswith('-800.webp'))
        if f:
            return '<img class="proj-shot" src="images/cases/%s/%s" alt="" loading="lazy">' % (slug, f[0])
    return cover(slug)


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
  <div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div>
  <section class="hero">
    <div class="hero-copy">
      <div class="hero-top"><picture class="hero-avatar"><source type="image/webp" srcset="images/profile-square.webp"><img src="images/profile.jpeg" width="96" height="96" alt=""></picture><p class="eyebrow"><span class="dot" aria-hidden="true"></span>Open to consulting, contracts and roles</p></div>
        <h1 data-i18n="hero.h1">I help health programmes turn <span class="mark">field data</span> into decisions.</h1>
      <p class="rotator" aria-live="off">I build <span class="rot-wrap"><span class="rot" data-words="Power BI dashboards|Survey123 forms|data quality checks|data systems|IT support|staff training">Power BI dashboards</span></span></p>
      <p class="lede" data-i18n="hero.lede">I am a Data Officer and M&amp;E specialist at Rural Health Care Initiative in Bo District, Sierra Leone. I design Survey123 forms, Power BI dashboards and data systems that nurses, programme managers and donors can read at a glance.</p>
      <div class="actions">
        <a class="btn btn-primary" href="portfolio.html" data-i18n="hero.projects">See projects</a>
        <a class="btn" href="contact.html" data-i18n="hero.contact">Contact me</a>
        <a class="text-link" href="{CV}" target="_blank" rel="noopener" data-i18n="hero.cv">Download CV (PDF)</a>
      </div>
      <p class="fact" data-i18n="hero.fact">Based in Bo, Sierra Leone. Open to roles, contracts and consulting, onsite or remote.</p>
    </div>
    <figure class="hero-art hero-photo">
      <picture><source type="image/webp" srcset="images/hero-portrait.webp"><img class="hero-portrait" src="images/hero-portrait.jpg" width="720" height="924" alt="Alhaji Ibrahim Mehemoh, Data Officer and M&amp;E specialist in Bo, Sierra Leone" fetchpriority="high"></picture>
      <span class="float-badge fb-1" aria-hidden="true"><b>Survey123</b> forms</span><span class="float-badge fb-2" aria-hidden="true"><b>Power BI</b> dashboards</span><span class="float-badge fb-3"><span class="live-dot" aria-hidden="true"></span>Bo, Sierra Leone <b><time id="boClock">GMT</time></b></span>
      <figcaption>Alhaji Ibrahim Mehemoh, Bo, Sierra Leone</figcaption>
    </figure>
  </section>
  <div class="marquee-row"><span class="chips-label">Tools I use</span><div class="marquee" aria-label="Tools I use"><div class="marquee-track"><ul><li>Survey123</li><li>XLSForm</li><li>Power BI</li><li>Excel</li><li>PostgreSQL</li><li>Flask</li><li>Google Apps Script</li><li>KoboToolbox</li><li>ODK</li><li>DHIS2</li><li>WordPress</li></ul><ul aria-hidden="true"><li>Survey123</li><li>XLSForm</li><li>Power BI</li><li>Excel</li><li>PostgreSQL</li><li>Flask</li><li>Google Apps Script</li><li>KoboToolbox</li><li>ODK</li><li>DHIS2</li><li>WordPress</li></ul></div></div></div>
  {partners()}
  @@HOME_STATS@@
  <div class="scroll-cue" aria-hidden="true"><span></span></div>
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

<section class="section band band-sheet">
  <div class="wrap">
    <div class="section-head"><h2>Selected work</h2><p>Case studies from my work at RHCI. The screens shown are design mockups with sample data; real programme data stays with the organisation. Ask me for a walkthrough.</p></div>
    @@HOME_WORK@@
  </div>
</section>

<section class="section band-sheet promo-band">
  <div class="wrap"><div class="promo promo-chart">
    <div class="promo-copy"><h2>See how a dashboard works</h2><p>Explore an interactive EPI dashboard built on sample data. Filter by facility and month, and switch between nurse, management and donor views.</p>
    <div class="actions"><a class="btn btn-primary" href="demo.html">Open the sample dashboard</a><a class="btn" href="resources.html">Free templates and checklists</a></div></div>
    <figure class="mini-dash" aria-label="Animated sample chart: monthly immunisation coverage rising from 42 to 86 percent, using made-up sample data">
      <figcaption><span><b>Penta 3 coverage</b> by month</span><span class="pill pill-design">Sample data</span></figcaption>
      <div class="mini-kpis"><div><span>Coverage</span><strong data-count="86">86</strong><em>%</em></div><div><span>Facilities</span><strong data-count="12">12</strong></div><div><span>On time</span><strong data-count="91">91</strong><em>%</em></div></div>
      <svg viewBox="0 0 400 180" aria-hidden="true"><g class="grid"><line x1="10" y1="150" x2="392" y2="150"/><line x1="10" y1="110" x2="392" y2="110"/><line x1="10" y1="70" x2="392" y2="70"/><line x1="10" y1="30" x2="392" y2="30"/></g><rect class="mb" style="--i:0" x="18" y="95" width="34" height="55" rx="6"/><rect class="mb" style="--i:1" x="66" y="78" width="34" height="72" rx="6"/><rect class="mb" style="--i:2" x="114" y="86" width="34" height="64" rx="6"/><rect class="mb" style="--i:3" x="162" y="68" width="34" height="82" rx="6"/><rect class="mb" style="--i:4" x="210" y="58" width="34" height="92" rx="6"/><rect class="mb" style="--i:5" x="258" y="62" width="34" height="88" rx="6"/><rect class="mb" style="--i:6" x="306" y="47" width="34" height="103" rx="6"/><rect class="mb" style="--i:7" x="354" y="38" width="34" height="112" rx="6"/><polyline class="mline" pathLength="1" points="35,81 83,64 131,72 179,54 227,44 275,48 323,33 371,24"/><circle class="md" style="--i:0" cx="35" cy="81" r="4"/><circle class="md" style="--i:1" cx="83" cy="64" r="4"/><circle class="md" style="--i:2" cx="131" cy="72" r="4"/><circle class="md" style="--i:3" cx="179" cy="54" r="4"/><circle class="md" style="--i:4" cx="227" cy="44" r="4"/><circle class="md" style="--i:5" cx="275" cy="48" r="4"/><circle class="md" style="--i:6" cx="323" cy="33" r="4"/><circle class="md" style="--i:7" cx="371" cy="24" r="4"/><text class="ml" x="35" y="170" text-anchor="middle">Jan</text><text class="ml" x="83" y="170" text-anchor="middle">Feb</text><text class="ml" x="131" y="170" text-anchor="middle">Mar</text><text class="ml" x="179" y="170" text-anchor="middle">Apr</text><text class="ml" x="227" y="170" text-anchor="middle">May</text><text class="ml" x="275" y="170" text-anchor="middle">Jun</text><text class="ml" x="323" y="170" text-anchor="middle">Jul</text><text class="ml" x="371" y="170" text-anchor="middle">Aug</text></svg>
    </figure>
  </div></div>
</section>


<section class="section laptops-band" id="tools-in-action">
  <div class="wrap">
    <div class="me-open" aria-hidden="true">
      <svg class="me-svg" viewBox="0 0 420 300">
        <defs><clipPath id="faceclip"><circle cx="210" cy="64" r="40"/></clipPath></defs>
        <ellipse cx="210" cy="290" rx="175" ry="9" class="me-shadow"/>
        <rect x="40" y="270" width="340" height="14" rx="4" class="me-desk"/>
        <path class="me-body" d="M112 272c0-92 40-160 98-160s98 68 98 160z"/>
        <path class="me-collar" d="M186 114l24 24 24-24"/>
        <image href="images/profile-square.webp" x="170" y="24" width="80" height="80" clip-path="url(#faceclip)" preserveAspectRatio="xMidYMid slice"/>
        <circle cx="210" cy="64" r="40" class="me-ring"/>
        <path class="me-arm me-arm-l" d="M132 168c-12 40 4 76 34 96"/>
        <path class="me-arm me-arm-r" d="M288 168c12 40-4 76-34 96"/>
        <g class="me-laptop">
          <g class="me-lid"><rect x="150" y="196" width="120" height="70" rx="6" class="lp-lid"/><rect x="157" y="203" width="106" height="56" rx="3" class="lp-glow"/>
            <g class="me-screen"><rect x="164" y="236" width="9" height="16" class="lp-bar"/><rect x="178" y="228" width="9" height="24" class="lp-bar"/><rect x="192" y="220" width="9" height="32" class="lp-bar"/><rect x="206" y="212" width="9" height="40" class="lp-bar am"/><rect x="222" y="212" width="34" height="5" rx="2.5" class="lp-line"/><rect x="222" y="222" width="24" height="4" rx="2" class="lp-line2"/></g></g>
          <rect x="138" y="264" width="144" height="8" rx="3" class="lp-sbase"/>
          <circle cx="162" cy="266" r="9" class="me-hand"/><circle cx="258" cy="266" r="9" class="me-hand"/>
        </g>
      </svg>
      <div class="me-bubble"><b>Let me show you how I work.</b><span>Illustration, with my real photo</span></div>
    </div>
    <div class="section-head sh-center"><h2>Tools in action</h2><p>Open a laptop to see the kind of work I do in each tool. All data shown is invented for illustration.</p></div>
    <div class="lp-tabs" role="tablist" aria-label="Choose a tool">
      <button role="tab" aria-selected="true" data-lp="pbi">Power BI</button><button role="tab" aria-selected="false" data-lp="xls">Excel</button><button role="tab" aria-selected="false" data-lp="py">Python</button>
    </div>
    <div class="lp-stage">
      <figure class="laptop is-active" data-lp="pbi" aria-label="Animated laptop showing a Power BI style dashboard with invented data">
        <div class="lp-screen"><div class="lp-display pbi">
          <div class="pbi-top"><span class="pbi-logo"></span><b>EPI Overview</b><em>Sample data</em></div>
          <div class="pbi-kpis"><div><span>Doses</span><b data-to="1284">0</b></div><div><span>Coverage</span><b data-to="74" data-suf="%">0</b></div><div><span>Facilities</span><b data-to="14">0</b></div></div>
          <div class="pbi-body"><div class="pbi-bars"><i style="--h:42%;--i:0"></i><i style="--h:55%;--i:1"></i><i style="--h:49%;--i:2"></i><i style="--h:63%;--i:3"></i><i style="--h:71%;--i:4"></i><i style="--h:68%;--i:5"></i><i style="--h:79%;--i:6"></i><i style="--h:86%;--i:7"></i></div>
          <svg class="pbi-donut" viewBox="0 0 42 42"><circle cx="21" cy="21" r="15.9" class="dn-bg"/><circle cx="21" cy="21" r="15.9" class="dn" pathLength="100"/><text x="21" y="24" text-anchor="middle">74%</text></svg></div>
        </div></div>
        <div class="lp-base"><span></span></div>
        <figcaption>Power BI: monthly coverage dashboard</figcaption>
      </figure>
      <figure class="laptop" data-lp="xls" aria-label="Animated laptop showing an Excel stock sheet with a formula being typed">
        <div class="lp-screen"><div class="lp-display xls">
          <div class="xls-top"><span class="xls-logo">X</span><b>stock-tracker.xlsx</b></div>
          <div class="xls-fx"><span>fx</span><code class="typer" data-text="=IF(I5<Settings!B3,&quot;REORDER&quot;,&quot;OK&quot;)"></code></div>
          <table class="xls-grid"><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th></tr>
            <tr><th>1</th><td>Item</td><td>Closing</td><td>Months</td><td>Status</td></tr>
            <tr><th>2</th><td>ORS</td><td>680</td><td>2.7</td><td><span class="xst ok">OK</span></td></tr>
            <tr><th>3</th><td>Paracetamol</td><td>800</td><td>1.0</td><td><span class="xst bad">REORDER</span></td></tr>
            <tr><th>4</th><td>Gloves</td><td>80</td><td>8.0</td><td><span class="xst warn">OVERSTOCK</span></td></tr>
            <tr><th>5</th><td>Zinc</td><td>120</td><td>1.5</td><td class="xls-sel"><span class="xst bad late">REORDER</span></td></tr></table>
        </div></div>
        <div class="lp-base"><span></span></div>
        <figcaption>Excel: stock tracker with automatic flags</figcaption>
      </figure>
      <figure class="laptop" data-lp="py" aria-label="Animated laptop showing Python code being typed and a chart appearing">
        <div class="lp-screen"><div class="lp-display py">
          <div class="py-top"><i></i><i></i><i></i><b>clean_epi.py</b></div>
          <pre class="py-code"><code class="typer" data-text="import pandas as pd
df = pd.read_csv(&quot;epi_export.csv&quot;)
df = df.drop_duplicates(&quot;record_id&quot;)
bad = df[df.dose3_date < df.dose1_date]
print(len(bad), &quot;dose order issues&quot;)
df.groupby(&quot;month&quot;).doses.sum().plot()"></code></pre>
          <div class="py-out"><span>&gt;&gt;&gt; 12 dose order issues</span><svg viewBox="0 0 120 40"><polyline points="0,34 17,30 34,31 51,22 68,18 85,20 102,10 120,6" class="py-line" pathLength="1"/></svg></div>
        </div></div>
        <div class="lp-base"><span></span></div>
        <figcaption>Python: cleaning an export and plotting it</figcaption>
      </figure>
    </div>
  </div>
</section>

@@HOME_SERVICES@@

<svg class="wave wave-top" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60V30C240 0 480 0 720 30s480 30 720 0v30z"/></svg>
<div class="mega" aria-hidden="true"><div class="mega-track"><span>Survey123 <i></i> Power BI <i></i> Data quality <i></i> M&amp;E reporting <i></i> Data systems <i></i> IT support <i></i> Training <i></i></span><span>Survey123 <i></i> Power BI <i></i> Data quality <i></i> M&amp;E reporting <i></i> Data systems <i></i> IT support <i></i> Training <i></i></span></div></div>

<section class="section band band-ink">
  <div class="wrap">
    <div class="section-head"><h2>How I work</h2><p>Four steps, the same on every project, so you always know what happens next.</p></div>
    <ol class="steps steps-line">
      <li><h3>Understand the need</h3><p>Who reads the report, and what decision does it support?</p></li>
      <li><h3>Design the data</h3><p>Forms, fields and checks that match how the field team really works.</p></li>
      <li><h3>Build and test</h3><p>Validate against real exports before anyone relies on the result.</p></li>
      <li><h3>Hand over and train</h3><p>Clear documentation, so your team can run it without me.</p></li>
    </ol>
  </div>
</section>

@@HOME_RESOURCES@@

@@HOME_NOTES@@

<section class="section band band-tint">
  <div class="wrap">
    <div class="section-head"><h2>What colleagues say</h2></div>
    <div class="quotes">
      <figure class="quote" style="margin:0"><p>Alhaji has a remarkable ability to turn complex data challenges into simple, workable systems. His Excel dashboards transformed how we track and report health program data every month.</p><footer><span class="q-av" aria-hidden="true">MH</span><span>Moses Hopanda Carter, Director of Projects, RHCI, Tikonko</span></footer></figure>
      <figure class="quote" style="margin:0"><p>Reliable, fast, and always willing to go the extra mile. Alhaji kept our IT systems running smoothly and trained staff effectively during a critical period for our organization.</p><footer><span class="q-av" aria-hidden="true">FA</span><span>Foday Abdulai, District Secretary General, SLPP, Bo District</span></footer></figure>
      <figure class="quote" style="margin:0"><p>His networking setup gave us stable Wi-Fi across the entire office floor, something we struggled with for months. Professional, well-documented, and completed on time.</p><footer><span class="q-av" aria-hidden="true">IT</span><span>IT client, Bo (office network setup)</span></footer></figure>
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


# ------------------------------------------------------------------ ABOUT
about_story = [
    ('2015', 'Where I started', 'I trained in computer software, hardware and networking at the Growth Centre Computer Training Institute in Bo. That year I also started my own small data and IT business, which still runs from an office in the Growth Centre compound.'),
    ('2016', 'Learning by teaching', 'As an ICT tutor and internet cafe attendant I taught Microsoft Office and fixed hardware and network problems every day. Teaching taught me to explain technical things in plain words.'),
    ('2022', 'Bigger systems', 'As IT and Data Officer for SLPP in Bo District and then Assistant IT Manager at SLIEPA in Freetown, I worked on membership databases, analysis, agency-wide infrastructure, helpdesk support, cybersecurity and staff training.'),
    ('2024', 'Health data', 'At Rural Health Care Initiative I manage immunisation, home visit and malaria programme data, build the Survey123 forms field teams use, and supervise a contract Data Assistant.'),
]
about_timeline = [
    ('Oct 2024 to present', 'Evaluator and Data Officer', 'Rural Health Care Initiative (RHCI), Tikonko', 'Health data systems, CHW database management, dashboards, mobile data collection and M&amp;E reporting. Reported a 25% accuracy improvement in programme data.', 'now'),
    ('Sep 2023 to Oct 2024', 'Assistant IT Manager', 'SLIEPA, Freetown', 'Agency-wide IT infrastructure, helpdesk, cybersecurity measures and staff ICT training. Reported 99% system availability.', ''),
    ('Jan 2022 to Sep 2023', 'IT and Data Officer', 'SLPP, Bo District', 'Centralised membership databases, data analysis and digital campaign management. Reported a 30% increase in online engagement.', ''),
    ('2017', 'Registrar; Exhibition and Distribution Officer', 'NEC and NCRA', 'Short-term registration, exhibition and distribution roles.', ''),
    ('2016 to 2021', 'ICT Tutor and Internet Cafe Attendant', 'Growth Centre, Bo', 'Taught Microsoft Office to more than 200 students and handled hardware and network troubleshooting.', ''),
    ('Sep 2015 to present', 'Independent data and IT consultant', 'Own business, Growth Centre compound, Bo', 'Data, IT support and training for individuals, offices and organisations, alongside my employed roles.', 'side'),
]
about_skills = [
    ('chart', 'Data and M&amp;E', ['Power BI', 'Excel', 'Survey123', 'XLSForm', 'Data cleaning', 'Data quality checks', 'Indicator reporting', 'Logframes']),
    ('db', 'Systems', ['PostgreSQL', 'Flask', 'Google Apps Script', 'Google Sheets', 'HTML and JavaScript', 'Progressive web apps', 'System design']),
    ('wifi', 'IT and networks', ['LAN and Wi-Fi', 'Hardware repair', 'Windows', 'Backups', 'Basic security', 'WordPress', 'Helpdesk']),
    ('teach', 'Training and communication', ['Staff ICT training', 'Data skills training', 'Reports', 'Presentations', 'Documentation', 'English and Krio']),
]
about_principles = [
    ('Solve a real problem', 'Technology should fix something people can name, like late reports or lost files.'),
    ('Keep it simple', 'The best tool is one the people using it every day can understand.'),
    ('Support after launch', 'Handover, training and follow-up matter as much as the build.'),
    ('Protect people', 'Collect only what is needed and keep personal data out of shared files.'),
]
story_html = ''.join('<li><span class="st-y">%s</span><h3>%s</h3><p>%s</p></li>' % (y, esc(t), esc(d)) for y, t, d in about_story)
tl_html = ''.join('<li class="%s"><span class="when">%s</span><div><h3>%s</h3><p class="tl-org">%s</p><p>%s</p></div></li>' % (c, w, r, o, d) for w, r, o, d, c in about_timeline)
sk_html = ''.join('<div class="sk-card">%s<h3>%s</h3><ul>%s</ul></div>' % (icon(ic), t, ''.join('<li>%s</li>' % esc(x) for x in xs)) for ic, t, xs in about_skills)
pr_html = ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in about_principles)
about_body = f'''<div class="wrap">
  <header class="about-hero">
    <div class="ah-text">
      <p class="eyebrow"><span class="dot" aria-hidden="true"></span>Open to roles, contracts and consulting</p>
      <h1>Hi, I am Alhaji.</h1>
      <p class="lede">I am a Data Officer and MEL specialist in Bo, Sierra Leone. I help health programmes turn field data into decisions, and I keep the technology behind that data working.</p>
      <ul class="trust"><li>Based in Bo</li><li>In IT since 2015</li><li>Health data since 2024</li><li>English and Krio</li></ul>
      <div class="actions"><a class="btn btn-primary" href="{CV}" target="_blank" rel="noopener">Download CV (PDF)</a><a class="btn" href="contact.html">Contact me</a>{('<a class="text-link" href="' + esc(C.LINKEDIN) + '" target="_blank" rel="me noopener">LinkedIn</a>') if C.LINKEDIN else ''}</div>
    </div>
    <figure class="ah-photo">
      <picture><source type="image/webp" srcset="images/profile-square.webp"><img src="images/profile.jpeg" width="640" height="640" alt="Portrait of Alhaji Ibrahim Mehemoh"></picture>
      <span class="float-badge fb-1" aria-hidden="true"><b>MEL</b> specialist</span>
      <span class="float-badge fb-2" aria-hidden="true"><b>RHCI</b> Data Officer</span>
    </figure>
  </header>
  <div class="glance about-glance">
    <div class="gl"><b>2015</b><span>first diploma and my own small business</span></div>
    <div class="gl"><b>3</b><span>programme data areas at RHCI: EPI, home visits and malaria</span></div>
    <div class="gl"><b>10</b><span>case studies on this site</span></div>
    <div class="gl"><b>17</b><span>free resources I made for others</span></div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>My story</h2><p>From a computer training centre in Bo to managing health programme data.</p></div>
    <ol class="story">{story_html}</ol>
    <aside class="callout c-quote about-quote"><span class="callout-l">What health taught me</span><p>A good system is one that field staff actually use and managers actually trust.</p></aside>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Experience</h2></div>
    <ul class="timeline about-tl">{tl_html}</ul>
    <p class="small muted" style="margin-top:1rem">Percentages are figures reported in those roles.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Skills and tools</h2></div>
    <div class="sk-grid">{sk_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap about-two">
    <div>
      <div class="section-head"><h2>How I work</h2></div>
      <ul class="principles">{pr_html}</ul>
    </div>
    <div>
      <div class="section-head"><h2>Education</h2></div>
      <ol class="jt edu">
        <li><span class="jt-when">In progress</span><b>BSc Computer Science</b><em>Currently studying, with a focus on maths for data and systems work</em></li>
        <li><span class="jt-when">2017 to 2019</span><b>Diploma in Networking</b><em>Growth Centre Computer Training Institute, Bo</em></li>
        <li><span class="jt-when">2015 to 2017</span><b>Diploma in Computer Hardware</b><em>Growth Centre Computer Training Institute, Bo</em></li>
        <li><span class="jt-when">2015 to 2016</span><b>Diploma in Computer Software</b><em>Growth Centre Computer Training Institute, Bo</em></li>
        <li><span class="jt-when">2011 to 2015</span><b>WASSCE</b><em>Secondary school</em></li>
      </ol>
    </div>
  </div>
</section>

{certs_section()}

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Organisations I have worked with</h2></div>
    <div class="about-orgs">{partners().replace('<span class="chip">SLPP</span><span class="chip">Growth Centre</span>', '<span class="chip">SLPP</span><span class="chip">NEC</span><span class="chip">NCRA</span><span class="chip">Growth Centre</span>')}</div>
  </div>
</section>

<section class="section-tight"><div class="wrap photo-strip">
  <figure class="ps ps-a"><img src="images/work/dashboard-review-800.webp" alt="Alhaji reviewing a dashboard at his desk" loading="lazy"></figure>
  <figure class="ps ps-b"><img src="images/work/navy-suit-portrait-800.webp" alt="Alhaji Ibrahim Mehemoh in a navy suit, outdoors" loading="lazy"></figure>
  <figure class="ps ps-c"><img src="images/work/office-desk-800.webp" alt="Alhaji working at an office computer" loading="lazy"></figure>
  <figure class="ps ps-d">{picture("images/cover.jpeg", "A team meeting in a busy room with laptops, documents and a projector", 1080, 810, "")}</figure>
</div></section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Beyond work</h2></div>
    <ul class="beyond">
      <li>{icon('tool')}<b>Electronics</b><span>Exploring circuits and Arduino projects.</span></li>
      <li>{icon('teach')}<b>Always learning</b><span>Building my maths for computer science, one evening at a time.</span></li>
      <li>{icon('web')}<b>Sharing knowledge</b><span>Writing notes and free templates for anyone learning data and IT.</span></li>
      <li>{icon('chart')}<b>Football</b><span>Following the game.</span></li>
    </ul>
  </div>
</section>

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


SVC_ICON = {'Dashboards and reports': 'chart', 'Survey and form design': 'form', 'Data quality audits': 'check',
            'M&amp;E reporting': 'report', 'Data systems': 'db', 'Training': 'teach', 'Technical support and hardware': 'tool',
            'Networking and internet': 'wifi', 'Web and digital': 'web', 'Security and backups': 'lock', 'Office and NGO IT support': 'office'}


def row2(h, p):
    ic = icon(SVC_ICON[h]) if h in SVC_ICON else ''
    return f'<li class="reg-row two svc-row">{ic}<h3>{h}</h3><p>{p}</p></li>'

from services_content import SERVICES, AUDIENCES, FINDER, PRICE_FACTORS
import notes_render as NR_S


def svc_card(sv):
    gets = ''.join('<li>%s</li>' % esc(g) for g in sv['gets'])
    href, label = sv['proof']
    q = 'request.html?service=' + sv['form'].replace(' ', '+').replace('&', '%26')
    return f"""<article class="svc-card" id="{sv['key']}" data-type="{sv['group']}">
  <div class="svc-top">{icon(sv['icon'])}<span class="svc-grp">{'Data and M&amp;E' if sv['group'] == 'data' else 'IT support'}</span></div>
  <h3><a class="svc-title" href="service-{sv['key']}.html">{esc(sv['title'])}</a></h3>
  <p class="svc-lead">{esc(sv['lead'])}</p>
  <p class="svc-l">What you get</p>
  <ul class="svc-gets">{gets}</ul>
  <p class="svc-fit"><b>Good for:</b> {esc(sv['fit'])}</p>
  <div class="svc-foot"><a class="btn btn-primary" href="{q}">Ask about this</a><a class="text-link" href="service-{sv['key']}.html">Full details</a></div>
  <p class="svc-proof">Proof: <a href="{href}">{esc(label)}</a></p>
</article>"""


svc_cards = ''.join(svc_card(sv) for sv in SERVICES)

SVC_BY = {sv['key']: sv for sv in SERVICES}
finder_opts = ''.join('<button type="button" class="fd-opt" data-svc="%s"><span>%s</span></button>' % (k, esc(t)) for t, k in FINDER)
finder_res = ''.join('<div class="fd-res" data-res="%s" hidden>%s<div><p class="fd-k">I recommend</p><h3>%s</h3><p>%s</p><div class="actions"><a class="btn btn-primary" href="service-%s.html">See the details</a><a class="btn" href="request.html?service=%s">Ask about this</a></div></div></div>' % (
    sv['key'], icon(sv['icon']), esc(sv['title']), esc(sv['lead']), sv['key'], sv['form'].replace(' ', '+').replace('&', '%26')) for sv in SERVICES)
price_html = ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in PRICE_FACTORS)
aud = ''.join('<li><span class="aud-art">%s</span><b>%s</b></li>' % (NR_S.hero_art(m), esc(a)) for a, m in AUDIENCES)
jump = ''.join('<a href="service-%s.html">%s%s</a>' % (sv['key'], icon(sv['icon']), esc(sv['title'])) for sv in SERVICES)
services_body = f'''<div class="wrap">
  <div class="page-head svc-hero">
    <div>
      <h1>Services</h1>
      <p class="lede">Data and M&amp;E work for health programmes and NGOs, plus practical IT support for offices, clinics and schools in Bo and across Sierra Leone.</p>
      <div class="actions"><a class="btn btn-primary" href="request.html">Request a quote</a><a class="btn" href="{WA}" target="_blank" rel="noopener">WhatsApp me</a></div>
      <ul class="trust"><li>Based in Bo</li><li>Onsite in Bo, remote nationwide</li><li>English and Krio</li><li>Quick replies on WhatsApp</li></ul>
    </div>
    <nav class="svc-jump" aria-label="Jump to a service"><p>Jump to a service</p>{jump}</nav>
  </div>
</div>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Who I work with</h2></div>
    <ul class="aud">{aud}</ul>
  </div>
</section>
<section class="section finder-band" id="finder">
  <div class="wrap">
    <div class="section-head"><h2>Which service do I need?</h2><p>Pick the sentence that sounds most like you.</p></div>
    <div class="finder"><div class="fd-opts" role="group" aria-label="Choose what sounds like you">{finder_opts}</div><div class="fd-out" aria-live="polite"><div class="fd-empty"><p>Your recommendation appears here.</p></div>{finder_res}</div></div>
  </div>
</section>
<section class="section" id="all-services">
  <div class="wrap">
    <div class="section-head"><h2>What I can do for you</h2><p>Data and M&amp;E work is priced by scope: send me your need and I will reply with a plan and a quote. IT support has fixed packages below.</p></div>
    <div class="filters" role="group" aria-label="Filter services"><button type="button" class="filter is-active" data-filter="all" aria-pressed="true">All 11</button><button type="button" class="filter" data-filter="data" aria-pressed="false">Data and M&amp;E</button><button type="button" class="filter" data-filter="it" aria-pressed="false">IT support</button></div>
    <p class="small muted" id="filterCount" data-noun="service" role="status" aria-live="polite"></p>
    <div class="svc-grid" data-filter-target>{svc_cards}</div>
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
    <div class="section-head"><h2>Which package fits?</h2></div>
    <div class="ntable cmp"><table><thead><tr><th scope="col"></th><th scope="col">Starter</th><th scope="col" class="cmp-hi">Standard</th><th scope="col">Premium</th></tr></thead><tbody>
      <tr><th scope="row">Best for</th><td>A one-off fix</td><td class="cmp-hi">Setting up or improving an office</td><td>Ongoing help every month</td></tr>
      <tr><th scope="row">How it is priced</th><td>Le 250 to Le 600</td><td class="cmp-hi">Le 800 to Le 2,500</td><td>Le 3,000+ per month contract</td></tr>
      <tr><th scope="row">Typical work</th><td>Setup, troubleshooting, printers, clean-up</td><td class="cmp-hi">Wi-Fi and routers, staff PC setup, network design, Excel templates</td><td>Ongoing support, backups and security checks, systems and training, priority response</td></tr>
    </tbody></table></div>
    <div class="section-head" id="pricing" style="margin-top:3rem;scroll-margin-top:6rem"><h2>What affects the price</h2><p>Data and M&amp;E work is quoted after a short conversation. These are the things that make the biggest difference.</p></div>
    <ul class="pf">{price_html}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>How a project runs</h2><p>Clear steps, so you always know what happens next and what it will cost.</p></div>
    <ol class="steps steps-line">
      <li><h3>Assess</h3><p>We agree what you need, who will use it and the deadline.</p></li>
      <li><h3>Design</h3><p>I propose the form, system or setup with a fixed scope and quote.</p></li>
      <li><h3>Build and test</h3><p>I deliver it and test it with your real data or equipment.</p></li>
      <li><h3>Hand over</h3><p>Documentation and training, so your team can keep it running.</p></li>
    </ol>
  </div>
</section>
<section class="section">
  <div class="wrap svc-split">
    <div class="sp-card"><span class="sp-k">Remote</span><h3>Across Sierra Leone</h3><ul class="bullets"><li>Dashboards, forms, data audits and reports</li><li>Calls and screen sharing for training</li><li>Files shared securely, never in group chats</li></ul></div>
    <div class="sp-card sp-on"><span class="sp-k">Onsite</span><h3>In Bo and nearby</h3><ul class="bullets"><li>Networks, hardware and office setup</li><li>Hands-on staff training</li><li>Assessments and maintenance visits</li></ul></div>
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

# ------------------------------------------------------------------ PROJECTS (portfolio + case studies)
from cases_content import CASES
import notes_render as NR_C

STATUS_PILL = {'Built': 'pill-ok', 'Completed': 'pill-ok', 'In progress': 'pill-dev', 'In development': 'pill-dev', 'In design': 'pill-design', 'Designed': 'pill-done'}


def video_embed(url):
    m = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{6,})', url)
    if m:
        return '<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/%s" title="Video" loading="lazy" allowfullscreen></iframe></div>' % m.group(1)
    if url.lower().endswith('.mp4'):
        return '<video class="video" controls preload="none" src="%s"></video>' % esc(url)
    return '<p><a class="btn" href="%s" target="_blank" rel="noopener">Watch the video</a></p>' % esc(url)


def cover_img(c, size='800'):
    """Mockup image for a case if one exists, otherwise the illustration."""
    key = c.get('cover')
    if not key:
        d = os.path.join(OUT, 'images', 'cases', c['slug'])
        if os.path.isdir(d):
            f = sorted(x for x in os.listdir(d) if x.endswith('-800.webp'))
            if f:
                key = c['slug'] + '/' + f[0][:-9]
    if key:
        return '<img class="proj-shot" src="images/cases/%s%s.webp" alt="" loading="lazy">' % (key, '-800' if size == '800' else ''), True
    if c.get('motif'):
        return NR_C.hero_art(c['motif']), False
    return cover(c['slug'] if c['slug'] != 'case-staff-id-cards' else 'case-chw-card-studio'), False


def status_pill(c):
    return '<span class="pill %s">%s</span>' % (STATUS_PILL.get(c['status'], 'pill-done'), esc(c['status'])) if c.get('status') else ''


def stepper(c):
    if not c.get('status'):
        return ''
    labels = ['Designed', c['status'] if c['stage'] == 2 else 'In development', c['status'] if c['stage'] == 3 else 'Built']
    out = ''
    for n, l in enumerate(labels, 1):
        cls = 'done' if n < c['stage'] or (n == c['stage'] and c['stage'] == 3) else ('now' if n == c['stage'] else '')
        out += '<li class="%s"><span></span>%s</li>' % (cls, esc(l))
    return '<ol class="stepper" aria-label="Project status: %s">%s</ol>' % (esc(c['status']), out)


def proj_card(c, featured=False):
    img, real = cover_img(c)
    tags = ' &middot; '.join(esc(t) for t in c['tools'][:3])
    mock = ('<span class="mock-tag">%s</span>' % ('Screenshot' if c.get('screens_real') else 'Design mockup')) if real else ''
    return f'''<a class="proj-card{' proj-featured' if featured else ''}" data-type="{c['types']}" href="{c['slug']}.html"><div class="proj-art">{img}{mock}</div><div class="proj-body"><div class="proj-meta">{status_pill(c)}<span class="proj-tags">{tags}</span></div><h3>{esc(c['title'])}</h3><p>{esc(c['short'])}</p>{('<ul class="proj-glance">' + ''.join('<li><b>%s</b>%s</li>' % (esc(a), esc(b)) for a, b in c['glance'][:3]) + '</ul>') if featured else ''}<span class="tile-link">Read the case study</span></div></a>'''


from cases_content import MORE_WORK
more_cards = ''.join('<div class="more-card">%s<span class="mc-k">%s</span><h3>%s</h3><p>%s</p></div>' % (icon(ic), esc(k), esc(t), esc(d)) for k, t, d, ic in MORE_WORK)
feat = CASES[0]
cards = proj_card(feat, True) + ''.join(proj_card(c) for c in CASES[1:])
n_built = sum(1 for c in CASES if c.get('status') in ('Built', 'Completed'))
portfolio_body = f'''<div class="wrap">
  <div class="page-head proj-hero"><h1>Projects</h1><p class="lede">Health data, M&amp;E and systems work from my role at Rural Health Care Initiative, plus earlier IT projects. Screens shown are design mockups with sample data; real programme data stays with the organisation.</p>
  <ul class="res-stats"><li><b>{len(CASES)}</b> case studies</li><li><b>{n_built}</b> built or completed</li><li><b>{len(MORE_WORK)}</b> more pieces of work</li><li><b>1,000+</b> health workers in scope</li></ul></div>
</div>
<section class="section" id="projects">
  <div class="wrap">
    <div class="section-head"><h2>Case studies</h2><p>Each one explains the problem, the approach, what was built and how quality is protected.</p></div>
    <div class="filters" role="group" aria-label="Filter projects by type"><button type="button" class="filter is-active" data-filter="all" aria-pressed="true">All</button><button type="button" class="filter" data-filter="health" aria-pressed="false">Health data</button><button type="button" class="filter" data-filter="systems" aria-pressed="false">Systems</button><button type="button" class="filter" data-filter="it" aria-pressed="false">IT and field tools</button></div>
    <p class="small muted" id="filterCount" role="status" aria-live="polite"></p>
    <div class="proj-grid" data-filter-target>{cards}
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

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>More work</h2><p>Smaller pieces from my day-to-day work in data, M&amp;E and operations.</p></div>
    <div class="more-grid">{more_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>How a project runs</h2><p>The same steps on every project, so you always know what happens next.</p></div>
    <ol class="steps steps-line">
      <li><h3>Understand the need</h3><p>Who reads the result, and what decision does it support?</p></li>
      <li><h3>Design the data</h3><p>Forms, fields, tables and checks that match how the team really works.</p></li>
      <li><h3>Build and test</h3><p>Validate against real exports before anyone relies on the result.</p></li>
      <li><h3>Hand over and train</h3><p>Clear documentation, so your team can run it without me.</p></li>
    </ol>
  </div>
</section>
{cta('Want something similar for your team?', 'Tell me what you track today and what you need to report. I will suggest the simplest system that works.')}'''
page('portfolio.html', 'Projects | Alhaji Ibrahim Mehemoh',
     'Health data and M&E case studies: an EPI Power BI dashboard, an EPI data quality audit, Survey123 field tools, CHW credential cards, staff ID cards and a data management system, from RHCI in Bo, Sierra Leone.',
     portfolio_body, crumbs=[('Projects', None)])


SHOT_CAPTIONS = {
    '01-management-overview': 'Management overview: encounters by month, facility and activity',
    '02-facility-and-nurse-performance': 'Facility and nurse performance: activity delivery and reporting completeness',
    '03-monthly-performance': 'Monthly performance: trends and previous-month comparison',
    '04-data-quality-review': 'Data quality review: flags by issue type and a priority review queue',
    '01-mobile-registration-form': 'Mobile registration form, designed to work offline',
    '02-qr-autofill-follow-up': 'Follow-up visit: scanning a QR code fills in the record',
    '03-offline-follow-up-screen': 'Follow-up screen: scan, verify, record',
    '04-offline-stock-dashboard': 'Offline stock dashboard with reorder flags',
    '01-card-and-qr-verification': 'Sample credential card and the QR verification page',
    '01-patient-registration-workspace': 'Registration workspace with a built-in data quality checklist',
    '01-home': 'Home page with the live Bo clock and project showcase',
    '02-free-resources': 'Free resources library with previews and filters',
    '03-note-page': 'A note with contents, key points and diagrams',
    '04-dark-mode-notes': 'Notes in dark mode',
}


def case_shots(slug, real=False):
    """Design mockups in images/cases/<slug>/ (full size plus -800 thumbnails) appear here automatically."""
    d = os.path.join(OUT, 'images', 'cases', slug)
    if not os.path.isdir(d):
        return ''
    files = sorted(f for f in os.listdir(d) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and '-800.' not in f)
    if not files:
        return ''
    figs = ''
    for f in files:
        base = os.path.splitext(f)[0]
        thumb = base + '-800.webp' if os.path.exists(os.path.join(d, base + '-800.webp')) else f
        label = SHOT_CAPTIONS.get(base, base.replace('-', ' '))
        tall = ' shot-tall' if 'form' in base or 'follow-up' in base else ''
        figs += ('<figure class="shot%s"><button type="button" class="shot-btn" data-full="images/cases/%s/%s" aria-label="Enlarge: %s">'
                 '<img src="images/cases/%s/%s" alt="Design mockup: %s" loading="lazy"><span class="shot-zoom" aria-hidden="true"></span></button>'
                 '<figcaption>%s</figcaption></figure>') % (tall, slug, f, esc(label), slug, thumb, esc(label), esc(label))
    if real:
        figs = figs.replace('alt="Design mockup: ', 'alt="Screenshot: ')
        return '<section class="section-tight case-gallery"><div class="gallery-head"><h2>Screenshots</h2><p class="mock-note">Screenshots of the live site.</p></div><div class="shots">%s</div></section>' % figs
    return ('<section class="section-tight case-gallery"><div class="gallery-head"><h2>All design mockups</h2>'
            '<p class="mock-note"><span class="pill pill-design">Sample data</span> These screens show the design using invented, anonymised data. Real programme data stays with RHCI.</p></div>'
            '<div class="shots">%s</div></section>') % figs


def render_case_body(c):
    def shot(m):
        name, _, cap = m.group(1).partition(' | ')
        return '::photo images/cases/%s/%s.webp | %s | Design mockup: %s' % (c['slug'], name.strip(), cap.strip(), cap.strip())
    body = re.sub(r'^::shot (.+)$', shot, c['body'], flags=re.M)
    return NR_C.render(body)


RES_ALL = {r['file']: r for r in json.load(open(os.path.join(OUT, 'downloads', 'resources.json')))['items']}
NOTE_TITLES = {n['slug']: n for n in json.load(open(os.path.join(OUT, 'notes.json'), encoding='utf-8'))}

for idx, c in enumerate(CASES):
    nxt, prv = CASES[(idx + 1) % len(CASES)], CASES[idx - 1]
    html_body, toc = render_case_body(c)
    img, real = cover_img(c, 'full')
    cap = 'Screenshot of the live site' if c.get('screens_real') else '<span class="pill pill-design">Sample data</span> Design mockup'
    hero_art = ('<figure class="case-cover"><div class="browser"><span class="b-dots"><i></i><i></i><i></i></span>%s</div><figcaption>%s</figcaption></figure>' % (img, cap)) if real else (
        '<div class="case-art">%s<p class="art-note">Illustration, not real data</p></div>' % img)
    glance = ''.join('<div class="gl"><b>%s</b><span>%s</span></div>' % (esc(a), esc(b)) for a, b in c['glance'])
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(v)) for k, v in c['facts'])
    tools = ''.join('<li>%s</li>' % esc(t) for t in c['tools'])
    toc_html = ''.join('<li><a href="#%s">%s</a></li>' % (a, esc(t)) for a, t in toc)
    notes_rel = ''.join('<a class="rn" href="%s.html"><span class="rn-art">%s</span><b>%s</b></a>' % (s_, NR_C.hero_art(NOTE_TITLES[s_].get('motif', 'checks')), esc(NOTE_TITLES[s_]['title'])) for s_ in c.get('notes', []) if s_ in NOTE_TITLES)
    res_rel = ''.join('<a class="rel-card" href="downloads/%s" download><img src="images/resources/%s.webp" alt="" width="720" height="562" loading="lazy"><span><span class="ftype ft-%s">%s</span><b>%s</b><em>%s</em></span></a>' % (
        f, RES_ALL[f]['slug'], {'PDF': 'pdf', 'Excel': 'xls', 'XLSForm': 'form'}[RES_ALL[f]['type']], RES_ALL[f]['type'], esc(RES_ALL[f]['title']), RES_ALL[f]['size']) for f in c.get('resources', []) if f in RES_ALL)
    shots = case_shots(c['slug'], c.get('screens_real', False))
    video = C.CASE_VIDEOS.get(c['slug'])
    video_html = '<section class="section-tight"><h2>Walkthrough video</h2>%s</section>' % video_embed(video) if video else ''
    result = C.CASE_RESULTS.get(c['slug']) if hasattr(C, 'CASE_RESULTS') else None
    result_html = '<div class="result"><strong>Result</strong><p>%s</p></div>' % esc(result) if result else ''
    wa = esc(wa_link('Hello Alhaji, I read your %s case study and would like to talk.' % c['title']))
    body = f'''<article class="case">
<div class="wrap">
  <header class="case-hero">
    <div class="case-hero-text">
      <p class="crumb"><a href="portfolio.html">Projects</a></p>
      <div class="case-status">{status_pill(c)}<span class="case-org">{esc(c['facts'][0][1].replace('Rural Health Care Initiative (RHCI), Bo District', 'RHCI, Bo District'))}</span></div>
      <h1>{esc(c['title'])}</h1>
      <p class="lede">{esc(c['lede'])}</p>
      <ul class="tool-chips">{tools}</ul>
      <div class="actions"><a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">Ask for a walkthrough</a><a class="btn" href="#{toc[0][0] if toc else ''}">Read the case study</a></div>
    </div>
    {hero_art}
  </header>
  <div class="glance">{glance}</div>
  <div class="case-layout">
    <aside class="case-side">
      <div class="case-facts"><p class="cf-l">Project facts</p><dl>{facts}</dl>{('<p class="cf-l">Status</p>' + stepper(c)) if c.get('status') else ''}</div>
      <nav class="note-toc"><p>On this page</p><ol>{toc_html}</ol></nav>
    </aside>
    <div class="case-main">
      {result_html}
      <div class="note-body case-body">{html_body}</div>
    </div>
  </div>
  {shots}
  {video_html}
  {('<section class="case-more"><h2>Read more on this topic</h2><div class="rn-grid">' + notes_rel + '</div></section>') if notes_rel else ''}
  {('<section class="note-rel case-res"><h2>Free tools from this work</h2><div class="rel-grid">' + res_rel + '</div></section>') if res_rel else ''}
  <nav class="note-pn" aria-label="More case studies">
    <a class="pn-card" href="{prv['slug']}.html"><span class="pn-l">Previous case study</span><span class="pn-art">{cover_img(prv)[0]}</span><b>{esc(prv['title'])}</b></a>
    <a class="pn-card" href="{nxt['slug']}.html"><span class="pn-l">Next case study</span><span class="pn-art">{cover_img(nxt)[0]}</span><b>{esc(nxt['title'])}</b></a>
  </nav>
</div>
</article>
{cta()}'''
    page(c['slug'] + '.html', c['title'] + ' | Case study | Alhaji Ibrahim Mehemoh', c['desc'], body, active='portfolio.html',
         crumbs=[('Projects', 'portfolio.html'), (c['title'], None)],
         wa_text='Hello Alhaji, I read your %s case study and would like to talk.' % c['title'])


# ------------------------------------------------------------------ HIRE
hire_roles = [
    ('chart', 'M&amp;E or Data Officer', 'Indicator tracking, data quality, reporting to management and donors.', 'case-epi-data-audit.html', 'EPI data quality audit'),
    ('report', 'Data Analyst', 'Cleaning, analysis and Power BI or Excel dashboards for several audiences.', 'case-epi-dashboard.html', 'EPI reporting dashboard'),
    ('form', 'Survey and data collection specialist', 'XLSForm design, field testing, collector training and supervision.', 'case-survey123.html', 'Survey123 forms and field tools'),
    ('db', 'Systems administrator', 'Databases, web tools, user access and documentation.', 'case-dms.html', 'Data Management System'),
    ('tool', 'IT support and help desk', 'Hardware, software, accounts, backups and user training.', 'service-hardware.html', 'Technical support service'),
    ('web', 'Web administrator', 'Fast, maintained websites, domains, hosting and email.', 'case-this-website.html', 'This website'),
    ('wifi', 'Network administrator', 'LAN and Wi-Fi design, routers, cabling and monitoring.', 'service-network.html', 'Networking service'),
]
hire_bring = [
    ('From form to board report', 'I have run real programme data for a health NGO end to end: the field form, the cleaning, the dashboard and the report management reads.'),
    ('Data you can defend', 'Every correction is logged and every figure is checked against the source before anyone relies on it.'),
    ('IT background behind the data', 'Years of hardware, networking and helpdesk work mean I understand the equipment and connectivity the data depends on.'),
    ('Teams that can carry on without me', 'Clear documentation and hands-on training for non-technical staff, in English and Krio.'),
]
hire_faq = [
    ('Are you available for full-time roles?', 'Yes. I am open to full-time roles, fixed-term contracts and consulting. Tell me about the role and we can discuss timing.'),
    ('Can you work remotely?', 'Yes. Data, dashboard, form and reporting work can be done remotely. I am based in Bo and can work onsite there and nearby.'),
    ('Can we see examples of your work?', 'Yes. The case studies on this site show the approach, with design mockups using sample data. I can walk you through real work on a call where the data owner allows it.'),
    ('Do you have references?', 'Yes. I can share references on request.'),
    ('Which languages do you work in?', 'English and Krio.'),
]
roles_html = ''.join('<article class="role-card">%s<h3>%s</h3><p>%s</p><a class="text-link" href="%s">See: %s</a></article>' % (icon(ic), t, esc(d), h, esc(l)) for ic, t, d, h, l in hire_roles)
bring_html = ''.join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in hire_bring)
hfaq_html = ''.join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (esc(a), esc(b)) for a, b in hire_faq)
hire_wa = esc(wa_link('Hello Alhaji, I have a role I would like to discuss with you.'))
hire_body = f'''<div class="wrap">
  <header class="about-hero hire-hero">
    <div class="ah-text">
      <p class="eyebrow"><span class="dot" aria-hidden="true"></span>Available for roles, contracts and consulting</p>
      <h1>Hire a data and MEL specialist who also knows the tech.</h1>
      <p class="lede">I am a Data Officer at Rural Health Care Initiative in Bo, Sierra Leone, with a background in IT since 2015. I am open to full-time, contract and consulting work, onsite in Bo or remote.</p>
      <div class="actions"><a class="btn btn-primary" href="{CV}" target="_blank" rel="noopener">Download CV (PDF)</a><a class="btn" href="{hire_wa}" target="_blank" rel="noopener">Discuss a role</a><a class="text-link" href="cv.html">View web CV</a></div>
    </div>
    <aside class="hire-card" aria-label="Quick facts">
      <p class="hc-l">At a glance</p>
      <dl>
        <div><dt>Current role</dt><dd>Evaluator and Data Officer, RHCI</dd></div>
        <div><dt>Location</dt><dd>Bo, Sierra Leone</dd></div>
        <div><dt>Work type</dt><dd>Full-time, contract, consulting</dd></div>
        <div><dt>Work mode</dt><dd>Onsite in Bo, or remote</dd></div>
        <div><dt>Languages</dt><dd>English and Krio</dd></div>
        <div><dt>Core tools</dt><dd>Power BI, Excel, Survey123, PostgreSQL</dd></div>
      </dl>
      <a class="btn btn-primary" href="mailto:{EMAIL}?subject=Role%20for%20Alhaji%20Ibrahim%20Mehemoh">Email me</a>
    </aside>
  </header>
</div>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Roles I am looking for</h2><p>Each one links to work that shows how I approach it.</p></div>
    <div class="role-grid">{roles_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap about-two">
    <div>
      <div class="section-head"><h2>What I bring</h2></div>
      <ul class="principles">{bring_html}</ul>
    </div>
    <div>
      <div class="section-head"><h2>Experience in brief</h2></div>
      <ol class="jt edu">
        <li><span class="jt-when">Oct 2024 to present</span><b>Evaluator and Data Officer</b><em>Rural Health Care Initiative, Tikonko</em></li>
        <li><span class="jt-when">Sep 2023 to Oct 2024</span><b>Assistant IT Manager</b><em>SLIEPA, Freetown</em></li>
        <li><span class="jt-when">Jan 2022 to Sep 2023</span><b>IT and Data Officer</b><em>SLPP, Bo District</em></li>
        <li><span class="jt-when">2016 to 2021</span><b>ICT Tutor and Internet Cafe Attendant</b><em>Growth Centre, Bo</em></li>
      </ol>
      <p style="margin-top:1rem"><a class="text-link" href="about.html">Full story and education</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Skills employers ask about</h2></div>
    <div class="sk-grid">
      <div class="sk-card">{icon('chart')}<h3>Data and M&amp;E</h3><ul><li>Power BI</li><li>Excel</li><li>Survey123</li><li>XLSForm</li><li>Data quality</li><li>Indicators</li><li>Logframes</li></ul></div>
      <div class="sk-card">{icon('db')}<h3>Systems</h3><ul><li>PostgreSQL</li><li>Flask</li><li>Google Apps Script</li><li>Web apps</li><li>Documentation</li></ul></div>
      <div class="sk-card">{icon('wifi')}<h3>IT</h3><ul><li>Networking</li><li>Hardware</li><li>Helpdesk</li><li>Backups</li><li>Security basics</li></ul></div>
      <div class="sk-card">{icon('teach')}<h3>People</h3><ul><li>Staff training</li><li>Supervising a Data Assistant</li><li>Reports</li><li>Presentations</li></ul></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Proof of work</h2><p>Case studies, free resources and notes on this site.</p></div>
    <div class="glance">
      <a class="gl gl-link" href="portfolio.html"><b>10</b><span>case studies</span></a>
      <a class="gl gl-link" href="resources.html"><b>17</b><span>free templates and checklists</span></a>
      <a class="gl gl-link" href="community.html"><b>19</b><span>practical notes</span></a>
      <a class="gl gl-link" href="demo.html"><b>1</b><span>interactive sample dashboard</span></a>
    </div>
  </div>
</section>

<section class="section"><div class="wrap"><div class="section-head"><h2>Questions from employers</h2></div><div class="faq-list">{hfaq_html}</div></div></section>

{cta('Let us talk about the role.', 'Send me the job description or the problem you want solved. I usually reply fastest on WhatsApp.')}'''
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
import notes_render as NR
for n in NOTES:
    n['fn'] = n['slug'] + '.html'
    n['html'], n['toc'] = NR.render(n['body'])
    n['mins'] = reading_minutes(n['body'])
    n['art'] = NR.hero_art(n.get('motif', 'checks'))
cats = sorted({n['category'] for n in NOTES})


def fmt_date(d):
    if not d:
        return ''
    try:
        return datetime.date.fromisoformat(d).strftime('%d %B %Y').lstrip('0')
    except ValueError:
        return d


def note_row(n):
    d = n.get('date') or n.get('updated')
    date = ('%s<time datetime="%s">%s</time> &middot; ' % ('' if n.get('date') else 'Updated ', d, fmt_date(d))) if d else ''
    hue = sum(map(ord, n['category'])) % 4
    return ('<a class="note-card c%d" data-cat="%s" data-search="%s" href="%s"><span class="nc-art">%s</span><span class="nc-in"><span class="nc-cat">%s</span><h3>%s</h3><p>%s</p>'
            '<span class="nc-meta">%s%d min read</span></span></a>') % (
        hue, esc(n['category']), esc((n['title'] + ' ' + n['summary'] + ' ' + n['body']).lower()), n['fn'], n['art'], esc(n['category']),
        esc(n['title']), esc(n['summary']), date, n['mins'])


rows = ''.join(note_row(n) for n in sorted(NOTES, key=lambda n: n.get('date') or '', reverse=True))
cat_btns = '<button type="button" class="filter is-active" data-cat="all" aria-pressed="true">All</button>' + ''.join(
    '<button type="button" class="filter" data-cat="%s" aria-pressed="false">%s</button>' % (esc(c), esc(c)) for c in cats)
notes_body = f'''<div class="wrap">
  <div class="page-head"><h1>Notes</h1><p class="lede">Short, practical posts on data, health systems, IT and cybersecurity.</p>
  <p class="small"><a class="rss-link" href="feed.xml">Subscribe with RSS</a> <span class="muted">to get new notes in your feed reader.</span></p></div>
</div>
<section class="section">
  <div class="wrap">
    <div class="notes-tools">
      <label class="sr-only" for="noteSearch">Search notes</label>
      <input id="noteSearch" type="search" placeholder="Search notes" autocomplete="off">
      <div class="filters" role="group" aria-label="Filter notes by category">{cat_btns}</div>
    </div>
    <p class="small muted" id="noteCount" role="status" aria-live="polite"></p>
    <div class="note-grid" id="noteList">{rows}</div>
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
RES = {r['file']: r for r in json.load(open(os.path.join(OUT, 'downloads', 'resources.json')))['items']}
for i, n in enumerate(NOTES):
    nxt = NOTES[(i + 1) % len(NOTES)]
    prv = NOTES[i - 1]
    pub = ('<span>Published <time datetime="%s">%s</time></span>' % (n['date'], fmt_date(n['date']))) if n.get('date') else ''
    upd = ('<span>Updated <time datetime="%s">%s</time></span>' % (n['updated'], fmt_date(n['updated']))) if n.get('updated') else ''
    page_url = BASE + n['fn']
    share_wa = esc(wa_link('%s %s' % (n['title'], page_url)))
    toc = ''.join('<li><a href="#%s">%s</a></li>' % (a, esc(t)) for a, t in n['toc'])
    take = ''.join('<li>%s</li>' % esc(t) for t in n.get('takeaways', []))
    rel = ''
    if n.get('resources'):
        cards = ''.join('<a class="rel-card" href="downloads/%s" download><img src="images/resources/%s.webp" alt="" width="720" height="562" loading="lazy"><span><span class="ftype ft-%s">%s</span><b>%s</b><em>%s</em></span></a>' % (
            f, RES[f]['slug'], {'PDF': 'pdf', 'Excel': 'xls', 'XLSForm': 'form'}[RES[f]['type']], RES[f]['type'], esc(RES[f]['title']), RES[f]['size']) for f in n['resources'] if f in RES)
        rel = '<section class="note-rel" aria-labelledby="rel-h"><h2 id="rel-h">Free tools for this note</h2><div class="rel-grid">%s</div><p class="small"><a class="text-link" href="resources.html">See all free resources</a></p></section>' % cards
    b = f'''<article class="note">
<div class="wrap">
  <header class="note-hero">
    <div class="note-hero-text">
      <p class="crumb"><a href="community.html">Notes</a></p>
      <p class="note-cat">{esc(n['category'])}</p>
      <h1>{esc(n['title'])}</h1>
      <p class="lede">{esc(n['summary'])}</p>
      <div class="note-meta"><picture><source type="image/webp" srcset="images/profile-square.webp"><img src="images/profile.jpeg" width="44" height="44" alt=""></picture>
        <div><b>Alhaji Ibrahim Mehemoh</b><p>{pub}{upd}<span>{n['mins']} min read</span></p></div></div>
    </div>
    <div class="note-hero-art">{n['art']}</div>
  </header>
  <div class="note-layout">
    <aside class="note-side" aria-label="On this page">
      <nav class="note-toc"><p>On this page</p><ol>{toc}</ol></nav>
      <div class="note-share"><p>Share</p><a class="btn" href="{share_wa}" target="_blank" rel="noopener">WhatsApp</a><button class="btn" type="button" data-copy="{page_url}">Copy link</button></div>
    </aside>
    <div class="note-main">
      <div class="takeaways"><p class="tk-l">In short</p><ul>{take}</ul></div>
      <div class="note-body">{n['html']}</div>
      {rel}
      <div class="author-card"><picture><source type="image/webp" srcset="images/profile-square.webp"><img src="images/profile.jpeg" width="84" height="84" alt="Alhaji Ibrahim Mehemoh"></picture>
        <div><p class="ac-l">Written by</p><b>Alhaji Ibrahim Mehemoh</b><p>Data Officer and M&amp;E specialist in Bo, Sierra Leone. I build Survey123 forms, Power BI dashboards and simple data systems for health programmes, and provide IT support for small organisations.</p>
        <p class="ac-links"><a href="about.html">About me</a><a href="contact.html">Contact</a><a href="feed.xml">Follow by RSS</a></p></div></div>
    </div>
  </div>
  <nav class="note-pn" aria-label="More notes">
    <a class="pn-card" href="{prv['fn']}"><span class="pn-l">Previous</span><span class="pn-art">{prv['art']}</span><b>{esc(prv['title'])}</b></a>
    <a class="pn-card" href="{nxt['fn']}"><span class="pn-l">Next</span><span class="pn-art">{nxt['art']}</span><b>{esc(nxt['title'])}</b></a>
  </nav>
</div>
</article>
{cta('Questions about your own data or IT setup?', 'Send me a message and I will point you in the right direction.')}'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": n['title'], "description": n['summary'],
           "author": {"@type": "Person", "name": "Alhaji Ibrahim Mehemoh", "url": BASE}, "mainEntityOfPage": page_url,
           "image": BASE + "images/og-image.jpg", "articleSection": n['category']}
    if n.get('date'):
        art["datePublished"] = n['date']
    if n.get('updated'):
        art["dateModified"] = n['updated']
    page(n['fn'], n['title'] + ' | Alhaji Ibrahim Mehemoh', n['summary'], b, active='community.html', ld=art,
         og_type='article', crumbs=[('Notes', 'community.html'), (n['title'], None)],
         wa_text='Hello Alhaji, I read your note "%s" and have a question.' % n['title'])


# ------------------------------------------------------------------ SERVICE DETAIL PAGES
SCREW = '''<div class="screw-anim" aria-hidden="true"><svg viewBox="0 0 240 150">  <rect x="20" y="96" width="200" height="34" rx="8" class="sw-board"/>  <g class="sw-chips"><rect x="40" y="104" width="26" height="18" rx="3"/><rect x="172" y="104" width="26" height="18" rx="3"/></g>  <path class="sw-trace" d="M66 113h30M144 113h28"/>  <g class="sw-screw"><circle cx="120" cy="113" r="12" class="sw-head"/><path d="M112 113h16M120 105v16" class="sw-slot"/></g>  <g class="sw-driver"><rect x="115" y="40" width="10" height="64" rx="2" class="sw-shaft"/><path d="M116 104l4 7 4-7z" class="sw-shaft"/><rect x="104" y="0" width="32" height="46" rx="10" class="sw-handle"/><path d="M112 8v30M120 8v30M128 8v30" class="sw-grip"/></g>  <g class="sw-sparks"><circle cx="100" cy="98" r="2"/><circle cx="142" cy="96" r="2"/><circle cx="96" cy="88" r="1.5"/></g></svg></div>'''
from services_content import DETAIL
SVC_ART = {'dashboards': 'case-epi-dashboard/01-management-overview', 'forms': 'case-survey123/01-mobile-registration-form',
           'quality': 'case-epi-dashboard/04-data-quality-review', 'systems': 'case-dms/01-patient-registration-workspace',
           'web': 'case-this-website/01-home', 'reporting': 'case-epi-dashboard/03-monthly-performance'}
SVC_MOTIF = {'training': 'people', 'hardware': 'wrench', 'network': 'tools', 'security': 'shield', 'contracts': 'matrix'}
CASE_BY = {c['slug']: c for c in CASES}
for k, sv in enumerate(SERVICES):
    d = DETAIL[sv['key']]
    q = 'request.html?service=' + sv['form'].replace(' ', '+').replace('&', '%26')
    if sv['key'] in SVC_ART:
        real = 'website' in SVC_ART[sv['key']]
        art = ('<figure class="case-cover"><div class="browser"><span class="b-dots"><i></i><i></i><i></i></span><img src="images/cases/%s.webp" alt=""></div><figcaption>%s</figcaption></figure>'
               % (SVC_ART[sv['key']], 'Screenshot of this website' if real else '<span class="pill pill-design">Sample data</span> Design mockup from my work'))
    else:
        art = ('<div class="case-art screw-hero">' + SCREW + '<p class="art-note">Illustration</p></div>') if sv['key'] == 'hardware' else '<div class="case-art">%s<p class="art-note">Illustration</p></div>' % NR.hero_art(SVC_MOTIF.get(sv['key'], 'checks'))
    gets = ''.join('<li>%s<span>%s</span></li>' % (icon('check'), esc(g)) for g in sv['gets'])
    how = ''.join('<li><h3>%s</h3><p>%s</p></li>' % (esc(a), esc(b)) for a, b in d['how'])
    faq = ''.join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (esc(a), esc(b)) for a, b in d['faq'])
    cases_html = ''.join('<a class="pn-card" href="%s.html"><span class="pn-l">Case study</span><span class="pn-art">%s</span><b>%s</b></a>' % (c, cover_img(CASE_BY[c])[0], esc(CASE_BY[c]['title'])) for c in d['cases'] if c in CASE_BY)
    notes_html = ''.join('<a class="rn" href="%s.html"><span class="rn-art">%s</span><b>%s</b></a>' % (s_, NR.hero_art(NOTE_TITLES[s_].get('motif', 'checks')), esc(NOTE_TITLES[s_]['title'])) for s_ in d['notes'] if s_ in NOTE_TITLES)
    res_html = ''.join('<a class="rel-card" href="downloads/%s" download><img src="images/resources/%s.webp" alt="" width="720" height="562" loading="lazy"><span><span class="ftype ft-%s">%s</span><b>%s</b><em>%s</em></span></a>' % (
        f, RES_ALL[f]['slug'], {'PDF': 'pdf', 'Excel': 'xls', 'XLSForm': 'form'}[RES_ALL[f]['type']], RES_ALL[f]['type'], esc(RES_ALL[f]['title']), RES_ALL[f]['size']) for f in d['resources'] if f in RES_ALL)
    others = ''.join('<a href="service-%s.html"%s>%s%s</a>' % (o['key'], ' aria-current="page"' if o['key'] == sv['key'] else '', icon(o['icon']), esc(o['title'])) for o in SERVICES)
    grp = 'Data and M&amp;E' if sv['group'] == 'data' else 'IT support'
    wa = esc(wa_link('Hello Alhaji, I would like to ask about %s.' % sv['title'].lower()))
    pk = '<p class="svc-pk">IT support has fixed packages from Le 250. <a class="text-link" href="services.html#packages">See the packages</a></p>' if sv['group'] == 'it' else '<p class="svc-pk">Priced by scope after a short conversation. <a class="text-link" href="services.html#pricing">What affects the price</a></p>'
    body = f"""<div class="wrap">
  <header class="case-hero svc-detail-hero">
    <div class="case-hero-text">
      <p class="crumb"><a href="services.html">Services</a></p>
      <div class="case-status"><span class="pill {'pill-ok' if sv['group'] == 'data' else 'pill-design'}">{grp}</span><span class="case-org">Bo, Sierra Leone &middot; onsite and remote</span></div>
      <h1>{esc(sv['title'])}</h1>
      <p class="lede">{esc(d['intro'])}</p>
      <div class="actions"><a class="btn btn-primary" href="{q}">Ask about this</a><a class="btn" href="{wa}" target="_blank" rel="noopener">WhatsApp me</a></div>
      {pk}
    </div>
    {art}
  </header>
</div>
<section class="section">
  <div class="wrap svc-two">
    <div><div class="section-head"><h2>What you get</h2></div><ul class="get-list">{gets}</ul><p class="svc-fit"><b>Good for:</b> {esc(sv['fit'])}</p></div>
    <div><div class="section-head"><h2>Common questions</h2></div><div class="faq-list">{faq}</div></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>How it works</h2></div>
    <ol class="steps steps-line">{how}</ol>
  </div>
</section>
{('<section class="section"><div class="wrap"><div class="section-head"><h2>Proof from my work</h2></div><div class="note-pn">' + cases_html + '</div></div></section>') if cases_html else ''}
{('<section class="section"><div class="wrap">' + ('<div class="case-more" style="margin-top:0"><h2>Read more</h2><div class="rn-grid">' + notes_html + '</div></div>' if notes_html else '') + ('<div class="note-rel case-res"><h2>Free tools</h2><div class="rel-grid">' + res_html + '</div></div>' if res_html else '') + '</div></section>') if (notes_html or res_html) else ''}
<section class="section-tight">
  <div class="wrap"><nav class="svc-others" aria-label="Other services"><p>All services</p>{others}</nav></div>
</section>
{cta('Ready to talk about ' + esc(sv['title'].lower()) + '?', 'Tell me what you need in a few lines. I will reply with a plan and a quote.')}"""
    ld = {"@context": "https://schema.org", "@type": "Service", "name": sv['title'], "description": d['intro'], "serviceType": sv['title'],
          "provider": {"@type": "Person", "name": "Alhaji Ibrahim Mehemoh", "url": BASE},
          "areaServed": {"@type": "Country", "name": "Sierra Leone"}, "url": BASE + 'service-%s.html' % sv['key']}
    page('service-%s.html' % sv['key'], '%s in Sierra Leone | Alhaji Ibrahim Mehemoh' % sv['title'], sv['lead'], body,
         active='services.html', ld=ld, crumbs=[('Services', 'services.html'), (sv['title'], None)],
         wa_text='Hello Alhaji, I would like to ask about %s.' % sv['title'].lower())


# ------------------------------------------------------------------ HOME (rendered last so it can show everything)
_home_cases = ['case-epi-dashboard', 'case-survey123', 'case-chw-card-studio', 'case-epi-data-audit', 'case-dms', 'case-staff-id-cards']
home_work = ('<div class="proj-grid home-proj">' + ''.join(proj_card(CASE_BY[c]) for c in _home_cases) + '</div>'
             '<p class="sc-note" style="margin-top:1rem"><span class="pill pill-design">Sample data</span> Screens are design mockups. Real programme data stays with the organisation.</p>'
             '<p style="margin-top:1rem"><a class="btn" href="portfolio.html">See all %d projects</a></p>' % len(CASES))
home_stats = ('<div class="glance home-glance">'
              '<a class="gl gl-link" href="portfolio.html"><b data-count="%d">%d</b><span>case studies</span></a>'
              '<a class="gl gl-link" href="services.html"><b data-count="%d">%d</b><span>services</span></a>'
              '<a class="gl gl-link" href="resources.html"><b data-count="%d">%d</b><span>free resources</span></a>'
              '<a class="gl gl-link" href="community.html"><b data-count="%d">%d</b><span>practical notes</span></a></div>') % (len(CASES), len(CASES), len(SERVICES), len(SERVICES), len(RES_ALL), len(RES_ALL), len(NOTES), len(NOTES))
home_services = ('<section class="section"><div class="wrap"><div class="svc-head-row"><div class="section-head"><h2>Services</h2><p>Data and M&amp;E for health programmes, and practical IT support for offices, clinics and schools.</p></div><div class="screw-anim" aria-hidden="true"><svg viewBox="0 0 240 150">  <rect x="20" y="96" width="200" height="34" rx="8" class="sw-board"/>  <g class="sw-chips"><rect x="40" y="104" width="26" height="18" rx="3"/><rect x="172" y="104" width="26" height="18" rx="3"/></g>  <path class="sw-trace" d="M66 113h30M144 113h28"/>  <g class="sw-screw"><circle cx="120" cy="113" r="12" class="sw-head"/><path d="M112 113h16M120 105v16" class="sw-slot"/></g>  <g class="sw-driver"><rect x="115" y="40" width="10" height="64" rx="2" class="sw-shaft"/><path d="M116 104l4 7 4-7z" class="sw-shaft"/><rect x="104" y="0" width="32" height="46" rx="10" class="sw-handle"/><path d="M112 8v30M120 8v30M128 8v30" class="sw-grip"/></g>  <g class="sw-sparks"><circle cx="100" cy="98" r="2"/><circle cx="142" cy="96" r="2"/><circle cx="96" cy="88" r="1.5"/></g></svg></div></div>'
                 '<div class="hs-grid">' + ''.join('<a class="hs" href="service-%s.html">%s<b>%s</b><span>%s</span></a>' % (sv['key'], icon(sv['icon']), esc(sv['title']), 'Data and M&amp;E' if sv['group'] == 'data' else 'IT support') for sv in SERVICES) +
                 '<a class="hs hs-cta" href="services.html#finder"><b>Not sure which?</b><span>Answer one question and I will point you to the right service.</span></a></div></div></section>')
_home_res = ['me-data-quality-checklist.pdf', 'stock-tracker.xlsx', 'xlsform-cheat-sheet.pdf', 'indicator-tracker.xlsx']
_kit = json.load(open(os.path.join(OUT, 'downloads', 'resources.json')))['kit']
home_resources = ('<section class="section band-sheet"><div class="wrap"><div class="section-head"><h2>Free resources</h2><p>Checklists, templates and trackers you can use today. No sign-up.</p></div><div class="rel-grid home-res">' +
                  ''.join('<a class="rel-card" href="downloads/%s" download><img src="images/resources/%s.webp" alt="" width="720" height="562" loading="lazy"><span><span class="ftype ft-%s">%s</span><b>%s</b><em>%s</em></span></a>' % (
                      f, RES_ALL[f]['slug'], {'PDF': 'pdf', 'Excel': 'xls', 'XLSForm': 'form'}[RES_ALL[f]['type']], RES_ALL[f]['type'], esc(RES_ALL[f]['title']), RES_ALL[f]['size']) for f in _home_res) +
                  '</div><div class="actions"><a class="btn btn-primary" href="downloads/%s" download>Download all %d as a ZIP (%s)</a><a class="btn" href="resources.html">Browse the library</a></div></div></section>') % (_kit['file'], len(RES_ALL), _kit['size'])
_home_notes = ['note-check-epi-data-quality', 'note-dashboards-people-use', 'note-survey123-mistakes']
_nb = {n['slug']: n for n in NOTES}
home_notes = ('<section class="section"><div class="wrap"><div class="section-head"><h2>Latest notes</h2><p>Short, practical guides on health data, M&amp;E and IT.</p></div><div class="note-grid home-notes">' +
              ''.join(note_row(_nb[k]) for k in _home_notes) + '</div><p style="margin-top:1.25rem"><a class="text-link" href="community.html">Read all %d notes</a></p></div></section>' % len(NOTES))
for k, v in [('@@HOME_WORK@@', home_work), ('@@HOME_STATS@@', home_stats), ('@@HOME_SERVICES@@', home_services), ('@@HOME_RESOURCES@@', home_resources), ('@@HOME_NOTES@@', home_notes)]:
    index_body = index_body.replace(k, v)
page('index.html', 'Alhaji Ibrahim Mehemoh | Health Data and M&E Specialist in Bo, Sierra Leone',
     'Data Officer and M&E specialist in Bo, Sierra Leone. Survey123 forms, Power BI dashboards, data quality and health data systems for NGOs and health programmes.',
     index_body, ld=person_ld)

# ------------------------------------------------------------------ 404
page('404.html', 'Page not found | Alhaji Ibrahim Mehemoh', 'This page does not exist.',
     '''<div class="wrap"><div class="page-head nf-head"><p class="nf-code" aria-hidden="true">4<span>0</span>4</p><h1>That page does not exist</h1><p class="lede">The link may be old or mistyped. Try one of these instead.</p>
<div class="actions"><a class="btn btn-primary" href="index.html">Go to the home page</a><a class="btn" href="portfolio.html">See projects</a><a class="btn" href="contact.html">Contact me</a></div></div></div>''',
     noindex=True)

# ------------------------------------------------------------------ extra pages, feed, sitemap, PWA files
import extras
extras.build_all(NOTES, TODAY)
print('built', len(PAGES), 'indexed pages')
