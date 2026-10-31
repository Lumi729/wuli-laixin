"""Export independent motifs from generated source atlases; no screenshot extraction."""
from PIL import Image
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R.parent/'generated_images'
C={
'starry':('exec-af0dd15b-df04-45ae-8512-8a8b85b593c5.png',[(0,630,326,960),(327,630,627,930),(0,960,350,1254),(350,930,627,1254)]),
'rabbit':('exec-db1e016a-3510-44ae-a616-d28087bb9b5d.png',[(0,660,295,905),(300,660,627,900),(0,905,300,1254),(310,900,627,1254)]),
'rain':('exec-89eaa491-68d3-4f28-a654-0f78d2784e5c.png',[(0,650,290,950),(295,650,627,950),(0,955,300,1254),(305,955,627,1254)]),
'postal':('exec-8d7d7660-e24a-4abb-8880-ef994950cf1b.png',[(0,665,310,945),(315,665,627,945),(0,950,310,1254),(315,950,627,1254)])}
for k,(f,boxes) in C.items():
 im=Image.open(S/f).convert('RGBA')
 for j,b in enumerate(boxes):
  a=im.crop(b);a=a.crop(a.getchannel('A').point(lambda x:255 if x>20 else 0).getbbox());a.thumbnail((180,180),Image.Resampling.LANCZOS);a.save(R/f'assets/poetic-v2/{k}/icon-{j+1}.webp',quality=90,method=4)
