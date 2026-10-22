"""Branded PDF resources. One shared template: green header band, title block, section cards, footer.
All content is general guidance or blank templates. Worked examples are labelled as examples."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, PageBreak, Flowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, 'tools', 'fonts')
for n in ['DMSans-400', 'DMSans-700', 'Bricolage-800', 'JetBrainsMono-500']:
    pdfmetrics.registerFont(TTFont(n, os.path.join(FD, n + '.ttf')))
pdfmetrics.registerFontFamily('DMSans', normal='DMSans-400', bold='DMSans-700', italic='DMSans-400', boldItalic='DMSans-700')

INK = colors.HexColor('#0F2430'); GREEN = colors.HexColor('#0B7A5C'); SOFT = colors.HexColor('#DDF0E8')
AMBER = colors.HexColor('#D68A00'); AMBER_SOFT = colors.HexColor('#FBEBC8'); MUTED = colors.HexColor('#475D68')
RULE = colors.HexColor('#D3DED9'); PAPER = colors.HexColor('#F3F6F4'); WHITE = colors.white
SITE = 'alhajiimehemoh.github.io'
W, H = A4
M = 16 * mm

S = {
    'body': ParagraphStyle('body', fontName='DMSans-400', fontSize=9.6, leading=13.6, textColor=INK),
    'small': ParagraphStyle('small', fontName='DMSans-400', fontSize=8.4, leading=11.5, textColor=MUTED),
    'lede': ParagraphStyle('lede', fontName='DMSans-400', fontSize=11, leading=15.5, textColor=MUTED),
    'h2': ParagraphStyle('h2', fontName='Bricolage-800', fontSize=13, leading=16, textColor=INK, spaceBefore=4, spaceAfter=6),
    'cell': ParagraphStyle('cell', fontName='DMSans-400', fontSize=9, leading=12.2, textColor=INK),
    'cellb': ParagraphStyle('cellb', fontName='DMSans-700', fontSize=9, leading=12.2, textColor=INK),
    'cellw': ParagraphStyle('cellw', fontName='DMSans-700', fontSize=9, leading=12, textColor=WHITE),
    'mono': ParagraphStyle('mono', fontName='JetBrainsMono-500', fontSize=8.2, leading=11.2, textColor=INK),
    'label': ParagraphStyle('label', fontName='JetBrainsMono-500', fontSize=7.4, leading=10, textColor=GREEN),
    'tip': ParagraphStyle('tip', fontName='DMSans-400', fontSize=9, leading=12.6, textColor=INK),
}


class Box(Flowable):
    """Empty tick box."""
    def __init__(self, size=9):
        super().__init__(); self.size = size; self.width = size; self.height = size
    def draw(self):
        self.canv.setStrokeColor(GREEN); self.canv.setLineWidth(1.1); self.canv.roundRect(0, 0, self.size, self.size, 2, stroke=1, fill=0)


class Lines(Flowable):
    """Ruled writing lines."""
    def __init__(self, n=3, gap=7 * mm):
        super().__init__(); self.n = n; self.gap = gap
    def wrap(self, aw, ah):
        self.width = aw; self.height = self.n * self.gap; return aw, self.height
    def draw(self):
        c = self.canv; c.setStrokeColor(RULE); c.setLineWidth(.6)
        for i in range(self.n):
            y = self.height - (i + 1) * self.gap + 2
            c.line(0, y, self.width, y)


def _page(meta):
    def draw(c, doc):
        c.saveState()
        # header band
        c.setFillColor(GREEN); c.rect(0, H - 14 * mm, W, 14 * mm, stroke=0, fill=1)
        c.setFillColor(AMBER); c.rect(0, H - 14 * mm - 1.2 * mm, 34 * mm, 1.2 * mm, stroke=0, fill=1)
        c.setFillColor(WHITE); c.setFont('Bricolage-800', 10.5); c.drawString(M, H - 8.8 * mm, 'Alhaji Ibrahim Mehemoh')
        c.setFont('JetBrainsMono-500', 7.6); c.drawRightString(W - M, H - 8.8 * mm, meta['category'].upper() + '  ·  FREE RESOURCE')
        # footer
        c.setStrokeColor(RULE); c.setLineWidth(.6); c.line(M, 13 * mm, W - M, 13 * mm)
        c.setFillColor(MUTED); c.setFont('DMSans-400', 7.6)
        c.drawString(M, 8.5 * mm, 'Free to use and adapt. Please keep this credit line.  ·  ' + SITE)
        c.setFont('JetBrainsMono-500', 7.6); c.drawRightString(W - M, 8.5 * mm, '%s  ·  page %d' % (meta['short'], doc.page))
        c.restoreState()
    return draw


def _title(meta):
    t = [Spacer(1, 4 * mm),
         Paragraph(meta['kicker'].upper(), S['label']), Spacer(1, 2.2 * mm),
         Paragraph(meta['title'], ParagraphStyle('t', fontName='Bricolage-800', fontSize=24, leading=27, textColor=INK)),
         Spacer(1, 2.5 * mm), Paragraph(meta['lede'], S['lede']), Spacer(1, 4 * mm)]
    if meta.get('fields'):
        cells = [[Paragraph(f.upper(), S['label']) for f in meta['fields']], ['' for _ in meta['fields']]]
        tb = Table(cells, colWidths=[(W - 2 * M) / len(meta['fields'])] * len(meta['fields']), rowHeights=[5 * mm, 8 * mm])
        tb.setStyle(TableStyle([('LINEBELOW', (0, 1), (-1, 1), .8, RULE), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 8), ('VALIGN', (0, 0), (-1, -1), 'BOTTOM')]))
        t += [tb, Spacer(1, 5 * mm)]
    return t


def _doc(path, meta, story):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=20 * mm, bottomMargin=18 * mm,
                          title=meta['title'], author='Alhaji Ibrahim Mehemoh', subject=meta['lede'], creator=SITE)
    fr = Frame(M, 18 * mm, W - 2 * M, H - 38 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='p', frames=[fr], onPage=_page(meta))])
    doc.build(_title(meta) + story)


def checklist_group(title, items, n=None):
    """A section card: coloured title bar, rows with tick box, item, Yes/No/NA."""
    head = [Paragraph(('<font name="JetBrainsMono-500" color="#B7E4D3">%02d</font>&nbsp;&nbsp;' % n if n else '') + title, S['cellw']), '', '']
    rows = [head] + [[Box(), Paragraph(i, S['cell']), Paragraph('Yes&nbsp;&nbsp;No&nbsp;&nbsp;N/A', S['small'])] for i in items]
    t = Table(rows, colWidths=[9 * mm, None, 24 * mm])
    t.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)), ('BACKGROUND', (0, 0), (-1, 0), GREEN),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, PAPER]),
        ('LINEBELOW', (0, 1), (-1, -1), .4, RULE), ('BOX', (0, 0), (-1, -1), .6, RULE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    return KeepTogether([t, Spacer(1, 4.5 * mm)])


def tip(text, title='Tip'):
    t = Table([[Paragraph('<b>%s.</b> %s' % (title, text), S['tip'])]], colWidths=[W - 2 * M])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), AMBER_SOFT), ('LINEBEFORE', (0, 0), (0, -1), 3, AMBER),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10), ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    return KeepTogether([t, Spacer(1, 4.5 * mm)])


def kv_table(rows, head=None, widths=(48 * mm, None), mono_first=False, zebra=True):
    data = []
    if head:
        data.append([Paragraph(h, S['cellw']) for h in head])
    for r in rows:
        data.append([Paragraph(str(r[0]), S['mono'] if mono_first else S['cellb'])] + [Paragraph(str(x), S['cell']) for x in r[1:]])
    t = Table(data, colWidths=list(widths), repeatRows=1 if head else 0)
    st = [('BOX', (0, 0), (-1, -1), .6, RULE), ('LINEBELOW', (0, 0), (-1, -1), .4, RULE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5), ('LEFTPADDING', (0, 0), (-1, -1), 7),
          ('ROUNDEDCORNERS', [6, 6, 6, 6])]
    if head:
        st += [('BACKGROUND', (0, 0), (-1, 0), INK)]
    if zebra:
        st += [('ROWBACKGROUNDS', (0, 1 if head else 0), (-1, -1), [WHITE, PAPER])]
    t.setStyle(TableStyle(st))
    return t


def write_table(head, nrows, widths, h=8.5 * mm):
    data = [[Paragraph(x, S['cellw']) for x in head]] + [['' for _ in head] for _ in range(nrows)]
    t = Table(data, colWidths=widths, rowHeights=[None] + [h] * nrows, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), INK), ('GRID', (0, 0), (-1, -1), .4, RULE),
                           ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, PAPER]), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 6), ('TOPPADDING', (0, 0), (-1, 0), 5), ('BOTTOMPADDING', (0, 0), (-1, 0), 5)]))
    return t


def sign_off(labels=('Checked by', 'Role', 'Date', 'Signature')):
    return [Spacer(1, 3 * mm), Paragraph('Sign-off', S['h2']),
            write_table(list(labels), 1, [(W - 2 * M) / len(labels)] * len(labels), h=12 * mm)]


# ====================================================================== the resources
PDFS = []


def resource(**meta):
    def wrap(fn):
        meta['build'] = fn; PDFS.append(meta); return fn
    return wrap


@resource(file='me-data-quality-checklist.pdf', short='Data quality checklist', category='M&E', kicker='Checklist · run monthly',
          title='M&amp;E data quality checklist', fields=['Programme', 'Reporting month', 'Dataset or form'],
          lede='Run this before every monthly report leaves your desk. Tick each line. Any "No" needs a short note and a named person to fix it.',
          blurb='Completeness, timeliness, accuracy, consistency, duplicates and privacy, on one sheet you run before every report.',
          tags=['Checklist', 'Monthly'])
def _dq():
    g = [
        ('Completeness', ['Every facility or team expected to report has reported', 'No blank required fields in the dataset', 'Zero values are entered as 0, not left empty', 'Missing reports are listed with a reason']),
        ('Timeliness', ['Reports arrived by the agreed deadline', 'The reporting period on each form is correct', 'Late reports are flagged and followed up']),
        ('Accuracy', ['Totals equal the sum of their parts', 'Values do not exceed the target population without an explanation', 'A sample of facilities was checked against the paper register', 'Dates are valid and not in the future']),
        ('Consistency', ['Every site uses the same indicator definitions', 'This month is compared with last month and large changes are explained', 'Units, codes and date formats are the same everywhere', 'Village and facility names match the master list']),
        ('Duplicates and outliers', ['No duplicate rows or repeated submissions', 'Extreme values were confirmed with the facility', 'GPS points fall inside the expected district', 'Every correction is logged: who, what, when']),
        ('Privacy and storage', ['No names, phone numbers or ID numbers in shared files', 'Raw data is backed up in two places', 'Files are named with site, month and version']),
    ]
    out = [checklist_group(t, i, n + 1) for n, (t, i) in enumerate(g)]
    out.append(tip('Keep a simple data cleaning log next to this checklist. When a manager asks "why did this number change?", the log answers in seconds.'))
    return out + sign_off()


@resource(file='indicator-reference-sheet.pdf', short='Indicator reference sheet', category='M&E', kicker='Template · one per indicator',
          title='Indicator reference sheet', fields=['Programme', 'Indicator code', 'Version'],
          lede='Write one sheet for every indicator you report, so everyone counts the same thing the same way. Page 1 is a worked example. Page 2 is blank.',
          blurb='Define each indicator once: numerator, denominator, source, frequency and limits. Includes a worked example and a blank sheet.',
          tags=['Template', 'Worked example'])
def _pirs():
    rows = [
        ('Indicator name', 'Percentage of children under 1 who received the third dose of pentavalent vaccine (Penta 3)'),
        ('Why it matters', 'Shows whether infants complete the primary vaccination series, not just start it.'),
        ('Numerator', 'Number of children under 1 year given Penta 3 during the reporting period'),
        ('Denominator', 'Estimated number of surviving infants (target population) for the same period and area'),
        ('Unit', 'Percentage (numerator ÷ denominator × 100)'),
        ('Disaggregation', 'Facility, chiefdom, district, month; fixed post or outreach'),
        ('Data source', 'Facility immunisation register and monthly summary form'),
        ('Collection method', 'Facility staff tally doses daily and complete the monthly summary'),
        ('Frequency', 'Monthly, with quarterly review'),
        ('Responsible', 'Facility in-charge (collection); programme data officer (checking and reporting)'),
        ('Baseline and target', 'Baseline value, year and source; target value and year'),
        ('Known limitations', 'Denominators are estimates, so coverage can exceed 100%. Doses given to children from outside the catchment area inflate the numerator.'),
        ('How the data is used', 'Monthly review meetings to plan outreach and follow up defaulters'),
    ]
    out = [Paragraph('Worked example (illustrative wording, not official national guidance)', S['h2']),
           kv_table(rows, widths=(42 * mm, None)), Spacer(1, 4 * mm),
           tip('If two people could count the same thing differently, the definition is not finished yet.'), PageBreak(),
           Paragraph('Blank sheet', S['h2'])]
    blank = [(r[0], '') for r in rows]
    t = Table([[Paragraph(k, S['cellb']), ''] for k, _ in blank], colWidths=[42 * mm, None], rowHeights=[11.5 * mm] * len(blank))
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), .6, RULE), ('INNERGRID', (0, 0), (-1, -1), .4, RULE),
                           ('BACKGROUND', (0, 0), (0, -1), PAPER), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('LEFTPADDING', (0, 0), (-1, -1), 7), ('ROUNDEDCORNERS', [6, 6, 6, 6])]))
    return out + [t] + sign_off(('Approved by', 'Role', 'Date', 'Next review'))


@resource(file='monthly-report-template.pdf', short='Monthly report template', category='M&E', kicker='Template · two pages',
          title='Monthly programme report', fields=['Programme', 'Month', 'Prepared by'],
          lede='A short, repeatable structure for monthly reports that managers and donors can read in five minutes.',
          blurb='A two-page structure for monthly reports: highlights, indicator table, challenges, actions and data quality notes.',
          tags=['Template', 'Report'])
def _report():
    out = [Paragraph('1. Highlights', S['h2']), Paragraph('Three bullet points a busy reader must not miss.', S['small']), Lines(3),
           Spacer(1, 3 * mm), Paragraph('2. Indicators this month', S['h2']),
           write_table(['Indicator', 'Target', 'This month', 'Last month', 'Year to date', 'Comment'], 7,
                       [52 * mm, 18 * mm, 20 * mm, 20 * mm, 22 * mm, None]),
           Spacer(1, 4 * mm), Paragraph('3. What changed and why', S['h2']),
           Paragraph('Explain any change larger than about 10% from last month, in plain words.', S['small']), Lines(4),
           PageBreak(), Paragraph('4. Challenges', S['h2']),
           write_table(['Challenge', 'Effect on the programme', 'Proposed solution'], 4, [55 * mm, 55 * mm, None], h=13 * mm),
           Spacer(1, 4 * mm), Paragraph('5. Actions for next month', S['h2']),
           write_table(['Action', 'Owner', 'Due date', 'Status'], 5, [80 * mm, 35 * mm, 25 * mm, None]),
           Spacer(1, 4 * mm), Paragraph('6. Data quality notes', S['h2']),
           Paragraph('Late or missing reports, corrections made and anything the reader should treat with caution.', S['small']), Lines(3),
           Spacer(1, 2 * mm), tip('Put the answer first. A reader who stops after section 1 should still know how the month went.')]
    return out


@resource(file='xlsform-cheat-sheet.pdf', short='XLSForm cheat sheet', category='Data collection', kicker='Reference · Survey123 and KoboToolbox',
          title='XLSForm cheat sheet', lede='The question types, rules and expressions used most often when building forms for Survey123, KoboToolbox and ODK.',
          blurb='Question types, required, relevant, constraint and calculation syntax with copy-ready examples and common mistakes.',
          tags=['Reference', 'Survey123', 'Kobo'])
def _xls():
    types = [('text', 'Free text'), ('integer / decimal', 'Whole or decimal numbers'), ('date / time / dateTime', 'Date and time pickers'),
             ('select_one list', 'One answer from a choices list'), ('select_multiple list', 'Several answers from a list'),
             ('geopoint', 'GPS location'), ('image / audio', 'Photo or recording'), ('barcode', 'Scan a barcode or QR code'),
             ('calculate', 'Hidden value worked out by a formula'), ('note', 'Text shown to the user, no answer'),
             ('begin group / end group', 'Show questions together'), ('begin repeat / end repeat', 'Ask a set of questions many times')]
    cols = [('required', 'yes', 'Answer cannot be skipped'),
            ('relevant', "${sex} = 'female'", 'Show only when the condition is true'),
            ('constraint', '. >= 0 and . <= 120', 'The dot means "this answer"'),
            ('constraint_message', 'Age must be 0 to 120', 'What the user sees when a rule fails'),
            ('calculation', '${doses_given} - ${doses_wasted}', 'Used with type calculate'),
            ('choice_filter', 'district = ${district}', 'Cascading lists, such as district then chiefdom'),
            ('default', 'today()', 'Pre-filled value'),
            ('appearance', 'minimal  ·  autocomplete  ·  multiline', 'Changes how a question looks')]
    expr = [('selected(${symptoms}, \'fever\')', 'True if "fever" was ticked in a select_multiple'),
            ('count-selected(${symptoms})', 'How many options were ticked'),
            ('regex(., \'^[0-9]{9}$\')', 'Exactly nine digits, useful for phone numbers'),
            ('string-length(.) >= 3', 'At least three characters'),
            ('. <= today()', 'Date cannot be in the future'),
            ('int((today() - ${dob}) div 365.25)', 'Approximate age in years from a date of birth'),
            ('if(${age} < 5, \'under5\', \'over5\')', 'Choose a value based on a condition'),
            ('concat(${first}, \' \', ${last})', 'Join text values')]
    out = [Paragraph('Question types', S['h2']), kv_table(types, head=['type', 'Use it for'], widths=(55 * mm, None), mono_first=True), Spacer(1, 5 * mm),
           Paragraph('Columns on the survey sheet', S['h2']), kv_table(cols, head=['Column', 'Example', 'What it does'], widths=(38 * mm, 66 * mm, None), mono_first=True),
           PageBreak(), Paragraph('Useful expressions', S['h2']), kv_table(expr, head=['Expression', 'What it does'], widths=(85 * mm, None), mono_first=True),
           Spacer(1, 5 * mm), Paragraph('Required sheets', S['h2']),
           kv_table([('survey', 'One row per question: type, name, label and rules'), ('choices', 'list_name, name, label for every select list'),
                     ('settings', 'form_title, form_id and version')], widths=(38 * mm, None), mono_first=True), Spacer(1, 5 * mm),
           Paragraph('Common mistakes', S['h2'])]
    out += [checklist_group('Check before you publish', [
        'Every name is unique, has no spaces and starts with a letter',
        'Every select list used on the survey sheet exists on the choices sheet',
        'Choice names are short codes, with the readable text in label',
        'Every relevant, constraint and calculation references ${names} that exist',
        'Phone numbers and IDs are text, not integer, so leading zeros are kept',
        'The version number was increased before republishing',
        'No question collects data you will not use, especially names and phone numbers'])]
    out.append(tip('Test the form on a real phone, offline, with the person who will use it in the field, before training the whole team.'))
    return out


@resource(file='dashboard-design-checklist.pdf', short='Dashboard checklist', category='Dashboards', kicker='Checklist · before you share',
          title='Dashboard design checklist', fields=['Dashboard', 'Audience', 'Reviewed on'],
          lede='A dashboard works when each reader can answer their own question without help. Use this before you share one.',
          blurb='Audience, layout, charts, numbers and trust: a one-page review to run before you share any Power BI or Excel dashboard.',
          tags=['Checklist', 'Power BI'])
def _dash():
    g = [('Audience and purpose', ['I can name who reads this and the decision it supports', 'Each page answers one main question', 'The most important number is top left']),
         ('Layout', ['No more than 4 to 6 visuals per page', 'Filters are in the same place on every page', 'Titles say what the chart shows, for example "Penta 3 coverage by month"']),
         ('Charts', ['Bars for comparing, lines for trends over time', 'Bar charts start at zero', 'No 3D charts and no more than one pie chart per page', 'Colour is used to highlight, not to decorate']),
         ('Numbers', ['Units are shown: %, doses, facilities', 'Totals match the source data exactly', 'Targets or last period are shown for context']),
         ('Trust', ['The data source and last refresh date are on the page', 'Definitions are one click away', 'A colleague checked three numbers against the raw data']),
         ('Access', ['Text is readable on a laptop and a projector', 'Works with colour blindness: do not rely on red versus green alone', 'Only people who should see the data can open it'])]
    return [checklist_group(t, i, n + 1) for n, (t, i) in enumerate(g)] + [tip('Show the draft to one real reader and watch them use it for two minutes without helping. Fix what confuses them.')]


@resource(file='backup-security-checklist.pdf', short='Backup and security', category='IT', kicker='Checklist · small offices',
          title='Backup and security checklist', fields=['Office', 'Checked by', 'Date'],
          lede='Simple habits that protect a small office, clinic or NGO from lost files, viruses and stolen accounts.',
          blurb='The 3-2-1 backup rule, passwords, updates, antivirus and safe sharing for small offices, clinics and NGOs.',
          tags=['Checklist', 'Security'])
def _sec():
    rule = Table([[[Paragraph('3', ParagraphStyle('n0B7A5C', fontName='Bricolage-800', fontSize=24, leading=26, textColor=colors.HexColor('#0B7A5C'))), Paragraph('copies of important data', S['cell'])],
                   [Paragraph('2', ParagraphStyle('nD68A00', fontName='Bricolage-800', fontSize=24, leading=26, textColor=colors.HexColor('#D68A00'))), Paragraph('different types of storage', S['cell'])],
                   [Paragraph('1', ParagraphStyle('n0F2430', fontName='Bricolage-800', fontSize=24, leading=26, textColor=colors.HexColor('#0F2430'))), Paragraph('copy kept away from the office', S['cell'])]]],
                 colWidths=[(W - 2 * M) / 3] * 3)
    rule.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), SOFT), ('LEFTPADDING', (0, 0), (-1, -1), 12), ('TOPPADDING', (0, 0), (-1, -1), 10),
                              ('BOTTOMPADDING', (0, 0), (-1, -1), 10), ('LINEAFTER', (0, 0), (1, 0), .6, WHITE), ('ROUNDEDCORNERS', [8, 8, 8, 8])]))
    g = [('Backups', ['Important folders are listed and backed up every week', 'One backup is on an external drive, one in the cloud', 'A restore was tested this quarter, not just the backup']),
         ('Passwords and accounts', ['Every staff member has their own account, no shared logins', 'Passwords are long phrases and not reused', 'Two-step verification is on for email and cloud storage', 'Accounts of staff who left were closed the same week']),
         ('Devices', ['Windows and apps install updates automatically', 'Antivirus is on and up to date on every computer', 'Screens lock after a few minutes', 'Laptops that hold sensitive data are encrypted']),
         ('Email and sharing', ['Staff know how to spot a fake email or link', 'Files with personal data are shared only with named people', 'USB drives are scanned before opening'])]
    return [Paragraph('The 3-2-1 backup rule', S['h2']), rule, Spacer(1, 5 * mm)] + [checklist_group(t, i, n + 1) for n, (t, i) in enumerate(g)]


@resource(file='field-supervision-checklist.pdf', short='Field supervision', category='Data collection', kicker='Checklist · supervisor visit',
          title='Field data collection supervision checklist', fields=['Team or enumerator', 'Location', 'Visit date'],
          lede='For supervisors visiting data collectors in the field. Catch problems on day one, not after the dataset is closed.',
          blurb='What a supervisor checks during a field visit: devices, consent, form use, GPS, sync and data quality spot checks.',
          tags=['Checklist', 'Field work'])
def _field():
    g = [('Device and app', ['Phone or tablet is charged and has a power bank', 'The latest form version is installed', 'Date and time on the device are correct', 'Unsent submissions are being synced daily']),
         ('Before each interview', ['The collector introduces themselves and the purpose', 'Consent is asked and recorded the way the protocol says', 'The interview is private where needed']),
         ('During data entry', ['Questions are read as written, not reworded', 'Numbers are entered directly, not from memory later', 'GPS is captured at the household or facility, not elsewhere', 'Photos do not show faces unless consent covers it']),
         ('Spot checks', ['Supervisor re-asked 3 key questions in one household and answers matched', 'No duplicate households in today\'s submissions', 'Times between interviews look realistic'])]
    out = [checklist_group(t, i, n + 1) for n, (t, i) in enumerate(g)]
    out += [Paragraph('Issues found and actions', S['h2']), write_table(['Issue', 'Action agreed', 'By when'], 4, [70 * mm, 70 * mm, None], h=11 * mm)]
    return out + sign_off(('Supervisor', 'Collector', 'Date', 'Next visit'))


@resource(file='new-staff-it-setup.pdf', short='New staff IT setup', category='IT', kicker='Checklist · onboarding and exit',
          title='New staff IT setup checklist', fields=['Staff role', 'Start date', 'Set up by'],
          lede='Set a new colleague up properly on day one, and close everything cleanly when they leave.',
          blurb='Accounts, device setup, security and training for a new colleague, plus the matching exit checklist.',
          tags=['Checklist', 'Onboarding'])
def _staff():
    g = [('Accounts', ['Personal email account created', 'Added to the right shared folders only', 'Two-step verification set up with the staff member', 'Password manager or safe password method explained']),
         ('Device', ['Computer named and recorded in the asset register', 'Updates, antivirus and backup installed and checked', 'Office printer and Wi-Fi connected', 'Standard software installed: office suite, PDF reader, browser']),
         ('First week', ['Shown where to save work so it is backed up', 'Shown how to report an IT problem', 'Data protection basics explained: no personal data on USB drives or WhatsApp']),
         ('When they leave', ['Accounts disabled on the last day', 'Work files moved to a shared folder', 'Device returned, checked and wiped', 'Shared passwords they knew are changed'])]
    return [checklist_group(t, i, n + 1) for n, (t, i) in enumerate(g)] + sign_off(('Staff member', 'IT support', 'Date', 'Manager'))


@resource(file='logframe-template.pdf', short='Logframe template', category='M&E', kicker='Template · project design',
          title='Logframe template', fields=['Project', 'Period', 'Version'],
          lede='Lay out how activities lead to outputs, outcomes and the goal, with an indicator, a source of evidence and an assumption at each level.',
          blurb='Goal, outcome, outputs and activities with indicators, means of verification and assumptions. Includes a guide, a worked example and a blank frame.',
          tags=['Template', 'Worked example'])
def _logframe():
    levels = [('Goal', 'The long-term change the project contributes to, together with others.'),
              ('Outcome', 'The change the project is directly responsible for by the end.'),
              ('Outputs', 'What the project delivers: people trained, systems built, services provided.'),
              ('Activities', 'The work done to produce each output.')]
    guide = kv_table(levels, head=['Level', 'What it means'], widths=(30 * mm, None))
    logic = tip('Read it from the bottom up: if we do these activities, we deliver these outputs; if the outputs are delivered and the assumptions hold, the outcome follows.', 'The logic')
    head = ['Level', 'Result statement', 'Indicator', 'Means of verification', 'Assumptions']
    widths = [21 * mm, 42 * mm, 42 * mm, 36 * mm, None]
    ex = [('Goal', 'Better use of data in immunisation planning in the district', 'Facilities using monthly data in review meetings', 'Meeting minutes', ''),
          ('Outcome', 'Facility immunisation data is complete, timely and accurate', 'Share of monthly reports on time and passing quality checks', 'Reporting tracker; data quality checklist', 'Facilities keep reporting through the year'),
          ('Output 1', 'Facility staff trained in data quality checks', 'Number of staff trained', 'Attendance records; pre and post tests', 'Trained staff remain in post'),
          ('Output 2', 'Monthly dashboard shared with facilities', 'Months the dashboard was shared on time', 'Email or WhatsApp records', 'Internet access at facilities'),
          ('Activities', 'Train staff; supervise monthly; build and share dashboard', 'Inputs and budget', 'Activity reports; finance records', 'Funds released on time')]
    data = [[Paragraph(h, S['cellw']) for h in head]] + [[Paragraph(r[0], S['cellb'])] + [Paragraph(x, S['cell']) for x in r[1:]] for r in ex]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), INK), ('GRID', (0, 0), (-1, -1), .4, RULE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, PAPER]), ('BACKGROUND', (0, 1), (0, -1), SOFT),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5), ('LEFTPADDING', (0, 0), (-1, -1), 6)]))
    blank = [[Paragraph(h, S['cellw']) for h in head]] + [[Paragraph(l, S['cellb']), '', '', '', ''] for l in ['Goal', 'Outcome', 'Output 1', 'Output 2', 'Output 3', 'Activities']]
    b = Table(blank, colWidths=widths, rowHeights=[None] + [27 * mm] * 6, repeatRows=1)
    b.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), INK), ('GRID', (0, 0), (-1, -1), .4, RULE), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('BACKGROUND', (0, 1), (0, -1), SOFT), ('TOPPADDING', (0, 0), (-1, -1), 5), ('LEFTPADDING', (0, 0), (-1, -1), 6)]))
    return [Paragraph('The four levels', S['h2']), guide, Spacer(1, 4 * mm), logic,
            Paragraph('Worked example (illustrative)', S['h2']), t, PageBreak(), Paragraph('Blank logframe', S['h2']), b]


@resource(file='training-session-plan.pdf', short='Training session plan', category='Training', kicker='Template · plan and review',
          title='Training session plan', fields=['Topic', 'Date and venue', 'Trainer'],
          lede='Plan a practical training for data collectors, facility staff or office teams, then record how it went.',
          blurb='Objectives, a timed agenda, a materials checklist and an after-session review for data, ICT and Survey123 trainings.',
          tags=['Template', 'Checklist'])
def _session():
    out = [Paragraph('Who is it for', S['h2']),
           write_table(['Audience', 'Number expected', 'Current skill level', 'Language'], 1, [(W - 2 * M) / 4] * 4, h=11 * mm),
           Spacer(1, 4 * mm), Paragraph('Learning objectives', S['h2']),
           Paragraph('By the end, participants will be able to... Use action words: enter, check, explain, fix.', S['small']), Lines(3),
           Spacer(1, 3 * mm), Paragraph('Agenda', S['h2']),
           write_table(['Time', 'Activity', 'Method', 'Materials', 'Lead'], 8, [22 * mm, 62 * mm, 32 * mm, 32 * mm, None]),
           Spacer(1, 3 * mm),
           tip('Keep slides short. Give every participant time to practise on their own device, with real (anonymised) examples.'),
           PageBreak()]
    out.append(checklist_group('Materials and setup', [
        'Venue booked, with power sockets and seating for everyone',
        'Projector, screen and extension cables tested the day before',
        'Devices charged, with the latest form or software version installed',
        'Practice data prepared, with no real names or phone numbers',
        'Attendance sheet and pre-test printed',
        'Handouts or quick guides ready to take away',
        'Refreshments and transport arranged where needed'], 1))
    out += [Paragraph('After the session', S['h2']),
            write_table(['Attended', 'Average pre-test', 'Average post-test', 'Follow-up date'], 1, [(W - 2 * M) / 4] * 4, h=11 * mm),
            Spacer(1, 4 * mm), Paragraph('What worked well', S['small']), Lines(2),
            Paragraph('What to change next time', S['small']), Lines(2),
            Paragraph('Follow-up actions', S['h2']),
            write_table(['Action', 'Owner', 'By when'], 3, [95 * mm, 40 * mm, None])]
    return out


def build_pdfs(outdir):
    os.makedirs(outdir, exist_ok=True)
    for r in PDFS:
        _doc(os.path.join(outdir, r['file']), r, r['build']())
    return PDFS
