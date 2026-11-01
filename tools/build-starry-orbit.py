"""Starry asymmetrical layout. Artwork is external; role images stay native."""
from pathlib import Path
import json,runpy,re
R=Path(__file__).resolve().parents[1]
BASE='https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/'
ART=BASE+'assets/starry-orbit/'
OLD=BASE+'assets/poetic-v3/starry/'
common=runpy.run_path(str(R/'tools/build-poetic-restored.py'))['COMMON']
css=common.replace('INK','#eef2ff').replace('BASECOLOR','#071b36').replace('URL',OLD)
css+='''
/* Asymmetric constellation header, open name, full-width message. */
*,*::before,*::after{scrollbar-width:none!important;scrollbar-gutter:auto!important;}
*::-webkit-scrollbar,*::-webkit-scrollbar-track,*::-webkit-scrollbar-thumb,*::-webkit-scrollbar-corner{display:none!important;width:0!important;height:0!important;}
#sheld,#chat{background:#071b36!important;border:0!important;padding-inline:0!important;}
#chat{width:100%!important;}
#chat .mes{grid-template-columns:minmax(0,46%) minmax(0,1fr)!important;gap:0 10px!important;padding:24px 6px clamp(100px,28vw,180px)!important;margin:0 auto 12px!important;background:#071b36!important;overflow:visible!important;}
#chat .mes>.mes_block,#chat .mes .ch_name{display:contents!important;}
#chat .mes>.mes_block::before,#chat .mes>.mes_block::after,#chat .mes::before{content:none!important;}
#chat .mes::after{left:0;right:0;bottom:0;height:clamp(110px,31vw,200px);background:url('SEA') center bottom/100% auto no-repeat;mask-image:linear-gradient(transparent,#000 42%);z-index:-1!important;}
#chat .mes .mesAvatarWrapper{grid-column:1!important;grid-row:1!important;align-self:center!important;width:100%!important;gap:4px 2px!important;padding:0!important;}
#chat .mes .avatar{aspect-ratio:1!important;border-radius:50%!important;overflow:visible!important;}
#chat .mes .avatar img{position:absolute!important;left:14%!important;top:14%!important;width:72%!important;height:72%!important;clip-path:circle(50%)!important;object-fit:cover!important;object-position:center 30%!important;border-radius:50%!important;}
#chat .mes .avatar::after{content:'';position:absolute;inset:-2%;pointer-events:none;background:none;}
#chat .mes .ch_name>.flex1{grid-column:2!important;grid-row:1!important;align-self:center!important;display:flex!important;flex-direction:column!important;align-items:flex-start!important;justify-content:center!important;gap:10px!important;width:100%!important;min-height:0!important;padding:0 8px 8px 0!important;background:none!important;text-align:left!important;}
#chat .mes .ch_name>.flex1::after{content:'';width:44px;height:20px;background:url('ART0.webp') center/contain no-repeat;pointer-events:none;}
#chat .mes .name_text{font-size:clamp(20px,5.8vw,31px)!important;line-height:1.45!important;font-weight:400!important;letter-spacing:.04em;text-align:left!important;overflow-wrap:anywhere;}
#chat .mes .timestamp{display:block;font-size:9px!important;opacity:.6;}
#chat .mes .mesIDDisplay,#chat .mes .mes_timer,#chat .mes .tokenCounterDisplay{font-size:8px!important;line-height:16px!important;opacity:.65;}
#chat .mes .mes_buttons{grid-column:1/-1!important;grid-row:2!important;box-sizing:border-box;position:relative!important;justify-self:start!important;display:flex!important;flex-wrap:wrap!important;align-items:center!important;justify-content:center!important;gap:4px!important;width:min(94%,380px)!important;max-width:100%!important;min-height:68px!important;margin:8px 0 4px!important;padding:12px 8px 16px!important;background:none!important;border:0!important;box-shadow:none!important;overflow:visible!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons){position:relative!important;inset:auto!important;box-sizing:border-box;flex:0 0 34px!important;width:34px!important;height:34px!important;min-width:34px!important;min-height:34px!important;margin:0!important;padding:0!important;border:0!important;box-shadow:none!important;background:var(--orbit-action,url('ART0.webp')) center/contain no-repeat!important;font-size:0!important;color:transparent!important;opacity:1!important;filter:none!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons)::before,#chat .mes .mes_buttons>:not(.extraMesButtons)::after{opacity:0!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons)>:is(i,span,img,svg){visibility:hidden!important;}
#chat .mes .mes_buttons>:nth-child(1),#chat .mes .mes_buttons>:nth-child(8){transform:translateY(-8px)!important;}
#chat .mes .mes_buttons>:nth-child(3),#chat .mes .mes_buttons>:nth-child(7){transform:translateY(-2px)!important;}
#chat .mes .mes_buttons>:nth-child(4),#chat .mes .mes_buttons>:nth-child(6){transform:translateY(4px)!important;}
#chat .mes .mes_buttons>:nth-child(5){transform:translateY(7px)!important;}
#chat .mes .extraMesButtons{position:absolute!important;left:8px!important;right:auto!important;top:100%!important;z-index:20;box-sizing:border-box;width:170px!important;max-width:170px!important;gap:8px!important;padding:10px!important;background:#102844!important;border:1px solid #6f849e!important;border-radius:8px;}
#chat .mes .extraMesButtons>.mes_button{color:#ecdcad!important;font-size:17px!important;min-width:28px;min-height:28px;background:none!important;}
#chat .mes .mes_text{grid-column:1/-1!important;width:100%!important;max-width:100%!important;min-height:0!important;padding:12px 0 18px!important;margin:0!important;border:0!important;background:none!important;line-height:1.9!important;}
#chat .mes .mes_text>p{margin-inline:0!important;padding-inline:0!important;text-align:justify!important;text-align-last:start!important;text-justify:inter-ideograph;}
#chat .mes>.mes_block>:not(.ch_name):not(.mes_text){grid-column:1/-1!important;box-sizing:border-box;min-width:0;max-width:100%;}
#chat .mes>.swipeRightBlock{position:absolute!important;right:8px!important;bottom:4px!important;z-index:3;}
#chat .mes .mes_edit_buttons{grid-column:1/-1;grid-row:2;}
#top-bar{background:#071b36!important;}
#send_form{background:#071b36!important;padding:12px 10px!important;}
#send_form::before{background:rgba(21,48,78,.85);border:0;border-radius:20px;}
#send_form :is(#options_button,#extensionsMenuButton,#send_but){flex:0 0 32px!important;width:32px!important;height:36px!important;min-width:32px!important;font-size:0!important;background-position:center!important;background-size:contain!important;background-repeat:no-repeat!important;}
#send_form #options_button{background-image:url('ART7.webp')!important;}
#send_form #extensionsMenuButton{background-image:url('ART8.webp')!important;}
#send_form #send_but{background-image:url('ART4.webp')!important;}
#send_form :is(#options_button,#extensionsMenuButton,#send_but)::before{opacity:0!important;}
@media(max-width:700px){#sheld{width:100%!important;max-width:100%!important;left:0!important;right:0!important;margin-inline:0!important;}#chat .mes{max-width:100%!important;}}
'''.replace('ART',ART).replace('SEA',OLD+'sea.webp')
# Keep the user's approved large portrait and its original painted frame.
css+="""
#chat .mes{grid-template-columns:minmax(0,1fr)!important;padding-top:0!important;}
#chat .mes .mesAvatarWrapper{grid-column:1!important;grid-row:1!important;gap:0!important;width:calc(100% + 12px)!important;max-width:none!important;margin-inline:-6px!important;}
#chat .mes .avatar{aspect-ratio:1.52!important;border-radius:0!important;}
#chat .mes .avatar img{position:static!important;inset:auto!important;width:100%!important;height:100%!important;clip-path:ellipse(50% 34% at 50% 49%)!important;object-position:center 35%!important;border-radius:0!important;}
#chat .mes .avatar::after{inset:0!important;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/poetic-v3/starry/hero.webp') center/contain no-repeat!important;}
#chat .mes .ch_name>.flex1{grid-column:1!important;grid-row:1!important;align-self:end!important;align-items:flex-start!important;width:94%!important;margin:0 0 28px!important;padding:0 30px 0 54px!important;z-index:4;}
#chat .mes .name_text{font-size:clamp(22px,5.8vw,31px)!important;}
#chat .mes .ch_name>.flex1::after{display:none!important;}
#chat .mes .mes_buttons{grid-column:1!important;grid-row:2!important;justify-self:end!important;margin-top:0!important;margin-bottom:0!important;min-height:58px!important;}
#chat .mes .mes_text{padding-top:4px!important;}
"""
for n,sel in {0:'.extraMesButtonsHint',1:'.mes_bookmark,.fa-flag',2:'.mes_narrate,.fa-music,.fa-bullhorn',3:'[title*="熊"],[title*="酒馆助手"],[class*="tavern_helper"]',4:'.mes_edit,.fa-pencil',5:'.mes_copy,.fa-layer-group',6:'.fa-chart-bar,.fa-chart-simple,[title*="统计"]'}.items():
 css+=f"\n#chat .mes .mes_buttons>:is({sel}){{--orbit-action:url('{ART}{n}.webp');}}"
for i in range(1,10):
 css+=f"\n#top-settings-holder>.drawer:nth-child({i}) .drawer-icon{{width:26px!important;height:30px!important;font-size:0!important;background:url('{BASE}assets/poetic-v2/starry/icon-{(i-1)%4+1}.webp') center/contain no-repeat!important;}}#top-settings-holder>.drawer:nth-child({i}) .drawer-icon::before{{opacity:0!important;}}"

# Preserve the exact portrait art; place controls inside its existing lower ribbon.
css+="""
#chat .mes{grid-template-columns:repeat(6,minmax(0,1fr))!important;gap:0!important;}
#chat .mes .mesAvatarWrapper,#chat .mes .ch_name{display:contents!important;}
#chat .mes .ch_name::before,#chat .mes .ch_name::after{content:none!important;}
#chat .mes .avatar{grid-column:1/-1!important;grid-row:1!important;width:calc(100% + 12px)!important;margin-inline:-6px!important;aspect-ratio:1.52!important;}
#chat .mes .avatar::after{pointer-events:none!important;}
#chat .mes .ch_name>.flex1{grid-column:1/4!important;grid-row:2!important;align-self:center!important;align-items:flex-start!important;justify-content:center!important;width:100%!important;margin:0!important;padding:14px 8px 12px 4px!important;text-align:left!important;background:none!important;}
#chat .mes .ch_name>.flex1::before,#chat .mes .ch_name>.flex1::after{content:none!important;}
#chat .mes .name_text{display:block!important;font-size:clamp(18px,4.7vw,25px)!important;line-height:1.4!important;text-align:left!important;text-wrap:balance;}
#chat .mes .mes_buttons{grid-column:1/-1!important;grid-row:1!important;align-self:end!important;justify-self:center!important;justify-content:center!important;align-items:center!important;gap:4px!important;width:84%!important;max-width:440px!important;min-height:0!important;margin:0 0 10px!important;padding:0!important;z-index:5!important;background:none!important;}
#chat .mes .mes_buttons>:not(.extraMesButtons){transform:none!important;flex:0 0 34px!important;width:34px!important;height:34px!important;min-width:34px!important;min-height:34px!important;background-image:var(--orbit-action,url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/painted-controls/starry/0.webp'))!important;}
#chat .mes .mesIDDisplay,#chat .mes .mes_timer,#chat .mes .tokenCounterDisplay{grid-row:2!important;align-self:center!important;justify-self:center!important;font-size:9px!important;opacity:.8!important;padding:0!important;margin:0!important;}
#chat .mes .mesIDDisplay{grid-column:4!important;}
#chat .mes .mes_timer{grid-column:5!important;}
#chat .mes .tokenCounterDisplay{grid-column:6!important;}
#chat .mes .mes_text{padding:8px 0 18px!important;}
#chat .mes .ch_name .extraMesButtons{top:100%!important;left:0!important;right:auto!important;}
@media(min-width:700px){#chat .mes .mes_buttons{margin-bottom:22px!important;gap:12px!important;}#chat .mes .mes_buttons>:not(.extraMesButtons){width:40px!important;height:40px!important;flex-basis:40px!important;}}
"""
# Use the legible matched painted controls, including a real chart symbol.
css=css.replace("assets/starry-orbit/", "assets/painted-controls/starry/").replace("assets/painted-controls/starry/header-panel.webp", "assets/starry-orbit/header-panel.webp")
theme=json.loads((R/'theme/Starry-Voyage-V3.json').read_text());theme['name']='星潮夜航';theme['custom_css']=css
out=R/'theme/starry-orbit';out.mkdir(exist_ok=True)
(out/'星潮夜航.json').write_text(json.dumps(theme,ensure_ascii=False,indent=2)+'\n')
(R/'theme/starry-orbit.css').write_text(css)
fixture=(R/'docs/starry-restored-fixture.html').read_text().replace('../theme/starry-restored.css','../theme/starry-orbit.css').replace('裴识渊','在雾钟城的黎明')
fixture=fixture.replace('<p>收到你的来信了。</p>','<p>夜色沿着海岸慢慢落下，星光随着浪花漫过窗前。</p><p>他将那封信放在你掌心，纸页还带着淡淡的花香。</p>')
(R/'docs/starry-orbit-fixture.html').write_text(fixture)
