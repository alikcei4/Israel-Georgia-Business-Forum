from pathlib import Path
from html import escape
import json

root=Path(__file__).parent
content=json.loads((root/'content.json').read_text(encoding='utf-8'))
manifest=json.loads((root/'photo-manifest.json').read_text(encoding='utf-8'))
photos={item['name']:item for group in manifest.values() for item in group}

def photo(name, cls='', eager=False):
    p=photos[name]
    loading='fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<figure class="photo {cls}"><img src="assets/photos/{name}.jpg" alt="{escape(p["alt"])}" width="{p["width"]}" height="{p["height"]}" {loading}></figure>'

def gallery(page, start=0, end=None, cls=''):
    return '<div class="gallery '+cls+'">'+''.join(photo(p['name']) for p in manifest[str(page)][start:end])+'</div>'

def para(record,cls=''):
    return f'<div class="copy {cls}" id="point-{record["number"]}"><p><span class="point-number">{record["number"]}.</span> {escape(record["text"])}</p></div>'

def logos(cls=''):
    return f'<div class="organizer-logos {cls}">'+photo('organizer-house')+photo('organizer-media')+'</div>'

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
        body=para(ps[0],'navy centered')+'<div class="nominees-heading">'+logos()+'<div><h2>ISRAEL-GEORGIA REAL ESTATE AND<br> BUSINESS TOURISM FORUM</h2><h3>BUSINESS AND GOVERNMENT NOMINEES</h3></div></div><div class="nominees-layout">'+photo('nominee-logos')+photo('media-logos')+photo('flags')+'</div>'+photo('media-logos-bottom','media-bottom')
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
 <link rel="stylesheet" href="styles.css">
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
  <section class="cover" id="home" aria-label="Forum introduction">
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
(root/'index.html').write_text(html,encoding='utf-8')
print('Built semantic HTML with all 25 numbered source points, 15 source sections and individual photographs.')
