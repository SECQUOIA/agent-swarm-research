#!/usr/bin/env python3
"""Record PDF text bounds and create page contact sheets for visual inspection.

This checks gross layout conditions, not mathematical correctness or accessibility.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--pdf',default='build/main.pdf');a.add_argument('--output',default='build/pdf-review');args=a.parse_args()
pdf=p/args.pdf;out=p/args.output;out.mkdir(parents=True,exist_ok=True)
subprocess.run(['pdftotext','-bbox',str(pdf),str(out/'bounds.html')],check=True)
raw=(out/'bounds.html').read_text()
controls={hex(ord(c)):raw.count(c) for c in set(raw) if ord(c)<32 and c not in '\n\r\t'}
clean=''.join(c for c in raw if ord(c)>=32 or c in '\n\r\t')
root=ET.fromstring(clean);ns={'x':'http://www.w3.org/1999/xhtml'}
pages=[]
for i,page in enumerate(root.findall('.//x:page',ns),1):
 words=page.findall('x:word',ns);w=float(page.attrib['width']);h=float(page.attrib['height'])
 boxes=[tuple(float(x.attrib[k]) for k in ('xMin','yMin','xMax','yMax')) for x in words]
 outside=[{'text':x.text,'box':b} for x,b in zip(words,boxes) if b[0]<0 or b[1]<0 or b[2]>w or b[3]>h]
 margin=[{'text':x.text,'box':b} for x,b in zip(words,boxes) if b[0]<30 or b[2]>w-30]
 pages.append(dict(page=i,words=len(words),bounds=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)] if boxes else None,outside_page=outside,near_horizontal_edge=margin))
subprocess.run(['pdftoppm','-scale-to','640','-png',str(pdf),str(out/'page')],check=True)
images=sorted(out.glob('page-*.png'),key=lambda x:int(x.stem.split('-')[-1]))
sheets=[]
for start in range(0,len(images),12):
 sheet=Image.new('RGB',(4*400,3*548),'#d5d5d5');draw=ImageDraw.Draw(sheet)
 for j,f in enumerate(images[start:start+12]):
  im=Image.open(f).convert('RGB');im.thumbnail((396,516));x=(j%4)*400+(400-im.width)//2;y=(j//4)*548+24;sheet.paste(im,(x,y));draw.text(((j%4)*400+8,(j//4)*548+6),f'Page {start+j+1}',fill='black')
 name=out/f'contact-{start//12+1:02}.png';sheet.save(name);sheets.append(str(name.relative_to(p)))
report=dict(pdf=str(pdf.relative_to(p)),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),python=sys.version,extracted_xml_controls_removed=controls,pages=len(pages),blank_text_pages=[x['page'] for x in pages if not x['words']],outside_page_count=sum(len(x['outside_page']) for x in pages),near_horizontal_edge_count=sum(len(x['near_horizontal_edge']) for x in pages),contact_sheets=sheets,page_data=pages,limitation='Bounding boxes detect gross overflow; contact sheets require separate visual inspection. This does not verify proofs. Invalid XML control characters emitted by pdftotext are counted and removed for parsing only; the PDF is untouched.')
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='page_data'},indent=2))
