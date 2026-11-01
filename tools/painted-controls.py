"""Layout only; every visible control face is independently generated raster art."""
def painted_controls(key, base):
 url=base+'assets/painted-controls/'+key+'/'
 css='''
/* Painted controls: no CSS-drawn borders, no native scrollbar gutters. */
:root{--scrollbar-width:0px;--scrollbarWidth:0px;}
*,*::before,*::after{scrollbar-width:none!important;scrollbar-gutter:auto!important;}
*::-webkit-scrollbar,*::-webkit-scrollbar-track,*::-webkit-scrollbar-thumb,*::-webkit-scrollbar-corner{display:none!important;width:0!important;height:0!important;border:0!important;}
#chat{width:100%!important;padding-inline:0!important;margin-inline:0!important;border-inline:0!important;}
#chat .mes .mes_text{width:100%!important;max-width:100%!important;padding-inline:8px!important;margin-inline:0!important;box-sizing:border-box!important;}
#chat .mes .mes_buttons{display:flex!important;flex-direction:row!important;flex-wrap:wrap!important;align-items:center!important;justify-content:center!important;gap:5px!important;padding:5px 0!important;border:0!important;border-radius:0!important;box-shadow:none!important;background:transparent!important;overflow:visible!important;}
#chat .mes .mes_buttons::after{display:none!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons),#chat .mes .extraMesButtons>.mes_button{box-sizing:border-box!important;flex:0 0 36px!important;width:36px!important;min-width:36px!important;max-width:36px!important;height:36px!important;min-height:36px!important;margin:0!important;padding:0!important;float:none!important;position:relative!important;inset:auto!important;transform:none!important;line-height:36px!important;text-align:center!important;border:0!important;border-radius:0!important;box-shadow:none!important;filter:none!important;text-shadow:none!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons){background:var(--painted-action,url('ART0.webp')) center/contain no-repeat!important;font-size:0!important;color:transparent!important;opacity:1!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons)::before,#chat .mes .mes_buttons>:not(.extraMesButtons)::after{opacity:0!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons)>:is(img,svg,i,span){visibility:hidden!important;}
#chat .mes .mes_buttons .extraMesButtons{position:absolute!important;top:100%!important;right:0!important;left:auto!important;width:160px!important;max-width:160px!important;flex-basis:auto!important;gap:6px!important;padding:6px!important;z-index:9;}
#send_form :is(#options_button,#extensionsMenuButton){width:36px!important;height:38px!important;min-width:36px!important;flex:0 0 36px!important;margin:0!important;padding:0!important;border:0!important;box-shadow:none!important;background-position:center!important;background-size:contain!important;background-repeat:no-repeat!important;font-size:0!important;filter:none!important;}
#send_form #options_button{background-image:url('ART7.webp')!important;}
#send_form #extensionsMenuButton{background-image:url('ART8.webp')!important;}
#send_form :is(#options_button,#extensionsMenuButton)::before,#send_form :is(#options_button,#extensionsMenuButton)::after{display:none!important;}
#send_form :is(#options_button,#extensionsMenuButton)>*{visibility:hidden!important;}
@media(max-width:700px){#sheld{width:100%!important;max-width:100%!important;left:0!important;right:0!important;margin-inline:0!important;border-inline:0!important;padding-inline:0!important;}#chat .mes{max-width:100%!important;}}
'''.replace('ART',url)
 # Match function, never DOM index: extension controls change order/count.
 mapping={0:'.extraMesButtonsHint',1:'.mes_bookmark,.mes_create_bookmark,.fa-flag',2:'.mes_narrate,.fa-music,.fa-volume-high,.fa-bullhorn',3:'[title*="熊"],[title*="酒馆助手"],[title*="Tavern Helper"],[class*="tavern_helper"]',4:'.mes_edit,.fa-pencil,.fa-pen',5:'.mes_copy,.fa-layer-group,.fa-copy',6:'.fa-chart-simple,.fa-chart-column,.fa-chart-bar,[title*="统计"],[class*="token_counter"]'}
 for n,sel in mapping.items():
  css+=f"\n#chat .mes .mes_buttons>:is({sel}){{--painted-action:url('{url}{n}.webp');}}"
 if key in ('rain','postal'):
  css+='''
#chat .mes .mes_buttons{position:relative!important;inset:auto!important;width:100%!important;min-width:0!important;max-width:100%!important;}
#chat .mes .mes_text{padding-inline:10px!important;}
'''
 if key=='rabbit':
  css+='\n#chat .mes{padding-inline:8px!important;}#chat .mes .mes_text{padding-inline:6px!important;}'
 if key=='starry':
  css+="""
#chat{background:#071b36!important;}
#chat .mes{background:#071b36!important;}
#chat .mes .ch_name,#chat .mes .mes_text{background:transparent!important;}
#chat .mes::after{mask-image:linear-gradient(transparent,#000 35%)!important;}
"""
 if key=='rain':
  css+="""
#chat{background:#eef7ff!important;}
#chat .mes{background:rgba(246,252,255,.88)!important;padding-bottom:125px!important;row-gap:16px!important;}
#chat .mes>.mes_block::before{content:'';inset:0 0 auto!important;height:auto!important;aspect-ratio:1!important;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/poetic-v3/rain/surface.webp') center top/100% auto no-repeat!important;mask-image:linear-gradient(#000 0%,rgba(0,0,0,.6) 45%,transparent 100%)!important;z-index:-2!important;}
#chat .mes .mes_text{background:none!important;border:0!important;border-radius:0!important;padding-bottom:20px!important;min-height:150px!important;}
#chat .mes .mes_text::before,#chat .mes .mes_text::after{display:none!important;}
#chat .mes::after{content:'';left:0;right:0;bottom:0;height:120px;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/poetic-v3/rain/rain-bottom.webp') center bottom/100% auto no-repeat;mask-image:linear-gradient(transparent,#000 30%);z-index:-1;}
#chat .mes .avatar{border:0!important;border-radius:4px!important;transform:rotate(-4deg)!important;}
#chat .mes .avatar img{clip-path:inset(7% round 3px)!important;}
#chat .mes .avatar::after{content:'';position:absolute;inset:0;pointer-events:none;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/painted-controls/rain/portrait.webp') center/contain no-repeat;}
#chat .mes .ch_name>.flex1{clip-path:none!important;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/painted-controls/rain/name.webp') center/contain no-repeat!important;padding:16px 5px!important;min-height:58px!important;}
#chat .mes .name_text{font-size:clamp(14px,4vw,20px)!important;line-height:1.35!important;text-align:center!important;}
#chat .mes .mesAvatarWrapper{grid-column:1/-1!important;grid-row:1!important;width:58%!important;justify-self:center!important;}
#chat .mes .ch_name{grid-column:1/-1!important;grid-row:2!important;padding-bottom:0!important;align-self:center!important;}
#top-bar,#send_form{background:#eef7ff!important;}
"""
 return css
