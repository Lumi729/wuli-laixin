"""Four independent SillyTavern layouts with separately drawn external artwork."""
from pathlib import Path
from PIL import Image
import json,re,zipfile
R=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/poetic-v2/'
CONFIG={
'starry':('星潮夜航','Starry-Voyage','#eef2ff','#102442','#8ba7d9','#0c1c38'),
'rabbit':('月兔涂鸦','Moon-Rabbit','#695383','#fffefe','#c9afe1','#f4edfc'),
'rain':('雨声留白','Rain-Window','#375e7b','#f9fdff','#b8d5e4','#edf7fc'),
'postal':('云端邮局','Cloud-Post-V2','#345c82','#fffefe','#b4cde5','#eaf4ff')}

def extract(key,path):
 im=Image.open(path).convert('RGBA');w,h=im.size;d=R/'assets/poetic-v2'/key;d.mkdir(parents=True,exist_ok=True)
 for name,box in [('header',(0,0,w//2,h//2)),('footer',(w//2,0,w,h//2)),('icons',(0,h//2,w//2,h)),('accent',(w//2,h//2,w,h))]:
  part=im.crop(box);bb=part.getchannel('A').point(lambda x:255 if x>20 else 0).getbbox()
  if not bb:raise ValueError(name)
  part=part.crop(bb);part.thumbnail((1100,900),Image.Resampling.LANCZOS);part.save(d/(name+'.webp'),quality=90,method=6)
  if name=='icons':
   # Four separately drawn motifs, prepared from the generated asset atlas (not the preview).
   iw,ih=part.size
   for j in range(4):
    icon=part.crop((j%2*iw//2,j//2*ih//2,(j%2+1)*iw//2,(j//2+1)*ih//2))
    ib=icon.getchannel('A').point(lambda x:255 if x>20 else 0).getbbox()
    if ib:icon=icon.crop(ib)
    icon.thumbnail((180,180),Image.Resampling.LANCZOS);icon.save(d/('icon-'+str(j+1)+'.webp'),quality=90,method=4)

def build(key):
 name,stem,ink,paper,line,bg=CONFIG[key];url=BASE+key+'/'
 css=f'''/* {name} · independent layout. External transparent artwork; no embedded bitmaps. */
:root{{--pv-ink:{ink};--pv-paper:{paper};--pv-line:{line};--pv-bg:{bg};}}
#sheld{{background:var(--pv-bg)!important;box-shadow:none!important;backdrop-filter:none!important;}}
#chat{{background:var(--pv-bg)!important;padding:14px 12px!important;container-type:inline-size;gap:0!important;}}
#chat .mes{{position:relative;isolation:isolate;box-sizing:border-box;display:grid!important;grid-template-columns:minmax(0,44%) minmax(0,1fr);align-items:center!important;column-gap:18px;row-gap:20px;width:100%!important;max-width:720px!important;min-width:0!important;margin:16px auto 32px!important;padding:28px 20px 76px!important;border:0!important;box-shadow:none!important;border-radius:0!important;background:var(--pv-paper)!important;color:var(--pv-ink)!important;backdrop-filter:none!important;}}
#chat .mes::before,#chat .mes::after{{content:'';position:absolute;pointer-events:none;background-repeat:no-repeat;background-size:contain;z-index:-1;}}
#chat .mes::after{{bottom:0;left:0;right:0;height:78px;background-image:url('{url}footer.webp');background-position:center bottom;}}
#chat .mes>.mes_block{{display:contents!important;}}
#chat .mes .mesAvatarWrapper{{grid-column:1;grid-row:1;display:flex!important;position:relative!important;flex-wrap:wrap;justify-content:space-around;align-content:start;gap:18px 2px;width:auto!important;max-width:100%!important;min-width:0!important;margin:0!important;padding:0!important;}}
#chat .mes .avatar{{position:relative;flex:0 0 100%;width:100%!important;max-width:none!important;height:auto!important;aspect-ratio:1;margin:0!important;padding:0!important;box-shadow:none!important;border:0!important;}}
#chat .mes .avatar img{{width:100%!important;height:100%!important;max-height:none!important;object-fit:cover!important;object-position:center 35%;border-radius:inherit!important;box-shadow:none!important;}}
#chat .mes .mesIDDisplay,#chat .mes .mes_timer,#chat .mes .tokenCounterDisplay{{position:static!important;width:auto!important;min-width:0!important;margin:0!important;padding:0!important;font-size:9px!important;line-height:1.4;color:var(--pv-ink)!important;opacity:.8;}}
#chat .mes .ch_name{{grid-column:2;grid-row:1;align-self:center;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:center!important;gap:14px;width:100%!important;min-width:0!important;margin:0!important;padding:0!important;background:none!important;}}
#chat .mes .ch_name>.flex1{{display:flex!important;justify-content:center;align-items:center;min-width:0;text-align:center;flex:none!important;}}
#chat .mes .name_text{{display:block;max-width:100%;font-size:21px!important;line-height:1.5;font-weight:400;color:var(--pv-ink)!important;text-align:center;overflow-wrap:anywhere;}}
#chat .mes .timestamp{{font-size:10px;}}
#chat .mes .mes_buttons{{position:relative!important;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:4px!important;width:100%!important;max-width:100%!important;min-width:0!important;margin:0!important;padding:8px 0!important;float:none!important;opacity:1!important;}}
#chat .mes .mes_button{{box-sizing:border-box;min-width:26px;flex:0 0 27%;min-height:30px;padding:4px!important;color:var(--pv-ink)!important;filter:none!important;text-shadow:none!important;}}
#chat .mes .extraMesButtons{{flex-wrap:wrap;justify-content:center;gap:4px;max-width:100%;}}
#chat .mes .mes_text{{grid-column:1/-1;position:relative;box-sizing:border-box;width:100%!important;min-width:0!important;margin:0!important;padding:12px 8px 20px!important;min-height:190px;line-height:1.9!important;color:var(--pv-ink)!important;overflow-wrap:anywhere;}}
#chat .mes .mes_text p{{margin:.35em 0 .85em;}}
#chat .mes .mes_text img,#chat .mes .mes_text video{{max-width:100%;height:auto;}}
#chat .mes .mes_text pre{{max-width:100%;overflow-x:auto;}}
#chat .mes .mes_text table{{display:block;max-width:100%;overflow-x:auto;}}
#chat .mes>.for_checkbox{{position:absolute;left:4px;top:4px;}}
#chat .mes>.swipe_left{{position:absolute;left:10px;bottom:15px;z-index:3;}}
#chat .mes>.swipe_right{{position:absolute;right:10px;bottom:15px;z-index:3;}}
#chat .mes .swipes-counter{{color:var(--pv-ink);}}
#top-bar{{background:var(--pv-paper)!important;border:0!important;border-bottom:1px solid var(--pv-line)!important;box-shadow:none!important;}}
#top-settings-holder{{gap:0!important;}}
#top-settings-holder .drawer{{min-width:0!important;flex:1 1 0;}}
#top-settings-holder .drawer-toggle{{display:flex;align-items:center;justify-content:center;min-height:38px;}}
#top-settings-holder .drawer-icon{{color:var(--pv-ink)!important;filter:none!important;opacity:1!important;font-size:22px!important;}}
#send_form{{box-sizing:border-box;gap:8px!important;border:1px solid var(--pv-line)!important;background:var(--pv-paper)!important;box-shadow:none!important;border-radius:22px!important;padding:10px 12px!important;}}
#send_textarea{{background:transparent!important;color:var(--pv-ink)!important;border:0!important;box-shadow:none!important;min-height:40px;}}
#send_textarea::placeholder{{color:var(--pv-ink);opacity:.65;}}
#send_form :is(i,.fa-solid,.fa-regular){{color:var(--pv-ink)!important;filter:none!important;}}
@media(max-width:360px){{#chat{{padding:10px 7px!important;}}#chat .mes{{padding-inline:14px!important;column-gap:12px;}}#chat .mes .name_text{{font-size:18px!important;}}}}
'''
 if key=='starry':
  css+=f'''
#chat .mes{{grid-template-columns:minmax(0,1fr);padding:0 16px 108px!important;background:#102442!important;border-radius:0 0 20px 20px!important;}}
#chat .mes .mesAvatarWrapper{{grid-column:1;grid-row:1;padding:14px 0 0!important;}}
#chat .mes .avatar{{aspect-ratio:16/9;border-radius:42% 20% 35% 14%!important;}}
#chat .mes .avatar::after{{content:'';position:absolute;inset:-8px -16px -8px;pointer-events:none;background:url('{url}header.webp') center/100% auto no-repeat;}}
#chat .mes .ch_name{{grid-column:1;grid-row:2;gap:4px;}}
#chat .mes .ch_name>.flex1{{justify-content:flex-start;padding-left:12px;}}
#chat .mes .mes_buttons{{justify-content:flex-end;padding-right:12px!important;border-bottom:1px solid #627fab;}}
#chat .mes .mes_text{{min-height:210px;padding:10px 16px 20px!important;}}
#chat .mes::after{{height:125px;background-size:100% auto;z-index:0;}}
#chat .mes .mes_button{{flex:0 0 auto;}}
#send_form{{border-color:#5679b0!important;}}
'''
 if key=='rabbit':
  css+=f'''
#chat .mes{{background:#fffefe!important;border-radius:18px 6px 26px 9px!important;}}
#chat .mes::before{{inset:0;border:3px dashed #dfc9ee;border-radius:18px 6px 26px 9px;}}
#chat .mes .avatar{{border-radius:50%!important;}}
#chat .mes .avatar::after{{content:'';position:absolute;inset:-14px;pointer-events:none;background:url('{url}header.webp') center/contain no-repeat;}}
#chat .mes .mes_text{{padding-top:20px!important;}}
#chat .mes .ch_name>.flex1{{border-bottom:3px solid #edc3de;padding-bottom:7px;}}
#chat .mes::after{{display:none;}}
#chat .mes .mes_text::after{{content:'';position:absolute;bottom:-46px;right:0;width:72px;height:72px;pointer-events:none;background:url('{url}accent.webp') center/contain no-repeat;}}
#send_form{{border:2px dashed #cbb1df!important;border-radius:8px 20px 8px 15px!important;}}
'''
 if key=='rain':
  css+=f'''
#chat .mes{{padding-top:76px!important;background:linear-gradient(145deg,#eef9ff,#ffffff 60%,#e6f2fa)!important;border-radius:16px!important;}}
#chat .mes::before{{top:0;left:-5px;width:72%;height:125px;background-image:url('{url}header.webp');background-position:left top;z-index:2;}}
#chat .mes .avatar{{border:6px solid #fff!important;border-bottom-width:17px!important;border-radius:2px!important;transform:rotate(-5deg);}}
#chat .mes .ch_name{{padding-top:44px!important;}}
#chat .mes .ch_name::before{{content:'';position:absolute;top:8px;right:5px;width:62px;height:130px;background:url('{url}footer.webp') center top/contain no-repeat;pointer-events:none;}}
#chat .mes .ch_name>.flex1{{border-bottom:1px solid #b8d5e4;padding-bottom:6px;}}
#chat .mes .mes_text{{border:1px solid #fff;border-radius:22px;background:rgba(255,255,255,.68);padding:24px 20px!important;}}
#chat .mes::after{{height:80px;background-image:url('{url}accent.webp');background-position:left bottom;background-size:auto 100%;z-index:0;}}
#top-bar,#send_form{{background:rgba(246,252,255,.92)!important;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);}}
'''
 if key=='postal':
  css+=f'''
#chat .mes{{grid-template-columns:minmax(0,1fr) minmax(0,35%);padding-top:60px!important;padding-bottom:95px!important;border:1px solid #d6e3ef!important;box-shadow:4px 5px 0 #dfebf7!important;}}
#chat .mes::before{{top:-28px;left:-5px;right:-5px;height:120px;background-image:url('{url}header.webp');background-position:center top;background-size:contain;}}
#chat .mes .mesAvatarWrapper{{grid-column:2;grid-row:1;}}
#chat .mes .avatar{{border:7px solid white!important;outline:2px dashed #a5c4df;outline-offset:2px;border-radius:0!important;}}
#chat .mes .ch_name{{grid-column:1;grid-row:1;}}
#chat .mes .ch_name>.flex1{{border-bottom:3px double #b4cde5;padding-bottom:8px;}}
#chat .mes .mes_text{{padding:20px 12px!important;}}
#chat .mes::after{{height:96px;background-size:contain;z-index:0;}}
#send_form{{border-radius:4px!important;border:2px solid #b4cde5!important;border-bottom:4px dashed #c7b5cf!important;}}
'''
 for j in range(1,10):
  css+=f"\n#top-settings-holder>.drawer:nth-child({j}) .drawer-icon{{{{width:28px!important;height:30px!important;font-size:0!important;background:url('{url}icon-{(j-1)%4+1}.webp') center/contain no-repeat!important;}}}}#top-settings-holder>.drawer:nth-child({j}) .drawer-icon::before{{{{opacity:0!important;}}}}".replace('{{','{').replace('}}','}')
 css+=f"\n#send_but{{{{background:url('{url}icon-2.webp') center/contain no-repeat!important;font-size:0!important;}}}}#send_but::before{{{{opacity:0;}}}}".replace('{{','{').replace('}}','}')
 css+='\n/* Smaller user portraits retain role identification without duplicating the large hero. */\n#chat .mes[is_user="true"]{padding-top:26px!important;}\n'
 theme=json.loads((R/'theme/Honeydew-Letter.json').read_text());theme['name']=name;theme['custom_css']=css
 def rgba(c):return 'rgba('+', '.join(str(int(c[i:i+2],16)) for i in (1,3,5))+', 1)'
 for p in ['main_text_color','italics_text_color','underline_text_color','quote_text_color']:theme[p]=rgba(ink)
 for p in ['blur_tint_color','chat_tint_color']:theme[p]=rgba(bg)
 theme['border_color']=rgba(line)
 (R/'theme'/f'{stem}.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2)+'\n')
 (R/'theme'/f'{key}-poetic.css').write_text(css)
 fixture=(R/'docs/honeydew-fixture.html').read_text().replace('../theme/honeydew.css',f'../theme/{key}-poetic.css').replace('蜜瓜花笺',name)
 fixture=fixture.replace('<span>16:9 · 头像位置保留</span>','<img src="sample-role.webp" alt="示例角色头像">').replace('<span class="name_text">'+name+'</span>','<span class="name_text">裴识渊</span>')
 fixture=fixture.replace('<i id="leftNavDrawerIcon" class="drawer-icon"></i>','<i id="leftNavDrawerIcon" class="drawer-icon">☰</i>')
 fixture=fixture.replace('<i id="API-status-top" class="drawer-icon"></i>','<i id="API-status-top" class="drawer-icon">⌁</i>')
 icons=iter(['✎','⚙','▧','♧','♙'])
 fixture=re.sub(r'<i class="drawer-icon"></i>',lambda m:'<i class="drawer-icon">'+next(icons)+'</i>',fixture)
 fixture=fixture.replace('<i id="WIDrawerIcon" class="drawer-icon"></i>','<i id="WIDrawerIcon" class="drawer-icon">▤</i>').replace('<i id="rightNavDrawerIcon" class="drawer-icon"></i>','<i id="rightNavDrawerIcon" class="drawer-icon">♧</i>')
 fixture=fixture.replace('<i id="options_button"></i>','<i id="options_button">＋</i>').replace('<i id="extensionsMenuButton"></i>','<i id="extensionsMenuButton">♧</i>').replace('<i id="send_but"></i>','<i id="send_but">➤</i>')
 (R/'docs'/f'{key}-poetic-fixture.html').write_text(fixture)
 assert 'data:image' not in css
 return stem
if __name__=='__main__':
 import sys
 if len(sys.argv)>1:extract(sys.argv[1],sys.argv[2])
 else:
  for key in CONFIG:build(key)
