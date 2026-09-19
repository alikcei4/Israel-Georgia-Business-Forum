# Israel–Georgia Business Forum

A real, responsive HTML/CSS website with the complete English content from the supplied 15-page PDF. Text is selectable, searchable and editable. Photos and graphic assets are separate JPEGs. The site does not render the PDF as page images.

## Content
- `content.json` contains the original numbered body copy, preserving its order and wording. The source skips point 13; this is preserved.
- `index.html` contains the full site, including the cover, programme, nominee graphics and contact details.
- `styles.css` adapts the layout to desktops and phones.
- `script.js` controls the mobile menu.
- `assets/photos/` contains cropped photographs and graphic assets from the PDF.
- Contact links open WhatsApp, email and the social profiles printed in the PDF.
- The PDF shows a registration-form label but does not contain a working form URL. That label is retained as text; no fake registration form is added.
- Source wording, dates and claims are reproduced without independent fact-checking. Original spelling is preserved.

## Local preview
Open `index.html` or run `python -m http.server 8000` and visit http://localhost:8000.

## Publish on GitHub Pages
Upload `index.html`, `styles.css`, `script.js`, `favicon.svg`, `.nojekyll` and `assets/photos/` to a public repository. Select Settings → Pages → Deploy from a branch → main → /(root) → Save. All asset paths are relative, so repository URLs work.

`bgc-forum-github-pages.zip` contains the current site and only the assets it uses. It excludes the old full-page WEBP version and the oversized source PDF.

## Editing and rebuilding
Edit `content.json` for numbered text, or edit `index.html` directly. `build_html_site.py` rebuilds the HTML using `content.json` and `photo-manifest.json`. `extract_site_photos.py` crops photos from the original PDF using pypdf and Pillow. These scripts are not needed for hosting.

Google Fonts is optional; Arial is used as a fallback. No hosting backend is needed.
