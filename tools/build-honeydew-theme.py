"""蜜瓜花笺: independent external artwork on the established Rose layout."""
from pathlib import Path
import json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/'
ART=BASE+'assets/honeydew-v1/'
css=(ROOT/'theme/rose-moon-phases.css').read_text()
# Keep the original layout and responsive behavior; replace only painted assets.
mapping={'paper.webp':None,'portrait-surround.webp':'portrait-surround.webp','bottom-left.webp':'bottom-left.webp','bottom-right.webp':'bottom-right.webp','moon-footer.webp':'bottom-center.webp','counter-frame.webp':'counter-mark.svg','name-left.webp':None,'name-right.webp':None,'name-ribbon.webp':'name-ribbon.webp','bar-frame.webp':'bar-frame.webp','reasoning-ribbon.webp':'name-ribbon.webp','message-divider.webp':'counter-mark.svg','controls-frame.webp':'controls-frame.webp'}
def replace(m):
 name=m[1].split('/')[-1]
 target=name if name.startswith('icon-') else mapping[name]
 return "url('"+ART+target+"')" if target else 'none'
css=re.sub(r"url\('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/(assets/[^']+)'\)",replace,css)
palette={'#4b3540':'#3e493d','#795560':'#879775','#fff6f3':'#fbfdf8','#f9e8ed':'#f7faf2','#b18a94':'#c9d5b9','#fff1f5':'#fbfdf8','#99717e':'#a3b392','#ad8592':'#9eae8f','#fff8fb':'#fcfdf9','#956578':'#7f966a','#fff7f9':'#fbfdf7','#c28b9e':'#becfa9','#e5becb':'#dce8ce','#bb93a3':'#bacbac','#ffe1ec':'#edf4e4','rgba(249,232,237,':'rgba(247,250,242,'}
for a,b in palette.items():css=css.replace(a,b)
css=css.replace('玫瑰月相 · external assets v1.','蜜瓜花笺 · independent external artwork.')
css+=f'''
/* Approved asymmetric lily-and-ribbon design. All bitmap art scales uniformly. */
#chat {{background:#fbfdf8!important;}}
#chat .mes {{background:none!important;margin-bottom:40px!important;}}
#chat .mes::before {{
 top:calc(100cqw * 9 / 941);height:calc(100cqw * 780 / 941);aspect-ratio:auto;
 background:url('{ART}portrait-surround.webp') center top / 100% auto no-repeat;
}}
#chat .mes + .mes::before {{
 top:calc(100cqw * 9 / 941);height:calc(100cqw * 780 / 941);
 background:url('{ART}portrait-surround.webp') center top / 100% auto no-repeat;
}}
#chat .mes > .mes_block::before,#chat .mes > .mes_block::after {{display:none;}}
#chat .mes > .mesAvatarWrapper > .avatar {{border-color:transparent;}}
#chat .mes > .mesAvatarWrapper::after {{
 left:0!important;right:0!important;
 background-image:url('{ART}counter-mark.svg'),url('{ART}counter-mark.svg'),linear-gradient(#b0bf9e,#b0bf9e);
 background-size:22px auto,22px auto,100% 1px;
 background-position:33.333% center,66.667% center,center bottom;background-repeat:no-repeat;
}}
#chat .mes .ch_name {{background-size:146px auto!important;}}
#chat .mes .ch_name > .flex1 {{min-height:44px;}}
#chat .mes .ch_name .name_text {{transform:translate(-7px,-2px);}}
#chat .mes .mes_buttons {{
 padding-block:calc(var(--wl-controls-width) * .1025)!important;
 align-content:center!important;align-items:center!important;
}}
#chat .mes .mes_buttons::before {{border:0;border-image:none;background:url('{ART}controls-frame.webp') center / contain no-repeat;}}
/* Three adjoining footer parts; source proportions and seams are preserved. */
#chat .mes::after {{
 height:calc(100cqw * 324 / 941);max-height:none;
 background-image:url('{ART}bottom-left.webp'),url('{ART}bottom-right.webp'),url('{ART}bottom-center.webp');
 background-size:31.88% auto,31.88% auto,36.24% auto;
 background-position:left bottom,right bottom,center bottom;
}}
#top-bar,#send_form {{border-color:transparent!important;outline:none!important;box-shadow:none!important;}}
#top-bar::after,#send_form::after {{
 inset:-2px 0!important;border:10px solid transparent!important;background:none!important;
 border-image:url('{ART}bar-frame.webp') 150 230 110 230 / 15px 23px 11px 23px / 0 stretch!important;
}}
#top-settings-holder .drawer-icon {{flex-basis:32px!important;width:32px!important;min-width:32px!important;background-size:32px 32px!important;filter:none!important;}}
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {{min-width:32px!important;min-height:32px!important;background-size:32px 32px!important;filter:none!important;}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes {{margin-bottom:calc(var(--c) * 40)!important;}}
 #chat .mes > .mesAvatarWrapper::after {{background-size:calc(var(--c) * 22) auto,calc(var(--c) * 22) auto,100% 1px;}}
 #chat .mes .ch_name {{background-size:calc(var(--c) * 146) auto!important;}}
 #chat .mes .ch_name > .flex1 {{min-height:calc(var(--c) * 44);}}
 #chat .mes .ch_name .name_text {{transform:translate(calc(var(--c) * -7),calc(var(--c) * -2));}}
}}
@media (min-width:600px) {{
 #top-settings-holder .drawer-icon {{background-size:36px 36px!important;}}
 #send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but) {{background-size:36px 36px!important;}}
}}
'''
css+=f'''
/* A small independent body accent, never a body-sized bitmap. */
#chat .mes .mes_text {{position:relative;}}
#chat .mes .mes_text::after {{content:"";position:absolute;right:-18px;top:25%;width:32px;aspect-ratio:2/3;pointer-events:none;background:url('{ART}body-sprig.webp') center / contain no-repeat;}}
#chat .mes .mes_buttons .mes_button {{color:#7f966a;}}
@media (min-width:600px) and (orientation:portrait) {{
 #chat .mes .mes_text::after {{right:calc(var(--c) * -18);width:calc(var(--c) * 32);}}
}}
'''
theme=json.loads((ROOT/'theme/Blue-Clean.json').read_text());theme['name']='蜜瓜花笺';theme['custom_css']=css
theme.update({
 'main_text_color':'rgba(62, 73, 61, 1)',
 'italics_text_color':'rgba(110, 130, 94, 1)',
 'underline_text_color':'rgba(111, 138, 87, 1)',
 'quote_text_color':'rgba(105, 125, 91, 1)',
 'blur_tint_color':'rgba(251, 253, 248, 0.94)',
 'chat_tint_color':'rgba(247, 250, 242, 0.82)',
 'user_mes_blur_tint_color':'rgba(251, 253, 248, 0)',
 'bot_mes_blur_tint_color':'rgba(251, 253, 248, 0)',
 'shadow_color':'rgba(0, 0, 0, 0)',
 'border_color':'rgba(201, 213, 185, 1)',
})
(ROOT/'theme/honeydew.css').write_text(css)
(ROOT/'theme/Honeydew-Letter.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2)+'\n')
urls=sorted(set(re.findall(r"url\(['\"]?([^)'\"]+)",css)))
for u in urls:
 assert u.startswith(ART),u
 p=ROOT/u.removeprefix(BASE);assert p.exists() and p.stat().st_size>100,p
 if p.suffix=='.webp':
  im=Image.open(p);im.load();assert im.mode=='RGBA'
assert 'data:image' not in css
print(len(css.encode()),'CSS bytes;',len(urls),'assets;',sum((ROOT/u.removeprefix(BASE)).stat().st_size for u in urls),'asset bytes')
