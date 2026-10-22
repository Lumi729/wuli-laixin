"""Package approved artwork into small theme assets; preserve Rose CSS layout."""
from pathlib import Path
from PIL import Image,ImageOps
import numpy as np,json,re,colorsys
R=Path(__file__).resolve().parents[1];D=R/'assets/ink-light-v1';D.mkdir(exist_ok=True)
img=Image.open(R/'assets/ink-v1/ink-atlas.webp').convert('RGB')
# Asset-sheet extraction only. Convert white paper into transparency for overlays.
rects={'v1/icon-book':(351,30,454,110),'v1/icon-cards':(912,30,979,111),'v1/icon-gift':(704,27,801,111),'v1/icon-landscape':(574,29,681,110),'v1/icon-letter':(251,29,328,112),'v1/icon-mask':(811,29,901,111),'v1/icon-moons':(139,29,226,108),'v1/icon-pendulum':(38,28,109,111),'v1/icon-quill':(251,29,328,112),'v3/icon-mirror':(475,25,552,111),'v1/moon-footer':(350,1280,676,1380),'v1/name-ribbon':(238,746,784,830),'v10/name-left':(0,690,100,1030),'v10/name-right':(924,690,1024,1030),'v11/message-divider':(232,1380,792,1435),'v4/bar-frame':(0,1432,1024,1530),'v5/counter-frame':(96,674,934,743),'v6/bottom-left':(0,1110,310,1380),'v6/bottom-right':(714,1110,1024,1380),'v7/portrait-surround':(0,136,1024,690),'v7/reasoning-ribbon':(238,746,784,830),'v9/controls-frame':(100,820,924,1024)}
source=(R/'theme/wuli-laixin.css').read_text();urls=sorted(set(re.findall(r"url\('../(assets/[^']+)'\)",source)));mapping={}
for u in urls:
 key=u.removeprefix('assets/').removesuffix('.webp');size=Image.open(R/u).size
 if key=='v1/paper':out=Image.new('RGBA',size,(255,255,255,255))
 else:
  crop=img.crop(rects[key]);v=np.asarray(crop.convert('L'));alpha=255-v
  rgba=np.zeros((*v.shape,4),dtype=np.uint8);rgba[:,:,3]=alpha
  tile=Image.fromarray(rgba);tile=ImageOps.contain(tile,size,Image.Resampling.LANCZOS)
  out=Image.new('RGBA',size);x=0 if key=='v10/name-left' else size[0]-tile.width if key=='v10/name-right' else (size[0]-tile.width)//2;out.alpha_composite(tile,(x,(size[1]-tile.height)//2))
 name=key.replace('/','-')+'.webp';out.save(D/name,lossless=True,method=6);mapping[u]='assets/ink-light-v1/'+name
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
(R/'theme/ink-letter-light.css').write_text(s)
d=json.loads((R/'theme/Rose-Moon-Phases.json').read_text());d['name']='墨羽来信·轻量版'
for k,v in d.items():
 if k.endswith('_color') and isinstance(v,str):d[k]=re.sub(r'rgba?\(([^)]+)\)',rgba,v)
base='https://raw.githubusercontent.com/Lumi729/wuli-laixin/ink-light-v1/'
d['custom_css']=s.replace('../assets/',base+'assets/')
(R/'theme/Ink-Letter-Light.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def normalized(css):
 css=re.sub(r'url\([^)]*\)','IMAGE',css);css=re.sub(r'#[0-9a-fA-F]{3,8}\b','COLOR',css);return re.sub(r'rgba?\([^)]*\)','COLOR',css)
assert normalized(s)==normalized(source)
old=json.loads((R/'theme/Rose-Moon-Phases.json').read_text())
assert all(d[k]==v for k,v in old.items() if k not in ('name','custom_css') and not k.endswith('_color'))
print(json.dumps({'json_bytes':(R/'theme/Ink-Letter-Light.json').stat().st_size,'asset_bytes':sum(p.stat().st_size for p in D.glob('*.webp')),'assets':len(mapping),'layout':'identical except image/color tokens','settings':'all non-color settings identical'}))
