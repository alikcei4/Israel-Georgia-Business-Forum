from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).parent
names = ['index.html', 'ru.html', 'he.html', 'styles.css', 'script.js',
         'favicon.svg', '.nojekyll', 'README.md', 'content.json',
         'content-ru.json', 'content-he.json', 'photo-manifest.json',
         'build_html_site.py', 'package_site.py',
         'assets/forum-video.mp4', 'assets/video-poster.jpg']
files = [root / name for name in names] + sorted((root / 'assets/photos').glob('*.jpg'))
with ZipFile(root / 'bgc-forum-github-pages.zip', 'w', ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.relative_to(root).as_posix())
print('Packaged English, Russian and Hebrew pages, shared photos and video.')
