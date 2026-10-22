"""Illustrated cover art (inline SVG) for projects, plus small icons for services.
Illustrations only: no real data, names or figures."""


def _svg(inner, label):
    return ('<svg class="cover-art" viewBox="0 0 400 250" role="img" aria-label="Illustration: %s">'
            '<rect class="a-bg" width="400" height="250" rx="0"/>'
            '<g class="a-grid">%s</g>%s</svg>') % (
        label, ''.join('<line x1="%d" y1="0" x2="%d" y2="250"/>' % (x, x) for x in range(25, 400, 25)), inner)


def cover(slug):
    if slug == 'case-epi-dashboard':
        bars = ''.join('<rect class="a-g ab" style="--i:%d" x="%d" y="%d" width="18" height="%d" rx="4"/>' % (
            i, 52 + i * 28, 196 - h, h) for i, h in enumerate([40, 58, 50, 72, 84, 78, 96]))
        inner = f'''<g class="float-a">
  <rect class="a-card" x="30" y="34" width="232" height="182" rx="16"/>
  <rect class="a-mu" x="48" y="52" width="90" height="9" rx="4.5"/><rect class="a-line" x="48" y="68" width="56" height="7" rx="3.5"/>
  <line class="a-axis" x1="46" y1="198" x2="246" y2="198"/>{bars}
  <polyline class="a-am a-path" pathLength="1" points="61,146 89,130 117,138 145,114 173,102 201,108 229,88"/>
</g>
<g class="float-b">
  <rect class="a-card" x="250" y="26" width="120" height="78" rx="14"/>
  <rect class="a-line" x="266" y="42" width="48" height="7" rx="3.5"/><rect class="a-ink-fill" x="266" y="62" width="24" height="24" rx="6"/>
  <rect class="a-gs" x="300" y="70" width="52" height="16" rx="8"/><rect class="a-g" x="300" y="70" width="38" height="16" rx="8"/>
</g>
<g class="float-c">
  <rect class="a-card" x="276" y="122" width="96" height="96" rx="14"/>
  <circle cx="324" cy="170" r="28" class="a-ring-bg"/><circle cx="324" cy="170" r="28" class="a-ring" pathLength="100" transform="rotate(-90 324 170)"/>
  <circle cx="324" cy="170" r="5" class="a-am-fill"/>
</g>'''
        return _svg(inner, 'a Power BI style dashboard with bars, a trend line and a progress ring')
    if slug == 'case-survey123':
        fields = ''.join('<rect class="a-line" x="128" y="%d" width="%d" height="7" rx="3.5"/><rect class="a-field" x="128" y="%d" width="116" height="20" rx="6"/>' % (
            70 + i * 44, w, 82 + i * 44) for i, w in enumerate([52, 70, 44]))
        qr = ''.join('<rect class="a-ink-fill" x="%d" y="%d" width="7" height="7"/>' % (284 + (k % 6) * 9, 64 + (k // 6) * 9)
                     for k in [0, 1, 2, 4, 5, 6, 8, 11, 13, 15, 17, 18, 21, 22, 24, 26, 29, 30, 31, 33, 35])
        inner = f'''<g class="float-a">
  <rect class="a-phone" x="110" y="26" width="152" height="214" rx="24"/>
  <rect class="a-card" x="118" y="40" width="136" height="192" rx="14"/>
  <rect class="a-g" x="128" y="50" width="62" height="10" rx="5"/>{fields}
  <rect class="a-g" x="128" y="204" width="116" height="20" rx="10"/>
  <path class="a-check" d="M219 167l6 6 12-12"/>
</g>
<g class="float-b">
  <rect class="a-card" x="272" y="52" width="80" height="80" rx="12"/>{qr}
  <line class="a-scan" x1="278" y1="92" x2="346" y2="92"/>
</g>
<g class="float-c">
  <rect class="a-card" x="30" y="150" width="96" height="62" rx="12"/>
  <circle cx="52" cy="181" r="10" class="a-gs-fill"/><path class="a-pin" d="M52 172c-4.4 0-8 3.4-8 7.6 0 5.4 8 12.4 8 12.4s8-7 8-12.4c0-4.2-3.6-7.6-8-7.6z"/>
  <rect class="a-line" x="70" y="172" width="40" height="7" rx="3.5"/><rect class="a-mu" x="70" y="186" width="28" height="7" rx="3.5"/>
</g>'''
        return _svg(inner, 'a phone showing a Survey123 form, a QR code being scanned and a GPS location card')
    if slug == 'case-chw-card-studio':
        qr = ''.join('<rect class="a-ink-fill" x="%d" y="%d" width="6" height="6"/>' % (238 + (k % 5) * 8, 108 + (k // 5) * 8)
                     for k in [0, 1, 2, 4, 5, 7, 9, 10, 12, 14, 15, 17, 19, 20, 21, 22, 24])
        inner = f'''<g class="float-c"><rect class="a-card a-back" x="96" y="52" width="232" height="146" rx="16" transform="rotate(-7 212 125)"/></g>
<g class="float-a">
  <rect class="a-card" x="76" y="62" width="232" height="146" rx="16"/>
  <rect class="a-g" x="76" y="62" width="232" height="34" rx="16"/><rect class="a-g" x="76" y="80" width="232" height="16"/>
  <rect class="a-white" x="92" y="74" width="70" height="9" rx="4.5"/>
  <rect class="a-gs" x="92" y="110" width="58" height="72" rx="10"/><circle class="a-g" cx="121" cy="136" r="13"/><path class="a-g" d="M100 176c3-13 11-19 21-19s18 6 21 19z"/>
  <rect class="a-line" x="162" y="114" width="62" height="9" rx="4.5"/><rect class="a-mu" x="162" y="132" width="46" height="7" rx="3.5"/><rect class="a-mu" x="162" y="146" width="56" height="7" rx="3.5"/>
  <rect class="a-am" x="162" y="166" width="40" height="14" rx="7"/>{qr}
</g>
<g class="float-b">
  <circle cx="318" cy="66" r="26" class="a-ok"/><path class="a-check-w" d="M306 66l8 8 16-16"/>
</g>'''
        return _svg(inner, 'a Community Health Worker ID card with a photo placeholder, a QR code and a verified tick')
    if slug == 'case-dms':
        mods = ''
        k = 0
        for r in range(3):
            for c in range(4):
                if k >= 11:
                    break
                cls = 'a-g' if k in (0, 5) else ('a-am' if k == 9 else 'a-gs')
                mods += '<rect class="%s mod" style="--i:%d" x="%d" y="%d" width="44" height="34" rx="8"/>' % (cls, k, 150 + c * 52, 52 + r * 46)
                k += 1
        inner = f'''<g class="float-c">
  <ellipse class="a-db" cx="80" cy="74" rx="44" ry="13"/><path class="a-db" d="M36 74v86c0 7 20 13 44 13s44-6 44-13V74"/>
  <path class="a-db-line" d="M36 103c0 7 20 13 44 13s44-6 44-13M36 132c0 7 20 13 44 13s44-6 44-13"/>
</g>
<path class="a-link" d="M124 112C140 112 136 86 150 86M124 120C140 120 136 160 150 160"/>
<g class="float-a"><rect class="a-card" x="138" y="38" width="236" height="166" rx="16"/>{mods}</g>
<g class="float-b"><rect class="a-card" x="300" y="176" width="78" height="44" rx="12"/><rect class="a-g" x="312" y="190" width="18" height="18" rx="5"/><rect class="a-line" x="336" y="194" width="30" height="7" rx="3.5"/></g>'''
        return _svg(inner, 'a database connected to a grid of eleven system modules')
    return ''


_I = {
    'chart': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'form': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v2h6V3M8.5 11l2 2 4-4M8.5 17h7"/>',
    'check': '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'report': '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>',
    'db': '<ellipse cx="12" cy="5.5" rx="8" ry="2.8"/><path d="M4 5.5v13c0 1.5 3.6 2.8 8 2.8s8-1.3 8-2.8v-13M4 12c0 1.5 3.6 2.8 8 2.8s8-1.3 8-2.8"/>',
    'teach': '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
    'tool': '<path d="M14.5 6.5a4 4 0 0 0 5 5L12 19a2.1 2.1 0 0 1-3-3l7.5-7.5"/><path d="M4 20l3-3"/>',
    'wifi': '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1"/>',
    'web': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>',
    'lock': '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',
    'office': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
}


def icon(name):
    return '<span class="svc-ico" aria-hidden="true"><svg viewBox="0 0 24 24">%s</svg></span>' % _I[name]
