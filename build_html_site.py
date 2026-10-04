from pathlib import Path
from html import escape
import json
import sys
from urllib.parse import quote

root=Path(__file__).parent
content=json.loads((root/'content.json').read_text(encoding='utf-8'))
language='he' if '--he' in sys.argv else ('ru' if '--ru' in sys.argv else 'en')
if language!='en':
    russian=json.loads((root/f'content-{language}.json').read_text(encoding='utf-8'))
    original=[p for section in content for p in section['paragraphs']]
    assert len(russian)==len(original)
    for source,translation in zip(original,russian):
        source['anchor_number']=source['number']
        source.update(translation)
manifest=json.loads((root/'photo-manifest.json').read_text(encoding='utf-8'))
photos={item['name']:item for group in manifest.values() for item in group}

def photo(name, cls='', eager=False):
    p=photos[name]
    loading='fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<figure class="photo {cls}"><img src="assets/photos/{name}.jpg" alt="{escape(p["alt"])}" width="{p["width"]}" height="{p["height"]}" {loading}></figure>'

def gallery(page, start=0, end=None, cls=''):
    return '<div class="gallery '+cls+'">'+''.join(photo(p['name']) for p in manifest[str(page)][start:end])+'</div>'

def para(record,cls=''):
    return f'<div class="copy {cls}" id="point-{record.get("anchor_number",record["number"])}"><p><span class="point-number">{record["number"]}.</span> {escape(record["text"])}</p></div>'

def logos(cls=''):
    return f'<div class="organizer-logos {cls}">'+photo('organizer-house')+photo('organizer-media')+'</div>'

def partner_grid():
    files=sorted(
        (path for path in (root/'assets/photos/partners').iterdir()
         if path.is_file() and path.stem.isdigit() and path.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.svg'}),
        key=lambda path: (int(path.stem),path.name))
    return '<div class="partner-logo-grid" dir="ltr">'+''.join(
        '<figure><img src="'+quote(path.relative_to(root).as_posix())+'" alt="Partner '+path.stem+'" loading="lazy"></figure>'
        for path in files)+'</div>'

labels={2:'Forum and organizers',3:'Gala dinner and participants',4:'Market analysis',5:'Projects and panel discussions',6:'Networking and presentations',7:'Investment strategies',8:'Banks and legal assistance',9:'Registration support and participation',10:'Hotels and government projects',11:'Insurance and consultation',12:'Tourism',13:'Invitation and media',14:'Nominees and future partners'}
sections=[]
for record in content:
    n=record['page']; ps=record['paragraphs']; dark=' dark' if record.get('dark') else ''
    if n==2:
        body=para(ps[0],'blue')+gallery(n,cls='three')+para(ps[1],'navy')
    elif n==3:
        body=para(ps[0],'navy')+gallery(n,cls='awards')+para(ps[1],'blue align-right')
    elif n==4:
        body=para(ps[0],'blue')+gallery(n,cls='three conference')+para(ps[1],'navy align-right')
    elif n==5:
        body='<div class="split top">'+para(ps[0])+ '<div>'+gallery(n,0,2,'two')+para(ps[1])+'</div></div>'+gallery(n,2,None,'three')
    elif n==6:
        body='<div class="split">'+para(ps[0],'navy')+gallery(n,0,2,'two')+'</div><div class="network-grid">'+photo('meeting-3')+para(ps[1],'blue')+photo('meeting-4')+'</div>'+para(ps[2],'navy')
    elif n==7:
        body=para(ps[0],'navy')+gallery(n,0,3,'market')+'<div class="split">'+photo('investment-4')+para(ps[1],'blue')+'</div>'
    elif n==8:
        body='<div class="bank-layout"><div>'+para(ps[0])+gallery(n,0,2,'two')+para(ps[1])+'</div>'+gallery(n,2,4,'stack')+gallery(n,4,6,'stack')+'</div>'
    elif n==9:
        body=para(ps[0],'blue')+gallery(n,0,3,'three')+'<div class="split weighted">'+photo('support-4')+para(ps[1],'navy')+'</div>'
    elif n==10:
        body='<div class="hotel-layout">'+para(ps[0],'blue')+photo('hotel-1')+photo('hotel-2')+photo('hotel-3')+photo('hotel-4')+para(ps[1],'navy')+'</div>'
    elif n==11:
        body='<div class="insurance-layout"><div>'+para(ps[0],'blue')+photo('insurance-3')+'</div><div>'+photo('insurance-1')+photo('insurance-4')+'</div>'+photo('insurance-2')+'</div>'+para(ps[1],'navy')
    elif n==12:
        body=gallery(n,0,3,'tourism')+'<div class="split tourism-copy">'+para(ps[0],'navy')+photo('tourism-4')+'</div>'
    elif n==13:
        body=para(ps[0],'statement')+'<p class="accent-statement">THE FORUM WILL BRING TOGETHER FUTURE PARTNERS!</p>'+gallery(n,cls='two projects')+'<div class="closing">'+logos()+'<div><h2 id="point-26"><span class="point-number">26.</span>ISRAEL GEORGIA BUSINESS FORUM</h2><p>The forum will be covered by Georgian and Israeli media</p></div></div>'
    elif n==14:
        body=para(ps[0],'navy centered')+'<div class="nominees-heading">'+logos()+'<div><h2>ISRAEL-GEORGIA REAL ESTATE AND<br> BUSINESS TOURISM FORUM</h2><h3>BUSINESS AND GOVERNMENT NOMINEES</h3></div></div>'+partner_grid()
    sections.append(f'<section class="document-section section-{n}{dark}" id="section-{n}" aria-label="{labels[n]}"><div class="section-content">{body}<span class="page-number" aria-label="Source page {n}">{n:02}</span></div></section>')

socials=[
 'https://www.facebook.com/profile.php?id=61573836564495',
 'https://www.facebook.com/businessmediacontact',
 'https://www.instagram.com/israelgeorgiabusinesshouse?igsh=a2cwcWd2YWY1NzNq',
 'https://youtube.com/@israel-georgiabusinesshouse?si=rXXIOcctUErjqmHk',
 'https://youtube.com/@businessmediacontactbmc7794?si=PYqPe9VWsC_B7KUt',
 'https://www.facebook.com/share/19vDyFiJbq/'
]
social_labels=[
 'Israel-Georgia Business House Facebook',
 'Business Media Contact Facebook',
 'Israel-Georgia Business House Instagram',
 'Israel-Georgia Business House Youtube',
 'Business Media Contact',
 'BGC International Facebook'
]
social_icons=['f','f','◎','▶','▶','f']
social_html=''.join('<li><a class="social-button" href="'+escape(url,quote=True)+'" target="_blank" rel="noopener noreferrer"><span class="social-icon" aria-hidden="true">'+icon+'</span><span class="social-title">'+escape(label)+'</span><span class="social-arrow" aria-hidden="true">↗</span></a></li>' for url,label,icon in zip(socials,social_labels,social_icons))
contact='<section class="document-section contact-section" id="contact" aria-label="Contacts and registration"><div class="section-content"><div class="contact-grid"><div><ul class="social-links">'+social_html+'</ul><div class="contact-box"><a href="https://wa.me/995511112441" target="_blank" rel="noopener noreferrer">WHATSAPP +995511112441</a><a href="mailto:israelgeorgiabusinesshouse@gmail.com">ISRAELGEORGIABUSINESSHOUSE@GMAIL.COM</a></div>'+logos()+'</div><div>'+photo('contact-conference')+'<div class="registration-label"><p>Israel-Georgia Business Forum<br>Registration Form for Foreign<br>Partners &amp; Guests&nbsp; 2</p></div><h2 class="registration-heading">ISRAEL-GEORGIA<br>BUSINESS FORUM REGISTRATION</h2></div></div><span class="page-number" aria-label="Source page 15">15</span></div></section>'

registration_url='https://docs.google.com/forms/d/1Qq1ImnOtpxSEg5opsbDKPuPpdpTFv3wMbR0NnLVHbfA/viewform?edit_requested=true'
video_section='''<section class="video-section" id="forum-video" aria-labelledby="video-title"><div class="video-inner"><div class="video-heading"><div><p class="video-eyebrow">VIDEO · 03:10</p><h2 id="video-title">BGC International</h2></div><span class="video-caption">Business Government Contact</span></div><video class="forum-video" controls playsinline preload="metadata" poster="assets/video-poster.jpg" width="848" height="478" aria-label="BGC International video"><source src="assets/forum-video.mp4" type="video/mp4">Your browser does not support embedded video. <a href="assets/forum-video.mp4">Open the video</a>.</video></div></section>'''
contact=video_section+contact
contact=contact.replace('<div class="registration-label"><p>Israel-Georgia Business Forum<br>Registration Form for Foreign<br>Partners &amp; Guests&nbsp; 2</p></div>','')
contact=contact.replace('<span class="page-number" aria-label="Source page 15">','<div class="registration-action"><a class="registration-button" href="'+escape(registration_url,quote=True)+'" target="_blank" rel="noopener noreferrer">Registration <span aria-hidden="true">↗</span></a></div><span class="page-number" aria-label="Source page 15">')

html='''<!doctype html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <meta name="description" content="Israel–Georgia Real Estate and Business Tourism Forum. Full programme, projects, organizers and contacts.">
 <meta name="theme-color" content="#063772">
 <title>Israel–Georgia Business Forum</title>
 <link rel="icon" href="favicon.svg" type="image/svg+xml">
 <link rel="stylesheet" href="styles.css?v=partners-2">
 <script src="script.js" defer></script>
</head>
<body>
 <a href="#main" class="skip-link">Skip to content</a>
 <header class="site-header">
  <a class="wordmark" href="#home" aria-label="BGC International home">BGC<span>INTERNATIONAL</span></a>
  <nav class="site-nav" id="site-nav" aria-label="Main navigation"><a href="#section-2">Forum</a><a href="#section-4">Programme</a><a href="#section-14">Nominees</a><a href="#contact">Contacts</a></nav>
  <a class="header-contact" href="https://wa.me/995511112441" target="_blank" rel="noopener noreferrer">WhatsApp <span aria-hidden="true">↗</span></a>
  <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span></button>
 </header>
 <main id="main">
  <section class="cover" id="home" lang="en" dir="ltr" aria-label="Forum introduction">
   <div class="cover-architecture">'''+photo('cover-georgia',eager=True)+photo('cover-city',eager=True)+'''</div>
   <div class="cover-geometry" aria-hidden="true"></div>
   <div class="cover-content">
    <div class="cover-top"><p>BUSINESS GOVERNMENT CONTACT</p><h1>BGC INTERNATIONAL – AWARD CEREMONY OF THE SACCESSFUL PROJECTS</h1></div>
    '''+logos()+'''
    <h2>ISRAEL GEORGIA REAL ISTATE<br>END BUSINESS TOURIZM FORUM</h2>
   </div>
  </section>
'''+ '\n'.join(sections)+contact+'''
 </main>
 <footer><span>ISRAEL–GEORGIA BUSINESS FORUM</span><a href="#home">Back to top ↑</a></footer>
</body>
</html>
'''
language_switch='<nav class="language-switch" aria-label="'+{'en':'Site language','ru':'Язык сайта','he':'שפת האתר'}[language]+'">'+''.join('<a class="language-link" href="'+file+'" lang="'+code+'" hreflang="'+code+'"'+(' aria-current="page"' if language==code else '')+'>'+label+'</a>' for code,file,label in [('en','index.html','English'),('ru','ru.html','Русский'),('he','he.html','עברית')])+'</nav>'
import re
html=re.sub(r'  <nav class="site-nav".*?</nav>\n','',html)
html=re.sub(r'  <button class="menu-toggle".*?</button>',language_switch,html)
header_registration='<a class="header-registration" href="'+escape(registration_url,quote=True)+'" target="_blank" rel="noopener noreferrer">Registration <span aria-hidden="true">↗</span></a>'
html=html.replace(language_switch,header_registration+language_switch)
html=html.replace(' <link rel="icon"',' <link rel="alternate" hreflang="en" href="index.html">\n <link rel="alternate" hreflang="ru" href="ru.html">\n <link rel="alternate" hreflang="he" href="he.html">\n <link rel="icon"')
# Preserve the same English banner across all three language versions.
english_cover=re.search(r'<section class="cover".*?</section>',html,re.S).group(0)
if language=='ru':
    translations={
        '<html lang="en">':'<html lang="ru">',
        '<title>Israel–Georgia Business Forum</title>':'<title>Израильско-грузинский бизнес-форум</title>',
        'Israel–Georgia Real Estate and Business Tourism Forum. Full programme, projects, organizers and contacts.':'Израильско-грузинский форум недвижимости и делового туризма. Программа, проекты, организаторы и контакты.',
        '>Skip to content<':'>Перейти к содержанию<',
        '>Forum<':'>О форуме<', '>Programme<':'>Программа<', '>Nominees<':'>Номинанты<', '>Contacts<':'>Контакты<',
        'aria-label="Open menu"':'aria-label="Открыть меню"',
        'aria-label="Main navigation"':'aria-label="Основная навигация"',
        'aria-label="BGC International home"':'aria-label="BGC International — главная"',
        'aria-label="Forum introduction"':'aria-label="О бизнес-форуме"',
        'BGC INTERNATIONAL – AWARD CEREMONY OF THE SACCESSFUL PROJECTS':'BGC INTERNATIONAL — ЦЕРЕМОНИЯ НАГРАЖДЕНИЯ УСПЕШНЫХ ПРОЕКТОВ',
        'ISRAEL GEORGIA REAL ISTATE<br>END BUSINESS TOURIZM FORUM':'ИЗРАИЛЬСКО-ГРУЗИНСКИЙ ФОРУМ<br>НЕДВИЖИМОСТИ И ДЕЛОВОГО ТУРИЗМА',
        'THE FORUM WILL BRING TOGETHER FUTURE PARTNERS!':'ФОРУМ ОБЪЕДИНИТ БУДУЩИХ ПАРТНЕРОВ!',
        'The forum will be covered by Georgian and Israeli media':'осветит Израильская и Грузинская Медиа',
        'ISRAEL-GEORGIA REAL ESTATE AND<br> BUSINESS TOURISM FORUM':'ИЗРАИЛЬСКО-ГРУЗИНСКИЙ ФОРУМ<br> НЕДВИЖИМОСТИ И ДЕЛОВОГО ТУРИЗМА',
        'BUSINESS AND GOVERNMENT NOMINEES':'НОМИНАНТЫ ОТ БИЗНЕСА И ГОСУДАРСТВА',
        'ISRAEL-GEORGIA<br>BUSINESS FORUM REGISTRATION':'РЕГИСТРАЦИЯ НА<br>ИЗРАИЛЬСКО-ГРУЗИНСКИЙ БИЗНЕС-ФОРУМ',
        '>Registration <':'>Регистрация <',
        'VIDEO · 03:10':'ВИДЕО · 03:10',
        'aria-label="BGC International video"':'aria-label="Видео BGC International"',
        'Your browser does not support embedded video.':'Ваш браузер не поддерживает встроенное видео.',
        '>Open the video<':'>Открыть видео<',
        'aria-label="Contacts and registration"':'aria-label="Контакты и регистрация"',
        '>Back to top ↑<':'>Наверх ↑<',
        '>ISRAEL–GEORGIA BUSINESS FORUM<':'>ИЗРАИЛЬСКО-ГРУЗИНСКИЙ БИЗНЕС-ФОРУМ<',
        'aria-label="Source page ':'aria-label="Страница источника ',
    }
    ru_sections=['Форум и организаторы','Гала-ужин и участники','Анализ рынка','Проекты и панельные дискуссии','Деловые встречи и презентации','Инвестиционные стратегии','Банки и юридическое сопровождение','Регистрация и участие','Гостиницы и государственные проекты','Страхование и консультации','Туризм','Приглашение и СМИ','Номинанты и будущие партнёры']
    for en,ru in zip(labels.values(),ru_sections):
        translations['aria-label="'+en+'"']='aria-label="'+ru+'"'
    for before,after in translations.items():
        html=html.replace(before,after)
    # Brand names and platform names on social buttons remain proper names.
    html=html.replace('>Israel-Georgia Business House Facebook<','>Israel-Georgia Business House — Facebook<').replace('>Business Media Contact Facebook<','>Business Media Contact — Facebook<').replace('>Israel-Georgia Business House Instagram<','>Israel-Georgia Business House — Instagram<').replace('>Israel-Georgia Business House Youtube<','>Israel-Georgia Business House — YouTube<').replace('>BGC International Facebook<','>BGC International — Facebook<')
if language=='he':
    translations={
        '<html lang="en">':'<html lang="he" dir="rtl">',
        '<title>Israel–Georgia Business Forum</title>':'<title>פורום העסקים ישראל–גאורגיה</title>',
        'Israel–Georgia Real Estate and Business Tourism Forum. Full programme, projects, organizers and contacts.':'פורום הנדל״ן ותיירות העסקים ישראל–גאורגיה. התוכנית המלאה, פרויקטים, מארגנים ופרטי קשר.',
        '>Skip to content<':'>דלגו לתוכן<',
        'aria-label="BGC International home"':'aria-label="BGC International — דף הבית"',
        'aria-label="Forum introduction"':'aria-label="על הפורום העסקי"',
        'BGC INTERNATIONAL – AWARD CEREMONY OF THE SACCESSFUL PROJECTS':'BGC INTERNATIONAL — טקס הענקת פרסים לפרויקטים מצליחים',
        'ISRAEL GEORGIA REAL ISTATE<br>END BUSINESS TOURIZM FORUM':'פורום הנדל״ן ותיירות העסקים<br>ישראל–גאורגיה',
        'THE FORUM WILL BRING TOGETHER FUTURE PARTNERS!':'הפורום יפגיש שותפים עתידיים!',
        'The forum will be covered by Georgian and Israeli media':'יסוקר על ידי התקשורת הישראלית והגאורגית',
        'ISRAEL-GEORGIA REAL ESTATE AND<br> BUSINESS TOURISM FORUM':'פורום הנדל״ן ותיירות העסקים<br> ישראל–גאורגיה',
        'BUSINESS AND GOVERNMENT NOMINEES':'מועמדים מטעם העסקים והממשלה',
        'ISRAEL-GEORGIA<br>BUSINESS FORUM REGISTRATION':'הרשמה לפורום העסקים<br>ישראל–גאורגיה',
        '>Registration <':'>הרשמה <',
        'VIDEO · 03:10':'וידאו · 03:10',
        'aria-label="BGC International video"':'aria-label="סרטון BGC International"',
        'Your browser does not support embedded video.':'הדפדפן שלכם אינו תומך בהפעלת וידאו מוטמע.',
        '>Open the video<':'>פתיחת הסרטון<',
        'aria-label="Contacts and registration"':'aria-label="יצירת קשר והרשמה"',
        '>Back to top ↑<':'>חזרה למעלה ↑<',
        '>ISRAEL–GEORGIA BUSINESS FORUM<':'>פורום העסקים ישראל–גאורגיה<',
        'aria-label="Source page ':'aria-label="עמוד מקור ',
    }
    he_sections=['הפורום והמארגנים','ארוחת הגאלה והמשתתפים','ניתוח השוק','פרויקטים ודיוני פאנל','מפגשים עסקיים ומצגות','אסטרטגיות השקעה','בנקים וסיוע משפטי','ליווי ברישום והשתתפות','מלונות ופרויקטים ממשלתיים','ביטוח וייעוץ','תיירות','הזמנה ותקשורת','מועמדים ושותפים עתידיים']
    for en,he in zip(labels.values(),he_sections):
        translations['aria-label="'+en+'"']='aria-label="'+he+'"'
    for before,after in translations.items():
        html=html.replace(before,after)
    # Keep brand names, telephone numbers and media controls in their own LTR flow.
    html=html.replace('class="social-title"','class="social-title" dir="ltr"').replace('class="wordmark"','class="wordmark" dir="ltr"').replace('class="contact-box"','class="contact-box" dir="ltr"').replace('class="forum-video"','class="forum-video" dir="ltr"')
html=re.sub(r'<section class="cover".*?</section>',lambda match: english_cover,html,flags=re.S)
(root/({'en':'index.html','ru':'ru.html','he':'he.html'}[language])).write_text(html,encoding='utf-8')
print('Built semantic HTML with all 25 numbered source points, 15 source sections and individual photographs.')
