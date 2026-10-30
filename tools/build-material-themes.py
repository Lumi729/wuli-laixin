"""Build external-asset material variants, retaining the existing Rose layout."""
from pathlib import Path
from io import BytesIO
from PIL import Image
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/'
CONFIG={
'ocean':('贝母潮汐·彩铅','Ocean-Pencil','#745763','#bb909f','#fffafb','#f6faff'),
'rabbit':('月兔糖纸·蜡笔','Rabbit-Crayon','#675679','#b5a1ce','#fcfaff','#faf7ff'),
'rain':('雨后手札·毛玻璃','Rain-Frosted','#455f5a','#9cbeb1','#f8fcfa','#f1f8f5'),
'postal':('云端邮局','Cloud-Post',' #4c617d'.strip(),'#9db7d3','#fbfcff','#f3f8fe')}
NAMES=['corner-tl','corner-tr','corner-bl','corner-br','icon-pendulum','icon-moons','icon-quill','icon-book','name-ribbon','controls-frame','bar-frame','divider','icon-mirror','icon-landscape','icon-gift','icon-mask']
def save(im,path):
 b=BytesIO();im.save(b,format='WEBP',quality=90,method=6);path.write_bytes(b.getvalue())
def fit(im,w,h):
 im=im.copy();im.thumbnail((w,h),Image.Resampling.LANCZOS);return im
def put(canvas,im,xy):canvas.alpha_composite(im,xy)
def export(key,source):
 art=ROOT/'assets'/('material-'+key+'-v1');art.mkdir(parents=True,exist_ok=True)
 atlas=Image.open(source).convert('RGBA'); w,h=atlas.size;parts={}
 for i,n in enumerate(NAMES):
  box=(round(i%4*w/4),round(i//4*h/4),round((i%4+1)*w/4),round((i//4+1)*h/4))
  if key in ('ocean','rain'):
   bounds=[(0,.26),(.27,.53),(.55,.705),(.73,1)][i//4];box=(round(i%4*w/4),round(bounds[0]*h),round((i%4+1)*w/4),round(bounds[1]*h))
  if key=='postal':
   bounds=[(0,.30),(.335,.535),(.595,.715),(.75,1)][i//4];box=(round(i%4*w/4),round(bounds[0]*h),round((i%4+1)*w/4),round(bounds[1]*h))
  if key=='rabbit':
   boxes=[(0,0,.25,.27),(.25,0,.5,.27),(.5,0,.75,.27),(.75,0,1,.27), (0,.28,.25,.52),(.25,.28,.5,.52),(.5,.28,.75,.52),(.75,.28,1,.52), (0,.53,.33,.67),(.33,.53,.655,.67),(.655,.53,1,.67),(.25,.67,.75,.755), (0,.755,.25,1),(.25,.755,.5,1),(.5,.755,.75,1),(.75,.755,1,1)]
   b=boxes[i];box=tuple(round(v*(w if j%2==0 else h)) for j,v in enumerate(b))
  im=atlas.crop(box)
  box=im.getchannel('A').point(lambda x:255 if x>16 else 0).getbbox();assert box,n
  im=im.crop(box);parts[n]=im
  save(im,art/(n+'.webp'))
 # Assemble original generated pieces on a native-size transparent canvas, never stretch.
 portrait=Image.new('RGBA',(941,780))
 for n,size,x,y in [('corner-tl',235,25,72),('corner-tr',210,706,76),('corner-bl',155,33,433),('corner-br',155,753,433)]:
  im=fit(parts[n],size,size);put(portrait,im,(x,y))
 save(portrait,art/'portrait-surround.webp')
 for n,side in [('bottom-left','corner-bl'),('bottom-right','corner-br')]:
  canvas=Image.new('RGBA',(300,324));im=fit(parts[side],280,280);put(canvas,im,((300-im.width)//2,324-im.height));save(canvas,art/(n+'.webp'))
 canvas=Image.new('RGBA',(341,324));im=fit(parts['divider'],341,110);put(canvas,im,((341-im.width)//2,324-im.height));save(canvas,art/'bottom-center.webp')
 for target,src in [('icon-cards','icon-mask'),('icon-letter','icon-mask'),('body-sprig','icon-book')]:save(parts[src],art/(target+'.webp'))
 color=CONFIG[key][3]
 (art/'counter-mark.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="60" height="20" viewBox="0 0 60 20"><path d="M0 10h22m16 0h22M30 4l6 6-6 6-6-6z" fill="none" stroke="{color}" stroke-width="1.4"/></svg>')
 return art

def build(key,art):
 name,stem,ink,line,paper,tint=CONFIG[key];url=BASE+str(art.relative_to(ROOT))+'/'
 css=(ROOT/'theme/honeydew.css').read_text().replace(BASE+'assets/honeydew-v1/',url)
 for a,b in {'#3e493d':ink,'#879775':line,'#fbfdf8':paper,'#f7faf2':tint,'#c9d5b9':line,'#b0bf9e':line,'#7f966a':line,'#fbfdf7':paper,'#fcfdf9':paper,'#a3b392':line,'#9eae8f':line,'#becfa9':line,'#dce8ce':tint,'#bacbac':line,'#edf4e4':tint,'rgba(247,250,242,':'rgba(250,250,252,'}.items():css=css.replace(a,b)
 css=css.replace('蜜瓜花笺',name)
 nameim=Image.open(art/'name-ribbon.webp');nameheight=round(164*nameim.height/nameim.width)+8
 controlim=Image.open(art/'controls-frame.webp');controlratio=controlim.height/controlim.width
 css+=f'''\n/* {name}: independent illustrations, fixed natural proportions. */
#chat .mes > .mesAvatarWrapper > .avatar {{border:1px solid {line}!important;background:{tint};}}
#chat .mes .ch_name {{background-position:center top!important;background-size:164px auto!important;}}
#chat .mes .ch_name > .flex1 {{min-height:{nameheight}px;width:135px;}}
#chat .mes .ch_name .name_text {{transform:none!important;}}
#chat .mes .mes_text::after {{display:none;}}
#chat .mes .mes_text {{padding-top:24px!important;padding-bottom:28px!important;}}
#chat .mes .mes_buttons {{min-height:calc(var(--wl-controls-width) * {controlratio:.5f}); padding:20px 26px!important;}}
#chat .mes .mes_buttons::before {{background-size:contain!important;}}
#top-bar,#send_form {{background-color:{paper}!important;}}
#top-bar::after,#send_form::after {{border-image:none!important;border:1px solid {line}!important;border-radius:9px;inset:0!important;
 background:url('{url}corner-tl.webp') left top / 30px auto no-repeat,url('{url}corner-br.webp') right bottom / 30px auto no-repeat!important;}}
#chat .mes {{padding-bottom:85px!important;}}
#chat .mes::after {{height:calc(100cqw * 230 / 941);background-size:25% auto,25% auto,40% auto;}}
@media(min-width:600px) and (orientation:portrait) {{
 #chat .mes .ch_name {{background-size:calc(var(--c) * 164) auto!important;}}
 #chat .mes .ch_name > .flex1 {{min-height:calc(var(--c) * {nameheight});}}
 #chat .mes .mes_buttons {{min-height:calc(var(--wl-controls-width) * {controlratio:.5f});padding:calc(var(--c) * 20) calc(var(--c) * 26)!important;}}
 #chat .mes .mes_text {{padding-top:calc(var(--c) * 24)!important;}}
 #chat .mes {{padding-bottom:calc(var(--c) * 85)!important;}}
}}
'''
 if key=='rabbit':
  css+='\n#chat .mes .ch_name > .flex1{padding-left:18px;box-sizing:border-box;}\n'
 if key=='rain':
  css+='''\n/* Frosted glass only on two fixed UI surfaces; scrolling messages stay unfiltered. */
#top-bar,#send_form{background-color:rgba(248,253,250,.80)!important;backdrop-filter:blur(8px)!important;-webkit-backdrop-filter:blur(8px)!important;}
#chat .mes .ch_name > .flex1{border-radius:10px;background:linear-gradient(120deg,rgba(255,255,255,.18),rgba(232,245,239,.12));}
@supports not (backdrop-filter:blur(8px)){#top-bar,#send_form{background-color:#f4faf7!important;}}
'''
 theme=json.loads((ROOT/'theme/Honeydew-Letter.json').read_text());theme['name']=name;theme['custom_css']=css
 def rgba(c,a=1):return 'rgba('+', '.join(str(int(c[i:i+2],16)) for i in (1,3,5))+f', {a})'
 for k in ['main_text_color','italics_text_color','underline_text_color','quote_text_color']:theme[k]=rgba(ink)
 theme['blur_tint_color']=rgba(paper,.94);theme['chat_tint_color']=rgba(tint,.82);theme['border_color']=rgba(line)
 (ROOT/'theme'/f'{stem}.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2)+'\n');(ROOT/'theme'/f'{key}-material.css').write_text(css)
 fixture=(ROOT/'docs/honeydew-fixture.html').read_text().replace('../theme/honeydew.css',f'../theme/{key}-material.css').replace('蜜瓜花笺',name).replace('16:9 · 头像位置保留','16:9 · 头像区域')
 fixture=fixture.replace('<span class="name_text">'+name+'</span>','<span class="name_text">裴识渊</span>')
 fixture=fixture.replace('#f5f9ed',tint).replace('#748465',ink).replace('#fbfdf8',paper)
 (ROOT/'docs'/f'{key}-material-fixture.html').write_text(fixture)
 urls=set(re.findall(r"url\(['\"]?([^)'\"]+)",css));assert all(u.startswith(url) for u in urls);assert all((ROOT/u.removeprefix(BASE)).exists() for u in urls);assert 'data:image' not in css
 print(key,len(css.encode()),'CSS bytes',len(urls),'external assets')
if __name__=='__main__':
 key,source=sys.argv[1:];build(key,export(key,source))
