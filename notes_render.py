"""Renderer for rich notes: extended markdown, hero art per note and inline figures."""
import html
import re

esc = lambda s: html.escape(s, quote=True)


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# ------------------------------------------------------------------ hero art (one motif per note)
def _frame(inner, label):
    grid = ''.join('<line x1="%d" y1="0" x2="%d" y2="240"/>' % (x, x) for x in range(20, 480, 20))
    return ('<svg class="cover-art note-art" viewBox="0 0 480 240" role="img" aria-label="Illustration: %s">'
            '<rect class="a-bg" width="480" height="240"/><g class="a-grid">%s</g>%s</svg>') % (esc(label), grid, inner)


def card(x, y, w, h, r=14, extra=''):
    return '<rect class="a-card" x="%d" y="%d" width="%d" height="%d" rx="%d"%s/>' % (x, y, w, h, r, extra)


def bar(x, y, w, h=8, cls='a-line'):
    return '<rect class="%s" x="%d" y="%d" width="%d" height="%d" rx="%d"/>' % (cls, x, y, w, h, h // 2)


MOTIFS = {}


def motif(name, label):
    def wrap(fn):
        MOTIFS[name] = (fn, label)
        return fn
    return wrap


@motif('checks', 'a dataset passing through six numbered checks')
def _m_checks():
    s = '<g class="float-a">' + card(150, 30, 180, 180)
    for i in range(6):
        y = 52 + i * 26
        s += '<circle class="%s" cx="174" cy="%d" r="8"/>' % ('a-g' if i < 5 else 'a-am', y)
        s += '<path class="a-check-w" d="M170 %d l3 3 6-6" style="stroke-width:2.2"/>' % y if i < 5 else ''
        s += bar(192, y - 4, [90, 70, 100, 60, 84, 76][i], 8, 'a-line' if i % 2 else 'a-mu')
    s += '</g><g class="float-b">' + card(40, 70, 90, 100) + ''.join(bar(54, 86 + k * 14, 62 - (k % 3) * 10, 6, 'a-mu') for k in range(5)) + '</g>'
    s += '<path class="a-link" d="M130 120 H150 M330 120 H350"/>'
    s += '<g class="float-c">' + card(350, 80, 90, 80) + ''.join('<rect class="a-g" x="%d" y="%d" width="10" height="%d" rx="3"/>' % (364 + k * 16, 140 - h, h) for k, h in enumerate([20, 32, 26, 44])) + '</g>'
    return s


@motif('phone', 'a phone form showing a validation message')
def _m_phone():
    s = '<g class="float-a"><rect class="a-phone" x="180" y="18" width="124" height="210" rx="22"/>' + card(188, 32, 108, 184, 12)
    s += bar(198, 44, 54, 8, 'a-g') + bar(198, 64, 40) + '<rect class="a-field" x="198" y="76" width="88" height="18" rx="5"/>'
    s += bar(198, 104, 50) + '<rect x="198" y="116" width="88" height="18" rx="5" fill="none" stroke="#B42318" stroke-width="2"/>'
    s += '<rect x="198" y="140" width="88" height="20" rx="5" fill="#FDE2E1"/>' + '<rect x="204" y="147" width="60" height="6" rx="3" fill="#B42318"/>'
    s += '<rect class="a-g" x="198" y="188" width="88" height="18" rx="9"/></g>'
    s += '<g class="float-b">' + card(330, 60, 110, 60) + bar(344, 74, 56) + '<text class="a-code" x="344" y="104">. &lt;= 500</text></g>'
    s += '<g class="float-c">' + card(40, 120, 110, 70) + '<circle class="a-gs-fill" cx="64" cy="155" r="14"/><path class="a-check" d="M57 155l5 5 9-9"/>' + bar(86, 146, 50) + bar(86, 160, 36, 6, 'a-mu') + '</g>'
    return s


@motif('dashboard', 'a dashboard with headline numbers, a trend line and a table')
def _m_dash():
    s = '<g class="float-a">' + card(60, 24, 360, 192)
    for k in range(3):
        s += '<rect class="a-gs" x="%d" y="40" width="100" height="42" rx="8"/>' % (76 + k * 112) + bar(86 + k * 112, 50, 40, 6, 'a-mu') + bar(86 + k * 112, 64, 54, 10, 'a-g' if k != 1 else 'a-am')
    s += '<polyline class="a-am a-path" pathLength="1" points="80,150 120,138 160,142 200,122 240,116 280,104" style="fill:none;stroke-width:3"/>'
    s += '<line x1="80" y1="112" x2="290" y2="112" stroke="var(--green)" stroke-dasharray="5 5" stroke-width="2"/>'
    s += ''.join('<rect class="a-g" x="%d" y="%d" width="14" height="%d" rx="3"/>' % (310 + k * 20, 160 - h, h) for k, h in enumerate([30, 46, 20, 56, 38]))
    s += ''.join(bar(76, 176 + k * 12, 320, 5, 'a-mu') for k in range(3)) + '</g>'
    return s


@motif('tools', 'four data collection tools compared side by side')
def _m_tools():
    s = ''
    for k in range(4):
        x = 40 + k * 104
        hi = k == 1
        s += '<g class="float-%s">' % 'abc'[k % 3] + card(x, 50 - (10 if hi else 0), 92, 150 + (20 if hi else 0))
        s += '<rect class="%s" x="%d" y="%d" width="28" height="28" rx="8"/>' % ('a-g' if hi else 'a-gs', x + 14, 64 - (10 if hi else 0))
        for r in range(4):
            y = 108 + r * 22 - (10 if hi else 0)
            ok = (k + r) % 3 != 0
            s += '<circle cx="%d" cy="%d" r="6" class="%s"/>' % (x + 20, y, 'a-g' if ok else 'a-mu') + bar(x + 32, y - 3, 44, 6, 'a-mu')
        s += '</g>'
    return s


@motif('grid', 'a spreadsheet with highlighted cleaned cells')
def _m_grid():
    s = '<g class="float-a">' + card(70, 26, 340, 188, 12) + '<rect class="a-g" x="70" y="26" width="340" height="26" rx="12"/><rect class="a-g" x="70" y="40" width="340" height="12"/>'
    for r in range(6):
        for c in range(5):
            x, y = 82 + c * 66, 62 + r * 24
            cls = 'a-mu'
            if (r, c) in [(1, 1), (3, 3), (4, 0)]:
                s += '<rect x="%d" y="%d" width="60" height="18" rx="4" fill="var(--amber-soft,#FBEBC8)"/>' % (x - 4, y - 5)
                cls = 'a-am'
            s += bar(x, y, 40 + (r * c) % 14, 7, cls)
    s += '</g><g class="float-b"><circle cx="400" cy="40" r="24" class="a-ok"/><path class="a-check-w" d="M390 40l7 7 13-13"/></g>'
    return s


@motif('star', 'a data model with one fact table linked to four lookup tables')
def _m_star():
    s = '<g class="a-link-g">' + ''.join('<line class="a-rel" x1="240" y1="120" x2="%d" y2="%d"/>' % p for p in [(90, 56), (390, 56), (90, 186), (390, 186)]) + '</g>'
    s += '<g class="float-a">' + card(185, 82, 110, 76) + '<rect class="a-g" x="185" y="82" width="110" height="22" rx="14"/><rect class="a-g" x="185" y="94" width="110" height="10"/>' + ''.join(bar(197, 114 + k * 12, 80 - k * 12, 6, 'a-mu') for k in range(3)) + '</g>'
    for k, (x, y) in enumerate([(40, 30), (340, 30), (40, 160), (340, 160)]):
        s += '<g class="float-%s">' % 'bcb c'.replace(' ', '')[k % 3] + card(x, y, 100, 52, 10) + '<rect class="a-gs" x="%d" y="%d" width="100" height="16" rx="10"/>' % (x, y) + bar(x + 12, y + 26, 60, 6, 'a-line') + bar(x + 12, y + 38, 40, 6, 'a-mu') + '</g>'
    return s


@motif('target', 'an indicator target with numerator over denominator')
def _m_target():
    s = '<g class="float-a">' + ''.join('<circle cx="140" cy="120" r="%d" class="%s"/>' % (r, c) for r, c in [(80, 'a-tgt1'), (58, 'a-tgt2'), (36, 'a-tgt1'), (14, 'a-am-fill')]) + '</g>'
    s += '<g class="float-b">' + card(260, 50, 170, 140) + bar(280, 72, 90, 9, 'a-g') + bar(280, 90, 120, 7, 'a-mu')
    s += '<line x1="280" y1="118" x2="410" y2="118" stroke="var(--ink)" stroke-width="3" stroke-linecap="round"/>' + bar(280, 132, 110, 9, 'a-line') + bar(280, 150, 70, 7, 'a-mu') + '</g>'
    return s


@motif('qr', 'an ID card with a QR code being scanned by a phone')
def _m_qr():
    qr = ''.join('<rect class="a-ink-fill" x="%d" y="%d" width="9" height="9"/>' % (110 + (k % 6) * 11, 92 + (k // 6) * 11) for k in [0, 1, 2, 4, 5, 6, 8, 11, 13, 15, 17, 18, 21, 22, 24, 26, 29, 30, 31, 33, 35])
    s = '<g class="float-a">' + card(80, 50, 200, 130) + '<rect class="a-g" x="80" y="50" width="200" height="28" rx="14"/><rect class="a-g" x="80" y="64" width="200" height="14"/>' + qr + bar(196, 98, 64) + bar(196, 114, 44, 6, 'a-mu') + bar(196, 128, 54, 6, 'a-mu') + '</g>'
    s += '<g class="float-b"><rect class="a-phone" x="310" y="40" width="96" height="164" rx="18"/>' + card(316, 52, 84, 140, 10) + '<rect x="330" y="80" width="56" height="56" rx="6" fill="none" stroke="var(--green)" stroke-width="2.5" stroke-dasharray="10 8"/><line class="a-scan" x1="332" y1="108" x2="384" y2="108"/>' + bar(328, 152, 60, 7, 'a-g') + '</g>'
    return s


@motif('boxes', 'stacked stock boxes beside a count sheet')
def _m_boxes():
    s = '<g class="float-a">'
    for (x, y, w, h) in [(60, 130, 90, 70), (150, 130, 90, 70), (100, 64, 90, 66)]:
        s += '<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="#D9B98A" stroke="#B8935C" stroke-width="2"/>' % (x, y, w, h)
        s += '<rect x="%d" y="%d" width="22" height="%d" fill="#C9A46E"/>' % (x + w // 2 - 11, y, h // 3)
    s += '</g><g class="float-b">' + card(290, 34, 150, 176)
    for r in range(6):
        s += bar(306, 56 + r * 24, 60, 7, 'a-mu') + bar(380, 56 + r * 24, 24, 7, 'a-line')
        s += '<circle cx="420" cy="%d" r="5" class="%s"/>' % (59 + r * 24, 'a-g' if r != 3 else 'a-am-fill')
    return s + '</g>'


@motif('db', 'a spreadsheet moving into a database')
def _m_db():
    s = '<g class="float-b">' + card(40, 60, 130, 120, 10) + '<rect class="a-g" x="40" y="60" width="130" height="18" rx="10"/>' + ''.join(bar(52, 90 + r * 16, 100 - (r % 2) * 20, 6, 'a-mu') for r in range(5)) + '</g>'
    s += '<path class="a-link" d="M180 120 H290"/><path d="M282 112l10 8-10 8" fill="none" stroke="var(--green)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    s += '<g class="float-a"><ellipse class="a-db" cx="370" cy="62" rx="62" ry="18"/><path class="a-db" d="M308 62v116c0 10 28 18 62 18s62-8 62-18V62"/><path class="a-db-line" d="M308 100c0 10 28 18 62 18s62-8 62-18M308 140c0 10 28 18 62 18s62-8 62-18"/></g>'
    return s


@motif('people', 'community health workers syncing reports from phones')
def _m_people():
    s = ''
    for k, x in enumerate([90, 200, 310]):
        s += '<g class="float-%s"><circle cx="%d" cy="90" r="22" class="a-gs-fill"/><circle cx="%d" cy="84" r="9" class="a-g"/><path class="a-g" d="M%d 104c3-10 9-14 14-14s11 4 14 14z"/>' % ('abc'[k], x, x, x - 14)
        s += '<rect class="a-phone" x="%d" y="128" width="40" height="64" rx="8"/><rect class="a-card" x="%d" y="134" width="32" height="50" rx="4"/>' % (x - 20, x - 16) + bar(x - 12, 142, 22, 5, 'a-g') + bar(x - 12, 154, 18, 5, 'a-mu') + '</g>'
        s += '<path class="a-link" d="M%d 128 Q%d 40 410 60"/>' % (x, x + 60) if k == 1 else ''
    s += '<g class="float-b"><circle cx="420" cy="60" r="26" class="a-ok"/><path class="a-check-w" d="M408 60l8 8 16-16"/></g>'
    return s


@motif('browser', 'a simple website open on a laptop and a phone')
def _m_browser():
    s = '<g class="float-a">' + card(50, 30, 300, 180, 12) + '<rect class="a-gs" x="50" y="30" width="300" height="24" rx="12"/><rect class="a-gs" x="50" y="44" width="300" height="10"/>'
    s += ''.join('<circle cx="%d" cy="42" r="4" class="a-mu"/>' % x for x in (66, 80, 94))
    s += bar(70, 72, 140, 14, 'a-line') + bar(70, 94, 190, 7, 'a-mu') + bar(70, 108, 160, 7, 'a-mu') + '<rect class="a-g" x="70" y="126" width="80" height="22" rx="11"/>'
    s += '<rect x="230" y="120" width="100" height="72" rx="8" class="a-gs-fill"/>' + ''.join('<rect class="a-mu" x="%d" y="166" width="80" height="34" rx="6"/>' % x for x in []) + '</g>'
    s += '<g class="float-b"><rect class="a-phone" x="370" y="70" width="70" height="130" rx="14"/>' + card(375, 80, 60, 110, 8) + bar(383, 94, 40, 8, 'a-line') + bar(383, 110, 44, 5, 'a-mu') + '<rect class="a-g" x="383" y="166" width="44" height="14" rx="7"/></g>'
    return s


@motif('drives', 'three backup copies on a laptop, a drive and the cloud')
def _m_drives():
    s = '<g class="float-a"><rect class="a-card" x="40" y="70" width="130" height="86" rx="8"/><rect class="a-gs-fill" x="50" y="80" width="110" height="64" rx="4"/><rect class="a-phone" x="26" y="156" width="158" height="12" rx="6"/></g>'
    s += '<g class="float-b"><rect class="a-phone" x="210" y="76" width="70" height="96" rx="12"/><circle cx="245" cy="148" r="5" fill="#7CF0C4"/>' + bar(226, 92, 38, 6, 'a-mu') + '</g>'
    s += '<g class="float-c"><path class="a-cloud" d="M330 150h90a28 28 0 0 0 0-56 40 40 0 0 0-76-8 30 30 0 0 0-14 64z"/></g>'
    s += ''.join('<text class="a-big" x="%d" y="226" text-anchor="middle">%s</text>' % (x, t) for x, t in [(105, '1'), (245, '2'), (380, '3')])
    return s


@motif('matrix', 'a priority matrix of impact against cost')
def _m_matrix():
    s = '<g class="float-a">' + card(110, 20, 260, 200, 12)
    s += '<line x1="240" y1="34" x2="240" y2="206" stroke="var(--rule)" stroke-width="2"/><line x1="124" y1="120" x2="356" y2="120" stroke="var(--rule)" stroke-width="2"/>'
    s += '<rect class="a-gs" x="128" y="38" width="104" height="74" rx="8"/><rect x="248" y="38" width="104" height="74" rx="8" fill="var(--amber-soft,#FBEBC8)"/>'
    for (x, y, c) in [(160, 66, 'a-g'), (196, 84, 'a-g'), (290, 70, 'a-am-fill'), (170, 160, 'a-mu'), (300, 170, 'a-mu')]:
        s += '<circle cx="%d" cy="%d" r="11" class="%s"/>' % (x, y, c)
    return s + '</g>'


@motif('health', 'a health facility register turning into a digital chart')
def _m_health():
    s = '<g class="float-b">' + card(40, 40, 140, 160, 8) + '<rect x="40" y="40" width="14" height="160" rx="4" fill="#C2410C" opacity=".8"/>' + ''.join(bar(66, 62 + r * 18, 96 - (r % 3) * 18, 6, 'a-mu') for r in range(7)) + '</g>'
    s += '<path class="a-link" d="M190 120 H270"/>'
    s += '<g class="float-a">' + card(280, 34, 160, 172) + '<circle cx="360" cy="78" r="24" class="a-gs-fill"/><path d="M352 78h16M360 70v16" stroke="var(--green)" stroke-width="5" stroke-linecap="round"/>'
    s += ''.join('<rect class="a-g" x="%d" y="%d" width="18" height="%d" rx="4"/>' % (300 + k * 28, 190 - h, h) for k, h in enumerate([30, 46, 38, 60, 72])) + '</g>'
    return s


@motif('wrench', 'IT tools around a computer screen with a settings gear')
def _m_wrench():
    s = '<g class="float-a"><rect class="a-phone" x="130" y="40" width="220" height="140" rx="12"/><rect class="a-gs-fill" x="142" y="52" width="196" height="116" rx="6"/><rect class="a-phone" x="210" y="180" width="60" height="20"/><rect class="a-phone" x="180" y="198" width="120" height="10" rx="5"/>'
    s += '<circle cx="240" cy="110" r="30" class="a-g"/><circle cx="240" cy="110" r="12" class="a-gs-fill"/>'
    s += ''.join('<rect class="a-g" x="234" y="70" width="12" height="16" rx="3" transform="rotate(%d 240 110)"/>' % a for a in range(0, 360, 45)) + '</g>'
    s += '<g class="float-b"><path d="M80 170l50-50" stroke="var(--amber)" stroke-width="12" stroke-linecap="round"/><circle cx="136" cy="114" r="14" fill="none" stroke="var(--amber)" stroke-width="8"/></g>'
    s += '<g class="float-c">' + card(370, 60, 80, 90, 10) + ''.join('<circle cx="388" cy="%d" r="5" class="a-g"/>' % y + bar(400, y - 3, 36, 6, 'a-mu') for y in (82, 104, 126)) + '</g>'
    return s


@motif('path', 'a winding path with milestones from training to data work')
def _m_path():
    s = '<path class="a-road" d="M30 200 C120 200 110 120 200 120 S300 50 440 40"/>'
    for k, (x, y) in enumerate([(52, 200), (150, 150), (230, 116), (320, 74), (420, 42)]):
        s += '<g class="float-%s"><circle cx="%d" cy="%d" r="14" class="%s"/><circle cx="%d" cy="%d" r="5" fill="#fff"/></g>' % ('abc'[k % 3], x, y, 'a-am-fill' if k == 4 else 'a-g', x, y)
    return s


@motif('shield', 'a shield protecting a laptop with a lock')
def _m_shield():
    s = '<g class="float-a"><path class="a-g" d="M240 24l78 30v58c0 50-34 86-78 104-44-18-78-54-78-104V54z"/><path d="M240 40l62 24v48c0 40-26 70-62 86z" fill="rgba(255,255,255,.15)"/>'
    s += '<rect x="214" y="108" width="52" height="42" rx="8" fill="#fff"/><path d="M224 108v-12a16 16 0 0 1 32 0v12" fill="none" stroke="#fff" stroke-width="7"/><circle cx="240" cy="128" r="6" class="a-g"/></g>'
    s += '<g class="float-b">' + card(40, 70, 100, 90) + ''.join('<circle cx="58" cy="%d" r="6" class="a-g"/><path class="a-check-w" d="M55 %d l2 2 4-4" style="stroke-width:1.8"/>' % (y, y) + bar(72, y - 3, 50, 6, 'a-mu') for y in (92, 114, 136)) + '</g>'
    s += '<g class="float-c"><rect x="350" y="80" width="90" height="70" rx="10" fill="#FDE2E1"/><path d="M380 100l30 30M410 100l-30 30" stroke="#B42318" stroke-width="7" stroke-linecap="round"/></g>'
    return s


@motif('cycle', 'a cycle from data collection to decision and action')
def _m_cycle():
    import math
    s = '<circle cx="240" cy="120" r="82" fill="none" stroke="var(--rule)" stroke-width="3" stroke-dasharray="6 8" class="a-spin"/>'
    for k in range(6):
        a = -math.pi / 2 + k * math.pi / 3
        x, y = 240 + 82 * math.cos(a), 120 + 82 * math.sin(a)
        s += '<g class="float-%s"><circle cx="%.0f" cy="%.0f" r="20" class="%s"/><text class="a-step" x="%.0f" y="%.0f" text-anchor="middle">%d</text></g>' % (
            'abc'[k % 3], x, y, 'a-am-fill' if k == 4 else 'a-g', x, y + 5, k + 1)
    s += '<circle cx="240" cy="120" r="34" class="a-gs-fill"/><path class="a-check" d="M226 120l9 9 18-18" style="stroke-width:4"/>'
    return s


def hero_art(motif_name):
    fn, label = MOTIFS[motif_name]
    return _frame(fn(), label)


# ------------------------------------------------------------------ inline figures
def fig_phone_error():
    return '''<div class="fx-phone" aria-hidden="true"><div class="fx-screen">
<p class="fx-q">Children vaccinated today</p><div class="fx-input bad">5000</div>
<p class="fx-err">Enter a number from 0 to 500</p>
<p class="fx-q">Any vaccine stock-out this month?</p><div class="fx-choices"><span>Yes</span><span class="on">No</span></div>
<div class="fx-send">Send</div></div></div>'''


def fig_wireframe():
    k = ''.join('<div class="wf-kpi"><span></span><b>%s</b><em>%s</em></div>' % (a, b) for a, b in [('Doses given', '1,284'), ('Coverage', '74%'), ('Facilities reporting', '14 of 17')])
    return f'''<div class="wf" aria-hidden="true"><div class="wf-top">{k}</div>
<div class="wf-mid"><div class="wf-card"><p>Coverage by month, target 80%</p><svg viewBox="0 0 200 70"><line x1="0" y1="18" x2="200" y2="18" class="wf-target"/><polyline class="wf-line" points="0,58 33,52 66,48 100,40 133,34 166,30 200,24"/></svg></div>
<div class="wf-card"><p>Lowest coverage first</p>{''.join('<div class="wf-row"><i style="width:%d%%" class="%s"></i></div>' % (w, 'lo' if w < 60 else '') for w in (42, 55, 68, 79, 88))}</div></div>
<div class="wf-table">{''.join('<span></span>' for _ in range(12))}</div><p class="wf-note">Sample layout with invented numbers</p></div>'''


def fig_star():
    dims = [('Facilities', 'FacilityID, Name, District'), ('Dates', 'Date, Month, Year'), ('Indicators', 'IndicatorID, Name, Unit'), ('Targets', 'FacilityID, Month, Target')]
    d = ''.join('<div class="st-dim st-%d"><b>%s</b><span>%s</span></div>' % (i, a, b) for i, (a, b) in enumerate(dims))
    return f'<div class="st" aria-hidden="true">{d}<div class="st-fact"><b>Facts</b><span>FacilityID, Date, IndicatorID, Doses</span></div><svg class="st-lines" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M25 22L50 50M75 22L50 50M25 78L50 50M75 78L50 50"/></svg></div>'


def fig_sitemap():
    pages = [('Home', 'One clear message, contact button'), ('About', 'Story, team, where you work'), ('Services', 'What you offer, how to ask'), ('Contact', 'WhatsApp, phone, email, map')]
    p = ''.join('<div class="sm-page"><div class="sm-bar"><i></i><i></i><i></i></div><b>%s</b><span>%s</span></div>' % x for x in pages)
    return f'<div class="sm" aria-hidden="true">{p}</div>'


def fig_321():
    items = [('3', 'copies', 'The original and two backups'), ('2', 'kinds of storage', 'For example a laptop and an external drive'), ('1', 'copy off-site', 'A cloud folder or a drive kept elsewhere')]
    return '<div class="b321" aria-hidden="true">' + ''.join('<div class="b321-i b%s"><b>%s</b><strong>%s</strong><span>%s</span></div>' % (n, n, a, b) for n, a, b in items) + '</div>'


def fig_matrix():
    q = [('Quick wins', 'High impact, low cost', 'Backups, shared passwords, short training', 'q1'),
         ('Big projects', 'High impact, high cost', 'New devices, network upgrade, a database', 'q2'),
         ('Fill-ins', 'Low impact, low cost', 'Tidy cables, desktop clean-up', 'q3'),
         ('Question these', 'Low impact, high cost', 'Software nobody asked for', 'q4')]
    cells = ''.join('<div class="mx-c %s"><b>%s</b><em>%s</em><span>%s</span></div>' % (c, a, b, d) for a, b, d, c in q)
    return f'<div class="mx" aria-hidden="true"><div class="mx-y">Impact</div><div class="mx-grid">{cells}</div><div class="mx-x">Cost to fix</div></div>'


def fig_journey():
    steps = [('2015 to 2019', 'Diplomas in software, hardware and networking', 'Growth Centre, Bo'),
             ('2016 to 2021', 'ICT tutor and internet cafe attendant', 'Growth Centre, Bo'),
             ('2022 to 2023', 'IT and Data Officer', 'SLPP, Bo District'),
             ('2023 to 2024', 'Assistant IT Manager', 'SLIEPA, Freetown'),
             ('2024 to now', 'Data Officer', 'Rural Health Care Initiative')]
    return '<ol class="jt">' + ''.join('<li><span class="jt-when">%s</span><b>%s</b><em>%s</em></li>' % s for s in steps) + '</ol>'


FIGS = {'phone-error': fig_phone_error, 'wireframe': fig_wireframe, 'star': fig_star, 'sitemap': fig_sitemap,
        '321': fig_321, 'matrix': fig_matrix, 'journey': fig_journey}


def fig_flow(spec):
    steps = [s.strip() for s in spec.split('>')]
    return '<ol class="flow">' + ''.join('<li style="--i:%d"><span class="flow-n">%d</span>%s</li>' % (i, i + 1, inline(s)) for i, s in enumerate(steps)) + '</ol>'


def fig_equation(spec):
    parts = re.split(r'\s+([+\-/=])\s+', spec)
    out = []
    for i, p in enumerate(parts):
        if i % 2:
            sym = {'-': '&minus;', '+': '+', '/': '&divide;', '=': '='}[p]
            out.append('<span class="eq-op">%s</span>' % sym)
        else:
            last = i == len(parts) - 1
            out.append('<span class="eq-t%s">%s</span>' % (' eq-res' if last else '', inline(p)))
    return '<div class="eq">' + ''.join(out) + '</div>'


# ------------------------------------------------------------------ markdown
def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+|[\w./#-]+)\)', r'<a href="\2">\1</a>', s)
    return s


CALLOUT = {'tip': 'tip', 'watch out': 'warn', 'example': 'example', 'what health taught me': 'quote'}


def figure(inner, caption, cls=''):
    cap = '<figcaption>%s</figcaption>' % inline(caption) if caption else ''
    return '<figure class="nfig %s">%s%s</figure>' % (cls, inner, cap)


def render(text):
    out, toc = [], []
    for block in re.split(r'\n\s*\n', text.strip()):
        lines = [l.rstrip() for l in block.split('\n')]
        first = lines[0]
        if first.startswith('## '):
            t = first[3:].strip()
            sid = slugify(t)
            toc.append((sid, t))
            out.append('<h2 id="%s">%s</h2>' % (sid, inline(t)))
        elif first.startswith('### '):
            out.append('<h3>%s</h3>' % inline(first[4:]))
        elif first.startswith('::flow '):
            spec, _, cap = first[7:].partition(' | ')
            out.append(figure(fig_flow(spec), cap, 'nfig-flow'))
        elif first.startswith('::equation '):
            spec, _, cap = first[11:].partition(' | ')
            out.append(figure(fig_equation(spec), cap, 'nfig-eq'))
        elif first.startswith('::fig '):
            name, _, cap = first[6:].partition(' | ')
            out.append(figure(FIGS[name.strip()](), cap, 'nfig-' + name.strip()))
        elif first.startswith('::photo '):
            parts = [p.strip() for p in first[8:].split(' | ')]
            src, cap = parts[0], parts[1] if len(parts) > 1 else ''
            alt = parts[2] if len(parts) > 2 else cap
            webp = src.rsplit('.', 1)[0] + '.webp'
            img = '<picture><source type="image/webp" srcset="%s"><img src="%s" alt="%s" loading="lazy"></picture>' % (webp, src, esc(alt))
            out.append(figure(img, cap, 'nfig-photo'))
        elif first.startswith('> '):
            body = ' '.join(l[2:] for l in lines)
            m = re.match(r'\*\*([^*:]+):\*\*\s*(.*)', body)
            label, rest = (m.group(1), m.group(2)) if m else ('Note', body)
            kind = CALLOUT.get(label.lower(), 'tip')
            out.append('<aside class="callout c-%s"><span class="callout-l">%s</span><p>%s</p></aside>' % (kind, esc(label), inline(rest)))
        elif all(l.startswith('[ ] ') for l in lines):
            out.append('<ul class="checklist">' + ''.join('<li><label><input type="checkbox"><span>%s</span></label></li>' % inline(l[4:]) for l in lines) + '</ul>')
        elif all(l.startswith('- ') for l in lines):
            out.append('<ul class="bullets">' + ''.join('<li>%s</li>' % inline(l[2:]) for l in lines) + '</ul>')
        elif all(re.match(r'\d+\. ', l) for l in lines):
            out.append('<ol class="numbered">' + ''.join('<li>%s</li>' % inline(re.sub(r'^\d+\. ', '', l)) for l in lines) + '</ol>')
        elif all(l.startswith('|') for l in lines):
            rows = [[c.strip() for c in l.strip('|').split('|')] for l in lines]
            head = '<thead><tr>%s</tr></thead>' % ''.join('<th scope="col">%s</th>' % inline(c) for c in rows[0])
            body = ''.join('<tr>%s</tr>' % ''.join(('<th scope="row">%s</th>' if j == 0 else '<td>%s</td>') % inline(c) for j, c in enumerate(r)) for r in rows[1:])
            out.append('<div class="ntable"><table>%s<tbody>%s</tbody></table></div>' % (head, body))
        else:
            out.append('<p>%s</p>' % inline(' '.join(lines)))
    return '\n'.join(out), toc
