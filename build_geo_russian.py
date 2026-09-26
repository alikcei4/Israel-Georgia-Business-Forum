"""Translate the Georgia page into Russian while preserving its English banner."""
from pathlib import Path
import json
from lxml import html, etree

ROOT = Path(__file__).parent

def build_russian():
    doc = html.fromstring((ROOT/'index2-en.html').read_text(encoding='utf-8'))
    doc.set('lang','ru')
    data=json.loads((ROOT/'content-geo-ru.json').read_text(encoding='utf-8'))
    for number,content in data.items():
        section=doc.get_element_by_id('geo-section-'+number)
        paragraphs=section.xpath('.//div[contains(concat(" ",normalize-space(@class)," ")," copy ")]/p')
        texts=([content['intro']] if content['intro'] else []) if isinstance(content,dict) else content
        assert len(paragraphs)==len(texts),number
        for node,text in zip(paragraphs,texts):
            node.text=text
        if isinstance(content,dict):
            criteria=section.xpath('.//ol/li/p')
            assert len(criteria)==len(content['criteria']),number
            for node,text in zip(criteria,content['criteria']):
                node.text=text
    labels={
        'Business and Government Nominees':'Номинанты от бизнеса и государства',
        'Business and government nominees':'Номинанты от бизнеса и государства',
        'Forum and Organizers':'Форум и организаторы',
        'Forum Objectives':'Цели форума',
        'Forum Participants':'Участники форума',
        'Forum Programme':'Программа форума',
        'Awards Ceremony':'Церемония награждения',
        'Project Selection Criteria':'Критерии отбора проектов',
        'Selection criteria for submitted projects:':'Критерии отбора представленных проектов:',
        'Media Partners':'Медиапартнёры',
        'Contact Information':'Контактная информация',
        'BGC International — Georgia':'BGC International — Грузия',
        'Skip to content':'Перейти к содержанию',
        'BGC International — Home':'BGC International — Главная',
        'Registration':'Регистрация',
        'VIDEO · 03:10':'ВИДЕО · 03:10',
        'BGC International video':'Видео BGC International',
        'Open the video':'Открыть видео',
        'Phone / WhatsApp / Telegram':'Телефон / WhatsApp / Telegram',
        'Back to top ↑':'Наверх ↑',
        'Facebook — Page':'Facebook — Страница',
        'Facebook — Post 1':'Facebook — Публикация 1',
        'Facebook — Post 2':'Facebook — Публикация 2',
        'Partner logo':'Логотип партнёра',
        'Business forum, projects and award ceremony':'Бизнес-форум, проекты и церемония награждения',
        'Site language':'Язык сайта',
    }
    cover=doc.get_element_by_id('geo-home')
    for node in doc.iter():
        if node is cover or cover in node.iterancestors():
            continue
        for field in ('text','tail'):
            value=getattr(node,field)
            if value and value.strip() in labels:
                setattr(node,field,value.replace(value.strip(),labels[value.strip()]))
        for attr in ('alt','aria-label'):
            if node.get(attr) in labels:
                node.set(attr,labels[node.get(attr)])
    doc.xpath('//meta[@name="description"]')[0].set('content','Израильско-грузинский бизнес-форум и BGC International. 21 декабря 2026 года, Pullman Tbilisi Axis Towers. Программа, номинанты и контакты.')
    for link in doc.xpath('//nav[contains(@class,"language-switch")]/a'):
        link.attrib.pop('aria-current',None)
        if link.get('lang')=='ru':
            link.set('aria-current','page')
    (ROOT/'index2-ru.html').write_text('<!doctype html>\n'+etree.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')
