from pathlib import Path
from PIL import Image
from io import BytesIO
R=Path(__file__).resolve().parents[1];S=R.parent/'generated_images';D=R/'assets/poetic-v3'
def out(im,key,name,trim=True,limit=(1100,1500)):
 im=im.convert('RGBA')
 if trim:
  b=im.getchannel('A').point(lambda x:255 if x>12 else 0).getbbox()
  if b:im=im.crop(b)
 im.thumbnail(limit,Image.Resampling.LANCZOS);b=BytesIO();im.save(b,format='WEBP',quality=88,method=4);p=D/key/(name+'.webp');p.write_bytes(b.getvalue());Image.open(p).load()
im=Image.open(S/'exec-8f4fa2df-1216-4f08-b3c6-cf0edc41b40b.png');w,h=im.size
for n,a,b in [('paper-top',0,.425),('paper-bottom',.435,.785)]:out(im.crop((0,int(a*h),w,int(b*h))),'rabbit',n)
out(im.crop((int(w*.3),int(h*.19),int(w*.45),int(h*.33))),'rabbit','paper-grain',False)
for k,f in [('rabbit','exec-5204d3f0-6c56-494a-a0c2-2b3463ca44d2.png'),('postal','exec-1e5cc84a-e713-48af-8178-6315e9a60daa.png')]:out(Image.open(S/f),k,'composer')
im=Image.open(S/'exec-bb790f6b-4a02-4e92-a1e0-db6c202bf045.png');w,h=im.size
out(im.crop((0,int(h*.67),w,h)),'rain','rain-bottom',False)
out(im.crop((0,0,int(w*.14),int(h*.64))),'rain','rain-left',False)
out(im.crop((int(w*.86),0,w,int(h*.64))),'rain','rain-right',False)
im=Image.open(S/'exec-8aced415-0212-4265-bc2c-29848761a52e.png');w,h=im.size
for n,a,b in [('letter-top',0,.475),('letter-bottom',.48,.785)]:out(im.crop((0,int(a*h),w,int(b*h))),'postal',n)
out(im.crop((int(w*.52),int(h*.19),int(w*.67),int(h*.33))),'postal','paper-grain',False)
