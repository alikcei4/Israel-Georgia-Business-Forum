"""Build the English version of the separate Georgia landing page."""
from pathlib import Path
import json
import re
from lxml import html, etree

ROOT = Path(__file__).parent

def build_english(source):
    doc = html.fromstring(source)
    doc.set('lang', 'en')
    data = json.loads((ROOT / 'content-geo-en.json').read_text(encoding='utf-8'))
    headings = {2:'Business and Government Nominees',3:'Forum and Organizers',4:'Forum Objectives',5:'Forum Participants',6:'Forum Programme',7:'Awards Ceremony',8:'Project Selection Criteria',9:'Project Selection Criteria',10:'Media Partners'}
    for number, heading in headings.items():
        doc.get_element_by_id(f'geo-heading-{number}').text = heading
    for number, content in data.items():
        section = doc.get_element_by_id(f'geo-section-{number}')
        paragraphs = section.xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," copy ")]/p')
        texts = ([content['intro']] if content['intro'] else []) if isinstance(content,dict) else content
        assert len(paragraphs) == len(texts), number
        for node, text in zip(paragraphs,texts):
            node.text = text
        if isinstance(content,dict):
            criteria = section.xpath('.//ol/li/p')
            assert len(criteria) == len(content['criteria']), number
            for node,text in zip(criteria,content['criteria']):
                node.text = text
            section.xpath('.//h3[@class="geo-criteria-title"]')[0].text = 'Selection criteria for submitted projects:'
    translations = {
        'BGC International — საქართველო':'BGC International — Georgia',
        'შინაარსზე გადასვლა':'Skip to content',
        'BGC International — მთავარი':'BGC International — Home',
        'რეგისტრაცია':'Registration',
        'წარმატებული პროექტების დაჯილდოების ცერემონიალი':'AWARD CEREMONY FOR SUCCESSFUL PROJECTS',
        'ისრაელ-საქართველოს უძრავი ქონებისა და ბიზნეს ტურიზმის ფორუმი':'ISRAEL–GEORGIA REAL ESTATE AND BUSINESS TOURISM FORUM',
        '21 დეკემბერი, 2026':'December 21, 2026',
        'ვიდეო · 03:10':'VIDEO · 03:10',
        'BGC International ვიდეო':'BGC International video',
        'ვიდეოს გახსნა':'Open the video',
        'საკონტაქტო ინფორმაცია':'Contact Information',
        'ტელეფონი / WhatsApp / Telegram':'Phone / WhatsApp / Telegram',
        'ზემოთ ↑':'Back to top ↑',
        'Facebook — გვერდი':'Facebook — Page',
        'Facebook — პუბლიკაცია 1':'Facebook — Post 1',
        'Facebook — პუბლიკაცია 2':'Facebook — Post 2',
        'თანამედროვე არქიტექტურა საქართველოში':'Modern architecture in Georgia',
        'ქალაქის პანორამა':'City panorama',
    }
    for node in doc.iter():
        for field in ('text','tail'):
            value = getattr(node,field)
            if value:
                for before,after in translations.items():
                    value=value.replace(before,after)
                setattr(node,field,value)
        for attr in ('alt','aria-label'):
            value=node.get(attr)
            if value:
                for before,after in translations.items():
                    value=value.replace(before,after)
                if attr=='alt' and re.search('[\u10a0-\u10ff]',value):
                    value = 'Partner logo' if '/partners/' in node.get('src','') else 'Business forum, projects and award ceremony'
                node.set(attr,value)
    doc.xpath('//meta[@name="description"]')[0].set('content','Israel–Georgia Business Forum and BGC International. December 21, 2026, Pullman Tbilisi Axis Towers. Programme, nominees and contacts.')
    switch=doc.xpath('//nav[contains(@class,"language-switch")]')[0]
    switch.set('aria-label','Site language')
    for link in switch:
        link.attrib.pop('aria-current',None)
        if link.get('lang')=='en':
            link.set('aria-current','page')
    (ROOT/'index2-en.html').write_text('<!doctype html>\n'+etree.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')
