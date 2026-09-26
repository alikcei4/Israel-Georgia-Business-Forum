"""Build the separate Georgian landing page from the owner's Geo.pptx."""
from pathlib import Path
from zipfile import ZipFile
from html import escape
from lxml import etree as ET
import json
import re
from hashlib import sha256
from urllib.parse import quote

ROOT = Path(__file__).parent
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
slides = []
if (ROOT / 'Geo.pptx').exists():
    with ZipFile(ROOT / 'Geo.pptx') as deck:
        names = sorted((name for name in deck.namelist()
                        if re.fullmatch(r'ppt/slides/slide\d+\.xml', name)),
                       key=lambda name: int(re.search(r'slide(\d+)', name).group(1)))
        for name in names:
            xml = ET.fromstring(deck.read(name))
            paragraphs = [''.join(p.xpath('.//a:t/text()', namespaces=NS)).strip()
                          for p in xml.xpath('//a:p', namespaces=NS)]
            slides.append([p for p in paragraphs if p])
else:
    slides=json.loads((ROOT / 'content-geo.json').read_text(encoding='utf-8'))

(ROOT / 'content-geo.json').write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding='utf-8')
REGISTRATION = 'https://docs.google.com/forms/d/1Qq1ImnOtpxSEg5opsbDKPuPpdpTFv3wMbR0NnLVHbfA/viewform?edit_requested=true'
TITLE = 'Israel-Georgia Real Estate and Business Tourism Forum'
PHOTO_DATA = {item['name']: item for group in json.loads((ROOT / 'photo-manifest.json').read_text(encoding='utf-8')).values() for item in group}

def photograph(name, description):
    item = PHOTO_DATA[name]
    return f'<figure class="geo-editorial-photo"><img src="assets/Photo%20geo/{name}.jpg" alt="{escape(description)}" width="{item["width"]}" height="{item["height"]}" loading="lazy"></figure>'

def photo_group(items, layout='pair'):
    return '<div class="geo-photo-group geo-photo-'+layout+'">'+''.join(photograph(name, description) for name,description in items)+'</div>'

def image(number, alt, cls=''):
    return f'<img class="{cls}" src="assets/Photo%20geo/slide-02-image-{number:02}.jpg" alt="{escape(alt)}" loading="lazy">'

def organizer_logos():
    return '<div class="organizer-logos"><figure class="photo">'+image(48, 'Israel-Georgia Business House')+'</figure><figure class="photo">'+image(49, 'Business Media Contact')+'</figure></div>'

ADDITIONAL_PHOTOS = {3: [{'file': 'WhatsApp Image 2026-09-26 at 18.21.20.jpeg', 'width': 1600, 'height': 1066}, {'file': 'WhatsApp Image 2026-09-26 at 18.23.12.jpeg', 'width': 1600, 'height': 1193}], 4: [{'file': 'WhatsApp Image 2026-09-26 at 18.19.51.jpeg', 'width': 1600, 'height': 1447}, {'file': 'WhatsApp Image 2026-09-26 at 18.22.00.jpeg', 'width': 1600, 'height': 1066}], 5: [{'file': 'WhatsApp Image 2026-09-26 at 18.22.46.jpeg', 'width': 1600, 'height': 1062}, {'file': 'WhatsApp Image 2026-09-26 at 18.29.25.jpeg', 'width': 1200, 'height': 1600}], 6: [{'file': 'WhatsApp Image 2026-09-26 at 18.22.28.jpeg', 'width': 1600, 'height': 1066}], 7: [{'file': 'WhatsApp Image 2026-09-26 at 18.20.14.jpeg', 'width': 1600, 'height': 1062}, {'file': 'WhatsApp Image 2026-09-26 at 18.20.55.jpeg', 'width': 1072, 'height': 1601}, {'file': 'WhatsApp Image 2026-09-26 at 18.24.03.jpeg', 'width': 1600, 'height': 1066}], 8: [{'file': 'WhatsApp Image 2026-09-26 at 18.23.29.jpeg', 'width': 1600, 'height': 1396}, {'file': 'WhatsApp Image 2026-09-26 at 18.26.33.jpeg', 'width': 1600, 'height': 1482}], 10: [{'file': 'WhatsApp Image 2026-09-26 at 18.29.13.jpeg', 'width': 1600, 'height': 1066}]}

def additional_photos(number):
    items=ADDITIONAL_PHOTOS.get(number, [])
    if not items:
        return ''
    return '<div class="geo-added-photos">'+''.join(
        '<figure><img src="'+quote('assets/Photo geo/'+item['file'])+'" alt="ბიზნეს ღონისძიების მონაწილეები და დაჯილდოების ცერემონია" width="'+str(item['width'])+'" height="'+str(item['height'])+'" loading="lazy"></figure>'
        for item in items)+'</div>'

def paragraph(text, tone='navy'):
    return f'<div class="copy {tone}"><p>{escape(text)}</p></div>'

def section(number, heading, body, dark=False):
    return f'<section class="document-section geo-section{ " dark" if dark else ""}" id="geo-section-{number}" aria-labelledby="geo-heading-{number}"><div class="section-content"><div class="geo-section-heading"><span class="geo-section-index">{number:02}</span><div><p class="geo-series-title" lang="en">{TITLE}</p><h2 id="geo-heading-{number}">{escape(heading)}</h2></div></div>{body}</div></section>'

logo_names = {
2:'Radio Holding Fortuna',3:'Starvision',4:'Мир',5:'IPN',6:'პირველი არხი',7:'IMEDI.FM',8:'იმედი',9:'ფორმულა',10:'Rustavi 2',11:'TV პირველი',12:'Palitra News',13:'Euronews Georgia',14:'GNARE',15:'Частное мнение',16:'TV 9',17:'קשת 12',18:'MIGNEWS',19:'חדשות 13',20:'GTV',21:'მედია ლოგო',22:'POSTV',23:'Colliers',24:'ICC Georgia',25:'Georgia',26:'თბილისის მერია',27:'Schuchmann Wines Georgia',28:'Monolit Group',29:'Schuchmann',30:'კომპანიის ლოგო',31:'W.',32:'Iberia Star Group',33:'VR Holding',34:'Inn Group Hotels',35:'ბინ',36:'Pullman Tbilisi Axis Towers',37:'Bioli Wellness Resort',38:'Silk Hospitality',39:'REA Investment',40:'Total Charm',41:'Hairline International',42:'კომპანიის ლოგო',43:'კომპანიის ლოგო',44:'First Radio Israel',45:'REKA',46:'EU-Georgia Business Council',47:'Business Chamber of Asian & Gulf Countries'}
# Use the owner's numbered filenames as the displayed order.
partner_folder = ROOT / 'assets/Photo geo/partners'
partner_files = sorted(
    (path for path in partner_folder.iterdir()
     if path.is_file() and path.stem.isdigit() and path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.svg'}),
    key=lambda path: (int(path.stem), path.name))
# Preserve the known accessible brand names when an original logo was renamed.
logo_labels = {}
for number, label in logo_names.items():
    original = ROOT / 'assets/geo' / f'slide-02-image-{number:02}.jpg'
    if original.exists():
        logo_labels[sha256(original.read_bytes()).digest()] = label
logo_grid = '<div class="geo-logo-grid">' + ''.join(
    '<figure><img src="' + quote(path.relative_to(ROOT).as_posix()) + '" alt="' +
    escape(logo_labels.get(sha256(path.read_bytes()).digest(), 'პარტნიორი ' + path.stem), quote=True) +
    '" loading="lazy"></figure>' for path in partner_files) + '</div>'
parts=[section(2,'ბიზნესისა და სახელმწიფო სექტორის ნომინანტები','<p class="geo-source-heading" lang="en">Business and government nominees</p>'+logo_grid)]
headings={3:'ფორუმი და ორგანიზატორები',4:'ფორუმის მიზანი',5:'ფორუმის მონაწილეები',6:'ფორუმის ფორმატი',7:'დაჯილდოების ცერემონიალი',8:'პროექტების შერჩევის კრიტერიუმები',9:'პროექტების შერჩევის კრიტერიუმები',10:'მედია პარტნიორები'}
for number in range(3,11):
    text=[p for p in slides[number-1] if p!=TITLE]
    if number in (8,9):
        prose=[];criteria=[]
        for p in text:
            match=re.match(r'^(\d+)\.\s*(.*)',p)
            if match:
                criteria.append('<li><span class="geo-criterion-number">'+match[1]+'</span><p>'+escape(match[2])+'</p></li>')
            elif p!='წარდგენილი პროექტების შესარჩევი კრიტერიუმები:':
                prose.append(paragraph(p,'navy'))
        body=''.join(prose)+'<h3 class="geo-criteria-title">წარდგენილი პროექტების შესარჩევი კრიტერიუმები:</h3><ol class="geo-criteria" start="'+('1' if number==8 else '9')+'">'+''.join(criteria)+'</ol>'
    elif number==10:
        body=''.join(paragraph(p,'blue') for p in text if p.strip()!='მედია პარტნიორები')
    else:
        blocks=[paragraph(p, '' if number==7 else ('blue' if i%2==0 else 'navy')) for i,p in enumerate(text)]
        if number==3:
            blocks.insert(1,photo_group([('panel-2','ფორუმის სპიკერები და აუდიტორია')],'wide'))
        elif number==5:
            blocks.insert(1,photo_group([('hotel-4','უძრავი ქონების გამოფენის მონაწილეები'),('discussion-5','ბიზნეს ფორუმის სტუმრები'),('panel-1','პროფესიული პანელური დისკუსია')],'story'))
        elif number==6:
            blocks.insert(1,photo_group([('meeting-2','ბიზნეს პრეზენტაცია და ჯგუფური შეხვედრა'),('meeting-4','საქმიანი ურთიერთობები და არაფორმალური შეხვედრა')]))
        body='<div class="geo-copy-stack">'+''.join(blocks)+'</div>'
        if number==3:
            body+=organizer_logos()
    if number==4:
        body+=photo_group([('investment-1','თანამშრომლობის შეთანხმების ხელმოწერა'),('project-2','თანამედროვე საცხოვრებელი პროექტი')])
    elif number==6:
        body+=photo_group([('wine-estate','ქართული ღვინის მამული და ვენახები'),('support-2','სასტუმრო და დასასვენებელი სივრცე'),('tourism-1','ქართული ღვინის მარანი')],'trio')
    elif number==7:
        body+=photo_group([('award-2','ჯილდოს გადაცემის ცერემონიალი'),('award-6','დაჯილდოების მონაწილე სცენაზე'),('award-7','გალა ვახშმის სტუმრები')],'awards')
    elif number==9:
        body+=photo_group([('project-1','მწვანე გარემოში მდებარე სასტუმრო'),('forest-residences','საცხოვრებელი კომპლექსი ბუნებრივ გარემოში')])
    elif number==10:
        body+=photo_group([('insurance-4','ბიზნეს ფორუმის პრეზენტაცია და აუდიტორია')],'wide')
    body+=additional_photos(number)
    parts.append(section(number,headings[number],body,dark=number==7))

social_links=[
('https://www.facebook.com/businessmediacontact','Business Media Contact Facebook','f'),
('https://www.facebook.com/profile.php?id=100087925803122','Facebook — გვერდი','f'),
('https://www.facebook.com/share/12DFQhtdu2Y/','Facebook — პუბლიკაცია 1','f'),
('https://www.facebook.com/share/16nzBRinbZ/','Facebook — პუბლიკაცია 2','f'),
('https://www.instagram.com/israelgeorgiabusinesshouse/?igsh=a2cwcWd2YWY1NzNq','Israel-Georgia Business House Instagram','◎'),
('https://www.youtube.com/@businessmediacontactbmc7794','Business Media Contact YouTube','▶'),
('https://www.youtube.com/@israel-georgiabusinesshouse','Israel-Georgia Business House YouTube','▶')]
social_html='<ul class="social-links geo-social-links">'+''.join('<li><a class="social-button" href="'+escape(url,quote=True)+'" target="_blank" rel="noopener noreferrer"><span class="social-icon" aria-hidden="true">'+icon+'</span><span class="social-title">'+escape(label)+'</span><span class="social-arrow" aria-hidden="true">↗</span></a></li>' for url,label,icon in social_links)+'</ul>'

html='''<!doctype html>
<html lang="ka">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <meta name="theme-color" content="#063772">
 <meta name="description" content="Israel Georgia Business Forum და BGC International. 2026 წლის 21 დეკემბერი, Pullman Tbilisi Axis Towers. პროგრამა, ნომინანტები და საკონტაქტო ინფორმაცია.">
 <title>BGC International — საქართველო</title>
 <link rel="icon" href="favicon.svg" type="image/svg+xml">
 <link rel="stylesheet" href="styles.css">
 <link rel="stylesheet" href="georgia.css?v=languages-1">
 <link rel="alternate" hreflang="ka" href="index2.html">
 <link rel="alternate" hreflang="en" href="index2-en.html">
 <link rel="alternate" hreflang="ru" href="index2-ru.html">
 <script src="script.js" defer></script>
</head>
<body class="georgia-site">
 <a class="skip-link" href="#geo-main">შინაარსზე გადასვლა</a>
 <header class="site-header geo-header">
  <a class="wordmark" href="#geo-home" aria-label="BGC International — მთავარი">BGC<span>INTERNATIONAL</span></a>
  <a class="header-contact" href="https://wa.me/995511112441" target="_blank" rel="noopener noreferrer">WhatsApp <span aria-hidden="true">↗</span></a>
  <a class="header-registration" href="'''+escape(REGISTRATION,quote=True)+'''" target="_blank" rel="noopener noreferrer">რეგისტრაცია <span aria-hidden="true">↗</span></a>
  <nav class="language-switch" aria-label="საიტის ენა"><a class="language-link" href="index2.html" lang="ka" hreflang="ka" aria-current="page">ქართული</a><a class="language-link" href="index2-en.html" lang="en" hreflang="en">English</a><a class="language-link" href="index2-ru.html" lang="ru" hreflang="ru">Русский</a></nav>
 </header>
 <main id="geo-main">
  <section class="cover geo-cover" id="geo-home" aria-labelledby="geo-title">
   <div class="cover-architecture"><figure class="photo"><img src="assets/Photo%20geo/cover-georgia.jpg" alt="თანამედროვე არქიტექტურა საქართველოში" fetchpriority="high"></figure><figure class="photo"><img src="assets/Photo%20geo/cover-city.jpg" alt="ქალაქის პანორამა"></figure></div>
   <div class="cover-geometry" aria-hidden="true"></div>
   <div class="cover-content">
    <div class="cover-top"><p lang="en">BUSINESS GOVERNMENT CONTACT</p><h1 id="geo-title">BGC INTERNATIONAL<br>წარმატებული პროექტების დაჯილდოების ცერემონიალი</h1></div>
    '''+organizer_logos()+'''
    <h2>ისრაელ-საქართველოს უძრავი ქონებისა და ბიზნეს ტურიზმის ფორუმი</h2>
    <div class="geo-event-details"><span>21 დეკემბერი, 2026</span><span lang="en">Pullman Tbilisi Axis Towers</span></div>
   </div>
  </section>
'''+''.join(parts)+'''
  <section class="video-section" id="geo-video" aria-labelledby="geo-video-title"><div class="video-inner"><div class="video-heading"><div><p class="video-eyebrow">ვიდეო · 03:10</p><h2 id="geo-video-title">BGC International</h2></div><span class="video-caption" lang="en">Business Government Contact</span></div><video class="forum-video" controls playsinline preload="metadata" poster="assets/video-poster.jpg" width="848" height="478" aria-label="BGC International ვიდეო"><source src="assets/forum-video.mp4" type="video/mp4"><a href="assets/forum-video.mp4">ვიდეოს გახსნა</a></video></div></section>
  <section class="document-section contact-section" id="geo-contact" aria-labelledby="geo-contact-title"><div class="section-content"><div class="geo-section-heading"><span class="geo-section-index">11</span><div><p class="geo-series-title" lang="en">'''+TITLE+'''</p><h2 id="geo-contact-title">საკონტაქტო ინფორმაცია</h2></div></div><div class="contact-grid"><div>'''+social_html+'''</div><div class="geo-contact-details"><div class="contact-box"><p>ტელეფონი / WhatsApp / Telegram</p><a href="tel:+995511112441">+995 511112441</a><a href="https://wa.me/995511112441" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a></div><div class="geo-emails"><a href="mailto:businessmediacontact@gmail.com">businessmediacontact@gmail.com</a><a href="mailto:Israelgeorgiabusinesshouse@gmail.com">Israelgeorgiabusinesshouse@gmail.com</a></div>'''+organizer_logos()+'''</div></div><div class="registration-action"><a class="registration-button" href="'''+escape(REGISTRATION,quote=True)+'''" target="_blank" rel="noopener noreferrer">რეგისტრაცია <span aria-hidden="true">↗</span></a></div></div></section>
 </main>
 <footer><span lang="en">ISRAEL–GEORGIA BUSINESS FORUM</span><a href="#geo-home">ზემოთ ↑</a></footer>
</body>
</html>
'''
# Share the main English banner, preserving this page's home anchor.
main_page=(ROOT/'index.html').read_text(encoding='utf-8')
cover=re.search(r'<section class="cover".*?</section>',main_page,re.S).group(0).replace('id="home"','id="geo-home"')
html=re.sub(r'<section class="cover geo-cover".*?</section>',lambda match: cover,html,flags=re.S)
(ROOT/'index2.html').write_text(html,encoding='utf-8')
from build_geo_english import build_english
build_english(html)
from build_geo_russian import build_russian
build_russian()
print('Created the separate Georgian HTML page from Geo.pptx.')
