#!/usr/bin/env python3
"""Makes capability-statement.pdf and cv-from-site.pdf from the built print pages (needs playwright)."""
import os, subprocess, sys, time
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8799', '--directory', ROOT], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for src, out in [('capability-statement.html', 'capability-statement.pdf'), ('cv.html', 'cv-from-site.pdf')]:
            pg.goto('http://localhost:8799/' + src); pg.emulate_media(media='print')
            pg.pdf(path=os.path.join(ROOT, out), format='A4', margin=dict(top='14mm', bottom='14mm', left='14mm', right='14mm'))
        b.close()
finally:
    srv.terminate()
print('pdfs written')
