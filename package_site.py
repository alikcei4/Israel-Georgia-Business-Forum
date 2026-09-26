from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).parent
names = ['index.html', 'ru.html', 'he.html', 'index2.html', 'index2-en.html', 'index2-ru.html', 'content-geo-ru.json', 'build_geo_russian.py', 'content-geo-en.json', 'build_geo_english.py', 'styles.css', 'georgia.css', 'script.js',
         'favicon.svg', '.nojekyll', 'README.md', 'content.json',
         'content-ru.json', 'content-he.json', 'photo-manifest.json',
         'build_html_site.py', 'build_georgia_site.py', 'content-geo.json', 'geo-media.json', 'package_site.py',
         'assets/forum-video.mp4', 'assets/video-poster.jpg']
files = [root / name for name in names] + sorted((root / 'assets/photos').rglob('*.jpg')) + sorted((root / 'assets/geo').glob('*.jpg')) + sorted(path for path in (root / 'assets/Photo geo').rglob('*') if path.is_file() and path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.svg'})
with ZipFile(root / 'bgc-forum-github-pages.zip', 'w', ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.relative_to(root).as_posix())
print('Packaged the multilingual website and separate Georgian page, photos and video.')
