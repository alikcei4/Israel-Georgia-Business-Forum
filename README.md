# Israel–Georgia Business Forum

Responsive HTML website in English, Russian and Hebrew, ready for GitHub Pages.

## Pages
- `index2.html`: a separate Georgian page based on the owner's `Geo.pptx`, with its complete Georgian body copy, nominee logos and contact URLs. It uses `georgia.css` in addition to the shared stylesheet. It is separate from the three-language page switch.
- `index.html`: English, using the source PDF text. The confirmed event date is December 21.
- `ru.html`: Russian text supplied by the owner, retaining its numbering and wording.
- `he.html`: Hebrew translation of the supplied Russian text, with right-to-left layout.
- The language switch preserves the current section. Photos, video and contact destinations are shared.
- The header contains WhatsApp, Registration and the three-language switch.
- Registration opens the Google Form supplied by the owner.
- A playable video section appears before the social buttons. It uses `assets/forum-video.mp4` and a poster image.

## Preview and publish
Open a page directly or run `python -m http.server 8000`.
Upload the three HTML pages, `styles.css`, `script.js`, `favicon.svg`, `.nojekyll`, and the media assets to the repository. Under Settings → Pages, select Deploy from a branch, main, /(root).
The ZIP contains all required pages, photos and video. Old full-page WEBP files and the oversized PDF are excluded.

## Rebuild
Edit `content.json`, `content-ru.json` or `content-he.json` for body copy. Run:

```
python build_html_site.py
python build_html_site.py --ru
python build_html_site.py --he
python package_site.py
```

Use `styles.css` for layout changes. The site uses optional Google Fonts with local fallbacks. No backend is required.

To rebuild the separate Georgian page, run `python build_georgia_site.py` with the original `Geo.pptx` in the project folder. Its source images are stored in `assets/geo/`. The Georgian page shares the existing forum video and registration destination. The publication ZIP includes this page and its assets; the source presentation is not required for hosting.
