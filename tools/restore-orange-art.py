from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
j=json.loads((R/'theme/Orange-Message-Fix.json').read_text())
j['name']='橘子汽水·完整装饰修复'
j['custom_css']+='''
/* Restore the approved illustration; grid lives on the real message block. */
#chat>.mes[is_user]{padding:0 0 30px!important;margin:0!important;background:var(--paper)!important;border:0!important;min-height:0!important}
#chat>.mes[is_user]>.mes_block{display:grid!important;grid-template-columns:minmax(0,62%) minmax(0,38%)!important;grid-template-rows:auto auto!important;align-items:start!important;padding:calc(42 * var(--u)) 0 calc(72 * var(--u))!important;min-height:calc(510 * var(--u))!important;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/editorial-faithful/orange/message.webp') left top/100% auto no-repeat,var(--paper)!important}
#chat>.mes[is_user]>.mes_block>.ch_name{grid-column:1/-1!important;grid-row:1!important;width:auto!important;margin:0 calc(65 * var(--u)) 18px calc(260 * var(--u))!important;min-height:calc(90 * var(--u))!important}
#chat>.mes[is_user]>.mes_block>.ch_name>.mes_buttons{position:relative!important;inset:auto!important;display:flex;flex-direction:row!important;flex-wrap:wrap!important;gap:8px!important}
#chat>.mes[is_user]>.mes_block>.mes_text{grid-column:1!important;grid-row:2!important;padding:0 calc(15 * var(--u)) 0 calc(160 * var(--u))!important;min-width:0!important;font-size:clamp(14px,2.8vw,29px)!important;line-height:1.8!important}
#chat>.mes[is_user]>.mes_block>.mes_reasoning_details{grid-column:2!important;grid-row:2!important;position:relative!important;margin:calc(125 * var(--u)) calc(22 * var(--u)) 0 calc(25 * var(--u))!important;padding:12px!important;width:auto!important;max-height:40dvh!important;min-height:calc(180 * var(--u));background:#dce6c9ed!important;border:0!important;border-radius:8px!important;box-shadow:0 2px 3px #4e5d3826}
#chat>.mes[is_user]>.mes_block>:is(.mes_media_wrapper,.mes_file_wrapper,.mes_bias){grid-column:1/-1!important;grid-row:auto!important;min-width:0;max-width:100%;margin:0 6%}
#chat>.mes[is_user]>.mesAvatarWrapper{position:absolute!important;left:calc(152 * var(--u))!important;top:calc(59 * var(--u))!important;width:calc(84 * var(--u))!important;height:calc(84 * var(--u))!important;margin:0!important;display:block!important;z-index:2}
#chat>.mes[is_user]>.mesAvatarWrapper>.avatar{position:static!important;width:100%!important;height:100%!important}
#chat>.mes[is_user]>.mesAvatarWrapper>:is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay){display:none!important}
#chat>.mes[is_user="true"]>.mes_block{display:block!important;min-height:calc(316 * var(--u))!important;padding:calc(55 * var(--u)) calc(190 * var(--u)) 32px calc(415 * var(--u))!important;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/editorial-faithful/orange/reply.webp') left top/100% auto no-repeat,#f8dfb6!important}
#chat>.mes[is_user="true"]>.mes_block>.ch_name{margin:0 0 12px!important;min-height:0!important}
#chat>.mes[is_user="true"]>.mes_block>.mes_text{padding:0!important}
#chat>.mes[is_user="true"]>.mesAvatarWrapper{left:auto!important;right:calc(37 * var(--u))!important;top:calc(59 * var(--u))!important;width:calc(140 * var(--u))!important;height:calc(140 * var(--u))!important}
#chat>.mes[is_user="true"]>.mes_block>.ch_name>.mes_buttons{gap:4px!important}
#chat>.mes[is_user] .mes_edit_buttons{grid-column:1/-1;position:relative!important;inset:auto!important;z-index:10;flex-wrap:wrap}
#chat>.mes[is_user]:has(.edit_textarea)>.mes_block{display:block!important;padding:16px!important}
#chat>.mes[is_user]:has(.edit_textarea)>.mes_block>.ch_name{margin:0!important}
#chat>.mes[is_user]:has(.edit_textarea) .edit_textarea{width:100%!important;box-sizing:border-box;min-height:200px}
#chat::after{content:''!important;display:block;flex:none;width:100%;aspect-ratio:1024/70;height:auto!important;background:url('https://raw.githubusercontent.com/Lumi729/wuli-laixin/main/assets/editorial-faithful/orange/footer.webp') left top/100% auto no-repeat}
/* Keep actual native header; no duplicated DOM or new extension. */
#chat>.mes[is_user="false"]:not([is_system="true"]):not(:has(~.mes[is_user="false"]:not([is_system="true"])))>.mesAvatarWrapper{position:fixed!important;top:0!important;left:0!important;width:100vw!important;height:calc(267 * var(--u))!important;z-index:32!important}
#chat>.mes[is_user="false"]:not([is_system="true"]):not(:has(~.mes[is_user="false"]:not([is_system="true"])))>.mesAvatarWrapper>.avatar{position:absolute!important;left:4.4%!important;top:8.6%!important;width:22.9%!important;height:86.5%!important}
#chat>.mes[is_user="false"]:not([is_system="true"]):not(:has(~.mes[is_user="false"]:not([is_system="true"])))>.mesAvatarWrapper>:is(.mesIDDisplay,.mes_timer,.tokenCounterDisplay){display:block!important}
'''
j['custom_css']+='''
#sheldheader{display:none!important}
#chat{inset:auto!important;margin-top:var(--heading)!important;border:0!important}
#chat>.mes[is_user]{padding-bottom:0!important;margin-bottom:10px!important}
#chat>.mes[is_user]>.mes_block{padding-bottom:calc(24 * var(--u))!important}
#chat>.mes[is_user]>.mes_block>.mes_reasoning_details{margin-top:calc(70 * var(--u))!important;max-height:calc(230 * var(--u))!important;min-height:0!important;background:transparent!important;border-radius:0!important;box-shadow:none!important;font-size:clamp(11px,1.9vw,20px)!important;padding:8px!important}
#chat>.mes[is_user]>.mes_block>.ch_name>.mes_buttons{position:absolute!important;left:calc(-200 * var(--u))!important;top:calc(40 * var(--u))!important;width:calc(60 * var(--u))!important;flex-direction:column!important;gap:4px!important}
#chat>.mes[is_user] .mes_button{font-size:clamp(12px,2.2vw,22px)!important;min-width:20px!important;min-height:20px!important;line-height:20px!important}
#chat>.mes[is_user="true"]>.mes_block>.ch_name>.mes_buttons{position:relative!important;inset:auto!important;width:auto!important;flex-direction:row!important}
#chat>.mes[is_user="true"]>.mes_block{padding-bottom:32px!important}
'''
j['custom_css']+="""
#chat>.mes[is_user]>.mes_block>.ch_name>.mes_buttons>.extraMesButtons{position:absolute!important;left:100%!important;top:0!important;right:auto!important;width:min(240px,70vw)!important;max-width:70vw!important;padding:8px!important;box-sizing:border-box;z-index:80!important;background:var(--paper)!important;box-shadow:0 2px 8px #0003;flex-direction:row!important;flex-wrap:wrap!important}
"""
(R/'theme/Orange-Full-Art.json').write_text(json.dumps(j,ensure_ascii=False,indent=2))
(R/'theme/Orange-Full-Art.css').write_text(j['custom_css'])
