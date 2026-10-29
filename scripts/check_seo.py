"""Verify indexable pages, schema, canonical URLs, sitemap and optimized assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin, unquote
from xml.etree import ElementTree
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = json.loads((ROOT / 'data/site.json').read_text(encoding='utf-8'))
SERVICES = json.loads((ROOT / 'data/services.json').read_text(encoding='utf-8'))
IMAGERY = json.loads((ROOT / 'data/imagery.json').read_text(encoding='utf-8'))['images']
ORIGIN = os.getenv('SITE_URL', SITE['url']).rstrip('/')
ERRORS = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.metas = {}
        self.canonical = ''
        self.schemas = []
        self.preloads = []
        self.images = []
        self.sources = []
        self.styles = []
        self.in_style = False
        self.visible = []
        self.in_title = False
        self.in_schema = False
        self.in_head = False
        self.in_script = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'head':
            self.in_head = True
        if tag == 'style':
            self.in_style = True
        if tag == 'source':
            self.sources.append(a)
        if tag == 'title':
            self.in_title = True
        if tag == 'script':
            self.in_script = True
            self.in_schema = a.get('type') == 'application/ld+json'
        if tag == 'meta':
            self.metas[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href', '')
        if tag == 'link' and a.get('rel') == 'preload':
            self.preloads.append(a)
        if tag == 'img':
            self.images.append(a)

    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False
        if tag == 'style':
            self.in_style = False
        if tag == 'title':
            self.in_title = False
        if tag == 'script':
            self.in_schema = False
            self.in_script = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_style:
            self.styles.append(data)
        if self.in_schema:
            try:
                self.schemas.append(json.loads(data))
            except ValueError:
                ERRORS.append('Invalid JSON-LD')
        if not self.in_head and not self.in_script:
            self.visible.append(data)


def read(path):
    page = Page()
    page.feed(path.read_text(encoding='utf-8'))
    return page


def require(condition, message):
    if not condition:
        ERRORS.append(message)



def check_inline_assets(page, page_url):
    base = urlsplit(ORIGIN).path.rstrip('/') + '/'
    for resource in re.findall(r"""url\(\s*['"]?([^)'"]+)""", ''.join(page.styles)):
        url = urlsplit(urljoin(page_url, resource))
        if url.netloc != urlsplit(ORIGIN).netloc:
            continue
        require(url.path.startswith(base), 'Inline CSS escapes site base: ' + resource)
        target = ROOT / unquote(url.path.removeprefix(base))
        require(target.is_file(), 'Missing inline CSS resource: ' + str(target))

paths = ['/', '/services/', '/contact/', '/privacy/', '/terms/'] + [
    '/services/' + item['slug'] + '/' for item in SERVICES
]
titles = set()
descriptions = set()
for path in paths:
    page = read(ROOT / path.lstrip('/') / 'index.html')
    expected = ORIGIN + path
    check_inline_assets(page, expected)
    require(page.canonical == expected, 'Wrong canonical: ' + path)
    require('noindex' not in page.metas.get('robots', ''), 'Indexing blocked: ' + path)
    require(page.title not in titles and page.title.strip(), 'Duplicate/empty title: ' + path)
    description = page.metas.get('description', '')
    require(description and description not in descriptions, 'Duplicate/empty description: ' + path)
    titles.add(page.title)
    descriptions.add(description)
    for key in ['og:title', 'og:description', 'og:image', 'og:image:alt',
                'twitter:card', 'twitter:image', 'twitter:image:alt']:
        require(bool(page.metas.get(key)), 'Missing ' + key + ': ' + path)
    require(page.metas.get('og:url') == expected, 'Wrong social URL: ' + path)
    require(bool(page.schemas), 'Missing structured data: ' + path)
    graph = [node for schema in page.schemas for node in schema.get('@graph', [])]
    types = {node.get('@type') for node in graph}
    if path == '/':
        require({'Organization', 'WebSite', 'WebPage'} <= types, 'Missing business/website graph')
        hero = next((i for i in page.images if i.get('class') == 'hero-image'), {})
        require('/assets/images/kenya-luxury-hero-' in hero.get('src', '')
                and hero.get('src', '').endswith('.webp'), 'Hero not optimized')
        require(hero.get('fetchpriority') == 'high' and hero.get('loading') != 'lazy',
                'Hero must load promptly')
        candidates = {hero.get('src')} | {
            entry.strip().split()[0] for source in page.sources
            for entry in source.get('srcset', '').split(',') if entry.strip()}
        require(any(p.get('href') in candidates and p.get('as') == 'image'
                    for p in page.preloads), 'Hero preload does not match image')
    if path.startswith('/services/'):
        breadcrumbs = [node for node in graph if node.get('@type') == 'BreadcrumbList']
        require(len(breadcrumbs) == 1, 'Missing breadcrumb: ' + path)
        for breadcrumb in breadcrumbs:
            items = breadcrumb.get('itemListElement', [])
            require(len(items) >= 2, 'Breadcrumb too short: ' + path)
            require([i.get('position') for i in items] == list(range(1, len(items) + 1)),
                    'Breadcrumb ordering: ' + path)
            require(all(i.get('name') and i.get('item', '').startswith(ORIGIN + '/')
                        for i in items), 'Invalid breadcrumb entry: ' + path)
    service = next((item for item in SERVICES
                    if path == '/services/' + item['slug'] + '/'), None)
    if service:
        require(any('/assets/images/' + service['image'] + '-' in image.get('src', '')
                    for image in page.images), 'Service image missing: ' + path)
        require('Service' in types, 'Missing service schema: ' + path)
        service_nodes = [node for node in graph if node.get('@type') == 'Service']
        require(len(service_nodes) == 1 and service_nodes[0].get('url') == expected,
                'Wrong service schema URL: ' + path)
        require(service['description'] in ' '.join(page.visible),
                'Service description missing from visible page: ' + path)
    for node in graph:
        require('aggregateRating' not in node and 'review' not in node,
                'Unverified review markup: ' + path)
        require(not (node.get('@type') == 'Organization' and 'address' in node),
                'Business address requires verification')

sitemap = ElementTree.parse(ROOT / 'sitemap.xml')
namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [item.text for item in sitemap.findall('.//s:loc', namespace)]
require(len(urls) == len(set(urls)) == len(paths), 'Sitemap count/duplicates')
require(set(urls) == {ORIGIN + path for path in paths}, 'Sitemap and canonicals differ')
require('noindex' in read(ROOT / '404.html').metas.get('robots', ''), '404 should not be indexed')
check_inline_assets(read(ROOT / '404.html'), ORIGIN + '/missing/deep/path')
for path in (ROOT / 'dist').rglob('*.html'):
    if path.name != '404.html' and path.parent.name != '404':
        require(read(path).canonical.startswith(ORIGIN + '/'),
                'Alternate build canonical differs: ' + str(path))

fonts = (ROOT / 'assets/fonts.css').read_text(encoding='utf-8')
require('.ttf' not in fonts and fonts.count('.woff2') == 9, 'Efficient font URLs missing')
for file in (ROOT / 'assets').glob('font-*.woff2'):
    require(file.read_bytes().startswith(b'wOF2'), 'Invalid WOFF2: ' + file.name)
require(len(list((ROOT / 'assets').glob('font-*.woff2'))) == 9, 'Missing font file')
require(len(IMAGERY) == 12, 'Expected twelve original brand images')
for name, item in IMAGERY.items():
    require((ROOT / item['source']).is_file(), 'Missing image source: ' + name)
    require(item.get('alt') and 'brand illustration' in item['alt'],
            'Missing descriptive illustration alternative: ' + name)
    for width in item['widths']:
        require(width <= item['width'], 'Image was enlarged: ' + name)
        for extension, budget in [('avif', 300_000), ('webp', 500_000)]:
            asset = ROOT / 'assets/images' / f'{name}-{width}.{extension}'
            require(asset.is_file() and 0 < asset.stat().st_size < budget,
                    'Missing image or exceeds asset budget: ' + asset.name)
    if name != 'kenya-luxury-hero':
        require(len(item['widths']) == 2, 'Responsive image variants missing: ' + name)
require((ROOT / '.nojekyll').is_file(), 'GitHub static publishing marker missing')

if ERRORS:
    print('\n'.join(ERRORS))
    sys.exit(1)
print('PASS: 15 unique, indexable pages; matching sitemap/canonicals; Organization, '
      'WebSite, Service and breadcrumb JSON-LD; social previews; error-page exclusion; '
      'twelve optimized responsive brand images and all nine WOFF2 fonts.')
