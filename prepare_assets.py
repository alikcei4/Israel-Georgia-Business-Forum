from pathlib import Path
from PIL import Image
from pypdf import PdfReader

out = Path('assets')
out.mkdir(exist_ok=True)
source = PdfReader(r'C:/Users/alikc/OneDrive/Desktop/ENG_202026_20-_20corrected.pdf')
def crop(page, box, name, width=None):
    original = source.pages[page - 1].images[0].image
    scale = original.width / 1440
    im = original.convert('RGB').crop(tuple(round(value * scale) for value in box))
    width = width or (1920 if name == 'architecture' else 1100)
    if width and im.width > width:
        im.thumbnail((width, 1800), Image.Resampling.LANCZOS)
    im.save(out / f'{name}.webp', quality=92)

crop(13, (742, 249, 1370, 598), 'architecture')
crop(4, (484, 286, 998, 633), 'conference')
crop(2, (58, 275, 445, 525), 'wine-estate')
crop(6, (988, 469, 1385, 731), 'networking')
crop(3, (49, 284, 349, 505), 'awards')
crop(15, (790, 65, 1356, 392), 'forum')
crop(14, (96, 104, 197, 193), 'business-house')
crop(14, (225, 107, 330, 191), 'business-media')
