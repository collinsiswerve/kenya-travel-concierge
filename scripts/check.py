"""Verify the distributable's links, assets, service coverage and document structure."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
errors = []
pages = list(DIST.rglob('*.html'))

class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.h1=0; self.title=False; self.description=False; self.images=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: errors.append(f'Duplicate id: {a["id"]}')
            self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='title': self.title=True
        if tag=='meta' and a.get('name')=='description': self.description=True
        if tag=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):
            errors.append('External target lacks noopener')
        if tag=='img' and not a.get('alt'): errors.append('Image has no alt text')
        for k in ('href','src'):
            if a.get(k): self.links.append(a[k])

for page in pages:
    doc=Document(); doc.feed(page.read_text())
    if doc.h1!=1 or not doc.title or not doc.description: errors.append(f'{page.relative_to(DIST)}: missing heading/title/description')
    for link in doc.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        if u.path:
            target=(DIST/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (page.parent/unquote(u.path))
            if target.is_dir(): target=target/'index.html'
            if not target.exists(): errors.append(f'{page.relative_to(DIST)}: missing local target {link}')
        elif u.fragment and u.fragment not in doc.ids:
            errors.append(f'{page.relative_to(DIST)}: missing anchor {link}')

services=json.loads((ROOT/'data/services.json').read_text())
assert len(services)==10
for service in services:
    file=DIST/'services'/service['slug']/'index.html'
    if not file.exists(): errors.append(f'Missing service page: {service["slug"]}')
    elif 'service='+service['slug'] not in file.read_text(): errors.append(f'Enquiry selection missing: {service["slug"]}')
if errors:
    print('\n'.join(sorted(set(errors)))); sys.exit(1)
print(f'PASS: {len(pages)} HTML documents; all local links and assets; all ten services; headings, metadata, alt text, and enquiry links.')
