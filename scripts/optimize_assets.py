"""Rebuild efficient assets; the published website needs no Python dependencies.

Development only: python -m pip install Pillow fonttools brotli
Then run this script followed by scripts/build.py.
"""
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont

ASSETS = Path(__file__).resolve().parents[1] / 'dist' / 'assets'
with Image.open(ASSETS / 'kenya-savannah.png') as image:
    image.save(ASSETS / 'kenya-savannah.webp', format='WEBP', quality=88, method=6)

for source in sorted(ASSETS.glob('font-*.ttf')):
    font = TTFont(source)
    font.flavor = 'woff2'
    output = source.with_suffix('.woff2')
    font.save(output)
    compressed = TTFont(output)
    if (font.getBestCmap() != compressed.getBestCmap()
            or font['hmtx'].metrics != compressed['hmtx'].metrics):
        raise RuntimeError('Font characters or metrics changed: ' + source.name)

print('Updated WebP hero and WOFF2 fonts. Run python3 scripts/build.py next.')
