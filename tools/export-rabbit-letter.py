from pathlib import Path
from PIL import Image
from io import BytesIO
R=Path(__file__).resolve().parents[1];D=R/'assets/rabbit-letter';G=R.parent/'generated_images';D.mkdir(exist_ok=True)
def save(im,name,size):
 im.thumbnail(size,Image.Resampling.LANCZOS);b=BytesIO();im.save(b,'WEBP',quality=92,method=6);(D/name).write_bytes(b.getvalue());Image.open(D/name).load()
save(Image.open(G/'exec-034ac339-026d-42d6-bd28-7136ab82ac3c.png'),'portrait.webp',(700,875))
save(Image.open(G/'exec-7b8151e0-ff10-49bc-93f7-7e95a69376da.png'),'footer.webp',(1100,400))
im=Image.open(G/'exec-6c9051f4-4212-4b79-80f8-b00ade283b6c.png')
for name,t,b in [('name',0,.37),('actions',.37,.70),('composer',.70,1)]:
 tile=im.crop((0,round(im.height*t),im.width,round(im.height*b)));save(tile,name+'.webp',(1000,400))
im=Image.open(G/'exec-d84ef1e2-a306-450a-a20a-90258b0d3bb9.png')
boxes=[(55,75,320,350),(350,110,620,340),(650,65,945,350),(975,65,1245,350),(55,390,330,655),(350,390,620,665),(670,480,930,590),(995,405,1230,650),(45,700,325,925),(370,675,620,930),(650,675,935,930),(975,675,1235,930),(65,995,310,1215),(365,945,625,1220),(640,930,965,1240),(1000,970,1235,1220)]
for i,box in enumerate(boxes):
 t=im.crop(box);t.thumbnail((125,125),Image.Resampling.LANCZOS);c=Image.new('RGBA',(144,144));c.alpha_composite(t,((144-t.width)//2,(144-t.height)//2));save(c,f'icon-{i}.webp',(144,144))
im=Image.open(G/'exec-d7f7a5b9-384f-4bb5-a88f-c6ad6cbff147.png');im=im.crop(im.getchannel('A').getbbox());save(im,'edge.webp',(160,1100))
