"""Extra pages, downloads, feed, sitemap and PWA files. Called from build.py."""
import datetime, json, os
import site_config as C
from layout import *


def head(title, lede, extra=''):
    return f'<div class="wrap"><div class="page-head"><h1>{title}</h1><p class="lede">{lede}</p>{extra}</div></div>'


# ------------------------------------------------------------------ downloads
def make_downloads():
    d = os.path.join(OUT, 'downloads')
    os.makedirs(d, exist_ok=True)
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill
        from openpyxl.worksheet.datavalidation import DataValidation
        hdr = PatternFill('solid', fgColor='0B7A5C')
        # stock tracker
        wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Stock'
        cols = ['Item', 'Unit', 'Opening stock', 'Received', 'Issued', 'Closing stock', 'Reorder level', 'Status']
        ws.append(cols)
        for r in range(2, 32):
            ws[f'F{r}'] = f'=IF(A{r}="","",C{r}+D{r}-E{r})'
            ws[f'H{r}'] = f'=IF(A{r}="","",IF(F{r}<=G{r},"REORDER","OK"))'
        for c in ws[1]:
            c.font = Font(bold=True, color='FFFFFF'); c.fill = hdr
        for i, w in enumerate([28, 10, 14, 12, 12, 14, 14, 12]):
            ws.column_dimensions[chr(65 + i)].width = w
        ws.freeze_panes = 'A2'
        ws2 = wb.create_sheet('How to use')
        for line in ['Type each item in column A and fill the blue-labelled numbers: opening stock, received, issued, reorder level.',
                     'Closing stock and Status calculate automatically.',
                     'Use one file per facility per month. Do not store patient names here.']:
            ws2.append([line])
        ws2.column_dimensions['A'].width = 100
        wb.save(os.path.join(d, 'stock-tracker.xlsx'))
        # sample XLSForm
        wb = openpyxl.Workbook(); s = wb.active; s.title = 'survey'
        s.append(['type', 'name', 'label', 'required', 'relevant', 'constraint', 'constraint_message'])
        rows = [
            ['start', 'start'], ['end', 'end'],
            ['select_one facility', 'facility', 'Health facility', 'yes'],
            ['date', 'visit_date', 'Date of visit', 'yes', '', '. <= today()', 'Date cannot be in the future'],
            ['integer', 'children_vaccinated', 'Children vaccinated today', 'yes', '', '. >= 0 and . <= 500', 'Enter a number from 0 to 500'],
            ['select_one yesno', 'stock_out', 'Any vaccine stock-out this month?', 'yes'],
            ['text', 'stock_out_detail', 'Which vaccine?', 'yes', "${stock_out} = 'yes'"],
            ['note', 'thanks', 'Thank you. Do not record names or phone numbers in this form.'],
        ]
        for r in rows:
            s.append(r)
        c = wb.create_sheet('choices'); c.append(['list_name', 'name', 'label'])
        for r in [['facility', 'phc1', 'Sample PHC 1'], ['facility', 'phc2', 'Sample PHC 2'], ['facility', 'phc3', 'Sample PHC 3'],
                  ['yesno', 'yes', 'Yes'], ['yesno', 'no', 'No']]:
            c.append(r)
        st = wb.create_sheet('settings'); st.append(['form_title', 'form_id']); st.append(['Sample EPI monthly check', 'sample_epi_check'])
        for sh in (s, c, st):
            for cell in sh[1]:
                cell.font = Font(bold=True)
            for col in 'ABCDEFG':
                sh.column_dimensions[col].width = 28
        wb.save(os.path.join(d, 'sample-epi-xlsform.xlsx'))
    except Exception as e:
        print('xlsx skipped:', e)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        st = getSampleStyleSheet()
        h = ParagraphStyle('h', parent=st['Title'], textColor=colors.HexColor('#0F2430'), fontSize=20, alignment=0)
        b = ParagraphStyle('b', parent=st['BodyText'], fontSize=10.5, leading=14)
        doc = SimpleDocTemplate(os.path.join(d, 'me-data-quality-checklist.pdf'), pagesize=A4, leftMargin=44, rightMargin=44,
                                topMargin=44, bottomMargin=44, title='M&E data quality checklist', author='Alhaji Ibrahim Mehemoh')
        el = [Paragraph('M&amp;E data quality checklist', h),
              Paragraph('Use this before you send a monthly report. Tick each box. Any "No" needs a note and an owner.', b), Spacer(1, 10)]
        groups = [
            ('Completeness', ['Every facility expected to report has reported', 'No blank required fields', 'Zero values are entered as 0, not left empty']),
            ('Timeliness', ['Reports arrived by the agreed deadline', 'The reporting period on each form is correct', 'Late reports are listed with a reason']),
            ('Accuracy', ['Totals equal the sum of their parts', 'Numbers vaccinated do not exceed the target population by an unexplained margin', 'Values were checked against the register for a sample of facilities']),
            ('Consistency', ['Same indicator definitions used by every facility', 'This month is compared with last month and large changes are explained', 'Units and date formats are the same everywhere']),
            ('Duplicates and outliers', ['No duplicate rows or repeated submissions', 'Extreme values were confirmed with the facility', 'Corrections are logged with who changed what and when']),
            ('Privacy and storage', ['No names, phone numbers or ID numbers in shared files', 'Raw data is backed up in two places', 'Files are named with facility, month and version']),
        ]
        for g, items in groups:
            data = [[Paragraph('<b>%s</b>' % g, b), '', '']] + [['[  ]', Paragraph(i, b), 'Yes / No / N/A'] for i in items]
            t = Table(data, colWidths=[30, 380, 85])
            t.setStyle(TableStyle([('SPAN', (0, 0), (-1, 0)), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E3EFEA')),
                                   ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#B9C7C2')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
            el += [t, Spacer(1, 8)]
        el.append(Paragraph('Alhaji Ibrahim Mehemoh, Data Officer and M&amp;E specialist. alhajiimehemoh.github.io', b))
        doc.build(el)
    except Exception as e:
        print('pdf skipped:', e)


# ------------------------------------------------------------------ resources
RES_ICON = {'PDF': 'pdf', 'Excel': 'xls', 'XLSForm': 'form'}


def resources():
    import json as _json
    data = _json.load(open(os.path.join(OUT, 'downloads', 'resources.json')))
    items, kit = data['items'], data['kit']
    slug = lambda c: c.lower().replace('&', '').replace(' ', '-').replace('--', '-')
    cats = []
    for it in items:
        if it['category'] not in cats:
            cats.append(it['category'])
    order = ['M&E', 'Data collection', 'Dashboards', 'Training', 'Inventory', 'IT']
    cats.sort(key=lambda c: order.index(c) if c in order else 99)
    n_pdf = sum(1 for i in items if i['type'] == 'PDF')
    n_xls = len(items) - n_pdf

    def card(it):
        meta = (('%d page%s' % (it['pages'], '' if it['pages'] == 1 else 's')) if it.get('pages') else '%d sheets' % it['sheets']) + ' &middot; ' + it['size']
        preview = ('<a class="btn" href="downloads/%s" target="_blank" rel="noopener">Preview</a>' % it['file']) if it['type'] == 'PDF' else ''
        tags = ''.join('<li>%s</li>' % esc(t) for t in it['tags'])
        return f'''<article class="res-card" data-type="{slug(it['category'])}">
  <a class="res-thumb" href="downloads/{it['file']}" download tabindex="-1" aria-hidden="true"><span class="res-paper"><img src="images/resources/{it['slug']}.webp" width="720" height="562" alt="" loading="lazy"></span></a>
  <div class="res-body">
    <div class="res-top"><span class="ftype ft-{RES_ICON[it['type']]}">{it['type']}</span><span class="res-cat">{esc(it['category'])}</span></div>
    <h3>{esc(it['title'])}</h3>
    <p>{esc(it['blurb'])}</p>
    <ul class="res-tags">{tags}</ul>
    <div class="res-foot"><span class="res-meta">{meta}</span><span class="res-actions">{preview}<a class="btn btn-primary" href="downloads/{it['file']}" download>Download</a></span></div>
  </div>
</article>'''
    cards = ''.join(card(i) for i in items)
    btns = '<button type="button" class="filter is-active" data-filter="all" aria-pressed="true">All <span>%d</span></button>' % len(items) + ''.join(
        '<button type="button" class="filter" data-filter="%s" aria-pressed="false">%s <span>%d</span></button>' % (
            slug(c), esc(c), sum(1 for i in items if i['category'] == c)) for c in cats)
    stack = ''.join('<img src="images/resources/%s.webp" alt="" width="720" height="562" style="--k:%d">' % (s_, k) for k, s_ in enumerate(
        ['me-data-quality-checklist', 'stock-tracker', 'xlsform-cheat-sheet']))
    video_block = ''
    if C.TUTORIAL_VIDEOS:
        import re
        vs = ''
        for v in C.TUTORIAL_VIDEOS:
            m = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{6,})', v['url'])
            emb = (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" title="{esc(v["title"])}" loading="lazy" allowfullscreen></iframe></div>'
                   if m else f'<p><a class="btn" href="{esc(v["url"])}" target="_blank" rel="noopener">Watch</a></p>')
            vs += f'<div><h3>{esc(v["title"])}</h3>{emb}</div>'
        video_block = f'<section class="section"><div class="wrap"><div class="section-head"><h2>Tutorials</h2></div><div class="cols">{vs}</div></div></section>'
    body = f'''<div class="wrap">
  <div class="page-head res-hero">
    <div>
      <h1>Free resources</h1>
      <p class="lede">Checklists, templates and trackers I use in health data and IT work. Free to download, no sign-up, ready to print or adapt.</p>
      <ul class="res-stats"><li><b>{len(items)}</b> free files</li><li><b>{n_pdf}</b> printable PDFs</li><li><b>{n_xls}</b> Excel and XLSForm</li></ul>
      <div class="actions"><a class="btn btn-primary" href="downloads/{kit['file']}" download>Download all as a ZIP ({kit['size']})</a><a class="btn" href="#library">Browse the library</a></div>
    </div>
    <div class="res-stack" aria-hidden="true">{stack}</div>
  </div>
</div>
<section class="section" id="library">
  <div class="wrap">
    <div class="section-head"><h2>The library</h2><p>Every file uses the same clean layout. PDFs print well on A4. Excel files have a How to use sheet, drop-down lists and formulas that fill in by themselves.</p></div>
    <div class="filters res-filters" role="group" aria-label="Filter resources by topic">{btns}</div>
    <p class="small muted" id="filterCount" data-noun="file" role="status" aria-live="polite"></p>
    <div class="res-grid" data-filter-target>{cards}</div>
  </div>
</section>
{video_block}
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Getting the most from them</h2></div>
    <ol class="steps">
      <li><h3>Start with one</h3><p>Pick the checklist that matches your next deadline and use it this month.</p></li>
      <li><h3>Adapt the words</h3><p>Change labels and examples to your programme. Keep the structure.</p></li>
      <li><h3>Remove personal data</h3><p>Never add patient names, phone numbers or ID numbers to shared files.</p></li>
      <li><h3>Make it routine</h3><p>Same file, same day, every month. Consistency is what improves data.</p></li>
    </ol>
  </div>
</section>
{cta('Want these tailored to your programme?', 'I can adapt any template to your indicators, build it into Survey123 or Power BI, and train your staff to use it.')}'''
    page('resources.html', 'Free resources: M&E checklists, Excel trackers and XLSForm templates | Alhaji Ibrahim Mehemoh',
         'Free downloads: M&E data quality checklist, indicator reference sheet, monthly report template, XLSForm cheat sheet, stock tracker, indicator tracker, data cleaning log and IT checklists.',
         body, active='resources.html', crumbs=[('Resources', None)])


# ------------------------------------------------------------------ demo dashboard
def demo():
    body = head('Sample dashboard', 'An interactive EPI-style dashboard built on invented sample data so you can see how filtering and views work. It contains no real facility or patient data.') + '''
<section class="section"><div class="wrap">
  <p class="notice" role="note"><strong>Sample data.</strong> Facility names and numbers are made up for demonstration.</p>
  <div class="demo-controls">
    <label>View <select id="dView"><option value="nurse">Nurse (my facility)</option><option value="mgmt" selected>Management (all facilities)</option><option value="donor">Donor (summary)</option></select></label>
    <label>Facility <select id="dFac"></select></label>
    <label>From <select id="dFrom"></select></label>
    <label>To <select id="dTo"></select></label>
  </div>
  <div class="kpis" id="dKpis"></div>
  <div class="demo-grid">
    <figure class="demo-card"><figcaption>Doses given by month</figcaption><svg id="dTrend" viewBox="0 0 600 260" role="img" aria-label="Line chart of doses given by month"></svg></figure>
    <figure class="demo-card"><figcaption>Coverage by facility (target 90%)</figcaption><svg id="dBars" viewBox="0 0 600 260" role="img" aria-label="Bar chart of coverage by facility"></svg></figure>
  </div>
  <div class="table-wrap"><table class="demo-table" id="dTable"><caption class="sr-only">Facility summary</caption></table></div>
  <p class="small muted">Built with the same approach I use in Power BI and Excel: one clean table, clear filters, one message per chart.</p>
</div></section>
<section class="section"><div class="wrap"><h2>Want something like this for your programme?</h2><p><a class="btn btn-primary" href="request.html?service=Dashboard">Request a dashboard</a></p></div></section>'''
    page('demo.html', 'Sample dashboard | Alhaji Ibrahim Mehemoh',
         'Interactive sample EPI dashboard on invented data, showing nurse, management and donor views.', body,
         active='portfolio.html', crumbs=[('Sample dashboard', None)], extra_head='\n  <script src="demo.js?v=%s" defer></script>' % CSS_V)
    js = r'''(function () {
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var facs = ['Sample PHC 1','Sample PHC 2','Sample PHC 3','Sample PHC 4','Sample PHC 5'];
  var seed = 7; function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
  var data = facs.map(function (f, i) {
    var target = 60 + i * 14;
    return { name: f, target: target, m: months.map(function (_, k) {
      return Math.round(target * (0.62 + 0.3 * rnd() + (i === 3 ? -0.12 : 0) + k * 0.004));
    }) };
  });
  var $ = function (id) { return document.getElementById(id); };
  var facSel = $('dFac'), from = $('dFrom'), to = $('dTo'), view = $('dView');
  if (!facSel) return;
  facSel.innerHTML = '<option value="all">All facilities</option>' + facs.map(function (f, i) { return '<option value="' + i + '">' + f + '</option>'; }).join('');
  [from, to].forEach(function (s, n) { s.innerHTML = months.map(function (m, i) { return '<option value="' + i + '"' + (i === (n ? 11 : 0) ? ' selected' : '') + '>' + m + '</option>'; }).join(''); });
  function sum(a) { return a.reduce(function (x, y) { return x + y; }, 0); }
  function svgEl(t, a) { var e = document.createElementNS('http://www.w3.org/2000/svg', t); for (var k in a) e.setAttribute(k, a[k]); return e; }
  function render() {
    var f = facSel.value, a = +from.value, b = +to.value; if (b < a) { b = a; to.value = b; }
    var mode = view.value;
    if (mode === 'nurse' && f === 'all') { f = '0'; facSel.value = '0'; }
    facSel.disabled = mode === 'donor';
    var rows = data.filter(function (d, i) { return f === 'all' || +f === i || mode === 'donor'; });
    var span = b - a + 1;
    var doses = sum(rows.map(function (d) { return sum(d.m.slice(a, b + 1)); }));
    var tgt = sum(rows.map(function (d) { return d.target * span; }));
    var cov = Math.round(doses / tgt * 100);
    var low = rows.filter(function (d) { return sum(d.m.slice(a, b + 1)) / (d.target * span) < 0.8; }).length;
    var k = [['Doses given', doses], ['Coverage', cov + '%'], ['Facilities below 80%', low], ['Months shown', span]];
    $('dKpis').innerHTML = k.map(function (x) { return '<div class="kpi"><span>' + x[0] + '</span><strong>' + x[1] + '</strong></div>'; }).join('');
    // trend
    var t = $('dTrend'); t.innerHTML = '';
    var series = []; for (var i = a; i <= b; i++) series.push(sum(rows.map(function (d) { return d.m[i]; })));
    var max = Math.max.apply(null, series) * 1.15 || 1, W = 600, H = 260, p = 36;
    var pts = series.map(function (v, i) { return [p + (series.length > 1 ? i * (W - 2 * p) / (series.length - 1) : (W - 2 * p) / 2), H - p - v / max * (H - 2 * p)]; });
    t.appendChild(svgEl('line', { x1: p, y1: H - p, x2: W - p, y2: H - p, stroke: 'currentColor', 'stroke-opacity': .3 }));
    t.appendChild(svgEl('polyline', { points: pts.map(function (q) { return q.join(','); }).join(' '), fill: 'none', stroke: 'var(--green)', 'stroke-width': 3 }));
    pts.forEach(function (q, i) {
      var c = svgEl('circle', { cx: q[0], cy: q[1], r: 4, fill: 'var(--green)' }); var tt = svgEl('title', {}); tt.textContent = months[a + i] + ': ' + series[i]; c.appendChild(tt); t.appendChild(c);
      var l = svgEl('text', { x: q[0], y: H - 12, 'text-anchor': 'middle', 'font-size': 11, fill: 'currentColor' }); l.textContent = months[a + i]; t.appendChild(l);
    });
    // bars
    var s = $('dBars'); s.innerHTML = '';
    var all = data.map(function (d) { return { n: d.name, c: Math.round(sum(d.m.slice(a, b + 1)) / (d.target * span) * 100) }; });
    var bw = (W - 2 * p) / all.length;
    var y90 = H - p - 90 / 120 * (H - 2 * p);
    all.forEach(function (d, i) {
      var h = Math.min(d.c, 120) / 120 * (H - 2 * p);
      var r = svgEl('rect', { x: p + i * bw + 10, y: H - p - h, width: bw - 20, height: h, rx: 4, fill: d.c >= 90 ? 'var(--green)' : d.c >= 80 ? 'var(--amber)' : 'var(--blue)' });
      var tt = svgEl('title', {}); tt.textContent = d.n + ': ' + d.c + '%'; r.appendChild(tt); s.appendChild(r);
      var l = svgEl('text', { x: p + i * bw + bw / 2, y: H - 12, 'text-anchor': 'middle', 'font-size': 10.5, fill: 'currentColor' }); l.textContent = d.n.replace('Sample ', ''); s.appendChild(l);
      var v = svgEl('text', { x: p + i * bw + bw / 2, y: H - p - h - 6, 'text-anchor': 'middle', 'font-size': 11, fill: 'currentColor' }); v.textContent = d.c + '%'; s.appendChild(v);
    });
    s.appendChild(svgEl('line', { x1: p, y1: y90, x2: W - p, y2: y90, stroke: 'currentColor', 'stroke-dasharray': '5 4', 'stroke-opacity': .6 }));
    // table
    var tbl = $('dTable');
    if (mode === 'donor') { tbl.innerHTML = '<caption class="sr-only">Summary</caption><tr><th>Programme</th><th>Doses</th><th>Coverage</th></tr><tr><td>All sample facilities</td><td>' + doses + '</td><td>' + cov + '%</td></tr>'; return; }
    tbl.innerHTML = '<caption class="sr-only">Facility summary</caption><tr><th>Facility</th><th>Doses</th><th>Target</th><th>Coverage</th></tr>' + rows.map(function (d) {
      var x = sum(d.m.slice(a, b + 1)), tg = d.target * span, c = Math.round(x / tg * 100);
      return '<tr><td>' + d.name + '</td><td>' + x + '</td><td>' + tg + '</td><td>' + c + '%</td></tr>'; }).join('');
  }
  [facSel, from, to, view].forEach(function (e) { e.addEventListener('change', render); });
  render();
})();
'''
    open(os.path.join(OUT, 'demo.js'), 'w', encoding='utf-8').write(js)


# ------------------------------------------------------------------ now, glossary, request, privacy, offline
def now():
    body = head('What I am doing now', 'A short, honest snapshot. Last reviewed: October 2026.') + '''
<section class="section"><div class="wrap prose">
  <ul class="bullets">
    <li><strong>Work:</strong> managing immunisation, home visit and malaria data at RHCI, and supporting the field teams who use the Survey123 forms.</li>
    <li><strong>Studying:</strong> Computer Science.</li>
    <li><strong>Building:</strong> reusable dashboard and data quality templates for health programmes.</li>
    <li><strong>Open to:</strong> consulting, short contracts and full-time roles in M&amp;E and health data.</li>
  </ul>
  <p>This page is inspired by the <a href="https://nownownow.com/about" target="_blank" rel="noopener">now page movement</a>.</p>
</div></section>''' + cta('Working on something similar?', 'Tell me about it.')
    page('now.html', 'Now | Alhaji Ibrahim Mehemoh', 'What Alhaji Ibrahim Mehemoh is working on and studying now.', body, crumbs=[('Now', None)])


GLOSSARY = [
    ('CHW', 'Community Health Worker. A trained community member who delivers basic health services and refers people to facilities.'),
    ('DHIS2', 'District Health Information Software 2. An open source platform many countries use to collect and analyse routine health data.'),
    ('DHMT', 'District Health Management Team. The group that manages health services in a district.'),
    ('EPI', 'Expanded Programme on Immunization. The programme that delivers routine childhood vaccines.'),
    ('HMIS', 'Health Management Information System. The routine system for collecting health facility data.'),
    ('KPI', 'Key Performance Indicator. A measure used to track progress toward a goal.'),
    ('M&E', 'Monitoring and Evaluation. Tracking activities during a programme and judging its results afterwards.'),
    ('MMS', 'Multiple Micronutrient Supplements, given to pregnant women to support health.'),
    ('PHC', 'Primary Health Care. First-level facilities such as community health posts and centres.'),
    ('Survey123', 'An ArcGIS tool for building forms that collect data on phones and tablets, including offline.'),
    ('XLSForm', 'A standard for writing forms in a spreadsheet. Works with Survey123, KoboToolbox and ODK.'),
    ('Data quality', 'How complete, timely, accurate and consistent data is. See the free checklist on the resources page.'),
]


def glossary():
    items = ''.join(f'<dt id="{esc(t.lower().replace(" ", "-").replace("&", ""))}">{esc(t)}</dt><dd>{esc(d)}</dd>' for t, d in GLOSSARY)
    ld = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Health data glossary",
          "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    body = head('Glossary', 'Plain-language definitions of terms used in health data and M&E work.') + f'<section class="section"><div class="wrap prose"><dl class="glossary">{items}</dl></div></section>'
    page('glossary.html', 'Glossary of health data terms | Alhaji Ibrahim Mehemoh',
         'Plain-language definitions of EPI, CHW, DHMT, M&E, HMIS, XLSForm and other health data terms.', body, ld=ld, crumbs=[('Glossary', None)])


def request():
    body = head('Request a quote', 'Tell me what you need. I reply with a plan and a quote, usually within a day. Do not include patient or staff names.') + f'''
<section class="section"><div class="wrap narrow">
  <form {form_attrs()} id="requestForm">
    <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
    <input type="hidden" name="_subject" value="Quote request from website">
    <div class="field"><label for="rq-name">Your name</label><input id="rq-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="rq-email">Your email</label><input id="rq-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="rq-wa">WhatsApp number (optional)</label><input id="rq-wa" name="whatsapp" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="rq-service">Service</label>
      <select id="rq-service" name="service">
        <optgroup label="Data and M&amp;E"><option>Dashboards and reports</option><option>Survey and form design</option><option>Data quality audits</option><option>M&amp;E reporting</option><option>Data systems</option><option>Training</option></optgroup>
        <optgroup label="IT support"><option>Technical support and hardware</option><option>Networking and internet</option><option>Web and digital</option><option>Security and backups</option><option>Office and NGO IT support</option><option>IT support (Starter)</option><option>IT support (Standard)</option><option>IT support (Premium)</option></optgroup>
        <option>Something else</option>
      </select></div>
    <div class="field"><label for="rq-budget">Budget range</label>
      <select id="rq-budget" name="budget"><option>Not sure yet</option><option>Under SLE 5,000</option><option>SLE 5,000 to 20,000</option><option>SLE 20,000 to 50,000</option><option>Over SLE 50,000</option></select></div>
    <div class="field"><label for="rq-deadline">Deadline</label><input id="rq-deadline" name="deadline" type="date"></div>
    <div class="field"><label for="rq-details">What do you need?</label><textarea id="rq-details" name="details" rows="6" required></textarea></div>
    <button class="btn btn-primary" type="submit">Send request</button>
    <p class="small muted" id="formStatus" role="status" aria-live="polite" style="margin-top:.75rem"></p>
  </form>
</div></section>'''
    page('request.html', 'Request a quote | Alhaji Ibrahim Mehemoh',
         'Request a quote for a dashboard, data collection form, M&E support, training or IT support from Alhaji Ibrahim Mehemoh.',
         body, crumbs=[('Request a quote', None)])


def privacy():
    an = {'goatcounter': 'GoatCounter', 'plausible': 'Plausible'}.get(C.ANALYTICS_PROVIDER, '')
    analytics = (f'<p>This site uses {an}, a privacy-friendly analytics service. It does not use cookies and does not track you across sites.</p>'
                 if an else '<p>This site does not currently use analytics.</p>')
    form = ('<p>When you send a form, your message goes to me through Formspree. I use it only to reply to you.</p>' if C.FORMSPREE_ID
            else '<p>When you use a form, your message is opened in WhatsApp so you can send it to me. Nothing is stored by this site.</p>')
    body = head('Privacy', 'Short version: I collect very little and I do not use cookies.') + f'''
<section class="section"><div class="wrap prose">
  <h2>Cookies</h2><p>This site sets no cookies. It remembers your theme choice in your own browser (local storage), and nowhere else.</p>
  <h2>Analytics</h2>{analytics}
  <h2>Forms</h2>{form}
  <h2>External links</h2><p>Links to WhatsApp, YouTube and other sites follow those sites&rsquo; own privacy rules. Embedded videos use the no-cookie YouTube domain.</p>
  <h2>Your data</h2><p>To ask me to delete anything you sent me, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>'''
    page('privacy.html', 'Privacy | Alhaji Ibrahim Mehemoh', 'Privacy notice: no cookies, minimal data, privacy-friendly analytics.', body, crumbs=[('Privacy', None)])


def offline():
    body = head('You are offline', 'This page is not saved on your device yet. Pages you have visited before still work. Reconnect and try again.',
                '<p><a class="btn btn-primary" href="index.html">Go to the home page</a></p>')
    page('offline.html', 'Offline | Alhaji Ibrahim Mehemoh', 'Offline page.', body, noindex=True, sitemap=False)


# ------------------------------------------------------------------ capability statement and CV
def capability():
    body = f'''<div class="wrap doc">
  <div class="doc-actions no-print"><button class="btn btn-primary" type="button" data-print>Print or save as PDF</button> <a class="btn" href="capability-statement.pdf" download>Download PDF</a></div>
  <header class="doc-head"><h1>Alhaji Ibrahim Mehemoh</h1><p>Data Officer and M&amp;E specialist &middot; Bo, Sierra Leone</p>
  <p>{EMAIL} &middot; WhatsApp +232 79 301 430 &middot; alhajiimehemoh.github.io</p></header>
  <h2>What I do</h2><p>I turn field data into decisions for health programmes: mobile data collection, dashboards, data quality and M&amp;E reporting.</p>
  <h2>Core services</h2><ul class="bullets"><li>Survey123 and XLSForm data collection design</li><li>Power BI and Excel dashboards</li><li>Data quality reviews and indicator reporting</li><li>Health data systems (PostgreSQL, Flask, Google Apps Script)</li><li>Staff training in Excel and data skills</li><li>Office IT, networks and cybersecurity basics</li></ul>
  <h2>Recent work</h2><ul class="bullets"><li>EPI reporting dashboard in Power BI</li><li>Survey123 forms for hospitalisation notification and field tools</li><li>CHW Card Studio, a card issuing tool</li><li>An 11-module data management system for vaccine and programme data</li></ul>
  <h2>Experience</h2><ul class="bullets"><li>Evaluator and Data Officer, Rural Health Care Initiative (RHCI), Oct 2024 to present</li><li>Assistant IT Manager, SLIEPA, 2023 to 2024</li><li>IT and Data Officer, SLPP, Bo District, 2022 to 2023</li><li>ICT Tutor, Growth Centre, Bo, 2016 to 2021</li></ul>
  <h2>Working terms</h2><p>Consulting, contract and full-time. Languages: English and Krio. Available onsite in Bo and remotely.</p>
</div>'''
    page('capability-statement.html', 'Capability statement | Alhaji Ibrahim Mehemoh', 'One-page capability statement for Alhaji Ibrahim Mehemoh, health data and M&E specialist.',
         body, crumbs=[('Capability statement', None)], progress=False)


def cv():
    body = f'''<div class="wrap doc">
  <div class="doc-actions no-print"><button class="btn btn-primary" type="button" data-print>Print or save as PDF</button> <a class="btn" href="{CV}" download>Download my formal CV</a></div>
  <header class="doc-head"><h1>Alhaji Ibrahim Mehemoh</h1><p>Data Officer and M&amp;E specialist &middot; Bo, Sierra Leone &middot; {EMAIL} &middot; +232 79 301 430</p></header>
  <h2>Profile</h2><p>Data Officer managing immunisation, home visit and malaria data for a health NGO. Builds Survey123 forms, Power BI dashboards and data quality processes. Works in English and Krio.</p>
  <h2>Experience</h2>
  <p><strong>Evaluator and Data Officer, RHCI, Tikonko</strong>, Oct 2024 to present. Health data systems, CHW database management, dashboards, mobile data collection and M&amp;E reporting.</p>
  <p><strong>Assistant IT Manager, SLIEPA, Freetown</strong>, Sep 2023 to Oct 2024. IT infrastructure, helpdesk, cybersecurity and staff ICT training.</p>
  <p><strong>IT and Data Officer, SLPP, Bo District</strong>, Jan 2022 to Sep 2023. Membership databases, data analysis and digital campaigns.</p>
  <p><strong>ICT Tutor, Growth Centre, Bo</strong>, 2016 to 2021. Taught Microsoft Office to more than 200 students; hardware and network troubleshooting.</p>
  <h2>Education</h2><ul class="bullets"><li>BSc Computer Science (in progress)</li><li>Diplomas in Networking, Hardware and Software, Growth Centre Computer Training Institute, 2015 to 2019</li></ul>
  <h2>Skills</h2><p>Power BI, Excel, Survey123, XLSForm, data cleaning and quality checks, PostgreSQL, Flask, Google Apps Script, networking, WordPress, staff training.</p>
</div>'''
    page('cv.html', 'Web CV | Alhaji Ibrahim Mehemoh', 'Web and printable CV of Alhaji Ibrahim Mehemoh, generated from the content of this site.',
         body, crumbs=[('Web CV', None)], progress=False)


# ------------------------------------------------------------------ admin note composer
def admin():
    cats = ['Health data', 'IT support', 'Career', 'Cybersecurity']
    opts = ''.join(f'<option>{c}</option>' for c in cats)
    body = head('Note composer', 'For my own use. Write a note, copy the JSON, paste it into notes.json, then rebuild. Nothing is saved or sent from this page.') + f'''
<section class="section"><div class="wrap narrow">
  <div class="field"><label for="n-title">Title</label><input id="n-title"></div>
  <div class="field"><label for="n-summary">One-sentence summary</label><input id="n-summary"></div>
  <div class="field"><label for="n-cat">Category</label><select id="n-cat">{opts}</select></div>
  <div class="field"><label for="n-date">Date</label><input id="n-date" type="date"></div>
  <div class="field"><label for="n-body">Body (use ## for headings and - for bullets)</label><textarea id="n-body" rows="12"></textarea></div>
  <button class="btn btn-primary" type="button" id="n-make">Make JSON</button>
  <div class="field" style="margin-top:1rem"><label for="n-out">Paste this into notes.json</label><textarea id="n-out" rows="10" readonly></textarea></div>
  <button class="btn" type="button" id="n-copy">Copy</button>
</div></section>
<script>
(function(){{var g=function(i){{return document.getElementById(i)}};
g('n-make').onclick=function(){{var t=g('n-title').value.trim();var slug='note-'+t.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
g('n-out').value=JSON.stringify({{slug:slug,title:t,summary:g('n-summary').value.trim(),category:g('n-cat').value,date:g('n-date').value,body:g('n-body').value.trim()}},null,2)+',';}};
g('n-copy').onclick=function(){{g('n-out').select();try{{navigator.clipboard.writeText(g('n-out').value)}}catch(e){{document.execCommand('copy')}}}};}})();
</script>'''
    page('admin.html', 'Note composer', 'Private note composer.', body, noindex=True, sitemap=False, progress=False)



FEED_XSL = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>RSS feed: <xsl:value-of select="rss/channel/title"/></title>
<link rel="icon" href="images/favicon-32.png" type="image/png"/>
<style>
@font-face{font-family:'Bricolage Grotesque';font-weight:200 800;font-display:swap;src:url(fonts/bricolage-grotesque-latin-var.woff2) format('woff2')}
@font-face{font-family:'DM Sans';font-weight:100 1000;font-display:swap;src:url(fonts/dm-sans-latin-var.woff2) format('woff2')}
@font-face{font-family:'JetBrains Mono';font-weight:500;font-display:swap;src:url(fonts/jetbrains-mono-latin-500-normal.woff2) format('woff2')}
:root{--paper:#F3F6F4;--sheet:#fff;--ink:#0F2430;--muted:#475D68;--rule:#D3DED9;--green:#0B7A5C;--green-soft:#DDF0E8;--amber:#D68A00}
@media (prefers-color-scheme:dark){:root{--paper:#0A171D;--sheet:#112630;--ink:#E7EFEC;--muted:#A3B6BD;--rule:#25404B;--green:#3CC79A;--green-soft:#12372F}}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(50rem 24rem at 85% -10%,rgba(11,122,92,.14),transparent 70%),var(--paper);color:var(--ink);font:400 1.0625rem/1.65 'DM Sans',system-ui,sans-serif}
.bar{position:sticky;top:0;background:color-mix(in srgb,var(--paper) 85%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--rule)}
.bar .in{width:min(64rem,100% - 2rem);margin:0 auto;display:flex;align-items:center;gap:.7rem;min-height:4rem}
.bar img{height:26px}.bar b{font-family:'Bricolage Grotesque',sans-serif;font-weight:750;letter-spacing:-.02em}
.bar a{color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:.6rem}.bar .r{margin-left:auto;font-weight:600;color:var(--green)}
.wrap{width:min(64rem,100% - 2rem);margin:0 auto;padding:3rem 0 4rem}
h1,h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;letter-spacing:-.035em;line-height:1.02}
h1{font-size:clamp(2.2rem,6vw,3.6rem);margin:.6rem 0 .8rem}
.tag{display:inline-flex;align-items:center;gap:.4rem;font:500 .75rem 'JetBrains Mono',monospace;background:var(--green-soft);color:var(--green);padding:.3rem .7rem;border-radius:999px}
.box{display:flex;gap:1rem;align-items:center;flex-wrap:wrap;background:var(--sheet);border:1.5px solid var(--rule);border-radius:18px;padding:1rem 1.2rem;margin:1.5rem 0 2.5rem;box-shadow:0 22px 44px -18px rgba(15,36,48,.28)}
.box p{margin:0;flex:1;min-width:16rem}.muted{color:var(--muted)}
code{display:block;margin-top:.4rem;font:500 .9rem 'JetBrains Mono',monospace;word-break:break-all;color:var(--green)}
.btn{display:inline-block;padding:.8rem 1.3rem;border-radius:999px;background:var(--green);color:#fff;font-weight:600;text-decoration:none}
a{color:var(--green);text-underline-offset:3px}
ol{list-style:none;margin:0;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(18rem,1fr))}
li{background:var(--sheet);border:1px solid var(--rule);border-radius:20px;padding:1.2rem 1.3rem;display:flex;flex-direction:column;gap:.4rem;transition:transform .25s,box-shadow .25s}
li:hover{transform:translateY(-4px);box-shadow:0 22px 44px -18px rgba(15,36,48,.28)}
li h2{font-size:1.15rem;margin:0;letter-spacing:-.02em;line-height:1.25}li h2 a{color:var(--ink);text-decoration:none}li h2 a:hover{color:var(--green)}
li p{margin:0;color:var(--muted);font-size:.93rem}.meta{font:500 .72rem 'JetBrains Mono',monospace;color:var(--muted)}
.cat{align-self:flex-start;font:500 .7rem 'JetBrains Mono',monospace;color:var(--green);background:var(--green-soft);padding:.2rem .55rem;border-radius:999px}
</style></head>
<body>
<div class="bar"><div class="in"><a href="index.html"><img src="images/brand/logo-mark.png" alt=""/><b>Alhaji Ibrahim Mehemoh</b></a><a class="r" href="community.html">All notes</a></div></div>
<div class="wrap">
<span class="tag">RSS feed</span>
<h1><xsl:value-of select="rss/channel/title"/></h1>
<p class="muted"><xsl:value-of select="rss/channel/description"/></p>
<div class="box"><p><strong>This is a feed you can follow.</strong> Copy this page address into a feed reader such as Feedly, Inoreader or NetNewsWire, and new notes arrive automatically.<code>{BASE}feed.xml</code></p><a class="btn" href="rss.html">How to follow</a></div>
<ol>
<xsl:for-each select="rss/channel/item">
<li><span class="cat"><xsl:value-of select="category"/></span>
<h2><a href="{link}"><xsl:value-of select="title"/></a></h2>
<p><xsl:value-of select="description"/></p>
<span class="meta"><xsl:value-of select="substring(pubDate,6,11)"/></span></li>
</xsl:for-each>
</ol>
</div></body></html>
</xsl:template>
</xsl:stylesheet>
"""

# ------------------------------------------------------------------ feed, sitemap, pwa
def feed(notes):
    items = ''
    for n in sorted(notes, key=lambda n: n.get('date') or '', reverse=True):
        pub = ''
        if n.get('date'):
            d = datetime.date.fromisoformat(n['date'])
            pub = '<pubDate>%s</pubDate>' % d.strftime('%a, %d %b %Y 08:00:00 +0000')
        items += f'<item><title>{esc(n["title"])}</title><link>{BASE}{n["fn"]}</link><guid>{BASE}{n["fn"]}</guid><category>{esc(n["category"])}</category>{pub}<description>{esc(n["summary"])}</description></item>\n'
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="feed.xsl"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Notes by Alhaji Ibrahim Mehemoh</title><link>{BASE}community.html</link>
<atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>
<description>Practical posts on health data, IT and cybersecurity.</description><language>en</language>
<image><url>{BASE}images/apple-touch-icon.png</url><title>Notes by Alhaji Ibrahim Mehemoh</title><link>{BASE}community.html</link></image>
{items}</channel></rss>
'''
    open(os.path.join(OUT, 'feed.xml'), 'w', encoding='utf-8').write(xml)
    open(os.path.join(OUT, 'feed.xsl'), 'w', encoding='utf-8').write(FEED_XSL.replace('{BASE}', BASE))


def sitemap(today):
    urls = ''.join(f'  <url><loc>{BASE if fn == "index.html" else BASE + fn}</loc><lastmod>{today}</lastmod></url>\n' for fn in sorted(set(PAGES)))
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8').write(
        f'User-agent: *\nAllow: /\nDisallow: /admin.html\n\nSitemap: {BASE}sitemap.xml\n')


def pwa(today):
    man = {"name": "Alhaji Ibrahim Mehemoh", "short_name": "Alhaji", "description": "Health data and M&E specialist, Bo, Sierra Leone.",
           "start_url": "./index.html", "scope": "./", "display": "standalone", "background_color": "#F3F6F4", "theme_color": "#0F2430",
           "icons": [{"src": "images/icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "images/icon-512.png", "sizes": "512x512", "type": "image/png"},
                     {"src": "images/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}
    json.dump(man, open(os.path.join(OUT, 'manifest.webmanifest'), 'w'), indent=2)
    core = sorted(set(PAGES + ['offline.html', 'style.css?v=' + CSS_V, 'shared.js?v=' + CSS_V, 'demo.js?v=' + CSS_V, 'manifest.webmanifest',
                               'images/favicon-32.png', 'fonts/bricolage-grotesque-latin-var.woff2', 'fonts/dm-sans-latin-var.woff2']))
    sw = '''const VERSION = 'v%s-%s';
const CORE = %s;
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
''' % (CSS_V, today.replace('-', ''), json.dumps(core))
    open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8').write(sw)


KRIO = {
    "nav.projects": "Wok dɛm", "nav.services": "Sɛvis dɛm", "nav.resources": "Tin dɛm fɔ yuz", "nav.notes": "Nōt dɛm",
    "nav.about": "Bɔt mi", "nav.hire": "Contract mi", "nav.contact": "Tɔk to mi",
    "hero.projects": "Si di wok dɛm", "hero.contact": "Tɔk to mi", "hero.cv": "Dawnload mi CV (PDF)"
}


def build_all(notes, today):
    # Downloads are built separately: python3 tools/make_resources.py
    for f in (resources, demo, now, glossary, request, privacy, offline, capability, cv, admin):
        f()
    json.dump(KRIO, open(os.path.join(OUT, 'lang', 'kri.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    feed(notes)
    sitemap(today)
    pwa(today)
