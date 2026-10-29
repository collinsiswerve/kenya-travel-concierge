"""Check both the GitHub Pages upload and the retained dist website."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SERVICES = json.loads((ROOT / 'data/services.json').read_text(encoding='utf-8'))
ERRORS = []


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.h1 = 0
        self.title = False
        self.description = False
        self.canonical = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                ERRORS.append('Duplicate id: ' + attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'title':
            self.title = True
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = True
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href', '')
        if tag == 'a' and attrs.get('target') == '_blank' and 'noopener' not in attrs.get('rel', ''):
            ERRORS.append('External target lacks noopener')
        if tag == 'img' and not attrs.get('alt'):
            ERRORS.append('Image has no alt text')
        for key in ('href', 'src', 'action'):
            if attrs.get(key):
                self.links.append(attrs[key])
        for candidate in attrs.get('srcset', '').split(','):
            if candidate.strip():
                self.links.append(candidate.strip().split()[0])


def inspect(site):
    files = list(site.rglob('*.html'))
    if site == ROOT:
        files = [file for file in files if not file.is_relative_to(ROOT / 'dist')]
    documents = {}
    for file in files:
        document = Document()
        document.feed(file.read_text(encoding='utf-8'))
        documents[file.resolve()] = document
        if document.h1 != 1 or not document.title or not document.description:
            ERRORS.append(str(file.relative_to(ROOT)) + ': missing heading/title/description')
    homepage = documents[(site / 'index.html').resolve()]
    public_base = urlsplit(homepage.canonical).path.rstrip('/')
    checked = 0
    for file, document in documents.items():
        for link in document.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith('/'):
                local = unquote(url.path)
                if public_base and local.startswith(public_base + '/'):
                    local = local[len(public_base):]
                target = site / local.lstrip('/')
            elif url.path:
                target = file.parent / unquote(url.path)
            else:
                target = file
            target = target.resolve()
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                ERRORS.append(str(file.relative_to(ROOT)) + ': missing target ' + link)
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                ERRORS.append(str(file.relative_to(ROOT)) + ': missing anchor ' + link)
            checked += 1
    for css in (site / 'assets').glob('*.css'):
        for match in re.finditer(r"""url\(\s*['"]?([^)'"]+)""", css.read_text(encoding='utf-8')):
            url = urlsplit(match.group(1).strip())
            if not url.scheme and not url.netloc and not (css.parent / unquote(url.path)).is_file():
                ERRORS.append(str(css.relative_to(ROOT)) + ': missing CSS resource ' + url.path)
    if len(SERVICES) != 10:
        ERRORS.append('Expected ten services')
    for service in SERVICES:
        file = site / 'services' / service['slug'] / 'index.html'
        if not file.is_file():
            ERRORS.append('Missing service page: ' + str(file.relative_to(ROOT)))
        elif 'service=' + service['slug'] not in file.read_text(encoding='utf-8'):
            ERRORS.append('Enquiry selection missing: ' + service['slug'])
    expected = len(SERVICES) + (6 if site == ROOT else 7)
    if len(documents) != expected:
        ERRORS.append('Unexpected HTML page count in ' + str(site))
    return len(documents), checked


results = [inspect(ROOT), inspect(ROOT / 'dist')]
if ERRORS:
    print('\n'.join(sorted(set(ERRORS))))
    sys.exit(1)
print('PASS: root contains all 15 content pages and 404.html; dist retains its 404 route; '
      + str(sum(links for _, links in results))
      + ' local links, assets and anchors; fonts; all ten services; metadata and enquiry links.')

