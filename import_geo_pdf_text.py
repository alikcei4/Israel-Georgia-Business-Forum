"""Import the three approved PDFs as the Georgia page's text sources."""
from pathlib import Path
import json,re
import pdfplumber
ROOT=Path(__file__).parent
TITLE='Israel-Georgia Real Estate and Business Tourism Forum'
SOURCES={'ka':'GEO.pdf','en':'GEOEN.pdf','ru':'GEOru.pdf'}
MARKERS={
'ka':{3:['ასევე წლევანდელი','IGBH და BMC','წლევანდელ ფორუმზე'],4:['1. ქართული','აგრეთვე ფორუმის მიზანია'],5:['საქართველოს მხრიდან'],6:['ფორუმის ფორმატში იქნება']},
'en':{3:['This year’s','Each year,','Furthermore,'],4:['1. Promote','The forum also aims'],5:['Also invited'],6:['The forum will present']},
'ru':{3:['Организатором форума','IGBH и BMC ежегодно','Так же в этом году'],4:['1. Продвижение','Также форум направлен'],5:['Со стороны Грузии'],6:['В рамках форума будут']}}
CRITERIA={'ka':'წარდგენილი პროექტების შესარჩევი კრიტერიუმები:','en':'Selection criteria for submitted projects:','ru':'Критерии отбора представленных проектов:'}
MEDIA={'ka':'მედია პარტნიორები','en':'Media Partners','ru':'Медиа-партнёры'}
FIXES={'market.The':'market. The','firms.Participants':'firms. Participants','GlobalNetworking':'Global Networking',
'награжденияуспешных':'награждения успешных','IsraelGeorgia':'Israel Georgia','международныйбизнес':'международный бизнес','иповышением':'и повышением','содействуетгрузинским':'содействует грузинским','целевойаудиторией.Организатором':'целевой аудиторией. Организатором','нарынке':'на рынке','деловыхтуристических':'деловых туристических','связей.IGBH':'связей. IGBH','международныепартнёрские':'международные партнёрские','Грузии.Так':'Грузии. Так','идевелоперские':'и девелоперские','компании.Так':'компании. Так','брокерскиетуры':'брокерские туры','провестибизнес':'провести бизнес','такжепредставить':'также представить','пресс- релизов':'пресс-релизов','Israel -Georgia':'Israel-Georgia','სავაჭრო- ეკონომიკური':'სავაჭრო-ეკონომიკური'}
for lang,filename in SOURCES.items():
    with pdfplumber.open(ROOT/filename) as pdf:
        raw=[page.extract_text(x_tolerance=1) or '' for page in pdf.pages]
    assert len(raw)==11
    data={}
    for number in range(3,11):
        lines=raw[number-1].splitlines()
        # The repeated title occupies two lines on these source pages.
        assert 'ISRAEL' in lines[0].upper()
        text=re.sub(r'\s+',' ',' '.join(lines[2:]).replace('•','').replace('*','')).strip()
        for old,new in FIXES.items():text=text.replace(old,new)
        # Restore missing spacing without rephrasing the approved copy.
        text=re.sub(r'([,:])(?=[A-Za-zА-Яа-я])',r'\1 ',text)
        if number in (8,9):
            intro,items=text.split(CRITERIA[lang],1)
            data[str(number)]={'intro':intro.strip(),'criteria':[v.strip() for v in re.split(r'\b\d+\.\s*',items)[1:]]}
            assert len(data[str(number)]['criteria'])==(8 if number==8 else 6)
        elif number==10:
            assert text.startswith(MEDIA[lang])
            data[str(number)]=[text[len(MEDIA[lang]):].strip()]
        else:
            for marker in MARKERS[lang].get(number,[]):
                assert marker in text,(lang,number,marker)
                text=text.replace(marker,'\n'+marker,1)
            data[str(number)]=[v.strip() for v in text.split('\n')]
    if lang=='ka':
        slides=json.loads((ROOT/'content-geo.json').read_text(encoding='utf-8'))
        for number,content in data.items():
            if isinstance(content,dict):
                start=1 if number=='8' else 9
                paragraphs=([content['intro']] if content['intro'] else [])+[CRITERIA[lang]]+[f'{i}. {v}' for i,v in enumerate(content['criteria'],start)]
            else:paragraphs=([MEDIA[lang]] if number=='10' else [])+content
            slides[int(number)-1]=[TITLE]+paragraphs
        (ROOT/'content-geo.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),encoding='utf-8')
    else:
        (ROOT/f'content-geo-{lang}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Imported',filename)
