#!/usr/bin/env python3
"""Checks every local link, image, script and stylesheet in the built HTML. Exit 1 if any are missing."""
import os, re, sys
from html.parser import HTMLParser
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad, ids = [], {}

class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs = []; s.ids = set()
    def handle_starttag(s, tag, a):
        a = dict(a)
        if a.get('id'): s.ids.add(a['id'])
        for k in ('href', 'src'):
            if a.get(k): s.refs.append(a[k])
        if a.get('srcset'): s.refs += [x.split()[0] for x in a['srcset'].split(',')]

pages = {}
for f in sorted(os.listdir(ROOT)):
    if f.endswith('.html'):
        p = P(); p.feed(open(os.path.join(ROOT, f), encoding='utf-8').read()); pages[f] = p
for f, p in pages.items():
    for r in p.refs:
        if re.match(r'(https?:|mailto:|tel:|data:|//|javascript:)', r): continue
        path, _, frag = r.partition('#'); path = path.split('?')[0]
        target = path or f
        if not os.path.exists(os.path.join(ROOT, target)): bad.append(f'{f}: missing {r}')
        elif frag and target in pages and frag not in pages[target].ids: bad.append(f'{f}: no anchor {r}')
print('\n'.join(bad) or f'All local links OK in {len(pages)} pages')
sys.exit(1 if bad else 0)
