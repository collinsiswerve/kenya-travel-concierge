"""Rebuild efficient assets; the published website needs no Python dependencies.

Development only: python -m pip install Pillow fonttools brotli
Then run this script followed by scripts/build.py.
"""
from pathlib import Path
import argparse
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'dist' / 'assets'
IMAGES = ASSETS / 'images'
IMAGES.mkdir(exist_ok=True)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--images-only', action='store_true', help='Keep existing font files')
args = parser.parse_args()
manifest_path = ROOT / 'data/imagery.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for name, item in manifest['images'].items():
    with Image.open(ROOT / item['source']) as source:
        source = source.convert('RGB')
        widths = ([source.width] if name == 'kenya-luxury-hero'
                  else sorted({min(640, source.width), min(1280, source.width)}))
        for width in widths:
            image = source.resize((width, round(width * source.height / source.width)),
                                  Image.Resampling.LANCZOS)
            image.save(IMAGES / f'{name}-{width}.avif', format='AVIF', quality=62, speed=6)
            image.save(IMAGES / f'{name}-{width}.webp', format='WEBP', quality=86, method=6)
        item.update(width=source.width, height=source.height, widths=widths)
        if name == 'kenya-luxury-hero':
            social = source.resize((1200, round(1200 * source.height / source.width)),
                                   Image.Resampling.LANCZOS)
            social.save(IMAGES / 'kenya-luxury-social.jpg', quality=89, optimize=True)
        print(name, ':', ', '.join(str(width) + 'px' for width in widths))
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
                         encoding='utf-8')

if not args.images_only:
    from fontTools.ttLib import TTFont
    for source in sorted(ASSETS.glob('font-*.ttf')):
        font = TTFont(source)
        font.flavor = 'woff2'
        output = source.with_suffix('.woff2')
        font.save(output)
        compressed = TTFont(output)
        if (font.getBestCmap() != compressed.getBestCmap()
                or font['hmtx'].metrics != compressed['hmtx'].metrics):
            raise RuntimeError('Font characters or metrics changed: ' + source.name)

print('Updated imagery. Run python3 scripts/build.py next.')
