from PIL import Image, ImageDraw
from pathlib import Path
p=Path(__file__).parent/'render'
files=sorted(p.glob('page-*.jpg'))
for start in range(0,len(files),20):
    out=Image.new('RGB',(1500,2050),'#dddddd'); draw=ImageDraw.Draw(out)
    for j,f in enumerate(files[start:start+20]):
        im=Image.open(f); im.thumbnail((294,380))
        x=(j%5)*300; y=(j//5)*510
        out.paste(im,(x,y+25)); draw.text((x+5,y+5),str(start+j+1),fill='black')
    out.save(p/f'contact-{start+1:03}.jpg')
print(len(files),'pages')
