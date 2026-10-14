from pathlib import Path
from pypdf import PdfReader
from PIL import Image

root = Path(__file__).parent
pages_dir = root / 'assets' / 'pages'
pages_dir.mkdir(exist_ok=True)
reader = PdfReader(r'C:/Users/alikc/OneDrive/Desktop/ENG_202026_20-_20corrected.pdf')
descriptions = [
    'Business Government Contact — BGC International. Israel–Georgia Real Estate and Business Tourism Forum. Cover and organizer logos.',
    'Forum introduction, December 8 at Pullman Tbilisi Axis Towers, and organizers Israel Georgia Business House and Business Media Contact.',
    'Gala dinner, award ceremony, international participants, and event photographs.',
    'Georgian real estate market topics, conference photographs, and remote business opportunities.',
    'Developer project presentations, investment offers, and panel discussions.',
    'Welcome party, networking, workshops, B2B and B2C meetings, and project presentations.',
    'Georgian market trends for 2026–2030, investment strategies, and development photographs.',
    'Bank offers, mortgage terms, legal assistance and international transfers.',
    'Company and property registration support, hotel offers, and forum participation opportunities.',
    'International hotel partnerships and government investment projects.',
    'Insurance offers, business and investment consultation, and legal support.',
    'Business tours, wine tourism, medical tourism, hospitality and resort opportunities.',
    'Invitation to the Georgian market and Israel–Georgia Business Forum media coverage.',
    'Business and government nominees, future partners and media logos.',
    'Social media links, WhatsApp, email, and Israel–Georgia Business Forum registration.',
]
assert len(reader.pages) == len(descriptions)
for number, page in enumerate(reader.pages, 1):
    image = page.images[0].image.convert('RGB')
    image.thumbnail((2560, 1440), Image.Resampling.LANCZOS)
    image.save(pages_dir / f'page-{number:02}.webp', quality=95, method=6)
    print(f'Prepared page {number}/15', flush=True)

page_markup = []
for number, description in enumerate(descriptions, 1):
    loading = 'fetchpriority="high"' if number == 1 else 'loading="lazy"'
    page_markup.append(f'''    <section class="pdf-page" id="page-{number}" aria-label="Page {number} of 15">
      <a class="page-link" href="assets/pages/page-{number:02}.webp" target="_blank" rel="noopener" aria-label="Open page {number} at full size">
        <img src="assets/pages/page-{number:02}.webp" width="2560" height="1440" {loading} alt="Page {number}: {description}">
      </a>
    </section>''')

(root / 'index.html').write_text('''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Israel–Georgia Real Estate and Business Tourism Forum. The complete original 15-page presentation.">
  <meta name="theme-color" content="#05336d">
  <title>Israel–Georgia Business Forum</title>
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main aria-label="Complete Israel–Georgia Business Forum presentation">
''' + '\n'.join(page_markup) + '''
  </main>
  <nav class="document-tools" aria-label="Document tools">
    <a href="#page-1">Back to top ↑</a>
  </nav>
</body>
</html>
''', encoding='utf-8')

(root / 'styles.css').write_text('''* { box-sizing: border-box; }
html { scroll-behavior: smooth; background: #05336d; }
body { margin: 0; }
main { width: 100%; margin: 0 auto; max-width: 2560px; }
.pdf-page { margin: 0; padding: 0; aspect-ratio: 16 / 9; background: #05336d; }
.page-link { display: block; width: 100%; height: 100%; cursor: zoom-in; }
.pdf-page img { display: block; width: 100%; height: auto; }
a:focus-visible { outline: 4px solid #00b9e7; outline-offset: -4px; }
.document-tools { display: flex; justify-content: center; flex-wrap: wrap; gap: 16px 36px; padding: 24px; background: #05336d; color: white; font: 13px/1.6 Arial, sans-serif; }
.document-tools a { color: inherit; text-underline-offset: 4px; }
@media (max-width: 600px) { .document-tools { padding: 20px 14px; gap: 14px 22px; font-size: 12px; } }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
''', encoding='utf-8')

(root / 'README.md').write_text('''# Israel–Georgia Business Forum

This version preserves all 15 pages of the supplied PDF in their original order, including the complete text, images, logos, layout, and spelling. No copy is rewritten or removed.

The PDF contains flattened page images. For visual fidelity the site displays high-resolution images of those pages in one vertical document. Text is therefore part of the image, not selectable HTML text. On a phone, tap a page to open it at full size and zoom.

## Preview
Open `index.html` or run `python -m http.server 8000`.

## GitHub Pages
Upload `index.html`, `styles.css`, `favicon.svg`, `.nojekyll`, and the `assets/pages` folder to a public repository. In Settings → Pages choose Deploy from a branch, main, /(root), then Save. All asset paths are relative and support a repository subpath.

The page itself has no external dependencies or registration form. Contact and social details remain exactly as shown in the PDF. Page images open individually on click.

`prepare_pdf_site.py` rebuilds this version from the source PDF path using Pillow and pypdf. The original landing page files are preserved locally in `tmp/previous-landing`.
''', encoding='utf-8')
