from pathlib import Path
from PIL import Image
import re,json
R=Path(__file__).resolve().parents[1];d=R/'assets/editorial-icons';d.mkdir(exist_ok=True)
paths={
'sliders':'M5 4v16M12 4v16M19 4v16M2 8h6M9 16h6M16 10h6',
'plug':'M8 3v5m8-5v5M6 8h12v4a6 6 0 0 1-12 0zM12 18v4',
'quill':'M4 21 17 4M5 17c-3-6 5-14 15-14 0 8-5 15-12 15M11 10l4 0M9 13h4',
'book':'M12 6Q6 2 2 5v15q5-3 10 0 5-3 10 0V5q-5-3-10 1v14',
'gear':'M10 3h4l1 3 3-1 2 3-2 3 2 3-2 3-3-1-1 3h-4l-1-3-3 1-2-3 2-3-2-3 2-3 3 1z M15 11a3 3 0 1 1-6 0 3 3 0 0 1 6 0',
'image':'M3 4h18v16H3zM3 17l6-6 4 4 3-3 5 5M17 8h.01',
'puzzle':'M3 4h6q-1-4 3-4t3 4h6v6q-4-1-4 3t4 3v6h-6q1-4-3-4t-3 4H3v-6q4 1 4-3t-4-3z',
'person':'M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0M4 22v-4a8 6 0 0 1 16 0v4z',
'cards':'M4 5l11-3 4 16-11 3zM18 5h4v17H11',
'send':'M2 3l20 9L2 21l4-9zM6 12h16',
'continue':'M8 5l8 7-8 7M3 5l8 7-8 7',
'copy':'M8 8h13v13H8zM4 16H2V2h14v2',
'edit':'M3 21l1-6L17 2l5 5L9 20zM14 5l5 5',
'chart':'M3 2v19h19M7 17v-6m5 6V5m5 12V8',
'music':'M9 18V5l12-2v13M9 5v4l12-2M9 18a3 2 0 1 1-6 0 3 2 0 0 1 6 0M21 16a3 2 0 1 1-6 0 3 2 0 0 1 6 0',
'more':'M4 12h.01M12 12h.01M20 12h.01'}
for key,p in paths.items():
 (d/(key+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48"><path d="{p}" fill="none" stroke="#30433b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
# Fixtures use static illustrative avatars only, never baked into the theme.
for key,src,box in [('night','exec-ce316bf7-6f90-46f4-9643-97ab68070a00.png',(80,105,305,387)),('orange','exec-28b3cac8-fcec-4b5f-896a-4c008199c3d7.png',(53,42,252,243)),('user','exec-28b3cac8-fcec-4b5f-896a-4c008199c3d7.png',(863,961,980,1083))]:
 if not (R.parent/'generated_images'/src).exists():
  assert (R/'docs'/f'editorial-{key}-avatar.webp').exists();continue
 im=Image.open(R.parent/'generated_images'/src).crop(box);im.save(R/'docs'/f'editorial-{key}-avatar.webp',quality=90)
nav=[('leftNavDrawerIcon','','sliders'),('API-status-top','','plug'),('','advanced-formatting-button','quill'),('WIDrawerIcon','','book'),('','user-settings-button','gear'),('','backgrounds-button','image'),('','extensions-settings-button','puzzle'),('','persona-management-button','person'),('rightNavDrawerIcon','','cards')]
navhtml=''.join(f'<div class="drawer" id="{parent}"><div class="drawer-toggle"><button id="{i}" class="drawer-icon" title="{icon}"><img src="../assets/editorial-icons/{icon}.svg"></button></div></div>' for i,parent,icon in nav)
base='''#top-settings-holder .drawer-icon img,#send_form button img{display:none}*{box-sizing:border-box}body{margin:0;color:#30433b;font-family:"Noto Serif CJK SC",serif}#top-bar{position:sticky;top:0;z-index:50}#top-settings-holder{display:flex;justify-content:space-around}button{font:inherit;cursor:pointer}.drawer-icon img{width:19px;height:19px}.drawer{display:flex;justify-content:center}.mes{display:flex}.mesAvatarWrapper{display:flex;flex-direction:column}.avatar{width:50px;height:50px}.avatar img{display:block}.mes_block{flex:1}.ch_name,.flex-container,.mes_buttons{display:flex}.mes_edit_buttons,.del_checkbox,.for_checkbox{display:none}.extraMesButtons{display:none}.mes_buttons button{border:0}.mes_buttons img{width:15px;height:15px}.mes_reasoning_summary{list-style:none}.mes_reasoning_header_block{display:flex}#send_form{display:flex;margin:0}#send_textarea{width:100%;min-height:45px;resize:vertical}#send_form button{border:0;padding:5px}#send_form img{width:20px;height:20px}#chat{display:flex;flex-direction:column}#sheld{max-width:100%}#send_form{position:sticky;bottom:0;z-index:50}.swipes-counter{display:inline}'''
for key in ['night-log','orange-soda']:
 def msg(n,user=False):
  avatar='user' if user else ('night' if key=='night-log' else 'orange')
  name='你' if user else ('沈砚' if key=='night-log' else '夏川')
  body='<p>我会来的。<br>你要记得带上那封信。</p>' if user else '<p>夜色沿着窗棂慢慢落下。</p><p>他将那封信放在你掌心，纸页还带着淡淡的花香。</p><p>「若你愿意，明夜仍在这里等我。」</p>'
  btn=''.join(f'<button class="mes_button '+('extraMesButtonsHint' if a=='more' else 'mes_'+a)+f'" title="{a}"><img src="../assets/editorial-icons/{a}.svg"></button>' for a in ['more','music','edit','copy','chart'])
  return f'''<article class="mes" mesid="{n}" is_user="{str(user).lower()}" ch_name="{name}"><div class="for_checkbox"></div><input class="del_checkbox" type="checkbox"><div class="mesAvatarWrapper"><div class="avatar"><img src="editorial-{avatar}-avatar.webp"></div><div class="mesIDDisplay">#{n}</div><div class="mes_timer">{'' if user else '604.1s'}</div><div class="tokenCounterDisplay">{'' if user else '37953t'}</div></div><div class="swipe_left">‹</div><div class="mes_block"><div class="ch_name"><div class="flex-container flex1 alignitemscenter"><div class="alignItemsBaseline"><span class="name_text">{name}</span><small class="timestamp">22:17</small></div></div><div class="mes_buttons">{btn}<div class="extraMesButtons"><button class="mes_button" title="expand-action">↶</button><button class="mes_button">↷</button></div></div></div>'''+('' if user else '''<details class="mes_reasoning_details" open><summary class="mes_reasoning_summary"><div class="mes_reasoning_header_block"><div class="mes_reasoning_header"><span class="mes_reasoning_header_title">思绪</span><span class="mes_reasoning_arrow">⌄</span></div></div></summary><div class="mes_reasoning"><p>他停顿片刻，认真收好这封信。或许有些话，要留到下一次见面再说。</p></div></details>''')+f'<div class="mes_text">{body}</div></div><div class="swipe_right"><span class="swipes-counter">1 / 3</span> ›</div></article>'
 inputhtml='<form id="send_form">'+''.join(f'<button type="button" id="{i}" title="{a}"><img src="../assets/editorial-icons/{a}.svg"></button>' for i,a in [('options_button','book'),('extensionsMenuButton','puzzle')])+'<textarea id="send_textarea" placeholder="写下你的回信…"></textarea>'+''.join(f'<button type="button" id="{i}" title="{a}"><img src="../assets/editorial-icons/{a}.svg"></button>' for i,a in [('mes_impersonate','person'),('mes_continue','continue'),('send_but','send')])+'</form>'
 html=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{key} · native DOM sample</title><style>{base}</style><link rel="stylesheet" href="../theme/{key}.css"><div id="top-bar"><div id="top-settings-holder">{navhtml}</div></div><main id="sheld"><div id="chat">{msg(12)}{msg(13,True)}</div></main>{inputhtml}<script>document.querySelectorAll('.extraMesButtonsHint').forEach(b=>b.onclick=()=>{{const e=b.parentElement.querySelector('.extraMesButtons');e.style.display=e.style.display==='flex'?'none':'flex'}});</script></html>'''
 (R/'docs'/f'{key}-fixture.html').write_text(html)
