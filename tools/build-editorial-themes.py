"""Two independent native-DOM themes. Art is external and uniformly scaled."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/'
common=r'''
/* Independent theme; replace custom CSS, do not append to Rose Moon Phases.
   No script, embedded raster, blur, animation, stretched decorative image. */
:root{--topBarBlockSize:58px;--ed-ink:#253343;--ed-paper:#f3eee3;--ed-tint:#e2e5e5;--ed-accent:#9d3d31;--ed-line:#b1a999;--ed-soft:#d4cec1}
#sheld{background:var(--ed-paper)!important;box-shadow:none!important;backdrop-filter:none!important}
#chat{position:relative;isolation:isolate;container-type:inline-size;padding:20px 12px 24px!important;gap:0!important;background:var(--ed-paper)!important;color:var(--ed-ink)!important}
#chat::before{content:var(--ed-title);display:block;flex:none;width:100%;box-sizing:border-box;white-space:pre-line;font:600 clamp(23px,4.8vw,44px)/1.2 Georgia,'Noto Serif CJK SC',serif;letter-spacing:.08em;color:var(--ed-ink);padding:12px 12px 90px;margin-bottom:18px;background:var(--ed-header) center bottom / 100% auto no-repeat;pointer-events:none}
#chat .mes{position:relative!important;isolation:isolate;box-sizing:border-box!important;width:100%!important;min-width:0!important;max-width:none!important;overflow:visible!important;flex:none!important;color:var(--ed-ink)!important;box-shadow:none!important;backdrop-filter:none!important;text-shadow:none!important}
#chat .mes :is(.mes_block,.mesAvatarWrapper,.ch_name,.flex1,.alignItemsBaseline){min-width:0;box-sizing:border-box}
#chat .mes>.mesAvatarWrapper{position:relative!important;align-self:start;min-width:0!important;max-width:100%!important;margin:0!important;gap:0!important}
#chat .mes .avatar{position:relative!important;box-sizing:border-box;max-width:100%!important;flex:none!important;margin:0!important;overflow:hidden;box-shadow:none!important}
#chat .mes .avatar img{width:100%!important;height:100%!important;object-fit:cover;box-shadow:none!important}
#chat .mes :is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay){position:static!important;display:block;max-width:100%;width:auto!important;margin:0!important;white-space:normal;overflow-wrap:anywhere;opacity:1!important;font:11px/1.6 Georgia,serif!important;color:var(--ed-ink)!important}
#chat .mes .mes_block{position:relative!important;flex:none!important;width:auto!important;max-width:100%!important;margin:0!important;min-width:0!important;overflow:visible!important}
#chat .mes .ch_name{display:flex!important;position:relative!important;align-items:flex-start!important;justify-content:space-between!important;gap:8px;margin:0!important;min-width:0!important;background:none!important}
#chat .mes .ch_name>.flex1{min-width:0;flex:1 1 auto!important}
#chat .mes .name_text{font:600 clamp(19px,3.4vw,29px)/1.4 Georgia,'Noto Serif CJK SC',serif!important;color:var(--ed-ink)!important;white-space:normal;overflow-wrap:anywhere}
#chat .mes .timestamp{font:10px/1.5 Georgia,serif;color:var(--ed-accent);margin-left:6px}
#chat .mes .mes_buttons{position:relative!important;inset:auto!important;align-items:center;justify-content:center;gap:5px;flex-wrap:wrap;max-width:100%;box-sizing:border-box;overflow:visible!important;transition:none!important;background:transparent;border:0;box-shadow:none}
#chat .mes .mes_button{box-sizing:border-box;align-items:center;justify-content:center;flex:0 0 auto;line-height:18px;text-align:center;min-width:28px;min-height:28px;padding:5px!important;border:1px solid var(--ed-line);border-radius:50%;font-size:13px;color:var(--ed-ink)!important;opacity:1;filter:none!important;transition:none!important;cursor:pointer;background:var(--ed-paper)}
#chat .mes .mes_button:hover{color:var(--ed-accent)!important;border-color:var(--ed-accent)}
#chat .mes .extraMesButtons{position:static!important;transform:none!important;flex:1 0 100%;gap:5px;flex-wrap:wrap;max-width:100%;padding:6px;background:var(--ed-tint);border:1px solid var(--ed-line);z-index:5}
#chat .mes .mes_text{position:relative;min-width:0;max-width:100%;width:100%!important;box-sizing:border-box;padding:14px 0 15px!important;margin:0!important;font-family:Georgia,'Noto Serif CJK SC','Songti SC',serif;line-height:1.95;font-size:clamp(16px,2.4vw,22px);overflow-wrap:anywhere;background:none!important;color:var(--ed-ink)!important}
#chat .mes .mes_text p{margin:.45em 0 1em;line-height:inherit}
#chat .mes .mes_text :is(img,video){max-width:100%;height:auto}
#chat .mes .mes_text :is(pre,table){max-width:100%;overflow:auto}
#chat .mes .mes_text blockquote{margin:12px 0;padding:6px 12px;border-left:3px solid var(--ed-accent);background:var(--ed-tint)}
#chat .mes .mes_reasoning_details{position:relative;box-sizing:border-box;min-width:0;max-width:100%;margin:16px 0 8px;padding:10px 14px;background:var(--ed-tint);border:1px solid var(--ed-line);border-radius:0 9px 0 2px;color:var(--ed-ink)}
#chat .mes .mes_reasoning_summary{display:flex;align-items:center;gap:6px;min-height:30px;cursor:pointer;color:var(--ed-ink)}
#chat .mes .mes_reasoning_header_block{min-width:0;flex:1}
#chat .mes .mes_reasoning_header{display:flex;gap:8px;align-items:center;background:transparent;border:0;padding:0;color:var(--ed-ink);font-size:14px}
#chat .mes .mes_reasoning{box-sizing:border-box;max-height:min(240px,32dvh);overflow:auto;overscroll-behavior:contain;margin:6px 0 0;padding:4px 0;font-size:.9em;line-height:1.8;color:var(--ed-ink);background:none}
#chat .mes .reasoning_edit_textarea{width:100%;max-height:240px;overflow:auto;background:var(--ed-paper);color:var(--ed-ink)}
#chat .mes :is(.swipe_left,.swipe_right){position:absolute;bottom:9px;z-index:4;color:var(--ed-accent);padding:8px;cursor:pointer}
#chat .mes .swipe_left{left:10px}#chat .mes .swipe_right{right:10px}
#chat .mes .swipes-counter{font-size:11px;color:var(--ed-ink)}
#top-bar{height:58px!important;min-height:58px!important;background:var(--ed-paper)!important;border:0!important;border-bottom:1px solid var(--ed-line)!important;box-shadow:none!important;backdrop-filter:none!important}
#top-settings-holder{height:100%;align-items:center!important;padding:0 7px!important;gap:3px!important}
#top-settings-holder>.drawer{flex:1 1 0!important;min-width:0!important}
#top-settings-holder .drawer-toggle{display:flex;align-items:center;justify-content:center;min-height:44px}
#top-settings-holder .drawer-icon{display:flex!important;align-items:center;justify-content:center;box-sizing:border-box;width:34px!important;height:34px!important;min-width:0!important;flex:none!important;font-size:19px!important;line-height:1!important;border:1px solid var(--ed-line);border-radius:50%;background:var(--ed-tint)!important;color:var(--ed-ink)!important;opacity:1!important;text-shadow:none!important;box-shadow:none!important}
#top-settings-holder .drawer-icon:hover{border-color:var(--ed-accent);color:var(--ed-accent)!important}
#send_form{position:relative;box-sizing:border-box;gap:5px!important;align-items:center!important;background:var(--ed-paper)!important;color:var(--ed-ink)!important;border:1px solid var(--ed-line)!important;outline:1px solid var(--ed-soft);outline-offset:-5px;border-radius:3px!important;padding:10px 12px!important;box-shadow:none!important;backdrop-filter:none!important;min-height:68px!important}
#send_textarea{min-width:0!important;box-sizing:border-box;font-family:Georgia,'Noto Serif CJK SC',serif!important;font-size:17px!important;line-height:1.6!important;color:var(--ed-ink)!important;background:transparent!important;border:0!important;box-shadow:none!important}
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but){flex:none;align-self:center;box-sizing:border-box;width:30px;min-width:25px;min-height:34px;color:var(--ed-ink)!important;opacity:1!important;background:none;text-shadow:none;font-size:20px}
#send_form #send_but{background:var(--ed-accent)!important;color:var(--ed-paper)!important;border-radius:50%;padding:8px;min-width:36px;min-height:36px;font-size:17px}
.fillLeft,.fillRight,.drawer-content,.popup{background:var(--ed-paper)!important;color:var(--ed-ink)!important;border-color:var(--ed-line)!important;box-shadow:none!important;backdrop-filter:none!important}
.drawer-content :is(input,select,textarea),.popup :is(input,select,textarea){background:var(--ed-tint);color:var(--ed-ink);border-color:var(--ed-line)}
.drawer-content :is(.inline-drawer-header,.menu_button),.popup .menu_button{background:var(--ed-tint);color:var(--ed-ink);border-color:var(--ed-line)}
#chat .mes .edit_textarea{width:100%;max-width:100%;box-sizing:border-box;color:var(--ed-ink);background:var(--ed-paper)}
@media(max-width:420px){#top-settings-holder .drawer-icon{width:29px!important;height:29px!important;font-size:16px!important}#send_form{padding:9px 7px!important;gap:3px!important}#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue){width:25px;min-width:22px;font-size:17px}}
'''
night=r'''
:root{--ed-title:"NIGHT LOG\A 夜航档案";--ed-header:url('@ASSET@harbor.webp')}
#chat{padding-top:14px!important;background-color:#e9e5dc!important;background-image:repeating-linear-gradient(0deg,#24344604 0 1px,transparent 1px 4px)!important}
#chat::before{padding-left:31%;padding-bottom:clamp(95px,23vw,180px);background-size:100% auto}
#chat .mes{display:grid!important;grid-template-columns:minmax(82px,28%) minmax(0,1fr)!important;column-gap:clamp(12px,3vw,28px);margin:0 0 26px!important;padding:20px 16px 66px!important;border:0!important;border-top:1px solid var(--ed-line)!important;border-radius:0!important;background:linear-gradient(90deg,#ded9ce 0 28%,#f3eee3 28% 100%)!important}
#chat .mes::before{content:"";position:absolute;left:5px;top:22px;bottom:64px;width:5px;background:radial-gradient(circle at center,#233443 0 2px,transparent 2.5px) center top/5px 25px repeat-y;pointer-events:none}
#chat .mes::after{content:"";position:absolute;right:24px;bottom:0;width:min(70%,410px);height:68px;background:url('@ASSET@footer.webp') right bottom/contain no-repeat;pointer-events:none}
#chat .mes>.mesAvatarWrapper{display:flex!important;flex-direction:column!important;width:100%!important;padding:0 5px!important;border-right:1px solid #aaa392;gap:0!important}
#chat .mes .avatar{width:100%!important;height:auto!important;aspect-ratio:3/4;border:5px solid #f8f5eb;border-radius:1px!important;outline:1px solid #aaa392;transform:rotate(-2deg);margin:0 0 18px!important}
#chat .mes .avatar img{border-radius:0!important}
#chat .mes .mesIDDisplay,#chat .mes .mes_timer,#chat .mes .tokenCounterDisplay{border-top:1px solid #b9b2a3;padding:8px 3px!important;line-height:1.4!important;font-size:12px!important}
#chat .mes .mesIDDisplay::after{content:"\A 档案条目";white-space:pre;font-size:9px;letter-spacing:.08em;color:#6c706e}
#chat .mes .mes_timer::after{content:"\A 回复用时";white-space:pre;font-size:9px;letter-spacing:.08em;color:#6c706e}
#chat .mes .tokenCounterDisplay::after{content:"\A TOKENS";white-space:pre;font-size:9px;letter-spacing:.08em;color:#6c706e}
#chat .mes>.mes_block{padding:0 0 0 33px!important}
#chat .mes .ch_name{border-bottom:1px solid var(--ed-accent);padding:0 0 8px!important;min-height:36px}
#chat .mes .mes_buttons{position:absolute!important;left:-37px!important;top:45px!important;right:auto!important;bottom:auto!important;width:30px;flex-direction:column;padding:0;z-index:4}
#chat .mes .extraMesButtons{position:relative!important;left:0;width:190px;max-width:min(190px,60vw);flex:none;align-self:flex-start}
#chat .mes[is_user="true"]{grid-template-columns:65px minmax(0,1fr)!important;margin-left:7%!important;width:93%!important;background:#e0e7eb!important;border:1px solid #b9c1c4!important;padding:18px 14px 48px!important}
#chat .mes[is_user="true"]>.mesAvatarWrapper{border:0;padding:0!important}
#chat .mes[is_user="true"] .avatar{aspect-ratio:3/4;border:4px solid #fffdf3}
#chat .mes[is_user="true"]>.mes_block{padding-left:0!important}
#chat .mes[is_user="true"] .mes_buttons{position:relative!important;inset:auto!important;flex-direction:row;width:auto;max-width:100%;margin-top:7px}
#chat .mes[is_user="true"] .ch_name{flex-wrap:wrap}
#chat .mes[is_user="true"]::after{width:90px;height:35px}
#chat .mes[is_user="true"]::before{display:none}
#chat .mes .mes_reasoning_details::before{content:"";position:absolute;top:-8px;right:14px;width:38px;height:15px;background:#bdb6a670;transform:rotate(4deg);pointer-events:none}
#top-settings-holder .drawer-icon{background:#253343!important;color:#f3eee3!important;outline:1px solid #253343;outline-offset:2px;border-color:#eee8db}
#send_form{border-left:5px solid var(--ed-accent)!important}
@media(max-width:440px){#chat{padding-inline:8px!important}#chat .mes{padding:14px 9px 58px!important;column-gap:10px;grid-template-columns:83px minmax(0,1fr)!important}#chat .mes>.mes_block{padding-left:27px!important}#chat .mes .mes_buttons{left:-31px!important;width:26px}#chat .mes .mes_button{min-width:25px;min-height:25px;padding:4px!important;font-size:11px}#chat .mes .name_text{font-size:20px!important}#chat .mes .mes_text{font-size:16px}#chat .mes[is_user="true"]{grid-template-columns:50px minmax(0,1fr)!important}#chat .mes[is_user="true"]>.mes_block{padding-left:0!important}}
'''
orange=r'''
:root{--ed-ink:#30433b;--ed-paper:#fff7e6;--ed-tint:#e0e8cf;--ed-accent:#df772e;--ed-line:#a7ad8b;--ed-soft:#d4d6b4;--ed-title:"ORANGE SODA\A 橘子汽水";--ed-header:url('@ASSET@bottle.webp')}
#chat{background-color:#f7edd8!important;background-image:radial-gradient(#c9a67b30 .7px,transparent .8px)!important;background-size:6px 6px!important}
#chat::before{font-weight:600;letter-spacing:.04em;padding:26px 30% 30px 16px;min-height:130px;background-position:right 16px center;background-size:auto 125px;border-bottom:1px dashed #bc9c72;margin-bottom:24px}
#chat .mes{display:grid!important;grid-template-columns:96px minmax(0,1fr)!important;gap:0 15px;margin:0 0 30px!important;padding:22px 20px 110px 50px!important;border:0!important;border-bottom:2px dashed #e3c79e!important;border-radius:0!important;background:#fff9eb!important;outline:0;box-shadow:3px 4px 0 #d5bf9525!important}
#chat .mes::before{content:"";position:absolute;top:-9px;left:22%;width:62px;height:20px;transform:rotate(-4deg);background:repeating-linear-gradient(90deg,#93ad8a80 0 6px,#e7edcfb0 6px 12px);border:1px solid #b0bd8b50;pointer-events:none}
#chat .mes::after{content:"";position:absolute;left:15px;bottom:5px;width:min(75%,350px);height:100px;background:url('@ASSET@footer.webp') left bottom/contain no-repeat;pointer-events:none}
#chat .mes>.mesAvatarWrapper{grid-column:1;grid-row:1;display:flex!important;flex-direction:column;align-items:center;gap:3px!important;width:100%!important;padding:0!important}
#chat .mes .avatar{width:82px!important;height:82px!important;aspect-ratio:1;border:3px solid #fff8e7;outline:1px solid #8d9e7b;outline-offset:3px;border-radius:50%!important;margin:0 0 10px!important}
#chat .mes .avatar img{border-radius:50%!important}
#chat .mes :is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay){font-size:10px!important;background:#ecedd6;border:1px solid #c6ccb2;border-radius:12px;padding:2px 8px!important}
#chat .mes>.mes_block{display:contents!important}
#chat .mes .ch_name{grid-column:2;grid-row:1;padding:8px 0 0!important;min-height:148px;border:0;align-self:start}
#chat .mes .name_text{font-size:clamp(25px,5vw,42px)!important;letter-spacing:.04em;border-bottom:3px solid #efa660;padding-bottom:6px;display:inline-block}
#chat .mes .ch_name::after{content:"";position:absolute;right:0;bottom:3px;width:74px;height:90px;background:url('@ASSET@bottle.webp') right bottom/contain no-repeat;pointer-events:none}
#chat .mes .mes_buttons{position:absolute!important;left:calc(-96px - 15px - 42px)!important;top:12px!important;bottom:auto!important;right:auto!important;flex-direction:column;width:30px;padding:5px 2px;border:1px dashed #cda96c;background:#ffe5b6;z-index:5;border-radius:2px}
#chat .mes .mes_button{border:0;background:none;border-radius:3px;color:#394b39!important}
#chat .mes .extraMesButtons{width:190px;max-width:min(190px,70vw);flex:none;align-self:flex-start;position:relative!important;background:#ecedd6}
#chat .mes .mes_text{grid-column:1/-1;padding-top:20px!important;padding-bottom:10px!important;min-height:100px}
#chat .mes .mes_reasoning_details{grid-column:1/-1;margin:20px 0 0 20px!important;background:#e2ebd3;border:1px solid #a2b28e;align-self:start}
#chat .mes .mes_reasoning_details::before{content:"";position:absolute;top:-7px;left:30%;width:44px;height:14px;background:repeating-linear-gradient(90deg,#90a88880 0 5px,#e5ebc980 5px 10px);transform:rotate(3deg);pointer-events:none}
#chat .mes[is_user="true"]{margin-left:7%!important;width:93%!important;background:#ffe6bd!important;outline-color:#f7d7a3;padding-bottom:52px!important}
#chat .mes[is_user="true"]::after{display:none}
#chat .mes[is_user="true"]::before{background:repeating-linear-gradient(90deg,#f5a15180 0 5px,#ffe9bd80 5px 10px);left:auto;right:22%}
#chat .mes[is_user="true"] .ch_name::after{display:none}
#chat .mes[is_user="true"] .name_text{font-size:24px!important}
#chat .mes[is_user="true"] .ch_name{min-height:110px}
#chat .mes[is_user="true"] :is(.mes_timer,.tokenCounterDisplay){display:none}
#send_form{background:#e3ecd4!important;border:1px solid #96aa82!important;border-radius:17px 17px 7px 7px!important;outline-color:#adbf9b}
#top-settings-holder .drawer-icon{background:#e1e8cd!important;border-color:#91a380;color:#30433b!important}
#top-settings-holder>.drawer:nth-child(3n+1) .drawer-icon{background:#ffe2b8!important;border-color:#e8ba78}
@media(max-width:440px){#chat{padding-inline:10px!important}#chat .mes{grid-template-columns:72px minmax(0,1fr)!important;column-gap:12px;padding:18px 14px 95px 43px!important}#chat .mes .avatar{width:62px!important;height:62px!important}#chat .mes .mes_buttons{left:calc(-72px - 12px - 37px)!important;width:28px}#chat .mes .mes_button{min-width:25px;min-height:25px;font-size:12px}#chat .mes .ch_name::after{height:70px;width:60px}#chat .mes .name_text{font-size:29px!important}#chat .mes .ch_name{min-height:135px}#chat .mes .mes_reasoning_details{margin-left:6px!important}#chat .mes .mes_text{font-size:17px}#chat .mes::after{height:90px}}
'''
for key,stem,title,part in [('night-log','Night-Log','夜航档案',night),('orange-soda','Orange-Soda','橘子汽水',orange)]:
 css=common+part.replace('@ASSET@',BASE+'assets/'+key+'-v1/')
 (R/'theme'/f'{key}.css').write_text(css)
 cfg=json.loads((R/'theme/Rose-Moon-Phases.json').read_text())
 cfg.update(name=title,custom_css=css,main_text_color='rgba(37, 51, 67, 1)' if key=='night-log' else 'rgba(48, 67, 59, 1)',italics_text_color='rgba(125, 99, 74, 1)',quote_text_color='rgba(137, 70, 44, 1)',blur_tint_color='rgba(245, 240, 228, 1)',chat_tint_color='rgba(245, 240, 228, 1)',border_color='rgba(175, 168, 145, 1)',avatar_style=0,chat_display=0,blur_strength=0,shadow_width=0,noShadows=True,reduced_motion=True)
 (R/'theme'/f'{stem}.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
 print(stem,len(css),len(json.dumps(cfg,ensure_ascii=False)))
# External, tiny vector navigation assets. Semantic native buttons stay in place.
nav=[('#leftNavDrawerIcon','sliders'),('#API-status-top','plug'),('#advanced-formatting-button .drawer-icon','quill'),('#WIDrawerIcon','book'),('#user-settings-button .drawer-icon','gear'),('#backgrounds-button .drawer-icon','image'),('#extensions-settings-button .drawer-icon','puzzle'),('#persona-management-button .drawer-icon','person'),('#rightNavDrawerIcon','cards')]
for key,stem in [('night-log','Night-Log'),('orange-soda','Orange-Soda')]:
 p=R/'theme'/f'{key}.css';s=p.read_text()
 s+='\n/* Keep icon shapes at their original aspect ratio, including native glyph replacements. */\n'
 for sel,icon in nav:
  s+=f"#top-settings-holder {sel}::before{{content:''!important;display:block;width:20px;height:20px;flex:none;background:currentColor;mask:url('{BASE}assets/editorial-icons/{icon}.svg') center/contain no-repeat;-webkit-mask:url('{BASE}assets/editorial-icons/{icon}.svg') center/contain no-repeat;}}\n"
 for sel,icon in [('options_button','book'),('extensionsMenuButton','puzzle'),('mes_impersonate','person'),('mes_continue','continue'),('send_but','send')]:
  s+=f"#send_form #{sel}::before{{content:''!important;display:block;width:20px;height:20px;margin:auto;background:currentColor;mask:url('{BASE}assets/editorial-icons/{icon}.svg') center/contain no-repeat;-webkit-mask:url('{BASE}assets/editorial-icons/{icon}.svg') center/contain no-repeat;}}\n"
 s+='\n#chat .mes :is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay):empty{display:none!important}\n'
 s+='\n#chat .mes .mes_reasoning p{margin:.3em 0;font-size:inherit;line-height:1.8}\n'
 s+='\n#chat .mes .swipe_left,#chat .mes .swipe_right{background:var(--ed-paper);border:1px solid var(--ed-line);border-radius:16px;min-height:26px;bottom:4px;padding:3px 9px}\n'
 p.write_text(s);q=R/'theme'/f'{stem}.json';cfg=json.loads(q.read_text());cfg['custom_css']=s;q.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
