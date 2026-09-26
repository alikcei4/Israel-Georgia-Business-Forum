from pathlib import Path
from PIL import Image
from pypdf import PdfReader
import json

root=Path(__file__).parent
output=root/'assets'/'photos'
output.mkdir(exist_ok=True)
source=PdfReader(r'C:/Users/alikc/OneDrive/Desktop/ENG_202026_20-_20corrected.pdf')
# Coordinates measured on the 1440 × 810 page previews. Only individual
# photographs and graphic assets are cropped; paragraph text is authored in HTML.
crops={
1:[('cover-georgia',(0,295,225,805),'Georgian modern architecture'),('cover-city',(1210,2,1438,502),'City skyline')],
2:[('wine-estate',(57,274,446,525),'Georgian wine estate and vineyards'),('residences',(470,274,913,528),'Residential development at sunset'),('forest-residences',(936,271,1382,522),'Residential buildings surrounded by forest')],
3:[('award-1',(49,284,350,506),'Award recipients at the ceremony'),('award-2',(398,284,726,504),'Presentation of an award'),('award-3',(763,284,998,590),'Guests at the award ceremony'),('award-4',(1054,29,1360,282),'Forum guests with an award'),('award-5',(1054,307,1360,593),'Guests at the gala dinner'),('award-6',(50,557,349,753),'Award recipient on stage'),('award-7',(399,560,725,752),'Gala dinner audience')],
4:[('panel-1',(58,288,451,556),'Real estate forum panel'),('panel-2',(485,286,996,632),'Speakers and conference audience'),('panel-3',(1033,288,1394,529),'Speaker presenting to an audience')],
5:[('discussion-1',(652,69,1008,306),'Panel speakers at a business forum'),('discussion-2',(1044,70,1404,306),'Presentation on a conference stage'),('discussion-3',(48,453,493,727),'Real estate panel discussion'),('discussion-4',(530,453,926,727),'Panel conversation'),('discussion-5',(959,453,1402,723),'Business forum participants')],
6:[('meeting-1',(655,22,960,431),'Roundtable business meeting'),('meeting-2',(988,169,1375,427),'Company presentation and group discussion'),('meeting-3',(44,353,483,598),'Industry panel on stage'),('meeting-4',(987,467,1387,732),'Informal business networking')],
7:[('investment-1',(111,242,564,473),'Agreement signing at Tbilisi Silk Road Forum'),('investment-2',(639,247,1032,476),'Waterfront development rendering'),('investment-3',(1107,35,1357,514),'Gonio Yachts and Marina architectural model'),('investment-4',(109,562,562,771),'Aerial view of waterfront buildings and marina')],
8:[('bank-1',(54,281,352,502),'Representatives at an agreement signing'),('bank-2',(385,282,707,502),'Digital construction forum'),('bank-3',(745,155,1043,452),'Business consultation'),('bank-4',(748,481,1040,701),'Signing business documents'),('bank-5',(1076,53,1379,278),'Banking panel discussion'),('bank-6',(1076,292,1379,749),'Bank partnership announcement')],
9:[('support-1',(108,176,484,425),'Professional consultation'),('support-2',(508,176,912,425),'Resort hotel and swimming pool'),('support-3',(965,175,1349,430),'Property consultation and key handover'),('support-4',(110,506,488,761),'Business and property advice')],
10:[('hotel-1',(535,33,959,308),'International hotel development'),('hotel-2',(979,33,1411,307),'Business workshop'),('hotel-3',(31,446,503,770),'Hotel atrium and reception'),('hotel-4',(541,354,958,770),'Real estate exhibition participants')],
11:[('insurance-1',(616,22,1019,303),'Insurance industry representative'),('insurance-2',(1054,22,1415,601),'Financing agreement signing'),('insurance-3',(30,224,592,599),'Industry panel discussion'),('insurance-4',(619,333,1016,601),'Forum presentation and audience')],
12:[('tourism-1',(29,64,469,355),'Georgian wine cellar'),('tourism-2',(507,65,831,355),'Medical tourism treatment'),('tourism-3',(836,64,1397,355),'Gala venue'),('tourism-4',(881,380,1373,770),'Batumi waterfront development')],
13:[('project-1',(74,253,702,598),'Landscaped hotel beside a lake'),('project-2',(744,251,1368,597),'Contemporary towers and gardens')],
14:[('organizer-house',(97,106,194,190),'Israel–Georgia Business House logo'),('organizer-media',(227,109,328,189),'Business Media Contact logo'),('nominee-logos',(88,281,1011,681),'Business and government nominee logos'),('media-logos',(1045,290,1170,755),'Media organization logos'),('media-logos-bottom',(96,718,1093,801),'International media logos'),('flags',(1180,96,1360,806),'Israeli and Georgian flags')],
15:[('contact-conference',(791,66,1355,391),'Forum audience in a conference hall')]
}
manifest={}
for page,items in crops.items():
    original=source.pages[page-1].images[0].image.convert('RGB')
    scale=original.width/1440
    manifest[str(page)]=[]
    for name,box,alt in items:
        im=original.crop(tuple(round(v*scale) for v in box))
        im.thumbnail((1600,1600),Image.Resampling.LANCZOS)
        im.save(output/f'{name}.jpg',quality=92,optimize=True)
        manifest[str(page)].append({'name':name,'alt':alt,'width':im.width,'height':im.height})
    print(f'Extracted photographs from page {page}',flush=True)
(root/'photo-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
