from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,base64,json
R=Path(__file__).resolve().parents[1];D=R/'assets/ink-continuous-v4';D.mkdir(exist_ok=True)
im=Image.open(R/'assets/ink-v1/ink-atlas.webp').convert('RGB')
def save(c,n):
 a=255-np.asarray(c.convert('L'));v=np.zeros((*a.shape,4),dtype=np.uint8);v[:,:,3]=a;o=Image.fromarray(v);o.save(D/(n+'.webp'),lossless=True);b=base64.b64encode((D/(n+'.webp')).read_bytes()).decode();w,h=o.size;(D/(n+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><image width="{w}" height="{h}" href="data:image/webp;base64,{b}"/></svg>')
# Entire header retained at one uniform scale, including full side pendants.
c=im.crop((0,136,1024,1090));d=ImageDraw.Draw(c)
d.polygon([(100,682),(240,682),(240,700),(784,700),(784,682),(924,682),(924,954),(100,954)],fill='white');save(c,'header')
# Separate the action ornament from the neighbouring hanging name pendants.
c=im.crop((100,818,924,1024));d=ImageDraw.Draw(c);d.rectangle((140,0,684,18),fill='white')
from scipy.ndimage import label,find_objects
a=np.array(c);labels,n=label(a[:,:,0]<230)
for k,sl in enumerate(find_objects(labels),1):
 if sl and sl[0].stop<25:a[labels==k]=255
c=Image.fromarray(a);save(c,'controls')
s=(R/'theme/ink-letter-aligned.css').read_text()
s+='''\n/* Continuous original artwork: one scale, no duplicated metadata/name overlays. */
#chat .mes {padding-top:calc(100cqw * 142 / 1024)!important;padding-inline:calc(100cqw * 100 / 1024)!important; background-position:2.64% 0,97.36% 0,3.71% 0,96.29% 0!important;}
#chat .mes::before {top:0;height:calc(100cqw * 954 / 1024);aspect-ratio:auto;background:url('../assets/ink-continuous-v4/header.svg') center top/100% auto no-repeat;}
#chat .mes + .mes::before {top:-24px;height:calc(100cqw * 954 / 1024 + 24px);background-image:url('../assets/ink-continuous-v4/header.svg'),url('../assets/ink-aligned-v2/v11-message-divider.svg');background-position:center 24px,center top;background-size:100% auto,auto 22px;}
#chat .mes > .mesAvatarWrapper {grid-template-rows:auto calc(100cqw * 68 / 1024);}
#chat .mes > .mesAvatarWrapper > .avatar {aspect-ratio:824/396;}
#chat .mes > .mesAvatarWrapper::after,#chat .mes > .mes_block::before,#chat .mes > .mes_block::after {content:none;}
#chat .mes .ch_name {background:none;width:100%;margin:0!important;container-type:normal;}
#chat .mes .ch_name > .flex1 {height:calc(100cqw * 88 / 1024);min-height:0;width:38%;flex:none!important;}
#chat .mes .name_text {font-size:clamp(12px,3.6vw,18px);}
#chat .mes .mes_buttons {--wl-controls-width:min(280px,calc(100cqw * .78));max-width:100%;min-height:calc(var(--wl-controls-width) * .25);padding:calc(var(--wl-controls-width) * .091) calc(var(--wl-controls-width) * .18) calc(var(--wl-controls-width) * .055);margin-top:2px!important;}
#chat .mes .mes_buttons::before {border-image-source:url('../assets/ink-continuous-v4/controls.svg');border-image-slice:75 200 45 200;border-width:calc(var(--wl-controls-width) * .091) calc(var(--wl-controls-width) * .243) calc(var(--wl-controls-width) * .055);border-image-width:calc(var(--wl-controls-width) * .091) calc(var(--wl-controls-width) * .243) calc(var(--wl-controls-width) * .055);}
'''
(R/'theme/ink-letter-continuous.css').write_text(s)
d=json.loads((R/'theme/Ink-Letter-Aligned.json').read_text());d['name']='墨羽来信·连续原图版';d['custom_css']=s.replace('../assets/ink-aligned-v2/','https://raw.githubusercontent.com/Lumi729/wuli-laixin/ink-aligned-v2/assets/ink-aligned-v2/').replace('../assets/ink-continuous-v4/','https://raw.githubusercontent.com/Lumi729/wuli-laixin/ink-continuous-v4/assets/ink-continuous-v4/');(R/'theme/Ink-Letter-Continuous.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
