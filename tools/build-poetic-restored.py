"""Build modular, reference-led material layouts. Never embed images in theme JSON."""
from pathlib import Path
import json,re,zipfile,shutil
R=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/'
CONFIG={
 'starry':('星潮夜航','Starry-Voyage-V3','#f0f3ff','#081936'),
 'rabbit':('月兔涂鸦','Moon-Rabbit-V3','#6d4b91','#f1e7fa'),
 'rain':('雨声留白','Rain-Window-V3','#315b82','#eef7ff'),
 'postal':('云端邮局','Cloud-Post-V3','#365f8b','#eaf4ff')}
COMMON='''
:root{--pr-ink:INK;--pr-base:BASECOLOR;}
#sheld{background:var(--pr-base)!important;box-shadow:none!important;backdrop-filter:none!important;}
#chat{padding:0!important;gap:0!important;container-type:inline-size;background:var(--pr-base) url('URLsurface.webp') center top/100% auto repeat-y!important;}
#chat .mes{position:relative;isolation:isolate;box-sizing:border-box;display:grid!important;grid-template-columns:minmax(0,48%) minmax(0,1fr);column-gap:12px;row-gap:16px;align-items:center!important;width:100%!important;max-width:720px!important;min-width:0!important;margin:0 auto 24px!important;padding:24px 20px 80px!important;border:0!important;border-radius:0!important;background:none!important;box-shadow:none!important;color:var(--pr-ink)!important;backdrop-filter:none!important;}
#chat .mes>.mes_block{display:contents!important;}
#chat .mes::before,#chat .mes::after,#chat .mes>.mes_block::before,#chat .mes>.mes_block::after{content:'';position:absolute;pointer-events:none;background-repeat:no-repeat;background-size:contain;z-index:-1;}
#chat .mes .mesAvatarWrapper{grid-column:1;grid-row:1;position:relative!important;display:flex!important;flex-wrap:wrap;justify-content:space-around;align-items:center;align-content:start;gap:12px 2px;width:auto!important;max-width:100%!important;min-width:0!important;margin:0!important;padding:0!important;}
#chat .mes .avatar{box-sizing:border-box;position:relative;flex:0 0 100%;width:100%!important;max-width:none!important;height:auto!important;aspect-ratio:1;margin:0!important;padding:0!important;border:0!important;box-shadow:none!important;background:none!important;}
#chat .mes .avatar img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:center 35%;border-radius:inherit!important;box-shadow:none!important;}
#chat .mes .mesIDDisplay,#chat .mes .mes_timer,#chat .mes .tokenCounterDisplay{position:static!important;width:auto!important;margin:0!important;padding:0!important;line-height:1.4!important;font-size:9px!important;color:var(--pr-ink)!important;opacity:.75;}
#chat .mes .ch_name{grid-column:2;grid-row:1;align-self:center;position:relative;display:flex!important;flex-direction:column!important;justify-content:center!important;align-items:stretch!important;gap:12px;width:100%!important;min-width:0!important;margin:0!important;padding:0!important;background:none!important;}
#chat .mes .ch_name>.flex1{display:flex!important;flex:none!important;justify-content:center;align-items:center;min-width:0;text-align:center;}
#chat .mes .name_text{display:block;max-width:100%;font-size:21px!important;line-height:1.4;font-weight:400;color:var(--pr-ink)!important;overflow-wrap:anywhere;}
#chat .mes .timestamp{font-size:9px;}
#chat .mes .mes_buttons{position:relative!important;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:2px!important;width:100%!important;max-width:100%!important;min-width:0!important;margin:0!important;padding:4px 0!important;float:none!important;opacity:1!important;}
#chat .mes .mes_button{box-sizing:border-box;flex:0 0 auto;min-width:20px;min-height:26px;padding:2px!important;color:var(--pr-ink)!important;filter:none!important;text-shadow:none!important;}
#chat .mes .extraMesButtons{flex-wrap:wrap;justify-content:center;gap:4px;max-width:100%;flex-basis:100%;}
#chat .mes .mes_text{grid-column:1/-1;position:relative;box-sizing:border-box;width:100%!important;min-width:0!important;margin:0!important;padding:24px 15px 35px!important;min-height:200px;line-height:1.9!important;color:var(--pr-ink)!important;overflow-wrap:anywhere;}
#chat .mes .mes_text p{margin:.4em 0 .9em;}
#chat .mes .mes_text img,#chat .mes .mes_text video{max-width:100%;height:auto;}
#chat .mes .mes_text pre{max-width:100%;overflow-x:auto;}
#chat .mes .mes_text table{display:block;max-width:100%;overflow-x:auto;}
#chat .mes>.for_checkbox{position:absolute;left:4px;top:4px;}
#chat .mes>.swipe_left{position:absolute;left:10px;bottom:14px;z-index:3;}
#chat .mes>.swipe_right{position:absolute;right:10px;bottom:14px;z-index:3;}
#chat .mes .swipes-counter{color:var(--pr-ink);}
#top-bar{background:var(--pr-base) url('URLsurface.webp') center top/100% auto!important;box-shadow:none!important;border:0!important;}
#top-settings-holder{gap:0!important;}
#top-settings-holder>.drawer{min-width:0!important;flex:1 1 0;}
#top-settings-holder .drawer-toggle{display:flex;align-items:center;justify-content:center;min-height:38px;}
#top-settings-holder .drawer-icon{color:var(--pr-ink)!important;filter:none!important;opacity:1!important;font-size:22px!important;}
#send_form{position:relative;isolation:isolate;box-sizing:border-box;gap:8px!important;min-height:64px;padding:12px 18px!important;border:0!important;box-shadow:none!important;border-radius:0!important;background:var(--pr-base) url('URLsurface.webp') center bottom/100% auto!important;}
#send_form::before{content:'';position:absolute;inset:5px;z-index:-1;pointer-events:none;background:rgba(255,255,255,.85);border-radius:20px;}
#send_textarea{background:transparent!important;color:var(--pr-ink)!important;border:0!important;box-shadow:none!important;min-height:36px;}
#send_textarea::placeholder{color:var(--pr-ink);opacity:.7;}
#send_form :is(i,.fa-solid,.fa-regular){color:var(--pr-ink)!important;filter:none!important;}
@media(min-width:700px){#chat .mes .name_text{font-size:25px!important;}#chat .mes .mes_text{font-size:18px;}}
'''
SPEC={
'starry':'''
#chat .mes{grid-template-columns:minmax(0,1fr);padding:0 0 clamp(110px,32vw,220px)!important;row-gap:0;background:url('URLsurface.webp') center/100% auto repeat-y!important;}
#chat .mes .mesAvatarWrapper{grid-column:1;grid-row:1;gap:0;}
#chat .mes .avatar{aspect-ratio:1.52;border-radius:0!important;}
#chat .mes .avatar img{clip-path:ellipse(50% 34% at 50% 49%);}
#chat .mes .avatar::after{content:'';position:absolute;inset:0;pointer-events:none;background:url('URLhero.webp') center/contain no-repeat;}
#chat .mes .mesIDDisplay,#chat .mes .mes_timer,#chat .mes .tokenCounterDisplay{z-index:3;line-height:18px!important;margin-top:0!important;font-size:8px!important;}
#chat .mes .ch_name{grid-column:1;grid-row:2;box-sizing:border-box;display:flex!important;flex-direction:row!important;flex-wrap:wrap;gap:0!important;align-items:center!important;margin-top:-12px!important;padding:0 25px 12px!important;z-index:2;}
#chat .mes .ch_name>.flex1{flex:1 1 35%!important;justify-content:flex-start;text-align:left;}
#chat .mes .mes_buttons{flex:1 1 55%;max-width:65%!important;padding-bottom:14px!important;}
#chat .mes .mes_buttons::after{content:'';position:absolute;left:0;right:0;bottom:-8px;height:22px;background:url('URLarc-line.svg') center/100% auto no-repeat;pointer-events:none;opacity:.8;z-index:-1;}
#chat .mes .mes_button{color:#e7ca81!important;font-size:16px;min-width:26px;}
#chat .mes .mes_text{min-height:150px;padding:26px 11% 34px!important;}
#chat .mes::after{left:0;right:0;bottom:0;height:clamp(150px,42vw,290px);background:url('URLsea.webp') center bottom/100% auto no-repeat;z-index:0;}
#send_form::before{inset:7px 10px;background:rgba(7,24,49,.88);border:1px solid #8aa7ca;border-radius:30px;}
#send_form{padding-block:17px!important;}
''',
'rabbit':'''
#chat .mes{width:calc(100% - 14px)!important;margin-top:25px!important;margin-bottom:32px!important;padding:20px 18px 50px!important;row-gap:12px;}
#chat .mes::before{inset:0;background:#fff url('URLpaper-grain.webp') center/360px auto repeat;mask:url('URLpaper-sides.svg') center top/100% auto repeat-y;z-index:-2;}
#chat .mes>.mes_block::before{left:0;right:0;top:-26px;height:65px;background:url('URLpaper-top.webp') center top/100% auto no-repeat;z-index:-3;}
#chat .mes::after{left:0;right:0;bottom:-15px;height:100px;background:url('URLpaper-bottom.webp') center bottom/100% auto no-repeat;z-index:-1;}
#chat .mes .avatar{border-radius:50%!important;}
#chat .mes .avatar::after{content:'';position:absolute;inset:-12px;pointer-events:none;background:url('URLportrait-ring.webp') center/contain no-repeat;}
#chat .mes .mesAvatarWrapper{gap:15px 2px;}
#chat .mes .ch_name{padding-top:12px!important;}
#chat .mes .ch_name>.flex1{padding:6px 0 8px;background:url('URLpink-stroke.svg') center bottom/90% 9px no-repeat;}
#chat .mes .mes_text{min-height:170px;padding:20px 20px 35px!important;}
#chat .mes .mes_text::before{content:'';position:absolute;left:-21px;top:35%;width:37px;height:76px;background:url('URLmargin-doodles.webp') center/contain no-repeat;pointer-events:none;}
#chat .mes .mes_text::after{content:'';position:absolute;right:-14px;bottom:-35px;width:64px;height:76px;background:url('URLbunny.webp') center/contain no-repeat;pointer-events:none;}
#send_form{padding:16px 20px!important;}
#send_form::before{inset:2px 6px;border-radius:0;background:url('URLcomposer.webp') center/100% auto no-repeat;}
''',
'rain':'''
#chat .mes{grid-template-columns:minmax(0,54%) minmax(0,1fr);padding:68px 15px 26px!important;gap:18px 12px;}
#chat .mes::before{left:0;top:-10px;width:79%;height:clamp(145px,42vw,240px);background:url('URLumbrella.webp') left top/contain no-repeat;z-index:2;}
#chat .mes .avatar{border:6px solid white!important;border-bottom-width:18px!important;border-radius:1px!important;transform:rotate(-7deg);}
#chat .mes .mesAvatarWrapper{gap:16px 2px;padding-left:5px!important;}
#chat .mes .ch_name{position:static;align-self:end;padding:0 3px 38px!important;}
#chat .mes .ch_name>.flex1{background:rgba(255,255,255,.8);padding:14px 0 18px;clip-path:polygon(0 7%,96% 0,100% 91%,4% 100%);}
#chat .mes .ch_name::before{content:'';position:absolute;top:8px;right:7px;width:22%;height:clamp(145px,42vw,240px);background:url('URLchime.webp') center top/contain no-repeat;pointer-events:none;}
#chat .mes .mes_buttons{position:absolute!important;right:3px;top:clamp(280px,76vw,470px);width:36px!important;max-width:36px!important;flex-direction:column!important;gap:9px!important;z-index:3;}
#chat .mes .mes_button{width:34px;height:34px;border:1px solid #fff;border-radius:50%;background:rgba(255,255,255,.72);color:#6c9fc2!important;box-shadow:0 2px 5px #b8d9eb44;}
#chat .mes .extraMesButtons{background:rgba(246,252,255,.95);border-radius:16px;}
#chat .mes .mes_text{width:calc(100% - 32px)!important;min-height:265px;padding:28px 23px 100px!important;border:1px solid #fff;border-radius:22px;background:rgba(248,252,255,.78);}
#chat .mes .mes_text::after{content:'';position:absolute;left:-8px;right:-8px;bottom:-8px;height:140px;pointer-events:none;background:url('URLrain-bottom.webp') center bottom/100% auto no-repeat;opacity:.9;mask-image:linear-gradient(transparent,#000 28%,#000 90%,transparent);}
#chat .mes .mes_text::before{content:'';position:absolute;inset:0;pointer-events:none;background:url('URLrain-left.webp') left top/24px auto repeat-y,url('URLrain-right.webp') right top/24px auto repeat-y;opacity:.5;}
#send_form::before{background:rgba(248,253,255,.76);border:1px solid white;box-shadow:inset 0 0 12px #fff8;border-radius:30px;}
#top-bar,#send_form{backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);}
''',
'postal':'''
#chat .mes{width:calc(100% - 24px)!important;grid-template-columns:minmax(0,1fr) minmax(0,29%);margin-top:120px!important;padding:24px 22px 58px!important;gap:8px 12px;}
#chat .mes::before{inset:0;background:#fff url('URLpaper-grain.webp') center/400px auto repeat;box-shadow:2px 2px 2px #bdd1e233;z-index:-2;}
#chat .mes>.mes_block::before{left:-4px;right:-4px;top:clamp(-100px,-13.5vw,-46px);height:130px;background:url('URLletter-top.webp') center top/100% auto no-repeat;z-index:-3;}
#chat .mes::after{left:-6px;right:-6px;bottom:-12px;height:135px;background:url('URLletter-bottom.webp') center bottom/100% auto no-repeat;z-index:0;}
#chat .mes .mesAvatarWrapper{grid-column:2;grid-row:1;transform:rotate(5deg);gap:10px 2px;}
#chat .mes .avatar{aspect-ratio:.83;background:#fff!important;border:7px solid #fff!important;border-radius:0!important;mask:url('URLstamp-mask.svg') center/100% 100% no-repeat;}
#chat .mes .avatar::after{content:'';position:absolute;inset:-7px;background:url('URLstamp-border.svg') center/100% 100% no-repeat;pointer-events:none;}
#chat .mes .ch_name{position:static;grid-column:1;grid-row:1;align-self:center;padding:0 0 15px!important;}
#chat .mes .ch_name>.flex1{position:relative;justify-content:flex-start;text-align:left;padding-bottom:22px;}
#chat .mes .name_text{font-size:23px!important;transform:rotate(-4deg);}
#chat .mes .ch_name>.flex1::after{content:'';position:absolute;left:0;bottom:-10px;width:100%;height:32px;background:url('URLpostmark.svg') left center/contain no-repeat;pointer-events:none;}
#chat .mes .mes_buttons{position:absolute!important;right:-2px;top:clamp(155px,41vw,270px);width:37px!important;max-width:37px!important;flex-direction:column!important;gap:4px!important;z-index:3;}
#chat .mes .mes_button{width:34px;height:30px;background-position:center!important;background-size:contain!important;background-repeat:no-repeat!important;border:0;}
#chat .mes .mes_text{min-height:180px;padding:14px 30px 25px 10px!important;}
#send_form{padding:22px 20px 15px!important;}
#send_form::before{inset:-12px 0 0;background:url('URLcomposer.webp') center/100% auto no-repeat;border-radius:0;}
'''}

def write_support():
 d=R/'assets/poetic-v3';d.mkdir(exist_ok=True)
 (d/'starry/arc-line.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="30"><path d="M0 5Q140 45 300 7" fill="none" stroke="#c8b57a" stroke-width=".8" stroke-dasharray="2 5"/></svg>')
 # Code-native clipping paths describe real paper/stamp edges; the visible materials are separately drawn images.
 (d/'rabbit/paper-sides.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="720" height="240" viewBox="0 0 720 240"><path fill="white" d="M7 0L4 15 9 26 5 39 8 50 3 64 7 79 4 94 8 110 5 126 9 141 3 156 7 170 4 188 8 205 4 221 7 240H713L716 223 711 207 716 188 712 172 717 155 712 138 716 120 712 104 717 87 712 72 716 55 711 38 716 20 713 0Z"/></svg>')
 (d/'rabbit/pink-stroke.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="12"><path d="M4 8Q70 2 195 4M9 10Q120 4 189 7" fill="none" stroke="#e9aacb" stroke-width="2" stroke-linecap="round"/></svg>')
 # Scalloped stamp silhouette is an SVG mask, avoiding an embedded bitmap or stretched decorative raster.
 holes=''.join(f'<circle cx="{x}" cy="0" r="4"/><circle cx="{x}" cy="240" r="4"/>' for x in range(10,200,15))+''.join(f'<circle cx="0" cy="{y}" r="4"/><circle cx="200" cy="{y}" r="4"/>' for y in range(10,240,15))
 (d/'postal/stamp-mask.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="240"><defs><mask id="s"><rect width="200" height="240" fill="white"/><g fill="black">'+holes+'</g></mask></defs><rect width="200" height="240" fill="white" mask="url(#s)"/></svg>')
 (d/'postal/stamp-border.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="240"><rect x="8" y="8" width="184" height="224" fill="none" stroke="#ccd1d5" stroke-width="1"/></svg>')
 (d/'postal/postmark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="230" height="55" viewBox="0 0 230 55"><g fill="none" stroke="#769cc7" stroke-width="1.2"><circle cx="192" cy="27" r="23"/><path d="M1 20Q45 10 88 20T173 20M1 29Q45 19 88 29T173 29M1 38Q45 28 88 38T173 38M179 27l25-11-10 22-4-9z"/></g></svg>')

def build(key):
 name,stem,ink,bg=CONFIG[key];url=BASE+'assets/poetic-v3/'+key+'/'
 css=('/* '+name+' · reference reconstruction, modular external textures and ornaments. */\n'+COMMON+SPEC[key]).replace('INK',ink).replace('BASECOLOR',bg).replace('URL',url)
 old=BASE+'assets/poetic-v2/'+key+'/'
 if key=='rabbit':css+='\n#send_form #send_but{background:none!important;font-size:0!important;}'
 for j in range(1,10):
  css+=f"\n#top-settings-holder>.drawer:nth-child({j}) .drawer-icon{{width:27px!important;height:29px!important;font-size:0!important;background:url('{old}icon-{(j-1)%4+1}.webp') center/contain no-repeat!important;}}#top-settings-holder>.drawer:nth-child({j}) .drawer-icon::before{{opacity:0!important;}}"
 if key=='postal':
  for j in range(2,7):
   css+=f"\n#chat .mes .mes_button:nth-child({j}){{background-image:url('{old}icon-{(j-2)%4+1}.webp');font-size:0!important;}}#chat .mes .mes_button:nth-child({j})::before{{opacity:0;}}"
 css+=f"\n#send_but{{background:url('{old}icon-{1 if key=='starry' else 4 if key=='rabbit' else 2}.webp') center/contain no-repeat!important;font-size:0!important;}}#send_but::before{{opacity:0;}}"
 if key in ('rain','postal'):
  css+='\n#chat .mes .mes_buttons .extraMesButtons{position:absolute;right:40px;top:0;width:76px;max-width:76px;flex-basis:auto;padding:6px;background:rgba(248,252,255,.98);border:1px solid #c5d9e7;border-radius:12px;z-index:5;}'
 if key=='postal':
  css+="\n#chat{background-position:center calc(-50vw)!important;}#chat .mes>.mes_block::after{right:8px;top:-115px;width:120px;height:75px;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/poetic-v2/postal/accent.webp') center/contain no-repeat;z-index:-1;}"
  css+='\n#chat .mes .mesAvatarWrapper :is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay){position:absolute!important;bottom:-16px;font-size:7px!important;}#chat .mes .mesAvatarWrapper .mesIDDisplay{left:0;}#chat .mes .mesAvatarWrapper .mes_timer{left:28%;}#chat .mes .mesAvatarWrapper .tokenCounterDisplay{right:0;}'
 theme=json.loads((R/'theme/Honeydew-Letter.json').read_text());theme['name']=name+' · 还原版';theme['custom_css']=css
 def rgba(c):return 'rgba('+', '.join(str(int(c[i:i+2],16)) for i in (1,3,5))+', 1)'
 for p in ['main_text_color','italics_text_color','underline_text_color','quote_text_color']:theme[p]=rgba(ink)
 for p in ['blur_tint_color','chat_tint_color']:theme[p]=rgba(bg)
 theme['border_color']=rgba(bg)
 (R/'theme'/f'{stem}.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2)+'\n');(R/'theme'/f'{key}-restored.css').write_text(css)
 fixture=(R/'docs'/f'{key}-poetic-fixture.html').read_text().replace(f'../theme/{key}-poetic.css',f'../theme/{key}-restored.css')
 # Same message length as the approved concept, while separate stress fixtures test long content.
 fixture=re.sub(r'<div class="mes_text">.*?</div></div></article>', '<div class="mes_text"><p>收到你的来信了。</p></div></div></article>',fixture,flags=re.S)
 (R/'docs'/f'{key}-restored-fixture.html').write_text(fixture)
 return stem
if __name__=='__main__':
 write_support()
 for k in CONFIG:build(k)
