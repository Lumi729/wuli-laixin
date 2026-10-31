"""Production crops of independently drawn modular asset sheets (never the UI reference)."""
from pathlib import Path
from PIL import Image
import shutil
R=Path(__file__).resolve().parents[1];S=R.parent/'generated_images';D=R/'assets/poetic-v3'
for k in ['starry','rabbit','rain','postal']:(D/k).mkdir(parents=True,exist_ok=True)
def save(src,key,name,box=None,trim=False,maxsize=(1100,1500),quality=87):
 im=Image.open(S/src).convert('RGBA')
 if box:im=im.crop(box)
 if trim:
  b=im.getchannel('A').point(lambda v:255 if v>12 else 0).getbbox()
  if b:im=im.crop(b)
 im.thumbnail(maxsize,Image.Resampling.LANCZOS);im.save(D/key/(name+'.webp'),quality=quality,method=4)
 return im
for key,src in {'starry':'exec-1bd18deb-dc25-4095-a8ae-4f0ac2e9276e.png','rabbit':'exec-bcaf0065-4da9-4923-b0c1-e101d1bca8b2.png','rain':'exec-1e7ae1ee-ac54-47ba-bb1b-7e82f63b9da9.png','postal':'exec-7e1c1744-bb14-47ee-bf8e-7b97bcc8777c.png'}.items():save(src,key,'surface',maxsize=(900,1200),quality=83)
save('exec-d90a5ca9-2502-46b7-a2d0-5bd740df7647.png','starry','hero')
save('exec-ee91de4e-9dfa-4cff-b44e-f8076c5fe8a5.png','starry','sea',trim=True)
save('exec-bb790f6b-4a02-4e92-a1e0-db6c202bf045.png','rain','rain-edges',maxsize=(900,1200))
for key,src,name in [('starry','accent','arc'),('rabbit','header','portrait-ring'),('rabbit','accent','bunny'),('rabbit','icon-1','margin-doodles'),('rain','header','umbrella'),('rain','footer','chime')]:shutil.copyfile(R/f'assets/poetic-v2/{key}/{src}.webp',D/key/(name+'.webp'))
src='exec-0429acc7-61a7-45a6-b794-61342a53d02e.png';im=Image.open(S/src);w,h=im.size
for n,box in [('paper-top',(0,0,w,290)),('paper-bottom',(0,292,w,538)),('composer',(0,540,w,h)),('paper-grain',(500,120,756,248))]:save(src,'rabbit',n,box,trim=n!='paper-grain')
src='exec-f904ba66-973c-4812-bfb5-7a8d5718130e.png';im=Image.open(S/src);w,h=im.size
for n,box in [('letter-top',(0,0,w,325)),('letter-bottom',(0,327,w,535)),('composer',(0,538,w,h)),('paper-grain',(1000,120,1256,248))]:save(src,'postal',n,box,trim=n!='paper-grain')
# A separately drawn white torn-paper name slip; no preview content involved.
shutil.copyfile(D/'rabbit/composer.webp',D/'rain/name-paper.webp')
