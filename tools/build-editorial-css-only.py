from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1]
B='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/editorial-faithful/'
# Use the native last character message as the shared portrait; never clone DOM.
last='#chat>.mes[is_user="false"]:not([is_system="true"]):not(:has(~.mes[is_user="false"]:not([is_system="true"])))'
common=r'''
:root{--ed-layout:none!important}
#ed-chrome{display:none!important;pointer-events:none!important}
body,#sheld,#chat,#chat>.mes,#chat>.mes>.mes_block{transform:none!important;filter:none!important;perspective:none!important;backdrop-filter:none!important;contain:none!important}
#chat>.mes{isolation:auto!important}
#top-bar{z-index:40!important;pointer-events:none}
#top-settings-holder{position:fixed!important;z-index:50!important;margin:0!important;transform:none!important;box-sizing:border-box!important;max-width:none!important;min-height:0!important;background:none!important}
#top-settings-holder>.drawer{display:block!important}
#top-settings-holder .drawer-content{top:var(--heading)!important;bottom:auto!important;min-height:0!important;max-height:calc(100dvh - var(--heading))!important;overflow:auto}
#sheld::before{content:'';position:fixed;z-index:30;pointer-events:none;background-position:left top;background-size:100% auto;background-repeat:no-repeat}
#sheld{overflow:visible!important}
#chat{flex:1 1 0!important;min-height:0!important;height:auto!important;isolation:auto!important}
#chat>.mes>.mes_block{width:auto!important;max-width:none!important;min-width:0!important;flex:none!important;background:none!important}
#chat>.mes .ch_name{height:0!important;min-height:0!important;grid-column:1/-1;grid-row:1;pointer-events:none}
#chat>.mes .ch_name>*{pointer-events:auto}
#chat>.mes .mes_reasoning_summary{display:flex!important;flex-wrap:wrap!important;gap:3px!important;margin:0!important;min-width:0!important}
#chat>.mes .mes_reasoning_header_block{flex:1 1 100%!important;min-width:0!important}
#chat>.mes .mes_reasoning_actions{flex-wrap:wrap;gap:3px}
#chat>.mes .mes_reasoning_actions .mes_button{min-width:14px!important;min-height:14px!important;line-height:14px!important;font-size:12px!important}
#chat>.mes .mes_reasoning{padding:0!important;margin-top:6px!important;border:0!important}
#chat>.mes .mes_reasoning_header{padding:0!important;margin:0!important;min-width:0!important;font-size:inherit!important}
#chat>.mes .mes_text{min-height:0!important;height:auto!important}
#chat>.mes .mes_buttons{height:auto!important;max-height:none!important}
#chat>.mes .mes_media_wrapper,#chat>.mes .mes_file_wrapper,#chat>.mes .mes_bias{grid-column:1/-1;max-width:100%;min-width:0}
#chat>.mes>.swipeRightBlock{position:absolute!important;bottom:6px!important;right:8px!important;top:auto!important;transform:none!important;z-index:4}
#chat>.mes>.swipeRightBlock .swipe_right{position:static!important}
#chat>.mes .mes_edit_buttons{position:relative!important;z-index:10;flex-wrap:wrap;background:var(--paper)}
#chat>.mes:has(.edit_textarea) .ch_name{height:auto!important}
#chat>.mes:has(.edit_textarea) .mes_block{display:block!important;padding:12px!important}
#form_sheld{position:relative!important;flex:0 0 auto!important;height:auto!important;min-height:0!important;max-height:40dvh!important;overflow:auto!important;background:var(--paper)}
#send_form{min-height:var(--composer)!important;height:auto!important;display:flex!important;flex-direction:column!important;padding:0!important;overflow:visible!important}
#nonQRFormItems{position:relative!important;display:flex!important;align-items:center!important;gap:8px!important;width:100%!important;min-height:var(--composer)!important;padding:var(--input-pad)!important;box-sizing:border-box}
#leftSendForm,#rightSendForm{position:static!important;display:flex!important;flex:0 0 auto!important;align-items:center!important;width:auto!important;min-width:0!important;max-width:25%;gap:6px;flex-wrap:wrap}
#send_textarea{position:static!important;inset:auto!important;flex:1 1 0!important;width:0!important;min-width:0!important;height:48px!important;min-height:38px!important;max-height:26dvh!important;margin:0!important;padding:4px!important;font-size:16px!important;line-height:1.5!important;resize:vertical!important}
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but,#mes_stop){position:static!important;inset:auto!important;width:26px!important;height:32px!important;min-width:26px!important;min-height:32px!important;line-height:32px!important;font-size:23px!important;padding:0!important}
#send_form #send_but{color:var(--accent)!important}
#send_form #options_button::after,#send_form #extensionsMenuButton::after,#send_form #mes_continue::after,#send_form #mes_impersonate::after{content:none!important}
#send_form :is(#options_button,#extensionsMenuButton,#mes_impersonate,#mes_continue,#send_but)::before{width:24px!important;height:24px!important}
LAST>.mesAvatarWrapper{position:fixed!important;display:block!important;z-index:32!important;margin:0!important;padding:0!important;pointer-events:none;max-width:none!important;border:0!important}
LAST>.mesAvatarWrapper>.avatar{position:absolute!important;display:block!important;margin:0!important;padding:0!important;border:0!important;pointer-events:auto}
LAST>.mesAvatarWrapper>.avatar img{object-fit:cover!important;aspect-ratio:auto!important;border-radius:inherit!important}
LAST :is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay){display:block!important;position:absolute!important;z-index:33;left:auto;top:auto;margin:0!important;padding:0!important;line-height:1.3!important;pointer-events:none;text-align:center!important}
LAST .name_text{position:fixed!important;z-index:33!important;pointer-events:none;margin:0!important;overflow-wrap:anywhere}
'''
orange=r'''
:root{--composer:clamp(86px,25vw,256px);--input-pad:clamp(10px,4vw,40px) 8% clamp(10px,6vw,60px) 13%}
#sheld::before{left:0;top:0;width:100%;height:calc(267 * var(--u));background-image:url('BASEheader.webp')}
#top-settings-holder{left:0!important;right:0!important;top:calc(267 * var(--u))!important;width:100%!important;height:calc(117 * var(--u))!important}
#chat>.mes{background:url('BASEmessage.webp') left top/100% auto no-repeat,var(--paper)!important;min-height:calc(510 * var(--u));display:grid!important;grid-template-columns:62% 38%!important}
#chat>.mes .mes_reasoning_details{max-height:calc(190 * var(--u))!important;overflow:auto!important;grid-column:2!important;grid-row:1!important;background:none!important;border:0!important;padding:0!important}
#chat>.mes .mes_text{grid-column:1!important;grid-row:1!important}
#chat>.mes[is_user="true"]{display:block!important;background:url('BASEreply.webp') left top/100% auto no-repeat,var(--paper)!important}
LAST>.mesAvatarWrapper{top:0!important;left:0!important;right:auto!important;width:100vw!important;height:calc(267 * var(--u))!important;background:none!important}
LAST>.mesAvatarWrapper>.avatar{left:4.4%!important;top:8.6%!important;width:22.9%!important;height:86.5%!important;border-radius:50%!important}
LAST .name_text{left:30%!important;top:calc(49 * var(--u))!important;width:22%!important;font-size:calc(60 * var(--u))!important;line-height:1.2!important}
LAST .mesIDDisplay{left:53.5%!important;top:24%!important;width:11%!important;font-size:calc(22 * var(--u))!important}
LAST .mes_timer{left:53.5%!important;top:42%!important;width:11%!important;font-size:calc(22 * var(--u))!important}
LAST .tokenCounterDisplay{left:53.5%!important;top:60%!important;width:11%!important;font-size:calc(22 * var(--u))!important}
'''
night=r'''
:root{--composer:clamp(74px,11vw,111px);--input-pad:10px 4%;}
#sheld::before{left:calc(355 * var(--u));top:0;width:calc(669 * var(--u));height:calc(326 * var(--u));background-image:url('BASEmasthead-type.webp'),url('BASEheader.webp')}
#top-settings-holder{left:calc(355 * var(--u))!important;right:0!important;top:calc(137 * var(--u))!important;width:calc(669 * var(--u))!important;height:calc(90 * var(--u))!important}
#chat>.mes{background:url('BASEmessage.webp') left top/100% auto no-repeat,var(--paper)!important}
#chat>.mes[is_user="false"]:nth-child(even){background:url('BASEnote.webp') left top/100% auto no-repeat,var(--paper)!important}
#chat>.mes[is_user="true"]{background:url('BASEreply.webp') left top/100% auto no-repeat,#cdd6e0!important}
LAST>.mesAvatarWrapper{left:0!important;top:0!important;width:calc(355 * var(--u))!important;height:calc(100dvh - var(--composer))!important;background:#1b2937 url('BASEsidebar.webp') left top/100% auto no-repeat!important}
LAST>.mesAvatarWrapper>.avatar{left:22%!important;top:calc(49 * var(--u))!important;width:68%!important;height:calc(771 * var(--u))!important;border-radius:0!important}
LAST>.mesAvatarWrapper>.avatar::after{content:'';position:absolute;inset:0;background:linear-gradient(168deg,transparent 39%,#e8e1d3 39.3%,#e8e1d3 40%,transparent 40.3%,transparent 69%,#e8e1d3 69.3%,#e8e1d3 70%,transparent 70.3%);pointer-events:none}
LAST .name_text{left:calc(90 * var(--u))!important;top:calc(830 * var(--u))!important;width:calc(230 * var(--u))!important;font-size:calc(45 * var(--u))!important;line-height:1.2!important}
LAST .mesIDDisplay{left:26%!important;top:calc(960 * var(--u))!important;width:60%!important;font-size:calc(24 * var(--u))!important}
LAST .mes_timer{left:26%!important;top:calc(1010 * var(--u))!important;width:60%!important;font-size:calc(24 * var(--u))!important}
LAST .tokenCounterDisplay{left:26%!important;top:calc(1060 * var(--u))!important;width:60%!important;font-size:calc(24 * var(--u))!important}
LAST .ch_name>.flex1{display:block!important}
LAST.reasoning .mes_reasoning_details[data-has-content="true"]{display:block!important}
LAST .mes_reasoning_details{position:fixed!important;z-index:33!important;left:calc(73 * var(--u))!important;top:calc(1150 * var(--u))!important;width:calc(245 * var(--u))!important;max-height:min(calc(245 * var(--u)),calc(100dvh - var(--composer) - 1150 * var(--u)))!important;overflow:auto!important;margin:0!important;padding:0!important;background:none!important;border:0!important}
'''
for stem,key,extra,label in [('Orange-Soda','orange',orange,'橘子汽水'),('Night-Log','night',night,'夜航档案')]:
 s=(R/'theme'/f'{stem}-Faithful.css').read_text()
 # Drop adapter-only visual rules; all remaining native rules retain original artwork.
 s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
 s=re.sub(r'([^{}]+)\{([^{}]*)\}',lambda m:'' if ('.ed-' in m[1] or '#ed-chrome' in m[1] or 'body:not([data-ed-layout])' in m[1]) else m[0],s)
 s=s.replace('body[data-ed-layout="'+key+'"]','body').replace('body[data-ed-layout]','body')
 s += '\n'+(common+extra).replace('LAST',last).replace('BASE',B+key+'/')
 j=json.loads((R/'theme'/f'{stem}-Faithful.json').read_text());j['name']=label+'·纯CSS修复';j['custom_css']=s;j['compact_input_area']=False
 (R/'theme'/f'{stem}-CSS-Only.css').write_text(s)
 (R/'theme'/f'{stem}-CSS-Only.json').write_text(json.dumps(j,ensure_ascii=False,indent=2))
