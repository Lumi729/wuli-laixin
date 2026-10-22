"""Package approved artwork into small theme assets; preserve Rose CSS layout."""
from pathlib import Path
from PIL import Image,ImageOps
import numpy as np,json,re,colorsys
R=Path(__file__).resolve().parents[1];D=R/'assets/ink-aligned-v2';D.mkdir(exist_ok=True)
img=Image.open(R/'assets/ink-v1/ink-atlas.webp').convert('RGB')
# Asset-sheet extraction only. Convert white paper into transparency for overlays.
rects={'v1/icon-book':(351,30,454,110),'v1/icon-cards':(912,30,979,111),'v1/icon-gift':(704,27,801,111),'v1/icon-landscape':(574,29,681,110),'v1/icon-letter':(251,29,328,112),'v1/icon-mask':(811,29,901,111),'v1/icon-moons':(139,29,226,108),'v1/icon-pendulum':(38,28,109,111),'v1/icon-quill':(251,29,328,112),'v3/icon-mirror':(475,25,552,111),'v1/moon-footer':(350,1280,676,1380),'v1/name-ribbon':(238,746,784,830),'v10/name-left':(0,690,100,1030),'v10/name-right':(924,690,1024,1030),'v11/message-divider':(232,1380,792,1435),'v4/bar-frame':(0,1432,1024,1530),'v5/counter-frame':(96,674,934,743),'v6/bottom-left':(0,1110,310,1380),'v6/bottom-right':(714,1110,1024,1380),'v7/portrait-surround':(0,136,1024,690),'v7/reasoning-ribbon':(238,746,784,830),'v9/controls-frame':(100,820,924,1024)}
source=(R/'theme/wuli-laixin.css').read_text();urls=sorted(set(re.findall(r"url\('../(assets/[^']+)'\)",source)));mapping={}
for u in urls:
 key=u.removeprefix('assets/').removesuffix('.webp');size=Image.open(R/u).size
 if key=='v1/paper':out=Image.new('RGBA',size,(255,255,255,255))
 else:
  # Reposition the approved atlas, using explicit source and destination anchors.
  def warp(xs,ys,tx,ty):
   result=Image.new('RGB',size,'white')
   for i in range(len(xs)-1):
    for j in range(len(ys)-1):
     part=img.crop((xs[i],ys[j],xs[i+1],ys[j+1]))
     result.paste(part.resize((tx[i+1]-tx[i],ty[j+1]-ty[j]),Image.Resampling.LANCZOS),(tx[i],ty[j]))
   return result
  w,h=size
  if key=='v7/portrait-surround':
   crop=warp([0,27,38,100,924,986,997,1024],[136,180,278,674,690],[0,24,35,65,876,906,917,941],[0,44,114,570,574])
  elif key=='v9/controls-frame':
   crop=warp([100,300,724,924],[820,878,988,1024],[0,240,760,1000],[32,86,251,301])
  elif key=='v5/counter-frame':
   crop=img.crop((20,680,1004,748)).resize(size,Image.Resampling.LANCZOS)
  elif key in ('v10/name-left','v10/name-right'):
   # Isolate the ivy/pendant band, excluding the separate action frame below it.
   box=(8,696,238,831) if key.endswith('left') else (786,696,1016,831)
   crop=Image.new('RGB',size,'white');crop.paste(img.crop(box).resize((284,137),Image.Resampling.LANCZOS),(0,0))
  elif key.startswith('v6/bottom-'):
   xs=[0,27,38,310] if key.endswith('left') else [714,986,997,1024]
   tx=[0,24,35,300] if key.endswith('left') else [0,265,276,300]
   crop=warp(xs,[1056,1346,1358,1380],tx,[0,290,302,324])
  elif key=='v1/moon-footer':
   crop=img.crop((350,1232,676,1380)).resize(size,Image.Resampling.LANCZOS)
  elif key=='v11/message-divider':
   crop=Image.new('RGB',size,'white');crop.paste(img.crop(rects[key]).resize((1000,98),Image.Resampling.LANCZOS),(100,134))
  else:
   crop=img.crop(rects[key]).resize(size,Image.Resampling.LANCZOS)
  v=np.asarray(crop.convert('L'));rgba=np.zeros((*v.shape,4),dtype=np.uint8);rgba[:,:,3]=255-v
  out=Image.fromarray(rgba)
 name=key.replace('/','-');out.save(D/(name+'.webp'),lossless=True,method=6)
 import base64
 encoded=base64.b64encode((D/(name+'.webp')).read_bytes()).decode()
 (D/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 {size[0]} {size[1]}"><image width="{size[0]}" height="{size[1]}" href="data:image/webp;base64,{encoded}"/></svg>')
 mapping[u]='assets/ink-aligned-v2/'+name+'.svg' 
# Replace only image references and color tokens. All layout declarations remain byte-identical.
def mono(m):
 token=m[0];h=token[1:];h=''.join(c*2 for c in h) if len(h) in (3,4) else h
 rgb=[int(h[i:i+2],16) for i in (0,2,4)];light=round((max(rgb)+min(rgb))/2)
 return '#'+f'{light:02x}'*3+(h[6:] if len(h)==8 else '')
def rgba(m):
 vals=[v.strip() for v in m[1].split(',')];light=round((max(map(float,vals[:3]))+min(map(float,vals[:3])))/2)
 return ('rgba' if len(vals)==4 else 'rgb')+'('+', '.join([str(light)]*3+vals[3:])+')'
s=source
for old,new in mapping.items():s=s.replace('../'+old,'../'+new)
s=re.sub(r'#[0-9a-fA-F]{3,8}\b',mono,s);s=re.sub(r'rgba?\(([^)]+)\)',rgba,s)
(R/'theme/ink-letter-aligned.css').write_text(s)
d=json.loads((R/'theme/Rose-Moon-Phases.json').read_text());d['name']='墨羽来信·原图对齐版'
for k,v in d.items():
 if k.endswith('_color') and isinstance(v,str):d[k]=re.sub(r'rgba?\(([^)]+)\)',rgba,v)
base='https://raw.githubusercontent.com/Lumi729/wuli-laixin/ink-aligned-v2/'
d['custom_css']=s.replace('../assets/',base+'assets/')
(R/'theme/Ink-Letter-Aligned.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def normalized(css):
 css=re.sub(r'url\([^)]*\)','IMAGE',css);css=re.sub(r'#[0-9a-fA-F]{3,8}\b','COLOR',css);return re.sub(r'rgba?\([^)]*\)','COLOR',css)
assert normalized(s)==normalized(source)
old=json.loads((R/'theme/Rose-Moon-Phases.json').read_text())
assert all(d[k]==v for k,v in old.items() if k not in ('name','custom_css') and not k.endswith('_color'))
print(json.dumps({'json_bytes':(R/'theme/Ink-Letter-Aligned.json').stat().st_size,'asset_bytes':sum(p.stat().st_size for p in D.glob('*.webp')),'assets':len(mapping),'layout':'identical except image/color tokens','settings':'all non-color settings identical'}))
